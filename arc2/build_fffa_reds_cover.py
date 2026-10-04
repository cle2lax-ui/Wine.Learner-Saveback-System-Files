"""Build the two photographs the FFFA "Red Wines of Germany" deck grades: the cover, and
the Stuttgart terraces on the closing page.

WHY A BUILD STEP. The photograph (Saman Taheri / Unsplash, 4912x7360) is a portrait
whose glass runs from ~14% to ~86% of the frame, and fff_cover() sets its type in the
lower third of the page, so the title would cross the stem and base. Rather than crop
into the glass or put a scrim over it, the whole glass is placed in the UPPER part of the
page and the photo's own black background is extended below it for the type -- the same
idea as build_fff_cover.py for the Viognier cover.

HOW. The photo is scaled to 28% (so the glass is ~1,480px tall), shifted up so the splash
tip sits ~190px from the top and the base clears the type zone (~y=1788), then composited
over flat near-black with feathered left, right and bottom edges so the spotlit halo fades
into the black instead of ending in a visible rectangle. Output is exactly 2160x2700, so
fff_cover() adds no further crop. The glass was first placed 110px up; the base then came
within ~50px of the kicker icon, tight against the 120px rhythm elsewhere, so it is 150px.

THE GLASSES COVER (current). Steve supplied a photograph of two glasses of red wine at a
candlelit table (photos/de_reds_cover_glasses_612.jpg, 612x408 px, no embedded credit or licence
data) and asked for a close crop on the glasses. That is a 334 px-wide crop filling a 2160 px
cover: a 6.5x ENLARGEMENT, which no treatment can make sharp. What was done to make it as good as
it can be (see build_glasses_cover): crop 334x339 around both glasses; denoise first (the JPEG's
8x8 blocks show as stair-steps on the rims under plain Lanczos); two 2x Lanczos steps; a light
unsharp mask; and fine monochrome film grain (sigma 5) so the remaining softness reads as
photographic texture rather than blur. The stems and table fade into near-black below the wine so
the type has a dark zone, as with the splash cover. The earlier splash cover is retained
(`--splash`) but no longer used.

THE TERRACES (closing page). The Stuttgart photograph is a dusk shot: its photo band measured
0.040 mean luminance against 0.19-0.30 on the deck's other five pages. A gamma lift of 0.6
(x ** 0.6) takes it to 0.095: the stone walls, huts and vine rows become legible and the dusk
mood survives; 0.5 (0.126) started to look flat. The original is untouched; the graded copy is
photos/de_reds_stuttgart_terraces_graded.jpg.
"""
import os
import sys

import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = f"{ROOT}/photos/de_reds_cover_splash.jpg"
OUT = f"{ROOT}/photos/fff_reds_cover.jpg"
W, H = 2160, 2700
SCALE = 0.28
SHIFT_UP = 150
FEATHER_SIDES, FEATHER_BOTTOM = 280, 220


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def build_glasses_cover(sigma_grain=5.0):
    import cv2
    from PIL import ImageFilter
    src = Image.open(f"{ROOT}/photos/de_reds_cover_glasses_612.jpg").convert("RGB")
    X0, X1, Y0 = 17, 351, 69          # tight on both glasses; the rims land ~330px from the top
    crop = src.crop((X0, Y0, X1, src.height))
    s = W / crop.width
    size = (W, int(round(crop.height * s)))
    den = cv2.fastNlMeansDenoisingColored(np.asarray(crop)[:, :, ::-1].copy(), None, 4, 4, 5, 15)[:, :, ::-1]
    x = Image.fromarray(den)
    for _ in range(2):
        x = x.resize((x.width * 2, x.height * 2), Image.LANCZOS)
    x = x.resize(size, Image.LANCZOS).filter(ImageFilter.UnsharpMask(2.5, 90, 2))
    arr = np.asarray(x).astype(float)
    rng = np.random.default_rng(7)
    arr = arr + rng.normal(0, sigma_grain, arr.shape[:2])[..., None]
    bg = np.array([10.0, 6.0, 5.0])
    canvas = np.zeros((H, W, 3)); canvas[:] = bg
    # opaque down to 1620 (just under the wine), fully black by ~1880. First pass faded over
    # 500px (to ~2150), which left the thin stems running behind the kicker icon (the type zone
    # starts at ~1788); this clears them before it.
    ys = np.arange(arr.shape[0], dtype=float)[:, None]
    alpha = 1 - smooth((ys - 1620) / 260.0)
    canvas[:arr.shape[0]] = canvas[:arr.shape[0]] * (1 - alpha[..., None]) + arr * alpha[..., None]
    out = f"{ROOT}/photos/fff_reds_cover_glasses.jpg"
    Image.fromarray(canvas.clip(0, 255).astype("uint8")).save(out, quality=95)
    print(f"glasses cover built: {out}  (crop {crop.size}, enlarged x{s:.2f}, grain sigma {sigma_grain})")


def grade_terraces(gamma=0.6):
    src = Image.open(f"{ROOT}/photos/de_reds_stuttgart_terraces.jpg").convert("RGB")
    a = np.asarray(src).astype(float) / 255.0
    out = f"{ROOT}/photos/de_reds_stuttgart_terraces_graded.jpg"
    Image.fromarray((np.clip(a ** gamma, 0, 1) * 255).astype("uint8")).save(out, quality=95)
    print(f"terraces graded (gamma {gamma}): {out}")


def main():
    grade_terraces()
    build_glasses_cover()
    if "--splash" in sys.argv:
        build_splash_cover()


def build_splash_cover():
    src = Image.open(SRC).convert("RGB")
    a = np.asarray(src).astype(float)
    edge = np.concatenate([a[:40].reshape(-1, 3), a[:, :40].reshape(-1, 3), a[:, -40:].reshape(-1, 3)])
    bg = np.median(edge, axis=0)                       # the photo's own near-black
    sw, sh = int(src.width * SCALE), int(src.height * SCALE)
    ph = np.asarray(src.resize((sw, sh), Image.LANCZOS)).astype(float)
    x0, y0 = (W - sw) // 2, -SHIFT_UP
    canvas = np.zeros((H, W, 3)); canvas[:] = bg
    # alpha for the placed photo: 1 inside, feathered toward the left, right and bottom edges
    xs = np.arange(sw)[None, :].astype(float); ys = np.arange(sh)[:, None].astype(float)
    alpha = smooth(np.minimum(xs, sw - 1 - xs) / FEATHER_SIDES) * smooth((sh - 1 - ys) / FEATHER_BOTTOM)
    top, bot = max(y0, 0), min(y0 + sh, H)
    sub_ph, sub_a = ph[top - y0:bot - y0], alpha[top - y0:bot - y0][..., None]
    canvas[top:bot, x0:x0 + sw] = canvas[top:bot, x0:x0 + sw] * (1 - sub_a) + sub_ph * sub_a
    Image.fromarray(canvas.clip(0, 255).astype("uint8")).save(OUT, quality=95)
    print(f"cover built: {OUT}  (bg {tuple(int(v) for v in bg)}, glass scaled to {sw}x{sh})")


if __name__ == "__main__":
    main()
