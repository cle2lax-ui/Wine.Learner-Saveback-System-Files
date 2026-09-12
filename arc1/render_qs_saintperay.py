"""QUICK SIPS — Saint-Péray. "No Red at All"

Arc 1, Mon 14 September — the first post of week two, and a deliberate
inversion of the post the arc opened on. Week one led with Cornas, the
only northern Rhône cru whose rules permit no white grape at all. Its
immediate neighbour to the south, the most southerly appellation in the
region, permits no red. Two adjoining crus, each of which has
legislated the other's entire production out of existence.

Every factual claim is from D3 Ch. 7, Saint-Péray AOC and the Marsanne
and Roussanne variety entries: most southerly of the northern Rhône
appellations; slightly cooler climate than its immediate neighbours;
devoted to white wines; limestone and granitic soils giving both
water-holding capacity and drainage; Marsanne the vast majority of
plantings with some Roussanne; 45 hL/ha; fermented in stainless steel
or oak barrels, aged in the same or in large old oak; higher quality
wines aged 10-12 months on the lees, some producers stirring for body;
good to very good, mid- to premium priced; traditional method sparkling
from the same varieties, increasingly rare.

NO HECTARE FIGURE APPEARS ANYWHERE IN THIS DECK. Ch. 7 gives hectares
for Cote-Rotie (250), Condrieu (197), Chateau-Grillet (3.5), Hermitage
(137), Crozes (~1,700) and Cornas (145). It gives none for Saint-Peray.
Week one's Cornas deck leaned on "145 hectares" in para2 and this one
cannot, so para2 carries the yield ceiling and the soils instead. The
cross-appellation comparison in the detail body uses Cornas's 40 hL/ha
against this appellation's 45, both of which are stated.

THE DASHBOARDS ARE VARIETAL, NOT PER-BOTTLE, AND THAT IS THE POINT.
Week one's Cornas deck ran two bottle-specific dashboards read off
Steve's actual bottles in hand. Those bottles do not exist yet here, and
inventing SAT values for a wine nobody has opened would be fabrication
of exactly the kind the arc's sourcing rule exists to prevent. But Ch. 7
gives explicit structural profiles for both permitted varieties, so the
dashboards carry Marsanne and Roussanne instead -- sourced, useful to a
student, and honest about what they are. When Steve's photography lands,
these can either stay (they teach more than two bottle profiles would)
or be replaced per-bottle. That is a review decision, not a build one.

BOTTLE SLOTS are qs_bottle_placeholder.png in both positions, same
mechanism week one used before Steve's shots arrived. Slot B is the
sparkling, and Ch. 7's "increasingly rare" is likely to show up in
availability -- see ARC1_WEEK2_PLAN.md for the fallback, which is a
single-bottle layout with the sparkling carried as text, never a
substitution from another appellation.

Social gates carried here (a 2-page post cannot carry all eight):
  cover hook ..... page 1 title -- a prohibition, mirroring week one's
  send line ...... the Cornas/Saint-Peray inversion itself
  save asset ..... the two varietal dashboards
  callback ....... closes the loop on the arc's opening post, one week
                   to the day after it published
"""
import os

import core
import modules  # noqa: F401  (imported for parity with the arc's other renderers)
import quick_sips

OUT = "/home/claude/out_qs_saintperay"
os.makedirs(OUT, exist_ok=True)

# Identical to render_qs_cornas.py -- Arc 1 signature, so week one and
# week two read as one arc in the grid.
PAL = dict(
    SIGNATURE=(58, 26, 46),
    ACCENT=(186, 149, 74),
    LEAD=(126, 54, 66),
    MARK=(58, 26, 46),
)

CRED_CRUSSOL = "Toutaitanous / Wikimedia Commons (CC BY-SA 3.0)"
BOTTLE_PLACEHOLDER = "qs_bottle_placeholder.png"

# WSET Level 3 SAT terms only, per §9. Five rows, not six: these are
# white wines, so no Tannins row. Locked system order otherwise.
#
# MARSANNE, from Ch. 7 verbatim: "low intensity honeysuckle, lemon and
# apricot fruit, an oily texture, medium acidity, full body and medium
# to high alcohol." Every row below is that sentence. The low aroma
# intensity is the surprising one and it is the chapter's own word --
# it is not a criticism of the variety, it is why Marsanne is a base
# rather than a soloist, and why lees ageing and lees stirring matter
# so much here.
STRUCTURE_MARSANNE = [
    ("Sweetness", 0.06, "Dry"),
    ("Acidity", 0.52, "Medium"),
    ("Alcohol", 0.80, "Medium\u2013High"),
    ("Body", 0.92, "Full"),
    ("Aroma Intensity", 0.22, "Low"),
]

