# -*- coding: utf-8 -*-
"""One-shot edit: Paintsville approved pricing (Oct 4 2026). Run from serenemain/paintsville."""
import io, re, sys

def sub1(s, old, new, label):
    n = s.count(old)
    if n != 1:
        print(f"!! {label}: expected 1 match, found {n}"); sys.exit(1)
    return s.replace(old, new)

# ---------------------------------------------------------------- content.py
p = "content.py"; c = io.open(p, encoding="utf-8").read()

c = sub1(c, '''    ("Injectables", "/botox-xeomin/", [
        ("Xeomin&reg;", "$10 / unit", "Wrinkle relaxer; units determined at consultation"),
        ("Botox&reg; Cosmetic", "$12 / unit", "Wrinkle relaxer; units determined at consultation"),
        ("Dermal filler (Juv&eacute;derm&reg;)", "$650 / syringe", "Cheeks, chin, jawline, smile lines and more; syringes confirmed at consultation"),
        ("Lip filler (Juv&eacute;derm&reg;)", "$500 / syringe", "Natural-looking lip volume and shape"),
        ("Lip flip", "$100", "A few units of wrinkle relaxer along the upper lip for a subtle, fuller look")]),''',
'''    ("Injectables", "/botox-xeomin/", [
        ("Botox&reg; Cosmetic", "$10 / unit", "Wrinkle relaxer; units determined at consultation"),
        ("Xeomin&reg;", "$9 / unit", "Wrinkle relaxer; units determined at consultation"),
        ("Dysport&reg;", "$4 / unit", "Wrinkle relaxer; about 2.5&ndash;3 Dysport units equal 1 Botox unit"),
        ("Lip flip", "$80", "A few units of wrinkle relaxer along the upper lip for a subtle, fuller look"),
        ("Dermal filler (Juv&eacute;derm&reg;)", "$550 / syringe", "Cheeks, chin, jawline, smile lines and more; 2 syringes $1,000"),
        ("Lip filler (Juv&eacute;derm&reg;)", "$450 / syringe", "Natural-looking lip volume and shape"),
        ("Sculptra&reg;", "$650 / vial", "Collagen stimulator for gradual, natural volume; 2 vials $1,250")]),
    ("Peels &amp; microneedling", "/vi-peel/", [
        ("VI Peel&reg; Original", "$250", "Medical-grade peel for tone, texture and fine lines; series of 3 $650"),
        ("VI Peel&reg; Purify or Precision Plus", "$300", "Purify for acne-prone skin; Precision Plus for sun spots and melasma"),
        ("VI Peel&reg; Body", "$350", "Back, chest or arms"),
        ("Microneedling", "$200", "Texture, pores, fine lines and scars"),
        ("Microneedling with PRP", "$500", "Your own platelet-rich plasma applied during microneedling (the &ldquo;PRP facial&rdquo;)")]),''', "PRICES injectables")

c = sub1(c, '("Lumecca IPL photofacial", "$175 / treatment", "Sun spots, dark spots, redness")]),',
            '("Lumecca IPL photofacial", "$150 / treatment", "Sun spots, dark spots, redness")]),', "PRICES lumecca")
c = sub1(c, '''    ("IV &amp; hormone wellness", None, [
        ("IV Wellness &mdash; Myers&rsquo; Cocktail", "$175", ""),''',
'''    ("IV &amp; hormone wellness", None, [
        ("IV Wellness &mdash; Myers&rsquo; Cocktail", "$175", ""),
        ("Vitamin B-12 injection", "$20", "4-pack $70; walk in or add to any visit"),''', "PRICES b12")

# specials: referral
c = sub1(c, '''     "New patients &middot; Paintsville"),
]''', '''     "New patients &middot; Paintsville"),
    ("Refer a friend: $50 credit for you both",
     "When a friend you refer completes their first treatment, you each receive a $50 credit toward your next visit. Just have them mention your name when they book.",
     "Everyone &middot; Paintsville"),
]''', "SPECIALS referral")

