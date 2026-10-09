# /perimenopause/ - patient education + hormone consult page (drafted Oct 9 2026, pending Robin's OK).
# Public copy rule: no prescription drug names. Stats verified Oct 9 2026 (sources in SOURCES below).
import json
from site_lib import shell, page_hero, book_band, HUDSON, BARB, TELE, SITE_URL

QUIZ = "https://form.jotform.com/262813862138057"

PERI_FAQ = [
    ("What is perimenopause?", "Perimenopause is the transition leading up to menopause, when the ovaries&rsquo; hormone output starts to swing up and down instead of following a steady monthly rhythm. Menopause itself is confirmed after 12 months in a row without a period."),
    ("At what age does perimenopause start, and how long does it last?", "It usually starts in the mid-40s but can begin in the mid-30s. On average it lasts about four years, and for some women up to eight."),
    ("Can a blood test diagnose perimenopause?", "Usually not on its own. Hormone levels change from week to week during perimenopause, so a single normal result doesn&rsquo;t rule it out. Diagnosis is mostly based on your age, your cycle pattern and your symptoms. Labs are still useful to check thyroid, iron and other causes of the same symptoms."),
    ("Can I still get pregnant during perimenopause?", "Yes. Ovulation becomes irregular but doesn&rsquo;t stop, so keep using birth control until your provider confirms it&rsquo;s safe to stop."),
    ("Is hormone therapy safe in perimenopause?", "For many healthy women, hormone therapy started in their 40s or early 50s has a favorable balance of benefits and risks, but it isn&rsquo;t right for everyone. Your provider reviews your personal and family history, including breast cancer, blood clots, stroke and heart disease, before recommending anything."),
    ("Can I be treated by telehealth?", "Yes, if you are in Ohio, West Virginia, Kentucky or Florida at the time of your visit. Dr. Arora can evaluate symptoms, order labs and prescribe non-controlled hormone therapy by video. Hormone pellets and other in-person options are available at our Hudson and Barboursville offices."),
]

