#!/usr/bin/env python3
"""mirror.py — snapshot the live serenemedspas.com (WordPress) into a folder of static files.

Run ON THE MAC (Terminal), stdlib only:
    python3 mirror.py "/Volumes/Extreme SSD/serenemain/site"

Crawls same-host pages + assets (CSS/JS/images/fonts, incl. url() refs inside CSS),
rewrites absolute serenemedspas.com links to root-relative, drops ?ver= cache-busters,
skips WordPress dynamic endpoints (admin, wp-json, feeds, cart/checkout/account, search).
Writes MANIFEST.txt (url -> file/status) next to the site folder.
"""
import os, re, sys, time, urllib.request, urllib.parse, urllib.error, html
from html.parser import HTMLParser

HOST = "serenemedspas.com"
ORIGIN = "https://" + HOST
OUT = next((a for a in sys.argv[1:] if not a.startswith("--")), "site")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36 serene-mirror"
DELAY = 0.15
MAX = 6000
SKIP_EXISTING = "--skip-existing" in sys.argv

SKIP = re.compile(r"(/wp-admin|/wp-login|/wp-json|/xmlrpc|/feed/?$|/feed/|/cart/?|/checkout/?|/my-account|/login/?$|/logout/?$|/password-reset|"
                  r"/comments/|/author/|/tag/|/category/|/page/\d+|\?(?:s|p|page_id|add-to-cart|replytocom|attachment_id|share|wc-ajax)=|/wp-cron|"
                  r"/wp-content/plugins/.*\.php|/\?rest_route|/embed/?$|/trackback|\.php(?:\?|$))", re.I)
ASSET_EXT = re.compile(r"\.(css|js|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|otf|eot|mp4|webm|pdf|json|xml|txt|avif|mp3)(?:\?|$)", re.I)

seen, queue, manifest = set(), [], []

def norm(u, base):
    u = html.unescape(u.strip())
    if not u or u.startswith(("#", "data:", "mailto:", "tel:", "sms:", "javascript:")): return None
    u = urllib.parse.urljoin(base, u)
    u = u.split("#", 1)[0]
    p = urllib.parse.urlsplit(u)
    if p.scheme not in ("http", "https"): return None
    h = p.netloc.lower()
    if h not in (HOST, "www." + HOST): return None
    path = p.path or "/"
    q = p.query
    # drop cache-busters on assets; keep other queries only if not skipped
    if ASSET_EXT.search(path):
        q = ""
    return urllib.parse.urlunsplit(("https", HOST, path, q, ""))

def local_path(u):
    p = urllib.parse.urlsplit(u)
    path = urllib.parse.unquote(p.path)
    if path.endswith("/"): path += "index.html"
    elif not ASSET_EXT.search(path) and "." not in os.path.basename(path): path += "/index.html"
    if p.query: path += "@" + re.sub(r"[^A-Za-z0-9=&._-]", "_", p.query)
    return os.path.join(OUT, path.lstrip("/"))

class LinkParser(HTMLParser):
    def __init__(self, base):
        super().__init__(); self.base = base; self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and "oembed" in (a.get("type") or "") or (a.get("rel") or "") in ("EditURI", "wlwmanifest", "https://api.w.org/"):
            return  # WordPress discovery links: not needed in a static copy
        for k in ("href", "src", "data-src", "poster", "data-bg", "data-background"):
            if a.get(k): self.links.append(a[k])
        if tag == "meta" and (a.get("property") or "").startswith("og:image") and a.get("content"):
            self.links.append(a["content"])
        for k in ("srcset", "data-srcset"):
            if a.get(k):
                for part in a[k].split(","):
                    self.links.append(part.strip().split(" ")[0])
        if a.get("style"):
            for m in CSS_URL.finditer(a["style"]): self.links.append(m.group(1))

CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", re.I)

def fetch(u):
    req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read(), r.geturl()

