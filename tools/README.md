# tools

The site is static, with no framework and no build step, except for these. Run
them with plain `python tools/<name>.py` from the site root.

## build_pages.py — regenerates the four pages

`index.html`, `platform.html`, `trust.html` and `company.html` share one header,
one mega menu and one footer, and they live in this script rather than in four
copies. Four hand-maintained navigations diverge on the first edit, and the
break usually shows up on one page only, late.

**The rule: edit a section inside whichever page holds it, then run this.** It
collects every `<section>` from all four pages, redistributes them according to
the `PAGES` map at the top, rewrites anchors that now point to another page, and
writes the four files back. It is safe to run repeatedly.

Do not hand-edit the header or the footer in a page: the next run overwrites it.

## build_legal.py — regenerates the legal pages

`privacidade.html` / `privacy.html` and `aviso-legal.html` / `legal-notice.html`,
one file per language, from a single shell so the two languages cannot drift
apart structurally. Unlike the site pages, these do not use the JavaScript
toggle: legal text is easier to review and to hand to a lawyer as a whole file.

Everything the client still has to supply is wrapped in `TODO.format(...)` and
renders as a loud red dashed badge. Those badges must never reach production.

## rebrand.py and rebrand_all.py — product captures

Turns captures of the platform into Infinite World assets: the sidebar lockup is
redrawn from the real brand file, the orange accent moves onto `#008040`, and
rasterised words are found by template match and repainted. Operational content
is never touched.

`rebrand.py <capture>` does one file into `_previews/`. `rebrand_all.py [outdir]`
does every capture the site uses and re-cuts the map crop, writing over
`assets/screens/` when no output directory is given.

Needs `pillow`, `numpy`, `opencv-python` and `fonttools`. The Montserrat TTF it
draws the wordmark with is generated on first run from the woff2 the site
already ships, so no font binary is tracked here.

## serve_nocache.py — local preview on port 8756

`python -m http.server` serves stale CSS and JS from cache and costs a lot of
confusion. This one sends `no-store`.
