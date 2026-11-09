#!/usr/bin/env python3
"""Lead relay for serenemedspas.com (stdlib only) — Nov 9 2026.

Why: bots were posting straight to Zoho's public WebToLeadForm using the form codes they scraped from our
HTML (~60 junk "Email signup" leads a day). Now every website lead form (consult form, New Client Special
popup, Obagi pickup cart) posts to /api/lead on our own domain. This service screens the submission and
only then forwards it to Zoho, adding the Zoho form codes itself (config.json, never sent to browsers).
Once Zoho's old public form is retired, posting to Zoho directly no longer works for bots.

POST /api/lead   (application/x-www-form-urlencoded, same field names Zoho expects)
  -> real lead:  forwarded to Zoho; 303 to the form's returnURL (or 200 JSON for background fetches)
  -> bot/junk:   NOT forwarded; same response, so bots learn nothing
GET  /api/lead/health -> {"ok": true, "forwarded": n, "blocked": n}

Never logs names, emails, phones or messages — only counts and the reason a submission was blocked.
"""
import json, os, re, time, threading, urllib.parse, urllib.request, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json")))
ZOHO_URL = CFG.get("zoho_url", "https://crm.zoho.com/crm/WebToLeadForm")
XNQ, XMI = CFG["xnQsjsdp"], CFG["xmIwtLD"]
HOSTS = set(CFG.get("allowed_hosts", ["serenemedspas.com", "www.serenemedspas.com"]))
DEFAULT_RETURN = CFG.get("default_return", "https://serenemedspas.com/thank-you/")
HONEYPOT = "aG9uZXlwb3Q"
RATE_MAX, RATE_WINDOW = int(CFG.get("rate_max", 4)), int(CFG.get("rate_window_sec", 600))
MAX_BODY = 32 * 1024
STATS = {"forwarded": 0, "blocked": 0, "zoho_errors": 0}
LOCK = threading.Lock()
HITS = {}   # ip -> [timestamps]


def log(msg):
    print(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ ") + msg, flush=True)


def host_of(url):
    try:
        return (urllib.parse.urlsplit(url).hostname or "").lower()
    except Exception:
        return ""


def rate_limited(ip):
    now = time.time()
    with LOCK:
        lst = [t for t in HITS.get(ip, []) if now - t < RATE_WINDOW]
        lst.append(now)
        HITS[ip] = lst
        if len(HITS) > 5000:                      # keep memory bounded
            for k in list(HITS)[:2500]:
                HITS.pop(k, None)
        return len(lst) > RATE_MAX


def screen(fields, origin, referer, ip):
    """Return '' to forward, or the reason to block."""
    if fields.get(HONEYPOT, "").strip():
        return "honeypot filled"
    src_host = host_of(origin) or host_of(referer)
    if src_host not in HOSTS:
        return "not sent from our website"
    last = fields.get("Last Name", "").strip()
    if not last:
        return "no last name"
    if last.lower() == "email signup":
        return "email-signup bot pattern"
    email = fields.get("Email", "").strip()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$", email):
        return "no valid email"
    if len(re.sub(r"\D", "", fields.get("Phone", ""))) < 10:
        return "no valid phone"
    if rate_limited(ip):
        return "too many submissions from one address"
    return ""


def forward(fields):
    data = {k: v for k, v in fields.items() if k not in (HONEYPOT, "xnQsjsdp", "xmIwtLD", "g-recaptcha-response")}
    data["xnQsjsdp"], data["xmIwtLD"] = XNQ, XMI
    data.setdefault("actionType", "TGVhZHM=")
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(ZOHO_URL, data=body, method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded",
                                          "User-Agent": "SereneLeadRelay/1.0"})

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(req, timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as e:          # a 3xx lands here because redirects are not followed
        return e.code
    except Exception as e:
        log("zoho forward failed: " + type(e).__name__)
        return 0


class H(BaseHTTPRequestHandler):
    server_version = "SereneLeadRelay"

    def log_message(self, *a):
        pass

    def _ip(self):
        xff = self.headers.get("X-Forwarded-For", "")
        return (xff.split(",")[0].strip() if xff else self.client_address[0])

    def _send(self, code, body=b"", ctype="application/json", location=None):
        self.send_response(code)
        if location:
            self.send_header("Location", location)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        if self.path.rstrip("/") == "/api/lead/health":
            return self._send(200, json.dumps({"ok": True, **STATS}).encode())
        return self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        if self.path.split("?")[0].rstrip("/") != "/api/lead":
            return self._send(404, b'{"error":"not found"}')
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0 or n > MAX_BODY:
            return self._send(400, b'{"error":"bad request"}')
        raw = self.rfile.read(n).decode("utf-8", "replace")
        ctype = (self.headers.get("Content-Type") or "").lower()
        if "application/x-www-form-urlencoded" not in ctype and "text/plain" not in ctype:
            return self._send(415, b'{"error":"unsupported"}')
        fields = {k: v for k, v in urllib.parse.parse_qsl(raw, keep_blank_values=True)}

        ret = fields.get("returnURL", "")
        if host_of(ret) not in HOSTS:
            ret = DEFAULT_RETURN
        reason = screen(fields, self.headers.get("Origin", ""), self.headers.get("Referer", ""), self._ip())
        if reason:
            with LOCK:
                STATS["blocked"] += 1
            log("blocked: " + reason)
        else:
            status = forward(fields)
            ok = 200 <= status < 400
            with LOCK:
                STATS["forwarded" if ok else "zoho_errors"] += 1
            log(("forwarded to Zoho (%s)" if ok else "ZOHO ERROR %s - lead may be lost") % status)

        # Browsers doing a normal form post get sent to the thank-you page; background fetches get JSON.
        if "text/html" in (self.headers.get("Accept") or ""):
            return self._send(303, location=ret)
        return self._send(200, b'{"ok":true}')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    log("lead relay listening on :%d" % port)
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
