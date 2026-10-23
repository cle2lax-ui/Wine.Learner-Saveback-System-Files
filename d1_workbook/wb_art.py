# -*- coding: utf-8 -*-
"""Artwork for the workbook's label-the-diagram exercises.

Each `Art` exposes:
    draw(c)            paints the unlabelled artwork into a W x H box at the origin
    targets            [(name, (x, y))] -- the point on the art each label refers to

The vine and grape drawings are the Mastery Guide's own code with only the
annotation block cut off, so the workbook shows the same artwork students met
in the guide. The shoot and flower drawings are new.
"""
import inspect
import math
import os
import sys
import textwrap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "d1_mastery"))
import graphics as G
from graphics import (_blend, _vine_leaf, _taper, LEAF_MID, LEAF_LIGHT, LEAF_DARK,
                      WOOD_DARK, WOOD_MID, WOOD_LIT)
from reportlab.lib import colors


def _strip_annotation(cls, marker):
    """Re-compile cls.draw keeping only the artwork (everything before `marker`)."""
    src = inspect.getsource(cls.draw)
    body = textwrap.dedent(src[:src.index(marker)])
    ns = {}
    exec(compile(body, "art_" + cls.__name__, "exec"), G.__dict__, ns)
    return ns["draw"]


_vine_draw = _strip_annotation(G.VineSchematic, "        # ---- annotation")
_berry_draw = _strip_annotation(G.BerrySection, "        ann = [")


class _Shim:
    """Just enough of a Flowable for the stripped draw() bodies."""
    def __init__(self, c, W, H):
        self.canv, self.width, self.height = c, W, H


class Art:
    name = ""
    aspect = 0.62          # height / width of the art box
    vis = (0.0, 1.0)       # horizontal extent actually painted, as fractions of W

    def __init__(self, W=270.0):
        self.W, self.H = W, W * self.aspect
        self.targets = self._targets()

    def draw(self, c):
        raise NotImplementedError

    def _targets(self):
        return []


# ===================================================================== zones
class Zones(Art):
    """The four structural zones -- the Mastery Guide's vine schematic."""
    name = "zones"
    aspect = 188.0 / 300.0
    vis = (0.08, 0.49)

    def draw(self, c):
        _vine_draw(_Shim(c, self.W, self.H))

    def _targets(self):
        W, H = self.W, self.H
        gx, soil_y, half = W * 0.30, H * 0.29, W * 0.148
        trunk_top = soil_y + H * 0.235
        shoot_h = H * 0.285
        spur_x = gx - half * 0.92 + 0.8 * half * 1.84        # a spur nub on the right cordon
        root_len = soil_y * 0.30
        rx = gx + 0.55 * root_len * math.cos(math.radians(-62))
        ry = soil_y - 1 + 0.55 * root_len * math.sin(math.radians(-62))
        return [("Shoots (the canopy)", (spur_x + 4, trunk_top + shoot_h * 0.55)),
                ("One-year-old wood", (spur_x, trunk_top + 2.6)),
                ("Permanent wood", (gx + 1, soil_y + H * 0.115)),
                ("Roots", (rx, ry))]


# ===================================================================== grape
class Grape(Art):
    """The grape in cross-section -- the Mastery Guide's berry."""
    name = "grape"
    aspect = 186.0 / 300.0
    vis = (0.04, 0.42)

    def draw(self, c):
        _berry_draw(_Shim(c, self.W, self.H))

    def _targets(self):
        W, H = self.W, self.H
        cx, cy = W * 0.235, H * 0.50
        R = min(W * 0.185, H * 0.34)
        ry = R * 1.08
        a = math.radians(38)
        return [("Skin", (cx + R * 0.93 * math.cos(a), cy + ry * 0.93 * math.sin(a))),
                ("Pulp", (cx + R * 0.52, cy - ry * 0.02)),
                ("Seed", (cx + 0.34 * R, cy + 0.16 * ry)),
                ("Bloom", (cx + R * 1.09, cy - ry * 0.45)),
                ("Stem", (cx - 1.4, cy + ry + 9))]


