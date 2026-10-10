"""Score and sound design for GUESS THE REGION: ANDERSON VALLEY (45 s, 48 kHz stereo).

Original and synthesized (reels/reel_audio.py). 120 BPM; the grid starts when the ident ends (3.0 s).
ARRANGEMENT -- the quiz's dramatic shape:
  0-3     the ident's sonic logo (gtr_ident.ident_audio): swish, ratchet, pin drop, a rising fifth (a question)
  3-29    B minor (Bm-G-D-A), a lighter "thinking" groove: kick on 1 and 3, eighth-note hats, plucked arpeggio, pad
  29-33   PAUSE AND GUESS: the music drops out -- a ticking clock, a beep on each count, a riser into the reveal
  33-41   the ANSWER: D major (D-A-Bm-G), the full groove (four-on-the-floor, clap, bass)
  41-45   resolve; bells D-A-D answer the ident's question
Sound effects read their times from the picture (mendo_gtr_reel.T and its cut lists). Checked by measurement.
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_audio import (SR, BEAT, rng, tvec, lp, hp, bp, place, saw, kick, clap, hat, pluck, knock, tick, pop,  # noqa: E402
                        impact, whoosh, riser)
from mendo_gtr_reel import T, DUR, CUTS_STRIPES, CUTS_PUSH, CUTS_WHIP  # noqa: E402
from gtr_ident import ident_audio, IDENT_DUR  # noqa: E402

N = int(SR * DUR)
QUIZ = (IDENT_DUR, 29.0)
PAUSE = (29.0, 33.0)
ANSWER = (33.0, 41.0)
MINOR = {"Bm": (61.74, (246.94, 293.66, 369.99)), "G": (98.0, (196.0, 246.94, 293.66)),
         "D": (73.42, (293.66, 369.99, 440.0)), "A": (110.0, (220.0, 277.18, 329.63))}
PROG_Q = ["Bm", "G", "D", "A"]
PROG_A = ["D", "A", "Bm", "G"]


def bell(fq, dur=1.4, amp=1.0):
    q = int(dur * SR); tq = tvec(q)
    return amp * sum(a * np.sin(2 * np.pi * fq * h * tq) * np.exp(-tq / d) for h, a, d in ((1, 1.0, 0.9), (2, 0.4, 0.5), (3, 0.2, 0.3)))


def beep(fq, dur=0.13):
    n = int(dur * SR); t = tvec(n)
    return np.sin(2 * np.pi * fq * t) * np.minimum(1, t / 0.004) * np.exp(-t / 0.08)


def boop():
    """The meter drops a point: a short descending tone."""
    n = int(0.26 * SR); t = tvec(n)
    f = 880 * (0.5 ** (t / 0.26))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)


def build():
    drums = np.zeros(N); kenv = np.zeros(N)
    mL = np.zeros(N); mR = np.zeros(N); verb = np.zeros(N); sfx = np.zeros(N)
    k = kick()
    # quiz: kick on 1 and 3 from the first clue; hats from the rules
    for b in np.arange(5.0, QUIZ[1], 2 * BEAT):
        place(drums, k, b, 0.85)
        i = int(b * SR); m = min(N, i + int(0.3 * SR)); kenv[i:m] = np.maximum(kenv[i:m], np.exp(-tvec(m - i) / 0.12))
    for j, b in enumerate(np.arange(3.0, QUIZ[1], BEAT / 2)):
        place(drums, hat(open_=(j % 8 == 7)), b, 0.32 * (1.0 if j % 2 else 0.6))
    # answer: four on the floor, clap, sixteenth hats
    for b in np.arange(ANSWER[0], ANSWER[1], BEAT):
        place(drums, k, b, 1.0)
        i = int(b * SR); m = min(N, i + int(0.3 * SR)); kenv[i:m] = np.maximum(kenv[i:m], np.exp(-tvec(m - i) / 0.12))
    for b in np.arange(ANSWER[0] + BEAT, ANSWER[1], 2 * BEAT):
        place(drums, clap(), b, 0.85)
    for j, b in enumerate(np.arange(ANSWER[0], ANSWER[1], BEAT / 4)):
        place(drums, hat(open_=(j % 8 == 6)), b, 0.42 * (1.0 if j % 4 == 2 else 0.55))
    duck = 1 - 0.5 * kenv
    for t0 in np.arange(IDENT_DUR, DUR, 2.0):
        if PAUSE[0] <= t0 < PAUSE[1]:
            continue
        ans = t0 >= ANSWER[0]
        bi = int(round((t0 - (ANSWER[0] if ans else IDENT_DUR)) / 2.0))
        name = "D" if t0 >= ANSWER[1] else (PROG_A if ans else PROG_Q)[bi % 4]
        root, chord = MINOR[name]
        n = int(min(2.0, DUR - t0) * SR)
        env = np.minimum(1, tvec(n) / 0.3) * np.minimum(1, (n / SR - tvec(n)) / 0.2 + 1e-4)
        for fq in chord:
            for side, dt in ((mL, -7), (mR, +7)):
                place(side, lp(saw(fq, n, 10, dt), 1800) * env * 0.06, t0)
        place(verb, lp(saw(chord[0], n, 8), 1500) * env * 0.05, t0)
        if t0 >= ANSWER[1]:
            continue
        pat = [0, 2, 1, 2, 0, 2, 1, 2]
        step = BEAT / 4 if ans else BEAT / 2
        for s in range(int(2.0 / step)):
            ta = t0 + s * step
            sig = pluck(chord[pat[s % 8]] * 2, 0.22, 1.4) * (0.15 if ans else 0.12)
            place(mL if s % 2 == 0 else mR, sig, ta)
            place(mR if s % 2 == 0 else mL, sig * 0.4, ta + 0.1875)
            place(verb, sig * 0.5, ta)
        if t0 >= 5.0:
            for e in range(8 if ans else 4):
                tb = t0 + e * (BEAT / 2 if ans else BEAT)
                nb = int(0.22 * SR)
                sig = lp(saw(root * (2 if (ans and e == 7) else 1), nb, 10), 650) * np.exp(-tvec(nb) / 0.12) * 0.48
                place(mL, sig, tb); place(mR, sig, tb)
    mL *= duck; mR *= duck
    # the close: resolve, and bells D-A-D answer the ident's rising fifth
    n = int(4.0 * SR); env = np.minimum(1, tvec(n) / 0.02) * np.exp(-tvec(n) / 1.6)
    for fq in (73.42, 146.83, 293.66, 369.99, 440.0, 659.25):
        sig = lp(saw(fq, n, 10), 2400) * env * 0.07
        place(mL, sig, ANSWER[1]); place(mR, sig, ANSWER[1]); place(verb, sig, ANSWER[1])
    for i, fq in enumerate((587.33, 880.0, 1174.66)):
        place(mL, bell(fq, amp=0.12), T("s_cta", 1.4) + 0.16 * i); place(mR, bell(fq, amp=0.12), T("s_cta", 1.4) + 0.01 + 0.16 * i)

    # ---- sound design
    for c in CUTS_STRIPES:
        place(sfx, whoosh(0.44, 300, 6500, 0.5), c - 0.22, 0.6)
        place(sfx, impact(1.0 if c > 10 else 0.8), c, 0.7 if c > 10 else 0.55)
    for c in CUTS_PUSH:
        place(sfx, whoosh(0.5, 300, 4000, 0.6), c - 0.25, 0.45)
    for c in CUTS_WHIP:
        place(sfx, whoosh(0.26, 600, 9000, 0.85), c - 0.13, 0.7)
        place(sfx, impact(0.6), c, 0.5)
    for u0 in (0.1, 0.45, 0.6):                                # the rules
        place(sfx, impact(0.35), T("s_rules", u0), 0.3)
    place(sfx, pop(), 3.75, 0.3)                               # the meter arrives
    for t_ in (11.0, 17.0, 23.0):                              # ...and drops a point at each clue
        place(sfx, boop(), t_ + 0.02, 0.32)
    for sc in ("s_clue_a", "s_clue_b", "s_clue_c", "s_clue_d"):
        place(sfx, pop(), T(sc, 0.08), 0.22)                   # CLUE chip
        for k_ in range(3):
            place(sfx, tick(), T(sc, 0.35 + 0.12 * k_), 0.08)  # the clue's lines rise
    place(sfx, pop(), T("s_clue_a", 1.25), 0.35)               # the bubble
    place(sfx, pop(), T("s_clue_a", 2.15), 0.25)               # = GOOD DRINKING
    m = int(1.2 * SR); tt = tvec(m)                            # the glasses clink
    clink = sum(a * np.sin(2 * np.pi * fq * tt) * np.exp(-tt / d) for fq, a, d in ((2637, 1.0, 0.6), (3951, 0.5, 0.35), (5274, 0.25, 0.2)))
    place(sfx, clink * 0.1, T("s_clue_a", 2.95))
    place(sfx, whoosh(0.5, 200, 2500, 0.8), T("s_clue_b", 0.8), 0.3)    # hills
    arrow = np.sin(2 * np.pi * np.cumsum(500 + 900 * tvec(int(1.0 * SR))) / SR) * np.sin(np.pi * tvec(int(1.0 * SR)) / 1.0) ** 2
    place(sfx, arrow * 0.05, T("s_clue_b", 1.6))                       # the axis draws
    air = lp(rng.normal(0, 1, int(3.0 * SR)), 700) * 0.06
    place(sfx, air * np.sin(np.pi * tvec(len(air)) / 3.0), T("s_clue_c", 0.8))   # fog
    for u0 in (2.0, 2.4):
        place(sfx, pop(), T("s_clue_c", u0), 0.22)
    for k_ in range(2):
        place(sfx, pop(), T("s_clue_d", 1.3 + 0.15 * k_), 0.22)
    for j in range(8):
        place(sfx, tick(), T("s_clue_d", 2.0 + 0.06 * j), 0.08)
    for j in range(9):
        place(sfx, tick(), T("s_clue_d", 2.7 + 0.9 * j / 9), 0.1)     # one tick per degree
    place(sfx, pop(), T("s_clue_d", 3.6), 0.3)                         # "? 39"
    for u0 in (0.0, 0.3):                                      # PAUSE AND GUESS (the first slam on the cut itself)
        place(sfx, impact(0.4), T("s_pause", u0), 0.35)
    for j, t_ in enumerate(np.arange(29.5, 33.0, 0.5)):        # the clock
        place(sfx, knock(), t_, 0.18 if j % 2 else 0.25)
    for u0, fq in ((0.6, 880.0), (1.6, 880.0), (2.6, 880.0), (3.6, 1320.0)):
        place(sfx, beep(fq), T("s_pause", u0), 0.3)
    place(sfx, riser(0.55), 32.45, 0.5)
    pen = hp(rng.normal(0, 1, int(0.8 * SR)), 3000) * 0.05      # the reveal
    place(sfx, pen * np.sin(np.pi * tvec(len(pen)) / 0.8), T("s_reveal", 0.05))
    place(sfx, pop(), T("s_reveal", 0.45), 0.3)
    for u0 in (0.9, 1.8):
        place(sfx, whoosh(0.8, 200, 3000, 0.7), T("s_reveal", u0), 0.35)
    place(sfx, pop(), T("s_reveal", 2.35), 0.35)
    place(sfx, impact(0.6), T("s_reveal", 2.7), 0.5)
    for j in range(5):
        place(sfx, pop(), T("s_reveal", 3.2 + 0.85 * (0.2 + 0.07 * j)), 0.15)
    place(sfx, whoosh(0.6, 200, 2500, 0.8), T("s_reveal", 4.4), 0.3)
    for k_ in range(3):
        place(sfx, tick(), T("s_reveal", 5.1 + 0.4 * k_), 0.12)
    for u0 in (0.05, 0.35):                                    # the close
        place(sfx, impact(0.4), T("s_cta", u0), 0.35)
    for k_ in range(4):
        place(sfx, pop(), T("s_cta", 0.8 + 0.12 * k_), 0.22)
    place(sfx, pop(), T("s_cta", 1.95), 0.3)

    ir_n = int(1.5 * SR)
    irL = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.42); irR = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.42)
    irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
    vL = fftconvolve(verb + sfx * 0.25, irL)[:N] * 0.6
    vR = fftconvolve(verb + sfx * 0.25, irR)[:N] * 0.6
    out = np.stack([hp(drums * 0.9 + mL + sfx + vL, 28), hp(drums * 0.9 + mR + sfx + vR, 28)], 1)
    a = ident_audio()
    out[:len(a)] += a
    fade = np.ones(N); fn = int(0.5 * SR); fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
    out *= fade[:, None]
    out = np.tanh(out * 1.4) / np.tanh(1.4)
    return out / (np.max(np.abs(out)) / 0.89)


if __name__ == "__main__":
    a = build()
    path = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/mendo_gtr_audio.wav"
    wavfile.write(path, SR, (a * 32767).astype(np.int16))
    print(f"wrote {path}: {len(a) / SR:.2f}s, peak {20 * np.log10(np.abs(a).max()):.2f} dBFS")
