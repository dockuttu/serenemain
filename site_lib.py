# -*- coding: utf-8 -*-
"""site_lib.py — shared shell (head/nav/footer), brand constants and helpers for serenemedspas.com (static)."""
import re, html, os, json

SITE_URL = "https://serenemedspas.com"
LOGO = "/wp-content/uploads/2024/11/Serene_Logo-1024x574.png"
HUDSON = {"name": "Hudson, OH", "addr1": "50 W Streetsboro St, Suite 2", "addr2": "Hudson, OH 44236", "tel": "+13304605915",
          "phone": "(330) 460-5915", "book": "https://booking.mangomint.com/serenemedspa/Hudson", "site": "https://hudson.serenemedspas.com/",
          "map": "https://maps.google.com/maps?q=50+W+Streetsboro+St+Suite+2,+Hudson,+OH+44236", "state": "Ohio"}
BARB = {"name": "Barboursville, WV", "addr1": "1 Chateau Grove Ln", "addr2": "Barboursville, WV 25504", "tel": "+13045200461",
        "phone": "(304) 520-0461", "book": "https://booking.mangomint.com/serenemedspa/Barboursville", "site": "https://barboursville.serenemedspas.com/",
        "map": "https://maps.google.com/maps?q=1+Chateau+Grove+Ln,+Barboursville,+WV+25504", "state": "West Virginia"}
TELE = {"phone": "(330) 775-2452", "tel": "+13307752452", "spruce": "https://spruce.care/serene-telehealth", "consent": "https://form.jotform.com/262647300953054"}
BLOG = "https://blog.serenemedspas.com/"
GTAG = "AW-788907512"
META_PIXEL = "475660982946848"

