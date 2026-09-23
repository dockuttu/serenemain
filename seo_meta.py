# -*- coding: utf-8 -*-
"""seo_meta.py — page-level SEO metadata applied inside site_lib.shell() for every page.

PAGE_META[path] may set: title, description, ld (list of extra JSON-LD objects), crumbs (list of (url, name)).
default_ld(path, title, description, existing) adds BreadcrumbList + WebPage for any page that doesn't have them.
Keep titles <= 60 chars and descriptions 120-160 chars.
"""
import re

SITE_URL = "https://serenemedspas.com"
ORG_ID = SITE_URL + "/#organization"
HUD_ID = SITE_URL + "/hudson/#business"
BV_ID = SITE_URL + "/barboursville/#business"

# social / map profiles — add Facebook + Hudson Instagram when confirmed
SAME_AS = [
    "https://www.instagram.com/serene.wellness.wv",
    "https://maps.google.com/maps?q=50+W+Streetsboro+St+Suite+2,+Hudson,+OH+44236",
    "https://maps.google.com/maps?q=1+Chateau+Grove+Ln,+Barboursville,+WV+25504",
]
SAME_AS_HUDSON = ["https://maps.google.com/maps?q=50+W+Streetsboro+St+Suite+2,+Hudson,+OH+44236"]
SAME_AS_BARB = ["https://maps.google.com/maps?q=1+Chateau+Grove+Ln,+Barboursville,+WV+25504", "https://www.instagram.com/serene.wellness.wv"]

def person(name, role, url, img, creds, alumni=None, same=None):
    p = {"@type": ["Person", "Physician"] if "MD" in name else "Person", "name": name, "jobTitle": role, "url": SITE_URL + url, "image": SITE_URL + img,
         "worksFor": {"@id": ORG_ID}, "knowsAbout": ["aesthetic medicine", "injectables", "medical weight loss", "hormone therapy"], "hasCredential": [
             {"@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": c} for c in creds]}
    if alumni: p["alumniOf"] = {"@type": "CollegeOrUniversity", "name": alumni}
    return p

ROBIN = person("Robin Arora, MD, MBA", "Founder & Medical Director", "/our-providers/robin-arora-md/", "/wp-content/uploads/2026/08/Robin-683x1024-1.jpg",
               ["Board Certified, Internal Medicine (ABIM)", "Board Certified, Nephrology (ABIM)", "Biote Certified Provider"], "Maulana Azad Medical College, University of Delhi")
SHWETA = person("Shweta Arora, MD", "Aesthetic Physician", "/our-providers/shweta-arora/", "/wp-content/uploads/2026/08/Shweta-Arora-MD.png",
                ["Board Certified, Anesthesiology (ABA)", "Certified in Aesthetic Medicine (AAAM)", "Biote Certified Provider"])
STEPH = person("Stephanie Welker, FNP-BC", "Nurse Practitioner", "/our-providers/stephanie-welker-fnp-bc/", "/wp-content/uploads/2025/10/Stephanie-Welker.png",
               ["Board Certified Family Nurse Practitioner (FNP-BC)", "Biote Certified Provider"])

def webapp(name, desc, path):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "description": desc, "url": SITE_URL + path,
            "applicationCategory": "HealthApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": ORG_ID}}

