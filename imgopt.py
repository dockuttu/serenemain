#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""imgopt.py — stdlib-only build step: copy the committed WebP variants (assets/webp/) into the site and rewrite
<img> tags / inline hero backgrounds to use them (srcset + sizes + width/height + lazy/eager + hero preload).

Usage: python3 imgopt.py bundle/site
Variants and manifest are produced by optimize_images.py (needs Pillow; run on the Mac and commit assets/webp/).
Any image without variants in the manifest is left exactly as it was.
"""
import os, re, sys, json, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else "bundle/site"
WEBP = os.path.join(HERE, "assets", "webp")
MANIFEST = os.path.join(WEBP, "manifest.json")

# context -> (sizes attribute, default width, eager?)
CTX = {
    "post-fig": ("(max-width: 960px) 100vw, 1200px", 1200, True),
    "prose":    ("(max-width: 960px) calc(100vw - 32px), 760px", 800, False),
    "card":     ("(max-width: 640px) calc(100vw - 32px), (max-width: 1100px) 50vw, 420px", 800, False),
    "default":  ("(max-width: 960px) 100vw, 800px", 800, False),
}
CARD_HINTS = ("post-card", "arch", "loctile", "provcard", 'class="prov ', "tile", "pc-", "g3", "g4", "g6")

ATTR_RX = re.compile(r'([a-zA-Z-]+)\s*=\s*"([^"]*)"')

def parse_attrs(tag):
    return dict(ATTR_RX.findall(tag))

def build_tag(attrs):
    order = ["src", "srcset", "sizes", "alt", "width", "height", "loading", "decoding", "fetchpriority", "class", "style"]
    keys = [k for k in order if k in attrs] + [k for k in attrs if k not in order]
    return "<img " + " ".join(f'{k}="{attrs[k]}"' for k in keys) + ">"

def variant(url, w):
    base, _ = os.path.splitext(url)
    return f"{base}-{w}.webp"

def context_for(html, pos):
    before = html[max(0, pos - 400):pos]
    if "post-fig" in before[-160:]: return "post-fig"
    if any(h in before[-260:] for h in CARD_HINTS): return "card"
    # inside the article body?
    a = html.rfind('<article class="prose"', 0, pos); e = html.rfind("</article>", 0, pos)
    if a != -1 and a > e: return "prose"
    return "default"

def rewrite(html, manifest):
    preload = None
    out = []; last = 0
    for m in re.finditer(r"<img\b[^>]*>", html):
        tag = m.group(0); attrs = parse_attrs(tag)
        src = attrs.get("src", "").split("?")[0]
        ent = manifest.get(src)
        if not ent:
            continue
        ctx = context_for(html, m.start())
        sizes, default_w, eager = CTX[ctx]
        widths = ent["widths"]
        dw = max([w for w in widths if w <= default_w] or [widths[0]])
        attrs["src"] = variant(src, dw)
        attrs["srcset"] = ", ".join(f"{variant(src, w)} {w}w" for w in widths)
        attrs["sizes"] = sizes
        if "width" not in attrs or "height" not in attrs or ctx == "post-fig":
            attrs["width"] = str(dw); attrs["height"] = str(max(1, round(ent["h"] * dw / ent["w"])))
        if eager:
            attrs.pop("loading", None); attrs["fetchpriority"] = "high"; attrs["decoding"] = "async"
            if not preload: preload = (attrs["srcset"], sizes, attrs["src"])
        else:
            attrs.setdefault("loading", "lazy"); attrs.setdefault("decoding", "async")
        out.append(html[last:m.start()]); out.append(build_tag(attrs)); last = m.end()
    out.append(html[last:])
    html = "".join(out)
    # inline hero backgrounds: url('/img/x.jpg') -> largest webp variant, preloaded
    def bg(m):
        nonlocal preload
        url = m.group(2); ent = manifest.get(url)
        if not ent: return m.group(0)
        v = variant(url, ent["widths"][-1])
        if not preload: preload = (None, None, v)
        return f"url({m.group(1)}{v}{m.group(1)})"
    html = re.sub(r"url\(('?)(/(?:wp-content/uploads|img)/[^'\")]+\.(?:jpe?g|png))\1\)", bg, html)
    if preload and "</head>" in html:
        srcset, sizes, href = preload
        link = (f'<link rel="preload" as="image" href="{href}" imagesrcset="{srcset}" imagesizes="{sizes}" fetchpriority="high">'
                if srcset else f'<link rel="preload" as="image" href="{href}" fetchpriority="high">')
        html = html.replace("</head>", link + "\n</head>", 1)
    return html

def main():
    if not os.path.exists(MANIFEST):
        print("imgopt: no assets/webp/manifest.json — nothing to do"); return
    manifest = json.load(open(MANIFEST))
    # copy variants next to the originals
    n = 0
    for dp, _, fs in os.walk(WEBP):
        for f in fs:
            if not f.endswith(".webp"): continue
            rel = os.path.relpath(os.path.join(dp, f), WEBP)
            dst = os.path.join(SITE, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(dp, f), dst); n += 1
    pages = imgs = 0
    for dp, _, fs in os.walk(SITE):
        for f in fs:
            if not f.endswith(".html"): continue
            p = os.path.join(dp, f); s = open(p, encoding="utf-8", errors="ignore").read()
            t = rewrite(s, manifest)
            if t != s:
                open(p, "w", encoding="utf-8").write(t); pages += 1; imgs += t.count("srcset=") - s.count("srcset=")
    print(f"imgopt: copied {n} variants, rewrote {imgs} images on {pages} pages")

if __name__ == "__main__":
    main()
