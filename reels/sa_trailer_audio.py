"""Score for the Wines of South Africa trailer Reel (30 s), VERSION 2 (Steve): quiet acoustic piano, and almost none of the whimsical sound effects.
Original, synthesized in code, so no licensing question. The drums, bass, pad, plucks, ticks, pops, claps, hats, risers and impacts of version 1 are gone.
  The piano: struck strings (partials with a little inharmonicity, a hammer-position comb, a fast-then-slow decay that is shorter for the high notes), two slightly detuned strings per note
  (the soft shimmer of real unisons), a felt-hammer thump, a soft top end that opens a little with touch, and a small room (about 2 s of reverb).
  The music: G major, one chord per 2-second bar (G, D/F#, Em7, Cmaj7, G, D, Em, Cadd9, G/B, Am7, D, G, Em, Cmaj7, G), so every picture cut (the scene starts are all bar lines) lands on a
  new chord. A slow two-note melody on top, a low root underneath, and a rolling broken-chord figure in eighth notes between, all played quietly (velocity 0.2 to 0.45).
  It starts on frame 1 (the Reel spec: already moving), and the last chord rings out under the closing fade, so the Reel loops back into its own first chord (G to G).
  The only effect left: a very soft, low page-turn swish at each of the six picture cuts, about 25 dB under the piano's peaks, to anchor the cut. Nothing else.
Level: quiet but present, about -16 LUFS integrated (version 1 was -14), true peak under -2 dBFS. Checked by measurement, not by ear. Instagram's audio library can replace it at upload.
Usage: python3 sa_trailer_audio.py audio.wav [gain_dB]
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_audio as A                                    # noqa: E402
from reel_audio import SR, tvec, lp                       # noqa: E402
import sa_trailer_reel as R                               # noqa: E402

DUR, BAR, EIGHTH = R.DUR, 2.0, 0.25
rng = np.random.default_rng(21)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def piano(m, dur, vel):
    """One struck note, midi number m, ringing for dur seconds, touch vel (0-1). Mono, peak about 0.55*vel."""
    f = hz(m)
    n = int(dur * SR)
    t = tvec(n)
    B = min(0.0016, 0.00030 * (f / 110.0) ** 1.4)                       # string stiffness: the upper partials run a little sharp
    tau0 = float(np.clip(9.0 * (110.0 / f) ** 0.55, 1.3, 10.0))         # the slow decay: long for low notes, short for high
    out = np.zeros(n)
    k = 0
    while True:
        k += 1
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > SR / 2 - 900 or k > 30:
            break
        a = k ** -(1.45 - 0.5 * vel) * (abs(np.sin(np.pi * k * 0.118)) + 0.18)     # touch opens the top; the hammer strikes about an eighth of the way along
        tk = tau0 / (1.0 + 0.55 * (k - 1) ** 0.85)
        env = 0.55 * np.exp(-t / (0.22 * tk + 0.05)) + 0.45 * np.exp(-t / tk)         # fast stage then slow stage
        w = np.sin(2 * np.pi * fk * t) + 0.8 * np.sin(2 * np.pi * fk * (1 + 0.00022 + 0.00005 * k) * t + 0.7)     # two strings, slightly detuned
        out += a * env * w
    out *= np.clip(t / 0.004, 0, 1)                                       # a felt hammer: a 4 ms attack, not a click
    out = out / max(np.max(np.abs(out)), 1e-9) * 0.55 * vel
    nn = int(0.06 * SR)
    th = lp(rng.normal(0, 1, nn) * np.exp(-np.arange(nn) / SR / 0.009), 1500)
    out[:nn] += th * 0.10 * vel                                           # the thump of the hammer on the string
    out = lp(out, 2600 + 4400 * vel)                                      # a soft top end
    out *= np.clip((dur - t) / 0.30, 0, 1)
    return out


# one chord per 2-second bar: (arpeggio notes low to high, melody [(offset s, midi, duration s)])
BARS = [
    ([55, 62, 67, 71], [(0.0, 71, 1.2), (1.0, 74, 1.4)]),                  # 0  G
    ([54, 62, 66, 69], [(0.0, 69, 1.2), (1.0, 66, 1.4)]),                  # 1  D/F#
    ([52, 59, 64, 67], [(0.0, 67, 1.2), (1.0, 71, 1.4)]),                  # 2  Em7
    ([48, 55, 59, 64], [(0.0, 72, 1.2), (1.0, 71, 1.4)]),                  # 3  Cmaj7
    ([55, 62, 67, 71], [(0.0, 74, 1.2), (1.0, 71, 1.4)]),                  # 4  G
    ([50, 57, 62, 66], [(0.0, 69, 1.2), (1.0, 74, 1.4)]),                  # 5  D
    ([52, 59, 64, 67], [(0.0, 76, 1.2), (1.0, 74, 1.4)]),                  # 6  Em
    ([48, 55, 62, 64], [(0.0, 72, 1.2), (1.0, 74, 1.4)]),                  # 7  Cadd9
    ([47, 55, 62, 67], [(0.0, 71, 1.2), (1.0, 74, 1.4)]),                  # 8  G/B
    ([57, 64, 67, 72], [(0.0, 72, 1.2), (1.0, 76, 1.4)]),                  # 9  Am7
    ([50, 57, 62, 66], [(0.0, 74, 1.2), (1.0, 69, 1.4)]),                  # 10 D
    ([55, 62, 67, 71], [(0.0, 71, 1.2), (1.0, 67, 1.4)]),                  # 11 G
    ([52, 59, 64, 67], [(0.0, 67, 1.2), (1.0, 71, 1.4)]),                  # 12 Em
    ([48, 55, 59, 64], [(0.0, 72, 1.2), (1.0, 71, 1.4)]),                  # 13 Cmaj7
    ([55, 62, 67, 71], [(0.0, 74, 3.2)]),                                  # 14 G: the last chord rings out
]
FIGURE = [0, 1, 2, 3, 2, 1, 2, 1]                                         # the rolling broken chord, eighth notes


def place_st(L, Rb, sig, t, gain, pan):
    """Place a mono note into the stereo buses (equal-power pan, -1 left .. +1 right)."""
    th = (pan + 1) * np.pi / 4
    A.place(L, sig, t, gain * np.cos(th))
    A.place(Rb, sig, t, gain * np.sin(th))


def reverb(x, rt60=2.1, predelay=0.018, wet=0.20):
    """A small room: exponentially decaying, softened noise, decorrelated left and right."""
    n = int(rt60 * 1.25 * SR)
    t = np.arange(n) / SR
    ir = []
    for _ in range(2):
        r = rng.normal(0, 1, n) * np.exp(-t * 6.9 / rt60)
        ir.append(lp(r, 5200))
    out = []
    for ch, irc in zip(x, ir):
        irc = np.concatenate([np.zeros(int(predelay * SR)), irc])
        irc /= np.sqrt(np.sum(irc ** 2))
        out.append(fftconvolve(ch, irc)[:len(ch)])
    return [c * (1 - wet * 0.5) + o * wet * 1.6 for c, o in zip(x, out)]


def build():
    nS = int((DUR + 3.0) * SR)
    L, Rb = np.zeros(nS), np.zeros(nS)
    for bar, (arp, mel) in enumerate(BARS):
        t0 = bar * BAR
        j = lambda: float(rng.uniform(-0.007, 0.007))                      # a human's timing
        place_st(L, Rb, piano(arp[0] - 12, 2.8 if bar < 14 else 6.0, 0.38), max(t0 + 0.02, 0.02), 0.9, -0.30)         # the low root: on frame 1 for bar 0
        for e in range(8):
            vel = (0.27 if e == 0 else 0.21 if e % 2 == 0 else 0.185) * float(rng.uniform(0.93, 1.07))
            m = arp[FIGURE[e]]
            place_st(L, Rb, piano(m, 1.6, vel), max(t0 + e * EIGHTH + (j() if e else 0.0) + 0.02, 0.02), 1.0, -0.2 + 0.5 * (m - 48) / 24.0)
        for off, m, d in mel:
            place_st(L, Rb, piano(m, d + 1.6, 0.44), max(t0 + off + j() + 0.02, 0.02), 1.0, 0.25)
    # the only effect left: a very soft, low page-turn swish at each of the six cuts
    sw = A.lp(A.hp(A.whoosh(0.5, 200, 2400, 0.5), 150), 2200)
    for s, d, n, _ in R.SCENE_TABLE:
        if n != "hook":
            place_st(L, Rb, sw, s + 0.02, 0.06, 0.0)
    L, Rb = reverb([L, Rb])
    t = np.arange(nS) / SR
    fade = np.clip((DUR - t) / 1.6, 0, 1)
    fade = np.where(t >= DUR, 0.0, 0.5 - 0.5 * np.cos(np.pi * fade))
    return L[:int(DUR * SR)] * fade[:int(DUR * SR)], Rb[:int(DUR * SR)] * fade[:int(DUR * SR)]


def write(path, gain_db=0.0):
    L, Rb = build()
    g = 10 ** (gain_db / 20)
    st = np.stack([L, Rb], 1) * g
    peak = np.max(np.abs(st))
    if peak > 0.9:                                                         # a soft ceiling only; the piano's own dynamics are left alone
        st = np.tanh(st * 1.1) / np.tanh(1.1)
    wavfile.write(path, SR, (np.clip(st, -1, 1) * 32767).astype(np.int16))


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/sa_out/audio.wav", float(sys.argv[2]) if len(sys.argv) > 2 else 0.0)
    print("audio written")
