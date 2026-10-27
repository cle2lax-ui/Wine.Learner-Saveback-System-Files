# -*- coding: utf-8 -*-
"""More workbook artwork in the house style: irrigation (Ch6), frost protection and mildews (Ch8), California sprawl (Ch10),
soil profile with a plow pan (Ch5)."""
import math
import random as _random
import wb_ink as K
alpha_ = K.alpha
from wb_art import (Art, HEX, _ground, _post, _wire, _tie, _shoot_with_leaves, _steel, _steel_poly, STEEL_L, STEEL_M, STEEL_D, INK_S,
                    vine_trunk, vine_head, vine_cordon, BARK_L, BARK_M, BARK_D)

BL_L, BL_M, BL_D, BL_I = HEX("#CFE8F6"), HEX("#7DBBE0"), HEX("#2F7FB0"), HEX("#1D4F73")
PIPE_L, PIPE_M, PIPE_D, PIPE_I = HEX("#6B7279"), HEX("#3A3F44"), HEX("#1E2327"), HEX("#101315")
WET_L, WET_M, WET_D = HEX("#CDB88F"), HEX("#A78D5C"), HEX("#7B6238")


def _drop(c, x, y, s=1.0):
    K.blob(c, x, y, 1.7 * s, 2.5 * s, 0, light=BL_L, mid=BL_M, dark=BL_D, ink=BL_I, lw=0.5)


def _vine(c, cx, y0, th=24, ch=44, spread=15, bunches=True, R=5.0, seed=None, young=False):
    """A small, correctly drawn vine for the scene drawings (see wb_vine.mini_vine)."""
    from wb_vine import mini_vine
    mini_vine(c, cx, y0, th=th, ch=ch, spread=spread, bunches=bunches, R=R, seed=seed, young=young)


def _arrow(c, pts, col, lw=1.6):
    K.line(c, pts, col, lw)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    c.saveState(); c.setFillColor(col); c.setStrokeColor(col)
    p = c.beginPath(); p.moveTo(x1, y1)
    p.lineTo(x1 - 6 * math.cos(a - 0.45), y1 - 6 * math.sin(a - 0.45))
    p.lineTo(x1 - 6 * math.cos(a + 0.45), y1 - 6 * math.sin(a + 0.45)); p.close()
    c.drawPath(p, stroke=0, fill=1); c.restoreState()


# ===================================================================== irrigation (Chapter 6)
class IrrDrip(Art):
    name = "drip"
    aspect = 1.0

    def draw(self, c):
        W = self.W
        _ground(c, W)
        for x in (14, 50, 70, 106):
            K.blob(c, x, 5, 9, 3, 0, light=WET_L, mid=WET_M, dark=WET_D, ink=WET_D, lw=0.4)
        _wire(c, 4, W - 4, 40)
        for cx in (32, 88):
            _vine(c, cx, 9, th=24, ch=44, spread=13)
        K.tube(c, [(2, 14), (W - 2, 14)], 3.4, 3.4, PIPE_M, light=PIPE_L, dark=PIPE_D, ink=PIPE_I, lw=0.8, hi=0.5, shade=0.4)
        for x in (14, 50, 70, 106):
            K.blob(c, x, 14, 2.3, 2.3, 0, light=HEX("#9AA3AA"), mid=PIPE_M, dark=PIPE_D, ink=PIPE_I, lw=0.6)
            _drop(c, x, 9.2, 0.9)


class IrrFlood(Art):
    name = "flood"
    aspect = 1.0

    def draw(self, c):
        W = self.W
        _ground(c, W)
        res = K.path(c, [("M", 0, 9), ("L", 8, 9), ("L", 8, 40), ("L", 0, 40), ("Z",)])
        K.fill_linear(c, res, 0, 40, 0, 9, [(0, BL_L), (1, BL_M)]); K.outline(c, res, BL_I, 0.9)
        sheet = K.path(c, [("M", 14, 9), ("L", W, 9), ("L", W, 21), ("C", W * 0.78, 24, W * 0.6, 18, W * 0.42, 22),
                           ("C", W * 0.3, 24, 24, 20, 14, 22), ("Z",)])
        K.fill_linear(c, sheet, 0, 22, 0, 9, [(0, BL_L), (1, BL_M)]); K.outline(c, sheet, BL_I, 0.9)
        for (x, y) in ((34, 16), (60, 14), (80, 17), (100, 14)):
            K.line(c, [(x - 5, y), (x + 5, y)], HEX("#F4FAFD"), 1.0)
        _steel(c, 8, 9, 6, 52, r=2, horizontal=False)                      # sluice post
        _steel(c, 8.6, 22, 4.8, 24, r=1, horizontal=False)                 # gate
        _arrow(c, [(15, 27), (30, 27)], BL_I, 1.4)
        for cx in (52, 100):
            _vine(c, cx, 14, th=22, ch=42, spread=13)


class IrrFurrow(Art):
    name = "furrow"
    aspect = 1.0

    def draw(self, c):
        W = self.W
        prof = [(0, 20), (6, 14), (14, 9), (22, 14), (30, 22), (38, 22), (46, 14), (54, 9), (66, 9), (74, 14), (82, 22), (90, 22),
                (98, 14), (106, 9), (114, 14), (120, 20)]
        p = K.path(c, [("M", 0, 0), ("L", 0, 20)] + [("L", x, y) for (x, y) in prof[1:]] + [("L", W, 0), ("Z",)])
        K.fill_linear(c, p, 0, 22, 0, 0, [(0, K.SOIL_L), (1, K.SOIL_D)])
        K.stipple(c, p, n=150, col=HEX("#6F5A36"), r=0.38, seed=11, a=0.6, bias=(0.0, -0.5))
        K.hatch(c, p, angle=-30, gap=2.1, col=HEX("#7B6238"), lw=0.25, depth=0.5, shadow=(0.3, -1.0), a=0.5)
        K.line(c, prof, K.INK_W, 1.1)
        for cx in (14, 60, 106):
            wp = K.path(c, [("M", cx - 8, 13.5), ("L", cx + 8, 13.5), ("L", cx + 5, 9.6), ("L", cx - 5, 9.6), ("Z",)])
            K.fill_linear(c, wp, 0, 13.5, 0, 9.6, [(0, BL_L), (1, BL_M)]); K.outline(c, wp, BL_I, 0.8)
        for cx in (34, 86):
            _vine(c, cx, 22, th=20, ch=42, spread=13)


class IrrSprinkler(Art):
    name = "sprinkler"
    aspect = 1.0

    def draw(self, c):
        W = self.W
        _ground(c, W)
        for cx in (20, 100):
            _vine(c, cx, 9, th=24, ch=40, spread=13)
        _steel(c, 57, 9, 6, 60, r=2, horizontal=False)
        _steel(c, 46, 71, 28, 3.6, r=1.5)
        K.blob(c, 60, 72, 5.5, 5, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=1.0)
        for side in (-1, 1):
            for k in range(1, 11):
                t = k / 10.0
                x = 60 + side * (8 + 46 * t)
                y = 76 + 34 * t * (1 - t) * 2.0 - 36 * t
                _drop(c, x, y, 0.8)


# ===================================================================== frost protection (Chapter 8)
def _frost_bg(c, W, H, warm_band=False):
    p = K.path(c, [("M", 0, 0), ("L", W, 0), ("L", W, H), ("L", 0, H), ("Z",)])
    K.fill_linear(c, p, 0, H, 0, 0, [(0, HEX("#D9E8F3")), (1, HEX("#F4F8FB"))])
    if warm_band:
        q = K.path(c, [("M", 0, H - 30), ("L", W, H - 30), ("L", W, H), ("L", 0, H), ("Z",)])
        K.fill_linear(c, q, 0, H, 0, H - 30, [(0, HEX("#F6D9A6")), (1, HEX("#FBEBD0"))])
        K.line(c, [(0, H - 30), (W, H - 30)], HEX("#D7A458"), 0.7)
    for (x, y) in ((16, 118), (130, 122), (40, 98), (112, 96), (88, 124)):
        for a in (0, 60, 120):
            r = 3.0
            K.line(c, [(x - r * math.cos(math.radians(a)), y - r * math.sin(math.radians(a))),
                       (x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a)))], HEX("#9DBBD0"), 0.6)


class FrostWindMachine(Art):
    name = "wind_machine"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        _frost_bg(c, W, H, warm_band=True)
        _ground(c, W)
        for cx in (26, 124):
            _vine(c, cx, 9, th=18, ch=32, spread=11, R=4.6, young=True)
        _steel(c, 72, 9, 6, 92, r=2, horizontal=False)
        _steel(c, 66, 100, 18, 8, r=3)
        for sgn in (-1, 1):
            K.blob(c, 75 + sgn * 17, 104 + sgn * 5, 16, 3.4, sgn * 18, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.9)
        K.blob(c, 75, 104, 3.6, 3.6, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.9)
        for sgn in (-1, 1):
            ctr = K.bezier((75 + sgn * 8, 98), (75 + sgn * 22, 88), (75 + sgn * 40, 76), (75 + sgn * 46, 56), n=14)
            _arrow(c, ctr, HEX("#D9822B"), 1.7)


class FrostSprinklers(Art):
    name = "aspersion"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        _frost_bg(c, W, H)
        _ground(c, W)
        for cx in (26, 124):
            _vine(c, cx, 9, th=18, ch=32, spread=11, R=4.6, young=True)
        _steel(c, 72, 9, 5, 52, r=2, horizontal=False)
        K.blob(c, 74.5, 63, 5, 4.6, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=1.0)
        for side in (-1, 1):
            for k in range(1, 12):
                t = k / 11.0
                x = 74.5 + side * (7 + 40 * t)
                y = 66 + 30 * t * (1 - t) * 2.0 - 30 * t
                _drop(c, x, y, 0.8)
        for cx in (26, 124):                                              # ice glaze on the shoots
            for dx in (-9, -3, 3, 9):
                K.blob(c, cx + dx, 9 + 18 + 3 + 32, 3.0, 4.0, 0, light=HEX("#FFFFFF"), mid=HEX("#D6EAF6"), dark=HEX("#9CC7E3"),
                       ink=HEX("#6FA6C9"), lw=0.6)