# ------------------------------------------------------------------ CSS
CSS = r"""
:root{
  --teal-900:#1E4A55;--teal-700:#2A6F7F;--teal-500:#3E8FA0;--teal-100:#E3F0F2;
  --sage:#7FAE93;--sage-100:#E9F3EC;
  --sand:#F4EEE6;--paper:#FBFAF7;--white:#fff;
  --ink:#1B2A2F;--ink-soft:#4A5B61;--muted:#7C8A8F;--rule:#E1E7E7;
  --rose:#D98A8A;--gold:#C9A56B;
  --shadow:0 18px 40px -22px rgba(30,74,85,.35);
  --r:18px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Jost',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:var(--paper);line-height:1.7;font-weight:400;overflow-x:hidden}
h1,h2,h3,h4{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;line-height:1.12;color:var(--teal-900);letter-spacing:-.01em}
h1{font-size:clamp(2.4rem,5.2vw,4rem)}h2{font-size:clamp(1.9rem,3.6vw,2.7rem)}h3{font-size:1.45rem}h4{font-size:1.1rem;font-family:'Jost',sans-serif;font-weight:600}
p{margin:0 0 1em}
a{color:var(--teal-700);text-decoration:none}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.narrow{max-width:820px}
section{padding:72px 0}
.eyebrow{font-size:.74rem;letter-spacing:.28em;text-transform:uppercase;font-weight:600;color:var(--sage);margin-bottom:14px;display:block}
.lede{font-size:1.18rem;color:var(--ink-soft);max-width:62ch}
.section-head{max-width:720px;margin-bottom:38px}
.section-head.center{margin-left:auto;margin-right:auto;text-align:center}
.btn{display:inline-block;background:var(--teal-700);color:#fff;padding:15px 32px;border-radius:40px;font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;font-weight:600;transition:.25s;border:1.5px solid var(--teal-700);cursor:pointer;line-height:1.2;text-align:center}
.btn:hover{background:var(--teal-900);border-color:var(--teal-900);transform:translateY(-2px);box-shadow:var(--shadow)}
.btn-outline{background:transparent;color:var(--teal-700)}
.btn-outline:hover{background:var(--teal-700);color:#fff}
.btn-ghost{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.8);color:#fff;backdrop-filter:blur(4px)}
.btn-ghost:hover{background:#fff;color:var(--teal-900);border-color:#fff}
.btn-sm{padding:11px 22px;font-size:.74rem}
.tint-sand{background:var(--sand)}.tint-teal{background:var(--teal-900);color:#fff}.tint-teal h2,.tint-teal h3{color:#fff}.tint-teal .eyebrow{color:var(--sage)}
.tint-sage{background:var(--sage-100)}
.grid{display:grid;gap:24px}
.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}.g4{grid-template-columns:repeat(4,1fr)}
.card{background:#fff;border:1px solid var(--rule);border-radius:var(--r);padding:28px;box-shadow:0 1px 0 rgba(0,0,0,.02);transition:.25s}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:transparent}
.card h3{margin-bottom:8px}
.card p{color:var(--ink-soft);margin-bottom:12px}
.card .more{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;font-weight:600}
/* promo + header */
.promo{background:var(--teal-900);color:#fff;text-align:center;font-size:.84rem;letter-spacing:.04em;padding:9px 16px}
.promo a{color:#fff;border-bottom:1px solid rgba(255,255,255,.6)}
header{position:sticky;top:0;z-index:60;background:rgba(251,250,247,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--rule)}
.nav{display:flex;align-items:center;justify-content:space-between;height:82px;gap:16px}
.nav .logo img{height:52px;width:auto}
.nav ul{display:flex;gap:6px;list-style:none;align-items:center;flex:1;justify-content:center}
.nav ul li{position:relative}
.nav ul a{font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;color:var(--ink);font-weight:500;padding:10px 12px;border-radius:8px;display:block;transition:.2s}
.nav ul li:hover>a,.nav ul a:hover{color:var(--teal-700);background:var(--teal-100)}
.drop{position:absolute;top:100%;left:0;min-width:240px;background:#fff;border:1px solid var(--rule);border-radius:14px;padding:10px;box-shadow:var(--shadow);display:none;z-index:70}
.drop.mega{min-width:720px;display:none;grid-template-columns:repeat(3,1fr);gap:8px 18px;padding:18px 20px;left:50%;transform:translateX(-50%)}
.nav li:hover>.drop{display:block}.nav li:hover>.drop.mega{display:grid}
.drop a{text-transform:none;letter-spacing:0;font-size:.92rem;padding:8px 10px;font-weight:400}
.drop h5{font-family:'Jost',sans-serif;font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--sage);margin:6px 10px 4px}
.nav .btn{padding:12px 24px;flex:0 0 auto}
.menu-toggle{display:none;background:none;border:0;font-size:1.8rem;color:var(--teal-700);cursor:pointer}
/* hero */
.hero{position:relative;min-height:78vh;display:flex;align-items:center;color:#fff;
  background:linear-gradient(100deg,rgba(20,45,52,.82) 0%,rgba(20,45,52,.55) 45%,rgba(20,45,52,.15) 100%),url('/wp-content/uploads/2024/07/2148574924.jpg') center/cover no-repeat}
.hero h1{color:#fff;max-width:14ch}
.hero .lede{color:rgba(255,255,255,.9);font-size:1.22rem;margin:18px 0 30px}
.hero .eyebrow{color:#BFE3D0}
.hero-cta{display:flex;gap:12px;flex-wrap:wrap}
.hero-chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:34px}
.chip{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);padding:8px 14px;border-radius:30px;font-size:.78rem;letter-spacing:.06em;backdrop-filter:blur(4px)}
/* page hero (interior) */
.page-hero{background:linear-gradient(120deg,var(--teal-100) 0%,var(--sage-100) 100%);padding:64px 0 48px}
.page-hero h1{max-width:20ch}
.page-hero .lede{margin-top:14px}
.crumbs{font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:18px}
.crumbs a{color:var(--muted)}
/* locations */
.loc{display:grid;grid-template-columns:1.05fr .95fr;overflow:hidden;background:#fff;border:1px solid var(--rule);border-radius:var(--r)}
.loc .loc-body{padding:34px}
.loc .map{width:100%;height:100%;min-height:280px;border:0;display:block}
.loc dl{margin:14px 0 22px}.loc dt{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--sage);font-weight:600;margin-top:12px}
.loc dd{font-size:1.05rem;font-weight:500}
.loc .state{font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal-500);font-weight:600}
.actions{display:flex;gap:10px;flex-wrap:wrap}
/* concern tiles */
.tile{position:relative;border-radius:var(--r);overflow:hidden;aspect-ratio:4/3;display:block}
.tile img{width:100%;height:100%;object-fit:cover;transition:.5s}
.tile:hover img{transform:scale(1.05)}
.tile span{position:absolute;left:0;right:0;bottom:0;padding:18px 20px;color:#fff;font-family:'Cormorant Garamond',serif;font-size:1.5rem;font-weight:600;background:linear-gradient(transparent,rgba(20,45,52,.85))}
/* tools */
.tool{display:flex;gap:16px;align-items:flex-start;background:#fff;border:1px solid var(--rule);border-radius:14px;padding:18px 20px;transition:.25s}
.tool:hover{border-color:var(--teal-500);box-shadow:var(--shadow);transform:translateY(-2px)}
.tool b{display:inline-flex;width:40px;height:40px;border-radius:50%;background:var(--teal-100);color:var(--teal-700);align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;font-size:1.3rem;flex:0 0 40px}
.tool h4{margin-bottom:2px;color:var(--teal-900)}.tool p{font-size:.92rem;color:var(--ink-soft);margin:0}
/* stats */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;text-align:center}
.stat b{display:block;font-family:'Cormorant Garamond',serif;font-size:2.8rem;color:var(--teal-700);line-height:1}
.stat span{font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
/* providers */
.prov{display:grid;grid-template-columns:1fr 1.2fr;gap:0;overflow:hidden;background:#fff;border-radius:var(--r);border:1px solid var(--rule)}
.prov img{width:100%;height:100%;object-fit:cover;min-height:360px}
.prov .pbody{padding:34px}
.prov .creds{list-style:none;margin:14px 0 20px;display:flex;flex-wrap:wrap;gap:8px}
.prov .creds li{font-size:.76rem;background:var(--sage-100);color:var(--teal-900);padding:6px 12px;border-radius:30px}
/* reviews */
.rev{background:#fff;border:1px solid var(--rule);border-radius:var(--r);padding:26px}
.rev .stars{color:var(--gold);letter-spacing:2px;margin-bottom:8px}
.rev p{font-size:1.02rem;color:var(--ink);font-style:italic}
.rev .who{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:600}
/* faq */
.faq{border-top:1px solid var(--rule)}
.faq details{border-bottom:1px solid var(--rule);padding:18px 0}
.faq summary{cursor:pointer;font-family:'Cormorant Garamond',serif;font-size:1.35rem;font-weight:600;color:var(--teal-900);list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--sage);font-size:1.6rem;line-height:1}
.faq details[open] summary::after{content:"\2013"}
.faq details p{margin-top:10px;color:var(--ink-soft)}
/* band */
.band{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center}
/* consult form */
.zf{max-width:760px}
.zf-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px 18px}
.zf-full{grid-column:1/-1}
.zf-field label{display:block;font-size:.76rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--teal-700);margin-bottom:6px}
.zf-field label span{color:#b0163f}
.zf-field input,.zf-field select,.zf-field textarea{width:100%;font:inherit;font-size:1rem;padding:13px 14px;border:1.5px solid var(--rule);border-radius:10px;background:#fff;color:var(--ink);-webkit-appearance:none;appearance:none}
.zf-field input:focus,.zf-field select:focus,.zf-field textarea:focus{outline:none;border-color:var(--teal-500)}
.zf-field textarea{min-height:110px;resize:vertical}
.zf-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;opacity:0}
.zf-actions{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:18px}
.zf-err{color:#b0163f;font-weight:600;font-size:.95rem}
.zf-done{border:1.5px solid var(--sage);background:#fff;padding:28px 30px;border-radius:var(--r);max-width:760px}
.zf-fine{font-size:.86rem;color:var(--muted);margin-top:14px}
/* article / prose */
.prose{max-width:760px}
.prose h2{margin:44px 0 14px;font-size:1.9rem}.prose h3{margin:30px 0 10px}.prose h4{margin:22px 0 8px}
.prose p,.prose li{font-size:1.08rem;color:var(--ink);line-height:1.8}
.prose ul,.prose ol{margin:0 0 1.2em 1.4em}
.prose img{border-radius:14px;margin:26px 0}
.prose a{text-decoration:underline;text-underline-offset:3px}
.prose blockquote{border-left:4px solid var(--sage);padding:8px 20px;margin:24px 0;color:var(--ink-soft);font-style:italic}
.prose table{width:100%;border-collapse:collapse;margin:20px 0;font-size:.98rem}
.prose th,.prose td{border:1px solid var(--rule);padding:10px 12px;text-align:left}
.prose th{background:var(--sand)}
.post-hero{padding:56px 0 30px}
.post-meta{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:14px}
.post-fig img{width:100%;max-height:520px;object-fit:cover;border-radius:var(--r)}
.post-wrap{display:grid;grid-template-columns:1fr 320px;gap:48px;align-items:start}
.side{position:sticky;top:100px}
.side .card{margin-bottom:18px}
.side .card h3{font-size:1.25rem}
.side .card .btn{width:100%;margin-top:8px}
.side .card ul{list-style:none}
.side .card li{padding:6px 0;border-bottom:1px dashed var(--rule);font-size:.95rem}
.related{margin-top:56px}
/* post cards */
.post-card{background:#fff;border:1px solid var(--rule);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;transition:.25s}
.post-card:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.post-card img{width:100%;aspect-ratio:16/10;object-fit:cover}
.post-card .pc-body{padding:20px 22px 22px;display:flex;flex-direction:column;flex:1}
.post-card .pc-cat{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--sage);font-weight:600;margin-bottom:6px}
.post-card h3{font-size:1.28rem;margin-bottom:8px}
.post-card p{font-size:.95rem;color:var(--ink-soft);flex:1}
.post-card .more{font-size:.76rem;letter-spacing:.12em;text-transform:uppercase;font-weight:600}
.cat-nav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 30px}
.cat-nav a{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;padding:9px 16px;border-radius:30px;border:1.5px solid var(--rule);background:#fff;color:var(--ink-soft)}
.cat-nav a:hover,.cat-nav a.on{border-color:var(--teal-700);color:var(--teal-700)}
/* embedded legacy widgets (contact, telehealth, tools) */
.embed{padding:32px 0 60px}
.embed .wrap>*{margin-left:auto;margin-right:auto}
/* prose accordions (post-care etc.) */
.prose details{border:1px solid var(--rule);border-radius:12px;padding:14px 18px;margin:12px 0;background:#fff}
.prose details summary{cursor:pointer;font-family:'Cormorant Garamond',Georgia,serif;font-size:1.35rem;font-weight:600;color:var(--teal-900);list-style:none;display:flex;justify-content:space-between;gap:16px}
.prose details summary::-webkit-details-marker{display:none}
.prose details summary::after{content:"+";color:var(--sage);font-size:1.5rem;line-height:1}
.prose details[open] summary::after{content:"\2013"}
.prose details>*:not(summary){margin-top:10px}
.prov img{max-height:480px}
.loc.compact{grid-template-columns:1fr}
.loc.compact .map{display:none}
.filter{display:flex;gap:10px;align-items:center;margin:0 0 22px}
.filter input{flex:1;font:inherit;font-size:1rem;padding:13px 16px;border:1.5px solid var(--rule);border-radius:30px;background:#fff}
.filter input:focus{outline:none;border-color:var(--teal-500)}
.hidden{display:none!important}
/* footer */
footer{background:var(--teal-900);color:rgba(255,255,255,.85);padding:64px 0 28px;margin-top:40px}
.foot-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1.1fr;gap:36px}
footer h4{color:#fff;font-family:'Jost',sans-serif;font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;margin-bottom:14px}
footer ul{list-style:none}footer li{margin:6px 0;font-size:.95rem}
footer a{color:rgba(255,255,255,.85)}footer a:hover{color:#fff}
footer img{height:54px;width:auto;margin-bottom:14px;filter:brightness(0) invert(1)}
.foot-bottom{border-top:1px solid rgba(255,255,255,.15);margin-top:36px;padding-top:20px;font-size:.82rem;color:rgba(255,255,255,.6);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
.foot-bottom a{color:rgba(255,255,255,.7);margin-right:14px}
/* sticky mobile bar */
.mbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:80;background:#fff;border-top:1px solid var(--rule);padding:10px 12px;gap:10px}
.mbar a{flex:1;text-align:center;padding:13px;border-radius:30px;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;font-weight:600}
.mbar-call{border:1.5px solid var(--teal-700);color:var(--teal-700)}.mbar-book{background:var(--teal-700);color:#fff}
/* reveal */
.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
/* responsive */
@media (max-width:1024px){.g4{grid-template-columns:repeat(2,1fr)}.foot-grid{grid-template-columns:1fr 1fr}.drop.mega{min-width:560px}.stats{grid-template-columns:repeat(2,1fr)}.post-wrap{grid-template-columns:1fr}.side{position:static}}
@media (max-width:820px){
  section{padding:52px 0}
  .g2,.g3{grid-template-columns:1fr}.loc,.prov,.band{grid-template-columns:1fr}.loc .map{min-height:220px}
  .nav ul{display:none;position:absolute;top:82px;left:0;right:0;background:#fff;flex-direction:column;align-items:stretch;padding:12px 16px 20px;border-bottom:1px solid var(--rule);gap:2px;max-height:calc(100vh - 82px);overflow:auto}
  .nav ul.open{display:flex}
  .nav ul li:hover>.drop,.nav ul li:hover>.drop.mega{display:none}
  .nav ul li.open>.drop,.nav ul li.open>.drop.mega{display:block;position:static;transform:none;min-width:0;box-shadow:none;border:0;padding:0 0 6px 14px}
  .nav .btn{display:none}.menu-toggle{display:block}
  .hero{min-height:70vh}
  .zf-grid{grid-template-columns:1fr}
  .mbar{display:flex}body{padding-bottom:64px}.promo-more{display:none}
  .foot-bottom{flex-direction:column}
}
@media (max-width:560px){.g4{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}.foot-grid{grid-template-columns:1fr}}
"""

