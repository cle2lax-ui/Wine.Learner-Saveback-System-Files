"""THE FIELD GUIDE -- opening bumper (ident) for every Field Guide Reel. 3.0 s, 1080x1920.

Steve: "a standard The Field Guide opening animation that can start all TFG Reels in the future ... a wine
glass and a book ... an opening bumper that our viewers will come to recognize." v2 (Steve): the wine glass
is WHITE line art with BURGUNDY wine; the stack of books is gone -- ONE white line-art book opens next to
the glass.

RECOGNITION COMES FROM SAMENESS, so the bumper looks and sounds identical at the start of every Field Guide
Reel, whatever the country: white line art, burgundy wine, cream and gold type on a warm dark ground. The arc
appears in exactly one detail: the color of the book's ribbon bookmark (accent=).

STORYBOARD
  0.05-0.4   the closed book draws itself (cover and spine, white line)
  0.35-0.95  the book swings open, both pages spreading from the spine; the ribbon drops
  0.85-1.25  one page lifts and turns over, right to left
  0.95-1.6   lines of text write themselves onto the pages
  0.7-1.3    the glass draws itself beside the book: foot, stem, both sides of the bowl, then the rim
  1.15-1.8   burgundy wine fills the bowl; its surface settles in a damped wave
  1.45-2.3   glint, warm glow, rising motes; THE / FIELD GUIDE reveals; a gold rule sweeps under it
  2.2-3.0    hold; the Reel's own transition covers the cut at 3.0
SONIC LOGO (bumper_audio): a paper swish; a cover "thup" as the book lands open; a page flutter; a glass
"ting" as the rim closes; a soft pour; bells A-E-A on the wordmark over a warm swell. Fixed pitches.

USAGE: frame = bumper(t, accent=theme_chip_color) for 0 <= t < BUMPER_DUR; audio = bumper_audio().
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_lib import (W, H, chip, clamp, fill_poly, fill_rect, in_cubic, in_out_cubic, letters, out_back, out_cubic,  # noqa: E402
                      out_expo, prog, round_rect, stroke_path, text, text_width)

BUMPER_DUR = 3.0
GROUND = (16, 12, 14)
BURGUNDY, FOREST, CREAM, GOLD = (104, 26, 38), (21, 63, 40), (236, 226, 204), (206, 168, 92)
LINE = (246, 242, 234)                       # the white line art
# burgundy WINE: darker and toward purple (the first v2 render read as raspberry: too light a base, and a
# pink surface band lifting it further)
WINE = (86, 14, 40)
WINE_DEEP = (36, 4, 16)
WINE_SURF = (122, 34, 60)
LW = 6                                       # line weight

# ---- layout: book on the left, glass on the right, both standing on one baseline
BASE = 1090
BX = 352                                     # the book's spine
GX = 790                                     # the glass's axis
PW, PH = 196, 286                            # one page's width and height when fully open
SC = 1.15
STEM_TOP = 175 * SC
PROFILE = [(STEM_TOP, 14), (STEM_TOP + 18 * SC, 60 * SC), (STEM_TOP + 60 * SC, 112 * SC), (STEM_TOP + 130 * SC, 132 * SC),
           (STEM_TOP + 200 * SC, 126 * SC), (STEM_TOP + 260 * SC, 108 * SC), (STEM_TOP + 300 * SC, 92 * SC)]
RIM = STEM_TOP + 300 * SC
GLASS_FOOT = BASE
from scipy.interpolate import PchipInterpolator     # noqa: E402
_PCHIP = PchipInterpolator([h for h, _ in PROFILE], [w for _, w in PROFILE])   # a smooth bowl, no corners


def _halfwidth(hh):
    if hh < PROFILE[0][0] or hh > PROFILE[-1][0]:
        return 0.0
    return float(_PCHIP(hh))


def _bez(p0, p1, p2, n=24):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2 = np.array(p0), np.array(p1), np.array(p2)
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2


def _partial(path, frac):
    pts = np.array(path, np.float64)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    L = frac * d[-1]
    k = int(np.searchsorted(d, L))
    if k <= 0:
        return pts[:1]
    if k >= len(pts):
        return pts
    a, b = pts[k - 1], pts[k]
    t = (L - d[k - 1]) / max(d[k] - d[k - 1], 1e-9)
    return np.vstack([pts[:k], a + (b - a) * t])


# ----------------------------------------------------------------------------- the book
def _page(side, w, lift=0.0):
    """One page's outline (a closed loop) at spread w in [0, 1]; side -1 = left, +1 = right."""
    xo = BX + side * PW * w
    top_o, top_s = (xo, BASE - PH - 12 * w), (BX, BASE - PH + 16)
    bot_o, bot_s = (xo, BASE - 10 * w), (BX, BASE + 4)
    top = _bez(top_s, (BX + side * PW * w * 0.45, BASE - PH - 26 * w - lift), top_o)
    bot = _bez(bot_o, (BX + side * PW * w * 0.5, BASE - 2), bot_s)
    return np.vstack([top, [top_o, bot_o], bot, [bot_s, top_s]])


