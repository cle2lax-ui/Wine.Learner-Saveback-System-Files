"""Instagram Reel: COMING UP, a 30-second trailer for the next two weeks on the page. 1080x1920, 30 fps, 900 frames.

WHAT IT SHOWS (every card is the real, locked post page; nothing is mocked up)
  0-2    HOOK     "COMING UP", on frame 1 (the spec: the complete hook is legible from the first frame)
  2-8    post 1   THE FIELD GUIDE, "Climate's Impact on Wine" (15 slides): cover, then three quick swipes
  8-12   post 2   GUESS THE WINE REGION, "Same Latitude, Different Ocean": the clues page, a pulsing "?"
  12-18  post 3   FIVE FASCINATING FACTS about climate change: the cover, then a swipe through all five facts
  18-22  post 4   WHAT AM I DRINKING?: the mystery page, a pulsing "?"
  22-28  tease    THEN, a new arc: WINES OF SOUTH AFRICA (Arc 5 plan: two currents and a wind; Cape Cabernet blends; Cap Classique)
  28-30  outro    FOLLOW, so you never miss one; fades to black so the Reel loops into "COMING UP"
Every scene is a whole number of 2-second bars (120 BPM), so every cut lands on a downbeat; SCENE_TABLE is the single source of truth and the audio reads it.

THE SPEC (guides/REELS_SPEC_v2.md): hard cuts between beats (nothing crosses a cut); motion INSIDE a beat (cards that slide in and drift, supers that move,
swipes); a persistent progress element, here five nodes, one per beat, EMPTY on frame 1 and COMPLETE on the last beat, so the loop reads as continuous;
silent-legible throughout; the bottom 270 px and the right edge are kept clear of text for Instagram's own interface.
The tease is the only content that is not a published post: it comes from the Arc 5 plan (arc5/ARC5_SOUTH_AFRICA_PLAN.md) and is one scene (22-28 s) that can be cut
(the beat lengths then close up on the same 2-second bars).

PHOTOS: the post pages are Steve's own locked decks. The tease backdrop is "Franschhoek vineyard, Western Cape" (South African Tourism, CC BY 2.0, via Wikimedia
Commons; credit in the caption). Nothing share-alike is used, because a video is a derivative work.

Usage:  python3 trailer_reel.py --preview 0.3,1.5,...   (PNG contact sheet)      python3 trailer_reel.py --render OUT.mp4 [START END]   (video only; audio is muxed separately)
"""
import math
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_lib import (W, H, FPS, ROOT, Photo, blit_center, clamp, darken, finish, in_out_cubic, out_back,  # noqa: E402
                      out_cubic, prog, round_rect, text, text_width, transform, vgrad)
from reel_lib import chip as _chip  # noqa: E402,F401

DUR = 30.0
N = int(DUR * FPS)
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = f"{HERE}/trailer_assets"

# the series' burgundy theme (engine/themes.py), as RGB
GROUND, GROUND_ALT = (16, 8, 11), (40, 16, 24)
WHITE, MUTED, GOLD = (255, 255, 255), (196, 178, 182), (214, 178, 104)
CHIP_FILL, GLOW = (150, 36, 56), (104, 26, 38)
INK = (28, 24, 26)

CARD_W, CARD_H, CARD_TOP = 800, 1000, 462
CARD_CY = CARD_TOP + CARD_H / 2
NODE_Y = 1618

_cache = {}


def card_layer(name):
    """The real page as a rounded-corner premultiplied RGBA layer (and its soft shadow)."""
    if name not in _cache:
        im = Image.open(f"{ASSETS}/{name}.jpg").convert("RGB").resize((CARD_W, CARD_H), Image.LANCZOS)
        a = np.zeros((CARD_H, CARD_W), np.uint8)
        m = Image.new("L", (CARD_W * 2, CARD_H * 2), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, CARD_W * 2 - 1, CARD_H * 2 - 1], radius=56, fill=255)
        a = np.asarray(m.resize((CARD_W, CARD_H), Image.LANCZOS), np.float32) / 255.0
        lay = np.empty((CARD_H, CARD_W, 4), np.float32)
        lay[..., :3] = np.asarray(im, np.float32) * a[..., None]
        lay[..., 3] = a
        _cache[name] = lay
    return _cache[name]


def shadow_layer():
    if "shadow" not in _cache:
        pad = 90
        a = np.zeros((CARD_H + 2 * pad, CARD_W + 2 * pad), np.float32)
        a[pad:pad + CARD_H, pad:pad + CARD_W] = 1.0
        a = cv2.GaussianBlur(a, (0, 0), 34)
        lay = np.zeros(a.shape + (4,), np.float32)
        lay[..., 3] = a
        _cache["shadow"] = lay
    return _cache["shadow"]


