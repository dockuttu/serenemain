#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_site.py — renders serenemedspaky.com (Serene Med Spa Paintsville, KY) as a static site.

Lives as the `paintsville/` subfolder of the serenemain repo and runs from any cwd with stdlib only:

    python3 paintsville/gen_site.py [out_dir]     # default out_dir = <repo>/bundle/paintsville/site

Everything is resolved relative to this script: imports (site_lib, content, check_site) and assets/.
Images are copied verbatim — the 800px srcset variants are pre-generated and committed under assets/img/800/
(Pillow is optional: if present and a variant is missing it is created, otherwise the step is skipped).
QA (check_site.py) runs at the end; problems are printed to stderr as warnings and never fail the build,
because the main site's deploy runs under `set -e`.
"""
import os, sys, json, shutil, hashlib, datetime, re
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
from site_lib import *
import site_lib as L
import content as C

ROOT = HERE
ASSETS = os.path.join(HERE, "assets", "img")
_args = [a for a in sys.argv[1:] if not a.startswith("-")]
OUT = os.path.abspath(_args[0]) if _args else os.path.normpath(os.path.join(HERE, "..", "bundle", "paintsville", "site"))
TODAY = datetime.date.today().isoformat()
PAGES = {}   # path -> html for sitemap + QA


# ================================================================== helpers
def write(path, html):
    """path like '/forma/' -> bundle/site/forma/index.html ; '/404.html' -> bundle/site/404.html"""
    if path.endswith("/"):
        fp = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    else:
        fp = os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f: f.write(html)
    PAGES[path] = html

def paras(txt): return "".join(f"<p>{p}</p>" for p in txt.split("\n\n"))

def cta_row(outline_href="/pricing/", outline_label="See pricing"):
    return f'<div class="actions"><a class="btn" href="{BOOK_URL}" target="_blank" rel="noopener">Book Online</a><a class="btn btn-outline" href="{outline_href}">{outline_label}</a></div>'

def service_ld(s):
    offers = [{"@type": "Offer", "name": text_of(l), "price": re.sub(r"[^\d.]", "", p.split("&ndash;")[0].split("/")[0]) or "0", "priceCurrency": "USD",
               "description": text_of(n) if n else None, "url": SITE_URL + f"/{s['slug']}/", "availability": "https://schema.org/InStock"} for l, p, n in s["prices"]]
    for o in offers:
        if o["description"] is None: del o["description"]
    return {"@context": "https://schema.org", "@type": "MedicalProcedure", "@id": SITE_URL + f"/{s['slug']}/#procedure", "name": text_of(s["name"]),
            "alternateName": s["procedure"], "procedureType": "https://schema.org/NoninvasiveProcedure", "bodyLocation": s["body"],
            "description": s["description"], "url": SITE_URL + f"/{s['slug']}/", "image": SITE_URL + s["og"],
            "howPerformed": text_of(" ".join(h + ": " + p for h, p in s["expect"])),
            "provider": {"@id": ORG_ID}, "offers": offers}

def medical_webpage(path, title, desc):
    d = webpage_ld(path, title, desc, "MedicalWebPage")
    d["lastReviewed"] = TODAY
    d["reviewedBy"] = {"@type": "Person", "name": "Robin Arora, MD, MBA", "jobTitle": "Medical Director"}
    return d


# ================================================================== pages
def home():
    trust = '<div class="trust"><div class="wrap"><span>Board-certified NP</span><span>Physician medical director</span><span>InMode technology</span><span>Biote Certified</span></div></div>'
    arches = "".join(f'<a class="arch reveal" href="/{slug}/">{img(im, C.BY_SLUG[slug]["hero_alt"] if im == C.BY_SLUG[slug]["hero"] else text_of(label) + " at Serene Med Spa Paintsville", sizes="(max-width:560px) 50vw, 25vw")}<span>{label}</span></a>' for slug, im, label in C.HOME_ARCHES)
    hl = [("Botox&reg;", "$10 / unit", "/botox-xeomin/"), ("Xeomin&reg;", "$9 / unit", "/botox-xeomin/"), ("Dysport&reg;", "$4 / unit", "/botox-xeomin/"), ("Laser hair removal", "from $75", "/laser-hair-removal/"),
          ("Lumecca IPL", "$150", "/lumecca-ipl/"), ("VI Peel", "from $250", "/vi-peel/"), ("Morpheus8 Body", "$600", "/morpheus8/"),
          ("Myers&rsquo; Cocktail IV", "$175", "/iv-therapy/")]
    highlights = "".join(f'<a class="card reveal" href="{h}"><span class="state">Regular rate</span><h3 style="font-size:1.15rem;margin-top:6px">{n}</h3><span class="price">{p}</span><span class="more">Details &rsaquo;</span></a>' for n, p, h in hl)
    review_link = GBP_REVIEW_URL if GBP_REVIEW_URL != "TODO" else "/contact/#review"
    body = f'''<section class="hero"><div class="wrap">
  <div class="hero-copy"><span class="eyebrow">Now open &middot; Paintsville, Kentucky</span><span class="script">Welcome to</span><h1>Serene Med Spa Paintsville</h1>
  <p class="lede">Physician-directed aesthetics and wellness in the heart of Johnson County &mdash; Botox&reg; and Xeomin&reg;, InMode laser and radiofrequency treatments, women&rsquo;s wellness, hormone therapy and IV therapy, all with Katrina Watkins, NP.</p>
  <div class="hero-cta"><a class="btn btn-lav" href="{BOOK_URL}" target="_blank" rel="noopener">Book Online</a><a class="btn btn-ghost" href="/pricing/">See Pricing</a></div>
  <div class="hero-chips"><span class="chip">Botox $10 / unit</span><span class="chip">Xeomin $9 / unit</span><span class="chip">Dysport $4 / unit</span><span class="chip">Laser hair removal from $75</span><span class="chip">Complimentary consults</span></div></div>
  <div class="hero-fig">{img("/img/katrina-optimas.jpg", "Katrina Watkins, NP with the InMode Optimas platform at Serene Med Spa Paintsville, KY", lazy=False, sizes="(max-width:900px) 100vw, 45vw")}<div class="tag"><span>Your provider</span><b>Katrina Watkins, NP</b></div></div>
</div></section>
{trust}
<section><div class="wrap"><div class="section-head center"><span class="eyebrow">Treatments</span><h2>What we do in Paintsville</h2><p class="lede">A focused menu of treatments that work, delivered with medical-grade InMode technology and a conservative, natural-results philosophy. <a href="/services/">See every treatment &rsaquo;</a></p></div>
<div class="grid g4">{arches}</div></div></section>
<section class="tint-sand" id="katrina"><div class="wrap"><div class="prov reveal">{img(C.KATRINA["img"], C.KATRINA["alt"], sizes="(max-width:900px) 100vw, 40vw")}<div class="pbody"><span class="eyebrow">Meet your provider</span><h2 style="font-size:2rem">Katrina Watkins, NP</h2><ul class="creds">{"".join(f"<li>{c}</li>" for c in C.KATRINA["creds"])}</ul><p class="lede" style="font-size:1.02rem">{C.KATRINA["bio"].split(chr(10)+chr(10))[0]}</p>
<div class="actions"><a class="btn btn-sm" href="/about/">Meet the team</a><a class="btn btn-sm btn-outline" href="{BOOK_URL}" target="_blank" rel="noopener">Book with Katrina</a></div></div></div>
<div class="grid g3" style="margin-top:28px">
  <div class="card reveal"><h3>Physician-directed</h3><p>Every protocol is set and supervised by Robin Arora, MD, MBA &mdash; board-certified physician, founder of Serene Med Spa and a Biote Certified Provider.</p><a class="more" href="/about/#dr-arora">About Dr. Arora &rsaquo;</a></div>
  <div class="card reveal"><h3>Honest, natural results</h3><p>We start conservatively, tell you what will and won&rsquo;t work, and never sell you a treatment you don&rsquo;t need. Complimentary consultations, always.</p><a class="more" href="/services/">Our treatments &rsaquo;</a></div>
  <div class="card reveal"><h3>Close to home</h3><p>No more driving to Lexington or Huntington. Serving Paintsville, Prestonsburg, Pikeville, Salyersville, Louisa and all of Eastern Kentucky from Broadway Street.</p><a class="more" href="/contact/">Directions &rsaquo;</a></div>
</div></div></section>
<section id="pricing"><div class="wrap"><div class="section-head"><span class="eyebrow">Transparent pricing</span><h2>Straightforward rates, no surprises</h2><p class="lede">Every price is published. {C.PRICE_NOTE}</p></div>
<div class="grid g4">{highlights}</div><p style="margin-top:26px"><a class="btn btn-outline" href="/pricing/">See the full price list</a></p></div></section>
<section class="tint-sage"><div class="wrap band flip">{img("/img/katrina-empowerrf.jpg", C.BY_SLUG["intimate-wellness"]["hero_alt"], sizes="(max-width:900px) 100vw, 40vw")}
<div><span class="eyebrow">Women&rsquo;s wellness &middot; EmpowerRF</span><h2>Intimate &amp; pelvic wellness, handled with care</h2><p class="lede">Bladder leaks, pelvic-floor weakness after childbirth, dryness and laxity are common &mdash; and treatable without surgery. VTone, FormaV and Morpheus8V in private, unhurried appointments with Katrina.</p>
<div class="actions"><a class="btn" href="/intimate-wellness/">Learn more</a><a class="btn btn-outline" href="{BOOK_URL}" target="_blank" rel="noopener">Book a private consult</a></div>
<p class="fine" style="margin-top:18px">{C.BY_SLUG["intimate-wellness"]["disclaimer"]}</p></div></div></section>
<section><div class="wrap"><div class="section-head"><span class="eyebrow">Feel as good as you look</span><h2>Hormone &amp; IV wellness</h2></div>
<div class="grid g2">
  <a class="card reveal" href="/hormone-therapy/"><img src="/img/logos/biote-dark.png" alt="Biote" width="120" height="40" loading="lazy" style="height:40px;width:auto;margin-bottom:14px"><h3>Biote hormone pellet therapy</h3><p>Lab-guided bioidentical testosterone and estrogen pellets for women and men, with dosing approved by our physician medical director. Pellets $675 &middot; labs $125.</p><span class="more">Hormone therapy &rsaquo;</span></a>
  <a class="card reveal" href="/iv-therapy/"><h3 style="margin-top:54px">IV therapy &mdash; Myers&rsquo; Cocktail</h3><p>B vitamins, vitamin C, magnesium and calcium in a relaxing 45-minute infusion for energy, immunity and recovery. $175.</p><span class="more">IV therapy &rsaquo;</span></a>
</div></div></section>
{logos_strip()}
<section class="tint-sand" id="reviews"><div class="wrap"><div class="section-head center"><span class="eyebrow">Reviews</span><h2>Be our first Google review</h2><p class="lede">Serene Paintsville is brand new, and we would love to hear how your visit went. Our Hudson and Barboursville offices are 5-star rated on Google &mdash; we intend to earn the same here.</p></div>
<div class="grid g3">
  <div class="rev reveal"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>Your review could be here. After your visit, tell Paintsville what you thought.</p><div class="who">&mdash; You</div></div>
  <div class="rev reveal"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>We read every review and reply personally.</p><div class="who">&mdash; Katrina &amp; the Serene team</div></div>
  <div class="rev reveal"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>See what patients say about Serene at our other offices.</p><div class="who"><a href="https://serenemedspas.com/reviews/" target="_blank" rel="noopener">serenemedspas.com/reviews</a></div></div>
</div><p style="text-align:center;margin-top:28px"><a class="btn" href="{review_link}" {'target="_blank" rel="noopener"' if review_link.startswith("http") else ""}>Leave a Google review</a></p></div></section>
<section id="location"><div class="wrap"><div class="section-head"><span class="eyebrow">Visit us</span><h2>On Broadway in downtown Paintsville</h2></div>
<div class="loc reveal"><div class="loc-body"><span class="state">Kentucky</span><h3 style="margin-top:6px">Serene Med Spa &mdash; Paintsville</h3>
<dl><dt>Address</dt><dd>{ADDR1}<br>{ADDR2}</dd><dt>Phone</dt><dd><a href="{tel_href()}">{PHONE}</a></dd><dt>Hours</dt><dd>{HOURS}</dd><dt>Serving</dt><dd style="font-weight:400;font-size:.95rem;color:var(--ink-soft)">Paintsville, Johnson County, Prestonsburg, Pikeville, Salyersville, Louisa, Ashland and Eastern Kentucky</dd></dl>
<div class="actions"><a class="btn btn-sm" href="{BOOK_URL}" target="_blank" rel="noopener">Book online</a><a class="btn btn-sm btn-outline" href="{MAP_LINK}" target="_blank" rel="noopener">Directions</a><a class="btn btn-sm btn-outline" href="/contact/">Contact</a></div></div>
<iframe class="map" src="{MAP_EMBED}" title="Map to Serene Med Spa, {ADDR1}, {ADDR2}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></section>
{book_band()}'''
    title = "Serene Med Spa Paintsville, KY | Botox, Laser & Wellness"
    desc = "Physician-directed med spa in Paintsville, KY: Botox $10/unit, Xeomin $9, Dysport $4, laser hair removal, VI Peel, Morpheus8, Biote hormones, IV therapy."
    write("/", shell("/", title, desc, body, og_image="/img/katrina-optimas.jpg", ld=[webpage_ld("/", title, desc)]))


def service_page(s):
    path = f"/{s['slug']}/"
    crumbs = [("/", "Home"), ("/services/", "Treatments"), (None, s["name"])]
    treats = "".join(f"<li>{t}</li>" for t in s["treats"])
    steps = "".join(f'<div class="step"><b></b><div><h4>{h}</h4><p>{p}</p></div></div>' for h, p in s["expect"])
    disc = f'<div class="disclaim">{s["disclaimer"]}</div>' if s.get("disclaimer") else ""
    glance = s["prices"] if len(s["prices"]) <= 6 else s["prices"][:5]
    more = f'<p style="margin-top:10px"><a href="#pricing" class="more" style="font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;font-weight:600">See all {len(s["prices"])} areas &darr;</a></p>' if len(s["prices"]) > 6 else ""
    body = page_hero(s["h1"], s["lede"], crumbs, s["eyebrow"], image=s["hero"], alt=s["hero_alt"], price=s["price_pill"]) + f'''
<section><div class="wrap band top"><div class="prose"><span class="eyebrow">What it is</span><h2 style="margin-top:0">About {s["name"]}</h2>{"".join(f"<p>{p}</p>" for p in s["what"])}{disc}</div>
<div><div class="card" style="background:var(--grey);border-color:transparent"><span class="eyebrow">At a glance</span><h3>Regular rates</h3>{price_table(glance, note=False, caption=text_of(s["name"]) + " pricing")}{more}<p class="fine" style="margin:12px 0 18px">{C.PRICE_NOTE}</p>{cta_row("/specials/", "Current specials")}</div></div></div></section>
<section class="tint-sand"><div class="wrap"><div class="section-head"><span class="eyebrow">What it treats</span><h2>Is {s["name"]} right for you?</h2><p class="lede">Common concerns we treat with {s["name"]} at our Paintsville office. A consultation confirms candidacy and sets realistic expectations.</p></div><ul class="checks">{treats}</ul></div></section>
<section><div class="wrap band top"><div class="steps">{steps}</div><div style="position:sticky;top:130px"><span class="eyebrow">What to expect</span><h2>Your visit, step by step</h2><p class="lede">Every treatment at Serene Paintsville is performed by Katrina Watkins, NP, following protocols set by our physician medical director, Robin Arora, MD.</p>{cta_row()}</div></div></section>
<section id="pricing"><div class="wrap narrow"><div class="section-head"><span class="eyebrow">Pricing</span><h2>{s["name"]} pricing in Paintsville</h2></div>{price_table(s["prices"], caption=text_of(s["name"]) + " price list")}</div></section>
{faq_section(s["faqs"], f"{s['name']} FAQs")}
{also_offered([C.BY_SLUG[a] for a in s["also"]], s["slug"])}
{book_band(f"Book {text_of(s['name'])} in Paintsville")}'''
    ld = [service_ld(s), faq_ld(s["faqs"]), medical_webpage(path, re.sub(r"\s*\|.*$", "", s["title"]), s["description"])]
    write(path, shell(path, s["title"], s["description"], body, og_image=s["og"], ld=ld, crumbs=crumbs))


def services():
    path = "/services/"
    crumbs = [("/", "Home"), (None, "Treatments")]
    groups = [("Face &amp; skin", ["botox-xeomin", "vi-peel", "forma", "lumecca-ipl", "morpheus8"]), ("Body &amp; laser", ["laser-hair-removal", "evolvex", "intimate-wellness"]), ("Wellness", ["hormone-therapy", "iv-therapy"])]
    secs = ""
    for i, (g, slugs) in enumerate(groups):
        cards = "".join(f'<a class="card reveal" href="/{sl}/">{img(C.BY_SLUG[sl]["hero"], C.BY_SLUG[sl]["hero_alt"], sizes="(max-width:900px) 100vw, 33vw")}<h3 style="margin-top:18px">{C.BY_SLUG[sl]["name"]}</h3><p>{C.BY_SLUG[sl]["short"]}</p><span class="price" style="font-size:1.2rem">{C.BY_SLUG[sl]["price_pill"][0]}</span><span class="more">Learn more &rsaquo;</span></a>' for sl in slugs)
        secs += f'<section class="{"tint-sand" if i % 2 else ""}" id="{re.sub(r"[^a-z]", "", text_of(g).lower())}"><div class="wrap"><div class="section-head"><h2>{g}</h2></div><div class="grid g3">{cards}</div></div></section>'
    body = page_hero("Med Spa Treatments in Paintsville", "Injectables, InMode laser and radiofrequency, women&rsquo;s wellness, hormones and IV therapy &mdash; a focused menu delivered by Katrina Watkins, NP, under physician direction. Complimentary consultations for every treatment.", crumbs, "Everything we offer") + secs + f'''
<section><div class="wrap narrow prose"><h2 style="margin-top:0">Not sure where to start?</h2><p>Book a complimentary consultation. Katrina will listen to what bothers you, look at your skin and health history, and recommend a plan &mdash; sometimes a single treatment, sometimes a combination like Lumecca plus Forma, and sometimes nothing at all yet. Patients visit us from Paintsville, Prestonsburg, Pikeville, Salyersville, Louisa, Ashland and across Eastern Kentucky.</p>{cta_row()}</div></section>
{book_band()}'''
    title = "Med Spa Treatments in Paintsville, KY | Serene Med Spa"
    desc = "All treatments at Serene Med Spa Paintsville, KY: Botox and Xeomin, laser hair removal, Lumecca IPL, Forma, EvolveX, Morpheus8, EmpowerRF, hormones and IV."
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE_URL + path, "name": "Med Spa Treatments in Paintsville", "description": desc, "about": {"@id": ORG_ID},
           "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": text_of(s["name"]), "url": SITE_URL + f"/{s['slug']}/"} for i, s in enumerate(C.SERVICES)]}}]
    write(path, shell(path, title, desc, body, ld=ld, crumbs=crumbs))


def packages_block(heading="Save with a package"):
    """Prepaid Vagaro packages + gift cards, bought online. Used on /pricing/ and /specials/."""
    cards = "".join(f'<div class="card reveal"><span class="eyebrow">Package</span><h3 style="font-size:1.25rem">{n}</h3>'
                    f'<p><span class="price" style="font-size:1.4rem">{p}</span> <span class="fine" style="text-decoration:line-through">{reg}</span></p><p>{note}</p>'
                    f'<a class="btn btn-sm" href="{PACKAGES_URL}" target="_blank" rel="noopener">Buy online</a></div>' for n, p, reg, note in C.PACKAGES)
    gift = (f'<div class="card reveal"><span class="eyebrow">Gift cards</span><h3 style="font-size:1.25rem">Give a Serene gift card</h3>'
            f'<p>Any amount, delivered by email or printed at home, good for every treatment in Paintsville. Gift cards never expire.</p>'
            f'<a class="btn btn-sm" href="{GIFT_URL}" target="_blank" rel="noopener">Buy a gift card</a></div>')
    return (f'<div class="reveal" id="packages" style="margin:8px 0 44px"><h2 style="font-size:1.6rem;margin-bottom:8px">{heading}</h2>'
            f'<p class="lede" style="font-size:1rem">Prepay for a series and save. Buy online through our secure Vagaro checkout (pay over time with Affirm), or at the front desk.</p>'
            f'<div class="grid g2" style="margin-top:18px">{cards}{gift}</div>'
            f'<p class="fine" style="margin-top:12px">Package prices can&rsquo;t be combined with other discounts. Packages are non-refundable but transferable to a friend or family member, and expire 12 months from purchase.</p></div>')


def pricing():
    path = "/pricing/"
    crumbs = [("/", "Home"), (None, "Pricing")]
    secs = ""
    for i, (g, link, rows) in enumerate(C.PRICES):
        more = f'<p style="margin-top:14px"><a class="more" href="{link}" style="font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;font-weight:600">About this treatment &rsaquo;</a></p>' if link else ""
        secs += f'<div class="reveal" id="{re.sub(r"[^a-z0-9]+", "-", text_of(g).lower()).strip("-")}" style="margin-bottom:44px"><h2 style="font-size:1.6rem;margin-bottom:16px">{g}</h2>{price_table(rows, note=False, caption=text_of(g) + " prices")}{more}</div>'
    body = page_hero("Med Spa Pricing in Paintsville", "Every regular rate at our Paintsville office, published. " + C.PRICE_NOTE + " Complimentary consultations; your total is confirmed before any treatment.", crumbs, "Transparent pricing") + f'''
<section><div class="wrap narrow">{secs}{packages_block()}
<div class="disclaim">All prices are regular rates in US dollars and may change. Current specials may apply &mdash; see <a href="/specials/">specials</a> or ask us. Unit counts, areas and number of sessions are determined at your consultation; the treatment plan and total cost are confirmed with you before anything is done. Individual results vary.</div>
{cta_row("/specials/", "Current specials")}</div></section>
{book_band("Ready to book?", "Prices are confirmed at your complimentary consultation. Book online through Vagaro or call the Paintsville clinic.")}'''
    title = "Med Spa Prices in Paintsville, KY | Serene Med Spa"
    desc = "Full price list for Serene Med Spa Paintsville, KY: Botox $10/unit, Xeomin $9, Dysport $4, filler $550, VI Peel $250, laser hair removal from $75."
    offers = [{"@type": "Offer", "name": text_of(l), "price": re.sub(r"[^\d.]", "", p.split("&ndash;")[0].split("/")[0]) or "0", "priceCurrency": "USD", "category": text_of(g)} for g, _, rows in C.PRICES for l, p, n in rows]
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "url": SITE_URL + path, "name": "Med Spa Pricing in Paintsville", "description": desc, "about": {"@id": ORG_ID},
           "mainEntity": {"@type": "OfferCatalog", "name": "Serene Med Spa Paintsville price list", "itemListElement": offers}}]
    write(path, shell(path, title, desc, body, ld=ld, crumbs=crumbs))


def about():
    path = "/about/"
    crumbs = [("/", "Home"), (None, "About")]
    def prov(p, flip=False):
        return f'''<div class="prov reveal" id="{p["id"]}" style="{'direction:rtl' if flip else ''}">{img(p["img"], p["alt"], sizes="(max-width:900px) 100vw, 40vw")}<div class="pbody" style="direction:ltr"><span class="eyebrow">{p["role"]}</span><h2 style="font-size:2rem">{p["name"]}</h2><ul class="creds">{"".join(f"<li>{c}</li>" for c in p["creds"])}</ul>{paras(p["bio"])}</div></div>'''
    body = page_hero("About Serene Med Spa Paintsville", "Part tranquil spa, part advanced medical-aesthetics clinic &mdash; physician-directed care in downtown Paintsville, Kentucky, led by nurse practitioner Katrina Watkins and founded by Robin Arora, MD.", crumbs, "Meet the team", image="/img/katrina-headshot.jpg", alt=C.KATRINA["alt"]) + f'''
<section><div class="wrap" style="display:grid;gap:28px">{prov(C.KATRINA)}{prov(C.DR_ARORA, flip=True)}</div></section>
<section class="tint-sand"><div class="wrap band"><div class="prose"><span class="eyebrow">Our story</span><h2 style="margin-top:0">Serene comes to Eastern Kentucky</h2>
<p>Serene Med Spa was founded by Dr. Robin Arora on a simple belief: good aesthetic care shouldn&rsquo;t require choosing between a clinical setting and a comfortable one. That idea grew from a first office in Hudson, Ohio, to Barboursville, West Virginia &mdash; and now to Paintsville, Kentucky, where Katrina Watkins, NP, brings the same physician-directed standards to Johnson County and the surrounding communities of Prestonsburg, Pikeville, Salyersville, Louisa and Ashland.</p>
<p>We use only medical-grade technology &mdash; the InMode Optimas, EmpowerRF and EvolveX platforms, Morpheus8, Botox&reg; and Xeomin&reg;, and Biote hormone optimization &mdash; and every treatment plan is customized to you. Never a menu of upsells.</p>
<p>Our mission is exceptional care in a peaceful setting, with results you can see and feel.</p>{cta_row("/services/", "Our treatments")}</div>
<div>{img("/img/katrina-evolvex.jpg", C.BY_SLUG["evolvex"]["hero_alt"], sizes="(max-width:900px) 100vw, 40vw")}</div></div></section>
{logos_strip("Our technology")}
{book_band()}'''
    title = "About Serene Med Spa Paintsville | Katrina Watkins, NP"
    desc = "Meet Katrina Watkins, NP, lead provider at Serene Med Spa Paintsville, KY, and medical director Robin Arora, MD. Physician-directed care in Eastern KY."
    ld = [{"@context": "https://schema.org", "@type": "AboutPage", "url": SITE_URL + path, "name": "About Serene Med Spa Paintsville", "description": desc, "mainEntity": {"@id": ORG_ID}},
          {"@context": "https://schema.org", "@type": "Person", "@id": SITE_URL + "/about/#katrina", "name": "Katrina Watkins, NP", "jobTitle": "Nurse Practitioner", "worksFor": {"@id": ORG_ID}, "image": SITE_URL + C.KATRINA["img"], "url": SITE_URL + "/about/#katrina",
           "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "Board-certified Nurse Practitioner"}], "knowsAbout": ["aesthetic medicine", "injectables", "laser hair removal", "radiofrequency skin tightening", "women's wellness", "hormone therapy"]},
          {"@context": "https://schema.org", "@type": ["Person", "Physician"], "@id": SITE_URL + "/about/#dr-arora", "name": "Robin Arora, MD, MBA", "jobTitle": "Founder & Medical Director", "worksFor": {"@id": ORG_ID}, "image": SITE_URL + C.DR_ARORA["img"], "url": SITE_URL + "/about/#dr-arora",
           "alumniOf": {"@type": "CollegeOrUniversity", "name": "Tulane University (Nephrology fellowship)"},
           "hasCredential": [{"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": n} for n in ["Board Certified, Internal Medicine (ABIM)", "Board Certified, Nephrology (ABIM)", "Biote Certified Provider"]]}]
    write(path, shell(path, title, desc, body, og_image="/img/katrina-headshot.jpg", ld=ld, crumbs=crumbs))


def contact():
    path = "/contact/"
    crumbs = [("/", "Home"), (None, "Contact")]
    if JOTFORM_ID and JOTFORM_ID != "TODO":
        form = f'<div class="jf"><iframe src="https://form.jotform.com/{JOTFORM_ID}" title="Contact Serene Med Spa Paintsville" loading="lazy" allow="geolocation; microphone; camera"></iframe></div><p class="fine" style="margin-top:10px">Please don&rsquo;t include private medical details in this form &mdash; we&rsquo;ll gather anything clinical securely at your visit.</p>'
    else:
        form = f'''<div class="card" style="background:var(--grey);border-color:transparent"><h3>Send us a message</h3><p>Our online form is on its way. In the meantime, the fastest way to reach Katrina and the team is by phone or email:</p>
<p style="font-size:1.25rem;font-weight:600;margin-bottom:6px"><a href="{tel_href()}">{PHONE}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<div class="actions"><a class="btn btn-sm" href="{BOOK_URL}" target="_blank" rel="noopener">Book online</a><a class="btn btn-sm btn-outline" href="{tel_href()}">Call now</a></div>
<!-- Set JOTFORM_ID in site_lib.py to replace this fallback with the embedded Jotform --></div>'''
    review = GBP_REVIEW_URL if GBP_REVIEW_URL != "TODO" else None
    review_block = (f'<p><a class="btn btn-outline" href="{review}" target="_blank" rel="noopener">Write a Google review</a></p>' if review
                    else '<p>Search <strong>&ldquo;Serene Med Spa Paintsville&rdquo;</strong> on Google Maps and tap <em>Write a review</em>. A direct link is coming soon.</p>')
    body = page_hero("Contact Serene Med Spa Paintsville", f"Call, book online or send a message. We&rsquo;re at {ADDR1}, {ADDR2} &mdash; on Broadway in downtown Paintsville, an easy drive from Prestonsburg, Pikeville, Salyersville and Louisa.", crumbs, "We&rsquo;d love to hear from you") + f'''
<section><div class="wrap"><div class="grid g2" style="align-items:start">
<div><span class="eyebrow">Get in touch</span><h2 style="font-size:1.8rem;margin-bottom:18px">Message us</h2>{form}</div>
<div><span class="eyebrow">Find us</span><h2 style="font-size:1.8rem;margin-bottom:18px">Location &amp; hours</h2>
<div class="loc" style="grid-template-columns:1fr"><div class="loc-body"><dl style="margin-top:0"><dt>Address</dt><dd>{ADDR1}<br>{ADDR2}</dd><dt>Phone</dt><dd><a href="{tel_href()}">{PHONE}</a></dd><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd><dt>Hours</dt><dd>{HOURS}</dd><dt>Booking</dt><dd><a href="{BOOK_URL}" target="_blank" rel="noopener">Book online through Vagaro</a></dd></dl>
<div class="actions"><a class="btn btn-sm btn-outline" href="{MAP_LINK}" target="_blank" rel="noopener">Get directions</a></div></div>
<iframe class="map" style="min-height:300px" src="{MAP_EMBED}" title="Map to Serene Med Spa, {ADDR1}, {ADDR2}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div>
</div></div></section>
<section class="tint-sand" id="review"><div class="wrap narrow" style="text-align:center"><span class="eyebrow">Already visited?</span><h2>Leave us a Google review</h2><p class="lede" style="margin:0 auto 18px">Reviews help neighbors in Paintsville and across Eastern Kentucky find physician-directed care close to home. Thank you!</p>{review_block}</div></section>
<section><div class="wrap narrow prose"><h2 style="margin-top:0">Getting here</h2><p>Serene Med Spa Paintsville is at {ADDR1}, in downtown Paintsville near the Johnson County courthouse district. From US-23, take the Paintsville exit toward downtown and follow Main Street to Broadway. Free street and lot parking is close by. We are roughly 20 minutes from Prestonsburg, 30 minutes from Salyersville and Louisa, 45 minutes from Pikeville and about an hour from Ashland.</p>
<h2>Before your first visit</h2><ul><li>Arrive 10 minutes early to complete a short health history.</li><li>Bring a list of medications and supplements.</li><li>For laser or IPL visits, avoid tanning for 4 weeks and shave the area within 24 hours.</li><li>Consultations are complimentary; pricing is confirmed before any treatment.</li></ul></div></section>'''
    title = "Contact Serene Med Spa Paintsville, KY | Book & Directions"
    desc = f"Contact Serene Med Spa Paintsville, {ADDR1}, {ADDR2}. Call {PHONE} or book online through Vagaro. Hours and map."
    ld = [{"@context": "https://schema.org", "@type": "ContactPage", "url": SITE_URL + path, "name": "Contact Serene Med Spa Paintsville", "description": desc, "mainEntity": {"@id": ORG_ID}}, business_ld()]
    write(path, shell(path, title, desc, body, ld=ld, crumbs=crumbs))


def specials():
    path = "/specials/"
    crumbs = [("/", "Home"), (None, "Specials")]
    if C.SPECIALS:
        cards = "".join(f'<div class="card reveal"><span class="eyebrow">{e}</span><h3>{t}</h3><p>{d}</p><a class="btn btn-sm" href="{BOOK_URL}" target="_blank" rel="noopener">Book now</a></div>' for t, d, e in C.SPECIALS)
        form = (f'<div class="jf"><iframe src="https://form.jotform.com/{JOTFORM_ID}" title="Claim your offer - Serene Med Spa Paintsville" loading="lazy" allow="geolocation; microphone; camera"></iframe></div>'
                f'<p class="fine" style="margin-top:10px">Please don&rsquo;t include private medical details in this form &mdash; we&rsquo;ll gather anything clinical securely at your visit.</p>') if JOTFORM_ID and JOTFORM_ID != "TODO" else ""
        main = (f'<div class="grid g2">{cards}</div><p class="fine" style="margin-top:18px">Specials can&rsquo;t be combined with other discounts. Mention the offer when you book.</p>'
                f'<div class="card reveal" style="margin-top:28px"><span class="eyebrow">Claim your offer</span><h3>Tell us what you&rsquo;re interested in</h3><p>Send this short form and Katrina will call or text to set up your complimentary consultation. Or <a href="{BOOK_URL}" target="_blank" rel="noopener">book online</a> and mention the offer.</p>{form}</div>')
    else:
        main = f'''<div class="offer reveal"><div><span class="eyebrow">Coming soon</span><h2>New client special coming soon</h2><p class="lede">We are putting the finishing touches on our opening offer for Paintsville. Book a complimentary consultation now and we will apply any special that is live on the day of your first treatment.</p>{cta_row("/pricing/", "See regular rates")}</div><div style="text-align:center"><span class="big">Soon</span><p class="fine">Follow Serene on social or check back here</p></div></div>'''
    body = page_hero("Specials", "Current offers at Serene Med Spa Paintsville. " + C.PRICE_NOTE, crumbs, "Paintsville offers", cta=False) + f'<section><div class="wrap">{main}<div style="margin-top:48px">{packages_block("Packages &amp; gift cards")}</div></div></section>{book_band()}'
    title = "Specials | Serene Med Spa Paintsville, KY"
    desc = "Current specials and new-client offers at Serene Med Spa Paintsville, KY — Botox, Xeomin, laser hair removal, InMode treatments, hormone and IV therapy."
    write(path, shell(path, title, desc, body, crumbs=crumbs))


def legal(path, h1, title, desc, html_body):
    crumbs = [("/", "Home"), (None, h1)]
    body = page_hero(h1, "", crumbs, cta=False) + f'<section><div class="wrap prose">{html_body}</div></section>'
    write(path, shell(path, title, desc, body, crumbs=crumbs))

def privacy():
    legal("/privacy-policy/", "Privacy Policy", "Privacy Policy | Serene Med Spa Paintsville, KY",
          "How Serene Med Spa Paintsville, KY collects, uses and protects your information on serenemedspaky.com, including booking, forms, analytics and your rights.", f'''
<p class="fine">Effective {TODAY}</p>
<p>{LEGAL} (&ldquo;Serene,&rdquo; &ldquo;we&rdquo;) operates serenemedspaky.com for Serene Med Spa Paintsville, {ADDR1}, {ADDR2}. This policy explains what information this website collects and how we use it.</p>
<h2>Information we collect</h2><ul><li><strong>Information you give us</strong> &mdash; name, phone, email and message content when you contact us or request an appointment. Contact forms are hosted by Jotform; online booking is hosted by Vagaro. Each has its own privacy policy.</li>
<li><strong>Usage data</strong> &mdash; if analytics are enabled, standard, largely anonymous data such as pages viewed, device type and approximate location, collected through cookies or similar technologies.</li></ul>
<h2>How we use it</h2><p>To respond to you, schedule and confirm appointments, send appointment reminders, improve the website, and &mdash; only with your consent &mdash; send occasional offers. We do not sell your personal information.</p>
<h2>Health information</h2><p>Please do not send private health details through this website. Clinical information is collected securely at the clinic and protected under our Notice of Privacy Practices, which is available at the front desk.</p>
<h2>Sharing</h2><p>We share information only with service providers who help us run the website and clinic (booking, forms, hosting, analytics), and when required by law.</p>
<h2>Cookies &amp; choices</h2><p>You can block cookies in your browser. To access, correct or delete the information we hold about you, or to stop marketing messages, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="{tel_href()}">{PHONE}</a>.</p>
<h2>Children</h2><p>This website is not directed to children under 13 and we do not knowingly collect their information.</p>
<h2>Changes</h2><p>We may update this policy; the effective date above will change when we do.</p>
<h2>Contact</h2><p>{LEGAL} &middot; {ADDR1}, {ADDR2} &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></p>''')

def terms():
    legal("/terms/", "Terms of Use", "Terms of Use | Serene Med Spa Paintsville, KY",
          "Terms of use for serenemedspaky.com, the website of Serene Med Spa Paintsville, KY: medical disclaimer, pricing, booking and liability.", f'''
<p class="fine">Effective {TODAY}</p>
<p>By using serenemedspaky.com you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>Not medical advice</h2><p>Content on this website is for general information only and is not medical advice, diagnosis or treatment. It does not create a provider&ndash;patient relationship. Always consult a qualified provider about your individual situation. Individual results vary; before-and-after images, where shown, are illustrative and not a guarantee of results. If you have a medical emergency, call 911.</p>
<h2>Treatments and candidacy</h2><p>All treatments require an in-person consultation and are provided only when medically appropriate. Device descriptions reflect manufacturer clearances for specific indications; some uses discussed with patients may be off-label and are explained as such at consultation.</p>
<h2>Pricing</h2><p>Prices shown are regular rates in US dollars and may change without notice. Specials cannot be combined unless stated. The final cost of any treatment is confirmed with you before it is performed.</p>
<h2>Booking and cancellations</h2><p>Online booking is provided through Vagaro. Please give at least 24 hours&rsquo; notice to cancel or reschedule so we can offer the time to another patient; repeated late cancellations or no-shows may require a deposit for future bookings.</p>
<h2>Intellectual property</h2><p>The text, images and design of this site belong to {LEGAL} or its licensors. Product and device names (Botox&reg;, Xeomin&reg;, InMode, Optimas, Lumecca, Forma, DiolazeXL, Morpheus8, EvolveX, EmpowerRF, VTone, FormaV, Morpheus8V, Biote&reg;) are trademarks of their respective owners and are used for identification only.</p>
<h2>Third-party links</h2><p>Links to Vagaro, Jotform, Google Maps and other sites are provided for convenience; we are not responsible for their content or privacy practices.</p>
<h2>Limitation of liability</h2><p>The site is provided &ldquo;as is.&rdquo; To the fullest extent permitted by law, {LEGAL} is not liable for any damages arising from use of, or inability to use, this website.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the Commonwealth of Kentucky.</p>
<h2>Contact</h2><p>{LEGAL} &middot; {ADDR1}, {ADDR2} &middot; <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="{tel_href()}">{PHONE}</a></p>''')

def not_found():
    body = f'''<section class="page-hero plain"><div class="wrap"><span class="eyebrow">404</span><h1>Page not found</h1><p class="lede">That page has moved or never existed. Try one of these instead.</p>
<div class="actions" style="justify-content:center;margin-top:22px"><a class="btn" href="/">Home</a><a class="btn btn-outline" href="/services/">Treatments</a><a class="btn btn-outline" href="/pricing/">Pricing</a><a class="btn btn-outline" href="/contact/">Contact</a></div></div></section>'''
    write("/404.html", shell("/404.html", "Page Not Found | Serene Med Spa Paintsville, KY", "The page you were looking for on serenemedspaky.com could not be found. Browse treatments, pricing and contact details for Serene Med Spa Paintsville, KY.", body, noindex=True))


# ================================================================== static files
FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#10322F"/><text x="32" y="45" text-anchor="middle" font-family="Georgia,'Noto Serif Display',serif" font-size="40" fill="#C4C7E6">S</text></svg>'''

def statics():
    with open(os.path.join(OUT, "favicon.svg"), "w") as f: f.write(FAVICON)
    with open(os.path.join(OUT, "site.webmanifest"), "w") as f:
        json.dump({"name": SITE_NAME, "short_name": "Serene KY", "start_url": "/", "display": "standalone", "background_color": "#ffffff", "theme_color": "#10322F",
                   "icons": [{"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, f, indent=1)
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    # Google Search Console ownership file (URL-prefix property https://serenemedspaky.com/, added Oct 1 2026). Keep forever.
    with open(os.path.join(OUT, "googleedf07ec694035423.html"), "w") as f:
        f.write("google-site-verification: googleedf07ec694035423.html")
    urls = [p for p in PAGES if p.endswith("/")]
    pri = lambda p: "1.0" if p == "/" else ("0.9" if p in ("/services/", "/pricing/", "/contact/") or p.strip("/") in C.BY_SLUG else ("0.3" if p in ("/privacy-policy/", "/terms/") else "0.7"))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{SITE_URL}{p}</loc><lastmod>{TODAY}</lastmod><changefreq>{'weekly' if p in ('/', '/specials/') else 'monthly'}</changefreq><priority>{pri(p)}</priority></url>\n" for p in urls) + "</urlset>\n"
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f: f.write(xml)
    # CSS with cache-busting hash
    css = CSS.strip() + "\n"
    v = hashlib.md5(css.encode()).hexdigest()[:8]
    with open(os.path.join(OUT, "main.css"), "w") as f: f.write(css)
    for p, h in list(PAGES.items()):
        h2 = h.replace("%%CSSV%%", v)
        PAGES[p] = h2
        fp = os.path.join(OUT, "index.html") if p == "/" else (os.path.join(OUT, p.strip("/"), "index.html") if p.endswith("/") else os.path.join(OUT, p.lstrip("/")))
        with open(fp, "w", encoding="utf-8") as f: f.write(h2)


def images():
    """Copy assets/img -> <out>/img verbatim. 800px variants live in assets/img/800/ (pre-generated, committed).
    If Pillow happens to be installed and a variant is missing, create it; otherwise skip silently."""
    dst = os.path.join(OUT, "img")
    for root, _, files in os.walk(ASSETS):
        rel = os.path.relpath(root, ASSETS)
        d = os.path.join(dst, rel) if rel != "." else dst
        os.makedirs(d, exist_ok=True)
        for fn in files:
            if fn.startswith("._") or fn == ".DS_Store":  # macOS metadata (external drives)
                continue
            src = os.path.join(root, fn); out = os.path.join(d, fn)
            if not os.path.exists(out) or os.path.getmtime(src) > os.path.getmtime(out) or os.path.getsize(src) != os.path.getsize(out):
                shutil.copyfile(src, out)  # copyfile, not copy2: xattrs on external volumes can't be copied
    # optional: fill in any missing 800px variant (dev convenience only)
    try:
        from PIL import Image
    except Exception:
        return
    small_dir = os.path.join(dst, "800"); os.makedirs(small_dir, exist_ok=True)
    for fn in os.listdir(ASSETS):
        ext = os.path.splitext(fn)[1].lower()
        if ext not in (".jpg", ".jpeg", ".webp"): continue
        small = os.path.join(small_dir, fn)
        if os.path.exists(small): continue
        try:
            im = Image.open(os.path.join(ASSETS, fn))
            if im.width > 800: im = im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS)
            if ext == ".webp": im.save(small, "WEBP", quality=80)
            else: im.convert("RGB").save(small, "JPEG", quality=80, optimize=True, progressive=True)
            print(f"  made missing variant img/800/{fn} (commit it to assets/img/800/)", file=sys.stderr)
        except Exception as e:
            print(f"  could not make variant for {fn}: {e}", file=sys.stderr)


# ================================================================== main
def build():
    if os.path.isdir(OUT):
        for n in os.listdir(OUT):
            p = os.path.join(OUT, n)
            if n == "img": continue          # image copies are refreshed in place
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(OUT, exist_ok=True)
    home(); services(); pricing(); about(); contact(); specials(); privacy(); terms(); not_found()
    for s in C.SERVICES: service_page(s)
    statics(); images()
    print(f"Built {len(PAGES)} pages into {OUT}")
    for p in sorted(PAGES): print(f"  {p:26s} {re.search(r'<title>(.*?)</title>', PAGES[p]).group(1)}")

if __name__ == "__main__":
    build()
    if "--no-check" not in sys.argv:
        try:
            import check_site
            rc = check_site.run(OUT)
            if rc: print("!!! paintsville: QA found problems (see above) — build output kept, continuing", file=sys.stderr)
        except Exception as e:
            print(f"!!! paintsville: QA step crashed ({e}) — continuing", file=sys.stderr)
    sys.exit(0)
