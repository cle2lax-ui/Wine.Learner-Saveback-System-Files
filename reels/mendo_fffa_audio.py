"""Score and sound design for FIVE FASCINATING FACTS ABOUT MENDOCINO (40 s, 48 kHz stereo). v3: a ROCK score.

Original and synthesized in code (reels/reel_audio.py plus the instruments below): no samples, no library music, so no licensing
question. 120 BPM in A minor; one bar = 2 s, so the picture's scenes are the music's bars. Steve: "more cool, less whimsical;
a rock beat, horn hits, driving drums and electric guitar color." So: a straight backbeat (snare on 2 and 4, driving 8th hats),
an 8th-note bass, double-tracked overdriven power-chord riffs with palm-muted chugs, a horn section for the punctuation and the
big hits, toms in the fills. The v2 marimba/bell/sonar/pop sounds are gone (the lit tiles are ascending horn stabs).

THE SHAPE:
  0-2    the opening bumper: crash + horn hit + an open A5 ring, then palm-muted pedal 8ths build and a snare/tom roll
  2-4    the montage on 16ths: kick/snare, a shutter click and a horn stab per shot; a roll into the whip
  4-10   fact 1: a sparse bar; STOP-TIME at the freeze (a horn hit, a shutter click, nothing else); the full riff slams back on the title
  10-18  fact 2: the full groove; four ascending horn stabs for the four lit tiles; stop-time before UNDER 1%
  18-24  fact 3 COLD: half-time, a clean tremolo guitar arpeggio, low toms, wind; the horns return when the vines wake
  24-30  fact 4 SUNRISE: half-time, a sustained open chord and a rising horn swell; stop-time before the stamp, then it slams
  30-36  fact 5: everything back, the biggest groove; low toms and horn stabs as the pins drop; a guitar run up the ladder
  36-40  recap hits (accelerating), then the closing bumper: the SAME hit as the opening, and a ring-out
Every event time is read from the picture (mendo_fffa_reel.T), so a timeline change cannot strand a sound. Where a cut has an impact
the impact REPLACES the kick on that beat (the GTR lesson: stacked low end overshoots true peak after AAC), and the 50 ms hole before
each hit has 4 ms ramps (a square-edged gate made the AAC encoder ring: +1.7 dBTP). Checked by measurement; I cannot listen.
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve, lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_audio import SR, BEAT, rng, tvec, lp, hp, bp, place, saw, kick, hat, impact, whoosh, riser  # noqa: E402
import mendo_fffa_reel as R  # noqa: E402

T = R.T
DUR = R.SCENE_TABLE[-1][0] + R.SCENE_TABLE[-1][1]
N = int(SR * DUR)
STEP = BEAT / 4                                             # a 16th: 0.125 s
LEAD = 0.006                                                # an impact's peak lands about 9 ms after its start
BREAKS = [(4.5, 5.0), (14.5, 15.0), (26.5, 27.0)]           # stop-time: the band is cut dead
CUT_HITS = (4.0, 10.0, 18.0, 24.0, 27.0, 30.0, 38.0)        # an impact here REPLACES the kick on the beat


def rel(n, ms=25):
    r = np.ones(n); m = min(int(ms / 1000 * SR), n); r[-m:] = np.linspace(1, 0, m); return r


# ------------------------------------------------------------------ drums and effects
def snare(g=1.0):
    n = int(0.30 * SR); t = tvec(n)
    nz = bp(rng.normal(0, 1, n), 1300, 8000) * np.exp(-t / 0.10)
    tone = np.sin(2 * np.pi * 195 * t) * np.exp(-t / 0.06) * 0.8 + np.sin(2 * np.pi * 330 * t) * np.exp(-t / 0.03) * 0.3
    return (nz * 0.85 + tone) * g


def tom(f0):
    n = int(0.5 * SR); t = tvec(n)
    f = f0 * (1 + 0.7 * np.exp(-t / 0.035))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.2) + bp(rng.normal(0, 1, n), 200, 1500) * np.exp(-t / 0.012) * 0.35) * 0.95


def rim():
    n = int(0.05 * SR); t = tvec(n)
    return (np.sin(2 * np.pi * 1750 * t) * np.exp(-t / 0.006) + hp(rng.normal(0, 1, n), 3000) * np.exp(-t / 0.004) * 0.5) * 0.7


def crash(dur=1.5):
    n = int(dur * SR); t = tvec(n)
    return hp(rng.normal(0, 1, n), 3500) * np.exp(-t / (dur * 0.38)) * 0.5


def ride():
    n = int(0.6 * SR); t = tvec(n)
    return hp(rng.normal(0, 1, n), 5500) * np.exp(-t / 0.25) * 0.22 + (np.sin(2 * np.pi * 3100 * t) + 0.6 * np.sin(2 * np.pi * 4700 * t)) * np.exp(-t / 0.12) * 0.07


def shutter():
    n = int(0.14 * SR); t = tvec(n)
    a = bp(rng.normal(0, 1, n), 700, 6500) * np.exp(-t / 0.006)
    b = bp(rng.normal(0, 1, n), 400, 3500) * np.exp(-np.clip(t - 0.045, 0, None) / 0.012) * (t >= 0.045)
    return (a * 0.9 + b * 0.7) * 0.8


def scratch(dur=0.28):
    n = int(dur * SR); t = tvec(n)
    f = 150 + 1900 * np.abs(np.sin(np.pi * t / dur * 1.5)) ** 1.2
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sign(np.sin(ph)) * 0.4 + np.sin(ph) * 0.4
    env = np.exp(-t / (dur * 0.7)) * np.clip(1 - (t / dur) ** 6, 0, 1)
    return (tone + bp(rng.normal(0, 1, n), 800, 6000) * 0.5) * env * 0.7


def glitch_burst(dur=0.26):
    n = int(dur * SR); t = tvec(n)
    nz = np.round(rng.normal(0, 1, n) * 3) / 3
    gate = (np.sin(2 * np.pi * 38 * t * (1 + 2 * t)) > 0).astype(float)
    return bp(nz, 500, 7000) * gate * np.sin(np.pi * t / dur) * 0.5


# ------------------------------------------------------------------ the electric guitar, the horns, the bass
def ks(freq, dur, decay=0.997):
    """Karplus-Strong plucked string."""
    n = int(dur * SR); p = int(SR / freq)
    ex = np.zeros(n); ex[:p] = lp(rng.normal(0, 1, p), 6000)
    a = np.zeros(p + 2); a[0] = 1; a[p] = -0.5 * decay; a[p + 1] = -0.5 * decay
    return lfilter([1], a, ex)


_G = {}


def egtr(freqs, dur=0.35, mute=False, drive=8.0, var=0):
    """An overdriven electric guitar (a chord or a single note): strings through a clipper and a speaker-cabinet band-pass.
    `var` picks a different noise burst, so the L and R takes of a double-tracked riff are different performances."""
    key = (tuple(freqs), round(dur, 3), mute, drive, var)
    if key not in _G:
        y = sum(ks(f, dur + 0.1, 0.985 if mute else 0.9975) for f in freqs)
        y = np.tanh(drive * y / (np.abs(y).max() + 1e-9))
        y = bp(y, 95, 2800 if mute else 4200)
        t = tvec(len(y))
        env = np.minimum(t / 0.002, 1) * (np.exp(-t / 0.07) if mute else np.exp(-t / (dur * 1.1))) * rel(len(y), 12 if mute else 30)
        _G[key] = y * env * 0.5
    return _G[key]


def cleang(freq, dur=0.9, var=0):
    """A clean electric guitar with tremolo: the cold scene's color."""
    key = ("c", freq, round(dur, 3), var)
    if key not in _G:
        y = ks(freq, dur, 0.9985)
        y = lp(np.tanh(1.3 * y / (np.abs(y).max() + 1e-9)), 3500)
        t = tvec(len(y))
        _G[key] = y * (0.72 + 0.28 * np.sin(2 * np.pi * 5.5 * t)) * np.minimum(t / 0.004, 1) * np.exp(-t / (dur * 0.8)) * rel(len(y), 40) * 0.5
    return _G[key]


