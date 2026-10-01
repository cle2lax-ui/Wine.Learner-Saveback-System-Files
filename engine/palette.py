"""Derive a deck's chart palette from its OWN cover photo.

The Mosel Field Guide (the system's visual benchmark) colours every chart
from the cover: vineyard gold, lamp orange, brick roofs, forest green, the
river's near-black teal -- each sampled from a named feature of the exact
cover crop, not picked by eye. This module is that method, made reusable.
See guides/VISUAL_BENCHMARK_v10.md.

How a feature is sampled: take the pixels inside a hand-chosen region whose
hue falls in a given range (and which are saturated and neither near-black
nor near-white), rank them by saturation weighted toward mid-lightness, and
average the top fraction. That gives the colour as it looks WHERE THE LIGHT
HITS, not a shadow-muddied average -- which matters on a moody photo, where
a plain average of "the foliage" comes out brown.

Typical use (see arc2/sample_cover_palette.py for a full worked example):

    img = <the cover exactly as rendered, RGB>
    FEATURES = {"vineyard_gold": ((40, 56), (140, 260, 40, 420), 0.35, (0.18, 0.85), 0.12), ...}
    for name, (rgb, n) in sample_palette(img, FEATURES).items(): ...

Then build the deck's chart dict from the results, check EVERY text/fill
pairing with core.contrast (>=4.5:1 body, >=3:1 large type), and adjust an
accent where one fails -- the Mosel deck's first tile accents measured
1.9:1 and 2.8:1 and had to change.
"""
import colorsys

import numpy as np


def sample_palette(img, features, work_size=(540, 675)):
    """features: {name: (hue_range_deg, (row0, row1, col0, col1),
    min_saturation, (min_lightness, max_lightness), keep_fraction)}; the
    box is in the img resized to work_size (cols, rows). Returns
    {name: ((r, g, b), n_pixels_in_family)}; a feature with fewer than 20
    matching pixels is omitted rather than guessed."""
    a = np.asarray(img.convert("RGB").resize(work_size)).astype(float)
    hls = np.array([[colorsys.rgb_to_hls(*(p / 255)) for p in row] for row in a])
    out = {}
    for name, (hue, (r0, r1, c0, c1), min_s, (lo, hi), keep) in features.items():
        sub = a[r0:r1, c0:c1].reshape(-1, 3)
        h = hls[r0:r1, c0:c1, 0].ravel() * 360
        l = hls[r0:r1, c0:c1, 1].ravel()
        s = hls[r0:r1, c0:c1, 2].ravel()
        idx = np.where((h >= hue[0]) & (h <= hue[1]) & (s >= min_s) & (l >= lo) & (l <= hi))[0]
        if len(idx) < 20:
            continue
        order = idx[np.argsort(-s[idx] * (1 - abs(l[idx] - 0.5)))][:max(20, int(len(idx) * keep))]
        out[name] = (tuple(int(v) for v in sub[order].mean(0)), len(idx))
    return out
