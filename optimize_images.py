#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""optimize_images.py — generate responsive WebP variants for every raster image the built site references.

Runs where Pillow is available (the Mac). Output goes to assets/webp/ (committed to git) so the VPS build,
which is stdlib-only, just copies the variants and rewrites <img> tags from the manifest (see imgopt.py).

Usage:  python3 optimize_images.py bundle/site          # after gen_site has produced the HTML
        python3 optimize_images.py bundle/site --force  # regenerate everything

Variants: <name>-480.webp, -800.webp, -1200.webp, -1600.webp (never upscaled) next to the original's path
under assets/webp/<same relative path>. Manifest: assets/webp/manifest.json  { "/wp-content/…/x.png": {"w":..,"h":..,"widths":[..],"ext":"webp"} }
Skips SVG/GIF, logos/badges/favicons, and anything under 40 KB (already small).
"""
import os, re, sys, json, time

try:
    from PIL import Image, ImageOps
except ImportError:
    print("optimize_images: Pillow not installed — skipping generation (committed variants will be used)")
    sys.exit(0)

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else "bundle/site"
FORCE = "--force" in sys.argv
OUT = os.path.join(HERE, "assets", "webp")
MANIFEST = os.path.join(OUT, "manifest.json")
WIDTHS = [480, 800, 1200, 1600]
QUALITY = 78
MIN_BYTES = 40 * 1024
SKIP_RX = re.compile(r"/(logos|badges)/|favicon|apple-touch|cropped-Picsart|-\d+x\d+\.(png|jpe?g)$", re.I)

def referenced_images(site):
    refs = set()
    for dp, _, fs in os.walk(site):
        for f in fs:
            if not f.endswith(".html"): continue
            s = open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read()
            for m in re.findall(r'(?:src|href|content)="(/(?:wp-content/uploads|img)/[^"?]+\.(?:jpe?g|png|webp))"', s, re.I): refs.add(m)
            for m in re.findall(r"url\('?(/(?:wp-content/uploads|img)/[^'\")]+\.(?:jpe?g|png|webp))'?\)", s, re.I): refs.add(m)
    return sorted(refs)

def main():
    os.makedirs(OUT, exist_ok=True)
    manifest = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) and not FORCE else {}
    refs = referenced_images(SITE)
    made = kept = skipped = 0
    for url in refs:
        if SKIP_RX.search(url): skipped += 1; continue
        src = os.path.join(SITE, url.lstrip("/"))
        if not os.path.exists(src): continue
        if os.path.getsize(src) < MIN_BYTES and not url.endswith(".webp"): skipped += 1; continue
        stamp = f"{os.path.getsize(src)}:{int(os.path.getmtime(src))}"
        rel = url.lstrip("/")
        base, _ = os.path.splitext(rel)
        ent = manifest.get(url)
        if ent and ent.get("stamp") == stamp and all(os.path.exists(os.path.join(OUT, f"{base}-{w}.webp")) for w in ent["widths"]):
            kept += 1; continue
        try:
            im = Image.open(src); im = ImageOps.exif_transpose(im)
        except Exception as e:
            print("  ! cannot open", url, e); continue
        w0, h0 = im.size
        if im.mode not in ("RGB", "RGBA"): im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        widths = [w for w in WIDTHS if w < w0] + ([w0] if w0 <= WIDTHS[-1] else [])
        widths = sorted(set(widths))
        os.makedirs(os.path.dirname(os.path.join(OUT, base)), exist_ok=True)
        for w in widths:
            dst = os.path.join(OUT, f"{base}-{w}.webp")
            r = im if w == w0 else im.resize((w, max(1, round(h0 * w / w0))), Image.LANCZOS)
            r.save(dst, "WEBP", quality=QUALITY, method=6)
        manifest[url] = {"w": w0, "h": h0, "widths": widths, "stamp": stamp}
        made += 1
        print(f"  {url}  {w0}x{h0} -> {widths}")
    # drop manifest entries no longer referenced
    for k in [k for k in manifest if k not in refs]: manifest.pop(k)
    json.dump(manifest, open(MANIFEST, "w"), indent=0, sort_keys=True)
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print(f"optimize_images: {made} generated, {kept} up to date, {skipped} skipped; {len(manifest)} in manifest; assets/webp = {total/1024/1024:.1f} MB")

if __name__ == "__main__":
    main()
