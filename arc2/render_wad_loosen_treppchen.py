"""WHAT AM I DRINKING? -- Dr. Loosen Erdener Treppchen Riesling Auslese 2020.

The first deck in the redesigned Quick Sips format (formats/
what_am_i_drinking.py). Brief (Steve): two pages; page 1 = logo with a
question mark, large title-case "What am I Drinking?", a region photo at the
top, a paragraph on the region/producer and why it matters, the structure
dashboard and tasting notes sourced from online reviews, a Read More bug;
page 2 = bottle shot on the right 30%, producer / region / year / wine name
in the title font, a few more words on the wine.

Round 2 (Steve): the logo lockup is horizontal (the title right beside the
glass-and-question-mark disc); page 1 is a "guess the wine" layout, so it
names nothing (the build FAILS if page 1 contains the wine, producer, vineyard
or region -- see hidden_terms); the hero is a more colourful Mosel photo; and
page 2 repeats the lockup with "I'm Drinking", the answer to page 1's question.

SOURCE TRACE -- nothing below is from memory:
  Producer's own site (drloosen.de/en/collections/erdener-treppchen):
    the site lies directly beside the Pralat; "so steep that stone steps
    were built centuries ago to allow workers better access"; iron-rich red
    slate; "spicy, almost peppery minerality"; Auslese: "concentrated
    sweetness with vibrant freshness and pronounced minerality", white
    peach and citrus, herbal and slate spice, "fine, saline minerality",
    "long, clean finish", "great potential for enjoyment and aging".
    Classification VDP.GROSSE LAGE (the producer's Treppchen product pages).
  Importer text (Empire Wine; Chambers Wines sheet): in the same family for
    more than 200 years; Ernst Loosen took over in 1988; ungrafted old vines;
    Auslese = very ripe clusters about 50% botrytis-affected, "balanced by
    Riesling's naturally crisp acidity". NOTE the Chambers sheet's analysis
    (8.0% / 76.5 g/L / 8.6 g/L acid) is for the 2016, and is NOT used here.
  Wine Enthusiast, 93 points, the 2020 vintage (via wine.com / MrDWine):
    "super lush, with nectarine, melon, apricot and spice aromas and flavors
    that are flanked by firm slate and savory mineral notes ... long and
    unctuous, but it keeps focused and balanced".
  Wine.com listing for the 2020: ABV 8%.
  D3 Ch. 11: "suss ('sweet')" = more than 45 g/L residual sugar.

STRUCTURE DASHBOARD -- WSET Level 3 SAT terms only, per the Quick Sips guide.
  Sweetness  Sweet        INFERRED, not measured: no published residual sugar
                          for the 2020 was found. The estate's Auslese has
                          run 76.5-81 g/L wherever analysis is published
                          (2016, 2019 [81], 2023 [77]); the 2020 Kabinett was
                          ~43 g/L, so the 2020 Auslese is above it, and D3
                          calls >45 g/L sweet.
  Acidity    High         producer: "vibrant", "captivating, vibrant acidity";
                          importer: "naturally crisp acidity".
  Alcohol    Low          8% (Wine.com listing for the 2020).
  Body       Medium (+)   producer/importer: "dense, intensely flavored and
                          rich"; Wine Enthusiast: "unctuous". One retailer
                          tag says medium-bodied; weighed against those.
  Aroma      Pronounced   Wine Enthusiast "super lush"; producer "seductive
  Intensity               aromas".

PHOTOGRAPHS
  Page 1: the Mosel loop at Bremm (de_bremm_mosel_loop.jpg), tom analogicus /
    Pexels -- golden-green vineyard bend, blue river, no signs or text in
    frame. Chosen over the first hero ("DE-RP Erdener Treppchen.jpg", whose vines
    spell the vineyard's name -- fatal for a guess-the-wine page) for colour
    and for being unmistakably Mosel. HONEST NOTE: Bremm is on the Lower Mosel;
    Erden is on the Middle Mosel. The photo is uncaptioned and shows "the
    Mosel", not Erden. Pexels carries no location data; the place is from the
    photographer's own title ("aerial view of Moselle river bend near Bremm").
  Page 2: Steve's bottle shot (IMG_2568). 344x1200 px, pure white
    background. Enlarged ~2.2x to fill the panel, so it is SOFT. The label
    in the shot reads 9.0% vol, which does NOT match the 8% listed for the
    2020 -- the shot is very probably another vintage's bottle. A larger,
    2020-label shot would fix both.
"""
import glob
import os

import core
from tokens import DEFAULT_PALETTE
from what_am_i_drinking import wad_page1, wad_page2

OUT = "/home/claude/out_wad_loosen"
os.makedirs(OUT, exist_ok=True)

PAL = dict(DEFAULT_PALETTE)
PAL.update(SIGNATURE=(45, 58, 74), ACCENT=(196, 158, 84), LEAD=(140, 95, 58))

PHOTOS = os.path.join(os.path.dirname(__file__), "..", "photos")

SLOT_1 = dict(
    # Page 1 is a "guess the wine" layout (Steve): nothing on it may name the
    # wine, producer, vineyard or region, so the guard below fails the build if
    # it does. The first hero (the Treppchen photo) was dropped partly for this:
    # the vineyard's name is spelled out in its vines.
    hidden_terms=["Loosen", "Treppchen", "Erden", "Mosel", "Riesling", "Auslese"],
    photo="de_bremm_mosel_loop",
    photo_anchor=0.5,
    photo_h=1000,
    photo_credit="tom analogicus / Pexels",
    paragraph_lead="So steep",
    # First draft (~60 words) overflowed the page by ~200px with the dashboard
    # and notes below it: trimmed, and the photo shortened 1080 -> 1000.
    paragraph="that stone steps were built into this vineyard centuries ago for "
              "the workers. Its iron-rich red slate gives the wines a spicy, "
              "almost peppery minerality. One family has held the estate for "
              "over 200 years, and under one winemaker since 1988 it has been "
              "built on old, ungrafted vines.",
    structure=[
        ("Sweetness", 0.78, "Sweet"),
        ("Acidity", 0.90, "High"),
        ("Alcohol", 0.20, "Low"),
        ("Body", 0.72, "Medium (+)"),
        ("Aroma Intensity", 0.90, "Pronounced"),
    ],
    notes=[
        ("Aromas", "Nectarine, melon, apricot, white peach, citrus zest."),
        ("Palate", "Spice, firm slate, a saline mineral edge."),
        ("Finish", "Long, unctuous yet focused."),
    ],
    notes_source="Wine Enthusiast, the producer",
)

SLOT_2 = dict(
    bottle=os.path.join(PHOTOS, "wad_loosen_treppchen_bottle.png"),
    bottle_h=2500,
    title_top=470,   # centres the text block against the full-height bottle
    producer="Dr. Loosen",
    region_year="Mosel · 2020",
    wine_lines=["Erdener Treppchen", "Riesling Auslese"],
    lead="Sweet, never heavy.",
    body="Auslese is selected harvest: very ripe, partly botrytised bunches, made "
         "sweet but held in balance by Riesling's crisp acidity at just 8% "
         "alcohol. The Treppchen's red slate adds spice and a saline edge, and "
         "the VDP ranks the site Grosse Lage. Wine Enthusiast gave this 2020 a "
         "93; the producer sees great potential for ageing.",
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
    pdf = f"{OUT}/WAD_Loosen_Treppchen_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