PAGE_META = {
    "/": {"title": "Serene Med Spa | Hudson, OH & Barboursville, WV",
          "description": "Physician-led med spa in Hudson, OH and Barboursville, WV: Botox from $10/unit, fillers, Morpheus8, laser, weight loss and hormone care — plus telehealth in OH, WV, KY and FL."},
    "/service/": {"title": "Med Spa Treatments & Services | Serene Med Spa",
                  "description": "Every treatment at Serene Med Spa in Hudson, OH and Barboursville, WV — injectables, skin and laser, body contouring, weight loss, hormones and hair restoration — explained by our physicians."},
    "/locations/": {"title": "Locations | Serene Med Spa – Hudson, OH & Barboursville, WV",
                    "description": "Serene Med Spa offices: 50 W Streetsboro St, Hudson, OH (Cleveland/Akron) and 1 Chateau Grove Ln, Barboursville, WV (Huntington) — hours, phones, directions and telehealth for OH, WV, KY & FL.",
                    "ld": [{"@context": "https://schema.org", "@type": "ItemList", "name": "Serene Med Spa locations", "itemListElement": [
                        {"@type": "ListItem", "position": 1, "item": {"@id": HUD_ID}}, {"@type": "ListItem", "position": 2, "item": {"@id": BV_ID}}]}]},
    "/telehealth/": {"title": "Telehealth Weight Loss & Hormone Care in OH, WV, KY & FL",
                     "description": "Video visits with Robin Arora, MD for medical weight management (GLP-1), hormone therapy and wellness. $149/month program for patients in Ohio, West Virginia, Kentucky and Florida."},
    "/our-providers/": {"title": "Our Providers | Physicians & NP | Serene Med Spa",
                        "ld": [{"@context": "https://schema.org", "@type": "ItemList", "name": "Serene Med Spa providers", "itemListElement": [
                            {"@type": "ListItem", "position": i + 1, "item": p} for i, p in enumerate([ROBIN, SHWETA, STEPH])]}]},
    "/our-providers/robin-arora-md/": {"title": "Robin Arora, MD, MBA | Founder & Medical Director | Serene",
                                       "description": "Robin Arora, MD is board certified in internal medicine and nephrology, founder and medical director of Serene Med Spa (Hudson, OH & Barboursville, WV) and Serene Telehealth."},
    "/our-providers/shweta-arora/": {"title": "Shweta Arora, MD | Aesthetic Physician | Serene Med Spa",
                                     "description": "Shweta Arora, MD is a board-certified anesthesiologist and aesthetic physician known for natural-looking injectables at Serene Med Spa in Hudson, OH and Barboursville, WV.",
                                     "ld": [dict(SHWETA, **{"@context": "https://schema.org"})]},
    "/our-providers/stephanie-welker-fnp-bc/": {"title": "Stephanie Welker, FNP-BC | Nurse Practitioner | Serene",
                                                "description": "Stephanie Welker, FNP-BC is a board-certified family nurse practitioner at Serene Med Spa Barboursville, WV — injectables, hormone therapy and skin treatments.",
                                                "ld": [dict(STEPH, **{"@context": "https://schema.org"})]},
    "/about-us/": {"title": "About Serene Med Spa | Physician-Led Aesthetics & Wellness",
                   "ld": [{"@context": "https://schema.org", "@type": "AboutPage", "url": SITE_URL + "/about-us/", "mainEntity": {"@id": ORG_ID}}]},
    "/reviews/": {"ld": [{"@context": "https://schema.org", "@type": "WebPage", "url": SITE_URL + "/reviews/", "name": "Patient Reviews", "about": {"@id": ORG_ID}}]},
    "/contact-us/": {"title": "Contact Serene Med Spa | Hudson, OH & Barboursville, WV",
                     "ld": [{"@context": "https://schema.org", "@type": "ContactPage", "url": SITE_URL + "/contact-us/", "mainEntity": {"@id": ORG_ID}}]},
    "/membership/": {"title": "Serene Elevate Membership | Monthly Med Spa Plan",
                     "ld": [{"@context": "https://schema.org", "@type": "Offer", "name": "Serene Elevate Membership", "url": SITE_URL + "/membership/",
                             "description": "Monthly aesthetic membership with a monthly treatment credit, member pricing on injectables, skin, laser and IV treatments, and priority booking.",
                             "offeredBy": {"@id": ORG_ID}, "areaServed": ["Hudson, OH", "Barboursville, WV"], "category": "Membership"}]},
    "/financing/": {"title": "Financing | Cherry & CareCredit | Serene Med Spa"},
    "/blogs/": {"title": "Med Spa Blog & Treatment Guides | Serene Med Spa"},
    "/recommendation-webapp/": {"title": "Treatment Finder | Serene Med Spa", "ld": [webapp("Serene Treatment Finder", "Answer a few questions about your concerns and get a treatment shortlist to bring to your consultation.", "/recommendation-webapp/")]},
    "/neuromodulator-iq/": {"title": "NeuromodulatorIQ: Botox, Dysport, Xeomin & Daxxify Planner", "ld": [webapp("NeuromodulatorIQ", "Estimate Botox, Dysport, Xeomin or Daxxify units and cost by treatment area.", "/neuromodulator-iq/")]},
    "/filleriq/": {"title": "FillerIQ: Dermal Filler Planner by Area | Serene Med Spa", "ld": [webapp("FillerIQ", "Plan dermal filler by facial area and syringe count, with realistic expectations.", "/filleriq/")]},
    "/liftiq-by-serene/": {"title": "LiftIQ: Compare Non-Surgical Lifting Treatments | Serene", "ld": [webapp("LiftIQ", "Compare Ultherapy, Morpheus8, PDO threads and Sculptra for non-surgical lifting.", "/liftiq-by-serene/")]},
    "/peel-iq/": {"title": "PeelIQ: Chemical Peel Matcher | Serene Med Spa", "ld": [webapp("PeelIQ", "Match a chemical peel to your skin type, concern and downtime.", "/peel-iq/")]},
    "/vitalityiq/": {"title": "VitalityIQ: Hormone & Wellness Self-Check | Serene Med Spa", "ld": [webapp("VitalityIQ", "A hormone and wellness self-assessment to prepare for your consultation.", "/vitalityiq/")]},
    "/fitzpatrick-skin-type-self-assessment/": {"title": "Fitzpatrick Skin Type Quiz | Serene Med Spa", "ld": [webapp("Fitzpatrick Skin Type Quiz", "Find your Fitzpatrick skin type — it guides laser and peel safety.", "/fitzpatrick-skin-type-self-assessment/")]},
    "/the-serene-hydration-bar/": {"title": "IV Hydration Bar Menu | Serene Med Spa", "ld": [webapp("Serene IV Bar Menu", "Build an IV drip and see what's in it.", "/the-serene-hydration-bar/")]},
    "/aroramd-skin-confidence-report/": {"title": "Skin Confidence Report | Serene Med Spa", "ld": [webapp("Skin Confidence Report", "A quick skin self-assessment with a personalized treatment plan.", "/aroramd-skin-confidence-report/")]},
}

