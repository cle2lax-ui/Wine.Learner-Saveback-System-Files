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
  Page 2: Steve's second bottle shot (IMG_0753.jpeg), 235x706 px (the bottle is 681px
    tall), near-white background. It replaced the first (IMG_2568, 344x1200, whose
    label read 9.0% vol against the copy's 8%). The new label reads 7.5% vol. It is
    SMALLER than the one it replaced, so filling the panel is a 3.5x enlargement:
    the large label type (Dr. Loosen, Erdener Treppchen, Riesling Auslese, Mosel)
    stays legible, the fine print is not recoverable, and the whole bottle is soft.
    Denoise-then-upscale was chosen over plain Lanczos (marginally smoother, less
    JPEG blocking). The label's vintage is not visible. A larger shot would help.

ROUND 3 (the four-designer review, applied): see arc2/REVIEW_WAD_loosen_treppchen.md.
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
    # The lockup is in the UPPER-LEFT corner (Steve), the title on ONE line at a smaller
    # size, with "(find out on the next page!)" in italics beneath it. That changed the
    # best crop: with the lockup in the corner, photo_anchor 1.0 (the review's pick for a
    # centred lockup) pushes the vineyard peninsula up under it. At 0.0 the lockup sits in
    # clear corner space over the sunset sky and hills, the whole vineyard bend stays
    # visible below it, and the photo is the brightest of the three crops.
    # The note is now part of the lockup (directly under the title, the stack centred on
    # the disc), so the scrim band is one disc tall instead of disc-plus-note. Re-swept for
    # that geometry: 0.52 was more than needed; 0.46 gives title 4.0:1, gold note 4.9:1 at
    # the 90th percentile, photo luminance 0.185 (0.160 before the lockup change).
    photo_anchor=0.0,
    scrim_strength=0.46,
    lockup_y=80,
    title_lines=["What am I Drinking?"],
    title_size=120,
    photo_h=1000,
    # Steve's wording; parentheses and italics kept from the earlier note, and no "!" since
    # his new text has none. The line is ~44 characters, so at 64px it ran 131px past the
    # title's right edge and made the lockup ragged; at the 60px type floor it ends only 48px
    # past (and 4.5:1 or better across its whole length, measured in its own ink box).
    lockup_note="(Make a guess, then find out on the next page)",
    lockup_note_size=60,
    photo_credit="tom analogicus / Pexels",
    paragraph_lead="So steep",
    # First draft (~60 words) overflowed the page by ~200px with the dashboard
    # and notes below it: trimmed, and the photo shortened 1080 -> 1000.
    # Review fixes. "this vineyard" -> "the vineyard": "this" pointed at the hero photo,
    # which is Bremm, not the Treppchen. The last sentence no longer says the estate "has
    # been built on" ungrafted vines: the importer says the 1988 owner saw ungrafted vines
    # averaging 60 years old in SOME of the top vineyards as his raw material.
    paragraph="that stone steps were built into the vineyard centuries ago for "
              "the workers. Its iron-rich red slate gives the wines a spicy, "
              "almost peppery minerality. One family has owned the estate for "
              "over 200 years; some of its best vineyards carry old, "
              "ungrafted vines.",
    structure=[
        ("Sweetness", 0.78, "Sweet"),
        ("Acidity", 0.90, "High"),
        ("Alcohol", 0.20, "Low"),
        ("Body", 0.72, "Medium (+)"),
        ("Aroma Intensity", 0.90, "Pronounced"),
    ],
    notes=[
        # "zest" dropped (the producer says white peach and citrus); "yet" dropped so
        # the Finish fits one line instead of leaving "focused." alone on the next.
        ("Aromas", "Nectarine, melon, apricot, white peach, citrus."),
        ("Palate", "Spice, firm slate, a saline mineral edge."),
        ("Finish", "Long, unctuous, focused."),
    ],
    notes_source="Wine Enthusiast, the producer",
)

SLOT_2 = dict(
    # The 235x706 shot Steve supplied, replacing the 344x1200 one whose label read 9.0%.
    # The bottle's top sits on the lockup's top line (y=100) and its base on the content
    # limit (y=2500), so the text column and the bottle share a top and a bottom axis.
    bottle=os.path.join(PHOTOS, "wad_loosen_treppchen_bottle2.jpg"),
    bottle_top=100,
    title_top=470,
    producer="Dr. Loosen",
    region_year="Mosel · 2020",
    wine_lines=["Erdener Treppchen", "Riesling Auslese"],
    # Review fixes. "never heavy" -> "held in balance": the absolute sat against Wine
    # Enthusiast's "unctuous" and page 1's own Body row. "Auslese is selected harvest" and
    # "the producer sees great potential for ageing" cut (redundant / soft). The alcohol is
    # "7.5-8%", not "8%": the supplied label reads 7.5%, Wine.com lists the 2020 at 8%, and
    # Wine-Searcher gives 7.5-8%; the label's vintage is not visible, so a single figure
    # would be a guess.
    lead="Sweet, held in balance.",
    body="Very ripe, partly botrytised bunches, kept fresh by crisp acidity at "
         "just 7.5\u20138% alcohol. The Treppchen's red slate adds spice and a "
         "saline edge, and the VDP ranks the site Grosse Lage. Wine Enthusiast "
         "gave this 2020 a 93.",
    rule=False,             # decorative: size and colour already separate name from body
    body_anchor="bottom",   # the last line sits on the bottle's base
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
