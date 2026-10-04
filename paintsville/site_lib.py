# -*- coding: utf-8 -*-
"""site_lib.py — constants, CSS, page shell and reusable components for serenemedspaky.com (Serene Med Spa Paintsville, KY).

Design system is the Serene v2 system shared with serenemedspas.com (Noto Serif Display + Poppins + Oooh Baby,
forest green / lavender / white, pill buttons, uppercase letter-spaced labels). Main-site-only features
(location chooser, Mangomint, Zoho newsletter, ad pixels) are intentionally left out.

Everything Robin is likely to edit lives in the CONSTANTS block below.
"""
import html, json, re

# ================================================================== CONSTANTS (edit here)
SITE_URL = "https://serenemedspaky.com"
BRAND = "Serene Med Spa"
SITE_NAME = "Serene Med Spa Paintsville KY"
LEGAL = "Serene Medical Spa LLC"

ADDR1 = "705 Broadway St, Suite 2"
CITY, STATE, ZIP = "Paintsville", "KY", "41240"
ADDR2 = f"{CITY}, {STATE} {ZIP}"
GEO = {"lat": 37.8145, "lng": -82.8071}          # approximate; refine from Google Business Profile

PHONE = "(606) 963-0001"     # confirmed by Robin (Sep 30, 2026)
HOURS = "Mon–Fri 9:00 AM – 5:00 PM"   # confirmed by Robin; used in footer, contact page and JSON-LD
HOURS_LD = ["Mo-Fr 09:00-17:00"]      # keep in sync with HOURS (schema.org openingHours format)
EMAIL = "info@serenemedspas.com"

BOOK_URL = "https://www.vagaro.com/serenemedspapaintsville"  # Vagaro listing for Serene Med Spa Paintsville (slug set by Katrina; rename in Vagaro Business Profile → update here)
JOTFORM_ID = "262724028776060"  # Jotform "Serene Med Spa Paintsville — Consultation Request" (notifications → info@serenemedspas.com)
GBP_REVIEW_URL = "https://g.page/r/CffoOTxD0IVvEBM/review"  # Google Business Profile "write a review" link (set Oct 1 2026)
GA4_ID = "G-VKGVG2NGBX"      # GA4 web stream "Serene Med Spa Paintsville (serenemedspaky.com)", stream 16039580534, property 446740170 (same property as serenemedspas.com; created Oct 4 2026)
META_PIXEL_ID = "475660982946848"  # Serene Med Spa business Meta pixel (same as serenemedspas.com; set Oct 3 2026)

MAP_QUERY = "705+Broadway+St+Suite+2,+Paintsville,+KY+41240"
MAP_LINK = f"https://maps.google.com/maps?q={MAP_QUERY}"
MAP_EMBED = f"https://www.google.com/maps?q={MAP_QUERY}&output=embed"

SISTER = [("https://serenemedspas.com/", "Serene Med Spa (main site)"),
          ("https://serenemedspas.com/hudson/", "Serene Hudson, OH"),
          ("https://serenemedspas.com/barboursville/", "Serene Barboursville, WV"),
          ("https://blog.serenemedspas.com/", "Serene blog")]
FACEBOOK_URL = "https://www.facebook.com/profile.php?id=61590974563966"  # Serene Med Spa Paintsville page (Katrina created; Robin admin since Oct 1 2026)
SAME_AS = [u for u, _ in SISTER] + [MAP_LINK, FACEBOOK_URL]

SERVICE_AREA = ["Paintsville", "Johnson County", "Prestonsburg", "Pikeville", "Salyersville", "Louisa", "Ashland"]

LOGO = "/img/serene-logo.png"
OG_DEFAULT = "/img/katrina-optimas.jpg"
FONTS = "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Noto+Serif+Display:wght@400;500&family=Oooh+Baby&display=swap"

def tel_href(p=PHONE):
    return "tel:+1" + re.sub(r"\D", "", p)

def esc(s): return html.escape(s or "", quote=True)

def text_of(s):
    """Strip tags and unescape entities — for alt text / JSON-LD."""
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

