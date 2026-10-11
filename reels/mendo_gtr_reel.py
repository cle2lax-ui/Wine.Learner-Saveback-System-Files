"""GUESS THE REGION: ANDERSON VALLEY -- a Reel (Arc 3, entry 2). 1080x1920, 30 fps, 43 s. Theme: usa.

Plan: arc3/GTR_ANDERSON_VALLEY_PLAN.md. The series' GTR DNA (four clues, the answer never named before the reveal, one
"release valve" clue) with what a Reel adds: the clues ESCALATE (hardest first, CLUE #1 .. CLUE #4); a 3-2-1 "make your
guess" countdown; the reveal on the real map; a closing question, how many clues you needed. No points (v4, Steve). It
tests The Field Guide (posted 2-3 days earlier): clue #4 is its callback.

TIMELINE (120 BPM, 2-second bars from the end of the ident; built from the scene lengths, so it follows the ident).
v5 (Steve): the ident is 2 s (1.5x faster), with a much larger wordmark.
  0-2    ident     the folded map unfolds and spins; the pin drops; GUESS THE / REGION
  2-26   clues     CLUE #1 .. CLUE #4 (6 s each); the stripes wipe opens #1, each later clue pushes in from the right
  26-30  pause     MAKE YOUR GUESS, THE ANSWER IS COMING IN: a 3-2-1 countdown ring
  30-39  reveal    flag-stripes wipe; California -> Mendocino County -> Anderson Valley on the real map; the valley; the blurb
  39-43  cta       HOW MANY CLUES DID YOU NEED?; next up: What Am I Drinking?; ends on black
CLUES (sources in the plan): A (v3, Steve: viticulture, not the local dialect) the rainfall, 900-2,000 mm a year shown as
about 35 to 79 inches (at 25.4 mm to the inch), and spring frost in the low-lying spots (D3 Ch. 23.1); B and C,
D3 Ch. 23.1; D, D3 plus geography (The Field Guide's latitude scene). Reveal blurb: D3. Deliberately not used: the
Navarro River, Boonville, Philo, Roederer Estate (entry 3).
PHOTOS: the fog (Pexels, Mick Haupt; NO location claimed); the reveal, 'Hillside Vineyards in Anderson Valley'
(Naotake Murayama, CC BY 2.0 -- credit in the caption).
"""
import math
import os
import subprocess
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_lib import (W, H, FPS, Photo, chip, clamp, darken, fill_poly, fill_rect, finish, in_cubic,  # noqa: E402
                      in_out_cubic, out_back, out_cubic, out_expo, prog, round_rect, stroke_path, text, text_width, vgrad)
import mendo_fg_reel as fg  # noqa: E402  (shared: theme colors, stripes wipe, whip, maps, chips, type helpers)
from mendo_fg_reel import (TH, RED, BLUE, GROUND, HERO, MUTED, TXT, GRAPE, stripes_wipe, whip, us_motif,  # noqa: E402
                           slam_text, rise_text, fit_chips, chip_lines, bg, photo)
from gtr_ident import ident, IDENT_DUR  # noqa: E402

LEMON = GRAPE["white"][0]
PANEL = (40, 820, W - 40, 1460)
CLUES = [
    ("A", 4, "Its vineyards see about 35 to 79 inches of rain a year, and spring frost threatens the low-lying spots."),
    ("B", 3, "A narrow valley a few miles from the Pacific, running north-west to south-east."),
    ("C", 2, "Cold air and fog funnel up a river into it, and most of its vineyards climb the slopes."),
    ("D", 1, "Pinot Noir and Chardonnay, sparkling and still, and Alsace\u2019s grapes, nine degrees south of Alsace."),
]


def wrap(txt, fname, size, maxw):
    lines, cur = [], ""
    for w_ in txt.split():
        trial = (cur + " " + w_).strip()
        if text_width(trial, fname, size) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    return lines + [cur]


def panel(f, u, color=None):
    q = out_cubic(prog(u, 0.15, 0.45))
    round_rect(f, *PANEL, 30, color or TH["map_panel"], q)
    return q


def clue_text(f, txt, u):
    for k, ln in enumerate(wrap(txt, "bold", 54, W - 120)):
        rise_text(f, ln, "bold", 54, TXT, 60, 470 + k * 74, u, 0.35 + 0.12 * k)


def clue_header(f, letter, u):
    """v4 (Steve): no points anywhere -- just CLUE #1 .. CLUE #4 (the difficulty labels went with the scoring)."""
    n = "ABCD".index(letter) + 1
    # v6 (Steve): a larger clue chip (34 -> 60px); centered at 270 so its bottom clears the clue text's first line
    chip(f, f"CLUE #{n}", 60, 270, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=60, align="left")


# ============================================================================= scenes
def s_ident(u, ur=0.0, D=3.0, S=1.0):
    return ident(u, accent=RED)


