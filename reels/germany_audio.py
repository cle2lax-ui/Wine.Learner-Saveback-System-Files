"""Original score and sound design for the Germany Reel (30.0 s, 48 kHz stereo).

v2 (30 s): every picture-event time is read from germany_reel.SCENE_TABLE via T(scene, u), so a sound
cannot drift off its event when the picture is retimed. The groove runs 2.0-26.0 s (cuts on downbeats).

Everything is synthesized here (no samples, no library music), so the Reel has no music-licensing
question. 120 BPM, A minor, Am-F-C-G, one chord per 2-second bar, matching the picture's bars.
Hook bar: pad swell, letter hits, a riser into the first cut. Groove from 2.0 s to 17.5 s: kick,
clap, hats, bass and a plucked arpeggio, the pad and bass ducked by the kick. 17.5 s: drums out,
a final impact and an A minor (add9) chord that rings out to the fade.

Sound effects are locked to the picture's own event times (germany_reel.py): whooshes on every
transition, impacts on the cuts, ticks while the counters run, knocks as the ladder's rungs land,
pops on the chips. Loudness is normalized at mux time (ffmpeg loudnorm, -14 LUFS, -1.5 dBTP).

LIMITATION, stated plainly: this was composed and checked numerically (levels, peaks, clipping,
timing against the picture), not auditioned by ear. Swapping in a track from Instagram's audio
library at posting time is always an option; the picture does not depend on this score.
"""
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from germany_reel import T, CUTS_BANDS, CUTS_WHIP, CUT_PAPER  # noqa: E402

SR = 48000
DUR = 30.0
GROOVE_END = 26.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(3)


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


# ------------------------------------------------------------------ score
CHORDS = {"Am": (110.0, (220.0, 261.63, 329.63)), "F": (87.31, (174.61, 220.0, 261.63)),
          "C": (130.81, (261.63, 329.63, 392.0)), "G": (98.0, (196.0, 246.94, 293.66))}
BARS = ["Am"] + ["Am", "F", "C", "G"] * 3                 # bars 0..12 (0-26 s); 26 s resolves to Am