# ================================================================== CSS
CSS = r"""
:root{
  --forest:#10322F;--forest-700:#1B4A44;--forest-500:#3E7F78;--mint:#DDEBE5;
  --lav:#C4C7E6;--lav-100:#ECEDF7;--grey:#F5F7FA;--white:#fff;
  --ink:#121417;--ink-soft:#4B5563;--muted:#8E919C;--rule:#E5E7EB;--gold:#C9A56B;
  --shadow:0 20px 50px -24px rgba(16,50,47,.35);--r:20px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Poppins',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:#fff;line-height:1.7;font-weight:400;font-size:16px;overflow-x:hidden}
h1,h2,h3,h4{font-family:'Noto Serif Display',Georgia,serif;font-weight:400;line-height:1.08;color:var(--forest)}
h1,h2{text-transform:uppercase;letter-spacing:.035em}
h1{font-size:clamp(2.2rem,5vw,4.2rem)}h2{font-size:clamp(1.75rem,3.2vw,2.6rem)}h3{font-size:1.45rem;letter-spacing:.01em}h4{font-size:1.05rem;font-family:'Poppins',sans-serif;font-weight:600}
p{margin:0 0 1em}
a{color:var(--forest-700);text-decoration:none}
img{max-width:100%;height:auto;display:block}
.wrap{max-width:1240px;margin:0 auto;padding:0 24px}
.narrow{max-width:820px}
section{padding:84px 0}
.script{font-family:'Oooh Baby',cursive;font-size:clamp(1.6rem,2.6vw,2.3rem);color:var(--forest-500);text-transform:none;letter-spacing:0;line-height:1.1;display:block;margin-bottom:6px}
.eyebrow{display:inline-block;font-size:.68rem;letter-spacing:.24em;text-transform:uppercase;font-weight:600;color:var(--forest);background:var(--lav-100);padding:7px 14px;border-radius:4px;margin-bottom:18px}
.lede{font-size:1.1rem;color:var(--ink-soft);max-width:62ch;line-height:1.75}
.section-head{max-width:760px;margin-bottom:44px}
.section-head.center{margin-left:auto;margin-right:auto;text-align:center}
.section-head.center .lede{margin:0 auto}
.btn{display:inline-block;background:var(--forest);color:#fff;padding:17px 34px;border-radius:40px;font-size:.76rem;letter-spacing:.2em;text-transform:uppercase;font-weight:600;transition:.25s;border:1.5px solid var(--forest);cursor:pointer;line-height:1.2;text-align:center;font-family:'Poppins',sans-serif}
.btn:hover{background:var(--forest-700);border-color:var(--forest-700);transform:translateY(-2px);box-shadow:var(--shadow)}
.btn-outline{background:transparent;color:var(--forest)}
.btn-outline:hover{background:var(--forest);color:#fff}
.btn-ghost{background:transparent;border-color:rgba(255,255,255,.85);color:#fff}
.btn-ghost:hover{background:#fff;color:var(--forest);border-color:#fff}
.btn-lav{background:var(--lav);border-color:var(--lav);color:var(--forest)}
.btn-lav:hover{background:#fff;border-color:#fff;color:var(--forest)}
.btn-sm{padding:12px 22px;font-size:.7rem}
.tint-sand{background:var(--grey)}.tint-teal{background:var(--forest);color:#fff}.tint-teal h2,.tint-teal h3{color:#fff}.tint-teal .eyebrow{background:rgba(255,255,255,.12);color:#fff}.tint-teal .lede{color:rgba(255,255,255,.82)}.tint-teal a:not(.btn){color:#fff;text-decoration:underline;text-underline-offset:3px}
.tint-sage{background:var(--lav-100)}.tint-lav{background:var(--lav)}
.grid{display:grid;gap:24px}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.g5{grid-template-columns:repeat(5,minmax(0,1fr))}
.card{background:#fff;border:1px solid var(--rule);border-radius:var(--r);padding:30px;transition:.25s}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:transparent}
.card h3{margin-bottom:8px}.card p{color:var(--ink-soft);margin-bottom:12px}
.card .more{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;font-weight:600}
.card .price{font-family:'Noto Serif Display',serif;font-size:1.6rem;color:var(--forest);display:block;margin:4px 0 6px}
.actions{display:flex;gap:10px;flex-wrap:wrap}
/* header */
.promo{background:var(--lav);color:var(--forest);text-align:center;font-size:.8rem;letter-spacing:.02em;padding:9px 16px;font-weight:500}
.promo a{color:var(--forest);text-decoration:underline;text-underline-offset:3px}
header{position:sticky;top:0;z-index:60;background:#fff;border-bottom:1px solid var(--rule)}
.nav{display:flex;align-items:center;justify-content:space-between;height:84px;gap:18px;position:relative}
.nav .logo img{height:52px;width:auto}
.nav ul{display:flex;gap:2px;list-style:none;align-items:center;flex:1;justify-content:center}
.nav ul li{position:relative}
.nav ul a{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--ink);font-weight:600;padding:12px 13px;display:block;white-space:nowrap;transition:.2s;border-bottom:2px solid transparent}
.car{display:inline-block;width:5px;height:5px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(45deg);margin:0 0 3px 7px;opacity:.7;vertical-align:middle;transition:.2s}
.nav ul li:hover>a>.car{transform:rotate(225deg);margin-bottom:0}
.nav ul li:hover>a,.nav ul a:hover{color:var(--forest-500)}
.drop{position:absolute;top:100%;left:0;min-width:260px;background:#fff;border:1px solid var(--rule);border-radius:0 0 16px 16px;padding:12px;box-shadow:var(--shadow);display:none;z-index:70}
.nav ul li.has-mega{position:static}.drop.mega{min-width:0;width:min(860px,calc(100vw - 32px));display:none;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 28px;padding:26px 30px 28px;left:50%;transform:translateX(-50%)}
.nav li:hover>.drop{display:block}.nav li:hover>.drop.mega{display:grid}
.nav .drop a{text-transform:none;letter-spacing:0;font-size:.9rem;line-height:1.35;padding:7px 8px;font-weight:400;border:0;color:var(--ink-soft);white-space:normal}
.nav .drop a:hover{color:var(--forest);background:var(--grey);border-radius:6px}
.drop h5{font-family:'Poppins',sans-serif;font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin:4px 8px 8px}
.nav .drop .view-all{font-weight:600;color:var(--forest);margin-top:4px}
.nav-right{display:flex;align-items:center;gap:10px;flex:0 0 auto}
.nav .btn{padding:14px 26px;font-size:.7rem}
.nav .tel{font-size:.78rem;font-weight:600;color:var(--forest);letter-spacing:.04em;white-space:nowrap}
.menu-toggle{display:none;background:none;border:0;font-size:1.8rem;color:var(--forest);cursor:pointer}
.cred-bar{border-top:1px solid var(--rule);background:#fff}
.cred-bar .wrap{display:flex;justify-content:center;align-items:center;min-height:34px;padding-top:4px;padding-bottom:4px}
.cred-link{display:inline-flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:6px 10px;font-size:.72rem;line-height:1.3;color:var(--ink-soft);text-align:center}
.cred-link b{color:var(--forest);font-weight:600}
.cred-link img{width:26px;height:26px;display:block;flex:0 0 auto}
.cred-verify{color:var(--forest);text-decoration:underline;text-underline-offset:2px}
.cred-short{display:none}
@media (max-width:640px){.cred-long{display:none}.cred-short{display:inline}.cred-link{flex-wrap:nowrap;font-size:.68rem;gap:8px}.cred-bar .wrap{min-height:30px}}
/* home hero (split) */
.hero{background:var(--forest);color:#fff;padding:0;overflow:hidden}
.hero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center;min-height:82vh}
.hero-copy{padding:72px 0}
.hero h1{color:#fff;max-width:14ch}
.hero .script{color:#DDE0F5}
.hero .lede{color:rgba(255,255,255,.88);font-size:1.12rem;margin:22px 0 32px}
.hero .eyebrow{background:rgba(255,255,255,.14);color:#fff}
.hero-cta{display:flex;gap:12px;flex-wrap:wrap}
.hero-chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:36px}
.chip{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.4);padding:8px 14px;border-radius:30px;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;font-weight:500}
.hero-fig{position:relative;height:100%;min-height:520px}
.hero-fig img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top;border-radius:0 0 0 220px}
.hero-fig .tag{position:absolute;left:24px;bottom:28px;background:#fff;color:var(--forest);border-radius:16px;padding:14px 18px;box-shadow:var(--shadow);max-width:280px}
.hero-fig .tag b{display:block;font-family:'Noto Serif Display',serif;font-size:1.15rem;line-height:1.2}
.hero-fig .tag span{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:600}
/* trust strip */
.trust{background:var(--lav);padding:16px 0}
.trust .wrap{display:flex;justify-content:space-around;gap:16px;flex-wrap:wrap}
.trust span{font-size:.7rem;letter-spacing:.22em;text-transform:uppercase;font-weight:600;color:var(--forest);display:flex;align-items:center;gap:10px}
.trust span::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--forest)}
/* interior page hero */
.page-hero{background:var(--grey);padding:64px 0 52px}
.page-hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center}
.page-hero h1{max-width:18ch}
.page-hero .lede{margin:18px 0 26px}
.page-hero img{width:100%;aspect-ratio:5/4;object-fit:cover;object-position:center 15%;border-radius:var(--r);box-shadow:var(--shadow)}
.page-hero.plain{text-align:center}.page-hero.plain .wrap{display:block}.page-hero.plain .actions{justify-content:center}.page-hero.plain h1,.page-hero.plain .lede,.page-hero.plain .crumbs{margin-left:auto;margin-right:auto}
.crumbs{font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:20px}
.crumbs a{color:var(--muted)}
.price-pill{display:inline-flex;align-items:baseline;gap:8px;background:#fff;border:1px solid var(--rule);border-radius:40px;padding:10px 20px;margin-bottom:22px}
.price-pill b{font-family:'Noto Serif Display',serif;font-size:1.4rem;color:var(--forest);font-weight:400}
.price-pill span{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);font-weight:600}
/* arches */
.arch{display:block;text-align:center;position:relative;transition:.3s}
.arch img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:999px 999px 26px 26px;filter:saturate(.9)}
.arch span{display:inline-block;background:var(--forest);color:#fff;font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;font-weight:600;padding:10px 16px;border-radius:30px;margin-top:-22px;position:relative;box-shadow:0 8px 20px -10px rgba(0,0,0,.5)}
.arch:hover{transform:translateY(-6px)}
/* two-column band */
.band{display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:center}
.band img{width:100%;border-radius:var(--r);object-fit:cover}
.band.flip{grid-template-columns:.8fr 1.2fr}.band.top{align-items:start}
/* providers */
.prov{display:grid;grid-template-columns:1fr 1.2fr;gap:0;overflow:hidden;background:#fff;border-radius:var(--r);border:1px solid var(--rule)}
.prov img{width:100%;height:100%;object-fit:cover;object-position:center top;min-height:360px}
.prov .pbody{padding:36px}
.prov .creds{list-style:none;margin:14px 0 20px;display:flex;flex-wrap:wrap;gap:8px}
.prov .creds li{font-size:.74rem;background:var(--lav-100);color:var(--forest);padding:6px 12px;border-radius:30px}
.provcard{text-align:center}
.provcard img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center top;border-radius:var(--r);margin-bottom:18px}
.provcard h3{font-size:1.4rem}
.provcard .role{font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);font-weight:600;display:block;margin-bottom:8px}
/* reviews */
.rev{background:#fff;border:1px solid var(--rule);border-radius:var(--r);padding:34px 30px 28px;position:relative;text-align:center}
.rev::before{content:"\201C";font-family:'Noto Serif Display',serif;font-size:4rem;line-height:1;color:var(--lav);display:block;margin-bottom:-10px}
.rev .stars{color:var(--gold);letter-spacing:2px;margin-bottom:8px}
.rev p{font-size:1rem;color:var(--ink);line-height:1.7}
.rev .who{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:600}
/* faq */
.faq{border-top:1px solid var(--rule)}
.faq details{border-bottom:1px solid var(--rule);padding:20px 0}
.faq summary{cursor:pointer;font-family:'Poppins',sans-serif;font-size:1.05rem;font-weight:600;color:var(--forest);list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--forest-500);font-size:1.5rem;line-height:1;flex:0 0 auto}
.faq details[open] summary::after{content:"\2013"}
.faq details p{margin-top:10px;color:var(--ink-soft)}
/* steps + checklist */
.steps{counter-reset:s}
.step{display:flex;gap:18px;align-items:flex-start;padding:18px 0;border-bottom:1px solid var(--rule)}
.step b{counter-increment:s;flex:0 0 42px;width:42px;height:42px;border-radius:50%;background:var(--lav-100);color:var(--forest);display:inline-flex;align-items:center;justify-content:center;font-family:'Noto Serif Display',serif;font-size:1.15rem;font-weight:400}
.step b::before{content:counter(s)}
.step h4{margin-bottom:2px;color:var(--forest)}.step p{color:var(--ink-soft);margin:0;font-size:.98rem}
.checks{list-style:none;columns:2;gap:28px}
.checks li{padding:8px 0 8px 30px;position:relative;break-inside:avoid;color:var(--ink)}
.checks li::before{content:"";position:absolute;left:0;top:14px;width:16px;height:16px;border-radius:50%;background:var(--lav);box-shadow:inset 0 0 0 4px #fff,0 0 0 1.5px var(--forest-500)}
/* offer / pricing */
.offer{background:var(--lav-100);border-radius:var(--r);padding:44px;display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center}
.offer h2{font-size:clamp(1.8rem,3vw,2.5rem)}
.offer .big{font-family:'Noto Serif Display',serif;font-size:clamp(3rem,6vw,5.5rem);line-height:1;color:var(--forest);text-transform:uppercase}
.pricetable{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.pricetable th,.pricetable td{padding:14px 18px;text-align:left;border-bottom:1px solid var(--rule);vertical-align:top}
.pricetable th{font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);font-weight:600;background:var(--grey)}
.pricetable td.p{font-family:'Noto Serif Display',serif;font-size:1.15rem;color:var(--forest);white-space:nowrap;text-align:right}
.pricetable td small{display:block;color:var(--muted);font-size:.82rem}
.pricetable tr:last-child td{border-bottom:0}
.pricewrap{border-radius:var(--r);overflow:hidden;border:1px solid var(--rule)}
.pricewrap .pricetable{border:0}
.fine{font-size:.82rem;color:var(--muted)}
.disclaim{font-size:.82rem;color:var(--ink-soft);background:var(--lav-100);border-left:4px solid var(--lav);padding:14px 18px;border-radius:0 12px 12px 0;margin:22px 0}
/* logos */
.logos{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:22px 44px}
.logos img{height:34px;width:auto;opacity:.82;filter:grayscale(1) contrast(1.05);transition:.25s}
.logos img:hover{opacity:1;filter:none}
.logos img.tall{height:64px}.logos img.mid{height:44px}
.badges{display:flex;flex-wrap:wrap;justify-content:center;gap:18px;margin-top:34px}
.badge{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--rule);border-radius:60px;padding:8px 18px 8px 8px}
.badge img{height:44px;width:auto}
.badge b{display:block;font-size:.86rem;color:var(--forest)}
.badge small{font-size:.72rem;color:var(--muted)}
/* location */
.loc{display:grid;grid-template-columns:1.05fr .95fr;overflow:hidden;background:#fff;border:1px solid var(--rule);border-radius:var(--r)}
.loc .loc-body{padding:36px}
.loc .map{width:100%;height:100%;min-height:320px;border:0;display:block}
.loc dl{margin:14px 0 22px}.loc dt{font-size:.66rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-top:12px}
.loc dd{font-size:1.02rem;font-weight:500}
.state{font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;color:var(--forest-500);font-weight:600}
/* prose */
.prose{max-width:760px}
.prose h2{margin:44px 0 14px;font-size:1.7rem}.prose h3{margin:30px 0 10px}
.prose p,.prose li{font-size:1.05rem;color:var(--ink);line-height:1.8}
.prose ul,.prose ol{margin:0 0 1.2em 1.4em}
.prose a{text-decoration:underline;text-underline-offset:3px}
/* form embed */
.jf{border:1px solid var(--rule);border-radius:var(--r);overflow:hidden;background:#fff}
.jf iframe{width:100%;min-height:720px;border:0;display:block}
/* footer */
footer{background:var(--forest);color:rgba(255,255,255,.82);padding:72px 0 28px}
.foot-grid{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1.2fr);gap:36px}
footer h4{color:#fff;font-family:'Poppins',sans-serif;font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;margin-bottom:16px}
footer ul{list-style:none}footer li{margin:7px 0;font-size:.92rem}
footer a{color:rgba(255,255,255,.82)}footer a:hover{color:#fff}
footer .flogo{height:56px;width:auto;margin-bottom:14px;filter:brightness(0) invert(1)}
.foot-brand p{max-width:440px;font-size:.95rem}
.foot-bottom{border-top:1px solid rgba(255,255,255,.14);margin-top:40px;padding-top:22px;font-size:.78rem;color:rgba(255,255,255,.6)}
.foot-bottom .row{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-top:12px}
.foot-bottom a{color:rgba(255,255,255,.7);margin-right:14px}
/* sticky mobile bar */
.mbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:80;background:#fff;border-top:1px solid var(--rule);padding:10px 12px;gap:10px}
.mbar a{flex:1;text-align:center;padding:14px;border-radius:30px;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;font-weight:600}
.mbar-call{border:1.5px solid var(--forest);color:var(--forest)}.mbar-book{background:var(--forest);color:#fff}
/* reveal */
.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
.sr{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
/* responsive */
@media (max-width:1180px){.foot-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.nav ul a{padding:12px 8px;letter-spacing:.1em;font-size:.68rem}.nav .tel{display:none}.g5{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:1040px){
  .nav ul{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;flex-direction:column;align-items:stretch;padding:12px 16px 20px;border-bottom:1px solid var(--rule);gap:2px;max-height:calc(100vh - 84px);overflow:auto}
  .nav ul.open{display:flex}
  .nav ul a{padding:12px 6px;border-bottom:1px solid var(--rule);font-size:.72rem;letter-spacing:.14em;display:flex;align-items:center;justify-content:space-between}
  .nav ul li:hover>.drop,.nav ul li:hover>.drop.mega{display:none}
  .nav ul li.open>.drop,.nav ul li.open>.drop.mega{display:block;position:static;transform:none;min-width:0;width:auto;box-shadow:none;border:0;padding:6px 0 10px 14px}
  .menu-toggle{display:block}
  .g4{grid-template-columns:repeat(2,minmax(0,1fr))}.offer{grid-template-columns:1fr}
}
@media (max-width:900px){
  section{padding:56px 0}
  .g2,.g3{grid-template-columns:1fr}.loc,.prov,.band,.band.flip,.page-hero .wrap{grid-template-columns:1fr}.loc .map{min-height:240px}
  .hero .wrap{grid-template-columns:1fr;min-height:0;gap:0}.hero-copy{padding:56px 0 40px}.hero-fig{min-height:0;height:auto;margin:0 -24px}.hero-fig img{position:static;aspect-ratio:4/3;border-radius:0}.hero-fig .tag{left:40px;bottom:20px}
  .page-hero{padding:44px 0 40px}.page-hero img{aspect-ratio:16/10}
  .nav{height:72px}.nav .logo img{height:44px}.nav ul{max-height:calc(100vh - 72px)}.nav .btn{display:none}
  .mbar{display:flex}body{padding-bottom:66px}
  .trust .wrap{justify-content:flex-start}
  .checks{columns:1}.logos img{height:22px}.logos img.tall{height:48px}.logos img.mid{height:34px}
  .prov img{max-height:420px}
}
@media (max-width:560px){.g4,.g5{grid-template-columns:repeat(2,minmax(0,1fr))}.hero-chips{display:none}.foot-grid{grid-template-columns:minmax(0,1fr)}.offer{padding:28px}.arch span{font-size:.58rem;padding:8px 12px}.pricetable th,.pricetable td{padding:12px 12px}.hero-fig .tag{display:none}}
"""

