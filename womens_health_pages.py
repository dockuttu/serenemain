# Women's Health Library: 7 articles from the A4M Women's Health Summit decks (drafted Oct 9 2026) + hub page /womens-health/.
# Lead author Shweta Arora, MD; reviewed by Robin Arora, MD. Public copy rules: no prescription drug names, no supplement or peptide
# claims, no lab/test/vendor brands, testosterone in person only, no "best"/guarantees. Stats verified against primary or society
# sources Oct 9 2026 (see SOURCES on each page; briefs in Claude scratchpad).
import json, html as _h
from site_lib import shell, page_hero, book_band, HUDSON, BARB, SITE_URL

QUIZ = "https://form.jotform.com/262813862138057"
BYLINE = ('<p style="font-size:.92rem;color:var(--muted);margin-bottom:18px">By <a href="/our-providers/shweta-arora/">Shweta Arora, MD</a>, '
          'board-certified physician &middot; Medically reviewed by <a href="/our-providers/robin-arora-md/">Robin Arora, MD</a> &middot; Updated October 2026</p>')
ALERT = '<p style="background:#fff5f2;border-left:5px solid #c0392b;padding:14px 18px;border-radius:8px;max-width:760px">{}</p>'

# Every article in the library, in reading order (first three were published Oct 9 2026 from earlier decks).
LIBRARY = [
    ("/perimenopause/", "Perimenopause: symptoms, diagnosis and treatment", "The years-long transition before your last period, and why it&rsquo;s so often missed."),
    ("/menopause-mood-sleep-brain-fog/", "Mood, sleep &amp; brain fog in midlife", "What hormone swings do to the brain, and what helps."),
    ("/menopause-weight-gain-heart-health/", "Midlife weight gain, blood sugar &amp; your heart", "Why the transition is the time to know your numbers."),
    ("/perimenopause-or-thyroid/", "Is it perimenopause or your thyroid?", "Two common midlife changes with the same symptoms, and how to tell them apart."),
    ("/hormone-testing-menopause/", "Do I need my hormones tested?", "Which labs help in perimenopause, which don&rsquo;t, and why."),
    ("/menopause-appetite-food-noise/", "Menopause, appetite &amp; &ldquo;food noise&rdquo;", "Why hunger can get louder in midlife, and why it isn&rsquo;t a willpower problem."),
    ("/strength-training-women-over-40/", "Strength after 40: muscle matters more than the scale", "Simple strength checks, a realistic plan and food-first protein."),
    ("/brain-health-after-40/", "Brain health after 40: estrogen, exercise &amp; eating", "What research says about protecting your memory for the long run."),
    ("/genetic-testing-women/", "Genetic testing for women: what your DNA can and can&rsquo;t tell you", "Family history, BRCA, Lp(a), clotting risk and at-home kits."),
    ("/endometriosis-symptoms/", "Endometriosis: more than a bad period", "Signs to know, why diagnosis takes years, and when to see a specialist."),
]
_TITLES = {s: t for s, t, _ in LIBRARY}

def _related(slugs):
    links = " &middot; ".join(f'<a href="{s}">{_TITLES[s]}</a>' for s in slugs)
    return f'<p>Related reading: {links}. Browse the full <a href="/womens-health/">Women&rsquo;s Health Library</a>.</p>'

def _see_us(extra=""):
    return (f'<h2>See us in person or by video</h2><p>Visit our physician-led team at our <a href="{HUDSON["site"]}">Hudson, Ohio</a> or '
            f'<a href="{BARB["site"]}">Barboursville, West Virginia</a> office, or meet <a href="/telehealth/">Dr. Robin Arora by telehealth</a> '
            f'from anywhere in Ohio, West Virginia, Kentucky or Florida.{extra}</p>')

def _cta(quiz=True):
    q = f'<a class="btn" href="{QUIZ}" target="_blank" rel="noopener">Take the 3-minute symptom check</a>' if quiz else ""
    return f'<div class="actions" style="margin:22px 0 8px">{q}<a class="btn{" btn-outline" if quiz else ""}" href="#book">Book a consult</a></div>'

ARTICLES = {}

