"""Graded cover for the Mendocino FFFA deck: darkens the lake under the cover type, leaves the vineyard and sky alone.

The original photo (us_mendo_garzini_cc0, No-till-vineyard, CC0) is kept untouched; this writes a graded COPY,
photos/fffa_mendocino_cover.jpg. Why: on the ungraded cover the white kicker measured 3.46:1 against the MEDIAN water
behind it but only 2.90:1 against the brightest water pixels, and the yellow subject 2.31:1 at its worst; the water is
a mid-blue lit by the sky. The grade is a smooth multiplicative ramp over the lower part of the photo, so it reads as
deeper water, not as a scrim box. Same idea as arc2/build_fffa_reds_cover.py.
Usage: python3 build_fffa_mendocino_cover.py [ramp_start=0.50] [floor=0.58]
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "..", "photos")


def build(ramp_start=0.50, floor=0.58):
    im = Image.open(os.path.join(PHOTOS, "us_mendo_garzini_cc0.jpg")).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    h = a.shape[0]
    y = np.linspace(0, 1, h)
    t = np.clip((y - ramp_start) / (1 - ramp_start), 0, 1)
    t = t * t * (3 - 2 * t)                       # smoothstep: no visible start line
    mult = 1.0 - (1.0 - floor) * t
    out = np.clip(a * mult[:, None, None], 0, 255).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(PHOTOS, "fffa_mendocino_cover.jpg"), quality=95)
    return im.size


if __name__ == "__main__":
    rs = float(sys.argv[1]) if len(sys.argv) > 1 else 0.50
    fl = float(sys.argv[2]) if len(sys.argv) > 2 else 0.58
    print("graded cover written from a", build(rs, fl), "source")