# ================================================================== NAV / FOOTER
# (href, label) — the service list is shared by the mega menu, footer and sitemap. Filled by content.py at import time.
NAV_SERVICES = [
    ("Face & Skin", [("/botox-xeomin/", "Botox & Xeomin"), ("/forma/", "Forma skin tightening"), ("/lumecca-ipl/", "Lumecca IPL photofacial"), ("/morpheus8/", "Morpheus8 RF microneedling")]),
    ("Body & Laser", [("/laser-hair-removal/", "Laser hair removal (DiolazeXL)"), ("/evolvex/", "EvolveX body toning"), ("/intimate-wellness/", "Intimate & pelvic wellness")]),
    ("Wellness", [("/hormone-therapy/", "Biote hormone therapy"), ("/iv-therapy/", "IV therapy"), ("/pricing/", "Full price list"), ("/services/", "View all treatments")]),
]
ABOUT_MENU = [("/about/", "Meet the team"), ("/specials/", "Specials"), ("/contact/", "Contact & directions")]


def _mega():
    cols = []
    for cat, items in NAV_SERVICES:
        links = "".join(f'<a href="{h}" class="view-all">{t}</a>' if t.startswith("View all") else f'<a href="{h}">{t}</a>' for h, t in items)
        cols.append(f'<div><h5>{cat}</h5>{links}</div>')
    return '<div class="drop mega">' + "".join(cols) + '</div>'

