# Women's Health Library, batch 2 (Oct 9 2026): 7 more articles from the A4M Women's Health Summit decks, plus verified
# additions folded into batch-1 articles. Importing this module mutates womens_health_pages.ARTICLES / LIBRARY, so it must be
# imported before WH.pages() runs (pages_custom imports it at module level). Same public-copy rules as batch 1.
import womens_health_pages as WH

NEW_LIB = [
    ("/fertility-after-35/", "Fertility after 35: what age, AMH tests and egg freezing really tell you", "When to get help, what tests can and can&rsquo;t predict, and how to prepare."),
    ("/beyond-hormone-therapy-midlife/", "On hormone therapy but still not yourself?", "The missing pieces: sleep, movement, food, alcohol and connection."),
    ("/everyday-chemicals-menopause-bone-health/", "Everyday chemicals, menopause &amp; bone health", "What the research shows, and calm, practical steps worth taking."),
    ("/unusual-perimenopause-symptoms/", "Unexpected perimenopause symptoms", "Frozen shoulder, itchy skin, ringing ears and more, and when to get checked."),
    ("/gut-health-midlife/", "Gut health in midlife", "How your gut changes with menopause, and the food habits that help."),
    ("/breast-health-perimenopause/", "Breast health in perimenopause", "Mammograms, dense-breast letters and the real numbers on hormone therapy."),
    ("/sexual-health-menopause/", "Low libido, dryness &amp; painful sex after 40", "What&rsquo;s common, what helps and how to bring it up."),
]
WH.LIBRARY.extend(NEW_LIB)
WH._TITLES.update({s: t for s, t, _ in NEW_LIB})
A = WH.ARTICLES

# ---------------------------------------------------------------------------------------------------------------- fertility (Shippy)
A["/fertility-after-35/"] = dict(
    h1="Fertility after 35: what age, AMH tests and egg freezing really tell you",
    hero="Thinking about pregnancy now or later? Here&rsquo;s what the evidence says about age, ovarian reserve tests, egg freezing and when to ask for help.",
    crumb="Fertility after 35", quiz=False,
    lede="Fertility questions often come with a lot of noise: home tests, social media timelines and well-meaning advice. The most useful facts are simpler, and they apply to both partners.",
    body='''
  <h2>Age is the biggest factor</h2>
  <p>According to the American Society for Reproductive Medicine (ASRM), a healthy 30-year-old has about a 20% chance of getting pregnant in any given month, while a 40-year-old has less than a 5% chance. The decline speeds up in the late 30s, mainly because egg quantity and quality fall with age.</p>
  <p>Infertility is common. The World Health Organization estimates that about 1 in 6 adults worldwide experience it at some point.</p>

  <h2>When to ask for an evaluation</h2>
  <p>ASRM recommends a fertility evaluation if you haven&rsquo;t become pregnant after:</p>
  <ul><li><strong>12 months</strong> of trying if you&rsquo;re under 35</li><li><strong>6 months</strong> of trying if you&rsquo;re 35 or older</li><li><strong>Sooner</strong> if you&rsquo;re over 40, have irregular or absent periods, known endometriosis, prior pelvic surgery, or a partner with known fertility concerns</li></ul>
  <p>Both partners should be evaluated at the same time. A semen analysis is part of a standard first workup, because male factors contribute to many couples&rsquo; infertility.</p>

  <h2>What an AMH test can and can&rsquo;t tell you</h2>
  <p>Anti-M&uuml;llerian hormone (AMH) is a blood test that reflects how many eggs remain in the ovaries. It&rsquo;s useful for planning fertility treatment. But ASRM advises that AMH should not be used as a test of whether you can get pregnant naturally, or on its own to push anyone toward egg freezing. Women with a low AMH can still conceive, and a normal AMH doesn&rsquo;t guarantee pregnancy. Age remains a stronger predictor.</p>

  <h2>Egg freezing: realistic expectations</h2>
  <ul>
    <li>Egg freezing works better at younger ages. ASRM notes that a woman around 38 may need roughly 25 to 30 eggs for a reasonable chance of one child.</li>
    <li>It doesn&rsquo;t guarantee a future pregnancy, and there isn&rsquo;t yet enough data to give precise live-birth odds for every age.</li>
    <li>Talking it through with a reproductive endocrinologist before deciding helps you weigh cost, timing and odds.</li>
  </ul>

  <h2>The male partner matters too</h2>
  <p>A large 2023 analysis found that average sperm concentration fell by about half between 1973 and 2018. Sperm health is also a marker of overall health. Partners should have their own checkup, including a semen analysis when trying hasn&rsquo;t worked, and a review of medicines, including testosterone, which can lower sperm production.</p>

  <h2>Getting your body ready</h2>
  <ul>
    <li><strong>Review every medicine and hormone treatment</strong> with your clinician before trying. Some weight-loss, hormone and other medicines should be stopped ahead of time.</li>
    <li><strong>Folic acid.</strong> The U.S. Preventive Services Task Force recommends folic acid for anyone who could become pregnant. Ask us which prenatal option fits you.</li>
    <li><strong>Check the basics:</strong> blood pressure, blood sugar (A1c), thyroid and vaccinations.</li>
    <li><strong>Everyday habits:</strong> not smoking, limiting alcohol, regular activity, sleep and a nutritious eating pattern help both partners.</li>
  </ul>
  <p>Our practice doesn&rsquo;t provide fertility treatment. We can help with preconception health, review medicines and refer you to a fertility specialist at the right time.</p>
''',
    alert="<strong>Seek urgent care for</strong> one-sided pelvic pain, shoulder-tip pain, dizziness or fainting with a positive or possible pregnancy, or heavy bleeding in early pregnancy. These can be signs of an ectopic pregnancy.",
    related=["/endometriosis-symptoms/", "/hormone-testing-menopause/", "/genetic-testing-women/"],
    faq=[
        ("When should I see a fertility specialist?", "After 12 months of trying if you&rsquo;re under 35, after 6 months if you&rsquo;re 35 or older, and sooner if you&rsquo;re over 40 or have irregular periods, endometriosis or other known concerns."),
        ("Can an AMH test tell me if I can get pregnant?", "No. AMH reflects egg supply and helps plan fertility treatment, but ASRM says it shouldn&rsquo;t be used to predict natural pregnancy. Age is a stronger predictor."),
        ("Is egg freezing a guarantee?", "No. It works better at younger ages and doesn&rsquo;t guarantee a future pregnancy. A reproductive endocrinologist can help you weigh the odds and costs."),
        ("Should my partner be tested too?", "Yes. Both partners should be evaluated at the same time, and a semen analysis is part of a standard first workup."),
        ("Do you offer fertility treatment?", "No. We help with preconception health and medicine reviews, and refer you to a fertility specialist when it&rsquo;s time."),
    ],
    sources="American Society for Reproductive Medicine: Age and Fertility patient guide, evaluation of infertility (2021), AMH testing (2020) and planned oocyte cryopreservation (2021, 2024); World Health Organization, infertility prevalence (2023); AUA/ASRM male infertility guideline (2020, 2024); Levine et al., <em>Human Reproduction Update</em> 2023; U.S. Preventive Services Task Force, folic acid for prevention of neural tube defects.",
    about=["Infertility"],
    seo_title="Fertility After 35: Age, AMH Tests & Egg Freezing Explained | Serene Med Spa",
    seo_desc="What age, AMH tests and egg freezing can really tell you, when to see a fertility specialist, and how both partners can prepare for pregnancy.",
)

