# -*- coding: utf-8 -*-
"""site_lib.py — shared shell (head/nav/footer), brand constants and helpers for serenemedspas.com (static)."""
import re, html, os, json

SITE_URL = "https://serenemedspas.com"
LOGO = "/wp-content/uploads/2024/11/Serene_Logo-1024x574.png"
HUDSON = {"name": "Hudson, OH", "addr1": "50 W Streetsboro St, Suite 2", "addr2": "Hudson, OH 44236", "tel": "+13304605915",
          "phone": "(330) 460-5915", "book": "https://booking.mangomint.com/serenemedspa/Hudson", "site": "https://hudson.serenemedspas.com/",
          "map": "https://maps.google.com/maps?q=50+W+Streetsboro+St+Suite+2,+Hudson,+OH+44236", "state": "Ohio"}
BARB = {"name": "Barboursville, WV", "addr1": "1 Chateau Grove Ln", "addr2": "Barboursville, WV 25504", "tel": "+13045200461",
        "phone": "(304) 520-0461", "book": "https://booking.mangomint.com/serenemedspa/Barboursville", "site": "/barboursville/",  # folded into the main domain (Phase 2, Sep 2026)
        "map": "https://maps.google.com/maps?q=1+Chateau+Grove+Ln,+Barboursville,+WV+25504", "state": "West Virginia"}
TELE = {"phone": "(330) 775-2452", "tel": "+13307752452", "spruce": "https://spruce.care/serene-telehealth", "consent": "https://form.jotform.com/262647300953054"}
BLOG = "https://blog.serenemedspas.com/"
GTAG = "AW-788907512"
META_PIXEL = "475660982946848"