def _drop(items):
    return '<div class="drop">' + "".join(f'<a href="{h}">{t}</a>' for h, t in items) + '</div>'

PROMO = '<div class="promo">&#10022; Now open in Paintsville &mdash; <a href="/specials/">see our current specials</a> or <a href="' + BOOK_URL + '" target="_blank" rel="noopener">book online</a></div>'

def nav():
    return PROMO + f'''<header>
  <div class="wrap nav">
    <a class="logo" href="/"><img src="{LOGO}" alt="{BRAND} Paintsville, KY" width="186" height="104"></a>
    <ul id="menu">
      <li class="has-mega"><a href="/services/">Treatments<i class="car"></i></a>{_mega()}</li>
      <li><a href="/pricing/">Pricing</a></li>
      <li><a href="/specials/">Specials</a></li>
      <li><a href="/about/">About<i class="car"></i></a>{_drop(ABOUT_MENU)}</li>
      <li><a href="/contact/">Contact</a></li>
    </ul>
    <div class="nav-right">
      <a class="tel" href="{tel_href()}">{PHONE}</a>
      <a class="btn" href="{BOOK_URL}" target="_blank" rel="noopener">Book Online</a>
      <button class="menu-toggle" aria-label="Menu" aria-controls="menu" aria-expanded="false" onclick="var m=document.getElementById('menu');m.classList.toggle('open');this.setAttribute('aria-expanded',m.classList.contains('open'))">&#9776;</button>
    </div>
  </div>
  <div class="cred-bar"><div class="wrap"><a class="cred-link" href="https://badges.abim.org/5fd362be-e972-4798-ad03-bc41774dc4c6" target="_blank" rel="noopener" title="Verify Dr. Arora&rsquo;s ABIM board certification"><img src="/img/badges/abim-board-certified.png" alt="American Board of Internal Medicine — Board Certified" width="26" height="26"><span><b>Medical Director Robin Arora, MD</b> &middot; <span class="cred-long">Board Certified, American Board of Internal Medicine</span><span class="cred-short">ABIM Board Certified</span></span><span class="cred-verify">Verify</span></a></div></div>
</header>'''

