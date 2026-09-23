# -*- coding: utf-8 -*-
"""post_overrides.py — per-article SEO overrides applied by gen_site.render_post.

Keys are article slugs. Supported fields:
  title        -> replaces the <title> / og:title (the on-page H1 is left as authored)
  description  -> replaces the meta description
  h1           -> replaces the on-page H1 (optional)
  ld_extra     -> list of extra JSON-LD objects to emit on the page (e.g. Service with price Offers)
Everything else about the article (content, FAQ schema, author) is generated automatically.
"""

SERENE_ORG = {"@type": "MedicalBusiness", "name": "Serene Med Spa", "url": "https://serenemedspas.com/"}

def _price_offer(name, price, area_url, area_name, unit="unit"):
    return {"@type": "Offer", "name": f"{name} — {area_name}", "price": str(price), "priceCurrency": "USD",
            "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(price), "priceCurrency": "USD", "unitText": f"per {unit}"},
            "url": area_url, "availability": "https://schema.org/InStock", "priceValidUntil": "2026-12-31"}

POST_OVERRIDES = {
    "/how-much-botox-cost/": {
        "title": "How Much Is Botox? $10–$20 Per Unit — 2026 Prices by Area",
        "description": "Botox costs $10–$20 per unit in 2026; frown lines (20 units) run $200–$400. See units and prices for every area, and Serene's price: $10/unit in Barboursville, WV and $11/unit in Hudson, OH.",
        "ld_extra": [{
            "@context": "https://schema.org", "@type": "Service", "name": "Botox Cosmetic (per unit)", "serviceType": "Botox injections",
            "provider": SERENE_ORG, "areaServed": ["Hudson, OH", "Barboursville, WV"],
            "offers": [
                _price_offer("Botox", 10, "https://serenemedspas.com/barboursville/botox/", "Barboursville, WV"),
                _price_offer("Botox", 11, "https://serenemedspas.com/hudson/botox/", "Hudson, OH"),
            ]}],
    },
    "/best-laser-for-tattoo-removal-guide/": {
        "title": "Best Tattoo Removal Laser (2026): Pico vs Q-Switched Compared",
        "description": "Which laser removes tattoos best? A physician compares picosecond vs Q-switched lasers on sessions, pain, ink colors and cost — with real prices at our Ohio and West Virginia offices.",
    },
    "/laser-tattoo-removal/": {
        "title": "How Laser Tattoo Removal Works: Sessions, Stages & Healing",
    },
    "/what-is-botox-guide/": {
        "title": "What Is Botox? How It Works, Results & What to Expect",
    },
    "/botox/": {
        "title": "Botox for Frown Lines: Benefits, Risks & Results | Serene Med Spa",
    },
    "/peptide-therapy-benefits-skin-hair-wellness/": {
        "title": "Peptide Therapy Benefits: Skin, Hair, Healing & Metabolism",
    },
    "/weight-loss/": {
        "title": "Weight Loss Injections Explained by a Physician (OH & WV)",
    },
    "/dermaplaning-facial-treatment-serene-med-spas/": {
        "title": "Dermaplaning Facial: Benefits, Results & Cost | Serene Med Spa",
    },
    "/botox-for-shoulder-slimming/": {
        "title": "Trap Botox (Shoulder Slimming): Units, Cost & Results",
    },
}

# authors named in the article byline -> provider profile
AUTHORS = {
    "robin arora":    {"@type": "Person", "name": "Robin Arora, MD", "jobTitle": "Physician, Founder & Medical Director", "url": "https://serenemedspas.com/our-providers/robin-arora-md/"},
    "shweta arora":   {"@type": "Person", "name": "Shweta Arora, MD", "jobTitle": "Aesthetic Physician", "url": "https://serenemedspas.com/our-providers/shweta-arora/"},
    "stephanie welker": {"@type": "Person", "name": "Stephanie Welker, FNP-BC", "jobTitle": "Nurse Practitioner", "url": "https://serenemedspas.com/our-providers/stephanie-welker-fnp-bc/"},
}
REVIEWER = AUTHORS["robin arora"]