# ------------------------------------------------------------------ CSS
CSS = r"""
:root{
  /* Serene design system v2 — modeled on the top US med spa sites (serif display + geometric sans, forest green + lavender + white) */
  --forest:#10322F;--forest-700:#1B4A44;--forest-500:#3E7F78;--mint:#DDEBE5;
  --lav:#C4C7E6;--lav-100:#ECEDF7;--grey:#F5F7FA;--white:#fff;
  --ink:#121417;--ink-soft:#4B5563;--muted:#8E919C;--rule:#E5E7EB;--gold:#C9A56B;
  /* legacy aliases used across templates */
  --teal-900:var(--forest);--teal-700:var(--forest-700);--teal-500:var(--forest-500);--teal-100:var(--mint);
  --sage:#6F9A8F;--sage-100:var(--lav-100);--sand:var(--grey);--paper:#fff;--rose:#D98A8A;
  --shadow:0 20px 50px -24px rgba(16,50,47,.35);
  --r:20px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Poppins',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:#fff;line-height:1.7;font-weight:400;font-size:16px;overflow-x:hidden}
h1,h2,h3,h4{font-family:'Noto Serif Display',Georgia,serif;font-weight:400;line-height:1.08;color:var(--forest)}
h1,h2{text-transform:uppercase;letter-spacing:.035em}
h1{font-size:clamp(2.4rem,5.2vw,4.4rem)}h2{font-size:clamp(1.85rem,3.3vw,2.75rem)}h3{font-size:1.5rem;letter-spacing:.01em}h4{font-size:1.05rem;font-family:'Poppins',sans-serif;font-weight:600}
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
.tint-sand{background:var(--grey)}.tint-teal{background:var(--forest);color:#fff}.tint-teal h2,.tint-teal h3{color:#fff}.tint-teal .eyebrow{background:rgba(255,255,255,.12);color:#fff}.tint-teal .lede{color:rgba(255,255,255,.82)}
.tint-sage{background:var(--lav-100)}
.tint-lav{background:var(--lav)}
.grid{display:grid;gap:24px}
.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.g6{grid-template-columns:repeat(6,minmax(0,1fr))}
.card{background:#fff;border:1px solid var(--rule);border-radius:var(--r);padding:30px;transition:.25s}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:transparent}
.card h3{margin-bottom:8px}
.card p{color:var(--ink-soft);margin-bottom:12px}
.card .more{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;font-weight:600}
/* promo + header */
.promo{background:var(--lav);color:var(--forest);text-align:center;font-size:.8rem;letter-spacing:.02em;padding:9px 16px;font-weight:500}
.promo a{color:var(--forest);text-decoration:underline;text-underline-offset:3px}
header{position:sticky;top:0;z-index:60;background:#fff;border-bottom:1px solid var(--rule)}
.nav{display:flex;align-items:center;justify-content:space-between;height:84px;gap:18px}
.nav .logo img{height:50px;width:auto}
.nav ul{display:flex;gap:2px;list-style:none;align-items:center;flex:1;justify-content:center}
.nav ul li{position:relative}
.nav ul a{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--ink);font-weight:600;padding:12px 13px;display:block;transition:.2s;border-bottom:2px solid transparent}
.nav ul li:hover>a,.nav ul a:hover{color:var(--forest-500)}
.drop{position:absolute;top:100%;left:0;min-width:250px;background:#fff;border:1px solid var(--rule);border-radius:0 0 16px 16px;padding:12px;box-shadow:var(--shadow);display:none;z-index:70}
.drop.mega{min-width:900px;display:none;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px 26px;padding:26px 30px 28px;left:50%;transform:translateX(-50%)}
.nav li:hover>.drop{display:block}.nav li:hover>.drop.mega{display:grid}
.drop a{text-transform:none;letter-spacing:0;font-size:.9rem;padding:7px 8px;font-weight:400;border:0;color:var(--ink-soft)}
.drop a:hover{color:var(--forest);background:var(--grey);border-radius:6px}
.drop h5{font-family:'Poppins',sans-serif;font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin:4px 8px 8px}
.drop .view-all{font-weight:600;color:var(--forest);margin-top:4px}
.nav-right{display:flex;align-items:center;gap:10px;flex:0 0 auto}
.nav .btn{padding:14px 26px;font-size:.7rem}
.locpick{position:relative}
.locpick>button{font:inherit;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--forest);background:#fff;border:1.5px solid var(--forest);border-radius:40px;padding:13px 20px;cursor:pointer;display:flex;align-items:center;gap:8px;line-height:1.2}
.locpick>button:hover{background:var(--grey)}
.locpick .drop{left:auto;right:0;min-width:300px;border-radius:16px;top:calc(100% + 8px);padding:16px}
.locpick.open .drop{display:block}
.locpick .drop b{display:block;font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin:0 8px 8px;font-weight:600}
.locpick .drop button{display:block;width:100%;text-align:left;font:inherit;font-size:.95rem;padding:10px 12px;border:0;background:none;cursor:pointer;border-radius:8px;color:var(--ink)}
.locpick .drop button:hover{background:var(--grey)}
.locpick .drop button small{display:block;font-size:.78rem;color:var(--muted)}
.locpick .drop button.on{background:var(--lav-100)}
.menu-toggle{display:none;background:none;border:0;font-size:1.8rem;color:var(--forest);cursor:pointer}
/* hero */
.hero{position:relative;min-height:86vh;display:flex;align-items:center;color:#fff;
  background:linear-gradient(90deg,rgba(16,50,47,.78) 0%,rgba(16,50,47,.45) 55%,rgba(16,50,47,.1) 100%),url('/wp-content/uploads/2024/07/IMG_0253-1.webp') center/cover no-repeat}
.hero h1{color:#fff;max-width:15ch}
.hero .script{color:#DDE0F5}
.hero .lede{color:rgba(255,255,255,.9);font-size:1.15rem;margin:22px 0 32px}
.hero .eyebrow{background:rgba(255,255,255,.14);color:#fff}
.hero-cta{display:flex;gap:12px;flex-wrap:wrap}
.hero-chips{display:flex;gap:10px;flex-wrap:wrap;margin-top:36px}
.chip{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.4);padding:8px 14px;border-radius:30px;font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;font-weight:500;backdrop-filter:blur(4px)}
/* trust strip */
.trust{background:var(--lav);padding:16px 0}
.trust .wrap{display:flex;justify-content:space-around;gap:16px;flex-wrap:wrap}
.trust span{font-size:.7rem;letter-spacing:.22em;text-transform:uppercase;font-weight:600;color:var(--forest);display:flex;align-items:center;gap:10px}
.trust span::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--forest)}
/* page hero (interior) */
.page-hero{background:var(--grey);padding:72px 0 56px;text-align:center}
.page-hero h1{max-width:22ch;margin:0 auto}
.page-hero .lede{margin:18px auto 0}
.crumbs{font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);margin-bottom:20px}
.crumbs a{color:var(--muted)}
/* treatment category arches */
.arch{display:block;text-align:center;position:relative;transition:.3s}
.arch img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:999px 999px 26px 26px;filter:saturate(.9)}
.arch span{display:inline-block;background:var(--forest);color:#fff;font-size:.66rem;letter-spacing:.22em;text-transform:uppercase;font-weight:600;padding:10px 16px;border-radius:30px;margin-top:-22px;position:relative;box-shadow:0 8px 20px -10px rgba(0,0,0,.5)}
.arch:hover{transform:translateY(-6px)}
/* locations */
.loc{display:grid;grid-template-columns:1.05fr .95fr;overflow:hidden;background:#fff;border:1px solid var(--rule);border-radius:var(--r)}
.loc .loc-body{padding:36px}
.loc .map{width:100%;height:100%;min-height:280px;border:0;display:block}
.loc dl{margin:14px 0 22px}.loc dt{font-size:.66rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-top:12px}
.loc dd{font-size:1.02rem;font-weight:500}
.loc .state,.state{font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;color:var(--forest-500);font-weight:600}
.actions{display:flex;gap:10px;flex-wrap:wrap}
/* location tiles (home) */
.loctile{position:relative;display:flex;flex-direction:column;justify-content:flex-end;min-height:420px;border-radius:var(--r);overflow:hidden;color:#fff;padding:34px;background:var(--forest)}
.loctile img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:.6s}
.loctile:hover img{transform:scale(1.04)}
.loctile::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(16,50,47,0) 30%,rgba(16,50,47,.92) 100%)}
.loctile>*:not(img){position:relative;z-index:1}
.loctile h3{color:#fff;font-size:2.1rem;text-transform:uppercase;letter-spacing:.04em;margin:6px 0 6px}
.loctile p{color:rgba(255,255,255,.85);margin-bottom:16px;max-width:40ch}
.loctile .state{color:#DDE0F5}
/* concern tiles */
.tile{position:relative;border-radius:var(--r);overflow:hidden;aspect-ratio:4/3;display:block}
.tile img{width:100%;height:100%;object-fit:cover;transition:.5s}
.tile:hover img{transform:scale(1.05)}
.tile span{position:absolute;left:0;right:0;bottom:0;padding:18px 20px;color:#fff;font-family:'Noto Serif Display',serif;font-size:1.35rem;text-transform:uppercase;letter-spacing:.04em;background:linear-gradient(transparent,rgba(16,50,47,.9))}
/* tools */
.tool{display:flex;gap:16px;align-items:flex-start;background:#fff;border:1px solid var(--rule);border-radius:16px;padding:20px 22px;transition:.25s}
.tool:hover{border-color:var(--forest-500);box-shadow:var(--shadow);transform:translateY(-2px)}
.tool b{display:inline-flex;width:40px;height:40px;border-radius:50%;background:var(--lav-100);color:var(--forest);align-items:center;justify-content:center;font-family:'Noto Serif Display',serif;font-size:1.2rem;flex:0 0 40px}
.tool>div{min-width:0}.tool h4{margin-bottom:2px;color:var(--forest)}.tool p{font-size:.9rem;color:var(--ink-soft);margin:0}
/* stats */
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;text-align:center}
.stat b{display:block;font-family:'Noto Serif Display',serif;font-size:3rem;color:var(--forest);line-height:1;font-weight:400}
.stat span{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:600}
/* providers */
.prov{display:grid;grid-template-columns:1fr 1.2fr;gap:0;overflow:hidden;background:#fff;border-radius:var(--r);border:1px solid var(--rule)}
.prov img{width:100%;height:100%;object-fit:cover;min-height:360px;max-height:520px}
.prov .pbody{padding:36px}
.prov .creds{list-style:none;margin:14px 0 20px;display:flex;flex-wrap:wrap;gap:8px}
.prov .creds li{font-size:.74rem;background:var(--lav-100);color:var(--forest);padding:6px 12px;border-radius:30px}
.provcard{text-align:center}
.provcard img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:var(--r);margin-bottom:18px}
.provcard h3{font-size:1.4rem}
.provcard .role{font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);font-weight:600;display:block;margin-bottom:8px}
/* reviews */
.rev{background:#fff;border:1px solid var(--rule);border-radius:var(--r);padding:34px 30px 28px;position:relative;text-align:center}
.rev::before{content:"\201C";font-family:'Noto Serif Display',serif;font-size:4rem;line-height:1;color:var(--lav);display:block;margin-bottom:-10px}
.rev .stars{color:var(--gold);letter-spacing:2px;margin-bottom:8px}
.rev p{font-size:1rem;color:var(--ink);line-height:1.7}
.rev .who{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);font-weight:600}
.tint-teal .rev{border-color:transparent}
/* faq */
.faq{border-top:1px solid var(--rule)}
.faq details{border-bottom:1px solid var(--rule);padding:20px 0}
.faq summary{cursor:pointer;font-family:'Poppins',sans-serif;font-size:1.05rem;font-weight:600;color:var(--forest);list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--forest-500);font-size:1.5rem;line-height:1}
.faq details[open] summary::after{content:"\2013"}
.faq details p{margin-top:10px;color:var(--ink-soft)}
/* band */
.band{display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:center}
/* consult form */
.zf{max-width:760px}
.zf-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px 18px}
.zf-full{grid-column:1/-1}
.zf-field label{display:block;font-size:.68rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--forest);margin-bottom:6px}
.zf-field label span{color:#b0163f}
.zf-field input,.zf-field select,.zf-field textarea{width:100%;font:inherit;font-size:1rem;padding:14px 16px;border:1.5px solid var(--rule);border-radius:12px;background:#fff;color:var(--ink);-webkit-appearance:none;appearance:none}
.zf-field input:focus,.zf-field select:focus,.zf-field textarea:focus{outline:none;border-color:var(--forest-500)}
.zf-field textarea{min-height:110px;resize:vertical}
.zf-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;opacity:0}
.zf-actions{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:18px}
.zf-err{color:#b0163f;font-weight:600;font-size:.95rem}
.zf-done{border:1.5px solid var(--forest-500);background:#fff;padding:28px 30px;border-radius:var(--r);max-width:760px}
.zf-fine{font-size:.84rem;color:var(--muted);margin-top:14px}
/* article / prose */
.prose{max-width:760px}
.prose h2{margin:44px 0 14px;font-size:1.7rem}.prose h3{margin:30px 0 10px}.prose h4{margin:22px 0 8px}
.prose p,.prose li{font-size:1.05rem;color:var(--ink);line-height:1.8}
.prose ul,.prose ol{margin:0 0 1.2em 1.4em}
.prose img{border-radius:14px;margin:26px 0}
.prose a{text-decoration:underline;text-underline-offset:3px}
.prose blockquote{border-left:4px solid var(--lav);padding:8px 20px;margin:24px 0;color:var(--ink-soft);font-style:italic}
.prose table{width:100%;border-collapse:collapse;margin:20px 0;font-size:.98rem}
.prose th,.prose td{border:1px solid var(--rule);padding:10px 12px;text-align:left}
.prose th{background:var(--grey)}
.post-hero{padding:56px 0 30px}
.post-hero h1{text-transform:none;letter-spacing:0;font-size:clamp(2rem,4vw,3.2rem)}
.post-meta{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:14px;font-weight:600}
.post-fig img{width:100%;max-height:520px;object-fit:cover;border-radius:var(--r)}
.post-wrap{display:grid;grid-template-columns:1fr 320px;gap:48px;align-items:start}
.side{position:sticky;top:104px}
.side .card{margin-bottom:18px}
.side .card h3{font-size:1.2rem}
.side .card .btn{width:100%;margin-top:8px}
.side .card ul{list-style:none}
.side .card li{padding:6px 0;border-bottom:1px dashed var(--rule);font-size:.95rem}
.related{margin-top:56px}
/* post cards */
.post-card{background:#fff;border:1px solid var(--rule);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;transition:.25s}
.post-card:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.post-card img{width:100%;aspect-ratio:16/10;object-fit:cover}
.post-card .pc-body{padding:22px 24px 24px;display:flex;flex-direction:column;flex:1}
.post-card .pc-cat{font-size:.64rem;letter-spacing:.22em;text-transform:uppercase;color:var(--forest-500);font-weight:600;margin-bottom:8px}
.post-card h3{font-size:1.2rem;margin-bottom:8px;line-height:1.3}
.post-card p{font-size:.92rem;color:var(--ink-soft);flex:1}
.post-card .more{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;font-weight:600}
.cat-nav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 30px;justify-content:center}
.cat-nav a{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;padding:10px 18px;border-radius:30px;border:1.5px solid var(--rule);background:#fff;color:var(--ink-soft);font-weight:600}
.cat-nav a:hover,.cat-nav a.on{border-color:var(--forest);color:var(--forest);background:var(--lav-100)}
/* embedded legacy widgets (contact, telehealth, tools) */
.embed{padding:32px 0 60px}
.embed .wrap>*{margin-left:auto;margin-right:auto}
/* prose accordions (post-care etc.) */
.prose details{border:1px solid var(--rule);border-radius:12px;padding:14px 18px;margin:12px 0;background:#fff}
.prose details summary{cursor:pointer;font-family:'Poppins',sans-serif;font-size:1.02rem;font-weight:600;color:var(--forest);list-style:none;display:flex;justify-content:space-between;gap:16px}
.prose details summary::-webkit-details-marker{display:none}
.prose details summary::after{content:"+";color:var(--forest-500);font-size:1.5rem;line-height:1}
.prose details[open] summary::after{content:"\2013"}
.prose details>*:not(summary){margin-top:10px}
.loc.compact{grid-template-columns:1fr}
.loc.compact .map{display:none}
.filter{display:flex;gap:10px;align-items:center;margin:0 0 22px}
.filter input{flex:1;font:inherit;font-size:1rem;padding:14px 18px;border:1.5px solid var(--rule);border-radius:30px;background:#fff}
.filter input:focus{outline:none;border-color:var(--forest-500)}
.hidden{display:none!important}
/* offer panel */
.offer{background:var(--lav-100);border-radius:var(--r);padding:44px;display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center}
.offer h2{font-size:clamp(1.8rem,3vw,2.5rem)}
.offer .big{font-family:'Noto Serif Display',serif;font-size:clamp(3rem,6vw,5.5rem);line-height:1;color:var(--forest);text-transform:uppercase}
/* footer */
footer{background:var(--forest);color:rgba(255,255,255,.82);padding:72px 0 28px;margin-top:0}
.foot-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1.35fr) minmax(0,1.6fr);gap:36px}
footer h4{color:#fff;font-family:'Poppins',sans-serif;font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;margin-bottom:16px}
footer ul{list-style:none}footer li{margin:7px 0;font-size:.92rem}
footer a{color:rgba(255,255,255,.82)}footer a:hover{color:#fff}
footer img{height:54px;width:auto;margin-bottom:14px;filter:brightness(0) invert(1)}
.newsletter{display:flex;gap:8px;margin:10px 0 8px;min-width:0}
.newsletter input{flex:1 1 0;width:0;font:inherit;font-size:.95rem;padding:13px 16px;border:1.5px solid rgba(255,255,255,.35);border-radius:30px;background:rgba(255,255,255,.06);color:#fff;min-width:0}
.newsletter input::placeholder{color:rgba(255,255,255,.5)}
.newsletter input:focus{outline:none;border-color:#fff}
.newsletter .btn{background:var(--lav);border-color:var(--lav);color:var(--forest);padding:13px 20px;font-size:.66rem}
.newsletter .btn:hover{background:#fff;border-color:#fff}
.foot-brand{grid-column:1/-1;display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap;padding-bottom:36px;border-bottom:1px solid rgba(255,255,255,.14);margin-bottom:36px}
.foot-brand p{max-width:540px;font-size:.95rem}
.foot-bottom{border-top:1px solid rgba(255,255,255,.14);margin-top:40px;padding-top:22px;font-size:.78rem;color:rgba(255,255,255,.6);display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
.foot-bottom a{color:rgba(255,255,255,.7);margin-right:14px}
/* sticky mobile bar */
.mbar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:80;background:#fff;border-top:1px solid var(--rule);padding:10px 12px;gap:10px}
.mbar a{flex:1;text-align:center;padding:14px;border-radius:30px;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;font-weight:600}
.mbar-call{border:1.5px solid var(--forest);color:var(--forest)}.mbar-book{background:var(--forest);color:#fff}
/* reveal */
.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}
/* responsive */
@media (max-width:1180px){.g6{grid-template-columns:repeat(3,minmax(0,1fr))}.drop.mega{min-width:760px;grid-template-columns:repeat(3,minmax(0,1fr))}.foot-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.nav ul a{padding:12px 9px;letter-spacing:.12em}}
@media (max-width:1024px){.g4{grid-template-columns:repeat(2,minmax(0,1fr))}.foot-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.post-wrap{grid-template-columns:1fr}.side{position:static}.offer{grid-template-columns:1fr}.locpick>button span{display:none}}
@media (max-width:900px){
  section{padding:56px 0}
  .g2,.g3{grid-template-columns:1fr}.loc,.prov,.band{grid-template-columns:1fr}.loc .map{min-height:220px}
  .nav{height:72px}.nav .logo img{height:42px}
  .nav ul{display:none;position:absolute;top:72px;left:0;right:0;background:#fff;flex-direction:column;align-items:stretch;padding:12px 16px 20px;border-bottom:1px solid var(--rule);gap:2px;max-height:calc(100vh - 72px);overflow:auto}
  .nav ul.open{display:flex}
  .nav ul a{padding:12px 6px;border-bottom:1px solid var(--rule)}
  .nav ul li:hover>.drop,.nav ul li:hover>.drop.mega{display:none}
  .nav ul li.open>.drop,.nav ul li.open>.drop.mega{display:block;position:static;transform:none;min-width:0;box-shadow:none;border:0;padding:6px 0 10px 14px}
  .nav .btn{display:none}.menu-toggle{display:block}
  .locpick>button{padding:11px 14px}
  .hero{min-height:72vh}
  .zf-grid{grid-template-columns:1fr}
  .mbar{display:flex}body{padding-bottom:66px}.promo-more{display:none}
  .foot-bottom{flex-direction:column}
  .trust .wrap{justify-content:flex-start}
  .loctile{min-height:320px;padding:26px}
}
@media (max-width:560px){.g6{grid-template-columns:repeat(2,minmax(0,1fr))}.g4{grid-template-columns:1fr}.hero-chips{display:none}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.foot-grid{grid-template-columns:minmax(0,1fr)}.offer{padding:28px}.arch span{font-size:.58rem;padding:8px 12px}}
"""