def perimenopause():
    faq_html = "".join(f'<div class="card reveal"><h3>{q}</h3><p style="font-size:.97rem">{a}</p></div>' for q, a in PERI_FAQ)
    body = page_hero("Perimenopause: when your body changes before your periods stop",
                     "Poor sleep, mood swings, brain fog, heavier periods, new aches &mdash; and a feeling that something is off. A physician-led team can help you sort out what&rsquo;s hormonal, what isn&rsquo;t, and what to do about it.",
                     [("/", "Home"), ("/service/", "Treatments"), (None, "Perimenopause")], "Women&rsquo;s hormone care") + f'''
<section><div class="wrap prose">
  <p class="lede">If you&rsquo;re in your late 30s or 40s and don&rsquo;t feel like yourself, you&rsquo;re not imagining it, and you&rsquo;re not alone. In a 2026 study of more than 7,600 U.S. women, one in three over 35 weren&rsquo;t sure whether they were in perimenopause &mdash; 42% of women aged 40&ndash;44.</p>
  <div class="actions" style="margin:22px 0 8px"><a class="btn" href="{QUIZ}" target="_blank" rel="noopener">Take the 3-minute symptom check</a><a class="btn btn-outline" href="#book">Book a hormone consult</a></div>

  <h2>What&rsquo;s actually happening</h2>
  <p>Through your 30s, each monthly cycle follows a predictable rise and fall of your ovarian hormones. As the supply of eggs dwindles, the brain pushes harder to get a response, and cycles become erratic. Some months estrogen runs high; others it crashes. The calming hormone your body makes after ovulation often drops first, because ovulation itself becomes less reliable.</p>
  <p>That uneven mix &mdash; not simply &ldquo;low hormones&rdquo; &mdash; explains why perimenopause can feel so unpredictable, and why symptoms can come and go for months at a time. Perimenopause usually begins in the mid-40s (sometimes the mid-30s) and lasts about four years on average, up to eight for some women.</p>

  <h2>Common symptoms</h2>
  <ul>
    <li><strong>Cycle changes:</strong> periods closer together or further apart, heavier or longer bleeding, spotting</li>
    <li><strong>Sleep:</strong> trouble falling asleep, waking at 3 a.m., night sweats</li>
    <li><strong>Hot flashes</strong> and flushing</li>
    <li><strong>Mood:</strong> irritability, anxiety, tearfulness, low mood, worse PMS</li>
    <li><strong>Brain fog:</strong> losing words, forgetting why you walked into a room, trouble concentrating</li>
    <li><strong>Energy and weight:</strong> fatigue, and weight that shifts to the middle even without changes in diet</li>
    <li><strong>Libido and intimacy:</strong> lower desire, vaginal dryness, discomfort with sex</li>
  </ul>

  <h2>The symptoms women don&rsquo;t connect to hormones</h2>
  <p>Estrogen receptors are found throughout the body, so the transition can show up in surprising places:</p>
  <ul>
    <li><strong>Joint and muscle aches</strong> &mdash; a review of studies found about 7 in 10 perimenopausal women report musculoskeletal pain</li>
    <li><strong>Heart palpitations</strong></li>
    <li><strong>Digestive changes</strong> such as bloating, reflux or new food sensitivities</li>
    <li><strong>Skin and hair:</strong> adult acne, dry or itchy skin, thinning hair</li>
    <li><strong>Headaches</strong> or migraines that are new or different</li>
    <li><strong>Frozen shoulder</strong>, dizziness or a burning sensation in the mouth</li>
  </ul>
  <p>Each of these can also have other causes, which is exactly why they deserve a proper evaluation instead of a shrug.</p>

  <h2>Why perimenopause gets missed</h2>
  <p>Many of these symptoms are treated one at a time &mdash; a sleep aid here, an antidepressant there &mdash; without anyone stepping back to look at the pattern. An analysis of 2019&ndash;2023 insurance claims for nearly 29 million U.S. women aged 45&ndash;51 found that only about one in five who saw a doctor for symptoms like irregular bleeding, poor sleep or mood changes received a perimenopause diagnosis.</p>
  <p>Another common pitfall is a single blood test. Because hormone levels swing from week to week, a &ldquo;normal&rdquo; result on one day doesn&rsquo;t rule perimenopause out.</p>

  <h2>How we evaluate you</h2>
  <ol>
    <li><strong>A real conversation.</strong> Your cycle history, symptoms, sleep, mood, family history and goals.</li>
    <li><strong>Targeted labs when they help.</strong> Thyroid, iron and blood count, metabolic and cholesterol markers, and hormone levels interpreted in context &mdash; not as a pass/fail test.</li>
    <li><strong>Ruling out other causes.</strong> Heavy or irregular bleeding is checked properly before anything is attributed to hormones.</li>
    <li><strong>A plan that fits your stage.</strong> What helps in early perimenopause is often different from what helps closer to menopause.</li>
  </ol>

  <h2>Treatment options</h2>
  <p>There&rsquo;s no single &ldquo;perimenopause protocol.&rdquo; Depending on your symptoms, health history and preferences, your plan may include:</p>
  <ul>
    <li><strong>Hormone therapy</strong> &mdash; bioidentical options in a pill, cream, gel, patch or (in person) <a href="/biote-hormone-therapy/">pellet</a>, at the lowest dose that controls your symptoms</li>
    <li><strong>Cycle and bleeding management</strong>, including options that also provide contraception</li>
    <li><strong>Non-hormonal treatments</strong> for hot flashes, sleep and mood when hormones aren&rsquo;t a fit</li>
    <li><strong>Metabolic support</strong> &mdash; nutrition, strength training guidance and, when appropriate, our <a href="/telehealth/">medical weight-management program</a></li>
    <li><strong>Intimate wellness</strong> for dryness and comfort, with in-office options at both locations</li>
  </ul>
  <p>Every plan is individualized, and treatment is recommended only when it&rsquo;s appropriate for you after your consultation.</p>

  <h2>See us in person or by video</h2>
  <p>Visit our physician-led team at our <a href="{HUDSON["site"]}">Hudson, Ohio</a> office (near Akron and Cleveland) or our <a href="{BARB["site"]}">Barboursville, West Virginia</a> office (near Huntington), or meet <a href="/telehealth/">Dr. Robin Arora by telehealth</a> from anywhere in Ohio, West Virginia, Kentucky or Florida.</p>
  <p style="background:#fff5f2;border-left:5px solid #c0392b;padding:14px 18px;border-radius:8px;max-width:760px"><strong>Don&rsquo;t wait on these:</strong> soaking a pad or tampon every hour, bleeding after 12 months without a period, bleeding after sex, chest pain, or thoughts of harming yourself. Call your doctor promptly &mdash; or 911 in an emergency.</p>
  <p style="font-size:.85rem;color:var(--muted)">Sources: The Menopause Society, <em>Menopause</em> (2026) perimenopause uncertainty study; Komodo Health, &ldquo;Lost in Transition&rdquo; claims analysis (2019&ndash;2023 data); Lu et al., <em>Neural Plasticity</em> 2020 meta-analysis of musculoskeletal pain; Cleveland Clinic, &ldquo;Perimenopause&rdquo;. This page is general education, not medical advice.</p>
</div></section>
<section class="tint-sand"><div class="wrap"><div class="section-head"><span class="eyebrow">Perimenopause FAQ</span><h2>Common questions</h2></div><div class="grid g2">{faq_html}</div></div></section>
{book_band()}'''
    ld = json.dumps([
        {"@context": "https://schema.org", "@type": "MedicalWebPage", "url": SITE_URL + "/perimenopause/", "name": "Perimenopause symptoms, diagnosis and treatment",
         "about": {"@type": "MedicalCondition", "name": "Perimenopause", "alternateName": "Menopausal transition"},
         "audience": {"@type": "MedicalAudience", "audienceType": "Patient"}, "lastReviewed": "2026-10-09",
         "reviewedBy": {"@type": "Person", "name": "Robin Arora, MD", "url": SITE_URL + "/our-providers/robin-arora-md/"}, "isPartOf": {"@type": "WebSite", "@id": SITE_URL + "/#website"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": __import__("html").unescape(a)}} for q, a in PERI_FAQ]},
    ], ensure_ascii=False)
    return shell("/perimenopause/", "Perimenopause Symptoms & Treatment | Serene Med Spa – Hudson, OH, Barboursville, WV & Telehealth",
                 "Physician-led perimenopause care: symptoms, why it gets missed, labs and hormone therapy options. In person in Hudson, OH and Barboursville, WV, or by telehealth in OH, WV, KY and FL.", body, ld=ld)
