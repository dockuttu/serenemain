#!/usr/bin/env python3
"""form_guard_inject.py — spam screening for the Zoho lead forms on serenemedspas.com (Oct 7 2026).
Copies form-guard.js into the built site and loads it on every page that has the consult form
(#zf-consult) or the footer newsletter (#zf-news). Idempotent; stdlib only.
Usage: python3 form_guard_inject.py [bundle/site]"""
import glob, hashlib, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = sys.argv[1] if len(sys.argv) > 1 else "bundle/site"
src = os.path.join(HERE, "form-guard.js")
shutil.copyfile(src, os.path.join(BASE, "form-guard.js"))
V = hashlib.sha256(open(src, "rb").read()).hexdigest()[:8]
TAG = '<script src="/form-guard.js?v=%s" defer></script>' % V
n = 0
for p in glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True):
    s = open(p, encoding="utf-8", errors="ignore").read()
    if "</body>" not in s or not ('id="zf-consult"' in s or 'id="zf-news"' in s):
        continue
    if "form-guard.js" in s:
        t = re.sub(r'<script src="/form-guard\.js(\?v=[0-9a-f]+)?" defer></script>', TAG, s)
    else:
        t = s.replace("</body>", TAG + "\n</body>", 1)
    if t != s:
        open(p, "w", encoding="utf-8").write(t); n += 1
print("form_guard_inject: form-guard.js on", n, "page(s)")