# ------------------------------------------------------------------ NAV / FOOTER
SERVICE_MENU = [
    ("Injectables", [("/botox-treatment-benefits/", "Botox & Wrinkle Relaxers"), ("/filler-injection-treatments-at-serene-med-spa/", "Dermal Fillers"), ("/lip-filler-injection/", "Lip Filler"),
                     ("/cheek-filler-treatment/", "Cheek Filler"), ("/jawline-filler-treatment-at-serene-med-spa/", "Jawline Filler"), ("/kybella-treatment-for-double-chin/", "Kybella"),
                     ("/sculptra/", "Sculptra"), ("/pdo-thread-lift-face-neck/", "PDO Thread Lift")]),
    ("Skin & Laser", [("/morpheus8-rf-microneedling-treatment-at-serene-med-spas/", "Morpheus8"), ("/hydrafacial-treatment-benefits/", "HydraFacial"),
                      ("/microneedling-with-prp/", "Microneedling & PRP"), ("/chemical-peel-treatments-serene-med-spa/", "Chemical Peels"), ("/laser-facial-treatment-at-serene-med-spa/", "Laser Facial"),
                      ("/laser-hair-removal-at-serene-med-spa/", "Laser Hair Removal"), ("/laser-tattoo-removal-process/", "Tattoo Removal"), ("/expert-spider-vein-treatment/", "Spider Veins")]),
    ("Body & Wellness", [("/inmode-evolvex-body-contouring/", "EvolveX Body Contouring"), ("/telehealth/", "Medical Weight Management"), ("/biote-hormone-therapy/", "Hormone Therapy"),
                         ("/the-serene-hydration-bar/", "IV Therapy"), ("/natural-prp-hair-restoration/", "PRP Hair Restoration"), ("/empowerrf-vaginal-rejuvenation-treatment/", "Women's Wellness (EmpowerRF)"),
                         ("/alma-duo-treatment-sexual-wellness/", "Sexual Wellness (Alma Duo)")]),
    ("By Concern", [("/service/#injectables", "Wrinkles & fine lines"), ("/service/#injectables", "Volume loss & contour"), ("/service/#skin", "Acne & scarring"),
                    ("/service/#skin", "Pigmentation & sun damage"), ("/service/#body", "Stubborn fat & body"), ("/service/#hair", "Thinning hair"),
                    ("/recommendation-webapp/", "Not sure? Try the Treatment Finder"), ("/service/", "View all treatments")]),
]
PATIENT_MENU = [("/specials/", "Monthly Specials"), ("/membership/", "Membership"), ("/financing/", "Financing"), ("/telehealth/", "Telehealth"),
                ("/post-care-instructions/", "Post-Care Instructions"), ("/recommendation-webapp/", "Treatment Finder"), ("/reviews/", "Patient Reviews"), ("/blogs/", "Journal")]