# ---------------------------------------------------------------------------------------------------------------- beyond HT (Sundermann)
A["/beyond-hormone-therapy-midlife/"] = dict(
    h1="On hormone therapy but still not feeling like yourself?",
    hero="Hormone therapy is the most effective treatment for hot flashes. It was never designed to build muscle, fix sleep habits or end loneliness. Here are the missing pieces.",
    crumb="Beyond hormone therapy", quiz=True,
    lede="&ldquo;My hot flashes are better. So why don&rsquo;t I feel like myself?&rdquo; It&rsquo;s one of the most common questions women ask once treatment starts working. The answer usually lies in the parts of life no prescription can reach.",
    body='''
  <h2>What hormone therapy does well, and what it can&rsquo;t do</h2>
  <p>According to The Menopause Society, hormone therapy is the most effective treatment for hot flashes, night sweats and vaginal dryness, and it helps prevent bone loss. For healthy women under 60 or within 10 years of menopause, the benefits generally outweigh the risks for these uses.</p>
  <p>It isn&rsquo;t a tool for preventing chronic disease on its own; the U.S. Preventive Services Task Force recommends against using it for that purpose. And it can&rsquo;t build fitness, change how you eat, create sleep habits or replace connection with other people.</p>

  <h2>The everyday pillars</h2>
  <ul>
    <li><strong>Movement:</strong> about 150 minutes a week of moderate activity plus strength training at least two days a week. See <a href="/strength-training-women-over-40/">strength after 40</a>.</li>
    <li><strong>Food:</strong> mostly whole foods, plenty of fiber and fewer ultra-processed foods. See <a href="/menopause-appetite-food-noise/">appetite &amp; food noise</a>.</li>
    <li><strong>Sleep:</strong> short sleep raises hunger. In an analysis of 11 studies, people who were sleep-deprived ate about 385 more calories a day. See <a href="/menopause-mood-sleep-brain-fog/">mood, sleep &amp; brain fog</a>.</li>
    <li><strong>Stress and alcohol</strong>, covered below.</li>
  </ul>

  <h2>The overlooked factor: connection</h2>
  <p>Midlife can be lonely, especially for women caring for children and aging parents at the same time. The U.S. Surgeon General&rsquo;s 2023 advisory reports that about half of U.S. adults experience loneliness, and that a lack of social connection is linked to higher risk of early death, heart disease and stroke.</p>
  <p>The flip side is encouraging: a review of 148 studies with more than 300,000 people found that people with stronger social relationships had 50% higher odds of survival over the study periods.</p>
  <p>Connection is something you can build on purpose: a standing walk with a friend, a weekly call, a class, a faith or volunteer group. Caregivers need support too.</p>

  <h2>Why knowing isn&rsquo;t the same as changing</h2>
  <p>Most of us already know what we &ldquo;should&rdquo; do. Change sticks when it&rsquo;s small and specific:</p>
  <ol>
    <li><strong>Pick one goal</strong> that&rsquo;s specific, measurable and time-bound. For example: a 30-minute brisk walk on Monday, Wednesday and Friday with a friend for the next month.</li>
    <li><strong>Rate your confidence</strong> from 1 to 10. If it&rsquo;s 6 or lower, make the goal smaller.</li>
    <li><strong>Check in</strong> after a week, adjust and keep going.</li>
  </ol>
  <p>Support between visits helps too. In an Australian trial of 351 women in the menopause transition, six phone coaching sessions on everyday habits led to larger drops in depression-symptom scores than usual care.</p>

  <h2>Alcohol as an &ldquo;off switch&rdquo;</h2>
  <p>A nightly glass of wine to wind down is a common midlife pattern. Alcohol fragments sleep, can trigger hot flashes and adds to next-day fatigue. Try noticing when and why you reach for it, and swapping in another wind-down ritual a few nights a week. If cutting back feels hard, tell us; support works better than willpower alone.</p>

  <h2>Building your plan with us</h2>
  <p>Bring a list of what&rsquo;s still bothering you, your sleep pattern, your typical week of movement and meals, and what matters most to you right now. We&rsquo;ll look at whether your treatment needs adjusting and help you choose one or two next steps that fit your life.</p>
''',
    alert="<strong>Get help right away</strong> if you have thoughts of harming yourself (call or text 988), chest pain or shortness of breath with activity, or bleeding after 12 months without a period.",
    related=["/menopause-mood-sleep-brain-fog/", "/strength-training-women-over-40/", "/menopause-appetite-food-noise/"],
    faq=[
        ("Why don&rsquo;t I feel 100% on hormone therapy?", "Hormone therapy treats hot flashes, night sweats and vaginal dryness very well, but sleep habits, fitness, eating patterns, stress and connection need their own plan."),
        ("Is hormone therapy used to prevent heart disease?", "No. It&rsquo;s prescribed for symptoms and bone protection. The U.S. Preventive Services Task Force recommends against using it only to prevent chronic disease."),
        ("Does loneliness really affect health?", "Yes. The U.S. Surgeon General reports that a lack of social connection is linked to higher risk of early death, heart disease and stroke."),
        ("How do I make habits stick?", "Pick one small, specific goal, rate your confidence from 1 to 10, and shrink the goal if your confidence is 6 or lower."),
        ("Can you adjust my treatment by telehealth?", "Yes, for most hormone and weight care in Ohio, West Virginia, Kentucky and Florida. Testosterone is evaluated and prescribed in person only."),
    ],
    sources="The Menopause Society 2022 Hormone Therapy Position Statement; U.S. Preventive Services Task Force, hormone therapy for primary prevention (2022); U.S. Surgeon General, Our Epidemic of Loneliness and Isolation (2023); Holt-Lunstad et al., <em>PLoS Medicine</em> 2010; Al Khatib et al., <em>Eur J Clin Nutr</em> 2017; Almeida et al., <em>Maturitas</em> 2016; CDC Physical Activity Guidelines for Adults.",
    about=["Menopause"],
    seo_title="On Hormone Therapy but Still Not Yourself? The Missing Pieces | Serene Med Spa",
    seo_desc="Hormone therapy eases hot flashes but can't build muscle, fix sleep habits or end loneliness. The everyday pieces that help you feel like yourself.",
)

