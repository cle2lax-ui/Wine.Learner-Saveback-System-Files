"""
Chapter Mind Map -- one landscape page summarising a chapter's full content
as a genuine branching hierarchy (hub -> branch -> sub -> twig), placed as
the closing element of each chapter Mastery Guide, immediately before its
practice test (see mastery.build(..., mindmap=<path>)).

Two prior approaches were tried and rejected before this one:
  1. Organic radial layout, freeform angles, collision-avoidance algorithm --
     looked "haphazard" no matter how well the collision system worked,
     because nothing constrained where a line of text ended.
  2. Grid panels with each sub-branch boxed as its own bordered card -- read
     as "just lists again": modular, but nothing was physically connected.

This engine keeps what worked from both: a strict Vignelli-style grid of
branch panels (fixed-width columns, so every line of text wraps to the same
measure -- nothing can look ragged or overlap, by construction) with a
circular hub in a band between two rows of panels; but the content inside
each panel is drawn as a real branching tree -- a spine dropping from the
header with a tick to each sub-branch, and a shorter secondary spine from
each sub-branch to its own twigs -- so the hierarchy is physically connected
at every level rather than nested boxes of text.

Deliberately reuses the Mastery Guide's own fonts (Serif/Serif-B/Sans/
Sans-B, already registered by importing mastery) and its exact color and
line-weight tokens, so a mind map page reads as part of the same document
family rather than a foreign insert. The one deliberate departure: each
branch keeps its own accent color (from PAL below) for its header rule,
icon, and hub connector, on top of the Mastery Guide's single-accent
convention -- this is a mind-map-specific dual-coding device (color +
icon identify a branch at a glance), not a general style change.
"""
import math
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from mastery import INK, BURGUNDY, GOLD, SLATE, MUTE, HAIRLINE, LINE_HAIR, LINE_RULE, LINE_BOLD

# This page is landscape US Letter, standing apart from the Mastery Guide's
# own portrait page geometry -- deliberately NOT importing PW/PH/MARGIN from
# mastery (those are the guide's portrait dimensions and would silently
# break every layout calculation below if reused here).
PW, PH = 792.0, 612.0
MARGIN = 18.0        # left/right/bottom -- 0.25in
MARGIN_TOP = 36.0    # top -- 0.5in, for 3-hole-punch clearance

F_SERIF, F_SERIF_B = "Serif", "Serif-B"
F_SANS, F_SANS_B = "Sans", "Sans-B"

# Per-branch accent palette -- the mind map's own dual-coding device (see
# module docstring). Eight hues, reused round-robin for chapters with more
# than eight main branches.
PAL = ["#7B2D3B", "#2F5D50", "#8A5A1E", "#33506E", "#6B3A63", "#1F6C71", "#8C3A28", "#4A5340"]


def new_canvas(path, doc_title):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=(PW, PH))
    c.setTitle(doc_title)
    return c