ABOUT_MENU = [("/our-story/", "Our Story"), ("/our-providers/", "Our Providers"), ("/about-us/", "About Serene"), ("/reviews/", "Reviews"), ("/contact-us/", "Contact")]
LOCATIONS = [("hudson", HUDSON), ("barboursville", BARB)]

def _drop(items):
    return '<div class="drop">' + "".join(f'<a href="{h}">{t}</a>' for h, t in items) + '</div>'
def _mega():
    cols = []
    for cat, items in SERVICE_MENU:
        links = "".join(f'<a href="{h}" class="view-all">{t}</a>' if (t.startswith("View all") or t.startswith("Not sure")) else f'<a href="{h}">{t}</a>' for h, t in items)
        cols.append(f'<div><h5>{cat}</h5>{links}</div>')
    return '<div class="drop mega">' + "".join(cols) + '</div>'
def _locpick():
    opts = "".join(f'<button type="button" data-set-loc="{k}"><strong>{L["name"]}</strong><small>{L["addr1"]} &middot; {L["phone"]}</small></button>' for k, L in LOCATIONS)
    return ('<div class="locpick" id="locpick"><button type="button" aria-haspopup="true" onclick="this.parentNode.classList.toggle(\'open\')">&#9906; <span data-loc-name>Choose location</span> &#9662;</button>'
            '<div class="drop"><b>Your Serene</b>' + opts + '<button type="button" data-set-loc="telehealth"><strong>Telehealth</strong><small>Video visits &middot; OH, WV, KY &amp; FL</small></button></div></div>')