class FrostHeaters(Art):
    name = "heaters"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        _frost_bg(c, W, H)
        _ground(c, W)
        for cx in (22, 128):
            _vine(c, cx, 9, th=18, ch=32, spread=11, R=4.6, young=True)
        for px in (58, 96):
            body = K.path(c, [("M", px - 8, 9), ("L", px + 8, 9), ("L", px + 6, 38), ("L", px - 6, 38), ("Z",)])
            K.fill_linear(c, body, px - 8, 0, px + 8, 0, [(0, PIPE_L), (0.35, PIPE_M), (1, PIPE_D)]); K.outline(c, body, PIPE_I, 1.1)
            _steel(c, px - 8, 36, 16, 4, r=1.5)
            K.blob(c, px, 49, 6, 9, 0, light=HEX("#FBE59A"), mid=HEX("#F2A53A"), dark=HEX("#D8641E"), ink=HEX("#8A3A12"), lw=0.9)
            K.blob(c, px, 47, 2.6, 4.6, 0, light=HEX("#FFF6C8"), mid=HEX("#FBE59A"), dark=HEX("#F2C14A"), ink=HEX("#F2A53A"), lw=0.4)
            for dx in (-12, 12):
                _arrow(c, K.bezier((px + dx * 0.5, 52), (px + dx, 62), (px + dx * 1.3, 70), (px + dx * 1.7, 80), n=10), HEX("#D9822B"), 1.2)
            K.line(c, K.bezier((px, 60), (px - 6, 70), (px + 6, 80), (px, 92), n=14), HEX("#9AA3AA"), 1.0)


# ===================================================================== mildews (Chapter 8)
class MildewDowny(Art):
    name = "downy"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        K.leaf(c, 70, 74, 60, rot=8, stalk=True, lw=1.1)
        for (x, y, rx, ry, rot) in ((58, 90, 8, 7, 10), (88, 82, 9, 8, -20), (68, 62, 8, 7.5, 30), (98, 62, 7, 6.5, 0),
                                    (46, 66, 7, 6.5, -10), (78, 104, 7, 6, 20), (54, 110, 6, 5.5, 0)):
            K.blob(c, x, y, rx, ry, rot, light=HEX("#F6EE9A"), mid=HEX("#DBCB4B"), dark=HEX("#A39625"), ink=HEX("#6F6516"), lw=0.7)
        c.saveState()
        circ = c.beginPath(); circ.circle(122, 26, 22)
        K.fill_linear(c, circ, 100, 48, 144, 4, [(0, HEX("#D7EBC3")), (1, HEX("#9CCB84"))]); K.outline(c, circ, K.INK_G, 1.3)
        c.restoreState()
        for (x, y) in ((113, 30), (125, 36), (130, 22), (116, 18), (122, 28), (110, 24), (128, 14)):
            K.blob(c, x, y, 5.0, 3.4, (x * 7) % 40 - 20, light=HEX("#FFFFFF"), mid=HEX("#F1F1EC"), dark=HEX("#D9D9D2"),
                   ink=HEX("#B9B9B0"), lw=0.5)
        K.line(c, [(106, 10), (92, -4)], K.INK_W, 2.2)

    def _targets(self):
        return []


class MildewPowdery(Art):
    name = "powdery"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        K.leaf(c, 100, 92, 44, rot=-6, stalk=False, lw=1.0)
        K.line(c, [(48, 130), (48, 118)], K.INK_G, 2.0)
        K.bunch(c, 50, 118, 48, 64, rows=(5, 5, 4, 4, 3, 2, 1))
        # the bloom: a fine gray-white dust, denser in patches (stippled, not painted)
        for (cx, cy, rx, ry, rot, n) in ((42, 100, 17, 11, 15, 150), (60, 84, 15, 10, -20, 120), (50, 66, 13, 9, 10, 90), (100, 100, 20, 12, -20, 170),
                                         (112, 82, 14, 10, 20, 110), (92, 76, 13, 8, 0, 90)):
            reg = K.ellipse_path(c, cx, cy, rx, ry, rot)
            K.stipple(c, reg, n=n, col=HEX("#F4F4EE"), r=0.62, seed=int(cx * 3 + cy), a=0.95)
            c.saveState(); c.setFillColor(K.alpha(HEX("#E9E9E2"), 0.28)); K.flat(c, reg, K.alpha(HEX("#E9E9E2"), 0.28)); c.restoreState()


# ===================================================================== California sprawl (Chapter 10)
def __getattr__(name):
    if name == "TrellisSprawl":
        import wb_vine
        return wb_vine.TrellisSprawl
    raise AttributeError(name)


# ===================================================================== soil profile with a plow pan (Chapter 5)
class SoilProfile(Art):
    name = "soil_profile"
    aspect = 0.50

    def draw(self, c):
        W, H = self.W, self.H
        top = H - 50
        pan_t, pan_b = top - 38, top - 47
        def wave(yb, x):
            return yb + 1.7 * math.sin(x * 0.043 + yb * 0.7) + 0.9 * math.sin(x * 0.121 + yb)
        xs_ = [i * W / 60.0 for i in range(61)]

        def band(y0, y1):
            top_ = [(x, wave(y1, x) if y1 < top - 0.5 else y1) for x in xs_]
            bot_ = [(x, wave(y0, x) if y0 > 1 else y0) for x in reversed(xs_)]
            return K.poly(c, top_ + bot_)
        sub = band(0, pan_b)
        K.fill_linear(c, sub, 0, pan_b, 0, 0, [(0, HEX("#D9C49C")), (1, HEX("#C4AB7A"))])
        tops = band(pan_t, top)
        K.fill_linear(c, tops, 0, top, 0, pan_t, [(0, HEX("#6B4A2B")), (1, HEX("#8A6540"))])
        pool = band(pan_t, pan_t + 10)
        K.fill_linear(c, pool, 0, pan_t + 10, 0, pan_t, [(0, HEX("#9FB9C9")), (1, HEX("#6E94AD"))])
        pan = band(pan_b, pan_t)
        K.fill_linear(c, pan, 0, pan_t, 0, pan_b, [(0, HEX("#4A3F36")), (1, HEX("#2F2823"))])
        for x in range(8, int(W), 14):
            K.line(c, [(x, pan_t - 3), (x + 9, pan_t - 3)], HEX("#7A6B5C"), 0.8)
            K.line(c, [(x + 4, pan_b + 3), (x + 13, pan_b + 3)], HEX("#6B5D4F"), 0.8)
        K.stipple(c, sub, n=260, col=HEX("#6F5A36"), r=0.45, seed=21, a=0.6, bias=(0.2, -0.6))
        K.stipple(c, tops, n=180, col=HEX("#2E1D0E"), r=0.42, seed=7, a=0.55)
        K.hatch(c, sub, angle=-33, gap=2.6, col=HEX("#6F5A36"), lw=0.28, depth=0.25, shadow=(0.2, -1.0), a=0.5)
        K.hatch(c, pan, angle=25, gap=1.5, col=HEX("#0E0A07"), lw=0.3, depth=0.9, a=0.6)
        for xr in range(6, int(W) - 10, 19):
            K.line(c, [(xr, pan_t + 4), (xr + 6, pan_t + 6.2), (xr + 12, pan_t + 4.4)], HEX("#F4FAFD"), 0.6)
        for (x, y, r) in ((30, 20, 4), (120, 34, 5), (200, 22, 4.5), (270, 40, 5), (160, 12, 3.5), (60, 44, 3.5), (300, 18, 4)):
            K.blob(c, x, y, r, r * 0.8, 15, light=HEX("#E8D7B5"), mid=HEX("#BBA173"), dark=HEX("#8C7549"), ink=HEX("#6B5A38"), lw=0.6)
        K.line(c, [(0, top), (W, top)], K.INK_W, 1.2)
        for yy in (pan_t, pan_b):
            K.line(c, [(x, wave(yy, x)) for x in xs_], HEX("#1C1612"), 0.9, taper=False)
        vx = 92
        _vine(c, vx, top - 3, th=15, ch=24, spread=11, bunches=False, R=5.2, seed=6)
        for (dx, wend, sg) in ((0, 48, 1), (0, 62, -1)):                  # roots spread, then are checked at the pan
            r0 = (vx, top - 2)
            ctr = K.bezier(r0, (vx + sg * 10, top - 14), (vx + sg * 32, pan_t + 17), (vx + sg * wend, pan_t + 8), n=18)
            K.tube(c, ctr, 3.4, 1.4, HEX("#B98A56"), light=HEX("#E3C08C"), dark=HEX("#7B5733"), ink=K.INK_W, lw=0.7, hi=0.4, shade=0.3)
        K.tube(c, [(vx, top - 2), (vx, top - 22), (vx + 4, pan_t + 6)], 3.0, 1.2, HEX("#B98A56"), light=HEX("#E3C08C"),
               dark=HEX("#7B5733"), ink=K.INK_W, lw=0.7, hi=0.4, shade=0.3)

    def _targets(self):
        W, H = self.W, self.H
        top = H - 50
        pan_t, pan_b = top - 38, top - 47
        return [("Topsoil", (200, top - 14), "R"), ("Plow pan", (230, (pan_t + pan_b) / 2.0), "R"), ("Subsoil", (240, pan_b - 20), "R"),
                ("Roots", (92 - 38, pan_t + 12), "L"), ("Pooled water", (170, pan_t + 5), "L")]