def _cover(w):
    cw = (PW + 18) * w
    return np.array([(BX - cw, BASE - PH + 4), (BX - cw, BASE + 6), (BX, BASE + 18), (BX + cw, BASE + 6), (BX + cw, BASE - PH + 4)])


def _turning_page(phi):
    """A page lifting off the right side and turning over the spine to the left, phi in [0, 1]."""
    ang = math.pi * phi
    xo = BX + PW * math.cos(ang)
    lift = 70 * math.sin(ang)
    top_o, bot_o = (xo, BASE - PH - 12 - lift), (xo, BASE - 10 - lift * 0.6)
    top = _bez((BX, BASE - PH + 16), ((BX + xo) / 2, BASE - PH - 30 - lift * 1.2), top_o, 20)
    bot = _bez(bot_o, ((BX + xo) / 2, BASE - 10 - lift * 0.8), (BX, BASE + 4), 20)
    return np.vstack([top, [top_o, bot_o], bot])


def _book(f, P, accent):
    """The book, from state P: draw (outline progress), w (spread), ribbon, turn (page-turn phase or 0),
    line(side, k) -> how much of each text line is written."""
    draw = P["draw"]
    if draw <= 0:
        return
    w = P["w"]
    stroke_path(f, _partial(_cover(w), draw), LINE, LW)
    for side in (-1, 1):
        pg = _page(side, w)
        fill_poly(f, pg, (255, 255, 255), 0.04 * P["page_fill"])
        stroke_path(f, _partial(pg, draw), LINE, LW)
    rq = P["ribbon"]
    if rq > 0:
        L = 92 * rq
        fill_poly(f, [(BX + 10, BASE - 4), (BX + 24, BASE - 4), (BX + 24, BASE + L), (BX + 17, BASE + L - 9), (BX + 10, BASE + L)], accent)
    tp = P["turn"]
    if 0 < tp < 1:
        stroke_path(f, _turning_page(tp), LINE, LW - 1, alpha=0.95)
    for side in (-1, 1):
        for k in range(5):
            q = P["line"](side, k)
            if q <= 0.04:                                      # a near-zero stroke draws as a stray dot
                continue
            y = BASE - PH + 70 + k * 42
            xa, xb = BX + side * 30, BX + side * (PW * w - 34) * (0.62 if k == 4 else 1.0)
            if abs(xb - xa) < 8:
                continue
            stroke_path(f, [(xa, y + 6), (xa + (xb - xa) * q, y)], LINE, 4, alpha=0.75)


# ----------------------------------------------------------------------------- the glass
def _glass_paths():
    foot = GLASS_FOOT
    left = [(GX - 4, foot)] + [(GX - 8, foot - h) for h in np.linspace(0, STEM_TOP, 8)]
    right = [(GX + 4, foot)] + [(GX + 8, foot - h) for h in np.linspace(0, STEM_TOP, 8)]
    hs = np.linspace(STEM_TOP, RIM, 90)
    left += [(GX - _halfwidth(h), foot - h) for h in hs]
    right += [(GX + _halfwidth(h), foot - h) for h in hs]
    return left, right


_MOTES = [((BX + GX) / 2 + (np.random.default_rng(i).random() - 0.5) * 820, 380 + np.random.default_rng(i + 50).random() * 700,
           0.4 + np.random.default_rng(i + 99).random() * 0.6) for i in range(16)]


