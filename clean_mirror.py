#!/usr/bin/env python3
"""clean_mirror.py — copy the WordPress snapshot (mirror/) to bundle/site/, stripping WordPress-only plumbing.

Removes: WP discovery links (api.w.org, EditURI, wlwmanifest, shortlink, oEmbed), the generator meta,
the emoji loader, Jetpack stats, WooCommerce / Ultimate Member / Site Kit / Hostinger Reach scripts and
their inline settings, comment-reply. Re-absolutizes canonical, og:url/og:image, twitter:image and
JSON-LD URLs (the snapshot made every serenemedspas.com URL root-relative). Drops retired dynamic
pages (cart, checkout, my-account, login, logout, password-reset, shop) — nginx redirects them.
Usage: python3 clean_mirror.py mirror bundle/site
"""
import os, re, shutil, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "mirror"
DST = sys.argv[2] if len(sys.argv) > 2 else "bundle/site"
ORIGIN = "https://serenemedspas.com"

DROP_DIRS = {"cart", "checkout", "my-account", "login", "logout", "password-reset", "shop", "feed", "wp-json", "wp-admin"}
DROP_FILES = {"sitemap_index.xml", "page-sitemap.xml", "post-sitemap.xml", "sitemap.xml", "robots.txt", "xmlrpc.php", "wp-login.php"}
# plugin trees whose tags are stripped from every page — no need to ship their assets
DROP_PLUGINS = {"woocommerce", "ultimate-member", "jetpack", "google-site-kit", "hostinger-reach"}

# whole <script ...>...</script> or <script src=...></script> blocks to remove, by pattern on the tag/body
DROP_SCRIPT_PATTERNS = [
    r"/wp-content/plugins/woocommerce/", r"/wp-content/plugins/ultimate-member/", r"/wp-content/plugins/jetpack/",
    r"/wp-content/plugins/google-site-kit/", r"/wp-content/plugins/hostinger-reach/",
    r"stats\.wp\.com", r"_wpemojiSettings", r"wp-emoji", r"wc_add_to_cart_params", r"wc_cart_fragments_params",
    r"woocommerce_params", r"wc_order_attribution", r"/wp-includes/js/comment-reply", r"um_scripts|um_frontend",
    r"_stq\.push", r"wp-polyfill", r"wp-includes/js/dist/hooks", r"wp-includes/js/dist/i18n",
    r"google-site-kit", r"googlesitekit",
]
DROP_LINK_PATTERNS = [
    r'rel=["\']https://api\.w\.org/["\']', r'rel=["\']EditURI["\']', r'rel=["\']wlwmanifest["\']', r'rel=["\']shortlink["\']',
    r'application/json\+oembed', r'text/xml\+oembed', r'rel=["\']alternate["\'][^>]*type=["\']application/rss\+xml',
    r'/wp-content/plugins/woocommerce/', r'/wp-content/plugins/ultimate-member/', r'/wp-content/plugins/google-site-kit/',
    r'/wp-content/plugins/hostinger-reach/', r'/wp-content/plugins/jetpack/', r'dns-prefetch["\'][^>]*s\.w\.org', r'rel=["\']pingback["\']',
]
SCRIPT_RX = re.compile(r"<script\b[^>]*>.*?</script>\s*", re.S | re.I)
LINK_RX = re.compile(r"<link\b[^>]*>\s*", re.I)
META_GEN_RX = re.compile(r'<meta name="generator"[^>]*>\s*', re.I)
STYLE_ID_RX = re.compile(r"<style\b[^>]*id=['\"](?:woocommerce-inline-inline-css|um_styles-inline-css)['\"][^>]*>.*?</style>\s*", re.S | re.I)

def abs_url(m):
    return m.group(1) + ORIGIN + m.group(2) + m.group(3)

def fix_ld(ld):
    ld = re.sub(r'"\\/(?!\\/)', '"https:\\\\/\\\\/serenemedspas.com\\\\/', ld)
    ld = re.sub(r'"/(?!/)', '"https://serenemedspas.com/', ld)
    return ld

def clean_html(s):
    s = META_GEN_RX.sub("", s)
    s = STYLE_ID_RX.sub("", s)
    def drop_script(m):
        blk = m.group(0)
        return "" if any(re.search(p, blk, re.I) for p in DROP_SCRIPT_PATTERNS) else blk
    s = SCRIPT_RX.sub(drop_script, s)
    def drop_link(m):
        blk = m.group(0)
        return "" if any(re.search(p, blk, re.I) for p in DROP_LINK_PATTERNS) else blk
    s = LINK_RX.sub(drop_link, s)
    # re-absolutize URLs that must be absolute
    s = re.sub(r'(<link\s+rel=["\']canonical["\']\s+href=["\'])(/[^"\']*)(["\'])', abs_url, s, flags=re.I)
    s = re.sub(r'(<link\s+rel=["\']alternate["\'][^>]*hreflang[^>]*href=["\'])(/[^"\']*)(["\'])', abs_url, s, flags=re.I)
    s = re.sub(r'(<meta\s+property=["\']og:(?:url|image|image:secure_url|video)["\']\s+content=["\'])(/[^"\']*)(["\'])', abs_url, s, flags=re.I)
    s = re.sub(r'(<meta\s+name=["\']twitter:image["\']\s+content=["\'])(/[^"\']*)(["\'])', abs_url, s, flags=re.I)
    s = re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', lambda m: m.group(1) + fix_ld(m.group(2)) + m.group(3), s, flags=re.S | re.I)
    # WordPress search forms -> home (nginx also 301s ?s=)
    s = re.sub(r'(<form[^>]*role="search"[^>]*action=")([^"]*)(")', r'\1/\3', s)
    return s

def main():
    if os.path.isdir(DST): shutil.rmtree(DST)
    n_html = 0
    for root, dirs, files in os.walk(SRC):
        rel = os.path.relpath(root, SRC)
        top = rel.split(os.sep)[0] if rel != "." else ""
        if top in DROP_DIRS:
            dirs[:] = []; continue
        dirs[:] = [d for d in dirs if not (rel == "." and d in DROP_DIRS)]
        if rel.replace(os.sep, "/") == "wp-content/plugins":
            dirs[:] = [d for d in dirs if d not in DROP_PLUGINS]
        # crawl junk: /<page>/1024/ etc. (WordPress serves the same page for a trailing numeric segment).
        # keep top-level year archives (/2025/...) and everything under wp-content/wp-includes.
        if top not in ("wp-content", "wp-includes") and not (rel == "." or top.isdigit()):
            dirs[:] = [d for d in dirs if not d.isdigit()]
        out_dir = os.path.join(DST, rel) if rel != "." else DST
        os.makedirs(out_dir, exist_ok=True)
        for f in files:
            if f.startswith(".") or "@" in f or (rel == "." and f in DROP_FILES) or f == "MANIFEST.txt":
                continue
            src = os.path.join(root, f); dst = os.path.join(out_dir, f)
            if f.endswith(".html"):
                s = open(src, encoding="utf-8", errors="replace").read()
                open(dst, "w", encoding="utf-8").write(clean_html(s)); n_html += 1
            else:
                shutil.copy2(src, dst)
    print(f"clean_mirror: {n_html} html pages -> {DST}")

if __name__ == "__main__":
    main()
