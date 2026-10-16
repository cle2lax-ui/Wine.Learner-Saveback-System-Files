"""WHAT AM I DRINKING? -- Roederer Estate L'Ermitage Brut 2019 (Anderson Valley). A two-page POST, not a Reel.

Steve (Oct 2026): "Let's do the What Am I Drinking as a Post, not a Reel. You already have a Roederer Estate sparkling
photo from our last deck. Use that." The photo is Steve's own shot of the L'ERMITAGE 2019 BRUT (its label reads
"2019 Brut L'Ermitage by Roederer Estate, Anderson Valley"), so this deck is about THAT wine -- the Arc 3 plan had said
Roederer Estate Brut NV, a different and humbler wine; the photo decides it. Format: formats/what_am_i_drinking.py
(wad_page1 / wad_page2), the redesigned Quick Sips two-pager locked with the Loosen deck. Page 1 is a "guess the wine"
page and NAMES NOTHING (the build fails if it does); page 2 is the answer.

SOURCE TRACE -- nothing below is from memory:
  Producer's technical sheet (roedererestate.com, 2019_RE_LErmitage-Brut.pdf), read in full:
    founded 1982; L'Ermitage "made only in exceptional years from all estate-grown grapes"; traditional method;
    debuted with the 1989 vintage; "juice from just the cuvee pressing; no premiere or deuxieme taille"; 2019 is "the
    first vintage of these wines to go through malolactic fermentation"; "about 4.9% of the wine was fermented in oak
    cask"; 52% Chardonnay, 48% Pinot Noir; reserve 3.9% Chardonnay 2016; disgorged February 2024; dosage 6 g/L; cases
    4,850; TA 6.5 g/L; pH 3.19; alcohol 12.9%; tasting note "quince paste and light pastry crust ... bright and textured
    midpalate ... mouthwatering finish ... pear skin and an even, creamy texture"; winemaker notes (via retailers):
    "hazelnut, brioche, and flint", "quince jelly", "bright acidity". "cool, fog-shrouded Anderson Valley".
  Wine Enthusiast (Tonya Pitts, May 2025): 100 points -- "the first 100-point score for a US sparkling wine from Wine
    Enthusiast" (K&L's wording) / "the first-ever perfect score for an American-made sparkling wine from a major wine
    publication" (the producer's press release, 5 June 2025). Notes: "creamy and light" mousse, stone fruit, quince,
    "blood orange zest", "layered salinity", "mouthwatering finish"; "full-bodied".
  Wine Spectator (Tim Fish, Feb 2025): 94 -- "Asian pear, baked apple, brioche, clove and nutmeg".
  Vinous (Antonio Galloni, 2025): 96 -- "the greatest wine ever made at Roederer Estate"; "beguiling" aromatics; the
    LOWEST DOSAGE EVER here, 6 g/L (K&L's staff note says the same).
  James Suckling (Dec 2025): 97 -- "delicate aromas of salt, herbs and pine forest", "fine bubbles", "medium- to
    full-bodied", "citrus oil and resinous herbs".
  Jeb Dunnuck (Virginie Boone, Feb 2025): "medium-bodied", "fresh natural acidity", "pastry crust". (Scores shown by
    retailers: 95 and 96 -- they disagree, so no Dunnuck number is used.)
  D3 Ch. 23.1 (Anderson Valley): a narrow valley a few miles from the Pacific; cold air and fog along the river
    (measured 4.2 miles from the AVA to open ocean: arc3/prepare_fg_classic_maps.py).

DELIBERATELY NOT USED
  Lees time: reviewers say "five years" (Wine Enthusiast, K&L) or "four" (a retailer), but a 2019 vintage disgorged in
    February 2024 is nearer four; the sources conflict, so no figure is given.
  Alcohol as a number: the producer's sheet says 12.9%, the importer and Wine.com 13.2%. Both are WSET "Medium".
  Any Dunnuck score (95 vs 96, above).

STRUCTURE DASHBOARD -- WSET Level 3 terms only; values on the Loosen deck's scale (Low .20, Medium .50, Medium(+) .72,
  High .90).
  Sweetness   Dry          MEASURED: dosage 6 g/L, producer. (WSET: Brut, up to 12 g/L, reads Dry.)
  Acidity     Medium (+)   INFERRED: TA 6.5 g/L, and the producer calls the 2019 vintage lower in acidity and "less
                           classic, taut"; reviewers say "bright", "vibrant", "mouthwatering", "fresh natural acidity".
  Alcohol     Medium       12.9% (producer) / 13.2% (importer): both Medium.
  Body        Medium (+)   reviewers span "medium-bodied" (Dunnuck), "medium- to full-bodied" (Suckling) and
                           "full-bodied" (Wine Enthusiast).
  Aroma       Medium (+)   INFERRED: "beguiling" (Vinous), "layered" (producer) but "delicate" (Suckling).
  Intensity

PHOTOGRAPHS
  Page 1: "Hillside Vineyards in Anderson Valley", Naotake Murayama (Wikimedia Commons, CC BY 2.0) -- the location is the
    file's own title. The page names no place; the vineyard is the wine's own valley.
  Page 2: Steve's own bottle shot (400 x 1,376 px, white background): a ~1.8x enlargement to fill the panel (the guide
    asks for 1,500 px; the Loosen shot was 3.5x). Its label reads 2019, matching the copy.
"""
import glob
import os

