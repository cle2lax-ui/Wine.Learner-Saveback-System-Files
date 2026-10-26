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


# =====================================================================================================================
#  PEN-AND-INK UPGRADE (v2)
#  The same API as above, but forms are now drawn like a fine botanical engraving: outlines are tapered and very slightly
#  irregular (thicker where the form turns away from the light), wood carries bark/grain, leaves are veined and serrated,
#  and shading can be built up with hatching and stippling.  Everything below overrides the earlier definitions.
# =====================================================================================================================
import random as _random

LIGHT_DIR = (-0.62, 0.78)          # light comes from the upper left


def _noise(x, y, s=0.0):
    """Smooth deterministic noise in [-1, 1]: a function of position, so shared edges stay together."""
    return (math.sin(x * 0.37 + y * 0.23 + s) + 0.8 * math.sin(x * 0.131 - y * 0.29 + 1.7 + s)
            + 0.4 * math.sin(x * 0.63 + y * 0.47 + 3.1 + s)) / 2.2


def _jit(pt, amp):
    return (pt[0] + amp * _noise(pt[0], pt[1], 0.0), pt[1] + amp * _noise(pt[0], pt[1], 5.3))


def _flatten(cmds):
    subs, cur = [], []
    for cm in cmds:
        t = cm[0]
        if t == "M":
            if cur:
                subs.append((cur, False))
            cur = [(cm[1], cm[2])]
        elif t == "L":
            cur.append((cm[1], cm[2]))
        elif t == "C" and cur:
            cur.extend(bezier(cur[-1], (cm[1], cm[2]), (cm[3], cm[4]), (cm[5], cm[6]), n=10)[1:])
        elif t == "Z":
            if cur:
                subs.append((cur, True))
            cur = []
    if cur:
        subs.append((cur, False))
    return subs


_path_v1 = path


def path(c, cmds):                                                    # noqa: F811
    p = _path_v1(c, cmds)
    p._cmds = list(cmds)
    p._poly = _flatten(cmds)
    return p


def poly(c, pts, close=True):                                        # noqa: F811
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    p._poly = [(list(pts), close)]
    return p


def rrect(c, x, y, w, h, r=4.0):
    """A rounded rectangle that the pen outline and hatching understand."""
    r = min(r, w / 2.0, h / 2.0)
    k = 0.5523 * r
    return path(c, [("M", x + r, y), ("L", x + w - r, y), ("C", x + w - r + k, y, x + w, y + r - k, x + w, y + r), ("L", x + w, y + h - r),
                    ("C", x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h), ("L", x + r, y + h),
                    ("C", x + r - k, y + h, x, y + h - r + k, x, y + h - r), ("L", x, y + r), ("C", x, y + r - k, x + r - k, y, x + r, y), ("Z",)])


def _signed_area(pts):
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return a / 2.0


def _stroke_weighted(c, pts, lw, ccw_sign):
    """Stroke a polyline with a width that varies with how far each edge faces away from the light."""
    c.setLineCap(1); c.setLineJoin(1)
    run, run_w = [pts[0]], None
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        if L < 1e-6:
            continue
        nx, ny = ccw_sign * dy / L, -ccw_sign * dx / L                 # outward normal
        facing = nx * -LIGHT_DIR[0] + ny * -LIGHT_DIR[1]               # >0 when the edge faces away from the light
        w = lw * (0.78 + 0.5 * max(0.0, facing) - 0.12 * max(0.0, -facing))
        wq = round(w * 5) / 5.0
        if run_w is None:
            run_w = wq
        if wq != run_w:
            c.setLineWidth(run_w)
            p = c.beginPath(); p.moveTo(*run[0])
            for q in run[1:]:
                p.lineTo(*q)
            c.drawPath(p, stroke=1, fill=0)
            run, run_w = [run[-1]], wq
        run.append((x1, y1))
    if len(run) > 1:
        c.setLineWidth(run_w or lw)
        p = c.beginPath(); p.moveTo(*run[0])
        for q in run[1:]:
            p.lineTo(*q)
        c.drawPath(p, stroke=1, fill=0)


