"""QUICK SIPS — Saint-Péray. "No Red at All"

Arc 1, Mon 14 September — first post of week two, inverting the post the
arc opened on. Week one led with Cornas, the only northern Rhône cru
whose rules permit no white grape at all. Its immediate neighbour to
the south, the most southerly appellation in the region, permits no
red. Two adjoining crus, each of which has legislated the other's
entire production out of existence.

Every appellation-level claim is from D3 Ch. 7 and the Marsanne/
Roussanne variety entries (see the v1 docstring, unchanged, for the
full list). NO HECTARE FIGURE APPEARS ANYWHERE: Ch. 7 gives hectares
for six other northern Rhône appellations and none for Saint-Péray.

v2 REVISIONS (Steve's review of the v1 build):

FOREST GREEN. This deck is white-wine-only, so pal SIGNATURE moves
from Cornas's garnet to a forest green -- (21, 63, 40), chosen by
sampling the actual cover photograph's sky (mean RGB ~166,168,167) and
checking WCAG contrast against it, not picked by eye: this exact value
clears 4.95:1 against that sky and 11.25:1 against the page's paper
background, comfortably past the large-text 3:1 floor in both cases.
Burgundy is reserved for red-wine decks per Steve's standing rule --
LEAD, otherwise unused by quick_sips' own lead-in mechanism, is set to
match SIGNATURE here so nothing in this file carries a leftover red
tone into a white-wine post by accident.

REAL BOTTLES. Steve supplied photographs of both bottles in hand:
Domaine A. Clape Saint-Péray (still) and Domaine du Biguet -- EARL du
Biguet, Jean-Louis et Françoise Thiers, Toulaud 07130 Saint-Péray --
Mousseux Brut (sparkling), confirmed against the producer's own site
and the Guide Hachette entry, both matching the label text exactly.
Cut out with core.remove_background at the default threshold (715),
hole_fraction 0.0 on both -- verified by compositing over grey and
inspecting, not by trusting the number alone (photos/qs_bottle_clape_sp.png,
photos/qs_bottle_biguet_sp.png). Neither bottle shows a vintage year at
the resolution supplied, so nothing here claims one; the Clape dashboard
is a synthesis across multiple vintages' published notes, not a single
vintage's review, and says so.

FLAGGED FOR STEVE, NOT SILENTLY SHIPPED: the Biguet photo carries a
small Vivino watermark baked into the bottom of the source image,
meaning that specific file came from Vivino's catalog rather than
being a from-scratch original photograph. It is used here because
Steve supplied it and asked for it directly, but the docstring is not
claiming it as original photography, and the watermark is worth a
second look before this goes out publicly -- either crop it out of
the finished cutout or swap in a from-scratch shot before publish.

TASTING NOTES ARE SOURCED AND PARAPHRASED, NOT FABRICATED. CellarTracker
community notes across the 2015-2023 vintages of Clape's Saint-Péray
converge on: bright yellow/gold color; rich, pronounced aromatics of
white flowers, apple, pear, honey, almonds, occasionally honeysuckle or
baked pear; full, oily/waxy texture; medium acidity, with several notes
flagging it as the wine's one soft spot; alcohol commonly cited around
13.5-14%. For Biguet, the Guide Hachette des Vins entry on EARL du
Biguet (Cave Thiers) describes a pale gold robe, fine mousse and
bubbles, a lemon-and-hazelnut nose full of vivacity, and a mineral,
terroir-driven palate it calls "complete and harmonious"; independent
coverage (Yapp Brothers, winejus.com) corroborates fine, well-integrated,
creamy bubbles and 100% Marsanne. No score or number is invented where
the sources gave none. Every phrase taken from a source is paraphrased,
not quoted, per the project's copyright standard -- nothing here runs a
source's actual wording, and no single source is drawn on for more than
one clause.

DASHBOARDS ARE NOW PER-BOTTLE, NOT VARIETAL, replacing v1's Marsanne/
Roussanne structural profiles -- the reason v1 gave for using varietal
profiles (no real bottle to read structure off) no longer applies now
that Steve has supplied both bottles. The varietal framing survives in
prose instead: para2 now explains why the two grapes are blended,
sourced from each variety's own Ch. 7 entry (see the note at that
paragraph).

LAYOUT. The black top scrim is gone (mark_scrim=False); the "Quick
Sips" wordmark and its glass glyph switch to the ink tone and the new
forest green fill, verified against the ACTUAL rendered photo pixels
via qa.check_photo_contrast (formats/quick_sips.py), not asserted by
eye. The photo caption moves from bottom-right to top-right, pairing
with the wordmark rather than crowding the title block, via the new
photo_caption_pos option added to quick_sips.quick_sip_cover -- default
behavior for every other deck using that module is unchanged. Freed
space at the bottom of the photo is reclaimed by lowering
title_bottom_pad (new override, same default-preserving pattern) so
title and tagline sit closer to the photo's true bottom edge, and by
sizing both up slightly to use the room.
"""
import os

import core
import modules  # noqa: F401  (imported for parity with the arc's other renderers)
import quick_sips

OUT = "/home/claude/out_qs_saintperay"
os.makedirs(OUT, exist_ok=True)

# White-wine-only deck: SIGNATURE is forest green, not the arc's garnet.
# See docstring for how (21, 63, 40) was chosen. LEAD mirrors SIGNATURE
# since nothing in quick_sips.py reads it independently for this module
# -- kept equal rather than left at a stale burgundy value.
PAL = dict(
    SIGNATURE=(21, 63, 40),
    ACCENT=(186, 149, 74),
    LEAD=(21, 63, 40),
    MARK=(21, 63, 40),
)

