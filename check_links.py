#!/usr/bin/env python3
"""check_links.py — verify every same-site href/src/srcset/url() in bundle/site resolves to a file.
Prints missing targets (with the referencing page). Exit 1 only if a *page* link (an .html target) is missing;
missing plugin assets are reported but not fatal. Usage: python3 check_links.py bundle/site
"""
import os, re, sys, urllib.parse
SITE = sys.argv[1] if len(sys.argv) > 1 else "bundle/site"
ATTR = re.compile(r'\b(?:href|src|data-src|poster)=["\']([^"\']+)["\']', re.I)
SRCSET = re.compile(r'\b(?:srcset|data-srcset)=["\']([^"\']+)["\']', re.I)
CSSURL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.I)
REDIRECTED = re.compile(r"^/(cart|checkout|my-account|login|logout|password-reset|shop|blog|feed|wp-json|wp-admin)(/|$)")

def exists(path):
    p = os.path.join(SITE, urllib.parse.unquote(path.split("?")[0].split("#")[0]).lstrip("/"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))

missing, pages_missing = {}, 0
for root, dirs, files in os.walk(SITE):
    for f in files:
        if not f.endswith((".html", ".css")): continue
        fp = os.path.join(root, f)
        s = open(fp, encoding="utf-8", errors="replace").read()
        refs = set(ATTR.findall(s)) if f.endswith(".html") else set()
        for m in SRCSET.findall(s):
            for part in m.split(","): refs.add(part.strip().split(" ")[0])
        for m in CSSURL.findall(s): refs.add(m.strip())
        base = "/" + os.path.relpath(root, SITE).replace(os.sep, "/") + "/" if root != SITE else "/"
        for r in refs:
            if not r or r.startswith(("http", "//", "data:", "mailto:", "tel:", "sms:", "#", "javascript:")): continue
            path = r if r.startswith("/") else urllib.parse.urljoin(base if f.endswith(".html") else base + f, r)
            if REDIRECTED.match(path) or exists(path): continue
            missing.setdefault(path, set()).add(os.path.relpath(fp, SITE))
            if path.endswith("/") or path.endswith(".html"): pages_missing += 1
for p, refs in sorted(missing.items()):
    print(f"MISSING {p}  <- {sorted(refs)[0]}{' (+%d)' % (len(refs)-1) if len(refs) > 1 else ''}")
print(f"check_links: {len(missing)} missing targets, {pages_missing} of them page links")
sys.exit(1 if pages_missing else 0)