DISCLAIMER = ("Individual results vary. The information on this website is for general education and is not medical advice; it does not create a provider&ndash;patient relationship. "
              "All treatments are provided after an in-person consultation and are subject to medical candidacy. Botox&reg; is a registered trademark of Allergan; Xeomin&reg; of Merz Pharmaceuticals; "
              "Optimas, Lumecca, Forma, DiolazeXL, Morpheus8, EvolveX, EmpowerRF, VTone, FormaV and Morpheus8V are trademarks of InMode; Biote&reg; is a registered trademark of BioTE Medical.")

def footer():
    services = [x for _, items in NAV_SERVICES for x in items if not x[1].startswith("View all") and x[0] != "/pricing/"]
    review = f'<li><a href="{GBP_REVIEW_URL}" target="_blank" rel="noopener">Leave a Google review</a></li>' if GBP_REVIEW_URL and GBP_REVIEW_URL != "TODO" else '<li><a href="/contact/#review">Leave a Google review</a></li>'
    return f'''<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img class="flogo" src="{LOGO}" alt="{BRAND}" width="186" height="104">
        <p>Serene Med Spa Paintsville is a physician-directed medical spa serving Paintsville, Johnson County and Eastern Kentucky &mdash; injectables, InMode laser and radiofrequency treatments, women&rsquo;s wellness, hormone therapy and IV therapy, led by Katrina Watkins, NP.</p>
        <p style="font-size:.82rem;color:rgba(255,255,255,.6);margin:0">Medical Director: Robin Arora, MD, MBA &middot; Board Certified, American Board of Internal Medicine &middot; <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Treatments</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in services)}<li><a href="/pricing/">Full price list</a></li></ul></div>
      <div><h4>Serene</h4><ul><li><a href="/about/">About &amp; providers</a></li><li><a href="/specials/">Specials</a></li><li><a href="/contact/">Contact</a></li>{review}<li style="margin-top:14px;font-weight:600;color:#fff">Our other offices</li>{"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in SISTER)}</ul></div>
      <div><h4>Visit us</h4>
        <ul><li><strong style="color:#fff">{BRAND} &mdash; Paintsville, KY</strong><br>{ADDR1}<br>{ADDR2}</li>
        <li><a href="{tel_href()}">{PHONE}</a></li>
        <li>{HOURS}</li>
        <li><a href="{MAP_LINK}" target="_blank" rel="noopener">Directions</a> &middot; <a href="{BOOK_URL}" target="_blank" rel="noopener">Book online</a></li></ul>
      </div>
    </div>
    <div class="foot-bottom">
      <p style="margin:0;font-size:.76rem;line-height:1.6">{DISCLAIMER}</p>
      <div class="row"><div>&copy; 2026 {LEGAL}. All rights reserved.</div>
      <div><a href="/privacy-policy/">Privacy Policy</a><a href="/terms/">Terms of Use</a><a href="/sitemap.xml">Sitemap</a></div></div>
    </div>
  </div>
</footer>
<div class="mbar"><a class="mbar-call" href="{tel_href()}">&#9742;&nbsp; Call</a><a class="mbar-book" href="{BOOK_URL}" target="_blank" rel="noopener">Book Online</a></div>'''