# ---- botox-xeomin page
c = sub1(c, '''  "slug": "botox-xeomin", "name": "Botox&reg; &amp; Xeomin&reg;", "nav": "Botox & Xeomin",
  "short": "Wrinkle relaxers for frown lines, forehead lines and crow&rsquo;s feet from $10 per unit.",
  "title": "Botox & Xeomin in Paintsville, KY | Serene Med Spa",
  "description": "Botox $12/unit and Xeomin $10/unit in Paintsville, KY. Natural-looking wrinkle relaxer results by Katrina Watkins, NP, under physician direction.",
  "eyebrow": "Wrinkle relaxers", "h1": "Botox&reg; &amp; Xeomin&reg; in Paintsville",''',
'''  "slug": "botox-xeomin", "name": "Botox&reg;, Xeomin&reg; &amp; Dysport&reg;", "nav": "Botox, Xeomin & Dysport",
  "short": "Botox $10, Xeomin $9 and Dysport $4 per unit for frown lines, forehead lines and crow&rsquo;s feet.",
  "title": "Botox, Xeomin & Dysport in Paintsville, KY | Serene",
  "description": "Botox $10, Xeomin $9 and Dysport $4 per unit in Paintsville, KY. Natural-looking wrinkle relaxer results by Katrina Watkins, NP, under physician direction.",
  "eyebrow": "Wrinkle relaxers", "h1": "Botox&reg;, Xeomin&reg; &amp; Dysport&reg; in Paintsville",''', "botox head")
c = sub1(c, '"price_pill": ("From $10 / unit", "Xeomin &middot; Botox $12 / unit"),',
            '"price_pill": ("From $4 / unit", "Dysport &middot; Botox $10 &middot; Xeomin $9"),', "botox pill")
c = sub1(c, 'Botox&reg; Cosmetic and Xeomin&reg; are prescription neuromodulators.',
            'Botox&reg; Cosmetic, Xeomin&reg; and Dysport&reg; are prescription neuromodulators.', "botox what1")
c = sub1(c, 'formulation without accessory proteins, which some patients prefer.",',
            'formulation without accessory proteins, which some patients prefer. Dysport spreads a little more and often starts working a day or two sooner; its units are smaller, so about 2.5&ndash;3 Dysport units equal 1 Botox unit.",', "botox what2")
c = sub1(c, '''  "prices": [("Xeomin&reg;", "$10 / unit", "Typical areas use 10&ndash;30 units each; total units confirmed at consultation"), ("Botox&reg; Cosmetic", "$12 / unit", ""),
             ("Dermal filler (Juv&eacute;derm&reg;)", "$650 / syringe", "Cheeks, chin, jawline, smile lines; syringes confirmed at consultation"), ("Lip filler (Juv&eacute;derm&reg;)", "$500 / syringe", ""), ("Lip flip", "$100", "")],''',
'''  "prices": [("Botox&reg; Cosmetic", "$10 / unit", "Typical areas use 10&ndash;30 units each; total units confirmed at consultation"), ("Xeomin&reg;", "$9 / unit", ""),
             ("Dysport&reg;", "$4 / unit", "About 2.5&ndash;3 Dysport units equal 1 Botox unit"), ("Lip flip", "$80", ""),
             ("Dermal filler (Juv&eacute;derm&reg;)", "$550 / syringe", "Cheeks, chin, jawline, smile lines; 2 syringes $1,000"), ("Lip filler (Juv&eacute;derm&reg;)", "$450 / syringe", ""),
             ("Sculptra&reg;", "$650 / vial", "Collagen stimulator; 2 vials $1,250; results build over months and last up to 2 years")],''', "botox prices")
c = sub1(c, '''("Botox or Xeomin &mdash; which is better?", "Both work the same way and both are excellent. Xeomin contains only the active neurotoxin without accessory proteins and is a little less expensive per unit; Botox has the longest track record. Katrina will recommend one based on your history and goals, and you can switch later if you like."),''',
'''("Botox, Xeomin or Dysport &mdash; which is better?", "All three work the same way and all three are excellent. Botox has the longest track record; Xeomin contains only the active neurotoxin without accessory proteins and is a little less expensive per unit; Dysport tends to kick in a day or two sooner and suits larger areas like the forehead. Katrina will recommend one based on your history and goals, and you can switch later if you like."),
           ("Why is Dysport only $4 a unit?", "Dysport units are measured differently &mdash; roughly 2.5&ndash;3 Dysport units do the work of 1 Botox unit &mdash; so a typical frown-line treatment costs about the same with either product. We publish all three prices per unit so you can compare honestly, and Katrina quotes the total before treating."),
           ("Do you offer filler and Sculptra?", "Yes. Juv&eacute;derm dermal filler is $550 per syringe (two for $1,000), lip filler $450 per syringe, and Sculptra collagen stimulator $650 per vial (two for $1,250). Everything is planned at a free consultation, and new patients receive 20% off their first visit."),''', "botox faq")