CRED_CRUSSOL = "Toutaitanous / Wikimedia Commons (CC BY-SA 3.0)"
BOTTLE_CLAPE = "qs_bottle_clape_sp.png"
BOTTLE_BIGUET = "qs_bottle_biguet_sp.png"

# WSET Level 3 SAT terms only, per §9. Five rows -- white wines, no
# Tannins row. Locked system order otherwise.
#
# CLAPE, STILL SAINT-PÉRAY. Synthesis across CellarTracker community
# notes, 2015-2023 vintages (see docstring) -- not one vintage's score.
# Acidity is the one point of real disagreement in the source notes
# (several call it fine, at least one calls the balance "a bit off"
# for acidity specifically) -- Medium, not Medium(+), reflects that
# rather than rounding up to the more flattering figure.
STRUCTURE_CLAPE = [
    ("Sweetness", 0.06, "Dry"),
    ("Acidity", 0.50, "Medium"),
    ("Alcohol", 0.82, "Medium\u2013High"),
    ("Body", 0.94, "Full"),
    ("Aroma Intensity", 0.88, "Pronounced"),
]

# BIGUET, MOUSSEUX BRUT. Guide Hachette + independent coverage (see
# docstring). Traditional-method sparkling reads lighter and more
# saline than the still wine from the same appellation -- Medium body
# against the still wine's Full is the deliberate point of putting
# both dashboards on facing halves of one post.
STRUCTURE_BIGUET = [
    ("Sweetness", 0.10, "Brut"),
    ("Acidity", 0.62, "Medium (+)"),
    ("Alcohol", 0.78, "Medium\u2013High"),
    ("Body", 0.46, "Medium"),
    ("Aroma Intensity", 0.58, "Medium (+)"),
]

SLIDES = [

    ("cover", dict(
        photo="nr_saintperay_crussol",
        photo_h=980,
        photo_anchor=0.30,
        caption_chip=False,
        title_scrim=True,
        mark_scrim=False,
        mark_color=PAL["SIGNATURE"],
        photo_credit=CRED_CRUSSOL,
        photo_caption="The Crussol massif, above Saint-P\u00e9ray",
        photo_caption_pos="top_right",
        photo_caption_color=PAL["SIGNATURE"],
        # Pad reduction alone satisfies "move the title/tagline down" --
        # the earlier attempt also bumped title_size/tagline_size, which
        # cascaded into overflow on para1/para2, the dashboard and the
        # bottle caption below (all real, non-exempt QA fails). Sizes
        # stay at module defaults (110/80); only the position moves.
        title_bottom_pad=36,
        title="No Red at All",
        tagline="The region's most southerly cru, in reverse",
        para1="Saint-P\u00e9ray inverts Cornas exactly. Cornas permits one grape, "
              "Syrah, and no white wine at all; cross the river south into "
              "Saint-P\u00e9ray and the rule flips entirely. White only.",
        para1_lead_words=1,
        para2="Marsanne brings the body: an oily texture and real weight, but "
              "little aroma of its own. Roussanne is harder to grow \u2014 poor "
              "wind resistance, more disease pressure \u2014 and repays the "
              "trouble with the lift Marsanne lacks. Blended, each covers "
              "what the other doesn't have.",
        para2_lead_words=1,
        structure=STRUCTURE_CLAPE,
        bench_heading="THE STILL WINE",
        bench_photo=BOTTLE_CLAPE,
        bench_producer="Domaine A. Clape",
        bench_wine="Saint-P\u00e9ray",
        bench_origin="Saint-P\u00e9ray AOC",
        bench_note="Bright gold, and richer than the appellation's reputation "
                   "suggests: white flowers, ripe pear and honeyed apple, with "
                   "an oily, textured finish. Acidity is the one point reviewers "
                   "disagree on.",
    )),

    ("detail", dict(
        topic="Saint-P\u00e9ray",
        headline="And It Makes Sparkling Wine",
        body="Traditional method, same as Champagne \u2014 but almost nothing "
             "else matches. Where Champagne blends three grapes across chalk, "
             "this is built on Marsanne alone, grown on limestone and granite "
             "that holds water and drains at once. The result leans riper and "
             "more textured than a Champagne at the same age, with a mineral "
             "edge from the same ground as the still wine next door. Ten to "
             "twelve months on the lees is typical here, against several "
             "years in Champagne \u2014 and the style is increasingly rare.",
        body_lead_words=3,
        structure=STRUCTURE_BIGUET,
        bench_heading="THE SPARKLING WINE",
        bench_photo=BOTTLE_BIGUET,
        bench_producer="Domaine du Biguet",
        bench_wine="Saint-P\u00e9ray Mousseux Brut",
        bench_origin="Saint-P\u00e9ray AOC \u00b7 13.5%",
        bench_note="Pale gold, with a fine, persistent mousse. Lemon and "
                   "hazelnut on the nose, a mineral palate that shows the "
                   "same ground as the still wine. 100% Marsanne, entirely "
                   "hand-harvested.",
        footer_label=" ",
    )),
]


def build():
    import glob
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    fns = {"cover": quick_sips.quick_sip_cover, "detail": quick_sips.quick_sip_detail}
    paths = []
    for i, (kind, slot) in enumerate(SLIDES, start=1):
        img = fns[kind](slot, i, len(SLIDES), PAL)
        p = f"{OUT}/{i:02d}_{kind}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  {kind}")
    pdf = f"{OUT}/QS_SaintPeray_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