def _intro_state(t):
    """The intro's timeline, as a state for _frame()."""
    def line(side, k):
        s_ = 0.95 + 0.06 * k + (0.18 if side > 0 else 0.0)
        return out_cubic(prog(t, s_, s_ + 0.3))
    return dict(draw=out_cubic(prog(t, 0.05, 0.4)), w=0.06 + 0.94 * out_back(prog(t, 0.35, 0.95), 1.3),
                page_fill=prog(t, 0.5, 0.9), ribbon=out_back(prog(t, 0.8, 1.1), 1.6), turn=in_out_cubic(prog(t, 0.85, 1.25)),
                line=line, foot=out_cubic(prog(t, 0.7, 0.88)), glass=in_out_cubic(prog(t, 0.8, 1.3)),
                rim=out_cubic(prog(t, 1.28, 1.4)), refl=0.35 * out_cubic(prog(t, 1.3, 1.6)),
                wine=out_cubic(prog(t, 1.15, 1.8)), wave=9 * math.exp(-max(t - 1.15, 0) * 3.2), glint=prog(t, 1.45, 2.0),
                chip=out_back(prog(t, 1.5, 1.85), 1.7), glow=out_cubic(prog(t, 1.2, 2.0)), motes=prog(t, 1.35, 1.85),
                mote_t=t, zoom=1 + 0.035 * in_out_cubic(prog(t, 0, BUMPER_DUR)), fade=0.0, t=t)


def _outro_state(t):
    """The outro (Steve: close with the same bug, the wine glass empty and the book swung closed). It starts
    exactly where the intro ends: the wine drains, the lines erase, the book swings closed, the glow fades."""
    def line(side, k):
        s_ = 0.85 + 0.05 * (4 - k) + (0.0 if side > 0 else 0.12)          # erase in reverse order
        return 1 - out_cubic(prog(t, s_, s_ + 0.25))
    drain = in_out_cubic(prog(t, 0.3, 1.25))
    close = in_out_cubic(prog(t, 1.25, 1.85))
    return dict(draw=1.0, w=0.06 + 0.94 * (1 - close), page_fill=1 - close, ribbon=1 - out_cubic(prog(t, 1.05, 1.3)),
                turn=0.0, line=line, foot=1.0, glass=1.0, rim=1.0, refl=0.35, wine=1 - drain,
                wave=6 * math.sin(math.pi * prog(t, 0.3, 1.25)) * (1 if drain < 1 else 0), glint=0.0,
                chip=1.0, glow=1 - out_cubic(prog(t, 1.9, 2.6)), motes=1 - prog(t, 1.6, 2.3), mote_t=BUMPER_DUR + t,
                zoom=1 + 0.035 * (1 - in_out_cubic(prog(t, 0, BUMPER_DUR))), fade=in_cubic(prog(t, 2.45, 3.0)), t=t)


