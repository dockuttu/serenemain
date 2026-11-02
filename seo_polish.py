# -*- coding: utf-8 -*-
"""seo_polish.py — post-build SEO pass over bundle/site/**/*.html (pure stdlib, idempotent).

 * TITLES: shortens <title>/og:title on pages whose generated title runs past ~65 characters (Google truncates
   around 60; the override map below keeps the keyword up front and drops the long brand suffix).
 * DESCRIPTIONS: trims the four meta descriptions that ran past 165 characters.
 * H1: the VitalityIQ app shell rendered a second <h1>; demote it so the page has one H1.
 * IMAGES: loading="lazy" + decoding="async" on every <img> after the first two (hero/logo stay eager);
   the header/footer logo is served from the 300px variant with a 768px srcset instead of the 1024px file.
 * Hudson/Barboursville builds run this same file after v2_merge so the shared shell gets the same treatment.

Usage: python3 seo_polish.py [site_dir]
"""
import glob, os, re, sys

SITE = sys.argv[1] if len(sys.argv) > 1 else "bundle/site"

# path -> (title, description or None). Titles <= 60 chars.
OVERRIDES = {
    "/strength-training-women-over-40/": ("Strength Training for Women Over 40: Muscle & Protein", None),
    "/inbody-body-scan/": ("Free InBody Body Scan | Hudson, OH & Barboursville, WV", None),
    "/genetic-testing-women/": ("Genetic Testing for Women: BRCA, Lp(a) & Clotting Risk", None),
    "/menopause-mood-sleep-brain-fog/": ("Menopause Brain Fog, Mood & Sleep: What Helps | Serene",
        "Brain fog, low mood and broken sleep in menopause are common and treatable. Dr. Shweta Arora on what causes them and what helps, from hormones to sleep habits."),
    "/beyond-hormone-therapy-midlife/": ("On Hormone Therapy but Still Not Yourself? What's Missing", None),
    "/breast-health-perimenopause/": ("Breast Health in Perimenopause: Mammograms & Hormones", None),
    "/weight-loss/brand-name-medications/": ("Brand-Name Weight-Loss Medication Prices | Serene", None),
    "/membership/": (None,
        "Serene Elevate: a monthly med spa membership with a treatment credit every month, member pricing on injectables and lasers, and priority booking at both offices."),
    "/unusual-perimenopause-symptoms/": ("Unexpected Perimenopause Symptoms: Frozen Shoulder & More", None),
    "/perimenopause/": ("Perimenopause Symptoms & Treatment | Serene Med Spa",
        "Perimenopause symptoms, labs and treatment options explained by physicians. Hormone therapy and non-hormonal care in Hudson, OH, Barboursville, WV and by telehealth."),
    "/menopause-weight-gain-heart-health/": ("Menopause Weight Gain, Insulin Resistance & Heart Health",
        "Why weight shifts to the middle in menopause, how insulin resistance drives it, and what protects your heart. Physician guidance from Serene Med Spa."),
    "/perimenopause-what-i-tell-women/": ("5 Things I Tell Women About Perimenopause | Dr. Arora", None),
    "/fertility-after-35/": ("Fertility After 35: AMH Tests & Egg Freezing Explained", None),
    "/events/inbody-open-house/": ("Free InBody Open House: Nov 2 & Nov 7 | Serene Med Spa", None),
    "/gut-health-midlife/": ("Gut Health in Midlife: Menopause, Microbiome & Diet", None),
    "/brain-health-after-40/": ("Brain Health After 40: Estrogen, Exercise & MIND Diet", None),
    "/guides/skin-resurfacing/": ("Free Guide: Choosing a Facial, Peel or Laser | Serene", None),
    "/guides/laser-hair-removal/": ("Free Guide to Laser Hair Removal | Serene Med Spa", None),
    "/guides/hair-restoration/": ("Free Guide: Thinning Hair, Causes & PRP | Serene Med Spa", None),
    "/guides/injectables/": ("Free Guide: Wrinkle Relaxers & Fillers for First-Timers", None),
    "/guides/medical-weight-loss/": ("Free Guide: Lose Fat, Keep Muscle | Medical Weight Loss", None),
    "/guides/ultherapy/": ("Free Guide: Ultherapy PRIME Non-Surgical Lift | Serene", None),
    "/menopause-appetite-food-noise/": ("Menopause Appetite & Food Noise: It's Not Willpower", None),
    "/hormone-testing-menopause/": ("Do I Need My Hormones Tested? Perimenopause Labs", None),
    "/sexual-health-menopause/": ("Low Libido, Dryness & Painful Sex After 40: What Helps", None),
    "/womens-health/": ("Women's Health Library: Perimenopause & Midlife | Serene", None),
    "/everyday-chemicals-menopause-bone-health/": ("Everyday Chemicals, Menopause & Bone Health", None),
    "/perimenopause-or-thyroid/": ("Perimenopause or Thyroid? Symptoms, Tests & Both", None),
}