SCRIPTS = '''<script>
(function(){var io=('IntersectionObserver' in window)?new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{threshold:.1}):null;
document.querySelectorAll('.reveal').forEach(function(el){if(io)io.observe(el);else el.classList.add('in');});
document.querySelectorAll('.nav ul li').forEach(function(li){var a=li.querySelector(':scope>a'),d=li.querySelector(':scope>.drop');if(!d)return;a.addEventListener('click',function(e){if(window.innerWidth<=1040){e.preventDefault();li.classList.toggle('open');}});});
})();
</script>'''

def analytics():
    """Analytics tags — emitted only when the ids above are filled in."""
    out = ""
    if GA4_ID:
        out += (f'<!-- Google tag (GA4) --><script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>'
                f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA4_ID}');</script>")
    else:
        out += "<!-- GA4: set GA4_ID in site_lib.py to enable -->"
    if META_PIXEL_ID:
        out += ("<!-- Meta Pixel --><script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
                f"fbq('init','{META_PIXEL_ID}');fbq('track','PageView');"
                # booking-intent click → Meta 'Lead' (+ GA4 'book_click' when GA4 is on)
                "document.addEventListener('click',function(e){var a=e.target.closest('a[href*=\"vagaro.com\"]');if(a){try{fbq('track','Lead',{content_name:'vagaro_book'});}catch(x){}try{if(window.gtag){gtag('event','book_click',{link_url:a.href});}}catch(x){}}},true);</script>"
                f'<noscript><img height="1" width="1" alt="" style="display:none" src="https://www.facebook.com/tr?id={META_PIXEL_ID}&ev=PageView&noscript=1"></noscript>')
    else:
        out += "<!-- Meta Pixel: set META_PIXEL_ID in site_lib.py to enable -->"
    return out