PROMO = '<div class="promo">&#10022; <a href="/specials/">September specials</a> are here &mdash; buy 2, get 1 free on V-Tone, Forma V, Morpheus V &amp; Evolve X<span class="promo-more"> &middot; New patients: <a href="/#offer">20% off your first visit</a></span></div>'

NAV = PROMO + f'''<header>
  <div class="wrap nav">
    <a class="logo" href="/"><img src="{LOGO}" alt="Serene Med Spa" width="220" height="123"></a>
    <ul id="menu">
      <li><a href="/service/">Treatments &#9662;</a>{_mega()}</li>
      <li><a href="/locations/">Locations &#9662;</a>{_drop([(HUDSON["site"], "Hudson, OH"), (BARB["site"], "Barboursville, WV"), ("/telehealth/", "Telehealth (OH, WV, KY, FL)"), ("/locations/", "All locations")])}</li>
      <li><a href="/specials/">Specials</a></li>
      <li><a href="/membership/">Membership</a></li>
      <li><a href="/specials/">For Patients &#9662;</a>{_drop(PATIENT_MENU)}</li>
      <li><a href="/about-us/">About &#9662;</a>{_drop(ABOUT_MENU)}</li>
    </ul>
    <div class="nav-right">
      {_locpick()}
      <a class="btn" href="/#book" data-loc-book>Book Now</a>
      <button class="menu-toggle" aria-label="Menu" aria-controls="menu" onclick="document.getElementById('menu').classList.toggle('open')">&#9776;</button>
    </div>
  </div>
</header>'''

