# /menopause-weight-gain-heart-health/ - perimenopause & cardiometabolic risk (drafted Oct 9 2026, pending Robin's OK).
# Lead author Shweta Arora, MD. Public copy: no prescription drug names, no supplement/peptide claims. Stats verified Oct 9 2026.
import json, html as _h
from site_lib import shell, page_hero, book_band, HUDSON, BARB, SITE_URL

QUIZ = "https://form.jotform.com/262813862138057"
SLUG = "/menopause-weight-gain-heart-health/"

FAQ = [
    ("Why am I gaining weight around my middle in my 40s?", "Fat distribution shifts during the menopause transition. In the SWAN study, women gained fat and lost lean muscle faster during perimenopause than before it, and body composition leveled off after menopause. Fat tends to move to the belly, where it is more metabolically active. Sleep loss, stress and lower activity add to it."),
    ("Does menopause really affect heart health?", "Yes. The American Heart Association reports that LDL cholesterol and apolipoprotein B rise during the transition, belly fat increases and muscle declines. Heart disease is the leading cause of death for women in the U.S., and the transition is a good time to start prevention."),
    ("What tests should I ask about?", "Blood pressure, a full lipid panel, and blood sugar markers such as A1c and fasting glucose are the basics. Depending on your history, your provider may add apolipoprotein B, lipoprotein(a), fasting insulin, a liver panel, thyroid testing or a coronary calcium scan."),
    ("Can hormone therapy protect my heart?", "Hormone therapy is prescribed to treat symptoms, not to prevent heart disease on its own. The American Heart Association notes that starting it before age 60 or within 10 years of menopause has been associated with lower cardiovascular risk, but the decision depends on your personal risk factors."),
    ("Do hot flashes matter for my heart?", "They may. Frequent hot flashes and night sweats have been linked with worse cardiovascular risk factors and early signs of artery changes. They are a good reason to check blood pressure, cholesterol and blood sugar."),
    ("Can you help with weight loss?", "Yes. Our physician-supervised medical weight-management program is available by telehealth in Ohio, West Virginia, Kentucky and Florida, with regular follow-ups. Medication is considered only when it is appropriate for you."),
]

