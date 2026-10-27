# -*- coding: utf-8 -*-
"""Vine anatomy for the workbook's drawings, and the five training systems (bush, VSP, GDC, Scott-Henry, California sprawl).

Everything here is drawn in a 120 x 142 pt design space and scaled to the box, so a drawing keeps its proportions at any width.

The rule for this module: a vine must never look like a post.  Wood is gnarled and twists; the trunk flares at the base, carries a
graft union and old pruning stubs, and peels in long strips; the head is a knuckle of old cuts; cordons taper, undulate and swell
at each spur; spurs are knobby; shoots are jointed at the nodes, carry petioled leaves and tendrils; bunches hang from the vine
on peduncles.  Posts, wires and beams (the only straight things) are drawn plainly so the contrast reads.
"""
import math
import os
import random as _random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wb_ink as K
from wb_art import Art, _ground, _post, _wire

HEX = K.HEX
BARK_L, BARK_M, BARK_D = HEX("#B38C62"), HEX("#7A5836"), HEX("#43301A")
SPUR_L, SPUR_M = HEX("#EBCB98"), HEX("#BE915C")
CUT_L, CUT_M = HEX("#F4E3BC"), HEX("#D6B47C")
SH_L, SH_M = HEX("#CDE7AE"), K.G_MID
FRONT = (HEX("#8CC66E"), HEX("#4E9440"), HEX("#2B6B30"))
BACK = (HEX("#6E9F5C"), HEX("#3A7A3A"), HEX("#1F4A26"))
MID = (HEX("#7DB562"), HEX("#448A3B"), HEX("#265F2B"))
TONES = {0: BACK, 1: MID, 2: FRONT}


# ------------------------------------------------------------------------------------------------ geometry helpers
def _frames(ctr):
    n = len(ctr)
    out = []
    for i in range(n):
        a_ = ctr[max(i - 1, 0)]
        b_ = ctr[min(i + 1, n - 1)]
        dx, dy = b_[0] - a_[0], b_[1] - a_[1]
        d = math.hypot(dx, dy) or 1.0
        out.append((dx / d, dy / d, -dy / d, dx / d))
    return out


def _off(ctr, fr, wid, i, f, extra=0.0):
    return (ctr[i][0] + fr[i][2] * wid[i] * (f + extra), ctr[i][1] + fr[i][3] * wid[i] * (f + extra))