# ---------------------------------------------------------------------------------------------------------------- chemicals & bone (Cohen)
A["/everyday-chemicals-menopause-bone-health/"] = dict(
    h1="Everyday chemicals, menopause and bone health",
    hero="Studies link some common chemicals to earlier menopause and weaker bones. Here&rsquo;s what the evidence actually shows, and a few calm, practical steps worth taking.",
    crumb="Everyday chemicals &amp; bone", quiz=False,
    lede="You don&rsquo;t need to overhaul your home or buy a &ldquo;detox&rdquo; kit. Most of what protects your bones in midlife is familiar, and a few simple swaps can lower the exposures researchers worry about most.",
    body='''
  <h2>What the research shows, and doesn&rsquo;t</h2>
  <ul>
    <li><strong>PFAS (&ldquo;forever chemicals&rdquo;).</strong> In the SWAN study of more than 1,100 midlife women, those with the highest blood PFAS levels reached natural menopause about two years earlier than those with the lowest.</li>
    <li><strong>Metals.</strong> In another SWAN analysis, higher urine levels of arsenic, cadmium, mercury and lead were linked to lower anti-M&uuml;llerian hormone, a marker of remaining egg supply.</li>
    <li>These are <strong>associations</strong> from large studies, not proof that the chemicals caused the changes. The goal is to reduce exposure where it&rsquo;s easy, not to reach zero.</li>
  </ul>
  <p>PFAS are widespread: the CDC notes that most people in the U.S. have PFAS in their blood, and the U.S. Geological Survey estimated that at least 45% of U.S. tap water has at least one type.</p>

  <h2>Why midlife matters for bone</h2>
  <p>Bone loss doesn&rsquo;t wait for your last period. In SWAN, bone density began falling about a year before the final period, and over a decade women lost roughly 10% of their spine bone density, most of it during the transition.</p>
  <p>Some metals are stored in bone. According to the CDC&rsquo;s Agency for Toxic Substances and Disease Registry, about 94% of the lead in an adult&rsquo;s body is in bones and teeth, and more of it can move back into the blood when bone turnover rises, including during menopause. Cadmium, mostly from tobacco smoke and food, stays in the body for decades, and higher levels have been linked to fracture risk in postmenopausal women.</p>
  <p>According to the Bone Health &amp; Osteoporosis Foundation, about 1 in 2 women over 50 will break a bone because of osteoporosis.</p>

  <h2>Your bones first: the proven basics</h2>
  <ul>
    <li>Strength and weight-bearing exercise. See <a href="/strength-training-women-over-40/">strength after 40</a>.</li>
    <li>Not smoking, and avoiding secondhand smoke. Smokers carry about twice as much cadmium.</li>
    <li>Limiting alcohol, preventing falls and reviewing medicines that can thin bone.</li>
    <li>A bone density (DEXA) scan at 65, or earlier if you have risk factors such as early menopause or a fracture from a minor fall.</li>
  </ul>

  <h2>Water: know your source</h2>
  <ul>
    <li>Read your water utility&rsquo;s yearly quality report, or test a private well.</li>
    <li>Find out whether your home has a lead service line.</li>
    <li>If PFAS or lead is a concern, the EPA suggests a filter certified to NSF/ANSI Standard 53 or 58, replaced on schedule.</li>
  </ul>

  <h2>Kitchen and home: a few high-yield swaps</h2>
  <ul>
    <li>Heat and store food in glass, ceramic or stainless steel rather than plastic.</li>
    <li>Choose fresh or frozen foods over canned when you can.</li>
    <li>Wet-dust, vacuum and take shoes off at the door, especially in homes built before 1978, when lead paint was still used.</li>
    <li>Choose fragrance-free products where practical, and ventilate when cleaning.</li>
  </ul>

  <h2>A word on &ldquo;detox&rdquo; products</h2>
  <p>Cleanses, sweats and supplements sold to flush out chemicals or metals don&rsquo;t have good evidence behind them. Cutting new exposure at the source is what helps. If you have a real concern, such as work or hobby exposure to metals, a blood lead test ordered by a clinician is the right next step.</p>

  <h2>When to talk with us</h2>
  <p>Early menopause, a fracture from a minor fall, fast bone loss, work or hobby exposure to metals, or a private well are all good reasons to book a visit.</p>
''',
    alert="<strong>Seek care promptly for</strong> a fracture from a minor fall, sudden severe back pain or height loss, or a positive lead test or water contamination notice.",
    related=["/strength-training-women-over-40/", "/perimenopause/", "/hormone-testing-menopause/"],
    faq=[
        ("Do PFAS cause early menopause?", "Studies have found a link, not proof. In SWAN, women with the highest PFAS levels reached menopause about two years earlier on average."),
        ("Should I buy a water filter?", "If your water report or well test shows PFAS or lead, a filter certified to NSF/ANSI 53 or 58, replaced on schedule, is a reasonable step."),
        ("Do detox products remove chemicals?", "There&rsquo;s no good evidence they do. Reducing new exposure at the source is what helps."),
        ("When should I get a bone density scan?", "At 65, or earlier if you have risk factors such as early menopause, a fracture from a minor fall or long-term use of bone-thinning medicines."),
        ("Can you test me for toxins?", "We don&rsquo;t recommend broad &ldquo;toxin&rdquo; panels. If you have a specific exposure, such as lead at work, a targeted blood test can help."),
    ],
    sources="Ding et al., <em>J Clin Endocrinol Metab</em> 2020 and 2024 (SWAN); Greendale et al., <em>J Bone Miner Res</em> 2012 (SWAN bone); CDC/ATSDR lead and cadmium; CDC/ATSDR PFAS; U.S. Geological Survey tap water study (2023); U.S. EPA, PFAS drinking water filters and lead; Bone Health &amp; Osteoporosis Foundation; NIH NIAMS, osteoporosis.",
    about=["Osteoporosis", "Menopause"],
    seo_title="Everyday Chemicals, Menopause & Bone Health: What's Worth Changing | Serene Med Spa",
    seo_desc="Studies link PFAS, lead and cadmium to earlier menopause and lower bone density. What the evidence shows and calm, practical steps for women over 40.",
)

