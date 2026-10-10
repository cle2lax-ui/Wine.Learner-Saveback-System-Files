"""THE FIELD GUIDE: MENDOCINO -- a Reel (Arc 3, entry 1). 1080x1920, 30 fps. Theme: usa.

Steve: every Arc 3 entry is a Reel, at the Germany Reel's polish; start with The Field Guide, with
animation, music and possibly voiceover. PROOF CUT: the first 20 s (hook, the place, two climates),
built to the full standard so the motion, music and pacing can be judged before the rest is built.

TIMELINE (120 BPM, 2-second bars; every cut on a bar line). SCENE_TABLE is the single source of truth:
the score (mendo_fg_audio.py) reads every event time from it through T(scene, u).
  0-4    hook     hillside photo drifting; the stars-and-stripes motif builds (blue band, five stars in
                  turn, stripes); THE FIELD GUIDE chip; MENDOCINO drops in letter by letter, then a sheen
  4-12   place    California draws itself; Mendocino County flashes red; the camera zooms state -> county;
                  the AVAs appear IN THE ORDER THEY WERE CREATED (1982 -> 2024) with a counter and a year
                  ticker; Anderson Valley lights up (ONE FAMOUS VALLEY); Mendocino Ridge; 7,000 ha counts up
  12-20  climates photo panels slide in; the Pacific -> inland strip draws; grape chips pop (burgundy = red
                  grapes, lemon = white); "Altitude flips it": Potter Valley, Sauvignon Blanc and Riesling
TRANSITIONS: a US stripes wipe (seven red and white stripes; at its midpoint the screen IS the flag, a
starred blue canton top left). The proof fades to black at 20 s.

FACTS (WSET first, DESIGN_PROCESS s12): D3 Ch. 23.1 -- 7,000 ha under vine; the Mendocino AVA; Anderson
Valley the best known; cooler AVAs near the Pacific (Pinot Noir, Chardonnay, aromatic whites) vs warmer
inland (Zinfandel, Syrah, Petite Sirah, Cabernet Sauvignon); high, inland Potter Valley: Sauvignon Blanc
and Riesling. CSW: about 17,000 acres. TTB: 12 AVAs wholly within the county, plus Pine Mountain-Cloverdale
Peak shared with Sonoma. AVA dates and boundaries: UC Davis AVA Project (CC0); Comptche per the TTB.
PHOTOS: Commons, CC BY 2.0 (Naotake Murayama: hook, top panel) and CC0 (No-till-vineyard: bottom panel,
headed INLAND AVAs, not a named AVA, since its exact location is not stated).
"""
import json
import math
import os
import subprocess
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_lib import (W, H, FPS, ROOT, Photo, chip, clamp, darken, fill_poly, fill_rect, finish,  # noqa: E402
                      in_cubic, in_out_cubic, letters, out_back, out_cubic, out_expo, prog, round_rect,
                      sheen, stroke_path, text, text_width, vgrad)
sys.path.insert(0, f"{ROOT}/engine")
from themes import theme, GRAPE  # noqa: E402

TH = theme("usa")
RED, FLAGWHITE, BLUE = TH["bands"]
GROUND, HERO, MUTED, TXT = TH["ground"], TH["hero"], TH["muted"], TH["text"]
DUR = 65.0
N = int(DUR * FPS)
_cache = {}


def photo(name):
    if name not in _cache:
        _cache[name] = Photo(name, 1.3)
    return _cache[name]


def bg(c):
    f = np.empty((H, W, 3), np.float32)
    f[:] = c
    return f


def star(cx, cy, r):
    return [(cx + (r if k % 2 == 0 else r * 0.42) * math.cos(math.radians(-90 + 36 * k)),
             cy + (r if k % 2 == 0 else r * 0.42) * math.sin(math.radians(-90 + 36 * k))) for k in range(10)]


# ----------------------------------------------------------------------------- the US motif, animated
def us_motif(f, x, y, u, w=230):
    """Blue band with white stars on top, over red and white stripes (the USA motif; three bars read as
    Dutch). Builds over u = 0 -> 1: the band opens, the stars pop in turn, the stripes draw."""
    bh, sh, ns = 40, 8, 5
    pb = out_expo(prog(u, 0.0, 0.3))
    if pb <= 0:
        return y
    fill_rect(f, x, y, x + w * pb, y + bh, BLUE)
    for i in range(5):
        q = out_back(prog(u, 0.2 + 0.07 * i, 0.4 + 0.07 * i), 2.2)
        if q > 0:
            fill_poly(f, star(x + w * (i + 0.5) / 5, y + bh / 2, 12 * q), FLAGWHITE)
    for j in range(ns):
        q = out_expo(prog(u, 0.45 + 0.06 * j, 0.8 + 0.06 * j))
        if q > 0:
            fill_rect(f, x, y + bh + j * sh, x + w * q, y + bh + (j + 1) * sh, RED if j % 2 == 0 else FLAGWHITE)
    return y + bh + ns * sh


# ----------------------------------------------------------------------------- transition: stripes wipe
def stripes_wipe(f, p):
    """Seven red and white stripes sweep left to right, staggered. At p = 0.5 they cover the frame and the
    starred blue canton sits top left: for an instant the screen is the flag."""
    if p <= 0 or p >= 1:
        return
    BWs = 2.2 * W
    X0, X1 = -BWs, W
    sh = H / 7
    for i in range(7):
        pi_ = clamp(p + (i - 3) * 0.018)
        X = X0 + (X1 - X0) * in_out_cubic(pi_)
        fill_rect(f, X, i * sh - 1, X + BWs, (i + 1) * sh + 1, RED if i % 2 == 0 else FLAGWHITE)
    # the canton follows the UNSTAGGERED midpoint, so at p = 0.5 it sits exactly at the top left (the first
    # version tied it to the first stripe's staggered position and it sat mostly off screen on the cut)
    Xc = X0 + (X1 - X0) * in_out_cubic(p) + 0.6 * W
    cw, chh = 0.62 * W, 3 * sh
    fill_rect(f, Xc, 0, Xc + cw, chh, BLUE)
    for r in range(5):
        for c in range(4 if r % 2 == 0 else 3):
            cx = Xc + cw * ((c + (0.5 if r % 2 == 0 else 1.0)) / 4)
            cy = chh * (r + 0.6) / 5.4
            fill_poly(f, star(cx, cy, 30), FLAGWHITE)


# ============================================================================= S1 HOOK (0-4)
TITLE = "MENDOCINO"
TSIZE = next(sz for sz in range(240, 100, -2) if text_width(TITLE, "cond", sz, 6) <= W - 2 * 60)


def s_hook(u, ur=0.0, D=4.0, S=1.0):
    ph = photo("us_mendo_av_hillside_murayama.jpg")
    f = ph.view(zoom=1.14 - 0.08 * out_cubic(prog(ur, 0, D)), fx=0.5, fy=0.64)
    darken(f, vgrad(760, 1250, 0.93, 0.0), GROUND)                # hold the deep sky through the type
    darken(f, vgrad(1550, H, 0.0, 0.7), GROUND)
    chip(f, "THE FIELD GUIDE", 60, 300, out_back(prog(u, 0.2, 0.45), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    kq = out_cubic(prog(u, 0.3, 0.6))
    if kq > 0:
        text(f, "CALIFORNIA \u00b7 NORTH COAST", "black", 34, MUTED, 62, 450, tracking=5, alpha=kq, dx=-30 * (1 - kq))

    def drop(i, n):
        s = 0.32 + 0.05 * i
        p = prog(u, s, s + 0.4)
        if p <= 0:
            return dict(alpha=0)
        return dict(alpha=out_cubic(prog(u, s, s + 0.14)), dy=-200 * (1 - out_back(p, 2.0)),
                    scale=1.5 - 0.5 * out_cubic(p), mblur=int(30 * (1 - p)) if p < 0.85 else 0)
    base = 450 + TSIZE * 0.92
    letters(f, TITLE, "cond", TSIZE, TXT, 60 - 4, base, drop, align="left", tracking=6)
    sheen(f, TITLE, "cond", TSIZE, 60 - 4, base, prog(u, 1.6, 2.15), align="left", tracking=6)
    my = us_motif(f, 62, base + 36, prog(u, 0.9, 1.75))
    for j, line in enumerate(("Anderson Valley", "and its neighbors")):
        q = out_cubic(prog(u, 1.3 + 0.12 * j, 1.7 + 0.12 * j))
        if q > 0:
            text(f, line, "serif_it", 70, TXT, 62, my + 110 + j * 84, alpha=q, dy=26 * (1 - q))
    return f


# ============================================================================= S2 THE PLACE (4-12)
GEO = f"{ROOT}/data/geo"
K = math.cos(math.radians(39.3))


def _rings(geom, tol=None):
    from shapely.geometry import shape
    g = shape(geom)
    if tol:
        g = g.simplify(tol, preserve_topology=True)
    polys = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
    return [np.array([(x * K, -y) for x, y in p.exterior.coords], np.float64) for p in polys]


def _bounds(rings):
    a = np.vstack(rings)
    return a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()


_STATE = _rings(json.load(open(f"{GEO}/california.geojson"))["features"][0]["geometry"])
_CTY = {c["properties"]["name"]: _rings(c["geometry"]) for c in json.load(open(f"{GEO}/mendocino_counties.geojson"))["features"]}
_AVA = []
for _a in json.load(open(f"{GEO}/mendocino_avas.geojson"))["features"]:
    _p = _a["properties"]
    if _p["name"] == "North Coast":
        continue
    _AVA.append(dict(name=_p["name"], year=int(str(_p["created"])[:4]), rings=_rings(_a["geometry"], 0.0004),
                     shared=_p["name"] == "Pine Mountain-Cloverdale Peak"))
_AVA.sort(key=lambda a: a["year"])                                    # created order, 1982 -> 2024
PANEL = (40, 600, W - 40, 1370)


def _view(rings, box):
    x0, y0, x1, y1 = _bounds(rings)
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
    return s, ((x0 + x1) / 2, (y0 + y1) / 2), ((bx0 + bx1) / 2, (by0 + by1) / 2)


V_STATE = _view(_STATE, (220, 640, 860, 1330))
V_CTY = _view(_CTY["Mendocino"], (500, 650, 900, 1330))      # room on the left for the label column


def _cam(t):
    """Camera between the state view and the county view: scale interpolates geometrically, so the zoom
    feels constant in speed."""
    (s0, c0, sc0), (s1, c1, sc1) = V_STATE, V_CTY
    s = s0 * (s1 / s0) ** t
    w = (s - s0) / (s1 - s0) if s1 != s0 else t
    c = (c0[0] + (c1[0] - c0[0]) * w, c0[1] + (c1[1] - c0[1]) * w)
    scr = (sc0[0] + (sc1[0] - sc0[0]) * t, sc0[1] + (sc1[1] - sc0[1]) * t)
    return lambda r: np.column_stack([(r[:, 0] - c[0]) * s + scr[0], (r[:, 1] - c[1]) * s + scr[1]])


def _perim_part(ring, frac):
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(ring, axis=0).T))]
    k = np.searchsorted(d, frac * d[-1])
    return ring[:max(k, 2)]