# ---------------------------------------------------------------------------------------------------------------- thyroid (McPherson)
ARTICLES["/perimenopause-or-thyroid/"] = dict(
    h1="Is it perimenopause or your thyroid?",
    hero="Tired, foggy, gaining weight, sleeping badly? Shifting hormones, an underactive thyroid, or both at once can cause the same symptoms. Here&rsquo;s how to tell them apart.",
    crumb="Perimenopause or thyroid?", quiz=True,
    lede="You finally mention the exhaustion, the brain fog and the five pounds that won&rsquo;t budge, and you hear &ldquo;it&rsquo;s probably perimenopause.&rdquo; Sometimes it is. Sometimes it&rsquo;s your thyroid. Quite often, it&rsquo;s both.",
    body=f'''
  <h2>Two changes, same decade</h2>
  <p>Thyroid problems are common in women. According to the American Thyroid Association, women are five to eight times more likely than men to have thyroid problems, about one woman in eight will develop one in her lifetime, and up to 60% of people with thyroid disease don&rsquo;t know it.</p>
  <p>Midlife is a common time for both changes to show up. In the SWAN study of more than 3,000 U.S. women aged 42 to 52, about 1 in 10 already had a thyroid-stimulating hormone (TSH) level outside the normal range.</p>

  <h2>The symptom overlap</h2>
  <p>Perimenopause and an underactive thyroid (hypothyroidism) can both cause:</p>
  <ul><li>Fatigue and low energy</li><li>Weight gain or trouble losing weight</li><li>Brain fog and trouble concentrating</li><li>Low mood or anxiety</li><li>Poor sleep</li><li>Low libido</li><li>Changes in your periods</li></ul>
  <p>An <em>overactive</em> thyroid can mimic perimenopause too: feeling hot, sweating, a racing heart, anxiety and trouble sleeping.</p>

  <h2>Clues that point one way or the other</h2>
  <ul>
    <li><strong>Timing.</strong> Symptoms that rise and fall with your cycle (worse sleep, irritability or anxiety the week before your period) point toward hormone swings. Symptoms that stay the same all month are worth a thyroid check.</li>
    <li><strong>Hot flashes, night sweats and vaginal dryness</strong> usually come from falling estrogen, not from an underactive thyroid.</li>
    <li><strong>Feeling cold, constipation, dry skin and thinning hair</strong> are classic underactive-thyroid signs.</li>
    <li><strong>What changed this year.</strong> In one study, people who had many symptoms that were <em>new or worse</em> over the past year were much more likely to have an underactive thyroid than people whose symptoms had been stable. Keep a list.</li>
  </ul>

  <h2>&ldquo;My labs are normal, but I don&rsquo;t feel normal&rdquo;</h2>
  <p>A thyroid check usually starts with TSH. Depending on your symptoms and history, it may make sense to add:</p>
  <ul>
    <li><strong>Free T4</strong>, the main hormone the thyroid makes.</li>
    <li><strong>Thyroid antibodies (TPO).</strong> They point to autoimmune thyroid disease, the most common cause of an underactive thyroid. In a 20-year study of women, those with both a raised TSH and positive antibodies were far more likely to develop an underactive thyroid over time.</li>
  </ul>
  <p>&ldquo;Subclinical&rdquo; hypothyroidism means TSH is a little high while free T4 is still normal. It affects up to 10% of adults. Whether to treat it depends on how high the TSH is, your symptoms, your age, your antibodies and whether you&rsquo;re planning pregnancy. It&rsquo;s a conversation, not an automatic yes or no.</p>
  <p>Get labs drawn the same way each time, with the same lab and at about the same time of day, so results can be compared fairly. TSH naturally runs higher in the morning than in the afternoon.</p>

  <h2>Already on thyroid medication and still not right?</h2>
  <p>You&rsquo;re not alone. In a Mayo Clinic chart review, about 1 in 4 people on thyroid medication still had symptoms even though their TSH was normal. An older study of more than 25,000 people found that about 40% of those taking thyroid medication had a TSH outside the normal range.</p>
  <p>Worth reviewing with your clinician: how and when you take your dose, other medicines that affect absorption, iron and vitamin levels, sleep, mood, and whether perimenopause is adding its own symptoms on top.</p>

  <h2>Starting or stopping estrogen? Check your thyroid too</h2>
  <p>Estrogen taken by mouth raises a blood protein that carries thyroid hormone, which can lower the amount of free hormone available. In a study in the <em>New England Journal of Medicine</em>, 7 of 18 women on thyroid medication needed a higher dose after starting estrogen by mouth. Estrogen through the skin has much less effect on that protein.</p>
  <p>If you take thyroid medication, ask whether to recheck your thyroid levels in the weeks after starting, stopping or changing estrogen.</p>

  <h2>How we look at the whole picture</h2>
  <p>At a hormone visit we review your cycle, symptoms and history, check your thyroid when it&rsquo;s indicated, and coordinate with your primary care clinician or endocrinologist when needed. Every plan is individualized, and treatment is recommended only when it&rsquo;s right for you.</p>
''',
    alert="",
    related=["/perimenopause/", "/hormone-testing-menopause/", "/menopause-mood-sleep-brain-fog/"],
    faq=[
        ("Can perimenopause cause thyroid problems?", "Perimenopause doesn&rsquo;t cause thyroid disease, but both are common in women in their 40s and 50s and they share many symptoms, so it&rsquo;s easy to miss one when the other is present."),
        ("Which thyroid tests should I ask for?", "TSH is the usual first test. Free T4 and thyroid antibodies (TPO) are often added when symptoms or history suggest a problem. Your clinician will choose based on your situation."),
        ("Do hot flashes mean it&rsquo;s my thyroid?", "Usually not. Hot flashes and night sweats are most often caused by falling estrogen. An overactive thyroid can cause heat intolerance and sweating, though, which is one reason a thyroid check can help."),
        ("I take thyroid medication. Does hormone therapy change my dose?", "It can. Estrogen taken by mouth can raise the amount of thyroid medication some women need. Estrogen through the skin has much less effect. Ask about rechecking your levels after any change."),
        ("Can you treat my thyroid by telehealth?", "We can review symptoms and order thyroid labs by telehealth in Ohio, West Virginia, Kentucky and Florida, and coordinate with your primary care clinician or endocrinologist."),
    ],
    sources="American Thyroid Association press room (general thyroid statistics); Sowers et al., <em>Clinical Endocrinology</em> 2003 (SWAN); Canaris et al., <em>J Gen Intern Med</em> 1997 and <em>Arch Intern Med</em> 2000; Vanderpump et al., <em>Clinical Endocrinology</em> 1995 (Whickham survey); Biondi, Cappola &amp; Cooper, <em>JAMA</em> 2019; Hidalgo et al., <em>Endocrine Practice</em> 2024 (via American Thyroid Association); Arafah, <em>NEJM</em> 2001.",
    about=["Hypothyroidism", "Perimenopause"],
    seo_title="Perimenopause or Thyroid? Symptoms, Tests & When It's Both | Serene Med Spa",
    seo_desc="Fatigue, weight gain, brain fog? In your 40s it may be perimenopause, your thyroid, or both. Learn the overlap and which thyroid tests to ask about.",
)

