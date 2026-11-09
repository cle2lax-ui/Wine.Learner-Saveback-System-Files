"""Score for the COMING UP trailer Reel (30 s). Original and synthesized in code (reel_audio.py): no samples, no library music, so no licensing question.
120 BPM in A minor (Am-F-C-G), one chord per 2-second bar, so the music's bars are the picture's scenes. Every sound effect is placed at the picture's own event
time, read from trailer_reel.SCENE_TABLE / LIT_AT, so a sound cannot drift off its picture event when the timing changes.

  0-2     hook: a low impact on the first frame, a riser into the first cut
  2-28    four on the floor, claps on 2 and 4, off-beat hats, a plucked arpeggio, bass on 1 and 3, a pad per bar
  events  whoosh as each card enters and on each swipe; a pop on each chip and each "?" badge; a tick as each progress node lights;
          pops with the three South Africa bullets; an impact on every cut
  28-30   outro: the drums drop out, one last impact, and the whole mix fades to silence so the Reel loops into its own opening

It was checked by measurement (integrated loudness, true peak, transient timing), not by ear. Instagram's audio library can replace it at posting time.
Usage: python3 trailer_audio.py audio.wav
"""
import os
import sys

import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_audio as A                                    # noqa: E402
from reel_audio import SR, place, tvec                    # noqa: E402
import trailer_reel as R                                  # noqa: E402

DUR = R.DUR
BAR, BEAT = 2.0, 0.5
CHORDS = [(110.0, [220.0, 261.63, 329.63]), (87.31, [174.61, 220.0, 261.63]),      # Am, F
          (130.81, [261.63, 329.63, 392.0]), (98.0, [196.0, 246.94, 293.66])]      # C, G


def scene(name):
    for s, d, n, _ in R.SCENE_TABLE:
        if n == name:
            return s, d
    raise KeyError(name)


def pad(notes, dur):
    n = int(dur * SR)
    out = sum(A.saw(f, n, 10, d) for f in notes for d in (-7, 7))
    out = A.lp(out, 1400)
    t = tvec(n)
    env = np.clip(t / 0.18, 0, 1) * np.clip((dur - t) / 0.35, 0, 1)
    return out * env * 0.11


def bass(f, dur):
    n = int(dur * SR); t = tvec(n)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t / 0.7) * np.clip(t / 0.01, 0, 1) * 0.55


def build():
    bus = np.zeros(int((DUR + 0.5) * SR))
    # ---- hook
    place(bus, A.impact(0.8), 0.02, 0.9)
    place(bus, A.riser(0.8), 1.2, 0.55)
    # ---- the groove, bars 2..13 (2 s to 28 s)
    for bar in range(1, 14):
        t0 = bar * BAR
        root, triad = CHORDS[(bar - 1) % 4]
        place(bus, pad(triad, BAR), t0, 1.0)
        place(bus, bass(root, 0.95), t0, 0.9)
        place(bus, bass(root, 0.95), t0 + 2 * BEAT, 0.75)
        for b in range(4):
            place(bus, A.kick(), t0 + b * BEAT, 0.55)
        for b in (1, 3):
            place(bus, A.clap(), t0 + b * BEAT, 0.5)
        for e in range(8):
            if e % 2:
                place(bus, A.hat(open_=(e == 7)), t0 + e * BEAT / 2, 0.55)
            seq = [0, 1, 2, 1, 2, 1, 0, 1]
            place(bus, A.pluck(triad[seq[e]] * 2, 0.22, 1.0), t0 + e * BEAT / 2, 0.20)
    # ---- the picture's events (every time comes from the scene table)
    for s, d, n, _ in R.SCENE_TABLE:
        if n in ("hook",):
            continue
        place(bus, A.impact(0.4), s, 0.8)                              # an impact on every cut
        place(bus, A.whoosh(0.5, 300, 4500, 0.6), s + 0.04, 0.55)       # the card (or title) arrives
        place(bus, A.pop(), s + 0.05, 0.5)                              # the chip pops
    for i, tl in enumerate(R.LIT_AT):
        place(bus, A.tick(), tl, 0.7)                                  # a progress node lights
        place(bus, A.pop(), tl + 0.05, 0.28)
    for name in ("fg", "fffa"):
        s, _ = scene(name)
        times = {"fg": [2.2, 3.6, 5.0], "fffa": [1.5, 2.4, 3.3, 4.2, 5.1]}[name]
        for t0 in times:
            place(bus, A.whoosh(0.34, 500, 6000, 0.55), s + t0, 0.5)    # a swipe
            place(bus, A.knock(), s + t0 + 0.3, 0.35)                   # the next card lands
    for name in ("gtr", "wad"):
        s, _ = scene(name)
        place(bus, A.pop(), s + 1.3, 0.55)                              # the "?" badge
    s, _ = scene("tease")
    for t0 in (1.5, 2.7, 3.9):
        place(bus, A.pop(), s + t0, 0.5)                                # a South Africa bullet
    place(bus, A.riser(0.9), scene("outro")[0] - 0.9, 0.5)              # into the outro
    place(bus, A.impact(1.0), scene("outro")[0], 1.0)
    # ---- the drums drop out in the outro: undo the last bar's groove tail by fading the whole bus
    t = np.arange(len(bus)) / SR
    bus *= np.clip((DUR - t) / 0.3, 0, 1)
    bus[int(DUR * SR):] = 0
    return bus[:int(DUR * SR)]


def write(path, gain_db=0.0):
    x = np.tanh(build() * 0.9)
    x = x * 10 ** (gain_db / 20)
    st = np.stack([x, x], 1)
    wavfile.write(path, SR, (np.clip(st, -1, 1) * 32767).astype(np.int16))


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/trailer_out/audio.wav", float(sys.argv[2]) if len(sys.argv) > 2 else 0.0)
    print("audio written")