# ROUSSANNE, from Ch. 7: "medium to medium (+) intensity aromatics of
# pear with herbal notes, medium to medium (+) acidity and medium to
# high alcohol", and "similar in colour and structure to Marsanne but
# the wines tend to age quicker."
#
# BODY IS DERIVED, NOT STATED. Ch. 7 gives Roussanne no body term of
# its own; the Full below comes from the "similar in structure to
# Marsanne" line. Flagged rather than passed off as directly sourced.
# If Steve would rather not derive it, the row comes out and the
# dashboard runs to four.
STRUCTURE_ROUSSANNE = [
    ("Sweetness", 0.06, "Dry"),
    ("Acidity", 0.64, "Medium (+)"),
    ("Alcohol", 0.80, "Medium\u2013High"),
    ("Body", 0.90, "Full"),
    ("Aroma Intensity", 0.62, "Medium (+)"),
]

SLIDES = [

    ("cover", dict(
        photo="nr_saintperay_crussol",
        photo_h=980,
        # Anchored high. The source frame runs ridge, then treeline,
        # then the modern edge of town and a car park along the river.
        # At 0.30 the crop keeps the limestone and the ruined chateau
        # and loses the town, which is the honest emphasis anyway --
        # Crussol is the limestone, and limestone is what the post is
        # about.
        photo_anchor=0.30,
        caption_chip=False,
        title_scrim=True,
        mark_scrim=True,
        photo_credit=CRED_CRUSSOL,
        # Caption claims the landform, not the vineyards. Vines are not
        # legible in this frame and the image is captioned on Commons as
        # the chateau seen from across the river, so claiming a vineyard
        # view would be asserting something the photograph does not show.
        photo_caption="The Crussol massif, above Saint-P\u00e9ray",
        title="No Red at All",
        tagline="The region's most southerly cru, in reverse",
        # Trimmed twice against the paragraph-overlap guard, which is a
        # real FAIL, not an exemption. "the most southerly appellation
        # in the northern Rhone" moved to the tagline's job and the
        # sentence lost its subordinate clause. Copy cut, type untouched.
        para1="Cornas permits one grape, Syrah, and no white wine at all. "
              "Saint-P\u00e9ray, next door south, inverts it exactly: white only.",
        para1_lead_words=2,
        para2="Marsanne for the vast majority, some Roussanne, at 45 hL/ha.",
        para2_lead_words=2,
        structure=STRUCTURE_MARSANNE,
        bench_heading="THE MAJORITY GRAPE",
        bench_photo=BOTTLE_PLACEHOLDER,
        bench_producer="Marsanne",
        bench_wine="Slot A \u00b7 still Saint-P\u00e9ray",
        bench_origin="Photography pending",
        bench_note="Late-budding and productive, so yields must be held down. "
                   "Best on stony, low-fertility soils.",
    )),

    ("detail", dict(
        topic="Saint-P\u00e9ray",
        headline="And It Makes Sparkling Wine",
        body="Traditional method, from the same two varieties \u2014 and, per the "
             "chapter, increasingly rare. Limestone and granite give water-holding "
             "capacity and drainage at once, on a site slightly cooler than its "
             "neighbours. The ceiling is 45 hL/ha against Cornas's 40. Better "
             "wines spend ten to twelve months on the lees, some stirred for body "
             "\u2014 worth knowing, given how little aromatic intensity Marsanne "
             "brings on its own. Fermentation is in stainless steel or oak, "
             "ageing in the same or in large old vessels.",
        body_lead_words=3,
        structure=STRUCTURE_ROUSSANNE,
        bench_heading="THE PARTNER",
        bench_photo=BOTTLE_PLACEHOLDER,
        bench_producer="Roussanne",
        bench_wine="Slot B \u00b7 sparkling Saint-P\u00e9ray",
        bench_origin="Photography pending",
        bench_note="Harder to grow \u2014 poor wind resistance, coulure, mildew "
                   "\u2014 so less widely planted. It brings the aromatics "
                   "Marsanne does not.",
        # Last page: drop the swipe cue rather than prompt toward a page
        # that does not exist (style guide §6.5).
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
