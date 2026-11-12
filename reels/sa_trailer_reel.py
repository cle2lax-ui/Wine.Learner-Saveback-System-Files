"""Instagram Reel: WATCH OUR PAGE FOR THESE POSTS, the Wines of South Africa (Arc 5) trailer. 1080x1920, 30 fps, 900 frames (30 s). VERSION 2 (Steve, after the Field Guide locked).
Posted at the same time as the South Africa Field Guide ("Two Currents, One Wind", tag sa-field-guide-final), and it teases the posts that follow it. Photography and motion are on frame 1 and in every beat.
v2 changes (Steve): graphics pulled from the FINAL Field Guide; the score is quiet acoustic piano; most of the whimsical sound effects are gone (see sa_trailer_audio.py).

  0-4    HOOK      the Field Guide's cover photograph (Overberg vineyards, natural color: the first cut used a sunset photo with a pink grade) pushing in from frame 0, the Field Guide's
                   Africa line drawing (South Africa in gold) in the upper right, and the title "Watch our Page for These Posts" legible on frame 1
  4-8    1  THE FIELD GUIDE      OUT NOW: four of its real slides swipe through (cover, climate, Sauvignon Blanc and Chardonnay, the Simonsberg wards) over a blurred Table Mountain
  8-12   2  GUESS THE WINE REGION  the Field Guide's real district map with every name masked, in a slow focus pull, a pulsing "?": a mystery that names no place
  12-18  3  FIVE FASCINATING FACTS   a Stellenbosch valley; three facts counting up: 12 months, about 90 days, 2x
  18-22  4  SPLIT DECISION   Cap Classique: 12 MONTHS or 36?  two photos (a riddling rack, a bottle stack), two sides, pick one
  22-26  5  WHAT AM I DRINKING?   a taster nosing a red, the glass held by its stem (never the bowl), a mystery Cape wine, a pulsing "?"
  26-30  outro     back to the opening photo at its opening framing, with the Africa drawing: FOLLOW; the Reel fades to black and loops into its own first frame
Every scene is a whole number of 2-second bars; SCENE_TABLE is the single source of truth and the audio reads it.

The teasers for posts that are NOT BUILT YET rest only on what the textbooks already fix (the Field Guide's own slides are real, so beats 1 and 2 may show them):
    at least 12 months on the lees ... Cap Classique's legal minimum (WSET D4 p. 116); 36 months is the 2022 extended lees aging tier (D4 p. 116)
    about 90 days from flowering to picking ... Cap Classique grapes (D4 p. 117);   2x ... Chenin Blanc: 16,000 ha, double the Loire's (D3 p. 507)
  Named but not described: Guess the Wine Region (no clue, no answer: the map shows no names), What Am I Drinking? (no producer).

GRAPHICS FROM THE FINAL FIELD GUIDE (trailer_assets/sa_fg_*.jpg, cut from the pixel-verified final slides): cover, climate (4), Sauvignon Blanc and Chardonnay (8), the Simonsberg wards (10), and the district map (3)
  cropped to the map alone. The Africa line drawing is drawn from data/geo/africa_countries.geojson (Natural Earth, public domain), the same data as the Field Guide's cover.
PHOTOS (Wikimedia Commons; nothing share-alike, because a video is a derivative work):
  hook and outro  "Vineyards, Overberg, Western Cape" (Axel Buhrmann, CC BY 4.0)         beat 1 backdrop  "Table Mountain from Blouberg" (South African Tourism, CC BY 2.0)
  beat 2 backdrop Cape Peninsula coast (lumoplank, CC0)                                  beat 3  "Stellenbosch Wine Route" (South African Tourism)
  beat 4          "Bottles in riddling rack" (Craig Hatfield) and "Stock de bouteilles a la Muratie Winery" (fabulousfabs)
  beat 5          "Humer en degustation a Stellenbosch" (marko8904, CC BY 2.0): a taster nosing a red by the stem of the glass, the bowl untouched (Steve: never show a hand on the bowl)

THE SPEC (guides/REELS_SPEC_v2.md): hard cuts between beats; motion inside a beat; a progress element (five nodes, one per post), EMPTY on frame 1 and COMPLETE on the last beat;
silent-legible; the bottom 270 px stays clear of text for Instagram's own interface.
Usage:  python3 sa_trailer_reel.py --preview 0.0,1.0,...   |   --render OUT.mp4 [START END]
"""
import json
import math
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_lib import (ROOT, W, H, FPS, Photo, clamp, darken, finish, font, in_cubic, in_out_cubic, out_back, out_cubic, prog,  # noqa: E402
                      round_rect, text, text_width, vgrad)