# ===================================================================== oak barrel (Chapter 14)
def _mix(a, b, f):
    f = max(0.0, min(1.0, f))
    return colors_.Color(a.red + (b.red - a.red) * f, a.green + (b.green - a.green) * f, a.blue + (b.blue - a.blue) * f)


class Barrel(Art):
    """An oak barrel lying on a cradle, in a true three-quarter view.
    Every part comes from one cylinder projection: the bilge profile, curved stave seams, hoops that wrap the form,
    the head with its chime, and the bung on the bilge."""
    name = "barrel"
    aspect = 0.5
    vis = (0.03, 0.90)
    PHI = math.radians(24)

    def _g(self):
        W, H = self.W, self.H
        return dict(cy=H * 0.50, sx=W * 0.17, L=W * 0.73, hc=H * 0.300, he=H * 0.222)

    def _h(self, t):
        g = self._g()
        u = 2 * t - 1
        return g["he"] + (g["hc"] - g["he"]) * (1 - u * u)

    def _pt(self, t, th):
        """Screen point on the barrel surface: t along the axis (0 head .. 1 far end), th around it (0 top, pi/2 front, pi bottom)."""
        g = self._g()
        h = self._h(t)
        return (g["sx"] + g["L"] * t * math.cos(self.PHI) + h * math.sin(self.PHI) * math.sin(th), g["cy"] + h * math.cos(th))

    def _seam(self, th, n=36):
        return [self._pt(i / float(n), th) for i in range(n + 1)]

    def draw(self, c):
        W, H = self.W, self.H
        g = self._g()
        cy, sx = g["cy"], g["sx"]
        N = 15
        ths = [math.pi * k / N for k in range(N + 1)]

        # ground shadow
        c.saveState(); c.setFillColor(K.alpha(HEX("#3A2A1A"), 0.20))
        c.ellipse(sx - 4, 2.0, sx + g["L"] * math.cos(self.PHI) + 16, 12.0, stroke=0, fill=1)
        c.restoreState()

        # the cradle: two timber chocks whose saddle tops follow the barrel's underside
        belly = self._seam(math.pi, 60)

        def ybot(x):
            for (x0_, y0_), (x1_, y1_) in zip(belly, belly[1:]):
                if x0_ <= x <= x1_:
                    return y0_ + (y1_ - y0_) * (x - x0_) / max(x1_ - x0_, 1e-6)
            return belly[-1][1] if x > belly[-1][0] else belly[0][1]

        for t_ in (0.20, 0.80):
            xc = sx + g["L"] * t_ * math.cos(self.PHI)
            foot = K.rrect(c, xc - 27, 3.5, 54, 7.0, 1.4)
            K.fill_linear(c, foot, 0, 10.5, 0, 3.5, [(0, K.WOOD_L), (1, K.WOOD_D)]); K.outline(c, foot, K.INK_W, 1.1)
            xs_ = [xc - 14 + 28 * i / 10.0 for i in range(11)]
            top_ = [(x, ybot(x) + 2.2) for x in xs_]
            wedge = K.poly(c, [(xc - 21, 10.5), (xc + 21, 10.5), (xc + 14, top_[-1][1] - 0.6)] + top_[::-1] + [(xc - 14, top_[0][1] - 0.6)])
            K.fill_linear(c, wedge, xc - 21, 0, xc + 21, 0, [(0, K.WOOD_L), (0.5, K.WOOD_M), (1, K.WOOD_D)]); K.outline(c, wedge, K.INK_W, 1.1)
            for gx in (-12, -5, 3, 10):
                K.line(c, [(xc + gx, 12), (xc + gx * 0.75, ybot(xc + gx * 0.75) - 1.0)], alpha_(K.WOOD_D, 0.55), 0.3, pen=False, taper=True)

        # staves: shaded bands that curve around the form, each with its own tone
        rnd = _random.Random(14)
        for k in range(N):
            th_m = (ths[k] + ths[k + 1]) / 2.0
            top_ = self._seam(ths[k]); bot_ = self._seam(ths[k + 1])
            band = K.poly(c, top_ + bot_[::-1])
            lit = 1.0 - th_m / math.pi                                  # 1 at the lit top, 0 at the shaded belly
            base = _mix(K.WOOD_D, K.WOOD_L, 0.12 + 0.86 * lit ** 0.8)
            base = _mix(base, HEX("#A97844") if rnd.random() < 0.5 else HEX("#C49A66"), 0.22 * rnd.random())
            K.flat(c, band, base)
            for gi in range(3):                                         # grain, following the stave
                fth = ths[k] + (ths[k + 1] - ths[k]) * (0.2 + 0.3 * gi + 0.1 * rnd.random())
                t0 = rnd.uniform(0.0, 0.55); t1 = min(1.0, t0 + rnd.uniform(0.25, 0.5))
                seg = [self._pt(t0 + (t1 - t0) * i / 14.0, fth + 0.004 * math.sin(i * 1.3 + k)) for i in range(15)]
                K.line(c, seg, alpha_(K.WOOD_D, 0.50), 0.3, pen=False, taper=True)
        for th in ths[1:-1]:                                            # stave seams
            K.line(c, self._seam(th), alpha_(HEX("#2A1A0C"), 0.80), 0.8, pen=False)

        # body silhouette: top edge, far rim, bottom edge
        n = 36
        top_edge = self._seam(0.0, n)
        bot_edge = self._seam(math.pi, n)
        rim = [self._pt(1.0, math.pi * i / 16.0) for i in range(17)]
        left_ = [self._pt(0.0, math.pi * (1 - i / 16.0)) for i in range(17)]
        body = K.poly(c, top_edge + rim + bot_edge[::-1] + left_)
        K.hatch(c, body, angle=-35, gap=2.2, col=K.WOOD_D, lw=0.3, depth=0.34, shadow=(0.25, -1.0), a=0.55)

        # sheen along the lit shoulder
        for i, (th, al) in enumerate(((0.42, 0.34), (0.58, 0.18))):
            K.line(c, [self._pt(0.10 + 0.80 * j / 20.0, th) for j in range(21)], K.alpha(HEX("#FFF3DA"), al), 1.6 - 0.5 * i, pen=False, taper=True)

        # hoops wrap the form: each is a band bounded by two circumferential arcs
        for t_, dt in ((0.075, 0.020), (0.150, 0.015), (0.330, 0.021), (0.670, 0.021), (0.850, 0.015), (0.925, 0.020)):
            ths_ = [math.pi * i / 22.0 for i in range(23)]
            a0 = [self._pt(t_ - dt, th) for th in ths_]
            a1 = [self._pt(t_ + dt, th) for th in ths_]
            hp = K.poly(c, a0 + a1[::-1])
            K.fill_linear(c, hp, 0, cy + self._h(t_), 0, cy - self._h(t_), [(0, STEEL_L), (0.38, HEX("#F4F6F8")), (0.55, STEEL_M), (1, STEEL_D)])
            K.outline(c, hp, INK_S, 0.95)
            K.line(c, [self._pt(t_ - dt * 0.35, th) for th in ths_[3:-4]], K.alpha(HEX("#FFFFFF"), 0.75), 0.6, pen=False)
            for th in (math.pi * 0.30, math.pi * 0.55, math.pi * 0.80):
                rx_, ry_ = self._pt(t_, th)
                K.blob(c, rx_, ry_, 0.9, 0.9, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.4)

        K.outline(c, body, K.INK_W, 1.4)

        # the head: chime rim, then the board disc
        hx, hy = sx, cy
        ry = g["he"]; rx = ry * math.sin(self.PHI)
        chime = K.ellipse_path(c, hx, hy, rx + 1.9, ry + 1.5, 0)
        K.fill_radial(c, chime, hx - rx * 0.4, hy + ry * 0.3, ry * 1.6, [(0, HEX("#C9A06C")), (1, K.WOOD_D)]); K.outline(c, chime, K.INK_W, 1.3)
        disc = K.ellipse_path(c, hx, hy, rx * 0.93, ry * 0.93, 0)
        K.fill_radial(c, disc, hx - rx * 0.35, hy + ry * 0.35, ry * 1.5, [(0, HEX("#E3C494")), (0.55, K.WOOD_L), (1, HEX("#AD8250"))])
        K.hatch(c, disc, angle=60, gap=1.5, col=K.WOOD_D, lw=0.26, depth=0.40, a=0.5)
        for f in (-0.55, -0.12, 0.30):                                   # head boards: parallel joints
            yy = ry * 0.93 * math.sqrt(max(0.0, 1 - f * f))
            K.line(c, [(hx + f * rx * 0.93, hy - yy * 0.97), (hx + f * rx * 0.93, hy + yy * 0.97)], alpha_(HEX("#2A1A0C"), 0.75), 0.7)
        K.outline(c, disc, K.INK_W, 1.1)
        ring = K.ellipse_path(c, hx, hy, rx * 0.74, ry * 0.76, 0)                      # the croze groove
        K.outline(c, ring, alpha_(K.WOOD_D, 0.8), 0.6, pen=False)

        # the bung, high on the bilge
        bx, by = self._pt(0.50, math.radians(38))
        hole = K.ellipse_path(c, bx, by, 6.6, 3.9, 8)
        K.fill_radial(c, hole, bx, by, 8, [(0, HEX("#150C06")), (1, HEX("#2A1B10"))]); K.outline(c, hole, K.INK_W, 1.2)
        plug = K.ellipse_path(c, bx, by + 0.9, 5.0, 2.9, 8)
        K.fill_radial(c, plug, bx - 1.5, by + 1.8, 7, [(0, HEX("#E0BE8A")), (0.6, K.WOOD_L), (1, K.WOOD_M)]); K.outline(c, plug, K.INK_W, 0.9)
        K.line(c, [(bx - 3.0, by + 1.6), (bx + 2.4, by + 2.2)], K.alpha(HEX("#FFFFFF"), 0.5), 0.6, pen=False)

    def _targets(self):
        hx, hy = self._g()["sx"], self._g()["cy"]
        rx = self._g()["he"] * math.sin(self.PHI)
        hp = self._pt(0.150, math.radians(62))
        bp = self._pt(0.50, math.radians(38))
        sp = self._pt(0.58, math.radians(112))
        return [("Head", (hx - rx * 0.30, hy - 2), "L"), ("Hoop", hp, "L"), ("Bung", bp, "R"), ("Stave", sp, "R")]


