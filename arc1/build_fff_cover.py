"""Build the FFFA Viognier cover image: cluster on black, luminous.

The source is a Viognier cluster shot against a pale studio wall. Three
problems have to be solved in order.

1. THE WALL IS NOT A FLAT COLOUR. It falls from a luminance sum of ~730
   at the top of the frame to ~400 at the bottom left, because the light
   rakes across it diagonally. core.remove_background works on a fixed
   white_threshold and would either keep a grey wedge at the bottom or
   eat the pale upper grapes.

   A per-ROW estimate is not enough either — that was the first attempt,
   and it failed because the falloff runs across the frame as well as
   down it. Averaging both edges of a row gives a level too high for the
   shadowed left side, so a slab of dark wall was kept as subject. The
   background is therefore modelled as a 2D FIELD: sample luminance
   wherever the pixel is neutral, fill the gaps from the nearest
   sample, and blur heavily. Every pixel is then judged against the wall
   as it actually is at that point.

2. LUMINANCE ALONE CANNOT SEPARATE THEM. The palest grapes are as bright
   as the darkest wall. Saturation can: the wall is neutral (measured
   saturation ~2) and the fruit is amber-green (~69). The test is
   therefore "bright for its row AND neutral", which neither signal
   passes on its own.

3. THE EDGE CARRIES THE WALL WITH IT. Every boundary pixel is a blend of
   grape and bright wall, so compositing straight onto black leaves a
   pale halo — the giveaway of a bad cutout. The mask is contracted a
   little before feathering, which trades a hairline of real fruit for
   no halo at all. On a dark ground that is the right trade.

Only then is the fruit brightened. Boosting before isolating would have
lifted the wall too and made step 1 harder.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/claude/styleguide/photos/fff_viognier_cluster.jpg"
OUT = "/home/claude/styleguide/photos/fff_viognier_cover.jpg"

# Grading. Deliberately restrained: the brief is luminous, not neon, and
# a variety deck's cover should still look like fruit.
SAT_GAIN = 1.38
GAMMA = 0.86          # < 1 lifts midtones
HIGHLIGHT_GAIN = 1.10
BLACK_LEVEL = 6       # not pure 0 — a dead-black ground looks like a cutout


def build():
    im = Image.open(SRC).convert("RGB")
    a = np.asarray(im).astype(float)
    h, w, _ = a.shape

    lum = a.sum(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)

    # 2D background field, built only from neutral (wall) pixels.
    neutral = sat < 18
    idx = ndimage.distance_transform_edt(~neutral, return_distances=False,
                                         return_indices=True)
    bg = lum[tuple(idx)]
    bg = ndimage.gaussian_filter(bg, sigma=60)

    is_bg = (lum > bg - 95) & (sat < 34)
    fg = ~is_bg
    fg = ndimage.binary_closing(fg, np.ones((9, 9)))
    fg = ndimage.binary_fill_holes(fg)

    lab, n = ndimage.label(fg)
    if n:
        sizes = ndimage.sum(fg, lab, range(1, n + 1))
        fg = lab == (int(np.argmax(sizes)) + 1)

    # Contract, then feather. See note 3 above.
    fg = ndimage.binary_erosion(fg, np.ones((5, 5)), iterations=2)
    alpha = ndimage.gaussian_filter(fg.astype(float), sigma=2.0)
    alpha = np.clip((alpha - 0.35) / 0.45, 0, 1)[:, :, None]

    # ---- grade the fruit -------------------------------------------
    x = a / 255.0
    grey = x.mean(axis=2, keepdims=True)
    x = np.clip(grey + (x - grey) * SAT_GAIN, 0, 1)
    x = np.power(x, GAMMA)
    x = np.clip(x * HIGHLIGHT_GAIN, 0, 1)

    ground = np.full_like(x, BLACK_LEVEL / 255.0)
    out = x * alpha + ground * (1 - alpha)

    Image.fromarray((out * 255).round().astype("uint8")).save(OUT, quality=94)
    print(f"wrote {OUT}  {im.size}  subject covers {alpha.mean():.1%} of frame")


if __name__ == "__main__":
    build()
