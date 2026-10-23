# -*- coding: utf-8 -*-
"""The workbook's illustration kit -- the house art standard.

Reference style (Lodi Grape Growers botanical figures):
  * every form has a DARK INKED OUTLINE (olive-black on greens, brown on yellows)
  * fills are SOFT GRADIENTS, never flat: a pale yellow-green light spot upper-left falling
    to a deep green at the shadow edge
  * thin PALE HIGHLIGHT STRIPES on stems and filaments give them a rounded, tubular look
  * yellow parts (anthers, stigma, pollen, eggs) are warm gold with a brown rim
  * simplified, friendly shapes -- nothing photographic, nothing flat or schematic

Every drawing in the workbook is built from these helpers so the whole book shares one hand.
"""
import math
from reportlab.lib import colors

HEX = colors.HexColor

# ------------------------------------------------------------------ palette
INK_G = HEX("#1F3317")       # outline on green parts
INK_Y = HEX("#5E4216")       # outline on yellow parts
INK_W = HEX("#3A2A18")       # outline on wood
INK_P = HEX("#2A1020")       # outline on purple fruit

G_LIGHT = HEX("#A9D68A")
G_MID = HEX("#58A049")
G_DARK = HEX("#2F7034")
G_DEEP = HEX("#1F5428")
G_PALE = HEX("#CFE5B3")
G_FIL = HEX("#BBD6A6")       # filament / pale stem green
Y_LIGHT = HEX("#FBE59A")
Y_MID = HEX("#F0C75A")
Y_DARK = HEX("#DFA73B")
CREAM = HEX("#F3E6BF")
WOOD_L = HEX("#A98255")
WOOD_M = HEX("#7B5733")
WOOD_D = HEX("#4F3721")
BERRY_L = HEX("#8A4A66")
BERRY_M = HEX("#5B2342")
BERRY_D = HEX("#341326")
SOIL_L = HEX("#E9DDC3")
SOIL_D = HEX("#CDB88F")


def alpha(col, a):
    return colors.Color(col.red, col.green, col.blue, alpha=a)


def mix(c1, c2, k):
    return colors.Color(c1.red + (c2.red - c1.red) * k, c1.green + (c2.green - c1.green) * k,
                        c1.blue + (c2.blue - c1.blue) * k)


# ------------------------------------------------------------------ paths
def path(c, cmds):
    """cmds: [('M',x,y) | ('L',x,y) | ('C',x1,y1,x2,y2,x3,y3) | ('Z',)] in absolute points."""
    p = c.beginPath()
    for cm in cmds:
        t = cm[0]
        if t == "M":
            p.moveTo(cm[1], cm[2])
        elif t == "L":
            p.lineTo(cm[1], cm[2])
        elif t == "C":
            p.curveTo(*cm[1:])
        elif t == "Z":
            p.close()
    return p


def poly(c, pts, close=True):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    return p


def ellipse_path(c, cx, cy, rx, ry, rot=0.0, n=48):
    pts = []
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
    return poly(c, pts)