# ================================================================== JSON-LD
ORG_ID = SITE_URL + "/#business"

def business_ld():
    return {"@context": "https://schema.org", "@type": ["MedicalBusiness", "HealthAndBeautyBusiness", "LocalBusiness"], "@id": ORG_ID,
            "name": SITE_NAME, "alternateName": BRAND + " Paintsville", "url": SITE_URL + "/", "logo": SITE_URL + LOGO, "image": SITE_URL + OG_DEFAULT,
            "telephone": "+1" + re.sub(r"\D", "", PHONE), "email": EMAIL, "priceRange": "$$",
            "address": {"@type": "PostalAddress", "streetAddress": ADDR1, "addressLocality": CITY, "addressRegion": STATE, "postalCode": ZIP, "addressCountry": "US"},
            "geo": {"@type": "GeoCoordinates", "latitude": GEO["lat"], "longitude": GEO["lng"]},
            "hasMap": MAP_LINK, "openingHours": HOURS_LD, "sameAs": SAME_AS,
            "areaServed": [{"@type": "City", "name": c} if c != "Johnson County" else {"@type": "AdministrativeArea", "name": "Johnson County, KY"} for c in SERVICE_AREA],
            "parentOrganization": {"@type": "MedicalBusiness", "name": BRAND, "url": "https://serenemedspas.com/"},
            "founder": {"@type": "Person", "name": "Robin Arora, MD, MBA"},
            "employee": [{"@type": "Person", "name": "Katrina Watkins, NP", "jobTitle": "Nurse Practitioner", "url": SITE_URL + "/about/#katrina"},
                         {"@type": "Person", "name": "Robin Arora, MD, MBA", "jobTitle": "Medical Director", "url": SITE_URL + "/about/#dr-arora"}],
            "potentialAction": {"@type": "ReserveAction", "target": BOOK_URL, "name": "Book online"}}

def breadcrumbs_ld(crumbs):
    """crumbs: list of (href, name); href None for the current page."""
    items = []
    for i, (h, n) in enumerate(crumbs):
        it = {"@type": "ListItem", "position": i + 1, "name": text_of(n)}
        if h: it["item"] = SITE_URL + h
        items.append(it)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def webpage_ld(path, title, description, typ="WebPage"):
    return {"@context": "https://schema.org", "@type": typ, "url": SITE_URL + path, "name": title, "description": description,
            "isPartOf": {"@type": "WebSite", "@id": SITE_URL + "/#website", "name": SITE_NAME, "url": SITE_URL + "/"}, "about": {"@id": ORG_ID}, "inLanguage": "en-US"}

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": text_of(q), "acceptedAnswer": {"@type": "Answer", "text": text_of(a)}} for q, a in faqs]}

# ================================================================== SHELL
def shell(path, title, description, body, og_image=None, noindex=False, ld=None, crumbs=None, extra_head=""):
    """Wrap a page body in the site shell. path like '/forma/'. ld: list of JSON-LD dicts."""
    canonical = SITE_URL + path
    og = SITE_URL + (og_image or OG_DEFAULT)
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    blocks = []
    if path == "/": blocks.append(business_ld())
    blocks += list(ld or [])
    if crumbs and not noindex: blocks.append(breadcrumbs_ld(crumbs))
    if not any(b.get("@type") in ("WebPage", "AboutPage", "ContactPage", "MedicalWebPage", "CollectionPage", "ItemList") for b in blocks if isinstance(b, dict)) and not noindex:
        blocks.append(webpage_ld(path, re.sub(r"\s*\|\s*Serene.*$", "", title), description))
    ldjson = "".join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False, separators=(",", ":")) + '</script>\n' for b in blocks)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{esc(SITE_NAME)}"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{og}">