# ---------------------------------------------------------------------------------------------------------------- unusual symptoms (Richards)
A["/unusual-perimenopause-symptoms/"] = dict(
    h1="Unexpected perimenopause symptoms",
    hero="Frozen shoulder. Itchy skin. Ringing ears. Odd smells. Some surprising symptoms may be linked to perimenopause, and some need a closer look.",
    crumb="Unexpected symptoms", quiz=True,
    lede="Hormones act on far more than the ovaries. Skin, joints, the inner ear and the brain all have hormone receptors, so the transition can show up in places nobody warned you about.",
    body='''
  <h2>Why perimenopause can show up in surprising places</h2>
  <p>In perimenopause, progesterone often falls first while estrogen swings up and down. Those swings can affect tissues throughout the body, which is why symptoms can come and go. Each symptom below can also have other causes, so it deserves a proper look rather than a shrug.</p>

  <h2>Frozen shoulder</h2>
  <p>Frozen shoulder (adhesive capsulitis) causes shoulder pain followed by stiffness that makes it hard to lift your arm. According to the American Academy of Orthopaedic Surgeons, it&rsquo;s most common in people in their 40s to 60s, affects women more often, and is much more common in people with diabetes or thyroid disease. It often starts without any injury.</p>
  <p>It moves through stages: a painful &ldquo;freezing&rdquo; phase over weeks to months, a stiff &ldquo;frozen&rdquo; phase, then a &ldquo;thawing&rdquo; phase that can take months to two years. Most people improve without surgery, and physical therapy is the usual first step. Researchers are still studying how much falling estrogen contributes.</p>

  <h2>Itchy, dry or more sensitive skin</h2>
  <p>The American Academy of Dermatology notes that skin loses about 30% of its collagen in the first five years of menopause, and holds less water, so it can become drier, thinner and more sensitive.</p>
  <ul><li>Use a mild cleanser and a fragrance-free moisturizer right after bathing.</li><li>Keep showers warm, not hot.</li><li>Wear sunscreen daily.</li></ul>
  <p>Itching all over without a rash is different. It can come from thyroid, kidney, liver or blood conditions, so it needs an exam and labs.</p>

  <h2>Ringing ears and changes in smell</h2>
  <p>Some women report new ringing in the ears (tinnitus) or smelling things that aren&rsquo;t there (phantom smells) during perimenopause. The inner ear and smell pathways have hormone receptors, but research on these symptoms is still early. Because hearing and smell changes have many possible causes, we check for those first.</p>

  <h2>Is it perimenopause or something else?</h2>
  <p>Thyroid problems, diabetes, low iron, medicine side effects and other conditions can mimic or add to these symptoms. See <a href="/perimenopause-or-thyroid/">perimenopause or thyroid?</a> and <a href="/hormone-testing-menopause/">which labs help</a>.</p>

  <h2>How we evaluate and treat</h2>
  <ol>
    <li>Keep a 4 to 8 week symptom diary: what, when, where you are in your cycle and how you slept.</li>
    <li>We take a full history, examine you and order targeted labs when they help.</li>
    <li>We treat the specific problem, such as physical therapy for frozen shoulder or skin care for dryness, and discuss whether hormone therapy fits your overall picture. See our <a href="/perimenopause/">perimenopause guide</a>.</li>
  </ol>
''',
    alert="<strong>Get same-day care for</strong> sudden hearing loss or ringing in one ear, ringing that pulses with your heartbeat, phantom smells with confusion, seizures or a severe headache, shoulder or arm pain with chest pressure or shortness of breath (call 911), or all-over itching with yellow skin or eyes.",
    related=["/perimenopause/", "/perimenopause-or-thyroid/", "/menopause-mood-sleep-brain-fog/"],
    faq=[
        ("Can perimenopause cause frozen shoulder?", "Frozen shoulder is most common in women in their 40s to 60s, and researchers are studying a possible hormone link. Diabetes and thyroid disease are well-established risk factors, so we check for those too."),
        ("Why is my skin so itchy in my 40s?", "Skin loses collagen and moisture around menopause, which can cause dryness and itching. Itching all over without a rash needs an exam, because it can have other causes."),
        ("Can hormones cause ringing in the ears?", "Some women report it during perimenopause, but research is limited. Ringing in one ear, sudden hearing loss or pulsing sounds need prompt evaluation."),
        ("Will hormone therapy fix these symptoms?", "It may help some symptoms, but each one is treated on its own merits. We&rsquo;ll discuss whether hormone therapy fits your overall health and goals."),
        ("Can you see me by telehealth?", "Yes, in Ohio, West Virginia, Kentucky and Florida. Some symptoms, like shoulder or skin changes, may need an in-person exam."),
    ],
    sources="American Academy of Orthopaedic Surgeons, OrthoInfo: Frozen Shoulder; American Academy of Dermatology, skin care during menopause; The Menopause Society 2022 Hormone Therapy Position Statement.",
    about=["Perimenopause", "Adhesive capsulitis"],
    seo_title="Unexpected Perimenopause Symptoms: Frozen Shoulder, Itchy Skin & More | Serene Med Spa",
    seo_desc="Frozen shoulder, itchy skin, ringing ears, odd smells: which surprise symptoms may be linked to perimenopause and when to get checked.",
)

