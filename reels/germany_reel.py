"""Instagram Reel: GERMANY IN 20 SECONDS. 1080x1920, 30 fps, 600 frames.

Summarizes the four Germany posts: the Mosel Field Guide, Guess the Region: Baden, What Am I
Drinking? (Dr. Loosen Erdener Treppchen Auslese 2020) and the FFFA on German reds. Every fact on
screen comes from those posts, which were sourced and reviewed there (D3 Ch. 11 plus the sources
noted in each deck). One addition: the translation of Treppchen ("little staircase", the
diminutive of Treppe, stairs).

TIMELINE (120 BPM; one bar = 2 s)
  0.0-2.0   HOOK       flag bands sweep; GERMANY drops in letter by letter; "in 20 seconds"
  2.0-5.0   MOSEL      the real Mosel draws itself (Natural Earth, public domain); camera dives
                       into a bend and dissolves to the loop photo; "SLOPES UP TO 70%" counts up
  5.0-8.0   LADDER     a five-rung ladder builds (Kabinett -> TBA): FIVE RUNGS. NONE MEANS SWEET.
                       Auslese lights up at the end, handing off to the next scene's wine
  8.0-11.0  TREPPCHEN  cream paper; the Loosen bottle slides in; Treppchen = "little staircase"
  11.0-14.0 BADEN      "Known for red..." then a ring fills to 61% WHITE; the extinct volcano
  14.0-17.5 REDS       nearly a third of German vines are red: bars, then three quick facts
  17.5-20.0 OUTRO      toast photo; PROST.; fades to black so the Reel loops into its own opening

PHOTOS: Unsplash / Pexels licensed, plus Steve's supplied bottle shot. The two CC BY-SA photos used
in the decks (Hatzenport, the Ahr) are deliberately NOT used: share-alike would extend to the video.

Usage:  python3 germany_reel.py --preview 0.9,3.0,...   (PNG contact sheet of those moments)
        python3 germany_reel.py --render OUT.mp4         (video only; audio is muxed separately)
"""
import math
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_lib import (W, H, FPS, ROOT, Photo, arc, blit_center, chip, clamp, darken, fill_poly, fill_rect,  # noqa: E402
                      finish, in_cubic, in_out_cubic, letters, load_geo_line, out_back, out_cubic,
                      out_expo, prog, round_rect, sheen, stroke_path, text, text_width, transform, vgrad)
import cv2  # noqa: E402

DUR = 20.0
N = int(DUR * FPS)
BLACK = (9, 9, 11); CHAR = (34, 34, 40); RED = (221, 0, 0); GOLD = (255, 206, 0)
PAPER = (250, 246, 238); INK = (28, 24, 26); WHITE = (255, 255, 255); DGOLD = (165, 112, 0)

_cache = {}


def photo(name, cover=1.35):
    if name not in _cache:
        _cache[name] = Photo(name, cover)
    return _cache[name]


def bg(color):
    f = np.empty((H, W, 3), np.float32)
    f[:] = color
    return f


# ----------------------------------------------------------------------------- transitions
BW = 900
K = H * math.tan(math.radians(20))


def bands(dst, p):
    """Flag bands (charcoal, red, gold) sweep left to right; fully cover the frame at p = 0.5."""
    if p <= 0 or p >= 1:
        return
    X0, X1 = -(3 * BW + K), W
    for j, col in enumerate((CHAR, RED, GOLD)):
        pj = clamp(p + (j - 1) * 0.035)
        X = X0 + (X1 - X0) * in_out_cubic(pj) + j * BW
        fill_poly(dst, [(X, H), (X + BW + 2, H), (X + BW + 2 + K, 0), (X + K, 0)], col)


