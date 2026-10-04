"""FFFA — Five Fascinating Facts About Red Wines of Germany. Arc 2.

Fixed 6-page format per FFFA_STYLE_GUIDE.md: fff_cover() once, then fff_fact() five times,
the fifth with closing=True folding "Cheers!" into the same page. Never 7 pages.

SOURCES. Every fact is from D3 Ch. 11 (Aug 2026 edition), the primary source, then checked
against current official figures (Wines of Germany / the German Wine Society's tables of
the 2022-25 statistics). The two disagree in a few places, and the copy is worded to be
TRUE UNDER BOTH rather than to pick a winner:

  Ahr's red share ... D3: 81%.  Wines of Germany 2025: 79% (and the highest of any region,
                      535 ha now vs D3's 560).  -> "Four in Five", chart bar "about 80%".
  Wurttemberg ....... D3: 66% black, "most planted: Trollinger, Lemberger and Schwarzriesling".
                      2022 statistics put Spatburgunder (11.5%) AHEAD of Schwarzriesling
                      (10.5%); Trollinger (16.7%) and Lemberger (15.5%) are 1 and 2 in both.
                      -> "Trollinger and Lemberger lead"; the Schwarzriesling/Spatburgunder
                      order, where D3 is slightly behind the figures, is avoided.
  Germany's red share  D3: 32% of plantings black in 2021; 90% white in 1980. Not disputed.

FACTS (all D3 Ch. 11 unless stated)
  1  1980: 90% white. 2021: 32% black. "the wines had improved": D3 says quality has
     "improved greatly" (better clones, vineyard management, warmer vineyards); the copy does
     not claim those CAUSED the planting increase, which D3 does not say. The chart's 1980 bar
     is "about 10%": D3 gives only "90 per cent white", so black is the remainder.
  2  Spatburgunder: Germany's most planted black grape, 11.5% of plantings; plantings "almost
     trebled"; "thrives particularly in warmer areas such as Baden".
  3  Dornfelder: the most significant black German cross, "from nothing" to second most
     planted black variety "in the past 30 years"; the most planted black in Rheinhessen and
     Pfalz, ahead of Spatburgunder.
  4  Ahr: very small, one of the most northerly; black grapes dominate; "narrow, sheltered
     valley with steep, south-facing slopes ... heat-retaining dark slate and greywacke".
  5  Wurttemberg: 66% black; fuller, riper, oak-aged examples "particularly from Lemberger".

LEFT OUT, DELIBERATELY (true or plausible, not in D3, or single-sourced)
  - "Germany is the world's third-largest Pinot Noir grower, after France and the USA": real,
    but from one DWI-affiliated site only. A strong candidate if a second source is found.
  - Dornfelder bred in 1955 (a secondary source, not D3); Fruhburgunder; Regent.
  - Any claim about Ahr or Wurttemberg prices.

HEADLINE COLOUR. A red-wine subject takes the per-deck override (style guide v3): sampled
from the cover's splash by the guide's method (the 80 brightest SATURATED reds, not the
blown-out pinks): (246, 31, 13), contrast 3.86:1 against INK (floor 3.0). The cover itself is a
graded build (build_fffa_reds_cover.py): the glass sits high so the type has black below it.

PHOTOGRAPHY, location-verified; FFFA fact pages carry credits only, never captions, so no
location is asserted on a page. Cover: red wine splash, Saman Taheri (Unsplash). 1: Rheinhessen
(Jugenheim) vineyard at sunrise, Sven Wilhelm. 2: red grapes, Waltershofen (Baden), Sven Finger.
3: dark grapes, Rheinland-Pfalz, Luca J. 4: autumn vines on steep slate terraces at
Mayschoss (Ahr), Superbass (Commons, CC BY-SA 3.0): Mayschoss is the village D3 names for the
oldest co-operative in the world. 5: terraced vineyards, Stuttgart, Heliao. Grape varieties
are NOT asserted for any photograph.

Social gates on a 6-page facts post:
  save asset ..... the five facts, and the two charts
  send line ...... fact 1: "In 1980, nine in ten vines were white."
  decode layer ... fact 5's headline: Pinot Meunier (Schwarzriesling) IS a Pinot, which is why
                   it says "Not Led by Pinot Noir", not "Not Pinot"
  callback ....... fact 2 names Baden: the Baden GTR is "Known for red, yet 61% of its vines
                   are white"; fact 5 pairs with the Mosel Field Guide's sweetness ladder
                   (not used here) only by being another D3 Ch. 11 region
"""
import glob
import os