def outline(c, p, col=INK_G, lw=1.2, pen=True):                      # noqa: F811
    subs = getattr(p, "_poly", None)
    c.saveState()
    c.setStrokeColor(col)
    if not subs or not pen:
        c.setLineWidth(lw); c.setLineJoin(1); c.setLineCap(1)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()
        return
    amp = min(0.10 + 0.16 * lw, 0.34)
    for pts, closed in subs:
        if len(pts) < 2:
            continue
        q = [_jit(t, amp) for t in pts]
        sign = 1.0
        if closed:
            q.append(q[0])
            sign = 1.0 if _signed_area(q[:-1]) >= 0 else -1.0
        _stroke_weighted(c, q, lw, sign)
    c.restoreState()


def line(c, pts, col=INK_G, lw=1.0, pen=True, taper=True):         # noqa: F811
    c.saveState()
    c.setStrokeColor(col); c.setLineCap(1); c.setLineJoin(1)
    if not pen or len(pts) < 2:
        c.setLineWidth(lw)
        p = c.beginPath(); p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, stroke=1, fill=0)
        c.restoreState()
        return
    amp = min(0.08 + 0.12 * lw, 0.26)
    q = [_jit(t, amp) for t in pts]
    n = len(q) - 1
    if n < 4 and taper:                                                # subdivide very short polylines so they can taper
        dense = []
        for i in range(n):
            for k in range(4):
                f = k / 4.0
                dense.append((q[i][0] + (q[i + 1][0] - q[i][0]) * f, q[i][1] + (q[i + 1][1] - q[i][1]) * f))
        dense.append(q[-1]); q = dense; n = len(q) - 1
    for i in range(n):
        t = (i + 0.5) / float(n)
        w = lw * ((0.55 + 0.6 * math.sin(math.pi * t) ** 0.6) if taper else 1.0)
        c.setLineWidth(w)
        c.line(q[i][0], q[i][1], q[i + 1][0], q[i + 1][1])
    c.restoreState()


# ------------------------------------------------------------------ shading by hatching and stippling
def hatch(c, p, angle=40.0, gap=1.9, col=INK_W, lw=0.32, depth=0.42, shadow=(0.62, -0.78), a=0.62):
    """Fine parallel hatching confined to the shadow side of a closed form (needs a path made by path/poly/rrect)."""
    subs = getattr(p, "_poly", None)
    if not subs:
        return
    pts = subs[0][0]
    sl = math.hypot(*shadow); sx, sy = shadow[0] / sl, shadow[1] / sl
    sh = [x * sx + y * sy for x, y in pts]
    smin, smax = min(sh), max(sh)
    thr = smax - depth * (smax - smin)
    th = math.radians(angle)
    ux, uy = math.cos(th), math.sin(th)                                  # along the hatch line
    vx, vy = -uy, ux                                                     # across
    vs = [x * vx + y * vy for x, y in pts]
    v0, v1 = min(vs), max(vs)
    c.saveState()
    c.setStrokeColor(alpha(col, a)); c.setLineCap(1)
    v = v0 + gap * 0.5
    k = 0
    while v < v1:
        xs = []
        n = len(pts)
        for i in range(n):
            x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % n]
            va, vb = x0 * vx + y0 * vy, x1 * vx + y1 * vy
            if (va - v) * (vb - v) < 0:
                f = (v - va) / (vb - va)
                x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
                xs.append(x * ux + y * uy)
        xs.sort()
        for j in range(0, len(xs) - 1, 2):
            u0, u1 = xs[j], xs[j + 1]
            # shadow coordinate along this chord is linear in u
            sa = (u0 * ux + v * vx) * sx + (u0 * uy + v * vy) * sy
            sb = (u1 * ux + v * vx) * sx + (u1 * uy + v * vy) * sy
            lo, hi = 0.0, 1.0
            if sa != sb:
                f = (thr - sa) / (sb - sa)
                if sb > sa:
                    lo = max(lo, f)
                else:
                    hi = min(hi, f)
            elif sa < thr:
                continue
            if hi <= lo:
                continue
            ua, ub = u0 + (u1 - u0) * lo, u0 + (u1 - u0) * hi
            c.setLineWidth(lw * (0.75 + 0.5 * ((k * 7) % 5) / 4.0))
            c.line(ua * ux + v * vx, ua * uy + v * vy, ub * ux + v * vx, ub * uy + v * vy)
        v += gap
        k += 1
    c.restoreState()


