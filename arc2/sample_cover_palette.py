"""Derive the Mosel Field Guide chart palette from its own cover photo.

Steve asked that the graph colours on slides 4, 6, 7 and 8 match the
cover. Rather than pick colours by eye, this samples named features of
the exact crop the cover shows (same zoom/anchor as render_cover) and
prints the result. Each value is the mean of the most saturated, mid-
light pixels of a hue family inside a hand-chosen region, so it
reflects the colour where the light actually hits, not a shadow-muddied
average. Re-run if the cover photo or its crop changes; paste any new
values into CHART in render_fg_mosel.py.

The sampling method itself is engine/palette.py (reusable by any deck);
this file is only the Mosel's configuration of it -- which features, in
which regions of its cover.

Usage: PYTHONPATH=../engine:../formats python3 sample_cover_palette.py
"""
from core import cover_fit, load_photo
from palette import sample_palette
from tokens import W, H
import render_fg_mosel as r

# name: (hue range deg, (row0,row1,col0,col1) in the 540x675 working
# crop, min saturation, lightness range, fraction of pixels kept)
FEATURES = {
    "vineyard_gold":   ((40, 56), (140, 260, 40, 420), 0.35, (0.18, 0.85), 0.12),
    "leaf_yellow":     ((48, 64), (100, 330, 0, 540), 0.45, (0.18, 0.85), 0.12),
    "reflection_orange": ((22, 40), (490, 560, 0, 540), 0.60, (0.30, 0.75), 0.25),
    "window_orange":   ((20, 38), (370, 430, 230, 400), 0.60, (0.30, 0.80), 0.25),
    "brick_red":       ((0, 16), (330, 440, 0, 540), 0.30, (0.20, 0.70), 0.30),
    "forest_green":    ((75, 135), (40, 300, 150, 540), 0.25, (0.14, 0.85), 0.30),
    "water_teal":      ((150, 215), (540, 675, 0, 540), 0.06, (0.06, 0.50), 0.50),
    "sky":             ((170, 215), (0, 60, 0, 540), 0.15, (0.55, 0.95), 0.50),
}


def main():
    sl = r.SLIDES[0][1]
    im = cover_fit(load_photo(sl["photo"]), W, H, y_anchor=sl["photo_anchor"],
                   zoom=sl["photo_zoom"]).convert("RGB")
    got = sample_palette(im, FEATURES)
    for name in FEATURES:
        if name in got:
            rgb, n = got[name]
            print(f"{name:18s} {rgb}   ({n} px)")
        else:
            print(f"{name:18s} too few pixels")


if __name__ == "__main__":
    main()