# ------------------------------------------------------------------ NAV / FOOTER
SERVICE_MENU = [
    ("Injectables", [("/botox-treatment-benefits/", "Botox & Wrinkle Relaxers"), ("/service/#injectables", "Dermal Fillers"), ("/lip-filler-injection/", "Lip Filler"),
                     ("/kybella-treatment-for-double-chin/", "Kybella"), ("/pdo-thread-lift-face-neck/", "PDO Thread Lift")]),
    ("Skin & Laser", [("/morpheus8-rf-microneedling-treatment-at-serene-med-spas/", "Morpheus8"), ("/hydrafacial-treatment-benefits/", "HydraFacial"),
                      ("/microneedling-with-prp/", "Microneedling & PRP"), ("/chemical-peel-treatments-serene-med-spa/", "Chemical Peels"),
                      ("/laser-hair-removal-at-serene-med-spa/", "Laser Hair Removal")]),
    ("Wellness", [("/telehealth/", "Telehealth & Weight Management"), ("/biote-hormone-therapy/", "Hormone Therapy"),
                  ("/the-serene-hydration-bar/", "IV Therapy"), ("/natural-prp-hair-restoration/", "PRP Hair Restoration"), ("/service/", "All treatments ›")]),
]
PATIENT_MENU = [("/telehealth/", "Telehealth"), ("/post-care-instructions/", "Post-Care Instructions"), ("/membership/", "Membership"),
                ("/financing/", "Financing"), ("/specials/", "Monthly Specials"), ("/recommendation-webapp/", "Treatment Finder"),
                ("/reviews/", "Patient Reviews"), ("/blogs/", "Blog")]
