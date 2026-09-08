"""SPLIT DECISION — Whole bunch or destemmed. Arc 1, Sat 12 September.

Two slides per SPLIT_DECISION_STYLE_GUIDE.md. Slide 1 poses the
question with two poles and no hint; slide 2 gives the mechanism,
takes a side briefly, and re-opens it.

WHY THIS QUESTION, AND NOT THE ONE I SAID IT WOULD BE.

I had this slot down as resolving the Field Guide's slide 9 —
Côte-Rôtie or Hermitage, aromatics or structure. Run against the
guide's three-part question test, that fails on two counts. "Which is
the better wine" is preference, which the guide rules out as
generating shallow comments; and rephrasing it as "which ages longer"
fails the other way, because D3 states Hermitage's longevity plainly,
which makes it a Quick Sips fact rather than an argument.

Whole bunch or destemmed passes all three. D3 sets out both sides
without settling it, it is reasonable from mechanism rather than from
memory of a bottle, and it is the live decision in the northern Rhône
cellar. It also lands better inside the week than the original would
have: it is the decision node on the Field Guide's slide 11, and it is
precisely what separates Monday's two bottles — Clape whole-bunch and
traditional, Vincent Paris destemmed and fresher-framed. A reader who
followed the week has already met both answers without being told
they were answers.

SOURCES. D3 Ch. 7 on northern Rhône cru production: whole bunches, or
partially destemmed, "to promote more intense aromatics"; or
destemmed, chilled and cold soaked 1-3 days to extract colour. D3
Ch. 3 sets out the general case: proponents say whole bunches aid
aeration of the must and can add perfume, freshness and fine tannins;
unripe stems extract green astringent tannins, and the resulting lower
acidity would not be welcome in warm vintages. The Burgundy history —
historical norm, Henri Jayer's influence toward destemming in the
1980s, whole bunch re-emerging recently — is D3's, and is what makes
the closing line a real re-opening rather than a hedge.

Palette inherits the Field Guide's Arc 1 signature so the pair read as
siblings in the grid. The two poles differ by MARK colour only —
neither may look like the favoured side before it is read.
"""
import os

import core
import modules

OUT = "/home/claude/out_sd_wholebunch"
os.makedirs(OUT, exist_ok=True)

# Same palette as the Field Guide — Arc 1 signature.
PAL = dict(
    SIGNATURE=(58, 26, 46),
    ACCENT=(186, 149, 74),
    LEAD=(126, 54, 66),
    MARK=(58, 26, 46),
)

CRED_LEMOINE = "Olivier Lemoine / Wikimedia Commons (CC BY-SA 4.0)"
CRED_AGNE = "Agne27 / Wikimedia Commons (CC BY-SA 3.0)"

SLIDES = [

    # ── 1 · THE QUESTION — no hint, no hedge ──────────────────────────
    ("duel", dict(
        # Band restored, with the labels naming the two POLES rather
        # than describing the photographs. That is what duel's labels
        # are for on this format — they are the sides of the argument,
        # sitting under a headline that has just posed it, not captions
        # asserting that these images depict stem inclusion. Dropping
        # the band entirely was the first fix and it left the bottom
        # half of the slide empty, which is a worse problem than the one
        # it solved. The photographs are illustrative: hand-picking into
        # crates, which is how whole unbroken bunches reach the winery,
        # and Syrah fruit.
        photos=("nr_harvest_hands", "nr_syrah_bunch"),
        labels=("Whole Bunch", "Destemmed"),
        photo_credit=f"Nico Becker / Pexels · {CRED_AGNE}",
        photo_position="bottom",
        kicker="SPLIT DECISION",
        headline="Whole Bunch or Destemmed?",
        standfirst="Northern Rhône cru reds are made both ways, and the choice changes "
                   "the wine more than the vintage does.",
        standfirst_leading=1.04,
        mode="columns",
        cols=[
            ("STEMS IN",
             "Bunches go into the fermenter intact, stalks and all. Aeration of the "
             "must, and perfume, freshness and fine tannin — if the stems are ripe."),
            ("STEMS OUT",
             "Destemmed, chilled, cold soaked one to three days to draw out colour. "
             "Nothing green can reach the wine."),
        ],
    )),

    # ── 2 · MECHANISM, POSITION, RE-OPEN ──────────────────────────────
    ("side_rail", dict(
        photo="nr_cellar_foudre",
        side="right",
        # Was "Open-top fermenters, northern Rhône" — wrong on both
        # counts. The file is "Cave à fût oxoline": barrels on a rotating
        # rack, not fermenters, and its Commons metadata carries no
        # location precise enough to name a region.
        photo_caption="Small barrels on an oxoline rack",
        photo_credit=CRED_LEMOINE,
        kicker="THE MECHANISM",
        headline="It Turns on\nStem Ripeness",
        standfirst="Not on style, not on tradition. It depends on whether the stems are "
                   "ripe enough to give without taking.",
        items=[
            ("What stems give", "Aeration, plus perfume, freshness and fine tannin."),
            ("What they take", "Unripe stems give green astringent tannin and lower acidity "
                               "— least welcome in a warm vintage."),
            ("Our position", "Whole bunch, in the years that earn it. Aromatics are the "
                             "point here, and stems amplify them."),
            # The guide requires the last line to re-open the question,
            # not to land the position. Burgundy is D3's own example and
            # it cuts against us: a whole region destemmed on one
            # winemaker's authority, then changed its mind again.
            ("And yet", "Burgundy destemmed after Jayer, then came back. Which of those "
                        "was the fashion?"),
        ],
    )),
]


def build():
    import glob
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    paths = []
    for i, (name, slot) in enumerate(SLIDES, start=1):
        img = modules.MODULES[name](slot, i, len(SLIDES), PAL)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  {name}")
    pdf = f"{OUT}/SD_WholeBunch_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
