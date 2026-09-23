# -*- coding: utf-8 -*-
"""pages_custom.py — hand-authored pages for serenemedspas.com (home, about, providers, reviews, locations, telehealth, …)."""
import re, os, json
import extract as X
from site_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))

REVIEWS = [
    ("Holley Lyall", "Today was my first time at Serene and Stephanie was fantastic! Super friendly and got me in so fast! Very affordable and nice clean atmosphere! I’m so excited to go back!"),
    ("Kirk F", "Such a positive and pleasant experience! Affordable HRT does exist. Stephanie and the rest of the staff were nothing short of amazing. I am referring my friends and already have two individuals committed to making appointments."),
    ("Heather Brown", "Beautiful and clean environment. Professional and friendly staff. Monthly and weekly deals. Have sent several new patients their way. Treat yo self!"),
    ("Dbeauty Angel", "Dr. Shweta Arora is skilled with fillers and Botox. She listens to your concerns and looks at your face to see what is needed. I look and feel 10 years younger after the first visit. She starts conservatively, which is nice if it’s your first time."),
    ("Roseann Cerrito", "Dr. Arora is the best! So considerate and patient. Took the time to answer my many questions without trying to rush me out. Extremely thorough and knowledgeable. I recommend emphatically."),
    ("Cara McDaniel", "Extremely nice and helpful staff! Love the office too."),
]
FAQ = [
    ("Do you accept insurance?", "Aesthetic treatments are not covered by insurance, so our practice is cash-pay. To keep care accessible we offer CareCredit and Cherry payment plans — you can pre-qualify in minutes without affecting your credit score — and a monthly membership that discounts every visit. Telehealth visits are also cash-pay ($149/month program fee)."),
    ("How much does a consultation cost?", "Consultations are complimentary and carry no commitment. You&rsquo;ll meet with one of our board-certified physicians or nurse practitioner, talk through your goals, and leave with a written plan and pricing. Virtual consultations are available too."),
    ("Which location should I choose?", "Hudson, Ohio serves Summit and Portage counties and the greater Cleveland–Akron area; Barboursville, West Virginia serves Huntington, Charleston and the Tri-State (WV, OH, KY). Both offices offer the full injectable, skin and laser menu; each office&rsquo;s own site lists its pricing and specials."),
    ("What is Serene Telehealth?", "Video visits with Dr. Robin Arora for medical weight management, hormone therapy and wellness care, for patients located in Ohio, West Virginia, Kentucky or Florida. Visits run through the HIPAA-secure Spruce app; a prescription is never guaranteed and is issued only when medically appropriate after your evaluation."),
    ("What forms of payment do you accept?", "All major credit cards, CareCredit and Cherry. Pre-paid treatments and packages make thoughtful gifts — call either office and we&rsquo;ll set it up."),
    ("Is there a cancellation policy?", "We ask for 24 hours&rsquo; notice. Cancellations, reschedules and no-shows inside that window carry a $25 fee to the card on file. Full details are in our <a href='/terms-of-service/'>Terms of Service</a>."),
    ("Do you provide pre- and post-treatment instructions?", "Yes — every treatment comes with written aftercare, and our <a href='/post-care-instructions/'>Post-Care Instructions</a> page has the essentials for injectables, lasers, peels, microneedling and more. Questions after hours? Call the office where you were seen or email info@serenemedspas.com."),
]
CONCERNS = [
    ("Wrinkles &amp; fine lines", "/service/#injectables", "/wp-content/uploads/2025/09/Wrinkles.jpg"),
    ("Volume loss &amp; contour", "/service/#injectables", "/wp-content/uploads/2025/09/Facial-Sagging.jpg"),
    ("Acne &amp; scarring", "/service/#skin", "/wp-content/uploads/2025/09/Acne-Scars.jpg"),
    ("Pigmentation &amp; sun damage", "/service/#skin", "/wp-content/uploads/2025/09/Pigmentation.jpg"),
    ("Stubborn fat &amp; body", "/service/#body", "/wp-content/uploads/2025/09/Body-Fat.jpg"),
    ("Thinning hair", "/service/#hair", "/wp-content/uploads/2025/09/Hair-Loss.jpg"),
]
TOOLS = [
    ("/recommendation-webapp/", "Treatment Finder", "Tell us your concerns and get a shortlist to bring to your consult."),
    ("/neuromodulator-iq/", "NeuromodulatorIQ", "Botox, Dysport, Xeomin or Daxxify — estimate units and cost by area."),
    ("/filleriq/", "FillerIQ", "Plan filler by area and syringe, with realistic expectations."),
    ("/liftiq-by-serene/", "LiftIQ", "Compare non-surgical lifting: Ultherapy, Morpheus8, threads, Sculptra."),
    ("/peel-iq/", "PeelIQ", "Match a chemical peel to your skin type, concern and downtime."),
    ("/fitzpatrick-skin-type-self-assessment/", "Skin Type Quiz", "Your Fitzpatrick type — it guides laser and peel safety."),
    ("/the-serene-hydration-bar/", "IV Bar Menu", "Build an IV drip and see what&rsquo;s in it."),
    ("/aroramd-skin-confidence-report/", "Skin Confidence Report", "A quick self-assessment with a personalized plan."),
]

def stars(): return '<div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'

# treatment categories shown as arches on the home page (real Serene photos in /img/)
CATEGORIES = [
    ("Injectables", "/service/#injectables", "/img/botox-inject.jpg"),
    ("Fillers", "/filler-injection-treatments-at-serene-med-spa/", "/img/lip-inject.jpg"),
    ("Facials &amp; Peels", "/service/#skin", "/img/hydrafacial.jpg"),
    ("Laser &amp; RF", "/service/#laser", "/img/laser.jpg"),
    ("Body", "/service/#body", "/img/morpheus8.jpg"),
    ("Hair &amp; Wellness", "/service/#wellness", "/img/hair-ted.jpg"),
]

