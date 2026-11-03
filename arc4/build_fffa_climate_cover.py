"""Graded cover for the FFFA Climate Change deck: darkens the lower part of the Franschhoek photo (the vine rows under the cover type and footer), leaves the sky
and mountain alone. The original (photos/fffa_climate_cover_franschhoek.jpg, South African Tourism, CC BY 2.0) is kept untouched; this writes a graded COPY.
Why: on the ungraded cover the page number measured 3.26:1 and the credit 3.83:1 (needs 4.5:1) against the bright orange rows. A smooth multiplicative ramp
(smoothstep, no visible start line), same idea as arc3/build_fffa_mendocino_cover.py. The floor was SWEPT against engine/text_audit.py.
Usage: python3 build_fffa_climate_cover.py [ramp_start=0.45] [floor=0.66] [out_name=fffa_climate_cover]
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.join(HERE, "..", "photos")


def build(ramp_start=0.45, floor=0.66, out_name="fffa_climate_cover"):
    im = Image.open(os.path.join(PHOTOS, "fffa_climate_cover_franschhoek.jpg")).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    h = a.shape[0]
    t = np.clip((np.linspace(0, 1, h) - ramp_start) / (1 - ramp_start), 0, 1)
    t = t * t * (3 - 2 * t)
    mult = 1.0 - (1.0 - floor) * t
    Image.fromarray(np.clip(a * mult[:, None, None], 0, 255).astype(np.uint8)).save(os.path.join(PHOTOS, out_name + ".jpg"), quality=95)
    return im.size


if __name__ == "__main__":
    rs = float(sys.argv[1]) if len(sys.argv) > 1 else 0.45
    fl = float(sys.argv[2]) if len(sys.argv) > 2 else 0.66
    nm = sys.argv[3] if len(sys.argv) > 3 else "fffa_climate_cover"
    print("graded cover written from a", build(rs, fl, nm), "source")