_H = {}


def horn(freqs, dur=0.22, att=0.012, fall=0.0):
    """A brass section: stacked sawtooth-ish partials, a bright 'blat' at the front of the note, an optional fall at the end."""
    key = (tuple(freqs), round(dur, 3), round(att, 3), fall)
    if key not in _H:
        n = int((dur + 0.06) * SR); t = tvec(n)
        out = np.zeros(n)
        for fq in freqs:
            fr = fq * (1 - fall * np.clip(t / (dur + 0.06), 0, 1) ** 2) if fall else np.full(n, fq)
            ph = 2 * np.pi * np.cumsum(fr) / SR
            for h in range(1, 11):
                out += np.sin(h * ph) / h ** 0.85
        bright = np.exp(-t / 0.05)
        out = lp(out, 1500) * (1 - bright) + lp(out, 5200) * bright
        out = out * np.minimum(t / att, 1) * np.exp(-t / (dur * 0.9)) * rel(n, 28)
        _H[key] = out / (np.abs(out).max() + 1e-9) * 0.55
    return _H[key]


def bass(freq, dur=0.2):
    n = int(dur * SR); t = tvec(n)
    y = np.tanh(1.5 * (lp(saw(freq, n, 8), 700) * 0.6 + np.sin(2 * np.pi * freq * t) * 0.9))
    return y * np.minimum(t / 0.004, 1) * np.exp(-t / (dur * 0.85)) * rel(n, 15) * 0.8