# ===================================================================== shoot
class Shoot(Art):
    """A vine shoot at flowering, springing from a cane.

    One structure per node, well separated, so every label has an unambiguous target:
      node 1 leaf (left) | node 2 leaf (right) + lateral shoot (left)
      node 3 leaf (left) + inflorescence (right) | node 4 leaf (right) + tendril (left)
      node 5 tiny young leaf (left) + a prompt bud in the axil (right)
    """
    name = "shoot"
    aspect = 0.90
    vis = (0.02, 0.50)
    NODES = (0.20, 0.40, 0.60, 0.79, 0.93)
    # (node index, side, radius)
    LEAVES = ((0, -1, 15.5), (1, 1, 15.5), (2, -1, 14.0), (3, 1, 12.0), (4, -1, 6.5))

    def _bez(self, t):
        W, H = self.W, self.H
        p = [(W * 0.20, H * 0.20), (W * 0.12, H * 0.45), (W * 0.44, H * 0.62), (W * 0.31, H * 0.975)]
        u = 1 - t
        return (u**3 * p[0][0] + 3 * u * u * t * p[1][0] + 3 * u * t * t * p[2][0] + t**3 * p[3][0],
                u**3 * p[0][1] + 3 * u * u * t * p[1][1] + 3 * u * t * t * p[2][1] + t**3 * p[3][1])

    def _leaf_c(self, i, side, R):
        x, y = self._bez(self.NODES[i])
        return x + side * (R * 0.95 + 5), y + 3 + R * 0.12

    def _lat(self):
        x, y = self._bez(self.NODES[1])
        return [(x, y), (x - 10, y + 12), (x - 17, y + 24), (x - 24, y + 38)]

    def _infl_geom(self):
        x, y = self._bez(self.NODES[2])
        return x, y, x + 30, y + 24            # node, peduncle tip

    def draw(self, c):
        W, H = self.W, self.H
        # ---- the cane the shoot grows from (one-year-old wood), with its buds
        _taper(c, W * 0.02, H * 0.150, W * 0.50, H * 0.185, 7.0, 4.6, WOOD_MID)
        _taper(c, W * 0.03, H * 0.163, W * 0.49, H * 0.196, 2.4, 1.6, WOOD_LIT)
        c.setFillColor(WOOD_DARK)
        for fx in (0.09, 0.34, 0.44):
            c.circle(W * fx, H * (0.150 + 0.035 * fx / 0.5) + 3.6, 2.1, stroke=0, fill=1)

        # ---- main green stem, tapering, with swollen nodes
        pts = [self._bez(i / 60.0) for i in range(61)]
        for i in range(60):
            c.setStrokeColor(_blend(LEAF_DARK, LEAF_MID, i / 90.0)); c.setLineWidth(3.1 - 1.9 * (i / 60.0))
            c.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])
        c.setFillColor(LEAF_DARK)
        for t in self.NODES:
            x, y = self._bez(t)
            c.circle(x, y, 2.9 - 1.0 * t, stroke=0, fill=1)

        # ---- leaves on petioles
        for k, (i, side, R) in enumerate(self.LEAVES):
            x, y = self._bez(self.NODES[i])
            lx, ly = self._leaf_c(i, side, R)
            c.setStrokeColor(LEAF_DARK); c.setLineWidth(1.0)
            c.line(x, y, lx - side * R * 0.30, ly - R * 0.48)
            _vine_leaf(c, lx, ly, R, rot=side * 8, fill=_blend(LEAF_MID, LEAF_LIGHT, (k % 2) * 0.5),
                       flip=side < 0, stalk=False)

        # ---- inflorescence (node 3, right): peduncle + a tapered cluster of tiny flower buds
        x, y, ix, iy = self._infl_geom()
        c.setStrokeColor(LEAF_DARK); c.setLineWidth(1.1)
        c.line(x, y, ix, iy)
        n = 0
        for row in range(8):
            fy = row / 7.0
            cnt = max(1, int(round(5 - 4 * fy)))
            spread = 11 * (1 - 0.8 * fy)
            for k in range(cnt):
                fx = 0.5 if cnt == 1 else k / float(cnt - 1)
                px = ix - spread + fx * 2 * spread + ((n * 7) % 3 - 1) * 0.5
                py = iy - 1 - fy * 25
                c.setFillColor(_blend(colors.HexColor("#B8C98A"), colors.HexColor("#8DA35E"), (n % 3) / 3.0))
                c.setStrokeColor(colors.HexColor("#6F8447")); c.setLineWidth(0.25)
                c.circle(px, py, 2.0, stroke=1, fill=1)
                n += 1

        # ---- tendril (node 4, left): a short stalk ending in a spiral
        x, y = self._bez(self.NODES[3])
        sx, sy = x - 11, y + 10
        c.setStrokeColor(LEAF_MID); c.setLineWidth(0.9)
        c.line(x, y, sx, sy)
        pts_s = []
        for i in range(0, 74):
            th = i * 0.17
            r = 1.2 + th * 1.05
            pts_s.append((sx - 2 + r * math.cos(th + 3.4), sy + 5 + r * math.sin(th + 3.4)))
        p = c.beginPath(); p.moveTo(*pts_s[0])
        for q in pts_s[1:]:
            p.lineTo(*q)
        c.setLineWidth(0.8); c.drawPath(p, stroke=1, fill=0)

        # ---- lateral shoot (node 2, left): a thin stem carrying two small leaves
        lp = self._lat()
        c.setStrokeColor(LEAF_MID); c.setLineWidth(1.5)
        p = c.beginPath(); p.moveTo(*lp[0]); p.curveTo(*lp[1], *lp[2], *lp[3])
        c.drawPath(p, stroke=1, fill=0)
        for (fx, fy, R, side) in ((-13.5, 16, 8.0, -1), (-22, 30, 7.0, 1)):
            _vine_leaf(c, lp[0][0] + fx + side * 5, lp[0][1] + fy, R, rot=side * 14, fill=LEAF_LIGHT,
                       flip=side < 0, stalk=False)
        c.setFillColor(LEAF_DARK); c.circle(lp[3][0], lp[3][1], 1.6, stroke=0, fill=1)

        # ---- a prompt bud in the leaf axil at node 5 (right): it has not grown out
        x, y = self._bez(self.NODES[4])
        c.setFillColor(colors.HexColor("#A68B5B")); c.setStrokeColor(WOOD_DARK); c.setLineWidth(0.5)
        c.saveState(); c.translate(x + 3.6, y + 4.6); c.rotate(-28)
        c.ellipse(-2.8, -4.2, 2.8, 4.2, stroke=1, fill=1)
        c.restoreState()

    def _targets(self):
        W, H = self.W, self.H
        bx, by = self._bez(self.NODES[4])
        leaf = self._leaf_c(1, 1, 15.5)
        _, _, ix, iy = self._infl_geom()
        tx, ty = self._bez(self.NODES[3])
        lp = self._lat()
        return [("Cane", (W * 0.28, H * 0.168), "L"),
                ("Prompt bud", (bx + 3.6, by + 4.6), "R"),
                ("Leaf", leaf, "R"),
                ("Inflorescence", (ix, iy - 12), "R"),
                ("Tendril", (tx - 13, ty + 15), "L"),
                ("Lateral shoot", (lp[0][0] - 17, lp[0][1] + 25), "L")]


