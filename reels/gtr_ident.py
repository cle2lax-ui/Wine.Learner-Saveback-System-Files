"""GUESS THE REGION -- opening ident for every Guess the Region Reel. 3.0 s, 1080x1920.

The series' second ident, in the same family as The Field Guide bumper (tfg_bumper.py): white line art on the same
warm dark ground, the chip in the arc's color, a sonic logo of its own. Identical on every Reel except the accent.

STORYBOARD
  0.05-0.5   a compass ring draws itself (white line)
  0.4-0.8    tick marks and N / E / S / W pop in
  0.7-1.5    the needle appears and spins, decelerating, then settles on north with a damped wobble
  1.4-1.85   a map pin drops onto the compass and bounces
  1.8        a lemon "?" pops inside the pin
  1.9-2.3    the GUESS THE REGION chip (accent fill, white type)
  2.3-3.0    hold, with a slow push-in; the Reel's own transition covers the cut at 3.0
SONIC LOGO (ident_audio): a swish as the ring draws; ratcheting ticks that slow as the needle settles; a pin-drop
thunk; a rising fifth E5 -> B5 (the sound of a question) over a warm swell. Fixed pitches on every Reel.
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
CX, CY, R = W / 2, 820, 250               # the compass


def _needle_angle(t):
    """Spin fast, decelerate, then settle on north (0) with a damped wobble."""
    if t < 0.7:
        return None
    if t < 1.5:
        p = prog(t, 0.7, 1.5)
        return (1 - out_cubic(p)) * 3 * 360 + 25 * (1 - p)
    return 25 * math.exp(-(t - 1.5) * 6) * math.cos((t - 1.5) * 18)


def ident(t, accent=(178, 34, 52)):
    import cv2
    f = np.empty((H, W, 3), np.float32)
    f[:] = GROUND
    gq = out_cubic(prog(t, 0.9, 1.8))                 # warm glow behind the compass
    if gq > 0:
        yy, xx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)
        r = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
        glow = np.kron(np.clip(1 - r / 620, 0, 1) ** 2 * 0.14 * gq, np.ones((4, 4), np.float32))[:H, :W, None]
        f[:] = f * (1 - glow) + np.array(GOLD, np.float32) * glow
    rq = in_out_cubic(prog(t, 0.05, 0.5))             # the ring draws itself
    if rq > 0:
        a = np.linspace(-math.pi / 2, -math.pi / 2 + 2 * math.pi * rq, max(int(120 * rq), 2))
        stroke_path(f, [(CX + R * math.cos(x), CY + R * math.sin(x)) for x in a], LINE, 7)
        if rq >= 1:
            stroke_path(f, [(CX + (R - 26) * math.cos(x), CY + (R - 26) * math.sin(x)) for x in np.linspace(0, 2 * math.pi, 120)],
                        LINE, 2, alpha=0.5)
    for k in range(36):                               # ticks
        q = out_back(prog(t, 0.4 + k * 0.006, 0.55 + k * 0.006), 2.0)
        if q <= 0:
            continue
        ang = math.radians(k * 10 - 90)
        L = (34 if k % 9 == 0 else 18 if k % 3 == 0 else 10) * q
        r0 = R - 30
        stroke_path(f, [(CX + r0 * math.cos(ang), CY + r0 * math.sin(ang)),
                        (CX + (r0 - L) * math.cos(ang), CY + (r0 - L) * math.sin(ang))], LINE, 4 if k % 9 == 0 else 2)
    for lab, ang in (("N", -90), ("E", 0), ("S", 90), ("W", 180)):
        q = out_cubic(prog(t, 0.6, 0.8))
        if q > 0:
            rr = R + 52
            text(f, lab, "black", 40, accent if lab == "N" else LINE, CX + rr * math.cos(math.radians(ang)),
                 CY + rr * math.sin(math.radians(ang)) + 14, align="center", alpha=q)
    na = _needle_angle(t)                             # the needle: red north half, white south half
    nfade = 1 - out_cubic(prog(t, 1.72, 1.95))        # it fades as the pin lands: the needle has found the place (left
    if na is not None and nfade > 0.01:               # visible, its white south half read as a tail on the pin)
        nq = out_back(prog(t, 0.7, 0.85), 1.6)
        L, Wd = (R - 70) * nq, 26 * nq
        a = math.radians(na - 90)
        tip = (CX + L * math.cos(a), CY + L * math.sin(a))
        tail = (CX - L * math.cos(a), CY - L * math.sin(a))
        side = (math.cos(a + math.pi / 2) * Wd, math.sin(a + math.pi / 2) * Wd)
        fill_poly(f, [tip, (CX + side[0], CY + side[1]), (CX - side[0], CY - side[1])], accent, nfade)
        fill_poly(f, [tail, (CX + side[0], CY + side[1]), (CX - side[0], CY - side[1])], LINE, nfade)
        fill_poly(f, [(CX + 12 * math.cos(x), CY + 12 * math.sin(x)) for x in np.linspace(0, 2 * math.pi, 20)], GROUND, nfade)
        stroke_path(f, [(CX + 12 * math.cos(x), CY + 12 * math.sin(x)) for x in np.linspace(0, 2 * math.pi, 20)], LINE, 3, alpha=nfade)
    # the map pin drops onto the compass and bounces
    pq = prog(t, 1.4, 1.85)
    if pq > 0:
        drop = out_back(pq, 2.4)
        py = CY - 120 - 700 * (1 - drop)
        pr = 74
        tipy = py + pr * 1.9
        pin = [(CX + pr * math.cos(x), py + pr * math.sin(x)) for x in np.linspace(math.radians(140), math.radians(400), 40)]
        pin = pin + [(CX, tipy)]
        fill_poly(f, pin, GROUND)
        stroke_path(f, pin + [pin[0]], LINE, 7)
        qq = out_back(prog(t, 1.8, 2.0), 2.4)
        if qq > 0:
            text(f, "?", "cond", 104, LEMON, CX, py + 38, align="center", scale=qq)
    cq = out_back(prog(t, 1.9, 2.25), 1.7)
    if cq > 0:
        chip(f, "GUESS THE REGION", W / 2, 1250, cq, fill=accent, ink=(255, 255, 255), size=54, align="center", tracking=2)
    z = 1 + 0.035 * in_out_cubic(prog(t, 0, IDENT_DUR))
    M = cv2.getRotationMatrix2D((W / 2, H * 0.45), 0, z)
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def ident_audio():
    from reel_audio import SR, tvec, lp, hp, bp, place, rng
    n = int(IDENT_DUR * SR)
    L = np.zeros(n); R_ = np.zeros(n)
    k0 = int(0.45 * SR)                               # the ring draws: a swish
    sw = bp(rng.normal(0, 1, k0), 1200, 6000) * np.sin(np.pi * tvec(k0) / 0.45) ** 2
    place(L, sw * 0.05, 0.05); place(R_, sw * 0.05, 0.07)
    t_, k = 0.72, 0                                   # ratcheting ticks that slow as the needle settles
    while t_ < 1.55:
        m = int(0.012 * SR)
        clk = np.sin(2 * np.pi * 3200 * tvec(m)) * np.exp(-tvec(m) / 0.003)
        place(L if k % 2 else R_, clk * 0.18, t_)
        t_ += 0.022 + 0.11 * prog(t_, 0.72, 1.55) ** 2
        k += 1
    th = (np.sin(2 * np.pi * 90 * tvec(int(0.2 * SR))) * np.exp(-tvec(int(0.2 * SR)) / 0.05)
          + bp(rng.normal(0, 1, int(0.2 * SR)), 250, 1400) * np.exp(-tvec(int(0.2 * SR)) / 0.02) * 0.5)
    place(L, th * 0.5, 1.72); place(R_, th * 0.5, 1.72)  # the pin lands
    for i, fq in enumerate((659.25, 987.77)):         # a rising fifth: the sound of a question
        q = int(1.4 * SR); tq = tvec(q)
        bell = sum(a * np.sin(2 * np.pi * fq * h * tq) * np.exp(-tq / d) for h, a, d in ((1, 1.0, 0.9), (2, 0.4, 0.5), (3, 0.2, 0.3)))
        place(L, bell * 0.14, 1.82 + 0.2 * i); place(R_, bell * 0.14, 1.83 + 0.2 * i)
    s = int(1.4 * SR); ts = tvec(s)                   # warm swell
    swl = sum(np.sin(2 * np.pi * fq * ts) for fq in (246.94, 329.63, 493.88)) * np.minimum(1, ts / 0.5) * np.exp(-np.maximum(ts - 0.8, 0) / 0.5)
    place(L, lp(swl, 1600) * 0.03, 1.6); place(R_, lp(swl, 1600) * 0.03, 1.6)
    return np.stack([hp(L, 30), hp(R_, 30)], 1)
