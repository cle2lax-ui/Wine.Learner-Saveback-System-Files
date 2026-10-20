"""FIVE FASCINATING FACTS ABOUT MENDOCINO: a Reel. 1080x1920, 30 fps, 36 s. Arc 3, the arc's last entry.

Steve: "use that FFFA deck as a starting point for a Reel that animates the five facts. Polished, slick and glossy as if
it was produced by Guy Ritchie."  The deck: arc3/render_fffa_mendocino.py (LOCKED, tag fffa-mendocino-final). Every claim
on screen is a claim on those pages, with the sources traced in that file's docstring; this Reel adds NO new facts.

THE STYLE (a reference to a film language, not an imitation of anyone): beat-locked cutting; snap zooms; freeze-frames with
annotated callouts and a viewfinder; whip pans and smash cuts; a teal-shadow, amber-highlight grade with crushed blacks, halation,
chromatic fringing, grain and dust; kinetic type with a specular sheen; the facts as "case files" with an evidence-style
source tag. The score is original, synthesized in code (mendo_fffa_audio.py): a stop-time caper groove.

TIMELINE (120 BPM, 2-second bars; every cut is a downbeat). Scene lengths are the single source of truth (SCENE_TABLE).
  0-4    title   frame 0 carries the whole hook; a six-shot montage on 16ths, one word per fact; FIVE FACTS. ONE COUNTY.
  4-8    f1      THE CHAMPAGNE JOB   (deck page 2)  freeze-frame, 1982 counter, bubbles
  8-14   f2      THE FOUR PERCENT    (page 3)       a 10 x 10 grid: four tiles light; the county is under one
  14-20  f3      THE FROST POCKET    (page 4)       cold air runs downhill and pools; the vines sit on the slopes
  20-26  f4      ABOVE THE FOG       (page 5)       the Ridge sits above a sea of fog at 1,200 feet
  26-32  f5      SIX MILES           (page 6)       the real AVA map: Philo, Boonville, Ukiah; the Winkler ladder
  32-36  outro   five-card recap, then a smash cut back to frame 0 so the replay reads as continuous
PHOTOS (as the deck, credited in the caption): the graded cover (No-till-vineyard, CC0); the Roederer flute (Missvain, CC0);
the Esterlina view and the slope (Ethan Prater, CC BY 2.0); fog and redwoods (Mick Haupt, Pexels; NO place claimed); the Husch
vineyard at Philo (No-till-vineyard, CC0). The maps are the UC Davis AVA Project (CC0) and the US Census (public domain).
"""
import functools
import math
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
sys.path.insert(0, os.path.join(HERE, "..", "formats"))
import reel_lib  # noqa: E402
from reel_lib import (W, H, FPS, Photo, blit, blit_center, chip, clamp, darken, fill_poly, fill_rect, finish,  # noqa: E402
                      in_cubic, in_out_cubic, letters, out_back, out_cubic, out_expo, prog, round_rect, sheen,
                      stroke_path, text, text_width, vgrad)

# Text layers are rasterized by PIL on every call; the same lines repeat every frame, so cache them (read-only use).
reel_lib.text_layer = functools.lru_cache(maxsize=1024)(reel_lib.text_layer)

# ------------------------------------------------------------------ palette: the series' own (FFFA), made cinematic
INK = (12, 10, 14)            # the near-black ground (the deck's ink block, pushed down for the grade)
PAPER = (251, 249, 244)
COBALT = (28, 74, 172)        # the series cobalt (grid mark, rules, bars)
COBALT_HI = (74, 122, 240)    # the same hue, lit: for glows and anything that must read on dark
YELLOW = (255, 197, 47)       # the series yellow: the headline color
AMBER = (255, 160, 56)
ICE = (150, 205, 255)
GREEN = (150, 196, 70)

_PH = {}


def ph(name):
    if name not in _PH:
        _PH[name] = Photo(name, 1.3)
    return _PH[name]


def bgc(c):
    f = np.empty((H, W, 3), np.float32)
    f[:] = c
    return f


# ------------------------------------------------------------------ camera: shake, punch, speed
def shake(t, amp=1.0, seed=0.0):
    """Smooth handheld offsets (about +-1 each); the caller scales them. Sums of incommensurate sines, so no loop is visible."""
    return (amp * (0.6 * math.sin(2 * math.pi * 0.9 * t + seed) + 0.4 * math.sin(2 * math.pi * 2.3 * t + 1.7 + seed)),
            amp * (0.6 * math.sin(2 * math.pi * 1.1 * t + 2.1 + seed) + 0.4 * math.sin(2 * math.pi * 2.9 * t + 0.4 + seed)))


def punch(u, t0, amp=0.12, tau=0.16):
    """A snap zoom on a beat: scale impulse that decays."""
    return 1.0 + amp * math.exp(-(u - t0) / tau) if u >= t0 else 1.0


def shot(name, zoom=1.0, fx=0.5, fy=0.5, t=0.0, sh=0.0, seed=0.0):
    dx, dy = shake(t, sh, seed)
    return ph(name).view(zoom, fx + dx * 0.012, fy + dy * 0.012)


def desat(f, a):
    g = (f[..., 0] * 0.299 + f[..., 1] * 0.587 + f[..., 2] * 0.114)[..., None]
    f[:] = f * (1 - a) + g * a


def flash(f, a, col=(255, 244, 226)):
    if a > 0.004:
        f[:] = f * (1 - a) + np.array(col, np.float32) * a


# ------------------------------------------------------------------ the grade (8-bit lookup tables: cheap per frame)
def _make_lut():
    x = np.linspace(0, 1, 256)
    s = x + 0.20 * np.sin(2 * math.pi * (x - 0.5)) * (1 - np.abs(2 * x - 1)) * 0.9      # an S curve with crushed blacks
    s = np.clip((s - 0.03) / 0.97, 0, 1)
    r = np.clip(s ** 1.06 * 1.05 + 0.004, 0, 1)                    # amber in the highlights
    g = np.clip(s ** 1.00 * 1.00, 0, 1)
    b = np.clip(s ** 0.96 * 0.93 + 0.045 * (1 - s) ** 2, 0, 1)    # teal in the shadows
    lut = np.stack([r, g, b], axis=-1) * 255
    return np.clip(lut, 0, 255).astype(np.uint8)[:, None, :]


_LUT = _make_lut()


def grade(img8):
    """Teal shadows, amber highlights, an S curve, a little saturation. img8: uint8 RGB."""
    out = cv2.LUT(img8, _LUT)
    gray = cv2.cvtColor(out, cv2.COLOR_RGB2GRAY)
    g3 = cv2.merge([gray, gray, gray])
    return cv2.addWeighted(out, 1.16, g3, -0.16, 0)