def _frame(P, accent):
    import cv2
    t = P["t"]
    f = np.empty((H, W, 3), np.float32)
    f[:] = GROUND
    if P["glow"] > 0:                                         # warm glow behind the pair
        yy, xx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
        r = np.sqrt((xx - (BX + GX) / 2) ** 2 + (yy - (BASE - 280)) ** 2)
        glow = np.clip(1 - r / 700, 0, 1) ** 2 * 0.15 * P["glow"]
        glow = np.kron(glow, np.ones((4, 4), np.float32))[:H, :W, None]
        f[:] = f * (1 - glow) + np.array(GOLD, np.float32) * glow
    _book(f, P, accent)
    if P["foot"] > 0:
        fw = 96 * SC * P["foot"]
        stroke_path(f, [(GX - fw, GLASS_FOOT), (GX + fw, GLASS_FOOT)], LINE, LW + 1)
    dp = P["glass"]
    left, right = _glass_paths()
    if P["wine"] > 0.01:                                      # burgundy wine
        level = STEM_TOP + 22 + (150 * SC - 22) * P["wine"]
        xs = np.linspace(-1, 1, 40)
        hw = _halfwidth(level) - 6
        surf = [(GX + x * hw, GLASS_FOOT - level + P["wave"] * math.sin(6 * x + t * 14)) for x in xs]
        body = [(GX + _halfwidth(h) - 6, GLASS_FOOT - h) for h in np.linspace(level, STEM_TOP + 22, 20)]
        body += [(GX - _halfwidth(h) + 6, GLASS_FOOT - h) for h in np.linspace(STEM_TOP + 22, level, 20)]
        fill_poly(f, surf[::-1] + body[:1] + body + surf[:1], WINE)
        span = level - STEM_TOP - 22
        for k in range(1, 9):
            top_h = STEM_TOP + 22 + span * (0.62 * k / 8)
            lay = [(GX + _halfwidth(h) - 6, GLASS_FOOT - h) for h in np.linspace(top_h, STEM_TOP + 22, 14)]
            lay += [(GX - _halfwidth(h) + 6, GLASS_FOOT - h) for h in np.linspace(STEM_TOP + 22, top_h, 14)]
            fill_poly(f, lay, WINE_DEEP, 0.085)
        band = [(x, y + 16) for x, y in surf]
        fill_poly(f, surf + band[::-1], WINE_SURF, 0.18)
        stroke_path(f, surf, WINE_SURF, 3, alpha=0.9)
    if dp >= 1:
        bowl = [(GX - _halfwidth(h), GLASS_FOOT - h) for h in np.linspace(STEM_TOP, RIM, 30)]
        bowl += [(GX + _halfwidth(h), GLASS_FOOT - h) for h in np.linspace(RIM, STEM_TOP, 30)]
        fill_poly(f, bowl, (255, 255, 255), 0.05)
    if dp > 0:
        stroke_path(f, _partial(left, dp), LINE, LW + 1)
        stroke_path(f, _partial(right, dp), LINE, LW + 1)
    if dp >= 1:
        refl = [(GX + _halfwidth(h) - 26, GLASS_FOOT - h) for h in np.linspace(STEM_TOP + 70 * SC, RIM - 50 * SC, 24)]
        stroke_path(f, refl, (255, 255, 255), 5, alpha=P["refl"])
        rq = P["rim"]
        stroke_path(f, [(GX - _halfwidth(RIM) * rq, GLASS_FOOT - RIM), (GX + _halfwidth(RIM) * rq, GLASS_FOOT - RIM)], LINE, LW + 1)
    sp = P["glint"]
    if 0 < sp < 1:
        h0 = STEM_TOP + 40 + (RIM - STEM_TOP - 80) * sp
        pts = [(GX - _halfwidth(h) + 22, GLASS_FOOT - h) for h in np.linspace(h0 - 40, h0 + 40, 10)]
        stroke_path(f, pts, (255, 255, 255), 6, alpha=math.sin(math.pi * sp) * 0.9)
    # the wordmark: a small white-on-red chip, matching the chip on the Reel's next slide (Steve). Its red is the
    # arc's chip color, so it matches the next slide in every arc.
    if P["chip"] > 0:
        chip(f, "THE FIELD GUIDE", W / 2, 1330, P["chip"], fill=accent, ink=(255, 255, 255), size=54, align="center", tracking=2)
    if P["motes"] > 0:
        for i, (mx, my, sp_) in enumerate(_MOTES):
            yy_ = my - (P["mote_t"] - 1.35) * 90 * sp_
            a = P["motes"] * 0.55 * (0.5 + 0.5 * math.sin(P["mote_t"] * 3 + i))
            fill_poly(f, [(mx + 3 * math.cos(k), yy_ + 3 * math.sin(k)) for k in np.linspace(0, 2 * math.pi, 10)], GOLD, a)
    M = cv2.getRotationMatrix2D((W / 2, H * 0.45), 0, P["zoom"])
    f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if P["fade"] > 0:
        f *= 1 - P["fade"]
    return f


def bumper(t, accent=(178, 34, 52)):
    return _frame(_intro_state(t), accent)


def bumper_outro(t, accent=(178, 34, 52)):
    return _frame(_outro_state(t), accent)


