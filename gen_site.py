#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_site.py — build the new serenemedspas.com from the WordPress snapshot (mirror/) + hand-authored pages.
Usage: python3 gen_site.py mirror bundle/site
"""
import os, re, sys, shutil, json, html, datetime, hashlib
import extract as X
from site_lib import *
import pages_custom as P

MIRROR = sys.argv[1] if len(sys.argv) > 1 else "mirror"
SITE = sys.argv[2] if len(sys.argv) > 2 else "bundle/site"

# ---------------------------------------------------------------- categories
CATS = [
    ("intimate", "Intimate Wellness", r"p-shot|o-shot|vaginal|labial|sexual|alma-duo|empowerrf|erectile|intimate"),
    ("hair", "Hair Restoration", r"hair-restoration|alma-ted|prp-hair|hair-loss|hair-growth|exosome"),
    ("wellness", "Wellness & Weight", r"\biv\b|iv-|vitamin|hormone|biote|weight|glp|semaglutide|tirzepatide|peptide|nad|longevity|testosterone|hydration|pro-nox|nitrous|telehealth"),
    ("laser", "Laser & Hair Removal", r"laser-hair|diolaze|tattoo|nail-fungus|vein|spider|laser-vein|hair-removal"),
    ("body", "Body Contouring", r"body|contour|evolve|emsculpt|bodytite|fat-|cellulite|slimming|butt|bbl|sculpt"),
    ("injectables", "Injectables", r"botox|dysport|xeomin|daxxify|filler|juvederm|restylane|radiesse|sculptra|kybella|lip|neurotoxin|jawline|cheek|chin|under-eye|thread|pdo|skinvive|belotero|revanesse|hylenex|tear-trough|wrinkle|frown|forehead|crow|hand-filler|cortisone|kenalog"),
    ("skin", "Skin & Facials", r"facial|hydrafacial|peel|microneedling|dermaplaning|prf|prp|skin|acne|pigment|melasma|rosacea|opus|morpheus|forma|resurfacing|photofacial|ipl|moxi|halo|glow|dermal|scar|micro|plasma|rf"),
]
CAT_NAME = dict((k, n) for k, n, _ in CATS)
def categorize(slug, title):
    hay = (slug + " " + title).lower()
    for key, name, rx in CATS:
        if re.search(rx, hay): return key
    return "skin"

# ---------------------------------------------------------------- redirects (also mirrored in bundle/nginx.conf)
REDIRECTS = {
    "/team/": "/our-providers/", "/treatments/": "/service/", "/about/": "/about-us/",
    "/our-providers/robin-arora/": "/our-providers/robin-arora-md/", "/our-providers/stephanie-welker/": "/our-providers/stephanie-welker-fnp-bc/",
    "/locations/locations/": "/locations/", "/locations/ormond-beach/": "/locations/", "/locations/visit-serene-med-spa-in-paintsville-ky/": "/locations/",
    "/locations/huntington-barboursville-wv/": BARB["site"], "/locations/visit-serene-med-spa-in-hudson-oh/": HUDSON["site"],
    "/cosmetic-filler-injectable-treatment-serene-med-spas/": BARB["site"] + "fillers/", "/juvederm-ultra-plus-filler-treatment/": BARB["site"] + "fillers/",
    "/juvederm-ultra-xc-filler-treatment-serene-med-spas/": BARB["site"] + "fillers/", "/top-filler-injection-treatments-serene-med-spas/": BARB["site"] + "fillers/",
    "/juvederm-volbella-xc-treatment-lip-filler-under-eye/": BARB["site"] + "lip-filler/",
}
SKIP_DIRS = {"wp-content", "wp-includes", "wp-json", "wp-admin", "cart", "checkout", "my-account", "login", "logout", "password-reset", "shop", "product", "feed", "_test"}

def write(path, content):
    dst = os.path.join(SITE, path.strip("/"), "index.html") if path != "/" else os.path.join(SITE, "index.html")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w", encoding="utf-8").write(content)

def redirect_page(target):
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{target}"><title>Redirecting…</title></head><body><p>This page has moved to <a href="{target}">{target}</a>.</p></body></html>'

# ---------------------------------------------------------------- inventory
def inventory():
    posts, pages = [], {}
    for root, dirs, files in os.walk(MIRROR):
        rel = os.path.relpath(root, MIRROR)
        top = rel.split(os.sep)[0]
        if top in SKIP_DIRS: dirs[:] = []; continue
        if "index.html" not in files: continue
        slug = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
        if re.match(r"^/\d{4}/", slug): continue                       # date archives -> /blogs/
        if slug in REDIRECTS: continue
        rec = X.load(MIRROR, slug)
        s = rec["raw"]
        bc = re.search(r'<body[^>]*class="([^"]*)"', s); bc = bc.group(1) if bc else ""
        rec["is_post"] = "single-post" in bc
        rec["cat"] = categorize(slug, rec["title"])
        if rec["is_post"]: posts.append(rec)
        else: pages[slug] = rec
    posts.sort(key=lambda r: r["published"] or "", reverse=True)
    return posts, pages

def fmt_date(iso):
    try: return datetime.date.fromisoformat(iso[:10]).strftime("%B %-d, %Y")
    except Exception: return ""

def post_card(r, show_cat=True):
    img = f'<img src="{esc(r["og_image"])}" alt="" loading="lazy">' if r.get("og_image") else ""
    cat = f'<div class="pc-cat">{CAT_NAME[r["cat"]]}</div>' if show_cat else ""
    return f'''<a class="post-card reveal" href="{r["slug"]}">{img}<div class="pc-body">{cat}<h3>{esc(r["title"])}</h3><p>{esc(X.text_of(r["description"], 150) or X.text_of(r["content"], 150))}</p><span class="more">Read more &rsaquo;</span></div></a>'''

# ---------------------------------------------------------------- renderers
def render_post(r, posts):
    body_html = r["content"]
    # drop a leading H1/H2 duplicating the title
    body_html = re.sub(r"^\s*<h[12]>[^<]*</h[12]>", "", body_html)
    related = [p for p in posts if p["cat"] == r["cat"] and p["slug"] != r["slug"]][:3]
    date = fmt_date(r["published"]); mod = fmt_date(r["modified"])
    author = r["author"] or "Serene Med Spa"
    fig = f'<div class="post-fig reveal"><img src="{esc(r["og_image"])}" alt="{esc(r["title"])}" width="1200" height="675"></div>' if r["og_image"] else ""
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": r["title"], "description": r["description"],
                     "image": (SITE_URL + r["og_image"]) if r["og_image"] else None, "datePublished": r["published"], "dateModified": r["modified"] or r["published"],
                     "author": {"@type": "Organization", "name": "Serene Med Spa"}, "publisher": {"@type": "Organization", "name": "Serene Med Spa", "logo": {"@type": "ImageObject", "url": SITE_URL + LOGO}},
                     "mainEntityOfPage": SITE_URL + r["slug"]}, ensure_ascii=False)
    body = f'''<section class="post-hero"><div class="wrap">
  <div class="crumbs"><a href="/">Home</a> &rsaquo; <a href="/service/">Treatments</a> &rsaquo; <a href="/service/#{r["cat"]}">{CAT_NAME[r["cat"]]}</a></div>
  <h1 style="max-width:24ch">{esc(r["title"])}</h1>
  <div class="post-meta" style="margin-top:14px">{CAT_NAME[r["cat"]]}{(' &middot; ' + date) if date else ''}{(' &middot; Updated ' + mod) if mod and mod != date else ''} &middot; Medically reviewed by Robin Arora, MD</div>
  {fig}
</div></section>
<section style="padding-top:20px"><div class="wrap post-wrap">
  <article class="prose">{body_html}
    <p style="margin-top:34px;font-size:.9rem;color:var(--muted)">Individual results vary. This article is educational and is not a substitute for a consultation with a licensed medical provider. Treatments are performed at Serene Med Spa in Hudson, OH and Barboursville, WV under the medical direction of Robin Arora, MD.</p>
  </article>
  <aside class="side">
    <div class="card"><h3>Book a complimentary consultation</h3><p style="font-size:.95rem">Same-week appointments. Choose the office nearest you.</p>
      <a class="btn btn-sm" href="{HUDSON["book"]}" target="_blank" rel="noopener">Hudson, OH</a>
      <a class="btn btn-sm" href="{BARB["book"]}" target="_blank" rel="noopener">Barboursville, WV</a>
      <a class="btn btn-sm btn-outline" href="/telehealth/">Telehealth visit</a></div>
    <div class="card"><h3>Call or text</h3><ul><li>Hudson &middot; <a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a></li><li>Barboursville &middot; <a href="tel:{BARB["tel"]}">{BARB["phone"]}</a></li><li>Telehealth &middot; <a href="tel:{TELE["tel"]}">{TELE["phone"]}</a></li></ul></div>
    <div class="card"><h3>Helpful links</h3><ul><li><a href="/post-care-instructions/">Post-care instructions</a></li><li><a href="/specials/">This month&rsquo;s specials</a></li><li><a href="/financing/">Financing &amp; payment plans</a></li><li><a href="/membership/">Membership</a></li><li><a href="/recommendation-webapp/">Treatment finder</a></li></ul></div>
  </aside>
</div></section>
{('<section class="tint-sand related"><div class="wrap"><div class="section-head"><span class="eyebrow">Keep reading</span><h2>Related treatments</h2></div><div class="grid g3">' + "".join(post_card(p, False) for p in related) + '</div></div></section>') if related else ''}
{book_band()}'''
    return shell(r["slug"], r["title"] + " | Serene Med Spa", r["description"] or X.text_of(body_html, 155), body, og_image=r["og_image"], ld=ld)

def render_service(posts):
    groups = {}
    for p in posts: groups.setdefault(p["cat"], []).append(p)
    order = ["injectables", "skin", "laser", "body", "wellness", "intimate", "hair"]
    nav = '<div class="cat-nav">' + "".join(f'<a href="#{k}">{CAT_NAME[k]}</a>' for k in order if k in groups) + '</div>'
    secs = ""
    for i, k in enumerate(order):
        if k not in groups: continue
        items = sorted(groups[k], key=lambda p: p["title"])
        secs += f'''<section id="{k}" class="{'tint-sand' if i % 2 else ''}" style="padding:56px 0"><div class="wrap"><div class="section-head"><span class="eyebrow">{len(items)} treatments</span><h2>{CAT_NAME[k]}</h2></div><div class="grid g3">{"".join(post_card(p, False) for p in items)}</div></div></section>'''
    body = page_hero("Treatments &amp; services", "Physician-led aesthetics and wellness across two offices and by telehealth. Browse by category, or use the <a href='/recommendation-webapp/'>treatment finder</a> if you&rsquo;re not sure where to start.", [("/", "Home"), (None, "Treatments")], "Hudson, OH &middot; Barboursville, WV") + \
        f'<section style="padding:36px 0 0"><div class="wrap">{nav}<p class="lede" style="font-size:1rem">Location-specific pricing and booking live on each office&rsquo;s site: <a href="{HUDSON["site"]}">Hudson</a> &middot; <a href="{BARB["site"]}">Barboursville</a>.</p></div></section>' + secs + book_band()
    return shell("/service/", "Med Spa Treatments & Services | Serene Med Spa – Hudson, OH & Barboursville, WV",
                 "Every treatment at Serene Med Spa — injectables, skin and laser, body contouring, wellness, intimate health and hair restoration — explained by our physician-led team.", body)

def render_blogs(posts):
    cards = "".join(post_card(p) for p in posts)
    body = page_hero("Serene Journal", f"Treatment guides, pricing explainers and skin-health notes from our physicians and providers. Our newest articles are published on <a href='{BLOG}'>blog.serenemedspas.com</a>.", [("/", "Home"), (None, "Blog")], f"{len(posts)} articles") + \
        f'<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>' + book_band()
    return shell("/blogs/", "Med Spa Blog | Serene Med Spa", "Treatment guides, pricing explainers and skin-health articles from Serene Med Spa in Hudson, OH and Barboursville, WV.", body)

def render_prose(r, path=None, title=None, lede="", eyebrow="", crumbs=None, extra=""):
    """title, lede, eyebrow are HTML (entities allowed); when title is omitted the record title is escaped."""
    path = path or r["slug"]
    title_html = title or esc(r["title"])
    title_txt = X.text_of(title_html)
    content = re.sub(r"^\s*<h[12]>[^<]*</h[12]>", "", r["content"])
    body = page_hero(title_html, lede, crumbs or [("/", "Home"), (None, title_html)], eyebrow) + f'<section><div class="wrap"><article class="prose">{content}{extra}</article></div></section>'
    return shell(path, title_txt + " | Serene Med Spa", r["description"] or X.text_of(content, 155), body, og_image=r.get("og_image"))

def render_embed(r, path=None, title=None, description=None, hero=None, noindex=False):
    """Self-styled block(s) pasted into the WP page -> dropped into the new shell as-is."""
    path = path or r["slug"]
    widgets = X.html_widgets(r["container"])
    inner = "".join(X.widget_body(w) for w in widgets) if widgets else X.simplify(r["container"])
    body = (hero or "") + f'<section class="embed"><div class="wrap">{inner}</div></section>'
    return shell(path, (title or r["title"]) + " | Serene Med Spa", description or r["description"] or X.text_of(inner, 155), body, og_image=r.get("og_image"), noindex=noindex)

# ---------------------------------------------------------------- main
def main():
    if os.path.isdir(SITE): shutil.rmtree(SITE, ignore_errors=True)
    os.makedirs(SITE, exist_ok=True)
    posts, pages = inventory()
    for r in posts: r["content"] = X.simplify(r["container"])
    for r in pages.values(): r["content"] = X.simplify(r["container"])
    print(f"gen_site: {len(posts)} posts, {len(pages)} pages")

    # assets: uploads only (images, pdfs); no plugins/themes/wp-includes
    up_src, up_dst = os.path.join(MIRROR, "wp-content", "uploads"), os.path.join(SITE, "wp-content", "uploads")
    shutil.copytree(up_src, up_dst, ignore=shutil.ignore_patterns("elementor", "*.css", "*.js", "._*", ".DS_Store"))
    css = CSS
    open(os.path.join(SITE, "main.css"), "w", encoding="utf-8").write(css)
    cssv = hashlib.md5(css.encode()).hexdigest()[:8]
    fav = "/wp-content/uploads/2024/05/cropped-Picsart_24-04-29_23-12-11-081-1.png"
    if os.path.exists(os.path.join(SITE, fav.strip("/"))): shutil.copy(os.path.join(SITE, fav.strip("/")), os.path.join(SITE, "favicon.png"))

    out = {}
    # posts
    for r in posts: out[r["slug"]] = render_post(r, posts)
    # generated indexes
    out["/service/"] = render_service(posts)
    out["/blogs/"] = render_blogs(posts)
    # custom pages
    out.update(P.build(pages, posts, render_prose, render_embed))
    # redirects
    for src, dst in REDIRECTS.items(): out[src] = redirect_page(dst)
    for slug, r in pages.items():
        if slug not in out:
            print("gen_site: page without a renderer, falling back to prose:", slug)
            out[slug] = render_prose(r)
    for path, content in out.items():
        write(path, content.replace("%%CSSV%%", cssv))
    print(f"gen_site: wrote {len(out)} pages -> {SITE}")

if __name__ == "__main__":
    main()