# ===================================================================== bottle necks and closures (Chapter 15)
GL_L, GL_M, GL_D, GL_I = HEX("#E4F0E9"), HEX("#B9D3C4"), HEX("#8FB3A0"), HEX("#2F4A3C")
CORK_L, CORK_M, CORK_D = HEX("#DDBB84"), HEX("#C79B5C"), HEX("#9B7237")


def _neck_paths(c):
    outer = K.path(c, [("M", 33, 134), ("L", 67, 134), ("L", 67, 123), ("L", 62, 120), ("L", 62, 92), ("C", 62, 70, 83, 64, 83, 38),
                       ("L", 83, 8), ("L", 17, 8), ("L", 17, 38), ("C", 17, 64, 38, 70, 38, 92), ("L", 38, 120), ("L", 33, 123), ("Z",)])
    inner = K.path(c, [("M", 41.5, 134), ("L", 58.5, 134), ("L", 58.5, 92), ("C", 58.5, 72, 79.5, 66, 79.5, 38), ("L", 79.5, 11.5),
                       ("L", 20.5, 11.5), ("L", 20.5, 38), ("C", 20.5, 66, 41.5, 72, 41.5, 92), ("Z",)])
    return outer, inner


def _bottle_neck(c, wine_y=92, wine=(HEX("#F3DE8E"), HEX("#D9B450"))):
    outer, inner = _neck_paths(c)
    K.fill_linear(c, outer, 8, 0, 92, 0, [(0, GL_M), (0.2, GL_L), (0.5, GL_M), (0.8, GL_L), (1, GL_D)])
    K.fill_linear(c, inner, 0, 0, 0, 1, [(0, HEX("#FBFBF8")), (1, HEX("#FBFBF8"))])
    c.saveState(); c.clipPath(inner, stroke=0, fill=0)
    wp = c.beginPath(); wp.rect(0, 0, 100, wine_y)
    K.fill_linear(c, wp, 0, wine_y, 0, 10, [(0, wine[0]), (1, wine[1])])
    c.restoreState()
    K.line(c, [(41.5, wine_y), (58.5, wine_y)], HEX("#B58C2E"), 0.9)
    K.hatch(c, outer, angle=-35, gap=1.5, col=GL_I, lw=0.24, depth=0.12, shadow=(0.8, -0.6), a=0.5)
    K.line(c, [(24, 30), (24, 56)], HEX("#FFFFFF"), 2.0)
    K.line(c, [(28, 26), (28, 40)], HEX("#FFFFFF"), 0.9)
    K.line(c, [(71, 46), (71, 24)], HEX("#FFFFFF"), 0.8)
    K.line(c, [(42.6, 118), (42.6, 90)], HEX("#FFFFFF"), 1.1)
    K.line(c, [(41.5, wine_y), (43.5, wine_y + 1.5), (56.5, wine_y + 1.5), (58.5, wine_y)], HEX("#B58C2E"), 0.8, pen=False)
    K.outline(c, inner, HEX("#6F8F7D"), 0.8)
    K.outline(c, outer, GL_I, 1.3)


class NeckCork(Art):
    name = "neck_cork"
    aspect = 1.45

    def draw(self, c):
        _bottle_neck(c)
        cp = K.path(c, [("M", 41.5, 101), ("L", 58.5, 101), ("L", 58.5, 134), ("L", 60, 138), ("C", 58, 141, 42, 141, 40, 138), ("L", 41.5, 134), ("Z",)])
        K.fill_linear(c, cp, 41, 0, 59, 0, [(0, CORK_M), (0.35, CORK_L), (1, CORK_D)]); K.outline(c, cp, K.INK_W, 1.2)
        for (x, y) in ((46, 108), (53, 112), (47, 118), (54, 123), (45, 128), (52, 131), (49, 105), (55, 117)):
            K.blob(c, x, y, 1.5, 0.8, 0, light=CORK_D, mid=CORK_D, dark=HEX("#5E4420"), ink=HEX("#5E4420"), lw=0.2)

    def _targets(self):
        return [("Closure", (50, 118), "R"), ("Headspace", (50, 96), "R"), ("Wine", (52, 40), "L"), ("Glass", (39.5, 108), "L")]


class NeckScrewcap(Art):
    name = "neck_screwcap"
    aspect = 1.45

    def draw(self, c):
        _bottle_neck(c)
        for y in (112, 108):
            K.line(c, [(38, y), (62, y)], GL_I, 0.7)
        cap = c.beginPath(); cap.roundRect(31, 111, 38, 29, 3)
        K.fill_linear(c, cap, 31, 0, 69, 0, [(0, STEEL_M), (0.25, STEEL_L), (0.6, STEEL_M), (1, STEEL_D)]); K.outline(c, cap, INK_S, 1.2)
        for x in range(35, 67, 4):
            K.line(c, [(x, 113), (x, 126)], STEEL_D, 0.8)
        K.line(c, [(31, 127), (69, 127)], INK_S, 0.9)
        K.line(c, [(33, 132), (67, 132)], HEX("#FFFFFF"), 1.4)


class NeckSynthetic(Art):
    name = "neck_synthetic"
    aspect = 1.45

    def draw(self, c):
        _bottle_neck(c)
        sp = K.path(c, [("M", 41.5, 100), ("L", 58.5, 100), ("L", 58.5, 134), ("L", 60.5, 137), ("C", 58, 142, 42, 142, 39.5, 137), ("L", 41.5, 134), ("Z",)])
        K.fill_linear(c, sp, 40, 0, 60, 0, [(0, HEX("#BDB9AB")), (0.35, HEX("#EEEBDF")), (1, HEX("#A6A294"))]); K.outline(c, sp, INK_S, 1.2)
        for y in (106, 112, 118, 124, 130):
            K.line(c, [(41.5, y), (58.5, y)], HEX("#8F8B7D"), 0.9)


class NeckGlassStopper(Art):
    name = "neck_glass"
    aspect = 1.45

    def draw(self, c):
        _bottle_neck(c)
        stem = c.beginPath(); stem.rect(43, 104, 14, 31)
        K.fill_linear(c, stem, 43, 0, 57, 0, [(0, HEX("#CFE6EF")), (0.4, HEX("#F4FAFC")), (1, HEX("#9DC3D3"))]); K.outline(c, stem, HEX("#2F5566"), 1.1)
        ring = c.beginPath(); ring.roundRect(41, 116, 18, 5, 2)
        K.fill_linear(c, ring, 41, 0, 59, 0, [(0, HEX("#6B7279")), (0.4, HEX("#9AA3AA")), (1, HEX("#3A3F44"))]); K.outline(c, ring, HEX("#15181B"), 1.0)
        head = c.beginPath(); head.roundRect(31, 134, 38, 10, 4)
        K.fill_linear(c, head, 31, 0, 69, 0, [(0, HEX("#CFE6EF")), (0.35, HEX("#F4FAFC")), (1, HEX("#9DC3D3"))]); K.outline(c, head, HEX("#2F5566"), 1.2)


# ===================================================================== must clarification (Chapter 16)
MUST_L, MUST_D = HEX("#F5E6A8"), HEX("#E5C867")
LEES_L, LEES_D = HEX("#A68455"), HEX("#5E4423")


def _tank_cutaway(c):
    """A stainless tank with a cut-away window; returns the window path (for clipping)."""
    _steel(c, 22, 20, 106, 104, r=11)
    _tank_trim(c, 22, 20, 106, 104, valve=False)
    win = K.rrect(c, 33, 31, 84, 82, 6)
    K.fill_linear(c, win, 0, 113, 0, 31, [(0, HEX("#FBF8EC")), (1, HEX("#F2EBD2"))])
    return win


def _tank_trim(c, x, y, w, h, valve=True):
    """Plinth, weld seams, rim bands and a racking valve, so a tank reads as real stainless equipment."""
    base = K.rrect(c, x - 3, y - 5, w + 6, 8, 2)
    K.fill_linear(c, base, 0, y + 3, 0, y - 5, [(0, STEEL_M), (1, STEEL_D)]); K.outline(c, base, INK_S, 1.0)
    for fx in (x + 3.6, x + w - 3.6):                                              # vertical weld seams on the side strips
        K.line(c, [(fx, y + 6), (fx, y + h - 6)], INK_S, 0.55, pen=False)
        for yy in range(int(y + 10), int(y + h - 8), 7):
            K.line(c, [(fx - 1.0, yy), (fx + 1.0, yy + 1.4)], HEX("#4A5258"), 0.4, pen=False)
    for fy in (y + h - 5.5, y + 5.5):                                              # horizontal rim bands
        K.line(c, [(x + 2, fy), (x + w - 2, fy)], HEX("#4A5258"), 0.5, pen=False)
        K.line(c, [(x + 2, fy + 1.0), (x + w - 2, fy + 1.0)], HEX("#FFFFFF"), 0.5, pen=False)
    if valve and w > 60:
        K.tube(c, [(x + w - 2, y + 14), (x + w + 8, y + 14)], 4.4, 4.4, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)
        K.blob(c, x + w + 9, y + 14, 3.2, 3.2, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.8)
        K.line(c, [(x + w + 9, y + 11), (x + w + 9, y + 17)], INK_S, 0.9, pen=False)


