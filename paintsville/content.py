# -*- coding: utf-8 -*-
"""content.py — all copy for serenemedspaky.com as data: services, prices, FAQs, bios, specials.

Source of truth for prices: assets/price-sheet.jpg ("rates without any specials"). Every price on the site is
rendered from PRICES / SERVICES below, so a price change is a one-line edit here.

Compliance notes (do not remove):
  * Never use the phrase "vaginal rejuvenation" — say intimate wellness / women's wellness / pelvic floor.
  * Laser hair removal is "long-term hair reduction", never "permanent".
  * EvolveX / Forma / Morpheus8 are radiofrequency; never "laser lipo".
  * No prescription drug names or compounding-pharmacy names anywhere on the site.
"""

PRICE_NOTE = "Regular rates; current specials may apply &mdash; ask us."

# ------------------------------------------------------------------ price list (grouped for /pricing/)
LHR_AREAS = [("Upper lip", "$75"), ("Chin", "$120"), ("Lip &amp; chin", "$175"), ("Sideburns", "$150"), ("Neck", "$160"), ("Full face", "$260"),
             ("Underarm", "$175"), ("Half arm", "$200"), ("Full arm", "$350"), ("Stomach", "$300"), ("Chest &amp; abdomen", "$400"),
             ("Half back", "$300&ndash;$400"), ("Full back", "$500&ndash;$600"), ("Bikini line", "$200"), ("Upper leg", "$325"), ("Lower leg", "$325"), ("Full leg", "$600")]

PRICES = [
    ("Consultation", "/contact/", [
        ("Complimentary consultation", "Free", "30 minutes with Katrina to review goals and build a plan; no obligation")]),
    ("Injectables", "/botox-xeomin/", [
        ("Xeomin&reg;", "$10 / unit", "Wrinkle relaxer; units determined at consultation"),
        ("Botox&reg; Cosmetic", "$12 / unit", "Wrinkle relaxer; units determined at consultation"),
        ("Dermal filler (Juv&eacute;derm&reg;)", "$650 / syringe", "Cheeks, chin, jawline, smile lines and more; syringes confirmed at consultation"),
        ("Lip filler (Juv&eacute;derm&reg;)", "$500 / syringe", "Natural-looking lip volume and shape"),
        ("Lip flip", "$100", "A few units of wrinkle relaxer along the upper lip for a subtle, fuller look")]),
    ("Skin &amp; body radiofrequency", None, [
        ("Forma skin tightening", "$100 / area / treatment", "Collagen &amp; skin tightening; results can be seen after one session"),
        ("Forma face &amp; neck combo", "$150 / treatment", ""),
        ("EvolveX body toning &amp; tightening", "$100 / area / treatment", "Typically a series of 5&ndash;6 treatments"),
        ("Morpheus8 Body RF microneedling", "$600 / treatment", "Typically 1&ndash;2 treatments; results can last up to a year")]),
    ("Light &amp; laser", None, [
        ("Lumecca IPL photofacial", "$175 / treatment", "Sun spots, dark spots, redness")]),
    ("Laser hair removal (DiolazeXL)", "/laser-hair-removal/", [(a, p, "") for a, p in LHR_AREAS]),
    ("Intimate &amp; pelvic wellness (EmpowerRF)", "/intimate-wellness/", [
        ("VTone", "$350 / treatment", "EMS pelvic-floor strengthening"),
        ("FormaV", "$350 / treatment", "Gentle radiofrequency for tissue circulation, elasticity and hydration"),
        ("Morpheus8V", "$650 / treatment", "RF microneedling for laxity, dryness and diminished sensitivity")]),
    ("IV &amp; hormone wellness", None, [
        ("IV Wellness &mdash; Myers&rsquo; Cocktail", "$175", ""),
        ("Biote testosterone pellets", "$675 / insertion", "Dose based on labs and symptoms"),
        ("Biote estrogen pellets", "$675 / insertion", ""),
        ("Hormone labs", "$125", "Baseline and follow-up lab panel")]),
]

# ------------------------------------------------------------------ providers
KATRINA = {
    "id": "katrina", "name": "Katrina Watkins, NP", "role": "Nurse Practitioner &middot; Lead Provider, Paintsville",
    "img": "/img/katrina-headshot.jpg", "alt": "Katrina Watkins, NP, nurse practitioner at Serene Med Spa Paintsville, KY",
    "creds": ["Board-certified Nurse Practitioner", "InMode Optimas, EmpowerRF &amp; EvolveX trained", "Botox&reg; &amp; Xeomin&reg; injector", "Biote hormone therapy", "Eastern Kentucky native"],
    "bio": ("Katrina Watkins is the board-certified nurse practitioner who leads our Paintsville clinic. She came to aesthetics the way many great injectors do &mdash; "
            "through years of hands-on patient care, where she learned that people feel best when someone actually listens. That is still how every visit with Katrina starts: "
            "a conversation about what you see in the mirror and what you would like to change, followed by an honest plan that fits your goals and your budget.\n\n"
            "Katrina performs every treatment in the office herself, from wrinkle relaxers to InMode laser, radiofrequency and women&rsquo;s wellness procedures, under the direction of "
            "Dr. Robin Arora. She is known for a light, natural touch, for explaining things in plain language, and for being genuinely excited when patients from Paintsville, "
            "Prestonsburg, Pikeville and across Eastern Kentucky no longer have to drive to Lexington for physician-directed aesthetic care."),
}
DR_ARORA = {
    "id": "dr-arora", "name": "Robin Arora, MD, MBA", "role": "Founder &amp; Medical Director",
    "img": "/img/dr-arora.jpg", "alt": "Robin Arora, MD, MBA, founder and medical director of Serene Med Spa",
    "creds": ["Board Certified, Internal Medicine (ABIM)", "Board Certified, Nephrology &amp; Hypertension", "Certified in Aesthetic Medicine", "Biote Certified Provider", "Licensed in OH, WV, KY &amp; FL", "16+ years in practice"],
    "bio": ("Dr. Robin Arora trained in nephrology at Tulane and brings an internist&rsquo;s judgment to aesthetic and wellness medicine. He founded Serene Med Spa in Hudson, Ohio, "
            "expanded to Barboursville, West Virginia, and now to Paintsville, Kentucky &mdash; and he supervises every treatment protocol at all three offices.\n\n"
            "As medical director, Dr. Arora sets the clinical standards the Paintsville team follows, reviews hormone lab work and treatment plans, and is available to Katrina "
            "and her patients whenever a physician&rsquo;s input is needed. He is board certified by the American Board of Internal Medicine and is a Biote Certified Provider."),
}
PROVIDERS = [KATRINA, DR_ARORA]