def home(posts):
    FEATURED = ["/botox-treatment-benefits/", "/hydrafacial-treatment-benefits/", "/morpheus8-rf-microneedling-treatment-at-serene-med-spas/"]
    by = {p["slug"]: p for p in posts}
    featured = [by[s] for s in FEATURED if s in by] or [p for p in posts if p["og_image"]][:3]
    from gen_site import post_card, CAT_NAME
    arches = "".join(f'<a class="arch reveal" href="{h}"><img src="{img}" alt="{X.text_of(t)} at Serene Med Spa" loading="lazy" width="600" height="800"><span>{t}</span></a>' for t, h, img in CATEGORIES)
    provs = ""
    for path, name, role, img, creds, blurb in PROVIDERS:
        provs += f'<a class="provcard reveal" href="{path}"><img src="{img}" alt="{X.text_of(name)}" loading="lazy"><span class="role">{role}</span><h3>{name}</h3><p style="color:var(--ink-soft);font-size:.92rem">{creds[0]}</p></a>'
    body = f"""
<section class="hero" style="background-image:linear-gradient(90deg,rgba(16,50,47,.8) 0%,rgba(16,50,47,.5) 50%,rgba(16,50,47,.12) 100%),url('/img/lobby.jpg')">
  <div class="wrap">
    <span class="script" data-loc-none>Physician-led aesthetics &amp; wellness</span>
    <span class="script hidden" data-loc-only="hudson">Serene Hudson, Ohio</span>
    <span class="script hidden" data-loc-only="barboursville">Serene Barboursville, West Virginia</span>
    <span class="script hidden" data-loc-only="telehealth">Serene Telehealth &middot; OH, WV, KY &amp; FL</span>
    <h1>Look refreshed.<br>Feel like yourself.</h1>
    <p class="lede">Injectables, skin and laser treatments, body contouring and medical wellness in Hudson, Ohio and Barboursville, West Virginia &mdash; planned by board-certified physicians and performed with a light hand.</p>
    <div class="hero-cta"><a class="btn btn-lav" href="/#book" data-loc-book>Book Now</a><a class="btn btn-ghost" href="/service/">Explore treatments</a><a class="btn btn-ghost hidden" data-loc-any data-loc-site href="/locations/">Your office &amp; pricing</a></div>
    <div class="hero-chips"><span class="chip">Board-certified physicians</span><span class="chip">Allergan Platinum Partner</span><span class="chip">Complimentary consultations</span><span class="chip">Telehealth in OH &middot; WV &middot; KY &middot; FL</span></div>
  </div>
</section>
<div class="trust"><div class="wrap"><span>Physician-designed plans</span><span>Medical-grade products &amp; devices</span><span>Natural-looking results</span><span>5-star rated on Google</span></div></div>

<div class="yourloc hidden" data-loc-only="hudson">
  <div class="wrap"><div><span class="eyebrow" style="background:rgba(255,255,255,.12);color:#fff;margin-bottom:8px">Your Serene</span><h3>Hudson, Ohio</h3></div>
    <div class="meta"><div><b>Address</b>{HUDSON["addr1"]}, {HUDSON["addr2"]}</div><div><b>Phone</b><a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a></div><div><b>Hours</b>Mon&ndash;Fri 9 AM &ndash; 5 PM &middot; Sat by appt.</div></div>
    <div class="actions"><a class="btn btn-lav" href="{HUDSON["book"]}" target="_blank" rel="noopener">Book Hudson</a><a class="btn btn-ghost" href="/hudson/pricing/">Hudson pricing</a><a class="btn btn-ghost" href="{HUDSON["map"]}" target="_blank" rel="noopener">Directions</a></div></div>
</div>
<div class="yourloc hidden" data-loc-only="barboursville">
  <div class="wrap"><div><span class="eyebrow" style="background:rgba(255,255,255,.12);color:#fff;margin-bottom:8px">Your Serene</span><h3>Barboursville, West Virginia</h3></div>
    <div class="meta"><div><b>Address</b>{BARB["addr1"]}, {BARB["addr2"]}</div><div><b>Phone</b><a href="tel:{BARB["tel"]}">{BARB["phone"]}</a></div><div><b>Hours</b>Mon&ndash;Fri 9 AM &ndash; 5 PM &middot; Sat by appt.</div></div>
    <div class="actions"><a class="btn btn-lav" href="{BARB["book"]}" target="_blank" rel="noopener">Book Barboursville</a><a class="btn btn-ghost" href="/barboursville/pricing/">Barboursville pricing</a><a class="btn btn-ghost" href="{BARB["map"]}" target="_blank" rel="noopener">Directions</a></div></div>
</div>
<div class="yourloc hidden" data-loc-only="telehealth">
  <div class="wrap"><div><span class="eyebrow" style="background:rgba(255,255,255,.12);color:#fff;margin-bottom:8px">Your Serene</span><h3>Telehealth with Dr. Robin Arora</h3></div>
    <div class="meta"><div><b>Where</b>Video visits for patients in OH, WV, KY &amp; FL</div><div><b>Phone / text</b><a href="tel:{TELE["tel"]}">{TELE["phone"]}</a></div><div><b>Program</b>$149 / month &middot; Mon&ndash;Fri 9&ndash;5 ET</div></div>
    <div class="actions"><a class="btn btn-lav" href="{TELE["spruce"]}" target="_blank" rel="noopener">Start a visit</a><a class="btn btn-ghost" href="/telehealth/">How it works</a></div></div>
</div>

<section>
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">Face &amp; body</span><h2>Treatments our physicians recommend</h2><p class="lede">Every plan starts with a complimentary consultation. Pick a category to see what we offer, how it works and what to expect.</p></div>
    <div class="grid g6">{arches}</div>
    <div class="actions" style="justify-content:center;margin-top:44px"><a class="btn" href="/#consult">Book a consult</a><a class="btn btn-outline" href="/service/">See all treatments</a></div>
  </div>
</section>

<section class="tint-sand" id="locations">
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">Two offices &middot; one standard of care</span><h2>Find your Serene</h2><p class="lede">Pick your office once and the whole site follows: Book Now, phone numbers, pricing and treatment pages all switch to your location. Each office page has its own team, menu, hours and directions.</p></div>
    <div class="grid g3">
      <a class="loctile reveal" href="{HUDSON["site"]}"><img src="/img/hudson-exterior.jpg" alt="Serene Med Spa Hudson, Ohio — 50 W Streetsboro St" loading="lazy"><span class="state">Ohio</span><h3>Hudson</h3><p>{HUDSON["addr1"]}, {HUDSON["addr2"]} &middot; Serving Akron, Stow, Twinsburg &amp; the Cleveland east side.</p><div class="actions"><span class="btn btn-lav btn-sm">Hudson menu &amp; pricing</span></div></a>
      <a class="loctile reveal" href="{BARB["site"]}"><img src="/img/lobby-2.jpg" alt="Serene Med Spa Barboursville, West Virginia" loading="lazy"><span class="state">West Virginia</span><h3>Barboursville</h3><p>{BARB["addr1"]}, {BARB["addr2"]} &middot; Serving Huntington, Charleston, Ashland &amp; the Tri-State.</p><div class="actions"><span class="btn btn-lav btn-sm">Barboursville menu &amp; pricing</span></div></a>
      <a class="loctile reveal" href="/telehealth/"><img src="/img/skin-analysis.jpg" alt="Serene Telehealth video visits" loading="lazy"><span class="state">OH &middot; WV &middot; KY &middot; FL</span><h3>Telehealth</h3><p>Medical weight management, hormone therapy and wellness by secure video with Dr. Robin Arora. $149/month program.</p><div class="actions"><span class="btn btn-lav btn-sm">How it works</span></div></a>
    </div>
    <p style="text-align:center;margin-top:30px;font-size:.9rem;color:var(--ink-soft)">Hudson <a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a> &nbsp;&middot;&nbsp; Barboursville <a href="tel:{BARB["tel"]}">{BARB["phone"]}</a> &nbsp;&middot;&nbsp; Telehealth <a href="tel:{TELE["tel"]}">{TELE["phone"]}</a></p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">Highly trained experts</span><h2>Meet our medical team</h2><p class="lede">Two board-certified physicians and a board-certified nurse practitioner. Physician-designed plans, physician-supervised care &mdash; at both offices and by telehealth.</p></div>
    <div class="grid g3">{provs}</div>
    <div class="actions" style="justify-content:center;margin-top:40px"><a class="btn btn-outline" href="/our-providers/">Meet the whole team</a></div>
  </div>
</section>

<section class="tint-sand" id="offer" style="padding-top:0">
  <div class="wrap">
    <div class="offer reveal">
      <div><span class="eyebrow">New patients</span><h2>Your first visit, 20% off</h2><p class="lede">Applies to any product or service at either office &mdash; injectables, facials, lasers, IV therapy or skincare. Can&rsquo;t be combined with another discount. Mention it when you book.</p>
        <div class="actions"><a class="btn" href="/#book" data-loc-book>Book Now</a><a class="btn btn-outline" href="/specials/">September specials</a></div></div>
      <div class="big" style="text-align:center">20%<br><span style="font-size:.28em;letter-spacing:.2em">off your first visit</span></div>
    </div>
  </div>
</section>

<section class="tint-sand">
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">Trusted partners &amp; technology</span><h2>The brands behind the results</h2><p class="lede">Top-tier partner status with the makers of Botox, Xeomin and Ultherapy, and the same devices you&rsquo;d find in a university aesthetics department.</p></div>
    <div class="badges">
      <div class="badge reveal"><img src="/img/badges/allergan-platinum-2026.png" alt="Allergan Partner Privileges Platinum 2026"><div><b>Allergan Platinum Partner</b><small>Botox, Juv&eacute;derm, SkinVive, Kybella</small></div></div>
      <div class="badge reveal"><img src="/img/badges/merz-elite-plus.png" alt="Merz Aesthetics ELITE+ Provider"><div><b>Merz Aesthetics ELITE+</b><small>Xeomin, Radiesse &amp; Ultherapy</small></div></div>
      <div class="badge reveal"><img src="/img/badges/ultherapy-prime.png" alt="Ultherapy PRIME provider"><div><b>Ultherapy PRIME</b><small>Non-surgical lifting</small></div></div>
      <div class="badge reveal"><img src="/img/badges/biote-certified-provider.webp" alt="Biote Certified Provider"><div><b>Biote Certified</b><small>Hormone optimization</small></div></div>
      <div class="badge reveal"><img src="/img/logos/obagi-medical-logo.png" alt="Obagi Medical" style="padding:6px"><div><b>Authorized Obagi Provider</b><small>Medical-grade skincare</small></div></div>
    </div>
    <p style="text-align:center;margin:40px 0 18px;font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;color:var(--muted);font-weight:600">Injectables &amp; skin</p>
    <div class="logos reveal">
      <img src="/img/logos/botox-cosmetic-dark.png" alt="Botox Cosmetic" class="tall"><img src="/img/logos/juvederm-dark.png" alt="Juv&eacute;derm"><img src="/img/logos/skinvive-dark.png" alt="SkinVive by Juv&eacute;derm"><img src="/img/logos/kybella-dark.png" alt="Kybella"><img src="/img/logos/diamondglow-dark.png" alt="DiamondGlow"><img src="/img/logos/alle-dark.png" alt="All&#275;" class="tall">
    </div>
    <p style="text-align:center;margin:34px 0 18px;font-size:.66rem;letter-spacing:.24em;text-transform:uppercase;color:var(--muted);font-weight:600">Laser, RF &amp; energy devices</p>
    <div class="logos reveal">
      <img src="/img/logos/alma-dark.png" alt="Alma Lasers"><img src="/img/logos/soprano-ice-platinum-dark.png" alt="Soprano ICE Platinum"><img src="/img/logos/opus-plasma-dark.png" alt="Opus Plasma"><img src="/img/logos/alma-hybrid-dark.png" alt="Alma Hybrid"><img src="/img/logos/alma-ted-dark.png" alt="Alma TED"><img src="/img/logos/alma-duo-dark.png" alt="Alma Duo" class="tall"><img src="/img/logos/harmony-bio-boost-dark.png" alt="Harmony Bio-Boost" class="tall"><img src="/img/logos/sknlab-dark.png" alt="SKNLAB">
    </div>
    <p style="text-align:center;margin-top:26px;font-size:.9rem;color:var(--ink-soft)">Plus Morpheus8, EvolveX, Forma and EmpowerRF by InMode, Sciton BBL &amp; MOXI, and HydraFacial.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="shopband reveal">
      <div><span class="eyebrow">Medical-grade skincare</span><h2>Shop Obagi &mdash; reserve online, pick up at your office</h2><p class="lede">Nu-Derm, ELASTIderm, Professional-C, Obagi-C and Suzan Obagi MD lines, chosen by our physicians. Add products to your cart online and they&rsquo;ll be waiting at the front desk &mdash; no shipping, no guesswork.</p>
        <div class="actions"><a class="btn" href="#" data-loc-shop>Shop Obagi</a><a class="btn btn-outline" href="/#consult">Ask which products fit your skin</a></div>
        <p class="zf-fine" data-loc-none>Choose your office first so we show the right shop.</p></div>
      <div class="products"><img src="/barboursville/img/obagi/professional-c-serum-20-400.webp" alt="Obagi Professional-C Serum 20%" loading="lazy"><img src="/barboursville/img/obagi/elastiderm-eye-cream-fine-lines-wrinkles-400.webp" alt="Obagi ELASTIderm Eye Cream" loading="lazy"><img src="/barboursville/img/obagi/hydrate-luxe-moisturizer-400.webp" alt="Obagi Hydrate Luxe" loading="lazy"><img src="/barboursville/img/obagi/skin-brightening-system-normal-to-oily-400.webp" alt="Obagi Nu-Derm Fx System" loading="lazy"><img src="/barboursville/img/obagi/mineral-broad-spectrum-spf-50-400.webp" alt="Obagi Sun Shield Mineral SPF 50" loading="lazy"><img src="/barboursville/img/obagi/clenziderm-acne-therapeutic-system-3-400.webp" alt="Obagi CLENZIderm System" loading="lazy"></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">Start with the concern</span><h2>What would you like to work on?</h2><p class="lede">Not sure which treatment fits? Pick a concern and we&rsquo;ll point you to the options &mdash; then a complimentary consultation turns it into a plan.</p></div>
    <div class="grid g3">{"".join(f'<a class="tile reveal" href="{h}"><img src="{img}" alt="{X.text_of(t)}" loading="lazy"><span>{t}</span></a>' for t, h, img in CONCERNS)}</div>
  </div>
</section>

<section class="tint-sage">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">Serene Smart Tools&trade;</span><h2>Plan before you book</h2><p class="lede">Free, private planning tools built by our physicians. Nothing you enter is stored or sent.</p></div>
    <div class="grid g4">{"".join(f'<a class="tool reveal" href="{h}"><b>{i+1}</b><div><h4>{t}</h4><p>{d}</p></div></a>' for i, (h, t, d) in enumerate(TOOLS))}</div>
  </div>
</section>

<section>
  <div class="wrap band">
    <div class="reveal"><img src="/img/team.jpg" alt="The Serene Med Spa team" style="border-radius:var(--r);max-height:640px;object-fit:cover;width:100%" loading="lazy"></div>
    <div>
      <span class="eyebrow">The Serene difference</span>
      <h2>Two physicians. One standard of care.</h2>
      <p class="lede">Serene was founded by Dr. Robin Arora, board certified in internal medicine and nephrology, and Dr. Shweta Arora, board certified in anesthesiology &mdash; both trained in aesthetic medicine. Every treatment plan is physician-designed, every injector physician-supervised, and every product medical-grade.</p>
      <ul style="list-style:none;display:grid;gap:12px;margin:20px 0 26px">
        <li><strong>Expert-led treatments.</strong> The latest techniques, used conservatively, for results that look like you.</li>
        <li><strong>Personalized plans.</strong> We take time to understand your goals before recommending anything.</li>
        <li><strong>Advanced technology.</strong> Morpheus8, Ultherapy, Alma lasers, EmpowerRF and premium injectables from Allergan and Galderma.</li>
      </ul>
      <div class="actions"><a class="btn" href="/our-story/">Our story</a><a class="btn btn-outline" href="/about-us/">About Serene</a></div>
    </div>
  </div>
</section>

<section class="tint-teal">
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">Loved across two states</span><h2>Patients love to love us</h2></div>
    <div class="grid g3">{"".join(f'<div class="rev reveal"><p>{q}</p><div class="who">&mdash; {n} &middot; Google</div></div>' for n, q in REVIEWS[:3])}</div>
    <p style="text-align:center;margin-top:34px"><a class="btn btn-ghost" href="/reviews/">Read more reviews</a></p>
  </div>
</section>

<section class="tint-sand">
  <div class="wrap">
    <div class="grid g2">
      <div class="card reveal"><span class="eyebrow">Serene Elevate</span><h3>Membership that pays you back</h3><p>Monthly credit that rolls over, member pricing on injectables, skin, laser and IV therapy, and first access to specials. No long-term contract.</p><a class="btn btn-sm" href="/membership/">Membership details</a></div>
      <div class="card reveal"><span class="eyebrow">Easy Pay</span><h3>Financing in 60 seconds</h3><p>Cherry and CareCredit payment plans with 0% APR options for qualified patients. Pre-qualify in minutes without affecting your credit score.</p><a class="btn btn-sm btn-outline" href="/financing/">Financing options</a></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">From the journal</span><h2>Treatment guides</h2></div>
    <div class="grid g3">{"".join(post_card(p) for p in featured)}</div>
    <p style="margin-top:30px;text-align:center"><a class="btn btn-outline" href="/blogs/">All articles</a></p>
  </div>
</section>

<section class="tint-sand">
  <div class="wrap" style="max-width:900px">
    <div class="section-head center"><span class="eyebrow">Good to know</span><h2>Frequently asked questions</h2></div>
    <div class="faq">{"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div>
  </div>
</section>

{book_band()}
{consult_form("serenemedspas.com/")}
"""
    return shell("/", "Serene Med Spa | Physician-Led Med Spa in Hudson, OH & Barboursville, WV",
                 "Physician-led medical spa and wellness in Hudson, Ohio and Barboursville, West Virginia, plus telehealth weight management and hormone care in OH, WV, KY and FL. Injectables, skin, laser, body contouring and IV therapy — natural results by board-certified physicians.", body, og_image="/img/lobby.jpg")