def _bubble(c, x, y, r):
    K.blob(c, x, y, r, r, 0, light=HEX("#FFFFFF"), mid=HEX("#E4EEF4"), dark=HEX("#9DB7C6"), ink=HEX("#5C7A8C"), lw=0.4)


class ClarSediment(Art):
    name = "sediment"
    aspect = 0.95

    def draw(self, c):
        win = _tank_cutaway(c)
        c.saveState(); c.clipPath(win, stroke=0, fill=0)
        liq = K.path(c, [("M", 33, 31), ("L", 117, 31), ("L", 117, 100), ("L", 33, 100), ("Z",)])
        K.fill_linear(c, liq, 0, 100, 0, 31, [(0, MUST_L), (1, MUST_D)])
        lees = K.path(c, [("M", 33, 31), ("L", 117, 31), ("L", 117, 52), ("C", 100, 55, 90, 49, 75, 53), ("C", 60, 57, 46, 50, 33, 54), ("Z",)])
        K.fill_linear(c, lees, 0, 56, 0, 31, [(0, LEES_L), (1, LEES_D)])
        K.stipple(c, lees, n=190, col=HEX("#2E1D0E"), r=0.5, seed=5, a=0.75)
        K.hatch(c, lees, angle=-30, gap=1.8, col=HEX("#2E1D0E"), lw=0.28, depth=0.9, a=0.5)
        K.stipple(c, liq, n=45, col=HEX("#B8913A"), r=0.35, seed=8, a=0.45)           # a few solids still settling
        c.restoreState()
        K.line(c, [(33, 100), (117, 100)], HEX("#B9923E"), 0.8, pen=False)
        for x in (23, 127):                                                          # chilling jacket
            for yy in range(30, 118, 8):
                K.line(c, [(x - 1.6, yy), (x, yy + 2.4), (x + 1.6, yy)], HEX("#2F7FB0"), 0.7, pen=False)
        K.outline(c, win, INK_S, 1.0)
        _steel(c, 120, 24, 22, 5, r=2)                                               # outlet valve
        K.blob(c, 140, 33, 3.4, 3.4, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.8)
        for k in range(3):
            K.line(c, [(133 + k * 3, 14), (133 + k * 3, 18)], HEX("#2F7FB0"), 0.6, pen=False)


class ClarFlotation(Art):
    name = "flotation"
    aspect = 0.95

    def draw(self, c):
        win = _tank_cutaway(c)
        c.saveState(); c.clipPath(win, stroke=0, fill=0)
        liq = K.path(c, [("M", 33, 31), ("L", 117, 31), ("L", 117, 104), ("L", 33, 104), ("Z",)])
        K.fill_linear(c, liq, 0, 104, 0, 31, [(0, MUST_L), (1, MUST_D)])
        cap = K.path(c, [("M", 33, 88), ("L", 117, 88), ("L", 117, 113), ("L", 33, 113), ("Z",)])
        K.fill_linear(c, cap, 0, 113, 0, 88, [(0, LEES_L), (1, HEX("#7B5B33"))])
        K.stipple(c, cap, n=170, col=HEX("#2E1D0E"), r=0.5, seed=12, a=0.75)
        for x in range(36, 116, 9):
            K.blob(c, x + (x % 3), 88 + (x % 4), 4.2, 3.0, 0, light=HEX("#B9976A"), mid=LEES_L, dark=LEES_D, ink=HEX("#2E1D0E"), lw=0.5)
        for (x, y, r) in ((45, 40, 2.2), (60, 55, 1.8), (75, 38, 2.6), (90, 62, 2.0), (66, 76, 2.4), (48, 70, 1.8), (100, 45, 2.3), (84, 80, 1.7),
                          (55, 90, 1.6), (105, 74, 2.1), (72, 62, 1.5), (40, 55, 1.6)):
            _bubble(c, x, y, r)
        c.restoreState()
        K.outline(c, win, INK_S, 1.0)
        _steel(c, 14, 40, 18, 5, r=2)                                                # gas inlet and stone
        K.blob(c, 38, 42.5, 3.4, 3.4, 0, light=HEX("#E6E6E0"), mid=HEX("#BDBDB3"), dark=HEX("#8A8A80"), ink=INK_S, lw=0.7)
        _steel(c, 100, 118, 40, 4, r=1.5)                                            # skimmer arm
        K.line(c, [(100, 120), (92, 108)], INK_S, 1.2, pen=False)


class ClarCentrifuge(Art):
    name = "centrifuge"
    aspect = 0.95

    def draw(self, c):
        _steel(c, 36, 8, 78, 16, r=4)                                                # base
        _steel(c, 66, 24, 18, 14, r=3, horizontal=False)                             # motor shaft housing
        cone = K.path(c, [("M", 44, 38), ("L", 106, 38), ("L", 118, 76), ("L", 32, 76), ("Z",)])
        K.fill_linear(c, cone, 32, 0, 118, 0, [(0, STEEL_M), (0.3, STEEL_L), (0.7, STEEL_M), (1, STEEL_D)])
        K.hatch(c, cone, angle=-38, gap=1.7, col=INK_S, lw=0.24, depth=0.3, a=0.55)
        K.outline(c, cone, INK_S, 1.2)
        _steel(c, 32, 76, 86, 30, r=8)                                               # bowl
        win = K.rrect(c, 40, 80, 70, 22, 4)
        K.fill_linear(c, win, 0, 102, 0, 80, [(0, HEX("#FBF8EC")), (1, HEX("#F2EBD2"))])
        c.saveState(); c.clipPath(win, stroke=0, fill=0)
        for k in range(9):                                                           # the stack of discs
            x = 42 + k * 8
            K.line(c, [(x, 80), (x + 7, 102)], INK_S, 1.0, pen=False)
        c.restoreState()
        K.outline(c, win, INK_S, 0.9)
        K.tube(c, [(75, 106), (75, 130)], 6, 6, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=1.0, hi=0.5, shade=0.4, grain=False)   # feed pipe
        for yy in (122, 116):
            K.line(c, [(75, yy), (71, yy + 4)], HEX("#B9923E"), 1.0, pen=False)
        K.tube(c, [(118, 90), (136, 94)], 5, 5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=1.0, hi=0.5, shade=0.4, grain=False)   # clear juice out
        K.blob(c, 138, 86, 2.0, 3.0, 0, light=MUST_L, mid=MUST_D, dark=HEX("#B9923E"), ink=HEX("#8A6A1E"), lw=0.5)
        K.tube(c, [(36, 56), (18, 50)], 5, 5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=1.0, hi=0.5, shade=0.4, grain=False)    # solids out
        K.blob(c, 12, 46, 6, 4.4, 0, light=LEES_L, mid=HEX("#7B5B33"), dark=LEES_D, ink=HEX("#2E1D0E"), lw=0.8)


# ===================================================================== four ways to concentrate the must (Chapter 17)
def _raisin(c, x, y, r):
    p = K.ellipse_path(c, x, y, r * 0.95, r * 0.80, (x * 13) % 60 - 30)
    K.fill_radial(c, p, x - r * 0.3, y + r * 0.3, r * 1.6, [(0, HEX("#7A4A58")), (0.55, HEX("#4A2638")), (1, HEX("#241018"))])
    for k in (-1, 0, 1):                                            # the wrinkles of a dried berry
        K.line(c, [(x - r * 0.7, y + k * r * 0.35), (x - r * 0.1, y + k * r * 0.45 + 0.3), (x + r * 0.7, y + k * r * 0.30)], HEX("#120810"), 0.4, pen=False)
    K.outline(c, p, HEX("#1B0C16"), 0.7)


def _botrytis(c, x, y, r):
    p = K.ellipse_path(c, x, y, r * 0.95, r * 0.88, 0)
    K.fill_radial(c, p, x - r * 0.3, y + r * 0.3, r * 1.6, [(0, HEX("#B8A27A")), (0.55, HEX("#8A7552")), (1, HEX("#4F4029"))])
    K.stipple(c, p, n=int(r * 9), col=HEX("#E9E6DC"), r=0.42, seed=int(x * 7 + y), a=0.9)
    K.line(c, [(x - r * 0.6, y + 0.2), (x, y - r * 0.35), (x + r * 0.6, y + 0.1)], HEX("#4F4029"), 0.4, pen=False)
    K.outline(c, p, HEX("#3C3020"), 0.6)


def _frozen(c, x, y, r):
    K.berry(c, x, y, r)
    c.saveState(); c.setFillColor(colors_.Color(0.88, 0.95, 1.0, alpha=0.55)); c.ellipse(x - r, y - r, x + r, y + r, stroke=0, fill=1); c.restoreState()
    K.line(c, [(x - r * 0.5, y + r * 0.5), (x + r * 0.1, y + r * 0.8)], HEX("#FFFFFF"), 0.8, pen=False)


from reportlab.lib import colors as colors_


def _cane_top(c, W, y, leafcol=None):
    """A one-year cane: gently wavy, with swollen nodes, short laterals and a tendril."""
    n = 26
    cen = [(6 + (W - 12) * i / float(n - 1), y + 3 + 3.2 * math.sin(i * 0.33) - 2.0 * (i / float(n))) for i in range(n)]
    wid = [5.6 - 1.2 * i / float(n) + (1.1 if i % 5 == 2 else 0.0) for i in range(n)]
    K.tube(c, cen, wid, None, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.1, hi=0.5, shade=0.4)
    for i in (2, 7, 12, 17, 22):                                         # nodes
        x_, y_ = cen[i]
        nd = K.ellipse_path(c, x_, y_, 2.4, 3.6, 0)
        K.fill_radial(c, nd, x_ - 0.5, y_ + 0.8, 4.0, [(0, K.WOOD_L), (1, K.WOOD_D)]); K.outline(c, nd, K.INK_W, 0.7)
    tx, ty = cen[20]
    cur = [(tx + 0.9 * i * math.cos(i * 0.62 + 3.0), ty - 1.0 - 0.9 * i * math.sin(i * 0.62 + 3.0) * 0.6) for i in range(0, 14)]
    K.line(c, cur, K.INK_G, 0.7, taper=True)


