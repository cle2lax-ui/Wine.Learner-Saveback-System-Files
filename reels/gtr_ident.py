"""GUESS THE REGION -- opening ident for every Guess the Region Reel. 3.0 s, 1080x1920.

v2 (Steve): tie in the series' own logo, the FOLDED MAP AND PIN (formats/guess_the_region._folded_map_icon, locked in
GTR_STYLE_GUIDE s4). The map starts open, spins a little, then the pin drops in. The geometry is the locked logo's,
recomputed from the same parameters (not traced), so the ident IS the logo, animated. Same family as The Field Guide
bumper: white line art on the same warm dark ground, the chip in the arc's color.

STORYBOARD (times below are the ORIGINAL 3-second timeline; on screen each is divided by SPEED = 1.5, so it all happens
in 2 s: the unfold at 0.23-0.7 s, the pin at 0.87-1.17 s, the wordmark at 1.27 s)
  0.05-0.3   v3 (Steve: unfold, spin, then the pin): the map pops in FOLDED, its four panels stacked accordion-style
  0.35-1.05  it unfolds panel by panel (the second and fourth panels swing out from behind) while it
  0.1-1.25   spins a little: swings in from -38 degrees with a swivel (squashed, as if turning toward you),
             overshoots slightly and settles square
  1.3-1.75   the pin drops in to its logo position over the dip, bounces; a shadow, then a landing ripple
  1.75-1.9   the pin's inner ring pops in
  1.9-2.3    the GUESS THE REGION chip (accent fill, white type)
  2.3-3.0    hold, with a slow push-in; the Reel's own transition covers the cut at 3.0
SONIC LOGO (ident_audio): a paper rustle as the map opens; a soft whoosh as it spins; a pin-drop thunk; a rising fifth
E5 -> B5 (the sound of a question) over a warm swell. Fixed pitches on every Reel.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_lib import (W, H, chip, fill_poly, in_out_cubic, out_back, out_cubic, prog, round_rect, stroke_path, text,  # noqa: E402
                      text_width)

IDENT_DUR = 2.0           # v4 (Steve: faster): the animation runs 1.5x faster, so the ident is 2 s, not 3
SPEED = 1.5               # every internal time below is in the original 3-second timeline, divided by SPEED on screen
_BASE = IDENT_DUR * SPEED
GROUND = (16, 12, 14)                     # the same warm dark as The Field Guide bumper
LINE = (246, 242, 234)
LEMON = (246, 232, 98)
GOLD = (206, 168, 92)
CX, CY = W / 2, 820                       # the map's center on screen
MW = 600                                  # the map's width (the logo's w)
LW_ = 22                                  # line weight: the decks draw the logo at about w/17


def _logo_geometry(w=MW, k=1.0):
    """The locked logo (guess_the_region._folded_map_icon), in coordinates centered on the map. k unfolds it: at k = 0
    the four panels are stacked accordion-style (each even panel folded back over the one before), at k = 1 it is the
    logo exactly. The folded-back panels' horizontal run goes from -a to +a, so the folds open continuously."""
    th = w * 0.59
    peak, dip, tip = 0.0, w * (0.644 - 0.57), w * 0.644
    a = 0.25 * w
    fx = [0.0]
    for dx in (a, a * (2 * k - 1), a, a * (2 * k - 1)):
        fx.append(fx[-1] + dx)
    top = [(x, y) for x, y in zip(fx, [tip, peak, dip, peak, tip])]
    bot = [(x, y) for x, y in zip(fx, [tip, peak + th, dip + th, peak + th, tip])]
    cx, cy = (min(fx) + max(fx)) / 2, (peak + max(tip, dip + th)) / 2     # stays centered as it unfolds
    route = []
    mids = [(t[1] + b[1]) / 2 for t, b in zip(top, bot)]
    for i in range(161):
        tt = i / 160
        seg = min(int(tt * 4), 3)
        lt = tt * 4 - seg
        route.append((fx[seg] + (fx[seg + 1] - fx[seg]) * lt, mids[seg] + (mids[seg + 1] - mids[seg]) * lt))
    pr = w * 0.155
    ptip = (fx[2] + w * 0.11, dip + th * 0.32)
    pc = (ptip[0], ptip[1] - pr * 2.05)
    sh = lambda pts: [(x - cx, y - cy) for x, y in pts]          # noqa: E731
    return dict(top=sh(top), bot=sh(bot), creases=[sh([top[i], bot[i]]) for i in (1, 2, 3)], route=sh(route),
                pin_c=(pc[0] - cx, pc[1] - cy), pin_tip=(ptip[0] - cx, ptip[1] - cy), pin_r=pr)


GEO_ = _logo_geometry()


def _spin(t):
    """In-plane angle and horizontal swivel: in from -38 degrees, a slight overshoot, settle square."""
    p = prog(t, 0.1, 1.25)
    ang = -38 * (1 - out_back(p, 1.5))
    sx = 0.45 + 0.55 * out_cubic(prog(t, 0.1, 0.9))
    return ang, sx