# ---------------------------------------------------------------------------------------------------------------- hormone testing (Zava)
ARTICLES["/hormone-testing-menopause/"] = dict(
    h1="Do I need my hormones tested?",
    hero="It&rsquo;s one of the most common questions we hear. For most women over 45, the honest answer is no &mdash; but some blood tests really do matter. Here&rsquo;s which, and why.",
    crumb="Hormone testing", quiz=True,
    lede="It seems logical: if hormones are changing, a hormone test should show it. In perimenopause, though, hormone levels can swing from week to week, so a single result is a snapshot of one moment, not a diagnosis.",
    body='''
  <h2>The short answer: over 45, your story is the test</h2>
  <p>For healthy women over 45, national guidelines (including the U.K.&rsquo;s National Institute for Health and Care Excellence, NICE) diagnose perimenopause from symptoms such as hot flashes and changing periods, and menopause after 12 months without a period, without lab tests.</p>
  <p>NICE specifically advises against using estradiol, anti-M&uuml;llerian hormone (AMH) or inhibin levels to diagnose perimenopause or menopause in women over 45.</p>

  <h2>Why one hormone test can&rsquo;t &ldquo;catch&rdquo; perimenopause</h2>
  <ul>
    <li><strong>Levels swing.</strong> Follicle-stimulating hormone (FSH) and estradiol can change from day to day in perimenopause. A &ldquo;normal&rdquo; result on a good week doesn&rsquo;t rule the transition out.</li>
    <li><strong>Birth control changes the numbers.</strong> FSH isn&rsquo;t reliable while you&rsquo;re using combined hormonal birth control or high-dose progestogen.</li>
    <li><strong>Results rarely change the plan.</strong> Treatment is guided by your symptoms, your health history and your preferences.</li>
  </ul>
  <p>Read more about how perimenopause is recognized in our <a href="/perimenopause/">perimenopause guide</a>.</p>

  <h2>When blood tests are worth it</h2>
  <ul>
    <li><strong>You&rsquo;re under 40 to 45</strong> and your periods have become irregular or stopped. Early or premature menopause needs a proper workup, and NICE advises FSH on two samples taken 4 to 6 weeks apart rather than a single test.</li>
    <li><strong>Heavy, very frequent or unusual bleeding</strong>, or any bleeding after 12 months without a period.</li>
    <li><strong>Symptoms that could be something else</strong>, such as thyroid problems, high prolactin or pregnancy. See <a href="/perimenopause-or-thyroid/">perimenopause or thyroid?</a></li>
    <li><strong>You&rsquo;ve had a hysterectomy</strong> and the picture is unclear without periods to track.</li>
  </ul>

  <h2>Saliva, urine and finger-prick hormone kits</h2>
  <p>Home hormone panels can look precise, but they aren&rsquo;t recommended for diagnosing menopause. The Menopause Society states that it does not recommend saliva testing to determine hormone levels, and that testing isn&rsquo;t needed to decide whether a woman has the &ldquo;right amount&rdquo; of hormones.</p>
  <p>Hormone creams and gels add another problem: hormone left on the skin or fingers can contaminate a sample. In one hospital review of 578 people using testosterone gel, several very high blood results were traced to gel contaminating the draw site.</p>

  <h2>If you start hormone therapy</h2>
  <p>For most women, how you feel is the main guide: symptom relief, side effects and bleeding patterns, along with blood pressure and your routine screenings. Blood tests do play a role for some treatments, such as testosterone, where levels are checked to keep you in a safe range. Testosterone for women is considered mainly for low sexual desire, and at Serene it is evaluated and prescribed in person only, never by telehealth.</p>

  <h2>Midlife labs that matter anyway</h2>
  <p>Even when hormone tests aren&rsquo;t needed, midlife is a good time to check the numbers that shape your long-term health: blood pressure, cholesterol, blood sugar (A1c) and other screenings based on your history. See <a href="/menopause-weight-gain-heart-health/">midlife weight gain &amp; heart health</a>.</p>

  <h2>What to bring to your visit</h2>
  <ul><li>A 2 to 3 month log of symptoms and periods</li><li>Your medicines and birth control</li><li>Your family history</li><li>Any outside lab results, so we can review them together</li></ul>
''',
    alert="",
    related=["/perimenopause/", "/perimenopause-or-thyroid/", "/menopause-weight-gain-heart-health/"],
    faq=[
        ("Can a blood test tell me if I&rsquo;m in perimenopause?", "Usually not on its own. Hormone levels swing during perimenopause, so one normal result doesn&rsquo;t rule it out. For women over 45, the diagnosis is based on symptoms and changes in your periods."),
        ("Should I use a saliva or urine hormone test?", "Leading menopause organizations don&rsquo;t recommend them for diagnosing menopause or setting hormone doses. Levels vary and don&rsquo;t reliably match how you feel."),
        ("When do I actually need hormone labs?", "If you&rsquo;re under 40 to 45 with missed or stopped periods, have heavy or unusual bleeding, or have symptoms that could come from your thyroid, prolactin or pregnancy."),
        ("Will you check my levels if I start hormone therapy?", "It depends on the treatment. For most estrogen and progesterone treatments we follow your symptoms and side effects. Some treatments, such as testosterone, are monitored with blood tests."),
        ("Can testosterone be prescribed by telehealth?", "No. At Serene, testosterone is evaluated and prescribed in person only."),
    ],
    sources="NICE guideline NG23, Menopause: diagnosis and management; The Menopause Society, &ldquo;What is hormone testing?&rdquo;; Australasian Menopause Society, Diagnosing menopause; Davis et al., Global Consensus Position Statement on Testosterone Therapy for Women, <em>J Clin Endocrinol Metab</em> 2019; Pinedo Pichilingue et al., <em>Heliyon</em> 2023.",
    about=["Menopause", "Perimenopause"],
    seo_title="Do I Need My Hormones Tested? Perimenopause & Menopause Labs | Serene Med Spa",
    seo_desc="Can a hormone test confirm perimenopause? Learn which blood tests help, why saliva and urine kits don't, and what matters most. Physician-led care.",
)