DUR = 30.0
N = int(DUR * FPS)
# the series' forest-green theme (engine/themes.py)
GROUND, GROUND_ALT = (8, 14, 11), (18, 36, 26)
WHITE, MUTED, GOLD = (255, 255, 255), (176, 196, 184), (214, 178, 104)
CHIP_FILL, SHADE = (36, 110, 70), (6, 12, 9)
INK = (28, 24, 26)
CHIP_Y, HEAD_Y0, SUB_Y, NODE_Y = 205, 318, 1500, 1618
TITLE = ("Watch our Page", "for These Posts")                      # the Reel's title, exactly as Steve gave it

_photos = {}


def ph(name, cover=1.22, size=None):
    key = (name, size)
    if key not in _photos:
        _photos[key] = Photo(f"{name}.jpg", cover, size)
    return _photos[key]


# ------------------------------------------------------------------------------------------ shared pieces
def fit(txt, fname, size, maxw, tracking=0):
    while size > 30 and text_width(txt, fname, size, tracking) > maxw:
        size -= 2
    return size


def fade_out(u, D, dur=0.3):
    return 1.0 - clamp(prog(u, D - dur, D))


def T(dst, txt, fname, size, color, x, y, **kw):
    """Text with a soft dark halo, so it reads over any photo."""
    return text(dst, txt, fname, size, color, x, y, glow=(9, (0, 0, 0), 0.75), **kw)


def chip(dst, label, u, D, y=CHIP_Y, delay=0.0):
    q = out_back(prog(u, delay, delay + 0.4))
    if q <= 0:
        return
    size = fit(label, "black", 38, 900, 2)
    tw = text_width(label, "black", size, 2) + 64
    hh = size * 0.98
    a = fade_out(u, D)
    round_rect(dst, 540 - tw / 2 * q, y - hh * q, 540 + tw / 2 * q, y + hh * q, int(hh), CHIP_FILL, a)
    text(dst, label, "black", size, WHITE, 540, y + size * 0.36, align="center", tracking=2, alpha=min(1, q * 1.2) * a, scale=q)


def headline(dst, lines, u, D, y0=HEAD_Y0, size=84, delay=0.12, solid=False):
    for i, ln in enumerate(lines):
        s = fit(ln, "serif_x", size, 940)
        p = 1.0 if solid else out_cubic(prog(u, delay + 0.08 * i, delay + 0.55 + 0.08 * i))
        T(dst, ln, "serif_x", s, GOLD if i == 0 else WHITE, 540 + (1 - p) * 70, y0 + i * (size + 8), align="center", alpha=p * fade_out(u, D))


def sub(dst, txt, u, D, y=SUB_Y, delay=0.7, size=50):
    p = out_cubic(prog(u, delay, delay + 0.4))
    s = fit(txt, "med", size, 940)
    T(dst, txt, "med", s, WHITE, 540, y + (1 - p) * 24, align="center", alpha=p * fade_out(u, D))


LIT_AT = [4.15, 8.15, 12.15, 18.15, 22.15]            # each progress node lights as its post's beat begins
DONE_T = [8.0, 12.0, 18.0, 22.0, 26.0]