# ---------------------------------------------------------------------------------------------------------------- gut health (Class gut + Minich food; independent sources)
A["/gut-health-midlife/"] = dict(
    h1="Gut health in midlife",
    hero="Your gut bacteria change along with your hormones. Here&rsquo;s what research shows, which food habits help, and which popular tests to skip.",
    crumb="Gut health", quiz=False,
    lede="Bloating, new food reactions and changes in digestion are common complaints in midlife. Some of that is the gut changing with menopause, and food is one of the most powerful tools you have.",
    body='''
  <h2>What changes in the gut after menopause</h2>
  <p>In a study of more than 2,300 adults, women after menopause tended to have less varied gut bacteria than women before menopause, and their gut bacteria looked more like men&rsquo;s. Their gut bacteria were also less active at handling estrogen. Researchers are still working out what these shifts mean for heart, bone and metabolic health.</p>

  <h2>The &ldquo;estrobolome,&rdquo; in plain language</h2>
  <p>After the liver packages estrogen for removal, some of it travels to the gut, where certain bacteria can &ldquo;unpackage&rdquo; it so it&rsquo;s reabsorbed. Scientists call this group of bacteria the estrobolome. It&rsquo;s one more reason a fiber-rich, varied diet matters in midlife. No home test or product has been shown to &ldquo;balance&rdquo; it.</p>

  <h2>Food habits that help</h2>
  <ul>
    <li><strong>Variety.</strong> In a large community study, people who ate about 30 or more different plants a week had more varied gut bacteria than people who ate 10 or fewer. Plants include vegetables, fruit, beans, whole grains, nuts, seeds and herbs.</li>
    <li><strong>Fermented foods.</strong> In a small randomized study, adults who added several daily servings of fermented foods, such as yogurt, kefir, sauerkraut and kimchi, saw their gut-bacteria diversity rise and some markers of inflammation fall.</li>
    <li><strong>Fiber.</strong> Most Americans don&rsquo;t get enough. Add it gradually, with water, to limit bloating.</li>
    <li><strong>Soy foods and ground flax</strong> are nutritious additions. The Menopause Society doesn&rsquo;t recommend soy products or diet changes as a treatment for hot flashes, though, so if hot flashes are affecting your life, ask about options that work.</li>
  </ul>

  <h2>Tests to skip</h2>
  <ul>
    <li><strong>IgG &ldquo;food sensitivity&rdquo; panels.</strong> The American Academy of Allergy, Asthma &amp; Immunology says these tests have never been proven to do what they claim; IgG usually just shows you&rsquo;ve eaten a food. Cutting out foods based on them can make your diet less varied.</li>
    <li><strong>&ldquo;Leaky gut&rdquo; tests.</strong> A 2024 review by gastroenterologists notes that leaky gut isn&rsquo;t an accepted medical diagnosis and there&rsquo;s no validated test for it.</li>
  </ul>
  <p>If you think a food bothers you, talk with us. A guided, short-term approach with a dietitian works better than a long list of foods to avoid.</p>

  <h2>When digestion needs a closer look</h2>
  <p>New or persistent bloating, a change in bowel habits, or pelvic and bowel symptoms that follow your cycle deserve an evaluation. In midlife, persistent bloating can also be a symptom of ovarian or bowel conditions. See <a href="/endometriosis-symptoms/">endometriosis</a> and make sure your colon cancer screening is up to date.</p>
''',
    alert="<strong>See a clinician promptly for</strong> blood in your stool, black stools, unintended weight loss, trouble swallowing, persistent vomiting, or bloating that doesn&rsquo;t go away and comes with pelvic pain or feeling full quickly.",
    related=["/menopause-appetite-food-noise/", "/menopause-weight-gain-heart-health/", "/endometriosis-symptoms/"],
    faq=[
        ("Does menopause change your gut?", "Research suggests it can. After menopause, gut bacteria tend to be less varied and look more like men&rsquo;s, though what that means for health is still being studied."),
        ("What should I eat for gut health?", "A wide variety of plants, plenty of fiber and some fermented foods like yogurt, kefir or sauerkraut."),
        ("Are food sensitivity tests accurate?", "IgG food sensitivity panels haven&rsquo;t been proven to work and can lead to unnecessary food restrictions."),
        ("Is leaky gut real?", "It isn&rsquo;t an accepted medical diagnosis, and there&rsquo;s no validated test for it. Persistent gut symptoms deserve a proper evaluation instead."),
        ("When is bloating a concern?", "When it&rsquo;s new, persistent or comes with pelvic pain, feeling full quickly, weight loss or bleeding. Book a visit."),
    ],
    sources="Peters et al., <em>mSystems</em> 2022; McDonald et al., <em>mSystems</em> 2018 (American Gut Project); Wastyk et al., <em>Cell</em> 2021; American Academy of Allergy, Asthma &amp; Immunology, IgG food test; Lacy et al., 2024 review on intestinal permeability; The Menopause Society 2023 Nonhormone Therapy Position Statement.",
    about=["Menopause"],
    seo_title="Gut Health in Midlife: Menopause, the Microbiome & What to Eat | Serene Med Spa",
    seo_desc="How gut bacteria change with menopause, the food habits that help, and why IgG food-sensitivity and leaky-gut tests aren't worth your money.",
)