def bezier(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / float(n)
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


# ------------------------------------------------------------------ fills and outlines
def fill_radial(c, p, cx, cy, r, stops):
    """stops: [(position 0..1, colour)]."""
    c.saveState()
    c.clipPath(p, stroke=0, fill=0)
    c.radialGradient(cx, cy, r, [s[1] for s in stops], [s[0] for s in stops], extend=True)
    c.restoreState()


def fill_linear(c, p, x0, y0, x1, y1, stops):
    c.saveState()
    c.clipPath(p, stroke=0, fill=0)
    c.linearGradient(x0, y0, x1, y1, [s[1] for s in stops], [s[0] for s in stops], extend=True)
    c.restoreState()


def outline(c, p, col=INK_G, lw=1.2):
    c.saveState()
    c.setStrokeColor(col); c.setLineWidth(lw); c.setLineJoin(1); c.setLineCap(1)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def flat(c, p, col):
    c.saveState(); c.setFillColor(col); c.drawPath(p, stroke=0, fill=1); c.restoreState()


def line(c, pts, col=INK_G, lw=1.0):
    c.saveState()
    c.setStrokeColor(col); c.setLineWidth(lw); c.setLineJoin(1); c.setLineCap(1)
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def blob(c, cx, cy, rx, ry, rot=0.0, light=Y_LIGHT, mid=Y_MID, dark=Y_DARK, ink=INK_Y, lw=1.2, light_at=(-0.35, 0.4)):
    """A soft-shaded ellipse with an inked rim -- anthers, stigma lobes, eggs, pollen, berries."""
    p = ellipse_path(c, cx, cy, rx, ry, rot)
    r = max(rx, ry)
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    lx = cx + (light_at[0] * rx) * cr - (light_at[1] * ry) * sr
    ly = cy + (light_at[0] * rx) * sr + (light_at[1] * ry) * cr
    fill_radial(c, p, lx, ly, r * 1.5, [(0, light), (0.45, mid), (1, dark)])
    outline(c, p, ink, lw)
    return p


# ------------------------------------------------------------------ tubes (stems, filaments, roots, canes)
def tube(c, centre, w0, w1, base, light=None, dark=None, ink=INK_G, lw=1.2, hi=0.30, shade=0.28):
    """A tapered tube along `centre` (list of points). Draws fill, a highlight stripe on the left,
    a shadow stripe on the right, and an inked outline."""
    n = len(centre)
    left, right, nrm = [], [], []
    for i, (x, y) in enumerate(centre):
        a = centre[max(i - 1, 0)]
        b = centre[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        w = w0 + (w1 - w0) * i / float(n - 1)
        left.append((x + nx * w / 2.0, y + ny * w / 2.0))
        right.append((x - nx * w / 2.0, y - ny * w / 2.0))
        nrm.append((nx, ny, w))
    body = poly(c, left + right[::-1])
    flat(c, body, base)

    def band(f0, f1):
        a = [(centre[i][0] + nrm[i][0] * nrm[i][2] * f0, centre[i][1] + nrm[i][1] * nrm[i][2] * f0) for i in range(n)]
        b = [(centre[i][0] + nrm[i][0] * nrm[i][2] * f1, centre[i][1] + nrm[i][1] * nrm[i][2] * f1) for i in range(n)]
        return poly(c, a + b[::-1])
    if light is not None:
        flat(c, band(0.06, 0.06 + hi * 0.5), alpha(light, 0.85))
    if dark is not None:
        flat(c, band(-0.5, -0.5 + shade), alpha(dark, 0.55))
    outline(c, body, ink, lw)
    return body


# ------------------------------------------------------------------ vine leaf (same five-lobe silhouette as the Mastery art)
def leaf(c, cx, cy, R, rot=0.0, flip=False, light=HEX("#8CC66E"), mid=HEX("#4E9440"), dark=HEX("#2B6B30"),
         ink=INK_G, lw=0.9, stalk=True):
    centers = (18.0, 90.0, 162.0, 234.0, 306.0)
    tops = (0.90, 1.00, 0.90, 0.72, 0.72)
    floors = (0.60, 0.60, 0.66, 0.58, 0.66)
    sgn = -1.0 if flip else 1.0
    pts = []
    N = 200
    for i in range(N + 1):
        u = i / float(N)
        seg = min(int(u * 5), 4)
        s = u * 5 - seg
        topA, topB = tops[seg], tops[(seg + 1) % 5]
        top_env = topA + (topB - topA) * s
        shape = (math.cos(2 * math.pi * s) + 1) / 2.0
        tooth = 0.012 * math.sin(u * math.pi * 17)
        r = R * max(floors[seg] + (top_env - floors[seg]) * (shape ** 0.8) + tooth, 0.25)
        a = math.radians(centers[seg] + s * 72.0 + rot)
        pts.append((cx + sgn * r * math.cos(a), cy + r * math.sin(a)))
    p = poly(c, pts)
    fill_radial(c, p, cx - sgn * R * 0.30, cy + R * 0.38, R * 1.35, [(0, light), (0.5, mid), (1, dark)])
    # veins
    base_a = math.radians(270.0 + rot)
    bx = cx + sgn * R * floors[3] * math.cos(base_a)
    by = cy + R * floors[3] * math.sin(base_a)
    c.saveState()
    c.setStrokeColor(alpha(HEX("#CFE8B0"), 0.75)); c.setLineCap(1)
    for k, ctr in enumerate(centers):
        a = math.radians(ctr + rot)
        rr = R * tops[k] * 0.80
        c.setLineWidth(0.7 if k == 1 else 0.45)
        c.line(bx, by, cx + sgn * rr * math.cos(a), cy + rr * math.sin(a))
    c.restoreState()
    outline(c, p, ink, lw)
    if stalk:
        line(c, [(bx, by), (bx - sgn * 2.0, by - R * 0.28)], INK_G, 1.4)
    return (bx, by)


# ------------------------------------------------------------------ berry and bunch
def berry(c, cx, cy, r, lw=0.8):
    blob(c, cx, cy, r, r * 1.04, 0, light=BERRY_L, mid=BERRY_M, dark=BERRY_D, ink=INK_P, lw=lw, light_at=(-0.38, 0.42))
    c.saveState()
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.38))
    c.saveState(); c.translate(cx - r * 0.34, cy + r * 0.38); c.rotate(-35)
    c.ellipse(-r * 0.24, -r * 0.10, r * 0.24, r * 0.10, stroke=0, fill=1)
    c.restoreState(); c.restoreState()


