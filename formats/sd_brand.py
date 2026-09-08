"""Split Decision — brand mark.

Two Quick Sips glasses tilted toward each other at the moment of the
clink. Not a redrawn glass: the actual QS glyph, used twice, so the two
series share a piece of house furniture rather than each owning a
similar-but-different wine glass.

COLOUR IS NOT FIXED. Split Decision inherits its arc's Field Guide
palette so the pair read as siblings in the grid — sd_mark takes the
palette dict and pulls SIGNATURE and ACCENT from it. The two glasses
must differ from each other, because the style guide requires the poles
to be distinguished by colour and never by size or weight; neither side
may look like the favoured one before it has been read.

THIS ONE DEPENDS ON A FILE, unlike the FFFA checklist and the GTR
folded map, which are drawn from primitives. That is a deliberate
trade: sharing the glyph is the point, and re-drawing it would defeat
it. The risk is real — the QS icon has already shipped once as an
opaque square and once missing entirely — so _glass_glyph raises
rather than silently drawing nothing, and it repairs a fully-opaque
source by deriving alpha from luminance the way the icon rebuild did.
"""
import functools
import math
import os

import numpy as np
from PIL import Image, ImageDraw

import core

GLASS_PATH = os.path.join(core.PHOTO_DIR, "QS_glass_icon_ink.png")


@functools.lru_cache(maxsize=4)
def _glass_glyph():
    """The QS glass as an alpha mask, cropped to its ink.

    Cropping matters: the source is a 392px square with the glyph
    occupying x 102-294, so using it uncropped would make the two
    glasses sit far apart with the gap set by padding rather than by
    the design.
    """
    if not os.path.exists(GLASS_PATH):
        raise FileNotFoundError(
            f"Split Decision mark needs the Quick Sips glass at {GLASS_PATH}. "
            "It is in the save-back photo bundle.")
    im = Image.open(GLASS_PATH).convert("RGBA")
    a = im.split()[-1]

    if a.getextrema()[0] > 250:
        # Fully opaque source: the glyph is dark linework on an opaque
        # white field. Derive alpha from luminance, as the icon rebuild
        # did, or the mark paints a white box on every page.
        lum = im.convert("L")
        a = lum.point(lambda v: max(0, min(255, int((235 - v) * 255 / 200))))

    return a.crop(a.getbbox())


