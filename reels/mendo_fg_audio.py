"""Score and sound design for THE FIELD GUIDE: MENDOCINO (65 s, 48 kHz stereo).

Original and synthesized (reels/reel_audio.py): no samples, no library music. Steve: "The pacing, music
and sound effects are excellent. Keep that direction."

ARRANGEMENT (120 BPM in D major, D-A-Bm-G; the grid starts when the bumper ends, at 3.0 s, so every scene
cut lands on a downbeat)
  0-3     the bumper's sonic logo (tfg_bumper.bumper_audio): book thumps, glass ting, pour, bells A-E-A
  3-7     hook: pad and plucks; hats creep in; a riser into the first full cut
  7-23    full groove: kick, clap, hats, bass, pad, plucked arpeggio (the kick ducks pad and bass)
  23-31   the fog: HALF-TIME -- no clap, kick on 1 and 3, drums low-passed, an airy pad: a breath mid-Reel
  31-59   full groove again; a shimmer layer through the sparkling scene
  59-65   resolve on D (add9); the sonic logo's A-E-A bells return under the end card, bookending the Reel
Every sound effect reads its time from the picture (mendo_fg_reel.T), so nothing drifts off its event.
Checked by measurement (onsets on the cuts, clipping, loudness), not by ear.
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_audio import (SR, BEAT, rng, tvec, lp, hp, place, saw, kick, clap, hat, pluck, knock, tick, pop,  # noqa: E402
                        impact, whoosh, riser)
from mendo_fg_reel import T, DUR, CUTS_STRIPES, CUTS_FOG, CUTS_WHIP, CUTS_DISSOLVE  # noqa: E402
from tfg_bumper import bumper_audio, bumper_outro_audio, BUMPER_DUR  # noqa: E402

N = int(SR * DUR)
G0 = BUMPER_DUR                      # the grid starts when the bumper ends
GROOVE = (7.0, T("s_close", 0.0))    # to the end card, read from the picture; Islands in the Sky brings it back up
FOG = (23.0, 31.0)
CH = {"D": (73.42, (293.66, 369.99, 440.0)), "A": (110.0, (220.0, 277.18, 329.63)),
      "Bm": (123.47, (246.94, 293.66, 369.99)), "G": (98.0, (196.0, 246.94, 293.66))}


def chord_at(t0):
    if t0 < 7.0 or t0 >= GROOVE[1]:
        return "D"
    return ["D", "A", "Bm", "G"][int(round((t0 - 7.0) / 2.0)) % 4]


def shimmer(dur=0.5):
    n = int(dur * SR); t = tvec(n)
    f = 1800 + 2600 * t / dur
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / dur) ** 2 * 0.5


def bell(fq, dur=1.4):
    q = int(dur * SR); tq = tvec(q)
    return sum(a * np.sin(2 * np.pi * fq * h * tq) * np.exp(-tq / d) for h, a, d in ((1, 1.0, 0.9), (2, 0.4, 0.5), (3, 0.2, 0.3), (4.2, 0.1, 0.15)))


def build():
    drums = np.zeros(N); fogdrums = np.zeros(N); kenv = np.zeros(N)
    mL = np.zeros(N); mR = np.zeros(N); verb = np.zeros(N); sfx = np.zeros(N)
    g0, g1 = GROOVE
    k = kick()
    for b in np.arange(g0, g1, BEAT):
        infog = FOG[0] <= b < FOG[1]
        if infog and int(round((b - g0) / BEAT)) % 2 == 1:
            continue                                           # half-time in the fog
        place(fogdrums if infog else drums, k, b)
        i = int(b * SR); m = min(N, i + int(0.3 * SR))
        kenv[i:m] = np.maximum(kenv[i:m], np.exp(-tvec(m - i) / 0.12) * (0.6 if infog else 1.0))
    for b in np.arange(g0 + BEAT, g1, 2 * BEAT):
        if not (FOG[0] <= b < FOG[1]):
            place(drums, clap(), b, 0.85)
    for j, b in enumerate(np.arange(5.0, g1, BEAT / 4)):
        infog = FOG[0] <= b < FOG[1]
        if infog and j % 2:
            continue
        acc = (1.0 if j % 4 == 2 else 0.55) * (0.5 if b < g0 else 1.0)
        place(fogdrums if infog else drums, hat(open_=(j % 8 == 6)), b, 0.45 * acc)
    drums += lp(fogdrums, 900) * 1.4                            # the fog's drums: low-passed, muffled
    duck = 1 - 0.5 * kenv
    for t0 in np.arange(G0, DUR, 2.0):
        name = chord_at(t0)
        root, chord = CH[name]
        infog = FOG[0] <= t0 < FOG[1]
        n = int(min(2.0, DUR - t0) * SR)
        env = np.minimum(1, tvec(n) / (0.6 if infog else 0.3)) * np.minimum(1, (n / SR - tvec(n)) / 0.2 + 1e-4)
        for fq in chord:
            for side, dt in ((mL, -7), (mR, +7)):
                place(side, lp(saw(fq, n, 10, dt), 1400 if infog else 2000) * env * (0.085 if infog else 0.065), t0)
        place(verb, lp(saw(chord[0], n, 8), 1600) * env * (0.09 if infog else 0.05), t0)
        if t0 >= GROOVE[1]:
            continue
        groove = g0 <= t0 < g1 and not infog
        pat = [0, 2, 1, 2, 0, 2, 1, 2] if groove else [0, 2, 1, 2]
        step = BEAT / 4 if groove else BEAT / 2
        for s in range(int(2.0 / step)):
            ta = t0 + s * step
            sig = pluck(chord[pat[s % len(pat)]] * 2, 0.22, 1.4) * (0.15 if groove else 0.11)
            place(mL if s % 2 == 0 else mR, sig, ta)
            place(mR if s % 2 == 0 else mL, sig * 0.4, ta + 0.1875)
            place(verb, sig * (0.8 if infog else 0.5), ta)
        if g0 <= t0 < g1:
            for e in range(8 if not infog else 4):
                tb = t0 + e * (BEAT / 2 if not infog else BEAT)
                nb = int(0.22 * SR)
                sig = lp(saw(root * (2 if e == 7 else 1), nb, 10), 650) * np.exp(-tvec(nb) / 0.12) * 0.5
                place(mL, sig, tb); place(mR, sig, tb)
    mL *= duck; mR *= duck
    n = int(4.2 * SR)                                          # resolve under the end card (the outro carries
    env = np.minimum(1, tvec(n) / 0.02) * np.exp(-tvec(n) / 1.6)   # the closing bells, descending)
    for fq in (73.42, 146.83, 293.66, 369.99, 440.0, 659.25):
        sig = lp(saw(fq, n, 10), 2400) * env * 0.075
        place(mL, sig, GROOVE[1]); place(mR, sig, GROOVE[1]); place(verb, sig, GROOVE[1])
    for t_ in np.arange(T("s_sparkle", 0), T("s_sparkle", 8.0), 1.0):   # shimmer through the sparkling scene
        place(sfx, shimmer(0.6), t_ + 0.3, 0.05)

    # ---- sound design, at the picture's own events
    for i in range(9):
        place(sfx, knock(), T("s_hook", 0.32 + 0.05 * i + 0.22), 0.32)
    place(sfx, impact(0.6), T("s_hook", 0.62), 0.45)
    for i in range(5):
        place(sfx, pop(), T("s_hook", 0.9 + 0.85 * (0.2 + 0.07 * i) + 0.08), 0.22)
    place(sfx, whoosh(0.3, 800, 6000, 0.6), T("s_hook", 0.9 + 0.85 * 0.45), 0.25)
    place(sfx, shimmer(0.55), T("s_hook", 1.6), 0.12)
    place(sfx, riser(0.55), 6.45, 0.45)
    for c in CUTS_STRIPES:
        place(sfx, whoosh(0.44, 300, 6500, 0.5), c - 0.22, 0.6)
        place(sfx, impact(1.0 if c != 3.0 else 0.8), c, 0.6)
    for c in CUTS_FOG:
        place(sfx, whoosh(1.0, 150, 1800, 0.5), c - 0.5, 0.7)
        place(sfx, impact(0.5), c, 0.35)
    for c in CUTS_WHIP:
        place(sfx, whoosh(0.26, 600, 9000, 0.85), c - 0.13, 0.7)
        place(sfx, impact(0.6), c, 0.5)
    pen = hp(rng.normal(0, 1, int(1.0 * SR)), 3000) * 0.05
    place(sfx, pen * np.sin(np.pi * tvec(len(pen)) / 1.0), T("s_place", 0.1))
    place(sfx, pop(), T("s_place", 0.98), 0.35)
    place(sfx, whoosh(0.8, 200, 3000, 0.7), T("s_place", 1.35), 0.4)
    for i in range(13):
        place(sfx, pop(), T("s_place", 2.3 + 0.15 * i + 0.04), 0.18)
        place(sfx, tick(), T("s_place", 2.3 + 0.15 * i + 0.06), 0.1)
    place(sfx, impact(0.45), T("s_place", 4.1), 0.4)
    place(sfx, pop(), T("s_place", 4.7), 0.25)
    for j in range(22):
        place(sfx, tick(), T("s_place", 5.4 + j * 0.035 * (1 + j / 22)), 0.1)
    for u0, g in ((0.0, 0.35), (0.15, 0.3), (0.55, 0.3)):
        place(sfx, whoosh(0.5, 200, 2500 if u0 < 0.5 else 5000, 0.8), T("s_climates", u0), g)
    for u0 in (0.27, 0.48, 0.58):
        place(sfx, pop(), T("s_climates", u0), 0.22)
    for u0 in (1.15, 2.55):
        place(sfx, impact(0.35), T("s_climates", u0), 0.35)
    for k_ in range(3):
        place(sfx, pop(), T("s_climates", 1.55 + 0.12 * k_ + 0.08), 0.22)
    for k_ in range(4):
        place(sfx, pop(), T("s_climates", 2.95 + 0.12 * k_ + 0.08), 0.22)
    place(sfx, whoosh(0.5, 300, 3500, 0.8), T("s_climates", 4.3), 0.35)
    place(sfx, impact(0.35), T("s_climates", 4.65), 0.3)      # ALTITUDE FLIPS IT slams in
    for k_ in range(2):
        place(sfx, pop(), T("s_climates", 5.15 + 0.15 * k_ + 0.08), 0.25)
    place(sfx, pop(), T("s_fog", 0.08), 0.22)                  # the fog
    place(sfx, impact(0.35), T("s_fog", 0.2), 0.3)
    place(sfx, pen * np.sin(np.pi * tvec(len(pen)) / 1.0) * 0.8, T("s_fog", 0.4))
    air = lp(rng.normal(0, 1, int(6.0 * SR)), 700) * 0.06
    place(sfx, air * np.minimum(1, tvec(len(air)) / 1.5) * np.minimum(1, (6.0 - tvec(len(air))) / 1.5), T("s_fog", 1.4))
    for u0 in (3.0, 4.2):
        place(sfx, whoosh(0.35, 400, 4000, 0.7), T("s_fog", u0), 0.25)
    place(sfx, pop(), T("s_numbers", 0.08), 0.22)              # by the numbers
    place(sfx, impact(0.35), T("s_numbers", 0.15), 0.3)
    for k_ in range(4):
        place(sfx, knock(), T("s_numbers", 0.6 + 0.35 * k_), 0.4)
        for j in range(8):
            place(sfx, tick(), T("s_numbers", 0.8 + 0.35 * k_ + 0.06 * j), 0.07)
    place(sfx, pop(), T("s_pinot", 0.08), 0.22)                # the Pinot Noir
    place(sfx, impact(0.4), T("s_pinot", 0.3), 0.35)
    for t0, lvl in ((1.0, 3), (1.5, 4)):
        for s_ in range(lvl):
            place(sfx, tick(), T("s_pinot", t0 + 0.1 * s_), 0.14)
    for k_ in range(3):
        place(sfx, pop(), T("s_pinot", 2.5 + 0.25 * k_ + 0.1), 0.3)
    for k_ in range(2):
        place(sfx, pop(), T("s_pinot", 3.6 + 0.25 * k_ + 0.1), 0.25)
    place(sfx, pop(), T("s_sparkle", 0.08), 0.22)              # sparkling, then the Alsace whites
    for u0 in (0.25, 0.55, 4.3, 4.55):
        place(sfx, impact(0.35), T("s_sparkle", u0), 0.3)
    for k_ in range(2):
        place(sfx, pop(), T("s_sparkle", 1.5 + 0.12 * k_ + 0.1), 0.22)
    place(sfx, whoosh(0.6, 300, 5000, 0.6), T("s_sparkle", 3.9), 0.3)
    for j in range(8):                                        # the latitude ruler draws its ticks
        place(sfx, tick(), T("s_sparkle", 4.7 + 0.06 * j), 0.08)
    place(sfx, pop(), T("s_sparkle", 5.2), 0.3)                # ALSACE lands
    place(sfx, whoosh(0.8, 300, 2500, 0.6), T("s_sparkle", 5.6), 0.3)   # the second pin travels south
    for j in range(9):
        place(sfx, tick(), T("s_sparkle", 5.6 + 0.8 * j / 9), 0.1)     # one tick per degree
    place(sfx, impact(0.4), T("s_sparkle", 6.4), 0.35)         # ANDERSON VALLEY lands
    place(sfx, whoosh(0.35, 500, 4000, 0.7), T("s_sparkle", 6.5), 0.25)  # the bracket
    for k_ in range(4):
        place(sfx, pop(), T("s_sparkle", 7.4 + 0.12 * k_ + 0.1), 0.22)
    place(sfx, pop(), T("s_business", 0.08), 0.22)             # the business
    place(sfx, impact(0.35), T("s_business", 0.15), 0.3)
    for k_ in range(3):
        place(sfx, whoosh(0.4, 300, 4000, 0.7), T("s_business", 0.6 + 1.0 * k_), 0.3)
        place(sfx, pop(), T("s_business", 1.0 + 1.0 * k_), 0.2)
    place(sfx, pop(), T("s_ridge", 0.08), 0.22)                # Islands in the Sky
    place(sfx, impact(0.4), T("s_ridge", 0.2), 0.35)
    place(sfx, whoosh(0.7, 150, 2200, 0.6), T("s_ridge", 0.15), 0.35)   # the ridges rise
    airr = lp(rng.normal(0, 1, int(1.2 * SR)), 600) * 0.05
    place(sfx, airr * np.sin(np.pi * tvec(len(airr)) / 1.2), T("s_ridge", 0.5))   # the fog fills the valleys
    for j in range(10):                                        # the 1,200 ft line draws across
        place(sfx, tick(), T("s_ridge", 1.0 + 0.06 * j), 0.08)
    for j in range(4):                                         # vines appear on the ridgetops
        place(sfx, pop(), T("s_ridge", 1.5 + 0.18 * j), 0.15)
    for j in range(16):                                        # 250 acres counts up
        place(sfx, tick(), T("s_ridge", 2.3 + j * 0.04 * (1 + j / 16)), 0.09)
    for k_ in range(2):
        place(sfx, pop(), T("s_ridge", 3.9 + 0.12 * k_ + 0.08), 0.22)
    place(sfx, impact(0.4), T("s_close", 0.25), 0.35)          # the end card
    place(sfx, pop(), T("s_close", 1.5), 0.3)

    ir_n = int(1.5 * SR)
    irL = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.42); irR = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.42)
    irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
    vL = fftconvolve(verb + sfx * 0.25, irL)[:N] * 0.6
    vR = fftconvolve(verb + sfx * 0.25, irR)[:N] * 0.6
    out = np.stack([hp(drums * 0.9 + mL + sfx + vL, 28), hp(drums * 0.9 + mR + sfx + vR, 28)], 1)
    b = bumper_audio()                                         # the sonic logo, 0-3 s
    out[:len(b)] += b
    o = bumper_outro_audio()                                   # and its mirror, closing the Reel
    i0 = int(T("s_outro", 0) * SR)
    out[i0:i0 + len(o)] += o[:max(0, N - i0)]
    fade = np.ones(N); fn = int(0.6 * SR); fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
    out *= fade[:, None]
    out = np.tanh(out * 1.4) / np.tanh(1.4)
    return out / (np.max(np.abs(out)) / 0.89)


if __name__ == "__main__":
    a = build()
    path = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/mendo_fg_audio.wav"
    wavfile.write(path, SR, (a * 32767).astype(np.int16))
    print(f"wrote {path}: {len(a) / SR:.2f}s, peak {20 * np.log10(np.abs(a).max()):.2f} dBFS")