ABOUT_MENU = [("/our-story/", "Our Story"), ("/our-providers/", "Our Providers"), ("/about-us/", "About Serene"), ("/reviews/", "Reviews"), ("/contact-us/", "Contact")]

def _drop(items):
    return '<div class="drop">' + "".join(f'<a href="{h}">{t}</a>' for h, t in items) + '</div>'
def _mega():
    cols = []
    for cat, items in SERVICE_MENU:
        cols.append(f'<div><h5>{cat}</h5>' + "".join(f'<a href="{h}">{t}</a>' for h, t in items) + '</div>')
    return '<div class="drop mega">' + "".join(cols) + '</div>'

PROMO = '<div class="promo">&#10022; <a href="/specials/">This month&rsquo;s specials</a> at Hudson &amp; Barboursville<span class="promo-more"> &middot; New: <a href="/telehealth/">Serene Telehealth</a> with Dr. Arora &mdash; weight management &amp; hormone care by video</span></div>'

NAV = PROMO + f'''<header>
  <div class="wrap nav">
    <a class="logo" href="/"><img src="{LOGO}" alt="Serene Med Spa" width="220" height="123"></a>
    <ul id="menu">
      <li><a href="/service/">Treatments &#9662;</a>{_mega()}</li>
      <li><a href="/about-us/">About &#9662;</a>{_drop(ABOUT_MENU)}</li>
      <li><a href="/telehealth/">For Patients &#9662;</a>{_drop(PATIENT_MENU)}</li>
      <li><a href="/locations/">Locations &#9662;</a>{_drop([(HUDSON["site"], "Hudson, OH"), (BARB["site"], "Barboursville, WV"), ("/telehealth/", "Telehealth (OH, WV, KY, FL)")])}</li>
      <li><a href="/contact-us/">Contact</a></li>
    </ul>
    <a class="btn" href="/#book">Book Now</a>
    <button class="menu-toggle" aria-label="Menu" aria-controls="menu" onclick="document.getElementById('menu').classList.toggle('open')">&#9776;</button>
  </div>
</header>'''

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img src="{LOGO}" alt="Serene Med Spa" width="220" height="123">
        <p style="max-width:340px">Physician-led medical aesthetics &amp; wellness in Hudson, Ohio and Barboursville, West Virginia &mdash; and by telehealth across Ohio, West Virginia, Kentucky and Florida. Natural results, personalized plans, care you can trust.</p>
        <p style="font-size:.85rem;color:rgba(255,255,255,.6)">Medical Director: Robin Arora, MD &middot; Board Certified, American Board of Internal Medicine</p>
      </div>
      <div>
        <h4>Hudson, OH</h4>
        <ul><li>{HUDSON["addr1"]}</li><li>{HUDSON["addr2"]}</li><li><a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a></li>
        <li><a href="{HUDSON["book"]}" target="_blank" rel="noopener">Book online</a></li><li><a href="{HUDSON["site"]}">hudson.serenemedspas.com &rsaquo;</a></li></ul>
        <h4 style="margin-top:22px">Barboursville, WV</h4>
        <ul><li>{BARB["addr1"]}</li><li>{BARB["addr2"]}</li><li><a href="tel:{BARB["tel"]}">{BARB["phone"]}</a></li>
        <li><a href="{BARB["book"]}" target="_blank" rel="noopener">Book online</a></li><li><a href="{BARB["site"]}">barboursville.serenemedspas.com &rsaquo;</a></li></ul>
      </div>
      <div>
        <h4>Patients</h4>
        <ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in PATIENT_MENU)}<li><a href="/service/">All Treatments</a></li><li><a href="{BLOG}">Serene Journal</a></li></ul>
      </div>
      <div>
        <h4>Telehealth</h4>
        <ul><li>Serene Telehealth with Dr. Arora</li><li><a href="tel:{TELE["tel"]}">{TELE["phone"]}</a></li><li><a href="sms:{TELE["tel"]}">Text us</a></li>
        <li><a href="{TELE["spruce"]}" target="_blank" rel="noopener">Message Dr. Arora securely &rsaquo;</a></li><li>Mon&ndash;Fri 9 AM &ndash; 5 PM ET</li></ul>
        <h4 style="margin-top:22px">Follow</h4>
        <ul><li><a href="https://www.instagram.com/serene.wellness.wv" target="_blank" rel="noopener">Instagram</a></li><li><a href="mailto:info@serenemedspas.com">info@serenemedspas.com</a></li></ul>
      </div>
    </div>
    <div class="foot-bottom">
      <div>&copy; 2026 Serene Medical Spa LLC. All rights reserved.</div>
      <div><a href="/privacy-practices/">Privacy Practices</a><a href="/llc-privacy-policy/">Privacy Policy</a><a href="/terms-of-service/">Terms of Service</a><a href="/terms-of-use/">Terms of Use</a><a href="/discrimination/">Nondiscrimination</a><a href="/return-policy/">Returns</a></div>
    </div>
  </div>
