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
     is "about 10%": D3 says only that 90 percent of plantings were white, so black is the remainder.
  2  Spatburgunder: Germany's most planted black grape, 11.5% of plantings; plantings "almost
     trebled" (D3's British wording; the deck says "tripled"); "thrives particularly in warmer areas such as Baden".
  3  Dornfelder: the most significant black German cross, "from nothing" to second most
     planted black variety "in the past 30 years"; the most planted black in Rheinhessen and
     Pfalz, ahead of Spatburgunder.
  4  Ahr: very small, one of the most northerly; black grapes dominate; "narrow, sheltered
     valley with steep, south-facing slopes ... heat-retaining dark slate and greywacke".
  5  Wurttemberg: 66% black; Trollinger and Lemberger lead (D3 lists them first). ORIGINS, checked
     at Steve's request: neither is indigenous (Trollinger: South Tyrol; Lemberger: Lower Styria,
     now Slovenia), but 98% / ~92% of Germany's plantings are in Wurttemberg, so "regional".
     Sources: German Wine Institute variety pages (Trollinger 1,855 of 1,888 ha, 2023; Lemberger
     1,757 of 1,917 ha, 2023, "originated in ... northeastern Slovenia and made its way to
     Wurttemberg in the 19th century"), Wine Grapes / Wikipedia on both origins.
     CAVEAT on "Mostly": Trollinger + Lemberger are ~32% of Wurttemberg's vineyard area, about HALF
     of its red plantings (66%); "mostly" is a stretch. "Leans Heavily On" would be exact.

LEFT OUT, DELIBERATELY (true or plausible, not in D3, or single-sourced)
  - "Germany is the world's third-largest Pinot Noir grower, after France and the USA": real,
    but from one DWI-affiliated site only. A strong candidate if a second source is found.
  - Dornfelder bred in 1955 (a secondary source, not D3); Fruhburgunder; Regent.
  - Any claim about Ahr or Wurttemberg prices.

HEADLINE COLOR. A red-wine subject takes the per-deck override (style guide v3): sampled by
the guide's method (the 80 brightest SATURATED reds, not the blown-out pinks) from the ORIGINAL
cover, a red-wine splash: (246, 31, 13), contrast 3.86:1 against INK (floor 3.0). The cover was
later replaced at Steve's request by a photograph of two glasses of red wine; the color was KEPT:
re-running the method on the new cover gives (244, 98, 40), 4.99:1, a red-ORANGE, because that
photo's warm tones are candle glow and ornaments, not wine. The scarlet is truer to a red-wine
subject. The cover is a graded build (build_fffa_reds_cover.py): the glasses fill the width,
and their stems and the table fade into near-black so the type has a dark zone.

TEXT COLORS NOW FOLLOW THE GERMAN FLAG (Steve), superseding the scarlet headline above: gold
(255,206,0) for the cover subject, fact headlines and "Cheers"; red (221,0,0) for the cover kicker,
the 01-05 numerals and the closing "!". Black stays the GROUND (invisible as text on the dark
block, 1.33:1). Contrast: gold 10.60:1 on INK / 13.61:1 on the cover's black; red 3.07:1 on INK
(floor 3.0) / 3.94:1 on black; the red kicker against the photo behind it is 3.46:1 at the 98th
percentile (the faintest stem remnants, ~2% of that zone, dip to 2.1:1). Cobalt (grid mark,
rules, chart bars) is unchanged: it is not a font, and it is the series identity.

PHOTOGRAPHY, location-verified; FFFA fact pages carry credits only, never captions, so no
location is asserted on a page. Cover: Steve's photograph of two glasses of red wine at a
candlelit table, 612x408 px, no embedded credit or license data, so NO credit is printed (and
612x408 is typical of a stock site's preview image: license it before posting if it is a comp).
The earlier splash cover was Saman Taheri (Unsplash). 1: Rheinhessen
(Jugenheim) vineyard at sunrise, Sven Wilhelm. 2: red grapes, Waltershofen (Baden), Sven Finger.
3: dark grapes, Rheinland-Pfalz, Luca J. 4: autumn vines on steep slate terraces at
Mayschoss (Ahr), Superbass (Commons, CC BY-SA 3.0): Mayschoss is the village D3 names for the
oldest cooperative in the world. 5: terraced vineyards, Stuttgart, Heliao. Grape varieties
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

# New work is American English (Steve): turn the opt-in spelling check on for this deck.
os.environ.setdefault("AMERICAN_ENGLISH", "1")

import core
from fff_facts import fff_cover, fff_fact

OUT = "/home/claude/out_fffa_german_reds"
os.makedirs(OUT, exist_ok=True)
TOTAL = 6

# TEXT COLORS: THE GERMAN FLAG (Steve). Official black (0,0,0), red (221,0,0), gold (255,206,0).
# Black cannot be a font color here (1.33:1 on the fact pages' ink block) so it stays the GROUND;
# the type takes the other two. Measured contrast: gold 10.60:1 on INK / 13.61:1 on the cover's
# black; red 3.07:1 on INK (over the 3.0 large-type floor) / 3.94:1 on black.
#   gold  -> the cover subject, every fact headline, the "Cheers" word  (the headline override)
#   red   -> the cover kicker, the 01-05 numerals, the closing "!"     (accent_text_color / kicker_color)
# Previously the headlines were a scarlet SAMPLED from the original splash cover (246,31,13,
# 3.86:1) and the numerals the series cobalt (1.98:1 on INK): both are more legible now.
# NOT changed, because they are not fonts: the cobalt grid mark, the short cobalt rules and the
# chart bars (the series identity), and the paper/gray body, labels and footers (readability).
FLAG_RED = (221, 0, 0)
FLAG_GOLD = (255, 206, 0)

CRED_TAHERI = "Saman Taheri / Unsplash"   # the splash cover's credit: unused since the cover changed
CRED_WILHELM = "Sven Wilhelm / Unsplash"
CRED_FINGER = "Sven Finger / Unsplash"
CRED_LUCA = "Luca J / Unsplash"
CRED_SUPERBASS = "Superbass / Wikimedia Commons (CC BY-SA 3.0)"
CRED_HELIAO = "Heliao / Unsplash"

COVER = dict(
    # Steve's photograph of a vine row with clusters of dark grapes (Pexels, Sayed Masoumi: the
    # name is from the file name). It replaced the two-glasses cover, which replaced the splash.
    # Built by build_fffa_reds_cover.py: scaled to the page width, the clusters framed above the
    # type zone, the bottom faded into near-black so the type has a clean ground. 3024x4032
    # source, so it is crisp. Location NOT asserted: Pexels carries none.
    photo="fff_reds_cover_vineyard.jpg",
    subject="Red Wines of Germany",
    photo_credit="Sayed Masoumi / Pexels",
)

SHARE = "BLACK GRAPES AS A SHARE OF ALL PLANTINGS"

FACTS = [
    dict(
        number=1,
        photo="de_reds_rheinhessen_rows",
        photo_anchor=0.5,
        headline="Nearly a Third of German Vines Are Red",
        body="In 1980, nine in ten vines were white. By 2021, 32 percent were black, "
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
        headline="Germany's Pinot Noir Almost Tripled",
        body="Spätburgunder is its most planted red grape, at 11.5 percent of all "
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
        # Steve's heading, with ONE change: "Local" -> "Regional". He asked for the facts to be
        # checked that Trollinger and Lemberger are INDIGENOUS. They are not: Trollinger very
        # probably originated in South Tyrol/Trentino (its German name is a corruption of
        # "Tirolinger", "of Tyrol"); Lemberger (Blaufraenkisch) originated in Lower Styria, now
        # northeastern Slovenia, and reached Wurttemberg only in the 19th century (the German Wine
        # Institute says so itself). What IS true is how concentrated they are: 98% of Germany's
        # Trollinger (1,855 of 1,888 ha) and ~92% of its Lemberger (1,757 of 1,917 ha) are in
        # Wurttemberg, so "regional specialties" is accurate and "local"/"native" is not. The body
        # says so in one line: with a two-line heading, a two-line body pushed "Cheers!" to 57px
        # from the page edge, and the closing page's total is three lines.
        headline="Württemberg Focuses Mostly on Regional Red Varieties",
        # One line holds ~49 characters. First try ("...lead, though both came from elsewhere.", 63) wrapped
        # to a second line and put "Cheers!" 56px from the page edge. "Imports" is factual: Tyrol, Slovenia.
        body="Trollinger and Lemberger lead; both are imports.",
        photo_credit=CRED_HELIAO,
    ),
]


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    paths = []
    img = fff_cover(COVER, total=TOTAL, headline_color=FLAG_GOLD, kicker_color=FLAG_RED)
    p = f"{OUT}/01_cover.png"
    img.save(p)
    paths.append(p)
    print("  01  cover")

    for i, slot in enumerate(FACTS, start=2):
        img = fff_fact(slot, i, total=TOTAL, closing=(i == TOTAL),
                       diagram=slot.get("diagram"), headline_color=FLAG_GOLD,
                       accent_text_color=FLAG_RED)
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