def s_clue_a(u, ur=0.0, D=6.0, S=1.0):
    """Clue A (v3): viticulture. Left, a rain gauge fills past 35 inches toward 79; right, a hillside cross-section where
    cold air pools in the hollow and frost settles there -- 'the low-lying spots', shown rather than told."""
    f = bg(GROUND)
    clue_header(f, "A", u)
    clue_text(f, CLUES[0][2], u)
    q = panel(f, u)
    if q > 0:
        x0, y0, x1, y1 = PANEL
        keep = f.copy()
        # ---- the rain gauge (left)
        gx0, gx1, gt, gb = x0 + 120, x0 + 250, y0 + 110, y1 - 150
        gq = out_cubic(prog(u, 0.9, 1.3))
        if gq > 0:
            stroke_path(f, [(gx0, gt), (gx0, gb), (gx1, gb), (gx1, gt)], TXT, 6, alpha=gq)
            inch_y = lambda v: gb - (gb - gt) * v / 90.0                       # a 0-90 inch scale
            for v in range(0, 91, 10):
                y = inch_y(v)
                fill_rect(f, gx1, y - 2, gx1 + (22 if v % 20 == 0 else 12), y + 2, TXT, 0.8 * gq)
                if v % 20 == 0:
                    text(f, str(v), "condb", 28, MUTED, gx1 + 30, y + 10, alpha=gq)
            lo, hi = 35, 79
            wq = in_out_cubic(prog(u, 1.3, 2.5))                               # the water rises to 35, then on to 79
            lvl = lo * min(wq / 0.45, 1.0) + (hi - lo) * max(0.0, (wq - 0.45) / 0.55)
            if lvl > 0:
                fill_rect(f, gx0 + 6, inch_y(lvl), gx1 - 6, gb - 3, (90, 140, 235), 0.85)
            if wq > 0.45:                                                       # the range, bracketed
                bq = out_cubic(prog(u, 2.5, 2.8))
                fill_rect(f, gx0 - 30, inch_y(hi), gx0 - 24, inch_y(lo), LEMON, bq)
                for v in (lo, hi):
                    fill_rect(f, gx0 - 44, inch_y(v) - 3, gx0 - 24, inch_y(v) + 3, LEMON, bq)
            for i, (po, xo) in enumerate(((0.0, 0.2), (0.53, 0.75), (0.21, 0.45), (0.77, 0.1), (0.38, 0.9), (0.92, 0.6))):
                ph = (ur * 1.6 + po) % 1.0                                      # irregular, like rain (evenly spaced
                if prog(u, 1.0, 1.2) > 0 and u < 3.2:                           # timings drew a tidy staircase)
                    yy = y0 + 20 + (gt - y0 - 10) * ph
                    xx = gx0 + 18 + xo * (gx1 - gx0 - 36)
                    fg._drop(f, xx, yy, 9, (130, 170, 245), 0.9 * (1 - ph * 0.3))
            rise_text(f, "35\u201379 IN", "cond", 64, LEMON, x0 + 60, y1 - 64, u, 2.6)
            rise_text(f, "OF RAIN A YEAR", "black", 26, TXT, x0 + 62, y1 - 26, u, 2.7, tracking=3)
        # ---- the frost pocket (right): a hillside cross-section; cold air drains down and pools in the hollow
        hx0, hx1, hb = x0 + 470, x1 - 40, y1 - 150
        hq = out_cubic(prog(u, 1.4, 1.9))
        if hq > 0:
            xs = np.linspace(hx0, hx1, 60)
            mid_ = (hx0 + hx1) / 2
            ys = hb - 300 * (np.abs(xs - mid_) / ((hx1 - hx0) / 2)) ** 1.6 * hq
            fill_poly(f, [(hx0, hb + 10)] + list(zip(xs, ys)) + [(hx1, hb + 10)], (52, 96, 64), 1.0)
            for j in range(9):                                                  # vines on the slopes
                xv = hx0 + 30 + j * (hx1 - hx0 - 60) / 8
                yv = float(np.interp(xv, xs, ys))
                if abs(xv - mid_) > 60:
                    stroke_path(f, [(xv, yv - 4), (xv, yv - 34 * hq)], (140, 196, 120), 4)
            pq = out_cubic(prog(u, 2.2, 3.0))                                   # the cold pool
            if pq > 0:
                lvl_y = hb - 110 * pq
                pts = [(x_, max(y_, lvl_y)) for x_, y_ in zip(xs, ys)]
                fill_poly(f, [(hx0, hb + 10)] + pts + [(hx1, hb + 10)], (200, 226, 255), 0.55 * pq)
                for sx_ in (-1, 1):                                             # cold air draining down
                    ax_ = mid_ + sx_ * (hx1 - hx0) * 0.36
                    ay_ = float(np.interp(ax_, xs, ys)) - 40
                    tip = (mid_ + sx_ * 70, hb - 150)
                    stroke_path(f, [(ax_, ay_), tip], (200, 226, 255), 4, alpha=0.8 * pq)
                    d = np.array(tip) - np.array((ax_, ay_)); d = d / np.hypot(*d); n_ = np.array([-d[1], d[0]])
                    fill_poly(f, [tuple(np.array(tip) + d * 14), tuple(np.array(tip) - d * 12 + n_ * 10),
                                  tuple(np.array(tip) - d * 12 - n_ * 10)], (200, 226, 255), 0.8 * pq)
            sq = out_back(prog(u, 2.9, 3.3), 1.8)                               # frost settles in the hollow
            if sq > 0.02:            # out_back(0) is not exactly 0: zero-length arms drew a dot (as in the bumper)
                fx_, fy_ = mid_, hb - 60
                for arm in range(6):
                    ang = math.radians(arm * 60 - 90)
                    L = 40 * sq
                    stroke_path(f, [(fx_, fy_), (fx_ + L * math.cos(ang), fy_ + L * math.sin(ang))], (255, 255, 255), 5)
            rise_text(f, "SPRING FROST", "cond", 60, TXT, hx0, y1 - 64, u, 3.0)
            rise_text(f, "IN THE LOW-LYING SPOTS", "black", 26, (200, 226, 255), hx0 + 2, y1 - 26, u, 3.1, tracking=2)
        f[:y0] = keep[:y0]; f[y1:] = keep[y1:]; f[:, :x0] = keep[:, :x0]; f[:, x1:] = keep[:, x1:]
    return f



