"""Shared audio toolkit for the Reels: synthesized instruments and sound effects (no samples, no library
music, so no licensing question). Extracted from germany_audio.py, which keeps its own copy so the finished
Germany Reel's audio stays byte-identical (its random-noise sequence depends on its own generator).

Each Reel's score module builds its arrangement and places sound effects at its picture's own event times.
"""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
BEAT = 0.5
rng = np.random.default_rng(7)


def tvec(n):
    return np.arange(n) / SR


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def place(bus, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(bus) or i + len(sig) <= 0:
        return
    j = min(len(bus), i + len(sig))
    bus[max(i, 0):j] += sig[max(0, -i):j - i] * gain


def saw(freq, n, harmonics=14, detune=0.0):
    t = tvec(n)
    out = np.zeros(n)
    f = freq * (2 ** (detune / 1200))
    for k in range(1, harmonics + 1):
        if f * k > SR / 2 - 500:
            break
        out += np.sin(2 * np.pi * f * k * t) / k
    return out * 0.6


# ------------------------------------------------------------------ instruments
def kick():
    n = int(0.42 * SR); t = tvec(n)
    f = 48 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.16)
    click = hp(rng.normal(0, 1, n), 2500) * np.exp(-t / 0.004) * 0.35
    return (body + click) * 0.95


def clap():
    n = int(0.3 * SR); t = tvec(n)
    nz = bp(rng.normal(0, 1, n), 900, 5500)
    env = np.exp(-t / 0.09)
    for d in (0.0, 0.011, 0.022):                               # the three-hit "clap" flam
        env += 0.6 * np.exp(-np.clip(t - d, 0, None) / 0.008) * (t >= d)
    tone = np.sin(2 * np.pi * 210 * t) * np.exp(-t / 0.05) * 0.3
    return (nz * env * 0.32 + tone) * 0.8


def hat(open_=False):
    n = int((0.16 if open_ else 0.05) * SR); t = tvec(n)
    return hp(rng.normal(0, 1, n), 7500, 3) * np.exp(-t / (0.06 if open_ else 0.014)) * 0.35


def pluck(freq, dur=0.22, bright=1.0):
    n = int(dur * SR); t = tvec(n)
    out = np.zeros(n)
    for k in range(1, 9):
        out += np.sin(2 * np.pi * freq * k * t) * (0.55 ** (k - 1)) * np.exp(-t * (6 + k * 5 / bright))
    return out * 0.5


def knock():
    n = int(0.12 * SR); t = tvec(n)
    return (np.sin(2 * np.pi * 185 * t) * np.exp(-t / 0.035) + bp(rng.normal(0, 1, n), 400, 2500) * np.exp(-t / 0.01) * 0.4) * 0.8


def tick():
    n = int(0.012 * SR); t = tvec(n)
    return np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.003)


def pop():
    n = int(0.06 * SR); t = tvec(n)
    f = 1100 * np.exp(-t / 0.03) + 500
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.02)


def impact(size=1.0):
    n = int(1.2 * SR); t = tvec(n)
    f = 34 + 40 * np.exp(-t / 0.08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.35 * size))
    crack = lp(rng.normal(0, 1, n), 3500) * np.exp(-t / 0.05) * 0.5
    return (boom + crack) * size


def whoosh(dur=0.4, lo=300, hi=5000, peak=0.6):
    n = int(dur * SR)
    nz = rng.normal(0, 1, n)
    out = np.zeros(n)
    blk = 512
    for i in range(0, n, blk):
        p = i / n
        c = lo * (hi / lo) ** (p if p < peak else peak - (p - peak) * peak / (1 - peak))
        seg = nz[max(0, i - 256):i + blk]
        y = bp(seg, max(c * 0.6, 40), min(c * 1.6, SR / 2 - 100))
        out[i:i + blk] = y[-len(out[i:i + blk]):]
    env = np.sin(np.pi * np.clip(np.arange(n) / n, 0, 1)) ** 1.5
    return out * env * 0.9


def riser(dur=0.6):
    n = int(dur * SR); t = tvec(n)
    f = 220 * (6 ** (t / dur))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    return (whoosh(dur, 400, 7000, 0.98) + tone) * (t / dur) ** 2