class ConcOnVine(Art):
    name = "on_vine"
    aspect = 1.18

    def draw(self, c):
        W, H = self.W, self.H
        _cane_top(c, W, H - 24)
        for (x, sd) in ((22, 1), (96, -1)):                          # yellowing autumn leaves
            K.leaf(c, x, H - 34, 17, rot=sd * 12, flip=sd < 0, light=HEX("#F3E08A"), mid=HEX("#D6A53A"), dark=HEX("#9C6A1E"), ink=HEX("#5E4216"), stalk=False)
        K.bunch(c, W * 0.5, H - 28, 44, 78, rows=(4, 5, 4, 4, 3, 2, 1), berry_fn=_raisin)
        K.line(c, [(W * 0.42, H - 24), (W * 0.46, H - 31)], K.INK_W, 1.4, pen=False)


class ConcOffVine(Art):
    name = "off_vine"
    aspect = 1.18

    def draw(self, c):
        W, H = self.W, self.H
        for xr in (10, W - 14):                                       # rack uprights
            K.tube(c, [(xr, 6), (xr, H - 14)], 5, 5, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.0, hi=0.5, shade=0.4)
        for (yy, n) in ((20, 2), (70, 2)):                           # two trays, each holding bunches laid on their sides
            tray = K.rrect(c, 6, yy, W - 12, 7, 2)
            K.fill_linear(c, tray, 0, yy + 7, 0, yy, [(0, K.WOOD_L), (1, K.WOOD_D)]); K.outline(c, tray, K.INK_W, 1.1)
            for k in range(n):
                c.saveState(); c.translate(18 + k * 46, yy + 19); c.rotate(90)
                K.bunch(c, 0, 0, 24, 34, rows=(3, 4, 3, 3, 2, 1), seed=k + yy, berry_fn=None)
                c.restoreState()
        tray3 = K.rrect(c, 6, 118, W - 12, 7, 2)
        K.fill_linear(c, tray3, 0, 125, 0, 118, [(0, K.WOOD_L), (1, K.WOOD_D)]); K.outline(c, tray3, K.INK_W, 1.1)


class ConcNobleRot(Art):
    name = "noble_rot"
    aspect = 1.18

    def draw(self, c):
        W, H = self.W, self.H
        _cane_top(c, W, H - 24)
        K.leaf(c, 20, H - 36, 15, rot=10, light=HEX("#B9D08A"), mid=HEX("#7E9648"), dark=HEX("#4F6128"), stalk=False)
        K.bunch(c, W * 0.5, H - 28, 46, 80, rows=(4, 5, 4, 4, 3, 2, 1), berry_fn=_botrytis)
        for (x, y) in ((16, 30), (100, 44), (30, 60), (88, 20)):      # a morning mist
            K.line(c, [(x - 9, y), (x - 3, y + 1.6), (x + 3, y - 1.0), (x + 9, y + 0.6)], HEX("#B8C6D0"), 0.8, pen=False)


class ConcFrozen(Art):
    name = "frozen"
    aspect = 1.18

    def draw(self, c):
        W, H = self.W, self.H
        bg = K.rrect(c, 0, 0, W, H, 4)
        K.fill_linear(c, bg, 0, H, 0, 0, [(0, HEX("#DCE9F4")), (1, HEX("#F6FAFD"))])
        for (x, y) in ((14, 118), (98, 124), (30, 96), (104, 92), (60, 130)):
            for a in (0, 60, 120):
                r = 3.0
                K.line(c, [(x - r * math.cos(math.radians(a)), y - r * math.sin(math.radians(a))),
                           (x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a)))], HEX("#9DBBD0"), 0.6, pen=False)
        _cane_top(c, W, H - 24)
        snow = K.ellipse_path(c, W * 0.5, H - 20, 42, 5, 0)
        K.fill_radial(c, snow, W * 0.45, H - 17, 40, [(0, HEX("#FFFFFF")), (1, HEX("#DCE9F4"))]); K.outline(c, snow, HEX("#8FB0C8"), 0.8)
        K.bunch(c, W * 0.5, H - 28, 44, 76, rows=(4, 5, 4, 4, 3, 2, 1), berry_fn=_frozen)
        for (x, y0, ln) in ((46, 44, 9), (58, 38, 12), (70, 46, 8), (52, 30, 7)):      # icicles
            ic = K.poly(c, [(x - 2, y0), (x + 2, y0), (x, y0 - ln)])
            K.fill_linear(c, ic, 0, y0, 0, y0 - ln, [(0, HEX("#FFFFFF")), (1, HEX("#AFCFE6"))]); K.outline(c, ic, HEX("#6FA6C9"), 0.6)


# ===================================================================== red fermentation: cap management and extraction (Chapter 18)
RED_L, RED_D = HEX("#8A2C48"), HEX("#3E1224")
HOSE_L, HOSE_M = HEX("#8A9096"), HEX("#3F454B")


def _red_tank(c, x=18, y=10, w=84, h=100, cap=True, level=0.9, liq=None):
    _steel(c, x, y, w, h, r=9)
    _tank_trim(c, x, y, w, h)
    win = K.rrect(c, x + 8, y + 6, w - 16, h - 12, 5)
    K.fill_linear(c, win, 0, y + h, 0, y, [(0, HEX("#FBF8EC")), (1, HEX("#F2EBD2"))])
    c.saveState(); c.clipPath(win, stroke=0, fill=0)
    top = y + 6 + (h - 12) * level
    liqp = K.path(c, [("M", x, y), ("L", x + w, y), ("L", x + w, top), ("L", x, top), ("Z",)])
    K.fill_linear(c, liqp, 0, top, 0, y, [(0, (liq or (RED_L, RED_D))[0]), (1, (liq or (RED_L, RED_D))[1])])
    if cap:
        capp = K.path(c, [("M", x, top - 15), ("L", x + w, top - 15), ("L", x + w, top + 2), ("L", x, top + 2), ("Z",)])
        K.fill_linear(c, capp, 0, top + 2, 0, top - 15, [(0, HEX("#2B0E1C")), (1, HEX("#4A1A2E"))])
        K.stipple(c, capp, n=130, col=HEX("#B07A92"), r=0.5, seed=int(x + y), a=0.7)
        K.stipple(c, capp, n=60, col=HEX("#E3C9D3"), r=0.35, seed=int(x * 3 + y), a=0.6)
    c.restoreState()
    K.outline(c, win, INK_S, 0.9)
    return win, top


class CapPunch(Art):
    name = "punch"
    aspect = 1.18

    def draw(self, c):
        win, top = _red_tank(c)
        K.tube(c, [(60, 132), (60, top - 2)], 4.5, 4.5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=1.0, hi=0.5, shade=0.4, grain=False)
        _steel(c, 46, 126, 28, 4.5, r=2)
        _steel(c, 40, top - 8, 40, 6, r=2)                                   # the plunger plate, pushing the cap down
        _arrow(c, [(92, top + 12), (92, top - 14)], HEX("#8A1F3C"), 1.8)


class CapPump(Art):
    name = "pump"
    aspect = 1.18

    def draw(self, c):
        win, top = _red_tank(c, x=34, w=78)
        K.tube(c, [(34, 28), (14, 28), (14, 128), (62, 128), (74, 120)], 4.5, 4.5, HOSE_M, light=HOSE_L, dark=HOSE_M, ink=PIPE_I, lw=0.9,
               hi=0.5, shade=0.4, grain=False)
        _steel(c, 3, 22, 14, 12, r=3)                                        # the pump
        K.blob(c, 10, 28, 3.0, 3.0, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.7)
        for k in range(-3, 4):                                               # liquid sprayed over the cap
            _drop_red(c, 74 + k * 5.2, top + 14 - abs(k) * 1.0, 0.9)
            _drop_red(c, 74 + k * 4.0, top + 22 - abs(k) * 0.8, 0.8)


def _drop_red(c, x, y, s=1.0):
    K.blob(c, x, y, 1.6 * s, 2.4 * s, 0, light=HEX("#C0506E"), mid=HEX("#8A2C48"), dark=HEX("#3E1224"), ink=HEX("#2A0C18"), lw=0.4)


class CapRack(Art):
    name = "rack"
    aspect = 1.18

    def draw(self, c):
        _red_tank(c, x=4, y=10, w=52, h=88, cap=True, level=0.30)           # wine drained, the cap sunk
        _red_tank(c, x=66, y=10, w=52, h=88, cap=False, level=0.85)           # the holding vessel
        K.tube(c, [(4, 26), (0, 26), (0, 118), (92, 118), (92, 104)], 4.5, 4.5, HOSE_M, light=HOSE_L, dark=HOSE_M, ink=PIPE_I, lw=0.9, hi=0.5, shade=0.4, grain=False)
        _arrow(c, [(40, 125), (62, 125)], HEX("#8A1F3C"), 1.6)


