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

# 1b. Site-wide nav fixes: "Choose Location" menu -> the two location sites (not the old WP location pages)
NAV_FIXES = [
    (re.compile(r'href="/locations/huntington-barboursville-wv/"(?=[^>]*class="elementor-sub-item[^"]*"[^>]*>\s*Barboursville, WV)'),
     'href="/barboursville/"'),
    (re.compile(r'href="/locations/visit-serene-med-spa-in-hudson-oh/"(?=[^>]*class="elementor-sub-item[^"]*"[^>]*>\s*Hudson, OH)'),
     'href="/hudson/"'),
]
n_fixed = 0
for root, dirs, files in os.walk(SITE):
    if "index.html" not in files: continue
    fp = os.path.join(root, "index.html")
    s = open(fp, encoding="utf-8", errors="replace").read()
    t = s
    for rx, repl in NAV_FIXES: t = rx.sub(repl, t)
    if t != s:
        open(fp, "w", encoding="utf-8").write(t); n_fixed += 1
print(f"overlays: location menu links fixed on {n_fixed} pages")

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
<p style="margin-top:28px"><a class="g" href="/hudson/">Hudson, OH</a> &middot; <a class="g" href="/barboursville/">Barboursville, WV</a> &middot; <a class="g" href="/telehealth/">Telehealth</a></p>
</div></body></html>''')

# 3. Sitemap from the indexable HTML pages
# <lastmod> only moves when a page's content actually changes (content hash tracked in sitemap_state.json, committed
# with the repo, same scheme as the Hudson/Barboursville builds) — a build-time mtime stamped every page "today".
import hashlib, json, subprocess
_STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitemap_state.json")
try: _state = json.load(open(_STATE_FILE))
except Exception: _state = {}
_new_state = {}
_today = datetime.date.today().isoformat()
def _lastmod(path, html):
    h = re.sub(r"\s+", " ", re.sub(r"\?v=[0-9a-zA-Z]+", "", html))
    h = hashlib.sha1(h.encode("utf-8")).hexdigest()[:16]
    old = _state.get(path)
    if old and old[0] == h: lm = old[1]
    elif old: lm = _today
    else:
        try: lm = subprocess.run(["git", "log", "-1", "--format=%cs"], capture_output=True, text=True, timeout=10).stdout.strip() or _today
        except Exception: lm = _today
    _new_state[path] = [h, lm]
    return lm
urls = []
for root, dirs, files in os.walk(SITE):
    rel = os.path.relpath(root, SITE)
    if rel.split(os.sep)[0] in ("wp-content", "wp-includes"): dirs[:] = []; continue
    if "index.html" in files:
        s = open(os.path.join(root, "index.html"), encoding="utf-8", errors="replace").read()
        if re.search(r'<meta name="robots" content="[^"]*noindex', s, re.I): continue
        path = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
        can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if can and can.group(1).replace(ORIGIN, "") not in (path, ""): continue   # duplicate pointing elsewhere
        if 'http-equiv="refresh"' in s: continue                                  # redirect stub
        urls.append((path, _lastmod(path, s)))
urls.sort()
json.dump(_new_state, open(_STATE_FILE, "w"), indent=0, sort_keys=True)
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p, d in urls:
    sm.append(f"  <url><loc>{ORIGIN}{p}</loc><lastmod>{d}</lastmod></url>")
sm.append("</urlset>")
open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
print(f"overlays: sitemap.xml with {len(urls)} URLs")

# 4. robots.txt
open(os.path.join(SITE, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /wp-content/plugins/\nDisallow: /wp-includes/\nDisallow: /media/guides/\n\nSitemap: {ORIGIN}/sitemap.xml\nSitemap: {ORIGIN}/barboursville/sitemap.xml\nSitemap: {ORIGIN}/hudson/sitemap.xml\n")
print("overlays: robots.txt")