</footer>
<div class="mbar"><a class="mbar-call" href="/contact-us/">&#9742;&nbsp; Call</a><a class="mbar-book" href="/#book">Book Now</a></div>'''

SCRIPTS = f'''<script>
(function(){{var io=new IntersectionObserver(function(e){{e.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target);}}}});}},{{threshold:.1}});
document.querySelectorAll('.reveal').forEach(function(el){{io.observe(el);}});
document.querySelectorAll('.nav ul li').forEach(function(li){{var a=li.querySelector(':scope>a'),d=li.querySelector(':scope>.drop');if(!d)return;a.addEventListener('click',function(e){{if(window.innerWidth<=820){{e.preventDefault();li.classList.toggle('open');}}}});}});
var f=document.getElementById('zf-consult');if(f){{var err=document.getElementById('zf-err'),btn=f.querySelector('.zf-btn');
f.addEventListener('submit',function(e){{e.preventDefault();err.textContent='';var bad=[].slice.call(f.querySelectorAll('[required]')).filter(function(i){{return !i.value.trim();}});var em=document.getElementById('zf-em');
if(bad.length){{bad[0].focus();err.textContent='Please fill in the required fields.';return;}}
if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]{{2,}}$/.test(em.value.trim())){{em.focus();err.textContent='Please enter a valid email address.';return;}}
btn.disabled=true;btn.textContent='Sending…';
fetch(f.action,{{method:'POST',body:new URLSearchParams(new FormData(f)),mode:'no-cors',credentials:'omit'}}).then(function(){{f.hidden=true;var d=document.getElementById('zf-done');d.hidden=false;d.scrollIntoView({{behavior:'smooth',block:'center'}});try{{if(window.gtag){{gtag('event','generate_lead',{{event_category:'form',event_label:'consult'}});}}}}catch(x){{}}}}).catch(function(){{f.submit();}});}});}}
}})();
</script>
<!-- Google Ads tag -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GTAG}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GTAG}');
document.addEventListener('click',function(e){{var a=e.target.closest('a[href*="booking.mangomint.com"]');if(a){{try{{gtag('event','conversion',{{'send_to':'{GTAG}/lQdCCL31zvUcEPiLl_gC'}});}}catch(x){{}}}}}},true);</script>
<!-- Meta Pixel -->
<script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','{META_PIXEL}');fbq('track','PageView');</script>
<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={META_PIXEL}&ev=PageView&noscript=1"></noscript>'''