def draw_card(dst, name, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    sh = transform(shadow_layer(), scale, rot)
    blit_center(dst, sh, cx, cy + 26, 0.62 * alpha)
    blit_center(dst, transform(card_layer(name), scale, rot), cx, cy, alpha)


# ------------------------------------------------------------------------------------------ background
def _bg_base():
    t = (np.linspace(0, 1, H, dtype=np.float32) ** 0.9)[:, None, None]
    top, bot = np.array(GROUND_ALT, np.float32), np.array(GROUND, np.float32)
    return np.broadcast_to(top * (1 - t) + bot * t, (H, W, 3)).copy()


def _glow_mask():
    yy, xx = np.mgrid[0:H + 500, 0:W + 500].astype(np.float32)
    r = np.sqrt(((xx - (W + 500) / 2) / 760) ** 2 + ((yy - (H + 500) / 2) / 760) ** 2)
    return (np.clip(1 - r, 0, 1) ** 2)[..., None]


BG, GLOWM = _bg_base(), _glow_mask()


def background(t):
    f = BG.copy()
    ox = int(250 + 220 * math.sin(t * 0.33))
    oy = int(250 + 200 * math.cos(t * 0.27))
    g = GLOWM[oy:oy + H, ox:ox + W]
    f += g * (np.array(GLOW, np.float32) - f) * 0.55
    return f


# ------------------------------------------------------------------------------------------ pieces
def fit(txt, fname, size, maxw, tracking=0):
    while size > 30 and text_width(txt, fname, size, tracking) > maxw:
        size -= 2
    return size


def fade_out(u, D, dur=0.3):
    return 1.0 - clamp(prog(u, D - dur, D))


def post_chip(dst, label, u, D):
    q = out_back(prog(u, 0.0, 0.4))
    if q <= 0:
        return
    size = fit(label, "black", 38, 900, 2)
    tw = text_width(label, "black", size, 2) + 64
    hh = size * 0.98
    cy = 205
    round_rect(dst, 540 - tw / 2 * q, cy - hh * q, 540 + tw / 2 * q, cy + hh * q, int(hh), CHIP_FILL, fade_out(u, D))
    text(dst, label, "black", size, WHITE, 540, cy + size * 0.36, align="center", tracking=2, alpha=min(1, q * 1.2) * fade_out(u, D), scale=q)


def headline(dst, lines, u, D, y0=318, size=76, delay=0.12):
    for i, ln in enumerate(lines):
        s = fit(ln, "serif_x", size, 940)
        p = out_cubic(prog(u, delay + 0.08 * i, delay + 0.55 + 0.08 * i))
        text(dst, ln, "serif_x", s, GOLD if i == 0 else WHITE, 540 + (1 - p) * 70, y0 + i * (size + 8), align="center",
             alpha=p * fade_out(u, D))


def subline(dst, txt, u, D, y=CARD_TOP + CARD_H + 78, delay=0.7):
    p = out_cubic(prog(u, delay, delay + 0.4))
    s = fit(txt, "med", 46, 940)
    text(dst, txt, "med", s, MUTED, 540, y + (1 - p) * 24, align="center", alpha=p * fade_out(u, D))


def nodes(dst, t, lit_at, done_t):
    """Five progress nodes. EMPTY at t=0, one lights per beat, COMPLETE (line filled) on the last beat."""
    xs = [540 + (i - 2) * 140 for i in range(5)]
    cv2.line(dst, (int(xs[0]), NODE_Y), (int(xs[-1]), NODE_Y), (96, 72, 80), 4, cv2.LINE_AA)
    last_x = xs[0]
    for i, x in enumerate(xs):
        q = out_back(prog(t, lit_at[i], lit_at[i] + 0.35))
        if q > 0:
            last_x = x
    fill_to = xs[0]
    for i, x in enumerate(xs):
        if t >= lit_at[i]:
            fill_to = x + 140 * clamp(prog(t, done_t[i], done_t[i] + 0.4)) if i < 4 else x
    fill_to = min(fill_to, xs[-1])
    if fill_to > xs[0]:
        cv2.line(dst, (int(xs[0]), NODE_Y), (int(fill_to), NODE_Y), GOLD, 6, cv2.LINE_AA)
    for i, x in enumerate(xs):
        q = out_back(prog(t, lit_at[i], lit_at[i] + 0.35))
        cv2.circle(dst, (int(x), NODE_Y), 27, (96, 72, 80), 3, cv2.LINE_AA)
        if q > 0:
            cv2.circle(dst, (int(x), NODE_Y), max(1, int(27 * q)), GOLD, -1, cv2.LINE_AA)
            text(dst, str(i + 1), "black", 30, INK, x, NODE_Y + 11, align="center", alpha=min(1, q))


def badge_q(dst, u, D, delay=1.3):
    """A pulsing '?' on the card's corner."""
    p = out_back(prog(u, delay, delay + 0.4))
    if p <= 0:
        return
    pulse = 1 + 0.06 * math.sin((u - delay) * 6.0)
    cx, cy = 540 + CARD_W / 2 - 34, CARD_TOP + 40
    r = 66 * p * pulse
    cv2.circle(dst, (int(cx), int(cy)), int(r + 10), (0, 0, 0), -1, cv2.LINE_AA)
    cv2.circle(dst, (int(cx), int(cy)), int(r), GOLD, -1, cv2.LINE_AA)
    text(dst, "?", "serif_x", 92, INK, cx, cy + 32, align="center", alpha=p, scale=pulse)


# ------------------------------------------------------------------------------------------ scenes
def card_stack(dst, pages, times, u, D):
    """`pages` swipe left in turn at `times` (seconds into the scene); the first card also enters from below."""
    enter = prog(u, 0.05, 0.7)
    e = out_back(enter, 1.25)
    base_y = CARD_CY + (1 - e) * 560
    drift = in_out_cubic(prog(u, 0, D))
    sc = (0.9 + 0.1 * e) * (1 + 0.025 * drift)
    rot0 = (1 - out_cubic(enter)) * 5.0 + 0.5 * math.sin(u * 0.8)
    k = sum(1 for t0 in times if u >= t0)
    if k == 0:
        draw_card(dst, pages[0], 540, base_y, sc, rot0)
        return
    t0 = times[k - 1]
    q = in_out_cubic(prog(u, t0, t0 + 0.34))
    old, new = pages[k - 1], pages[k]
    draw_card(dst, new, 540 + (1 - q) * 1000, CARD_CY, sc, 3.0 * (1 - q))
    draw_card(dst, old, 540 - q * 1000, CARD_CY, sc, -3.5 * q, 1 - 0.35 * q)


def s_hook(u, ur=0.0, D=2.0):
    f = background(ur)
    q = out_back(prog(u, 0.0, 0.6), 1.3)
    sc = 0.94 + 0.06 * q
    text(f, "COMING", "serif_x", 236, GOLD, 540, 760, align="center", scale=sc)
    text(f, "UP", "serif_x", 236, WHITE, 540, 1000, align="center", scale=sc)
    tw = text_width("ON OUR PAGE", "black", 40, 6)
    round_rect(f, 540 - tw / 2 - 40, 1150, 540 + tw / 2 + 40, 1236, 43, CHIP_FILL)
    text(f, "ON OUR PAGE", "black", 40, WHITE, 540, 1209, align="center", tracking=6)
    text(f, "The next two weeks", "med", 50, MUTED, 540, 1330, align="center")
    return f


def post_scene(chip_label, lines, sub, pages, times, with_q=False, head_size=76):
    def fn(u, ur=0.0, D=4.0):
        f = background(ur + 0.0)
        card_stack(f, pages, times, u, D)
        headline(f, lines, u, D, size=head_size)
        post_chip(f, chip_label, u, D)
        subline(f, sub, u, D)
        if with_q:
            badge_q(f, u, D)
        return f
    return fn


_sa = None


def s_tease(u, ur=0.0, D=6.0):
    global _sa
    if _sa is None:
        _sa = Photo("fffa_climate_cover_franschhoek.jpg", 1.25)
    f = _sa.view(1.0 + 0.10 * in_out_cubic(prog(u, 0, D)), 0.5 + 0.03 * math.sin(u * 0.5), 0.55).copy()
    darken(f, vgrad(180, 1450, 0.52, 0.88), (14, 6, 9))
    post_chip(f, "THEN, A NEW ARC", u, D)
    for i, (ln, col) in enumerate([("Wines of", WHITE), ("South Africa", GOLD)]):
        p = out_cubic(prog(u, 0.15 + 0.1 * i, 0.7 + 0.1 * i))
        s = fit(ln, "serif_x", 132, 960)
        text(f, ln, "serif_x", s, col, 540 + (1 - p) * 80, 500 + i * 150, align="center", alpha=p * fade_out(u, D))
    items = ["Two currents, one wind", "Cape Cabernet blends", "Cap Classique"]
    for i, ln in enumerate(items):
        t0 = 1.5 + 1.2 * i
        p = out_cubic(prog(u, t0, t0 + 0.45))
        y = 900 + i * 125
        if p > 0.02:
            cv2.circle(f, (150, int(y - 17)), max(1, int(11 * p)), GOLD, -1, cv2.LINE_AA)
        text(f, ln, "bold", 62, WHITE, 190 + (1 - p) * 60, y, align="left", alpha=p * fade_out(u, D))
    return f


def s_outro(u, ur=0.0, D=2.0):
    f = background(ur)
    p = out_back(prog(u, 0.0, 0.5), 1.3)
    text(f, "FOLLOW", "serif_x", 190, GOLD, 540, 860, align="center", scale=0.92 + 0.08 * p, alpha=min(1, p))
    text(f, "so you never miss one", "med", 54, WHITE, 540, 990, align="center", alpha=out_cubic(prog(u, 0.3, 0.8)))
    return f


FG = ["fg1", "fg2", "fg3", "fg4"]
FFP = ["ff1", "ff2", "ff3", "ff4", "ff5", "ff6"]
SCENE_TABLE = [  # (start, duration, name, fn)
    (0.0, 2.0, "hook", s_hook),
    (2.0, 6.0, "fg", post_scene("THE FIELD GUIDE", ["Climate's Impact", "on Wine"], "15 slides on what shapes every vintage",
                                FG, [2.2, 3.6, 5.0])),
    (8.0, 4.0, "gtr", post_scene("GUESS THE WINE REGION", ["Same Latitude,", "Different Ocean"], "Can you name the region?",
                                 ["gtr1"], [], with_q=True)),
    (12.0, 6.0, "fffa", post_scene("FIVE FASCINATING FACTS", ["Climate Change", "and Wine"], "Swipe through five facts",
                                   FFP, [1.5, 2.4, 3.3, 4.2, 5.1])),
    (18.0, 4.0, "wad", post_scene("WHAT AM I DRINKING?", ["A Mystery Red", "Six Years in Barrel"], "Can you guess it?",
                                  ["wad1"], [], with_q=True)),
    (22.0, 6.0, "tease", s_tease),
    (28.0, 2.0, "outro", s_outro),
]
LIT_AT = [2.15, 8.15, 12.15, 18.15, 22.15]            # each node lights as its beat begins
DONE_T = [8.0, 12.0, 18.0, 22.0, 28.0]               # the line to the next node completes at the next cut; the last node closes at the outro


def frame_at(t):
    f = None
    for start, dur, name, fn in SCENE_TABLE:
        if start <= t < start + dur or (name == "outro" and t >= start):
            f = fn(t - start, ur=t - start, D=dur)
            break
    nodes(f, t, LIT_AT, DONE_T)
    if t >= DUR - 0.3:
        f *= 1 - prog(t, DUR - 0.3, DUR)
    return f


def render(out, start=0, end=None):
    end = N if end is None else end
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(start, end):
        pr.stdin.write(finish(frame_at(fi / FPS), fi).tobytes())
        if fi % 30 == 0:
            print(f"frame {fi}/{N}", flush=True)
    pr.stdin.close()
    pr.wait()
    print("video done:", out)


def preview(times, out):
    tiles = [Image.fromarray(finish(frame_at(min(t, DUR - 1 / FPS)), int(round(t * FPS)))).resize((270, 480)) for t in times]
    cols = min(8, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 276, rows * 500), (60, 60, 60))
    d = ImageDraw.Draw(sheet)
    for i, (im, t) in enumerate(zip(tiles, times)):
        x, y = (i % cols) * 276, (i // cols) * 500
        sheet.paste(im, (x, y))
        d.text((x + 4, y + 482), f"{t:.2f}s", fill=(255, 255, 255))
    sheet.save(out)
    print("preview:", out, sheet.size)


if __name__ == "__main__":
    if "--preview" in sys.argv:
        i = sys.argv.index("--preview")
        preview([float(x) for x in sys.argv[i + 1].split(",")], sys.argv[i + 2] if len(sys.argv) > i + 2 else "/home/claude/trailer_preview.png")
    elif "--render" in sys.argv:
        i = sys.argv.index("--render")
        rng_ = sys.argv[i + 2:i + 4]
        render(sys.argv[i + 1], *(int(x) for x in rng_)) if len(rng_) == 2 else render(sys.argv[i + 1])
