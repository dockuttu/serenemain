#!/usr/bin/env python3
"""overlays.py — post-snapshot additions to bundle/site: telehealth disclosures, 404 page, sitemap, robots.
Usage: python3 overlays.py bundle/site
"""
import os, re, sys, datetime

SITE = sys.argv[1] if len(sys.argv) > 1 else "bundle/site"
ORIGIN = "https://serenemedspas.com"
HERE = os.path.dirname(os.path.abspath(__file__))

# 1. Telehealth disclosures (LegitScript): insert before "Already a patient?" on /telehealth/
tele = os.path.join(SITE, "telehealth", "index.html")
if os.path.exists(tele):
    s = open(tele, encoding="utf-8").read()
    block = open(os.path.join(HERE, "telehealth-disclosures.html"), encoding="utf-8").read()
    if "Where we offer telehealth" not in s:
        anchor = "<h2>Already a patient?</h2>"
        if anchor in s:
            s = s.replace(anchor, block + "\n" + anchor, 1)
        else:
            s = s.replace('<p class="note">', block + '\n<p class="note">', 1)
        open(tele, "w", encoding="utf-8").write(s)
        print("overlays: telehealth disclosures added")
    else:
        print("overlays: telehealth disclosures already present")
else:
    print("overlays: WARNING /telehealth/ missing from snapshot")

# 2. Branded 404
open(os.path.join(SITE, "404.html"), "w", encoding="utf-8").write('''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="robots" content="noindex, follow">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Page Not Found | Serene Med Spa</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Jost:wght@500;700&display=swap" rel="stylesheet">
<style>body{margin:0;font-family:Jost,Arial,sans-serif;color:#17272C;background:#FBFAF7;display:flex;min-height:100vh;align-items:center;justify-content:center;text-align:center;padding:24px}
h1{font-family:'Cormorant Garamond',Georgia,serif;color:#2A5F6E;font-size:2.6rem;margin:0 0 12px}p{font-size:1.1rem;margin:0 0 22px;color:#3A4C52}
a.b{display:inline-block;background:#3C8296;color:#fff;text-decoration:none;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:14px 26px;margin:4px}
a.g{color:#3C8296;font-weight:700}</style></head><body><div>
<p style="font-size:.85rem;letter-spacing:.18em;text-transform:uppercase;color:#3C8296;font-weight:700">Error 404</p>
<h1>We couldn&rsquo;t find that page</h1>
<p>The page may have moved. Try one of these instead.</p>
<a class="b" href="/">Home</a> <a class="b" href="/service/">Treatments</a> <a class="b" href="/locations/">Locations</a> <a class="b" href="/contact-us/">Contact</a>
<p style="margin-top:28px"><a class="g" href="https://hudson.serenemedspas.com/">Hudson, OH</a> &middot; <a class="g" href="https://barboursville.serenemedspas.com/">Barboursville, WV</a> &middot; <a class="g" href="/telehealth/">Telehealth</a></p>
</div></body></html>''')

# 3. Sitemap from the indexable HTML pages
urls = []
for root, dirs, files in os.walk(SITE):
    rel = os.path.relpath(root, SITE)
    if rel.split(os.sep)[0] in ("wp-content", "wp-includes"): dirs[:] = []; continue
    if "index.html" in files:
        s = open(os.path.join(root, "index.html"), encoding="utf-8", errors="replace").read()
        if re.search(r'<meta name="robots" content="[^"]*noindex', s, re.I): continue
        path = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
        mtime = datetime.date.fromtimestamp(os.path.getmtime(os.path.join(root, "index.html"))).isoformat()
        urls.append((path, mtime))
urls.sort()
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p, d in urls:
    sm.append(f"  <url><loc>{ORIGIN}{p}</loc><lastmod>{d}</lastmod></url>")
sm.append("</urlset>")
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
print(f"overlays: sitemap.xml with {len(urls)} URLs")

# 4. robots.txt
open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /wp-content/plugins/\nDisallow: /wp-includes/\n\nSitemap: {ORIGIN}/sitemap.xml\n")
print("overlays: robots.txt")