def cardio_page():
    faq_html = "".join(f'<div class="card reveal"><h3>{q}</h3><p style="font-size:.97rem">{a}</p></div>' for q, a in FAQ)
    body = page_hero("Midlife weight gain, blood sugar and your heart",
                     "The menopause transition changes where your body stores fat, how it handles sugar and what your cholesterol looks like. It&rsquo;s also an ideal window to protect your heart for decades to come.",
                     [("/", "Home"), ("/service/", "Treatments"), (None, "Weight &amp; heart health")], "Women&rsquo;s hormone care") + f'''
<section><div class="wrap prose">
  <p style="font-size:.92rem;color:var(--muted);margin-bottom:18px">By <a href="/our-providers/shweta-arora/">Shweta Arora, MD</a>, board-certified physician &middot; Medically reviewed by <a href="/our-providers/robin-arora-md/">Robin Arora, MD</a> &middot; Updated October 2026</p>
  <p class="lede">Same diet, same workouts &mdash; yet the scale creeps up and your waistband gets tighter. If that sounds familiar in your 40s, you&rsquo;re not doing anything wrong. Your metabolism is changing, and so is your heart risk.</p>
  <div class="actions" style="margin:22px 0 8px"><a class="btn" href="{QUIZ}" target="_blank" rel="noopener">Take the 3-minute symptom check</a><a class="btn btn-outline" href="#book">Book a consult</a></div>

  <h2>What changes during the transition</h2>
  <ul>
    <li><strong>Body composition.</strong> In the long-running SWAN study, women gained fat and lost lean muscle faster during perimenopause; both leveled off after menopause.</li>
    <li><strong>Where fat goes.</strong> More fat settles around the belly and organs (visceral fat), which raises heart and diabetes risk even when weight is normal.</li>
    <li><strong>Cholesterol.</strong> LDL (&ldquo;bad&rdquo;) cholesterol and apolipoprotein B rise during the transition, according to the American Heart Association.</li>
    <li><strong>Blood sugar.</strong> Estrogen helps the body respond to insulin. As levels swing and fall, insulin resistance becomes more common.</li>
    <li><strong>Blood vessels and blood pressure.</strong> Estrogen helps arteries stay flexible; as it declines, blood pressure often climbs.</li>
  </ul>

  <h2>Why it matters</h2>
  <p>Heart disease is the leading cause of death for women in the U.S. Many of the changes above happen quietly, years before any symptom. The good news: risk factors found early are among the most treatable in medicine.</p>
  <p>Hot flashes matter too. Frequent hot flashes and night sweats have been linked with worse cardiovascular risk factors, so they&rsquo;re a reason to check your numbers, not just a nuisance.</p>

  <h2>Know your numbers</h2>
  <p>A midlife check-in should include:</p>
  <ul>
    <li>Blood pressure and waist measurement</li>
    <li>A full lipid panel, and often apolipoprotein B and a one-time lipoprotein(a)</li>
    <li>Blood sugar markers: A1c, fasting glucose and sometimes fasting insulin</li>
    <li>Liver enzymes and thyroid testing when your history suggests them</li>
    <li>A coronary calcium scan for some women with borderline risk</li>
  </ul>

  <h2>What actually helps</h2>
  <ul>
    <li><strong>Strength training</strong> 2&ndash;3 times a week to protect muscle, which drives metabolism and blood sugar control. Only about 7% of women in the transition meet physical activity guidelines.</li>
    <li><strong>Protein and fiber at every meal</strong>, fewer ultra-processed foods and less alcohol.</li>
    <li><strong>Sleep.</strong> Night sweats and poor sleep raise hunger hormones and worsen insulin resistance; treating them helps.</li>
    <li><strong>Stress.</strong> Chronic stress raises cortisol, which favors belly fat and higher blood sugar.</li>
    <li><strong>Medical treatment when needed</strong> for blood pressure, cholesterol or blood sugar.</li>
    <li><strong>Hormone therapy</strong> for bothersome symptoms when it&rsquo;s appropriate for you. It&rsquo;s prescribed for symptoms rather than heart protection alone; the American Heart Association notes that starting before 60 or within 10 years of menopause has been associated with lower cardiovascular risk.</li>
    <li><strong>Physician-supervised weight management.</strong> Our <a href="/telehealth/">medical weight-management program</a> combines nutrition, activity and, when appropriate, medication, with regular follow-ups.</li>
  </ul>
  <p>Every plan is individualized, and treatment is recommended only when it&rsquo;s right for you after your consultation. Related reading: <a href="/perimenopause/">perimenopause</a> and <a href="/menopause-mood-sleep-brain-fog/">mood, sleep &amp; brain fog</a>.</p>

  <h2>See us in person or by video</h2>
  <p>Visit our physician-led team at our <a href="{HUDSON["site"]}">Hudson, Ohio</a> or <a href="{BARB["site"]}">Barboursville, West Virginia</a> office, or meet <a href="/telehealth/">Dr. Robin Arora by telehealth</a> from anywhere in Ohio, West Virginia, Kentucky or Florida.</p>
  <p style="background:#fff5f2;border-left:5px solid #c0392b;padding:14px 18px;border-radius:8px;max-width:760px"><strong>Call 911 for:</strong> chest pain or pressure, shortness of breath, pain spreading to the arm, jaw or back, sudden weakness, numbness, trouble speaking or a drooping face. Women often have subtler heart attack symptoms, like unusual fatigue, nausea or shortness of breath &mdash; don&rsquo;t wait them out.</p>
  <p style="font-size:.85rem;color:var(--muted)">Sources: El Khoudary et al., American Heart Association Scientific Statement, <em>Circulation</em> 2020; Greendale et al., <em>JCI Insight</em> 2019 (SWAN body composition); U.S. Centers for Disease Control and Prevention, heart disease facts. This page is general education, not medical advice.</p>
</div></section>
<section class="tint-sand"><div class="wrap"><div class="section-head"><span class="eyebrow">Common questions</span><h2>Weight &amp; heart health FAQ</h2></div><div class="grid g2">{faq_html}</div></div></section>
{book_band()}'''
    ld = json.dumps([
        {"@context": "https://schema.org", "@type": "MedicalWebPage", "url": SITE_URL + SLUG, "name": "Midlife weight gain, blood sugar and heart health",
         "about": [{"@type": "MedicalCondition", "name": "Menopause"}, {"@type": "MedicalCondition", "name": "Insulin resistance"}, {"@type": "MedicalCondition", "name": "Cardiovascular disease"}],
         "audience": {"@type": "MedicalAudience", "audienceType": "Patient"}, "lastReviewed": "2026-10-09",
         "author": {"@type": "Person", "name": "Shweta Arora, MD", "url": SITE_URL + "/our-providers/shweta-arora/"},
         "reviewedBy": {"@type": "Person", "name": "Robin Arora, MD", "url": SITE_URL + "/our-providers/robin-arora-md/"}, "isPartOf": {"@type": "WebSite", "@id": SITE_URL + "/#website"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _h.unescape(a)}} for q, a in FAQ]},
    ], ensure_ascii=False)
    return shell(SLUG, "Menopause Weight Gain, Insulin Resistance & Heart Health | Serene Med Spa",
                 "Why midlife brings belly fat, rising cholesterol and insulin resistance, which numbers to check, and how a physician-led team can help. In person in OH and WV or by telehealth in OH, WV, KY and FL.", body, ld=ld)