def rewrite_text(s):
    s = s.replace("https://www." + HOST, "").replace("http://www." + HOST, "")
    s = s.replace("https://" + HOST, "").replace("http://" + HOST, "")
    s = s.replace("https:\\/\\/www." + HOST, "").replace("https:\\/\\/" + HOST, "").replace("http:\\/\\/" + HOST, "")
    s = s.replace("https%3A%2F%2F" + HOST, "")
    # drop ?ver= / ?v= cache-busters on same-site assets
    s = re.sub(r"(\.(?:css|js|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|otf|eot|json|xml))\?(?:ver|v)=[^\"'\s)>&]*", r"\1", s, flags=re.I)
    return s

def enqueue(u):
    if u and u not in seen and not SKIP.search(u) and len(seen) < MAX:
        seen.add(u); queue.append(u)

def run():
    os.makedirs(OUT, exist_ok=True)
    for start in ["/", "/sitemap_index.xml", "/sitemap.xml", "/page-sitemap.xml", "/robots.txt", "/favicon.ico"]:
        enqueue(ORIGIN + start)
    # extra seeds (one path per line) — pages that nothing links to, e.g. /telehealth/
    seeds = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seeds.txt")
    if os.path.exists(seeds):
        for line in open(seeds):
            line = line.strip()
            if line and not line.startswith("#"): enqueue(norm(line, ORIGIN + "/"))
    n = 0
    while queue:
        u = queue.pop(0); n += 1
        lp0 = local_path(u)
        if SKIP_EXISTING and os.path.exists(lp0) and os.path.getsize(lp0) > 0:
            # already mirrored: don't refetch, but still harvest links from the local copy
            if lp0.endswith(".html") or lp0.endswith(".css") or lp0.endswith(".xml"):
                s = open(lp0, encoding="utf-8", errors="replace").read()
                if lp0.endswith(".html"):
                    p = LinkParser(u)
                    try: p.feed(s)
                    except Exception: pass
                    for l in p.links: enqueue(norm(l, u))
                for m in CSS_URL.finditer(s): enqueue(norm(m.group(1), u))
                for m in re.finditer(r"<loc>([^<]+)</loc>", s): enqueue(norm(m.group(1), u))
            continue
        try:
            st, ct, body, final = fetch(u)
        except urllib.error.HTTPError as e:
            manifest.append(f"{e.code}\t{u}"); print(f"[{n}] {e.code} {u}"); continue
        except Exception as e:
            manifest.append(f"ERR\t{u}\t{e}"); print(f"[{n}] ERR {u} {e}"); continue
        lp = local_path(u)
        os.makedirs(os.path.dirname(lp), exist_ok=True)
        if "text/html" in ct:
            s = body.decode("utf-8", "replace")
            p = LinkParser(u);
            try: p.feed(s)
            except Exception: pass
            for l in p.links:
                enqueue(norm(l, u))
            for m in CSS_URL.finditer(s):  # inline style url()
                enqueue(norm(m.group(1), u))
            open(lp, "w", encoding="utf-8").write(rewrite_text(s))
        elif "text/css" in ct or lp.endswith(".css"):
            s = body.decode("utf-8", "replace")
            for m in CSS_URL.finditer(s):
                enqueue(norm(m.group(1), u))
            for m in re.finditer(r"@import\s+['\"]([^'\"]+)['\"]", s):
                enqueue(norm(m.group(1), u))
            open(lp, "w", encoding="utf-8").write(rewrite_text(s))
        elif "xml" in ct and (lp.endswith(".xml") or "sitemap" in u):
            s = body.decode("utf-8", "replace")
            for m in re.finditer(r"<loc>([^<]+)</loc>", s):
                enqueue(norm(m.group(1), u))
            open(lp, "w", encoding="utf-8").write(rewrite_text(s))
        elif "javascript" in ct or lp.endswith(".js"):
            s = body.decode("utf-8", "replace")
            open(lp, "w", encoding="utf-8").write(rewrite_text(s))
        else:
            open(lp, "wb").write(body)
        manifest.append(f"{st}\t{u}\t{os.path.relpath(lp, OUT)}")
        print(f"[{n}/{len(seen)}] {st} {u}")
        time.sleep(DELAY)
    open(os.path.join(os.path.dirname(OUT.rstrip('/')) or ".", "MANIFEST.txt"), "w").write("\n".join(manifest) + "\n")
    print(f"\nDone: {n} URLs fetched -> {OUT}")

if __name__ == "__main__":
    run()