def loc_card(L, blurb, compact=False):
    return f'''<div class="loc reveal{" compact" if compact else ""}">
  <div class="loc-body"><span class="state">{L["state"]}</span><h3 style="font-size:1.9rem;margin-top:4px">Serene Med Spa &middot; {L["name"].split(",")[0]}</h3><p style="color:var(--ink-soft)">{blurb}</p>
    <dl><dt>Address</dt><dd>{L["addr1"]}, {L["addr2"]}</dd><dt>Phone</dt><dd><a href="tel:{L["tel"]}">{L["phone"]}</a></dd><dt>Hours</dt><dd>Mon&ndash;Fri 9 AM &ndash; 5 PM &middot; Sat&ndash;Sun by appointment</dd></dl>
    <div class="actions"><a class="btn btn-sm" href="{L["book"]}" target="_blank" rel="noopener">Book online</a><a class="btn btn-sm btn-outline" href="{L["site"]}">Visit the {L["name"].split(",")[0]} site</a><a class="btn btn-sm btn-outline" href="{L["map"]}" target="_blank" rel="noopener">Directions</a></div>
  </div>
  <iframe class="map" src="https://maps.google.com/maps?q={L["addr1"].replace(" ", "+")},+{L["addr2"].replace(" ", "+")}&t=m&z=15&output=embed&iwloc=near" title="Map of Serene Med Spa {L["name"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</div>'''