FOOT_TREATMENTS = [("/botox-treatment-benefits/", "Botox & Dysport"), ("/filler-injection-treatments-at-serene-med-spa/", "Dermal Fillers"), ("/morpheus8-rf-microneedling-treatment-at-serene-med-spas/", "Morpheus8"),
                   ("/hydrafacial-treatment-benefits/", "HydraFacial"), ("/laser-hair-removal-at-serene-med-spa/", "Laser Hair Removal"), ("/telehealth/", "Weight Management"), ("/biote-hormone-therapy/", "Hormone Therapy"), ("/service/", "View all treatments")]

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="{LOGO}" alt="Serene Med Spa" width="220" height="123">
        <div><p>Physician-led medical aesthetics &amp; wellness in Hudson, Ohio and Barboursville, West Virginia &mdash; and by telehealth across Ohio, West Virginia, Kentucky and Florida. Natural results, personalized plans, care you can trust.</p>
        <p style="font-size:.82rem;color:rgba(255,255,255,.6);margin:0">Medical Director: Robin Arora, MD &middot; Board Certified, American Board of Internal Medicine &middot; <a href="mailto:info@serenemedspas.com">info@serenemedspas.com</a></p></div>
      </div>
      <div><h4>Treatments</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in FOOT_TREATMENTS)}</ul></div>
      <div><h4>Patients</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in PATIENT_MENU)}</ul></div>
      <div><h4>About</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in ABOUT_MENU)}<li><a href="https://www.instagram.com/serene.wellness.wv" target="_blank" rel="noopener">Instagram</a></li></ul></div>
      <div><h4>Visit us</h4>
        <ul><li><strong style="color:#fff">Hudson, OH</strong><br>{HUDSON["addr1"]}<br>{HUDSON["addr2"]}<br><a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a> &middot; <a href="{HUDSON["book"]}" target="_blank" rel="noopener">Book</a></li>
        <li style="margin-top:14px"><strong style="color:#fff">Barboursville, WV</strong><br>{BARB["addr1"]}<br>{BARB["addr2"]}<br><a href="tel:{BARB["tel"]}">{BARB["phone"]}</a> &middot; <a href="{BARB["book"]}" target="_blank" rel="noopener">Book</a></li>
        <li style="margin-top:14px"><strong style="color:#fff">Telehealth</strong> &middot; OH, WV, KY, FL<br><a href="tel:{TELE["tel"]}">{TELE["phone"]}</a> &middot; <a href="{TELE["spruce"]}" target="_blank" rel="noopener">Message securely</a></li></ul>
      </div>
      <div><h4>20% off your first visit</h4>
        <p style="font-size:.9rem">Join our list for monthly specials and new treatments. New patients get 20% off their first visit &mdash; any product or service.</p>
        <form class="newsletter" id="zf-news" action="https://crm.zoho.com/crm/WebToLeadForm" method="POST" accept-charset="UTF-8" novalidate>
          <input type="hidden" name="xnQsjsdp" value="29c1b6f4e6219d1e5682cd0434b1ce181ccda55241b6394ae70c33a7f83e1dfa"><input type="hidden" name="xmIwtLD" value="139bc9e7ae4c09a2ea84b820c0c3b10459ed2d907a8c88693956f8d217af21d20ea75c0d1b75b947bf1bf59cc28d7274"><input type="hidden" name="actionType" value="TGVhZHM="><input type="hidden" name="returnURL" value="https://serenemedspas.com/thank-you/">
          <input type="hidden" name="Last Name" value="Email signup"><input type="hidden" name="Lead Status" value="Not Contacted"><input type="hidden" name="LEADCF1" value="Website form: newsletter">
          <input type="email" name="Email" placeholder="Your email" aria-label="Email address" required autocomplete="email" inputmode="email"><button class="btn" type="submit">Subscribe</button>
        </form>
        <p id="zf-news-done" hidden style="font-size:.9rem;color:#fff">Thanks &mdash; you&rsquo;re on the list. Mention the offer when you book.</p>
        <p style="font-size:.72rem;color:rgba(255,255,255,.5);margin:0">Can&rsquo;t be combined with another discount. Unsubscribe any time. <a href="/llc-privacy-policy/">Privacy</a>.</p>
      </div>
    </div>
    <div class="foot-bottom">
      <div>&copy; 2026 Serene Medical Spa LLC. All rights reserved.</div>
      <div><a href="/privacy-practices/">Privacy Practices</a><a href="/llc-privacy-policy/">Privacy Policy</a><a href="/terms-of-service/">Terms of Service</a><a href="/terms-of-use/">Terms of Use</a><a href="/discrimination/">Nondiscrimination</a><a href="/return-policy/">Returns</a></div>
    </div>
  </div>
