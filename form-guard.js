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