def build():
    L = np.zeros(N); R = np.zeros(N)
    drums = np.zeros(N); kick_env = np.zeros(N)
    music_L = np.zeros(N); music_R = np.zeros(N); verb_send = np.zeros(N)
    sfx = np.zeros(N)

    # --- drums 2.0 -> 17.5
    k = kick()
    for b in np.arange(2.0, GROOVE_END, BEAT):
        place(drums, k, b, 1.0)
        i = int(b * SR); m = min(N, i + int(0.3 * SR))
        kick_env[i:m] = np.maximum(kick_env[i:m], np.exp(-tvec(m - i) / 0.12))
    c = clap()
    for b in np.arange(2.5, GROOVE_END, 2 * BEAT):
        place(drums, c, b, 0.9)
    for j, b in enumerate(np.arange(2.0, GROOVE_END, BEAT / 4)):
        acc = 1.0 if j % 4 == 2 else 0.55
        place(drums, hat(open_=(j % 8 == 6)), b, 0.5 * acc)

    duck = 1 - 0.55 * kick_env                                 # sidechain from the kick

    # --- bass (8ths) and pad per bar, arp 16ths
    for bi, name in enumerate(BARS):
        t0 = bi * 2.0
        root, chord = CHORDS[name]
        if t0 >= GROOVE_END:
            continue
        # pad
        n = int(min(2.0, GROOVE_END - t0 + 0.05) * SR)
        env = np.minimum(1, tvec(n) / 0.25) * np.minimum(1, (n / SR - tvec(n)) / 0.2 + 0.0001)
        for fq in chord:
            for side, dt in ((music_L, -6), (music_R, +6)):
                place(side, lp(saw(fq, n, 10, dt), 1800) * env * 0.07, t0)
        place(verb_send, lp(saw(chord[0], n, 8), 1500) * env * 0.05, t0)
        if t0 >= 2.0:
            # bass: 8th notes, root with an octave pop on the last 8th
            for e in range(4 * 2):
                tb = t0 + e * BEAT / 2
                if tb >= GROOVE_END:
                    break
                fq = root * (2 if e == 7 else 1)
                nb = int(0.22 * SR)
                sig = lp(saw(fq, nb, 10), 700) * np.exp(-tvec(nb) / 0.12) * 0.45
                place(music_L, sig, tb); place(music_R, sig, tb)
            # arp 16ths over chord tones, up an octave; the delay echoes go to the other side
            pat = [0, 1, 2, 1, 0, 2, 1, 2]
            for s16 in range(16):
                ta = t0 + s16 * BEAT / 4
                if ta >= GROOVE_END:
                    break
                fq = chord[pat[s16 % 8]] * 2
                sig = pluck(fq, 0.2, 1.2) * 0.16
                place(music_L if s16 % 2 == 0 else music_R, sig, ta)
                place(music_R if s16 % 2 == 0 else music_L, sig * 0.45, ta + 0.1875)
                place(verb_send, sig * 0.5, ta)
    music_L *= duck; music_R *= duck

    # --- hook bar: rising motif on "in 20 seconds"
    for i, fq in enumerate((440.0, 523.25, 659.25, 880.0)):
        place(music_L, pluck(fq, 0.5, 2) * 0.18, 1.12 + 0.12 * i)
        place(music_R, pluck(fq, 0.5, 2) * 0.18, 1.14 + 0.12 * i)
        place(verb_send, pluck(fq, 0.5, 2) * 0.3, 1.12 + 0.12 * i)

    # --- ending: final Am(add9) chord rings through the 4-second outro
    n = int(4.0 * SR)
    env = np.minimum(1, tvec(n) / 0.02) * np.exp(-tvec(n) / 2.0)
    for fq in (110.0, 220.0, 261.63, 329.63, 493.88):
        sig = lp(saw(fq, n, 10), 2200) * env * 0.09
        place(music_L, sig, GROOVE_END); place(music_R, sig, GROOVE_END); place(verb_send, sig * 1.2, GROOVE_END)
    for i, fq in enumerate((880.0, 659.25, 523.25)):          # a falling sparkle under PROST.
        place(verb_send, pluck(fq, 0.6, 2) * 0.35, T("s6", 0.12 + 0.12 * i))

    # --- sound design, locked to picture events
    place(sfx, whoosh(0.42, 250, 6000, 0.7), 0.0, 0.5)         # opening flag sweep
    place(sfx, impact(0.8), 0.42, 0.55)                          # GERMANY lands
    for i in range(7):
        place(sfx, knock(), 0.62 + 0.05 * i, 0.35)               # letter by letter
    place(sfx, riser(0.55), 1.45, 0.45)
    for c_ in CUTS_BANDS:                                        # flag-band cuts
        place(sfx, whoosh(0.4, 300, 6500, 0.55), c_ - 0.2, 0.6)
        place(sfx, impact(0.7 if c_ == CUTS_BANDS[1] else 1.0), c_, 0.9 if c_ == CUTS_BANDS[-1] else 0.65)
    for c_ in CUTS_WHIP:                                         # whip cuts
        place(sfx, whoosh(0.26, 600, 9000, 0.85), c_ - 0.13, 0.7)
        place(sfx, impact(0.6), c_, 0.5)
    place(sfx, whoosh(0.3, 200, 2500, 0.8), CUT_PAPER - 0.22, 0.45)   # the paper sheet slides up
    for kk in range(5):
        place(sfx, knock(), T("s2", 0.18 + 0.14 * kk + 0.08), 0.7)    # ladder rungs land
    for t_, n_, st in ((T("s1", 1.65), 22, 1.10), (T("s4", 0.75), 20, 1.10),
                       (T("s5", 0.55), 10, 1.35), (T("s5", 0.67), 10, 1.35)):   # counters
        for j in range(n_):
            place(sfx, tick(), t_ + j * 0.03 * (1 + j / n_) * st, 0.12)
    for t_ in (T("s1", 0.1), T("s2", 0.06), T("s3", 0.12), T("s4", 0.08), T("s5", 0.02),
               T("s3", 1.9), T("s3", 2.05), T("s6", 1.15)):           # chips and pops
        place(sfx, pop(), t_, 0.25)
    for t_ in (T("s2", 1.0), T("s2", 1.32), T("s4", 1.6), T("s5", 0.1)):   # headline slams
        place(sfx, impact(0.35), t_, 0.35)

    # --- reverb (synthetic decaying-noise IR, stereo) and mix
    ir_n = int(1.6 * SR)
    irL = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.45); irR = rng.normal(0, 1, ir_n) * np.exp(-tvec(ir_n) / 0.45)
    irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
    vL = fftconvolve(verb_send + sfx * 0.25, irL)[:N] * 0.6
    vR = fftconvolve(verb_send + sfx * 0.25, irR)[:N] * 0.6
    L = drums * 0.9 + music_L + sfx + vL
    R = drums * 0.9 + music_R + sfx + vR
    out = np.stack([hp(L, 28), hp(R, 28)], 1)
    fade = np.ones(N); fn = int(0.45 * SR); fade[-fn:] = np.linspace(1, 0, fn) ** 1.5
    out *= fade[:, None]
    out = np.tanh(out * 1.4) / np.tanh(1.4)                      # gentle saturation / soft limit
    out /= np.max(np.abs(out)) / 0.89
    return out


if __name__ == "__main__":
    import sys
    a = build()
    path = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/germany_reel_audio.wav"
    wavfile.write(path, SR, (a * 32767).astype(np.int16))
    rms = 20 * np.log10(np.sqrt((a ** 2).mean()) + 1e-12)
    print(f"wrote {path}: {a.shape[0] / SR:.2f}s stereo, peak {20 * np.log10(np.abs(a).max()):.2f} dBFS, RMS {rms:.1f} dBFS")