import core
from tokens import DEFAULT_PALETTE
from what_am_i_drinking import wad_page1, wad_page2

OUT = "/home/claude/out_wad_roederer"
os.makedirs(OUT, exist_ok=True)

PAL = dict(DEFAULT_PALETTE)
PAL.update(SIGNATURE=(45, 58, 74), ACCENT=(196, 158, 84), LEAD=(140, 95, 58))

PHOTOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "photos")

SLOT_1 = dict(
    # Nothing on page 1 may name the wine, producer, place or grapes. (The photograph is checked by eye: no signs.)
    hidden_terms=["Roederer", "Ermitage", "Anderson", "Mendocino", "California", "Philo", "Pinot", "Chardonnay",
                  "Champagne", "Louis"],
    photo="us_mendo_av_vineyard_murayama",
    photo_anchor=0.0,
    # Swept (guide: never guess): 0.46 was the Loosen photo's value. On this photo's blue sky 0.30 is enough -- title 6.6:1,
    # gold note 4.62:1 against the BRIGHTEST background pixels (need 4.5), and the hero keeps 86% of its brightness
    # (81% at 0.46). Below 0.25 the note falls under 4.5:1.
    scrim_strength=0.30,
    lockup_y=80,
    title_lines=["What am I Drinking?"],
    title_size=120,
    photo_h=1000,
    lockup_note="(Make a guess, then find out on the next page)",
    lockup_note_size=60,
    photo_credit="Naotake Murayama / Wikimedia Commons (CC BY 2.0)",
    paragraph_lead="Only in the best years",
    paragraph="is this wine made, from one estate's own grapes, grown in a fog-cooled valley a few miles from the "
              "ocean. Only the first, cuvée pressing goes in, and about 5% is fermented in oak.",
    structure=[
        ("Sweetness", 0.12, "Dry"),
        ("Acidity", 0.72, "Medium (+)"),
        ("Alcohol", 0.50, "Medium"),
        ("Body", 0.72, "Medium (+)"),
        ("Aroma Intensity", 0.72, "Medium (+)"),
    ],
    notes=[
        ("Aromas", "Quince paste, hazelnut, brioche, pastry crust."),
        ("Palate", "Asian pear, baked apple, clove; a creamy mousse."),
        ("Finish", "Mouthwatering, pear skin, creamy."),
    ],
    notes_source="Critics and the producer",
)

SLOT_2 = dict(
    bottle=os.path.join(PHOTOS, "wad_roederer_lermitage_bottle.jpg"),
    bottle_top=100,
    title_top=470,
    # The producer's name is the page's headline and shrinks to fit one line (174px); the format wants it 30px above
    # the lockup. "Dr. Loosen" (short) stayed at 200px, "Roederer Estate" cannot: the lockup goes 160 -> 130px
    # (page 1's is 120px, so the pair now match more closely).
    lockup_size=130,
    producer="Roederer Estate",
    region_year="Anderson Valley \u00b7 2019",
    wine_lines=["L'Ermitage", "Brut"],
    rule=False,
    lead="Dry, creamy, and rare.",
    body="The 2019: 52% Chardonnay and 48% Pinot Noir, in just 4,850 cases. Dosage is just 6 g/L, "
         "the lowest the wine has had, and it is the first L'Ermitage to go through malolactic fermentation. Wine "
         "Enthusiast gave this 2019 a 100, the first it has given an American sparkling wine.",
    body_anchor="bottom",
)


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)
    paths = []
    for i, (fn, slot) in enumerate([(wad_page1, SLOT_1), (wad_page2, SLOT_2)], start=1):
        img = fn(slot, i, 2, PAL)
        p = f"{OUT}/{i:02d}_page{i}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  page{i}")
    pdf = f"{OUT}/WAD_Roederer_Lermitage_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
