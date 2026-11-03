"""FFFA -- Five Fascinating Facts About Climate Change. Arc 4 (the Climate arc), entry 3. Fixed 6-page format (FFFA_STYLE_GUIDE.md): fff_cover() once,
then fff_fact() five times, the fifth with closing=True folding "Cheers!" into the same page. Never 7 pages.

THE BRIEF. The Field Guide (15 slides) spent climate's FACTORS and, in two closing slides, a short note on adaptation (slide 15: "rising temperatures speed the vine
cycle and push sugar ahead of aroma and tannin"). This post is the deeper look at what a warming climate does, all from D1 section 3.6 (pp. 44-45), each fact
checked against the book's own words first. Order: the vine, the grape, the aroma, the sites, the upside.

FACTS (D1 "3.6. Climate Change"; the quoted words are the book's)
  1  Warming speeds up the vine's whole year.
       D1 p. 44: "In warmer temperatures, the vine cycle is faster. Budburst occurs earlier in the spring and each stage of the vine cycle becomes quicker."
  2  Sugar and acid outrun aroma and tannin.
       D1 p. 44: "The increased temperatures speed up the rate of sugar accumulation and reduction of acidity, but do not quicken the ripening of most aroma and
       tannin compounds. ... grapes may be picked with higher levels of sugar, causing higher alcohol levels in wines and lower levels of acidity." The copy keeps
       D1's "may". The same paragraph adds "The more rapid fall in acidity can give wines with higher pH levels, and this can be problematic in winemaking" (the plan's
       separate fact 3): it is NOT printed, to hold the 15-20 word body; it is the first fact held for a later post.
  3  Black pepper may fade from Northern Rhone Syrah.
       D1 p. 45: "black pepper is often a characteristic of Syrah grown in moderate climates, such as the Northern Rhone. With increasing temperatures in this region,
       it is likely that this hallmark aroma may no longer develop." The plan had held this for the Syrah What Am I Drinking? post; that slot became the Tondonia
       Rioja, so the pepper is free, and it replaces the plan's pH fact. D1 also says "The effects on aroma compounds is complex": the copy says "may".
  4  Some vineyard sites may be abandoned in 50 to 100 years.
       D1 p. 45: "A number of wine regions are starting to experience very significant problems with excessive temperatures and/or drought (e.g. parts of California and
       South Africa), and it is thought that at least some vineyard sites in many of these regions will be abandoned in the next 50-100 years." The copy keeps "thought".
       It does NOT say California or South Africa WILL lose sites: D1 says "many of these regions", with those two as examples.
  5  Colder regions may gain from warming.
       D1 p. 45: "there is the potential for production to increase or improve in quality in regions and countries that have previously been too cold to ripen grapes
       (however, extreme and erratic weather and altered rainfall patterns still pose a risk in these areas)."

LEFT OUT, DELIBERATELY
  - Higher pH (above). Drier conditions and photosynthesis stopping in water-stressed vines (D1 p. 45): the abandonment fact carries the drought. Rain and humidity just before
    harvest raising disease pressure (p. 45). D1 p. 46 on adaptation and mitigation: spent by The Field Guide's slide 15.
  - Any temperature or date figure. D1 gives none for climate change except "50-100 years", so the deck carries no numbers beyond that and no chart: a diagram
    would have to invent magnitudes. (The guide: "a diagram is for comparative, scalar or relational claims, not a default".) Recorded for the Social Pass: gate 2 (save
    asset) rests on the facts and the caption; the format has no chart slide here.

PHOTOS (all in photos/, each from Wikimedia Commons; no place is claimed in any copy)
  cover  "Franschhoek vineyard, Western Cape, South Africa" (South African Tourism, CC BY 2.0): a hot sky over vine rows; South Africa is one of D1's two examples.
         A graded COPY (build_fffa_climate_cover.py, floor 0.66, swept): ungraded, the page number was 3.26:1 and the credit 3.83:1 (needs 4.5); graded, 6.4 and 7.2.
  1      "20140407Wein Hockenheim3" (AnRo0002, CC0): buds swelling on a cane in early spring.
  2      "A bunch of grapes on a vine" (Ian Schneider, CC0, from Unsplash): ripe dark grapes.
  3      "Nahrungsmittel 2012-07-08-9528" (Slick, CC0): black peppercorns.
  4      "Jeunes vignes et vue de Mana a Stellenbosch" (Mister-E, CC BY 2.0): young vines in dry, sandy soil.
  5      "Rebstocke nach dem Winterschnitt" (Ilka Franz, CC0): pruned vines in winter dormancy.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
sys.path.insert(0, os.path.join(HERE, "..", "formats"))
os.environ.setdefault("AMERICAN_ENGLISH", "1")

import core                                    # noqa: E402
from core import legible                       # noqa: E402
from fff_facts import fff_cover, fff_fact      # noqa: E402
from tokens import FFFA_ACCENT, INK            # noqa: E402

# The series cobalt is 1.98:1 on the fact pages' ink block; the format's opt-in override takes a lighter cobalt of the SAME hue (3.3:1).
NUMERAL_BLUE = legible(FFFA_ACCENT, INK, 3.3)

OUT = "/home/claude/out_fffa_climate"
os.makedirs(OUT, exist_ok=True)
TOTAL = 6

CRED_SAT = "South African Tourism / Wikimedia Commons (CC BY 2.0)"
CRED_ANRO = "AnRo0002 / Wikimedia Commons (CC0)"
CRED_SCHNEIDER = "Ian Schneider / Unsplash via Wikimedia Commons (CC0)"
CRED_SLICK = "Slick / Wikimedia Commons (CC0)"
CRED_MISTERE = "Mister-E / Wikimedia Commons (CC BY 2.0)"
CRED_FRANZ = "Ilka Franz / Wikimedia Commons (CC0)"

COVER = dict(
    photo=os.environ.get("FFFA_CLIMATE_COVER", "fffa_climate_cover"),      # the graded copy (build_fffa_climate_cover.py)
    photo_anchor=0.5,
    subject="Climate Change",
    photo_credit=CRED_SAT,
)

FACTS = [
    dict(
        number=1,
        photo="fffa_climate_budburst",
        photo_anchor=0.5,
        headline="Warming Speeds Up the Vine's Whole Year",
        body="Budburst comes earlier in spring, and every stage of the vine cycle runs quicker.",
        photo_credit=CRED_ANRO,
    ),
    dict(
        number=2,
        photo="fffa_climate_grapes",
        photo_anchor=0.5,
        headline="Sugar and Acid Outrun Aroma and Tannin",
        body="Heat speeds sugar gain and acid loss, but not most aroma or tannin ripening, so grapes may be picked riper.",
        photo_credit=CRED_SCHNEIDER,
    ),
    dict(
        number=3,
        photo="fffa_climate_pepper",
        photo_anchor=0.5,
        headline="Black Pepper May Fade From Northern Rh\u00f4ne Syrah",
        body="Pepper often marks Syrah from moderate climates. In the Northern Rh\u00f4ne, rising temperatures may stop that aroma developing.",
        photo_credit=CRED_SLICK,
    ),
    dict(
        number=4,
        photo="fffa_climate_young_vines",
        photo_anchor=0.5,
        headline="Some Vineyard Sites May Be Abandoned in 50 to 100 Years",
        body="Some sites in regions with severe heat and drought, such as parts of California and South Africa, are thought likely to go.",
        photo_credit=CRED_MISTERE,
    ),
    dict(
        number=5,
        photo="fffa_climate_winter_vines",
        photo_anchor=0.5,
        # One line of headline and one of body: the first build's two-and-two left "Cheers!" 56 px from the page edge (the guide: 217 good, 57 crowded).
        headline="Once-Too-Cold Regions May Gain",
        body="Erratic weather and altered rainfall still pose a risk.",
        photo_credit=CRED_FRANZ,
    ),
]


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)
    paths = []
    img = fff_cover(COVER, total=TOTAL)
    p = f"{OUT}/01_cover.png"
    img.save(p)
    paths.append(p)
    print("  01  cover")
    for i, slot in enumerate(FACTS, start=2):
        img = fff_fact(slot, i, total=TOTAL, closing=(i == TOTAL), diagram=slot.get("diagram"),
                       accent_text_color=NUMERAL_BLUE, credit_chip=True)
        p = f"{OUT}/{i:02d}_fact{slot['number']}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  fact {slot['number']}")
    pdf = f"{OUT}/FFFA_Climate_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
