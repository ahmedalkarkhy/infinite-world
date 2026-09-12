# -*- coding: utf-8 -*-
"""Splits the single page into four, from one shared shell.

The header, the mega menu and the footer exist here once. Four copies of a
navigation diverge on the first edit, and that is the kind of drift nobody
notices until a link is wrong on one page only.

Run this after editing sections in index.html: it reads the current file as the
source of truth, then rewrites all four pages.
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")

# which page each section lands on, and in what order
PAGES = {
    "index.html": {
        "sections": ["hero", "proof", "company", "verticals", "contact"],
        "title_key": "pt_home",
        "desc_key": "pd_home",
        "title": "Infinite World | The Intelligence Layer for the Real World",
        "desc": "One technology core, seven categories, thirty solutions and six verticals. Headquarters in Dubai, European hub in Brussels.",
        "engine": False,
    },
    "platform.html": {
        "sections": ["platform", "biometrics", "screens", "value", "commercial"],
        "title_key": "pt_platform",
        "desc_key": "pd_platform",
        "title": "What We Do | Infinite World",
        "desc": "The digital catalogue: seven categories and thirty solutions on a single technology core, the biometric workforce layer, and the commercial architecture from diagnosis to expansion.",
        "engine": True,
    },
    "trust.html": {
        "sections": ["trust", "compliance"],
        "title_key": "pt_trust",
        "desc_key": "pd_trust",
        "title": "Trust | Infinite World",
        "desc": "Redundancy, recovery and protection inside the European Union, and the regulatory framework the platform is built against: GDPR and the AI Act.",
        "engine": False,
    },
    "company.html": {
        "sections": ["group", "pillars", "philosophy"],
        "title_key": "pt_company",
        "desc_key": "pd_company",
        "title": "Who We Are | Infinite World",
        "desc": "A Dubai holding with international operations. Global headquarters in Dubai, European hub in Brussels, and the principles the company operates by.",
        "engine": False,
    },
}

WHERE = {sid: page for page, cfg in PAGES.items() for sid in cfg["sections"]}

HEAD = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title data-i18n="{title_key}">{title}</title>
    <meta name="description" data-i18n-content="{desc_key}" content="{desc}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:type" content="website" />
    <link rel="icon" type="image/png" href="assets/favicon-256.png" />
    <link
      rel="preload"
      href="assets/fonts/montserrat-latin.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
"""

TAIL = """    <script src="i18n.js"></script>
    <script src="main.js"></script>
{engine}  </body>
</html>
"""


def read(p):
    return io.open(p, encoding="utf-8").read()


src = read(SRC)

header = re.search(r"    <!-- NAV -->\n    <header id=\"nav\">.*?\n    </header>\n", src, re.S)
assert header, "header not found"
footer = re.search(r"    <!-- FOOTER -->\n    <footer id=\"footer\">.*?\n    </footer>\n", src, re.S)
assert footer, "footer not found"

# Sections are collected from wherever they currently live, so this stays
# runnable after the split: edit a section inside its own page, run again.
# The trailing newline is a lookahead: consuming it would swallow the start of
# the next match, and adjacent sections would lose their comment.
SECTION_RE = re.compile(
    r'\n(      <!-- [^\n]*-->\n)?(      <section id="(\w+)".*?\n      </section>)(?=\n)', re.S
)

sections = {}
for name in ["index.html"] + [p for p in PAGES if p != "index.html"]:
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        continue
    for m in SECTION_RE.finditer(read(path)):
        sid = m.group(3)
        if sid in sections:
            continue
        block = (m.group(1) or "") + m.group(2) + "\n"
        # inner pages carry their opening heading as h1; store the h2 form
        if '<h1 class="sec-title"' in block:
            block = block.replace('<h1 class="sec-title" data-i18n=', "<h2 data-i18n=", 1)
            block = block.replace("</h1>", "</h2>", 1)
        sections[sid] = block
missing = set(WHERE) - set(sections)
assert not missing, "sections missing from source: %s" % missing


def retarget(html, current_page):
    """An anchor to a section that now lives elsewhere becomes a page link.

    Links already carrying a page are normalised back to a bare anchor first,
    otherwise a second run would read its own output and never correct a link
    whose section has since moved.
    """
    html = re.sub(r'href="[\w-]+\.html#(\w+)"', r'href="#\1"', html)

    def sub(m):
        sid = m.group(1)
        page = WHERE.get(sid)
        if page is None or page == current_page:
            return 'href="#%s"' % sid
        return 'href="%s#%s"' % (page, sid)

    return re.sub(r'href="#(\w+)"', sub, html)


for page, cfg in PAGES.items():
    body = "".join(sections[sid] for sid in cfg["sections"])
    # every page needs exactly one h1; on the inner pages the opening section
    # heading is promoted, which is why .section h1 is sized like an h2
    if page != "index.html":
        body = body.replace("<h2 data-i18n=", '<h1 class="sec-title" data-i18n=', 1)
        i = body.index('<h1 class="sec-title"')
        j = body.index("</h2>", i)
        body = body[:j] + "</h1>" + body[j + len("</h2>") :]

    html = (
        HEAD.format(**cfg)
        + retarget(header.group(0), page)
        + "\n    <main>\n"
        + retarget(body, page)
        + "    </main>\n\n"
        + retarget(footer.group(0), page)
        + "\n"
        + TAIL.format(
            engine='    <script type="module" src="engine.js"></script>\n'
            if cfg["engine"]
            else ""
        )
    )
    io.open(os.path.join(ROOT, page), "w", encoding="utf-8", newline="").write(html)
    print("%-16s %2d sections%s" % (page, len(cfg["sections"]), "  + engine" if cfg["engine"] else ""))