_CB = {}


def _clue_b_geo():
    """Clue B on the REAL geography (Steve: the first version was a stylized drawing). Coastline from the US Census
    county polygons (filled as land, NO county lines, which would hint at the county); the valley is the Anderson Valley
    AVA polygon (UC Davis, CC0), unlabeled; its NW -> SE axis is the polygon's principal axis; 'a few miles from the
    Pacific' is MEASURED: the shortest distance from the AVA polygon to open ocean. Coordinates are (lon * cos(lat),
    -lat), so one unit is one degree of latitude, about 69 miles, in both directions."""
    if _CB:
        return _CB
    from shapely.geometry import Polygon, box
    from shapely.ops import nearest_points, unary_union
    av_ring = max(next(a for a in fg._AVA if a["name"] == "Anderson Valley")["rings"], key=len)
    avp = Polygon(av_ring).buffer(0)
    land = unary_union([Polygon(r).buffer(0) for rings in fg._CTY.values() for r in rings])
    x0, y0, x1, y1 = avp.bounds
    frame = box(x0 - 0.20, y0 - 0.07, x1 + 0.07, y1 + 0.07)
    ocean = frame.difference(land)
    pa, po = nearest_points(avp, ocean)
    miles = pa.distance(po) * 69.0
    # the axis runs through the polygon's AREA centroid, along its minimum rotated rectangle's long side (the first
    # version averaged the VERTICES: the jagged southern boundary has far more of them, so the axis sat on that edge)
    pts = np.asarray(av_ring)
    c = np.array(avp.centroid.coords[0])
    rect = np.asarray(avp.minimum_rotated_rectangle.exterior.coords)[:4]
    e_a, e_b = rect[1] - rect[0], rect[2] - rect[1]
    ax = e_a if np.hypot(*e_a) >= np.hypot(*e_b) else e_b
    ax = ax / np.hypot(*ax)
    proj = (pts - c) @ ax
    e1, e2 = c + ax * proj.min(), c + ax * proj.max()
    nw, se = (e1, e2) if (e1[0] + e1[1]) < (e2[0] + e2[1]) else (e2, e1)
    bx0, by0, bx1, by1 = PANEL[0] + 20, PANEL[1] + 20, PANEL[2] - 20, PANEL[3] - 20
    fx0, fy0, fx1, fy1 = frame.bounds
    sc = min((bx1 - bx0) / (fx1 - fx0), (by1 - by0) / (fy1 - fy0))
    ox, oy = (bx0 + bx1) / 2 - sc * (fx0 + fx1) / 2, (by0 + by1) / 2 - sc * (fy0 + fy1) / 2
    P = lambda r: np.column_stack([np.asarray(r)[:, 0] * sc + ox, np.asarray(r)[:, 1] * sc + oy])   # noqa: E731
    land_rings = [P(np.asarray(g.exterior.coords)) for g in (land.geoms if land.geom_type == "MultiPolygon" else [land])]
    # where to write PACIFIC: the ocean point farthest from land inside the frame
    from shapely.geometry import Point
    best, bd = None, -1
    for gx in np.linspace(fx0, fx1, 30):
        for gy in np.linspace(fy0, fy1, 30):
            q = Point(gx, gy)
            if ocean.contains(q):
                dd = q.distance(land)
                if dd > bd:
                    best, bd = (gx, gy), dd
    _CB.update(av=P(av_ring), land=land_rings, nw=P([nw])[0], se=P([se])[0], pa=P([(pa.x, pa.y)])[0], po=P([(po.x, po.y)])[0],
               miles=miles, pacific=P([best])[0])
    return _CB