<meta name="geo.region" content="US-KY"><meta name="geo.placename" content="Paintsville"><meta name="geo.position" content="{GEO['lat']};{GEO['lng']}"><meta name="ICBM" content="{GEO['lat']}, {GEO['lng']}">
<meta name="theme-color" content="#10322F">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="/main.css?v=%%CSSV%%">
{ldjson}{extra_head}
</head>
<body>
{nav()}
<main id="main">
{body}
</main>
{footer()}
{SCRIPTS}
{analytics()}
</body>
</html>'''

# ================================================================== IMAGES
def img(src, alt, cls="", w=None, h=None, lazy=True, sizes="(max-width:900px) 100vw, 50vw"):
    """<img> with srcset (800px variant pre-generated in assets/img/800/) and lazy loading."""
    d, fn = src.rsplit("/", 1)
    srcset = f'{d}/800/{fn} 800w, {src} 1600w'
    dims = (f' width="{w}"' if w else "") + (f' height="{h}"' if h else "")
    return (f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}"{dims}'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + (f' class="{cls}"' if cls else "") + '>')

# ================================================================== COMPONENTS
def crumbs_html(crumbs):
    return '<div class="crumbs">' + " &rsaquo; ".join(f'<a href="{h}">{t}</a>' if h else t for h, t in crumbs) + '</div>'

def page_hero(title, lede="", crumbs=None, eyebrow="", image=None, alt="", price=None, cta=True):
    c = crumbs_html(crumbs) if crumbs else ""
    e = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    pp = f'<div class="price-pill"><b>{price[0]}</b><span>{price[1]}</span></div>' if price else ""
    act = (f'<div class="actions"><a class="btn" href="{BOOK_URL}" target="_blank" rel="noopener">Book Online</a>'
           f'<a class="btn btn-outline" href="{tel_href()}">Call {PHONE}</a></div>') if cta else ""
    if image:
        return (f'<section class="page-hero"><div class="wrap"><div>{c}{e}<h1>{title}</h1>'
                f'{f"<p class=lede>{lede}</p>" if lede else ""}{pp}{act}</div>'
                f'<div>{img(image, alt or text_of(title), lazy=False)}</div></div></section>')
    return f'<section class="page-hero plain"><div class="wrap">{c}{e}<h1>{title}</h1>{f"<p class=lede>{lede}</p>" if lede else ""}{pp}{act}</div></section>'

def faq_section(faqs, title="Frequently asked questions", eyebrow="Good to know"):
    items = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    return f'<section class="tint-sand" id="faq"><div class="wrap narrow"><div class="section-head"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2></div><div class="faq">{items}</div></div></section>'

def price_table(rows, note=True, caption=None):
    """rows: list of (label, price, note) — price is a display string like '$175' or '$10 / unit'."""
    trs = "".join(f'<tr><td>{l}{f"<small>{n}</small>" if n else ""}</td><td class="p">{p}</td></tr>' for l, p, n in rows)
    cap = f'<caption class="sr">{esc(caption)}</caption>' if caption else ""
    out = f'<div class="pricewrap"><table class="pricetable">{cap}<thead><tr><th scope="col">Treatment</th><th scope="col" style="text-align:right">Regular rate</th></tr></thead><tbody>{trs}</tbody></table></div>'
    if note: out += f'<p class="fine" style="margin-top:12px">Regular rates; current specials may apply &mdash; <a href="/specials/">see specials</a> or ask us. Pricing is confirmed at your consultation.</p>'
    return out

def book_band(title="Ready when you are", lede=None, eyebrow="Book in Paintsville"):
    lede = lede or f"Book online through Vagaro in under a minute, or call the clinic at {PHONE}. Complimentary consultations, and we&rsquo;ll always tell you honestly what will and won&rsquo;t work for you."
    return f'''<section class="tint-teal" id="book"><div class="wrap band">
  <div><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><p class="lede">{lede}</p>
  <div class="actions"><a class="btn" style="background:#fff;color:var(--forest);border-color:#fff" href="{BOOK_URL}" target="_blank" rel="noopener">Book Online</a><a class="btn btn-ghost" href="{tel_href()}">Call {PHONE}</a></div></div>
  <div class="card" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);color:#fff"><h3 style="color:#fff">{BRAND} &mdash; Paintsville</h3>
  <p style="color:rgba(255,255,255,.85)">{ADDR1}<br>{ADDR2}</p><p style="color:rgba(255,255,255,.85)">{HOURS}<br><a href="{MAP_LINK}" target="_blank" rel="noopener">Get directions</a></p></div>
</div></section>'''

def also_offered(services, current_slug, limit=3):
    """Cross-link cards to other services (services: list of dicts from content.py)."""
    others = [s for s in services if s["slug"] != current_slug][:limit]
    cards = "".join(f'<a class="card reveal" href="/{s["slug"]}/"><h3>{s["name"]}</h3><p>{s["short"]}</p><span class="more">Learn more &rsaquo;</span></a>' for s in others)
    return f'<section><div class="wrap"><div class="section-head"><span class="eyebrow">Also offered in Paintsville</span><h2>You may also like</h2></div><div class="grid g3">{cards}</div></div></section>'

def logos_strip(title="The technology behind our treatments"):
    items = [("optimasmax-dark.png", "InMode Optimas platform", "tall"), ("lumecca-peak-dark.png", "Lumecca IPL", ""), ("forma-dark.png", "Forma", ""), ("morpheus8-dark.png", "Morpheus8", ""),
             ("evolvex-dark.png", "EvolveX", "tall"), ("empowerrf-dark.png", "EmpowerRF", "tall"), ("formav-dark.png", "FormaV", ""), ("morpheus8v-dark.png", "Morpheus8V", ""),
             ("botox-cosmetic-dark.png", "Botox Cosmetic", "mid"), ("biote-dark.png", "Biote", "mid")]
    imgs = "".join(f'<img src="/img/logos/{f}" alt="{a}" loading="lazy" class="{c}" height="{64 if c == "tall" else (44 if c == "mid" else 34)}">' for f, a, c in items)
    return f'''<section><div class="wrap"><div class="section-head center"><span class="eyebrow">Physician-grade technology</span><h2>{title}</h2><p class="lede">FDA-cleared InMode platforms operated by a board-certified nurse practitioner under physician direction. The same devices used at our Hudson and Barboursville offices.</p></div>
<div class="logos reveal">{imgs}</div>
<div class="badges reveal"><div class="badge"><img src="/img/badges/abim-board-certified.png" alt="ABIM Board Certified" width="44" height="44"><div><b>Board-certified medical director</b><small>Robin Arora, MD &middot; American Board of Internal Medicine</small></div></div>
<div class="badge"><img src="/img/badges/biote-certified-provider.webp" alt="Biote Certified Provider" width="44" height="44"><div><b>Biote Certified Provider</b><small>Hormone optimization with pellet therapy</small></div></div></div></div></section>'''