def s_place(u, ur=0.0, D=8.0, S=1.0):
    f = bg(GROUND)
    pa = out_cubic(prog(u, 0.0, 0.35))
    round_rect(f, *PANEL, 28, TH["map_panel"], pa)
    keep = f.copy()
    z = in_out_cubic(prog(u, 1.35, 2.15))
    P = _cam(z)
    # state outline draws itself, then the county flashes red
    draw = in_out_cubic(prog(u, 0.1, 1.1))
    st_alpha = 1 - 0.65 * z
    for r in _STATE:
        pts = P(_perim_part(r, draw) if draw < 1 else r)
        if draw >= 1:
            fill_poly(f, pts, TH["ground_alt"], 0.9 * st_alpha)
        stroke_path(f, pts, TH["map_line"], 3, alpha=st_alpha)
    flash = prog(u, 0.95, 1.3)
    for nm, rings in _CTY.items():
        for r in rings:
            pts = P(r)
            if nm == "Mendocino":
                if flash > 0:
                    fill_poly(f, pts, TH["map_land"] if z > 0.6 else RED, flash * (1 if z > 0.6 else 1 - 0.35 * z))
                    if z > 0.6:
                        stroke_path(f, np.vstack([pts, pts[:1]]), TXT, 3, alpha=0.6)
            elif z > 0.3:
                stroke_path(f, np.vstack([pts, pts[:1]]), TH["map_line"], 2, alpha=0.3 * z)
    # AVAs appear in creation order
    t0, step = 2.3, 0.15
    n_in, year, shared_in = 0, None, False
    for i, a in enumerate(_AVA):
        q = prog(u, t0 + step * i, t0 + step * i + 0.25)
        if q <= 0:
            continue
        year = a["year"]
        if a["shared"]:
            shared_in = True
        else:
            n_in += 1
        hot = a["name"] == "Anderson Valley" and u > 4.1
        ridge = a["name"] == "Mendocino Ridge" and u > 4.7
        parent = a["name"] == "Mendocino"
        for r in a["rings"]:
            pts = P(r)
            if parent:
                fill_poly(f, pts, (255, 255, 255), 0.06 * q)
                stroke_path(f, np.vstack([pts, pts[:1]]), TH["map_line"], 2, alpha=0.6 * q)
            elif hot:
                fill_poly(f, pts, RED, 0.95)
                stroke_path(f, np.vstack([pts, pts[:1]]), (255, 255, 255), 3, alpha=0.95)
            elif ridge:
                fill_poly(f, pts, (110, 118, 200), 0.85)
            else:
                fill_poly(f, pts, (255, 255, 255), 0.16 * q + 0.5 * (1 - q) * (q > 0))
                stroke_path(f, np.vstack([pts, pts[:1]]), TH["map_line"], 2, alpha=0.9 * q)
    # restore everything outside the panel (the map lives on its lighter field)
    x0, y0, x1, y1 = PANEL
    f[:y0] = keep[:y0]; f[y1:] = keep[y1:]; f[:, :x0] = keep[:, :x0]; f[:, x1:] = keep[:, x1:]
    # labels: two, left column over the Pacific; straight leaders that cannot cross (one above the other,
    # anchors in the same vertical order)
    labs = []
    if u > 4.1:
        labs.append(("ANDERSON VALLEY", "Anderson Valley", HERO, out_back(prog(u, 4.1, 4.4))))
    if u > 4.7:
        labs.append(("MENDOCINO RIDGE", "Mendocino Ridge", (160, 170, 240), out_back(prog(u, 4.7, 5.0))))
    slots = {"Anderson Valley": 960, "Mendocino Ridge": 1200}
    for lab, nm, col, q in labs:
        a = next(a for a in _AVA if a["name"] == nm)
        from shapely.geometry import Polygon
        rp = max((Polygon(r) for r in a["rings"]), key=lambda p: p.area).representative_point()
        ax, ay = P(np.array([[rp.x, rp.y]]))[0]
        ly = slots[nm]
        LX = 450
        assert text_width(lab, "cond", 46) <= LX - 60, lab         # never off the left edge again
        stroke_path(f, [(ax, ay), (LX + 16, ly - 14)], MUTED, 2, alpha=0.8 * min(q, 1))
        fill_poly(f, star(ax, ay, 9 * min(q, 1)), TXT)
        text(f, lab, "cond", 46, col, LX, ly, align="right", alpha=min(q, 1), scale=min(q, 1) ** 0.3)
    text(f, "PACIFIC", "black", 30, MUTED, 74, 1330, tracking=6, alpha=0.7 * prog(u, 1.6, 2.2))
    # header: chip, counter, year ticker, +1 shared, ONE FAMOUS VALLEY
    chip(f, "THE PLACE", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    if n_in > 0:
        pop = 1 + 0.06 * math.sin(math.pi * prog(u, 4.0, 4.15))
        text(f, f"{n_in} AVA{'s' if n_in > 1 else ''}", "cond", 170, TXT, 56, 450, scale=pop)
    if year:
        text(f, str(year), "cond", 64, MUTED, W - 60, 450, align="right")
        text(f, "CREATED", "black", 26, MUTED, W - 60, 372, align="right", tracking=4)
    if shared_in:
        q = out_back(prog(u, t0 + step * 10, t0 + step * 10 + 0.3), 1.7)
        tw = text_width("+1 SHARED WITH SONOMA", "black", 30, 2) + 56
        chip(f, "+1 SHARED WITH SONOMA", W - 60 - tw, 250, q, fill=(255, 255, 255), ink=GROUND, size=30, align="left")
    q = out_cubic(prog(u, 4.15, 4.5))
    if q > 0:
        text(f, "ONE FAMOUS VALLEY.", "cond", 84, HERO, 60, 548, alpha=q, dx=-40 * (1 - q))
    # the stat
    sq = prog(u, 5.4, 6.3)
    if sq > 0:
        v = int(round(7000 * out_cubic(sq) / 100.0) * 100)
        text(f, f"{v:,} ha", "cond", 124, HERO, 60, 1530, alpha=prog(u, 5.4, 5.55))
        q2 = out_cubic(prog(u, 5.9, 6.3))
        cx = 60 + text_width("7,000 ha", "cond", 124) + 40         # measured, so the caption never touches it
        text(f, "UNDER VINE", "black", 36, TXT, cx, 1462, tracking=3, alpha=q2)
        text(f, "about 17,000 acres", "med", 38, MUTED, cx, 1512, alpha=q2)
    return f


def _split2(label):
    """Best two-line split of a multi-word label (minimizes the longer line)."""
    w = label.split()
    best = None
    for i in range(1, len(w)):
        a, b = " ".join(w[:i]), " ".join(w[i:])
        m = max(len(a), len(b))
        if best is None or m < best[0]:
            best = (m, [a, b])
    return best[1]


def fit_chips(items, avail, size, gap=14):
    """Lay out chips on ONE row: if they overflow, split the widest multi-word chip onto two lines inside
    itself, then the next widest, until the row fits (Steve: keep them on the row, wrap text in the chip).
    Returns [(lines, kind, width)], or None if even that cannot fit."""
    lay = [([v], kind) for v, kind in items]
    def width(lines):
        return max(text_width(l, "black", size, 1) for l in lines) + 56
    while True:
        ws = [width(l) for l, _ in lay]
        if sum(ws) + gap * (len(ws) - 1) <= avail:
            return [(l, k, w) for (l, k), w in zip(lay, ws)]
        cands = [i for i, (l, _) in enumerate(lay) if len(l) == 1 and " " in l[0]]
        if not cands:
            return None
        i = max(cands, key=lambda j: ws[j])
        lay[i] = (_split2(lay[i][0][0]), lay[i][1])


def chip_lines(f, lines, x, yc, q, fill, ink, size, width):
    """A chip with one or two lines of text, vertically centered on yc."""
    if q <= 0:
        return
    lh = size * 1.08
    hh = (size * 0.98) if len(lines) == 1 else (size * 0.62 + lh * len(lines) / 2)
    cx = x + width / 2
    round_rect(f, cx - width / 2 * q, yc - hh * q, cx + width / 2 * q, yc + hh * q, int(min(hh, 30)), fill)
    for k, ln in enumerate(lines):
        dy = (k - (len(lines) - 1) / 2) * lh
        text(f, ln, "black", size, ink, cx, yc + dy + size * 0.36, align="center", tracking=1, alpha=min(1.0, q * 1.2), scale=q)


# ============================================================================= S3 TWO CLIMATES (12-20)
SEAM = 930


CLIMATE_ROWS = ([("PINOT NOIR", "red"), ("CHARDONNAY", "white"), ("AROMATIC WHITES", "white")],
                [("ZINFANDEL", "red"), ("SYRAH", "red"), ("PETITE SIRAH", "red"), ("CABERNET SAUVIGNON", "red")])
# one shared chip size for both rows: the largest (34 -> 30) at which each row fits on ONE line with in-chip wrapping
CLIMATE_CHIP = next(sz for sz in (34, 33, 32, 31, 30) if all(fit_chips(r, W - 120, sz, gap=12) for r in CLIMATE_ROWS))


def s_climates(u, ur=0.0, D=8.0, S=1.0):
    f = bg(GROUND)
    for name, y0, y1, fy, start, frm in (("us_mendo_av_vineyard_murayama.jpg", 0, SEAM - 30, 0.6, 0.0, -1),
                                          ("us_mendo_garzini_cc0.jpg", SEAM + 30, H, 0.55, 0.15, 1)):
        key = (name, y1 - y0)
        if key not in _cache:
            _cache[key] = Photo(name, 1.25, size=(W, y1 - y0))
        ph = _cache[key]
        q = out_expo(prog(u, start, start + 0.6))
        if q <= 0:
            continue
        img = ph.view(zoom=1.12 - 0.08 * prog(ur, 0, D), fx=0.5, fy=fy)
        darken(img, np.float32(0.22), GROUND)
        hh = y1 - y0
        if frm < 0:      # top panel: its text sits in the lower half
            darken(img, vgrad(int(hh * 0.25), int(hh * 0.62), 0.0, 0.82, height=hh), GROUND)
        else:            # bottom panel: its text sits near the top, over bright sky
            darken(img, vgrad(0, int(hh * 0.62), 0.86, 0.45, height=hh), GROUND)
        off = int((1 - q) * (y1 - y0) * frm)
        ya, yb = y0 + off, y1 + off
        sa, sb = max(ya, 0), min(yb, H)
        if sb > sa:
            f[sa:sb] = img[sa - ya:sb - ya]
    darken(f, vgrad(0, 420, 0.85, 0.0), GROUND)
    # Pacific -> inland strip
    sp = out_expo(prog(u, 0.55, 1.1))
    cold, warm = (70, 110, 210), (205, 50, 60)
    for i in range(60):
        t = i / 59
        if t > sp:
            break
        col = tuple(cold[k] + (warm[k] - cold[k]) * t for k in range(3))
        fill_rect(f, W * t, SEAM - 30, W * (t + 1 / 59) + 1, SEAM + 30, col)
    q = out_cubic(prog(u, 0.9, 1.2))
    text(f, "PACIFIC", "black", 32, (255, 255, 255), 60, SEAM + 12, tracking=4, alpha=q)
    text(f, "INLAND", "black", 32, (255, 255, 255), W - 60, SEAM + 12, align="right", tracking=4, alpha=q)
    chip(f, "TWO CLIMATES", 60, 250, out_back(prog(u, 0.25, 0.55), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    # legend: the grape colors
    lx = W - 60
    for j, (lab, kind) in enumerate((("WHITE GRAPES", "white"), ("RED GRAPES", "red"))):
        w = text_width(lab, "black", 28, 1) + 56
        lx -= w
        chip(f, lab, lx, 250, out_back(prog(u, 0.45 + 0.1 * j, 0.75 + 0.1 * j), 1.7), fill=GRAPE[kind][0], ink=GRAPE[kind][1],
             size=28, align="left", tracking=1)
        lx -= 16

    def block(base, kicker, kcol, heading, chips, t0):
        q = out_cubic(prog(u, t0, t0 + 0.3))
        text(f, kicker, "black", 32, kcol, 60, base - 120, tracking=5, alpha=q, dx=-30 * (1 - q))

        def slam(i, n):
            s = t0 + 0.15 + 0.025 * i
            p = prog(u, s, s + 0.25)
            if p <= 0:
                return dict(alpha=0)
            return dict(alpha=out_cubic(prog(u, s, s + 0.08)), scale=1.7 - 0.7 * out_expo(p))
        letters(f, heading, "cond", 112, TXT, 58, base - 10, slam, align="left")
        lay = fit_chips(chips, W - 120, CLIMATE_CHIP, gap=12)
        assert lay is not None, chips
        x = 60
        for k, (lines, kind, w) in enumerate(lay):
            cq = out_back(prog(u, t0 + 0.55 + 0.12 * k, t0 + 0.85 + 0.12 * k), 2.0)
            chip_lines(f, lines, x, base + 72, cq, GRAPE[kind][0], GRAPE[kind][1], CLIMATE_CHIP, w)
            x += w + 12
    block(740, "COOLER \u00b7 NEAR THE PACIFIC", (160, 186, 240), "ANDERSON VALLEY",
          CLIMATE_ROWS[0], 1.0)
    block(1200, "WARMER \u00b7 FURTHER INLAND", (240, 150, 140), "INLAND AVAs",
          CLIMATE_ROWS[1], 2.4)
    # the twist: a bright WHITE callout card (Steve: cleaner, and it should pop) -- the one light element on a
    # dark page; it sits inside the safe zone (the first card ran into the caption area at the bottom)
    cq = out_back(prog(u, 4.3, 4.85), 1.3)
    if cq > 0:
        y0 = 1395 + 260 * (1 - min(cq, 1.0))
        cx0, cx1, cy1 = 40, W - 40, y0 + 200
        round_rect(f, cx0, y0 + 10, cx1, cy1 + 10, 30, (0, 0, 0), 0.35 * min(cq, 1))    # soft drop shadow
        round_rect(f, cx0, y0, cx1, cy1, 30, (246, 244, 240), min(cq, 1))
        mp = out_cubic(prog(u, 4.6, 5.0))                      # two peaks, flag blue, white snowcaps
        bx, by = 92, y0 + 165
        for px, ph, pw in ((bx + 52, 118, 66), (bx, 86, 54)):
            if mp < 0.03:                                     # a zero-height peak drew as a stray line
                break
            hgt = ph * mp
            fill_poly(f, [(px - pw, by), (px, by - hgt), (px + pw, by)], BLUE, min(cq, 1))
            if mp > 0.6:
                c = (mp - 0.6) / 0.4
                fill_poly(f, [(px - pw * 0.34, by - hgt * 0.66), (px, by - hgt), (px + pw * 0.34, by - hgt * 0.66),
                              (px + pw * 0.12, by - hgt * 0.58), (px - pw * 0.08, by - hgt * 0.7)], (255, 255, 255), c)
        tx = 252
        slam_text(f, "ALTITUDE FLIPS IT", 64, RED, tx, y0 + 74, u, 4.65)
        rise_text(f, "High, inland Potter Valley grows", "med", 34, (40, 36, 40), tx + 2, y0 + 120, u, 4.95)
        lay = fit_chips([("SAUVIGNON BLANC", "white"), ("RIESLING", "white")], W - 80 - tx, 30)
        x = tx
        for k, (lines, kind, w) in enumerate(lay):
            q = out_back(prog(u, 5.15 + 0.15 * k, 5.45 + 0.15 * k), 2.0)
            # lemon on a white card needs an edge to read as a shape: a thin darker outline under the chip
            chip_lines(f, lines, x - 2, y0 + 162, q, (196, 176, 60), GRAPE[kind][1], 30, w + 4)
            chip_lines(f, lines, x, y0 + 162, q, GRAPE[kind][0], GRAPE[kind][1], 30, w)
            x += w + 18
    return f


# ============================================================================= transitions (more)
def whip(frame, p_out, p_in):
    """Zoom-blur whip with a white flash (as in the Germany Reel)."""
    p = max(p_out, p_in)
    if p <= 0:
        return frame
    s = 1 + 0.45 * p * p
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s)
    f = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    f = cv2.blur(f, (1, int(2 + 40 * p)))
    flash = 0.75 * p ** 2
    return f * (1 - flash) + 255 * flash


_FOGTEX = cv2.resize(cv2.GaussianBlur(np.random.default_rng(3).random((96, 54)).astype(np.float32), (0, 0), 2.5),
                     (W * 2, H), interpolation=cv2.INTER_CUBIC)
_FOGTEX = (_FOGTEX - _FOGTEX.min()) / (_FOGTEX.max() - _FOGTEX.min())


def fog_sweep(f, p):
    """Into the fog scene: a bank of fog rolls across from the left and clears to the right."""
    if p <= 0 or p >= 1:
        return
    off = int(p * W)
    tex = _FOGTEX[:, off:off + W]
    xs = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    front = np.clip((p * 2.2 - xs * 0.9) * 2.5, 0, 1) * np.clip(((1 - p) * 2.2 - (1 - xs) * 0.9) * 2.5, 0, 1)
    a = np.clip(front * (0.82 + 0.3 * tex), 0, 1)[..., None]
    f[:] = f * (1 - a) + np.array((232, 236, 242), np.float32) * a


# ============================================================================= helpers for the new scenes
def _fixed_view(rings, box, pad=0.0):
    x0, y0, x1, y1 = _bounds(rings)
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / (x1 - x0), (by1 - by0) / (y1 - y0))
    cx, cy, sx, sy = (x0 + x1) / 2, (y0 + y1) / 2, (bx0 + bx1) / 2, (by0 + by1) / 2
    return lambda r: np.column_stack([(r[:, 0] - cx) * s + sx, (r[:, 1] - cy) * s + sy])


def _mask(polys, dilate=0):
    m = np.zeros((H, W), np.uint8)
    for pts in polys:
        cv2.fillPoly(m, [np.round(pts * 16).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=4)
    if dilate:
        m = cv2.dilate(m, np.ones((dilate, dilate), np.uint8))
    return m.astype(np.float32) / 255.0


def chips_row(f, items, x, y, t0, u, size=34, gap=14, max_x=None, row_h=80):
    """Grape chips that pop in turn and wrap (never dropped)."""
    max_x = max_x or W - 60
    cx, row = x, 0
    for k, (v, kind) in enumerate(items):
        w = text_width(v, "black", size, 1) + 56
        if cx + w > max_x:
            cx, row = x, row + 1
        q = out_back(prog(u, t0 + 0.12 * k, t0 + 0.3 + 0.12 * k), 2.0)
        chip(f, v, cx, y + row * row_h, q, fill=GRAPE[kind][0], ink=GRAPE[kind][1], size=size, align="left", tracking=1)
        cx += w + gap


def slam_text(f, txt, size, col, x, y, u, t0, align="left"):
    def a(i, n):
        s = t0 + 0.025 * i
        p = prog(u, s, s + 0.25)
        if p <= 0:
            return dict(alpha=0)
        return dict(alpha=out_cubic(prog(u, s, s + 0.08)), scale=1.7 - 0.7 * out_expo(p))
    letters(f, txt, "cond", size, col, x, y, a, align=align)


def rise_text(f, txt, fname, size, col, x, y, u, t0, align="left", tracking=0):
    q = out_cubic(prog(u, t0, t0 + 0.3))
    if q > 0:
        text(f, txt, fname, size, col, x, y, align=align, alpha=q, dy=24 * (1 - q), tracking=tracking)


# ============================================================================= S4 THE FOG MACHINE
_AVR = max(next(a for a in _AVA if a["name"] == "Anderson Valley")["rings"], key=len)
FOG_BOX = (110, 640, 970, 1330)
_PF = _fixed_view([_AVR], FOG_BOX, pad=0.16)
_FOG = {}


def _fog_static():
    if _FOG:
        return _FOG
    land = []
    for nm, rings in _CTY.items():
        land += [_PF(r) for r in rings]
    av = _PF(_AVR)
    land_m = _mask(land)
    av_m = _mask([av], dilate=5)
    pts = av
    c = pts.mean(0)
    u_, s_, vt = np.linalg.svd(pts - c, full_matrices=False)
    ax = vt[0]
    proj = (pts - c) @ ax
    e1, e2 = c + ax * proj.min(), c + ax * proj.max()
    nw, se = (e1, e2) if (e1[0] + e1[1]) < (e2[0] + e2[1]) else (e2, e1)
    coast = []
    for r in _CTY["Mendocino"]:
        coast += list(_PF(r))
    coast = np.array(coast)
    west = coast[coast[:, 0] < nw[0]]
    cp = west[np.argmin(np.hypot(*(west - nw).T))]
    sea = cp + (cp - nw) / max(np.hypot(*(cp - nw)), 1) * 120
    corridor = _mask([np.array([cp + (0, -26), nw + (0, -22), nw + (0, 22), cp + (0, 26)])], dilate=9)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    tpar = np.clip((((xx - nw[0]) * (se[0] - nw[0]) + (yy - nw[1]) * (se[1] - nw[1])) /
                    ((se[0] - nw[0]) ** 2 + (se[1] - nw[1]) ** 2)), 0, 1)
    cool, warm = np.array((80, 130, 225), np.float32), np.array((236, 126, 64), np.float32)
    grad = cool + (warm - cool) * tpar[..., None]
    x0, y0, x1, y1 = FOG_BOX[0] - 70, FOG_BOX[1] - 40, FOG_BOX[2] + 70, FOG_BOX[3] + 40
    box_m = np.zeros((H, W), np.float32)
    box_m[y0:y1, x0:x1] = 1
    allowed = np.clip((1 - land_m) * box_m + av_m + corridor, 0, 1)
    allowed = cv2.GaussianBlur(allowed, (0, 0), 6)
    _FOG.update(land=land, av=av, av_m=av_m, grad=grad, nw=nw, se=se, cp=cp, sea=sea, allowed=allowed,
                path=np.array([sea, cp, nw, se]), panel=(x0, y0, x1, y1))
    return _FOG


def s_fog(u, ur=0.0, D=8.0, S=1.0):
    F = _fog_static()
    f = bg(GROUND)
    x0, y0, x1, y1 = F["panel"]
    pa = out_cubic(prog(u, 0.0, 0.35))
    round_rect(f, x0, y0, x1, y1, 28, TH["map_panel"], pa)
    keep = f.copy()
    lq = out_cubic(prog(u, 0.15, 0.5))
    for pts in F["land"]:
        fill_poly(f, pts, TH["map_land"], lq)
        stroke_path(f, np.vstack([pts, pts[:1]]), TH["map_line"], 2, alpha=0.5 * lq)
    # the land stays on its panel (the first cut ran it down the page, under the callouts)
    f[:y0] = keep[:y0]; f[y1:] = keep[y1:]; f[:, :x0] = keep[:, :x0]; f[:, x1:] = keep[:, x1:]
    # the valley: outline draws, then the cool -> warm gradient fills it
    dq = in_out_cubic(prog(u, 0.4, 1.2))
    if dq > 0:
        gq = out_cubic(prog(u, 1.0, 1.6))
        if gq > 0:
            a = F["av_m"][..., None] * 0.85 * gq
            f[:] = f * (1 - a) + F["grad"] * a
        stroke_path(f, _perim_part(np.vstack([F["av"], F["av"][:1]]), dq), TXT, 3)
    # fog streams in from the Pacific, through the corridor, up the valley, thinning as it warms inland
    fq = prog(u, 1.4, 2.2) * (1 - prog(u, 7.4, 8.0) * 0.3)
    if fq > 0:
        P = F["path"]
        seg = np.hypot(*np.diff(P, axis=0).T)
        cum = np.r_[0, np.cumsum(seg)] / seg.sum()
        m = np.zeros((H, W), np.float32)
        rng_ = np.random.default_rng(21)
        NP = 120
        phase = rng_.random(NP)
        lat = (rng_.random(NP) - 0.5)
        rad = 18 + rng_.random(NP) * 22
        spd = 0.10 + rng_.random(NP) * 0.06
        for i in range(NP):
            sfrac = (phase[i] + (u - 1.4) * spd[i]) % 1.0
            k = int(np.searchsorted(cum, sfrac, side="right") - 1)
            k = min(k, len(P) - 2)
            tt = (sfrac - cum[k]) / max(cum[k + 1] - cum[k], 1e-6)
            pt = P[k] + (P[k + 1] - P[k]) * tt
            d = P[k + 1] - P[k]
            nrm = np.array([-d[1], d[0]]) / max(np.hypot(*d), 1)
            width = 60 if k == 0 else 26 if k == 1 else 34
            pt = pt + nrm * lat[i] * width * 2
            thin = 1 - 0.6 * max(0.0, (sfrac - cum[2]) / (1 - cum[2]))      # thins as the valley warms
            cv2.circle(m, (int(pt[0]), int(pt[1])), int(rad[i]), float(0.55 * thin), -1, lineType=cv2.LINE_AA)
        m = cv2.GaussianBlur(m, (0, 0), 14) * F["allowed"] * fq
        a = np.clip(m * 1.6, 0, 0.92)[..., None]
        f[:] = f * (1 - a) + np.array((236, 240, 246), np.float32) * a
    rise_text(f, "PACIFIC", "black", 30, MUTED, x0 + 30, y1 - 30, u, 0.6, tracking=6)
    # north arrow (the valley runs north-west to south-east)
    nq = out_cubic(prog(u, 0.8, 1.1))
    if nq > 0:
        ax_, ay_ = x1 - 60, y0 + 90
        fill_poly(f, [(ax_, ay_ - 34), (ax_ - 14, ay_ + 6), (ax_ + 14, ay_ + 6)], TXT, nq)
        text(f, "N", "black", 30, TXT, ax_, ay_ + 46, align="center", alpha=nq)
    chip(f, "ANDERSON VALLEY", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    slam_text(f, "COLD AIR AND FOG", 104, TXT, 58, 420, u, 0.2)
    rise_text(f, "FUNNEL IN FROM THE PACIFIC", "cond", 62, HERO, 60, 500, u, 0.6)
    rise_text(f, "along the Navarro River", "serif_it", 44, MUTED, 60, 568, u, 0.9)
    # callouts under the map: what the fog does at each end
    for j, (k1, k2, col, t0, x) in enumerate((("COLD EVENINGS", "AND MORNINGS", (150, 186, 250), 3.0, 60),
                                              ("NARROWER AND", "WARMER INLAND", (250, 160, 110), 4.2, 560))):
        q = out_cubic(prog(u, t0, t0 + 0.35))
        if q > 0:
            fill_rect(f, x, 1430, x + 8, 1530, col, q)
            text(f, k1, "cond", 52, col, x + 26, 1478, alpha=q, dx=-20 * (1 - q))
            text(f, k2, "cond", 52, TXT, x + 26, 1532, alpha=q, dx=-20 * (1 - q))
    return f


# ============================================================================= S5b ISLANDS IN THE SKY (Mendocino Ridge)
# Source: the CSW Study Guide (D3 does not cover Mendocino Ridge; DESIGN_PROCESS s12 allows any authoritative source
# where WSET is silent): only land at 1,200 ft (366 m) or above is included, so the AVA is noncontiguous ("Islands
# in the Sky"); above the fog line, the vines get cool-climate sunshine; just over 250 of its 250,000 acres are
# planted; new plantings mostly Pinot Noir, plus old-vine Zinfandel. Not claimed: "the only noncontiguous AVA"
# (the guide's 2018 wording; it may no longer hold). The ridges below are ILLUSTRATIVE, not survey data.
RIDGE_PANEL = (40, 560, W - 40, 1170)
LINE_Y = 820                                  # the 1,200 ft line inside the panel


def _ridges(xs, base, peaks):
    """A ridge line with deliberate peaks (center x, height, width). The first version used random sums of
    sines: only one peak cleared the 1,200 ft line, so the 'islands' did not read."""
    y = np.full_like(xs, base, dtype=np.float64)
    for c, h, w in peaks:
        y -= h * np.exp(-((xs - c) / w) ** 2)
    # a ridgeline is not a smooth wave: small irregularities, fixed per ridge
    y += 9 * np.sin(xs / 23.0 + base) + 6 * np.sin(xs / 11.0 + base * 1.7) + 4 * np.sin(xs / 5.3 + base * 0.3)
    return y


def s_ridge(u, ur=0.0, D=6.0, S=1.0):
    f = bg(GROUND)
    x0, y0, x1, y1 = RIDGE_PANEL
    pa = out_cubic(prog(u, 0.0, 0.3))
    keep = f.copy()
    # sky: deep navy, warmer toward a low sun at the right
    yy = np.arange(y0, y1, dtype=np.float32)[:, None, None]
    sky = np.array((14, 18, 40), np.float32) + (np.array((40, 52, 96), np.float32) - np.array((14, 18, 40), np.float32)) * ((yy - y0) / (y1 - y0))
    f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - pa) + sky * pa
    sq = out_cubic(prog(u, 0.2, 1.0))
    if sq > 0:
        yy2, xx2 = np.mgrid[y0:y1:2, x0:x1:2].astype(np.float32)
        r = np.sqrt((xx2 - 860) ** 2 + (yy2 - 690) ** 2)
        glow = cv2.resize(np.clip(1 - r / 420, 0, 1) ** 2 * 0.5 * sq, (x1 - x0, y1 - y0))[..., None]
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - glow) + np.array((250, 196, 120), np.float32) * glow
    xs = np.arange(x0, x1, 3, dtype=np.float64)
    rise = out_cubic(prog(u, 0.15, 0.9))
    # far peaks show faintly behind; on the near ridge four peaks clear the line: the islands
    layers = [(1000, [(150, 360, 120), (520, 330, 150), (900, 370, 130)], (54, 64, 112)),
              (1070, [(300, 270, 110), (700, 230, 120)], (36, 44, 84)),
              (1130, [(110, 370, 92), (430, 410, 100), (790, 390, 96), (1010, 300, 80)], (20, 26, 54))]
    profs = []
    for base, peaks, col in layers:
        yp = _ridges(xs, base + (1 - rise) * 260, peaks)
        profs.append(yp)
        fill_poly(f, [(x0, y1)] + list(zip(xs, yp)) + [(x1, y1)], col, pa)
    # vines on the near ridgetops above the line
    vq = prog(u, 1.4, 2.2)
    if vq > 0:
        near = profs[-1]
        for i in range(0, len(xs), 6):
            if near[i] < LINE_Y - 14:
                q = clamp(vq * 3 - (i / len(xs)))
                if q > 0:
                    stroke_path(f, [(xs[i], near[i] + 8), (xs[i], near[i] + 8 + min(40, LINE_Y - near[i] - 16) * q)], (120, 186, 110), 4, alpha=0.95)
    # fog rises to fill the valleys, just under the 1,200 ft line
    fq = out_cubic(prog(u, 0.5, 1.5))
    if fq > 0:
        top = y1 - (y1 - (LINE_Y + 26)) * fq
        off = int((ur * 40) % W)
        tex = _FOGTEX[y0:y1, off:off + (x1 - x0)]
        rows = np.arange(y0, y1, dtype=np.float32)[:, None]
        a = np.clip((rows - top) / 70, 0, 1) * (0.55 + 0.2 * tex)       # translucent: ridges ghost through
        a = np.clip(a, 0, 0.72)[..., None]
        f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - a) + np.array((232, 236, 244), np.float32) * a
    # the 1,200 ft line draws across, dashed
    lq = out_cubic(prog(u, 1.0, 1.6))
    if lq > 0:
        xe = x0 + 30 + (x1 - x0 - 60) * lq
        x = x0 + 30
        while x < xe:
            fill_rect(f, x, LINE_Y - 2, min(x + 26, xe), LINE_Y + 2, (255, 255, 255), 0.9)
            x += 42
        tq = out_cubic(prog(u, 1.4, 1.7))
        round_rect(f, x0 + 30, LINE_Y - 66, x0 + 30 + 300, LINE_Y - 14, 12, GROUND, 0.75 * tq)
        text(f, "1,200 FT (366 M)", "black", 30, TXT, x0 + 46, LINE_Y - 28, tracking=2, alpha=tq)
    # outside the panel stays the page
    f[:y0] = keep[:y0]; f[y1:] = keep[y1:]; f[:, :x0] = keep[:, :x0]; f[:, x1:] = keep[:, x1:]
    chip(f, "MENDOCINO RIDGE", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    slam_text(f, "ISLANDS IN THE SKY", 108, TXT, 58, 420, u, 0.2)
    rise_text(f, "vineyards above the fog line", "serif_it", 46, MUTED, 60, 496, u, 0.6)
    sq2 = prog(u, 2.3, 3.0)
    if sq2 > 0:
        v = int(round(250 * out_cubic(sq2)))
        text(f, "JUST OVER", "black", 30, MUTED, 62, 1250, tracking=3, alpha=prog(u, 2.3, 2.45))
        text(f, f"{v} ACRES", "cond", 104, HERO, 58, 1350, alpha=prog(u, 2.3, 2.45))
        rise_text(f, "of 250,000 are planted to vines", "med", 38, MUTED, 62, 1408, u, 2.9)
    # CSW: areas at 1,200 ft OR HIGHER (not "above")
    rise_text(f, "ONLY LAND AT 1,200 FT OR HIGHER COUNTS,", "condb", 32, TXT, 62, 1470, u, 3.4)
    rise_text(f, "SO THE AVA COMES IN PIECES", "condb", 32, TXT, 62, 1512, u, 3.5)
    chips_row(f, [("PINOT NOIR", "red"), ("OLD-VINE ZINFANDEL", "red")], 60, 1585, 3.9, u)
    return f


# ============================================================================= S5 BY THE NUMBERS
def _drop(f, cx, cy, r, col, a=1.0):
    pts = [(cx + r * math.cos(t_), cy + r * math.sin(t_)) for t_ in np.linspace(0, math.pi, 14)]
    pts = [(cx, cy - r * 2.1)] + [(cx + r, cy)] + pts[1:-1] + [(cx - r, cy)]
    fill_poly(f, pts, col, a)


def s_numbers(u, ur=0.0, D=6.0, S=1.0):
    f = bg(GROUND)
    chip(f, "ANDERSON VALLEY", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    slam_text(f, "BY THE NUMBERS", 110, TXT, 58, 420, u, 0.15)
    tiles = [(60, 520, 525, 1000), (555, 520, 1020, 1000), (60, 1030, 525, 1510), (555, 1030, 1020, 1510)]
    for k, (tx0, ty0, tx1, ty1) in enumerate(tiles):
        q = out_back(prog(u, 0.45 + 0.35 * k, 0.8 + 0.35 * k), 1.4)
        if q <= 0:
            continue
        cx, cy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
        hw, hh = (tx1 - tx0) / 2 * q, (ty1 - ty0) / 2 * q
        round_rect(f, cx - hw, cy - hh, cx + hw, cy + hh, 26, TH["ground_alt"])
        if q < 0.9:
            continue
        lu = u - (0.8 + 0.35 * k)                         # the tile's own clock
        if k == 0:     # rain
            for j in range(3):
                yy = ty0 + 70 + ((lu * 260 + j * 70) % 150)
                _drop(f, tx0 + 120 + j * 70, yy, 14, (130, 170, 245), 0.9)
            lo = int(900 * out_cubic(prog(lu, 0.0, 0.5)))
            hi = int(900 + 1100 * out_cubic(prog(lu, 0.5, 1.1)))
            label = f"{lo:,}" if lu < 0.5 else f"900\u2013{hi:,}"
            text(f, label, "cond", 92, HERO, tx0 + 34, ty0 + 330)
            text(f, "MM OF RAIN A YEAR", "black", 28, TXT, tx0 + 36, ty0 + 380, tracking=2)
            rise_text(f, "wettest in the north-west", "med", 30, MUTED, tx0 + 36, ty0 + 428, u, 0.8 + 0.35 * k + 1.0)
        elif k == 1:   # slopes
            hp_ = out_cubic(prog(lu, 0.0, 0.6))
            base = ty0 + 250
            hill = [(tx0 + 40, base)] + [(tx0 + 40 + x, base - 150 * math.sin(math.pi * x / 380) ** 1.3 * hp_) for x in np.linspace(0, 380, 30)] + [(tx0 + 420, base)]
            fill_poly(f, hill, (52, 96, 64))
            for j in range(7):
                x = tx0 + 90 + j * 45
                yt = base - 150 * math.sin(math.pi * (x - tx0 - 40) / 380) ** 1.3 * hp_
                if prog(lu, 0.3 + 0.05 * j, 0.5 + 0.05 * j) > 0:
                    stroke_path(f, [(x, base - 8), (x, yt + 12)], (140, 196, 120), 4, alpha=prog(lu, 0.3 + 0.05 * j, 0.5 + 0.05 * j))
            text(f, "MOST VINEYARDS", "cond", 58, TXT, tx0 + 36, ty0 + 350)
            text(f, "ON THE SLOPES", "cond", 58, HERO, tx0 + 36, ty0 + 412)
        elif k == 2:   # frost
            sp = out_cubic(prog(lu, 0.0, 0.7))
            fx, fy = tx0 + 120, ty0 + 150
            for arm in range(6):
                ang = math.radians(arm * 60 - 90)
                L = 80 * sp
                ex, ey = fx + L * math.cos(ang), fy + L * math.sin(ang)
                stroke_path(f, [(fx, fy), (ex, ey)], (200, 226, 255), 5)
                for b in (0.55, 0.8):
                    bx, by = fx + L * b * math.cos(ang), fy + L * b * math.sin(ang)
                    for side in (-1, 1):
                        a2 = ang + side * math.radians(45)
                        stroke_path(f, [(bx, by), (bx + 22 * sp * math.cos(a2), by + 22 * sp * math.sin(a2))], (200, 226, 255), 4)
            text(f, "SPRING FROST", "cond", 58, TXT, tx0 + 36, ty0 + 350)
            text(f, "IN THE LOW SPOTS", "cond", 58, (170, 206, 255), tx0 + 36, ty0 + 412)
        else:          # planted
            v = int(round(1000 * out_cubic(prog(lu, 0.0, 0.8)) / 10.0) * 10)
            text(f, "JUST UNDER", "black", 30, MUTED, tx0 + 36, ty0 + 150, tracking=3)
            text(f, f"{v:,} ha", "cond", 110, HERO, tx0 + 34, ty0 + 290)
            text(f, "PLANTED", "black", 30, TXT, tx0 + 36, ty0 + 350, tracking=3)
    return f


# ============================================================================= S6 THE PINOT NOIR
def _circle(f, cx, cy, r, col, a=1.0):
    fill_poly(f, [(cx + r * math.cos(t_), cy + r * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 28)], col, a)


def _raspberry(f, cx, cy, q):
    for row, n in enumerate((3, 4, 5, 4, 3)):
        for i in range(n):
            x = cx + (i - (n - 1) / 2) * 22 * q
            y = cy + (row - 2) * 19 * q
            _circle(f, x, y, 12 * q, (190, 30, 72))
            _circle(f, x - 3 * q, y - 4 * q, 4 * q, (240, 120, 150), 0.8)


def _cherries(f, cx, cy, q):
    stroke_path(f, [(cx - 26 * q, cy), (cx + 4 * q, cy - 80 * q), (cx + 30 * q, cy + 6 * q)], (110, 140, 60), 5)
    for dx in (-26, 30):
        _circle(f, cx + dx * q, cy + 22 * q, 30 * q, (150, 12, 34))
        _circle(f, cx + dx * q - 10 * q, cy + 12 * q, 8 * q, (240, 140, 150), 0.7)


def _plum(f, cx, cy, q):
    fill_poly(f, [(cx + 44 * q * math.cos(t_), cy + 52 * q * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 32)], (96, 34, 96))
    stroke_path(f, [(cx, cy - 50 * q), (cx + 4 * q, cy - 72 * q)], (110, 140, 60), 5)
    fill_poly(f, [(cx - 18 * q + 10 * q * math.cos(t_), cy - 14 * q + 16 * q * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 16)],
              (190, 150, 210), 0.45)


def s_pinot(u, ur=0.0, D=8.0, S=1.0):
    f = bg(GROUND)
    chip(f, "IN THE GLASS", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    rise_text(f, "ANDERSON VALLEY", "black", 34, MUTED, 62, 360, u, 0.15, tracking=5)
    slam_text(f, "PINOT NOIR", 150, TXT, 56, 500, u, 0.3)
    labels = ["LOW", "MED (\u2013)", "MEDIUM", "MED (+)", "HIGH"]
    for j, (name, lvl, val, t0) in enumerate((("BODY", 3, "MEDIUM", 1.0), ("ACIDITY", 4, "MEDIUM (+)", 1.5))):
        y = 660 + j * 150
        q = out_cubic(prog(u, t0 - 0.2, t0))
        if q <= 0:
            continue
        text(f, name, "black", 34, TXT, 62, y + 40, alpha=q, tracking=3)
        for s_ in range(5):
            x = 300 + s_ * 100
            fill_rect(f, x, y, x + 88, y + 52, TH["ground_alt"], q)
            fq = out_expo(prog(u, t0 + 0.1 * s_, t0 + 0.1 * s_ + 0.25))
            if s_ < lvl and fq > 0:
                fill_rect(f, x, y, x + 88 * fq, y + 52, RED)
        vq = out_cubic(prog(u, t0 + 0.5, t0 + 0.8))
        text(f, val, "cond", 50, HERO, W - 60, y + 44, align="right", alpha=vq)    # inside the margin
        if j == 1:
            for s_, lab in enumerate(labels):
                text(f, lab, "condb", 26, MUTED, 300 + s_ * 100 + 44, y + 96, align="center", alpha=q * 0.9)
    rise_text(f, "FRESH RED FRUIT", "black", 34, TXT, 62, 1020, u, 2.3, tracking=3)
    for k, (fn, lab) in enumerate(((_raspberry, "RASPBERRY"), (_cherries, "CHERRY"), (_plum, "PLUM"))):
        q = out_back(prog(u, 2.5 + 0.25 * k, 2.85 + 0.25 * k), 1.8)
        if q > 0:
            cx = 200 + k * 340
            fn(f, cx, 1150, q)
            text(f, lab, "black", 28, MUTED, cx, 1262, align="center", alpha=min(q, 1), tracking=2)
    for k, (cap, val, fill, ink) in enumerate((("QUALITY", "GOOD TO OUTSTANDING", (255, 255, 255), GROUND),
                                                ("PRICE", "PREMIUM", RED, (255, 255, 255)))):
        q = out_back(prog(u, 3.6 + 0.25 * k, 3.9 + 0.25 * k), 1.7)
        x = 60 if k == 0 else 640
        if q > 0:
            text(f, cap, "black", 26, MUTED, x + 4, 1356, tracking=4, alpha=min(q, 1))
            chip(f, val, x, 1410, q, fill=fill, ink=ink, size=36, align="left", tracking=1)
    return f


# ============================================================================= S7 SPARKLING, AND THE ALSACE WHITES
_BUB = [(np.random.default_rng(i).random(), np.random.default_rng(i + 7).random(), np.random.default_rng(i + 13).random()) for i in range(60)]


def s_sparkle(u, ur=0.0, D=10.0, S=1.0):
    half = out_cubic(prog(u, 3.9, 4.4))
    a = photo("us_mendo_roederer_flute_cc0.jpg").view(zoom=1.12 - 0.06 * prog(ur, 0, D), fx=0.5, fy=0.5)
    if half > 0:
        b = photo("us_mendo_husch_philo_cc0.jpg").view(zoom=1.15 - 0.08 * prog(ur, 4, D), fx=0.55, fy=0.55)
        f = a * (1 - half) + b * half
    else:
        f = a
    darken(f, np.float32(0.38), GROUND)
    darken(f, vgrad(0, 900, 0.85, 0.2), GROUND)
    darken(f, vgrad(1200, H, 0.0, 0.7), GROUND)
    # bubbles rise through the first half, burst into the second
    for i, (rx, rs, rr) in enumerate(_BUB):
        yy = H + 40 - ((u * (220 + rs * 360) + rr * H) % (H + 80))
        xx = 80 + rx * (W - 160) + 10 * math.sin(u * 4 + i)
        alpha = 0.55 * (1 - half) + 0.0
        if alpha > 0.02:
            stroke_path(f, [(xx + (4 + rr * 5) * math.cos(t_), yy + (4 + rr * 5) * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 12)],
                        (255, 248, 230), 2, alpha=alpha)
    if half < 1:
        q1 = 1 - half
        chip(f, "SPARKLING AND STILL", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7) * q1, fill=RED, ink=(255, 255, 255), size=34, align="left")
        if q1 > 0.5:
            slam_text(f, "PINOT NOIR", 132, TXT, 56, 430, u, 0.25)
            slam_text(f, "+ CHARDONNAY", 132, TXT, 56, 560, u, 0.55)
            rise_text(f, "the two most planted, for sparkling", "med", 40, MUTED, 60, 640, u, 1.1)
            rise_text(f, "and still wines alike", "med", 40, MUTED, 60, 694, u, 1.2)
            chips_row(f, [("PINOT NOIR", "red"), ("CHARDONNAY", "white")], 60, 790, 1.5, u)
    if half > 0:
        # Steve: the aromatic-whites page was a list. Now it makes a point: Alsace's grapes grow here about 9 degrees
        # of latitude further south than Alsace (about 48 N vs about 39 N, roughly 1,000 km / 620 mi at ~111 km a
        # degree; Washington, D.C. is 38.9 N), because cold Pacific air and fog keep the valley cool (D3).
        darken(f, np.float32(0.35 * half), GROUND)
        chip(f, "ALSACE-STYLE WHITES", 60, 250, half, fill=RED, ink=(255, 255, 255), size=34, align="left")
        slam_text(f, "ALSACE'S GRAPES,", 104, TXT, 56, 410, u, 4.3)
        slam_text(f, "9\u00b0 FURTHER SOUTH", 104, GRAPE["white"][0], 56, 520, u, 4.55)
        # the latitude ruler
        X, TOP, BOT = 300, 640, 1300
        lat_y = lambda lat: TOP + (50 - lat) / (50 - 36) * (BOT - TOP)
        rq = out_cubic(prog(u, 4.7, 5.2))
        if rq > 0:
            stroke_path(f, [(X, TOP), (X, TOP + (BOT - TOP) * rq)], TXT, 4, alpha=0.9)
            for lat in range(50, 35, -2):
                y = lat_y(lat)
                if y <= TOP + (BOT - TOP) * rq:
                    fill_rect(f, X - 14, y - 2, X, y + 2, TXT, 0.9)
                    text(f, f"{lat}\u00b0N", "condb", 30, MUTED, X - 24, y + 10, align="right")
        def pin(lat, label, sub, col, q):
            if q <= 0:
                return
            y = lat_y(lat)
            fill_poly(f, [(X + 6, y), (X + 34, y - 18), (X + 34, y + 18)], col, min(q, 1))
            round_rect(f, X + 34, y - 18, X + 52, y + 18, 4, col, min(q, 1))
            text(f, label, "cond", 58, col, X + 72, y + 4, alpha=min(q, 1), dx=-30 * (1 - min(q, 1)))
            text(f, sub, "med", 30, MUTED, X + 74, y + 44, alpha=min(q, 1))
        pin(48, "ALSACE", "France, about 48\u00b0N", (236, 226, 204), out_back(prog(u, 5.15, 5.45), 1.6))
        # the second pin travels down the ruler, counting degrees, and lands at Anderson Valley
        tp = in_out_cubic(prog(u, 5.6, 6.4))
        if tp > 0:
            lat = 48 - 9 * tp
            y = lat_y(lat)
            stroke_path(f, [(X + 20, lat_y(48)), (X + 20, y)], GRAPE["white"][0], 4, alpha=0.55)
            if tp < 1:
                fill_poly(f, [(X + 6, y), (X + 34, y - 18), (X + 34, y + 18)], GRAPE["white"][0])
                text(f, f"{lat:.0f}\u00b0N", "cond", 50, GRAPE["white"][0], X + 60, y + 18)
            else:
                pin(39, "ANDERSON VALLEY", "about 39\u00b0N, the latitude of Washington, D.C.", GRAPE["white"][0], 1.0)
        bq = out_cubic(prog(u, 6.5, 6.9))
        if bq > 0:                                             # the gap, bracketed
            y48, y39 = lat_y(48), lat_y(39)
            bx = 150
            stroke_path(f, [(bx + 20, y48), (bx, y48), (bx, y48 + (y39 - y48) * bq), (bx + 20, y48 + (y39 - y48) * bq)], HERO, 4)
            if bq > 0.9:
                text(f, "\u2248 9\u00b0", "cond", 54, HERO, bx - 16, (y48 + y39) / 2 - 4, align="right")
                text(f, "1,000 km", "condb", 30, HERO, bx - 16, (y48 + y39) / 2 + 34, align="right")
                text(f, "620 mi", "condb", 30, HERO, bx - 16, (y48 + y39) / 2 + 68, align="right")
        rise_text(f, "Cold Pacific air keeps it cool enough.", "serif_it", 46, TXT, 60, 1400, u, 7.0)
        AW = [("GEWURZTRAMINER", "white"), ("RIESLING", "white"), ("PINOT GRIS", "white"), ("PINOT BLANC", "white")]
        csz = next(sz for sz in (30, 29, 28, 27, 26) if fit_chips(AW, W - 120, sz, gap=12))   # one row, as on Two Climates
        lay = fit_chips(AW, W - 120, csz, gap=12)
        x = 60
        for k, (lines, kind, w) in enumerate(lay):
            q = out_back(prog(u, 7.4 + 0.12 * k, 7.7 + 0.12 * k), 2.0)
            chip_lines(f, lines, x, 1490, q, GRAPE[kind][0], GRAPE[kind][1], csz, w)
            x += w + 12
    return f


# ============================================================================= S8 THE BUSINESS
def s_business(u, ur=0.0, D=6.0, S=1.0):
    f = bg(GROUND)
    chip(f, "THE BUSINESS", 60, 250, out_back(prog(u, 0.05, 0.35), 1.7), fill=RED, ink=(255, 255, 255), size=34, align="left")
    slam_text(f, "VALUE, AND DEMAND", 100, TXT, 58, 410, u, 0.15)
    rows = [("PRICED BELOW", "NAPA AND SONOMA", "Mendocino grapes, generally", "tag"),
            ("OFTEN BLENDED", "ACROSS REGIONS", "in multi-regional blends", "merge"),
            ("BOUGHT BY WINERIES", "ELSEWHERE", "Anderson Valley fruit", "out")]
    for k, (l1, l2, note, icon) in enumerate(rows):
        t0 = 0.6 + 1.0 * k
        q = out_expo(prog(u, t0, t0 + 0.45))
        if q <= 0:
            continue
        y = 560 + k * 330
        ix = 150 - 260 * (1 - q)
        iy = y + 110
        round_rect(f, 60 - 260 * (1 - q), y, 1020, y + 270, 26, TH["ground_alt"], min(q * 1.2, 1))
        if icon == "tag":
            fill_poly(f, [(ix - 60, iy - 40), (ix + 30, iy - 40), (ix + 70, iy), (ix + 30, iy + 40), (ix - 60, iy + 40)], (236, 226, 204))
            _circle(f, ix + 26, iy, 9, TH["ground_alt"])
            aq = out_cubic(prog(u, t0 + 0.4, t0 + 0.8))
            stroke_path(f, [(ix + 10, iy + 60), (ix + 10, iy + 60 + 70 * aq)], HERO, 7)
            if aq > 0.9:
                fill_poly(f, [(ix - 8, iy + 124), (ix + 28, iy + 124), (ix + 10, iy + 148)], HERO)
        elif icon == "merge":
            aq = out_cubic(prog(u, t0 + 0.3, t0 + 0.9))
            for j, col in enumerate(((150, 30, 60), (90, 40, 110), (200, 60, 70))):
                sx, sy = ix - 70 + j * 70, iy - 70
                ex, ey = ix, iy + 40
                _circle(f, sx + (ex - sx) * aq, sy + (ey - sy) * aq, 18, col)
            fill_poly(f, [(ix - 22, iy + 30), (ix + 22, iy + 30), (ix + 22, iy + 110), (ix - 22, iy + 110)], (236, 226, 204))
            fill_poly(f, [(ix - 9, iy + 6), (ix + 9, iy + 6), (ix + 9, iy + 30), (ix - 9, iy + 30)], (236, 226, 204))
        else:
            for j in range(3):
                for i in range(4 - j):
                    _circle(f, ix - 30 + i * 20 + j * 10, iy - 20 + j * 18, 11, (130, 30, 70))
            aq = out_cubic(prog(u, t0 + 0.4, t0 + 0.9))
            for ang in (-40, 0, 40):
                a_ = math.radians(ang)
                stroke_path(f, [(ix + 40, iy + 10), (ix + 40 + 80 * aq * math.cos(a_), iy + 10 + 80 * aq * math.sin(a_))], HERO, 5)
        text(f, l1, "cond", 60, TXT, 290, y + 110, alpha=q)
        text(f, l2, "cond", 60, HERO, 290, y + 172, alpha=q)
        text(f, note, "med", 34, MUTED, 292, y + 226, alpha=q)
    return f


# ============================================================================= S9 CLOSE
_EMBLEM = {}


def _emblem():
    if "img" not in _EMBLEM:
        from tfg_bumper import bumper as _b, GROUND as BG
        full = _b(2.6)
        # crop to whatever the bumper actually draws above its wordmark (fixed coordinates broke when the
        # bumper changed from a book stack to a book beside the glass)
        ink = np.abs(full[:1240] - np.array(BG, np.float32)).sum(2) > 60
        ys, xs = np.where(ink)
        y0, y1 = max(ys.min() - 30, 0), ys.max() + 30
        x0, x1 = max(xs.min() - 30, 0), min(xs.max() + 30, W)
        crop = full[y0:y1, x0:x1]
        sc = min(0.55, 520 / crop.shape[1])
        small = cv2.resize(crop, (int(crop.shape[1] * sc), int(crop.shape[0] * sc)), interpolation=cv2.INTER_AREA)
        _EMBLEM["img"] = small
    return _EMBLEM["img"]


def s_close(u, ur=0.0, D=4.0, S=1.0):
    """The end card: the place, and the next post. The brand closes the Reel in the outro that follows."""
    from tfg_bumper import GROUND as BG
    f = bg(BG)
    rise_text(f, "THAT WAS", "black", 34, MUTED, W / 2, 700, u, 0.1, align="center", tracking=8)
    slam_text(f, "MENDOCINO", 170, TXT, W / 2, 880, u, 0.25, align="center")
    us_motif(f, W / 2 - 115, 930, prog(u, 0.6, 1.3))
    rise_text(f, "NEXT UP", "black", 34, MUTED, W / 2, 1160, u, 1.3, align="center", tracking=8)
    cq = out_back(prog(u, 1.45, 1.85), 1.7)
    if cq > 0:
        tw = text_width("GUESS THE REGION", "black", 44, 2) + 56
        chip(f, "GUESS THE REGION", W / 2 - tw / 2, 1240, cq, fill=RED, ink=(255, 255, 255), size=44, align="left")
    rise_text(f, "Follow for the whole series", "serif_it", 48, MUTED, W / 2, 1380, u, 2.0, align="center")
    return f


# ============================================================================= timeline (v2: 65 s, with the bumper)
from tfg_bumper import bumper as _bumper, bumper_outro as _bumper_outro, BUMPER_DUR  # noqa: E402


def s_bumper(u, ur=0.0, D=3.0, S=1.0):
    return _bumper(u, accent=RED)


def s_outro(u, ur=0.0, D=3.0, S=1.0):
    """Steve: close the Reel with the same bug, the wine glass empty and the book swung closed."""
    return _bumper_outro(u, accent=RED)


# (start, duration, scene, stretch). Every scene after the bumper is a whole number of 2-second bars, so
# every cut lands on a downbeat of the score (whose grid starts when the bumper ends, at 3.0 s).
# v3 (72 s): Islands in the Sky added after the fog (Steve: one more fact-based slide); the end card is 4 s and
# the outro bug closes the Reel.
SCENE_TABLE = [(0.0, BUMPER_DUR, s_bumper, 1.0), (3.0, 4.0, s_hook, 1.0), (7.0, 8.0, s_place, 1.0),
               (15.0, 8.0, s_climates, 1.0), (23.0, 8.0, s_fog, 1.0), (31.0, 6.0, s_ridge, 1.0),
               (37.0, 6.0, s_numbers, 1.0), (43.0, 8.0, s_pinot, 1.0), (51.0, 10.0, s_sparkle, 1.0),
               (61.0, 6.0, s_business, 1.0), (67.0, 4.0, s_close, 1.0), (71.0, BUMPER_DUR, s_outro, 1.0)]
DUR = 74.0                                   # v4: the aromatic-whites half of the sparkle scene gained 2 s
N = int(DUR * FPS)
# transitions vary (the proof used one wipe everywhere; across nine cuts it would repeat): the flag-stripes
# wipe for the main beats, a fog bank into the fog scene, whips elsewhere
CUTS_STRIPES = (3.0, 7.0, 15.0, 43.0, 61.0)
CUTS_FOG = (23.0,)
CUTS_WHIP = (31.0, 37.0, 51.0, 67.0)
CUTS_DISSOLVE = (71.0,)                      # the end card dissolves into the outro bug
CUTS = CUTS_STRIPES + CUTS_FOG + CUTS_WHIP + CUTS_DISSOLVE


def T(scene, u):
    for start, dur, fn, st in SCENE_TABLE:
        if fn.__name__ == scene:
            return start + u * st
    raise KeyError(scene)


def frame_at(t):
    def scene_frame(tt):
        for start, dur, fn, st in SCENE_TABLE:
            if start <= tt < start + dur or (fn is SCENE_TABLE[-1][2] and tt >= start):
                ur = tt - start
                return fn(ur / st, ur=ur, D=dur, S=st)
    f = scene_frame(t)
    for c in CUTS_DISSOLVE:                  # a short dip to black (a dissolve ghosted the bug over the card)
        if c - 0.25 <= t < c:
            f = f * (1 - in_cubic(prog(t, c - 0.25, c)))
        elif c <= t < c + 0.3:
            f = f * out_cubic(prog(t, c, c + 0.3))
    for c in CUTS_WHIP:
        if c - 0.13 <= t < c + 0.13:
            f = whip(f, in_cubic(prog(t, c - 0.13, c)), 1 - out_cubic(prog(t, c, c + 0.13)) if t >= c else 0)
    for c in CUTS_STRIPES:
        stripes_wipe(f, prog(t, c - 0.22, c + 0.22))
    for c in CUTS_FOG:
        fog_sweep(f, prog(t, c - 0.45, c + 0.45))
    if t >= DUR - 0.1:
        f *= 1 - prog(t, DUR - 0.1, DUR)
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