def locations():
    body = page_hero("Our locations", "Two physician-led offices and a telehealth program that reaches four states. Choose the one nearest you &mdash; both offer complimentary consultations and same-week appointments.", [("/", "Home"), (None, "Locations")], "Hudson, OH &middot; Barboursville, WV &middot; Telehealth") + f'''
<section><div class="wrap"><div class="grid" style="gap:28px">
  {loc_card(HUDSON, "Just off Route 303 in historic downtown Hudson. Serving Hudson, Stow, Twinsburg, Aurora, Cuyahoga Falls, Akron and the east side of Cleveland.")}
  {loc_card(BARB, "One Chateau Grove Lane, minutes from I-64. Serving Barboursville, Huntington, Milton, Ashland (KY), Ironton (OH) and Charleston.")}
</div></div></section>
<section class="tint-teal"><div class="wrap band"><div><span class="eyebrow">Can&rsquo;t come in?</span><h2>Serene Telehealth</h2><p class="lede" style="color:rgba(255,255,255,.85)">Weight management, hormone therapy and wellness by secure video with Dr. Robin Arora, for patients located in Ohio, West Virginia, Kentucky or Florida.</p><div class="actions"><a class="btn btn-ghost" href="/telehealth/">Learn more</a><a class="btn" style="background:#fff;color:var(--teal-900);border-color:#fff" href="tel:{TELE["tel"]}">{TELE["phone"]}</a></div></div>
<div class="card" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);color:#fff"><h3 style="color:#fff">Hours</h3><p>Video visits Monday&ndash;Friday, 9 AM &ndash; 5 PM ET. Secure messaging any time; replies during business hours. Not for emergencies &mdash; call 911.</p></div></div></section>
{consult_form("serenemedspas.com/locations/")}'''
    return shell("/locations/", "Our Locations | Serene Med Spa – Hudson, OH & Barboursville, WV", "Serene Med Spa locations: 50 W Streetsboro St, Hudson, OH and 1 Chateau Grove Ln, Barboursville, WV — plus telehealth for OH, WV, KY and FL. Addresses, hours, phone numbers and online booking.", body)

