"""GUESS THE REGION — Baden. Arc 2.

Two pages per GTR_STYLE_GUIDE.md: page 1 poses four clues without naming
the region, page 2 reveals it. The brief: red wines as well as white.

Every clue is checkable against D3 Ch. 11 (Aug 2026 edition), the BADEN
section and the climate / grape-variety passages around it:

  A  "warmest, sunniest" -- "Germany's warmest, sunniest and one of the
     driest wine-producing regions". "Facing Alsace across the Rhine" --
     the main vineyard area "is situated on the eastern side of the Rhine
     opposite Alsace". (Pfalz also borders Alsace, but on the Rhine's west
     side, which is why "across the Rhine" does real work.)
  B  Spatburgunder "is the most planted variety"; "61 per cent of Baden's
     plantings are white".
  C  Grauburgunder and Weissburgunder: "a reputation for very good
     Grauburgunder, Weissburgunder and Chardonnay, often matured in oak";
     both varieties are "particularly" planted in Baden.
  D  "The steep, south-facing slopes around Kaiserstuhl, an extinct
     volcano, produce the fullest-bodied wines with high alcohol and
     complex, smoky ripe fruit flavours."

Reveal blurb: "from just north of Heidelberg to the Swiss border"; Muller-
Thurgau is "the second most planted variety" (so the leading white);
trocken 64 per cent in Baden in 2021 -- the same figure the Mosel Field
Guide's slide 7 charts, deliberately: a reader who swiped that deck has
already met this number.

DELIBERATELY NOT USED: co-operatives make ~75 per cent of Baden's wine
(true, but it doesn't help anyone place the region); Zone B enrichment
(true, and the sort of fact that gives the answer away to a specialist
before the clues do).

NAMING: the answer, "Baden", appears nowhere on page 1. "Alsace" does --
it is the release valve that makes the quiz solvable.

PHOTOGRAPHY, both Unsplash, both with photographer-set location data:
  page 1 blade: red grapes on the vine, Waltershofen (Freiburg im
    Breisgau) -- Sven Finger. A vertical crop centred on the cluster.
  page 2 reveal: terraced vineyards, tagged "kaiserstuhl" -- Hanna
    Schwichtenberg. Cropped tight on the terraces (the frame was half sky).
The red grapes carry the "red" half of the brief on the cover; the
whites are carried by clue C and the blurb. No variety is claimed for
either photograph.

FLAG: the reveal draws a country flag beside the region name. Baden needed
a German one, so formats/guess_the_region.py gained "german" (horizontal
black / red / gold, at Germany's true 5:3 ratio rather than the 3:2 the
other flags use). Existing decks are unchanged -- verified pixel-identical
on the Cornas deck before and after.

Social gates on a two-page quiz:
  open question ... the format is the question
  decode layer ... "facing Alsace across the Rhine": the east bank is what
                   separates Baden from Pfalz, never explained in copy
  callback ....... the 64 per cent trocken figure, from the Mosel Field
                   Guide's slide 7
"""
import glob
import os

from tokens import DEFAULT_PALETTE
import core
from guess_the_region import gtr_cover, gtr_reveal

OUT = "/home/claude/out_gtr_baden"
os.makedirs(OUT, exist_ok=True)

PAL = dict(DEFAULT_PALETTE)
PAL["ACCENT"] = (196, 158, 84)      # series gold -- fixed across GTR decks
PAL["SIGNATURE"] = (114, 47, 55)    # region-name burgundy

SLOT_COVER = dict(
    photo="gtr_baden_blade.jpg",
    # First draft ran 65-80 characters a clue and pushed the swipe cue to
    # y=2747 against a 2500 limit. The panel holds ~24 characters a line, so
    # two lines is ~45 characters: cut copy, never shrink type. What went:
    # "facing Alsace across the Rhine" split into its own clue (the release
    # valve, and the east-bank point that separates Baden from Pfalz), and
    # the Grauburgunder / Weissburgunder clue was cut -- the volcano is the
    # more placeable fact and pays off in the reveal caption. The whites are
    # carried by clue C's 61 per cent and by the blurb.
    clues=[
        "Germany's warmest, sunniest region.",
        "Across the Rhine from Alsace.",
        "Known for red, yet 61% of its vines are white.",
        "An extinct volcano shapes its fullest wines.",
    ],
    photo_credit="Sven Finger / Unsplash",
)

SLOT_REVEAL = dict(
    photo="gtr_baden_reveal.jpg",
    region="Baden",
    flag="german",
    # The first blurb (~66 words, with the white varieties and Muller-Thurgau)
    # overflowed by 94px even at the 60px type floor. Cut to the three
    # things the page is for; the varieties live in the caption instead.
    blurb="Germany's warmest, sunniest region, a strip of vineyards on the "
          "Rhine's eastern bank. Spätburgunder is its most planted grape and "
          "among the country's finest reds, yet 61 per cent of its vines are "
          "white. In 2021, 64 per cent of its wine was trocken.",
    caption="Terraced vineyards on the Kaiserstuhl, an extinct volcano",
    photo_credit="Hanna Schwichtenberg / Unsplash",
)


def build():
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
    pdf = f"{OUT}/GTR_Baden_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