PW = {"A": (110.0, 164.81, 220.0), "C": (130.81, 196.0, 261.63), "D": (146.83, 220.0, 293.66), "F": (87.31, 130.81, 174.61), "E": (82.41, 123.47, 164.81)}
ROOT = {"A": 55.0, "C": 65.41, "D": 73.42, "F": 43.65, "E": 41.2}
HORN = {"A": (110.0, 220.0, 329.63, 440.0, 523.25), "C": (130.81, 261.63, 392.0, 523.25, 659.25), "D": (146.83, 293.66, 440.0, 587.33, 698.46),
        "E": (164.81, 246.94, 329.63, 493.88, 587.33), "F": (174.61, 261.63, 349.23, 440.0, 523.25)}
BAR_A = [(0, "A", "o", 0.28), (2, "A", "m"), (4, "A", "m"), (6, "A", "m"), (8, "A", "o", 0.20), (10, "C", "o", 0.14), (12, "D", "o", 0.28), (14, "A", "m")]
BAR_B = [(0, "A", "o", 0.28), (2, "A", "m"), (4, "A", "m"), (6, "A", "m"), (8, "F", "o", 0.20), (10, "F", "m"), (12, "E", "o", 0.40), (14, "E", "m")]
LICK = {8: 440.0, 10: 523.25, 11: 587.33, 12: 659.25}


