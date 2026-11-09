#!/usr/bin/env python3
"""lead_relay_rewrite.py <built-site-dir> — point every website lead form at our own /api/lead relay
instead of Zoho's public WebToLeadForm (Nov 9 2026; see leadrelay/app.py).

Runs as the LAST build step, over every .html and .js file, so it catches the consult form, the
New Client Special popup (popup.js), the Obagi pickup cart and anything added later. Idempotent.
The same file is copied into serenehudson / serenebarboursville."""
import os, sys

ZOHO = "https://crm.zoho.com/crm/WebToLeadForm"
RELAY = "/api/lead"

root = sys.argv[1] if len(sys.argv) > 1 else "bundle/site"
files = changed = 0
for dp, _, fns in os.walk(root):
    for fn in fns:
        if not fn.endswith((".html", ".js")):
            continue
        p = os.path.join(dp, fn)
        try:
            s = open(p, encoding="utf-8").read()
        except Exception:
            continue
        files += 1
        if ZOHO in s:
            open(p, "w", encoding="utf-8").write(s.replace(ZOHO, RELAY))
            changed += 1
print("lead_relay_rewrite: %d of %d files now post leads to %s" % (changed, files, RELAY))
left = []
for dp, _, fns in os.walk(root):
    for fn in fns:
        if fn.endswith((".html", ".js")):
            p = os.path.join(dp, fn)
            try:
                if ZOHO in open(p, encoding="utf-8").read():
                    left.append(p)
            except Exception:
                pass
if left:
    sys.exit("lead_relay_rewrite: FAILED, still posting to Zoho: %s" % left[:5])