class CapRotary(Art):
    name = "rotary"
    aspect = 1.18

    def draw(self, c):
        for x in (26, 94):                                                    # roller supports
            _steel_poly(c, [(x - 12, 8), (x + 12, 8), (x + 6, 34), (x - 6, 34)], horizontal=False)
            K.blob(c, x, 36, 7, 7, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=1.0)
        _steel(c, 6, 38, 108, 66, r=30)
        win = K.rrect(c, 16, 46, 88, 50, 22)
        K.fill_linear(c, win, 0, 96, 0, 46, [(0, HEX("#FBF8EC")), (1, HEX("#F2EBD2"))])
        c.saveState(); c.clipPath(win, stroke=0, fill=0)
        liq = K.path(c, [("M", 16, 46), ("L", 104, 46), ("L", 104, 80), ("L", 16, 80), ("Z",)])
        K.fill_linear(c, liq, 0, 80, 0, 46, [(0, RED_L), (1, RED_D)])
        K.stipple(c, liq, n=120, col=HEX("#B07A92"), r=0.45, seed=19, a=0.7)
        for ang in (25, 115):                                                 # internal blades
            a = math.radians(ang)
            K.line(c, [(60 - 40 * math.cos(a), 71 - 24 * math.sin(a)), (60 + 40 * math.cos(a), 71 + 24 * math.sin(a))], INK_S, 2.0, pen=False)
        c.restoreState()
        K.outline(c, win, INK_S, 0.9)
        arc = [(60 + 54 * math.cos(math.radians(a)), 71 + 40 * math.sin(math.radians(a))) for a in range(20, 160, 10)]
        _arrow(c, arc[::-1][:-1] + [arc[0]] if False else arc[::-1], HEX("#8A1F3C"), 1.6)


class ExtractionCurves(Art):
    """Colour and tannin extraction across the stages of a red ferment (a schematic graph)."""
    name = "extraction"
    aspect = 0.52
    vis = (0.0, 1.0)

    def draw(self, c):
        W, H = self.W, self.H
        x0, x1, y0, y1 = 28.0, W - 14.0, 22.0, H - 14.0
        K.line(c, [(x0, y1), (x0, y0), (x1, y0)], INK_S, 1.2, pen=False)
        for fx in (0.33, 0.66):                                              # stage boundaries
            xx = x0 + (x1 - x0) * fx
            c.saveState(); c.setStrokeColor(HEX("#9AA3AA")); c.setLineWidth(0.6); c.setDash(2, 2); c.line(xx, y0, xx, y1); c.restoreState()
        c.setFont("Sans", 6.8); c.setFillColor(K.INK_W)
        for (fx, t) in ((0.165, "Before fermentation"), (0.495, "Alcoholic fermentation"), (0.83, "After fermentation")):
            c.drawCentredString(x0 + (x1 - x0) * fx, 10, t)
        c.saveState(); c.translate(11, (y0 + y1) / 2); c.rotate(90); c.drawCentredString(0, 0, "Amount extracted"); c.restoreState()
        n = 40
        ant = [(x0 + (x1 - x0) * t / n, y0 + (y1 - y0) * (0.92 * (1 - math.exp(-5.2 * t / n)) ** 0.9) * (1.0 if t / n < 0.66 else 1.0 - 0.14 * (t / n - 0.66) / 0.34)) for t in range(n + 1)]
        tan = [(x0 + (x1 - x0) * t / n, y0 + (y1 - y0) * (0.03 + 0.9 * (t / n) ** 2.1)) for t in range(n + 1)]
        K.line(c, ant, HEX("#7A1E3A"), 2.2, taper=False)
        K.line(c, tan, HEX("#8A6A2E"), 2.2, taper=False)

    def _targets(self):
        W, H = self.W, self.H
        x0, x1, y0, y1 = 28.0, W - 14.0, 22.0, H - 14.0
        return [("Anthocyanins (color)", (x0 + (x1 - x0) * 0.2, y0 + (y1 - y0) * (0.92 * (1 - math.exp(-5.2 * 0.2)) ** 0.9)), "L"),
                ("Tannin", (x0 + (x1 - x0) * 0.85, y0 + (y1 - y0) * (0.03 + 0.9 * 0.85 ** 2.1)), "R")]


# ===================================================================== three ways to make rose (Chapter 19)
import wb_art as _A


class RoseDirect(_A.PressBasket):
    """Direct pressing: black grapes straight to the press, a pale pink juice running out."""
    name = "rose_direct"

    def draw(self, c):
        old = (_A.JUICE_L, _A.JUICE_D)
        _A.JUICE_L, _A.JUICE_D = HEX("#F6D2CC"), HEX("#E39A9A")
        try:
            _A.PressBasket.draw(self, c)
        finally:
            _A.JUICE_L, _A.JUICE_D = old
        K.bunch(c, 18, 104, 22, 40, rows=(3, 3, 3, 2, 1), seed=2)


class RoseShortMac(Art):
    """Short maceration: crushed black grapes soaking on their skins for hours to days; the juice is already tinted."""
    name = "rose_shortmac"
    aspect = 0.95

    def draw(self, c):
        win, top = _red_tank(c, liq=(HEX("#EDA6AC"), HEX("#C26A7A")), level=0.86)
        cx, cy = 118, 122                                                    # a clock: time on the skins
        K.blob(c, cx, cy, 12, 12, 0, light=HEX("#FFFFFF"), mid=HEX("#F3EFE4"), dark=HEX("#C9C2B0"), ink=INK_S, lw=1.1)
        for a in range(0, 360, 30):
            r0, r1 = (9.0, 10.8)
            K.line(c, [(cx + r0 * math.cos(math.radians(a)), cy + r0 * math.sin(math.radians(a))),
                       (cx + r1 * math.cos(math.radians(a)), cy + r1 * math.sin(math.radians(a)))], INK_S, 0.6, pen=False)
        K.line(c, [(cx, cy), (cx, cy + 7)], INK_S, 1.2, pen=False)
        K.line(c, [(cx, cy), (cx + 5, cy - 3)], INK_S, 1.2, pen=False)


class RoseBlend(Art):
    """Blending: a little red wine poured into much more white wine."""
    name = "rose_blend"
    aspect = 0.95

    def draw(self, c):
        win, top = _red_tank(c, x=36, w=84, cap=False, level=0.82, liq=(HEX("#F2BDB6"), HEX("#F6E8C8")))
        K.line(c, [(35, 100), (122, 100)], HEX("#B58C2E"), 0.8, pen=False)
        c.saveState(); c.translate(19, 126); c.rotate(-128)                   # a small carafe of red wine, tipping to pour
        body = K.path(c, [("M", -9, -16), ("L", 9, -16), ("L", 9, 4), ("L", 4, 10), ("L", 4, 18), ("L", 5, 20), ("L", -5, 20), ("L", -4, 18), ("L", -4, 10), ("L", -9, 4), ("Z",)])
        K.fill_linear(c, body, -9, 0, 9, 0, [(0, HEX("#D7E8E0")), (0.4, HEX("#F6FBF8")), (1, HEX("#9DBDAE"))])
        wine = K.path(c, [("M", -8, -15), ("L", 8, -15), ("L", 8, 3), ("L", 3, 9), ("L", -3, 9), ("L", -8, 3), ("Z",)])
        K.fill_linear(c, wine, 0, 3, 0, -15, [(0, HEX("#8A2C48")), (1, HEX("#5A1A2E"))])
        K.outline(c, body, GL_I, 1.0)
        c.restoreState()
        K.line(c, [(34, 116), (38, 110), (42, 103)], HEX("#6A1F38"), 2.4, taper=False)            # the stream of red wine
        K.blob(c, 46, 97, 7, 3.2, -10, light=HEX("#D98A9A"), mid=HEX("#C0607A"), dark=HEX("#9A3A58"), ink=HEX("#7A2A44"), lw=0.5)
        K.line(c, [(40, 95), (56, 94), (66, 96)], HEX("#B8586F"), 0.7, pen=False)


# ===================================================================== dealcoholization (Chapter 20)
WINE_L, WINE_D = HEX("#F0D98A"), HEX("#D2AC4A")
PERM_L, PERM_D = HEX("#EAF4F8"), HEX("#BFD8E4")


class DealcRO(Art):
    """Reverse osmosis: wine pumped at pressure along a membrane; a pale alcohol/water permeate passes through."""
    name = "ro"
    aspect = 0.95

    def draw(self, c):
        _steel(c, 34, 46, 90, 50, r=10)
        win = K.rrect(c, 42, 54, 74, 34, 5)
        K.fill_linear(c, win, 0, 88, 0, 54, [(0, HEX("#FBF8EC")), (1, HEX("#F2EBD2"))])
        c.saveState(); c.clipPath(win, stroke=0, fill=0)
        left = K.path(c, [("M", 42, 54), ("L", 77, 54), ("L", 77, 88), ("L", 42, 88), ("Z",)])
        K.fill_linear(c, left, 0, 88, 0, 54, [(0, WINE_L), (1, WINE_D)])
        right = K.path(c, [("M", 80, 54), ("L", 116, 54), ("L", 116, 88), ("L", 80, 88), ("Z",)])
        K.fill_linear(c, right, 0, 88, 0, 54, [(0, PERM_L), (1, PERM_D)])
        c.restoreState()
        mem = K.rrect(c, 76.5, 52, 4, 38, 1.5)                                  # the membrane
        K.fill_linear(c, mem, 76, 0, 81, 0, [(0, HEX("#6B5A3C")), (1, HEX("#3A2E1C")), ])
        K.stipple(c, mem, n=26, col=HEX("#E9E2C8"), r=0.4, seed=3, a=0.9)
        K.outline(c, mem, K.INK_W, 0.8)
        K.outline(c, win, INK_S, 0.9)
        for (x, y) in ((88, 70), (98, 62), (104, 78), (94, 82)):                  # small molecules that pass through
            K.blob(c, x, y, 1.6, 1.6, 0, light=HEX("#FFFFFF"), mid=HEX("#CFE3EC"), dark=HEX("#8FB3C6"), ink=HEX("#5C7A8C"), lw=0.4)
        _steel(c, 6, 66, 24, 12, r=5)                                          # the pump and feed
        K.blob(c, 18, 72, 4.0, 4.0, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.8)
        K.tube(c, [(30, 72), (34, 72)], 5, 5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)
        _arrow(c, [(8, 90), (8, 104), (30, 104)], HEX("#8A6A1E"), 1.4)
        K.tube(c, [(100, 96), (100, 116)], 5, 5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)
        _arrow(c, [(100, 118), (100, 130)], HEX("#4F86A3"), 1.6)                  # permeate out
        K.tube(c, [(50, 46), (50, 30), (24, 30)], 5, 5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)