def nodes(dst, t):
    """Five nodes, one per post: EMPTY at t=0, one lights per beat, COMPLETE (line filled, all lit) from the last beat."""
    xs = [540 + (i - 2) * 140 for i in range(5)]
    cv2.line(dst, (int(xs[0]), NODE_Y), (int(xs[-1]), NODE_Y), (120, 140, 128), 4, cv2.LINE_AA)
    fill_to = xs[0]
    for i, x in enumerate(xs):
        if t >= LIT_AT[i]:
            fill_to = x + (140 * clamp(prog(t, DONE_T[i], DONE_T[i] + 0.4)) if i < 4 else 0)
    if fill_to > xs[0]:
        cv2.line(dst, (int(xs[0]), NODE_Y), (int(min(fill_to, xs[-1])), NODE_Y), GOLD, 6, cv2.LINE_AA)
    for i, x in enumerate(xs):
        q = out_back(prog(t, LIT_AT[i], LIT_AT[i] + 0.35))
        cv2.circle(dst, (int(x), NODE_Y), 27, (150, 170, 158), 3, cv2.LINE_AA)
        if q > 0:
            cv2.circle(dst, (int(x), NODE_Y), max(1, int(27 * q)), GOLD, -1, cv2.LINE_AA)
            text(dst, str(i + 1), "black", 30, INK, x, NODE_Y + 11, align="center", alpha=min(1, q))


def shade(f, top=0.0, bottom=0.0, mid=0.0, mid_band=(700, 1250)):
    a = vgrad(100, 760, top, 0.0) + vgrad(1180, 1640, 0.0, bottom)
    if mid:
        a = a + vgrad(mid_band[0] - 160, mid_band[0], 0.0, mid) * vgrad(mid_band[1], mid_band[1] + 160, 1.0, 0.0)
    darken(f, np.clip(a, 0, 0.92), SHADE)


def q_badge(dst, u, D, delay=1.0, cx=540, cy=900, r0=120):
    p = out_back(prog(u, delay, delay + 0.45))
    if p <= 0:
        return
    pulse = 1 + 0.07 * math.sin((u - delay) * 6.0)
    r = r0 * p * pulse
    cv2.circle(dst, (int(cx), int(cy)), int(r + 12), (0, 0, 0), -1, cv2.LINE_AA)
    cv2.circle(dst, (int(cx), int(cy)), int(r), GOLD, -1, cv2.LINE_AA)
    text(dst, "?", "serif_x", max(12, int(r0 * 1.42 * p)), INK, cx, cy + r0 * 0.48 * p, align="center", alpha=min(1, p) * fade_out(u, D))


def count(v, p):
    return int(round(v * clamp(out_cubic(p))))


# ------------------------------------------------------------------------------------------ graphics from the final Field Guide
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trailer_assets")
_africa = {}