ORG_LD = json.dumps({
    "@context": "https://schema.org", "@type": "MedicalBusiness", "name": "Serene Med Spa", "url": SITE_URL, "logo": SITE_URL + LOGO,
    "image": SITE_URL + "/wp-content/uploads/2024/07/2148574924.jpg", "telephone": "+1-330-460-5915", "email": "info@serenemedspas.com",
    "founder": {"@type": "Person", "name": "Robin Arora, MD"},
    "sameAs": ["https://www.instagram.com/serene.wellness.wv"],
    "department": [
        {"@type": "MedicalBusiness", "name": "Serene Med Spa — Hudson, OH", "url": HUDSON["site"], "telephone": "+1-330-460-5915",
         "address": {"@type": "PostalAddress", "streetAddress": "50 W Streetsboro St, Suite 2", "addressLocality": "Hudson", "addressRegion": "OH", "postalCode": "44236", "addressCountry": "US"}},
        {"@type": "MedicalBusiness", "name": "Serene Med Spa — Barboursville, WV", "url": BARB["site"], "telephone": "+1-304-520-0461",
         "address": {"@type": "PostalAddress", "streetAddress": "1 Chateau Grove Ln", "addressLocality": "Barboursville", "addressRegion": "WV", "postalCode": "25504", "addressCountry": "US"}},
    ]}, ensure_ascii=False)

