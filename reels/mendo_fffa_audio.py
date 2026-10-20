"""Score and sound design for FIVE FASCINATING FACTS ABOUT MENDOCINO (36 s, 48 kHz stereo). Original, synthesized in code
(reels/reel_audio.py plus the instruments below): no samples, no library music, so no licensing question.

120 BPM in A minor, one bar = 2 s, so the picture's scenes are the music's bars. THE SHAPE (a caper's):
  0-0.5   a vinyl-crackle bed and a low drone: the hook card is almost silent, so the montage lands as a hit
  0.5-2   six cuts on 16ths: shutter click + kick/snare + a stab on each; the snare rolls
  2-4     FIVE FACTS. ONE COUNTY.: brass stabs, five rising ticks, a riser into the whip
  4-8     the groove (stop-time breakbeat: kick, ghost snares, hats, a walking bass, fuzz-guitar stabs); STOPS dead on the freeze
          (4.5-5.0: scratch + shutter, nothing else) and slams back on the title
  8-14    full groove; four rising coins for the four lit tiles; stop-time again before UNDER 1%
  14-20   COLD: the groove thins to a kick, a pad and ice bells while the cold air pools; it returns full when the vines light
  20-26   warm: a pad swell and a glitch burst into the sunrise; the music drops before the stamp, and the stamp lands on it
  26-32   full groove; sonar pings for the three towns; marimba notes up the heat ladder
  32-36   five recap hits (one a beat), the end-card slam, then a TAPE STOP on the smash cut: the tail is the same crackle the
          Reel opened on, so the replay loops
Every event time is read from the picture (mendo_fffa_reel.T and its cut lists), so a timeline change cannot strand a sound.
Where a cut has an impact, the impact REPLACES the kick on that beat (the GTR lesson: stacked low end overshoots true peak
after AAC encoding). Checked by measurement, not by ear (I cannot listen to audio): loudness and true peak of the encoded file.
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
import mendo_fffa_reel as R  # noqa: E402

T = R.T
DUR = R.SCENE_TABLE[-1][0] + R.SCENE_TABLE[-1][1]
N = int(SR * DUR)
STEP = BEAT / 4                                            # a 16th: 0.125 s
CHORD = {"A": (55.0, (220.0, 261.63, 329.63)), "F": (43.65, (174.61, 220.0, 261.63)), "E": (41.2, (164.81, 207.65, 246.94))}
CYCLE = ["A", "A", "F", "E"]                               # a bar each: Am Am F E (the E major pulls back to Am)


# ------------------------------------------------------------------ the new instruments
def snare():
    n = int(0.26 * SR); t = tvec(n)
    nz = bp(rng.normal(0, 1, n), 1500, 8500) * np.exp(-t / 0.075)
    tone = np.sin(2 * np.pi * 188 * t) * np.exp(-t / 0.05) * 0.5
    return (nz * 0.6 + tone) * 0.85


def ghost():
    return snare()[:int(0.12 * SR)] * np.linspace(1, 0.2, int(0.12 * SR)) * 0.35


def tamb():
    n = int(0.09 * SR); t = tvec(n)
    return hp(rng.normal(0, 1, n), 6000, 2) * np.exp(-t / 0.03) * 0.28


def tick_f(freq, amp=1.0):
    n = int(0.014 * SR); t = tvec(n)
    return np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.0035) * amp


def shutter():
    """A camera: two clicks (mirror, shutter) and a small thunk."""
    n = int(0.16 * SR); out = np.zeros(n)
    for d, g in ((0.0, 1.0), (0.05, 0.8)):
        i = int(d * SR); m = int(0.012 * SR)
        out[i:i + m] += bp(rng.normal(0, 1, m), 1800, 7500) * np.exp(-tvec(m) / 0.0035) * g
    out[:int(0.03 * SR)] += np.sin(2 * np.pi * 130 * tvec(int(0.03 * SR))) * np.exp(-tvec(int(0.03 * SR)) / 0.01) * 0.5
    return out * 0.9


def scratch(dur=0.32):
    """A record scratch: a saw whose pitch is dragged back and forth through a band-pass."""
    n = int(dur * SR); t = tvec(n)
    f = 320 + 260 * np.sin(2 * np.pi * 7.0 * t + 0.6) * np.exp(-t / 0.5) - 120 * t / dur
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.33 * np.sin(3 * ph)) * 0.4
    nz = bp(rng.normal(0, 1, n), 800, 5200) * 0.5
    env = np.minimum(1, t / 0.01) * np.exp(-t / (dur * 0.7))
    return bp(tone + nz, 500, 6000) * env * 0.9


def tape_stop(freqs, dur=0.5):
    """The tape stops: a chord whose pitch falls to nothing."""
    n = int(dur * SR); t = tvec(n)
    out = np.zeros(n)
    for fq in freqs:
        f = fq * np.exp(-t / (dur * 0.34))
        ph = 2 * np.pi * np.cumsum(f) / SR
        out += np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
    return lp(out, 3000) * np.exp(-t / (dur * 0.6)) * 0.30


def stab(freqs, dur=0.3, bright=2800):
    """A brass-ish stab: stacked saws with a fast attack and a quick decay."""
    n = int(dur * SR); t = tvec(n)
    out = np.zeros(n)
    for fq in freqs:
        out += saw(fq, n, harmonics=10) + saw(fq, n, harmonics=10, detune=9)
    env = np.minimum(1, t / 0.006) * np.exp(-t / (dur * 0.42))
    return lp(out, bright) * env * 0.16


def fuzz(freqs, dur=0.3):
    """A fuzz-guitar chord: plucked strings pushed through a clipper."""
    out = sum(pluck(fq, dur, 1.4) for fq in freqs)
    out = np.tanh(out * 3.2)
    return lp(hp(out, 140), 3400) * 0.30


def bass_note(freq, dur=0.3):
    n = int(dur * SR); t = tvec(n)
    out = np.sin(2 * np.pi * freq * t) + 0.45 * np.sin(2 * np.pi * freq * 2 * t) * np.exp(-t / 0.15) + 0.2 * saw(freq, n, harmonics=6)
    return lp(out, 420) * np.minimum(1, t / 0.004) * np.exp(-t / (dur * 0.8)) * 0.62


def pad(freqs, dur):
    n = int(dur * SR); t = tvec(n)
    out = np.zeros(n)
    for fq in freqs:
        for dt in (-0.4, 0.4):
            out += np.sin(2 * np.pi * fq * (1 + dt * 0.004) * t)
    env = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.5)
    trem = 0.85 + 0.15 * np.sin(2 * np.pi * 5.2 * t)
    return lp(out, 1800) * env * trem * 0.07


def bell(fq, dur=1.2, amp=1.0):
    n = int(dur * SR); t = tvec(n)
    return amp * sum(a * np.sin(2 * np.pi * fq * h * t) * np.exp(-t / d) for h, a, d in ((1, 1.0, 0.7), (2.76, 0.3, 0.35), (5.4, 0.12, 0.18))) * 0.3


def sonar(fq):
    n = int(0.9 * SR); t = tvec(n)
    p = np.sin(2 * np.pi * fq * t) * np.exp(-t / 0.22) * np.minimum(1, t / 0.003)
    for d, g in ((0.18, 0.4), (0.36, 0.18)):
        i = int(d * SR); p[i:] += p[:n - i] * g
    return p * 0.45


def marimba(fq):
    n = int(0.4 * SR); t = tvec(n)
    return (np.sin(2 * np.pi * fq * t) * np.exp(-t / 0.09) + 0.3 * np.sin(2 * np.pi * fq * 4 * t) * np.exp(-t / 0.03)) * 0.55


def fizz(dur=0.12):
    n = int(dur * SR); t = tvec(n)
    return hp(rng.normal(0, 1, n), 6500, 2) * np.exp(-t / (dur * 0.35)) * 0.12


def glitch_burst(dur=0.22):
    n = int(dur * SR)
    nz = np.round(rng.normal(0, 1, n) * 3) / 3                       # bit-crushed
    gate = (np.sin(2 * np.pi * 38 * tvec(n)) > -0.2).astype(float) * (rng.random(n // 600 + 1).repeat(600)[:n] > 0.35)
    return bp(nz * gate, 400, 9000) * np.exp(-tvec(n) / (dur * 0.7)) * 0.6


def revcym(dur=0.8):
    n = int(dur * SR); t = tvec(n)
    return hp(rng.normal(0, 1, n), 5000, 2) * (t / dur) ** 2.4 * 0.5


def crash():
    n = int(1.6 * SR); t = tvec(n)
    return hp(rng.normal(0, 1, n), 4200, 2) * np.exp(-t / 0.55) * 0.4


def stamp():
    n = int(0.5 * SR); t = tvec(n)
    thud = np.sin(2 * np.pi * (70 + 60 * np.exp(-t / 0.05)) * t) * np.exp(-t / 0.12)
    slap = bp(rng.normal(0, 1, n), 700, 4500) * np.exp(-t / 0.03) * 0.6
    return (thud + slap) * 0.9


def crackle_bed(dur):
    n = int(dur * SR); bed = np.zeros(n)
    for pos in rng.integers(0, n - 200, int(dur * 38)):
        m = int(rng.integers(8, 90))
        bed[pos:pos + m] += rng.normal(0, 1, m) * np.exp(-np.arange(m) / (m * 0.3)) * rng.uniform(0.2, 1.0)
    return hp(bed, 900) * 0.10 + hp(rng.normal(0, 1, n), 5000) * 0.004


# ------------------------------------------------------------------ the arrangement
BREAKS = [(4.5, 5.0), (11.5, 12.0), (22.5, 23.0)]                    # stop-time: the groove is cut dead
SECTIONS = [(4.0, 11.5, "full"), (12.0, 13.5, "full"), (14.0, 17.5, "cold"), (18.0, 19.5, "full"),
            (20.0, 22.5, "light"), (23.0, 25.5, "full"), (26.0, 31.5, "full")]
ROLLS = [(3.5, 4.0), (13.5, 14.0), (17.5, 18.0), (19.5, 20.0), (25.5, 26.0), (31.5, 31.94)]
LEAD = 0.006                                                         # an impact's peak lands ~9 ms after its start
CUT_IMPACTS = (4.0, 8.0, 14.0, 20.0, 26.0)                           # an impact here REPLACES the kick on the beat


def build():
    drums, bassb, gtr, keys, sfx = (np.zeros(N) for _ in range(5))
    pan_keys = np.zeros(N)
    K, S, G, H_, HO, TB = kick(), snare(), ghost(), hat(), hat(open_=True), tamb()

    def at_cut(t):
        return any(abs(t - c) < 1e-3 for c in CUT_IMPACTS)

    # ---- the groove, bar by bar
    for (a, b, kind) in SECTIONS:
        bar0 = a
        while bar0 < b - 1e-6:
            ci = int(bar0 // 2) % 4
            root, chord = CHORD[CYCLE[ci]]
            for st in range(16):
                t = bar0 + st * STEP + (0.012 if st % 2 else 0.0)                 # a little swing on the off 16ths
                if t >= b or any(x <= t < y for x, y in BREAKS):
                    continue
                if kind == "full":
                    if st in (0, 7, 10) and not at_cut(t) and not (st == 0 and False):
                        place(drums, K, t, 0.80 if st == 0 else 0.62)
                    if st in (4, 12):
                        place(drums, S, t, 0.78)
                    if st in (7, 15, 9):
                        place(drums, G, t, 0.55)
                    if st % 2 == 0:
                        place(drums, H_, t, 0.30 if st % 4 else 0.38)
                    if st == 14:
                        place(drums, HO, t, 0.30)
                    if st % 2 == 0:
                        place(drums, TB, t, 0.5)
                    for s0, mult, d in ((0, 1, 0.30), (3, 1, 0.18), (6, 2, 0.18), (8, 1, 0.30), (11, 1.5, 0.18), (14, 1.335 if CYCLE[ci] == "A" else 1, 0.18)):
                        if st == s0:
                            place(bassb, bass_note(root * mult * 2 if CYCLE[ci] == "E" else root * mult * 2, d), t, 0.9)
                    if st in (6, 14):
                        place(gtr, fuzz(chord, 0.26), t, 0.7)
                elif kind == "cold":
                    if st == 0 and not at_cut(t):
                        place(drums, K, t, 0.62)
                    if st == 8:
                        place(drums, K, t, 0.30)
                    if st in (0, 4, 8, 12):
                        place(drums, H_, t, 0.18)
                    if st == 0:
                        place(bassb, bass_note(root * 2, 0.9), t, 0.7)
                elif kind == "light":
                    if st in (0, 10) and not at_cut(t):
                        place(drums, K, t, 0.66)
                    if st in (4, 12):
                        place(drums, knock(), t, 0.7)
                    if st % 2 == 0:
                        place(drums, H_, t, 0.2)
                    if st in (0, 8):
                        place(bassb, bass_note(root * 2, 0.55), t, 0.8)
            bar0 += 2.0
    # ---- snare rolls into the cuts (16ths, crescendo)
    for a, b in ROLLS:
        n_ = int((b - a) / STEP)
        for j in range(n_):
            place(drums, S, a + j * STEP, 0.20 + 0.42 * (j / max(n_ - 1, 1)))
    # ---- pads: the warm and the cold
    for a, b, chord in ((14.0, 18.0, (110.0, 220.0, 261.63, 329.63)), (20.0, 22.5, (174.61, 220.0, 261.63, 349.23)),
                        (23.0, 26.0, (220.0, 261.63, 329.63, 440.0)), (26.0, 32.0, (110.0, 220.0, 261.63))):
        place(keys, pad(chord, b - a), a, 0.9)
    place(keys, pad((55.0, 110.0), 4.0), 0.0, 0.8)                                        # the opening drone
    place(sfx, crackle_bed(4.0), 0.0, 1.0)
    place(sfx, crackle_bed(1.0), 35.0, 0.9)                                              # the same crackle returns: the loop

    # ---- TITLE
    place(sfx, whoosh(0.5, 200, 3000, 0.8), 0.0 + 0.0, 0.18)                             # the sheen
    for k_ in range(6):                                                                  # the six montage cuts, on 16ths
        t = 0.5 + 0.25 * k_
        place(sfx, shutter(), t, 0.55)
        place(drums, K if k_ % 2 == 0 else S, t, 0.8)
        if k_ % 2 == 0:
            place(keys, stab(CHORD["A"][1] if k_ == 0 else (CHORD["F"][1] if k_ == 2 else CHORD["E"][1]), 0.22), t, 0.9)
    place(sfx, crash(), 2.0, 0.5)
    place(sfx, impact(0.7), 2.0, 0.55)
    place(keys, stab((110.0, 220.0, 261.63, 329.63, 440.0), 0.5), 2.0, 1.0)
    place(sfx, pop(), 2.05, 0.3)                                                          # the icon
    place(sfx, impact(0.3), T("s_title", 2.15), 0.3)
    place(sfx, impact(0.35), T("s_title", 2.65), 0.4)
    place(keys, stab(CHORD["F"][1], 0.3), T("s_title", 2.65), 0.8)
    place(sfx, whoosh(0.7, 300, 5000, 0.6), T("s_title", 2.5), 0.22)
    for i, fq in enumerate((880.0, 1046.5, 1318.5, 1760.0, 2093.0)):                      # the five ticks, rising
        place(sfx, marimba(fq), T("s_title", 2.35 + 0.18 * i), 0.5)
    place(sfx, riser(0.5), 3.5, 0.6)
    # ---- the cuts
    place(sfx, whoosh(0.5, 300, 6000, 0.7), 4.0 - 0.25, 0.32)
    place(sfx, impact(1.0), 4.0 - LEAD, 0.66)
    place(sfx, whoosh(0.5, 300, 6000, 0.7), 26.0 - 0.25, 0.32)
    place(sfx, impact(0.9), 26.0 - LEAD, 0.64)
    place(sfx, impact(0.9), 8.0 - LEAD, 0.64)
    place(sfx, whoosh(0.5, 200, 4500, 0.6), 14.0 - 0.25, 0.34)
    place(sfx, impact(0.7), 14.0 - LEAD, 0.5)
    place(sfx, glitch_burst(0.26), 20.0 - 0.05, 0.6)
    place(sfx, impact(0.7), 20.0 - LEAD, 0.55)
    # ---- FACT 1: the freeze
    for t in np.arange(4.0, 8.0, 0.21):
        place(sfx, fizz(), t + rng.uniform(0, 0.1), rng.uniform(0.3, 0.7))
    place(sfx, scratch(0.34), T("s_f1", 0.5), 0.75)
    place(sfx, shutter(), T("s_f1", 0.5), 0.8)
    place(sfx, pop(), T("s_f1", 0.75), 0.3)
    for j in range(5):
        place(sfx, tick(), T("s_f1", 0.80 + 0.06 * j), 0.1)
    place(keys, stab(CHORD["A"][1], 0.3), T("s_f1", 1.0), 0.9)                            # the title slams: the groove returns on it
    place(drums, clap(), T("s_f1", 1.0), 0.8)
    place(sfx, whoosh(0.5, 400, 5000, 0.7), T("s_f1", 1.5), 0.2)
    place(sfx, pop(), T("s_f1", 1.3), 0.3)
    for j in range(18):                                                                    # the 1982 counter
        place(sfx, tick_f(1800 + 70 * j), T("s_f1", 1.3 + 0.8 * j / 18), 0.11)
    place(sfx, pop(), T("s_f1", 2.5), 0.28)
    # ---- FACT 2: the tiles
    place(drums, clap(), T("s_f2", 0.1), 0.7)
    place(sfx, whoosh(0.9, 400, 6500, 0.8), T("s_f2", 0.3), 0.3)
    place(sfx, whoosh(1.0, 500, 7500, 0.8), T("s_f2", 0.5), 0.26)
    for j in range(8):
        place(sfx, tick(), T("s_f2", 0.28 + 0.08 * j), 0.08)
    for k_, fq in enumerate((880.0, 1046.5, 1318.5, 1760.0)):                              # four tiles, four rising coins
        place(sfx, marimba(fq), T("s_f2", 1.7 + 0.22 * k_), 0.8)
        place(sfx, pop(), T("s_f2", 1.7 + 0.22 * k_), 0.25)
    for j in range(10):
        place(sfx, tick_f(2000 + 90 * j), T("s_f2", 1.7 + 1.0 * j / 10), 0.1)
    place(sfx, pop(), T("s_f2", 2.6), 0.25)
    place(sfx, revcym(0.7), 11.0, 0.5)                                                      # into the county
    place(sfx, scratch(0.3), 11.5, 0.7)
    place(sfx, impact(0.4), 11.5, 0.35)
    place(drums, clap(), T("s_f2", 3.9), 0.8)
    place(keys, stab(CHORD["A"][1], 0.3), 12.0, 0.9)
    place(sfx, marimba(2093.0), T("s_f2", 4.2), 0.8)
    place(sfx, pop(), T("s_f2", 4.4), 0.25)
    # ---- FACT 3: cold
    rng_b = np.random.default_rng(31)
    for t in np.arange(14.3, 18.0, 0.37):                                                  # ice bells twinkle
        place(sfx, bell(float(rng_b.choice([1760.0, 2093.0, 2637.0, 3136.0])), 0.9, 0.5), t, rng_b.uniform(0.35, 0.7))
    place(sfx, lp(rng.normal(0, 1, int(2.3 * SR)), 900) * np.linspace(0, 1, int(2.3 * SR)) ** 2 * 0.5, T("s_f3", 0.9), 0.9)
    place(sfx, bell(2637.0, 1.4, 1.0), T("s_f3", 1.7), 0.7)
    place(sfx, pop(), T("s_f3", 1.7), 0.25)
    place(sfx, revcym(0.5), 17.5, 0.5)
    for k_, fq in enumerate((440.0, 523.25, 659.25, 880.0)):                               # the vines wake: a green arpeggio
        place(sfx, marimba(fq), T("s_f3", 3.6 + 0.1 * k_), 0.6)
    place(sfx, pop(), T("s_f3", 3.7), 0.25)
    place(drums, clap(), 18.0, 0.7)
    # ---- FACT 4: sunrise
    for k_ in range(4):
        place(sfx, knock(), T("s_f4", 0.2 + 0.12 * k_), 0.5)
    for j, t in enumerate(np.arange(20.25, 22.5, STEP * 2)):                               # a sparkling arpeggio, A minor pentatonic
        place(sfx, marimba((440.0, 523.25, 587.33, 659.25, 783.99)[j % 5] * 2), t, 0.20)
    place(sfx, whoosh(0.8, 300, 6000, 0.9), T("s_f4", 0.9), 0.28)
    for j in range(8):
        place(sfx, tick(), T("s_f4", 0.9 + 0.09 * j), 0.08)
    place(sfx, pop(), T("s_f4", 1.2), 0.28)
    place(sfx, pop(), T("s_f4", 1.5), 0.28)
    place(sfx, revcym(0.5), 22.5, 0.55)
    place(sfx, scratch(0.3), 22.5, 0.5)
    place(sfx, stamp(), T("s_f4", 3.0), 0.9)                                               # the stamp lands on the drop
    place(sfx, crash(), T("s_f4", 3.0), 0.5)
    place(drums, K, T("s_f4", 3.0), 0.8)
    place(keys, stab(CHORD["A"][1], 0.4), T("s_f4", 3.0), 1.0)
    # ---- FACT 5: the map
    place(drums, clap(), T("s_f5", 0.1), 0.6)
    for i, fq in enumerate((440.0, 523.25, 587.33, 659.25, 783.99)):                       # the ladder, up
        place(sfx, marimba(fq), T("s_f5", 0.9 + 0.08 * i), 0.55)
    for u0, fq in ((1.0, 659.25), (1.9, 880.0), (2.9, 1046.5)):                            # Philo, Boonville, Ukiah: sonar pings
        place(sfx, sonar(fq), T("s_f5", u0), 0.85)
        place(sfx, knock(), T("s_f5", u0 + 0.25), 0.4)
    for j in range(12):
        place(sfx, tick(), T("s_f5", 1.7 + 0.05 * j), 0.1)
    place(sfx, pop(), T("s_f5", 2.3), 0.3)
    place(drums, clap(), T("s_f5", 3.5), 0.8)
    place(keys, stab(CHORD["A"][1], 0.35), T("s_f5", 3.5), 0.9)
    place(sfx, pop(), T("s_f5", 4.5), 0.25)
    place(sfx, riser(0.45), 31.5, 0.5)
    # ---- OUTRO: the dip, five recap hits, the end card, the tape stop
    for k_ in range(5):
        t = 32.0 + 0.5 * k_
        place(sfx, shutter(), t, 0.5)
        if not at_cut(t):
            place(drums, K, t, 0.85)
        if k_ % 2 == 1:
            place(drums, clap(), t, 0.8)
        place(keys, stab(CHORD[("A", "F", "A", "E", "A")[k_]][1], 0.3), t, 0.95)
    place(sfx, impact(0.9), 32.0 - LEAD, 0.6)
    place(drums, S, 34.25, 0.5)
    place(drums, S, 34.375, 0.7)
    t_end = T("s_outro", 2.5)
    place(sfx, impact(1.0), t_end - LEAD, 0.66)
    place(sfx, crash(), t_end, 0.55)
    place(keys, stab((110.0, 220.0, 261.63, 329.63, 440.0, 523.25), 0.8), t_end, 1.1)
    place(sfx, pop(), T("s_outro", 3.0), 0.28)
    place(sfx, tape_stop((220.0, 261.63, 329.63, 110.0), 0.6), 35.38, 1.0)                  # the smash cut back to frame 0

    # ---- the sidechain: a duck on every kick, so the stabs and bass breathe around it
    duck = np.ones(N)
    for t in np.arange(4.0, 32.0, BEAT):
        i = int(t * SR); m = min(N, i + int(0.16 * SR))
        duck[i:m] = np.minimum(duck[i:m], 0.72 + 0.28 * np.linspace(0, 1, m - i))
    keys *= duck
    bassb *= duck
    # ---- the silence around the dip, then the slam
    dip = np.ones(N)
    dip[int(31.94 * SR):int(32.0 * SR)] = 0.0
    for c in (4.0, 8.0, 14.0, 20.0, 26.0, 34.5):                       # a 50 ms hole before each hit: the cut slams into near-silence
        dip[int((c - 0.056) * SR):int((c - LEAD) * SR)] = 0.10
    dip = np.convolve(dip, np.ones(int(0.004 * SR)) / int(0.004 * SR), "same")      # 4 ms ramps: a square-edged gate makes the AAC encoder ring (+1.7 dBTP)
    # ---- reverb send, stereo
    ir_n = int(1.2 * SR)
    irL = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.34); irR = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.34)
    irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
    send = keys * 0.7 + gtr * 0.4 + sfx * 0.22
    vL = fftconvolve(send, irL)[:N] * 0.55
    vR = fftconvolve(send, irR)[:N] * 0.55
    dl = int(0.011 * SR)
    gL = gtr * 0.8; gR = np.concatenate([np.zeros(dl), gtr])[:N] * 0.55
    kL = keys * 0.75; kR = keys * 0.95
    L = hp(drums * 0.92 + bassb * 0.95 + gL + kL + sfx + vL, 28) * dip
    Rr = hp(drums * 0.92 + bassb * 0.95 + gR + kR + sfx + vR, 28) * dip
    out = np.stack([L, Rr], 1)
    out = np.tanh(out * 1.35) / np.tanh(1.35)
    return out / (np.max(np.abs(out)) / 0.89)


if __name__ == "__main__":
    a = build()
    path = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/mendo_fffa_audio.wav"
    wavfile.write(path, SR, (a * 32767).astype(np.int16))
    print(f"wrote {path}: {len(a) / SR:.2f}s, peak {20 * np.log10(np.abs(a).max()):.2f} dBFS")
