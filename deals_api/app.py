#!/usr/bin/env python3
"""Deal of the Day sold-out service (stdlib only).

GET  /api/deals/status                -> {"date": "YYYY-MM-DD", "hudson": {"sold": bool}, "barboursville": {"sold": bool}}
POST /api/deals/hook/<HOOK_TOKEN>     -> Hostinger mail webhook (message.received on info@). If the new message is a
                                         Mangomint online gift-card notification naming "Hudson" or "Barboursville",
                                         that office's deal is marked sold for today (Eastern time).
GET  /api/deals/admin/<ADMIN_TOKEN>?office=hudson|barboursville&sold=1|0   -> manual override (staff link)
State lives in /data/state.json keyed by date, so every office resets automatically at midnight ET.
"""
import json, os, re, datetime, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DATA = os.environ.get("DATA_DIR", "/data")
HOOK_TOKEN = os.environ["HOOK_TOKEN"]
ADMIN_TOKEN = os.environ["ADMIN_TOKEN"]
OFFICES = ("hudson", "barboursville")
LOCK = threading.Lock()
os.makedirs(DATA, exist_ok=True)

def eastern_today(now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    y = now.year
    # US DST: 2nd Sunday of March 2:00 local (07:00 UTC) -> 1st Sunday of November 2:00 local (06:00 UTC)
    mar = datetime.datetime(y, 3, 8); start = mar + datetime.timedelta(days=(6 - mar.weekday()) % 7, hours=7)
    nov = datetime.datetime(y, 11, 1); end = nov + datetime.timedelta(days=(6 - nov.weekday()) % 7, hours=6)
    off = -4 if start <= now < end else -5
    return (now + datetime.timedelta(hours=off)).date().isoformat()

def load():
    try: return json.load(open(os.path.join(DATA, "state.json")))
    except Exception: return {}

def save(st):
    tmp = os.path.join(DATA, "state.tmp"); json.dump(st, open(tmp, "w")); os.replace(tmp, os.path.join(DATA, "state.json"))

def set_sold(office, sold, source):
    with LOCK:
        st = load(); d = eastern_today()
        day = st.setdefault(d, {o: {"sold": False} for o in OFFICES})
        day[office] = {"sold": bool(sold), "at": datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z", "by": source}
        for k in sorted(st)[:-14]: st.pop(k, None)          # keep two weeks
        save(st)

def status():
    d = eastern_today(); day = load().get(d, {})
    return {"date": d, **{o: {"sold": bool(day.get(o, {}).get("sold"))} for o in OFFICES}}

def log(line):
    # metadata only (no message bodies, no client details)
    line = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z " + line[:300]
    print(line, flush=True)
    with open(os.path.join(DATA, "hook.log"), "a") as f: f.write(line + "\n")

SCHEDULE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "schedule.json")))
API_TOKEN = os.environ.get("HOSTINGER_MAIL_TOKEN", "")      # optional: lets us read the message when the webhook sends only an id
MAILBOX = os.environ.get("HOSTINGER_MAILBOX_ID", "")

def _find_uid(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in ("uid", "messageuid", "message_uid") and isinstance(v, (int, str)): return v
            r = _find_uid(v)
            if r is not None: return r
    if isinstance(obj, list):
        for v in obj:
            r = _find_uid(v)
            if r is not None: return r
    return None

def _fetch_text(uid):
    if not (API_TOKEN and MAILBOX and uid is not None): return ""
    import urllib.request
    req = urllib.request.Request(f"https://api.mail.hostinger.com/api/v1/mailboxes/{MAILBOX}/folders/INBOX/messages/{uid}/text",
                                 headers={"Authorization": "Bearer " + API_TOKEN, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r: return r.read().decode("utf-8", "replace")
    except Exception as e:
        log(f"fetch failed: {type(e).__name__}"); return ""

def classify(payload):
    """Mangomint's internal email: subject 'Online gift card purchase', body '... bought an online gift card ...
    Gift card value: $150.00'. Today's two deals always have different values, so the value picks the office."""
    text = json.dumps(payload, ensure_ascii=False)
    low = text.lower()
    if "gift card" not in low: return None, "not-gift-card"
    if not re.search(r"gift card value", low):
        extra = _fetch_text(_find_uid(payload))
        if extra: text, low = text + " " + extra, (text + " " + extra).lower()
    m = re.search(r"gift card value[^0-9$]*\$?\s*([0-9][0-9,]*(?:\.[0-9]{2})?)", low)
    if not m: return None, "no-value"
    value = float(m.group(1).replace(",", ""))
    today = SCHEDULE.get(eastern_today(), {})
    hits = [o for o, d in today.items() if abs(float(d["value"]) - value) < 0.01]
    if len(hits) == 1: return hits[0], f"value {value:g}"
    return None, f"value {value:g} matches {len(hits)} deals"

class H(BaseHTTPRequestHandler):
    server_version = "serene-deals/1"
    def _send(self, code, obj, ctype="application/json"):
        body = (json.dumps(obj) if ctype == "application/json" else obj).encode()
        self.send_response(code); self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): pass
    def do_GET(self):
        p = self.path.split("?")[0]
        if p in ("/api/deals/status", "/api/deals/status/"): return self._send(200, status())
        if p.rstrip("/") == "/api/deals/admin/" + ADMIN_TOKEN:
            q = dict(kv.split("=", 1) for kv in (self.path.split("?", 1) + [""])[1].split("&") if "=" in kv)
            o = q.get("office")
            if o in OFFICES and q.get("sold") in ("0", "1"):
                set_sold(o, q["sold"] == "1", "admin"); log(f"admin {o} sold={q['sold']}")
            s = status()
            rows = "".join(f"<p><b>{o.title()}</b>: {'SOLD OUT' if s[o]['sold'] else 'available'} &nbsp; "
                           f"<a href='?office={o}&sold=1'>mark sold</a> &middot; <a href='?office={o}&sold=0'>reopen</a></p>" for o in OFFICES)
            return self._send(200, f"<!doctype html><meta name=viewport content='width=device-width'><meta name=robots content=noindex><title>Deal status</title><body style='font:16px system-ui;padding:24px'><h2>Deal of the Day &middot; {s['date']}</h2>{rows}</body>", "text/html")
        return self._send(404, {"error": "not found"})
    def do_POST(self):
        p = self.path.split("?")[0].rstrip("/")
        if p != "/api/deals/hook/" + HOOK_TOKEN: return self._send(404, {"error": "not found"})
        n = int(self.headers.get("Content-Length") or 0); raw = self.rfile.read(min(n, 1_000_000))
        try: payload = json.loads(raw or b"{}")
        except Exception: payload = {"raw": raw.decode("utf-8", "replace")}
        office, why = classify(payload)
        def shape(o, d=0):
            if isinstance(o, dict) and d < 3: return {k: shape(v, d + 1) for k, v in list(o.items())[:25]}
            if isinstance(o, list): return [shape(o[0], d + 1)] if o else []
            return type(o).__name__
        keys = json.dumps(shape(payload))[:280]
        log(f"hook result={office or '-'} ({why}) keys={keys}")
        if office: set_sold(office, True, "mangomint")
        return self._send(200, {"ok": True})

if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), H).serve_forever()