# ---------------------------------------------------------------------------------------------------------------- appetite / food noise (Class)
ARTICLES["/menopause-appetite-food-noise/"] = dict(
    h1="Menopause, appetite and &ldquo;food noise&rdquo;",
    hero="Thinking about food more than you used to? Hungrier at night, harder to feel full? Midlife changes the signals that run appetite. It isn&rsquo;t a willpower problem.",
    crumb="Appetite &amp; food noise", quiz=True,
    lede="&ldquo;Food noise&rdquo; is the constant background chatter about what to eat next. Many women notice it getting louder in their 40s, often alongside a waistline that&rsquo;s changing while the scale barely moves. Both have a biological explanation.",
    body='''
  <h2>Same weight, different body</h2>
  <p>In the long-running SWAN study of U.S. women, the rate of fat gain roughly doubled during the menopause transition while lean muscle started to decline. Weight on the scale rose only slowly, so the change was easy to miss. The shift began about two years before the final period and leveled off a year or two after it.</p>
  <p>That&rsquo;s why the scale alone can be misleading in midlife. Where fat goes matters too; we cover that in <a href="/menopause-weight-gain-heart-health/">midlife weight gain &amp; heart health</a>.</p>

  <h2>Why appetite can get louder</h2>
  <ul>
    <li><strong>Fullness is hormonal.</strong> Your gut releases hormones after you eat that tell your brain you&rsquo;ve had enough. How strongly you feel those signals varies from person to person.</li>
    <li><strong>Short sleep raises hunger.</strong> Night sweats and 3 a.m. wake-ups leave you hungrier and craving quick energy the next day.</li>
    <li><strong>Stress and caregiving load.</strong> Chronic stress keeps cortisol up and makes comfort eating more likely, especially for women caring for kids and parents at the same time.</li>
    <li><strong>Highly processed food.</strong> Foods designed to be easy to overeat make fullness signals harder to hear.</li>
  </ul>

  <h2>What helps quiet it</h2>
  <ul>
    <li><strong>Protein and fiber at each meal.</strong> Both help you feel full longer. Think eggs, Greek yogurt, fish, chicken, beans and lentils, plus vegetables, fruit and whole grains.</li>
    <li><strong>Regular meals</strong> rather than skipping and grazing later.</li>
    <li><strong>A 10-minute walk after eating.</strong> An easy habit that also helps blood sugar.</li>
    <li><strong>Sleep.</strong> Treating night sweats and protecting sleep is one of the most underrated appetite tools. See <a href="/menopause-mood-sleep-brain-fog/">mood, sleep &amp; brain fog</a>.</li>
    <li><strong>Strength training</strong> at least two days a week to protect muscle. See <a href="/strength-training-women-over-40/">strength after 40</a>.</li>
    <li><strong>Less alcohol</strong>, which loosens food decisions and disrupts sleep.</li>
  </ul>

  <h2>Measure what matters</h2>
  <ul>
    <li><strong>Body composition</strong> (fat and muscle), not weight alone.</li>
    <li><strong>Waist size.</strong> The National Heart, Lung, and Blood Institute considers a waist over 35 inches in women a sign of higher risk for heart disease and type 2 diabetes.</li>
    <li><strong>A1c.</strong> Below 5.7% is normal, 5.7% to 6.4% is prediabetes and 6.5% or higher is diabetes, per the CDC.</li>
  </ul>

  <h2>If you use, or plan to stop, a prescription weight medication</h2>
  <p>Prescription weight medications can quiet appetite a great deal. They work as part of a longer plan. In one large clinical trial, people regained about two-thirds of the weight they had lost within a year of stopping treatment. If you&rsquo;re taking one:</p>
  <ul><li>Talk with your clinician before stopping, and plan the next step together.</li><li>Keep up strength training and protein to protect muscle while you lose weight.</li><li>Build the sleep, meal and movement habits that will carry you after treatment.</li></ul>
  <p>Our physician-supervised <a href="/telehealth/">medical weight-management program</a> combines nutrition, activity and, only when appropriate, medication, with regular follow-ups.</p>

  <h2>When to ask for more support</h2>
  <p>If eating feels out of control, you eat large amounts in secret, or food is tangled up with guilt or low mood, please tell us. Those patterns deserve real support, and we can connect you with behavioral health and nutrition care.</p>
''',
    alert="",
    related=["/menopause-weight-gain-heart-health/", "/strength-training-women-over-40/", "/menopause-mood-sleep-brain-fog/"],
    faq=[
        ("What is food noise?", "Food noise is a common term for persistent, intrusive thoughts about food. It reflects appetite signaling, sleep, stress and environment, not a lack of willpower."),
        ("Why am I hungrier in perimenopause?", "Poor sleep from night sweats, stress, and changes in body composition can all turn up hunger. Protein and fiber at meals, regular eating and better sleep often help."),
        ("Why is my waist bigger when my weight hasn&rsquo;t changed much?", "During the menopause transition fat gain speeds up while muscle declines, so body shape can change even when the scale barely moves."),
        ("What happens if I stop a weight-loss medication?", "Weight often returns. In one large trial people regained about two-thirds of the weight they had lost within a year. Plan any change with your clinician."),
        ("Can you help by telehealth?", "Yes. Our medical weight-management program is available by telehealth in Ohio, West Virginia, Kentucky and Florida."),
    ],
    sources="Greendale et al., <em>JCI Insight</em> 2019 (SWAN body composition); National Heart, Lung, and Blood Institute, overweight and obesity; U.S. Centers for Disease Control and Prevention, A1c test and physical activity guidelines; Wilding et al., <em>Diabetes, Obesity and Metabolism</em> 2022 (weight after treatment withdrawal).",
    about=["Menopause", "Obesity"],
    seo_title="Menopause Appetite & Food Noise: Why It's Not Willpower | Serene Med Spa",
    seo_desc="Hungrier in your 40s? Why appetite and food noise get louder in midlife, what the scale misses, and practical ways to quiet cravings. Physician-led care.",
)

# ---------------------------------------------------------------------------------------------------------------- strength (Virgin)
ARTICLES["/strength-training-women-over-40/"] = dict(
    h1="Strength after 40: why muscle matters more than the scale",
    hero="Your metabolism isn&rsquo;t broken. What changes most in midlife is muscle, and muscle is something you can measure, train and feed.",
    crumb="Strength after 40", quiz=False,
    lede="&ldquo;My metabolism slowed down&rdquo; is one of the most common things we hear from women in their 40s. The research tells a more hopeful story.",
    body='''
  <h2>Your metabolism isn&rsquo;t &ldquo;broken&rdquo;</h2>
  <p>A large study in <em>Science</em> measured daily energy use in thousands of people across the lifespan. Adjusted for body size, it stayed remarkably steady from about age 20 to 60.</p>
  <p>Muscle is a different story. Muscle mass declines by roughly 3% to 8% per decade after age 30, and faster after 60, unless you work to keep it. Muscle powers how you move, keeps you steady on your feet and is one of the body&rsquo;s biggest users of blood sugar.</p>

  <h2>Measure what matters: your &ldquo;muscle vital signs&rdquo;</h2>
  <p>The scale can&rsquo;t tell muscle from fat. A body composition scan can, and simple strength checks tell you how well your muscles work.</p>
  <ul>
    <li><strong>Grip strength.</strong> In a review of 14 studies, people in the weakest group had a 67% higher risk of death over follow-up than people in the strongest group.</li>
    <li><strong>30-second chair stand.</strong> Sit in a sturdy chair with arms crossed and count full stands in 30 seconds.</li>
    <li><strong>Single-leg balance.</strong> Stand on one foot next to a counter you can grab.</li>
    <li><strong>Walking speed.</strong> Time a comfortable 4-meter (about 13-foot) walk.</li>
  </ul>
  <p>Write your numbers down and retest every few months. Your trend matters more than any chart.</p>

  <h2>Your strength-training plan, made simple</h2>
  <p>U.S. guidelines call for muscle-strengthening work for all major muscle groups at least two days a week. A 2026 position stand from the American College of Sports Medicine, which reviewed 137 systematic reviews, adds practical detail:</p>
  <ul>
    <li>Train each major muscle group at least twice a week: push, pull, squat or hinge, and core.</li>
    <li>Do 2 to 3 challenging sets. You don&rsquo;t need to train to failure; stopping a rep or two short works.</li>
    <li>Bands, body weight and home workouts count. The biggest gain comes from going from nothing to something.</li>
  </ul>
  <p>In a 2026 study of more than 147,000 adults, most of them women, about 1.5 to 2 hours of strength training a week was linked with lower risk of death, and combining it with aerobic activity was linked with even lower risk.</p>

  <h2>Steps, cardio and short bursts</h2>
  <ul>
    <li><strong>150 minutes a week</strong> of moderate activity like brisk walking, per CDC guidelines. Your daily steps count.</li>
    <li><strong>About 7,000 steps a day.</strong> A 2025 analysis of 57 studies linked about 7,000 daily steps, compared with 2,000, with a 47% lower risk of death and fewer falls.</li>
    <li><strong>Short, brisk bursts</strong> such as taking the stairs or walking fast uphill add benefit.</li>
  </ul>
  <p>Only about 1 in 5 U.S. women meet both the aerobic and strength guidelines, so if you&rsquo;re not there yet, you&rsquo;re in good company. Start where you are.</p>

  <h2>Feed your muscle with whole-food protein</h2>
  <p>Muscle needs protein to rebuild, and many midlife women eat less than they think. Include a protein-rich food at each meal: fish, eggs, poultry, Greek yogurt, cottage cheese, beans, lentils or tofu. Needs vary with body size, activity and kidney health, so ask us for your personal target.</p>

  <h2>Getting started safely</h2>
  <p>Talk with a clinician before starting vigorous exercise if you have heart disease, chest pain, uncontrolled blood pressure, dizziness or a history of falls. At a visit we can check body composition and strength, review your labs and build a plan that fits your life.</p>
''',
    alert="<strong>Stop and call 911</strong> if you have chest pain or pressure, severe shortness of breath, fainting or a racing, irregular heartbeat during exercise.",
    related=["/menopause-appetite-food-noise/", "/menopause-weight-gain-heart-health/", "/brain-health-after-40/"],
    faq=[
        ("Does metabolism slow down in your 40s?", "Not as much as most people think. Adjusted for body size, daily energy use stays fairly steady from about 20 to 60. Losing muscle is a bigger factor, and strength training helps you keep it."),
        ("How often should women over 40 strength train?", "At least two days a week, working all major muscle groups, according to U.S. guidelines. Two to three challenging sets per exercise is a good start."),
        ("Do I need a gym?", "No. Resistance bands, dumbbells and body-weight exercises like squats, push-ups against a counter and step-ups all count."),
        ("How much protein do I need?", "It depends on your size, activity and kidney health. A practical start is a protein-rich food at every meal. Ask us for a personal target."),
        ("Can you check my body composition?", "Yes. We can review body composition, strength checks and labs at an office visit and build a plan with you."),
    ],
    sources="Pontzer et al., <em>Science</em> 2021; Volpi et al., <em>Curr Opin Clin Nutr Metab Care</em> 2004; Cooper et al., <em>BMJ</em> 2010; American College of Sports Medicine 2026 resistance training position stand; Zhang et al., <em>Br J Sports Med</em> 2026 (via Harvard Health Publishing); Ding et al., <em>Lancet Public Health</em> 2025; CDC Physical Activity Guidelines for Adults; CDC NCHS Data Brief 443 (2022).",
    about=["Sarcopenia", "Menopause"],
    seo_title="Strength Training for Women Over 40: Muscle, Metabolism & Protein | Serene Med Spa",
    seo_desc="Metabolism stays fairly steady from 20 to 60, but muscle quietly declines. Simple strength checks, a realistic exercise plan and protein tips for women 40+.",
)

