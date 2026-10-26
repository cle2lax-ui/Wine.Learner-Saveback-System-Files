# -*- coding: utf-8 -*-
"""Artwork for the workbook's label-the-diagram exercises, drawn in the house style (wb_ink.py).

Each `Art` exposes:
    draw(c)     paints the unlabelled artwork into a W x H box at the origin
    targets     [(name, (x, y), side)] -- the point on the art each label refers to ("L" or "R")
    vis         horizontal extent actually painted, as fractions of W (used to centre / clip the art)
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wb_ink as K

HEX = K.HEX


class Art:
    name = ""
    aspect = 0.62          # height / width of the art box
    vis = (0.0, 1.0)

    def __init__(self, W=270.0):
        self.W, self.H = W, W * self.aspect
        self.s = W / 330.0           # scale for absolute-pt details (line weights stay fixed)
        self.targets = self._targets()

    def draw(self, c):
        raise NotImplementedError

    def _targets(self):
        return []


def seed(c, cx, cy, r, rot=0.0):
    """A pear-shaped grape seed, beak pointing along +y before rotation."""
    c.saveState()
    c.translate(cx, cy); c.rotate(rot)
    p = K.path(c, [("M", 0, r * 1.45), ("C", r * 0.55, r * 0.95, r * 0.98, -r * 0.1, r * 0.58, -r * 0.88),
                   ("C", r * 0.25, -r * 1.22, -r * 0.25, -r * 1.22, -r * 0.58, -r * 0.88),
                   ("C", -r * 0.98, -r * 0.1, -r * 0.55, r * 0.95, 0, r * 1.45), ("Z",)])
    K.fill_radial(c, p, -r * 0.25, r * 0.35, r * 1.7, [(0, HEX("#C9A06A")), (0.5, HEX("#8A5E32")), (1, HEX("#4F3219"))])
    K.outline(c, p, K.INK_W, 1.1)
    K.flat(c, K.ellipse_path(c, 0, -r * 0.55, r * 0.17, r * 0.17), HEX("#2F1D0E"))
    c.restoreState()


# ===================================================================== grape
class Grape(Art):
    """The grape in cross-section: bloom, skin, pulp, seeds, and the stem."""
    name = "grape"
    aspect = 0.64
    vis = (0.02, 0.48)

    def _geom(self):
        W, H = self.W, self.H
        return 0.25 * W, 0.45 * H, 0.185 * W, 0.185 * W * 1.06

    def draw(self, c):
        W, H = self.W, self.H
        cx, cy, R, ry = self._geom()
        # stem first, so the berry overlaps its foot
        ctr = K.bezier((cx, cy + ry * 0.90), (cx + 2, cy + ry + 0.05 * H), (cx - 4, cy + ry + 0.12 * H), (cx - 2, 0.985 * H), n=24)
        K.tube(c, ctr, 0.040 * W, 0.030 * W, K.G_MID, light=HEX("#CDE7AE"), dark=K.G_DEEP, ink=K.INK_G, lw=1.4, hi=0.5)
        # bloom: a soft bluish-white haze around the skin
        c.saveState()
        for i in range(7):
            k = i / 6.0
            c.setFillColor(colors_alpha(HEX("#E6EAF4"), 0.10))
            c.ellipse(cx - R * (1.03 + k * 0.14), cy - ry * (1.03 + k * 0.14), cx + R * (1.03 + k * 0.14),
                      cy + ry * (1.03 + k * 0.14), stroke=0, fill=1)
        c.restoreState()
        # skin
        skin = K.ellipse_path(c, cx, cy, R, ry)
        K.fill_radial(c, skin, cx - 0.35 * R, cy + 0.40 * ry, 1.7 * R, [(0, K.BERRY_L), (0.45, K.BERRY_M), (1, K.BERRY_D)])
        K.hatch(c, skin, angle=-40, gap=1.5, col=K.INK_P, lw=0.3, depth=0.30, a=0.65)
        K.outline(c, skin, K.INK_P, 1.7)
        # pulp
        pulp = K.ellipse_path(c, cx, cy, R * 0.855, ry * 0.855)
        K.fill_radial(c, pulp, cx - 0.2 * R, cy + 0.25 * ry, 1.05 * R, [(0, HEX("#FBF5E2")), (0.6, HEX("#EDE0BC")), (1, HEX("#D6C397"))])
        K.stipple(c, pulp, n=260, col=HEX("#9A8660"), r=0.36, seed=5, a=0.5)
        K.hatch(c, pulp, angle=-40, gap=1.7, col=HEX("#8C7A52"), lw=0.25, depth=0.30, a=0.55)
        K.outline(c, pulp, HEX("#8C7A52"), 0.9)
        # vascular "brush" and cell walls
        c.saveState(); c.setStrokeColor(colors_alpha(HEX("#A8935E"), 0.75)); c.setLineWidth(0.6); c.setLineCap(1)
        for i in range(18):
            a = math.radians(i * 20 + 5)
            c.line(cx + R * 0.30 * math.cos(a), cy + ry * 0.30 * math.sin(a), cx + R * 0.80 * math.cos(a), cy + ry * 0.80 * math.sin(a))
        c.restoreState()
        K.line(c, [(cx, cy - ry * 0.78), (cx, cy + ry * 0.80)], colors_alpha(HEX("#B9A472"), 0.8), 1.0)
        # four seeds, beaks toward the stem
        for dx, dy, rot in ((-0.33, 0.18, 20), (0.33, 0.18, -20), (-0.30, -0.34, 30), (0.30, -0.34, -30)):
            seed(c, cx + dx * R, cy + dy * ry, 0.205 * R, rot)
        # specular highlight on the skin
        c.saveState(); c.setFillColor(colors_alpha(HEX("#FFFFFF"), 0.30))
        c.translate(cx - 0.52 * R, cy + 0.58 * ry); c.rotate(-40)
        c.ellipse(-0.20 * R, -0.075 * R, 0.20 * R, 0.075 * R, stroke=0, fill=1)
        c.restoreState()
        # the cap where the stem joins, with its brush
        cap = K.ellipse_path(c, cx, cy + ry * 0.985, 0.052 * W, 0.020 * H)
        K.fill_radial(c, cap, cx - 3, cy + ry, 0.08 * W, [(0, K.WOOD_L), (1, K.WOOD_M)])
        K.outline(c, cap, K.INK_W, 1.2)

    def _targets(self):
        cx, cy, R, ry = self._geom()
        W, H = self.W, self.H
        a = math.radians(32)
        b = math.radians(-24)
        return [("Skin", (cx + R * 0.99 * math.cos(a), cy + ry * 0.99 * math.sin(a)), "R"),
                ("Pulp", (cx + 0.60 * R, cy - 0.06 * ry), "R"),
                ("Seed", (cx + 0.33 * R, cy + 0.20 * ry), "R"),
                ("Bloom", (cx + R * 1.15 * math.cos(b), cy + ry * 1.15 * math.sin(b)), "R"),
                ("Stem", (cx - 3, cy + ry + 0.095 * H), "R")]


def colors_alpha(col, a):
    return K.alpha(col, a)


# ===================================================================== shoot
class Shoot(Art):
    """A vine shoot at flowering, springing from a cane. One structure per node so every label is unambiguous:
      node 1 leaf (left) | node 2 leaf (right) + lateral shoot (left)
      node 3 leaf (left) + inflorescence (right) | node 4 leaf (right) + tendril (left)
      node 5 tiny young leaf (left) + a prompt bud in the axil (right)"""
    name = "shoot"
    aspect = 0.92
    vis = (0.02, 0.52)
    NODES = (0.20, 0.40, 0.60, 0.79, 0.93)
    LEAVES = ((0, -1, 17.0), (1, 1, 17.0), (2, -1, 15.0), (3, 1, 13.0), (4, -1, 7.0))

    def _bez(self, t):
        W, H = self.W, self.H
        p = [(W * 0.20, H * 0.20), (W * 0.12, H * 0.45), (W * 0.44, H * 0.62), (W * 0.31, H * 0.975)]
        u = 1 - t
        return (u**3 * p[0][0] + 3 * u * u * t * p[1][0] + 3 * u * t * t * p[2][0] + t**3 * p[3][0],
                u**3 * p[0][1] + 3 * u * u * t * p[1][1] + 3 * u * t * t * p[2][1] + t**3 * p[3][1])

    def _leaf_c(self, i, side, R):
        x, y = self._bez(self.NODES[i])
        return x + side * (R * 0.95 + 6), y + 3 + R * 0.12

    def _lat(self):
        x, y = self._bez(self.NODES[1])
        return [(x, y), (x - 10, y + 12), (x - 17, y + 24), (x - 25, y + 40)]

    def _infl(self):
        x, y = self._bez(self.NODES[2])
        return x, y, x + 32, y + 26

    def draw(self, c):
        W, H = self.W, self.H
        # ---- the cane (one-year-old wood) the shoot springs from, with bark texture and eyes
        cane = [(W * 0.02 + (W * 0.48) * i / 30.0, H * 0.150 + (H * 0.035) * i / 30.0) for i in range(31)]
        K.tube(c, cane, 12, 8.5, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.5, hi=0.5, shade=0.4)
        c.saveState(); c.setStrokeColor(K.alpha(K.WOOD_D, 0.7)); c.setLineWidth(0.7); c.setLineCap(1)
        for fx in (0.07, 0.15, 0.24, 0.33, 0.42):          # short bark ticks along the cane
            x = W * (0.02 + 0.48 * fx / 0.5)
            y = H * (0.150 + 0.035 * fx / 0.5)
            c.line(x, y - 2.2, x + 5, y + 1.0)
        c.restoreState()
        for fx in (0.09, 0.34, 0.44):
            x, y = W * fx, H * (0.150 + 0.035 * fx / 0.5) + 6
            K.blob(c, x, y, 3.6, 3.0, 0, light=K.WOOD_L, mid=K.WOOD_M, dark=K.WOOD_D, ink=K.INK_W, lw=1.0)

        # ---- main stem: a tapering tube, nodes swollen
        ctr = [self._bez(i / 60.0) for i in range(61)]
        K.tube(c, ctr, 7.2, 3.8, K.G_MID, light=HEX("#CDE7AE"), dark=K.G_DEEP, ink=K.INK_G, lw=1.4, hi=0.5)
        for t in self.NODES:
            x, y = self._bez(t)
            K.blob(c, x, y, 5.2 - 1.6 * t, 4.6 - 1.4 * t, 0, light=K.G_LIGHT, mid=K.G_MID, dark=K.G_DARK, ink=K.INK_G, lw=1.2)

        # ---- leaves on petioles
        for k, (i, side, R) in enumerate(self.LEAVES):
            x, y = self._bez(self.NODES[i])
            lx, ly = self._leaf_c(i, side, R)
            petiole = [(x + (lx - side * R * 0.28 - x) * u, y + (ly - R * 0.46 - y) * u + 2.5 * math.sin(math.pi * u))
                       for u in [j / 12.0 for j in range(13)]]
            K.tube(c, petiole, 2.8, 2.2, K.G_MID, light=HEX("#CDE7AE"), ink=K.INK_G, lw=0.9, hi=0.4)
            K.leaf(c, lx, ly, R, rot=side * 8, flip=side < 0, stalk=False)

        # ---- inflorescence (node 3, right): peduncle plus a tapered cluster of flower buds
        x, y, ix, iy = self._infl()
        K.tube(c, [(x + (ix - x) * u, y + (iy - y) * u) for u in [j / 8.0 for j in range(9)]], 3.0, 2.2, K.G_MID,
               light=HEX("#CDE7AE"), ink=K.INK_G, lw=0.9, hi=0.4)
        n = 0
        for row in range(8):
            fy = row / 7.0
            cnt = max(1, int(round(5 - 4 * fy)))
            spread = 12 * (1 - 0.8 * fy)
            for k in range(cnt):
                fx = 0.5 if cnt == 1 else k / float(cnt - 1)
                px = ix - spread + fx * 2 * spread + ((n * 7) % 3 - 1) * 0.6
                py = iy - 1 - fy * 28
                K.blob(c, px, py, 2.9, 2.9, 0, light=HEX("#E3F0B0"), mid=HEX("#AECB63"), dark=HEX("#6F9A3A"),
                       ink=K.INK_G, lw=0.7)
                n += 1

        # ---- tendril (node 4, left): inked spiral on a short stalk
        x, y = self._bez(self.NODES[3])
        sx, sy = x - 12, y + 11
        pts = [(x, y), (sx, sy)]
        sp = []
        for i in range(0, 78):
            th = i * 0.17
            r = 1.2 + th * 1.15
            sp.append((sx - 2 + r * math.cos(th + 3.4), sy + 5 + r * math.sin(th + 3.4)))
        K.line(c, pts + sp, K.INK_G, 2.6)
        K.line(c, pts + sp, HEX("#8CC66E"), 1.2)

        # ---- lateral shoot (node 2, left)
        lp = self._lat()
        K.tube(c, K.bezier(*lp, n=24), 4.2, 2.6, K.G_MID, light=HEX("#CDE7AE"), ink=K.INK_G, lw=1.0, hi=0.4)
        for (fx, fy, R, side) in ((-14.5, 17, 9.0, -1), (-24, 32, 8.0, 1)):
            K.leaf(c, lp[0][0] + fx + side * 5, lp[0][1] + fy, R, rot=side * 14, flip=side < 0, stalk=False)

        # ---- prompt bud in the axil at node 5 (right)
        x, y = self._bez(self.NODES[4])
        K.blob(c, x + 4.4, y + 5.2, 3.2, 4.4, -28, light=HEX("#D2B07A"), mid=K.WOOD_L, dark=K.WOOD_M, ink=K.INK_W, lw=1.1)

    def _targets(self):
        W, H = self.W, self.H
        bx, by = self._bez(self.NODES[4])
        leaf = self._leaf_c(1, 1, 17.0)
        _, _, ix, iy = self._infl()
        tx, ty = self._bez(self.NODES[3])
        lp = self._lat()
        return [("Cane", (W * 0.28, H * 0.168), "L"),
                ("Prompt bud", (bx + 4.4, by + 5.2), "R"),
                ("Leaf", leaf, "R"),
                ("Inflorescence", (ix, iy - 13), "R"),
                ("Tendril", (tx - 14, ty + 16), "L"),
                ("Lateral shoot", (lp[0][0] - 17, lp[0][1] + 25), "L")]


# ===================================================================== zones (the whole vine)
class Zones(Art):
    """The four structural zones of a trained vine: shoots, one-year-old wood, permanent wood, roots."""
    name = "zones"
    aspect = 0.66
    vis = (0.02, 0.60)

    def _g(self):
        W, H = self.W, self.H
        return 0.31 * W, 0.30 * H, 0.30 * H + 0.255 * H      # gx, soil_y, trunk_top

    SHOOTS = (-0.195, -0.130, -0.065, 0.065, 0.130, 0.195)

    def draw(self, c):
        W, H = self.W, self.H
        gx, soil_y, top = self._g()
        # ---- soil block
        soil = K.path(c, [("M", W * 0.02, 0), ("L", W * 0.60, 0), ("L", W * 0.60, soil_y), ("L", W * 0.02, soil_y), ("Z",)])
        K.fill_linear(c, soil, 0, soil_y, 0, 0, [(0, K.SOIL_L), (1, K.SOIL_D)])
        topsoil = K.path(c, [("M", W * 0.02, soil_y * 0.64), ("L", W * 0.60, soil_y * 0.64), ("L", W * 0.60, soil_y), ("L", W * 0.02, soil_y), ("Z",)])
        K.fill_linear(c, topsoil, 0, soil_y, 0, soil_y * 0.64, [(0, HEX("#BFA77A")), (1, HEX("#D3BD92"))])
        K.stipple(c, soil, n=190, col=HEX("#6F5A36"), r=0.42, seed=4, bias=(0.1, -0.5), a=0.6)
        K.stipple(c, topsoil, n=70, col=HEX("#5E4A2A"), r=0.35, seed=9, a=0.5)
        K.hatch(c, soil, angle=-32, gap=2.6, col=HEX("#6F5A36"), lw=0.28, depth=0.22, shadow=(0.25, -1.0), a=0.5)
        K.line(c, [(W * 0.02, soil_y * 0.64), (W * 0.15, soil_y * 0.62), (W * 0.33, soil_y * 0.66), (W * 0.60, soil_y * 0.63)], HEX("#8C7347"), 0.6)
        for (px, py, r) in ((0.09, 0.07, 4.2), (0.52, 0.11, 3.6), (0.44, 0.05, 2.8), (0.15, 0.20, 3.0), (0.56, 0.22, 2.4), (0.05, 0.14, 2.2)):
            st = K.ellipse_path(c, W * px, H * py, r * 1.3 * self.s + 1.0, r * self.s + 0.8, 20)
            K.fill_radial(c, st, W * px - 2, H * py + 2, r * 3, [(0, HEX("#F3EBD8")), (0.55, HEX("#D2C6A8")), (1, HEX("#9E9070"))])
            K.hatch(c, st, angle=55, gap=1.2, col=HEX("#5A4C32"), lw=0.25, depth=0.45)
            K.outline(c, st, HEX("#5A4C32"), 0.8)
        K.outline(c, soil, K.INK_W, 1.4)
        for gxp in range(0, 11):                                                      # grass tufts along the surface
            tx = W * 0.04 + gxp * W * 0.052
            for d_ in (-1.6, 0, 1.6):
                K.line(c, [(tx + d_, soil_y), (tx + d_ * 2.2, soil_y + 4.2 + (gxp % 3))], HEX("#4E7A3A"), 0.7, taper=True)

        # ---- roots: a tap root and branching laterals, tapering
        roots = [((gx, soil_y), (gx - 3, soil_y * 0.70), (gx + 4, soil_y * 0.38), (gx - 1, soil_y * 0.06), 8.0, 1.6),
                 ((gx, soil_y), (gx + 14, soil_y * 0.86), (gx + 30, soil_y * 0.60), (gx + 46, soil_y * 0.42), 5.6, 1.2),
                 ((gx, soil_y), (gx - 14, soil_y * 0.86), (gx - 30, soil_y * 0.60), (gx - 47, soil_y * 0.40), 5.6, 1.2),
                 ((gx + 2, soil_y * 0.70), (gx + 18, soil_y * 0.60), (gx + 30, soil_y * 0.34), (gx + 36, soil_y * 0.12), 3.2, 0.9),
                 ((gx - 2, soil_y * 0.62), (gx - 16, soil_y * 0.50), (gx - 28, soil_y * 0.28), (gx - 33, soil_y * 0.10), 3.2, 0.9)]
        for (p0, p1, p2, p3, w0, w1) in roots:
            ctr_r = K.bezier(p0, p1, p2, p3, n=26)
            K.tube(c, ctr_r, w0, w1, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.0, hi=0.4)
            for q_ in range(5, 24, 3):                                                 # fine feeder roots
                rx, ry = ctr_r[q_]
                sd = 1 if q_ % 2 else -1
                K.line(c, [(rx, ry), (rx + sd * 4.5, ry - 3.0), (rx + sd * 8.5, ry - 4.2 - (q_ % 4))], K.INK_W, 0.55)
                K.line(c, [(rx + sd * 4.5, ry - 3.0), (rx + sd * 7.5, ry - 7.5)], K.INK_W, 0.4)

        # ---- trunk: a slightly sinuous tube with bark lines
        trunk = [(gx + 2.4 * math.sin(i / 30.0 * math.pi * 1.2) + 1.1 * math.sin(i * 0.9), soil_y - 2 + (top - soil_y + 2) * i / 30.0) for i in range(31)]
        K.tube(c, trunk, 23.0, 15.5, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.5, hi=0.45, shade=0.4)
        c.saveState(); c.setStrokeColor(K.alpha(K.WOOD_D, 0.6)); c.setLineWidth(0.7); c.setLineCap(1)
        for off in (-3.4, 0.8, 4.6):
            pts = [(x + off * (1 - 0.2 * i / 30.0), y) for i, (x, y) in enumerate(trunk)]
            p = c.beginPath(); p.moveTo(*pts[2])
            for q in pts[3:-2:2]:
                p.lineTo(*q)
            c.drawPath(p, stroke=1, fill=0)
        c.restoreState()

        # ---- cordons: arching arms
        for sgn in (-1, 1):
            arm = [self._arm_xy(sgn * (i / 30.0) * 0.23) for i in range(31)]
            K.tube(c, arm, 13.0, 6.5, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.4, hi=0.45, shade=0.4)

        # ---- the shoulder where trunk and cordons meet (hides the seam)
        sh = K.ellipse_path(c, gx, top + 1.5, 11.5, 8.0)
        K.fill_radial(c, sh, gx - 3, top + 4, 16, [(0, K.WOOD_L), (0.55, K.WOOD_M), (1, K.WOOD_D)])
        K.outline(c, sh, K.INK_W, 1.4)

        # ---- spurs (one-year-old wood), shoots, leaves, tendrils, bunches
        for k, off in enumerate(self.SHOOTS):
            sx, sy = self._arm_top(off)
            lean = off * 26
            # spur: a short pale stub of last season's wood
            K.tube(c, [(sx, sy - 1), (sx + lean * 0.05, sy + 7)], 6.0, 5.0, HEX("#B98C58"), light=HEX("#E2C08C"),
                   dark=K.WOOD_M, ink=K.INK_W, lw=1.1, hi=0.5)
            h = H * (0.255 + 0.025 * math.sin(k * 1.9))
            ctr = K.bezier((sx + lean * 0.05, sy + 6), (sx + lean * 0.2, sy + h * 0.35), (sx + lean * 0.7, sy + h * 0.7), (sx + lean, sy + h), n=22)
            K.tube(c, ctr, 3.8, 2.4, K.G_MID, light=HEX("#CDE7AE"), ink=K.INK_G, lw=1.0, hi=0.5)
            for j in range(3):
                fy = 0.30 + 0.27 * j
                pt = ctr[int(fy * 21)]
                side = 1 if (k + j) % 2 == 0 else -1
                K.leaf(c, pt[0] + side * 12.5, pt[1] + 4, 14.5 + (j % 2) * 2.0 - (k % 2) * 1.2, rot=side * 14 + j * 8 + k * 3, flip=side < 0, stalk=False)
                nd = K.ellipse_path(c, pt[0], pt[1], 2.2, 1.7, 0)
                K.fill_radial(c, nd, pt[0] - 0.5, pt[1] + 0.5, 3, [(0, HEX("#CDE7AE")), (1, K.G_DARK)]); K.outline(c, nd, K.INK_G, 0.6)
            tx, ty = ctr[-1]
            sp = [(tx + (1.0 + 0.28 * i) * math.cos(i * 0.5 + 3.4) * 1.1 + 2 * i * 0.06, ty + 2 + (1.0 + 0.28 * i) * math.sin(i * 0.5 + 3.4) * 1.1)
                  for i in range(0, 16)]
            K.line(c, sp, K.INK_G, 2.2); K.line(c, sp, HEX("#8CC66E"), 1.0)
        for off in (-0.160, 0.100, 0.165):
            bx, by = self._arm_xy(off)
            by -= 5.5
            K.line(c, [(bx, by + 2), (bx, by - 5)], K.INK_G, 1.4)
            K.bunch(c, bx, by - 5, 0.082 * W, 0.135 * H, rows=(4, 5, 4, 3, 3, 2, 1), seed=int(off * 100))

    def _arm_xy(self, off):
        """Centre-line point of the cordon at horizontal offset `off` (fraction of W, signed)."""
        W, H = self.W, self.H
        gx, soil_y, top = self._g()
        sgn = 1 if off >= 0 else -1
        X = lambda t: 3 * 0.085 * (1 - t) ** 2 * t + 3 * 0.17 * (1 - t) * t * t + 0.23 * t ** 3
        lo, hi = 0.0, 1.0
        for _ in range(30):
            mid = (lo + hi) / 2.0
            lo, hi = (mid, hi) if X(mid) < abs(off) else (lo, mid)
        t = (lo + hi) / 2.0
        y = top * (1 - t) ** 3 + 3 * (top + 4) * (1 - t) ** 2 * t + 3 * (top + 4) * (1 - t) * t * t + (top - 3) * t ** 3
        return gx + sgn * X(t) * W, y

    def _arm_top(self, off):
        """Top surface of the cordon (where a spur springs from)."""
        x, y = self._arm_xy(off)
        t = min(abs(off) / 0.23, 1.0)
        return x, y + (13.0 - 6.5 * t) / 2.0 - 1.2

    def _targets(self):
        W, H = self.W, self.H
        gx, soil_y, top = self._g()
        off = 0.130
        sx, sy = self._arm_top(off)
        lean = off * 26
        ox, oy = self._arm_top(0.195)
        return [("Shoots (the canopy)", (sx + lean * 0.55 + 1, sy + H * 0.15), "R"),
                ("One-year-old wood", (ox + 0.5, oy + 4.5), "R"),
                ("Permanent wood", (gx + 5.5, soil_y + 0.115 * H), "R"),
                ("Roots", (gx + 17, soil_y * 0.80), "R")]


# ===================================================================== flower
import wb_ink as K
HEX = K.HEX


class Flower(Art):
    """An open vine flower with a cutaway ovary, in the house style (see wb_ink.py).

    Anatomy follows the Lodi Grape Growers reference: pedicel, nectary lobes, barrel-shaped ovary
    with a cutaway chamber (pollen tube, ovule/embryo sac, eggs), lumpy stigma, two stamens with
    long curved filaments and crinkled anthers, and pollen grains drifting above.
    """
    name = "flower"
    aspect = 1.0
    vis = (0.17, 0.83)

    # centre-lines of the two filaments, as fractions of the box
    FIL_L = ((0.445, 0.250), (0.350, 0.215), (0.225, 0.330), (0.205, 0.610))
    FIL_R = ((0.555, 0.250), (0.660, 0.220), (0.790, 0.330), (0.775, 0.545))

    def _pt(self, f):
        return (f[0] * self.W, f[1] * self.H)

    def _fil(self, which):
        p = self.FIL_L if which == "L" else self.FIL_R
        return K.bezier(*[self._pt(q) for q in p], n=44)

    SC, DX, DY = 0.90, 0.05, 0.10          # the flower proper sits at 90% scale, leaving room for a long pedicel

    def draw(self, c):
        W, H = self.W, self.H
        c.saveState()
        c.translate(self.DX * W, self.DY * H)
        c.scale(self.SC, self.SC)
        X = lambda f: f * W
        Y = lambda f: f * H
        cx = 0.5 * W

        # ---------- pedicel (stem): pale highlight left, deep green right, fading out at the foot
        yb = -0.125 * H
        ped = K.path(c, [("M", X(.472), yb), ("C", X(.472), Y(.04), X(.462), Y(.09), X(.420), Y(.215)),
                         ("L", X(.580), Y(.215)), ("C", X(.538), Y(.09), X(.528), Y(.04), X(.528), yb), ("Z",)])
        K.fill_linear_faded(c, ped, X(.42), X(.58),
                            [(0, K.G_PALE), (0.28, HEX("#7CB85E")), (0.68, K.G_MID), (1, K.G_DARK)], yb, Y(.15))
        K.line(c, K.bezier((X(.472), yb + Y(.02)), (X(.472), Y(.04)), (X(.462), Y(.09)), (X(.420), Y(.213)), n=20), K.INK_G, 1.5)
        K.line(c, K.bezier((X(.528), yb + Y(.02)), (X(.528), Y(.04)), (X(.538), Y(.09)), (X(.580), Y(.213)), n=20), K.INK_G, 1.5)

        # ---------- receptacle ring under the nectary
        rec = K.ellipse_path(c, cx, Y(.215), X(.125), Y(.042))
        K.fill_radial(c, rec, cx - X(.04), Y(.235), X(.17), [(0, K.G_LIGHT), (0.55, K.G_MID), (1, K.G_DARK)])
        K.outline(c, rec, K.INK_G, 1.25)

        # ---------- filaments (drawn first so the ovary and nectary overlap their bases)
        for which in ("L", "R"):
            ctr = self._fil(which)
            K.tube(c, ctr, X(.044), X(.026), K.G_FIL, light=HEX("#EAF4DC"), dark=HEX("#7FA070"),
                   ink=K.INK_G, lw=1.6, hi=0.45, shade=0.35)

        # ---------- ovary: barrel, light spot upper-left, deep green shadow right
        ov = K.path(c, [("M", X(.50), Y(.245)),
                        ("C", X(.595), Y(.245), X(.645), Y(.33), X(.645), Y(.45)),
                        ("C", X(.645), Y(.56), X(.600), Y(.655), X(.50), Y(.655)),
                        ("C", X(.400), Y(.655), X(.355), Y(.56), X(.355), Y(.45)),
                        ("C", X(.355), Y(.33), X(.405), Y(.245), X(.50), Y(.245)), ("Z",)])
        K.fill_radial(c, ov, X(.43), Y(.56), X(.34), [(0, HEX("#A6D585")), (0.45, HEX("#52984A")), (1, K.G_DEEP)])
        # carpel seam lines (soft, darker green)
        for (x0, x1) in ((0.572, 0.590), (0.545, 0.558)):
            K.line(c, K.bezier((X(x0), Y(.640)), (X(x0 + .03), Y(.52)), (X(x0 + .026), Y(.38)), (X(x1), Y(.275)), n=20),
                   K.alpha(K.G_DEEP, 0.55), 1.0)
        K.outline(c, ov, K.INK_G, 1.8)

        # ---------- cutaway window: pale chamber with a dark green rim
        ch = K.path(c, [("M", X(.52), Y(.290)),
                        ("C", X(.570), Y(.290), X(.592), Y(.36), X(.592), Y(.45)),
                        ("C", X(.592), Y(.54), X(.570), Y(.625), X(.52), Y(.625)),
                        ("C", X(.470), Y(.625), X(.448), Y(.54), X(.448), Y(.45)),
                        ("C", X(.448), Y(.36), X(.470), Y(.290), X(.52), Y(.290)), ("Z",)])
        K.fill_radial(c, ch, X(.52), Y(.47), X(.16), [(0, HEX("#DCEBC9")), (0.55, HEX("#A8C791")), (1, HEX("#6E9A60"))])
        K.outline(c, ch, K.G_DEEP, 1.7)
        # inner shading on the left lip of the cut
        K.line(c, K.bezier((X(.452), Y(.52)), (X(.447), Y(.47)), (X(.449), Y(.41)), (X(.462), Y(.34)), n=14),
               K.alpha(K.G_DEEP, 0.35), 2.2)

        # ---------- ovule (embryo sac) at the foot of the chamber, with two eggs
        ovule = K.ellipse_path(c, X(.520), Y(.345), X(.062), Y(.050))
        K.fill_radial(c, ovule, X(.50), Y(.36), X(.09), [(0, HEX("#F1F2D2")), (1, HEX("#B7CC96"))])
        K.outline(c, ovule, HEX("#4F7A45"), 1.0)
        K.blob(c, X(.497), Y(.338), X(.019), Y(.026), -10, ink=K.INK_Y, lw=1.0)
        K.blob(c, X(.543), Y(.342), X(.019), Y(.026), 12, ink=K.INK_Y, lw=1.0)

        # ---------- pollen tube running from the stigma down to the ovule
        tubep = K.path(c, [("M", X(.512), Y(.682)), ("L", X(.512), Y(.385)), ("L", X(.526), Y(.385)),
                           ("L", X(.526), Y(.682)), ("Z",)])
        K.flat(c, tubep, K.CREAM)
        K.outline(c, tubep, HEX("#8A6A3A"), 0.9)
        K.blob(c, X(.519), Y(.40), X(.0075), Y(.011), 0, light=HEX("#6B4A2A"), mid=HEX("#4B3220"), dark=HEX("#2C1C10"),
               ink=HEX("#2C1C10"), lw=0.6)     # a sperm cell

        # ---------- nectary lobes at the base of the ovary
        for (lx, ly, rx, ry, rot) in ((.392, .252, .052, .036, 20), (.608, .252, .052, .036, -20),
                                       (.425, .222, .074, .040, 6), (.575, .222, .074, .040, -6)):
            p = K.ellipse_path(c, X(lx), Y(ly), X(rx), Y(ry), rot)
            K.fill_radial(c, p, X(lx) - X(.025), Y(ly) + Y(.02), X(.12), [(0, K.G_LIGHT), (0.55, HEX("#4F984A")), (1, K.G_DARK)])
            K.outline(c, p, K.INK_G, 1.5)

        # ---------- style stub and lumpy stigma
        stub = K.ellipse_path(c, X(.512), Y(.652), X(.046), Y(.021))
        K.fill_radial(c, stub, X(.49), Y(.66), X(.07), [(0, K.G_MID), (1, K.G_DEEP)])
        K.outline(c, stub, K.INK_G, 1.1)
        for (lx, ly, rx, ry, rot) in ((.472, .680, .030, .023, 18), (.506, .690, .029, .024, -8),
                                       (.543, .684, .031, .024, 10), (.575, .674, .029, .022, -20)):
            K.blob(c, X(lx), Y(ly), X(rx), Y(ry), rot, ink=K.INK_Y, lw=1.7)

        # ---------- anthers: big crinkled bean shapes at the filament tips
        for (ax, ay, rx, ry, rot, fl) in ((.200, .655, .088, .049, -16, 1), (.773, .592, .078, .045, 24, -1)):
            K.blob(c, X(ax), Y(ay), X(rx), Y(ry), rot, ink=K.INK_Y, lw=1.9, light_at=(-0.4, 0.5))
            cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))

            def R(u, v):
                return (X(ax) + u * X(rx) * cr - v * Y(ry) * sr, Y(ay) + u * X(rx) * sr + v * Y(ry) * cr)
            crease = K.bezier(R(-0.62, 0.05), R(-0.25, -0.35), R(0.15, 0.30), R(0.62, -0.18), n=24)
            K.line(c, crease, HEX("#9A6C1E"), 1.0)
            K.blob(c, *R(-0.38 * fl, 0.38), X(.009), Y(.009), 0, light=K.Y_LIGHT, mid=K.Y_MID, dark=K.Y_DARK,
                   ink=K.INK_Y, lw=0.8)

        # ---------- pollen grains drifting above the stigma
        for (gx, gy, r) in ((.300, .800, 0), (.345, .835, 30), (.385, .805, -20), (.425, .845, 15), (.470, .815, -40),
                            (.520, .850, 25), (.575, .820, -10), (.625, .845, 35)):
            K.blob(c, X(gx), Y(gy), X(.0105), Y(.0085), r, ink=K.INK_Y, lw=0.9)
        c.restoreState()

    def _targets(self):
        W, H = self.W, self.H
        X = lambda f: f * W
        Y = lambda f: f * H
        T = lambda p: (p[0] * self.SC + self.DX * W, p[1] * self.SC + self.DY * H)
        fl = self._fil("L")
        fpt = fl[int(len(fl) * 0.50)]
        return [("Anther", T((X(.150), Y(.675))), "L"),
                ("Pollen", T((X(.385), Y(.805))), "L"),
                ("Ovary", T((X(.372), Y(.50))), "L"),
                ("Filament", T(fpt), "L"),
                ("Stigma", T((X(.598), Y(.684))), "R"),
                ("Pollen tube", T((X(.519), Y(.55))), "R"),
                ("Ovule", T((X(.520), Y(.304))), "R"),
                ("Egg", T((X(.543), Y(.342))), "R")]


# ===================================================================== trellis systems (Chapter 7)
import random as _rnd


def _ground(c, W):
    g = K.path(c, [("M", 0, 0), ("L", W, 0), ("L", W, 9), ("L", 0, 9), ("Z",)])
    K.fill_linear(c, g, 0, 9, 0, 0, [(0, K.SOIL_L), (1, HEX("#C4AB7D"))])
    K.stipple(c, g, n=int(W * 0.8), col=HEX("#6F5A36"), r=0.36, seed=int(W) + 3, a=0.6, bias=(0.0, -0.6))
    K.hatch(c, g, angle=-30, gap=2.0, col=HEX("#7B6238"), lw=0.25, depth=0.45, shadow=(0.3, -1.0), a=0.5)
    K.line(c, [(0, 9), (W, 9)], K.INK_W, 1.1)
    for i in range(0, int(W) - 6, 13):                                  # a few blades of grass along the surface
        for d_ in (-1.4, 0.0, 1.4):
            K.line(c, [(i + 6 + d_, 9), (i + 6 + d_ * 2.0, 12.4 + (i % 3))], HEX("#4E7A3A"), 0.6)


def _post(c, x, y0, y1, w=4.6):
    """A treated timber post: straight, squared, weathered, with a flat cap. (The vine must never look like this.)"""
    K.tube(c, [(x, y0), (x, y1)], w, w, HEX("#9A7B52"), light=HEX("#C9AE86"), dark=HEX("#5E4626"), ink=K.INK_W, lw=1.0, hi=0.5, shade=0.4, grain=True)
    cap = K.rrect(c, x - w / 2.0 - 0.6, y1 - 1.2, w + 1.2, 2.6, 0.8)
    K.fill_linear(c, cap, 0, y1 + 1.4, 0, y1 - 1.2, [(0, HEX("#B9A07A")), (1, HEX("#6E5632"))]); K.outline(c, cap, K.INK_W, 0.7)


def _wire(c, x0, x1, y):
    K.line(c, [(x0, y), (x1, y)], HEX("#4A4A4A"), 0.8)


# ---- vine wood: gnarled, tapering, never ruler-straight -------------------------------------------------------------
BARK_L, BARK_M, BARK_D = HEX("#A9825A"), HEX("#7A5836"), HEX("#4A331C")
SPUR_L, SPUR_M = HEX("#E2C08C"), HEX("#B98C58")


def vine_trunk(c, x, y0, y1, w, seed=0, lean=0.0):
    """A trunk that twists, flares at the base, tapers, swells and carries pruning scars. Returns its centre-line."""
    rnd = _rnd.Random(seed * 7 + 3)
    n = 30
    ph = rnd.uniform(0, 6.28)
    cen, wid = [], []
    for i in range(n):
        t = i / float(n - 1)
        xx = x + lean * t + w * 0.34 * math.sin(t * 4.6 + ph) + w * 0.12 * math.sin(t * 11.0 + ph * 1.7)
        yy = y0 + (y1 - y0) * t
        flare = 1.0 + 0.62 * math.exp(-t * 8.5)
        swell = 1.0 + 0.10 * math.sin(t * 12.0 + ph) + 0.05 * math.sin(t * 27.0 + ph)
        cen.append((xx, yy)); wid.append(w * (1.0 - 0.20 * t) * flare * swell)
    K.tube(c, cen, wid, None, BARK_M, light=BARK_L, dark=BARK_D, ink=K.INK_W, lw=1.25, hi=0.5, shade=0.45, grain=True)
    for f in (0.30, 0.55, 0.78):                                            # old pruning scars and burls
        i = int(f * (n - 1))
        sd = 1 if (i + seed) % 2 else -1
        px, py = cen[i][0] + sd * wid[i] * 0.34, cen[i][1]
        for rr in (1.9, 1.2, 0.6):
            kp = K.ellipse_path(c, px, py, rr * 1.35, rr * 1.7, 12)
            K.outline(c, kp, K.alpha(BARK_D, 0.95), 0.4, pen=False)
    return cen, wid


def vine_head(c, x, y, w, seed=0):
    """The swollen knuckle where the trunk divides into cordons."""
    rnd = _rnd.Random(seed + 11)
    sh = K.ellipse_path(c, x, y, w * 0.78, w * 0.56, rnd.uniform(-8, 8))
    K.fill_radial(c, sh, x - w * 0.25, y + w * 0.2, w * 1.4, [(0, BARK_L), (0.55, BARK_M), (1, BARK_D)])
    K.hatch(c, sh, angle=60, gap=1.3, col=BARK_D, lw=0.26, depth=0.45, a=0.6)
    K.outline(c, sh, K.INK_W, 1.2)
    for k in range(3):
        K.line(c, [(x - w * 0.5 + k * w * 0.32, y - w * 0.3), (x - w * 0.45 + k * w * 0.32 + 0.8, y + w * 0.28)], alpha_ink(), 0.4, pen=False)


def alpha_ink():
    return K.alpha(BARK_D, 0.85)


def vine_cordon(c, hx, hy, sgn, length, w, seed=0, arch=2.0, droop=0.0, spurs=True, spur_gap=None):
    """A cordon: leaves the head thick, thins toward its tip, undulates, and carries short spurs.
    Returns the list of (x, y) tops of its spurs (where shoots spring from)."""
    rnd = _rnd.Random(seed * 13 + 5)
    m = 22
    ph = rnd.uniform(0, 6.28)
    cen, wid = [], []
    for i in range(m):
        t = i / float(m - 1)
        xx = hx + sgn * length * t
        yy = hy + arch * math.sin(t * math.pi * 0.85) * (1.0 - 0.3 * t) - droop * t * t + w * 0.16 * math.sin(t * 8.5 + ph)
        cen.append((xx, yy)); wid.append(w * (1.0 - 0.52 * t ** 0.9) * (1.0 + 0.08 * math.sin(t * 17 + ph)))
    K.tube(c, cen, wid, None, BARK_M, light=BARK_L, dark=BARK_D, ink=K.INK_W, lw=1.1, hi=0.5, shade=0.45, grain=True)
    tops = []
    if spurs:
        gap = spur_gap or max(9.0, w * 2.6)
        k = 0.17
        while k < 0.97:
            i = int(k * (m - 1))
            x, y = cen[i]
            tw = max(wid[i] * 0.62, 2.4)
            lean = rnd.uniform(-1.2, 1.2)
            sp = [(x, y + wid[i] * 0.32), (x + lean * 0.5, y + wid[i] * 0.32 + 3.0), (x + lean, y + wid[i] * 0.32 + 6.5)]
            K.tube(c, sp, tw, tw * 0.85, SPUR_M, light=SPUR_L, dark=BARK_M, ink=K.INK_W, lw=0.8, hi=0.5, grain=False)
            tops.append((x + lean, y + wid[i] * 0.32 + 6.5))
            k += gap / max(length, 1.0)
    return tops, cen


def _tie(c, x, y):
    K.line(c, [(x - 1.8, y - 2.2), (x, y + 0.4), (x + 1.8, y - 2.2)], HEX("#5E4626"), 0.9, pen=False)


def _shoot_with_leaves(c, ctr, leaves_at, R=5.6, lw=0.6):
    K.tube(c, ctr, 2.0, 1.4, K.G_MID, light=HEX("#CDE7AE"), ink=K.INK_G, lw=0.7, hi=0.5)
    n = len(ctr)
    for k, f in enumerate(leaves_at):
        x, y = ctr[min(int(f * (n - 1)), n - 1)]
        side = 1 if k % 2 == 0 else -1
        K.leaf(c, x + side * (R * 0.9), y, R, rot=side * 12, flip=side < 0, stalk=False, lw=lw)


class TrellisBush(Art):
    name = "bush"
    aspect = 1.18

    def draw(self, c):
        W, H = self.W, self.H
        _ground(c, W)
        cx = W * 0.5
        cen, wid = vine_trunk(c, cx, 8, 50, 10.5, seed=3, lean=2.0)
        hx, hy = cen[-1]
        arms = []
        for (sgn, ln, up, sd) in ((-1, 21, 14, 1), (1, 22, 15, 2), (1, 8, 24, 3)):
            pts = []
            m = 16
            for i in range(m):
                t = i / float(m - 1)
                pts.append((hx + sgn * ln * t * (1.0 if sd < 3 else 0.5), hy + 4 + up * t ** 0.8 + 1.4 * math.sin(t * 7 + sd)))
            K.tube(c, pts, [5.6 * (1 - 0.5 * i / (m - 1)) + 0.8 for i in range(m)], None, BARK_M, light=BARK_L, dark=BARK_D, ink=K.INK_W, lw=1.0, hi=0.5, shade=0.45, grain=True)
            arms.append(pts[-1])
        vine_head(c, hx, hy + 2, 10.5, seed=2)
        K.bunch(c, hx - 11, hy - 2, 13, 17, rows=(3, 3, 3, 2, 1), seed=1)
        K.bunch(c, hx + 12, hy - 4, 13, 17, rows=(3, 3, 3, 2, 1), seed=2)
        for (ax, ay), (ex, ey, sgn) in zip(arms, ((-30, 60, -1), (30, 60, 1), (10, 88, 1))):
            ctr = K.bezier((ax, ay), (ax + ex * 0.35, ay + 30), (ax + ex * 0.9, ay + 34), (ax + ex, ay + ey * 0.0 - 20), n=22)
            _shoot_with_leaves(c, ctr, (0.18, 0.36, 0.54, 0.72, 0.9), R=6.8)


class TrellisVSP(Art):
    name = "vsp"
    aspect = 1.18

    def draw(self, c):
        W, H = self.W, self.H
        _ground(c, W)
        for y in (46, 74, 102, 124):
            _wire(c, 8, W - 8, y)
        _post(c, 8, 8, 130); _post(c, W - 8, 8, 130)
        cx = W * 0.5
        cen, wid = vine_trunk(c, cx, 8, 44, 9.0, seed=5, lean=-1.5)
        hx, hy = cen[-1]
        tops = []
        for sgn, ln, sd in ((-1, 38, 1), (1, 38, 2)):
            t_, cc = vine_cordon(c, hx, 46.5, sgn, ln, 6.0, seed=sd, arch=1.0)
            tops += t_
            for (x, y) in cc[3::5]:
                _tie(c, x, y + 3)
        vine_head(c, hx, 46.5, 9.0, seed=4)
        for i, (x, y) in enumerate(sorted(tops)):
            ctr = [(x + 1.2 * math.sin(j / 4.0 + i), y + (122 - y) * j / 18.0) for j in range(19)]
            _shoot_with_leaves(c, ctr, (0.16, 0.36, 0.58, 0.8), R=5.4)
        for x in (36, 74, 94):
            K.bunch(c, x, 41, 11, 14, rows=(3, 3, 2, 1))


class TrellisGDC(Art):
    name = "gdc"
    aspect = 1.18

    def draw(self, c):
        W, H = self.W, self.H
        _ground(c, W)
        cx = W * 0.5
        _post(c, cx + 9, 8, 100, 5.4)                                              # the support post, separate from the vine
        K.tube(c, [(16, 104), (W - 16, 104)], 4.4, 4.4, HEX("#9A7B52"), light=HEX("#C9AE86"), dark=HEX("#5E4626"), ink=K.INK_W, lw=1.0, hi=0.5, shade=0.4, grain=True)
        cen, wid = vine_trunk(c, cx - 3, 8, 98, 9.0, seed=8, lean=2.0)
        hx, hy = cen[-1]
        for sgn, sd in ((-1, 1), (1, 2)):                                           # a cordon along each side of the cross-arm
            _t, cc = vine_cordon(c, hx, 101.5, sgn, 44, 5.2, seed=sd, arch=1.2, droop=1.0, spurs=False)
        vine_head(c, hx, 100, 8.0, seed=6)
        for x in (16, W - 16):
            K.blob(c, x, 104, 3.4, 3.4, 0, light=HEX("#C9CCCF"), mid=HEX("#8A8D90"), dark=HEX("#4A4A4A"), ink=HEX("#2A2A2A"), lw=0.9)
        for side in (-1, 1):
            base = 16 if side < 0 else W - 16
            for i, dx in enumerate((-10, -3.5, 3.5, 10)):
                x = base + dx + side * 4
                ctr = [(x + 1.2 * math.sin(j / 3.0 + i), 100 - (100 - 44) * j / 16.0) for j in range(17)]
                _shoot_with_leaves(c, ctr, (0.15, 0.38, 0.62, 0.86), R=5.2)
            K.bunch(c, base + side * 2, 58, 10, 12)


class TrellisSH(Art):
    name = "scott_henry"
    aspect = 1.18

    def draw(self, c):
        W, H = self.W, self.H
        _ground(c, W)
        for y in (90, 118, 36, 24):
            _wire(c, 8, W - 8, y)
        _post(c, 8, 8, 130); _post(c, W - 8, 8, 130)
        cx = W * 0.5
        cen, wid = vine_trunk(c, cx, 8, 54, 9.0, seed=9, lean=1.5)
        hx, hy = cen[-1]
        tops = []
        for sgn, sd in ((-1, 1), (1, 2)):
            t_, cc = vine_cordon(c, hx, 59.5, sgn, 38, 6.0, seed=sd + 3, arch=0.8)
            tops += t_
            for (x, y) in cc[3::5]:
                _tie(c, x, y + 3)
        vine_head(c, hx, 59.5, 9.0, seed=7)
        tops = sorted(tops)
        for i, (x, y) in enumerate(tops):
            if i % 2 == 0:
                ctr = [(x + 1.2 * math.sin(j / 4.0 + i), y + (123 - y) * j / 16.0) for j in range(17)]
                _shoot_with_leaves(c, ctr, (0.2, 0.45, 0.7, 0.92), R=5.4)
            else:
                ctr = [(x + 1.2 * math.sin(j / 4.0 + i), 56 - (56 - 20) * j / 12.0) for j in range(13)]
                _shoot_with_leaves(c, ctr, (0.25, 0.55, 0.85), R=5.0)
        K.bunch(c, 40, 54, 10, 12)
        K.bunch(c, 66, 54, 10, 12)


# ===================================================================== presses (Chapter 13)
STEEL_L, STEEL_M, STEEL_D, INK_S = HEX("#EDF0F2"), HEX("#B3BBC1"), HEX("#6E777E"), HEX("#2E353B")
JUICE_L, JUICE_D = HEX("#F1D98C"), HEX("#D8AE45")


def _steel(c, x, y, w, h, r=5, horizontal=True, lw=1.1):
    p = K.rrect(c, x, y, w, h, r)
    if horizontal:
        K.fill_linear(c, p, x, y + h, x, y, [(0, STEEL_M), (0.25, STEEL_L), (0.6, STEEL_M), (1, STEEL_D)])
    else:
        K.fill_linear(c, p, x, y, x + w, y, [(0, STEEL_M), (0.3, STEEL_L), (0.65, STEEL_M), (1, STEEL_D)])
    K.hatch(c, p, angle=-38, gap=1.7, col=INK_S, lw=0.24, depth=0.28, a=0.55)
    if min(w, h) > 5:
        K.line(c, [(x + r * 0.9, y + h - 1.6), (x + w - r * 0.9, y + h - 1.6)] if horizontal else [(x + 1.6, y + r * 0.9), (x + 1.6, y + h - r * 0.9)],
               HEX("#FFFFFF"), 0.7, pen=False)
    K.outline(c, p, INK_S, lw)
    if w > 40 and h > 22:                                               # rivets along a large panel
        for k in range(int(w // 14)):
            rx = x + 9 + k * 14
            if rx < x + w - 6:
                for ry in (y + 4.5, y + h - 4.5):
                    K.blob(c, rx, ry, 1.2, 1.2, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.4)


def _steel_poly(c, pts, horizontal=True, lw=1.1):
    p = K.poly(c, pts)
    ys = [q[1] for q in pts]; xs = [q[0] for q in pts]
    if horizontal:
        K.fill_linear(c, p, 0, max(ys), 0, min(ys), [(0, STEEL_M), (0.3, STEEL_L), (1, STEEL_D)])
    else:
        K.fill_linear(c, p, min(xs), 0, max(xs), 0, [(0, STEEL_M), (0.3, STEEL_L), (1, STEEL_D)])
    K.hatch(c, p, angle=-38, gap=1.7, col=INK_S, lw=0.24, depth=0.28, a=0.55)
    K.outline(c, p, INK_S, lw)


def _juice(c, x0, x1, y):
    p = K.path(c, [("M", x0, y), ("L", x1, y), ("L", x1 - 2, y + 4), ("L", x0 + 2, y + 4), ("Z",)])
    K.fill_linear(c, p, 0, y + 4, 0, y, [(0, JUICE_L), (1, JUICE_D)])


class PressPneumatic(Art):
    name = "pneumatic"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        for x in (30, 112):
            _steel_poly(c, [(x - 9, 4), (x + 9, 4), (x + 5, 46), (x - 5, 46)], horizontal=False)
        _steel(c, 20, 30, 110, 11, r=3)
        _juice(c, 28, 122, 33)
        _steel(c, 8, 44, 134, 72, r=16)
        p = c.beginPath(); p.roundRect(20, 54, 110, 52, 8)
        K.fill_linear(c, p, 20, 106, 20, 54, [(0, HEX("#FBF3DC")), (1, HEX("#EBDDB4"))]); K.outline(c, p, INK_S, 0.9)
        for j, y in enumerate(range(60, 104, 7)):                       # the grape mass
            for x in range(27 + (4 if j % 2 else 0), 80, 8):
                K.berry(c, x, y, 3.6, lw=0.6)
        m = K.path(c, [("M", 130, 54), ("L", 108, 54), ("C", 90, 62, 90, 98, 108, 106), ("L", 130, 106), ("Z",)])   # the air bag
        K.fill_linear(c, m, 90, 0, 130, 0, [(0, HEX("#B9CADA")), (0.5, HEX("#8DA6BD")), (1, HEX("#5E7890"))])
        K.outline(c, m, HEX("#1F2F3D"), 1.1)
        for y in (70, 90):
            K.line(c, [(122, y), (104, y)], HEX("#F4F8FB"), 1.6)
            K.line(c, [(104, y), (110, y + 4)], HEX("#F4F8FB"), 1.6); K.line(c, [(104, y), (110, y - 4)], HEX("#F4F8FB"), 1.6)
        K.line(c, [(20, 106), (20, 54)], INK_S, 1.0)
        _steel(c, 142, 76, 6, 8, r=2)                                   # air inlet
        K.blob(c, 70, 118, 6, 3, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=1.0)   # loading port

    def _targets(self):
        return []


class PressBasket(Art):
    name = "basket"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        _steel(c, 18, 22, 114, 12, r=3)                                 # base tray and spout
        _steel_poly(c, [(130, 24), (146, 18), (146, 26), (130, 32)])
        _juice(c, 24, 126, 27)
        for x in (143, 144):
            K.blob(c, x, 12, 1.8, 2.6, 0, light=JUICE_L, mid=JUICE_D, dark=JUICE_D, ink=HEX("#8A6A1E"), lw=0.6)
        body = c.beginPath(); body.roundRect(42, 34, 66, 76, 5)
        K.fill_linear(c, body, 42, 0, 108, 0, [(0, K.WOOD_M), (0.35, K.WOOD_L), (1, K.WOOD_D)])
        for i in range(1, 11):                                          # slats, with the grapes showing through the gaps
            x = 42 + i * 66 / 11.0
            K.line(c, [(x, 36), (x, 108)], HEX("#5B2342"), 1.5)
            K.line(c, [(x - 2.4, 36), (x - 2.4, 108)], K.WOOD_D, 0.5)
        K.outline(c, body, K.INK_W, 1.3)
        for y in (50, 92):                                              # hoops
            _steel(c, 40, y, 70, 6, r=2)
        _steel(c, 44, 110, 62, 8, r=2)                                  # pressing plate
        _steel(c, 71.5, 118, 7, 18, r=2, horizontal=False)              # screw
        _steel(c, 56, 133, 38, 4.5, r=2)                                # handle bar
        for x in (56, 94):
            K.blob(c, x, 135, 3.6, 3.6, 0, light=STEEL_L, mid=STEEL_M, dark=STEEL_D, ink=INK_S, lw=0.9)

    def _targets(self):
        return []


class PressContinuous(Art):
    name = "continuous"
    aspect = 0.95

    def draw(self, c):
        W, H = self.W, self.H
        for x in (30, 100):
            _steel_poly(c, [(x - 9, 4), (x + 9, 4), (x + 5, 44), (x - 5, 44)], horizontal=False)
        _steel(c, 16, 28, 98, 11, r=3)
        _juice(c, 22, 108, 31)
        _steel(c, 14, 44, 104, 46, r=8)
        p = c.beginPath(); p.roundRect(22, 52, 88, 30, 5)
        K.fill_linear(c, p, 22, 82, 22, 52, [(0, HEX("#FBF3DC")), (1, HEX("#EBDDB4"))]); K.outline(c, p, INK_S, 0.9)
        for x in range(26, 108, 9):                                     # the screw flights
            K.line(c, [(x, 54), (x + 7, 80)], INK_S, 1.5)
        K.line(c, [(22, 67), (110, 67)], INK_S, 2.2)                   # shaft
        for x in range(24, 116, 7):                                     # perforations
            K.blob(c, x, 47.5, 1.0, 1.0, 0, light=INK_S, mid=INK_S, dark=INK_S, ink=INK_S, lw=0.2)
        _steel_poly(c, [(12, 124), (62, 124), (50, 90), (26, 90)])      # hopper
        for (x, y) in ((28, 132), (40, 137), (50, 130), (36, 128)):
            K.berry(c, x, y, 3.8, lw=0.6)
        cone = K.path(c, [("M", 118, 46), ("L", 142, 58), ("L", 142, 76), ("L", 118, 88), ("Z",)])
        K.fill_linear(c, cone, 0, 88, 0, 46, [(0, STEEL_M), (0.3, STEEL_L), (1, STEEL_D)]); K.outline(c, cone, INK_S, 1.1)
        K.blob(c, 140, 67, 6, 8, 0, light=K.BERRY_L, mid=K.BERRY_M, dark=K.BERRY_D, ink=K.INK_P, lw=0.9)   # pomace cake

    def _targets(self):
        return []