def _inside(pts, x, y):
    ins = False
    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i]; xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi:
            ins = not ins
        j = i
    return ins


def stipple(c, p, n=60, col=INK_W, r=0.32, seed=1, a=0.55, bias=None):
    """Scatter fine dots inside a form (soil, pith, bark).  bias=(dx, dy) clusters them toward one side."""
    subs = getattr(p, "_poly", None)
    if not subs:
        return
    pts = subs[0][0]
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    rnd = _random.Random(seed)
    c.saveState(); c.setFillColor(alpha(col, a))
    got, tries = 0, 0
    while got < n and tries < n * 30:
        tries += 1
        x, y = rnd.uniform(min(xs), max(xs)), rnd.uniform(min(ys), max(ys))
        if bias:
            t = ((x - min(xs)) / (max(xs) - min(xs) + 1e-9)) * bias[0] + ((y - min(ys)) / (max(ys) - min(ys) + 1e-9)) * bias[1]
            if rnd.random() > max(0.12, min(1.0, 0.5 + t * 0.7)):
                continue
        if _inside(pts, x, y):
            c.circle(x, y, r * rnd.uniform(0.6, 1.4), stroke=0, fill=1)
            got += 1
    c.restoreState()


# ------------------------------------------------------------------ tubes: bark and grain, a shadow hatch, a pen outline
def tube(c, centre, w0, w1, base, light=None, dark=None, ink=INK_G, lw=1.2, hi=0.30, shade=0.28, grain=None):   # noqa: F811
    n = len(centre)
    left, right, nrm = [], [], []
    for i, (x, y) in enumerate(centre):
        a_ = centre[max(i - 1, 0)]
        b_ = centre[min(i + 1, n - 1)]
        dx, dy = b_[0] - a_[0], b_[1] - a_[1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        w = (w0[i] if isinstance(w0, (list, tuple)) else w0 + (w1 - w0) * i / float(n - 1))
        left.append((x + nx * w / 2.0, y + ny * w / 2.0))
        right.append((x - nx * w / 2.0, y - ny * w / 2.0))
        nrm.append((nx, ny, w))
    body = poly(c, left + right[::-1])
    flat(c, body, base)

    def band(f0, f1):
        a_ = [(centre[i][0] + nrm[i][0] * nrm[i][2] * f0, centre[i][1] + nrm[i][1] * nrm[i][2] * f0) for i in range(n)]
        b_ = [(centre[i][0] + nrm[i][0] * nrm[i][2] * f1, centre[i][1] + nrm[i][1] * nrm[i][2] * f1) for i in range(n)]
        return poly(c, a_ + b_[::-1])
    if light is not None:
        flat(c, band(0.06, 0.06 + hi * 0.5), alpha(light, 0.85))
    if dark is not None:
        flat(c, band(-0.5, -0.5 + shade), alpha(dark, 0.55))
    wmean = (sum(w0) / len(w0)) if isinstance(w0, (list, tuple)) else (w0 + w1) / 2.0
    if grain is None:
        grain = (ink == INK_W) and wmean >= 3.6
    if grain:
        rnd = _random.Random(int(centre[0][0] * 13 + centre[0][1] * 7 + n))
        gcol = dark if dark is not None else ink
        for k in range(max(3, int(wmean / 2.2))):
            f = rnd.uniform(-0.40, 0.40)
            ph = rnd.uniform(0, 6.28)
            seg = [(centre[i][0] + nrm[i][0] * nrm[i][2] * (f + 0.035 * math.sin(i * 0.8 + ph)),
                    centre[i][1] + nrm[i][1] * nrm[i][2] * (f + 0.035 * math.sin(i * 0.8 + ph))) for i in range(n)]
            i0 = rnd.randint(0, max(0, n // 4)); i1 = n - rnd.randint(0, max(0, n // 4))
            if i1 - i0 >= 3:
                line(c, seg[i0:i1], alpha(gcol, 0.7), 0.34, pen=False, taper=False)
        if wmean >= 5.0:                                               # bark: short cracks and flakes across the grain
            step = 2 if wmean >= 9 else 3
            for i in range(1, n - 1, step):
                if rnd.random() < 0.7:
                    f = rnd.uniform(-0.40, 0.25)
                    ln = nrm[i][2] * rnd.uniform(0.12, 0.30)
                    x, y = centre[i][0] + nrm[i][0] * nrm[i][2] * f, centre[i][1] + nrm[i][1] * nrm[i][2] * f
                    tx, ty = -nrm[i][1], nrm[i][0]
                    line(c, [(x, y), (x + nrm[i][0] * ln + tx * 0.8, y + nrm[i][1] * ln + ty * 0.8)], alpha(gcol, 0.85), 0.34, pen=False, taper=False)
            if wmean >= 9.0:
                kx = rnd.randint(2, max(2, n - 3))
                f = rnd.uniform(-0.2, 0.2)
                kxp, kyp = centre[kx][0] + nrm[kx][0] * nrm[kx][2] * f, centre[kx][1] + nrm[kx][1] * nrm[kx][2] * f
                for rr_ in (1.9, 1.2, 0.6):
                    kp_ = ellipse_path(c, kxp, kyp, rr_ * 1.5, rr_, 25)
                    outline(c, kp_, alpha(gcol, 0.9), 0.32, pen=False)
    outline(c, body, ink, lw)
    return body


# ------------------------------------------------------------------ vine leaf: five lobes, serrated, with a real vein structure
def leaf(c, cx, cy, R, rot=0.0, flip=False, light=HEX("#8CC66E"), mid=HEX("#4E9440"), dark=HEX("#2B6B30"),    # noqa: F811
         ink=INK_G, lw=0.9, stalk=True):
    centers = (18.0, 90.0, 162.0, 234.0, 306.0)
    tops = (0.90, 1.00, 0.90, 0.72, 0.72)
    floors = (0.60, 0.60, 0.66, 0.58, 0.66)
    sgn = -1.0 if flip else 1.0
    teeth = 31 if R >= 7 else 17
    tamp = 0.030 if R >= 7 else 0.018
    pts = []
    N = 220
    for i in range(N + 1):
        u = i / float(N)
        seg = min(int(u * 5), 4)
        s = u * 5 - seg
        topA, topB = tops[seg], tops[(seg + 1) % 5]
        top_env = topA + (topB - topA) * s
        shape = (math.cos(2 * math.pi * s) + 1) / 2.0
        tooth = tamp * (((u * teeth) % 1.0) - 0.5)                       # sawtooth margin
        r = R * max(floors[seg] + (top_env - floors[seg]) * (shape ** 0.8) + tooth, 0.25)
        a_ = math.radians(centers[seg] + s * 72.0 + rot)
        pts.append((cx + sgn * r * math.cos(a_), cy + r * math.sin(a_)))
    p = poly(c, pts)
    fill_radial(c, p, cx - sgn * R * 0.30, cy + R * 0.38, R * 1.35, [(0, light), (0.5, mid), (1, dark)])
    base_a = math.radians(270.0 + rot)
    bx = cx + sgn * R * floors[3] * math.cos(base_a)
    by = cy + R * floors[3] * math.sin(base_a)
    c.saveState()
    c.setLineCap(1)
    vcol = alpha(HEX("#16300F"), 0.55)
    hcol = alpha(HEX("#E4F2C8"), 0.80)
    for k, ctr in enumerate(centers):
        a_ = math.radians(ctr + rot)
        rr = R * tops[k] * (0.84 if R >= 7 else 0.78)
        ex, ey = cx + sgn * rr * math.cos(a_), cy + rr * math.sin(a_)
        wv = (0.55 if k == 1 else 0.42) * (1.0 if R >= 7 else 0.8)
        off = 0.45 if R >= 7 else 0.3
        nx, ny = -(ey - by), (ex - bx)
        nl = math.hypot(nx, ny) or 1.0
        nx, ny = nx / nl * off, ny / nl * off
        c.setStrokeColor(hcol); c.setLineWidth(wv)
        c.line(bx + nx, by + ny, ex + nx, ey + ny)
        c.setStrokeColor(vcol); c.setLineWidth(wv * 0.9)
        c.line(bx, by, ex, ey)
        if R >= 11:                                                      # side veins branching off each main vein
            for f in (0.35, 0.55, 0.74):
                px, py = bx + (ex - bx) * f, by + (ey - by) * f
                ang = math.atan2(ey - by, ex - bx)
                for sd in (-1, 1):
                    a2 = ang + sd * math.radians(48)
                    ll = R * 0.17 * (1.0 - 0.35 * f)
                    c.setLineWidth(0.3)
                    c.line(px, py, px + ll * math.cos(a2), py + ll * math.sin(a2))
    c.restoreState()
    outline(c, p, ink, lw)
    if stalk:
        line(c, [(bx, by), (bx - sgn * 1.2, by - R * 0.16), (bx - sgn * 2.0, by - R * 0.30)], INK_G, 1.3, taper=False)
    return (bx, by)


# ------------------------------------------------------------------ berries with bloom, bunches with a visible rachis
def berry(c, cx, cy, r, lw=0.8):                                      # noqa: F811
    k = ((int(cx * 7) + int(cy * 5)) % 5) / 4.0
    mid = mix(BERRY_M, HEX("#4A3B6A"), 0.28 * k)
    blob(c, cx, cy, r, r * 1.04, 0, light=BERRY_L, mid=mid, dark=BERRY_D, ink=INK_P, lw=lw, light_at=(-0.38, 0.42))
    c.saveState()
    c.setFillColor(colors.Color(0.82, 0.86, 0.95, alpha=0.16))            # waxy bloom
    c.ellipse(cx - r * 0.82, cy - r * 0.55, cx + r * 0.62, cy + r * 0.80, stroke=0, fill=1)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.46))
    c.saveState(); c.translate(cx - r * 0.34, cy + r * 0.38); c.rotate(-35)
    c.ellipse(-r * 0.26, -r * 0.10, r * 0.26, r * 0.10, stroke=0, fill=1)
    c.restoreState()
    c.setFillColor(alpha(HEX("#1B0C16"), 0.8))                            # the dark calyx scar
    c.circle(cx + r * 0.12, cy - r * 0.86, max(r * 0.07, 0.25), stroke=0, fill=1)
    c.restoreState()


def bunch(c, cx, cy, w, h, rows=(4, 4, 3, 3, 2, 1), seed=0, berry_fn=None):          # noqa: F811
    """A natural, slightly lopsided bunch: staggered rows, uneven berry sizes, a shoulder, a visible rachis."""
    n = len(rows)
    rnd = _random.Random(int(cx * 3 + cy * 5) + seed)
    rad = w / (max(rows) * 1.58)
    lean = rnd.uniform(-0.10, 0.10) * w
    line(c, [(cx, cy + 3.0), (cx + 0.5, cy), (cx + lean * 0.5, cy - h * 0.6)], INK_W, max(0.7, rad * 0.35), taper=False)
    line(c, [(cx, cy + 6.0), (cx, cy + 2.0)], INK_W, max(1.0, rad * 0.5), taper=False)
    items = []
    for ri, count in enumerate(rows):
        fy = ri / float(max(n - 1, 1))
        y = cy - fy * h * (0.97 if ri else 1.0)
        span = w * (1.0 - 0.80 * fy ** 1.05)
        stagger = (0.5 if ri % 2 else 0.0) * (span / max(count, 1)) * 0.5
        for k in range(count):
            fx = 0.5 if count == 1 else k / float(count - 1)
            x = cx + lean * fy - span / 2.0 + fx * span + stagger - (span / max(count, 1)) * 0.12 * (ri % 2)
            x += rnd.uniform(-0.30, 0.30) * rad
            yy = y + rnd.uniform(-0.28, 0.28) * rad
            rr = rad * (1.0 - 0.14 * fy) * rnd.uniform(0.86, 1.10)
            items.append((yy, x, rr))
    for (y, x, rr) in sorted(items, key=lambda t: -t[0]):
        (berry_fn or berry)(c, x, y, rr)
