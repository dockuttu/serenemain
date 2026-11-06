/* form-guard.js — lightweight spam screening for the Zoho lead forms (consult form + offer popup + footer newsletter).
   serenemedspas.com copy (Oct 7 2026): adds the newsletter form (#zf-news) and '+digits' email aliases.
   Runs in the capture phase, before each form's own submit handler.
   - Honeypot filled  -> pretend success, send nothing.
   - Suspicious CONTENT (links, Cyrillic, SEO/marketing pitches, vendor solicitations) or a
     submit faster than a human could type -> still delivered, but tagged "Junk Lead" and
     prefixed so the front desk can skip it.
   - Structurally INVALID data (letters in the phone field, the same string repeated across
     name and phone, a whole sentence in a name field, the site's own confirmation copy echoed
     back, a heavily dotted gmail alias) -> same treatment. Added 9/2026 after a scraper bot
     submitted the form's own success message into First Name / Last Name / Phone.
   Nothing real is ever silently dropped. */
(function () {
  var T0 = Date.now();
  var PITCH = /(seo\b|search engine|online (visibility|presence|performance)|rank(ing)? (higher|on google)|website (audit|design|redesign)|improv\w* (the |your )?(site|website)|backlink|guest post|web ?developer|digital marketing|lead generation|bookkeeping|virtual assistant|merchant (services|cash)|business (loan|funding)|crypto|casino|free spins|wagering|jackpot|interested in (purchasing|buying)|serious buyer|used (aesthetic |medical )?equipment|\baudit\b|search rankings?|local (search|seo)|noticed (a few|a couple|some) (things|issues|opportunities|areas))/i;
  /* Copy the site itself renders on success — if it comes back as form input, a scraper echoed it. */
  var ECHO = /(thank you (very much )?for your (inquiry|interest|message)|we('| a)?ll be in touch|we have received|your (message|request) has been (sent|received)|thanks for reaching out)/i;

  function norm(v) { return (v || "").trim().replace(/\s+/g, " "); }
  function words(v) { return norm(v) ? norm(v).split(" ").length : 0; }

  function suspicious(text, elapsed) {
    if (/[Ѐ-ӿ]/.test(text)) return "non-English script";
    if (/https?:\/\/|www\.|\.(workers\.dev|ru|xyz|top)\b/i.test(text)) return "link in message";
    if (PITCH.test(text)) return "sales/marketing pitch";
    if (elapsed < 3000) return "submitted too fast";
    return "";
  }

  /* High-precision checks on field shape. A real person never trips these. */
  function structural(first, last, phone, email) {
    if (phone && /[A-Za-z]{3,}/.test(phone)) return "letters in phone field";
    var vals = [first, last, phone].map(norm).filter(function (v) { return v.length > 3; });
    for (var i = 0; i < vals.length; i++)
      for (var j = i + 1; j < vals.length; j++)
        if (vals[i].toLowerCase() === vals[j].toLowerCase()) return "same value repeated across fields";
    if (words(first) >= 5 || words(last) >= 5) return "sentence in name field";
    if (norm(first).length > 40 || norm(last).length > 40) return "name field too long";
    if (ECHO.test(first + " " + last + " " + phone)) return "site confirmation copy echoed into form";
    var local = (email || "").split("@")[0] || "";
    if ((local.match(/\./g) || []).length >= 4) return "heavily dotted email alias";
    if (/\+s?\d{4,}$/i.test(local)) return "numbered email alias (bot pattern)";
    return "";
  }

  function setHidden(f, name, val) {
    var i = f.querySelector('[name="' + name + '"]');
    if (!i) { i = document.createElement("input"); i.type = "hidden"; i.name = name; f.appendChild(i); }
    i.value = val;
  }
  function val(f, n) { var e = f.querySelector('[name="' + n + '"]'); return e ? e.value : ""; }


  /* Google Ads "Consult form submission" (Oct 7 2026). The forms send in the background and show an
     inline thank-you (#zf-done / popup .np-ok) instead of loading /thank-you/, so that page-load
     conversion never fired. Fire it here when a REAL submission succeeds (not junk-tagged, not honeypot). */
  var CONV = "AW-788907512/t1anCJXh6_0cEPiLl_gC", sgLast = null, fired = false;
  function fire() {
    if (fired || !sgLast || sgLast.hp || sgLast.junk) return;
    fired = true;
    try { if (window.gtag) gtag("event", "conversion", { send_to: CONV }); } catch (x) {}
  }
  if (window.MutationObserver) {
    new MutationObserver(function (ms) {
      for (var k = 0; k < ms.length; k++) {
        var m = ms[k];
        if (m.type === "attributes" && m.target.id === "zf-done" && !m.target.hidden) fire();
        if (m.type === "childList") for (var a = 0; a < m.addedNodes.length; a++) {
          var nd = m.addedNodes[a];
          if (nd.nodeType === 1 && (nd.classList.contains("np-ok") || (nd.querySelector && nd.querySelector(".np-ok")))) fire();
        }
      }
    }).observe(document.documentElement, { subtree: true, childList: true, attributes: true, attributeFilter: ["hidden"] });
  }

  document.addEventListener("submit", function (e) {
    var f = e.target;
    if (!f || !(f.id === "zf-consult" || f.id === "zf-news" || (f.classList && f.classList.contains("np-zf")))) return;
    var hp = f.querySelector('[name="aG9uZXlwb3Q"]');
    if (f.id !== "zf-news") sgLast = { hp: !!(hp && hp.value.trim()), junk: false };
    if (hp && hp.value.trim()) {
      e.preventDefault(); e.stopImmediatePropagation();
      if (f.id === "zf-consult") { f.hidden = true; var d = document.getElementById("zf-done"); if (d) d.hidden = false; }
      else if (f.id === "zf-news") { f.hidden = true; var nd = document.getElementById("zf-news-done"); if (nd) nd.hidden = false; }
      else { f.outerHTML = '<div class="np-ok">&#10003; Thank you!</div>'; }
      return;
    }
    var desc = f.querySelector('[name="Description"]');
    var first = val(f, "First Name"), last = val(f, "Last Name");
    var phone = val(f, "Phone"), email = val(f, "Email");
    var text = [desc && desc.tagName === "TEXTAREA" ? desc.value : "", first, last].join(" ");
    var why = suspicious(text, Date.now() - T0) || structural(first, last, phone, email);
    if (why) {
      if (f.id !== "zf-news" && sgLast) sgLast.junk = true;
      setHidden(f, "Lead Status", "Junk Lead");
      if (desc) desc.value = "[Auto-flagged: " + why + "] " + desc.value;
    }
  }, true);
})();

/* reCAPTCHA v2 "I'm not a robot" box on every Zoho lead form (Nov 6 2026, after a bot flood posted straight to
   Zoho). Zoho's "Request a Consultation" webform verifies the token server-side, so posts that skip this page fail.
   - Covers the consult form, the New Client Special popup (.np-zf), and the Obagi pickup cart (#co): any <form> whose
     action is Zoho's WebToLeadForm, plus those two.
   - Google's script loads only when someone starts filling in a lead form (keeps pages fast).
   - Runs in the capture phase BEFORE each form's own submit handler: no ticked box -> nothing is sent, the box
     is shown and the visitor gets a plain message. The widget's hidden "g-recaptcha-response" field sits inside
     the form, so FormData-based senders include it automatically; the cart adds it itself. */
(function () {
  var RC_KEY = "6LdCZhMuAAAAAPfnBNlYg4J52zxLRRTxMP7qJc_V", loading = false, ready = false, queue = [];
  function isLead(f) { return !!f && f.tagName === "FORM" && (/WebToLeadForm/.test(f.getAttribute("action") || "") || f.id === "co" || (f.classList && f.classList.contains("np-zf"))); }
  function load() {
    if (loading) return; loading = true;
    window.__sereneRcReady = function () { ready = true; queue.splice(0).forEach(render); };
    var s = document.createElement("script");
    s.src = "https://www.google.com/recaptcha/api.js?onload=__sereneRcReady&render=explicit";
    s.async = true; s.defer = true; document.head.appendChild(s);
  }
  function render(f) {
    if (f.__rcId !== undefined) return;
    if (!ready || !window.grecaptcha) { if (queue.indexOf(f) < 0) queue.push(f); load(); return; }
    var box = document.createElement("div");
    box.className = "zf-rc"; box.style.cssText = "margin:12px 0 4px;min-height:78px;max-width:100%;overflow:hidden";
    var btn = f.querySelector('button[type="submit"],input[type="submit"]');
    var at = btn ? (btn.closest(".zf-actions") || btn) : null;
    if (at && f.contains(at) && at.parentNode) at.parentNode.insertBefore(box, at); else f.appendChild(box);
    var narrow = (f.getBoundingClientRect().width || 400) < 320;
    try { f.__rcId = window.grecaptcha.render(box, { sitekey: RC_KEY, size: narrow ? "compact" : "normal",
      callback: function () { msg(f, ""); } }); } catch (x) {}
  }
  function token(f) {
    try { return (f.__rcId !== undefined && window.grecaptcha) ? window.grecaptcha.getResponse(f.__rcId) : ""; } catch (x) { return ""; }
  }
  function msg(f, t) {
    var m = f.querySelector(".zf-rc-msg");
    if (!m) { if (!t) return; m = document.createElement("p"); m.className = "zf-rc-msg"; m.setAttribute("role", "alert");
      m.style.cssText = "margin:4px 0 8px;font-size:15px;font-weight:600;color:#b3261e";
      var box = f.querySelector(".zf-rc"); if (box && box.parentNode) box.parentNode.insertBefore(m, box.nextSibling); else f.appendChild(m); }
    m.textContent = t;
  }
  window.SereneCaptcha = { token: token };   // used by the Obagi cart, which builds its own request
  document.addEventListener("focusin", function (e) { var f = e.target && e.target.closest && e.target.closest("form"); if (isLead(f)) render(f); }, true);
  document.addEventListener("submit", function (e) {
    var f = e.target; if (!isLead(f)) return;
    var hp = f.querySelector('[name="aG9uZXlwb3Q"]'); if (hp && hp.value.trim()) return;   // honeypot path handled by the guard above
    if (token(f)) return;
    e.preventDefault(); e.stopImmediatePropagation();
    render(f);
    msg(f, "Please tick the “I’m not a robot” box, then press the button again.");
  }, true);
})();