# ---------------------------------------------------------------------------------------------------------------- breast health (Simmons; guideline-built)
A["/breast-health-perimenopause/"] = dict(
    h1="Breast health in perimenopause",
    hero="When to start mammograms, what a dense-breast letter means, and what hormone therapy really does to breast cancer risk, in plain numbers.",
    crumb="Breast health", quiz=False,
    lede="Breasts change in your 40s, and so do the questions: Is this lump normal? Do I need a mammogram every year? Is hormone therapy safe for my breasts? Here&rsquo;s what current guidelines say.",
    body='''
  <h2>Why breasts change in your 40s</h2>
  <p>As hormones swing in perimenopause, many women notice tender, full or lumpy breasts, especially before a period. That&rsquo;s often normal. A new lump or a change that doesn&rsquo;t go away after a full cycle still needs an exam.</p>

  <h2>When to start mammograms, and how often</h2>
  <ul>
    <li>The U.S. Preventive Services Task Force (2024) recommends a screening mammogram every two years from age 40 to 74.</li>
    <li>The American Cancer Society says women can choose yearly mammograms at 40 to 44, should have them yearly at 45 to 54, and can switch to every two years at 55 and older.</li>
    <li>The American College of Radiology recommends yearly mammograms from 40, and a breast cancer risk assessment by age 25.</li>
  </ul>
  <p>The groups differ on how often, but all agree on starting by 40. Choose a schedule with your clinician based on your risk and preferences.</p>

  <h2>&ldquo;Your breast tissue is dense&rdquo;: what the letter means</h2>
  <p>Since September 2024, the FDA requires every mammogram report and patient letter to say whether your breasts are dense. According to the National Cancer Institute, nearly half of women 40 and older who get mammograms have dense breasts. It&rsquo;s common and normal, but dense tissue can hide cancers on a mammogram and slightly raises risk.</p>
  <p>If you get a dense-breast letter, ask about your overall risk and whether added imaging, such as ultrasound or MRI, makes sense for you. National guidelines don&rsquo;t yet agree on extra imaging for everyone with dense breasts.</p>

  <h2>Your personal risk</h2>
  <p>Family history on both sides, including ovarian, pancreatic and prostate cancer, can change when and how you screen. See <a href="/genetic-testing-women/">genetic testing for women</a>.</p>

  <h2>Hormone therapy and breast cancer: the real numbers</h2>
  <p>The Women&rsquo;s Health Initiative, the largest trial of hormone therapy, found that results depended on the type of therapy. In long-term follow-up published in 2020:</p>
  <ul>
    <li><strong>Estrogen plus a synthetic progestin</strong> (for women with a uterus): about 45 breast cancer diagnoses per 10,000 women per year, compared with 36 on placebo.</li>
    <li><strong>Estrogen alone</strong> (for women without a uterus): about 30 per 10,000 women per year, compared with 37 on placebo.</li>
  </ul>
  <p>Risk depends on your age, the type and dose of hormones, how long you use them and your personal history. The Menopause Society considers the benefit-risk balance favorable for most healthy women under 60 or within 10 years of menopause who have bothersome symptoms. Keep up your mammograms if you use hormone therapy. No blood, saliva or tear test replaces recommended screening.</p>

  <h2>Everyday risk reducers</h2>
  <ul><li>Limit alcohol.</li><li>Stay active. See <a href="/strength-training-women-over-40/">strength after 40</a>.</li><li>Look after your metabolic health. See <a href="/menopause-weight-gain-heart-health/">midlife weight &amp; heart health</a>.</li></ul>
''',
    alert="<strong>Book a prompt visit for</strong> a new lump in the breast or armpit, skin dimpling or an orange-peel texture, a nipple that newly turns inward, bloody or clear discharge from one nipple, or one breast that suddenly becomes red, swollen and warm.",
    related=["/genetic-testing-women/", "/hormone-testing-menopause/", "/beyond-hormone-therapy-midlife/"],
    faq=[
        ("When should I start getting mammograms?", "By age 40. The USPSTF recommends every two years from 40 to 74; other groups recommend yearly. Decide with your clinician."),
        ("What does it mean if I have dense breasts?", "Dense tissue is common and normal, but it can hide cancers on a mammogram and slightly raises risk. Ask whether added imaging makes sense for you."),
        ("Does hormone therapy cause breast cancer?", "It depends on the type. In the WHI trial, estrogen plus a synthetic progestin slightly raised breast cancer rates, while estrogen alone did not."),
        ("Can I skip mammograms if I&rsquo;m on hormone therapy?", "No. Keep up recommended screening. No blood, saliva or tear test replaces a mammogram."),
        ("Are tender, lumpy breasts normal in perimenopause?", "Often, especially before a period. A new lump or a change that lasts through a full cycle still needs an exam."),
    ],
    sources="U.S. Preventive Services Task Force, breast cancer screening (2024); American Cancer Society screening recommendations; American College of Radiology (Monticciolo et al., 2023); U.S. FDA Mammography Quality Standards Act final rule (2023, effective 2024); National Cancer Institute, dense breasts; Chlebowski et al., <em>JAMA</em> 2020 (WHI); The Menopause Society 2022 Hormone Therapy Position Statement.",
    about=["Breast cancer"],
    seo_title="Breast Health in Perimenopause: Mammograms, Dense Breasts & Hormones | Serene Med Spa",
    seo_desc="Mammograms from 40, what a dense-breast letter means, and what hormone therapy really does to breast cancer risk, explained by physicians.",
)