</footer>
<div class="mbar"><a class="mbar-call" href="/contact-us/" data-loc-tel>&#9742;&nbsp; Call</a><a class="mbar-book" href="/#book" data-loc-book>Book Now</a></div>'''

LOC_JS = json.dumps({
    "hudson": {"name": "Hudson, OH", "book": HUDSON["book"], "tel": HUDSON["tel"], "site": HUDSON["site"]},
    "barboursville": {"name": "Barboursville, WV", "book": BARB["book"], "tel": BARB["tel"], "site": BARB["site"]},
    "telehealth": {"name": "Telehealth", "book": TELE["spruce"], "tel": TELE["tel"], "site": "/telehealth/"}})

SCRIPTS = f'''<script>
(function(){{var LOC={LOC_JS};
function get(){{try{{return localStorage.getItem('serene_loc')||'';}}catch(e){{return '';}}}}
function apply(k){{var L=LOC[k];
document.querySelectorAll('[data-loc-name]').forEach(function(el){{el.textContent=L?L.name:'Choose location';}});
document.querySelectorAll('[data-loc-book]').forEach(function(a){{if(L){{a.href=L.book;a.target='_blank';a.rel='noopener';}}else{{a.href='/#book';a.removeAttribute('target');}}}});
document.querySelectorAll('[data-loc-tel]').forEach(function(a){{a.href=L?'tel:'+L.tel:'/contact-us/';}});
document.querySelectorAll('[data-set-loc]').forEach(function(b){{b.classList.toggle('on',b.getAttribute('data-set-loc')===k);}});
document.querySelectorAll('[data-loc-only]').forEach(function(el){{el.classList.toggle('hidden',!!L&&el.getAttribute('data-loc-only')!==k);}});}}
document.querySelectorAll('[data-set-loc]').forEach(function(b){{b.addEventListener('click',function(){{var k=b.getAttribute('data-set-loc');try{{localStorage.setItem('serene_loc',k);}}catch(e){{}}apply(k);var p=document.getElementById('locpick');if(p)p.classList.remove('open');}});}});
document.addEventListener('click',function(e){{var p=document.getElementById('locpick');if(p&&!p.contains(e.target))p.classList.remove('open');}});
apply(get());
var n=document.getElementById('zf-news');if(n){{n.addEventListener('submit',function(e){{e.preventDefault();var em=n.querySelector('input[type=email]');if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]{{2,}}$/.test(em.value.trim())){{em.focus();return;}}
fetch(n.action,{{method:'POST',body:new URLSearchParams(new FormData(n)),mode:'no-cors',credentials:'omit'}}).then(function(){{n.hidden=true;document.getElementById('zf-news-done').hidden=false;try{{if(window.gtag)gtag('event','generate_lead',{{event_category:'form',event_label:'newsletter'}});}}catch(x){{}}}}).catch(function(){{n.submit();}});}});}}
}})();
</script>
<script>
(function(){{var io=new IntersectionObserver(function(e){{e.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target);}}}});}},{{threshold:.1}});
document.querySelectorAll('.reveal').forEach(function(el){{io.observe(el);}});
document.querySelectorAll('.nav ul li').forEach(function(li){{var a=li.querySelector(':scope>a'),d=li.querySelector(':scope>.drop');if(!d)return;a.addEventListener('click',function(e){{if(window.innerWidth<=900){{e.preventDefault();li.classList.toggle('open');}}}});}});
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
        {"@type": "MedicalBusiness", "name": "Serene Med Spa — Hudson, OH", "url": (SITE_URL + HUDSON["site"]) if HUDSON["site"].startswith("/") else HUDSON["site"], "telephone": "+1-330-460-5915",
         "address": {"@type": "PostalAddress", "streetAddress": "50 W Streetsboro St, Suite 2", "addressLocality": "Hudson", "addressRegion": "OH", "postalCode": "44236", "addressCountry": "US"}},
        {"@type": "MedicalBusiness", "name": "Serene Med Spa — Barboursville, WV", "url": (SITE_URL + BARB["site"]) if BARB["site"].startswith("/") else BARB["site"], "telephone": "+1-304-520-0461",
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
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Noto+Serif+Display:wght@400;500&family=Oooh+Baby&display=swap" rel="stylesheet">
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
      <div class="card"><span class="state" style="font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal-500);font-weight:600">West Virginia</span><h3>Barboursville</h3><p>{BARB["addr1"]}<br>{BARB["addr2"]}<br><a href="tel:{BARB["tel"]}">{BARB["phone"]}</a></p><div class="actions"><a class="btn btn-sm" href="{BARB["book"]}" target="_blank" rel="noopener">Book Barboursville</a><a class="btn btn-sm btn-outline" href="{BARB["site"]}">Pricing &amp; menu</a></div></div>
      <div class="card"><span class="state" style="font-size:.74rem;letter-spacing:.2em;text-transform:uppercase;color:var(--teal-500);font-weight:600">OH &middot; WV &middot; KY &middot; FL</span><h3>Telehealth</h3><p>Weight management, hormone therapy &amp; wellness by secure video with Dr. Robin Arora.<br><a href="tel:{TELE["tel"]}">{TELE["phone"]}</a></p><div class="actions"><a class="btn btn-sm" href="{TELE["spruce"]}" target="_blank" rel="noopener">Start a visit</a><a class="btn btn-sm btn-outline" href="/telehealth/">Learn more</a></div></div>
    </div>
  </div>
</section>'''

def page_hero(title, lede="", crumbs=None, eyebrow=""):
    c = ""
    if crumbs:
        c = '<div class="crumbs">' + " &rsaquo; ".join(f'<a href="{h}">{t}</a>' if h else t for h, t in crumbs) + '</div>'
    return f'''<section class="page-hero"><div class="wrap">{c}{f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ''}<h1>{title}</h1>{f'<p class="lede">{lede}</p>' if lede else ''}</div></section>'''