# ---- lumecca $150
for old, new in [
    ('"short": "Intense pulsed light for sun spots, age spots, redness and uneven tone &mdash; $175 per treatment.",', '"short": "Intense pulsed light for sun spots, age spots, redness and uneven tone &mdash; $150 per treatment.",'),
    ('"description": "Lumecca IPL photofacial in Paintsville, KY — $175 per treatment for sun spots, age spots, redness and uneven skin tone on the face, neck, chest and hands.",', '"description": "Lumecca IPL photofacial in Paintsville, KY — $150 per treatment for sun spots, age spots, redness and uneven skin tone on the face, neck, chest and hands.",'),
    ('"price_pill": ("$175", "per treatment"),', '"price_pill": ("$150", "per treatment"),'),
    ('"prices": [("Lumecca IPL photofacial", "$175 / treatment", "Face, neck, chest or hands; most patients do 1&ndash;2 sessions")],', '"prices": [("Lumecca IPL photofacial", "$150 / treatment", "Face, neck, chest or hands; most patients do 1&ndash;2 sessions")],'),
    ('"also": ["forma", "morpheus8", "botox-xeomin"],\n },\n {\n  "slug": "forma"', '"also": ["vi-peel", "forma", "morpheus8"],\n },\n {\n  "slug": "forma"'),
]:
    c = sub1(c, old, new, "lumecca " + old[:30])

# ---- iv-therapy: B-12
c = sub1(c, '''  "short": "Myers&rsquo; Cocktail vitamin and mineral infusion for energy, immunity and recovery &mdash; $175.",
  "title": "IV Therapy & Myers' Cocktail in Paintsville, KY | Serene",
  "description": "IV vitamin therapy in Paintsville, KY. The classic Myers' Cocktail infusion ($175) delivers B vitamins, vitamin C and magnesium for energy and recovery.",''',
'''  "short": "Myers&rsquo; Cocktail infusion $175 and vitamin B-12 injections $20 for energy, immunity and recovery.",
  "title": "IV Therapy & B-12 Shots in Paintsville, KY | Serene",
  "description": "IV vitamin therapy in Paintsville, KY. Myers' Cocktail infusion $175 and vitamin B-12 injections $20 (4 for $70) for energy, immunity and recovery, by an NP.",''', "iv head")
c = sub1(c, '"price_pill": ("$175", "Myers&rsquo; Cocktail"),', '"price_pill": ("$175", "Myers&rsquo; Cocktail &middot; B-12 shot $20"),', "iv pill")
c = sub1(c, '"prices": [("IV Wellness &mdash; Myers&rsquo; Cocktail", "$175", "B-complex, B12, vitamin C, magnesium and calcium in saline")],',
            '"prices": [("IV Wellness &mdash; Myers&rsquo; Cocktail", "$175", "B-complex, B12, vitamin C, magnesium and calcium in saline"), ("Vitamin B-12 injection", "$20", "Quick intramuscular shot; 4-pack $70; walk in or add to any visit")],', "iv prices")
c = sub1(c, '''("Do you offer other infusions or add-ins?", "We are starting with the Myers&rsquo; Cocktail in Paintsville and expanding the menu &mdash; ask Katrina what is available or check our specials page.")],''',
'''("Do you offer B-12 shots?", "Yes &mdash; a vitamin B-12 injection is $20, or four for $70. It takes two minutes, no appointment is needed when Katrina is in, and it can be added to any visit. Many patients come in every one to two weeks for energy and metabolism support."),
           ("Do you offer other infusions or add-ins?", "We are starting with the Myers&rsquo; Cocktail in Paintsville and expanding the menu &mdash; ask Katrina what is available or check our specials page.")],''', "iv faq")

