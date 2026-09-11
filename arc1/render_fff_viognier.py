"""FFFA — Five Fascinating Facts About Viognier. Arc 1, Thu 10 September.

Fixed 6-page format per FFFA_STYLE_GUIDE.md: fff_cover() once, then
fff_fact() five times, the fifth with closing=True folding "Cheers!"
into the same page. Never 7 pages.

EVERY FACT IS FROM D3 Ch. 7. In particular:

- The "Viognier was down to a handful of hectares in the 1960s" claim
  that circulates everywhere is NOT in the primary sources and was
  flagged unsourced in the Field Guide spec. It does not appear here.
  What D3 does support is that Château-Grillet built the variety's
  reputation, some of it domaine-bottled from the 1830s, "before the
  variety came back into fashion in the 1980s" — so fact 3 makes the
  revival claim with the date D3 actually gives, and makes no claim
  about how little was planted.
- The 20 per cent co-fermentation rule is scoped to Côte-Rôtie, where
  D3 places it, not to "northern Rhône reds" generally.

Headline colour stays FFFA_YELLOW — no per-deck override. The series
default is a golden yellow and the subject is a white wine whose D3
descriptors are honeysuckle, apricot and peach; a deck override exists
for cases like the Cabernet Franc red deck, and this is not one.

Photography: the cover cluster is Washington-grown Viognier and the
harvest bin on page 2 is Chardonnay in the Yakima Valley — neither is
Rhône fruit, and neither is claimed to be. FFFA fact pages carry no
photo captions, only credits, so no location assertion is made
anywhere. The Rhône-specific images are the Condrieu, Château-Grillet
and Côte-Rôtie photographs already sourced and location-verified for
the Field Guide.

Social gates on a 6-page facts post:
  save asset ..... the five facts are the asset
  decode layer ... fact 3's Château-Grillet photo is the estate itself
  send line ...... fact 1, the picking window
  callback ....... fact 5 pays off the Field Guide's slide 6
"""
import os

import core
from fff_facts import fff_cover, fff_fact

OUT = "/home/claude/out_fff_viognier"
os.makedirs(OUT, exist_ok=True)
TOTAL = 6

CRED_AGNE = "Agne27 / Wikimedia Commons (CC BY-SA 3.0)"
CRED_CASAMANCE = "Marianne Casamance / Wikimedia Commons (CC BY-SA 4.0)"
CRED_AGNE_BIN = "Agne27 / Wikimedia Commons (CC BY-SA 3.0)"
CRED_LEMOINE = "Olivier Lemoine / Wikimedia Commons (CC BY-SA 4.0)"
CRED_PHILDIC = "PHILDIC / Wikimedia Commons (CC0)"
CRED_GOUDAN = "Goudan07 / Wikimedia Commons (CC BY-SA 3.0)"
CRED_KAREN = "Karen / Wikimedia Commons (CC BY 2.0)"

# Cover is the cluster, per Steve — this reverses my own earlier call
# to move it off for reading like a catalogue entry. It is the most
# direct statement of what the deck is about, and a grape-variety deck
# arguably should open on the grape.
COVER = dict(
    # Graded cover build, not the raw file: cluster isolated onto near
    # black and brightened. See build_fff_cover.py for why the wall
    # needed a 2D background model rather than a threshold.
    photo="fff_viognier_cover.jpg",
    subject="Viognier",
    photo_anchor=0.45,
    photo_credit=CRED_AGNE,
)

FACTS = [
    dict(
        number=1,
        # New image for this page now the cluster has gone to the cover.
        # White grapes already in the bin at the end of a row: the
        # picking decision has been made and executed, which is what the
        # fact is about. A refractometer shot was the first candidate —
        # thematically exact, since brix is how the call gets made — but
        # it is a stainless sink, a plastic jug and a camera flash, and
        # nothing in the frame carries the register.
        photo="fff_harvest_bin.jpg",
        photo_anchor=0.62,
        headline="The Picking Window Is Brutally Narrow",
        body="Pick early and the pronounced aromas never arrive. Pick late and it loses "
             "flavour and acidity, and gains sugar fast.",
        photo_credit=CRED_AGNE_BIN,
    ),
    dict(
        number=2,
        photo="nr_echalas_condrieu",
        photo_anchor=0.45,
        headline="It Buds Early and Sets Badly",
        body="Early budding means spring frost. Poor flowering and fruit set mean low, "
             "unpredictable yields. It is grown on poles against the wind.",
        photo_credit=CRED_LEMOINE,
    ),
    dict(
        number=3,
        photo="nr_grillet",
        photo_anchor=0.5,
        headline="3.5 Hectares Made Its Reputation",
        body="Château-Grillet, domaine-bottling from the 1830s, established Viognier as "
             "one of France's great wines — long before it came back into fashion in "
             "the 1980s.",
        photo_credit=CRED_PHILDIC,
    ),
    dict(
        number=4,
        photo="nr_condrieu_pano",
        photo_anchor=0.5,
        headline="Condrieu Is the World's Model",
        body="197 hectares, 100 per cent Viognier, 41 hL/ha. Premium to super-premium, "
             "and the benchmark for the grape everywhere else.",
        photo_credit=CRED_GOUDAN,
    ),
    dict(
        number=5,
        photo="nr_cover_coterotie",
        photo_anchor=0.5,
        headline="It Goes Into Red Wine Too",
        body="Côte-Rôtie permits up to 20 per cent Viognier in the red — co-fermented "
             "with the Syrah, never blended in afterwards.",
        photo_credit=CRED_KAREN,
    ),
]


def build():
    import glob
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    paths = []
    img = fff_cover(COVER, total=TOTAL)
    p = f"{OUT}/01_cover.png"
    img.save(p)
    paths.append(p)
    print("  01  cover")

    for i, slot in enumerate(FACTS, start=2):
        img = fff_fact(slot, i, total=TOTAL, closing=(i == TOTAL))
        p = f"{OUT}/{i:02d}_fact{slot['number']}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  fact {slot['number']}")

    pdf = f"{OUT}/FFF_Viognier_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