# ---------------------------------------------------------------------------------------------------------------- sexual health (Gupta + Killen)
A["/sexual-health-menopause/"] = dict(
    h1="Low libido, dryness and painful sex after 40",
    hero="Changes in desire, comfort and arousal are common in perimenopause and menopause, and very treatable. Here&rsquo;s what&rsquo;s normal and what helps.",
    crumb="Sexual health", quiz=True,
    lede="Sexual health is health. Yet many women never bring it up, and many clinicians never ask. If something has changed and it bothers you, it&rsquo;s worth a conversation.",
    body='''
  <h2>You&rsquo;re not alone, and it&rsquo;s not &ldquo;just aging&rdquo;</h2>
  <p>In a large U.S. survey of more than 31,000 women, about 43% reported some kind of sexual problem, but about 12% had a problem that also caused them distress. That rate was highest in women aged 45 to 64, at about 1 in 7. What matters isn&rsquo;t how often you have sex; it&rsquo;s whether something has changed in a way that bothers you.</p>

  <h2>Desire can change shape</h2>
  <p>Many women experience <strong>responsive</strong> desire: interest that builds after touch and closeness begin, rather than appearing out of the blue. That&rsquo;s normal. Stress, poor sleep, mood, pain, relationship strain and some medicines, including certain antidepressants and hormonal birth control, can all turn desire down.</p>

  <h2>Genitourinary syndrome of menopause (GSM)</h2>
  <p>Falling estrogen thins and dries the tissues of the vagina, vulva and bladder. The Menopause Society estimates that this affects 27% to 84% of postmenopausal women. Symptoms include dryness, burning, pain with sex, urgency and repeat urinary tract infections. Unlike hot flashes, it usually doesn&rsquo;t improve on its own.</p>
  <p>A 2025 guideline from the American Urological Association and partner societies recommends:</p>
  <ul>
    <li><strong>Vaginal moisturizers</strong> used regularly and <strong>lubricants</strong> for sex</li>
    <li><strong>Low-dose vaginal estrogen</strong> for dryness, irritation and painful sex, and for women with GSM and repeat urinary tract infections</li>
    <li><strong>Other prescription vaginal and oral options</strong> when estrogen isn&rsquo;t preferred</li>
  </ul>
  <p>The same guideline notes there&rsquo;s no evidence linking low-dose vaginal estrogen to breast cancer. If you&rsquo;ve had breast cancer, the decision is made together with your cancer team.</p>

  <h2>When sex hurts: at the opening or deep inside</h2>
  <ul>
    <li><strong>Pain at the opening</strong> can come from GSM, skin conditions of the vulva such as lichen sclerosus, nerve sensitivity or tight pelvic floor muscles.</li>
    <li><strong>Deep pain</strong> can come from endometriosis, pelvic infection, or bladder or bowel conditions. See <a href="/endometriosis-symptoms/">endometriosis</a>.</li>
  </ul>
  <p>Each has specific treatments, including pelvic floor physical therapy, so pain is worth reporting rather than pushing through.</p>

  <h2>What a sexual-health visit looks like</h2>
  <p>We start with a conversation about what&rsquo;s changed, your health history, medicines and relationship. If an exam is needed, it&rsquo;s gentle, explained step by step and stops whenever you ask. Hormone blood tests don&rsquo;t diagnose low libido. See <a href="/hormone-testing-menopause/">hormone testing</a>.</p>

  <h2>Treatments with evidence</h2>
  <ul>
    <li><strong>Talking therapies:</strong> sex therapy, couples therapy, cognitive behavioral therapy and mindfulness are core treatments for low desire.</li>
    <li><strong>Pelvic floor physical therapy</strong> and gentle dilator programs for pain.</li>
    <li><strong>Vaginal hormone options</strong> for GSM.</li>
    <li><strong>FDA-approved medicines for low desire</strong> in premenopausal women.</li>
    <li><strong>Testosterone</strong> for postmenopausal women with distressing low desire. The 2019 global consensus says this is its only evidence-based use in women. At Serene it&rsquo;s evaluated, prescribed and monitored in person only.</li>
  </ul>

  <h2>Everyday steps</h2>
  <ul><li>Use a water- or silicone-based lubricant, and skip scented products and douches.</li><li>Make time for intimacy that isn&rsquo;t rushed, and talk openly with your partner.</li><li>Protect sleep, move regularly and manage stress. See <a href="/menopause-mood-sleep-brain-fog/">mood, sleep &amp; brain fog</a>.</li><li>Bring a list of your medicines to your visit.</li></ul>
''',
    alert="<strong>See a clinician promptly for</strong> any bleeding after menopause, bleeding after sex, a new vulvar sore, lump or white patch, pain with fever or unusual discharge, or new severe pelvic pain. If you feel unsafe in a relationship, call the National Domestic Violence Hotline at 1-800-799-7233.",
    related=["/perimenopause/", "/endometriosis-symptoms/", "/beyond-hormone-therapy-midlife/"],
    faq=[
        ("Is low libido in perimenopause normal?", "It&rsquo;s common. It&rsquo;s worth treating when it bothers you. Hormones, sleep, stress, mood, medicines and relationship factors can all play a part."),
        ("What helps vaginal dryness after menopause?", "Regular vaginal moisturizers, lubricants for sex and, when needed, low-dose vaginal hormone options, which guidelines recommend."),
        ("Is vaginal estrogen safe?", "A 2025 guideline found no evidence linking low-dose vaginal estrogen to breast cancer. If you&rsquo;ve had breast cancer, decide together with your cancer team."),
        ("Can testosterone help my libido?", "For postmenopausal women with distressing low desire, it can. At Serene, testosterone is evaluated and prescribed in person only."),
        ("Why does sex hurt?", "Pain at the opening and deep pain have different causes, from dryness and skin conditions to pelvic floor tension and endometriosis. Each has specific treatments."),
    ],
    sources="Shifren et al., <em>Obstetrics &amp; Gynecology</em> 2008 (PRESIDE); The Menopause Society 2020 GSM Position Statement; AUA/SUFU/AUGS Genitourinary Syndrome of Menopause Guideline (2025); Davis et al., Global Consensus Position Statement on Testosterone Therapy for Women, <em>J Clin Endocrinol Metab</em> 2019; Islam et al., <em>Lancet Diabetes &amp; Endocrinology</em> 2019.",
    about=["Female sexual dysfunction", "Genitourinary syndrome of menopause"],
    seo_title="Low Libido, Vaginal Dryness & Painful Sex After 40: What Helps | Serene Med Spa",
    seo_desc="Low desire, dryness or pain with sex in perimenopause and menopause are common and treatable. Learn the causes and evidence-based options.",
)