def twrap(text, font, size, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def _ic_thermometer(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.6); c.setFillColor(col)
    c.roundRect(x - r * 0.16, y - r * 0.15, r * 0.32, r * 1.15, r * 0.16, stroke=1, fill=0)
    c.circle(x, y - r * 0.55, r * 0.32, stroke=0, fill=1)
    c.line(x, y - r * 0.15, x, y + r * 0.5)


def _ic_droplet(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.6)
    p = c.beginPath()
    p.moveTo(x, y + r * 0.85)
    p.curveTo(x + r * 0.55, y + r * 0.05, x + r * 0.4, y - r * 0.65, x, y - r * 0.75)
    p.curveTo(x - r * 0.4, y - r * 0.65, x - r * 0.55, y + r * 0.05, x, y + r * 0.85)
    c.drawPath(p, stroke=1, fill=0)


def _ic_sun(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.6)
    c.circle(x, y, r * 0.4, stroke=1, fill=0)
    for i in range(8):
        a = math.radians(i * 45)
        x0, y0 = x + math.cos(a) * r * 0.58, y + math.sin(a) * r * 0.58
        x1, y1 = x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92
        c.line(x0, y0, x1, y1)


def _ic_leaf(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    p = c.beginPath()
    p.moveTo(x, y - r * 0.85)
    p.curveTo(x + r * 0.75, y - r * 0.4, x + r * 0.6, y + r * 0.75, x, y + r * 0.85)
    p.curveTo(x - r * 0.6, y + r * 0.75, x - r * 0.75, y - r * 0.4, x, y - r * 0.85)
    c.drawPath(p, stroke=1, fill=0)
    c.line(x, y - r * 0.75, x, y + r * 0.75)


def _ic_grapes(c, x, y, r, col):
    c.setStrokeColor(col); c.setFillColor(col)
    pts = [(-0.32, 0.5), (0.0, 0.5), (0.32, 0.5),
           (-0.18, 0.18), (0.18, 0.18),
           (-0.32, -0.14), (0.0, -0.14), (0.32, -0.14),
           (-0.18, -0.46), (0.18, -0.46), (0.0, -0.75)]
    for dx, dy in pts:
        c.circle(x + dx * r, y + dy * r, r * 0.16, stroke=0, fill=1)
    c.setLineWidth(1.3)
    c.line(x, y + r * 0.66, x, y + r * 0.95)


def _ic_root(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    c.line(x, y + r * 0.85, x, y - r * 0.1)
    for dx, dy in ((-0.5, -0.75), (-0.15, -0.9), (0.2, -0.85), (0.55, -0.6)):
        c.line(x, y - r * 0.1, x + dx * r, y + dy * r)


def _ic_helix(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.7)
    steps = 16
    pts_a, pts_b = [], []
    for i in range(steps + 1):
        t = i / steps
        yy = y + (t - 0.5) * r * 1.7
        xx = x + math.sin(t * math.pi * 1.4) * r * 0.5
        pts_a.append((xx, yy))
        pts_b.append((x - (xx - x), yy))
    for pts in (pts_a, pts_b):
        p = c.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        c.drawPath(p, stroke=1, fill=0)
    for i in (4, 12):
        c.line(*pts_a[i], *pts_b[i])


def _ic_caliper(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    c.line(x - r * 0.75, y - r * 0.4, x - r * 0.75, y + r * 0.4)
    c.line(x + r * 0.75, y - r * 0.4, x + r * 0.75, y + r * 0.4)
    c.line(x - r * 0.75, y, x + r * 0.75, y)
    for tx in (-0.4, -0.1, 0.2, 0.5):
        c.line(x + tx * r, y, x + tx * r, y - r * 0.22)


def _ic_hourglass(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    c.line(x - r * 0.6, y + r * 0.8, x + r * 0.6, y + r * 0.8)
    c.line(x - r * 0.6, y - r * 0.8, x + r * 0.6, y - r * 0.8)
    p = c.beginPath()
    p.moveTo(x - r * 0.55, y + r * 0.75)
    p.lineTo(x + r * 0.55, y + r * 0.75)
    p.lineTo(x - r * 0.55, y - r * 0.75)
    p.lineTo(x + r * 0.55, y - r * 0.75)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(col)
    c.circle(x, y, r * 0.08, stroke=0, fill=1)


def _ic_recycle(c, x, y, r, col):
    c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(1.5)
    for i in range(3):
        a0 = math.radians(i * 120 - 90)
        a1 = math.radians(i * 120 - 20)
        x0, y0 = x + math.cos(a0) * r * 0.55, y + math.sin(a0) * r * 0.55
        x1, y1 = x + math.cos(a1) * r * 0.55, y + math.sin(a1) * r * 0.55
        mxa, mya = x + math.cos(math.radians(i * 120 - 55)) * r * 0.68, \
                   y + math.sin(math.radians(i * 120 - 55)) * r * 0.68
        p = c.beginPath()
        p.moveTo(x0, y0)
        p.curveTo(mxa, mya, mxa, mya, x1, y1)
        c.drawPath(p, stroke=1, fill=0)
        ang = math.radians(i * 120 - 20)
        ah = 5.5
        p2 = c.beginPath()
        p2.moveTo(x1, y1)
        p2.lineTo(x1 - ah * math.cos(ang - 0.9), y1 - ah * math.sin(ang - 0.9))
        p2.lineTo(x1 - ah * math.cos(ang + 0.4), y1 - ah * math.sin(ang + 0.4))
        p2.close()
        c.drawPath(p2, stroke=0, fill=1)


def _ic_sprout(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    c.line(x - r * 0.55, y - r * 0.7, x + r * 0.55, y - r * 0.7)
    c.line(x, y - r * 0.7, x, y + r * 0.1)

    def _blade(x0, y0, x1, y1, w):
        dx, dy = x1 - x0, y1 - y0
        dist = max(0.001, (dx * dx + dy * dy) ** 0.5)
        nx, ny = -dy / dist, dx / dist
        mx1, my1 = (x0 + x1) / 2.0 + nx * w, (y0 + y1) / 2.0 + ny * w
        mx2, my2 = (x0 + x1) / 2.0 - nx * w, (y0 + y1) / 2.0 - ny * w
        p = c.beginPath()
        p.moveTo(x0, y0)
        p.curveTo(mx1, my1, mx1, my1, x1, y1)
        p.curveTo(mx2, my2, mx2, my2, x0, y0)
        c.drawPath(p, stroke=1, fill=0)

    _blade(x, y + r * 0.1, x - r * 0.55, y + r * 0.75, r * 0.22)
    _blade(x, y + r * 0.1, x + r * 0.55, y + r * 0.75, r * 0.22)


def _ic_moon(c, x, y, r, col):
    c.setFillColor(col)
    c.circle(x, y, r * 0.72, stroke=0, fill=1)
    c.setFillColor(HexColor("#FCFBF9"))
    c.circle(x + r * 0.34, y + r * 0.1, r * 0.62, stroke=0, fill=1)


def _ic_map(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.4)
    p = c.beginPath()
    p.moveTo(x - r * 0.9, y - r * 0.55)
    p.lineTo(x - r * 0.3, y - r * 0.8)
    p.lineTo(x + r * 0.3, y - r * 0.55)
    p.lineTo(x + r * 0.9, y - r * 0.8)
    p.lineTo(x + r * 0.9, y + r * 0.55)
    p.lineTo(x + r * 0.3, y + r * 0.8)
    p.lineTo(x - r * 0.3, y + r * 0.55)
    p.lineTo(x - r * 0.9, y + r * 0.8)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    c.setDash(1.5, 1.5)
    c.line(x - r * 0.3, y - r * 0.8, x - r * 0.3, y + r * 0.55)
    c.line(x + r * 0.3, y - r * 0.55, x + r * 0.3, y + r * 0.8)
    c.setDash()
    c.setFillColor(col)
    c.circle(x + r * 0.05, y + r * 0.05, r * 0.15, stroke=0, fill=1)


def _ic_pin(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    p = c.beginPath()
    p.moveTo(x, y - r * 0.9)
    p.curveTo(x + r * 0.7, y - r * 0.3, x + r * 0.55, y + r * 0.55, x, y + r * 0.9)
    p.curveTo(x - r * 0.55, y + r * 0.55, x - r * 0.7, y - r * 0.3, x, y - r * 0.9)
    c.drawPath(p, stroke=1, fill=0)
    c.circle(x, y - r * 0.1, r * 0.22, stroke=1, fill=0)


def _ic_flask(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    p = c.beginPath()
    p.moveTo(x - r * 0.22, y + r * 0.85)
    p.lineTo(x - r * 0.22, y + r * 0.1)
    p.lineTo(x - r * 0.55, y - r * 0.8)
    p.curveTo(x - r * 0.55, y - r * 0.95, x + r * 0.55, y - r * 0.95, x + r * 0.55, y - r * 0.8)
    p.lineTo(x + r * 0.22, y + r * 0.1)
    p.lineTo(x + r * 0.22, y + r * 0.85)
    c.drawPath(p, stroke=1, fill=0)
    c.line(x - r * 0.32, y + r * 0.85, x + r * 0.32, y + r * 0.85)


def _ic_shield(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    p = c.beginPath()
    p.moveTo(x, y + r * 0.9)
    p.curveTo(x + r * 0.7, y + r * 0.6, x + r * 0.65, y + r * 0.1, x + r * 0.65, y - r * 0.15)
    p.curveTo(x + r * 0.65, y - r * 0.65, x + r * 0.35, y - r * 0.85, x, y - r * 0.95)
    p.curveTo(x - r * 0.35, y - r * 0.85, x - r * 0.65, y - r * 0.65, x - r * 0.65, y - r * 0.15)
    p.curveTo(x - r * 0.65, y + r * 0.1, x - r * 0.7, y + r * 0.6, x, y + r * 0.9)
    c.drawPath(p, stroke=1, fill=0)


def _ic_gear(c, x, y, r, col):
    c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(1.2)
    c.circle(x, y, r * 0.32, stroke=1, fill=0)
    for i in range(8):
        a = math.radians(i * 45)
        cx0, cy0 = x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.5
        w, h = r * 0.22, r * 0.22
        c.saveState()
        c.translate(cx0, cy0)
        c.rotate(math.degrees(a))
        c.rect(-w / 2.0, -h / 2.0, w, h, stroke=0, fill=1)
        c.restoreState()


def _ic_soil(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.4)
    for i, dy in enumerate((-0.55, -0.1, 0.35)):
        c.roundRect(x - r * 0.75, y + dy * r, r * 1.5, r * 0.32, r * 0.05, stroke=1, fill=0)


def _ic_vine(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.8)
    p = c.beginPath()
    p.moveTo(x, y - r * 0.95)
    p.curveTo(x + r * 0.5, y - r * 0.25, x - r * 0.5, y + r * 0.25, x, y + r * 0.95)
    c.drawPath(p, stroke=1, fill=0)
    for sx, sy in ((-0.42, -0.05), (0.42, 0.45)):
        c.setFillColor(col)
        p2 = c.beginPath()
        p2.moveTo(x + sx * r, y + sy * r - r * 0.32)
        p2.curveTo(x + sx * r + r * 0.32, y + sy * r, x + sx * r + r * 0.2, y + sy * r + r * 0.32,
                   x + sx * r, y + sy * r + r * 0.32)
        p2.curveTo(x + sx * r - r * 0.2, y + sy * r + r * 0.32, x + sx * r - r * 0.32, y + sy * r,
                   x + sx * r, y + sy * r - r * 0.32)
        c.drawPath(p2, stroke=0, fill=1)


def _ic_calendar(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.4)
    c.roundRect(x - r * 0.75, y - r * 0.65, r * 1.5, r * 1.3, r * 0.1, stroke=1, fill=0)
    c.line(x - r * 0.75, y + r * 0.2, x + r * 0.75, y + r * 0.2)
    c.line(x - r * 0.35, y - r * 0.85, x - r * 0.35, y - r * 0.55)
    c.line(x + r * 0.35, y - r * 0.85, x + r * 0.35, y - r * 0.55)


def _ic_scale(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.4)
    c.line(x, y - r * 0.85, x, y + r * 0.75)
    c.line(x - r * 0.6, y + r * 0.75, x + r * 0.6, y + r * 0.75)
    c.line(x - r * 0.65, y - r * 0.4, x + r * 0.65, y - r * 0.4)
    for dx in (-0.65, 0.65):
        c.line(x + dx * r, y - r * 0.4, x + dx * r - r * 0.22, y + r * 0.05)
        c.line(x + dx * r, y - r * 0.4, x + dx * r + r * 0.22, y + r * 0.05)
        c.ellipse(x + dx * r - r * 0.22, y - r * 0.02, x + dx * r + r * 0.22, y + r * 0.12, stroke=1, fill=0)


def _ic_mountain(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.6)
    p = c.beginPath()
    p.moveTo(x - r * 0.9, y - r * 0.6)
    p.lineTo(x - r * 0.4, y + r * 0.75)
    p.lineTo(x - r * 0.05, y + r * 0.3)
    p.lineTo(x + r * 0.35, y + r * 0.6)
    p.lineTo(x + r * 0.9, y - r * 0.6)
    c.drawPath(p, stroke=1, fill=0)
    c.line(x - r * 0.56, y + r * 0.32, x - r * 0.32, y + r * 0.55)
    c.line(x + r * 0.2, y + r * 0.42, x + r * 0.35, y + r * 0.6)


def _ic_wind(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.6)
    for dy, ext in ((0.35, 0.5), (0.0, 0.85), (-0.35, 0.35)):
        p = c.beginPath()
        p.moveTo(x - r * 0.85, y + dy * r)
        p.curveTo(x, y + dy * r - r * 0.25, x + r * ext, y + dy * r + r * 0.25, x + r * ext, y + dy * r)
        c.drawPath(p, stroke=1, fill=0)


def _ic_clock(c, x, y, r, col):
    c.setStrokeColor(col); c.setLineWidth(1.5)
    c.circle(x, y, r * 0.8, stroke=1, fill=0)
    c.line(x, y, x, y + r * 0.45)
    c.line(x, y, x + r * 0.35, y - r * 0.1)


ICONS = {
    "thermometer": _ic_thermometer, "droplet": _ic_droplet, "sun": _ic_sun,
    "leaf": _ic_leaf, "grapes": _ic_grapes, "root": _ic_root, "helix": _ic_helix,
    "pin": _ic_pin, "flask": _ic_flask, "shield": _ic_shield, "gear": _ic_gear,
    "soil": _ic_soil, "vine": _ic_vine, "calendar": _ic_calendar,
    "scale": _ic_scale, "clock": _ic_clock, "mountain": _ic_mountain, "wind": _ic_wind, "map": _ic_map,
    "caliper": _ic_caliper, "hourglass": _ic_hourglass, "recycle": _ic_recycle, "sprout": _ic_sprout,
    "moon": _ic_moon,
}


def draw_icon(c, name, x, y, r, color):
    fn = ICONS.get(name)
    if fn:
        fn(c, x, y, r, HexColor(color) if isinstance(color, str) else color)

class Node:
    def __init__(self, label, children=None, icon=None):
        self.label = label            # short keyword / phrase -- NOT a sentence
        self.children = children or []
        self.icon = icon
        self.color = None
        self.x = self.y = 0.0
        self.angle = 0.0


def tint(hexcol, f):
    c = hexcol if hasattr(hexcol, "red") else HexColor(hexcol)
    return Color(c.red + (1 - c.red) * f, c.green + (1 - c.green) * f, c.blue + (1 - c.blue) * f)


def _measure_tree(branch, inner_w, scale=1.0):
    """Pre-measure the whole sub/twig tree for this branch so the main
    spine can be drawn as one continuous line before the ticks and text
    are drawn on top of it -- and so content height stays flexible to any
    number of subs/twigs rather than a fixed template. `scale` shrinks
    font size and line-height uniformly, which is how a branch with far
    more content than its neighbours still fits: the grid no longer caps
    how many subs/twigs a branch may have, it just measures what's
    actually there and the page-level fit pass (see build_grid_page)
    finds the one scale that makes every panel fit simultaneously."""
    sub_size, twig_size = 7.8 * scale, 7.4 * scale
    sub_lh, twig_lh = 9.6 * scale, 9.0 * scale
    sub_x_offset = 13
    twig_x_offset = 12
    sub_text_w = inner_w - sub_x_offset - 4
    twig_text_w = inner_w - sub_x_offset - twig_x_offset - 4
    items = []  # (kind, lines, font, size, lh)
    for sub in branch.children:
        sub_lines = twrap(sub.label.upper(), F_SANS_B, sub_size, sub_text_w)
        items.append(("sub", sub_lines, F_SANS_B, sub_size, sub_lh))
        for twig in sub.children:
            twig_lines = twrap("\u2013 " + twig.label, F_SANS, twig_size, twig_text_w)
            items.append(("twig", twig_lines, F_SANS, twig_size, twig_lh))
    h = 0.0
    for kind, lines, font, size, lh in items:
        h += lh * len(lines)
        h += (2.0 if kind == "sub" else 1.2) * scale
    return items, h


def _draw_tree(c, x, y_top, inner_w, branch, color, scale=1.0):
    """Draw the branch's sub/twig content as an actual connected tree --
    a spine dropping from the header with a tick to each sub-branch, and
    a shorter secondary spine + tick from each sub down to its own
    twigs -- rather than nesting them as text inside boxes. This is what
    keeps it reading as a mind map (hub -> branch -> sub -> twig, all
    physically connected) instead of a list."""
    sub_x = x + 13
    twig_x = sub_x + 12
    items, _ = _measure_tree(branch, inner_w, scale)

    # Phase 1: figure out where every tick lands, without drawing yet
    ty = y_top
    sub_ticks = []   # y of each sub's first line (spine attaches here)
    twig_ticks = []  # (y, parent_sub_x) for each twig's first line
    layout = []      # (kind, lines, font, size, lh, y_start)
    for kind, lines, font, size, lh in items:
        y_start = ty
        layout.append((kind, lines, font, size, lh, y_start))
        if kind == "sub":
            sub_ticks.append(y_start - size * 0.78)
        else:
            twig_ticks.append(y_start - size * 0.78)
        ty -= lh * len(lines)
        ty -= (2.0 if kind == "sub" else 1.2) * scale

    # Phase 2: main spine, from the header down to the last tick of all
    if sub_ticks:
        c.setStrokeColor(tint(color, 0.35))
        c.setLineWidth(LINE_RULE)
        c.line(sub_x, y_top + 6, sub_x, min(sub_ticks + twig_ticks) if twig_ticks else sub_ticks[-1])

    # Phase 3: per-sub secondary spine (covers just that sub's own twigs)
    i = 0
    cur_sub_top = None
    while i < len(layout):
        kind, lines, font, size, lh, y_start = layout[i]
        if kind == "sub":
            cur_sub_top = y_start - size * 0.78
            j = i + 1
            twig_bottoms = []
            while j < len(layout) and layout[j][0] == "twig":
                twig_bottoms.append(layout[j][5] - layout[j][3] * 0.78)
                j += 1
            if twig_bottoms:
                c.setStrokeColor(tint(color, 0.55))
                c.setLineWidth(LINE_HAIR)
                c.line(twig_x - 6, cur_sub_top, twig_x - 6, twig_bottoms[-1])
        i += 1

    # Phase 4: ticks + text on top
    for kind, lines, font, size, lh, y_start in layout:
        if kind == "sub":
            tick_y = y_start - size * 0.78
            c.setStrokeColor(tint(color, 0.35))
            c.setLineWidth(LINE_RULE)
            c.line(sub_x, tick_y, sub_x + 8, tick_y)
            c.setFillColor(color if hasattr(color, "red") else HexColor(color))
            c.circle(sub_x, tick_y, 1.6, stroke=0, fill=1)
            c.setFont(font, size)
            c.setFillColor(GOLD)
            ty2 = y_start
            for ln in lines:
                c.drawString(sub_x + 12, ty2 - size * 0.85, ln)
                ty2 -= lh
        else:
            tick_y = y_start - size * 0.78
            c.setStrokeColor(tint(color, 0.55))
            c.setLineWidth(LINE_HAIR)
            c.line(twig_x - 6, tick_y, twig_x, tick_y)
            c.setFont(font, size)
            c.setFillColor(INK)
            ty2 = y_start
            for k, ln in enumerate(lines):
                c.drawString(twig_x + 3 + (0 if k == 0 else 4), ty2 - size * 0.85, ln)
                ty2 -= lh

    _, total_h = _measure_tree(branch, inner_w, scale)
    return y_top - total_h


def _draw_branch_cell(c, x, y, w, h, branch, connector_side, scale=1.0):
    """Rule-only, Swiss-table header (colored top rule + hairline under
    the icon/name) with the sub/twig content below rendered as a real
    branching tree via _draw_tree, so the hierarchy is physically
    connected -- hub to branch to sub to twig -- rather than nested
    boxes of text."""
    color = branch.color
    pad = 9

    c.setStrokeColor(HexColor(color))
    c.setLineWidth(LINE_BOLD)
    c.line(x, y + h, x + w, y + h)

    icon_r = 10.0
    icon_cx, icon_cy = x + pad + icon_r, y + h - pad - icon_r - 2
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(LINE_HAIR)
    c.circle(icon_cx, icon_cy, icon_r + 2, stroke=1, fill=0)
    if branch.icon:
        draw_icon(c, branch.icon, icon_cx, icon_cy, icon_r, HexColor(color))

    c.setFont(F_SERIF_B, 11.5)
    c.setFillColor(HexColor(color))
    header_y = y + h - pad - icon_r - 6
    c.drawString(x + pad + icon_r * 2 + 8, header_y, branch.label)

    rule_y = y + h - pad * 2 - icon_r * 2 - 2
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(LINE_RULE)
    c.line(x, rule_y, x + w, rule_y)

    inner_w = w - 2 * pad
    ty_end = _draw_tree(c, x + pad, rule_y - 10, inner_w, branch, color, scale)

    if connector_side == "bottom":
        # this panel's content stacks downward from the header, same
        # direction as this connector -- if a branch has enough subs to
        # nearly fill the row, the nominal panel edge can coincide with
        # (or sit just above) the last block's own bottom edge, putting
        # the connector line's start right through that block's text.
        # Guarantee real clearance from the actual content, not just the
        # nominal row boundary.
        return (x + w / 2.0, min(y, ty_end - 10))
    else:
        return (x + w / 2.0, y + h)


def draw_inset(c, x, y, w, inset_title, items):
    """Numbered-chain inset for genuine sequence/chronology content --
    styled to match the Mastery Guide's caption/rule conventions."""
    n = len(items)
    pad = 8
    h = pad * 2 + 12 + 34
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(LINE_RULE)
    c.line(x, y, x + w, y)
    c.line(x, y - h, x + w, y - h)
    c.setFont(F_SANS_B, 7.6)
    c.setFillColor(GOLD)
    c.drawString(x, y - pad - 7, inset_title.upper())

    avail = w - 0
    step = avail / max(1, n - 1) if n > 1 else 0
    row_y = y - pad - 22
    for i, label in enumerate(items):
        ix = x + step * i if n > 1 else x + w / 2.0
        c.setFillColor(BURGUNDY)
        c.circle(ix, row_y, 6.2, stroke=0, fill=1)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont(F_SANS_B, 6.2)
        c.drawCentredString(ix, row_y - 2.2, str(i + 1))
        if i < n - 1:
            c.setStrokeColor(MUTE)
            c.setLineWidth(LINE_HAIR)
            ax0, ax1 = ix + 7.2, ix + step - 7.2
            c.line(ax0, row_y, ax1, row_y)
        c.setFont(F_SANS, 6.2)
        c.setFillColor(SLATE)
        maxw_lbl = step - 4 if n > 1 else avail
        label_lines = twrap(label, F_SANS, 6.2, maxw_lbl)
        # the first and last items' circles sit exactly on the inset's own
        # left/right edge -- centering their labels on the circle (as the
        # middle items do) lets half the text run past the inset's own
        # bounding box and off the page. Anchor those two to the inside
        # edge instead; only the interior items stay centered.
        if n > 1 and i == 0:
            for k, ln in enumerate(label_lines):
                c.drawString(ix, row_y - 15 - k * 7, ln)
        elif n > 1 and i == n - 1:
            for k, ln in enumerate(label_lines):
                c.drawRightString(ix, row_y - 15 - k * 7, ln)
        else:
            for k, ln in enumerate(label_lines):
                c.drawCentredString(ix, row_y - 15 - k * 7, ln)


def draw_spectrum_inset(c, x, y, w, inset_title, items, color_lo="#4E6E8C", color_hi="#A6462F"):
    """Un-numbered, arrow-free colour-graded bar for genuinely ordered
    content that is a continuum rather than a sequence of steps. Uses the
    Mastery Guide's own COOL->HOT ramp endpoints by default."""
    n = len(items)
    pad = 8
    bar_h = 8
    h = pad * 2 + 12 + 10 + bar_h + 14
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(LINE_RULE)
    c.line(x, y, x + w, y)
    c.line(x, y - h, x + w, y - h)
    c.setFont(F_SANS_B, 7.6)
    c.setFillColor(GOLD)
    c.drawString(x, y - pad - 7, inset_title.upper())

    bar_x0, bar_x1 = x, x + w
    bar_top = y - pad - 20
    lo, hi = HexColor(color_lo), HexColor(color_hi)
    strips = 60
    sw = (bar_x1 - bar_x0) / strips
    for s in range(strips):
        t = s / (strips - 1)
        col = Color(lo.red + (hi.red - lo.red) * t, lo.green + (hi.green - lo.green) * t,
                    lo.blue + (hi.blue - lo.blue) * t)
        c.setFillColor(col)
        c.rect(bar_x0 + s * sw, bar_top - bar_h, sw + 0.5, bar_h, stroke=0, fill=1)

    avail = bar_x1 - bar_x0
    step = avail / max(1, n - 1) if n > 1 else 0
    for i, label in enumerate(items):
        ix = bar_x0 + step * i if n > 1 else (bar_x0 + bar_x1) / 2.0
        c.setStrokeColor(HexColor("#FFFFFF"))
        c.setLineWidth(1.2)
        c.line(ix, bar_top - bar_h - 1, ix, bar_top + 1)
        c.setFont(F_SANS, 6.2)
        c.setFillColor(SLATE)
        maxw_lbl = step - 4 if n > 1 else avail
        label_lines = twrap(label, F_SANS, 6.2, maxw_lbl)
        if n > 1 and i == 0:
            for k, ln in enumerate(label_lines):
                c.drawString(ix, bar_top - bar_h - 12 - k * 7, ln)
        elif n > 1 and i == n - 1:
            for k, ln in enumerate(label_lines):
                c.drawRightString(ix, bar_top - bar_h - 12 - k * 7, ln)
        else:
            for k, ln in enumerate(label_lines):
                c.drawCentredString(ix, bar_top - bar_h - 12 - k * 7, ln)


def draw_inset_vertical(c, x, y_top, y_bottom, w, inset_title, items):
    """Same numbered-chain device as draw_inset, rotated to run top-to-
    bottom down a side column instead of left-to-right along a strip --
    for a chapter where the horizontal strip would compete with branch
    panels for height, but there's an unused side column to use instead."""
    n = len(items)
    pad = 6
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(LINE_RULE)
    c.line(x, y_top, x + w, y_top)
    c.setFont(F_SANS_B, 7.2)
    c.setFillColor(GOLD)
    for k, ln in enumerate(twrap(inset_title.upper(), F_SANS_B, 7.2, w)):
        c.drawString(x, y_top - pad - 7 - k * 8.6, ln)
    title_lines = len(twrap(inset_title.upper(), F_SANS_B, 7.2, w))
    chain_top = y_top - pad - 10 - title_lines * 8.6

    avail = chain_top - y_bottom - pad
    step = avail / max(1, n - 1) if n > 1 else 0
    cx = x + 8
    for i, label in enumerate(items):
        iy = chain_top - step * i if n > 1 else (chain_top + y_bottom) / 2.0
        c.setFillColor(BURGUNDY)
        c.circle(cx, iy, 6.2, stroke=0, fill=1)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setFont(F_SANS_B, 6.2)
        c.drawCentredString(cx, iy - 2.2, str(i + 1))
        if i < n - 1:
            c.setStrokeColor(MUTE)
            c.setLineWidth(LINE_HAIR)
            c.line(cx, iy - 7.2, cx, iy - step + 7.2)
        c.setFont(F_SANS, 6.4)
        c.setFillColor(SLATE)
        for k, ln in enumerate(twrap(label, F_SANS, 6.4, w - 18)):
            c.drawString(cx + 12, iy + 2 - k * 7, ln)
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(LINE_RULE)
    c.line(x, y_bottom, x + w, y_bottom)


def build_grid_page(c, title, subtitle, hub_label, hub_icon, main_branches,
                     footer="", cross_links=None, colors=None, inset=None):
    cols = colors or PAL
    n = len(main_branches)
    for i, b in enumerate(main_branches):
        b.color = cols[i % len(cols)]

    full_title = f"{title} \u2014 Content Mind Map Summary"
    c.setFillColor(INK)
    c.setFont(F_SERIF_B, 14.5)
    c.drawString(MARGIN, PH - MARGIN_TOP - 10, full_title)
    c.setFont(F_SANS, 8.4)
    c.setFillColor(SLATE)
    c.drawRightString(PW - MARGIN, PH - MARGIN_TOP - 10, subtitle)
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(LINE_RULE)
    c.line(MARGIN, PH - MARGIN_TOP - 17, PW - MARGIN, PH - MARGIN_TOP - 17)

    top_n = math.ceil(n / 2.0)
    bot_n = n - top_n
    ncols = max(top_n, bot_n)

    # hub size must be known before the rows are laid out -- hub_band_h
    # used to be a flat constant, which wasted row height on every chapter
    # whose hub label is short (most of them) at the expense of chapters
    # with content-dense branches that need every point of row height
    hub_lines_preview = twrap(hub_label.title(), F_SERIF_B, 13.0, 92)
    widest = max(pdfmetrics.stringWidth(ln, F_SERIF_B, 13.0) for ln in hub_lines_preview)
    hub_r = max(36 if len(hub_lines_preview) <= 1 else (44 if len(hub_lines_preview) == 2 else 52),
                widest / 2.0 + 12)
    hub_band_h = 2 * hub_r + 34.0

    content_top = PH - MARGIN_TOP - 30
    content_bottom = MARGIN + 10
    available_total = content_top - content_bottom

    usable_w = PW - 2 * MARGIN
    col_w = usable_w / ncols
    gutter = 14.0
    cell_w = col_w - gutter

    # Insets get a real placement choice rather than always being a
    # horizontal strip that steals height from whichever row is nearest:
    #   "stacked" (default) -- its own zone in the vertical stack, sized
    #       to its own content, competing for space on equal terms with
    #       every branch panel rather than being special-cased
    #   "side"   -- a vertical chain in unused width (only available when
    #       the two rows have different branch counts, leaving a gap)
    #   "block"  -- placed beside the hub, enlarging the hub band instead
    #       of taking a vertical slot of its own
    inset_mode = (inset or {}).get("placement", "stacked")
    inset_stack_h = 0.0
    inset_side_w = 0.0
    if inset and inset_mode == "stacked":
        inset_stack_h = (72.0 if inset.get("kind") == "spectrum" else 68.0) + 12.0
    elif inset and inset_mode == "side" and top_n != bot_n:
        inset_side_w = inset.get("w", 130) + 20.0
    elif inset and inset_mode == "block":
        block_h = inset.get("block_h", 130.0)
        hub_band_h = max(hub_band_h, block_h)

    if inset_side_w:
        usable_w -= inset_side_w
        col_w = usable_w / ncols
        cell_w = col_w - gutter

    icon_r = 10.0
    header_overhead = 9 * 2 + icon_r * 2 + 2 + 10  # pad*2 + icon + rule gaps + tree start offset

    def zone_natural_h(branches, scale):
        tallest = 0.0
        for b in branches:
            _, th = _measure_tree(b, cell_w - 18, scale)
            tallest = max(tallest, header_overhead + th)
        return tallest

    top_branches = main_branches[:top_n]
    bot_branches = main_branches[top_n:]

    # find the largest scale (<=1.0) at which every zone's tallest branch
    # fits in the space actually available -- this is what removes the
    # fixed "4 subs max" ceiling: a branch may carry as many subs/twigs as
    # its content needs, and the page compresses uniformly to make room,
    # rather than an arbitrary per-branch cap that has nothing to do with
    # how much the page can actually hold
    scale = 1.0
    for _ in range(40):
        top_h = zone_natural_h(top_branches, scale)
        bot_h = zone_natural_h(bot_branches, scale)
        needed = inset_stack_h + top_h + hub_band_h + bot_h
        if needed <= available_total or scale <= 0.72:
            break
        scale -= 0.02
    scale = max(0.72, scale)

    top_row_h = zone_natural_h(top_branches, scale)
    bot_row_h = zone_natural_h(bot_branches, scale)

    bot_row_y = content_bottom
    top_row_y = content_bottom + bot_row_h + hub_band_h

    x0 = MARGIN + inset_side_w
    connectors = []
    edge_points = [None] * n
    for i, b in enumerate(top_branches):
        cell_x = x0 + (usable_w - top_n * col_w) / 2.0 + i * col_w + gutter / 2.0
        pt = _draw_branch_cell(c, cell_x, top_row_y, cell_w, top_row_h, b, "bottom", scale)
        connectors.append((pt, b.color))
        edge_points[i] = ("bottom", pt)
    for i, b in enumerate(bot_branches):
        cell_x = x0 + (usable_w - bot_n * col_w) / 2.0 + i * col_w + gutter / 2.0
        pt = _draw_branch_cell(c, cell_x, bot_row_y, cell_w, bot_row_h, b, "top", scale)
        connectors.append((pt, b.color))
        edge_points[top_n + i] = ("top", pt)

    hub_cy = content_bottom + bot_row_h + hub_band_h / 2.0
    hub_cx = x0 + usable_w / 2.0

    for (px, py), color in connectors:
        c.setStrokeColor(tint(color, 0.3))
        c.setLineWidth(LINE_RULE)
        dx, dy = hub_cx - px, hub_cy - py
        dist = max(1.0, (dx * dx + dy * dy) ** 0.5)
        ux, uy = dx / dist, dy / dist
        hx, hy = hub_cx - ux * hub_r, hub_cy - uy * hub_r
        c.line(px, py, hx, hy)
        c.setFillColor(HexColor(color))
        c.circle(px, py, 2.0, stroke=0, fill=1)

    c.setFillColor(HexColor("#FFFFFF"))
    c.setStrokeColor(INK)
    c.setLineWidth(LINE_BOLD)
    c.circle(hub_cx, hub_cy, hub_r, stroke=1, fill=1)
    icon_cy = hub_cy + hub_r * 0.34
    icon_rad = 14 if hub_r <= 44 else 12
    if hub_icon:
        draw_icon(c, hub_icon, hub_cx, icon_cy, icon_rad, BURGUNDY)
    c.setFillColor(BURGUNDY)
    ty = icon_cy - icon_rad - 11
    for ln_txt in hub_lines_preview:
        c.setFont(F_SERIF_B, 13.0)
        c.drawCentredString(hub_cx, ty, ln_txt)
        ty -= 15.5

    if cross_links:
        c.setDash(3, 3)
        c.setLineWidth(LINE_HAIR)
        cross_row_k = 0
        for i, j, label in cross_links:
            side_a, (ax, ay) = edge_points[i]
            side_b, (bx, by) = edge_points[j]
            mx = (ax + bx) / 2.0
            near_hub = False
            if side_a == side_b:
                bulge = 58.0
                cyo_a = ay + (bulge if side_a == "top" else -bulge)
                cyo_b = by + (bulge if side_b == "top" else -bulge)
                my = (cyo_a + cyo_b) / 2.0
                near_hub = ((mx - hub_cx) ** 2 + (my - hub_cy) ** 2) ** 0.5 < hub_r + 24
            if side_a != side_b:
                # genuine cross-row link (top-to-bottom): a symmetric bulge
                # toward each other always collapses onto the hub no matter
                # the magnitude, so route this one over the top of the
                # whole grid instead, staggered so multiple such links
                # don't stack on each other
                lvl = top_row_y + top_row_h + 20 + cross_row_k * 13
                cyo_a = cyo_b = my = lvl
                cross_row_k += 1
            elif near_hub:
                # a same-row link whose natural bulge midpoint lands on/near
                # the hub (e.g. a symmetric pair in an even-numbered row --
                # first+last or middle-two both average to the exact row
                # center, which is also the hub's x-position). Shift the
                # midpoint sideways to clear the hub rather than relocating
                # it vertically: there's frequently no safe vertical room to
                # relocate to (the bottom row already sits at the page's
                # bottom margin; the top row may have an inset above it).
                # The shift has to clear the hub by the label's own half-
                # width too, not just place the anchor point outside the
                # hub -- a long label centered on a barely-cleared anchor
                # still reaches back into the circle.
                label_tw = pdfmetrics.stringWidth(label or "", F_SANS, 6.6) if label else 0.0
                shift = hub_r + label_tw / 2.0 + 24 + (cross_row_k // 2) * 22
                mx = hub_cx - shift if cross_row_k % 2 == 0 else hub_cx + shift
                cross_row_k += 1
            c.setStrokeColor(MUTE)
            p = c.beginPath()
            p.moveTo(ax, ay)
            p.curveTo(ax, cyo_a, mx, my, mx, my)
            c.drawPath(p)
            p2 = c.beginPath()
            p2.moveTo(mx, my)
            p2.curveTo(mx, my, bx, cyo_b, bx, by)
            c.drawPath(p2)
            c.setDash()
            if label:
                c.setFont(F_SANS, 6.6)
                tw = pdfmetrics.stringWidth(label, F_SANS, 6.6)
                c.setFillColor(HexColor("#FFFFFF"))
                c.setStrokeColor(HAIRLINE)
                c.setLineWidth(LINE_HAIR)
                c.roundRect(mx - tw / 2.0 - 3, my - 5, tw + 6, 10, 2, stroke=1, fill=1)
                c.setFillColor(SLATE)
                c.drawCentredString(mx, my - 2, label)
            c.setDash(3, 3)
        c.setDash()

    if inset:
        if inset_mode == "side":
            draw_inset_vertical(c, MARGIN, content_top, content_bottom,
                                 inset_side_w - 20, inset["title"], inset["items"])
        elif inset_mode == "block":
            block_w = inset.get("w", 190)
            block_x = MARGIN
            block_y = hub_cy + hub_band_h / 2.0
            if inset.get("kind") == "spectrum":
                draw_spectrum_inset(c, block_x, block_y, block_w, inset["title"], inset["items"],
                                     color_lo=inset.get("color_lo", "#4E6E8C"),
                                     color_hi=inset.get("color_hi", "#A6462F"))
            else:
                draw_inset(c, block_x, block_y, block_w, inset["title"], inset["items"])
        else:
            inset_x = MARGIN
            inset_y = content_top
            inset_w = inset.get("w", 220)
            if inset.get("kind") == "spectrum":
                draw_spectrum_inset(c, inset_x, inset_y, inset_w, inset["title"], inset["items"],
                                     color_lo=inset.get("color_lo", "#4E6E8C"),
                                     color_hi=inset.get("color_hi", "#A6462F"))
            else:
                draw_inset(c, inset_x, inset_y, inset_w, inset["title"], inset["items"])

    if footer:
        c.setFont(F_SANS, 6.8)
        c.setFillColor(MUTE)
        c.drawCentredString(PW / 2.0, MARGIN - 6, footer)
    c.showPage()


def build_cycle_page(c, title, subtitle, hub_label, hub_icon, stages, cross_links=None, footer=""):
    """The vine growth cycle is a loop, not a category tree, so it keeps its
    wheel-of-cards structure -- restyled here with the same fonts, palette,
    and line weights as the grid pages so the whole set reads as one family."""
    n = len(stages)
    cols = PAL

    full_title = f"{title} \u2014 Content Mind Map Summary"
    c.setFillColor(INK)
    c.setFont(F_SERIF_B, 14.5)
    c.drawString(MARGIN, PH - MARGIN_TOP - 10, full_title)
    c.setFont(F_SANS, 8.4)
    c.setFillColor(SLATE)
    c.drawRightString(PW - MARGIN, PH - MARGIN_TOP - 10, subtitle)
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(LINE_RULE)
    c.line(MARGIN, PH - MARGIN_TOP - 17, PW - MARGIN, PH - MARGIN_TOP - 17)

    cx, cy = PW / 2.0, (PH - MARGIN_TOP - MARGIN) / 2.0 + MARGIN
    Rx, Ry = 340.0, 226.0
    card_w = 220.0

    positions = []
    for i in range(n):
        a = math.radians(90 - i * (360.0 / n))
        x = cx + math.cos(a) * Rx
        y = cy + math.sin(a) * Ry
        positions.append((x, y, a))

    cards = []
    for i, st in enumerate(stages):
        col = cols[i % len(cols)]
        font_s, size_s = F_SANS, 7.6
        lines = [("head", st["name"], F_SERIF_B, 10.0)]
        lines.append(("timing", st["timing"], F_SANS, 7.4))
        lines.append(("needs", "+ " + st["needs"], font_s, size_s))
        lines.append(("risk", "\u2013 " + st["risk"], font_s, size_s))
        for bl in st["bullets"]:
            for k, wl in enumerate(twrap(bl, font_s, size_s, card_w - 20)):
                lines.append(("bullet" if k == 0 else "bulletc", ("\u2022 " if k == 0 else "  ") + wl, font_s, size_s))
        h = 14
        for kind, txt, fnt, sz in lines:
            h += sz * 1.35
        cards.append(dict(color=col, lines=lines, h=h, x=positions[i][0], y=positions[i][1],
                           angle=positions[i][2], icon=st["icon"]))

    c.setLineWidth(1.6)
    for i in range(n):
        a, b = cards[i], cards[(i + 1) % n]
        loop = (i == n - 1)
        col = tint(a["color"], 0.2) if not loop else MUTE
        c.setStrokeColor(col)
        if loop:
            c.setDash(4, 3)
        mx = cx + (a["x"] + b["x"] - 2 * cx) * 0.58
        my = cy + (a["y"] + b["y"] - 2 * cy) * 0.58
        p = c.beginPath()
        p.moveTo(a["x"], a["y"])
        p.curveTo(mx, my, mx, my, b["x"], b["y"])
        c.drawPath(p)
        ang = math.atan2(b["y"] - my, b["x"] - mx)
        ah = 6.0
        hx, hy = b["x"] - 34 * math.cos(ang), b["y"] - 34 * math.sin(ang)
        c.setFillColor(col)
        p2 = c.beginPath()
        p2.moveTo(hx, hy)
        p2.lineTo(hx - ah * math.cos(ang - 0.4), hy - ah * math.sin(ang - 0.4))
        p2.lineTo(hx - ah * math.cos(ang + 0.4), hy - ah * math.sin(ang + 0.4))
        p2.close()
        c.drawPath(p2, stroke=0, fill=1)
        if loop:
            c.setDash()

    c.setLineWidth(LINE_HAIR)
    for card in cards:
        c.setStrokeColor(tint(card["color"], 0.68))
        c.line(cx, cy, card["x"], card["y"])

    hub_lines = twrap(hub_label.title(), F_SERIF_B, 13.0, 92)
    hub_widest = max(pdfmetrics.stringWidth(ln, F_SERIF_B, 13.0) for ln in hub_lines)
    hub_r = max(38, 30 if len(hub_lines) <= 1 else 44, hub_widest / 2.0 + 12)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setStrokeColor(INK)
    c.setLineWidth(LINE_BOLD)
    c.circle(cx, cy, hub_r, stroke=1, fill=1)
    icon_cy = cy + hub_r * 0.13
    icon_rad = 14 if hub_r <= 44 else 12
    if hub_icon:
        draw_icon(c, hub_icon, cx, icon_cy, icon_rad, BURGUNDY)
    c.setFillColor(BURGUNDY)
    ty = icon_cy - icon_rad - 11
    for ln_txt in hub_lines:
        c.setFont(F_SERIF_B, 13.0)
        c.drawCentredString(cx, ty, ln_txt)
        ty -= 15.5

    for card in cards:
        left = max(MARGIN, min(card["x"] - card_w / 2.0, PW - MARGIN - card_w))
        top = min(card["y"] + card["h"] / 2.0, PH - MARGIN_TOP - 26)
        top = max(top, MARGIN + card["h"] + 4)
        c.setFillColor(HexColor("#FFFFFF"))
        c.setStrokeColor(HAIRLINE)
        c.setLineWidth(LINE_HAIR)
        c.roundRect(left, top - card["h"], card_w, card["h"], 5, stroke=1, fill=1)
        c.setStrokeColor(HexColor(card["color"]))
        c.setLineWidth(LINE_BOLD)
        c.line(left, top, left + card_w, top)
        ir = 10.5
        c.setStrokeColor(HAIRLINE)
        c.setLineWidth(LINE_HAIR)
        c.setFillColor(HexColor("#FFFFFF"))
        c.circle(left + card_w - ir - 8, top - ir - 9, ir + 2, stroke=1, fill=1)
        if card["icon"]:
            draw_icon(c, card["icon"], left + card_w - ir - 8, top - ir - 9, ir, HexColor(card["color"]))
        y = top - 10
        for kind, txt, fnt, sz in card["lines"]:
            c.setFont(fnt, sz)
            if kind == "head":
                c.setFillColor(HexColor(card["color"]))
            elif kind == "timing":
                c.setFillColor(SLATE)
            elif kind == "needs":
                c.setFillColor(HexColor("#3D6B4F"))
            elif kind == "risk":
                c.setFillColor(HexColor("#93412B"))
            else:
                c.setFillColor(INK)
            c.drawString(left + 8, y - sz, txt)
            y -= sz * 1.35

    if cross_links:
        c.setDash(3, 3)
        c.setLineWidth(LINE_HAIR)
        pulls = [0.24, 0.34, 0.44, 0.20, 0.40]
        for k, (i, j, label) in enumerate(cross_links):
            a, b = cards[i], cards[j]
            c.setStrokeColor(MUTE)
            mx, my = (a["x"] + b["x"]) / 2.0, (a["y"] + b["y"]) / 2.0
            pull = pulls[k % len(pulls)]
            cxo = cx + (mx - cx) * pull
            cyo = cy + (my - cy) * pull
            p = c.beginPath()
            p.moveTo(a["x"], a["y"])
            p.curveTo(cxo, cyo, cxo, cyo, b["x"], b["y"])
            c.drawPath(p)
            c.setDash()
            if label:
                c.setFont(F_SANS, 6.6)
                tw = pdfmetrics.stringWidth(label, F_SANS, 6.6)
                c.setFillColor(HexColor("#FFFFFF"))
                c.setStrokeColor(HAIRLINE)
                c.setLineWidth(LINE_HAIR)
                c.roundRect(cxo - tw / 2.0 - 3, cyo - 5, tw + 6, 10, 2, stroke=1, fill=1)
                c.setFillColor(SLATE)
                c.drawCentredString(cxo, cyo - 2, label)
            c.setDash(3, 3)
        c.setDash()

    if footer:
        c.setFont(F_SANS, 6.8)
        c.setFillColor(MUTE)
        c.drawCentredString(PW / 2.0, MARGIN - 6, footer)
    c.showPage()