# ----------------------------------------------------------------------------- the sonic logo
def bumper_audio():
    from reel_audio import SR, tvec, lp, hp, bp, place, knock, impact, rng
    n = int(BUMPER_DUR * SR)
    L = np.zeros(n); R = np.zeros(n)
    k0 = int(0.3 * SR)                                        # a paper swish as the book draws itself
    sw0 = bp(rng.normal(0, 1, k0), 1500, 6000) * np.sin(np.pi * tvec(k0) / 0.3) ** 2
    place(L, sw0 * 0.05, 0.08); place(R, sw0 * 0.05, 0.1)
    th = (np.sin(2 * np.pi * 110 * tvec(int(0.16 * SR))) * np.exp(-tvec(int(0.16 * SR)) / 0.04)
          + bp(rng.normal(0, 1, int(0.16 * SR)), 300, 1500) * np.exp(-tvec(int(0.16 * SR)) / 0.015) * 0.5)
    place(L, th * 0.5, 0.86); place(R, th * 0.5, 0.86)        # the cover lands open: a soft thup
    k1 = int(0.4 * SR); tk1 = tvec(k1)                        # a page flutter as one page turns
    flut = bp(rng.normal(0, 1, k1), 1200, 5000) * (0.55 + 0.45 * np.sin(2 * np.pi * 26 * tk1)) * np.sin(np.pi * tk1 / 0.4) ** 1.5
    place(L, flut * 0.07, 0.86); place(R, flut * 0.06, 0.9)
    m = int(1.6 * SR); tt = tvec(m)                           # the glass: inharmonic bell partials
    ting = sum(a * np.sin(2 * np.pi * fq * tt) * np.exp(-tt / d) for fq, a, d in
               ((2349, 1.0, 0.9), (3520, 0.55, 0.6), (5280, 0.3, 0.35), (6912, 0.18, 0.2)))
    place(L, ting * 0.11, 1.32); place(R, ting * 0.11, 1.325)   # the rim closes
    k = int(0.6 * SR); tk = tvec(k)                           # the pour
    pour = bp(rng.normal(0, 1, k), 300, 1800) * (0.5 + 0.5 * np.sin(2 * np.pi * 11 * tk)) * np.sin(np.pi * tk / 0.6)
    place(L, pour * 0.05, 1.15); place(R, pour * 0.05, 1.15)
    for i, fq in enumerate((440.0, 659.25, 880.0)):          # A - E - A on the wordmark
        q = int(1.4 * SR); tq = tvec(q)
        bell = sum(a * np.sin(2 * np.pi * fq * h * tq) * np.exp(-tq / d) for h, a, d in ((1, 1.0, 0.9), (2, 0.4, 0.5), (3, 0.2, 0.3), (4.2, 0.1, 0.15)))
        place(L, bell * 0.13, 1.55 + 0.16 * i); place(R, bell * 0.13, 1.56 + 0.16 * i)
    s = int(1.6 * SR); ts = tvec(s)                           # warm swell under the wordmark
    sw = sum(np.sin(2 * np.pi * fq * ts) for fq in (220.0, 329.63, 440.0, 554.37)) * np.minimum(1, ts / 0.6) * np.exp(-np.maximum(ts - 0.9, 0) / 0.5)
    sw = lp(sw, 1800) * 0.03
    place(L, sw, 1.4); place(R, sw, 1.4)
    out = np.stack([hp(L, 30), hp(R, 30)], 1)
    return out


def bumper_outro_audio():
    """The outro's sound mirrors the intro's: the wine drains, the lines erase, the cover closes with a thump,
    and the bells play A-E-A descending (high to low)."""
    from reel_audio import SR, tvec, lp, hp, bp, place, rng
    n = int(BUMPER_DUR * SR)
    L = np.zeros(n); R = np.zeros(n)
    k = int(0.95 * SR); tk = tvec(k)                          # the wine drains: a soft, falling gurgle
    gl = bp(rng.normal(0, 1, k), 200, 1100) * (0.5 + 0.5 * np.sin(2 * np.pi * (9 - 4 * tk) * tk)) * np.sin(np.pi * tk / 0.95)
    place(L, gl * 0.05, 0.3); place(R, gl * 0.05, 0.3)
    k1 = int(0.35 * SR)                                       # the lines erase
    sw = bp(rng.normal(0, 1, k1), 2000, 7000) * np.sin(np.pi * tvec(k1) / 0.35) ** 2
    place(L, sw * 0.035, 0.85); place(R, sw * 0.035, 0.95)
    th = (np.sin(2 * np.pi * 96 * tvec(int(0.2 * SR))) * np.exp(-tvec(int(0.2 * SR)) / 0.05)
          + bp(rng.normal(0, 1, int(0.2 * SR)), 250, 1400) * np.exp(-tvec(int(0.2 * SR)) / 0.02) * 0.5)
    place(L, th * 0.55, 1.84); place(R, th * 0.55, 1.84)      # the cover closes
    for i, fq in enumerate((880.0, 659.25, 440.0)):           # A - E - A, descending
        q = int(1.6 * SR); tq = tvec(q)
        bell = sum(a * np.sin(2 * np.pi * fq * h * tq) * np.exp(-tq / d) for h, a, d in ((1, 1.0, 1.0), (2, 0.4, 0.55), (3, 0.2, 0.3), (4.2, 0.1, 0.15)))
        place(L, bell * 0.13, 1.95 + 0.17 * i); place(R, bell * 0.13, 1.96 + 0.17 * i)
    out = np.stack([hp(L, 30), hp(R, 30)], 1)
    fade = np.ones(n); fn = int(0.5 * SR); fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
    return out * fade[:, None]