def africa_layers(size=(400, 418)):
    """The Field Guide cover's line drawing of Africa, rendered once: (base rgb, base alpha, South Africa rgb, South Africa alpha), all float32 at `size`.
    A faint deep-blue plate and white hairline borders; South Africa filled gold with a white edge, Lesotho left as the hole it is; a soft shadow beneath."""
    if size not in _africa:
        from PIL import ImageFilter
        countries = json.load(open(os.path.join(ROOT, "data", "geo", "africa_countries.geojson")))["countries"]
        lon0, lon1, lat0, lat1 = -18.0, 52.0, -35.5, 38.0
        bw, bh = size
        sc = min(bw / (lon1 - lon0), bh / (lat1 - lat0))
        ox, oy = (bw - sc * (lon1 - lon0)) / 2, (bh - sc * (lat1 - lat0)) / 2
        S = 4
        P = lambda p: ((ox + (p[0] - lon0) * sc) * S, (oy + (lat1 - p[1]) * sc) * S)
        sz = (bw * S, bh * S)
        plate, lines, fill, edge = (Image.new("L", sz, 0) for _ in range(4))
        pd, ld, fd, ed = (ImageDraw.Draw(x) for x in (plate, lines, fill, edge))
        for c in countries:
            for ring in c["rings"]:
                pts = [P(p) for p in ring]
                pd.polygon(pts, fill=88)
                ld.line(pts + [pts[0]], fill=225, width=3 * S, joint="curve")
                if c["name"] == "South Africa":
                    fd.polygon(pts, fill=255)
                elif c["name"] == "Lesotho":
                    fd.polygon(pts, fill=0)
                if c["name"] in ("South Africa", "Lesotho"):
                    ed.line(pts + [pts[0]], fill=255, width=3 * S, joint="curve")
        shadow = Image.merge("L", [Image.eval(Image.blend(lines, fill, 0.5), lambda v: 150 if v else 0)]).filter(ImageFilter.GaussianBlur(5 * S))
        down = lambda im: np.asarray(im.resize((bw, bh), Image.LANCZOS), np.float32) / 255.0
        a_shadow, a_plate, a_lines, a_fill, a_edge = down(shadow), down(plate), down(lines), down(fill), down(edge)
        rgb = np.zeros((bh, bw, 3), np.float32)
        al = np.zeros((bh, bw), np.float32)
        for col, a_ in (((0, 0, 0), a_shadow), ((14, 40, 70), a_plate * 0.45), ((255, 255, 255), a_lines * 0.84)):
            rgb = rgb * (1 - a_[..., None]) + np.array(col, np.float32) * a_[..., None]
            al = al + a_ * (1 - al)
        ge = np.zeros((bh, bw, 3), np.float32)
        ge[:] = (196, 158, 84)
        a_sa = np.clip(a_fill * 0.92, 0, 1)
        ge = ge * (1 - a_edge[..., None]) + 255.0 * a_edge[..., None]
        a_sa = np.maximum(a_sa, a_edge)
        _africa[size] = (rgb, al, ge, a_sa)
    return _africa[size]


def africa(dst, x0, y0, a=1.0, glow=0.0, size=(400, 418)):
    """Draw the Africa line drawing with its top-left at (x0, y0); `glow` (0-1) breathes South Africa's gold."""
    rgb, al, ge, a_sa = africa_layers(size)
    h, w = al.shape
    reg = dst[y0:y0 + h, x0:x0 + w]
    aa = (al * a)[..., None]
    reg[:] = reg * (1 - aa) + rgb * aa
    ab = (a_sa * a * (0.88 + 0.12 * glow))[..., None]
    reg[:] = reg * (1 - ab) + ge * ab


_cards = {}


def card_img(name, w, h):
    """A Field Guide slide (or the district map) as a framed card, w x h, with a thin white edge; float32."""
    key = (name, w, h)
    if key not in _cards:
        im = Image.open(os.path.join(ASSETS, f"sa_fg_{name}.jpg")).convert("RGB")
        im = im.resize((w, h), Image.LANCZOS)
        a = np.asarray(im, np.float32)
        a[:4], a[-4:], a[:, :4], a[:, -4:] = 245.0, 245.0, 245.0, 245.0
        _cards[key] = a
    return _cards[key]