class DealcVacuum(Art):
    """Vacuum distillation: wine warmed in a boiler under vacuum; alcohol vapor rises to a condenser."""
    name = "vacuum"
    aspect = 0.95

    def draw(self, c):
        _steel(c, 34, 10, 66, 38, r=9)                                          # boiler
        win = K.rrect(c, 41, 15, 52, 28, 4)
        K.fill_linear(c, win, 0, 43, 0, 15, [(0, WINE_L), (1, WINE_D)]); K.outline(c, win, INK_S, 0.9)
        for k in range(4):                                                      # heat
            x = 42 + k * 14
            K.line(c, [(x, 4), (x - 2, 7), (x + 2, 9), (x, 12)], HEX("#D9822B"), 1.0, pen=False)
        K.tube(c, [(67, 48), (67, 92)], 14, 14, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=1.1, hi=0.5, shade=0.4, grain=False)   # column
        for yy in (62, 74, 86):
            _arrow(c, [(67, yy), (67, yy + 8)][::-1], HEX("#8A6A8A"), 1.0)
        _steel(c, 44, 92, 46, 26, r=6)                                          # condenser with a coil
        cw = K.rrect(c, 50, 97, 34, 16, 3)
        K.fill_linear(c, cw, 0, 113, 0, 97, [(0, PERM_L), (1, PERM_D)])
        for k in range(5):
            K.line(c, [(52 + k * 7, 99), (55 + k * 7, 111)], HEX("#2F7FB0"), 1.2, pen=False)
        K.outline(c, cw, INK_S, 0.8)
        K.tube(c, [(90, 106), (110, 106), (110, 90)], 4, 4, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)
        _steel(c, 104, 70, 24, 20, r=5)                                          # the vacuum pump
        K.blob(c, 116, 80, 5, 5, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.9)
        K.tube(c, [(44, 104), (26, 104), (26, 78)], 4, 4, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)
        bk = K.path(c, [("M", 14, 52), ("L", 38, 52), ("L", 34, 22), ("L", 18, 22), ("Z",)])   # receiver for the distilled alcohol
        K.fill_linear(c, bk, 0, 52, 0, 22, [(0, HEX("#F4FAFC")), (1, HEX("#D6E6EE"))]); K.outline(c, bk, GL_I, 1.0)
        K.line(c, [(17, 28), (35, 28)], HEX("#5C7A8C"), 0.6, pen=False)


class DealcCone(Art):
    """Spinning cone column: a thin film of wine runs over stacked cones; aroma, then alcohol, are stripped off."""
    name = "cone"
    aspect = 0.95

    def draw(self, c):
        _steel(c, 40, 10, 66, 118, r=10)
        win = K.rrect(c, 48, 16, 50, 106, 6)
        K.fill_linear(c, win, 0, 122, 0, 16, [(0, HEX("#FBF8EC")), (1, HEX("#F2EBD2"))])
        c.saveState(); c.clipPath(win, stroke=0, fill=0)
        K.line(c, [(73, 122), (73, 16)], INK_S, 2.0, pen=False)                    # central shaft
        for k in range(5):
            y = 104 - k * 20
            fixed = K.poly(c, [(48, y + 8), (73, y - 8), (98, y + 8)], close=False)          # fixed cone from the wall
            K.line(c, [(48, y + 8), (73, y - 8), (98, y + 8)], STEEL_D, 1.6, pen=False)
            K.line(c, [(60, y - 4), (73, y + 4), (86, y - 4)][::-1], HEX("#6B7279"), 1.2, pen=False)   # spinning cone on the shaft
            K.line(c, [(50, y + 6.6), (73, y - 6.8), (96, y + 6.6)], WINE_D, 0.9, pen=False)        # the thin film of wine
        c.restoreState()
        K.outline(c, win, INK_S, 0.9)
        K.tube(c, [(73, 128), (73, 140)], 5, 5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)
        _arrow(c, [(73, 142), (73, 134)], HEX("#8A6A1E"), 1.4)                    # wine in at the top
        K.tube(c, [(106, 112), (130, 112)], 5, 5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)
        K.tube(c, [(106, 62), (130, 62)], 5, 5, STEEL_M, light=STEEL_L, dark=STEEL_D, ink=INK_S, lw=0.9, hi=0.5, shade=0.4, grain=False)
        _arrow(c, [(122, 110), (136, 110)], HEX("#8A6A8A"), 1.4)
        _arrow(c, [(122, 60), (136, 60)], HEX("#4F86A3"), 1.4)
        _arrow(c, [(73, 8), (73, 0)], HEX("#8A6A1E"), 1.4)


# ===================================================================== machine against hand harvest (Chapter 21)
class HarvestMachine(Art):
    """A straddle harvester over a trellised row: bow rods shake the canopy, a conveyor lifts the fruit to a hopper."""
    name = "harvest_machine"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        _ground(c, W)
        for xp in (6, W - 6):
            K.tube(c, [(xp, 8), (xp, 106)], 4, 4, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.0, hi=0.5, shade=0.4)
        _vine(c, W / 2.0, 9, th=30, ch=48, spread=18, R=5.4, seed=4)
        for x in (24, W - 24):                                                       # the wheels
            K.blob(c, x, 22, 17, 17, 0, light=HEX("#4A4F55"), mid=HEX("#2A2E32"), dark=HEX("#0F1214"), ink=HEX("#0A0C0E"), lw=1.2)
            K.blob(c, x, 22, 7, 7, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.9)
        _steel(c, 14, 36, 14, 78, r=4, horizontal=False)                              # the frame
        _steel(c, W - 28, 36, 14, 78, r=4, horizontal=False)
        _steel(c, 14, 104, W - 28, 14, r=5)
        for sd in (-1, 1):                                                           # bow rods striking the canopy
            for k in range(4):
                y = 52 + k * 9
                x0 = (28 if sd < 0 else W - 28)
                K.line(c, K.bezier((x0, y), (x0 + sd * 8, y + 6), (x0 + sd * 14, y + 4), (x0 + sd * 20, y - 4), n=10), HEX("#C9A84A"), 1.2, pen=False)
        belt = K.poly(c, [(W - 40, 28), (W - 28, 24), (W - 14, 70), (W - 26, 74)])
        K.fill_linear(c, belt, 0, 74, 0, 24, [(0, HEX("#4A4F55")), (1, HEX("#2A2E32"))]); K.outline(c, belt, INK_S, 1.0)
        _steel(c, W - 22, 68, 18, 16, r=3)
        K.blob(c, W - 13, 90, 6, 4, 0, light=K.BERRY_L, mid=K.BERRY_M, dark=K.BERRY_D, ink=K.INK_P, lw=0.7)


def _shoot_with_leaves_(c, ctr):
    import wb_art as _A
    _A._shoot_with_leaves(c, ctr, (0.2, 0.45, 0.7, 0.92), R=4.2)


class HarvestHand(Art):
    """Hand harvest: bunches cut with secateurs into a small, shallow crate."""
    name = "harvest_hand"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        K.tube(c, [(0, H - 12), (W * 0.35, H - 16), (W * 0.7, H - 14), (W, H - 18)], 6, 5, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.1, hi=0.5, shade=0.4)
        K.leaf(c, 24, H - 30, 18, rot=8, stalk=False)
        K.leaf(c, W - 24, H - 30, 17, rot=-6, flip=True, stalk=False)
        K.bunch(c, W * 0.5, H - 20, 34, 52, rows=(4, 4, 3, 3, 2, 1))                    # the bunch about to be cut
        K.line(c, [(W * 0.5, H - 14), (W * 0.5, H - 22)], K.INK_W, 1.6, pen=False)
        for (ax, ay, rot) in ((W * 0.5 - 14, H - 22, 20), (W * 0.5 + 14, H - 22, -20)):      # secateurs
            c.saveState(); c.translate(ax, ay); c.rotate(rot)
            blade = K.poly(c, [(-2, 0), (2, 0), (1.2, 14), (-0.6, 15)])
            K.fill_linear(c, blade, -2, 0, 2, 0, [(0, STEEL_M), (0.4, STEEL_L), (1, STEEL_D)]); K.outline(c, blade, INK_S, 0.8)
            K.line(c, [(0, 0), (0, -14)], HEX("#B2253A"), 3.0, taper=False)
            K.line(c, [(0, 0), (0, -14)], HEX("#E6677A"), 1.0, pen=False)
            c.restoreState()
        crate = K.rrect(c, 12, 6, W - 24, 42, 3)                                       # a small, shallow crate
        K.fill_linear(c, crate, 12, 0, W - 12, 0, [(0, K.WOOD_L), (0.5, HEX("#B98E5E")), (1, K.WOOD_D)])
        for yy in (14, 26, 38):
            K.line(c, [(12, yy), (W - 12, yy)], K.WOOD_D, 0.9, pen=False)
        K.hatch(c, crate, angle=-35, gap=2.2, col=K.WOOD_D, lw=0.28, depth=0.28, shadow=(0.3, -1.0), a=0.5)
        K.outline(c, crate, K.INK_W, 1.3)
        for k, bx in enumerate((W * 0.3, W * 0.5, W * 0.7)):
            c.saveState(); c.translate(bx, 50); c.rotate(-90 + (k - 1) * 14)
            K.bunch(c, 0, 0, 20, 30, rows=(3, 3, 2, 2, 1), seed=k)
            c.restoreState()