# ------------------------------------------------------------------ specials
# One entry per live special: (title, detail, ends). Empty list = "coming soon" placeholder on /specials/.
SPECIALS = [
    # (title, description, eyebrow) — wording of the new-patient offer is Robin's standard (Oct 4 2026); keep verbatim.
    ("New-patient welcome: 20% off your first visit",
     "20% off your first visit, applies to any product or service, can&rsquo;t be combined with another discount. Mention the offer when you book, or send us the form below and Katrina will reach out.",
     "New patients &middot; Paintsville"),
]

# ------------------------------------------------------------------ services
# Each entry drives /<slug>/: title (<=60 chars), description (120-155 chars), hero, sections, prices, FAQ, JSON-LD.
SERVICES = [
 {
  "slug": "botox-xeomin", "name": "Botox&reg; &amp; Xeomin&reg;", "nav": "Botox & Xeomin",
  "short": "Wrinkle relaxers for frown lines, forehead lines and crow&rsquo;s feet from $10 per unit.",
  "title": "Botox & Xeomin in Paintsville, KY | Serene Med Spa",
  "description": "Botox $12/unit and Xeomin $10/unit in Paintsville, KY. Natural-looking wrinkle relaxer results by Katrina Watkins, NP, under physician direction.",
  "eyebrow": "Wrinkle relaxers", "h1": "Botox&reg; &amp; Xeomin&reg; in Paintsville",
  "lede": "Soften frown lines, forehead lines and crow&rsquo;s feet with precise, conservative dosing. Injected by Katrina Watkins, NP, with plans reviewed by our physician medical director.",
  "hero": "/img/botox-inject.jpg", "hero_alt": "Wrinkle relaxer injection at Serene Med Spa", "og": "/img/botox-inject.jpg",
  "price_pill": ("From $10 / unit", "Xeomin &middot; Botox $12 / unit"),
  "procedure": "Botulinum toxin injection (neuromodulator)", "body": "Face",
  "what": ["Botox&reg; Cosmetic and Xeomin&reg; are prescription neuromodulators. A few tiny injections temporarily relax the small muscles that fold the skin when you frown, squint or raise your brows, so the lines they create soften and, over time, stop etching in. Both products have long safety records; Xeomin is a &ldquo;purified&rdquo; formulation without accessory proteins, which some patients prefer.",
           "At Serene Paintsville we favor a natural look: you should still look like you, just rested. Katrina maps your muscle movement before dosing, starts conservatively on first visits, and offers a complimentary two-week check so anything can be fine-tuned."],
  "treats": ["Frown lines between the brows (the &ldquo;11s&rdquo;)", "Horizontal forehead lines", "Crow&rsquo;s feet around the eyes", "Bunny lines on the nose", "A subtle brow lift", "Lip flip and downturned mouth corners", "Chin dimpling", "Jaw clenching and masseter slimming (consultation required)"],
  "expect": [("Consultation &amp; mapping", "We talk through what bothers you, check your medical history and watch how your muscles move. You get a unit estimate and a price before anything is injected."),
             ("Treatment in about 15 minutes", "A series of very small injections with an ultra-fine needle. Most people describe a quick pinch; no numbing is needed and there is no downtime."),
             ("Results in 3&ndash;14 days", "Movement begins to soften around day 3 and is fully settled by two weeks. Results typically last 3&ndash;4 months."),
             ("Two-week check-in", "Come back at no charge so we can look at your result together and touch up if needed. Most patients maintain every 3&ndash;4 months.")],
  "prices": [("Xeomin&reg;", "$10 / unit", "Typical areas use 10&ndash;30 units each; total units confirmed at consultation"), ("Botox&reg; Cosmetic", "$12 / unit", ""),
             ("Dermal filler (Juv&eacute;derm&reg;)", "$650 / syringe", "Cheeks, chin, jawline, smile lines; syringes confirmed at consultation"), ("Lip filler (Juv&eacute;derm&reg;)", "$500 / syringe", ""), ("Lip flip", "$100", "")],
  "faqs": [("How many units will I need?", "It depends on the area and how strong your muscles are. As a rough guide, frown lines often use 15&ndash;25 units, the forehead 10&ndash;20 and crow&rsquo;s feet 10&ndash;24 in total. Katrina will give you an exact unit count and price at your consultation before treating."),
           ("Botox or Xeomin &mdash; which is better?", "Both work the same way and both are excellent. Xeomin contains only the active neurotoxin without accessory proteins and is a little less expensive per unit; Botox has the longest track record. Katrina will recommend one based on your history and goals, and you can switch later if you like."),
           ("Will I look frozen?", "Not at Serene. We dose to soften lines while keeping natural expression, and we would rather add a few units at your two-week check than over-treat on day one."),
           ("Does it hurt, and is there downtime?", "Most patients feel a brief pinch. You can return to work immediately. We ask you to stay upright, skip strenuous exercise and avoid rubbing the area for the rest of the day."),
           ("How long does it last?", "Typically 3&ndash;4 months. With regular treatment many patients find the lines soften even between visits because the muscles are no longer folding the skin all day."),
           ("Who should not have wrinkle relaxers?", "Patients who are pregnant or breastfeeding, have certain neuromuscular conditions, or have an active skin infection at the site should wait. We review your medical history at every visit.")],
  "also": ["forma", "lumecca-ipl", "morpheus8"],
 },
 {
  "slug": "laser-hair-removal", "name": "Laser Hair Removal", "nav": "Laser hair removal",
  "short": "DiolazeXL diode laser for long-term hair reduction on the face and body, from $75 per session.",
  "title": "Laser Hair Removal in Paintsville, KY | Serene Med Spa",
  "description": "DiolazeXL laser hair removal in Paintsville, KY from $75 per session. Long-term hair reduction on the face, underarms, legs, back and bikini line.",
  "eyebrow": "InMode DiolazeXL", "h1": "Laser Hair Removal in Paintsville",
  "lede": "Long-term hair reduction with the DiolazeXL diode laser on the InMode Optimas platform &mdash; fast, comfortable and priced per area, with a consultation first to confirm you are a good candidate.",
  "hero": "/img/katrina-optimas.jpg", "hero_alt": "Katrina Watkins, NP with the InMode Optimas laser platform at Serene Med Spa Paintsville", "og": "/img/katrina-optimas.jpg",
  "price_pill": ("From $75", "per area, per session"),
  "procedure": "Laser hair removal (diode laser)", "body": "Face, underarms, arms, legs, back, chest, abdomen, bikini line",
  "what": ["DiolazeXL is a high-powered diode laser that targets the pigment in the hair follicle, heating it enough to disable regrowth while a built-in cooling tip protects the surrounding skin. Its large treatment head covers areas like the back or legs quickly, and its wavelength is effective on a range of skin types.",
           "Because the laser only affects hairs in their active growth phase, a series is needed &mdash; typically 3&ndash;5 sessions spaced 4&ndash;8 weeks apart depending on the thickness, color and texture of the hair. The result is long-term hair reduction; most patients see significantly less, finer hair and need only occasional maintenance."],
  "treats": ["Upper lip, chin and sideburns", "Full face and neck", "Underarms", "Half and full arms", "Stomach, chest and abdomen", "Half and full back", "Bikini line", "Upper, lower and full legs"],
  "expect": [("Consultation &amp; candidacy check", "Laser hair removal works best on hair that is darker than the surrounding skin; very light, grey or red hair responds poorly. Katrina assesses your skin type and hair, reviews sun exposure and medications, and confirms you are a good candidate before booking a series."),
             ("Prep", "Shave the area within 24 hours of your visit, avoid waxing, plucking and tanning for 4 weeks beforehand, and come in with clean skin free of lotions or deodorant."),
             ("Treatment", "Sessions run from about 10 minutes for a lip to 45 minutes for full legs. Most patients describe a warm snapping sensation; the cooled tip keeps it very tolerable."),
             ("Aftercare &amp; series", "Mild redness fades within hours. Treated hairs shed over 1&ndash;3 weeks. Sessions are repeated every 4&ndash;8 weeks for 3&ndash;5 treatments, with a touch-up or two per year if needed.")],
  "prices": [(a, p, "") for a, p in LHR_AREAS],
  "faqs": [("Are the results long-term?", "Yes. Laser hair removal is properly described as long-term hair reduction. After a full series most patients see a large, lasting reduction in the amount, thickness and color of hair, with an occasional maintenance session to keep the area smooth."),
           ("How many sessions will I need?", "Typically 3&ndash;5, spaced 4&ndash;8 weeks apart. Hair grows in cycles and the laser only disables follicles in the active phase, so several rounds are needed to catch them all. Coarse, dark hair usually responds fastest."),
           ("Am I a candidate?", "The best candidates have hair that is darker than their skin. DiolazeXL is safe for many skin tones, but very light, grey or red hair contains too little pigment to respond. Your consultation determines candidacy, and we will tell you honestly if a different option makes more sense."),
           ("Does it hurt?", "Most people find it very manageable &mdash; a quick warm snap with each pulse, softened by the built-in cooling tip. No numbing is needed for most areas."),
           ("Can I be in the sun?", "Avoid tanning (sun, beds and self-tanner) for 4 weeks before and 2 weeks after each session, and use sunscreen on treated areas. Tanned skin raises the risk of pigment changes."),
           ("Do you offer packages?", "Yes &mdash; ask about series pricing and our current specials at your consultation. Prices listed are regular per-session rates.")],
  "also": ["lumecca-ipl", "forma", "evolvex"],
 },
 {
  "slug": "lumecca-ipl", "name": "Lumecca IPL Photofacial", "nav": "Lumecca IPL",
  "short": "Intense pulsed light for sun spots, age spots, redness and uneven tone &mdash; $175 per treatment.",
  "title": "Lumecca IPL Photofacial in Paintsville, KY | Serene",
  "description": "Lumecca IPL photofacial in Paintsville, KY — $175 per treatment for sun spots, age spots, redness and uneven skin tone on the face, neck, chest and hands.",
  "eyebrow": "InMode Lumecca", "h1": "Lumecca IPL Photofacial",
  "lede": "The most powerful IPL on the market for sun damage and pigment. Visible improvement in sun spots, dark spots and redness after just one or two sessions.",
  "hero": "/img/lumecca-hero.jpg", "hero_alt": "Clear, even skin after Lumecca IPL photofacial", "og": "/img/lumecca-hero.jpg",
  "price_pill": ("$175", "per treatment"),
  "procedure": "Intense pulsed light (IPL) photofacial", "body": "Face, neck, chest, hands, arms",
  "what": ["Lumecca is InMode&rsquo;s intense pulsed light (IPL) device. Bright flashes of light are absorbed by brown pigment (sun spots, age spots, freckles) and red pigment (broken capillaries, rosacea flushing), heating and breaking them up so the body clears them over the following days. Lumecca delivers up to three times more energy in the key wavelengths than typical IPL, which is why most patients need fewer sessions.",
           "It is the go-to treatment for the cumulative sun damage many of us in Eastern Kentucky carry from years outdoors &mdash; on the face, neck, chest and backs of the hands."],
  "treats": ["Sun spots and age spots", "Freckles and uneven pigmentation", "Redness, flushing and rosacea", "Broken capillaries and small facial veins", "Dull, sun-damaged skin on the face, neck, chest and hands"],
  "expect": [("Consultation", "Katrina reviews your skin tone, recent sun exposure and medications. IPL is best on lighter to medium skin tones and untanned skin; we will let you know if another treatment is the safer choice."),
             ("Treatment in 20&ndash;30 minutes", "Cool gel is applied and the handpiece delivers quick flashes of light. It feels like a warm snap of a rubber band; no numbing is needed."),
             ("Days 1&ndash;7", "Spots darken and look like coffee grounds, then flake away over about a week. Redness settles within hours. Wear SPF daily."),
             ("Results &amp; maintenance", "Most patients see a clear difference after one session and are happiest after two, about 4 weeks apart. A yearly session keeps new sun damage in check.")],
  "prices": [("Lumecca IPL photofacial", "$175 / treatment", "Face, neck, chest or hands; most patients do 1&ndash;2 sessions")],
  "faqs": [("How many Lumecca sessions do I need?", "Many patients see obvious improvement after one treatment; two sessions about four weeks apart is typical for heavier sun damage. A maintenance session each year helps keep new spots from building up."),
           ("What does IPL feel like?", "A quick, warm snap with each pulse. The cooled treatment tip makes it comfortable for most people without numbing cream."),
           ("Is there downtime?", "You may be pink for a few hours. Brown spots darken and then flake off over 5&ndash;7 days &mdash; makeup can be worn the next day. Avoid direct sun and use SPF 30+ afterwards."),
           ("Can Lumecca be used on darker skin?", "IPL relies on the contrast between pigment and skin, so it is most effective and safest on lighter to medium skin tones. Your consultation determines candidacy; Morpheus8 or Forma may be recommended instead."),
           ("Can I combine it with other treatments?", "Yes. Lumecca pairs well with Forma for tightening and with wrinkle relaxers for a complete refresh. Many patients do Lumecca and Forma in the same visit.")],
  "also": ["forma", "morpheus8", "botox-xeomin"],
 },
 {
  "slug": "forma", "name": "Forma Skin Tightening", "nav": "Forma",
  "short": "Painless radiofrequency skin tightening for the face and neck &mdash; $100 per area, $150 face &amp; neck.",
  "title": "Forma Skin Tightening in Paintsville, KY | Serene",
  "description": "Forma radiofrequency skin tightening in Paintsville, KY: $100 per area or $150 face and neck. No-downtime collagen treatment; results after one session.",
  "eyebrow": "InMode Forma", "h1": "Forma Radiofrequency Skin Tightening",
  "lede": "A warm, relaxing radiofrequency treatment that stimulates collagen and tightens loose skin on the face, jawline and neck. No needles, no downtime, and a glow you can see the same day.",
  "hero": "/img/forma-card.jpg", "hero_alt": "Smooth, tightened skin after Forma radiofrequency treatment", "og": "/img/forma-card.jpg",
  "price_pill": ("$100", "per area &middot; $150 face &amp; neck"),
  "procedure": "Radiofrequency skin tightening", "body": "Face, jawline, neck",
  "what": ["Forma uses bipolar radiofrequency energy to gently heat the deeper layers of the skin to the temperature at which collagen remodels and new collagen forms. Built-in temperature sensors keep the heat consistent and safe, so the treatment feels like a warm stone massage rather than a procedure.",
           "Over the weeks that follow, skin becomes firmer, smoother and more lifted. Many patients notice a tighter, glowing look after a single session &mdash; which is why Forma is popular before events &mdash; and results build with a series."],
  "treats": ["Mild to moderate skin laxity on the face and neck", "Softening jawline and early jowls", "Fine lines and crepey skin around the eyes and mouth", "Loss of firmness and &ldquo;bounce&rdquo;", "Dull skin texture"],
  "expect": [("Consultation", "Katrina assesses your skin laxity and goals and recommends a plan &mdash; often a series of 4&ndash;6 weekly sessions, then maintenance."),
             ("Treatment in 30&ndash;45 minutes", "A gliding handpiece warms the skin to a comfortable therapeutic temperature. Most patients find it relaxing enough to close their eyes."),
             ("Immediately after", "Skin looks slightly flushed and pleasantly plump for a few hours. There is no downtime; makeup can go straight on."),
             ("Results", "A visible tightening after one session, with the best results 6&ndash;8 weeks after a series as new collagen forms. Maintenance every few months keeps it going.")],
  "prices": [("Forma &mdash; one area", "$100 / treatment", "Face, neck, jawline or around the eyes"), ("Forma &mdash; face &amp; neck combo", "$150 / treatment", "")],
  "faqs": [("Does Forma hurt?", "No. Forma is one of the most comfortable treatments we offer &mdash; it feels like a hot-stone facial. There is no numbing and no downtime."),
           ("How many sessions will I need?", "Results can be seen after one session, and a series of 4&ndash;6 weekly treatments gives the most lasting collagen response. Many patients then maintain every 2&ndash;3 months."),
           ("How is Forma different from Morpheus8?", "Both use radiofrequency to build collagen. Forma is needle-free and surface-level &mdash; ideal for mild laxity and no downtime. Morpheus8 delivers RF through tiny needles deeper into the skin for more significant laxity, texture and scarring, with a few days of recovery."),
           ("Is Forma safe for all skin tones?", "Yes. Because Forma heats tissue with radiofrequency rather than light, it does not target pigment and is safe for all skin types."),
           ("When is the best time to have Forma?", "Any time of year. Many patients book a session the week of a wedding, reunion or photos for an immediate glow, then continue a series for lasting firmness.")],
  "also": ["lumecca-ipl", "morpheus8", "botox-xeomin"],
 },
 {
  "slug": "evolvex", "name": "EvolveX Body Toning", "nav": "EvolveX",
  "short": "Hands-free radiofrequency and EMS to tighten skin and tone muscle on the abdomen, arms, thighs and more.",
  "title": "EvolveX Body Toning in Paintsville, KY | Serene Med Spa",
  "description": "EvolveX body toning in Paintsville, KY — $100 per area per treatment. Hands-free radiofrequency and muscle stimulation for abdomen, arms and thighs.",
  "eyebrow": "InMode EvolveX", "h1": "EvolveX Body Toning &amp; Tightening",
  "lede": "A hands-free, non-invasive body treatment that tightens skin, remodels tissue and tones muscle with radiofrequency and electrical muscle stimulation &mdash; while you lie back and relax.",
  "hero": "/img/katrina-evolvex.jpg", "hero_alt": "Katrina Watkins, NP with the InMode EvolveX body treatment system at Serene Med Spa Paintsville", "og": "/img/katrina-evolvex.jpg",
  "price_pill": ("$100", "per area, per treatment"),
  "procedure": "Radiofrequency body contouring with electrical muscle stimulation", "body": "Abdomen, flanks, arms, thighs, buttocks",
  "what": ["EvolveX is InMode&rsquo;s all-in-one body platform. Its applicators are strapped comfortably to the treatment area and deliver two technologies: <strong>radiofrequency</strong> that heats skin and the tissue beneath to tighten and remodel, and <strong>electrical muscle stimulation (EMS)</strong> that produces deep, involuntary contractions to strengthen and define muscle. Sessions are hands-free and monitored by Katrina throughout.",
           "EvolveX is not a weight-loss treatment and it is not surgery. It is for people close to their goal who want smoother, firmer skin and better tone on the abdomen, arms, thighs or buttocks &mdash; including after pregnancy or weight change."],
  "treats": ["Loose or crepey skin on the abdomen after pregnancy or weight change", "Soft tissue and skin laxity on the upper arms", "Inner and outer thighs", "Buttock lift and tone", "Flanks (&ldquo;love handles&rdquo;)", "Core and muscle definition"],
  "expect": [("Consultation", "Katrina maps the areas that bother you, sets realistic expectations and designs a series &mdash; typically 5&ndash;6 weekly treatments per area."),
             ("Treatment in 30&ndash;60 minutes", "Applicators are placed on the area and the energy is ramped up to a comfortable level. RF feels like a deep warmth; EMS feels like a strong workout you are not doing yourself."),
             ("After", "Skin may be warm and pink for an hour. There is no downtime &mdash; most patients come in on a lunch break."),
             ("Results", "Firmness and tone improve progressively over the series and continue to develop for up to 3 months as collagen remodels. Healthy habits and occasional maintenance keep results.")],
  "prices": [("EvolveX &mdash; one area", "$100 / treatment", "Series of 5&ndash;6 treatments typically recommended; ask about series pricing")],
  "faqs": [("Is EvolveX a fat-removal or weight-loss treatment?", "No. EvolveX uses radiofrequency and muscle stimulation to tighten skin, remodel tissue and tone muscle. It is designed for people near their goal weight who want smoother, firmer, more defined areas &mdash; not as a substitute for diet, exercise or surgery."),
           ("How many treatments are needed?", "Most patients do 5&ndash;6 weekly sessions per area. Improvement is gradual and continues for about 3 months after the last session as new collagen forms."),
           ("Does it hurt?", "No. The radiofrequency feels like deep warmth and the EMS like an intense muscle workout. Katrina adjusts the intensity to your comfort throughout."),
           ("Which areas can be treated?", "Abdomen, flanks, upper arms, inner and outer thighs and buttocks are the most popular. Multiple areas can be done in one visit."),
           ("Is there downtime?", "None. You can return to normal activity, including exercise, immediately.")],
  "also": ["morpheus8", "forma", "laser-hair-removal"],
 },
 {
  "slug": "morpheus8", "name": "Morpheus8 Body", "nav": "Morpheus8",
  "short": "Fractional radiofrequency microneedling that tightens and remodels skin deep in the tissue &mdash; $600 per treatment.",
  "title": "Morpheus8 RF Microneedling in Paintsville, KY | Serene",
  "description": "Morpheus8 Body RF microneedling in Paintsville, KY — $600 per treatment. Deep collagen remodeling for loose skin and stretch marks; lasts up to a year.",
  "eyebrow": "InMode Morpheus8", "h1": "Morpheus8 RF Microneedling",
  "lede": "The gold standard in radiofrequency microneedling. Morpheus8 delivers heat deep into the tissue to tighten, tone and rebuild collagen &mdash; typically in just one or two treatments, with results that can last up to a year.",
  "hero": "/img/morpheus8.jpg", "hero_alt": "Morpheus8 radiofrequency microneedling treatment at Serene Med Spa", "og": "/img/morpheus8.jpg",
  "price_pill": ("$600", "per treatment &middot; typically 1&ndash;2"),
  "procedure": "Fractional radiofrequency microneedling", "body": "Abdomen, arms, thighs, knees, buttocks, neck, face",
  "what": ["Morpheus8 combines microneedling with radiofrequency. Ultra-fine gold-coated needles deliver RF energy at precise depths &mdash; up to 8&nbsp;mm with the Body handpiece &mdash; heating the deep layers where collagen and elastin are made and remodeling the fat and connective tissue beneath. The surface is barely disturbed, so recovery is short, but the change happens where it counts.",
           "It is the treatment we recommend for skin that is truly loose or textured &mdash; the lower abdomen after pregnancy, the upper arms, above the knees, the neck and jawline &mdash; and for stretch marks and scars. Results build for three months and can last up to a year or more."],
  "treats": ["Loose skin on the abdomen, arms, thighs and knees", "Sagging along the jawline and neck", "Stretch marks and acne scarring", "Uneven texture and crepey skin", "Fine lines and deep wrinkles", "Excess sweating (hyperhidrosis) &mdash; ask us"],
  "expect": [("Consultation", "Katrina examines the area, discusses your goals and downtime, and plans depth and number of passes. Most patients need 1&ndash;2 treatments 4&ndash;6 weeks apart."),
             ("Numbing &amp; treatment", "Strong topical numbing is applied for 30&ndash;45 minutes. The treatment itself takes 30&ndash;60 minutes and feels like warmth and pressure."),
             ("Recovery", "Expect redness and a sunburn-like feeling for 1&ndash;3 days, with tiny grid marks that fade within a week. Most patients return to work the next day."),
             ("Results", "Tightening begins within a few weeks and peaks around 3 months as collagen rebuilds. Results can last up to a year; many patients repeat annually.")],
  "prices": [("Morpheus8 Body", "$600 / treatment", "Typically 1&ndash;2 treatments; results can last up to a year")],
  "faqs": [("How is Morpheus8 different from regular microneedling?", "Standard microneedling creates micro-channels at the surface. Morpheus8 adds radiofrequency energy delivered through the needle tips at controlled depths, heating the deep dermis and the tissue below it. That is what allows true tightening and remodeling, not just texture improvement."),
           ("How many treatments do I need?", "Most patients see a meaningful change after one session and are happiest after two, spaced 4&ndash;6 weeks apart. Because it stimulates your own collagen, results continue improving for about 3 months."),
           ("How long do results last?", "Up to a year or more, depending on age, skin quality and lifestyle. Many patients schedule a single maintenance session annually."),
           ("Does Morpheus8 hurt?", "We apply a strong topical numbing cream first. With numbing, most patients describe warmth and pressure rather than pain. The tenderness afterwards is similar to a mild sunburn."),
           ("What is the downtime?", "Plan for 1&ndash;3 days of redness and mild swelling and about a week for tiny grid marks to fade. Avoid makeup for 24 hours, and sun exposure and heavy sweating for a few days."),
           ("Is Morpheus8 safe for darker skin?", "Yes. Because it uses radiofrequency rather than light, Morpheus8 does not target pigment and is safe for all skin tones when performed by a trained provider.")],
  "also": ["forma", "evolvex", "intimate-wellness"],
 },
 {
  "slug": "intimate-wellness", "name": "Intimate &amp; Pelvic Wellness", "nav": "Intimate wellness",
  "short": "EmpowerRF &mdash; VTone, FormaV and Morpheus8V &mdash; for pelvic floor strength, comfort and confidence.",
  "title": "Intimate & Pelvic Wellness in Paintsville, KY | Serene",
  "description": "Women's intimate wellness in Paintsville, KY with InMode EmpowerRF: VTone pelvic-floor EMS ($350), FormaV ($350) and Morpheus8V ($650). Private consults.",
  "eyebrow": "InMode EmpowerRF &middot; Women&rsquo;s wellness", "h1": "Intimate &amp; Pelvic Wellness",
  "lede": "Non-surgical, in-office treatments for the changes that come with childbirth, age and menopause &mdash; bladder leaks, pelvic-floor weakness, dryness and laxity. Private, unhurried appointments with Katrina Watkins, NP.",
  "hero": "/img/katrina-empowerrf.jpg", "hero_alt": "Katrina Watkins, NP with the InMode EmpowerRF women's wellness platform at Serene Med Spa Paintsville", "og": "/img/katrina-empowerrf.jpg",
  "price_pill": ("From $350", "per treatment"),
  "procedure": "Radiofrequency and electrical muscle stimulation therapy for pelvic floor and intimate tissue", "body": "Pelvic floor, vaginal and vulvar tissue",
  "what": ["EmpowerRF is InMode&rsquo;s women&rsquo;s wellness platform. It offers three complementary technologies that Katrina can use alone or in combination after a private consultation:",
           "<strong>VTone</strong> uses gentle electrical muscle stimulation (EMS) with a small intravaginal applicator to contract and strengthen the pelvic-floor muscles &mdash; think of it as a highly effective, guided Kegel workout. It is used for stress urinary incontinence (leaking with coughing, laughing or exercise), pelvic-floor weakness after pregnancy, and core strength and support.",
           "<strong>FormaV</strong> delivers controlled radiofrequency to gently warm vaginal and vulvar tissue, improving circulation, elasticity and natural hydration. It is comfortable and has no downtime.",
           "<strong>Morpheus8V</strong> is fractional radiofrequency microneedling for intimate tissue, stimulating collagen, remodeling tissue and increasing blood flow for laxity, dryness and diminished sensitivity."],
  "treats": ["Stress urinary incontinence (leaks with coughing, laughing, exercise)", "Pelvic-floor weakness after pregnancy and childbirth", "Core strength and support", "Vaginal dryness and discomfort, including after menopause", "Loss of tissue elasticity and laxity", "Diminished sensitivity", "Reduced circulation and hydration of intimate tissue"],
  "expect": [("Private consultation", "A confidential conversation with Katrina about your symptoms, history and goals, with a brief exam. We explain each option plainly and recommend a plan &mdash; often a short series of 3 sessions."),
             ("Treatment", "VTone and FormaV sessions take about 20&ndash;30 minutes, are comfortable and need no numbing. Morpheus8V takes about 30 minutes after topical numbing."),
             ("After", "VTone and FormaV have no downtime. After Morpheus8V we ask you to avoid intercourse, baths and tampons for about 3 days."),
             ("Results", "Many patients notice improvement in bladder control and comfort within a few weeks, with results building over a 3-session series and maintenance every 6&ndash;12 months.")],
  "prices": [("VTone (pelvic-floor EMS)", "$350 / treatment", "Series of 3 typically recommended"), ("FormaV (radiofrequency)", "$350 / treatment", "Series of 3 typically recommended"), ("Morpheus8V (RF microneedling)", "$650 / treatment", "Typically 1&ndash;3 treatments")],
  "faqs": [("Which EmpowerRF treatment is right for me?", "It depends on your main concern. VTone is for bladder leaks and pelvic-floor weakness; FormaV is for dryness, comfort and mild laxity with no downtime; Morpheus8V is for more significant laxity and sensitivity changes. Katrina will recommend one or a combination at a private consultation."),
           ("Do the treatments hurt?", "VTone feels like rhythmic muscle contractions and FormaV like gentle warmth; neither needs numbing. Morpheus8V is done after topical numbing and most patients describe pressure and warmth."),
           ("How many sessions are needed?", "A series of 3 sessions, 2&ndash;4 weeks apart, is typical for VTone and FormaV. Morpheus8V is usually 1&ndash;3 sessions. Maintenance every 6&ndash;12 months keeps results."),
           ("Are these treatments FDA approved?", "EmpowerRF devices are FDA-cleared for specific indications; they are not FDA-approved for intimate or sexual-wellness indications. Results vary. We discuss what the evidence supports, and what it does not, at your consultation."),
           ("Who performs the treatment, and is it private?", "All treatments are performed by Katrina Watkins, NP, in a private treatment room. Your consultation, exam and treatment are confidential."),
           ("Can I have treatment after menopause or a hysterectomy?", "Often yes &mdash; many of our patients are post-menopausal. Certain conditions and devices such as pacemakers or pelvic implants may rule out some treatments, so a consultation and medical history review is always the first step.")],
  "disclaimer": "EmpowerRF devices are FDA-cleared for specific indications; they are not FDA-approved for intimate or sexual-wellness indications. Results vary.",
  "also": ["hormone-therapy", "morpheus8", "forma"],
 },
 {
  "slug": "iv-therapy", "name": "IV Therapy", "nav": "IV therapy",
  "short": "Myers&rsquo; Cocktail vitamin and mineral infusion for energy, immunity and recovery &mdash; $175.",
  "title": "IV Therapy & Myers' Cocktail in Paintsville, KY | Serene",
  "description": "IV vitamin therapy in Paintsville, KY. The classic Myers' Cocktail infusion ($175) delivers B vitamins, vitamin C and magnesium for energy and recovery.",
  "eyebrow": "IV wellness", "h1": "IV Therapy in Paintsville",
  "lede": "A relaxing 45-minute infusion of vitamins and minerals delivered straight to the bloodstream, administered by a nurse practitioner. Hydrate, recharge and recover.",
  "hero": "/img/iv-therapy-supplies.jpg", "hero_alt": "IV vitamin infusion supplies prepared at Serene Med Spa", "og": "/img/iv-therapy-supplies.jpg",
  "price_pill": ("$175", "Myers&rsquo; Cocktail"),
  "procedure": "Intravenous vitamin and mineral infusion", "body": "Whole body",
  "what": ["IV therapy delivers fluids, vitamins and minerals directly into your bloodstream, bypassing the digestive system so that nutrients are fully available to your body right away. Our signature infusion is the classic <strong>Myers&rsquo; Cocktail</strong>: a blend of B-complex vitamins, vitamin B12, vitamin C, magnesium and calcium in sterile saline, developed decades ago and still the most requested wellness IV in the country.",
           "Every infusion at Serene Paintsville is screened and administered by Katrina Watkins, NP, in a comfortable private room. It is a supportive wellness treatment &mdash; not a replacement for medical care &mdash; and we will let you know if a visit with your physician is the better next step."],
  "treats": ["Fatigue and low energy", "Immune support during cold and flu season", "Recovery after travel, illness or a hard week", "Dehydration and headaches", "Muscle cramps and post-workout soreness", "Seasonal allergies and general wellness"],
  "expect": [("Quick screening", "A brief health history and vital signs with Katrina to confirm IV therapy is appropriate for you."),
             ("Infusion in about 45 minutes", "A small IV is placed and the infusion runs while you relax with a blanket, your phone or a book."),
             ("Right after", "Most patients feel hydrated and refreshed within hours; some notice improved energy over the next day or two."),
             ("How often", "Some patients come monthly for maintenance, others before travel or during flu season. We will help you find a rhythm that fits.")],
  "prices": [("IV Wellness &mdash; Myers&rsquo; Cocktail", "$175", "B-complex, B12, vitamin C, magnesium and calcium in saline")],
  "faqs": [("What is in a Myers&rsquo; Cocktail?", "B-complex vitamins, vitamin B12, vitamin C, magnesium and calcium in a bag of sterile saline. It is the classic wellness infusion and a good all-round choice for energy, immunity and recovery."),
           ("How long does it take?", "Plan on about an hour door to door: a short screening, then a 45-minute infusion in a comfortable private room."),
           ("Is IV therapy safe?", "For healthy adults, yes. Katrina reviews your medical history and vitals first. Patients with certain heart, kidney or other conditions may not be candidates, and we will say so."),
           ("How will I feel afterwards?", "Most people feel hydrated and clearer-headed the same day, with an energy lift over the following day or two. Effects vary from person to person."),
           ("Do you offer other infusions or add-ins?", "We are starting with the Myers&rsquo; Cocktail in Paintsville and expanding the menu &mdash; ask Katrina what is available or check our specials page.")],
  "also": ["hormone-therapy", "botox-xeomin", "forma"],
 },
 {
  "slug": "hormone-therapy", "name": "Biote Hormone Therapy", "nav": "Hormone therapy",
  "short": "Bioidentical hormone pellet therapy for women and men, with labs reviewed by our physician medical director.",
  "title": "Biote Hormone Therapy in Paintsville, KY | Serene Med Spa",
  "description": "Biote bioidentical hormone pellet therapy in Paintsville, KY for women and men. Testosterone or estrogen pellets $675, labs $125. Physician-directed care.",
  "eyebrow": "Biote Certified Provider", "h1": "Biote Hormone Therapy in Paintsville",
  "lede": "Bioidentical hormone optimization with Biote pellets for women and men &mdash; a lab-guided, physician-directed approach to the fatigue, weight change, low mood, poor sleep and low libido that often come with hormonal decline.",
  "hero": "/img/skin-analysis.jpg", "hero_alt": "Wellness consultation at Serene Med Spa", "og": "/img/skin-analysis.jpg",
  "price_pill": ("$675", "per pellet insertion &middot; labs $125"),
  "procedure": "Bioidentical hormone pellet therapy", "body": "Whole body (subcutaneous pellet insertion, hip)",
  "what": ["Biote is the nation&rsquo;s leading method of bioidentical hormone replacement using pellets: tiny, custom-dosed cylinders of testosterone or estrogen placed just under the skin of the hip in a quick office procedure. Pellets release hormone steadily for 3&ndash;5 months, avoiding the peaks and troughs of creams, pills and injections.",
           "Your care starts with a comprehensive lab panel and a symptom review. Results are interpreted by Katrina together with Dr. Robin Arora, our board-certified medical director and a Biote Certified Provider, who approves each dose. It is genuine medical care delivered in a med-spa setting &mdash; and one of the few places in Eastern Kentucky offering it."],
  "treats": ["Fatigue and low energy", "Weight gain and difficulty building muscle", "Low mood, irritability and brain fog", "Poor sleep and night sweats", "Hot flashes and menopause symptoms", "Low libido and sexual wellness", "Joint aches and reduced exercise recovery"],
  "expect": [("Labs first", "A comprehensive hormone and wellness panel ($125) drawn in office or at a local lab. We look at hormone levels along with thyroid, vitamin D and other markers."),
             ("Review &amp; plan", "Katrina reviews your results and symptoms with you; Dr. Arora approves the dose. We are clear about who is and is not a candidate."),
             ("Pellet insertion", "A 15-minute office procedure under local anesthetic: a tiny incision at the upper hip, the pellets are placed and the site is covered with a small dressing. No stitches."),
             ("Follow-up", "Repeat labs about 6 weeks later to fine-tune. Women typically re-pellet every 3&ndash;4 months, men every 5&ndash;6 months.")],
  "prices": [("Biote testosterone pellets", "$675 / insertion", "Women and men; dose based on labs"), ("Biote estrogen pellets", "$675 / insertion", ""), ("Hormone labs", "$125", "Baseline and follow-up panel")],
  "faqs": [("What are bioidentical hormones?", "Hormones that are molecularly identical to the ones your body makes. Biote pellets contain testosterone or estradiol derived from plant sources and are custom-dosed to your labs."),
           ("How long do pellets last?", "Typically 3&ndash;4 months for women and 5&ndash;6 months for men. Because the pellet dissolves slowly, hormone levels stay steady rather than spiking and crashing."),
           ("Does the insertion hurt?", "The area is numbed with local anesthetic, so most patients feel only pressure. Mild soreness or bruising at the site for a few days is normal. Avoid vigorous lower-body exercise and soaking in water for about 3 days."),
           ("Is hormone therapy safe?", "For appropriately selected patients under medical supervision, yes. Every Serene Paintsville patient has labs before treatment, dosing approved by our physician medical director, and follow-up testing. Certain histories, such as some cancers or clotting disorders, rule out treatment, and we screen for them."),
           ("Do you treat men as well as women?", "Yes. Testosterone pellet therapy for men is one of our most requested wellness services, for energy, strength, mood and libido."),
           ("What does it cost overall?", "Labs are $125 and each pellet insertion is $675, so most patients budget for 2&ndash;3 insertions a year plus follow-up labs. We will lay out the full year for you at your consultation.")],
  "also": ["iv-therapy", "intimate-wellness", "evolvex"],
 },
]
BY_SLUG = {s["slug"]: s for s in SERVICES}

# Home page arches (service, image, label) — images are 3:4 crops handled in CSS
HOME_ARCHES = [("botox-xeomin", "/img/botox-inject.jpg", "Botox &amp; Xeomin"), ("laser-hair-removal", "/img/laser.jpg", "Laser hair removal"),
               ("lumecca-ipl", "/img/lumecca-hero.jpg", "Lumecca IPL"), ("forma", "/img/forma-card.jpg", "Forma tightening"),
               ("evolvex", "/img/evolvex-hero.jpg", "EvolveX body"), ("morpheus8", "/img/morpheus8.jpg", "Morpheus8"),
               ("intimate-wellness", "/img/empowerrf-consult.jpg", "Intimate wellness"), ("hormone-therapy", "/img/skin-analysis.jpg", "Hormones &amp; IV")]