def whip(frame, p_out, p_in):
    """Zoom-blur whip with a white flash: p_out ramps 0->1 before the cut, p_in 1->0 after."""
    p = max(p_out, p_in)
    if p <= 0:
        return frame
    s = 1 + 0.45 * p * p
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s)
    f = cv2.warpAffine(frame, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    k = int(2 + 40 * p)
    f = cv2.blur(f, (1, k))
    flash = 0.75 * p ** 2
    return f * (1 - flash) + 255 * flash


# ----------------------------------------------------------------------------- S0 HOOK
# Fit GERMANY inside 60px side margins (first pass at 232px ran off the right edge).
GSIZE = next(sz for sz in range(232, 120, -2) if text_width("GERMANY", "cond", sz, 8) <= W - 2 * 75)
def s0(t):
    f = bg(BLACK)
    # flag mini-bars
    q = out_back(prog(t, 0.35, 0.62))
    if q > 0:
        for j, col in enumerate(((22, 22, 26), RED, GOLD)):
            w = 170 * q
            y = 560 + j * 28
            fill_rect(f, W / 2 - w / 2, y, W / 2 + w / 2, y + 20, col)
        if q > 0.2:
            stroke_path(f, [(W / 2 - 85 * q, 560), (W / 2 + 85 * q, 560), (W / 2 + 85 * q, 580),
                            (W / 2 - 85 * q, 580), (W / 2 - 85 * q, 560)], (95, 95, 102), 2)

    def drop(i, n):
        s = 0.42 + 0.05 * i
        p = prog(t, s, s + 0.38)
        if p <= 0:
            return dict(alpha=0)
        return dict(alpha=out_cubic(prog(t, s, s + 0.14)), dy=-230 * (1 - out_back(p, 2.2)),
                    scale=1.55 - 0.55 * out_cubic(p), mblur=int(36 * (1 - p)) if p < 0.85 else 0)
    glow = (16, GOLD, 0.30 * prog(t, 0.95, 1.3)) if t > 0.95 else None
    left, tw = letters(f, "GERMANY", "cond", GSIZE, WHITE, W / 2, 905, drop, tracking=8, glow=glow)
    sheen(f, "GERMANY", "cond", GSIZE, W / 2, 905, prog(t, 1.38, 1.85), align="center", tracking=8)
    u = out_expo(prog(t, 1.0, 1.35))
    if u > 0:
        fill_rect(f, W / 2 - tw / 2 * u, 948, W / 2 + tw / 2 * u, 962, GOLD)

    def rise(i, n):
        s = 1.12 + 0.022 * i
        p = prog(t, s, s + 0.3)
        return dict(alpha=out_cubic(p), dy=26 * (1 - out_cubic(p)))
    letters(f, "in 20 seconds", "serif_it", 98, GOLD, W / 2, 1090, rise)
    bands(f, prog(t, 0.0, 0.42))                       # the opening sweep across black
    return f


# ----------------------------------------------------------------------------- S1 MOSEL
_river = [c for c in load_geo_line(f"{ROOT}/data/geo/mosel_river.geojson") if c[1] > 49.45]
_lat0 = 49.9


def _proj_setup():
    xs = [c[0] * math.cos(math.radians(_lat0)) for c in _river]
    ys = [c[1] for c in _river]
    bx0, bx1, by0, by1 = 100, 980, 620, 1380
    s = min((bx1 - bx0) / (max(xs) - min(xs)), (by1 - by0) / (max(ys) - min(ys)))
    ox = bx0 + ((bx1 - bx0) - s * (max(xs) - min(xs))) / 2
    oy = by0 + ((by1 - by0) - s * (max(ys) - min(ys))) / 2
    return lambda lon, lat: (ox + s * (lon * math.cos(math.radians(_lat0)) - min(xs)),
                             oy + s * (max(ys) - lat))


PROJ = _proj_setup()
RIVER_PTS = [PROJ(*c) for c in _river]
TOWNS = [("Trier", 6.6371, 49.7499), ("Bernkastel", 7.0711, 49.9161), ("Koblenz", 7.5890, 50.3569)]
BREMM = PROJ(7.1089, 50.1022)


def _nearest_idx(pt):
    d = [(p[0] - pt[0]) ** 2 + (p[1] - pt[1]) ** 2 for p in RIVER_PTS]
    return int(np.argmin(d))


TOWN_IDX = [(_nearest_idx(PROJ(lo, la)), nm, PROJ(lo, la)) for nm, lo, la in TOWNS]


_rhine = []
for _ft in __import__("json").load(open(f"{ROOT}/data/geo/de_rivers.geojson"))["features"]:
    if _ft["properties"].get("name_en") in ("Rhein", "Rhine"):
        for _part in _ft["geometry"]["coordinates"]:
            _seg = [c for c in _part if 6.0 < c[0] < 8.6 and 49.2 < c[1] < 50.8]
            if len(_seg) > 1:
                _rhine.append(_seg)


def mosel_map(u):
    f = bg((10, 12, 18))
    ra = 0.5 * prog(u, 0.0, 0.35)
    for seg in _rhine:                                        # context: the Rhine, which the Mosel joins at Koblenz
        stroke_path(f, [PROJ(*c) for c in seg], (90, 120, 160), 6, alpha=ra)
    if ra > 0:
        rx, ry = PROJ(7.62, 50.47)
        text(f, "RHEIN", "bold", 30, (120, 150, 190), rx - 12, ry - 6, align="right", tracking=4, alpha=ra * 1.4)
    for lat in (49.5, 49.75, 50.0, 50.25):
        y = PROJ(7.0, lat)[1]
        a = 0.28 if lat == 50.0 else 0.08
        fill_rect(f, 0, y - 1, W, y + 1, (120, 140, 170), a * prog(u, 0.0, 0.3))
    if u > 0.45:
        y50 = PROJ(7.0, 50.0)[1]
        text(f, "50°N", "bold", 34, (150, 170, 200), 60, y50 - 14, alpha=out_cubic(prog(u, 0.45, 0.7)))
    fr = in_out_cubic(prog(u, 0.05, 1.05))
    n = len(RIVER_PTS)
    k = fr * (n - 1)
    i = int(k)
    pts = RIVER_PTS[:i + 1]
    if i < n - 1:
        a, b = RIVER_PTS[i], RIVER_PTS[i + 1]
        pts = pts + [(a[0] + (b[0] - a[0]) * (k - i), a[1] + (b[1] - a[1]) * (k - i))]
    stroke_path(f, pts, GOLD, 9, glow=11)
    hx, hy = pts[-1]
    if fr < 1:
        fill_poly(f, [(hx + 13 * math.cos(a), hy + 13 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24)], WHITE)
    for idx, nm, (tx, ty) in TOWN_IDX:
        if k >= idx:
            q = out_back(prog(u, 0.05 + 1.0 * idx / (n - 1), 0.25 + 1.0 * idx / (n - 1)))
            fill_poly(f, [(tx + 8 * q * math.cos(a), ty + 8 * q * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 18)], WHITE)
            right = nm != "Koblenz"
            text(f, nm, "bold", 38, WHITE, tx + (20 if right else -20), ty + 13, align="left" if right else "right",
                 alpha=0.85 * out_cubic(prog(u, 0.1 + 1.0 * idx / (n - 1), 0.3 + 1.0 * idx / (n - 1))))
    return f


def s1(u):
    f = mosel_map(u) if u < 1.6 else None
    if u >= 1.15 and f is not None:
        z = 1 + 4.0 * in_cubic(prog(u, 1.15, 1.6))
        M = np.float32([[z, 0, W / 2 - z * BREMM[0]], [0, z, H * 0.55 - z * BREMM[1]]])
        tt = in_cubic(prog(u, 1.15, 1.6))
        M[0, 2] = (1 - tt) * 0 + tt * M[0, 2]
        M[1, 2] = (1 - tt) * 0 + tt * M[1, 2]
        M[0, 0] = M[1, 1] = z
        f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    if u >= 1.35:
        ph = photo("de_bremm_mosel_loop.jpg")
        g = ph.view(zoom=1.22 - 0.10 * out_cubic(prog(u, 1.35, 3.0)), fx=0.5, fy=0.55)
        darken(g, np.float32(0.30))
        darken(g, vgrad(700, 1500, 0.0, 0.55))
        darken(g, vgrad(0, 560, 0.55, 0.0))
        x = out_cubic(prog(u, 1.35, 1.65))
        f = g if f is None else f * (1 - x) + g * x
    # the post's label persists across both halves
    chip(f, "FIELD GUIDE: THE MOSEL", W / 2, 300, out_back(prog(u, 0.1, 0.4), 1.6))
    if u >= 1.55:
        p = out_cubic(prog(u, 1.6, 1.85))
        text(f, "SLOPES UP TO", "black", 66, WHITE, W / 2, 820, align="center", tracking=4, alpha=p, dy=30 * (1 - p))
        v = int(round(70 * out_cubic(prog(u, 1.65, 2.3))))
        pop = 1 + 0.09 * math.sin(math.pi * prog(u, 2.3, 2.48))
        text(f, f"{v}%", "cond", 330, GOLD, W / 2, 1150, align="center", alpha=prog(u, 1.63, 1.75),
             scale=pop, glow=(22, GOLD, 0.35))
        sheen(f, "70%", "cond", 330, W / 2, 1150, prog(u, 2.45, 2.9), align="center", strength=0.6)
        p2 = out_cubic(prog(u, 2.35, 2.6))
        text(f, "Riesling on slate,", "med", 50, WHITE, W / 2, 1262, align="center", alpha=p2, dy=24 * (1 - p2))
        p3 = out_cubic(prog(u, 2.45, 2.7))
        text(f, "above a looping river.", "med", 50, WHITE, W / 2, 1326, align="center", alpha=p3, dy=24 * (1 - p3))
    return f


# ----------------------------------------------------------------------------- S2 LADDER
def _slate():
    rng = np.random.default_rng(5)
    n = cv2.resize(rng.normal(0, 1, (H // 24, W // 6)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    n = cv2.GaussianBlur(n, (0, 0), 2)
    strata = 0.5 + 0.5 * np.sin(np.arange(H, dtype=np.float32)[:, None] / 7.0 + n * 2.2)
    base = np.array((22, 24, 30), np.float32)
    s = base + (strata[..., None] * 9 + n[..., None] * 4) * np.array((0.9, 0.95, 1.1), np.float32)
    s *= (1 - 0.35 * vgrad(0, H, 0.0, 1.0))
    return s


SLATE = _slate()
RUNGS = ["Kabinett", "Spätlese", "Auslese", "Beerenauslese", "TBA"]


def s2(u):
    f = SLATE.copy()
    chip(f, "FIELD GUIDE: THE MOSEL", W / 2, 250, 1.0 if u > 0.05 else 0.0)
    rail = out_cubic(prog(u, 0.0, 0.32))
    yb, yt = 1545, 845            # lowered: the explainer lines crowded the top rung
    for x in (200, 330):
        if rail > 0:
            fill_rect(f, x - 7, yb - (yb - yt) * rail, x + 7, yb, GOLD)
    for k, name in enumerate(RUNGS):
        s = 0.18 + 0.14 * k
        p = prog(u, s, s + 0.3)
        if p <= 0:
            continue
        y = 1470 - k * 148
        w = 130 * out_back(p)
        fill_rect(f, 265 - w / 2 - 8, y - 9, 265 + w / 2 + 8, y + 9, GOLD)
        hot = name == "Auslese" and u > 2.15
        col = GOLD if hot else WHITE
        pulse = 1 + (0.07 * math.sin(math.pi * prog(u, 2.15, 2.45)) if hot else 0)
        text(f, name, "cond", 78, col, 395, y + 28, alpha=out_cubic(p), dx=120 * (1 - out_expo(p)), scale=pulse)
        text(f, str(k + 1), "bold", 30, (150, 150, 160), 120, y + 11, alpha=0.8 * out_cubic(p))

    def slam(start):
        def a(i, n):
            s = start + 0.028 * i
            p = prog(u, s, s + 0.26)
            if p <= 0:
                return dict(alpha=0)
            return dict(alpha=out_cubic(prog(u, s, s + 0.1)), scale=1.7 - 0.7 * out_expo(p),
                        blur=4 * (1 - p))
        return a
    letters(f, "FIVE RUNGS.", "cond", 132, WHITE, W / 2, 400, slam(1.0))
    l2, tw2 = letters(f, "NONE MEANS SWEET.", "cond", 104, GOLD, W / 2, 520, slam(1.32))
    ul = out_expo(prog(u, 1.75, 2.05))
    if ul > 0:
        fill_rect(f, l2, 548, l2 + tw2 * ul, 560, RED)
    p = out_cubic(prog(u, 2.0, 2.3))
    text(f, "Ripeness at harvest,", "med", 46, (235, 235, 238), W / 2, 628, align="center", alpha=p, dy=20 * (1 - p))
    p = out_cubic(prog(u, 2.1, 2.4))
    text(f, "not sugar in the bottle.", "med", 46, (235, 235, 238), W / 2, 686, align="center", alpha=p, dy=20 * (1 - p))
    return f


# ----------------------------------------------------------------------------- S3 TREPPCHEN
def _paper():
    # plain paper with a soft radial falloff; the first pass's diagonal stair pattern read as a stray
    # ribbon behind the bottle and is replaced by a deliberate stone-steps illustration (in s3)
    f = bg(PAPER)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W * 0.62) / W) ** 2 + ((yy - H * 0.45) / H) ** 2)
    f *= (1 - 0.10 * np.clip(r, 0, 1))[..., None]
    return f


PAPER_BG = _paper()


def _bottle():
    im = cv2.cvtColor(cv2.imread(f"{ROOT}/photos/wad_loosen_treppchen_bottle2.jpg"), cv2.COLOR_BGR2RGB).astype(np.float32)
    s = 1160 / im.shape[0]
    im = cv2.resize(im, (int(im.shape[1] * s), 1160), interpolation=cv2.INTER_CUBIC)
    return np.clip(im / 255.0, 0, 1)


BOTTLE = _bottle()


def s3(u):
    f = PAPER_BG.copy()        # static: a rolling drift would leave a seam in the stair pattern
    # shadow, then the bottle multiplied in (its white backdrop disappears into the paper)
    p = out_expo(prog(u, 0.0, 0.55))
    cx = 800 + 520 * (1 - p)
    rot = 9 * (1 - out_back(prog(u, 0.0, 0.7), 1.4))
    sh = np.zeros((H, W), np.float32)
    cv2.ellipse(sh, (int(cx), 1512), (150, 22), 0, 0, 360, 1.0, -1, lineType=cv2.LINE_AA)
    sh = cv2.GaussianBlur(sh, (0, 0), 14)[..., None] * 0.22 * p
    f = f * (1 - sh)
    bh, bw = BOTTLE.shape[:2]
    M = cv2.getRotationMatrix2D((bw / 2, bh), rot, 1.0)
    M[0, 2] += cx - bw / 2
    M[1, 2] += 1500 - bh
    mult = cv2.warpAffine(BOTTLE, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                          borderValue=(1.0, 1.0, 1.0))
    f *= mult
    chip(f, "WHAT AM I DRINKING?", 72, 405, out_back(prog(u, 0.12, 0.42), 1.6), align="left")
    # stone steps: built one by one as the copy says "they built stone steps"
    for k in range(6):
        p = out_back(prog(u, 1.35 + 0.08 * k, 1.6 + 0.08 * k), 1.4)
        if p <= 0:
            continue
        x0 = 72 + k * 78
        top = 1520 - (k + 1) * 46
        hgt = (1520 - top) * p
        fill_rect(f, x0, 1520 - hgt, x0 + 80, 1520, (222, 208, 180))
        fill_rect(f, x0, 1520 - hgt, x0 + 80, 1520 - hgt + 7, (190, 168, 124))
        fill_rect(f, x0 + 78, 1520 - hgt, x0 + 80, 1520, (205, 188, 155))
    for j, (w_, y) in enumerate((("Erdener", 562), ("Treppchen", 680))):
        p = out_cubic(prog(u, 0.3 + 0.12 * j, 0.62 + 0.12 * j))
        text(f, w_, "serif", 102, INK, 68, y, alpha=p, dy=40 * (1 - p))
    p = out_cubic(prog(u, 0.85, 1.15))
    text(f, "= \u2018little staircase\u2019", "serif_it", 56, DGOLD, 72, 772, alpha=p, dx=-30 * (1 - p))
    for j, (w_, y) in enumerate((("So steep, they built", 900), ("stone steps.", 960))):
        p = out_cubic(prog(u, 1.35 + 0.1 * j, 1.65 + 0.1 * j))
        text(f, w_, "med", 46, INK, 72, y, alpha=p, dy=22 * (1 - p))
    # chips measured, not guessed (the first pass's estimate left them nearly touching)
    x0 = 72
    for j, (label, fillc, txtc) in enumerate((("SWEET", GOLD, INK), ("7.5\u20138% ALC.", RED, WHITE))):
        p = prog(u, 1.9 + 0.15 * j, 2.2 + 0.15 * j)
        chip(f, label, x0, 1062, out_back(p, 2.0) if p > 0 else 0, fill=fillc, ink=txtc, size=36, align="left")
        x0 += text_width(label, "black", 36, 2) + 56 + 22
    p = out_cubic(prog(u, 2.25, 2.55))
    text(f, "Dr. Loosen \u00b7 Riesling Auslese 2020", "med", 34, (90, 80, 76), 72, 1170, alpha=p)
    return f


# ----------------------------------------------------------------------------- S4 BADEN
def s4(u):
    ph = photo("de_baden_kaiserstuhl_terraces.jpg")
    f = ph.view(zoom=1.16 - 0.08 * prog(u, 0, 3), fx=0.40 + 0.2 * prog(u, 0, 3), fy=0.5)
    darken(f, np.float32(0.42))
    darken(f, vgrad(0, 600, 0.45, 0.0))
    darken(f, vgrad(1100, 1700, 0.0, 0.55))
    chip(f, "GUESS THE REGION: BADEN", W / 2, 300, out_back(prog(u, 0.08, 0.38), 1.6))
    p = out_cubic(prog(u, 0.3, 0.6))
    text(f, "Known for red\u2026", "serif_it", 86, WHITE, W / 2, 480, align="center", alpha=p, dy=30 * (1 - p))
    cx, cy, r = W / 2, 850, 225
    tp = out_cubic(prog(u, 0.6, 0.85))
    if tp > 0:
        arc(f, cx, cy, r, 44, 0, 360, WHITE, 0.18 * tp)
    a = out_cubic(prog(u, 0.75, 1.55))
    if a > 0:
        arc(f, cx, cy, r, 44, 0, 360 * 0.61 * a, GOLD)
        text(f, f"{int(round(61 * a))}%", "cond", 168, WHITE, cx, cy + 58, align="center",
             alpha=prog(u, 0.75, 0.85), scale=1 + 0.08 * math.sin(math.pi * prog(u, 1.55, 1.72)))
    p = out_cubic(prog(u, 1.45, 1.7))
    text(f, "OF ITS VINES ARE", "black", 50, WHITE, W / 2, 1170, align="center", tracking=3, alpha=p, dy=24 * (1 - p))

    def slam(i, n):
        s = 1.6 + 0.03 * i
        pp = prog(u, s, s + 0.25)
        if pp <= 0:
            return dict(alpha=0)
        return dict(alpha=out_cubic(prog(u, s, s + 0.08)), scale=1.8 - 0.8 * out_expo(pp))
    letters(f, "WHITE", "cond", 132, GOLD, W / 2, 1305, slam, glow=(18, GOLD, 0.3))
    for j, (w_, y) in enumerate((("Plus an extinct volcano:", 1404), ("the Kaiserstuhl.", 1462))):
        p = out_cubic(prog(u, 2.05 + 0.1 * j, 2.35 + 0.1 * j))
        text(f, w_, "med", 46, WHITE, W / 2, y, align="center", alpha=p, dy=22 * (1 - p))
    return f


# ----------------------------------------------------------------------------- S5 REDS
def s5(u):
    ph = photo("de_baden_red_grapes.jpg")
    f = ph.view(zoom=1.1 + 0.1 * prog(u, 0, 3.5), fx=0.5, fy=0.5)
    darken(f, np.float32(0.6))
    darken(f, vgrad(0, H, 0.0, 0.25), (60, 0, 10))

    def slam(start, sz):
        def a(i, n):
            s = start + 0.025 * i
            p = prog(u, s, s + 0.24)
            if p <= 0:
                return dict(alpha=0)
            return dict(alpha=out_cubic(prog(u, s, s + 0.08)), scale=sz - (sz - 1) * out_expo(p), mblur=0)
        return a
    chip(f, "FIVE FASCINATING FACTS", W / 2, 260, out_back(prog(u, 0.02, 0.3), 1.6))
    letters(f, "NEARLY A THIRD", "cond", 132, GOLD, W / 2, 425, slam(0.1, 1.7), glow=(16, GOLD, 0.25))
    p = out_cubic(prog(u, 0.36, 0.64))
    text(f, "OF GERMAN VINES ARE RED", "cond", 70, WHITE, W / 2, 515, align="center", tracking=2, alpha=p, dy=24 * (1 - p))
    for j, (yr, val, shown, col) in enumerate((("1980", 10, "about 10%", (175, 175, 182)), ("2021", 32, "32%", RED))):
        y = 640 + j * 118
        p = out_expo(prog(u, 0.55 + 0.12 * j, 1.15 + 0.12 * j))
        a = out_cubic(prog(u, 0.5 + 0.12 * j, 0.7 + 0.12 * j))
        text(f, yr, "black", 46, WHITE, 100, y + 46, alpha=a)
        wmax = 600 * val / 32
        if p > 0:
            fill_rect(f, 250, y, 250 + wmax * p, y + 64, col)
            text(f, shown if p > 0.95 else f"{int(round(val * p))}%", "black", 44, WHITE, 250 + wmax * p + 18, y + 47, alpha=a)
    rows = [("\u22483\u00d7", "Pinot Noir: almost tripled"), ("#2", "Dornfelder: 0 to No. 2 red"),
            ("4/5", "Ahr: 4 in 5 vines are red")]
    for j, (icon, desc) in enumerate(rows):
        s = 1.3 + 0.45 * j
        p = prog(u, s, s + 0.35)
        if p <= 0:
            continue
        y = 1015 + j * 140
        text(f, icon, "cond", 96, GOLD, 100, y + 34, alpha=out_cubic(p), scale=out_back(p, 2.2))
        text(f, desc, "bold", 44, WHITE, 300, y + 18, alpha=out_cubic(p), dx=90 * (1 - out_expo(p)))
        fill_rect(f, 300, y + 40, 300 + 640 * out_expo(prog(u, s + 0.1, s + 0.5)), y + 43, (255, 255, 255), 0.25)
    return f


# ----------------------------------------------------------------------------- S6 OUTRO
def s6(u):
    ph = photo("de_reds_toast_pexels_rdne.jpg")
    f = ph.view(zoom=1.05 + 0.08 * prog(u, 0, 2.5), fx=0.52, fy=0.45)
    f *= np.array((1.04, 0.99, 0.92), np.float32)
    darken(f, np.float32(0.45))
    darken(f, vgrad(500, 1400, 0.15, 0.5))

    def rise(i, n):
        s = 0.12 + 0.06 * i
        p = prog(u, s, s + 0.4)
        if p <= 0:
            return dict(alpha=0)
        return dict(alpha=out_cubic(p), dy=90 * (1 - out_expo(p)), blur=6 * (1 - p))
    letters(f, "PROST.", "serif", 250, GOLD, W / 2, 900, rise, glow=(22, GOLD, 0.35 * prog(u, 0.5, 0.9)))
    sheen(f, "PROST.", "serif", 250, W / 2, 900, prog(u, 1.25, 1.75), align="center", strength=0.75)
    q = out_back(prog(u, 0.6, 0.85))
    if q > 0:
        for j, col in enumerate(((20, 20, 24), RED, GOLD)):
            fill_rect(f, W / 2 - 90 * q, 960 + j * 22, W / 2 + 90 * q, 960 + j * 22 + 20, col)
    p = out_cubic(prog(u, 0.85, 1.15))
    text(f, "Germany, in four posts.", "med", 54, WHITE, W / 2, 1140, align="center", alpha=p, dy=26 * (1 - p))
    c = prog(u, 1.15, 1.45)
    if c > 0:
        sc = out_back(c, 2.0)
        tw = 560
        round_rect(f, W / 2 - tw / 2 * sc, 1240 - 40 * sc, W / 2 + tw / 2 * sc, 1240 + 40 * sc, 40, GOLD)
        text(f, "Full stories on our grid", "black", 38, INK, W / 2, 1254, align="center", alpha=out_cubic(c), scale=sc)
    return f


# ----------------------------------------------------------------------------- timeline
SCENES = [(0.0, 2.0, s0), (2.0, 5.0, s1), (5.0, 8.0, s2), (8.0, 11.0, s3), (11.0, 14.0, s4),
          (14.0, 17.5, s5), (17.5, 20.0, s6)]
CUTS_BANDS = (2.0, 11.0, 17.5)
CUTS_WHIP = (5.0, 14.0)
CUT_PAPER = 8.0


def frame_at(t):
    for a, b, fn in SCENES:
        if a <= t < b or (fn is s6 and t >= a):
            f = fn(t - a)
            break
    for c in CUTS_WHIP:
        if c - 0.13 <= t < c + 0.13:
            f = whip(f, in_cubic(prog(t, c - 0.13, c)), 1 - out_cubic(prog(t, c, c + 0.13)) if t >= c else 0)
    for c in CUTS_BANDS:
        bands(f, prog(t, c - 0.2, c + 0.2))
    if CUT_PAPER - 0.22 <= t < CUT_PAPER:
        p = out_cubic(prog(t, CUT_PAPER - 0.22, CUT_PAPER))
        y = H * (1 - p)
        fill_rect(f, 0, y - 30, W, y, (0, 0, 0), 0.25)
        fill_rect(f, 0, y, W, H, PAPER)
    if t >= DUR - 0.3:
        f *= 1 - prog(t, DUR - 0.3, DUR)
    return f


def render(out, start=0, end=None):
    """Render frames [start, end) to `out`. The sandbox ends background processes when the call
    that started them returns, so a full render is done as chunks joined losslessly afterwards
    (every chunk starts on a keyframe; same encoder settings throughout)."""
    end = N if end is None else end
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(start, end):
        t = fi / FPS
        pr.stdin.write(finish(frame_at(t), fi).tobytes())
        if fi % 30 == 0:
            print(f"frame {fi}/{N}", flush=True)
    pr.stdin.close()
    pr.wait()
    print("video done:", out)


def preview(times, out):
    from PIL import Image
    tiles = []
    for t in times:
        fi = int(round(t * FPS))
        im = Image.fromarray(finish(frame_at(min(t, DUR - 1 / FPS)), fi)).resize((270, 480))
        tiles.append(im)
    cols = min(6, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 276, rows * 500), (60, 60, 60))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for i, (im, t) in enumerate(zip(tiles, times)):
        x, y = (i % cols) * 276, (i // cols) * 500
        sheet.paste(im, (x, y))
        d.text((x + 4, y + 482), f"{t:.2f}s", fill=(255, 255, 255))
    sheet.save(out)
    print("preview:", out, sheet.size)


if __name__ == "__main__":
    if "--preview" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1].split(",")]
        preview(ts, sys.argv[sys.argv.index("--preview") + 2] if len(sys.argv) > sys.argv.index("--preview") + 2 else "/home/claude/reel_preview.png")
    elif "--render" in sys.argv:
        i = sys.argv.index("--render")
        rng_ = sys.argv[i + 2:i + 4]
        render(sys.argv[i + 1], *(int(x) for x in rng_)) if len(rng_) == 2 else render(sys.argv[i + 1])