PROVIDERS = [
    ("/our-providers/robin-arora-md/", "Robin Arora, MD, MBA", "Founder &amp; Medical Director", "/wp-content/uploads/2026/08/Robin-683x1024-1.jpg",
     ["Board Certified, Internal Medicine (ABIM)", "Board Certified, Nephrology &amp; Hypertension", "Certified in Aesthetic Medicine", "Biote Certified Provider", "Licensed in OH, WV, KY &amp; FL", "16+ years in practice"],
     "Dr. Robin Arora trained in nephrology at Tulane and brings an internist&rsquo;s judgment to aesthetic and wellness medicine. He leads Serene Telehealth and supervises every treatment protocol at both offices."),
    ("/our-providers/shweta-arora/", "Shweta Arora, MD", "Aesthetic Physician", "/wp-content/uploads/2026/08/Shweta-Arora-MD.png",
     ["Board Certified, Anesthesiology (ABA)", "Certified in Aesthetic Medicine (AAAM)", "Biote Certified Provider", "Licensed in Ohio &amp; West Virginia", "16+ years in practice"],
     "Dr. Shweta Arora is the artistic eye behind Serene&rsquo;s injectables &mdash; conservative, anatomy-first and known for results that look rested rather than done. She sees patients at both offices."),
    ("/our-providers/stephanie-welker-fnp-bc/", "Stephanie Welker, FNP-BC", "Nurse Practitioner", "/wp-content/uploads/2025/10/Stephanie-Welker.png",
     ["Board Certified Family Nurse Practitioner", "Biote Certified Provider", "Allergan &amp; InMode trained", "8+ years as an NP"],
     "Stephanie is a board-certified family nurse practitioner with a background in emergency nursing. Patients love her calm, thorough approach to injectables, hormone therapy and skin treatments."),
]

def providers(pages):
    # use each provider page's og image if present
    imgs = {}
    for path, *_ in PROVIDERS:
        r = pages.get(path)
        if r and r.get("og_image"): imgs[path] = r["og_image"]
    cards = ""
    for path, name, role, img, creds, blurb in PROVIDERS:
        img = imgs.get(path, img)
        cards += f'''<div class="prov reveal"><img src="{img}" alt="{X.text_of(name)}" loading="lazy"><div class="pbody"><span class="eyebrow">{role}</span><h2 style="font-size:2rem">{name}</h2><ul class="creds">{"".join(f'<li>{c}</li>' for c in creds)}</ul><p class="lede" style="font-size:1.05rem">{blurb}</p><a class="btn btn-sm btn-outline" href="{path}">Full profile</a></div></div>'''
    body = page_hero("Our providers", "Two board-certified physicians and a board-certified nurse practitioner. Physician-designed plans, physician-supervised care, at both offices and by telehealth.", [("/", "Home"), (None, "Our Providers")], "Meet the team") + \
        f'<section><div class="wrap grid" style="gap:28px">{cards}</div></section>' + book_band()
    return shell("/our-providers/", "Our Providers | Serene Med Spa", "Meet the physicians and nurse practitioner behind Serene Med Spa: Robin Arora, MD; Shweta Arora, MD; and Stephanie Welker, FNP-BC.", body)

def about(pages):
    r = pages.get("/about-us/")
    body = page_hero("About Serene Med Spa", "Part tranquil spa, part advanced medical-aesthetics center &mdash; physician-owned and physician-led in Hudson, Ohio and Barboursville, West Virginia.", [("/", "Home"), (None, "About")], "Where beauty meets wellness") + f'''
<section><div class="wrap band">
  <div class="prose">
    <p>Serene Med Spa was built on a simple belief: good aesthetic care shouldn&rsquo;t require choosing between a clinical setting and a comfortable one. From the moment you walk in, the atmosphere invites you to relax &mdash; while a physician-led medical team makes sure every decision is a sound one.</p>
    <p>Our founders, Dr. Robin Arora and Dr. Shweta Arora, are both board-certified physicians who trained further in aesthetic medicine. Together with our nurse practitioner and aestheticians they bring more than 25 years of combined experience to every visit, and every plan is customized to you &mdash; never a menu of upsells.</p>
    <p>We use only medical-grade products and devices: Allergan and Galderma injectables, Morpheus8 and EmpowerRF by InMode, Ultherapy, Alma lasers, Biote hormone optimization, and professional skincare from Obagi, Alastin and SkinMedica.</p>
    <h2>What we do</h2>
    <ul>
      <li>Wrinkle relaxers, dermal fillers, Kybella and PDO threads</li>
      <li>Morpheus8, microneedling with PRP/PRF, chemical peels, HydraFacial and laser facials</li>
      <li>Laser hair removal, tattoo removal, vein and nail-fungus lasers</li>
      <li>Body contouring, EvolveX, EmpowerRF and intimate wellness</li>
      <li>Medical weight management, hormone optimization and IV nutrient therapy &mdash; in office and by <a href="/telehealth/">telehealth</a></li>
    </ul>
    <p>Our mission is simple: exceptional care in a peaceful setting, using the most advanced technology, for results you can see and feel. Because beautiful skin takes commitment &mdash; and we&rsquo;re committed to you.</p>
    <div class="actions" style="margin-top:22px"><a class="btn" href="/our-story/">Read our story</a><a class="btn btn-outline" href="/our-providers/">Meet the providers</a></div>
  </div>
  <div class="reveal"><img src="/wp-content/uploads/2025/04/Robin-and-Shweta-768x1024.jpg" alt="Dr. Robin Arora and Dr. Shweta Arora" style="border-radius:var(--r)"></div>
</div></section>
{book_band()}'''
    return shell("/about-us/", "About Serene Med Spa | Physician-Led Aesthetics & Wellness", (r or {}).get("description") or "Physician-owned medical spa in Hudson, OH and Barboursville, WV. Meet the team, our philosophy and the medical-grade technology behind our treatments.", body)

def reviews():
    body = page_hero("Patient reviews", "Real words from real patients at our Hudson and Barboursville offices. Reviews are collected on Google; we never edit them.", [("/", "Home"), (None, "Reviews")], "5-star rated on Google") + f'''
<section><div class="wrap"><div class="grid g3">{"".join(f'<div class="rev reveal">{stars()}<p>&ldquo;{q}&rdquo;</p><div class="who">&mdash; {n} &middot; Google</div></div>' for n, q in REVIEWS)}</div>
<div class="grid g2" style="margin-top:34px">
  <div class="card"><h3>Hudson, OH</h3><p>Read and leave reviews for our Hudson office.</p><a class="btn btn-sm btn-outline" href="https://www.google.com/maps/search/Serene+Med+Spa+Hudson+OH" target="_blank" rel="noopener">Hudson on Google</a></div>
  <div class="card"><h3>Barboursville, WV</h3><p>Read and leave reviews for our Barboursville office.</p><a class="btn btn-sm btn-outline" href="https://g.page/r/CXHpqD_ZeNBmEBM/review" target="_blank" rel="noopener">Barboursville on Google</a></div>
</div></div></section>
{book_band()}'''
    return shell("/reviews/", "Patient Reviews | Serene Med Spa", "What patients say about Serene Med Spa in Hudson, OH and Barboursville, WV — Google reviews of our physicians, nurse practitioner and staff.", body)