def esc(s): return html.escape(s or "", quote=True)

def shell(path, title, description, body, og_image=None, noindex=False, extra_head="", ld=None, body_class=""):
    """Wrap page body in the site shell. path like '/telehealth/'."""
    canonical = SITE_URL + path
    og = SITE_URL + (og_image if og_image and og_image.startswith("/") else (og_image or "/wp-content/uploads/2024/07/2148574924.jpg"))
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    ldjson = ""
    for block in ([ORG_LD] if path == "/" else []) + ([ld] if ld else []):
        ldjson += f'<script type="application/ld+json">{block}</script>\n'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Serene Med Spa">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{og}">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/main.css?v=%%CSSV%%">
{ldjson}{extra_head}
</head>
<body class="{body_class}">
{NAV}
<main>
{body}
</main>
{FOOTER}
{SCRIPTS}
</body>
</html>'''

# ------------------------------------------------------------------ reusable blocks
def consult_form(source="serenemedspas.com"):
    return f'''<section class="tint-sand" id="consult">
  <div class="wrap band">
    <div>
      <span class="eyebrow">Get in touch</span>
      <h2>Request a complimentary consultation</h2>
      <p class="lede">In person at either location, or by video. Tell us what you&rsquo;re interested in and our team will reach out within one business day.</p>
      <p class="zf-fine">Please don&rsquo;t include private medical details in this form &mdash; we&rsquo;ll gather anything clinical securely at your visit.</p>
    </div>
    <div>
    <form class="zf" id="zf-consult" action="https://crm.zoho.com/crm/WebToLeadForm" method="POST" accept-charset="UTF-8" novalidate>
      <input type="hidden" name="xnQsjsdp" value="29c1b6f4e6219d1e5682cd0434b1ce181ccda55241b6394ae70c33a7f83e1dfa">
      <input type="hidden" name="xmIwtLD" value="139bc9e7ae4c09a2ea84b820c0c3b10459ed2d907a8c88693956f8d217af21d20ea75c0d1b75b947bf1bf59cc28d7274">
      <input type="hidden" name="actionType" value="TGVhZHM=">
      <input type="hidden" name="returnURL" value="https://serenemedspas.com/thank-you/">
      <input type="hidden" name="zc_gad" id="zc_gad" value="">
      <input type="hidden" name="Lead Status" value="Not Contacted">
      <input type="hidden" name="LEADCF1" id="zf-src" value="Website form: {source}">
      <input type="text" name="aG9uZXlwb3Q" value="" tabindex="-1" autocomplete="off" class="zf-hp" aria-hidden="true">
      <div class="zf-grid">
        <div class="zf-field"><label for="zf-fn">First name</label><input type="text" id="zf-fn" name="First Name" maxlength="40" autocomplete="given-name"></div>
        <div class="zf-field"><label for="zf-ln">Last name <span>*</span></label><input type="text" id="zf-ln" name="Last Name" maxlength="80" required autocomplete="family-name"></div>
        <div class="zf-field"><label for="zf-em">Email <span>*</span></label><input type="email" id="zf-em" name="Email" maxlength="100" required autocomplete="email" inputmode="email"></div>
        <div class="zf-field"><label for="zf-ph">Phone <span>*</span></label><input type="tel" id="zf-ph" name="Phone" maxlength="30" required autocomplete="tel" inputmode="tel"></div>
        <div class="zf-field zf-full"><label for="zf-loc">Preferred location</label><select id="zf-loc" name="LEADCF3"><option value="">Choose a location</option><option value="Hudson, OH">Hudson, OH</option><option value="Barboursville, WV">Barboursville, WV</option><option value="Telehealth">Telehealth (video visit)</option></select></div>
        <div class="zf-field zf-full"><label for="zf-msg">What are you interested in?</label><textarea id="zf-msg" name="Description" rows="4" placeholder="e.g. wrinkle relaxers, a weight-management consult, Morpheus8 &hellip;"></textarea></div>
      </div>
      <div class="zf-actions"><button type="submit" class="btn zf-btn">Request Consultation</button><span class="zf-err" id="zf-err" role="alert"></span></div>
      <p class="zf-fine">By submitting, you agree to be contacted by Serene Med Spa about your request. We never sell your information.</p>
    </form>
    <div class="zf-done" id="zf-done" hidden><h3>Thank you &mdash; we got your request.</h3><p>A member of our team will reach out within one business day. Prefer not to wait? Call <a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a> (Hudson) or <a href="tel:{BARB["tel"]}">{BARB["phone"]}</a> (Barboursville).</p></div>
    </div>
  </div>