# ---------------------------------------------------------------------------------------------------------------- brain longevity (Retzler)
ARTICLES["/brain-health-after-40/"] = dict(
    h1="Brain health after 40: estrogen, exercise and eating",
    hero="Nearly two in three Americans with Alzheimer&rsquo;s are women. Here&rsquo;s what research says about protecting your memory for the long run, starting in midlife.",
    crumb="Brain health after 40", quiz=True,
    lede="Brain fog in perimenopause is common and usually temporary. Long-term brain health is a different question, and midlife is when the habits that shape it matter most.",
    body='''
  <h2>Why women should think about brain health now</h2>
  <p>According to the Alzheimer&rsquo;s Association, nearly two-thirds of Americans with Alzheimer&rsquo;s disease are women, and a woman&rsquo;s lifetime risk at age 65 is about 1 in 5. Living longer explains much of the difference.</p>
  <p>The hopeful part: a 2024 <em>Lancet</em> Commission identified 14 risk factors that can be changed, including high blood pressure, high LDL cholesterol, diabetes, inactivity, hearing loss, smoking and depression, and estimated that nearly half of dementia cases could potentially be prevented or delayed.</p>
  <p>Short-term brain fog is covered in <a href="/menopause-mood-sleep-brain-fog/">mood, sleep &amp; brain fog</a>.</p>

  <h2>Estrogen and your brain: what research does and doesn&rsquo;t show</h2>
  <p>Estrogen acts throughout the brain, on memory centers, blood flow and how brain cells use energy. Brain imaging studies show changes in brain structure and energy use around menopause, with partial recovery afterward.</p>
  <p>Does hormone therapy protect memory? Clinical trials say it isn&rsquo;t a memory booster. In the KEEPS trial, women who started hormone therapy within a few years of menopause showed no change in thinking skills, better or worse, compared with placebo. Hormone therapy isn&rsquo;t recommended to prevent dementia.</p>
  <p>Treating hot flashes and night sweats may still help you feel sharper, because protecting sleep matters for the brain. Hormone therapy is a personal decision made with a clinician, based on your symptoms, age, time since menopause and health history.</p>

  <h2>Strength training: two sessions a week for your brain, too</h2>
  <p>Strength training builds more than muscle. A review of 33 trials found it meaningfully reduced symptoms of depression, and studies link it to better memory and focus. Aim for at least two days a week. See <a href="/strength-training-women-over-40/">strength after 40</a>.</p>

  <h2>Get your heart rate up, and make it fun</h2>
  <ul>
    <li>Aim for 150 minutes a week of moderate activity, or 75 minutes of vigorous activity.</li>
    <li>Movement that makes you think, like dance, tennis, pickleball or learning a new routine, adds a mental challenge.</li>
    <li>Yoga and tai chi help with stress and balance.</li>
  </ul>

  <h2>Eating for your brain: the MIND pattern</h2>
  <p>The MIND pattern emphasizes leafy greens, other vegetables, berries, beans, nuts, whole grains, fish and olive oil, and limits pastries and sweets, fried food, red meat, butter and cheese.</p>
  <p>To be honest about the evidence: in a 2023 trial of 604 older adults, thinking skills improved in both the MIND group and a comparison diet group, with no significant difference between them. The larger Finnish FINGER trial, which combined healthy eating, exercise, brain training and heart-risk care for two years, slowed cognitive decline in older adults at risk. The lesson: the whole package matters more than any single food.</p>

  <h2>When you eat matters too</h2>
  <p>Late-night eating can disrupt sleep and next-day blood sugar. Finishing your last meal about three hours before bed is a simple habit to try.</p>

  <h2>A sample brain-healthy week</h2>
  <ul><li><strong>3 days</strong> of brisk walking, cycling or a class you enjoy</li><li><strong>2 days</strong> of strength training</li><li><strong>1 day</strong> of yoga or tai chi</li><li><strong>1 day</strong> of active rest</li><li><strong>Every day:</strong> MIND-style meals, good sleep and time with people you like</li></ul>
  <p>Know your heart numbers too, since what&rsquo;s good for your heart is good for your brain. See <a href="/menopause-weight-gain-heart-health/">midlife weight gain &amp; heart health</a>.</p>

  <h2>When to talk with a clinician</h2>
  <p>Tell us if memory changes are getting steadily worse, are affecting work or daily tasks, or if family members are worried. Checking hearing, mood, sleep, medicines, thyroid and vitamin B12 is a good start, and we can refer you to a memory specialist when needed.</p>
''',
    alert="<strong>Call 911 for</strong> sudden confusion, trouble speaking, a drooping face, weakness or numbness on one side, or a sudden severe headache. These can be signs of a stroke.",
    related=["/menopause-mood-sleep-brain-fog/", "/strength-training-women-over-40/", "/menopause-weight-gain-heart-health/"],
    faq=[
        ("Does menopause cause dementia?", "No. Brain fog during perimenopause is common and usually improves. Dementia risk is shaped by many factors, and many of them, like blood pressure, activity and hearing, can be changed."),
        ("Will hormone therapy protect my memory?", "Clinical trials haven&rsquo;t shown that hormone therapy improves memory, and it isn&rsquo;t recommended to prevent dementia. It can treat hot flashes and night sweats, which may help sleep."),
        ("What is the MIND diet?", "An eating pattern that emphasizes leafy greens, berries, beans, nuts, whole grains, fish and olive oil, and limits sweets, fried food, red meat, butter and cheese."),
        ("What exercise is good for the brain?", "A mix: about 150 minutes a week of moderate aerobic activity, strength training at least twice a week, and movement that challenges coordination, like dance or tennis."),
        ("When should I worry about my memory?", "If changes are getting steadily worse, interfere with daily life, or family members are concerned. Book a visit so we can look for treatable causes."),
    ],
    sources="Alzheimer&rsquo;s Association, Women and Alzheimer&rsquo;s; Livingston et al., 2024 <em>Lancet</em> Commission on dementia (via Alzheimer Europe); Mosconi et al., <em>Scientific Reports</em> 2021; Gleason et al., <em>PLoS Medicine</em> 2015 (KEEPS-Cog); Gordon et al., <em>JAMA Psychiatry</em> 2018; Barnes et al., <em>NEJM</em> 2023 (MIND trial); Ngandu et al., <em>Lancet</em> 2015 (FINGER); CDC Physical Activity Guidelines for Adults.",
    about=["Dementia", "Menopause"],
    seo_title="Brain Health After 40: Estrogen, Exercise & the MIND Diet | Serene Med Spa",
    seo_desc="Nearly 2 in 3 Americans with Alzheimer's are women. What research says about estrogen, exercise and the MIND diet for long-term brain health in midlife.",
)

