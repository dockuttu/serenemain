# -*- coding: utf-8 -*-
"""hipaa_badge.py - add a "HIPAA-compliant patient forms" badge to every page footer.

    python3 hipaa_badge.py bundle/site /privacy-practices/

Arg 1: built site directory.  Arg 2: link to the site's privacy / HIPAA notice page.
Our patient intake and appointment forms run on a HIPAA-enabled Jotform account (BAA in
place), so the badge describes the forms, not the whole website. It is our own simple
shield icon - not a certification seal (there is no official HIPAA certification).
Idempotent: pages that already carry the badge are skipped.
"""
import os
import sys

SITE = sys.argv[1] if len(sys.argv) > 1 else "site"
PRIV = sys.argv[2] if len(sys.argv) > 2 else "/privacy/"
MARKER = 'id="hipaa-badge"'

SHIELD = ('<svg width="44" height="44" viewBox="0 0 24 24" aria-hidden="true" '
          'style="display:block"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z" '
          'fill="#2e7d5b"/><rect x="8.5" y="11" width="7" height="5.5" rx="1" fill="#fff"/>'
          '<path d="M10 11V9.5a2 2 0 0 1 4 0V11" stroke="#fff" stroke-width="1.4" fill="none"/></svg>')

BLOCK = (
    '<div %s style="max-width:1100px;margin:18px auto 0;padding:0 20px;display:flex;'
    'gap:14px;align-items:center;color:inherit">'
    '<span style="flex:0 0 auto;line-height:0">%s</span>'
    '<p style="margin:0;font-size:14px;line-height:1.45;color:inherit">'
    '<strong>HIPAA-compliant patient forms</strong> &middot; Your intake and appointment '
    'information is encrypted and kept private &middot; <a href="%s" '
    'style="color:inherit;text-decoration:underline">Privacy practices</a></p></div>'
) % (MARKER, SHIELD, PRIV)


def inject(doc):
    if MARKER in doc:
        return doc, False
    i = doc.rfind("</footer>")
    if i == -1:
        return doc, False
    return doc[:i] + BLOCK + doc[i:], True


def main():
    if not os.path.isdir(SITE):
        print("hipaa_badge: no such directory:", SITE)
        return
    done = skipped = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            with open(p, encoding="utf-8") as fh:
                doc = fh.read()
            new, changed = inject(doc)
            if changed:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(new)
                done += 1
            else:
                skipped += 1
    print("hipaa_badge: added to %d pages (%d skipped)" % (done, skipped))


if __name__ == "__main__":
    main()