# ---- new service page: vi-peel
NEW = ''' {
  "slug": "vi-peel", "name": "VI Peel&reg; &amp; Microneedling", "nav": "VI Peel & microneedling",
  "short": "Medical-grade VI Peel from $250 and microneedling from $200 &mdash; with PRP $500 &mdash; for tone, texture, acne and scars.",
  "title": "VI Peel & Microneedling in Paintsville, KY | Serene",
  "description": "VI Peel chemical peels from $250 and microneedling from $200 (with PRP $500) in Paintsville, KY. Smoother tone, fewer dark spots, acne and scar improvement.",
  "eyebrow": "Peels &amp; microneedling", "h1": "VI Peel&reg; &amp; Microneedling in Paintsville",
  "lede": "Two of the most effective treatments for skin that looks tired, blotchy or scarred: the VI Peel family of medical-grade chemical peels, and microneedling &mdash; with the option of your own platelet-rich plasma (PRP) for a faster, brighter result.",
  "hero": "/img/facial-1.jpg", "hero_alt": "Medical-grade peel and microneedling treatment room at Serene Med Spa Paintsville", "og": "/img/facial-1.jpg",
  "price_pill": ("From $250", "VI Peel &middot; microneedling $200 &middot; with PRP $500"),
  "procedure": "Chemical peel and microneedling (collagen induction therapy)", "body": "Face, neck, chest, back, arms, hands",
  "what": ["<strong>VI Peel</strong> is a medical-grade blended peel &mdash; TCA, salicylic, retinoic and phenol acids with vitamins and minerals &mdash; that is applied in about 20 minutes and peels over 3&ndash;7 days, revealing smoother, more even skin. Unlike older peels it is comfortable, needs no downtime from normal life, and is safe for all skin tones. We carry <strong>VI Peel Original</strong> for overall tone, texture and fine lines, <strong>Purify</strong> for acne-prone skin, <strong>Precision Plus</strong> for sun spots and melasma, and <strong>VI Peel Body</strong> for the back, chest and arms.",
           "<strong>Microneedling</strong> uses a sterile pen with ultra-fine needles to create thousands of micro-channels in the skin, triggering your body to produce new collagen and elastin. It smooths texture, shrinks pores, softens fine lines and improves acne and surgical scars. Adding <strong>PRP</strong> &mdash; platelet-rich plasma spun from a small sample of your own blood and applied during the treatment (often called a &ldquo;PRP facial&rdquo;) &mdash; floods the channels with growth factors for faster healing and a brighter, plumper result."],
  "treats": ["Sun spots, age spots and uneven pigmentation", "Melasma and post-acne dark marks", "Active acne and congested, oily skin", "Acne scars and surgical scars", "Fine lines and crepey texture", "Large pores and dull, rough skin", "Sun damage on the chest, back and arms (VI Peel Body)"],
  "expect": [("Consultation", "Katrina looks at your skin, your history and your downtime, and recommends a peel formula, microneedling, or a combination series. Peels and microneedling are usually spaced 4&ndash;6 weeks apart; most patients do 3 sessions, then maintain every 3&ndash;4 months."),
             ("VI Peel &mdash; 20 minutes", "Skin is cleansed and the peel is applied in layers; it tingles and warms, then numbs itself within minutes. You leave with the solution on, wash it off at home that evening, and use the included aftercare kit."),
             ("Microneedling &mdash; 45&ndash;60 minutes", "Topical numbing for 20&ndash;30 minutes, then the pen glides over the skin with your PRP (if chosen) applied as we go. Expect a sunburn-pink look for 24&ndash;48 hours."),
             ("Results", "VI Peel: peeling days 3&ndash;5, fresh skin by day 7 and pigment continues to lift for weeks. Microneedling: glow within a week, collagen improvement building for 3 months. A series gives the most lasting change.")],
  "prices": [("VI Peel&reg; Original", "$250", "Series of 3 $650"), ("VI Peel&reg; Purify or Precision Plus", "$300", "Acne-prone skin, or sun spots and melasma"), ("VI Peel&reg; Body", "$350", "Back, chest or arms"),
             ("Microneedling", "$200", "Face; add neck or chest at consultation"), ("Microneedling with PRP", "$500", "Includes blood draw and PRP preparation")],
  "faqs": [("Which VI Peel is right for me?", "Original is the all-round choice for tone, texture and fine lines. Purify is for breakouts and oily, congested skin. Precision Plus is the strongest for sun spots and melasma. VI Peel Body treats the back, chest and arms. Katrina chooses the formula at your consultation and may alternate them over a series."),
           ("How much will I peel, and can I work?", "Most patients peel like a mild sunburn from day 3 to day 5 or 6 &mdash; flaking rather than sheets. You can work and wear mineral makeup; just avoid picking, sweating heavily and sun exposure for the week. The included aftercare kit keeps skin comfortable."),
           ("Is VI Peel safe for darker skin?", "Yes. VI Peel is formulated for all skin tones, including those that cannot safely have IPL. Katrina still reviews your history and may pre-treat for a few days before a stronger peel."),
           ("What is a PRP facial?", "Microneedling with platelet-rich plasma. A small amount of your blood is drawn and spun to concentrate the platelets; that plasma is applied during microneedling so growth factors reach the deeper skin. It speeds healing and gives a brighter, plumper result than microneedling alone. Nothing synthetic is used."),
           ("How many microneedling sessions do I need?", "For glow and texture, 1&ndash;3 sessions. For acne scars or deeper lines, 3&ndash;6 sessions spaced 4&ndash;6 weeks apart. Results build for about 3 months after each treatment as new collagen forms."),
           ("Can I combine these with other treatments?", "Yes. A VI Peel pairs well with Lumecca IPL for stubborn pigment and with Forma for tightening; microneedling with PRP is often alternated with Morpheus8 for scars and laxity. Katrina will sequence them safely.")],
  "also": ["lumecca-ipl", "morpheus8", "botox-xeomin"],
 },
 {
  "slug": "forma",'''