def membership():
    body = page_hero("Serene Elevate Membership", "A monthly membership that turns maintenance into a habit &mdash; and rewards you for it. Available at both offices.", [("/", "Home"), (None, "Membership")], "Members save on every visit") + f'''
<section><div class="wrap band">
  <div class="reveal"><img src="/wp-content/uploads/2026/08/Serene-Elevate-Membership-791x1024.png" alt="Serene Elevate Membership details" style="border-radius:var(--r);box-shadow:var(--shadow)"></div>
  <div class="prose">
    <h2>How it works</h2>
    <p>Choose a monthly tier, bank your credit toward treatments and skincare, and enjoy member pricing on injectables, facials, lasers and IV therapy. Credits roll over, there&rsquo;s no long-term contract, and members get first access to monthly specials.</p>
    <ul><li>Member pricing on wrinkle relaxers, fillers and skin treatments</li><li>Monthly credit that rolls over</li><li>Priority booking and early access to <a href="/specials/">specials</a></li><li>Cancel any time after your first three months</li></ul>
    <p>Details, tiers and current pricing are on the card at left; our front desk can enroll you at your next visit or by phone.</p>
    <div class="actions"><a class="btn" href="tel:{HUDSON["tel"]}">Hudson {HUDSON["phone"]}</a><a class="btn btn-outline" href="tel:{BARB["tel"]}">Barboursville {BARB["phone"]}</a></div>
  </div>
</div></section>
{book_band()}'''
    return shell("/membership/", "Aesthetic Membership Plan | Serene Med Spa", "Serene Elevate Membership: monthly credit, member pricing on injectables, skin, laser and IV treatments, priority booking. Hudson, OH and Barboursville, WV.", body)

def financing():
    body = page_hero("Financing &amp; payment plans", "Start now, pay over time. Pre-qualify in minutes with no impact on your credit score.", [("/", "Home"), (None, "Financing")], "Easy Pay") + f'''
<section><div class="wrap grid g2">
  <div class="card reveal"><img src="/wp-content/uploads/2025/10/cherry-logo-dark-15JORFDf.svg" alt="Cherry" style="height:34px;width:auto;margin-bottom:16px"><h3>Cherry</h3><p>Flexible monthly plans, 0% APR options for qualified patients, and a 60-second application that doesn&rsquo;t affect your credit score. Use it for any treatment or package.</p><a class="btn btn-sm" href="https://pay.withcherry.com/serene-medical-spa-llc?utm_source=practice&m=30323" target="_blank" rel="noopener">Apply with Cherry</a></div>
  <div class="card reveal"><img src="/wp-content/uploads/2025/10/Carecredit-Logo.png" alt="CareCredit" style="height:34px;width:auto;margin-bottom:16px"><h3>CareCredit</h3><p>The healthcare credit card accepted at both offices, with promotional financing on qualifying purchases. Already a cardholder? Just let the front desk know.</p><a class="btn btn-sm" href="https://www.carecredit.com/go/778CHS/" target="_blank" rel="noopener">Apply for CareCredit</a></div>
</div>
<div class="wrap prose" style="margin-top:40px"><h2>Good to know</h2><ul><li>We also accept all major credit cards and offer a <a href="/membership/">monthly membership</a> with member pricing.</li><li>Pre-paid packages and gift certificates are available at either office.</li><li>Aesthetic treatments are not covered by insurance; telehealth is cash-pay.</li></ul></div></section>
{book_band()}'''
    return shell("/financing/", "Financing Options | Serene Med Spa", "Pay over time for treatments at Serene Med Spa with Cherry or CareCredit. 0% APR options for qualified patients; pre-qualify without affecting your credit score.", body)

# ---- Monthly specials: edit SPECIALS_MONTH / SPECIALS each month (no flyer image needed) ----
SPECIALS_MONTH = "September"
SPECIALS_YEAR = "2026"
SPECIALS = [
    # (deal, [(treatment, href, one-line blurb)], note)
    ("Buy 2, get 1 free", [
        ("V-Tone", "/empowerrf-vaginal-rejuvenation-treatment/", "Gentle electrical muscle stimulation for pelvic-floor strength and bladder control."),
        ("Forma V", "/empowerrf-vaginal-rejuvenation-treatment/", "Radiofrequency for intimate comfort, tissue quality and blood flow &mdash; no downtime."),
        ("Morpheus V", "/empowerrf-vaginal-rejuvenation-treatment/", "Fractional RF microneedling for deeper remodeling of vaginal and vulvar tissue."),
    ], "EmpowerRF women&rsquo;s wellness &middot; series of 3 recommended"),
    ("Buy 1, get 1 free", [
        ("PRP Hair Restoration", "/natural-prp-hair-restoration/", "Your own platelet-rich plasma, injected into the scalp to wake up thinning follicles."),
    ], "Two sessions for the price of one"),
    ("Buy 2, get 1 free", [
        ("Evolve X", "/inmode-evolvex-body-contouring/", "Hands-free RF body contouring &mdash; tighten skin, reduce fat and tone muscle in one platform."),
    ], "Series pricing on Tite, Trim &amp; Tone"),
]

def specials(pages):
    month = SPECIALS_MONTH
    cards = ""
    for deal, items, note in SPECIALS:
        rows = "".join(f'<li><a href="{href}"><strong>{name}</strong></a><span>{blurb}</span></li>' for name, href, blurb in items)
        cards += f'''
    <div class="card reveal special">
      <span class="eyebrow">{month} special</span>
      <h3 class="deal">{deal}</h3>
      <ul class="deal-list">{rows}</ul>
      <p class="deal-note">{note}</p>
    </div>'''
    body = page_hero(f"{month} specials", "More glow, more you &mdash; this month&rsquo;s savings at Hudson and Barboursville. Specials change monthly; members see them first.", [("/", "Home"), (None, "Specials")], f"{month} {SPECIALS_YEAR} &middot; Hudson, OH &middot; Barboursville, WV") + f'''
<style>
.special{{display:flex;flex-direction:column;border-top:4px solid var(--sage)}}
.special .deal{{font-size:2rem;color:var(--teal-900);margin:0 0 18px}}
.deal-list{{list-style:none;margin:0 0 18px;padding:0;display:grid;gap:14px}}
.deal-list li{{display:grid;gap:3px;padding-left:26px;position:relative}}
.deal-list li::before{{content:"";position:absolute;left:0;top:.45em;width:12px;height:12px;border-radius:50%;background:var(--sage)}}
.deal-list a{{color:var(--teal-700);text-decoration:none;font-size:1.05rem}}
.deal-list a:hover{{text-decoration:underline}}
.deal-list span{{font-size:.92rem;color:var(--ink-soft)}}
.deal-note{{margin-top:auto;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--teal-500);font-weight:600}}
.fine{{font-size:.9rem;color:var(--ink-soft);max-width:760px}}
</style>
<section><div class="wrap">
  <div class="grid g3">{cards}
  </div>
  <p class="fine" style="margin-top:28px">Offers valid through {month} 30, {SPECIALS_YEAR} at both offices. Free session is of equal or lesser value and must be used by the same patient. Can&rsquo;t be combined with another discount or membership pricing; a consultation may be required to confirm candidacy.</p>
</div></section>
<section class="tint-sand"><div class="wrap band">
  <div class="prose"><h2>How to claim a special</h2><p>Book online or call the office and mention the {month} special when you check in. Specials can&rsquo;t be combined with other discounts, and some require a consultation first so we can confirm you&rsquo;re a good candidate.</p>
  <p>Want them in your inbox? Ask the front desk to add you to our monthly email, or follow <a href="https://www.instagram.com/serene.wellness.wv" target="_blank" rel="noopener">@serene.wellness.wv</a>.</p>
  <div class="actions"><a class="btn" href="{HUDSON["book"]}" target="_blank" rel="noopener">Book Hudson</a><a class="btn" href="{BARB["book"]}" target="_blank" rel="noopener">Book Barboursville</a></div></div>
  <div class="card reveal"><span class="eyebrow">Members save every month</span><h3>Serene Elevate Membership</h3><p>Members get priority access to specials plus discounted pricing on every visit. See what&rsquo;s included and join online.</p><div class="actions"><a class="btn btn-sm" href="/membership/">Membership details</a><a class="btn btn-sm btn-outline" href="/financing/">Financing</a></div></div>
</div></section>'''
    import calendar as _cal
    _mnum = list(_cal.month_name).index(month); _last = _cal.monthrange(int(SPECIALS_YEAR), _mnum)[1]
    offers_ld = json.dumps({"@context": "https://schema.org", "@type": "OfferCatalog", "name": f"{month} {SPECIALS_YEAR} specials — Serene Med Spa", "url": SITE_URL + "/specials/",
        "itemListElement": [{"@type": "Offer", "name": f"{deal}: {X.text_of(name)}", "description": X.text_of(blurb), "url": SITE_URL + href, "category": "Promotion",
                             "validFrom": f"{SPECIALS_YEAR}-{_mnum:02d}-01", "validThrough": f"{SPECIALS_YEAR}-{_mnum:02d}-{_last:02d}", "offeredBy": {"@id": SITE_URL + "/#organization"},
                             "areaServed": ["Hudson, OH", "Barboursville, WV"]} for deal, items, note in SPECIALS for name, href, blurb in items]}, ensure_ascii=False)
    return shell("/specials/", f"{month} Med Spa Specials | Serene Med Spa", f"{month} {SPECIALS_YEAR} specials at Serene Med Spa in Hudson, OH and Barboursville, WV: buy 2 get 1 free on V-Tone, Forma V, Morpheus V and Evolve X, and buy 1 get 1 free on PRP hair restoration.", body, ld=offers_ld)