def _round_clip(f, keep, box_, r=30):
    """Restore everything outside a rounded rectangle from keep."""
    x0, y0, x1, y1 = box_
    m = np.zeros((H, W), np.uint8)
    cv2.rectangle(m, (x0 + r, y0), (x1 - r, y1), 255, -1)
    cv2.rectangle(m, (x0, y0 + r), (x1, y1 - r), 255, -1)
    for cxy in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)):
        cv2.circle(m, cxy, r, 255, -1, lineType=cv2.LINE_AA)
    a = (m.astype(np.float32) / 255)[..., None]
    f[:] = f * a + keep * (1 - a)


OCEAN, LAND = (20, 36, 80), (78, 88, 124)      # land clearly lifted off the ocean (the first pass was 1.1:1, unreadable)


def s_clue_b(u, ur=0.0, D=6.0, S=1.0):
    f = bg(GROUND)
    clue_header(f, "B", u)
    clue_text(f, CLUES[1][2], u)
    q = out_cubic(prog(u, 0.15, 0.45))
    if q <= 0:
        return f
    G = _clue_b_geo()
    keep = f.copy()
    x0, y0, x1, y1 = PANEL
    f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - q) + np.array(OCEAN, np.float32) * q          # the ocean
    lq = out_cubic(prog(u, 0.5, 0.9))                                                       # the land, no borders
    for r in G["land"]:
        fill_poly(f, r, LAND, lq)
        stroke_path(f, np.vstack([r, r[:1]]), (150, 186, 240), 2, alpha=0.35 * lq)          # the coastline only
    dq = in_out_cubic(prog(u, 1.0, 1.6))                                                    # the valley
    if dq > 0:
        if dq >= 1:
            fill_poly(f, G["av"], LEMON, 0.88 * out_cubic(prog(u, 1.55, 1.85)))
        stroke_path(f, fg._perim_part(np.vstack([G["av"], G["av"][:1]]), dq), (255, 255, 255), 3)
    aq = in_out_cubic(prog(u, 1.9, 2.7))                                                    # its NW -> SE axis, dashed
    if aq > 0:
        p0, p1 = np.array(G["nw"]), np.array(G["se"])
        d = (p1 - p0) / np.hypot(*(p1 - p0))
        p0, p1 = p0 - d * 60, p1 + d * 60
        L = np.hypot(*(p1 - p0)) * aq
        s_ = 0.0
        while s_ < L:
            stroke_path(f, [tuple(p0 + d * s_), tuple(p0 + d * min(s_ + 22, L))], (255, 255, 255), 5)
            s_ += 36
        if aq >= 1:
            nrm = np.array([-d[1], d[0]])
            fill_poly(f, [tuple(p1 + d * 22), tuple(p1 - d * 24 + nrm * 18), tuple(p1 - d * 24 - nrm * 18)], (255, 255, 255))
    mq = out_cubic(prog(u, 2.8, 3.2))                                                       # the measured distance
    if mq > 0:
        pa, po = np.array(G["pa"]), np.array(G["po"])
        pe = pa + (po - pa) * mq
        stroke_path(f, [tuple(pa), tuple(pe)], HERO, 5)
        for pt in (pa, pe):
            fill_poly(f, [(pt[0] + 8 * math.cos(a_), pt[1] + 8 * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 14)], HERO)
    _round_clip(f, keep, PANEL)
    tw_p = text_width("PACIFIC", "black", 30, 6)
    px_ = min(max(G["pacific"][0], x0 + 30 + tw_p / 2), x1 - 30 - tw_p / 2)                   # inside the panel
    rise_text(f, "PACIFIC", "black", 30, (200, 220, 250), px_, G["pacific"][1] + 10, u, 0.7, align="center", tracking=6)
    nq = out_cubic(prog(u, 0.9, 1.2))
    if nq > 0:
        ax_, ay_ = x1 - 70, y0 + 80
        fill_poly(f, [(ax_, ay_ - 34), (ax_ - 14, ay_ + 6), (ax_ + 14, ay_ + 6)], TXT, nq)
        text(f, "N", "black", 30, TXT, ax_, ay_ + 46, align="center", alpha=nq)
    dvec = (np.array(G["se"]) - np.array(G["nw"])) / np.hypot(*(np.array(G["se"]) - np.array(G["nw"])))
    nwp, sep = np.array(G["nw"]) - dvec * 110, np.array(G["se"]) + dvec * 110        # clear of the arrow's ends
    rise_text(f, "NW", "black", 30, TXT, nwp[0], nwp[1] - 14, u, 2.0, align="center", tracking=3)
    rise_text(f, "SE", "black", 30, TXT, sep[0], sep[1] + 14, u, 2.6, align="center", tracking=3)
    lab = f"\u2248 {G['miles']:.0f} MILES"
    lx, ly = (G["pa"][0] + G["po"][0]) / 2, max(G["pa"][1], G["po"][1]) + 70         # BELOW the line (it covered NW)
    if mq > 0.9:
        tw = text_width(lab, "black", 30, 2) + 40
        chip(f, lab, lx - tw / 2, ly, out_back(prog(u, 3.1, 3.4), 1.8), fill=HERO, ink=(255, 255, 255), size=30, align="left")
    return f