import core
from fff_facts import fff_cover, fff_fact

OUT = "/home/claude/out_fffa_german_reds"
os.makedirs(OUT, exist_ok=True)
TOTAL = 6

# Sampled from the cover's splash: see the docstring and the style guide.
RED = (246, 31, 13)

CRED_TAHERI = "Saman Taheri / Unsplash"
CRED_WILHELM = "Sven Wilhelm / Unsplash"
CRED_FINGER = "Sven Finger / Unsplash"
CRED_LUCA = "Luca J / Unsplash"
CRED_SUPERBASS = "Superbass / Wikimedia Commons (CC BY-SA 3.0)"
CRED_HELIAO = "Heliao / Unsplash"

COVER = dict(
    photo="fff_reds_cover.jpg",          # the graded build, not the raw file
    subject="Red Wines of Germany",
    photo_credit=CRED_TAHERI,
)

SHARE = "BLACK GRAPES AS A SHARE OF ALL PLANTINGS"

FACTS = [
    dict(
        number=1,
        photo="de_reds_rheinhessen_rows",
        photo_anchor=0.5,
        headline="Nearly a Third of German Vines Are Red",
        body="In 1980, nine in ten vines were white. By 2021, 32 per cent were black, "
             "and the wines had improved.",
        bars_title=SHARE,
        bars=[("1980", 10, "about 10%", False), ("2021", 32, "32%", True)],
        photo_credit=CRED_WILHELM,
        diagram="bars",
    ),
    dict(
        number=2,
        photo="de_baden_red_grapes",
        photo_anchor=0.5,
        headline="Germany's Pinot Noir Almost Trebled",
        body="Spätburgunder is its most planted red grape, at 11.5 per cent of all "
             "vines, and thrives in warm Baden.",
        photo_credit=CRED_FINGER,
    ),
    dict(
        number=3,
        photo="de_reds_rlp_grapes",
        photo_anchor=0.45,
        # "Number Two" alone could read as second overall: it is second among REDS.
        headline="Dornfelder Went From Nothing to No. 2 Red",
        body="This German crossing rose in 30 years to second most planted red, and is "
             "the leading red in Rheinhessen and Pfalz.",
        photo_credit=CRED_LUCA,
    ),
    dict(
        number=4,
        photo="de_reds_ahr_mayschoss",
        photo_anchor=0.5,
        headline="Four in Five Ahr Vines Are Red",
        # First draft ended on an orphaned "it possible." line.
        body="One of Germany's most northerly regions, where steep, sheltered, "
             "south-facing slopes of dark slate hold the heat.",
        bars_title=SHARE,
        bars=[("Germany", 32, "32%", False), ("Württemberg", 66, "66%", False),
              ("Ahr", 80, "about 80%", True)],
        photo_credit=CRED_SUPERBASS,
        diagram="bars",
    ),
    dict(
        number=5,
        photo="de_reds_stuttgart_terraces_graded",   # gamma 0.6; see build_fffa_reds_cover.py
        photo_anchor=0.5,
        # First draft: "Two-Thirds Red, but Not Led by Pinot Noir", on two lines, which pushed
        # "Cheers!" to 57px from the page edge (the margin is 120). One line brings it up; and
        # "Not Pinot" would have been wrong anyway: Schwarzriesling IS a Pinot (Meunier), so the
        # claim is specifically about Pinot Noir and lives in the body.
        headline="Württemberg Is Two-Thirds Red",
        body="Trollinger and Lemberger lead, not Pinot Noir. Lemberger, often oak-aged, "
             "is making fuller, riper reds.",
        photo_credit=CRED_HELIAO,
    ),
]


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    paths = []
    img = fff_cover(COVER, total=TOTAL, headline_color=RED)
    p = f"{OUT}/01_cover.png"
    img.save(p)
    paths.append(p)
    print("  01  cover")

    for i, slot in enumerate(FACTS, start=2):
        img = fff_fact(slot, i, total=TOTAL, closing=(i == TOTAL),
                       diagram=slot.get("diagram"), headline_color=RED)
        p = f"{OUT}/{i:02d}_fact{slot['number']}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  fact {slot['number']}")

    pdf = f"{OUT}/FFFA_German_Reds_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
