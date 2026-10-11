"""GUESS THE REGION -- opening ident for every Guess the Region Reel. 3.0 s, 1080x1920.

v2 (Steve): tie in the series' own logo, the FOLDED MAP AND PIN (formats/guess_the_region._folded_map_icon, locked in
GTR_STYLE_GUIDE s4). The map starts open, spins a little, then the pin drops in. The geometry is the locked logo's,
recomputed from the same parameters (not traced), so the ident IS the logo, animated. Same family as The Field Guide
bumper: white line art on the same warm dark ground, the chip in the arc's color.

STORYBOARD
  0.05-0.5   the map draws itself, already open: outline, then the creases, then the dashed route
  0.1-1.25   it spins a little: swings in from -38 degrees with a swivel (squashed, as if turning toward you),
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
from reel_lib import (W, H, chip, fill_poly, in_out_cubic, out_back, out_cubic, prog, stroke_path, text)  # noqa: E402

IDENT_DUR = 3.0
GROUND = (16, 12, 14)                     # the same warm dark as The Field Guide bumper
LINE = (246, 242, 234)
LEMON = (246, 232, 98)
GOLD = (206, 168, 92)
CX, CY = W / 2, 820                       # the map's center on screen
MW = 600                                  # the map's width (the logo's w)
LW_ = 22                                  # line weight: the decks draw the logo at about w/17


def _logo_geometry(w=MW):
    """The locked logo (guess_the_region._folded_map_icon), in coordinates centered on the map."""
    th = w * 0.59
    peak, dip, tip = 0.0, w * (0.644 - 0.57), w * 0.644
    fx = [0.0, 0.25 * w, 0.5 * w, 0.75 * w, w]
    top = [(x, y) for x, y in zip(fx, [tip, peak, dip, peak, tip])]
    bot = [(x, y) for x, y in zip(fx, [tip, peak + th, dip + th, peak + th, tip])]
    cx, cy = w / 2, (peak + max(tip, dip + th)) / 2
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


def ident(t, accent=(178, 34, 52)):
    import cv2
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
    dq = in_out_cubic(prog(t, 0.05, 0.42))            # the outline draws, from the left tip both ways
    if dq > 0:
        for edge in ("top", "bot"):
            stroke_path(f, _xf(_partial_path(G[edge], dq), ang, sx), LINE, LW_)
        for end in (G["top"][0], G["top"][-1]):
            if dq >= 1:
                fill_poly(f, _xf([(end[0] + LW_ / 2 * math.cos(a_), end[1] + LW_ / 2 * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 14)], ang, sx), LINE)
    for i, cr in enumerate(G["creases"]):             # the creases
        q = out_cubic(prog(t, 0.3 + 0.05 * i, 0.5 + 0.05 * i))
        if q > 0:
            stroke_path(f, _xf(_partial_path(cr, q), ang, sx), LINE, LW_ - 6)
    rq = prog(t, 0.45, 0.85)                          # the dashed route
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
        fill_poly(f, _xf(outline, ang, sx), GROUND)   # filled, so the map's lines don't show through it
        stroke_path(f, _xf(outline + [outline[0]], ang, sx), LINE, LW_ - 2)
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
        chip(f, "GUESS THE REGION", W / 2, 1250, cq, fill=accent, ink=(255, 255, 255), size=54, align="center", tracking=2)
    z = 1 + 0.035 * in_out_cubic(prog(t, 0, IDENT_DUR))
    M = cv2.getRotationMatrix2D((W / 2, H * 0.45), 0, z)
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def clamp_(v):
    return max(0.0, min(1.0, v))


def ident_audio():
    from reel_audio import SR, tvec, lp, hp, bp, place, rng
    n = int(IDENT_DUR * SR)
    L = np.zeros(n); R_ = np.zeros(n)
    k0 = int(0.5 * SR); tk0 = tvec(k0)                # the map opens: a paper rustle
    rus = bp(rng.normal(0, 1, k0), 1500, 7000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 17 * tk0))) * np.sin(np.pi * tk0 / 0.5) ** 1.5
    place(L, rus * 0.07, 0.05); place(R_, rus * 0.06, 0.08)
    k1 = int(0.9 * SR); tk1 = tvec(k1)                # it spins: a soft whoosh
    fsw = 300 + 2200 * np.sin(np.pi * tk1 / 0.9)
    wsh = bp(rng.normal(0, 1, k1), 400, 3500) * np.sin(np.pi * tk1 / 0.9) ** 2
    place(L, wsh * 0.05, 0.15); place(R_, wsh * 0.045, 0.18)
    th = (np.sin(2 * np.pi * 90 * tvec(int(0.2 * SR))) * np.exp(-tvec(int(0.2 * SR)) / 0.05)
          + bp(rng.normal(0, 1, int(0.2 * SR)), 250, 1400) * np.exp(-tvec(int(0.2 * SR)) / 0.02) * 0.5)
    place(L, th * 0.5, 1.56); place(R_, th * 0.5, 1.56)  # the pin lands (first contact of its bounce)
    for i, fq in enumerate((659.25, 987.77)):         # a rising fifth: the sound of a question
        q = int(1.4 * SR); tq = tvec(q)
        bell = sum(a * np.sin(2 * np.pi * fq * h * tq) * np.exp(-tq / d) for h, a, d in ((1, 1.0, 0.9), (2, 0.4, 0.5), (3, 0.2, 0.3)))
        place(L, bell * 0.14, 1.82 + 0.2 * i); place(R_, bell * 0.14, 1.83 + 0.2 * i)
    s = int(1.4 * SR); ts = tvec(s)                   # warm swell
    swl = sum(np.sin(2 * np.pi * fq * ts) for fq in (246.94, 329.63, 493.88)) * np.minimum(1, ts / 0.5) * np.exp(-np.maximum(ts - 0.8, 0) / 0.5)
    place(L, lp(swl, 1600) * 0.03, 1.6); place(R_, lp(swl, 1600) * 0.03, 1.6)
    return np.stack([hp(L, 30), hp(R_, 30)], 1)