# ---------------------------------------------------------------------------------------------------------------- genetics (Feingold)
ARTICLES["/genetic-testing-women/"] = dict(
    h1="Genetic testing for women: what your DNA can and can&rsquo;t tell you",
    hero="Some inherited risks really do change your care in midlife. Others are marketing. Here&rsquo;s how to tell the difference.",
    crumb="Genetic testing", quiz=False,
    lede="At-home DNA kits and &ldquo;personalized&rdquo; gene panels promise a custom plan for your hormones, diet and supplements. The genetics that matter most for women in midlife are more specific, and they usually start with a conversation about your family.",
    body='''
  <h2>Your family history is still your most useful &ldquo;genetic test&rdquo;</h2>
  <p>Before any kit, ask your relatives:</p>
  <ul><li>Who had cancer, which kind, and at what age? Breast, ovarian, uterine, colon and pancreatic cancers matter most here.</li><li>Who had a heart attack or stroke at a young age?</li><li>Who had a blood clot in a leg or lung?</li></ul>
  <p>Write the answers down and bring them to your visit. They guide which tests, if any, make sense.</p>

  <h2>Hereditary cancer genes: BRCA and Lynch syndrome</h2>
  <ul>
    <li><strong>BRCA1 and BRCA2.</strong> According to the National Cancer Institute, more than 60% of women with a harmful BRCA1 or BRCA2 change will develop breast cancer in their lifetime, compared with about 13% of women overall. Ovarian cancer risk rises too.</li>
    <li><strong>Lynch syndrome</strong> raises the risk of colon, uterine and other cancers. About 1 in 279 people in the U.S. carry a Lynch-related gene change.</li>
  </ul>
  <p>The U.S. Preventive Services Task Force recommends that women with a personal or family history, or ancestry linked to BRCA changes, have a brief risk assessment and, if it&rsquo;s positive, genetic counseling and possibly testing. Routine BRCA testing isn&rsquo;t recommended for women without those risk features.</p>

  <h2>Heart risk written in your genes</h2>
  <ul>
    <li><strong>Lipoprotein(a), or Lp(a).</strong> About 1 in 5 people have high Lp(a). It&rsquo;s mostly inherited, diet and exercise don&rsquo;t lower it, and it isn&rsquo;t part of a standard cholesterol panel. The American Heart Association recommends that every adult be tested at least once.</li>
    <li><strong>Familial hypercholesterolemia</strong> affects about 1 in 311 people, according to the CDC. It causes very high LDL cholesterol from a young age, and without treatment about 30% of women with it have a heart attack by 60.</li>
  </ul>
  <p>For the rest of your heart numbers, see <a href="/menopause-weight-gain-heart-health/">midlife weight gain &amp; heart health</a>.</p>

  <h2>Clotting risk and menopause hormone therapy</h2>
  <p>Factor V Leiden is the most common inherited clotting tendency: about 3% to 8% of people of European ancestry carry one copy. Estrogen, whether for birth control or menopause symptoms, raises clot risk further.</p>
  <p>That&rsquo;s why we ask about any personal or family history of blood clots before hormone therapy. A history of clots doesn&rsquo;t automatically rule treatment out. The type of hormone therapy, the dose and whether it goes through the skin or by mouth all affect clot risk, so the plan can be tailored.</p>

  <h2>What at-home DNA kits and &ldquo;nutrigenomic&rdquo; panels can&rsquo;t tell you</h2>
  <ul>
    <li><strong>They can miss what matters.</strong> The National Cancer Institute notes that some consumer tests don&rsquo;t check every harmful BRCA change, so a &ldquo;clear&rdquo; result isn&rsquo;t the whole story.</li>
    <li><strong>Raw data can be wrong.</strong> In one study, 40% of gene changes reported in consumer raw data were false alarms when retested in a clinical lab.</li>
    <li><strong>Common variants are overinterpreted.</strong> MTHFR is a good example. The CDC says people with common MTHFR variants can process all types of folate, including folic acid, so it isn&rsquo;t a reason to avoid folic acid.</li>
    <li><strong>Gene-matched diet and product plans</strong> aren&rsquo;t supported by major medical guidelines.</li>
  </ul>
  <p>Any result that could change your care should be confirmed in a clinical lab and reviewed with a clinician or genetic counselor.</p>

  <h2>Genes load the dice. Lifestyle still matters</h2>
  <p>Your genes aren&rsquo;t your destiny. Strength training, vegetables and fiber, enough protein, less alcohol, good sleep and not smoking help across almost every genetic background. See <a href="/strength-training-women-over-40/">strength after 40</a>.</p>

  <h2>How we approach genetics at Serene</h2>
  <p>We review your personal and family history, order evidence-based tests such as Lp(a) when appropriate, refer you to certified genetic counselors when your history calls for it, and coordinate with your OB-GYN or primary care clinician.</p>
''',
    alert="",
    related=["/menopause-weight-gain-heart-health/", "/hormone-testing-menopause/", "/perimenopause/"],
    faq=[
        ("Should I get genetic testing for breast cancer?", "If you have a personal or family history of breast, ovarian, or related cancers, or ancestry linked to BRCA changes, start with a risk assessment and genetic counseling. Routine testing isn&rsquo;t recommended for women without risk features."),
        ("What is Lp(a), and should I be tested?", "Lp(a) is an inherited type of cholesterol particle linked to heart disease. The American Heart Association recommends every adult be tested at least once."),
        ("Can I take hormone therapy if I have a clotting gene?", "Possibly. A history of clots or an inherited clotting tendency changes which options are safest, so it needs an individualized discussion."),
        ("Are at-home DNA kits accurate?", "They can miss important gene changes and raw data can contain false alarms. Any result that could change your care should be confirmed in a clinical lab."),
        ("Should I avoid folic acid if I have an MTHFR variant?", "No. The CDC says people with common MTHFR variants can process folic acid normally."),
    ],
    sources="National Cancer Institute, BRCA gene changes fact sheet; U.S. Preventive Services Task Force, BRCA-related cancer risk assessment (2019); MedlinePlus Genetics, Lynch syndrome and Factor V Leiden thrombophilia; CDC, familial hypercholesterolemia and MTHFR gene variants; American Heart Association, Lipoprotein(a); Tandy-Connor et al., <em>Genetics in Medicine</em> 2018; The Menopause Society 2022 hormone therapy position statement.",
    about=["Hereditary breast and ovarian cancer syndrome", "Familial hypercholesterolemia"],
    seo_title="Genetic Testing for Women: BRCA, Lp(a), Clotting Risk & DNA Kits | Serene Med Spa",
    seo_desc="Which genetic tests matter in midlife? Family history, BRCA, Lynch, Lp(a) and clotting risk, plus what at-home DNA kits can't tell you.",
)