def telehealth():
    disc = open(os.path.join(HERE, "telehealth-disclosures.html"), encoding="utf-8").read()
    # restyle the disclosure block's classes to the new design
    disc = disc.replace('class="grid"', 'class="grid g3"').replace('<p class="small"', '<p style="font-size:.95rem;color:var(--ink-soft)"')
    body = f'''
<section class="hero" style="min-height:62vh;background:linear-gradient(100deg,rgba(20,45,52,.9) 0%,rgba(20,45,52,.6) 60%,rgba(20,45,52,.3) 100%),url('/wp-content/uploads/2024/07/2148574924.jpg') center/cover no-repeat">
  <div class="wrap"><span class="eyebrow">Telehealth &middot; Ohio, West Virginia, Kentucky &amp; Florida</span><h1 style="max-width:16ch">Serene Telehealth with Dr. Robin Arora</h1>
  <p class="lede">Medical weight management, hormone therapy and wellness care from home, by secure video with a board-certified physician.</p>
  <div class="hero-cta"><a class="btn" style="background:#fff;color:var(--teal-900);border-color:#fff" href="{TELE["spruce"]}" target="_blank" rel="noopener">Start a telehealth visit</a><a class="btn btn-ghost" href="tel:{TELE["tel"]}">Call {TELE["phone"]}</a><a class="btn btn-ghost" href="sms:{TELE["tel"]}">Text us</a></div>
  <div class="hero-chips"><span class="chip">Monday &ndash; Friday, 9 AM &ndash; 5 PM ET</span><span class="chip">$149 / month program</span><span class="chip">HIPAA-secure Spruce app</span></div></div>
</section>
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">How it works</span><h2>Three steps, one secure conversation</h2></div>
  <div class="grid g3">
    <div class="card reveal"><span class="eyebrow">Step 1</span><h3>Consent &amp; reach out</h3><p>Complete the short <a href="{TELE["consent"]}" target="_blank" rel="noopener">Telehealth Informed Consent</a>, then tap <strong>Start a telehealth visit</strong> or call us. The link opens the free Spruce app &mdash; a private, HIPAA-secure way to message our office.</p></div>
    <div class="card reveal"><span class="eyebrow">Step 2</span><h3>See Dr. Arora by video</h3><p>Your visit happens by live video in Spruce. Dr. Arora reviews your history, goals and any labs, confirms your identity and location, and builds a plan with you.</p></div>
    <div class="card reveal"><span class="eyebrow">Step 3</span><h3>Ongoing care</h3><p>Follow-up visits, dose adjustments and questions are handled in the same secure conversation, so you always know where to find us.</p></div>
  </div>
</div></section>
<section class="tint-sand"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we treat by telehealth</span><h2>Wellness that fits your week</h2></div>
  <div class="grid g3">
    <div class="card reveal"><h3>Medical weight management</h3><p>Physician-supervised programs that can include GLP-1 medications when they are appropriate for you, with regular follow-ups to track progress and adjust your plan.</p></div>
    <div class="card reveal"><h3>Hormone therapy</h3><p>Hormone optimization for women and men, guided by your symptoms and lab work. Dr. Arora is Biote certified; pellet therapy is placed in person at our offices.</p></div>
    <div class="card reveal"><h3>Wellness &amp; longevity</h3><p>Personalized wellness plans, lab review and prescription options to help you feel your best.</p></div>
  </div>
</div></section>
<section><div class="wrap"><div class="prose" style="max-width:none">{disc}</div>
  <h2>Already a patient?</h2><p>Message Dr. Arora securely any time in the Spruce app. We reply during business hours.</p>
  <p><a class="btn" href="{TELE["spruce"]}" target="_blank" rel="noopener">Message Dr. Arora securely</a></p>
  <h2>Prefer an in-person visit?</h2><p>Serene Med Spa has two offices: <a href="{HUDSON["site"]}">Hudson, Ohio</a> and <a href="{BARB["site"]}">Barboursville, West Virginia</a>.</p>
  <p style="background:#fff5f2;border-left:5px solid #c0392b;padding:14px 18px;border-radius:8px;font-weight:600;max-width:760px">Telehealth is not for emergencies. If you have a medical emergency, call 911.</p>
</div></section>'''
    states = [{"@type": "State", "name": n, "sameAs": u} for n, u in [("Ohio", "https://en.wikipedia.org/wiki/Ohio"), ("West Virginia", "https://en.wikipedia.org/wiki/West_Virginia"), ("Kentucky", "https://en.wikipedia.org/wiki/Kentucky"), ("Florida", "https://en.wikipedia.org/wiki/Florida")]]
    tele_faq = [
        ("Which states is Serene Telehealth available in?", "Ohio, West Virginia, Kentucky and Florida. You must be physically located in one of these states at the time of your video visit; Dr. Robin Arora is licensed in all four."),
        ("How much does the telehealth program cost?", "The program is a flat $149 per month, which covers your video visits, follow-ups and secure messaging with the physician. Medication and labs are separate and paid directly to the pharmacy or lab. We do not bill insurance."),
        ("Can I get GLP-1 weight-loss medication through telehealth?", "After a video evaluation, Dr. Arora may prescribe GLP-1 medication (such as semaglutide or tirzepatide) when it is medically appropriate. A prescription is never guaranteed, and prescriptions go to the pharmacy of your choice."),
        ("Do you prescribe controlled substances by telehealth?", "No. Telehealth prescribing is limited to non-controlled medications. Testosterone and other controlled therapies are offered only in person at our Hudson, OH and Barboursville, WV offices."),
        ("How do video visits work?", "Visits happen by live video in the HIPAA-secure Spruce Health app. Before your first visit you complete a short consent form and upload a photo ID; the physician confirms your identity on camera."),
    ]
    ld = json.dumps([
        {"@context": "https://schema.org", "@type": "MedicalBusiness", "@id": SITE_URL + "/telehealth/#business", "name": "Serene Telehealth with Dr. Robin Arora", "url": SITE_URL + "/telehealth/", "telephone": "+1-330-775-2452",
         "image": SITE_URL + "/wp-content/uploads/2026/08/Robin-683x1024-1.jpg", "priceRange": "$149/month", "areaServed": states, "medicalSpecialty": ["Endocrinology", "Primary Care"],
         "parentOrganization": {"@id": SITE_URL + "/#organization"}, "founder": {"@type": "Person", "name": "Robin Arora, MD", "url": SITE_URL + "/our-providers/robin-arora-md/"},
         "availableService": [
             {"@type": "MedicalProcedure", "name": "Telehealth medical weight management", "procedureType": "https://schema.org/NoninvasiveProcedure", "description": "Physician-supervised weight-management program by video, which may include GLP-1 medication when appropriate."},
             {"@type": "MedicalProcedure", "name": "Telehealth hormone therapy", "procedureType": "https://schema.org/NoninvasiveProcedure", "description": "Hormone optimization for women and men guided by symptoms and lab work (non-controlled therapies by telehealth)."},
             {"@type": "MedicalProcedure", "name": "Wellness and longevity visits", "procedureType": "https://schema.org/NoninvasiveProcedure", "description": "Personalized wellness plans, lab review and prescription options."}],
         "offers": {"@type": "Offer", "name": "Serene Telehealth program", "price": "149", "priceCurrency": "USD", "priceSpecification": {"@type": "UnitPriceSpecification", "price": "149", "priceCurrency": "USD", "unitText": "per month"}, "url": SITE_URL + "/telehealth/"},
         "potentialAction": {"@type": "ReserveAction", "target": TELE["spruce"], "name": "Start a telehealth visit"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in tele_faq]},
        {"@context": "https://schema.org", "@type": "MedicalWebPage", "url": SITE_URL + "/telehealth/", "name": "Serene Telehealth", "about": {"@id": SITE_URL + "/telehealth/#business"}, "audience": {"@type": "MedicalAudience", "audienceType": "Patient", "geographicArea": states}},
    ], ensure_ascii=False)
    faq_html = '<section class="tint-sand"><div class="wrap"><div class="section-head"><span class="eyebrow">Telehealth FAQ</span><h2>Common questions</h2></div><div class="grid g2">' + "".join(f'<div class="card reveal"><h3>{q}</h3><p style="font-size:.97rem">{a}</p></div>' for q, a in tele_faq) + '</div></div></section>'
    # place the FAQ just before the "Already a patient?" block
    _k = body.find('<h2>Already a patient?</h2>')
    _sec = body.rfind('<section', 0, _k) if _k != -1 else -1
    body = (body[:_sec] + faq_html + body[_sec:]) if _sec != -1 else body + faq_html
    return shell("/telehealth/", "Serene Telehealth with Dr. Robin Arora | Weight Management & Hormone Care by Video",
                 "Telehealth weight management, hormone therapy and wellness visits with board-certified physician Robin Arora, MD for patients in Ohio, West Virginia, Kentucky and Florida. $149/month, HIPAA-secure video via Spruce.", body, ld=ld)

