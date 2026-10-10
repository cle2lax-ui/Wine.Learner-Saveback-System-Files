"""GUESS THE REGION: ANDERSON VALLEY -- a Reel (Arc 3, entry 2). 1080x1920, 30 fps, 45 s. Theme: usa.

Plan: arc3/GTR_ANDERSON_VALLEY_PLAN.md. The series' GTR DNA (four clues, the answer never named before the reveal, one
"release valve" clue) with what a Reel adds: the clues ESCALATE (hardest first) and a POINTS METER drops 4 -> 1 as
each clue arrives, so viewers commit early; a 3-2-1 "pause and guess"; the reveal on the real map; a closing question
whose answer is the viewer's own score. It tests The Field Guide (posted 2-3 days earlier): clue D is its callback.

TIMELINE (120 BPM, 2-second bars; every cut on a bar line; T(scene, u) gives the score its event times)
  0-3    ident     the Guess the Region ident (gtr_ident.py)
  3-5    rules     FOUR CLUES. FEWER CLUES, MORE POINTS. -- the meter arrives at 4
  5-29   clues     A, B, C, D (6 s each), each pushed in from the right; the meter flips 4 -> 3 -> 2 -> 1
  29-33  pause     PAUSE AND GUESS: a 3-2-1 countdown ring
  33-41  reveal    flag-stripes wipe; California -> Mendocino County -> Anderson Valley on the real map; ANDERSON
                   VALLEY; then the valley itself (the hillside photo) and the blurb
  41-45  cta       HOW MANY POINTS DID YOU SCORE?; next up: What Am I Drinking?; ends on black
CLUES (sources in the plan): A Boontling's "bahl hornin'" = good drinking (Anderson Valley Winegrowers, Atlas Obscura,
Time, Wikipedia; the word "Boontling" deliberately never shown: it contains "Boont", short for Boonville); B and C,
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
    ("A", 4, "Its locals once invented their own lingo. In it, \u201cbahl hornin\u2019\u201d means good drinking."),
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
    chip(f, f"CLUE {letter}", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    rise_text(f, {"A": "HARDEST", "B": "HARD", "C": "EASIER", "D": "EASIEST"}[letter], "black", 26, MUTED, 62, 340, u, 0.2,
              tracking=6)


# ============================================================================= scenes
def s_ident(u, ur=0.0, D=3.0, S=1.0):
    return ident(u, accent=RED)


def s_rules(u, ur=0.0, D=2.0, S=1.0):
    f = bg(GROUND)
    slam_text(f, "FOUR CLUES.", 150, TXT, 58, 760, u, 0.1)
    slam_text(f, "FEWER CLUES,", 112, LEMON, 58, 900, u, 0.45)
    slam_text(f, "MORE POINTS.", 112, LEMON, 58, 1020, u, 0.6)
    rise_text(f, "Pause the moment you know it.", "serif_it", 50, MUTED, 60, 1120, u, 0.95)
    return f


def _glass(f, cx, base, tilt, q, col):
    """A small line-art wine glass, tilted (for the clink in clue A)."""
    def rot(x, y):
        a = math.radians(tilt)
        return (cx + (x - cx) * math.cos(a) - (y - base) * math.sin(a), base + (x - cx) * math.sin(a) + (y - base) * math.cos(a))
    bowl = [rot(cx + 46 * math.sin(t_) * q, base - 120 * q - 70 * q * (1 - math.cos(t_))) for t_ in np.linspace(-math.pi / 2, math.pi / 2, 30)]
    stroke_path(f, bowl, col, 5)
    stroke_path(f, [rot(cx - 46 * q, base - 190 * q), rot(cx + 46 * q, base - 190 * q)], col, 5)
    stroke_path(f, [rot(cx, base - 120 * q), rot(cx, base)], col, 5)
    stroke_path(f, [rot(cx - 34 * q, base), rot(cx + 34 * q, base)], col, 5)


def s_clue_a(u, ur=0.0, D=6.0, S=1.0):
    f = bg(GROUND)
    clue_header(f, "A", u)
    clue_text(f, CLUES[0][2], u)
    if panel(f, u) > 0:
        bq = out_back(prog(u, 1.2, 1.6), 1.6)                 # a speech bubble pops
        if bq > 0:
            bx0, by0, bx1, by1 = 160, 900, 920, 1150
            cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
            hw, hh = (bx1 - bx0) / 2 * bq, (by1 - by0) / 2 * bq
            round_rect(f, cx - hw, cy - hh, cx + hw, cy + hh, 40, (255, 255, 255), 0.06)
            outline = []
            for (ax_, ay_, a0) in ((cx + hw - 40, cy - hh + 40, -90), (cx + hw - 40, cy + hh - 40, 0), (cx - hw + 40, cy + hh - 40, 90), (cx - hw + 40, cy - hh + 40, 180)):
                outline += [(ax_ + 40 * math.cos(math.radians(a0 + d)), ay_ + 40 * math.sin(math.radians(a0 + d))) for d in np.linspace(0, 90, 8)]
            stroke_path(f, outline + [outline[0]], TXT, 6)
            fill_poly(f, [(cx - 140 * bq, cy + hh - 2), (cx - 60 * bq, cy + hh - 2), (cx - 170 * bq, cy + hh + 70 * bq)], (40, 46, 84))
            stroke_path(f, [(cx - 140 * bq, cy + hh), (cx - 170 * bq, cy + hh + 70 * bq), (cx - 60 * bq, cy + hh)], TXT, 6)
            tq = out_cubic(prog(u, 1.55, 1.9))
            text(f, "bahl hornin\u2019", "serif_it", 104, LEMON, cx, cy + 34, align="center", alpha=tq, scale=0.9 + 0.1 * tq)
        cq = out_back(prog(u, 2.1, 2.4), 2.0)                 # the translation, as a chip
        if cq > 0:
            tw = text_width("= GOOD DRINKING", "black", 40, 2) + 56
            chip(f, "= GOOD DRINKING", W - 120 - tw, 1290, cq, fill=LEMON, ink=(28, 24, 26), size=40, align="left")
        gq = out_cubic(prog(u, 2.5, 2.9))                     # two glasses clink
        if gq > 0:
            sw = 18 * (1 - out_back(prog(u, 2.5, 3.0), 2.0))
            _glass(f, 230 - sw, 1400, -14, gq, TXT)
            _glass(f, 330 + sw, 1400, 14, gq, TXT)
            if prog(u, 2.9, 3.3) > 0 and prog(u, 2.9, 3.3) < 1:
                sp = prog(u, 2.9, 3.3)
                for a_ in range(0, 360, 45):
                    r0, r1 = 12 + 30 * sp, 22 + 40 * sp
                    stroke_path(f, [(280 + r0 * math.cos(math.radians(a_)), 1222 + r0 * math.sin(math.radians(a_))),
                                    (280 + r1 * math.cos(math.radians(a_)), 1222 + r1 * math.sin(math.radians(a_)))], LEMON, 4, alpha=1 - sp)
    return f


def s_clue_b(u, ur=0.0, D=6.0, S=1.0):
    f = bg(GROUND)
    clue_header(f, "B", u)
    clue_text(f, CLUES[1][2], u)
    q = panel(f, u)
    if q > 0:
        x0, y0, x1, y1 = PANEL
        keep = f.copy()
        oq = out_cubic(prog(u, 0.6, 1.1))                     # the Pacific, top left
        fill_poly(f, [(x0, y0), (x0 + 330, y0), (x0, y0 + 300)], (52, 82, 150), oq)
        for k in range(3):
            yy = y0 + 70 + k * 50
            stroke_path(f, [(x0 + 30 + 20 * j, yy + 8 * math.sin(j + ur * 3)) for j in range(0, 8)], (150, 186, 240), 3, alpha=0.6 * oq)
        hq = out_cubic(prog(u, 0.8, 1.5))                     # hills either side of a NW -> SE valley
        if hq > 0:
            off = (1 - hq) * 80
            fill_poly(f, [(x0 + 330, y0), (x1, y0), (x1, y1 - 260), (x0 + 560 + off, y0 + 420), (x0 + 200 + off, y0 + 130)],
                      (38, 74, 54), hq)
            fill_poly(f, [(x0, y0 + 300), (x0 + 120 - off, y0 + 260), (x0 + 480 - off, y0 + 560), (x1 - 200, y1), (x0, y1)],
                      (30, 62, 46), hq)
            fill_poly(f, [(x0 + 200, y0 + 130), (x0 + 560, y0 + 420), (x1, y1 - 260), (x1, y1), (x1 - 200, y1),
                          (x0 + 480, y0 + 560), (x0 + 120, y0 + 260)], (70, 104, 70), hq * 0.9)
        aq = in_out_cubic(prog(u, 1.6, 2.6))                  # the valley's axis, NW -> SE, dashed
        if aq > 0:
            p0, p1 = np.array((x0 + 170, y0 + 200)), np.array((x1 - 90, y1 - 120))
            pe = p0 + (p1 - p0) * aq
            n = int(np.hypot(*(pe - p0)) // 34)
            for j in range(n):
                a_ = p0 + (p1 - p0) * (j * 34 / np.hypot(*(p1 - p0)))
                b_ = p0 + (p1 - p0) * ((j * 34 + 20) / np.hypot(*(p1 - p0)))
                stroke_path(f, [tuple(a_), tuple(b_)], TXT, 5)
            if aq >= 1:
                d = (p1 - p0) / np.hypot(*(p1 - p0))
                nrm = np.array([-d[1], d[0]])
                fill_poly(f, [tuple(p1 + d * 20), tuple(p1 - d * 26 + nrm * 20), tuple(p1 - d * 26 - nrm * 20)], TXT)
        f[:y0] = keep[:y0]; f[y1:] = keep[y1:]; f[:, :x0] = keep[:, :x0]; f[:, x1:] = keep[:, x1:]
        rise_text(f, "PACIFIC", "black", 28, (200, 220, 250), x0 + 30, y0 + 46, u, 0.9, tracking=5)
        nq = out_cubic(prog(u, 1.0, 1.3))
        if nq > 0:
            ax_, ay_ = x1 - 70, y0 + 80
            fill_poly(f, [(ax_, ay_ - 34), (ax_ - 14, ay_ + 6), (ax_ + 14, ay_ + 6)], TXT, nq)
            text(f, "N", "black", 30, TXT, ax_, ay_ + 46, align="center", alpha=nq)
        rise_text(f, "NW", "black", 30, LEMON, x0 + 130, y0 + 190, u, 1.6, tracking=3)
        rise_text(f, "SE", "black", 30, LEMON, x1 - 150, y1 - 60, u, 2.6, tracking=3)
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


def s_pause(u, ur=0.0, D=4.0, S=1.0):
    f = bg(GROUND)
    slam_text(f, "PAUSE", 210, TXT, W / 2, 520, u, 0.05, align="center")
    slam_text(f, "AND GUESS", 120, LEMON, W / 2, 660, u, 0.3, align="center")
    cx, cy, r = W / 2, 1040, 210
    rq = out_cubic(prog(u, 0.4, 0.6))
    if rq > 0:
        stroke_path(f, [(cx + r * math.cos(a_), cy + r * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 120)], (255, 255, 255), 18, alpha=0.12 * rq)
    for k, (num, t0) in enumerate((("3", 0.6), ("2", 1.6), ("1", 2.6))):
        p = prog(u, t0, t0 + 1.0)
        if 0 < p < 1 or (k == 2 and p >= 1 and u < 3.6):
            pp = min(p, 1.0)
            a1 = -math.pi / 2 + 2 * math.pi * pp
            stroke_path(f, [(cx + r * math.cos(a_), cy + r * math.sin(a_)) for a_ in np.linspace(-math.pi / 2, a1, max(int(120 * pp), 2))], LEMON, 18)
            sc = 1.25 - 0.25 * out_back(prog(u, t0, t0 + 0.25), 2.0)
            text(f, num, "cond", 300, TXT, cx, cy + 105, align="center", scale=sc, alpha=out_cubic(prog(u, t0, t0 + 0.12)))
    rise_text(f, "4 points at A \u00b7 3 at B \u00b7 2 at C \u00b7 1 at D", "med", 38, MUTED, W / 2, 1360, u, 0.8, align="center")
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


def s_reveal(u, ur=0.0, D=8.0, S=1.0):
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
             ("Watched The Field Guide? Clue D was your way in.", "serif_it", 46, LEMON))
    for k, (ln, fn, sz, col) in enumerate(blurb):
        sz = next(z for z in range(sz, 24, -1) if text_width(ln, fn, z) <= W - 160)
        rise_text(f, ln, fn, sz, col, 80, 1330 + k * 82, u, 5.1 + 0.4 * k)
    return f


def s_cta(u, ur=0.0, D=4.0, S=1.0):
    f = bg(GROUND)
    slam_text(f, "HOW MANY POINTS", 120, TXT, W / 2, 560, u, 0.05, align="center")
    slam_text(f, "DID YOU SCORE?", 120, LEMON, W / 2, 690, u, 0.35, align="center")
    x = 90
    for k, (letter, pts) in enumerate((("A", 4), ("B", 3), ("C", 2), ("D", 1))):
        q = out_back(prog(u, 0.8 + 0.12 * k, 1.1 + 0.12 * k), 2.0)
        if q > 0:
            cx = 150 + k * 260
            round_rect(f, cx - 100 * q, 860 - 90 * q, cx + 100 * q, 860 + 90 * q, 26, TH["ground_alt"])
            text(f, str(pts), "cond", 120, LEMON if k == 0 else TXT, cx, 885, align="center", scale=q)
            text(f, f"AT {letter}", "black", 26, MUTED, cx, 932, align="center", tracking=3, alpha=min(q, 1))
    rise_text(f, "Tell us below.", "serif_it", 56, TXT, W / 2, 1100, u, 1.4, align="center")
    rise_text(f, "NEXT UP", "black", 32, MUTED, W / 2, 1260, u, 1.8, align="center", tracking=8)
    cq = out_back(prog(u, 1.95, 2.3), 1.7)
    if cq > 0:
        tw = text_width("WHAT AM I DRINKING?", "black", 42, 2) + 56
        chip(f, "WHAT AM I DRINKING?", W / 2 - tw / 2, 1335, cq, fill=RED, ink=(255, 255, 255), size=42, align="left")
    return f


# ============================================================================= the points meter (an overlay)
def meter(f, t):
    """Fixed top right from the rules to the pause, drawn ABOVE the transitions so it stays put while the clues slide
    underneath. The number flips down as each clue arrives: 4 -> 3 -> 2 -> 1."""
    if not (3.6 <= t < 29.0):
        return
    q = out_back(prog(t, 3.6, 4.0), 1.8) * (1 - prog(t, 28.6, 29.0))
    cx, cy, r = W - 140, 300, 78
    stroke_path(f, [(cx + r * math.cos(a_), cy + r * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 90)], LEMON, 7, alpha=q)
    text(f, "POINTS", "black", 24, MUTED, cx, cy - r - 18, align="center", tracking=5, alpha=q)
    # the LATEST mark reached, not the largest value (the first version took max() of the values, so the meter never
    # dropped and flashed a 5 at the first flip)
    marks = [(4.0, 4), (11.0, 3), (17.0, 2), (23.0, 1)]
    idx = max(i for i, (tt, _) in enumerate(marks) if t >= tt) if t >= 4.0 else 0
    t0, cur = marks[idx]
    prev = marks[idx - 1][1] if idx > 0 else cur
    p = prog(t, t0, t0 + 0.4)
    if t0 > 4.0 and p < 1:                                      # the old number falls away, the new one drops in
        text(f, str(prev), "cond", 110, TXT, cx, cy + 40 + 90 * out_cubic(p), align="center", alpha=q * (1 - p))
        text(f, str(cur), "cond", 110, LEMON, cx, cy + 40 - 90 * (1 - out_back(p, 1.6)), align="center", alpha=q * p)
    else:
        text(f, str(cur), "cond", 110, TXT, cx, cy + 40, align="center", alpha=q)


# ============================================================================= timeline
SCENE_TABLE = [(0.0, IDENT_DUR, s_ident, 1.0), (3.0, 2.0, s_rules, 1.0), (5.0, 6.0, s_clue_a, 1.0), (11.0, 6.0, s_clue_b, 1.0),
               (17.0, 6.0, s_clue_c, 1.0), (23.0, 6.0, s_clue_d, 1.0), (29.0, 4.0, s_pause, 1.0), (33.0, 8.0, s_reveal, 1.0),
               (41.0, 4.0, s_cta, 1.0)]
DUR = 45.0
N = int(DUR * FPS)
CUTS_STRIPES = (3.0, 33.0)
CUTS_PUSH = (5.0, 11.0, 17.0, 23.0)          # each clue pushes the last one off to the left
CUTS_WHIP = (29.0, 41.0)


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
    meter(f, t)
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