# ---------------------------------------------------------------------------------------------------------------- endometriosis (Brighten)
ARTICLES["/endometriosis-symptoms/"] = dict(
    h1="Endometriosis: more than a bad period",
    hero="Bloating, bowel or bladder pain around your period, pain with sex, exhaustion? Endometriosis affects about 1 in 10 women of reproductive age, and it often takes years to be recognized.",
    crumb="Endometriosis", quiz=False,
    lede="Many women with endometriosis are told for years that their pain is normal, that it&rsquo;s IBS, or, in their 40s, that it&rsquo;s just perimenopause. Knowing the signs can shorten that wait.",
    body='''
  <h2>What is endometriosis?</h2>
  <p>Endometriosis is a long-term condition in which tissue similar to the lining of the uterus grows outside the uterus, causing inflammation and pain. The World Health Organization estimates it affects about 10% of women and girls of reproductive age worldwide, roughly 190 million people. There is no cure yet, but treatment can control symptoms.</p>

  <h2>Symptoms that go beyond painful periods</h2>
  <ul>
    <li>Period pain that disrupts work, school or daily life</li>
    <li>Pelvic pain between periods</li>
    <li>Deep pain during or after sex</li>
    <li>Painful bowel movements, or bloating, constipation or diarrhea that follows your cycle</li>
    <li>Painful urination or bladder symptoms around your period</li>
    <li>Low back or hip pain, and fatigue</li>
    <li>Trouble getting pregnant</li>
  </ul>

  <h2>Why diagnosis often takes years</h2>
  <p>The WHO reports that the average time to diagnosis is 4 to 12 years. Symptoms often get labeled as IBS, a bladder problem or &ldquo;normal&rdquo; periods. Women with endometriosis are about three times as likely to also have an IBS diagnosis, and one doesn&rsquo;t rule out the other.</p>
  <p>A normal pelvic exam or routine ultrasound doesn&rsquo;t rule endometriosis out either. Guidelines say a normal result shouldn&rsquo;t end the conversation if symptoms continue.</p>

  <h2>Endometriosis in your late 30s and 40s</h2>
  <p>Perimenopause can blur the picture. Heavier, less predictable periods, poor sleep and mood changes can come from shifting hormones, while pain that follows your cycle, painful bowel movements and deep pain with sex point more toward endometriosis. Both can be true at once. See our <a href="/perimenopause/">perimenopause guide</a>.</p>
  <p>Endometriosis can also change the menopause timeline. In a 2025 analysis of nearly 280,000 women, those with endometriosis reached natural menopause a few months earlier on average and were much more likely to have surgical menopause.</p>

  <h2>How endometriosis is diagnosed today</h2>
  <p>Surgery is no longer always the first step. The European Society of Human Reproduction and Embryology (ESHRE) 2022 guideline recommends ultrasound or MRI as part of the workup, and says treatment can be started based on symptoms and imaging when appropriate. Specialized imaging read by an experienced team is more useful than a routine scan. Diagnosis and treatment decisions belong with a gynecologist or endometriosis specialist.</p>

  <h2>When to see a gynecologist or endometriosis specialist</h2>
  <ul>
    <li>Pain that&rsquo;s severe, keeps coming back or doesn&rsquo;t improve with first treatments</li>
    <li>Bowel or bladder symptoms that follow your cycle</li>
    <li>A cyst on an ovary, or a pelvic mass on exam</li>
    <li>Trouble getting pregnant</li>
    <li>Symptoms that return after surgery</li>
  </ul>

  <h2>Track your whole cycle, not just bleeding</h2>
  <p>For 2 to 3 cycles, note each day: pain from 0 to 10, bowel and bladder symptoms, pain with sex, energy, sleep, mood, bleeding and any pain medicine you used. Mark which days fall before, during and after your period. Patterns help your care team see what&rsquo;s going on.</p>

  <h2>How a physician-led team can support you</h2>
  <p>We don&rsquo;t perform surgery or diagnose endometriosis surgically. We can help you track symptoms, coordinate referrals and records with a gynecologist or endometriosis specialist, support pain, sleep and quality of life, check heart and bone health, and plan midlife hormone care that takes endometriosis into account. Exams happen in person; some follow-up visits can be done by telehealth.</p>
''',
    alert="<strong>Go to the ER or call 911 for</strong> sudden severe pelvic or abdominal pain (especially with vomiting), pelvic pain with fever, very heavy bleeding (soaking a pad or tampon every hour for 2 hours or more), fainting, pelvic pain or bleeding when you could be pregnant, or being unable to pass urine, stool or gas.",
    related=["/perimenopause/", "/hormone-testing-menopause/", "/menopause-mood-sleep-brain-fog/"],
    faq=[
        ("What are the first signs of endometriosis?", "Period pain that disrupts daily life is common, but endometriosis can also cause pelvic pain between periods, deep pain with sex, painful bowel movements or urination around your period, bloating and fatigue."),
        ("Can endometriosis be mistaken for IBS?", "Yes. The symptoms overlap, and women with endometriosis are about three times as likely to have an IBS diagnosis. An IBS diagnosis doesn&rsquo;t rule endometriosis out."),
        ("Does a normal ultrasound mean I don&rsquo;t have endometriosis?", "No. Routine imaging can miss it. Specialized ultrasound or MRI read by experienced teams is more helpful, and guidelines say a normal result shouldn&rsquo;t end the evaluation if symptoms continue."),
        ("Does endometriosis go away at menopause?", "Symptoms often improve, but not always. If you have endometriosis and are considering menopause hormone therapy, the type of therapy matters, so plan it with a clinician who knows your history."),
        ("Do you treat endometriosis?", "We help with symptom tracking, referrals, pain and quality-of-life support and midlife hormone care, alongside a gynecologist or endometriosis specialist who makes the diagnosis and directs treatment."),
    ],
    sources="World Health Organization, Endometriosis fact sheet (2025); ESHRE guideline: endometriosis, <em>Human Reproduction Open</em> 2022; NICE guideline NG73, Endometriosis: diagnosis and management; Nabi et al., <em>Frontiers in Medicine</em> 2022; Chung et al., <em>Human Reproduction</em> 2025; EMAS clinical guide, <em>Maturitas</em> 2025.",
    about=["Endometriosis"],
    seo_title="Endometriosis Symptoms: More Than a Bad Period | Serene Med Spa",
    seo_desc="Painful periods, bloating, bowel or bladder pain, fatigue? Learn the signs of endometriosis, why diagnosis takes years, and when to see a specialist.",
)