# ------------------------------------------------------------------------------------------------ old wood
def wood(c, ctr, wid, seed=0, strips=2, lw=1.2, grain=True):
    """Gnarled permanent wood: grain, bark cracks, long peeling strips of pale bark with a shadow line beside each."""
    K.tube(c, ctr, list(wid), None, BARK_M, light=BARK_L, dark=BARK_D, ink=K.INK_W, lw=lw, hi=0.5, shade=0.45, grain=grain)
    rnd = _random.Random(seed * 31 + 7)
    fr = _frames(ctr)
    n = len(ctr)
    wm = sum(wid) / float(n)
    if wm >= 4.5:
        for k in range(strips):
            i0 = rnd.randint(1, max(1, n // 3))
            i1 = min(n - 2, i0 + rnd.randint(max(3, n // 4), max(4, n // 2)))
            f = rnd.uniform(-0.34, 0.34)
            pts = [_off(ctr, fr, wid, i, f, 0.035 * math.sin(i * 0.9 + k)) for i in range(i0, i1 + 1)]
            pts2 = [_off(ctr, fr, wid, i, f + 0.075, 0.035 * math.sin(i * 0.9 + k)) for i in range(i0, i1 + 1)]
            K.line(c, pts, K.alpha(BARK_L, 0.98), max(0.55, wm * 0.075), pen=False, taper=True)
            K.line(c, pts2, K.alpha(BARK_D, 0.85), 0.34, pen=False, taper=True)
            ex, ey = pts[-1]                                                  # the loose end of the strip curls out
            K.line(c, [pts[-1], (ex + fr[i1][2] * wm * 0.18 + fr[i1][0] * 0.9, ey + fr[i1][3] * wm * 0.18 + fr[i1][1] * 0.9)],
                   K.alpha(BARK_D, 0.9), 0.4, pen=False, taper=True)


def stub(c, x, y, ang, L, w):
    """An old pruning stub: a short thick snag ending in a pale cut face with growth rings."""
    a = math.radians(ang)
    ex, ey = x + L * math.cos(a), y + L * math.sin(a)
    K.tube(c, [(x, y), ((x + ex) / 2.0, (y + ey) / 2.0), (ex, ey)], w, w * 0.84, BARK_M, light=BARK_L, dark=BARK_D, ink=K.INK_W,
           lw=0.85, hi=0.5, shade=0.4, grain=False)
    face = K.ellipse_path(c, ex, ey, w * 0.26, w * 0.52, ang, 24)
    K.fill_radial(c, face, ex - 0.3, ey + 0.3, w * 0.8, [(0, CUT_L), (1, CUT_M)])
    K.outline(c, face, K.INK_W, 0.6)
    ring = K.ellipse_path(c, ex, ey, w * 0.13, w * 0.27, ang, 18)
    K.outline(c, ring, K.alpha(BARK_D, 0.8), 0.28, pen=False)


def trunk(c, x, y0, y1, w, seed=0, lean=0.0, graft=True, stubs=((0.58, 1), (0.80, -1)), twist=0.34):
    """A real trunk: S-curved, flared at the root collar, a graft-union swelling low down, tapering, knotted, with old stubs."""
    rnd = _random.Random(seed * 7 + 3)
    n = 52
    ph = rnd.uniform(0, 6.28)
    waves = max(1.0, (y1 - y0) / 46.0)
    ctr, wid = [], []
    for i in range(n):
        t = i / float(n - 1)
        env = min(1.0, t * 5.0)                                              # the base sits square on the ground; the twist grows from there
        xx = x + lean * t + env * (w * twist * math.sin(t * 3.7 * waves + ph) + w * 0.10 * math.sin(t * 9.5 * waves + ph * 1.7))
        yy = y0 + (y1 - y0) * t
        flare = 1.0 + 0.55 * math.exp(-t * 9.0)
        bump = 1.0 + (0.20 * math.exp(-((t - 0.14) / 0.05) ** 2) if graft else 0.0)
        swell = 1.0 + 0.07 * math.sin(t * 11.0 + ph) + 0.04 * math.sin(t * 25.0 + ph)
        ctr.append((xx, yy))
        wid.append(w * (1.0 - 0.22 * t) * flare * bump * swell)
    wood(c, ctr, wid, seed=seed, strips=3, lw=1.3)
    for (f, sd) in stubs:
        i = int(f * (n - 1))
        stub(c, ctr[i][0] + sd * wid[i] * 0.36, ctr[i][1], 24 if sd > 0 else 156, 2.7, 2.6)
    return ctr, wid


def head(c, x, y, w, seed=0, stubs=2):
    """The swollen head where the trunk divides: a knuckle of old wood with pruning stubs."""
    rnd = _random.Random(seed + 11)
    sh = K.ellipse_path(c, x, y, w * 0.74, w * 0.55, rnd.uniform(-10, 10))
    K.fill_radial(c, sh, x - w * 0.25, y + w * 0.2, w * 1.4, [(0, BARK_L), (0.55, BARK_M), (1, BARK_D)])
    K.hatch(c, sh, angle=60, gap=1.3, col=BARK_D, lw=0.26, depth=0.45, a=0.6)
    K.outline(c, sh, K.INK_W, 1.2)
    for k in range(3):
        K.line(c, [(x - w * 0.42 + k * w * 0.30, y - w * 0.28), (x - w * 0.37 + k * w * 0.30 + 0.8, y + w * 0.26)], K.alpha(BARK_D, 0.85), 0.4, pen=False)
    for k in range(stubs):
        sd = 1 if k % 2 == 0 else -1
        stub(c, x + sd * w * 0.12, y + w * 0.42, 90 + sd * 35, 2.6, 2.3)


# ------------------------------------------------------------------------------------------------ cordons and spurs
def cordon(c, hx, hy, sgn, length, w, seed=0, arch=1.0, droop=0.0, spurs=True, gap=9.5, first=0.15, dirs=None, spur_len=7.2, lift=0.0):
    """A cordon: thick at the head, thinning to its tip, undulating, swelling at every spur.  Spurs are short knobby snags.
    Returns ([(x, y, dir)] spur tops, centre-line, widths)."""
    rnd = _random.Random(seed * 13 + 5)
    m = 36
    ph = rnd.uniform(0, 6.28)
    pos = []
    t = first
    while t < 0.95:
        pos.append(t)
        t += gap / float(length)
    ctr, wid = [], []
    for i in range(m):
        t = i / float(m - 1)
        xx = hx + sgn * length * t
        yy = hy + arch * math.sin(t * math.pi * 0.8) - droop * t * t + lift * t * t + w * 0.13 * math.sin(t * 9.0 + ph)
        bump = 1.0
        for s_ in pos:
            bump += 0.17 * math.exp(-((t - s_) / 0.033) ** 2)
        ctr.append((xx, yy))
        wid.append(w * (1.0 - 0.52 * t ** 0.85) * bump * (1.0 + 0.05 * math.sin(t * 19.0 + ph)))
    tops = []
    if spurs:
        for k, s_ in enumerate(pos):
            i = int(round(s_ * (m - 1)))
            x, y = ctr[i]
            d = 1 if (dirs is None or dirs[k % len(dirs)] == "up") else -1
            lean = rnd.uniform(-0.9, 0.9) + sgn * 0.7
            base = (x, y + d * wid[i] * 0.05)
            top = (x + lean, y + d * (wid[i] * 0.32 + spur_len))
            mid = (x + lean * 0.35, y + d * (wid[i] * 0.32 + spur_len * 0.5))
            sw = max(3.0, wid[i] * 0.56)
            K.tube(c, [base, mid, top], sw, sw * 0.82, SPUR_M, light=SPUR_L, dark=BARK_M, ink=K.INK_W, lw=0.8, hi=0.5, shade=0.4, grain=False)
            nd = K.ellipse_path(c, mid[0] + 0.2, mid[1], sw * 0.62, sw * 0.40, 0, 14)           # a swollen bud on the spur
            K.fill_radial(c, nd, mid[0] - 0.3, mid[1] + 0.3, sw, [(0, SPUR_L), (1, SPUR_M)])
            K.outline(c, nd, K.INK_W, 0.5)
            tops.append((top[0], top[1], d))
    wood(c, ctr, wid, seed=seed + 2, strips=1, lw=1.1)
    return tops, ctr, wid


def under(ctr, wid, x):
    """The y of the underside of a cordon at horizontal position x (for hanging a bunch from it)."""
    best = min(range(len(ctr)), key=lambda i: abs(ctr[i][0] - x))
    return ctr[best][0], ctr[best][1] - wid[best] * 0.42


def tie(c, x, y, h=6.0):
    """A wire tie / cane tie round a cordon where it meets its wire."""
    c.saveState()
    c.setStrokeColor(HEX("#3B3B3B")); c.setLineWidth(0.8); c.setLineCap(1)
    c.line(x - 0.9, y + h * 0.5, x - 0.2, y - h * 0.5)
    c.line(x + 0.9, y + h * 0.5, x + 0.2, y - h * 0.5)
    c.restoreState()


# ------------------------------------------------------------------------------------------------ green growth
def leaf_at(c, node, ang, R, petiole=None, flip=False, tone=1, lw=0.7):
    """A leaf joined to `node` by a petiole; the blade points along `ang` (degrees)."""
    pet = R * 0.5 if petiole is None else petiole
    a = math.radians(ang)
    cxl, cyl = node[0] + math.cos(a) * (pet + 0.58 * R), node[1] + math.sin(a) * (pet + 0.58 * R)
    ab = ang + 180.0
    rot = (ab - 270.0) if not flip else ((180.0 - ab) - 270.0)
    bx, by = node[0] + math.cos(a) * pet, node[1] + math.sin(a) * pet
    K.line(c, [node, ((node[0] + bx) / 2.0 + 0.2, (node[1] + by) / 2.0), (bx, by)], K.INK_G, 0.9, pen=False, taper=False)
    lt, md, dk = TONES[tone]
    K.leaf(c, cxl, cyl, R, rot=rot, flip=flip, light=lt, mid=md, dark=dk, stalk=False, lw=lw)


def tendril(c, x, y, ang, turns=2.2, size=2.0):
    """A corkscrew tendril."""
    pts = []
    a0 = math.radians(ang)
    for i in range(0, 22):
        t = i / 21.0
        r = size * (1.0 - 0.55 * t) * 0.9
        th = turns * 2 * math.pi * t
        along = size * 2.6 * t
        pts.append((x + math.cos(a0) * along - math.sin(a0) * r * math.sin(th), y + math.sin(a0) * along + math.cos(a0) * r * math.sin(th)))
    K.line(c, pts, K.INK_G, 0.8, pen=False, taper=True)
    K.line(c, pts, HEX("#9CCB7C"), 0.35, pen=False, taper=False)


def shoot(c, ctr, R=5.6, seed=0, leaves=6, tone=1, w0=2.4, w1=1.0, spread=62, tendrils=True, tip=True, size_fall=0.28, petiole=0.5):
    """A green shoot, jointed at the nodes, with petioled leaves alternating left and right, tendrils, and a tip of small young leaves."""
    rnd = _random.Random(seed * 17 + 1)
    n = len(ctr)
    K.tube(c, ctr, w0, w1, SH_M, light=SH_L, ink=K.INK_G, lw=0.7, hi=0.5)
    fr = _frames(ctr)
    for k in range(leaves):
        f = 0.10 + 0.74 * k / float(max(leaves - 1, 1))
        i = min(int(f * (n - 1)), n - 1)
        node = ctr[i]
        side = 1 if k % 2 == 0 else -1
        if k > 1 and rnd.random() < 0.09:
            continue                                                                        # not every node carries a good leaf
        base_ang = math.degrees(math.atan2(fr[i][1], fr[i][0]))
        ang = base_ang - side * (spread + rnd.uniform(-20, 20))
        size = R * (1.0 - size_fall * f) * rnd.uniform(0.84, 1.14)
        nd = K.ellipse_path(c, node[0], node[1], 1.5, 1.2, 0, 12)                           # the swollen node
        K.fill_radial(c, nd, node[0] - 0.3, node[1] + 0.3, 2.4, [(0, SH_L), (1, K.G_DARK)])
        K.outline(c, nd, K.INK_G, 0.5)
        if tendrils and k % 3 == 1:
            tendril(c, node[0], node[1], base_ang + side * 70, size=R * 0.34)
        leaf_at(c, node, ang, size, petiole=size * petiole, flip=side < 0, tone=tone)
    if tip:
        tx, ty = ctr[-1]
        base_ang = math.degrees(math.atan2(fr[-1][1], fr[-1][0]))
        for sd, da in ((1, 38), (-1, 38)):
            leaf_at(c, (tx, ty), base_ang - sd * da, R * 0.46, petiole=R * 0.14, flip=sd < 0, tone=tone, lw=0.55)
        leaf_at(c, (tx, ty), base_ang, R * 0.36, petiole=R * 0.05, tone=tone, lw=0.5)


def arc(p0, p1, p2, p3, n=24):
    return K.bezier(p0, p1, p2, p3, n=n)


def hang_bunch(c, attach, bx, by, w=11.0, h=15.0, seed=0, rows=(3, 3, 3, 2, 1)):
    """A bunch that hangs from the vine: a peduncle runs from `attach` to the shoulder of the bunch at (bx, by)."""
    ax, ay = attach
    ped = K.bezier((ax, ay), (ax + (bx - ax) * 0.1, ay - 2.5), (bx, by + 10.0), (bx, by + 6.0), n=12)
    K.tube(c, ped, 1.5, 1.2, SH_M, light=SH_L, ink=K.INK_G, lw=0.6, hi=0.5)
    K.bunch(c, bx, by, w, h, rows=rows, seed=seed)


def _plain_post(c, x, y0, y1, w=4.4):
    _post(c, x, y0, y1, w)


def _wire_pair(c, x0, x1, y):
    _wire(c, x0, x1, y)


# ------------------------------------------------------------------------------------------------ whole vines
def mini_vine(c, cx, y0, th=24, ch=44, spread=15, bunches=True, R=5.0, seed=None, young=False, w=7.2):
    """A small, correctly drawn vine for the scene drawings (irrigation, frost, harvest).  `young` gives the short soft shoots of spring."""
    sd = int(cx) if seed is None else seed
    ctr, wid = trunk(c, cx, y0, y0 + th, w, seed=sd % 9, lean=((sd % 3) - 1) * 1.2, stubs=((0.66, 1),))
    hx, hy = ctr[-1]
    tops = []
    for sgn in (-1, 1):
        tp, cc, cw = cordon(c, hx, hy + 1.0, sgn, spread, 4.4, seed=sd % 7 + (0 if sgn < 0 else 3), arch=0.8, gap=7.0, first=0.2, spur_len=4.6)
        tops += [(x, y) for (x, y, d) in tp]
    head(c, hx, hy + 0.5, w * 0.86, seed=sd % 5, stubs=1)
    tops = sorted(tops)
    rnd = _random.Random(sd)
    for i, (x, y) in enumerate(tops):
        L = ch * (0.34 if young else rnd.uniform(0.9, 1.05))
        lean = (x - hx) * 0.10
        sp = [(x, y), (x + lean * 0.3 + 0.6 * math.sin(i), y + L * 0.35), (x + lean * 0.8 - 0.8 * math.sin(i + 1), y + L * 0.7), (x + lean, y + L)]
        ctr_s = arc(*sp, n=16)
        shoot(c, ctr_s, R=R * (0.62 if young else 1.0), seed=sd + i, leaves=3 if young else 5, tone=(0 if i % 2 else 2), w0=1.9, w1=0.9,
              tendrils=not young, size_fall=0.22)
    if bunches and not young:
        for k, sgn in enumerate((-1, 1)):
            bx = hx + sgn * spread * 0.62
            hang_bunch(c, (bx, hy + 6.0), bx + sgn * 0.5, hy - 3.0, w=8.5, h=11.5, seed=sd + k, rows=(3, 3, 2, 2, 1))


class _Trellis(Art):
    aspect = 1.18
    DW, DH = 120.0, 142.0

    def draw(self, c):
        c.saveState()
        c.scale(self.W / self.DW, self.W / self.DW)
        self.paint(c)
        c.restoreState()

    def paint(self, c):
        raise NotImplementedError


class TrellisBush(_Trellis):
    """Bush vine (gobelet): free-standing, a short thick trunk, a head of stout curving arms, shoots that arch and droop to make a rounded canopy."""
    name = "bush"

    def paint(self, c):
        _ground(c, 120)
        ctr, wid = trunk(c, 60, 8, 40, 11.8, seed=3, lean=2.0, twist=0.30, stubs=((0.5, 1), (0.72, -1)))
        hx, hy = ctr[-1]
        arms = []
        for (sgn, ln, up, w0, sd) in ((-1, 22, 22, 6.4, 1), (1, 23, 24, 6.4, 2), (-1, 8, 31, 5.4, 3), (1, 9, 33, 5.4, 4)):
            pts = []
            m = 26
            rnd = _random.Random(sd * 5)
            ph = rnd.uniform(0, 6)
            for i in range(m):
                t = i / float(m - 1)
                pts.append((hx + sgn * ln * t ** 1.15 + 0.8 * math.sin(t * 6 + ph), hy + 2 + up * t ** 0.8 + 1.1 * math.sin(t * 7 + ph)))
            wd = [w0 * (1 - 0.64 * i / (m - 1)) + 0.7 for i in range(m)]
            arms.append((pts, wd))
        for (pts, wd) in arms[2:] + arms[:2]:
            wood(c, pts, wd, seed=len(pts) + int(pts[-1][0]), strips=1, lw=1.0)
        head(c, hx, hy + 1.5, 11.0, seed=2, stubs=2)
        tips = [p[-1] for p, w_ in arms]
        spec = [(tips[0], (-20, 8), (-27, -24), 2), (tips[1], (20, 10), (27, -20), 0), (tips[2], (-6, 32), (-20, -2), 1),
                (tips[3], (6, 34), (18, 0), 1), (tips[0], (-4, 36), (-15, 8), 0), (tips[1], (6, 38), (17, 6), 0)]
        for k, ((sx, sy), (c1x, c1y), (ex, ey), tone) in enumerate(spec):
            p0 = (sx, sy + 1)
            p1 = (sx + c1x * 0.4, sy + c1y + 14)
            p2 = (sx + c1x * 1.1, sy + c1y + 30)
            p3 = (sx + ex, sy + ey + 30)
            shoot(c, arc(p0, p1, p2, p3, n=28), R=7.6, seed=40 + k, leaves=8, tone=tone, w0=2.5, w1=1.0, spread=58, size_fall=0.12, petiole=0.35)
        for k, (ai, ti, dx, drop, sd) in enumerate(((0, 14, -3, 22, 1), (1, 15, 3, 22, 2), (0, 22, 1, 20, 3))):
            pts, wd = arms[ai]
            ax, ay = pts[ti][0], pts[ti][1] - wd[ti] * 0.42
            hang_bunch(c, (ax, ay + 1.5), ax + dx, ay - drop + 4, w=11.0, h=14.8, seed=sd)


class TrellisVSP(_Trellis):
    """Vertical shoot positioning: a cordon on the fruiting wire, spurs, and shoots combed straight up between catch-wires into a hedge."""
    name = "vsp"

    def paint(self, c):
        _ground(c, 120)
        for y in (52, 80, 104, 126):
            _wire(c, 5, 115, y)
        _post(c, 5, 8, 134, 4.4); _post(c, 115, 8, 134, 4.4)
        ctr, wid = trunk(c, 60, 8, 48, 10.0, seed=5, lean=-1.5)
        hx, hy = ctr[-1]
        tops, cords = [], []
        for sgn, sd in ((-1, 1), (1, 2)):
            tp, cc, cw = cordon(c, hx, 51.0, sgn, 41, 6.8, seed=sd, arch=0.8, gap=9.0, first=0.17)
            tops += [(x, y, sgn) for (x, y, d) in tp]
            cords.append((cc, cw))
            for (x, y) in cc[7::9]:
                tie(c, x, y)
        head(c, hx, 50.5, 9.6, seed=4, stubs=2)
        tops.sort()
        for i, (x, y, sgn) in enumerate(tops):                                      # the canopy: a wall of overlapping shoots
            lean = (x - hx) * 0.06
            L = 126 - y + 5.0 * math.sin(i * 2.1 + 0.6)
            p = [(x, y), (x + lean * 0.4 + 0.9 * math.sin(i * 1.3), y + L * 0.34), (x + lean * 0.9 - 1.6 * math.sin(i * 1.7), y + L * 0.68), (x + lean * 1.2 + 1.4 * math.sin(i * 2.9), y + L)]
            shoot(c, arc(*p, n=28), R=7.4, seed=11 + i, leaves=9, tone=(0 if i % 2 == 0 else 2), w0=2.5, w1=1.1, spread=58, size_fall=0.16, petiole=0.35)
        for k, bx in enumerate((26, 44, 78, 96)):
            cc, cw = cords[0] if bx < hx else cords[1]
            ax, ay = under(cc, cw, bx)
            hang_bunch(c, (ax, ay + 1.5), bx + (2 if k % 2 else -2), 47 - (k % 2) * 3, w=10.6, h=14.0, seed=k + 1)


class TrellisGDC(_Trellis):
    """Geneva Double Curtain: one trunk tied to a post, a head at the centre of a cross-arm, an arm along each end of the cross-arm
    carrying the cordon wire, and two curtains of shoots hanging down."""
    name = "gdc"

    def paint(self, c):
        _ground(c, 120)
        beam_y = 100.0
        _post(c, 64, 8, beam_y + 2, 5.0)                                              # the support post, with the vine tied to it
        K.tube(c, [(10, beam_y + 3), (110, beam_y + 3)], 5.0, 5.0, HEX("#9A7B52"), light=HEX("#C9AE86"), dark=HEX("#5E4626"), ink=K.INK_W, lw=1.0, hi=0.5, shade=0.4, grain=True)
        for x in (16, 104):                                                           # the two cordon wires, carried on brackets
            K.line(c, [(x, beam_y + 5.5), (x, beam_y + 11)], HEX("#4A4A4A"), 0.9)
            _wire(c, x - 9, x + 9, beam_y + 11)
        ctr, wid = trunk(c, 58, 8, beam_y + 6, 9.4, seed=8, lean=2.0, twist=0.40)
        hx, hy = ctr[-1]
        for y_ in (30, 62):                                                           # ties holding the trunk to the post
            i = min(range(len(ctr)), key=lambda k: abs(ctr[k][1] - y_))
            tie(c, ctr[i][0] + 1.0, ctr[i][1], h=wid[i] * 0.9)
        tops, cords = [], []
        for sgn, sd in ((-1, 1), (1, 2)):
            ex = 16 if sgn < 0 else 104
            L = abs(ex - hx)
            tp, cc, cw = cordon(c, hx, beam_y + 11.5, sgn, L, 5.8, seed=sd + 4, arch=0.6, gap=7.4, first=0.40, spur_len=3.8, dirs=["down"])
            tops += [(x, y) for (x, y, d) in tp]
            cords.append((cc, cw))
            for (x, y) in cc[22::7]:
                tie(c, x, y, h=5.0)
        head(c, hx, beam_y + 9.0, 8.8, seed=6, stubs=1)
        for i, (x, y) in enumerate(sorted(tops)):
            out = -1 if x < hx else 1
            L = 60 + (i % 2) * 6
            p = [(x, y), (x + out * 2.5, y - 9), (x + out * 5 + 1.5 * math.sin(i), y - L * 0.62), (x + out * 3.5 + 1.2 * math.sin(i * 2), y - L)]
            shoot(c, arc(*p, n=26), R=7.4, seed=21 + i, leaves=9, tone=(0 if i % 2 == 0 else 2), w0=2.3, w1=1.0, spread=64, size_fall=0.10, tendrils=False, petiole=0.35)
        for k, bx in enumerate((20, 30, 92, 102)):
            cc, cw = cords[0] if bx < hx else cords[1]
            ax, ay = under(cc, cw, bx)
            hang_bunch(c, (ax, ay + 1.5), bx + (1.5 if k % 2 else -1.5), 84 - (k % 2) * 6, w=9.6, h=13.0, seed=k + 1)


class TrellisSH(_Trellis):
    """Scott-Henry: shoots from alternate spurs are trained up, the others are trained down, splitting the canopy vertically into two curtains."""
    name = "scott_henry"

    def paint(self, c):
        _ground(c, 120)
        for y in (24, 40, 62, 96, 122):
            _wire(c, 5, 115, y)
        _post(c, 5, 8, 134, 4.4); _post(c, 115, 8, 134, 4.4)
        ctr, wid = trunk(c, 60, 8, 56, 10.0, seed=9, lean=1.5)
        hx, hy = ctr[-1]
        tops, cords = [], []
        for sgn, sd in ((-1, 1), (1, 2)):
            tp, cc, cw = cordon(c, hx, 59.0, sgn, 41, 6.6, seed=sd + 3, arch=0.6, gap=8.0, first=0.16, dirs=["up", "down"])
            tops += [(x, y, d, sgn) for (x, y, d) in tp]
            cords.append((cc, cw))
            for (x, y) in cc[7::9]:
                tie(c, x, y)
        head(c, hx, 58.5, 9.6, seed=7, stubs=2)
        tops.sort()
        for i, (x, y, d, sgn) in enumerate(tops):
            lean = (x - hx) * 0.05
            if d > 0:
                L = 122 - y + 5.0 * math.sin(i * 2.3 + 1.0)
                p = [(x, y), (x + lean * 0.4 + 0.9 * math.sin(i), y + L * 0.34), (x + lean * 0.9 - 1.6 * math.sin(i * 2), y + L * 0.68), (x + lean * 1.2 + 1.3 * math.sin(i * 3.1), y + L)]
                shoot(c, arc(*p, n=26), R=7.1, seed=31 + i, leaves=9, tone=(0 if i % 4 == 1 else 2), w0=2.4, w1=1.0, spread=58, size_fall=0.16, petiole=0.35)
            else:
                L = y - 26
                p = [(x, y), (x + sgn * 2.5, y - L * 0.3), (x + sgn * 3.8 + math.sin(i), y - L * 0.65), (x + sgn * 3.2, y - L)]
                shoot(c, arc(*p, n=24), R=6.6, seed=51 + i, leaves=7, tone=1, w0=2.3, w1=1.0, spread=62, size_fall=0.10, tendrils=False, petiole=0.35)
        for k, bx in enumerate((38, 82)):
            cc, cw = cords[0] if bx < hx else cords[1]
            ax, ay = under(cc, cw, bx)
            hang_bunch(c, (ax, ay + 1.5), bx, 52, w=10.0, h=13.4, seed=k + 1)


class TrellisSprawl(_Trellis):
    """California sprawl: a tall trunk, cordons on one high wire, no shoot positioning -- the shoots flop over and hang in a dense, untidy curtain."""
    name = "sprawl"

    def paint(self, c):
        _ground(c, 120)
        _post(c, 5, 8, 112, 4.4); _post(c, 115, 8, 112, 4.4)
        _wire(c, 5, 115, 92)
        ctr, wid = trunk(c, 60, 8, 87, 10.4, seed=2, lean=-2.0, twist=0.40)
        hx, hy = ctr[-1]
        tops, cords = [], []
        for sgn, sd in ((-1, 1), (1, 2)):
            tp, cc, cw = cordon(c, hx, 90.0, sgn, 42, 6.4, seed=sd + 5, arch=0.8, gap=7.4, first=0.16)
            tops += [(x, y, sgn) for (x, y, d) in tp]
            cords.append((cc, cw))
            for (x, y) in cc[8::10]:
                tie(c, x, y)
        head(c, hx, 89.5, 9.4, seed=5, stubs=2)
        tops.sort()
        for i, (x, y, sgn) in enumerate(tops):
            out = -1 if x < hx else 1
            if i % 2:
                out = -out
            reach = 12 + (i % 3) * 5
            p = [(x, y), (x + out * 3, y + 24), (x + out * (reach * 0.9), y + 30), (x + out * reach, y - 6 - (i % 3) * 8)]
            shoot(c, arc(*p, n=30), R=7.2, seed=61 + i, leaves=9, tone=(i % 3), w0=2.4, w1=1.0, spread=62, size_fall=0.10, petiole=0.35)
        for k, bx in enumerate((32, 44, 78, 90)):
            cc, cw = cords[0] if bx < hx else cords[1]
            ax, ay = under(cc, cw, bx)
            hang_bunch(c, (ax, ay + 1.5), bx + (1.5 if k % 2 else -1.5), 76 - (k % 2) * 4, w=10.4, h=14.0, seed=k + 1)
