# -*- coding: utf-8 -*-
"""Re-brands the product captures from Decadas to Infinite World.

The platform belongs to Infinite World; Decadas is one operator of it. These
captures are the Decadas instance, so the sidebar lockup is swapped for the
Infinite World one and the orange accent is moved onto the brand green. All
operational content is left untouched.
"""
import colorsys
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))

SIDEBAR = (13, 27, 43)
GREEN_HUE = 150.0 / 360.0  # brand green #008040
BRAND_GREEN = (0, 128, 64)
SYMBOL = os.path.join(ROOT, "assets", "simbolo-transparente-escuro-2048.png")
FONT = os.path.join(HERE, "montserrat.ttf")

if not os.path.exists(FONT):
    # derived from the woff2 the site already ships, so no binary is tracked
    from fontTools.ttLib import TTFont

    f = TTFont(os.path.join(ROOT, "assets", "fonts", "montserrat-latin.woff2"))
    f.flavor = None
    f.save(FONT)


def is_orange(r, g, b):
    """The Decadas accent, wide enough to catch antialiased edges."""
    if r < 90 or r - b < 45:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return 0.015 < h < 0.13 and s > 0.35 and v > 0.30





def recolour(im, sidebar=0, protect=()):
    """Move orange onto the brand green.

    The sidebar is pure interface, and lossy compression leaves its warm tints
    scattered between orange and pink, so any red dominant pixel there has its
    red and green channels swapped: same luminance, opposite hue. The content
    area is photography and semantic colour, so it gets the narrow hue rule and
    protected boxes keep map roads orange."""
    px = im.load()
    moved = 0
    for y in range(im.height):
        for x in range(im.width):
            if any(bx0 <= x < bx1 and by0 <= y < by1 for bx0, by0, bx1, by1 in protect):
                continue
            r, g, b = px[x, y]
            if x < sidebar:
                if r <= g:
                    continue
                px[x, y] = (g, r, b)
                moved += 1
                continue
            if not is_orange(r, g, b):
                continue
            _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s > 0.55:
                # a solid brand surface: land it exactly on #008040
                px[x, y] = BRAND_GREEN
            else:
                # an antialiased edge or a tint: keep its own weight
                nr, ng, nb = colorsys.hsv_to_rgb(GREEN_HUE, min(s * 1.05, 1.0), v * 0.9)
                px[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255))
            moved += 1
    return moved


def draw_lockup(im, box, mark_h, text_size, tracking, pad=20):
    """Clear the old logo block and draw symbol + INFINITE WORLD in its place."""
    x0, y0, x1, y1 = box
    ImageDraw.Draw(im).rectangle(box, fill=SIDEBAR)

    sym = Image.open(SYMBOL).convert("RGBA")
    sym = sym.crop(sym.getbbox())
    w = max(1, round(sym.width * mark_h / sym.height))
    sym = sym.resize((w, mark_h), Image.LANCZOS)

    font = ImageFont.truetype(FONT, text_size)
    try:
        font.set_variation_by_axes([700])
    except Exception:
        pass

    word = "INFINITE WORLD"
    d = ImageDraw.Draw(im)
    widths = [d.textlength(c, font=font) for c in word]
    text_w = sum(widths) + tracking * (len(word) - 1)

    total_h = mark_h + 8 + text_size
    top = y0 + max(0, ((y1 - y0) - total_h) // 2)

    im.paste(sym, (x0 + pad, top), sym)

    x = float(x0 + pad)
    ty = top + mark_h + 8
    for c, cw in zip(word, widths):
        d.text((x, ty), c, font=font, fill=(244, 244, 242))
        x += cw + tracking


LAYOUT = {
    # capture: (logo box to clear, symbol height, wordmark size, tracking)
    "desk": ((0, 0, 140, 48), 17, 8, 1.5),
}


SIDEBAR_END = 249

# Map tiles are photography, not interface: their orange roads stay orange.
PROTECT = {
    "desk-overview.webp": ((282, 404, 1400, 690),),
}


def process(name, kind="desk"):
    src = os.path.join(ROOT, "assets", "screens", name)
    im = Image.open(src).convert("RGB")
    sidebar = SIDEBAR_END if kind == "desk" else 0
    moved = recolour(im, sidebar=sidebar, protect=PROTECT.get(name, ()))
    # after the recolour, or the swap would strip the red arc out of the mark
    if kind == "desk":
        draw_lockup(im, *LAYOUT["desk"])
    return im, moved


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "desk-team.webp"
    out = os.path.join(HERE, "rebrand-" + target.replace(".webp", ".png"))
    im, moved = process(target)
    im.save(out)
    print("escrito", out, "| pixeis laranja movidos:", moved)