LOGO_OLD = "/wp-content/uploads/2024/11/Serene_Logo-1024x574.png"
LOGO_SM = "/wp-content/uploads/2024/11/Serene_Logo-300x168.png"
LOGO_MD = "/wp-content/uploads/2024/11/Serene_Logo-768x431.png"
IMG = re.compile(r"<img\b[^>]*>", re.I)
TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

changed = 0
for page in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
    html = open(page, encoding="utf-8", errors="ignore").read(); orig = html
    rel = "/" + os.path.relpath(page, SITE).replace("index.html", "").replace(os.sep, "/")
    if rel.endswith("/404.html"): rel = "/404.html"

    # --- title / description overrides (main-site pages only; location builds pass /hudson/… paths that never match)
    ov = OVERRIDES.get(rel)
    if ov:
        t, d = ov
        if t:
            html = TITLE.sub("<title>%s</title>" % esc(t), html, count=1)
            html = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + esc(t) + m.group(2), html, count=1)
            html = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1) + esc(t) + m.group(2), html, count=1)
        if d:
            html = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + esc(d) + m.group(2), html, count=1)
            html = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + esc(d) + m.group(2), html, count=1)

    # --- VitalityIQ: the embedded app rendered its own <h1>; keep the page hero as the single H1
    if rel == "/vitalityiq/":
        html = html.replace("<h1 className=", "<h2 className=").replace("</h1>\n            </div>", "</h2>\n            </div>")

    # --- images: the header logo and the first content image (likely the LCP hero) stay eager; everything else
    #     lazy-loads. Tracking pixels and small icons (<300px wide) don't count as the "first content image".
    big = [0]
    def fix(m):
        tag = m.group(0)
        if LOGO_OLD in tag and "srcset=" not in tag:
            tag = tag.replace(LOGO_OLD, LOGO_SM, 1)
            host = re.search(r'src="(https?://[^/]+)?/wp-content', tag)
            pre = host.group(1) or "" if host else ""
            tag = tag[:-1].rstrip("/") + ' srcset="%s%s 300w, %s%s 768w" sizes="220px">' % (pre, LOGO_SM, pre, LOGO_MD)
        if "Serene_Logo" in tag or "facebook.com/tr?" in tag or 'style="display:none' in tag:
            return tag
        w = re.search(r'\bwidth="(\d+)"', tag)
        is_big = (not w) or int(w.group(1)) >= 300
        if is_big:
            big[0] += 1
            if big[0] == 1:   # first content image: keep eager and prioritise it (hero / LCP candidate)
                tag = re.sub(r'\s+loading="lazy"', "", tag)
                if "fetchpriority=" not in tag: tag = tag[:-1].rstrip("/") + ' fetchpriority="high">'
                return tag
        if "loading=" not in tag:
            tag = tag[:-1].rstrip("/") + ' loading="lazy" decoding="async">'
        return tag
    html = IMG.sub(fix, html)

    if html != orig:
        open(page, "w", encoding="utf-8").write(html); changed += 1
print("seo_polish: %d page(s) updated" % changed)