def bunch(c, cx, cy, w, h, rows=(4, 4, 3, 3, 2, 1)):
    n = len(rows)
    rad = w / (max(rows) * 1.62)
    for ri, count in enumerate(rows):
        fy = ri / float(n - 1)
        y = cy - fy * h
        spread = w * (1.0 - 0.70 * fy) / 2.0
        for k in range(count):
            fx = 0.5 if count == 1 else k / float(count - 1)
            jitter = ((ri * 7 + k * 13) % 5 - 2) * 0.35
            berry(c, cx - spread + fx * spread * 2 + jitter, y, rad * (1.0 - 0.12 * fy))


# ------------------------------------------------------------------ soft ground shadow / fade helpers
def fade_bottom(c, p, x0, x1, y_bottom, height, steps=70, col=colors.white):
    """Fade the foot of a shape into the page (as the reference's pedicel does)."""
    c.saveState()
    c.clipPath(p, stroke=0, fill=0)
    for i in range(steps):
        a = 0.97 * (1 - (i + 0.5) / float(steps)) ** 1.6
        c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=a))
        c.rect(x0, y_bottom + height * i / float(steps), x1 - x0, height / float(steps) + 0.15, stroke=0, fill=1)
    c.restoreState()


def fill_linear_faded(c, p, x0, x1, stops, y_bottom, height, steps=48):
    """Horizontal gradient fill whose foot dissolves into the page.

    Painted as OPAQUE slices from the bottom up, each blended toward white and overlapping the next, so
    there are no seams (alpha stripes show hairlines in some viewers)."""
    fill_linear(c, p, x0, 0, x1, 0, stops)
    for i in range(steps):
        k = 0.97 * (1 - (i + 0.5) / float(steps)) ** 1.6
        faded = [(pos, mix(col, colors.white, k)) for pos, col in stops]
        band = c.beginPath()
        band.rect(x0 - 2, y_bottom + height * i / float(steps), (x1 - x0) + 4, height / float(steps) + 1.2)
        c.saveState()
        c.clipPath(p, stroke=0, fill=0)
        c.clipPath(band, stroke=0, fill=0)
        c.linearGradient(x0, 0, x1, 0, [s[1] for s in faded], [s[0] for s in faded], extend=True)
        c.restoreState()
