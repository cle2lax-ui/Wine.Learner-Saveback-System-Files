"""Derive The Field Guide: Mendocino (classic deck) chart palette from its own cover photo.

Same method as the benchmark (arc2/sample_cover_palette.py; engine/palette.py): the most saturated, mid-light pixels of
each named feature inside a hand-chosen region of the EXACT cover crop. Cover: 'Hillside Vineyards in Anderson Valley'
(Naotake Murayama, CC BY 2.0), anchor 0.5, zoom 1.0. Regions are in the 540x675 working image:
  sky        rows 0-200        the clear summer sky
  hill_gold  rows 250-400      the golden summer grass on the hills
  redwood    rows 230-430      the dark conifer stands on the hills
  vine       rows 440-620      the sunlit vine canopy
  shade      rows 600-675      the canopy's shade near the trunks
Re-run if the cover or its crop changes; paste new values into CHART in render_fg_mendocino_classic.py.
Usage: PYTHONPATH=../engine python3 sample_fg_classic_palette.py
"""
from core import cover_fit, load_photo
from palette import sample_palette
from tokens import W, H

FEATURES = {
    "sky":       ((200, 225), (0, 200, 0, 540), 0.30, (0.45, 0.85), 0.30),
    "hill_gold": ((22, 48), (250, 400, 0, 540), 0.15, (0.45, 0.85), 0.20),
    "redwood":   ((80, 170), (230, 430, 0, 540), 0.15, (0.08, 0.35), 0.40),
    "vine":      ((65, 110), (440, 620, 0, 540), 0.40, (0.25, 0.60), 0.20),
    "shade":     ((60, 140), (600, 675, 0, 540), 0.20, (0.06, 0.30), 0.40),
}


def main():
    im = cover_fit(load_photo("us_mendo_av_hillside_murayama"), W, H, y_anchor=0.5, zoom=1.0).convert("RGB")
    got = sample_palette(im, FEATURES)
    for name in FEATURES:
        print(f"{name:10s} {got[name][0] if name in got else 'too few pixels'}   ({got.get(name, (0, 0))[1]} px)")


if __name__ == "__main__":
    main()