CRUMB_NAMES = {"service": "Treatments", "blogs": "Blog", "our-providers": "Our providers", "about-us": "About", "locations": "Locations", "specials": "Specials",
               "membership": "Membership", "financing": "Financing", "telehealth": "Telehealth", "reviews": "Reviews", "contact-us": "Contact"}

def breadcrumbs(path, title):
    parts = [p for p in path.strip("/").split("/") if p]
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
    acc = ""
    for i, p in enumerate(parts):
        acc += "/" + p
        name = title if i == len(parts) - 1 else CRUMB_NAMES.get(p, p.replace("-", " ").capitalize())
        items.append({"@type": "ListItem", "position": i + 2, "name": name, "item": SITE_URL + acc + "/"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def default_ld(path, title, description, existing_json):
    """Extra JSON-LD blocks a page should carry on top of whatever the renderer supplied."""
    out = []
    clean = re.sub(r"\s*\|\s*Serene.*$", "", title)
    if path != "/" and '"BreadcrumbList"' not in existing_json: out.append(breadcrumbs(path, clean))
    if not any(t in existing_json for t in ('"WebPage"', '"Article"', '"AboutPage"', '"ContactPage"', '"MedicalWebPage"', '"CollectionPage"')):
        out.append({"@context": "https://schema.org", "@type": "WebPage", "url": SITE_URL + path, "name": clean, "description": description,
                    "isPartOf": {"@type": "WebSite", "@id": SITE_URL + "/#website", "name": "Serene Med Spa", "url": SITE_URL + "/"},
                    "about": {"@id": ORG_ID}, "inLanguage": "en-US"})
    return out
