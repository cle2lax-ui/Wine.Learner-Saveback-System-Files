"""Reel toolkit: motion-graphics primitives for vertical (9:16) video, built on numpy + OpenCV + PIL.

Everything works on float32 frames (H x W x 3, 0-255). Layers are PREMULTIPLIED RGBA float32
(rgb already multiplied by alpha), so scaling, rotating and blurring them never produces dark
fringes. Kept dependency-light on purpose: one CPU and 3 GB of RAM are enough.
"""
import functools
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONT_DIR = f"{ROOT}/fonts"
PHOTO_DIR = f"{ROOT}/photos"
W, H, FPS = 1080, 1920, 30

FONT_FILES = {
    "cond": "ArchivoCond-Black.ttf", "condb": "ArchivoCond-Bold.ttf", "black": "Archivo-Black.ttf",
    "bold": "Archivo-Bold.ttf", "med": "Archivo-Medium.ttf", "serif": "Playfair-Black.ttf",
    "serif_it": "Playfair-BoldItalic.ttf", "serif_x": "Playfair-XBold.ttf",
}

# --------------------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def prog(t, a, b):
    """0 before a, 1 after b, linear between."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def out_cubic(p):
    return 1 - (1 - p) ** 3


def in_cubic(p):
    return p ** 3


def in_out_cubic(p):
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def out_expo(p):
    return 1.0 if p >= 1 else 1 - 2 ** (-10 * p)


def out_back(p, s=1.7):
    p -= 1
    return p * p * ((s + 1) * p + s) + 1


def out_elastic(p):
    if p <= 0 or p >= 1:
        return p
    return 2 ** (-10 * p) * math.sin((p * 10 - 0.75) * (2 * math.pi) / 3) + 1


# --------------------------------------------------------------------------- text
@functools.lru_cache(None)
def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{FONT_FILES[name]}", int(size))


def text_width(txt, fname, size, tracking=0):
    f = font(fname, size)
    if tracking:
        return sum(f.getlength(c) for c in txt) + tracking * (len(txt) - 1)
    return f.getlength(txt)


@functools.lru_cache(maxsize=4096)
def text_layer(txt, fname, size, color, tracking=0):
    """Premultiplied RGBA layer of a text run. Returns (layer, ox, oy): the text's left
    baseline origin sits at (ox, oy) inside the layer."""
    f = font(fname, size)
    asc, desc = f.getmetrics()
    pad = int(size * 0.35) + 4
    w = text_width(txt, fname, size, tracking)
    img = Image.new("L", (int(math.ceil(w)) + 2 * pad, asc + desc + 2 * pad), 0)
    d = ImageDraw.Draw(img)
    if tracking:
        x = pad
        for c in txt:
            d.text((x, pad + asc), c, font=f, fill=255, anchor="ls")
            x += f.getlength(c) + tracking
    else:
        d.text((pad, pad + asc), txt, font=f, fill=255, anchor="ls")
    a = np.asarray(img, np.float32) / 255.0
    layer = np.empty((img.height, img.width, 4), np.float32)
    layer[..., :3] = np.array(color, np.float32) * a[..., None]
    layer[..., 3] = a
    return layer, pad, pad + asc


def transform(layer, scale=1.0, rot=0.0, blur=0.0, mblur=0, mangle=90.0):
    """Scale/rotate about the layer center, Gaussian blur, and directional motion blur
    (mblur px along mangle degrees; 90 = vertical)."""
    out = layer
    if abs(scale - 1) > 1e-3 or abs(rot) > 1e-3:
        h, w = out.shape[:2]
        r = math.radians(rot)
        nw = int(abs(w * math.cos(r)) * scale + abs(h * math.sin(r)) * scale) + 6
        nh = int(abs(w * math.sin(r)) * scale + abs(h * math.cos(r)) * scale) + 6
        M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale)
        M[0, 2] += nw / 2 - w / 2
        M[1, 2] += nh / 2 - h / 2
        out = cv2.warpAffine(out, M, (max(nw, 1), max(nh, 1)), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    if mblur and mblur > 1:
        L = int(mblur)
        pad = L
        out = cv2.copyMakeBorder(out, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        k = np.zeros((2 * L + 1, 2 * L + 1), np.float32)
        a = math.radians(mangle)
        for i in range(-L, L + 1):
            x, y = int(round(L + i * math.cos(a))), int(round(L + i * math.sin(a)))
            k[y, x] = 1
        k /= k.sum()
        out = cv2.filter2D(out, -1, k)
    if blur > 0.3:
        pad = int(blur * 3) + 1
        out = cv2.copyMakeBorder(out, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        out = cv2.GaussianBlur(out, (0, 0), blur)
    return out


def blit(dst, layer, x, y, alpha=1.0):
    """Composite a premultiplied layer with its top-left at (x, y)."""
    if alpha <= 0.002:
        return
    h, w = layer.shape[:2]
    xi, yi = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(xi, 0), max(yi, 0), min(xi + w, W), min(yi + h, H)
    if x0 >= x1 or y0 >= y1:
        return
    L = layer[y0 - yi:y1 - yi, x0 - xi:x1 - xi]
    a = L[..., 3:4] * alpha
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + L[..., :3] * alpha


def blit_center(dst, layer, cx, cy, alpha=1.0):
    h, w = layer.shape[:2]
    blit(dst, layer, cx - w / 2, cy - h / 2, alpha)


def glow_of(layer, sigma, color, strength=1.0):
    a = cv2.GaussianBlur(layer[..., 3], (0, 0), sigma) * strength
    g = np.empty(layer.shape, np.float32)
    g[..., :3] = np.array(color, np.float32) * a[..., None]
    g[..., 3] = np.clip(a, 0, 1)
    return g


def text(dst, txt, fname, size, color, x, y, align="left", tracking=0, alpha=1.0, scale=1.0,
         dx=0.0, dy=0.0, blur=0.0, mblur=0, mangle=90.0, glow=None, rot=0.0):
    """Place a text run with its baseline at y. align: left | center | right (x is that edge)."""
    layer, ox, oy = text_layer(txt, fname, int(size), tuple(color), tracking)
    tw = text_width(txt, fname, int(size), tracking)
    left = x - (tw / 2 if align == "center" else tw if align == "right" else 0)
    cx = left - ox + layer.shape[1] / 2 + dx
    cy = y - oy + layer.shape[0] / 2 + dy
    if glow:
        gl = glow_of(layer, glow[0], glow[1], glow[2])
        blit_center(dst, transform(gl, scale, rot), cx, cy, alpha)
    lay = transform(layer, scale, rot, blur, mblur, mangle) if (scale != 1 or blur or mblur or rot) else layer
    blit_center(dst, lay, cx, cy, alpha)
    return left, tw


def letters(dst, txt, fname, size, color, x, y, anim, align="center", tracking=0, glow=None):
    """Per-letter animation. anim(i, n) -> dict(alpha, dx, dy, scale, mblur, rot, blur)."""
    tw = text_width(txt, fname, int(size), tracking)
    left = x - (tw / 2 if align == "center" else tw if align == "right" else 0)
    f = font(fname, int(size))
    xs, cur = [], left
    for c in txt:
        xs.append(cur)
        cur += f.getlength(c) + tracking
    n = len(txt)
    for i, c in enumerate(txt):
        if c == " ":
            continue
        p = anim(i, n)
        if p.get("alpha", 1) <= 0.002:
            continue
        text(dst, c, fname, size, color, xs[i], y, alpha=p.get("alpha", 1), scale=p.get("scale", 1),
             dx=p.get("dx", 0), dy=p.get("dy", 0), mblur=p.get("mblur", 0), mangle=p.get("mangle", 90),
             blur=p.get("blur", 0), rot=p.get("rot", 0), glow=glow)
    return left, tw


# --------------------------------------------------------------------------- shapes
def _mask_box(pts, pad=4):
    pts = np.asarray(pts, np.float64)
    x0 = int(max(math.floor(pts[:, 0].min()) - pad, 0)); x1 = int(min(math.ceil(pts[:, 0].max()) + pad, W))
    y0 = int(max(math.floor(pts[:, 1].min()) - pad, 0)); y1 = int(min(math.ceil(pts[:, 1].max()) + pad, H))
    return x0, y0, x1, y1


def fill_poly(dst, pts, color, alpha=1.0):
    x0, y0, x1, y1 = _mask_box(pts)
    if x0 >= x1 or y0 >= y1 or alpha <= 0:
        return
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    p = np.round((np.asarray(pts, np.float64) - [x0, y0]) * 16).astype(np.int32)
    cv2.fillPoly(m, [p], 255, lineType=cv2.LINE_AA, shift=4)
    a = m.astype(np.float32)[..., None] / 255.0 * alpha
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + np.array(color, np.float32) * a


def fill_rect(dst, x0, y0, x1, y1, color, alpha=1.0):
    fill_poly(dst, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color, alpha)


def round_rect(dst, x0, y0, x1, y1, r, color, alpha=1.0):
    bx0, by0, bx1, by1 = int(max(x0 - 2, 0)), int(max(y0 - 2, 0)), int(min(x1 + 2, W)), int(min(y1 + 2, H))
    if bx0 >= bx1 or by0 >= by1:
        return
    m = Image.new("L", ((bx1 - bx0) * 2, (by1 - by0) * 2), 0)
    ImageDraw.Draw(m).rounded_rectangle([(x0 - bx0) * 2, (y0 - by0) * 2, (x1 - bx0) * 2, (y1 - by0) * 2],
                                        radius=r * 2, fill=255)
    a = np.asarray(m.resize((bx1 - bx0, by1 - by0), Image.LANCZOS), np.float32)[..., None] / 255.0 * alpha
    dst[by0:by1, bx0:bx1] = dst[by0:by1, bx0:bx1] * (1 - a) + np.array(color, np.float32) * a


def stroke_path(dst, pts, color, width, alpha=1.0, glow=0.0, glow_color=None):
    """Anti-aliased polyline, optional soft glow underneath."""
    if len(pts) < 2:
        return
    pad = int(width + glow * 3 + 6)
    x0, y0, x1, y1 = _mask_box(pts, pad)
    if x0 >= x1 or y0 >= y1:
        return
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    p = np.round((np.asarray(pts, np.float64) - [x0, y0]) * 16).astype(np.int32)
    cv2.polylines(m, [p], False, 255, int(width), lineType=cv2.LINE_AA, shift=4)
    a = m.astype(np.float32) / 255.0
    if glow:
        g = cv2.GaussianBlur(a, (0, 0), glow)[..., None] * 0.9 * alpha
        gc = np.array(glow_color or color, np.float32)
        dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - g) + gc * g
    a = a[..., None] * alpha
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + np.array(color, np.float32) * a


def arc(dst, cx, cy, r, thick, a0, a1, color, alpha=1.0):
    """Ring arc from angle a0 to a1 (degrees, 0 = 12 o'clock, clockwise)."""
    if a1 - a0 < 0.2:
        return
    x0, y0, x1, y1 = int(cx - r - thick), int(cy - r - thick), int(cx + r + thick), int(cy + r + thick)
    m = np.zeros((y1 - y0, x1 - x0), np.uint8)
    cv2.ellipse(m, (int((cx - x0) * 16), int((cy - y0) * 16)), (int(r * 16), int(r * 16)), -90, a0, a1,
                255, int(thick), lineType=cv2.LINE_AA, shift=4)
    a = m.astype(np.float32)[..., None] / 255.0 * alpha
    sx0, sy0 = max(x0, 0), max(y0, 0)
    sub = a[sy0 - y0:sy0 - y0 + (min(y1, H) - sy0), sx0 - x0:sx0 - x0 + (min(x1, W) - sx0)]
    dst[sy0:min(y1, H), sx0:min(x1, W)] = dst[sy0:min(y1, H), sx0:min(x1, W)] * (1 - sub) + np.array(color, np.float32) * sub


# --------------------------------------------------------------------------- photos & camera
class Photo:
    """A photo prepared once at `cover` x the frame's cover size, so camera moves up to that zoom
    never upsample. view(zoom, fx, fy) frames it with zoom 1 = exactly fills the frame."""

    def __init__(self, name, cover=1.35):
        im = Image.open(f"{PHOTO_DIR}/{name}").convert("RGB")
        s = max(W * cover / im.width, H * cover / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        self.img = np.asarray(im, np.float32)
        self.sh, self.sw = self.img.shape[:2]
        self.base = max(W / self.sw, H / self.sh)

    def view(self, zoom=1.0, fx=0.5, fy=0.5):
        s = self.base * zoom
        hw, hh = W / 2 / s, H / 2 / s
        cx = clamp(fx * self.sw, hw, self.sw - hw)
        cy = clamp(fy * self.sh, hh, self.sh - hh)
        M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
        return cv2.warpAffine(self.img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def vgrad(y0, y1, a0, a1):
    """Column vector (H x 1 x 1) of alpha ramping a0 -> a1 between rows y0 and y1."""
    ys = np.arange(H, dtype=np.float32)
    t = np.clip((ys - y0) / max(y1 - y0, 1), 0, 1)
    return (a0 + (a1 - a0) * (t * t * (3 - 2 * t)))[:, None, None]


def darken(frame, amount_col, color=(0, 0, 0)):
    frame[:] = frame * (1 - amount_col) + np.array(color, np.float32) * amount_col


# --------------------------------------------------------------------------- finishing
_rng = np.random.default_rng(11)
GRAIN = [cv2.resize(_rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (W, H),
                    interpolation=cv2.INTER_LINEAR)[..., None] for _ in range(6)]
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_r = np.sqrt(((_xx - W / 2) / (W / 2)) ** 2 + ((_yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
VIGNETTE = (1 - 0.32 * np.clip(_r - 0.35, 0, 1) ** 1.5 / 0.65 ** 1.5)[..., None].astype(np.float32)
del _yy, _xx, _r


def finish(frame, fi, grain=4.0):
    frame *= VIGNETTE
    frame += GRAIN[fi % len(GRAIN)] * grain
    return np.clip(frame, 0, 255).astype(np.uint8)


def load_geo_line(path):
    g = json.load(open(path))
    return [c for part in g["features"][0]["geometry"]["coordinates"] for c in part]


def sheen(dst, txt, fname, size, x, y, p, align="left", tracking=0, band=110, angle=22, strength=0.7,
          color=(255, 255, 255)):
    """A light sheen that sweeps across already-drawn text (p: 0 -> 1). Only the glyphs catch it."""
    if p <= 0 or p >= 1:
        return
    layer, ox, oy = text_layer(txt, fname, int(size), (255, 255, 255), tracking)
    tw = text_width(txt, fname, int(size), tracking)
    left = x - (tw / 2 if align == "center" else tw if align == "right" else 0)
    h, w = layer.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    pos = -band * 2 + (w + band * 4) * p
    d = (xx + yy * math.tan(math.radians(angle))) - pos
    prof = np.exp(-(d / band) ** 2 * 2.5)
    a = layer[..., 3] * prof * strength
    s = np.empty_like(layer)
    s[..., :3] = np.array(color, np.float32) * a[..., None]
    s[..., 3] = a
    blit(dst, s, left - ox, y - oy)


def chip(dst, label, x, y, q, fill=(221, 0, 0), ink=(255, 255, 255), size=34, align="center", tracking=2):
    """A rounded label chip that pops in (q: 0 -> 1, eased by the caller)."""
    if q <= 0:
        return
    tw = text_width(label, "black", size, tracking) + 56
    cx = x if align == "center" else x + tw / 2
    hh = size * 0.98
    round_rect(dst, cx - tw / 2 * q, y - hh * q, cx + tw / 2 * q, y + hh * q, int(hh), fill)
    text(dst, label, "black", size, ink, cx, y + size * 0.36, align="center", tracking=tracking,
         alpha=min(1.0, q * 1.2), scale=q)