def _xf(pts, ang, sx, sc=1.0):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for x, y in pts:
        x, y = x * sx * sc, y * sc
        out.append((CX + x * ca - y * sa, CY + x * sa + y * ca))
    return out


def _dashes(pts, frac, dash, gap):
    """The route as dashes, revealed along its length up to frac."""
    P = np.array(pts, np.float64)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    L = d[-1] * frac
    segs, s0, on = [], 0.0, True
    while s0 < L:
        s1 = min(s0 + (dash if on else gap), L)
        if on:
            i0, i1 = np.searchsorted(d, s0), np.searchsorted(d, s1)
            seg = [tuple(np.interp(s0, d, P[:, k]) for k in (0, 1))] + [tuple(P[i]) for i in range(i0, i1)]
            seg.append(tuple(np.interp(s1, d, P[:, k]) for k in (0, 1)))
            segs.append(seg)
        s0, on = s1, not on
    return segs


def _partial_path(pts, frac):
    P = np.array(pts, np.float64)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    L = d[-1] * frac
    k = int(np.searchsorted(d, L))
    if k <= 0:
        return [tuple(P[0])]
    if k >= len(P):
        return [tuple(p) for p in P]
    e = P[k - 1] + (P[k] - P[k - 1]) * ((L - d[k - 1]) / max(d[k] - d[k - 1], 1e-9))
    return [tuple(p) for p in P[:k]] + [tuple(e)]


def _wordmark(f, q, accent):
    """v4 (Steve: much larger): GUESS THE / REGION as a two-line chip, sized to the largest that fits the width (a one-line
    chip could only grow about 1.5x before reaching the screen edges)."""
    lines = ("GUESS THE", "REGION")
    sz = next(z for z in range(160, 54, -2) if max(text_width(l, "black", z, 2) for l in lines) + 1.2 * z <= W - 120)
    lh = 1.06 * sz
    hw = (max(text_width(l, "black", sz, 2) for l in lines) + 1.2 * sz) / 2
    hh = lh + 0.42 * sz
    cx, cy = W / 2, 1300
    round_rect(f, cx - hw * q, cy - hh * q, cx + hw * q, cy + hh * q, int(0.32 * sz * q) + 1, accent)
    for k, ln in enumerate(lines):
        yc = cy + (k - 0.5) * lh * q
        text(f, ln, "black", sz, (255, 255, 255), cx, yc + 0.36 * sz * q, align="center", tracking=2,
             alpha=min(1.0, q * 1.2), scale=q)


def ident(t, accent=(178, 34, 52)):
    import cv2
    t = t * SPEED                                     # run the original timeline 1.5x faster
    f = np.empty((H, W, 3), np.float32)
    f[:] = GROUND
    gq = out_cubic(prog(t, 0.9, 1.8))                 # warm glow behind the map
    if gq > 0:
        yy, xx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
        r = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
        glow = np.kron(np.clip(1 - r / 640, 0, 1) ** 2 * 0.14 * gq, np.ones((4, 4), np.float32))[:H, :W, None]
        f[:] = f * (1 - glow) + np.array(GOLD, np.float32) * glow
    ang, sx = _spin(t)
    G = GEO_
    aq = out_back(prog(t, 0.05, 0.3), 1.6)            # the folded map pops in...
    if aq > 0.02:
        k = in_out_cubic(prog(t, 0.35, 1.05))         # ...and unfolds while it spins
        Gk = _logo_geometry(MW, k) if k < 1 else G
        for edge in ("top", "bot"):
            stroke_path(f, _xf(Gk[edge], ang, sx, aq), LINE, LW_)
        for end in (Gk["top"][0], Gk["top"][-1]):
            fill_poly(f, _xf([(end[0] + LW_ / 2 * math.cos(a_), end[1] + LW_ / 2 * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 14)], ang, sx, aq), LINE)
        for cr in Gk["creases"]:                       # the creases (the folds themselves)
            stroke_path(f, _xf(cr, ang, sx, aq), LINE, LW_ - 6)
    rq = prog(t, 1.05, 1.35)                          # the dashed route, once it is flat
    if rq > 0:
        for seg in _dashes(G["route"], rq, MW * 0.042, MW * 0.034):
            stroke_path(f, _xf(seg, ang, sx), LINE, LW_ - 9)
    # the pin drops in (its logo position), with a shadow on the map and a landing ripple
    pq = prog(t, 1.3, 1.75)
    if pq > 0:
        drop = out_back(pq, 2.4)
        dy = -760 * (1 - drop)
        pc, ptip, pr = G["pin_c"], G["pin_tip"], G["pin_r"]
        sq = clamp_(pq * 1.6) * (1 - out_cubic(prog(t, 1.75, 2.2)))   # the shadow fades once the pin has landed,
                                                                        # so the ident ends on the exact logo
        sh_c = _xf([ptip], ang, sx)[0]
        fill_poly(f, [(sh_c[0] + 46 * sq * math.cos(a_), sh_c[1] + 12 * sq * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 24)],
                  (0, 0, 0), 0.45 * sq)
        a38 = math.radians(38)
        body = [(pc[0] + pr * math.cos(a_), pc[1] + pr * math.sin(a_)) for a_ in np.linspace(math.radians(90 + 38), math.radians(90 + 360 - 38), 40)]
        outline = [(x, y + dy) for x, y in body + [ptip]]
        fill_poly(f, _xf(outline, ang, sx), accent)   # v5 (Steve): a RED pin, matching the wordmark chip (filled, so the
        stroke_path(f, _xf(outline + [outline[0]], ang, sx), accent, LW_ - 2)   # map's lines don't show through it)
        iq = out_back(prog(t, 1.75, 1.9), 2.4)
        if iq > 0:
            ir = pr * 0.42 * iq
            stroke_path(f, _xf([(pc[0] + ir * math.cos(a_), pc[1] + dy + ir * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 30)], ang, sx),
                        LINE, LW_ - 6)
        rp = prog(t, 1.56, 2.1)                       # the landing ripple
        if 0 < rp < 1:
            rr = 40 + 150 * out_cubic(rp)
            stroke_path(f, [(sh_c[0] + rr * math.cos(a_), sh_c[1] + rr * 0.3 * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 60)],
                        LINE, 4, alpha=0.7 * (1 - rp))
    cq = out_back(prog(t, 1.9, 2.25), 1.7)
    if cq > 0:
        _wordmark(f, cq, accent)
    z = 1 + 0.035 * in_out_cubic(prog(t, 0, _BASE))
    M = cv2.getRotationMatrix2D((W / 2, H * 0.45), 0, z)
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def clamp_(v):
    return max(0.0, min(1.0, v))


