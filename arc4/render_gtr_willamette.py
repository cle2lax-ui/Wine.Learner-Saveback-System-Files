"""GUESS THE WINE REGION -- Willamette Valley, "Same Latitude, Different Ocean". Arc 4, entry 2 (the Climate arc).

Two pages per GTR_STYLE_GUIDE.md. It tests The Field Guide: Climate's Impact on Wine (slide 6, the Willamette-vs-Margaux duel), posted days earlier.

CLUES (escalating: the hardest first, the release valve last; each checkable against D1 Ch. 3, p. 30, or D3 Ch. 24):
  A  "Its growing season averages just 15.9C."   D1 p. 30: "average growing season temperature in Willamette Valley is 15.9C / 61F" (the Fahrenheit is D1's own, added at Steve's request).
  B  "A cold Pacific current cools it."           D1 p. 30: the west coast of North America, "including Oregon, is cooled by the cold California current,
                                                  which flows from the northern Pacific". The current is not NAMED: "California" would mislead half the solvers.
  C  "Its main grape ripens early: Pinot Noir."   D1 p. 30: "the main grape in the Willamette is early-ripening Pinot Noir".
  D  "Level with Margaux in Bordeaux: about 45 N." D1 p. 30: both "located at approximately 45 degrees latitude". The release valve: Margaux is the foil, never the answer.
REVEAL: "only 80 kilometers (50 miles) from the Pacific Ocean" and "one of the coolest ... areas in Oregon" (D3 Ch. 24); Margaux 17.7C (D1 p. 30);
  Margaux "is capable of growing late-ripening Cabernet Sauvignon" (D1 p. 30).
HEDGE kept from the Field Guide review: D1 says Margaux's warmth is "at least partially due to the Gulf Stream". The Gulf Stream is not asserted here at all.
NOT DERIVED: the 1.8C gap (17.7 minus 15.9) stays off the slide; both of D1's own numbers are shown instead.

DELIBERATELY NOT USED: the Willamette's 11,000 ha, 700 wineries and Portland (true, but they place the region for anyone who knows Oregon); the Van Duzer
  Corridor wind (the best Willamette fact, saved for a later post); the California Current by name.
PHOTOS: cover, a foggy headland and the cold Pacific (Bonnie Moreland, public domain, Wikimedia Commons; "Foggy morning on Beverly Beach, Oregon"; no caption on the
  slide, so no place is claimed; chosen because the cover must not repeat a photo from an earlier post, and it carries clue B's cold Pacific);
  reveal, vineyard in the Willamette Valley (Sheila Sund, CC BY 2.0, Wikimedia Commons; place from the Commons file title).
FLAG: the reveal needed a US flag, so formats/guess_the_region.py gained "us" (13 stripes, 50 stars, the official 1.9:1). Existing decks are unchanged.
Social gates on a two-page quiz: open question ... the format is the question; callback ... clue D, and the caption points to the Field Guide's slide 6.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
sys.path.insert(0, os.path.join(HERE, "..", "formats"))
from tokens import DEFAULT_PALETTE   # noqa: E402
import core                           # noqa: E402
from guess_the_region import gtr_cover, gtr_reveal   # noqa: E402

OUT = "/home/claude/out_gtr_willamette"
os.makedirs(OUT, exist_ok=True)

PAL = dict(DEFAULT_PALETTE)
PAL["ACCENT"] = (196, 158, 84)      # series gold, fixed across GTR decks
PAL["SIGNATURE"] = (114, 47, 55)    # region-name burgundy

SLOT_COVER = dict(
    photo="gtr_willamette_blade.jpg",
    swipe_label="READ MORE",
    clues=[
        "Its growing season averages 15.9\u00b0C (61\u00b0F).",
        "A cold Pacific current cools it.",
        "Its main grape ripens early: Pinot Noir.",
        "Level with Margaux in Bordeaux: about 45\u00b0 N.",
    ],
    photo_credit="Bonnie Moreland / Wikimedia Commons (public domain)",
)

SLOT_REVEAL = dict(
    photo="gtr_willamette_reveal.jpg",
    region="Willamette Valley",
    flag="us",
    blurb="A cool Oregon valley, 80 km (50 miles) from the Pacific. A cold current cools it to 15.9\u00b0C, while "
          "Margaux, at the same latitude, averages 17.7\u00b0C. Its main grape is early-ripening Pinot Noir; Margaux "
          "can grow late-ripening Cabernet Sauvignon.",
    caption="Vineyard in the Willamette Valley",
    photo_credit="Sheila Sund / Wikimedia Commons (CC BY 2.0)",
)

SLIDES = [("gtr_cover", SLOT_COVER), ("gtr_reveal", SLOT_REVEAL)]


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)
    paths = []
    for i, (fn, slot) in enumerate([(gtr_cover, SLOT_COVER), (gtr_reveal, SLOT_REVEAL)], start=1):
        img = fn(slot, i, 2, PAL)
        p = f"{OUT}/{i:02d}_{'cover' if i == 1 else 'reveal'}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  {'cover' if i == 1 else 'reveal'}")
    pdf = f"{OUT}/GTR_Willamette_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
