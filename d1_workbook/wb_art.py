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
        K.outline(c, skin, K.INK_P, 1.7)
        # pulp
        pulp = K.ellipse_path(c, cx, cy, R * 0.855, ry * 0.855)
        K.fill_radial(c, pulp, cx - 0.2 * R, cy + 0.25 * ry, 1.05 * R, [(0, HEX("#FBF5E2")), (0.6, HEX("#EDE0BC")), (1, HEX("#D6C397"))])
        K.outline(c, pulp, HEX("#8C7A52"), 0.9)
        # vascular "brush" and cell walls
        c.saveState(); c.setStrokeColor(colors_alpha(HEX("#B9A472"), 0.55)); c.setLineWidth(0.6); c.setLineCap(1)
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
        c.saveState()
        for i in range(34):                                           # fine aggregate
            x = W * 0.03 + ((i * 53.7) % (W * 0.56))
            y = 3 + ((i * 29.3) % (soil_y - 8))
            c.setFillColor(K.alpha(HEX("#9C8760"), 0.45)); c.circle(x, y, 0.6 + (i % 3) * 0.35, stroke=0, fill=1)
        c.restoreState()
        for (px, py, r) in ((0.09, 0.06, 4.0), (0.52, 0.10, 3.4), (0.44, 0.04, 2.6), (0.15, 0.21, 2.8)):
            K.blob(c, W * px, H * py, r * 1.3 * self.s + 1, r * self.s + 1, 20, light=HEX("#F3EBD8"), mid=HEX("#D8CDB4"),
                   dark=HEX("#B7AA8A"), ink=HEX("#7A6C4E"), lw=0.8)
        K.outline(c, soil, K.INK_W, 1.4)

        # ---- roots: a tap root and branching laterals, tapering
        roots = [((gx, soil_y), (gx - 3, soil_y * 0.70), (gx + 4, soil_y * 0.38), (gx - 1, soil_y * 0.06), 8.0, 1.6),
                 ((gx, soil_y), (gx + 14, soil_y * 0.86), (gx + 30, soil_y * 0.60), (gx + 46, soil_y * 0.42), 5.6, 1.2),
                 ((gx, soil_y), (gx - 14, soil_y * 0.86), (gx - 30, soil_y * 0.60), (gx - 47, soil_y * 0.40), 5.6, 1.2),
                 ((gx + 2, soil_y * 0.70), (gx + 18, soil_y * 0.60), (gx + 30, soil_y * 0.34), (gx + 36, soil_y * 0.12), 3.2, 0.9),
                 ((gx - 2, soil_y * 0.62), (gx - 16, soil_y * 0.50), (gx - 28, soil_y * 0.28), (gx - 33, soil_y * 0.10), 3.2, 0.9)]
        for (p0, p1, p2, p3, w0, w1) in roots:
            K.tube(c, K.bezier(p0, p1, p2, p3, n=26), w0, w1, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.0, hi=0.4)

        # ---- trunk: a slightly sinuous tube with bark lines
        trunk = [(gx + 1.6 * math.sin(i / 30.0 * math.pi * 1.2), soil_y - 2 + (top - soil_y + 2) * i / 30.0) for i in range(31)]
        K.tube(c, trunk, 19.0, 15.0, K.WOOD_M, light=K.WOOD_L, dark=K.WOOD_D, ink=K.INK_W, lw=1.5, hi=0.45, shade=0.4)
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
                K.leaf(c, pt[0] + side * 9.5, pt[1] + 3, 11.0 + (j % 2) * 1.2, rot=side * 14 + j * 8, flip=side < 0, stalk=False)
            tx, ty = ctr[-1]
            sp = [(tx + (1.0 + 0.28 * i) * math.cos(i * 0.5 + 3.4) * 1.1 + 2 * i * 0.06, ty + 2 + (1.0 + 0.28 * i) * math.sin(i * 0.5 + 3.4) * 1.1)
                  for i in range(0, 16)]
            K.line(c, sp, K.INK_G, 2.2); K.line(c, sp, HEX("#8CC66E"), 1.0)
        for off in (-0.160, 0.100, 0.165):
            bx, by = self._arm_xy(off)
            by -= 5.5
            K.line(c, [(bx, by + 2), (bx, by - 5)], K.INK_G, 1.4)
            K.bunch(c, bx, by - 5, 0.066 * W, 0.105 * H)

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
