"""FFFA -- Five Fascinating Facts About Mendocino. Arc 3, the arc's last text post.

Fixed 6-page format per FFFA_STYLE_GUIDE.md: fff_cover() once, then fff_fact() five times, the fifth with closing=True
folding "Cheers!" into the same page. Never 7 pages.

THE BRIEF. The Field Guide (13 slides) already spent the obvious Mendocino facts: 12 AVAs, 7,000 ha, the rain, 4 miles to
the Pacific, 1983, Cole Ranch, the organic share, the six AVAs under the Mendocino AVA. So these five are NEW, and each was
checked against WSET first (D1, D3, D4), then the primary regulatory text (TTB), then outside sources. The order runs from
the place to the land, the cold, the height and the heat, and ends on the Winkler classes that open the Climate arc.

FACTS
  1  A Champagne house founded Roederer Estate in Anderson Valley.
       D4 s17.1: "Many wineries from outside the region buy Anderson Valley grapes for their sparkling wines. This region is
       home to Roederer Estate, founded by Roederer Champagne house." 1982: the producer's own technical sheet (the L'Ermitage
       2019 sheet, read in full for the What Am I Drinking? post). D4 also names Roederer Estate as its example of a specialist
       sparkling company founded by a Champagne house (s17.3).
  2  Even Anderson Valley is only about 4 percent vines.
       D3: "Just under 1,000 ha are planted"; Mendocino County: "Of around one million ha, 7,000 ha are under vine" (0.7%).
       The AVA's area is MEASURED from the UC Davis AVA Project polygon (CC0): 89.9 sq mi = about 57,500 acres = about 23,300 ha.
       Under 1,000 / 23,300 = 4.3% at most, so "about 4 percent" (and "under 1 percent" for the county). CROSS-CHECK of the polygon
       method: the same file gives 83,500 acres for the Mendocino Ridge's land above 1,200 ft, and the TTB's own figure is 87,466
       (within 5%), so the area is sound to about 5%: 4.1-4.5%.
  3  The frost risk sits on the valley floor, and the vines sit on the slopes.
       D3: "The vast majority of the vineyards are planted on the sloped sides of the valley. Cold nights mean frost can be an issue
       in the spring particularly in low-lying areas."  D1 s8.1 (frost): "As cold air is denser than warm air, this freezing cold
       air will collect in valley bottoms"; "choose hillside sites where cold air can drain away." The copy states the two D3 facts and
       the D1 principle and does NOT say growers chose slopes FOR frost: neither source says so. Supporting primary text (TTB
       T.D. ATF-392, quoting Matt Kramer): the sun-loving varieties "could [not] have prospered in the cool, frost-prone Anderson
       Valley floor"; on the ridges "the ridge sites rarely see the spring frosts".
  4  Mendocino Ridge sits above the fog.
       TTB T.D. ATF-392 (62 FR 55512, 27 Oct 1997): the AVA "encompasses only the areas at or above 1200 feet in elevation";
       "ATF is not aware of any grapes being grown at the lower elevations in the area below the 1200 foot coastal fog line";
       "the elevation line being at approximately the fog line means that while the valleys may be full of coastal fog, the
       vineyards are fully exposed to the sun". CSW (2018): "unique in that it is noncontiguous" and "above the fog line". "Only
       non-contiguous AVA in the U.S.": the CSW says unique; Decanter, Wikipedia and the regional association say only.
       NUMBERS SETTLED, because the sources look like they conflict: the CSW's "250,000 acres" is the OUTER boundary (the TTB's
       262,400 acres); the AVA itself is the 87,466 acres above 1,200 ft, about 2% of which is plantable; the TTB counted about
       75 acres planted in 1997, the CSW says just over 250 in 2018. NOT PRINTED: any island count. The TTB names 24 ridges, the
       UC Davis polygons split the AVA into 73 pieces, and the two are different counts; neither is "the number of islands".
  5  In six miles, the heat class changes.
       TTB T.D. ATF-139 (48 FR 37370, 18 Aug 1983), the Anderson Valley rule: Philo is Winkler Region I; "the area around
       Boonville is warmer and consequently is classified as Region II"; Boonville is "six miles up Anderson Valley"; "In
       comparison the Ukiah area, which lies approximately 15 miles to the northeast of Anderson Valley, is warmer and
       consequently is classified as a Region II and Region III area." D1 s3.4 gives the five Winkler bands (Zone I cool, Zone V
       very hot) and the growing degree day method. The chart places I, II and II-III on that five-step scale; it is ordinal, the
       bar lengths are class positions, not degree days (the title says so).

LEFT OUT, DELIBERATELY
  - McDowell Valley "first single-vineyard AVA": TTB's table dates it 12/4/1981 while two aggregator sites say 4 Jan 1982, and the
    "first" rests on retail pages. Not verified, so not used.
  - Mendocino Ridge's rename. The TTB proposed "Mendocino Coast Ridge" (NPRM 5 Jan 2024, comments closed 5 Mar 2024) and the
    federal regulatory agenda targets a FINAL RULE for 10/2026, i.e. this month. As of today no final rule is published and
    "Mendocino Ridge" is the legal name; labels would have a two-year transition. Slide 4 names the AVA "Mendocino Ridge": check the
    Federal Register before posting.
  - The Ridge's diurnal swing (20 F against 40-50 F in Anderson Valley): on Wikipedia only; it is not in the 1997 rule. Unverified.
  - Any claim about cannabis, a county-wide "first organic winery", Boontling (Steve removed it earlier), and the Ridge island count.

PHOTOS (all in photos/, credited from data/NR_PHOTO_MANIFEST.json; places only where the Commons file title states them)
  cover  the lake and vine rows (No-till-vineyard, CC0): the title is not asserted. A graded copy, see COVER below.
  1      the Roederer flute (Missvain, CC0): the glass carries the estate's monogram; the file's own title places it in Philo.
  2      "View from Esterlina Tasting Room, Anderson Valley" (Ethan Prater, CC BY 2.0).
  3      "Vineyard in Anderson Valley" (Ethan Prater, CC BY 2.0).
  4      redwoods in fog (Mick Haupt, Pexels): the Pexels file carries no place, so none is claimed. The TTB rule describes the
         ridge-tops as "timber covered" and the Ridge as "dominated by timber type soils with redwood, Douglas fir"; the fog
         is the point. No Commons photo of ridgetops above fog was found.
  5      the Husch vineyard at Philo (No-till-vineyard, CC0), the vineyard the TTB rule itself names for the Region I portion
         ("the portion of the valley shared by Edmeades and Husch Vineyards, near Philo").
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

# The series cobalt is 1.98:1 on the fact pages' ink block (every FFFA deck: the 01-05 numerals and the closing "!" at
# 150-230 px, under the 3:1 floor for large text). The format's opt-in accent_text_color override (v4) takes a lighter
# cobalt of the SAME hue: 3.3:1 here. The grid mark, the short rules and the chart bars stay the series cobalt (identity).
NUMERAL_BLUE = legible(FFFA_ACCENT, INK, 3.3)

OUT = "/home/claude/out_fffa_mendocino"
os.makedirs(OUT, exist_ok=True)
TOTAL = 6

CRED_NTV = "No-till-vineyard / Wikimedia Commons (CC0)"
CRED_MISSVAIN = "Missvain / Wikimedia Commons (CC0)"
CRED_PRATER = "Ethan Prater / Wikimedia Commons (CC BY 2.0)"
CRED_HAUPT = "Mick Haupt / Pexels"

COVER = dict(
    # A graded copy (arc3/build_fffa_mendocino_cover.py; the original is untouched): the lake under the type is darkened by a
    # smooth ramp. Ungraded, the white kicker was 2.90:1 and the yellow subject 2.31:1 against the brightest water pixels;
    # graded (ramp from 50% down, floor 0.58): 3.66:1 and 4.45:1. Same photo, same framing.
    photo="fffa_mendocino_cover",
    photo_anchor=0.5,
    subject="Mendocino",
    photo_credit=CRED_NTV,
)

FACTS = [
    dict(
        number=1,
        photo="us_mendo_roederer_flute_cc0",
        photo_anchor=0.55,
        headline="A Champagne House Founded Roederer Estate in Anderson Valley",
        body="Roederer Estate dates to 1982. Many wineries from outside the region also buy Anderson Valley "
             "grapes for sparkling wine.",
        photo_credit=CRED_MISSVAIN,
    ),
    dict(
        number=2,
        photo="us_mendo_av_esterlina_view_prater",
        photo_anchor=0.5,
        headline="Even Anderson Valley Is Only About 4 Percent Vines",
        body="Just under 1,000 of its roughly 23,000 hectares are planted. Across Mendocino County, "
             "vines cover under 1 percent.",
        photo_credit=CRED_PRATER,
    ),
    dict(
        number=3,
        photo="us_mendo_av_slope_prater",
        photo_anchor=0.5,
        headline="Anderson Valley's Frost Risk Sits on the Valley Floor",
        body="Dense cold air settles in low ground. Most of the valley's vineyards sit on its slopes, "
             "where it can drain away.",
        photo_credit=CRED_PRATER,
    ),
    dict(
        number=4,
        photo="us_mendo_fog_redwoods_pexels",
        photo_anchor=0.5,
        headline="Mendocino Ridge Sits Above the Fog",
        body="It includes only land at 1,200 feet or higher, so it is America's only non-contiguous AVA, "
             "a scatter of ridgetops.",
        photo_credit=CRED_HAUPT,
    ),
    dict(
        number=5,
        photo="us_mendo_husch_philo_cc0",
        photo_anchor=0.5,
        # One-line headline and body, and the distances in the chart's labels: the first build's two-line headline plus
        # two-line body left "Cheers!" 16px from the page edge (the guide: 217px good, 57px crowded; QA does not catch it).
        headline="In Six Miles, the Heat Class Changes",
        body="Philo is among California's coolest grape areas.",
        bars_title="WINKLER HEAT CLASS ON A FIVE-STEP SCALE (V = HOTTEST)",
        bars=[("Philo", 20, "Region I", False),
              ("Boonville, 6 mi on", 40, "Region II", False),
              ("Ukiah, 15 mi NE", 50, "Regions II\u2013III", True)],
        photo_credit=CRED_NTV,
        diagram="bars",
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
                       accent_text_color=NUMERAL_BLUE,
                       credit_chip=True)     # the closing page prints its credit top-right over the photo
        p = f"{OUT}/{i:02d}_fact{slot['number']}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  fact {slot['number']}")
    pdf = f"{OUT}/FFFA_Mendocino_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
