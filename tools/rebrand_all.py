# -*- coding: utf-8 -*-
"""Re-brands every product capture used on the site, Decadas to Infinite World.

Three passes per capture: the accent colour moves onto the brand green, the
sidebar lockup is replaced, and the rasterised words that name the operator are
found by template match and repainted. Operational content is never touched.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rebrand import LAYOUT, PROTECT, SIDEBAR_END, draw_lockup, recolour

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCREENS = os.path.join(ROOT, "assets", "screens")

SANS = "C:/Windows/Fonts/segoeui.ttf"
SANS_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
MONO_BOLD = "C:/Windows/Fonts/consolab.ttf"


def tight_bbox(im, region, ink_max=170):
    """The bounding box of the dark ink inside a rough region."""
    x0, y0, x1, y1 = region
    a = np.asarray(im.convert("L").crop(region))
    ys, xs = np.where(a < ink_max)
    if not len(ys):
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)


def find_all(im, template, threshold=0.80):
    a = np.asarray(im.convert("L"))
    t = np.asarray(template.convert("L"))
    th, tw = t.shape
    if a.shape[0] < th or a.shape[1] < tw:
        return []
    score = cv2.matchTemplate(a, t, cv2.TM_CCOEFF_NORMED)
    hits = []
    ys, xs = np.where(score >= threshold)
    for y, x in sorted(zip(ys, xs), key=lambda p: -score[p[0], p[1]]):
        if any(abs(y - hy) < th and abs(x - hx) < tw for hy, hx in hits):
            continue
        hits.append((int(y), int(x)))
    return sorted(hits)


def ink_colour(tile, share=25):
    a = np.asarray(tile).reshape(-1, 3).astype(int)
    darkest = a[a.sum(1).argsort()[: max(1, len(a) // share)]]
    return tuple(int(v) for v in darkest.mean(0))


def draw_tracked(d, xy, text, font, fill, width):
    """Draw text stretched to a target width by even letter spacing."""
    x, y = xy
    widths = [d.textlength(c, font=font) for c in text]
    slack = width - sum(widths)
    step = slack / max(1, len(text) - 1)
    for c, cw in zip(text, widths):
        d.text((x, y), c, font=font, fill=fill)
        x += cw + step


# One clean sample of each word, taken from the capture where it sits alone,
# then matched against every capture. Layouts differ per screen, so hunting by
# fixed coordinates in each one is fragile.
TEMPLATES = [
    {
        "src": "desk-works.webp",
        "box": (284, 170, 334, 179),
        "text": "LICENÇA",
        "font": MONO_BOLD,
        "tracked": True,
    },
    {
        "src": "desk-audit.webp",
        "box": (301, 121, 349, 132),
        "text": "Licença",
        "font": SANS_BOLD,
        "tracked": False,
    },
    {
        "src": "desk-audit.webp",
        "box": (489, 291, 578, 307),
        "text": "Infinite World",
        "font": SANS,
        "tracked": False,
    },
]


def load_templates():
    out = []
    for t in TEMPLATES:
        src = Image.open(os.path.join(SCREENS, t["src"])).convert("RGB")
        tile = src.crop(t["box"])
        out.append({**t, "tile": tile, "ink": ink_colour(tile)})
    return out


def swap_words(im, templates):
    d = ImageDraw.Draw(im)
    done = 0
    for t in templates:
        tile = t["tile"]
        w, h = tile.size
        for y, x in find_all(im, tile):
            bg = im.getpixel((x, max(0, y - 3)))
            # one pixel of padding: an ascender can sit just outside the box
            d.rectangle((x - 1, y - 1, x + w, y + h), fill=bg)
            size = h + 4
            font = ImageFont.truetype(t["font"], size)
            while d.textlength(t["text"], font=font) > w and size > 7:
                size -= 1
                font = ImageFont.truetype(t["font"], size)
            asc, _ = font.getmetrics()
            ty = y + h - asc + (asc - h) // 2
            if t["tracked"]:
                draw_tracked(d, (x, ty), t["text"], font, t["ink"], w)
            else:
                d.text((x, ty), t["text"], font=font, fill=t["ink"])
            done += 1
    return done


DESKTOPS = [
    "desk-overview.webp",
    "desk-team.webp",
    "desk-works.webp",
    "desk-alerts.webp",
    "desk-audit.webp",
]
PHONES = ["phone-checkin.webp", "phone-report.webp"]


def build(name, kind, templates):
    im = Image.open(os.path.join(SCREENS, name)).convert("RGB")
    words = swap_words(im, templates)
    sidebar = SIDEBAR_END if kind == "desk" else 0
    moved = recolour(im, sidebar=sidebar, protect=PROTECT.get(name, ()))
    if kind == "desk":
        draw_lockup(im, *LAYOUT["desk"])
    return im, moved, words


if __name__ == "__main__":
    OUT = sys.argv[1] if len(sys.argv) > 1 else SCREENS
    os.makedirs(OUT, exist_ok=True)
    templates = load_templates()
    for name in DESKTOPS + PHONES:
        kind = "desk" if name.startswith("desk") else "phone"
        im, moved, words = build(name, kind, templates)
        out = os.path.join(OUT, name)
        im.save(out, "WEBP", quality=90, method=6)
        print(f"{name:22s} pixeis recolorados={moved:6d}  palavras trocadas={words}")

    # the menu card crop is taken from the rebranded overview
    src = Image.open(os.path.join(OUT, "desk-overview.webp")).convert("RGB")
    w = 624
    h = int(w / 1.6)
    crop = src.crop((src.width - w, src.height - h, src.width, src.height))
    crop = crop.resize((w * 2, h * 2), Image.LANCZOS)
    crop.save(os.path.join(OUT, "map-works.webp"), "WEBP", quality=88, method=6)
    print("map-works.webp          regenerado a partir do overview")