c = sub1(c, ''' {
  "slug": "forma",''', NEW, "insert vi-peel")

io.open(p, "w", encoding="utf-8").write(c)

# ---------------------------------------------------------------- gen_site.py
p = "gen_site.py"; g = io.open(p, encoding="utf-8").read()
g = sub1(g, '''    hl = [("Xeomin&reg;", "$10 / unit", "/botox-xeomin/"), ("Botox&reg;", "$12 / unit", "/botox-xeomin/"), ("Laser hair removal", "from $75", "/laser-hair-removal/"),
          ("Lumecca IPL", "$175", "/lumecca-ipl/"), ("Forma face &amp; neck", "$150", "/forma/"), ("Morpheus8 Body", "$600", "/morpheus8/"),
          ("VTone / FormaV", "$350", "/intimate-wellness/"), ("Myers&rsquo; Cocktail IV", "$175", "/iv-therapy/")]''',
'''    hl = [("Botox&reg;", "$10 / unit", "/botox-xeomin/"), ("Xeomin&reg;", "$9 / unit", "/botox-xeomin/"), ("Dysport&reg;", "$4 / unit", "/botox-xeomin/"), ("Laser hair removal", "from $75", "/laser-hair-removal/"),
          ("Lumecca IPL", "$150", "/lumecca-ipl/"), ("VI Peel", "from $250", "/vi-peel/"), ("Morpheus8 Body", "$600", "/morpheus8/"),
          ("Myers&rsquo; Cocktail IV", "$175", "/iv-therapy/")]''', "home highlights")
g = sub1(g, '<span class="chip">Botox from $12 / unit</span><span class="chip">Xeomin $10 / unit</span>',
            '<span class="chip">Botox $10 / unit</span><span class="chip">Xeomin $9 / unit</span><span class="chip">Dysport $4 / unit</span>', "hero chips")
g = sub1(g, 'desc = "Physician-directed med spa in Paintsville, KY: Botox $12/unit, Xeomin $10/unit, laser hair removal, Morpheus8, EmpowerRF, Biote hormones and IV therapy."',
            'desc = "Physician-directed med spa in Paintsville, KY: Botox $10/unit, Xeomin $9/unit, Dysport $4/unit, laser hair removal, VI Peel, Morpheus8, Biote hormones and IV therapy."', "home desc")
g = sub1(g, '("Face &amp; skin", ["botox-xeomin", "forma", "lumecca-ipl", "morpheus8"])', '("Face &amp; skin", ["botox-xeomin", "vi-peel", "forma", "lumecca-ipl", "morpheus8"])', "services groups")
g = sub1(g, 'desc = "Full price list for Serene Med Spa Paintsville, KY: Botox $12/unit, Xeomin $10/unit, laser hair removal from $75, Morpheus8 $600, Biote pellets $675."',
            'desc = "Full price list for Serene Med Spa Paintsville, KY: Botox $10/unit, Xeomin $9, Dysport $4, filler $550, VI Peel $250, laser hair removal from $75, Biote $675."', "pricing desc")
io.open(p, "w", encoding="utf-8").write(g)

# ---------------------------------------------------------------- site_lib.py nav
p = "site_lib.py"; s = io.open(p, encoding="utf-8").read()
s = sub1(s, '("Face & Skin", [("/botox-xeomin/", "Botox & Xeomin"), ("/forma/", "Forma skin tightening")',
            '("Face & Skin", [("/botox-xeomin/", "Botox, Xeomin & Dysport"), ("/vi-peel/", "VI Peel & microneedling"), ("/forma/", "Forma skin tightening")', "nav")
s = sub1(s, '("/iv-therapy/", "IV therapy")', '("/iv-therapy/", "IV therapy & B-12 shots")', "nav iv")
io.open(p, "w", encoding="utf-8").write(s)
print("edits applied")