def put_card(dst, img, cx, cy, alpha=1.0, scale=1.0, shadow=0.55):
    """Composite a card centered at (cx, cy) with a soft shadow; clipped to the frame."""
    h, w = img.shape[:2]
    if scale != 1.0:
        img = cv2.resize(img, (max(2, int(w * scale)), max(2, int(h * scale))), interpolation=cv2.INTER_LINEAR)
        h, w = img.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    sx, sy = max(0, -x0), max(0, -y0)
    ex, ey = min(w, W - x0), min(h, H - y0)
    if ex <= sx or ey <= sy:
        return
    X0, Y0, X1, Y1 = x0 + sx, y0 + sy, x0 + ex, y0 + ey
    pad = 46
    gx0, gy0, gx1, gy1 = max(0, X0 - pad), max(0, Y0 - pad + 18), min(W, X1 + pad), min(H, Y1 + pad + 18)
    sh = np.zeros((gy1 - gy0, gx1 - gx0), np.float32)
    sh[max(0, Y0 - gy0 + 8):Y1 - gy0 - 8 + 1 if Y1 - gy0 - 8 > 0 else 0, max(0, X0 - gx0 + 8):X1 - gx0 - 8 + 1 if X1 - gx0 - 8 > 0 else 0] = 1.0
    sh = cv2.GaussianBlur(sh, (0, 0), 20) * shadow * alpha
    dst[gy0:gy1, gx0:gx1] *= (1 - sh[..., None])
    dst[Y0:Y1, X0:X1] = dst[Y0:Y1, X0:X1] * (1 - alpha) + img[sy:ey, sx:ex] * alpha


def backdrop(name, u, D, fx=0.5, fy=0.5, blur=16.0, dim=0.55, z0=1.05, z1=1.18):
    """A blurred, dimmed photograph behind the cards, drifting slowly."""
    f = ph(name).view(z0 + (z1 - z0) * in_out_cubic(prog(u, 0, D)), fx, fy).copy()
    f = cv2.GaussianBlur(f, (0, 0), blur)
    darken(f, np.full((H, 1, 1), dim, np.float32), SHADE)
    return f


# ------------------------------------------------------------------------------------------ kinetic type
SHINE = (255, 244, 214)


def _mix(a, b, w):
    return tuple(int(round(a[i] + (b[i] - a[i]) * w)) for i in range(3))


def kinetic(dst, txt, fname, size, base, x, y, u, first=0, stagger=0.03, sweeps=(), wave=True, tint=SHINE):
    """Per-letter animation that is FULLY LEGIBLE from u=0 (the Reel spec: the whole hook reads on frame 1).
    Entrance: each letter starts 40 px low, 14% large and 3 degrees off, then springs into place, left to right (a wave), so frame 1 is a readable line of
    type that is visibly alive. After it settles: a slow rolling wave, and `sweeps` (windows in seconds) send a light sweep through the letters."""
    f = font(fname, int(size))
    tw = text_width(txt, fname, int(size), 0)
    cur = x - tw / 2
    for k, c in enumerate(txt):
        w = f.getlength(c)
        if c != " ":
            gi = first + k
            d0 = stagger * gi
            p = prog(u, d0, d0 + 0.75)
            e = out_back(p, 1.9)
            dy = 40 * (1 - e)
            if wave:
                dy += 5.0 * math.sin(u * 3.4 - gi * 0.45) * clamp(prog(u, 1.2, 1.8))
            wgt = 0.0
            for (a, b) in sweeps:
                sx = -160 + (W + 320) * prog(u, a, b)
                wgt = max(wgt, math.exp(-(((cur + w / 2) - sx) / 130.0) ** 2))
            text(dst, c, fname, size, _mix(base, tint, 0.85 * wgt), cur, y, alpha=0.9 + 0.1 * p, scale=1 + 0.14 * (1 - e), dy=dy,
                 rot=(3.0 if gi % 2 else -3.0) * (1 - e), glow=(9, (0, 0, 0), 0.75))
        cur += w


def karaoke(dst, txt, fname, size, base, x, y, u, t0, t1, hi=(255, 226, 150)):
    """Words stay readable; a highlight travels through them from t0 to t1."""
    words = txt.split(" ")
    f = font(fname, int(size))
    sp = f.getlength(" ")
    tw = text_width(txt, fname, int(size), 0)
    cur = x - tw / 2
    pos = (len(words) + 1.2) * prog(u, t0, t1) - 0.6
    for i, wd in enumerate(words):
        w = f.getlength(wd)
        wgt = clamp(1 - abs(i - pos) / 1.1)
        text(dst, wd, fname, size, _mix(base, hi, wgt), cur, y - 6 * wgt, scale=1 + 0.05 * wgt, glow=(9, (0, 0, 0), 0.75))
        cur += w + sp