def _article(slug):
    a = ARTICLES[slug]
    faq_html = "".join(f'<div class="card reveal"><h3>{q}</h3><p style="font-size:.97rem">{ans}</p></div>' for q, ans in a["faq"])
    alert = ALERT.format(a["alert"]) if a["alert"] else ""
    body = page_hero(a["h1"], a["hero"], [("/", "Home"), ("/womens-health/", "Women&rsquo;s Health"), (None, a["crumb"])], "Women&rsquo;s health library") + f'''
<section><div class="wrap prose">
  {BYLINE}
  <p class="lede">{a["lede"]}</p>
  {_cta(a["quiz"])}
{a["body"]}
  <p>Every plan is individualized, and treatment is recommended only when it&rsquo;s right for you after your consultation.</p>
  {_related(a["related"])}
  {_see_us()}
  {alert}
  <p style="font-size:.85rem;color:var(--muted)">Sources: {a["sources"]} This page is general education, not medical advice.</p>
</div></section>
<section class="tint-sand"><div class="wrap"><div class="section-head"><span class="eyebrow">Common questions</span><h2>Frequently asked questions</h2></div><div class="grid g2">{faq_html}</div></div></section>
{book_band()}'''
    ld = json.dumps([
        {"@context": "https://schema.org", "@type": "MedicalWebPage", "url": SITE_URL + slug, "name": _h.unescape(a["h1"]),
         "about": [{"@type": "MedicalCondition", "name": n} for n in a["about"]],
         "audience": {"@type": "MedicalAudience", "audienceType": "Patient"}, "lastReviewed": "2026-10-09",
         "author": {"@type": "Person", "name": "Shweta Arora, MD", "url": SITE_URL + "/our-providers/shweta-arora/"},
         "reviewedBy": {"@type": "Person", "name": "Robin Arora, MD", "url": SITE_URL + "/our-providers/robin-arora-md/"},
         "isPartOf": {"@type": "WebSite", "@id": SITE_URL + "/#website"}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": _h.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": _h.unescape(ans)}} for q, ans in a["faq"]]},
    ], ensure_ascii=False)
    return shell(slug, a["seo_title"], a["seo_desc"], body, ld=ld)


def hub():
    cards = "".join(f'<a class="card reveal" href="{s}" style="text-decoration:none;color:inherit"><h3>{t}</h3><p style="font-size:.97rem">{d}</p><span style="color:var(--teal-500);font-weight:600">Read the guide &rarr;</span></a>' for s, t, d in LIBRARY)
    body = page_hero("Women&rsquo;s Health Library", "Plain-language guides to perimenopause, menopause and midlife health from our physician-led team, led by Shweta Arora, MD.",
                     [("/", "Home"), (None, "Women&rsquo;s Health")], "Education") + f'''
<section><div class="wrap">
  {BYLINE}
  <div class="actions" style="margin:6px 0 26px"><a class="btn" href="{QUIZ}" target="_blank" rel="noopener">Take the 3-minute symptom check</a><a class="btn btn-outline" href="#book">Book a consult</a></div>
  <div class="grid g2">{cards}</div>
  <p style="font-size:.85rem;color:var(--muted);margin-top:26px">These guides are general education, not medical advice. In person in Hudson, OH and Barboursville, WV; telehealth in Ohio, West Virginia, Kentucky and Florida.</p>
</div></section>
{book_band()}'''
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE_URL + "/womens-health/", "name": "Women's Health Library",
                     "hasPart": [{"@type": "MedicalWebPage", "url": SITE_URL + s, "name": _h.unescape(t)} for s, t, _ in LIBRARY],
                     "isPartOf": {"@type": "WebSite", "@id": SITE_URL + "/#website"}}, ensure_ascii=False)
    return shell("/womens-health/", "Women's Health Library: Perimenopause, Menopause & Midlife Health | Serene Med Spa",
                 "Physician-written guides on perimenopause, thyroid, hormone testing, appetite, strength, brain health, genetics and endometriosis. By Shweta Arora, MD.", body, ld=ld)


def pages():
    out = {s: _article(s) for s in ARTICLES}
    out["/womens-health/"] = hub()
    return out