def halation(f, strength=0.22):
    """Highlights bloom warm into the dark: down-blur-up on the bright part (8 ms)."""
    small = cv2.resize(f, (W // 8, H // 8), interpolation=cv2.INTER_AREA)
    hi = np.clip(small - 170, 0, None) * (255.0 / 85.0)
    hi = cv2.GaussianBlur(hi, (0, 0), 5)
    up = cv2.resize(hi, (W, H), interpolation=cv2.INTER_LINEAR)
    f += up * np.array((1.0, 0.62, 0.30), np.float32) * strength


def fringe(img8, px=2):
    """Chromatic fringing: red and blue planes pulled apart toward the frame's edges."""
    out = img8.copy()
    out[:, px:, 0] = img8[:, :-px, 0]
    out[:, :-px, 2] = img8[:, px:, 2]
    return out


_RNG = np.random.default_rng(5)


def dust(img8, fi):                                 # (no longer called: the grain and dust were removed)
    """A few specks and one hairline scratch now and then: the film is physical."""
    rg = np.random.default_rng(1000 + fi)
    for _ in range(int(rg.integers(2, 6))):
        x, y, r = int(rg.integers(0, W)), int(rg.integers(0, H)), int(rg.integers(1, 3))
        cv2.circle(img8, (x, y), r, (225, 220, 210), -1, cv2.LINE_AA)
    if rg.random() < 0.04:
        x = int(rg.integers(60, W - 60))
        y0 = int(rg.integers(0, H // 2))
        cv2.line(img8, (x, y0), (x + int(rg.integers(-3, 4)), y0 + int(rg.integers(120, 420))), (205, 200, 192), 1, cv2.LINE_AA)
    return img8


_DITHER = ((np.random.default_rng(11).random((H, W, 1)) + np.random.default_rng(12).random((H, W, 1)) - 1.0) * 0.9).astype(np.float32)


def post(f, fi, t):
    """float frame -> graded, fringed uint8 frame (vignette from the shared finish()). NO film grain and NO dust or scratches
    (Steve: the grain static was distracting). A FIXED dither of about one level, the same every frame, so it cannot read as static,
    stops the slow dark gradients from banding now that the grain no longer dithers them."""
    halation(f)
    f += _DITHER
    out = finish(f, fi, grain=0.0)
    out = grade(out)
    return fringe(out, 2)


# ------------------------------------------------------------------ the series icon and UI furniture
_ICON = {}


def icon_layer(size, color=PAPER, badge=COBALT_HI):
    """The FFFA checklist icon, drawn by the format's own function so it is the exact mark (premultiplied RGBA)."""
    key = (size, color, badge)
    if key not in _ICON:
        from fff_facts import _checklist_icon
        pad = 6
        im = Image.new("RGBA", (size + 2 * pad, size + 2 * pad), (0, 0, 0, 0))
        _checklist_icon(ImageDraw.Draw(im), pad, pad, size, color, badge_color=badge)
        a = np.asarray(im, np.float32) / 255.0
        lay = np.empty(a.shape, np.float32)
        lay[..., :3] = a[..., :3] * 255 * a[..., 3:4]
        lay[..., 3] = a[..., 3]
        _ICON[key] = lay
    return _ICON[key]


def brackets(f, x0, y0, x1, y1, p, size=70, thick=8, col=YELLOW, alpha=1.0):
    """Viewfinder corners that snap in from outside (p: 0 -> 1)."""
    if p <= 0:
        return
    k = (1 - out_expo(p)) * 60
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        ox, oy = cx - sx * k, cy - sy * k
        fill_rect(f, min(ox, ox + sx * size), min(oy, oy + sy * thick), max(ox, ox + sx * size), max(oy, oy + sy * thick), col, alpha)
        fill_rect(f, min(ox, ox + sx * thick), min(oy, oy + sy * size), max(ox, ox + sx * thick), max(oy, oy + sy * size), col, alpha)


def timecode(f, x, y, t, label="REC", alpha=0.9):
    """A running timecode with a blinking REC dot: the freeze-frame's evidence furniture."""
    if int(t * 2) % 2 == 0:
        cv2.circle(f, (int(x), int(y - 14)), 11, (235, 40, 40), -1, cv2.LINE_AA)
    text(f, label, "condb", 34, PAPER, x + 26, y, alpha=alpha, tracking=2)
    fr = int(t * FPS) % FPS
    sec = int(t) % 60
    text(f, f"00:{sec:02d}:{fr:02d}", "condb", 34, PAPER, x + 140, y, alpha=alpha, tracking=2)


def hud(f, idx, u, D, show=1.0):
    """The persistent progress element (spec v2, category 1): the icon, FACT 0N / 05, five segments that fill one by one.
    Fixed on every fact scene; the current segment fills over the scene."""
    if show <= 0:
        return
    y = 300
    ic = icon_layer(84)
    blit(f, ic, 56 - 6, y - 70 - 6, show)
    text(f, "FACT", "condb", 40, PAPER, 160, y - 36, alpha=show * 0.9, tracking=4)
    text(f, f"0{idx}", "cond", 76, YELLOW, 160, y + 26, alpha=show, tracking=2)
    text(f, "/ 05", "condb", 42, PAPER, 268, y + 24, alpha=show * 0.75, tracking=3)
    seg_w, gap, x0 = 74, 10, W - 56 - (5 * 74 + 4 * 10)
    for i in range(5):
        x = x0 + i * (seg_w + gap)
        round_rect(f, x, y - 14, x + seg_w, y + 6, 10, (255, 255, 255), 0.18 * show)
        fill = 1.0 if i < idx - 1 else (out_cubic(prog(u, 0.3, D - 0.6)) if i == idx - 1 else 0.0)
        if fill > 0:
            round_rect(f, x, y - 14, x + seg_w * fill, y + 6, 10, YELLOW, show)


def source_tag(f, txt, u, t0=0.4, y=1546):
    """The evidence tag: where the fact comes from. Rises in on its own beat."""
    q = out_cubic(prog(u, t0, t0 + 0.3))
    if q <= 0:
        return
    tw = text_width(txt, "condb", 34, 3) + 56
    round_rect(f, 56, y - 36, 56 + tw, y + 22, 10, (0, 0, 0), 0.55 * q)
    fill_rect(f, 56, y - 36, 64, y + 22, YELLOW, q)
    text(f, txt, "condb", 34, PAPER, 84, y + 3, tracking=3, alpha=q, dy=14 * (1 - q))


def fit_size(txt, fname, max_w, hi=300, lo=40, tracking=0):
    return next((s for s in range(hi, lo, -2) if text_width(txt, fname, s, tracking) <= max_w), lo)


def slam(f, txt, fname, size, col, x, y, u, t0, align="center", tracking=0, glow=None, dur=0.22):
    """A line that slams in: letters arrive large and settle, staggered 20 ms apart."""
    def a(i, n):
        s = t0 + 0.02 * i
        p = prog(u, s, s + dur)
        if p <= 0:
            return dict(alpha=0)
        return dict(alpha=out_cubic(prog(u, s, s + 0.06)), scale=1.9 - 0.9 * out_expo(p), mblur=int(26 * (1 - p)), mangle=90)
    return letters(f, txt, fname, size, col, x, y, a, align=align, tracking=tracking, glow=glow)


# ================================================================== SCENE 0: TITLE (0-4 s)
COVER = "fffa_mendocino_cover.jpg"
KICKER = "FIVE FASCINATING FACTS ABOUT"
TSIZE = fit_size("Mendocino", "serif", W - 120, hi=330)
MONTAGE = [("us_mendo_roederer_flute_cc0.jpg", 0.55, 0.50, "CHAMPAGNE", "01"),
           ("us_mendo_av_esterlina_view_prater.jpg", 0.50, 0.55, "4 PERCENT", "02"),
           ("us_mendo_av_slope_prater.jpg", 0.50, 0.55, "FROST", "03"),
           ("us_mendo_fog_redwoods_pexels.jpg", 0.50, 0.50, "ABOVE THE FOG", "04"),
           ("us_mendo_husch_philo_cc0.jpg", 0.50, 0.50, "HEAT CLASS", "05"),
           (COVER, 0.50, 0.55, "MENDOCINO", "")]


def hook_card(f, u, sheen_p=0.0):
    """The title page. It opens the Reel (0-2 s) and closes it (the last 2 s): the SAME page and the same 2-second animation.
    The slow breath returns to 1.0, so the bumper begins and ends on one frame, and the replay is seamless. Nothing animates in:
    frame 0 is the whole hook."""
    z = 1.0 + 0.022 * math.sin(math.pi * clamp(u / 2.0, 0, 1))
    f[:] = ph(COVER).view(z, 0.5, 0.5)
    darken(f, vgrad(760, 1500, 0.0, 0.80), (4, 6, 14))
    darken(f, vgrad(0, 420, 0.45, 0.0), (4, 6, 14))
    blit(f, icon_layer(150), 50, 1190)
    text(f, "FIVE FASCINATING", "cond", 70, PAPER, 226, 1262, tracking=5)       # the deck's own two-line kicker
    text(f, "FACTS ABOUT", "cond", 70, PAPER, 226, 1336, tracking=5)
    text(f, "Mendocino", "serif", TSIZE, YELLOW, 54, 1550, glow=(18, (255, 160, 40), 0.45))
    sheen(f, "Mendocino", "serif", TSIZE, 54, 1550, sheen_p, band=130, strength=0.8)


def s_title(u, ur=0.0, D=4.0, S=1.0):
    f = np.zeros((H, W, 3), np.float32)
    if u < 2.0:                                                 # the opening bumper: the title page, held 2 s
        hook_card(f, u, sheen_p=prog(u, 0.4, 1.4))
        return f
    if u < 3.5:                                                 # the montage: six shots on 16ths, a word apiece
        v = u - 2.0
        k = min(int(v / 0.25), 5)
        w = v - 0.25 * k
        name, fx, fy, word, num = MONTAGE[k]
        z = 1.34 - 0.30 * out_expo(prog(w, 0, 0.2))
        f[:] = shot(name, z, fx, fy, t=u, sh=1.0, seed=k * 1.3)
        darken(f, vgrad(900, 1500, 0.0, 0.45), (4, 6, 14))
        sz = fit_size(word, "cond", W - 110, hi=250, tracking=4)
        col = YELLOW if k % 2 == 0 else PAPER
        fill_rect(f, 0, 820, W, 1130, (4, 6, 14), 0.62)
        fill_rect(f, 0, 820, W, 826, YELLOW, 0.9)
        fill_rect(f, 0, 1124, W, 1130, YELLOW, 0.9)
        text(f, word, "cond", sz, col, W / 2, 1010, align="center", tracking=4, scale=1.0 + 0.10 * (1 - out_expo(prog(w, 0, 0.12))),
             glow=(14, (255, 170, 40), 0.4))
        if num:
            text(f, num, "cond", 190, PAPER, 60, 560, alpha=0.9, tracking=2)
        fill_rect(f, 0, 0, W, H, (255, 255, 255), 0.55 * (1 - prog(w, 0, 0.05)) if w < 0.05 else 0.0)
        return f
    v = u - 3.5                                                 # pre-roll: the numerals scatter, the strobe
    f[:] = bgc(INK)
    for i in range(5):
        a = 0.9 - 0.9 * prog(v, 0.0, 0.5)
        ang = (i - 2) * 0.55
        text(f, f"0{i + 1}", "cond", 260, COBALT_HI if i % 2 else YELLOW, W / 2 + (i - 2) * 190 * (1 + 3 * v * v), 960 + 600 * v * v * (1 if i % 2 else -1),
             align="center", alpha=a, rot=ang * v * 12)
    flash(f, 0.95 if int(v * 16) % 2 == 0 and v > 0.25 else 0.0)
    return f


# ================================================================== helpers for the fact scenes
def lgrad(f, y0, y1, c0, c1, x0=0, x1=W):
    """A vertical gradient rectangle."""
    y0, y1 = max(int(y0), 0), min(int(y1), H)
    if y1 <= y0:
        return
    t = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
    f[y0:y1, x0:x1] = np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t


def dashed(f, x0, y0, x1, y1, col, width=4, dash=26, gap=16, p=1.0, alpha=1.0):
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1 or p <= 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    d = 0.0
    while d < L * p:
        e = min(d + dash, L * p)
        a = np.array([x0 + ux * d, y0 + uy * d]); b = np.array([x0 + ux * e, y0 + uy * e])
        if alpha >= 0.99:
            cv2.line(f, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), col, width, cv2.LINE_AA)
        else:
            stroke_path(f, np.array([a, b]), col, width, alpha)
        d += dash + gap


def snowflake(f, cx, cy, r, col, alpha=1.0, rot=0.0):
    for k in range(6):
        a = math.radians(60 * k + rot)
        ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        stroke_path(f, np.array([[cx, cy], [ex, ey]]), col, max(2, r * 0.09), alpha)
        for fr in (0.5, 0.75):
            bx, by = cx + r * fr * math.cos(a), cy + r * fr * math.sin(a)
            for sg in (-1, 1):
                b = a + sg * math.radians(48)
                stroke_path(f, np.array([[bx, by], [bx + r * 0.26 * math.cos(b), by + r * 0.26 * math.sin(b)]]), col, max(2, r * 0.07), alpha)


def pin(f, cx, cy, q, col, ring=PAPER, r=20):
    if q <= 0:
        return
    rr = r * q
    cv2.circle(f, (int(cx), int(cy)), int(rr * 2.4), tuple(int(c) for c in col), 3, cv2.LINE_AA)       # a halo ring
    cv2.circle(f, (int(cx), int(cy)), int(rr), tuple(int(c) for c in col), -1, cv2.LINE_AA)
    cv2.circle(f, (int(cx), int(cy)), int(rr), ring, max(3, int(rr * 0.28)), cv2.LINE_AA)


def pill(f, txt, x, y, q, fill, ink, size=40, align="left", tracking=2):
    """A rounded label that pops (q: 0 -> 1). Returns its (x0, x1)."""
    if q <= 0:
        return x, x
    tw = text_width(txt, "cond", size, tracking) + 44
    x0 = x if align == "left" else x - tw / 2
    h = size * 0.82
    round_rect(f, x0, y - h * q, x0 + tw, y + h * 0.48 * q, int(h * 0.5), fill, 1.0)
    text(f, txt, "cond", size, ink, x0 + 22, y + size * 0.20, tracking=tracking, alpha=min(1, q * 1.3), scale=q if q < 1 else 1.0)
    return x0, x0 + tw


_GLOW = {}


def cached_glow(key, center, radius, sigma, color):
    """A big soft glow that never changes: blurred once (a full-frame sigma-40 blur costs over a second a frame)."""
    if key not in _GLOW:
        g = np.zeros((H, W, 3), np.float32)
        cv2.circle(g, center, radius, color, -1, cv2.LINE_AA)
        _GLOW[key] = cv2.GaussianBlur(g, (0, 0), sigma)
    return _GLOW[key]


_NOISE = cv2.resize(cv2.GaussianBlur(np.random.default_rng(9).random((40, 90)).astype(np.float32), (0, 0), 2.2), (W * 2, 560),
                    interpolation=cv2.INTER_CUBIC)
_NOISE = (_NOISE - _NOISE.min()) / (_NOISE.max() - _NOISE.min())

# ================================================================== SCENE 1: THE CHAMPAGNE JOB (4-8 s)
FLUTE = "us_mendo_roederer_flute_cc0.jpg"
_BUB = [(0.30 + 0.40 * np.random.default_rng(i).random(), 0.18 + 0.50 * np.random.default_rng(i + 40).random(),
         np.random.default_rng(i + 80).random(), 2 + 5 * np.random.default_rng(i + 120).random()) for i in range(54)]
_BOKEH = [(np.random.default_rng(i + 200).random(), 0.05 + 0.10 * np.random.default_rng(i + 240).random(),
           np.random.default_rng(i + 280).random(), 22 + 50 * np.random.default_rng(i + 320).random()) for i in range(10)]


def s_f1(u, ur=0.0, D=6.0):
    f = np.zeros((H, W, 3), np.float32)
    z = (1.30 - 0.20 * out_expo(prog(u, 0.0, 0.5))) * punch(u, 0.5, 0.07, 0.12) * (1 + 0.012 * max(u - 0.5, 0))   # a slow push after the freeze
    f[:] = shot(FLUTE, z, 0.50, 0.42, t=min(u, 0.5), sh=(1.8 if u < 0.5 else 0.0), seed=2.0)
    desat(f, 0.50 * out_cubic(prog(u, 0.5, 0.85)))
    darken(f, vgrad(820, 1500, 0.0, 0.86), (4, 6, 14))
    darken(f, vgrad(0, 400, 0.6, 0.0), (4, 6, 14))
    for bx, spd, ph0, r in _BUB:
        s = (ur * spd * 0.9 + ph0) % 1.0
        cv2.circle(f, (int(bx * W + 8 * math.sin(6 * s + ph0 * 9)), int(1010 - s * 460)), int(r), (255, 244, 220), -1, cv2.LINE_AA)
    for bx, spd, ph0, r in _BOKEH:
        s = (ur * spd * 0.35 + ph0) % 1.0
        ov = f.copy()
        cv2.circle(ov, (int(bx * W), int(1500 - s * 1300)), int(r), (255, 190, 90), -1, cv2.LINE_AA)
        f[:] = f * 0.9 + ov * 0.1
    hud(f, 1, u, D)
    if u >= 0.5:
        brackets(f, 120, 470, W - 120, 1085, prog(u, 0.5, 0.75), size=84, thick=8)
        timecode(f, 64, 396, 4.5)
        q = out_back(prog(u, 0.8, 1.1), 2.0)
        if q > 0:
            dashed(f, 330, 640, 480, 700, YELLOW, 4, 14, 10, p=q)
            pill(f, "ROEDERER ESTATE", 70, 640, q, YELLOW, INK, size=50)
    ts = fit_size("THE CHAMPAGNE JOB", "cond", W - 100, hi=150, tracking=2)
    slam(f, "THE CHAMPAGNE JOB", "cond", ts, YELLOW, W / 2, 1230, u, 1.0, tracking=2, glow=(14, (255, 170, 40), 0.35))
    sheen(f, "THE CHAMPAGNE JOB", "cond", ts, W / 2, 1230, prog(u, 1.5, 2.1), align="center", band=110, tracking=2, strength=0.75)
    if u >= 1.4:
        a = out_cubic(prog(u, 1.4, 1.6))
        text(f, str(int(1900 + 82 * out_cubic(prog(u, 1.4, 2.2)))), "cond", 150, PAPER, 60, 1380, alpha=a, tracking=2)
        text(f, "FOUNDED BY A", "condb", 58, PAPER, 372, 1326, alpha=a, tracking=2)
        text(f, "CHAMPAGNE HOUSE", "condb", 58, YELLOW, 372, 1388, alpha=a, tracking=2)
    if u >= 2.8:
        a = out_cubic(prog(u, 2.8, 3.1))
        fill_rect(f, 60, 1450, 68, 1568, YELLOW, a)
        text(f, "MANY WINERIES BUY ANDERSON", "condb", 60, PAPER, 90, 1500, alpha=a, dy=14 * (1 - a), tracking=1)
        text(f, "VALLEY GRAPES FOR SPARKLING.", "condb", 60, PAPER, 90, 1564, alpha=a, dy=14 * (1 - a), tracking=1)
    return f


# ================================================================== SCENE 2: THE FOUR PERCENT (8-14 s)
TS, TG = 70, 8
GX0, GY0 = (W - (10 * TS + 9 * TG)) // 2, 540
LIT = [(1, 7), (3, 2), (6, 8), (8, 4)]
TILE = (30, 33, 44)


def tile_xy(r, c):
    return GX0 + c * (TS + TG), GY0 + r * (TS + TG)


def s_f2(u, ur=0.0, D=8.0):
    f = bgc((8, 9, 16))
    lgrad(f, 0, H, (10, 12, 26), (6, 7, 12))
    for gx in range(0, W, 90):
        fill_rect(f, gx, 0, gx + 1, H, COBALT, 0.10)
    hud(f, 2, u, D)
    slam(f, "THE FOUR PERCENT", "cond", fit_size("THE FOUR PERCENT", "cond", W - 100, hi=112, tracking=3), YELLOW, W / 2, 450, u, 0.1,
         tracking=3, glow=(12, (255, 170, 40), 0.3))
    county = u >= 4.6
    cap = "EVERY TILE = 1% OF MENDOCINO COUNTY" if county else "EVERY TILE = 1% OF ANDERSON VALLEY"
    text(f, cap, "condb", 50, ICE, W / 2, 510, align="center", tracking=2, alpha=out_cubic(prog(u, 0.4, 0.7)))
    wave = 22 * prog(u, 0.45, 1.5)
    for r in range(10):
        for c in range(10):
            x, y = tile_xy(r, c)
            a = out_cubic(prog(u, 0.25 + (r + c) * 0.014, 0.45 + (r + c) * 0.014))
            if a <= 0:
                continue
            boost = math.exp(-((r + c) - wave) ** 2 / 5.0) * (1 if u < 1.6 else 0)
            col = np.array(TILE, np.float32) + np.array(COBALT_HI, np.float32) * boost * 0.9
            fill_rect(f, x, y, x + TS, y + TS, tuple(col), a)
            fill_rect(f, x, y, x + TS, y + 3, (255, 255, 255), 0.07 * a)
    lit_layer = np.zeros((H, W, 3), np.float32)
    n_lit = 0
    if not county:
        for k, (r, c) in enumerate(LIT):
            t0 = 1.7 + 0.22 * k
            q = out_back(prog(u, t0, t0 + 0.28), 2.6)
            if q <= 0:
                continue
            n_lit += 1
            x, y = tile_xy(r, c)
            cx, cy, h = x + TS / 2, y + TS / 2, TS / 2 * q
            fill_rect(lit_layer, cx - h, cy - h, cx + h, cy + h, YELLOW, 1.0)
            fill_rect(f, cx - h, cy - h, cx + h, cy + h, YELLOW, 1.0)
            fill_rect(f, cx - h, cy - h, cx + h, cy - h * 0.1, (255, 255, 255), 0.30)
        if n_lit:
            f += cv2.GaussianBlur(lit_layer, (0, 0), 16) * 0.9
    else:
        x, y = tile_xy(4, 5)
        q = out_cubic(prog(u, 4.9, 5.5))
        fill_rect(f, x, y + TS * (1 - 0.7 * q), x + TS, y + TS, YELLOW, 1.0)
        gl = np.zeros((H, W, 3), np.float32)
        fill_rect(gl, x, y + TS * (1 - 0.7 * q), x + TS, y + TS, YELLOW, 1.0)
        f += cv2.GaussianBlur(gl, (0, 0), 14) * 0.9
        brackets(f, x - 24, y - 24, x + TS + 24, y + TS + 24, prog(u, 4.9, 5.2), size=26, thick=5)
    if not county:
        pct = 4.0 * out_cubic(prog(u, 1.7, 2.7))
        a = out_cubic(prog(u, 1.7, 1.9))
        text(f, f"ABOUT {pct:.0f}%", "cond", 190, YELLOW, W / 2, 1470, align="center", alpha=a, tracking=2, glow=(16, (255, 170, 40), 0.4))
        text(f, "OF ANDERSON VALLEY IS VINES.", "condb", 62, PAPER, W / 2, 1546, align="center", alpha=out_cubic(prog(u, 2.6, 2.9)), tracking=2)
        sheen(f, "ABOUT 4%", "cond", 190, W / 2, 1470, prog(u, 2.8, 3.4), align="center", band=120, tracking=2, strength=0.6)
    else:
        a = out_cubic(prog(u, 4.9, 5.3))
        text(f, "UNDER 1%", "cond", 190, YELLOW, W / 2, 1470, align="center", alpha=a, tracking=2, glow=(16, (255, 170, 40), 0.4))
        text(f, "OF THE WHOLE COUNTY IS VINES.", "condb", 62, PAPER, W / 2, 1546, align="center", alpha=out_cubic(prog(u, 5.4, 5.7)), tracking=2)
    return f


# ================================================================== SCENE 3: THE FROST POCKET (14-20 s)
def valley_y(x, y_floor=1330.0, y_top=640.0, half=120.0):
    d = np.abs(np.asarray(x, np.float64) - W / 2)
    p = np.clip((d - half) / (W / 2 - half), 0, 1)
    p = p * p * (3 - 2 * p)
    return y_floor - (y_floor - y_top) * p


_XS = np.arange(0, W + 1, 6, dtype=np.float64)
_STARS = [(np.random.default_rng(i).random() * W, 330 + np.random.default_rng(i + 50).random() * 380, 1 + np.random.default_rng(i + 90).random() * 2)
          for i in range(70)]
_COLD = [(np.random.default_rng(i + 500).random(), np.random.default_rng(i + 540).random(), (-1) ** i) for i in range(64)]


def s_f3(u, ur=0.0, D=6.0):
    f = np.zeros((H, W, 3), np.float32)
    lgrad(f, 0, H, (4, 8, 24), (22, 40, 86))
    for sx, sy, sr in _STARS:                                        # a clear, still night: the radiative-frost sky
        tw = 0.6 + 0.4 * math.sin(ur * 2.2 + sx)
        cv2.circle(f, (int(sx), int(sy)), int(sr), (255, 250, 235), -1, cv2.LINE_AA) if tw > 0.55 else None
    cv2.circle(f, (880, 560), 150, (60, 90, 150), -1, cv2.LINE_AA)
    f += cached_glow("moon", (880, 560), 70, 38, (255, 244, 220)) * 0.9
    cv2.circle(f, (880, 560), 56, (250, 246, 232), -1, cv2.LINE_AA)
    dx, dy = shake(ur, 4.0, 3.0)
    ys = valley_y(_XS) + dy * 0.4
    far = np.column_stack([_XS, valley_y(_XS, 1280, 600, 160) - 70 + dy * 0.2])
    fill_poly(f, np.vstack([far, [[W, H], [0, H]]]), (36, 52, 92), 1.0)
    land = np.column_stack([_XS, ys])
    fill_poly(f, np.vstack([land, [[W, H], [0, H]]]), (24, 32, 52), 1.0)
    darken(f, vgrad(1330, 1700, 0.0, 0.75), (4, 6, 14))
    stroke_path(f, land, (170, 205, 255), 4, 0.85, glow=8, glow_color=(120, 170, 255))
    # the vines: on the slopes (and three on the floor: "most", not "all")
    glow_vines = out_cubic(prog(u, 3.6, 4.3))
    vine_pts = []
    for x in list(range(140, 450, 22)) + list(range(630, 940, 22)):
        for lvl in (0, 1):
            xx = x + 11 * lvl
            yy = float(valley_y(xx)) + dy * 0.4 - 16 - 20 * lvl
            vine_pts.append((xx, yy))
    for xx in (480, 540, 600):
        vine_pts.append((xx, float(valley_y(xx)) + dy * 0.4 - 16))
    vg = np.zeros_like(f)
    for xx, yy in vine_pts:
        col = GREEN
        cv2.line(f, (int(xx), int(yy)), (int(xx), int(yy + 16)), col, 4, cv2.LINE_AA)
        cv2.circle(f, (int(xx), int(yy)), 5, (205, 235, 120), -1, cv2.LINE_AA)
        if glow_vines > 0 and abs(xx - W / 2) > 120:
            cv2.circle(vg, (int(xx), int(yy)), 9, (200, 255, 110), -1, cv2.LINE_AA)
    if glow_vines > 0:
        f += cv2.GaussianBlur(vg, (0, 0), 10) * (0.9 * glow_vines)
    # cold air runs downhill
    for ph0, sp, sgn in _COLD:
        s = (ur * (0.13 + 0.12 * sp) + ph0) % 1.0
        x0 = W / 2 + sgn * (150 + 330 * sp)
        x = x0 + (W / 2 - x0) * s ** 1.4
        y = float(valley_y(x)) + dy * 0.4 - 8
        a = math.sin(math.pi * s) ** 0.8 * 0.75 * out_cubic(prog(u, 0.3, 1.0))
        x_prev = x0 + (W / 2 - x0) * max(s - 0.03, 0) ** 1.4
        y_prev = float(valley_y(x_prev)) + dy * 0.4 - 8
        x_prev = x0 + (W / 2 - x0) * max(s - 0.07, 0) ** 1.4
        y_prev = float(valley_y(x_prev)) + dy * 0.4 - 8
        stroke_path(f, np.array([[x_prev, y_prev], [x, y]]), (200, 232, 255), 7, a)
    # the pool of cold air rises on the valley floor
    depth = 175 * out_cubic(prog(u, 0.9, 3.2))
    if depth > 4:
        ysurf = 1330 - depth + dy * 0.4
        wob = 5 * np.sin(_XS / 38.0 + ur * 2.2)
        top = ysurf + wob
        pts_top, pts_bot = [], []
        for x, yt, yl in zip(_XS, top, ys):
            if yl > yt:
                pts_top.append((x, yt)); pts_bot.append((x, yl))
        if len(pts_top) > 2:
            poly = np.array(pts_top + pts_bot[::-1], np.float32)
            fill_poly(f, poly, (96, 160, 255), 0.42)
            stroke_path(f, np.array(pts_top), (200, 230, 255), 4, 0.9)
        sf = 0.5 + 0.5 * math.sin(ur * 3.0)
        snowflake(f, W / 2, 1330 - depth * 0.45, 52, (230, 245, 255), alpha=0.95, rot=ur * 14)
    hud(f, 3, u, D)
    slam(f, "THE FROST POCKET", "cond", fit_size("THE FROST POCKET", "cond", W - 100, hi=112, tracking=3), YELLOW, W / 2, 470, u, 0.1,
         tracking=3, glow=(12, (255, 170, 40), 0.3))
    q = out_back(prog(u, 1.7, 2.0), 2.0)
    if q > 0:
        dashed(f, 540, 1356, 540, 1330 - depth * 0.5 + 30, ICE, 4, 12, 10, p=q)
        pill(f, "FROST RISK", W / 2, 1392, q, ICE, INK, size=48, align="center")
    q = out_back(prog(u, 3.7, 4.0), 2.0)
    if q > 0:
        dashed(f, 200, 1010, 262, 960, GREEN, 4, 12, 10, p=q)
        pill(f, "MOST VINES", 60, 1052, q, GREEN, INK, size=48)
    if u < 3.4:
        a = out_cubic(prog(u, 1.2, 1.5))
        fill_rect(f, 0, 1424, W, 1584, (4, 6, 14), 0.70 * a)
        text(f, "COLD AIR IS DENSE:", "condb", 66, PAPER, 60, 1492, alpha=a, tracking=2)
        text(f, "IT SETTLES IN LOW GROUND.", "condb", 66, YELLOW, 60, 1562, alpha=a, tracking=2)
    else:
        a = out_cubic(prog(u, 3.5, 3.8))
        fill_rect(f, 0, 1424, W, 1584, (4, 6, 14), 0.70 * a)
        text(f, "MOST VINES SIT ON THE SLOPES,", "condb", 66, PAPER, 60, 1492, alpha=a, tracking=1)
        text(f, "WHERE COLD AIR CAN DRAIN AWAY.", "condb", 66, YELLOW, 60, 1562, alpha=a, tracking=1)
    return f


# ================================================================== SCENE 4: ABOVE THE FOG (20-26 s)
FOG_Y = 1070.0
_PEAKS = [(150, 835, 1.25), (470, 905, 0.95), (770, 790, 1.4), (1010, 880, 1.05)]


def _peak(cx, top, wid, base=1240):
    return np.array([[cx - 210 * wid, base], [cx - 95 * wid, top + 70], [cx - 22 * wid, top + 6], [cx + 18 * wid, top],
                     [cx + 80 * wid, top + 50], [cx + 215 * wid, base]], np.float32)


def s_f4(u, ur=0.0, D=6.0):
    f = np.zeros((H, W, 3), np.float32)
    lgrad(f, 0, int(FOG_Y) + 40, (8, 18, 52), (255, 170, 96))
    lgrad(f, int(FOG_Y) + 40, H, (20, 26, 44), (8, 10, 18))
    dx, dy = shake(ur, 5.0, 7.0)
    f += cached_glow("sun", (800, 930), 150, 70, (255, 210, 130)) * 1.2           # (the disc below still moves with the shake)
    cv2.circle(f, (800, 930 + int(dy)), 74, (255, 238, 196), -1, cv2.LINE_AA)
    far = np.array([[0, 1100], [0, 960], [130, 900], [260, 950], [420, 880], [600, 940], [720, 895], [900, 950], [W, 905], [W, 1100]], np.float32)
    fill_poly(f, far, (52, 66, 112), 1.0)
    # fog bank 1 (behind the near ridges), drifting
    off = int(ur * 46) % W
    tex = _NOISE[:, off:off + W]
    ys_ = np.arange(H, dtype=np.float32)[:, None]
    ramp = np.clip((ys_ - (FOG_Y - 40)) / 90.0, 0, 1)
    fog_a = np.clip(ramp * (0.78 + 0.35 * np.pad(tex, ((int(FOG_Y) - 300, H - int(FOG_Y) - 260), (0, 0)), mode="edge")[:H]), 0, 1)[..., None]
    f[:] = f * (1 - fog_a * 0.9) + np.array((226, 220, 224), np.float32) * fog_a * 0.9
    # the near ridgetops: islands above the fog, a few vines on each
    for k, (cx, top, wid) in enumerate(_PEAKS):
        q = out_cubic(prog(u, 0.2 + 0.12 * k, 0.9 + 0.12 * k))
        if q <= 0:
            continue
        pk = _peak(cx + dx, top + dy + (1 - q) * 160, wid)
        fill_poly(f, pk, (14, 18, 30), 1.0)
        stroke_path(f, pk[1:5], (255, 196, 120), 3, 0.7 * q)
        for j in range(4):
            vx = cx + dx - 36 + j * 24 + 4 * k
            vy = top + dy + (1 - q) * 160 + 28 - 4 * abs(j - 1.5)
            cv2.circle(f, (int(vx), int(vy)), 7, (205, 235, 120), -1, cv2.LINE_AA)
    # fog bank 2 in FRONT of the ridge bases: the sea
    ramp2 = np.clip((ys_ - (FOG_Y + 20)) / 70.0, 0, 1)
    off2 = int(ur * 70 + 400) % W
    tex2 = _NOISE[:, off2:off2 + W]
    fa2 = np.clip(ramp2 * (0.86 + 0.28 * np.pad(tex2, ((int(FOG_Y) - 280, H - int(FOG_Y) - 280), (0, 0)), mode="edge")[:H]), 0, 1)[..., None]
    f[:] = f * (1 - fa2) + np.array((214, 214, 226), np.float32) * fa2
    darken(f, vgrad(1130, 1330, 0.0, 0.92), (6, 8, 16))
    hud(f, 4, u, D)
    slam(f, "ABOVE THE FOG", "cond", fit_size("ABOVE THE FOG", "cond", W - 100, hi=112, tracking=3), YELLOW, W / 2, 470, u, 0.1, tracking=3,
         glow=(12, (255, 170, 40), 0.3))
    # the 1,200 ft line
    p = out_cubic(prog(u, 0.9, 1.6))
    dashed(f, 40, FOG_Y, 40 + 1000 * p, FOG_Y, YELLOW, 4, 22, 14)
    if p > 0.95:
        text(f, "1,200 FT", "cond", 62, YELLOW, W - 56, FOG_Y - 18, align="right", tracking=3, alpha=out_cubic(prog(u, 1.5, 1.8)))
    q = out_back(prog(u, 1.2, 1.5), 2.0)
    pill(f, "MENDOCINO RIDGE", 60, 770, q, YELLOW, INK, size=52)
    if u >= 1.6:
        a = out_cubic(prog(u, 1.7, 2.0))
        text(f, "ONLY LAND AT 1,200 FT", "condb", 66, PAPER, 60, 1334, alpha=a, tracking=2, dy=14 * (1 - a))
        text(f, "OR HIGHER COUNTS.", "condb", 66, PAPER, 60, 1400, alpha=a, tracking=2, dy=14 * (1 - a))
    if u >= 3.0:
        q = out_back(prog(u, 3.0, 3.35), 2.4)
        if q > 0:
            lab1, lab2 = "THE ONLY NON-CONTIGUOUS", "AVA IN THE U.S."
            w1 = text_width(lab1, "cond", 64, 2)
            round_rect(f, 52, 1432, 52 + w1 * q + 56, 1432 + 140 * q, 14, YELLOW, 1.0)
            text(f, lab1, "cond", 64, INK, 80, 1494, tracking=2, alpha=min(1, q * 1.3), scale=q)
            text(f, lab2, "cond", 64, INK, 80, 1556, tracking=2, alpha=min(1, q * 1.3), scale=q)
    return f


# ================================================================== SCENE 5: SIX MILES (26-32 s)
import mendo_fg_reel as fg  # noqa: E402  (the real AVA polygons and the county outline, shared with the Field Guide Reel)

_K = fg.K
_AVR5 = max(next(a for a in fg._AVA if a["name"] == "Anderson Valley")["rings"], key=len)
_CTY5 = max(fg._CTY["Mendocino"], key=len)
PANEL5 = (40, 510, W - 40, 1160)
_BB = (-123.66, -123.14, 38.95, 39.20)                              # lon0, lon1, lat0, lat1: the whole AVA, and Ukiah
_S5 = min((PANEL5[2] - PANEL5[0]) / ((_BB[1] - _BB[0]) * _K), (PANEL5[3] - PANEL5[1]) / (_BB[3] - _BB[2]))
_CX5, _CY5 = ((_BB[0] + _BB[1]) / 2) * _K, -((_BB[2] + _BB[3]) / 2)


def P5(lon, lat):
    return ((lon * _K - _CX5) * _S5 + (PANEL5[0] + PANEL5[2]) / 2, (-lat - _CY5) * _S5 + (PANEL5[1] + PANEL5[3]) / 2)


def _proj_ring(r):
    return np.column_stack([(r[:, 0] - _CX5) * _S5 + (PANEL5[0] + PANEL5[2]) / 2, (r[:, 1] - _CY5) * _S5 + (PANEL5[1] + PANEL5[3]) / 2])


TOWNS = dict(Philo=(-123.4447, 39.0657), Boonville=(-123.3661, 39.0093), Ukiah=(-123.2078, 39.1502))
HEAT = [(92, 170, 255), (110, 205, 215), (255, 205, 70), (255, 140, 52), (232, 60, 40)]


def _miles(a, b):
    dlat, dlon = (b[1] - a[1]), (b[0] - a[0]) * math.cos(math.radians((a[1] + b[1]) / 2))
    return math.hypot(dlat, dlon) * 69.0


def s_f5(u, ur=0.0, D=6.0):
    f = bgc((7, 9, 18))
    lgrad(f, 0, H, (8, 12, 30), (6, 7, 12))
    hud(f, 5, u, D)
    slam(f, "SIX MILES", "cond", fit_size("SIX MILES", "cond", W - 100, hi=124, tracking=3), YELLOW, W / 2, 462, u, 0.1, tracking=3,
         glow=(12, (255, 170, 40), 0.3))
    x0, y0, x1, y1 = PANEL5
    round_rect(f, x0, y0, x1, y1, 22, (14, 20, 44), 1.0)
    pa = np.ascontiguousarray(f[y0:y1, x0:x1])                       # draw the map into the panel only
    off = np.array([x0, y0])
    for g in range(0, x1 - x0, 80):
        fill_rect(pa, g, 0, g + 1, y1 - y0, COBALT, 0.12)
    for g in range(0, y1 - y0, 80):
        fill_rect(pa, 0, g, x1 - x0, g + 1, COBALT, 0.12)
    stroke_path(pa, _proj_ring(_CTY5) - off, (110, 140, 200), 2, 0.45)
    ring = _proj_ring(_AVR5) - off
    aq = out_cubic(prog(u, 0.2, 0.9))
    fill_poly(pa, ring, COBALT, 0.78 * aq)
    stroke_path(pa, ring, COBALT_HI, 4, 0.95 * aq, glow=10, glow_color=COBALT_HI)
    f[y0:y1, x0:x1] = pa
    pts = {k: P5(*v) for k, v in TOWNS.items()}
    cols = dict(Philo=HEAT[0], Boonville=HEAT[1], Ukiah=HEAT[2])      # Region I, II, and II-III (the boundary rung)
    names = dict(Philo="PHILO", Boonville="BOONVILLE", Ukiah="UKIAH")
    regs = dict(Philo="REGION I", Boonville="REGION II", Ukiah="REGIONS II–III")
    times = dict(Philo=1.0, Boonville=1.9, Ukiah=2.9)
    for k in ("Philo", "Boonville", "Ukiah"):
        q = out_back(prog(u, times[k], times[k] + 0.3), 2.4)
        px, py = pts[k]
        pin(f, px, py, q, cols[k])
    qd = prog(u, 1.7, 2.3)
    if qd > 0:                                                       # the measured 6 miles, Philo to Boonville
        a, b = pts["Philo"], pts["Boonville"]
        dashed(f, a[0], a[1], b[0], b[1], PAPER, 4, 16, 10, p=out_cubic(qd))
        if qd >= 1:
            mid = ((a[0] + b[0]) / 2 + 66, (a[1] + b[1]) / 2)
            pill(f, f"{round(_miles(TOWNS['Philo'], TOWNS['Boonville']))} MI", mid[0], mid[1], out_back(prog(u, 2.3, 2.6), 2.2), PAPER, INK, size=48,
                 align="center")
    for k in ("Philo", "Boonville", "Ukiah"):
        qq = out_cubic(prog(u, times[k] + 0.2, times[k] + 0.5))
        if qq > 0:
            px, py = pts[k]
            right = k == "Boonville"
            lx = px + (64 if right else -64)                # clear of the pin's halo ring
            text(f, names[k], "cond", 54, PAPER, lx, py - 8, align="left" if right else "right", tracking=3, alpha=qq)
            text(f, regs[k], "cond", 48, cols[k], lx, py + 38, align="left" if right else "right", tracking=3, alpha=qq)
    # the Winkler heat ladder: five steps, I (cool) to V (hot); markers drop onto it
    ly0, ly1 = 1262, 1342
    sw, gp, lx0 = 188, 10, 60
    for i in range(5):
        x = lx0 + i * (sw + gp)
        a = out_cubic(prog(u, 0.9 + 0.08 * i, 1.2 + 0.08 * i))
        round_rect(f, x, ly0, x + sw, ly1, 14, HEAT[i], 0.95 * a)
        fill_rect(f, x, ly0, x + sw, ly0 + 22, (255, 255, 255), 0.18 * a)
        text(f, ["I", "II", "III", "IV", "V"][i], "cond", 58, INK, x + sw / 2, ly1 - 20, align="center", alpha=a, tracking=2)
    text(f, "WINKLER HEAT CLASS", "condb", 40, PAPER, 60, 1208, tracking=4, alpha=out_cubic(prog(u, 1.0, 1.3)) * 0.9)
    seg_c = lambda i: lx0 + i * (sw + gp) + sw / 2                  # center of rung i (0 = I)
    for k, mx in (("Philo", seg_c(0)), ("Boonville", seg_c(1)), ("Ukiah", lx0 + 2 * (sw + gp) - gp / 2)):   # II-III: the line between II and III
        q = out_back(prog(u, times[k] + 0.25, times[k] + 0.55), 2.2)
        if q > 0:
            tri = np.array([[mx - 24, ly0 - 10 - 34 * q], [mx + 24, ly0 - 10 - 34 * q], [mx, ly0 - 10]], np.float32)
            fill_poly(f, tri, cols[k], 1.0)
            cv2.polylines(f, [tri.astype(np.int32)], True, (255, 255, 255), 3, cv2.LINE_AA)
    if u >= 3.5:
        a = out_cubic(prog(u, 3.5, 3.8))
        text(f, "IN SIX MILES,", "condb", 68, PAPER, 60, 1440, alpha=a, tracking=2, dy=14 * (1 - a))
        text(f, "THE HEAT CLASS CHANGES.", "condb", 68, YELLOW, 60, 1514, alpha=a, tracking=2, dy=14 * (1 - a))
    return f


# ================================================================== SCENE 6: OUTRO (32-36 s)
CARDS = [("01", "CHAMPAGNE", FLUTE, 0.50), ("02", "FOUR PERCENT", "us_mendo_av_esterlina_view_prater.jpg", 0.50),
         ("03", "FROST POCKET", "us_mendo_av_slope_prater.jpg", 0.50), ("04", "ABOVE THE FOG", "us_mendo_fog_redwoods_pexels.jpg", 0.50),
         ("05", "SIX MILES", "us_mendo_husch_philo_cc0.jpg", 0.50)]


EDGES = (0.0, 0.5, 1.0, 1.5, 1.75, 2.0)        # five recap cards that ACCELERATE (2 s in all), then the closing bumper


def s_outro(u, ur=0.0, D=4.0):
    f = np.zeros((H, W, 3), np.float32)
    if u < 2.0:
        k = max(i for i in range(5) if u >= EDGES[i])
        w = u - EDGES[k]
        num, word, name, fy = CARDS[k]
        f[:] = shot(name, 1.30 - 0.22 * out_expo(prog(w, 0, 0.3)), 0.5, fy, t=u, sh=1.4, seed=k * 1.9)
        desat(f, 0.35)
        darken(f, vgrad(700, 1500, 0.0, 0.8), (4, 6, 14))
        darken(f, vgrad(0, 420, 0.5, 0.0), (4, 6, 14))
        fill_rect(f, 0, 900, W, 1180, (4, 6, 14), 0.6)
        fill_rect(f, 0, 900, W, 906, YELLOW, 0.9)
        fill_rect(f, 0, 1174, W, 1180, YELLOW, 0.9)
        text(f, num, "cond", 190, YELLOW, 56, 790, tracking=2, alpha=0.95)
        sz = fit_size(word, "cond", W - 110, hi=200, tracking=4)
        text(f, word, "cond", sz, PAPER, W / 2, 1090, align="center", tracking=4, scale=1.0 + 0.10 * (1 - out_expo(prog(w, 0, 0.12))),
             glow=(12, (255, 170, 40), 0.3))
        seg_w, gap, sx0 = 74, 10, W - 56 - (5 * 74 + 4 * 10)       # the progress element completes
        for i in range(5):
            x = sx0 + i * (seg_w + gap)
            round_rect(f, x, 286, x + seg_w, 306, 10, (255, 255, 255), 0.18)
            if i <= k:
                round_rect(f, x, 286, x + seg_w, 306, 10, YELLOW, 1.0)
        flash(f, 0.5 * (1 - prog(w, 0, 0.06)) if w < 0.06 else 0.0)
        return f
    hook_card(f, u - 2.0, sheen_p=prog(u - 2.0, 0.4, 1.4))      # the closing bumper: the SAME title page and animation as the opening
    return f


# ================================================================== frame composer, render, preview
SCENES = []          # filled by later parts of this module (scene, duration)
SCENE_TABLE = []


def T(scene, u):
    for start, dur, fn in SCENE_TABLE:
        if fn.__name__ == scene:
            return start + u
    raise KeyError(scene)


def scene_frame(t):
    for start, dur, fn in SCENE_TABLE:
        if start <= t < start + dur or (fn is SCENE_TABLE[-1][2] and t >= start):
            return fn(t - start, ur=t - start, D=dur)


# Cut times (all downbeats of the 120 BPM grid except the final smash cut, which lands on beat 4 of the last bar) and their treatments.
CUTS_WHIP = (4.0, 30.0)        # a zoom-blur whip with a flash (the series' own `whip`)
CUTS_FLASH = (10.0, 38.0)      # a hard flash-cut with a punch-in; 38.0 is the smash cut onto the closing bumper
CUTS_PUSH = (18.0,)            # a horizontal push with motion blur
CUTS_GLITCH = (24.0,)          # an RGB-split, slice-shift glitch cut
CUTS_DIP = (36.0,)             # a three-frame dip to black into the recap


def glitch(f, p):
    """Slice-shift and RGB-split; p: 0 -> 1 intensity."""
    if p <= 0.01:
        return f
    out = f.copy()
    rg = np.random.default_rng(int(p * 997) + 3)
    ys = sorted(int(v) for v in rg.integers(0, H, 10))
    for i in range(0, 9, 2):
        y0, y1 = ys[i], ys[i + 1]
        if y1 > y0:
            out[y0:y1] = np.roll(f[y0:y1], int(rg.integers(-110, 110) * p), axis=1)
    sh = int(30 * p)
    out[..., 0] = np.roll(out[..., 0], sh, axis=1)
    out[..., 2] = np.roll(out[..., 2], -sh, axis=1)
    return out


def punch_zoom(f, z):
    if z <= 1.001:
        return f
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def frame_at(t):
    f = scene_frame(t)
    for c in CUTS_PUSH:
        if c - 0.25 <= t < c + 0.25:
            p = in_out_cubic(prog(t, c - 0.25, c + 0.25))
            fa, fb = scene_frame(min(t, c - 1e-3)), scene_frame(max(t, c))
            sh = int(round(p * W))
            out = np.empty_like(fa)
            out[:, :W - sh] = fa[:, sh:]
            out[:, W - sh:] = fb[:, :sh]
            k = 1 + 2 * int(30 * math.sin(math.pi * p))
            f = cv2.blur(out, (k, 1)) if k > 1 else out
    for c in CUTS_WHIP:
        if c - 0.13 <= t < c + 0.13:
            # out before the cut, in after it (the Field Guide Reels passed the outgoing amount on both sides, which left the flash on
            # screen for four frames after the cut; here it is gone within a frame or two)
            f = fg.whip(f, in_cubic(prog(t, c - 0.13, c)) if t < c else 0.0, (1 - out_cubic(prog(t, c, c + 0.13))) if t >= c else 0.0)
    for c in CUTS_FLASH:
        if c <= t < c + 0.2:
            q = 1 - prog(t, c, c + 0.2)
            f = punch_zoom(f, 1 + 0.07 * q)
            flash(f, 0.9 * q ** 2)
    for c in CUTS_GLITCH:
        if c - 0.07 <= t < c + 0.2:
            f = glitch(f, math.sin(math.pi * prog(t, c - 0.07, c + 0.2)))
            if t >= c:
                flash(f, 0.35 * (1 - prog(t, c, c + 0.08)))
    for c in CUTS_DIP:
        if c - 0.1 <= t < c + 0.1:
            f = f * (abs(t - c) / 0.1)
    return f


def render(out, start=0, end=None):
    n = int(SCENE_TABLE[-1][0] * FPS + SCENE_TABLE[-1][1] * FPS)
    end = n if end is None else end
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "16",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(start, end):
        pr.stdin.write(post(frame_at(fi / FPS), fi, fi / FPS).tobytes())
    pr.stdin.close()
    pr.wait()
    print("video done:", out)


def preview(times, out, cols=6):
    tiles = [Image.fromarray(post(frame_at(t), int(t * FPS), t)).resize((270, 480)) for t in times]
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 276, rows * 500), (60, 60, 60))
    d = ImageDraw.Draw(sheet)
    for i, (im, t) in enumerate(zip(tiles, times)):
        x, y = (i % cols) * 276, (i // cols) * 500
        sheet.paste(im, (x, y))
        d.text((x + 4, y + 482), f"{t:.2f}s", fill=(255, 255, 255))
    sheet.save(out)
    print("preview:", out)


SCENE_TABLE[:] = [(0.0, 4.0, s_title), (4.0, 6.0, s_f1), (10.0, 8.0, s_f2), (18.0, 6.0, s_f3), (24.0, 6.0, s_f4),
                  (30.0, 6.0, s_f5), (36.0, 4.0, s_outro)]

if __name__ == "__main__":
    if "--preview" in sys.argv:
        i = sys.argv.index("--preview")
        preview([float(x) for x in sys.argv[i + 1].split(",")], sys.argv[i + 2])
    elif "--render" in sys.argv:
        i = sys.argv.index("--render")
        r = sys.argv[i + 2:i + 4]
        render(sys.argv[i + 1], *(int(x) for x in r)) if len(r) == 2 else render(sys.argv[i + 1])