# ------------------------------------------------------------------------------------------ scenes (text=False draws the photo only: used to measure contrast)
def s_hook(u, ur=0.0, D=4.0, text_on=True):
    z = 1.0 + 0.20 * in_out_cubic(prog(u, 0, D + 0.5))               # moving from frame 0
    f = ph("sa_overberg_vineyards").view(z, 0.50 + 0.05 * (u / D), 0.60).copy()
    shade(f, top=0.30, bottom=0.62, mid=0.0)
    darken(f, vgrad(840, 1000, 0.0, 0.58) * vgrad(1440, 1520, 1.0, 0.0), SHADE)        # a band of shade behind the title
    if text_on:
        africa(f, 640, 290, a=1.0, glow=0.5 + 0.5 * math.sin(u * 2.6))                    # the Field Guide's drawing of Africa, South Africa in gold
        chip(f, "WINES OF SOUTH AFRICA", 0.6 + 0.04 * math.sin(u * 4.0), D)                      # fully shown on frame 1, with a gentle pulse
        first = 0
        for i, ln in enumerate(TITLE):
            s = fit(ln, "serif_x", 124, 960)
            kinetic(f, ln, "serif_x", s, GOLD if i == 0 else WHITE, 540, 1090 + i * 140, u, first=first, sweeps=((0.9, 2.0), (2.8, 3.8)))
            first += len(ln)
        karaoke(f, "The Field Guide is out now. These come next.", "med", 50, WHITE, 540, 1390, u, 0.8, 3.0)
    return f


FG_CARDS = ("cover", "climate", "whites", "wards")


def s_fg(u, ur=0.0, D=4.0, text_on=True):
    f = backdrop("sa_table_mountain_blouberg", u, D, fx=0.45, fy=0.5, blur=11.0, dim=0.40)
    shade(f, top=0.30, bottom=0.55)
    cw, chh, cy = 680, 850, 1030
    slot, tin = 0.85, 0.42
    n = len(FG_CARDS)
    for i, name in enumerate(FG_CARDS):
        t_in = 0.12 + slot * i
        p_in = out_cubic(prog(u, t_in, t_in + tin))
        t_out = t_in + slot
        p_out = in_cubic(prog(u, t_out, t_out + tin)) if i < n - 1 else 0.0
        if p_in <= 0.0 or p_out >= 1.0:
            continue
        cx = 540 + (1 - p_in) * 900 - p_out * 900
        sc = 0.94 + 0.06 * p_in
        put_card(f, card_img(name, cw, chh), cx, cy, alpha=1.0, scale=sc)
    if text_on:
        chip(f, "OUT NOW", u, D)
        headline(f, ["Two Currents,", "One Wind"], u, D, size=84)
        sub(f, "The Field Guide to South Africa", u, D, y=1560, delay=0.5, size=48)
    return f


def s_gtr(u, ur=0.0, D=4.0, text_on=True):
    f = backdrop("sa_cape_peninsula_coast", u, D, fx=0.5, fy=0.5, blur=10.0, dim=0.42, z0=1.0, z1=1.1)
    shade(f, top=0.32, bottom=0.55)
    mp = card_img("districts", 960, 551)
    sig = 20 - 14 * out_cubic(prog(u, 0.0, 3.0))                      # a slow focus pull that never quite resolves: a mystery that names no place
    blurred = cv2.GaussianBlur(mp, (0, 0), max(sig, 0.1))
    put_card(f, blurred, 540, 985, alpha=1.0, scale=1.0 + 0.04 * in_out_cubic(prog(u, 0, D)))
    if text_on:
        chip(f, "GUESS THE WINE REGION", u, D)
        headline(f, ["Name the", "Cape Region"], u, D)
        q_badge(f, u, D, delay=0.9, cy=985)
        sub(f, "Clues first. Answer on page two.", u, D)
    return f


