"""Score for the Wines of South Africa trailer Reel (30 s): original, synthesized in code (reel_audio.py), so no licensing question. 120 BPM, A minor
(Am-F-C-G), one chord per 2-second bar. Every sound is placed from the picture's own event times (sa_trailer_reel.SCENE_TABLE, LIT_AT and the in-scene
timings), so a sound cannot drift off its picture.
  0-2   the music is already moving on frame 1 (pad, bass and a plucked arpeggio, with an impact on the first frame), and a riser leads to the first cut
  2-26  four on the floor, claps on 2 and 4, off-beat hats, an arpeggio, bass on 1 and 3
  every cut: an impact, a whoosh, a pop for the chip, a tick as the progress node lights
  "?" badges and the "VS": a pop;  counting numbers: a tick per step, a pop when they land
  26-30 the outro: one last impact, drums out, the mix fades to silence so the Reel loops into its own first frame
Checked by measurement, not by ear. Instagram's audio library can replace it at upload.   Usage: python3 sa_trailer_audio.py audio.wav [gain_dB]
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_audio as A                                    # noqa: E402
from reel_audio import SR, place, tvec                    # noqa: E402
import sa_trailer_reel as R                               # noqa: E402

DUR, BAR, BEAT = R.DUR, 2.0, 0.5
CHORDS = [(110.0, [220.0, 261.63, 329.63]), (87.31, [174.61, 220.0, 261.63]), (130.81, [261.63, 329.63, 392.0]), (98.0, [196.0, 246.94, 293.66])]


def start(name):
    return [s for s, d, n, _ in R.SCENE_TABLE if n == name][0]


def pad(notes, dur):
    n = int(dur * SR)
    out = A.lp(sum(A.saw(f, n, 10, d) for f in notes for d in (-7, 7)), 1400)
    t = tvec(n)
    return out * np.clip(t / 0.18, 0, 1) * np.clip((dur - t) / 0.35, 0, 1) * 0.11


def bass(f, dur):
    n = int(dur * SR); t = tvec(n)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t / 0.7) * np.clip(t / 0.01, 0, 1) * 0.55


def build():
    bus = np.zeros(int((DUR + 0.5) * SR))
    place(bus, A.impact(0.8), 0.02, 0.9)                                    # on the first frame: the Reel is already moving
    place(bus, A.riser(0.9), 3.1, 0.5)                                      # into the first cut
    for bar in range(0, 14):
        t0 = bar * BAR
        root, triad = CHORDS[bar % 4]
        place(bus, pad(triad, BAR), t0, 1.0)
        place(bus, bass(root, 0.95), t0, 0.9)
        place(bus, bass(root, 0.95), t0 + 2 * BEAT, 0.75)
        for e in range(8):
            seq = [0, 1, 2, 1, 2, 1, 0, 1]
            place(bus, A.pluck(triad[seq[e]] * 2, 0.22, 1.0), t0 + e * BEAT / 2, 0.20)
        if bar >= 1:                                                         # the groove from the second bar
            for b in range(4):
                place(bus, A.kick(), t0 + b * BEAT, 0.55)
            for b in (1, 3):
                place(bus, A.clap(), t0 + b * BEAT, 0.5)
            for e in range(8):
                if e % 2:
                    place(bus, A.hat(open_=(e == 7)), t0 + e * BEAT / 2, 0.55)
    for s, d, n, _ in R.SCENE_TABLE:
        if n == "hook":
            continue
        place(bus, A.impact(0.4), s, 0.8)                                    # an impact on every cut
        place(bus, A.whoosh(0.5, 300, 4500, 0.6), s + 0.04, 0.55)
        place(bus, A.pop(), s + 0.05, 0.5)                                   # the chip
    for tl in R.LIT_AT:
        place(bus, A.tick(), tl, 0.7)                                       # a progress node lights
        place(bus, A.pop(), tl + 0.05, 0.28)
    place(bus, A.pop(), start("gtr") + 0.9, 0.55)                           # the "?" badges
    place(bus, A.pop(), start("wad") + 1.0, 0.55)
    s = start("fffa")
    for i in range(3):                                                       # the three counting numbers
        t0 = s + 0.7 + 1.75 * i
        for k in range(8):
            place(bus, A.tick(), t0 + 0.05 + k * 0.095, 0.4)
        place(bus, A.pop(), t0 + 0.85, 0.5)
    s = start("sd")                                                          # the two panels, their counts and the VS
    place(bus, A.whoosh(0.4, 400, 5000, 0.5), s + 0.02, 0.5)
    for d0, g in ((0.35, 0.4), (0.55, 0.4)):
        for k in range(8):
            place(bus, A.tick(), s + d0 + k * 0.1, g)
        place(bus, A.pop(), s + d0 + 0.85, 0.45)
    place(bus, A.pop(), s + 0.95, 0.6)
    o = start("outro")
    place(bus, A.riser(0.9), o - 0.9, 0.5)
    place(bus, A.impact(1.0), o, 1.0)
    t = np.arange(len(bus)) / SR
    bus *= np.clip((DUR - t) / 0.3, 0, 1)
    bus[int(DUR * SR):] = 0
    return bus[:int(DUR * SR)]


def write(path, gain_db=0.0):
    x = np.tanh(build() * 0.9) * 10 ** (gain_db / 20)
    wavfile.write(path, SR, (np.clip(np.stack([x, x], 1), -1, 1) * 32767).astype(np.int16))


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/sa_out/audio.wav", float(sys.argv[2]) if len(sys.argv) > 2 else 0.0)
    print("audio written")