</section>'''

def book_band():
    return f'''<section id="book">
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">Book online</span><h2>Choose your location</h2><p class="lede" style="margin:0 auto">Same-week appointments at both offices. Video visits for weight management and hormone care through Serene Telehealth.</p></div>
    <div class="grid g3">
      <div class="card"><span class="state" style="font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal-500);font-weight:600">Ohio</span><h3>Hudson</h3><p>{HUDSON["addr1"]}<br>{HUDSON["addr2"]}<br><a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a></p><div class="actions"><a class="btn btn-sm" href="{HUDSON["book"]}" target="_blank" rel="noopener">Book Hudson</a><a class="btn btn-sm btn-outline" href="{HUDSON["site"]}">Visit site</a></div></div>
      <div class="card"><span class="state" style="font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal-500);font-weight:600">West Virginia</span><h3>Barboursville</h3><p>{BARB["addr1"]}<br>{BARB["addr2"]}<br><a href="tel:{BARB["tel"]}">{BARB["phone"]}</a></p><div class="actions"><a class="btn btn-sm" href="{BARB["book"]}" target="_blank" rel="noopener">Book Barboursville</a><a class="btn btn-sm btn-outline" href="{BARB["site"]}">Visit site</a></div></div>
      <div class="card"><span class="state" style="font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal-500);font-weight:600">OH &middot; WV &middot; KY &middot; FL</span><h3>Telehealth</h3><p>Weight management, hormone therapy &amp; wellness by secure video with Dr. Robin Arora.<br><a href="tel:{TELE["tel"]}">{TELE["phone"]}</a></p><div class="actions"><a class="btn btn-sm" href="{TELE["spruce"]}" target="_blank" rel="noopener">Start a visit</a><a class="btn btn-sm btn-outline" href="/telehealth/">Learn more</a></div></div>
    </div>
  </div>
</section>'''

def page_hero(title, lede="", crumbs=None, eyebrow=""):
    c = ""
    if crumbs:
        c = '<div class="crumbs">' + " &rsaquo; ".join(f'<a href="{h}">{t}</a>' if h else t for h, t in crumbs) + '</div>'
    return f'''<section class="page-hero"><div class="wrap">{c}{f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ''}<h1>{title}</h1>{f'<p class="lede">{lede}</p>' if lede else ''}</div></section>'''