def s_fffa(u, ur=0.0, D=6.0, text_on=True):
    f = ph("sa_stell_valley").view(1.0 + 0.14 * in_out_cubic(prog(u, 0, D)), 0.55 - 0.12 * in_out_cubic(prog(u, 0, D)), 0.55).copy()
    shade(f, top=0.84, bottom=0.78, mid=0.76)
    if text_on:
        chip(f, "FIVE FASCINATING FACTS", u, D)
        headline(f, ["Five Facts,", "One Surprise Each"], u, D, size=76)
        stats = [("AT LEAST", 12, "", "months on the lees", "the Cap Classique minimum"),
                 ("ABOUT", 90, "", "days from flowering", "to picking, for Cap Classique"),
                 ("", 2, "×", "the Loire's area", "of Chenin Blanc")]
        for i, (tag, val, suf, l1, l2) in enumerate(stats):
            t0 = 0.7 + 1.75 * i
            a_in = prog(u, t0, t0 + 0.35)
            a = out_cubic(a_in) * (1 - clamp(prog(u, t0 + 1.25, t0 + 1.45))) if i < 2 else out_cubic(a_in) * fade_out(u, D)
            if a <= 0.01:
                continue
            c = count(val, prog(u, t0 + 0.05, t0 + 0.8))
            pop = 1.0 + 0.10 * max(0.0, 1 - prog(u, t0 + 0.7, t0 + 1.0)) * (1 if c == val else 0)
            if tag:
                T(f, tag, "black", 40, MUTED, 540, 850, align="center", tracking=6, alpha=a)
            T(f, f"{c}{suf}", "serif_x", 230, GOLD, 540, 1040, align="center", alpha=a, scale=pop)
            T(f, l1, "bold", 58, WHITE, 540, 1130, align="center", alpha=a)
            T(f, l2, "med", 46, MUTED if False else WHITE, 540, 1200, align="center", alpha=a * 0.92)
        sub(f, "Swipe for all five.", u, D, delay=1.2)
    return f


_split = {}


def _panel(name, side, z, fx, fy):
    key = (name, side)
    if key not in _split:
        _split[key] = Photo(f"{name}.jpg", 1.3, (540, H))
    return _split[key].view(z, fx, fy).copy()


def s_sd(u, ur=0.0, D=4.0, text_on=True):
    e = out_cubic(prog(u, 0.0, 0.55))
    zl, zr = 1.0 + 0.10 * (u / D), 1.0 + 0.10 * (u / D)
    left = _panel("sa_riddling_rack", "L", zl, 0.45, 0.55)
    right = _panel("sa_muratie_bottles", "R", zr, 0.5, 0.82)
    left = left * 0.62 + np.array((36, 110, 70), np.float32) * 0.20                        # forest green: the standard rule
    right = right * 0.62 + np.array((196, 140, 60), np.float32) * 0.20                     # amber: the extended rule
    f = np.empty((H, W, 3), np.float32)
    f[:] = GROUND
    xl = int(-540 * (1 - e))
    xr = int(540 + 540 * (1 - e))
    if xl > -540:
        f[:, max(xl, 0):xl + 540] = left[:, max(-xl, 0):]
    if xr < W:
        f[:, xr:min(xr + 540, W)] = right[:, :min(xr + 540, W) - xr]
    shade(f, top=0.74, bottom=0.70, mid=0.64)
    if text_on:
        cv2.line(f, (540, 560), (540, 1500), GOLD, 4, cv2.LINE_AA)
        chip(f, "SPLIT DECISION", u, D)
        headline(f, ["Cap Classique:", "12 Months or 36?"], u, D, size=78)
        for x, val, lab, d0 in ((270, 12, "months", 0.35), (810, 36, "months", 0.55)):
            a = out_cubic(prog(u, d0, d0 + 0.3)) * fade_out(u, D)
            T(f, str(count(val, prog(u, d0, d0 + 0.8))), "serif_x", 240, GOLD if x < 540 else WHITE, x, 1010, align="center", alpha=a)
            T(f, lab, "bold", 54, WHITE, x, 1090, align="center", alpha=a)
        vp = out_back(prog(u, 0.9, 1.3))
        if vp > 0:
            cv2.circle(f, (540, 930), int(58 * vp) + 8, (0, 0, 0), -1, cv2.LINE_AA)
            cv2.circle(f, (540, 930), int(58 * vp), GOLD, -1, cv2.LINE_AA)
            text(f, "VS", "black", max(10, int(46 * vp)), INK, 540, 930 + 17 * vp, align="center", alpha=min(1, vp) * fade_out(u, D))
        sub(f, "Pick a side.", u, D, delay=1.2)
    return f


