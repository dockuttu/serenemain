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
    now = now or datetime.datetime.utcnow()
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
        day[office] = {"sold": bool(sold), "at": datetime.datetime.utcnow().isoformat() + "Z", "by": source}
        for k in sorted(st)[:-14]: st.pop(k, None)          # keep two weeks
        save(st)

def status():
    d = eastern_today(); day = load().get(d, {})
    return {"date": d, **{o: {"sold": bool(day.get(o, {}).get("sold"))} for o in OFFICES}}

def log(line):
    # metadata only (no message bodies, no client details)
    with open(os.path.join(DATA, "hook.log"), "a") as f: f.write(datetime.datetime.utcnow().isoformat() + "Z " + line[:300] + "\n")

def classify(payload):
    """Return 'hudson' / 'barboursville' / None from a webhook payload (subject/snippet fields, whatever Hostinger sends)."""
    flat = json.dumps(payload, ensure_ascii=False)
    low = flat.lower()
    if "mangomint" not in low and "gift card" not in low: return None, "not-mangomint"
    if not re.search(r"gift\s*card", low): return None, "no-gift-card-words"
    has_h, has_b = "hudson deal" in low, "barboursville deal" in low
    if has_h and not has_b: return "hudson", "ok"
    if has_b and not has_h: return "barboursville", "ok"
    return None, "office-not-found"

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
        keys = list(payload.keys()) if isinstance(payload, dict) else type(payload).__name__
        log(f"hook keys={keys} result={office or '-'} ({why})")
        if office: set_sold(office, True, "mangomint")
        return self._send(200, {"ok": True})

if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), H).serve_forever()