def s_clue_c(u, ur=0.0, D=6.0, S=1.0):
    f = bg(GROUND)
    clue_header(f, "C", u)
    clue_text(f, CLUES[2][2], u)
    q = out_cubic(prog(u, 0.15, 0.6))
    if q > 0:
        x0, y0, x1, y1 = PANEL
        key = ("fogpanel", x1 - x0, y1 - y0)
        if key not in fg._cache:
            fg._cache[key] = Photo("us_mendo_fog_redwoods_pexels.jpg", 1.25, size=(x1 - x0, y1 - y0))
        img = fg._cache[key].view(zoom=1.15 - 0.1 * prog(ur, 0, D), fx=0.5, fy=0.5)
        darken(img, np.float32(0.25), GROUND)
        off = int((ur * 60) % W)                              # fog drifting across
        tex = fg._FOGTEX[y0:y1, off:off + (x1 - x0)]
        a = np.clip(0.18 + 0.35 * tex * out_cubic(prog(u, 0.8, 2.0)), 0, 0.6)[..., None]
        img = img * (1 - a) + np.array((236, 240, 246), np.float32) * a
        m = np.zeros((y1 - y0, x1 - x0), np.float32)
        cv2.rectangle(m, (0, 0), (x1 - x0 - 1, y1 - y0 - 1), 1.0, -1)
        reg = f[y0:y1, x0:x1]
        mq = q * np.ones_like(m)[..., None]
        f[y0:y1, x0:x1] = reg * (1 - mq) + img * mq
        corner = np.zeros((y1 - y0, x1 - x0), np.uint8)      # rounded corners: repaint outside a rounded rect
        cv2.rectangle(corner, (30, 0), (x1 - x0 - 31, y1 - y0 - 1), 255, -1)
        cv2.rectangle(corner, (0, 30), (x1 - x0 - 1, y1 - y0 - 31), 255, -1)
        for cxy in ((30, 30), (x1 - x0 - 31, 30), (30, y1 - y0 - 31), (x1 - x0 - 31, y1 - y0 - 31)):
            cv2.circle(corner, cxy, 30, 255, -1, lineType=cv2.LINE_AA)
        cm = (corner.astype(np.float32) / 255)[..., None]
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * cm + np.array(GROUND, np.float32) * (1 - cm)
        rise_text(f, "FOG UP A RIVER", "cond", 64, TXT, x0 + 40, y1 - 110, u, 2.0)
        rise_text(f, "VINES ON THE SLOPES", "cond", 64, LEMON, x0 + 40, y1 - 40, u, 2.4)
    return f


_BUB = [(np.random.default_rng(i + 300).random(), np.random.default_rng(i + 307).random(), np.random.default_rng(i + 313).random()) for i in range(34)]