def build():
    drums, bassb, gL, gR, horns, sfx, verb = (np.zeros(N) for _ in range(7))
    kicks = []

    def K(t, g=0.9):
        place(drums, kick(), t, g); kicks.append(t)

    def at_cut(t):
        return any(abs(t - c) < 1e-3 for c in CUT_HITS)

    def gtr(chord, t, dur=0.3, mute=False, g=0.6, drive=8.0):
        place(gL, egtr(PW[chord], dur, mute, drive, 0), t, g); place(gR, egtr(PW[chord], dur, mute, drive, 1), t, g)

    def hornhit(chord, t, dur=0.14, g=0.5, fall=0.0):
        place(horns, horn(HORN[chord], dur, fall=fall), t, g)

    def fill(c, g=1.0):
        """A roll into a cut: five crescendo snares and three toms falling (0.5 s)."""
        for j in range(5):
            place(drums, snare(), c - 0.5 + j * 0.0625, g * (0.35 + 0.12 * j))
        for j, f0 in enumerate((190.0, 150.0, 112.0)):
            place(drums, tom(f0), c - 0.1875 + j * 0.0625, g * 0.85)

    def hit(c, big=1.0, chord="A"):
        """The hit on a cut: an impact (in place of the kick), a crash, a horn hit with a fall, an open power chord."""
        place(sfx, impact(big), c - LEAD, 0.55 * big)
        place(sfx, crash(), c, 0.40 * big)
        place(horns, horn(HORN[chord] + (HORN[chord][0] * 4,), 0.50, fall=0.04), c, 0.65 * big)
        gtr(chord, c, 0.65, False, 0.62 * big)

    def groove(t0, t1, mode="full"):
        k = int(round(t0 / STEP))
        while k * STEP < t1 - 1e-6:
            t, i = k * STEP, k % 16
            bar = int(t // 2.0)
            k += 1
            if any(a <= t < b for a, b in BREAKS):
                continue
            riff = BAR_B if bar % 2 == 1 else BAR_A
            if mode == "full":
                if i in (0, 8, 10) or (i == 14 and bar % 2 == 1):
                    if not at_cut(t):
                        K(t, 0.95 if i == 0 else (0.85 if i == 8 else 0.65))
                if i in (4, 12):
                    place(drums, snare(), t, 0.92)
                if i == 15 and bar % 2 == 1:
                    place(drums, snare(), t, 0.16)
                if i % 2 == 0:
                    place(drums, hat(open_=(i == 14 and bar % 2 == 0)), t, 0.5 if i % 4 == 0 else 0.34)
                for e in riff:
                    if e[0] == i:
                        gtr(e[1], t, e[3] if e[2] == "o" else 0.12, e[2] == "m", 0.62 if e[2] == "o" else 0.5)
                        if i % 2 == 0:
                            place(bassb, bass(ROOT[e[1]], 0.2), t, 0.85)
                if i in (6, 14):
                    hornhit("E" if (i == 14 and bar % 2 == 1) else "A", t, 0.13, 0.5)
                if bar % 4 == 3 and i in LICK:
                    place(gL, egtr((LICK[i],), 0.5 if i == 12 else 0.16, False, 5.0, 0), t, 0.4)
            elif mode == "half":
                if i == 0 and not at_cut(t):
                    K(t, 0.9)
                if i == 8:
                    place(drums, snare(), t, 0.85)
                if i % 4 == 0:
                    place(drums, ride(), t, 0.5)
                if i == 0:
                    place(bassb, bass(ROOT["A" if t < 26.0 else "F"], 1.2), t, 0.8)
            elif mode == "cold":
                if i in (0, 10) and not at_cut(t):
                    K(t, 0.7 if i == 0 else 0.5)
                if i == 8:
                    place(drums, rim(), t, 0.8)
                if i == 12 and bar % 2 == 1:
                    place(drums, tom(100.0), t, 0.4)
                if i == 0:
                    place(bassb, bass(ROOT["A" if t < 21.0 else "F"], 1.7), t, 0.8)

    # ============================================================ OPENING BUMPER (0-2) and the montage (2-3.5), the roll (3.5-4)
    hit(0.0, 0.95)                                              # the bumper's hit: the closing bumper repeats it exactly
    place(bassb, bass(ROOT["A"], 1.4), 0.0, 0.9)
    place(sfx, whoosh(0.9, 200, 3000, 0.7), 0.4, 0.25)          # under the title's sheen sweep
    for j in range(8):                                          # palm-muted pedal 8ths, building
        t = 1.0 + 0.125 * j
        gtr("A", t, 0.12, True, 0.28 + 0.05 * j)
        place(drums, hat(), t, 0.15 + 0.04 * j)
    fill(2.0, 0.9)
    place(sfx, riser(0.5), 1.5, 0.35)
    for k_ in range(6):                                         # the montage on 16ths
        t = 2.0 + 0.25 * k_
        place(sfx, shutter(), t, 0.5)
        if k_ % 2 == 0:
            K(t, 0.9)
            hornhit(("A", "C", "D")[k_ // 2], t, 0.13, 0.55)
        else:
            place(drums, snare(), t, 0.9)
        gtr("A", t, 0.12, True, 0.45)
        place(drums, hat(), t + 0.125, 0.4)
    fill(4.0, 1.0)
    place(sfx, riser(0.5), 3.5, 0.4)
    place(sfx, whoosh(0.3, 300, 6000, 0.7), 3.86, 0.5)

    # ============================================================ FACT 1 (4-10): sparse, STOP-TIME at the freeze, then the riff
    hit(4.0, 1.1)
    place(bassb, bass(ROOT["A"], 0.6), 4.0, 0.9)
    place(drums, hat(), 4.25, 0.4)
    place(horns, horn(HORN["A"] + (HORN["A"][0] * 4,), 0.45, fall=0.05), T("s_f1", 0.5), 0.8)       # the freeze: a horn hit on the beat, then stop-time
    place(sfx, shutter(), T("s_f1", 0.5), 0.8)
    place(sfx, rim(), T("s_f1", 0.8), 0.5)
    groove(5.0, 9.5, "full")
    hit(T("s_f1", 1.0), 0.6)                                    # the title slams; the groove returns on it
    place(drums, snare(), T("s_f1", 1.0), 0.8)
    for j in range(12):                                         # the year counter: a hi-hat roll that climbs
        place(drums, hat(), T("s_f1", 1.4 + 0.065 * j), 0.18 + 0.03 * j)
    place(sfx, rim(), T("s_f1", 2.25), 0.6)
    hornhit("A", T("s_f1", 2.8), 0.16, 0.6)
    fill(10.0, 1.0)

    # ============================================================ FACT 2 (10-18): the full groove; four climbing horn stabs; stop-time before UNDER 1%
    hit(10.0, 1.0)
    place(sfx, whoosh(0.5, 400, 7000, 0.9), 9.78, 0.35)
    groove(10.0, 14.5, "full")
    place(sfx, riser(0.9), T("s_f2", 0.5), 0.3)
    for k_, (lo, hi_) in enumerate(((220.0, 440.0), (261.63, 523.25), (293.66, 587.33), (329.63, 659.25))):
        t = T("s_f2", 1.7 + 0.22 * k_)
        place(horns, horn((lo, hi_, hi_ * 1.5), 0.13), t, 0.62)
        place(sfx, rim(), t, 0.5)
    for j in range(10):
        place(drums, hat(), T("s_f2", 1.7 + 0.1 * j), 0.18 + 0.03 * j)
    place(sfx, whoosh(0.4, 4000, 300, 0.3), 14.2, 0.45)
    place(horns, horn(HORN["A"] + (HORN["A"][0] * 4,), 0.45, fall=0.05), 14.5, 0.8)                  # stop-time before UNDER 1%: the same horn hit
    groove(15.0, 17.5, "full")
    hit(T("s_f2", 4.9), 0.7)                                    # the county tile fills; the band comes back
    place(sfx, rim(), T("s_f2", 5.4), 0.5)
    fill(18.0, 1.0)

    # ============================================================ FACT 3 (18-24): COLD. Half-time, a clean tremolo guitar, toms, wind
    place(sfx, whoosh(0.5, 200, 4500, 0.5), 17.75, 0.45)
    place(sfx, impact(0.7), 18.0 - LEAD, 0.5)
    groove(18.0, 23.5, "cold")
    for j in range(11):                                         # a sparse clean arpeggio: Am, then F
        t = 18.5 + 0.5 * j
        cyc = ((220.0, 329.63, 440.0, 329.63) if t < 21.0 else (174.61, 261.63, 349.23, 261.63))[j % 4]
        place(sfx, cleang(cyc, 0.9, j % 2), t, 0.6)
    wind = bp(rng.normal(0, 1, int(5.2 * SR)), 380, 1300) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.35 * tvec(int(5.2 * SR)) + 1.0))
    place(sfx, wind * np.minimum(tvec(len(wind)) / 0.6, 1) * 0.12, 18.3, 1.0)
    place(sfx, lp(rng.normal(0, 1, int(2.2 * SR)), 110) * np.minimum(tvec(int(2.2 * SR)) / 1.0, 1), T("s_f3", 0.9), 0.5)
    place(sfx, cleang(659.25, 1.3), T("s_f3", 1.7), 0.7)
    place(sfx, rim(), T("s_f3", 1.7), 0.5)
    place(sfx, rim(), T("s_f3", 3.5), 0.4)
    t = T("s_f3", 3.7)                                          # the vines wake: the horns return and a lick climbs
    hornhit("A", t, 0.2, 0.6)
    for j, f_ in enumerate((220.0, 261.63, 293.66, 329.63)):
        place(gL, egtr((f_,), 0.14, True, 5.0, 0), t + 0.1 * j, 0.5)
    place(sfx, riser(0.5), 23.5, 0.4)
    fill(24.0, 1.0)

    # ============================================================ FACT 4 (24-30): SUNRISE. Half-time, an open chord, a horn swell, stop-time, the stamp
    place(sfx, glitch_burst(0.26), 23.95, 0.7)
    hit(24.0, 1.0)
    groove(24.0, 26.5, "half")
    gtr("A", 24.2, 1.9, False, 0.5, 6.0)
    place(horns, horn((220.0, 329.63, 440.0, 523.25), 2.3, att=0.9), 24.2, 0.5)       # a brass swell into the stop
    for j in range(4):
        place(sfx, tom(88.0 + 8 * j), T("s_f4", 0.2 + 0.12 * j), 0.8)
    for j in range(8):                                          # the 1,200 ft line draws: a hi-hat ratchet
        place(drums, hat(), T("s_f4", 0.9 + 0.1 * j), 0.28)
    place(sfx, rim(), T("s_f4", 1.5), 0.5)
    place(sfx, riser(0.5), 26.5, 0.5)
    place(sfx, impact(1.0), T("s_f4", 3.0) - LEAD, 0.8)         # the stamp lands on the drop
    place(sfx, crash(), T("s_f4", 3.0), 0.5)
    hornhit("A", T("s_f4", 3.0), 0.5, 0.8, fall=0.05)
    gtr("A", T("s_f4", 3.0), 0.65, False, 0.65)
    groove(27.0, 29.5, "full")
    fill(30.0, 1.0)

    # ============================================================ FACT 5 (30-36): everything back; pins, a run up the ladder, the biggest groove
    place(sfx, whoosh(0.3, 300, 6000, 0.7), 29.86, 0.55)
    hit(30.0, 1.15)
    groove(30.0, 35.5, "full")
    for j, f_ in enumerate((220.0, 261.63, 293.66, 329.63, 392.0)):      # the ladder's five rungs: a guitar run up A minor pentatonic
        place(gL, egtr((f_,), 0.14, True, 5.0, 0), T("s_f5", 0.9 + 0.08 * j), 0.6)
    for u0, f0, ch in ((1.0, 110.0, "A"), (1.9, 130.0, "C"), (2.9, 150.0, "D")):    # Philo, Boonville, Ukiah: a low tom and a horn stab
        place(sfx, tom(f0), T("s_f5", u0), 0.9)
        hornhit(ch, T("s_f5", u0), 0.12, 0.55)
    for j in range(8):
        place(drums, hat(), T("s_f5", 1.7 + 0.075 * j), 0.28)
    place(sfx, rim(), T("s_f5", 2.4), 0.6)
    hit(T("s_f5", 3.5), 0.6)
    fill(36.0, 1.0)

    # ============================================================ OUTRO (36-40): the recap hits, then the closing bumper (the same hit)
    place(sfx, impact(0.9), 36.0 - LEAD, 0.6)
    for k_, (t_off, ch) in enumerate(((0.0, "A"), (0.5, "C"), (1.0, "D"), (1.5, "E"), (1.75, "A"))):
        t = 36.0 + t_off
        place(sfx, shutter(), t, 0.5)
        if k_:
            K(t, 0.9)
        place(drums, snare(), t + (0.0 if k_ % 2 else 0.0), 0.7 if k_ % 2 else 0.0)
        hornhit(ch, t, 0.14, 0.6)
        gtr("A", t, 0.12, True, 0.5)
    place(sfx, riser(1.0), 37.0, 0.3)
    hit(38.0, 0.95)                                             # the SAME hit as the opening
    place(bassb, bass(ROOT["A"], 1.8), 38.0, 0.9)
    place(sfx, whoosh(0.9, 200, 3000, 0.7), 38.4, 0.25)

    # ============================================================ the mix: ducking, the holes before the hits (with ramps), a send reverb, a soft clip
    duck = np.ones(N)
    for t in kicks:
        i = int(t * SR); m = min(N, i + int(0.14 * SR))
        duck[i:m] = np.minimum(duck[i:m], 0.78 + 0.22 * np.linspace(0, 1, m - i))
    bassb *= duck; gL *= duck; gR *= duck
    dip = np.ones(N)
    dip[int(35.94 * SR):int(36.0 * SR)] = 0.0
    for c in (4.0, 10.0, 18.0, 24.0, 30.0, 38.0):
        dip[int((c - 0.056) * SR):int((c - LEAD) * SR)] = 0.10
    ramp = int(0.004 * SR)
    dip = np.convolve(dip, np.ones(ramp) / ramp, "same")        # 4 ms ramps: a square-edged gate makes the AAC encoder ring
    ir_n = int(1.3 * SR)
    irL = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.34); irR = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.34)
    irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
    send = horns * 0.6 + (gL + gR) * 0.25 + sfx * 0.2
    vL = fftconvolve(send, irL)[:N] * 0.5
    vR = fftconvolve(send, irR)[:N] * 0.5
    L = hp(drums * 0.95 + bassb * 0.9 + gL * 1.0 + horns * 0.85 + sfx + vL, 28) * dip
    Rr = hp(drums * 0.95 + bassb * 0.9 + gR * 1.0 + horns * 0.85 + sfx + vR, 28) * dip
    out = np.stack([L, Rr], 1)
    fade = np.ones(N); fn = int(0.06 * SR); fade[-fn:] = np.linspace(1, 0, fn)
    out *= fade[:, None]
    out = np.tanh(out * 1.3) / np.tanh(1.3)
    return out / (np.max(np.abs(out)) / 0.89)


def check_audio(a):
    """The low band's onset (the impact's boom) within +-100 ms of each hit, in ms from the cut."""
    from scipy.signal import butter, sosfilt
    lo = np.convolve(np.abs(sosfilt(butter(2, 150, "low", fs=SR, output="sos"), a.mean(1))), np.ones(48) / 48, "same")
    res = []
    for c in (0.0, 4.0, 10.0, 18.0, 24.0, 27.0, 30.0, 36.0, 38.0):
        i0, i1 = max(int((c - 0.10) * SR), 0), int((c + 0.12) * SR)
        seg = lo[i0:i1]
        res.append((c, (i0 + int(np.argmax(seg > 0.35 * seg.max()))) / SR - c))
    return res


if __name__ == "__main__":
    a = build()
    path = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/mendo_fffa_audio.wav"
    wavfile.write(path, SR, (a * 32767).astype(np.int16))
    print(f"wrote {path}: {len(a) / SR:.2f}s, peak {20 * np.log10(np.abs(a).max()):.2f} dBFS")
    print("low-band onset vs. hit (ms):", "  ".join(f"{c:g}s:{off * 1000:+.1f}" for c, off in check_audio(a)))