def s_wad(u, ur=0.0, D=4.0, text_on=True):
    f = ph("sa_taster_stem_crop").view(1.0 + 0.10 * in_out_cubic(prog(u, 0, D)), 0.5, 0.56).copy()     # tight on the glass held by its STEM (never the bowl), the face out of frame
    shade(f, top=0.80, bottom=0.78)
    if text_on:
        chip(f, "WHAT AM I DRINKING?", u, D)
        headline(f, ["A Mystery", "Cape Wine"], u, D)
        q_badge(f, u, D, delay=1.0, cx=850, cy=690, r0=92)
        sub(f, "Name it from the clues.", u, D)
    return f


def s_outro(u, ur=0.0, D=4.0, text_on=True):
    f = ph("sa_overberg_vineyards").view(1.0 + 0.05 * in_out_cubic(prog(u, 0, D)), 0.50, 0.60).copy()   # the opening photo at its opening framing
    shade(f, top=0.30, bottom=0.62)
    darken(f, vgrad(840, 1000, 0.0, 0.58) * vgrad(1440, 1520, 1.0, 0.0), SHADE)
    if text_on:
        africa(f, 640, 290, a=1.0, glow=0.5 + 0.5 * math.sin(u * 2.6))
        kinetic(f, "FOLLOW", "serif_x", 200, GOLD, 540, 1160, u, stagger=0.05, sweeps=((1.0, 2.2),))
        karaoke(f, TITLE[0] + " " + TITLE[1], "med", 54, WHITE, 540, 1290, u, 0.6, 2.4)
    return f


SCENE_TABLE = [(0.0, 4.0, "hook", s_hook), (4.0, 4.0, "fg", s_fg), (8.0, 4.0, "gtr", s_gtr), (12.0, 6.0, "fffa", s_fffa),
               (18.0, 4.0, "sd", s_sd), (22.0, 4.0, "wad", s_wad), (26.0, 4.0, "outro", s_outro)]


def frame_at(t, text_on=True):
    f = None
    for start, dur, name, fn in SCENE_TABLE:
        if start <= t < start + dur or (name == "outro" and t >= start):
            f = fn(t - start, ur=t - start, D=dur, text_on=text_on)
            break
    if text_on:
        nodes(f, t)
        if t >= DUR - 0.3:
            f *= 1 - prog(t, DUR - 0.3, DUR)
    return f


def render(out, start=0, end=None):
    end = N if end is None else end
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
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
        preview([float(x) for x in sys.argv[i + 1].split(",")], sys.argv[i + 2] if len(sys.argv) > i + 2 else "/home/claude/sa_preview.png")
    elif "--render" in sys.argv:
        i = sys.argv.index("--render")
        rng_ = sys.argv[i + 2:i + 4]
        render(sys.argv[i + 1], *(int(x) for x in rng_)) if len(rng_) == 2 else render(sys.argv[i + 1])