def s_clue_d(u, ur=0.0, D=6.0, S=1.0):
    f = bg(GROUND)
    clue_header(f, "D", u)
    clue_text(f, CLUES[3][2], u)
    q = panel(f, u)
    if q > 0:
        x0, y0, x1, y1 = PANEL
        keep = f.copy()
        for i, (rx, rs, rr) in enumerate(_BUB):              # bubbles rise through the panel
            yy = y1 + 30 - ((ur * (120 + rs * 200) + rr * (y1 - y0)) % (y1 - y0 + 60))
            xx = x0 + 40 + rx * 440 + 8 * math.sin(ur * 4 + i)
            stroke_path(f, [(xx + (4 + rr * 5) * math.cos(t_), yy + (4 + rr * 5) * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 12)],
                        (255, 248, 230), 2, alpha=0.5 * q)
        f[:y0] = keep[:y0]; f[y1:] = keep[y1:]; f[:, :x0] = keep[:, :x0]; f[:, x1:] = keep[:, x1:]
        lay = fit_chips([("PINOT NOIR", "red"), ("CHARDONNAY", "white")], W, 34, gap=12)   # stacked, not one row
        yc = y0 + 80
        for k, (lines, kind, w) in enumerate(lay):
            cq = out_back(prog(u, 1.3 + 0.15 * k, 1.6 + 0.15 * k), 2.0)
            chip_lines(f, lines, x0 + 40, yc + k * 96, cq, GRAPE[kind][0], GRAPE[kind][1], 34, w)
        rise_text(f, "SPARKLING", "cond", 60, TXT, x0 + 44, y0 + 330, u, 1.7)
        rise_text(f, "AND STILL", "cond", 60, TXT, x0 + 44, y0 + 396, u, 1.8)
        X, TOP, BOT = x1 - 300, y0 + 70, y1 - 70                 # a mini latitude ruler: Alsace -> "?"
        lat_y = lambda lat: TOP + (50 - lat) / 14 * (BOT - TOP)
        rq = out_cubic(prog(u, 2.0, 2.5))
        if rq > 0:
            stroke_path(f, [(X, TOP), (X, TOP + (BOT - TOP) * rq)], TXT, 4, alpha=0.9)
            for lat in range(50, 35, -2):
                y = lat_y(lat)
                if y <= TOP + (BOT - TOP) * rq:
                    fill_rect(f, X - 12, y - 2, X, y + 2, TXT, 0.85)
        if rq >= 1:
            text(f, "ALSACE 48\u00b0", "cond", 44, (236, 226, 204), X + 30, lat_y(48) + 14)
            fill_poly(f, [(X + 4, lat_y(48)), (X + 24, lat_y(48) - 13), (X + 24, lat_y(48) + 13)], (236, 226, 204))
        tp = in_out_cubic(prog(u, 2.7, 3.6))
        if tp > 0:
            lat = 48 - 9 * tp
            y = lat_y(lat)
            stroke_path(f, [(X + 14, lat_y(48)), (X + 14, y)], LEMON, 4, alpha=0.6)
            fill_poly(f, [(X + 4, y), (X + 24, y - 13), (X + 24, y + 13)], LEMON)
            text(f, f"{lat:.0f}\u00b0" if tp < 1 else "? 39\u00b0", "cond", 50 if tp >= 1 else 44, LEMON, X + 30, y + 16)
        if tp >= 1:
            rise_text(f, "9\u00b0 SOUTH", "black", 30, HERO, X - 20, (lat_y(48) + lat_y(39)) / 2 + 10, u, 3.7, align="right", tracking=2)
    return f


GUESS_SIZE = next(sz for sz in range(128, 60, -2) if text_width("MAKE YOUR GUESS,", "cond", sz) <= W - 120)


def s_pause(u, ur=0.0, D=4.0, S=1.0):
    """Steve: 'Make Your Guess, the Answer is Coming in' with a large countdown below."""
    f = bg(GROUND)
    slam_text(f, "MAKE YOUR GUESS,", GUESS_SIZE, TXT, W / 2, 470, u, 0.05, align="center")   # fitted (128px ran 1,080px wide)
    slam_text(f, "THE ANSWER IS", 100, LEMON, W / 2, 600, u, 0.3, align="center")
    slam_text(f, "COMING IN", 100, LEMON, W / 2, 712, u, 0.42, align="center")
    cx, cy, r = W / 2, 1110, 280                     # a larger ring and number
    rq = out_cubic(prog(u, 0.4, 0.6))
    if rq > 0:
        stroke_path(f, [(cx + r * math.cos(a_), cy + r * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 140)], (255, 255, 255), 22, alpha=0.12 * rq)
    for k, (num, t0) in enumerate((("3", 0.6), ("2", 1.6), ("1", 2.6))):
        p = prog(u, t0, t0 + 1.0)
        if 0 < p < 1 or (k == 2 and p >= 1 and u < 3.6):
            pp = min(p, 1.0)
            a1 = -math.pi / 2 + 2 * math.pi * pp
            stroke_path(f, [(cx + r * math.cos(a_), cy + r * math.sin(a_)) for a_ in np.linspace(-math.pi / 2, a1, max(int(140 * pp), 2))], LEMON, 22)
            sc = 1.25 - 0.25 * out_back(prog(u, t0, t0 + 0.25), 2.0)
            text(f, num, "cond", 420, TXT, cx, cy + 148, align="center", scale=sc, alpha=out_cubic(prog(u, t0, t0 + 0.12)))
    return f


# ---- the reveal: California -> the county -> the valley, on the real map
_AV = next(a for a in fg._AVA if a["name"] == "Anderson Valley")
V_AV = fg._view(_AV["rings"], (330, 760, 750, 1240))
V_CTY2 = fg._view(fg._CTY["Mendocino"], (330, 660, 750, 1330))


def _cam_between(v0, v1, t):
    (s0, c0, sc0), (s1, c1, sc1) = v0, v1
    s = s0 * (s1 / s0) ** t
    w = (s - s0) / (s1 - s0) if s1 != s0 else t
    c = (c0[0] + (c1[0] - c0[0]) * w, c0[1] + (c1[1] - c0[1]) * w)
    scr = (sc0[0] + (sc1[0] - sc0[0]) * t, sc0[1] + (sc1[1] - sc0[1]) * t)
    return lambda r: np.column_stack([(r[:, 0] - c[0]) * s + scr[0], (r[:, 1] - c[1]) * s + scr[1]])


REVEAL_SIZE = next(sz for sz in range(128, 60, -2) if text_width("ANDERSON VALLEY", "cond", sz) <= W - 120)