# ================================================================================================================ fold-ins (batch 1 articles)
def _ins(slug, before, html):
    b = A[slug]["body"]
    assert before in b, (slug, before)
    A[slug]["body"] = b.replace(before, html + before, 1)

# hormone testing: Jones (calendar), Minich (FSH timeline), Smeaton (already on HT)
_ins("/hormone-testing-menopause/", "  <h2>When blood tests are worth it</h2>", '''  <h2>Your calendar is often the best test</h2>
  <p>Researchers stage the transition by cycle changes, not lab values. Early perimenopause is when the length of your cycles keeps varying by 7 days or more; late perimenopause is when you go 60 days or more without a period. A simple period-tracking app can tell you more than a single blood test.</p>
  <p>FSH, one of the first hormones to shift, began rising about six years before the final period in the SWAN study and leveled off about two years after it. Estradiol can stay normal or even spike for much of that time, which is why one result can point the wrong way.</p>

''')
_ins("/hormone-testing-menopause/", "  <h2>Midlife labs that matter anyway</h2>", '''  <h2>Already on hormone therapy? When an estrogen level helps</h2>
  <ul>
    <li><strong>The same dose works differently in different bodies.</strong> Estrogen through the skin, as a patch, gel or spray, is absorbed differently from person to person, so two women on the same prescription can have quite different levels.</li>
    <li><strong>A level can help</strong> if you still have bothersome symptoms despite treatment and we want to know whether you&rsquo;re absorbing it, or if you went through menopause before 40. Changing how estrogen is delivered often helps more than chasing a number, according to the British Menopause Society.</li>
    <li><strong>Timing matters.</strong> With gels, the result depends on when you last applied it, so follow the timing instructions you&rsquo;re given and draw blood from the opposite arm.</li>
    <li><strong>No magic number for bone.</strong> Hormone therapy protects bone in a dose-related way, but there&rsquo;s no proven minimum blood level. In one two-year trial, even a very low-dose estrogen patch improved spine and hip bone density in women aged 60 to 80. Bone density scans, not hormone levels, are how bone health is tracked.</li>
  </ul>

''')
A["/hormone-testing-menopause/"]["sources"] = A["/hormone-testing-menopause/"]["sources"].rstrip(".") + "; Harlow et al., STRAW+10, <em>Menopause</em> 2012; Randolph et al., <em>J Clin Endocrinol Metab</em> 2011 (SWAN); British Menopause Society, measurement of serum estradiol (2025); Ettinger et al., <em>Obstet Gynecol</em> 2004."

# strength: SWAN bone timing (Minich FSH brief)
_ins("/strength-training-women-over-40/", "  <h2>Feed your muscle with whole-food protein</h2>", '''  <h2>Your bones are on the same clock</h2>
  <p>Bone loss doesn&rsquo;t wait for your last period. In the SWAN study, bone density began dropping about a year before the final period, and over a decade women lost roughly 10% of their spine bone density, most of it during the transition. That makes your 40s an important time for strength and impact training, and for asking whether a bone density scan makes sense for you. See <a href="/everyday-chemicals-menopause-bone-health/">menopause &amp; bone health</a>.</p>

''')
A["/strength-training-women-over-40/"]["sources"] = A["/strength-training-women-over-40/"]["sources"].rstrip(".") + "; Greendale et al., <em>J Bone Miner Res</em> 2012 (SWAN)."

# brain: 2025 WHO-commissioned meta-analysis (Brighten brain brief)
_old = "Hormone therapy isn&rsquo;t recommended to prevent dementia.</p>"
assert _old in A["/brain-health-after-40/"]["body"]
A["/brain-health-after-40/"]["body"] = A["/brain-health-after-40/"]["body"].replace(_old, "Hormone therapy isn&rsquo;t recommended to prevent dementia. A large 2025 analysis of studies including about a million women, commissioned for the World Health Organization, found no link between hormone therapy and dementia risk in either direction.</p>", 1)
A["/brain-health-after-40/"]["sources"] = A["/brain-health-after-40/"]["sources"].rstrip(".") + "; 2025 meta-analysis on menopausal hormone therapy and dementia, <em>Lancet Healthy Longevity</em> (via University College London)."