def ident_audio():
    """The sonic logo at the faster speed: every event time is divided by SPEED; the buffer runs 1.5 s past the ident so
    the bells ring out into the first clue instead of being cut off."""
    from reel_audio import SR, tvec, lp, hp, bp, place, rng
    S_ = SPEED
    n = int((IDENT_DUR + 1.5) * SR)
    L = np.zeros(n); R_ = np.zeros(n)
    k0 = int(0.7 / S_ * SR); tk0 = tvec(k0)          # the map unfolds: a paper rustle
    rus = bp(rng.normal(0, 1, k0), 1500, 7000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 17 * S_ * tk0))) * np.sin(np.pi * tk0 / (0.7 / S_)) ** 1.5
    place(L, rus * 0.07, 0.35 / S_); place(R_, rus * 0.06, 0.38 / S_)
    sn = bp(rng.normal(0, 1, int(0.08 * SR)), 800, 6000) * np.exp(-tvec(int(0.08 * SR)) / 0.012)
    place(L, sn * 0.22, 1.03 / S_); place(R_, sn * 0.22, 1.03 / S_)    # ...and snaps flat
    k1 = int(0.9 / S_ * SR); tk1 = tvec(k1)           # it spins: a soft whoosh
    wsh = bp(rng.normal(0, 1, k1), 400, 3500) * np.sin(np.pi * tk1 / (0.9 / S_)) ** 2
    place(L, wsh * 0.05, 0.15 / S_); place(R_, wsh * 0.045, 0.18 / S_)
    th = (np.sin(2 * np.pi * 90 * tvec(int(0.2 * SR))) * np.exp(-tvec(int(0.2 * SR)) / 0.05)
          + bp(rng.normal(0, 1, int(0.2 * SR)), 250, 1400) * np.exp(-tvec(int(0.2 * SR)) / 0.02) * 0.5)
    place(L, th * 0.5, 1.56 / S_); place(R_, th * 0.5, 1.56 / S_)      # the pin lands
    for i, fq in enumerate((659.25, 987.77)):         # a rising fifth: the sound of a question
        q = int(1.4 * SR); tq = tvec(q)
        bell = sum(a * np.sin(2 * np.pi * fq * h * tq) * np.exp(-tq / d) for h, a, d in ((1, 1.0, 0.9), (2, 0.4, 0.5), (3, 0.2, 0.3)))
        place(L, bell * 0.14, (1.82 + 0.2 * i) / S_); place(R_, bell * 0.14, (1.83 + 0.2 * i) / S_)
    s = int(1.4 * SR); ts = tvec(s)                   # warm swell
    swl = sum(np.sin(2 * np.pi * fq * ts) for fq in (246.94, 329.63, 493.88)) * np.minimum(1, ts / 0.5) * np.exp(-np.maximum(ts - 0.8, 0) / 0.5)
    place(L, lp(swl, 1600) * 0.03, 1.6 / S_); place(R_, lp(swl, 1600) * 0.03, 1.6 / S_)
    return np.stack([hp(L, 30), hp(R_, 30)], 1)
