"""GUESS THE REGION — Cornas. Arc 1, Wed 9 September.

Two pages per GTR_STYLE_GUIDE.md: page 1 poses four clues without
naming the region, page 2 reveals it.

Every clue is checkable against D3 Ch. 7, Cornas AOC: red wine only,
100% Syrah, no white grape permitted; a south- and east-facing
amphitheatre with some steep slopes on granite; warm, well sheltered,
so usually the first Syrah harvested in the northern Rhône; 145 ha;
40 hL/ha. Clue D's twelve-times figure is Crozes-Hermitage's ~1,700 ha
against Cornas's 145 -- the same comparison the Quick Sips detail page
makes, deliberately, since a reader who saw Monday's post can solve
this one and that is a reward rather than a leak.

The etymology of "Cornas" as an Occitan phrase for burnt earth is
often repeated and is NOT in the primary sources. It is not used here.

PHOTOGRAPHY. Steve's call to use the shot with the church tower, on
the grounds that only enthusiasts will place it. Handled by splitting
the frame rather than repeating it: page 1's blade is a vertical crop
from the right of the image -- vines, valley, haze, no tower -- and
page 2's reveal is the full frame with the tower in it. So the
landmark lands on the answer page where it belongs, the two pages do
not look like one picture used twice, and page 1 does not repeat
Monday's Quick Sips cover in the grid.

Social gates carried on a 2-page quiz:
  open question ... the format is the question
  decode layer ... the church tower on page 2, never mentioned in copy
  send line ...... "no white, no rosé, no exceptions"
  callback ....... clue D pays off Monday's Cornas post; the reveal
                   pays forward into Saturday's Split Decision
"""
import os

from tokens import DEFAULT_PALETTE
import core
from guess_the_region import gtr_cover, gtr_reveal

OUT = "/home/claude/out_gtr_cornas"
os.makedirs(OUT, exist_ok=True)

PAL = dict(DEFAULT_PALETTE)
PAL["ACCENT"] = (196, 158, 84)      # series gold — fixed across GTR decks
PAL["SIGNATURE"] = (114, 47, 55)    # region-name burgundy

CREDIT = "Jacques Forêt / Wikimedia Commons (CC BY-SA 4.0)"

SLOT_COVER = dict(
    photo="gtr_cornas_blade.jpg",
    # Two lines each at most, per the guide. The first pass ran B and D
    # to three lines, which is the signal to cut copy rather than shrink.
    #
    # Clue C originally read "the earliest harvest in its valley" — cut,
    # because the valley includes the southern Rhône, which is warmer and
    # picks earlier. D3's claim is that Cornas is often the first Syrah
    # picked in the NORTHERN Rhône. Scoped down to something true.
    clues=[
        "Red wine only — no white, no rosé.",
        "One black grape, on granite, facing south.",
        "145 hectares, and often the first Syrah picked.",
        "Across the river, a cru twelve times its size.",
    ],
    photo_credit=CREDIT,
)

SLOT_REVEAL = dict(
    photo="gtr_cornas_reveal.jpg",
    region="Cornas",
    blurb="The smallest of the northern Rhône's red appellations, and the only "
          "one whose rules permit no white grape at all. Warm, sheltered and "
          "steep, it ripens first and ages longest — a wine built on tannin "
          "rather than charm.",
    # No caption. The adaptive logic placed it top-right over sunlit
    # foliage where it read poorly, and "vines above the village" told
    # the reader nothing the photograph and the region name below it do
    # not already say.
    photo_credit=CREDIT,
)


def build():
    import glob
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    paths = []
    for i, (fn, slot) in enumerate([(gtr_cover, SLOT_COVER),
                                    (gtr_reveal, SLOT_REVEAL)], start=1):
        img = fn(slot, i, 2, PAL)
        p = f"{OUT}/{i:02d}_{'cover' if i == 1 else 'reveal'}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  {'cover' if i == 1 else 'reveal'}")
    pdf = f"{OUT}/GTR_Cornas_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