@functools.lru_cache(maxsize=4)
def _glass_parts():
    """Split the QS glyph into (walls, interior) masks.

    The glyph draws the liquid as a straight bar across the bowl. Rotated
    with the glass, that bar tilts with it — which is what wine does not
    do. So the bar is lifted out here and redrawn per-glass at an angle
    that cancels the tilt.

    `walls` is the glyph with the liquid bar removed. `interior` is the
    open space inside the bowl, used to clip the replacement liquid so it
    stops exactly at the inside of the glass wall rather than crossing it.

    The bar is found rather than hard-coded: in the bowl region it is the
    only row band where the ink forms a SINGLE run spanning most of the
    width. Everywhere else the bowl reads as two runs, one per wall.
    """
    mask = _glass_glyph()
    a = np.asarray(mask).copy()
    ink = a > 8
    h, w = ink.shape

    band = [y for y in range(int(h * 0.2), int(h * 0.7))
            if ink[y].any()
            and (np.diff(np.where(ink[y])[0]) > 1).sum() == 0
            and np.ptp(np.where(ink[y])[0]) > w * 0.85]
    if not band:
        # No detectable bar: leave the glyph alone rather than guess.
        return mask, Image.new("L", mask.size, 0)
    y0, y1 = band[0], band[-1]

    # Wall x-positions taken just outside the bar, where the two runs
    # are unambiguous, then interpolated across it.
    def walls_at(y):
        """Inner edges of the two bowl walls on this row.

        Takes the WIDEST gap, not the first. The source is anti-aliased,
        so a row often contains stray one-pixel runs before the real
        bowl cavity; picking the first gap returned two edges a pixel
        apart, the row was discarded as degenerate, and the interior
        mask came out striped — which is what tore the liquid surface
        into ribbons.
        """
        xs = np.where(ink[y])[0]
        if len(xs) < 2:
            return None
        d = np.diff(xs)
        gaps = np.where(d > 1)[0]
        if len(gaps) == 0:
            return None
        widest = gaps[np.argmax(d[gaps])]
        return xs[widest], xs[widest + 1]

    above, below = walls_at(y0 - 4), walls_at(y1 + 4)
    if above is None or below is None:
        return mask, Image.new("L", mask.size, 0)

    # Widen the removal by a couple of rows: the source is anti-aliased,
    # so the rows just outside the detected band keep faint ink that
    # survives as a hairline across the bowl.
    y0, y1 = y0 - 2, y1 + 2
    for i, y in enumerate(range(y0, y1 + 1)):
        t = i / max(1, (y1 - y0))
        li = int(round(above[0] + (below[0] - above[0]) * t))
        ri = int(round(above[1] + (below[1] - above[1]) * t))
        a[y, li + 1:ri] = 0

    walls = Image.fromarray(a, "L")

    # Interior: the open space inside the bowl, found by FLOOD FILL from
    # a seed inside the bowl rather than by reading wall edges row by
    # row. Row-wise edge detection kept producing a wedge: the bar's own
    # rows return a single run, so they had to be interpolated across,
    # and any stray anti-aliased run threw the interpolation far enough
    # off that the mask bled outside the glass on one side and cut a
    # diagonal out of it on the other. A flood fill has none of those
    # failure modes — it simply cannot escape a closed outline.
    filled = Image.new("L", walls.size, 0)
    open_space = Image.eval(walls, lambda v: 0 if v > 8 else 255)
    seed_y = max(0, y0 - 12)
    ImageDraw.floodfill(open_space, (walls.width // 2, seed_y), 128, thresh=0)
    ImageDraw.floodfill(open_space, (walls.width // 2, min(h - 1, y1 + 12)),
                        128, thresh=0)
    inner = np.asarray(open_space).copy()
    filled = Image.fromarray(np.where(inner == 128, 255, 0).astype("uint8"), "L")

    return walls, filled


def _liquid_mask(size, tilt, slosh=3.0):
    """A near-horizontal liquid surface, drawn in glyph space.

    Pre-rotated by -tilt so that when the whole glass is rotated by
    +tilt the surface comes out level, which is what a liquid actually
    does. `slosh` tips it a few degrees off true so it reads as wine
    that has just been knocked rather than a spirit level.
    """
    walls, interior = _glass_parts()
    w, h = walls.size
    layer = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(layer)

    ink = np.asarray(interior) > 0
    rows = np.where(ink.any(axis=1))[0]
    if len(rows) == 0:
        return layer
    # Surface height: where the glyph's own bar sat, so the fill level
    # is unchanged from the Quick Sips glass.
    band = [y for y in rows if ink[y].sum() > w * 0.5]
    cy = (band[0] + band[-1]) / 2 if band else float(np.mean(rows))
    cx = w / 2.0

    # PIL rotates counter-clockwise, so a line drawn at `ang` ends up at
    # (ang - tilt) once the glass is rotated. To land level we want that
    # to equal `slosh`, hence ang = tilt + slosh. Signing it the other
    # way doubled the tilt instead of cancelling it.
    ang = math.radians(tilt + slosh)
    half = w * 1.2
    dx, dy = math.cos(ang) * half, math.sin(ang) * half
    lw = max(2, int(round(h * 0.062)))
    d.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=255, width=lw)

    layer = Image.composite(layer, Image.new("L", (w, h), 0), interior)
    return layer


def _tinted(size, color, tilt):
    """One glass: walls plus a level liquid surface, tinted, scaled to
    `size` tall, then rotated by tilt."""
    walls, _ = _glass_parts()
    combined = Image.new("L", walls.size, 0)
    combined.paste(walls, (0, 0))
    liquid = _liquid_mask(size, tilt)
    combined.paste(liquid, (0, 0), liquid)

    h = max(8, int(size))
    w = max(4, int(round(combined.width * h / combined.height)))
    m = combined.resize((w, h), Image.LANCZOS)

    glyph = Image.new("RGBA", m.size, tuple(color) + (0,))
    glyph.putalpha(m)
    # expand=True so the rotated corners are not clipped
    return glyph.rotate(tilt, resample=Image.BICUBIC, expand=True)


def sd_mark_bbox(size, gap=0.30, tilt=18):
    left = _tinted(size, (0, 0, 0), -tilt)
    right = _tinted(size, (0, 0, 0), tilt)
    overlap = int(left.width * gap)
    return left.width + right.width - overlap, max(left.height, right.height)


def sd_mark(img, x, y, size, pal, gap=0.30, tilt=18):
    """Two glasses leaning into each other, rims almost touching.

    They lean toward each other rather than standing upright because two
    upright glasses read as a pair of glasses; leaning, they read as a
    toast — and as two positions meeting, which is the format.

    `gap` is the fraction of a glass's width by which the two overlap.
    It has to be substantial: the glyph carries its own padding either
    side of the bowl, so at a small gap the rims sit visibly apart and
    the mark reads as two separate glasses rather than as contact.
    """
    # PIL rotates counter-clockwise for positive angles, so the LEFT
    # glass takes the negative tilt to lean its rim right, toward its
    # partner. Signed the obvious way round, both glasses leaned
    # outward and the mark read as two glasses being set down rather
    # than a toast.
    left = _tinted(size, pal["SIGNATURE"], -tilt)
    right = _tinted(size, pal["ACCENT"], tilt)
    overlap = int(left.width * gap)

    base = y + max(left.height, right.height)
    img.alpha_composite(left, (int(x), int(base - left.height))) \
        if img.mode == "RGBA" else \
        img.paste(left, (int(x), int(base - left.height)), left)

    rx = int(x + left.width - overlap)
    img.alpha_composite(right, (rx, int(base - right.height))) \
        if img.mode == "RGBA" else \
        img.paste(right, (rx, int(base - right.height)), right)

    return left.width + right.width - overlap, max(left.height, right.height)


def sd_lockup(img, x, y, size, pal, wordmark=True):
    """Mark plus the serif name treatment, as it would sit on a cover.

    Playfair Black, matching the Field Guide and Quick Sips display face
    rather than FFFA's grotesque: Split Decision inherits its arc's
    palette, so it should inherit the house serif too.
    """
    mw, mh = sd_mark(img, x, y, size, pal)
    d = ImageDraw.Draw(img)
    if not wordmark:
        return mw, mh

    f = core.font("display_black", int(size * 0.46))
    tw = core.text_w(d, "Split Decision", f)
    a, dsc = f.getmetrics()
    cx = x + mw / 2
    ty = y + mh + int(size * 0.16)
    d.text((cx - tw / 2, ty), "Split Decision", font=f, fill=pal["SIGNATURE"])

    ry = ty + a + dsc + int(size * 0.08)
    rw = tw * 0.5
    d.line([(cx - rw / 2, ry), (cx + rw / 2, ry)],
           fill=pal["ACCENT"], width=max(3, int(size * 0.035)))
    return mw, (ry - y)