def thank_you():
    body = page_hero("Request received", "Thank you for reaching out to Serene Med Spa. Our team will contact you within one business day to schedule your complimentary, no-commitment consultation.", [("/", "Home"), (None, "Thank you")], "We&rsquo;ll be in touch") + f'''
<section><div class="wrap grid g3">
  <div class="card"><h3>Prefer to talk now?</h3><p>Hudson, OH &mdash; <a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a><br>Barboursville, WV &mdash; <a href="tel:{BARB["tel"]}">{BARB["phone"]}</a></p></div>
  <div class="card"><h3>Book online instead</h3><p>Pick a time that suits you.</p><div class="actions"><a class="btn btn-sm" href="{HUDSON["book"]}" target="_blank" rel="noopener">Hudson</a><a class="btn btn-sm" href="{BARB["book"]}" target="_blank" rel="noopener">Barboursville</a></div></div>
  <div class="card"><h3>While you wait</h3><p><a href="/service/">Browse treatments</a>, check <a href="/specials/">this month&rsquo;s specials</a>, or try the <a href="/recommendation-webapp/">treatment finder</a>.</p></div>
</div></section>'''
    return shell("/thank-you/", "Thank You | Serene Med Spa", "Your consultation request has been received.", body, noindex=True)

EMBED_PAGES = ["/contact-us/", "/discrimination/", "/filleriq/", "/fitzpatrick-skin-type-self-assessment/", "/liftiq-by-serene/", "/llc-privacy-policy/", "/neuromodulator-iq/",
               "/our-providers/robin-arora-md/", "/our-providers/shweta-arora/", "/our-providers/stephanie-welker-fnp-bc/", "/our-story/", "/peel-iq/", "/privacy-practices/",
               "/recommendation-webapp/", "/terms-of-service/", "/terms-of-use/", "/the-serene-hydration-bar/", "/vitalityiq/", "/aroramd-skin-confidence-report/"]
PROSE_PAGES = {
    "/post-care-instructions/": ("Post-care instructions", "Simple, treatment-by-treatment aftercare from our providers. Always follow the specific instructions you were given at your visit.", "After your visit"),
    "/return-policy/": ("Return &amp; exchange policy", "For retail skincare and product purchases.", "Legal &amp; policies"),
    "/terms-and-conditions/": ("Terms and conditions", "For use of serenemedspas.com and purchases made through the site.", "Legal &amp; policies"),
    "/p-shot-and-o-shot-treatments/": ("P-Shot &amp; O-Shot treatments", "PRP-based intimate wellness treatments for men and women, performed by our physicians.", "Intimate wellness"),
}

def build(pages, posts, render_prose, render_embed):
    out = {"/": home(posts), "/locations/": locations(), "/our-providers/": providers(pages), "/about-us/": about(pages), "/reviews/": reviews(),
           "/membership/": membership(), "/financing/": financing(), "/specials/": specials(pages), "/telehealth/": telehealth(), "/thank-you/": thank_you()}
    for p in EMBED_PAGES:
        if p in pages: out[p] = render_embed(pages[p])
    for p, (title, lede, eyebrow) in PROSE_PAGES.items():
        if p in pages: out[p] = render_prose(pages[p], title=title, lede=lede, eyebrow=eyebrow)
    return out