def s_reveal(u, ur=0.0, D=9.0, S=1.0):
    f = bg(GROUND)
    z1 = in_out_cubic(prog(u, 0.9, 1.7))
    z2 = in_out_cubic(prog(u, 1.8, 2.6))
    P = _cam_between(fg.V_STATE, V_CTY2, z1) if z2 <= 0 else _cam_between(V_CTY2, V_AV, z2)
    x0, y0, x1, y1 = 40, 600, W - 40, 1400
    round_rect(f, x0, y0, x1, y1, 30, TH["map_panel"], out_cubic(prog(u, 0.0, 0.3)))
    keep = f.copy()
    sa = 1 - 0.6 * max(z1, z2)
    for r in fg._STATE:
        pts = P(r)
        fill_poly(f, pts, TH["ground_alt"], 0.9 * sa)
        stroke_path(f, pts, TH["map_line"], 3, alpha=sa)
    for nm, rings in fg._CTY.items():
        for r in rings:
            pts = P(r)
            if nm == "Mendocino":
                fill_poly(f, pts, RED if z1 < 0.6 else TH["map_land"], out_cubic(prog(u, 0.4, 0.8)))
                if z1 >= 0.6:
                    stroke_path(f, np.vstack([pts, pts[:1]]), TXT, 3, alpha=0.6)
            elif z1 > 0.3:
                stroke_path(f, np.vstack([pts, pts[:1]]), TH["map_line"], 2, alpha=0.3)
    aq = out_cubic(prog(u, 2.3, 2.7))
    if aq > 0:
        for r in _AV["rings"]:
            pts = P(r)
            fill_poly(f, pts, RED, aq)
            stroke_path(f, np.vstack([pts, pts[:1]]), (255, 255, 255), 4, alpha=aq)
        pr = prog(u, 2.7, 3.4)                                   # a pulse ring around the valley
        if 0 < pr < 1:
            c = np.vstack([P(r) for r in _AV["rings"]]).mean(0)
            rr = 60 + 260 * pr
            stroke_path(f, [(c[0] + rr * math.cos(a_), c[1] + rr * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 90)], LEMON, 6, alpha=1 - pr)
    f[:y0] = keep[:y0]; f[y1:] = keep[y1:]; f[:, :x0] = keep[:, :x0]; f[:, x1:] = keep[:, x1:]
    # the valley itself: the map dissolves into the hillside photo
    pq = in_out_cubic(prog(u, 4.4, 5.0))
    if pq > 0:
        img = photo("us_mendo_av_hillside_murayama.jpg").view(zoom=1.12 - 0.06 * prog(ur, 4.4, D), fx=0.5, fy=0.66)
        darken(img, vgrad(700, 1150, 0.9, 0.0), GROUND)
        darken(img, vgrad(1250, H, 0.0, 0.85), GROUND)
        f = f * (1 - pq) + img * pq
    chip(f, "THE ANSWER", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    slam_text(f, "ANDERSON VALLEY", REVEAL_SIZE, TXT, 58, 450, u, 2.7)      # fitted to the width (128px ran off the edge)
    rise_text(f, "MENDOCINO COUNTY \u00b7 CALIFORNIA", "black", 32, MUTED, 62, 520, u, 3.1, tracking=4)
    if u > 3.2:
        us_motif(f, 62, 548, prog(u, 3.2, 3.9))
    # the blurb sits on a dark card (over the bright vineyard it was unreadable), each line fitted to ONE line
    cq = out_cubic(prog(u, 5.0, 5.3))
    if cq > 0:
        round_rect(f, 40, 1250, W - 40, 1560, 28, GROUND, 0.82 * cq)
    blurb = (("Just under 1,000 ha of vines.", "bold", 46, TXT),
             ("Its Pinot Noir: fresh red fruit, medium (+) acidity.", "med", 40, (214, 218, 232)),
             ("Watched The Field Guide? Clue #4 was your way in.", "serif_it", 46, LEMON))
    for k, (ln, fn, sz, col) in enumerate(blurb):
        sz = next(z for z in range(sz, 24, -1) if text_width(ln, fn, z) <= W - 160)
        rise_text(f, ln, fn, sz, col, 80, 1330 + k * 82, u, 5.1 + 0.4 * k)
    return f


def s_cta(u, ur=0.0, D=4.0, S=1.0):
    f = bg(GROUND)
    slam_text(f, "HOW MANY CLUES", 120, TXT, W / 2, 560, u, 0.05, align="center")      # v4: no points, just clues
    slam_text(f, "DID YOU NEED?", 120, LEMON, W / 2, 690, u, 0.35, align="center")
    for k in range(4):
        q = out_back(prog(u, 0.8 + 0.12 * k, 1.1 + 0.12 * k), 2.0)
        if q > 0:
            cx = 150 + k * 260
            round_rect(f, cx - 100 * q, 860 - 90 * q, cx + 100 * q, 860 + 90 * q, 26, TH["ground_alt"])
            text(f, f"#{k + 1}", "cond", 110, LEMON if k == 0 else TXT, cx, 885, align="center", scale=q)
            text(f, "CLUE", "black", 26, MUTED, cx, 932, align="center", tracking=3, alpha=min(q, 1))
    rise_text(f, "Tell us below.", "serif_it", 56, TXT, W / 2, 1100, u, 1.4, align="center")
    rise_text(f, "NEXT UP", "black", 32, MUTED, W / 2, 1260, u, 1.8, align="center", tracking=8)
    cq = out_back(prog(u, 1.95, 2.3), 1.7)
    if cq > 0:
        tw = text_width("WHAT AM I DRINKING?", "black", 42, 2) + 56
        chip(f, "WHAT AM I DRINKING?", W / 2 - tw / 2, 1335, cq, fill=RED, ink=(255, 255, 255), size=42, align="left")
    return f


# ============================================================================= timeline
# v4 (Steve): no rules page -- straight to the first clue; the reveal holds 1 s longer (9 s), so the cut into the close
# lands on a beat (beat 3 of its bar) rather than a downbeat
# v5 (Steve: a faster ident): built from the ident's own length, so the timeline follows it (2 s now; 43 s in all)
_LEN = [(s_ident, IDENT_DUR), (s_clue_a, 6.0), (s_clue_b, 6.0), (s_clue_c, 6.0), (s_clue_d, 6.0), (s_pause, 4.0),
        (s_reveal, 9.0), (s_cta, 4.0)]
SCENE_TABLE, _t = [], 0.0
for _fn, _d in _LEN:
    SCENE_TABLE.append((_t, _d, _fn, 1.0))
    _t += _d
DUR = _t
N = int(DUR * FPS)
_START = {fn.__name__: st for st, _d, fn, _s in SCENE_TABLE}
CUTS_STRIPES = (_START["s_clue_a"], _START["s_reveal"])
CUTS_PUSH = (_START["s_clue_b"], _START["s_clue_c"], _START["s_clue_d"])   # each clue pushes the last one off
CUTS_WHIP = (_START["s_pause"], _START["s_cta"])


def T(scene, u):
    for start, dur, fn, st in SCENE_TABLE:
        if fn.__name__ == scene:
            return start + u * st
    raise KeyError(scene)


def scene_frame(t):
    for start, dur, fn, st in SCENE_TABLE:
        if start <= t < start + dur or (fn is SCENE_TABLE[-1][2] and t >= start):
            return fn((t - start) / st, ur=t - start, D=dur, S=st)


def frame_at(t):
    f = scene_frame(t)
    for c in CUTS_PUSH:
        if c - 0.25 <= t < c + 0.25:
            p = in_out_cubic(prog(t, c - 0.25, c + 0.25))
            fa, fb = scene_frame(min(t, c - 1e-3)), scene_frame(max(t, c))
            sh = int(round(p * W))
            out = np.empty_like(fa)
            out[:, :W - sh] = fa[:, sh:]
            out[:, W - sh:] = fb[:, :sh]
            f = out
    for c in CUTS_WHIP:
        if c - 0.13 <= t < c + 0.13:
            f = whip(f, in_cubic(prog(t, c - 0.13, c)), 1 - out_cubic(prog(t, c, c + 0.13)) if t >= c else 0)
    for c in CUTS_STRIPES:
        stripes_wipe(f, prog(t, c - 0.22, c + 0.22))
    if t >= DUR - 0.4:
        f *= 1 - prog(t, DUR - 0.4, DUR)
    return f


def render(out, start=0, end=None):
    end = N if end is None else end
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(start, end):
        pr.stdin.write(finish(frame_at(fi / FPS), fi).tobytes())
    pr.stdin.close()
    pr.wait()
    print("video done:", out)


def preview(times, out):
    from PIL import Image, ImageDraw
    tiles = [Image.fromarray(finish(frame_at(min(t, DUR - 1 / FPS)), int(t * FPS))).resize((270, 480)) for t in times]
    cols = min(6, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 276, rows * 500), (60, 60, 60))
    d = ImageDraw.Draw(sheet)
    for i, (im, t) in enumerate(zip(tiles, times)):
        x, y = (i % cols) * 276, (i // cols) * 500
        sheet.paste(im, (x, y))
        d.text((x + 4, y + 482), f"{t:.2f}s", fill=(255, 255, 255))
    sheet.save(out)
    print("preview:", out)


if __name__ == "__main__":
    if "--preview" in sys.argv:
        i = sys.argv.index("--preview")
        preview([float(x) for x in sys.argv[i + 1].split(",")], sys.argv[i + 2])
    elif "--render" in sys.argv:
        i = sys.argv.index("--render")
        r = sys.argv[i + 2:i + 4]
        render(sys.argv[i + 1], *(int(x) for x in r)) if len(r) == 2 else render(sys.argv[i + 1])