# ===================================================================== flower
class Flower(Art):
    """A vine flower in section, with a pollen tube reaching the ovule."""
    name = "flower"
    aspect = 0.74
    vis = (0.19, 0.76)

    def draw(self, c):
        W, H = self.W, self.H
        cx = W * 0.50
        GREEN = colors.HexColor("#A9BE7C"); GREEN_D = colors.HexColor("#6F8447")
        YEL = colors.HexColor("#E2BE54"); YEL_D = colors.HexColor("#A8832A")
        TAN = colors.HexColor("#C8A97A")

        # --- receptacle / base
        c.setFillColor(GREEN); c.setStrokeColor(GREEN_D); c.setLineWidth(0.7)
        c.ellipse(cx - 30, H * 0.10, cx + 30, H * 0.19, stroke=1, fill=1)

        # --- stamens (filament + anther), left and right
        for s in (-1, 1):
            x0, y0 = cx + s * 24, H * 0.17
            x1, y1 = cx + s * W * 0.215, H * 0.64
            c.setStrokeColor(GREEN_D); c.setLineWidth(1.7)
            p = c.beginPath(); p.moveTo(x0, y0)
            p.curveTo(x0 + s * 22, y0 + 12, x1 - s * 10, y1 - 34, x1, y1 - 7)
            c.drawPath(p, stroke=1, fill=0)
            c.saveState(); c.translate(x1, y1); c.rotate(s * -12)
            c.setFillColor(YEL); c.setStrokeColor(YEL_D); c.setLineWidth(0.7)
            c.ellipse(-8.5, -8, 8.5, 8, stroke=1, fill=1)
            c.setStrokeColor(YEL_D); c.setLineWidth(0.4); c.line(0, -7, 0, 7)
            c.restoreState()
            c.setFillColor(YEL_D)
            for (dx, dy) in ((-3.5, 2), (3.5, -1), (0, 4.5), (-2, -4)):
                c.circle(x1 + dx, y1 + dy, 0.9, stroke=0, fill=1)
            # loose pollen drifting
            for (dx, dy) in ((s * 14, 12), (s * 20, 2), (s * 9, 19)):
                c.setFillColor(YEL); c.setStrokeColor(YEL_D); c.setLineWidth(0.3)
                c.circle(x1 + dx, y1 + dy, 1.9, stroke=1, fill=1)

        # --- ovary with two ovules, each holding an egg
        c.setFillColor(colors.HexColor("#C9D9A0")); c.setStrokeColor(GREEN_D); c.setLineWidth(0.9)
        oy = H * 0.37
        c.ellipse(cx - 29, oy - 36, cx + 29, oy + 36, stroke=1, fill=1)
        for s in (-1, 1):
            c.setFillColor(colors.HexColor("#E9DDB8")); c.setStrokeColor(TAN); c.setLineWidth(0.7)
            c.saveState(); c.translate(cx + s * 12.5, oy - 4); c.rotate(s * 10)
            c.ellipse(-8, -13, 8, 13, stroke=1, fill=1)
            c.restoreState()
            c.setFillColor(colors.HexColor("#B67A5A")); c.setStrokeColor(colors.HexColor("#7A4A32"))
            c.setLineWidth(0.4)
            c.circle(cx + s * 12.5 + s * 0.8, oy - 11, 2.5, stroke=1, fill=1)

        # --- short style + stigma
        c.setStrokeColor(GREEN_D); c.setFillColor(GREEN); c.setLineWidth(0.8)
        c.rect(cx - 4.2, oy + 34, 8.4, H * 0.14, stroke=1, fill=1)
        sy = oy + 34 + H * 0.14
        c.setFillColor(colors.HexColor("#DDE59A")); c.setStrokeColor(GREEN_D)
        c.ellipse(cx - 14, sy, cx + 14, sy + 10, stroke=1, fill=1)
        c.setStrokeColor(colors.HexColor("#9DB05B")); c.setLineWidth(0.4)
        for i in range(-5, 6):
            c.line(cx + i * 2.4, sy + 9.2, cx + i * 2.4, sy + 12.4)

        # --- pollen grains on the stigma; one has germinated and grown a tube
        for dx in (-9, 3, 9):
            c.setFillColor(YEL); c.setStrokeColor(YEL_D); c.setLineWidth(0.3)
            c.circle(cx + dx, sy + 14, 2.6, stroke=1, fill=1)
        c.setStrokeColor(colors.HexColor("#8C5A2B")); c.setLineWidth(1.1)
        p = c.beginPath(); p.moveTo(cx - 9, sy + 12)
        p.curveTo(cx - 7, sy + 4, cx - 3, oy + 40, cx - 3, oy + 28)
        p.curveTo(cx - 3, oy + 18, cx + 7, oy + 8, cx + 11.5, oy + 8)
        c.drawPath(p, stroke=1, fill=0)

    def _targets(self):
        W, H = self.W, self.H
        cx = W * 0.50
        oy = H * 0.37
        sy = oy + 34 + H * 0.14
        x1, y1 = cx + W * 0.215, H * 0.64
        return [("Anther", (cx - W * 0.215, H * 0.64 + 6), "L"),
                ("Pollen", (cx + 9, sy + 14.5), "R"),
                ("Stigma", (cx + 11, sy + 5), "R"),
                ("Pollen tube", (cx - 3, oy + 34), "L"),
                ("Ovule", (cx + 15, oy - 1), "R"),
                ("Egg", (cx - 11.7, oy - 11), "L"),
                ("Ovary", (cx - 25, oy - 24), "L"),
                ("Filament", (cx + 41, H * 0.36), "R")]
