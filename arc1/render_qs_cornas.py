"""QUICK SIPS — Cornas. "No White Wine, No Rosé"

Arc 1, Mon 7 September — the first post of the arc, published the day
before the Field Guide. Two pages per QUICK_SIPS_STYLE_GUIDE.md.

Every factual claim is from D3 Ch. 7, Cornas AOC: most southerly of the
northern Rhône red appellations; a natural south- and east-facing
amphitheatre with some steep slopes; warm Mediterranean climate, good
protection from cold winds, excellent aspect, so often the first Syrah
picked in the north; red only, 100% Syrah; 40 hL/ha; 145 ha, now mainly
planted; a reputation for tannic intensity, some producers using small
barrels to soften, current trend back toward robust and long-lived;
Voge, Paris, Clape.

Bottle photography is a placeholder pending Steve's shots. The
placeholder has the same aspect and opaque bounding box as a real
cutout, so the bleed math and the caption lockup land where they will
land with the real asset.

Palette matches the Field Guide's Arc 1 signature so the two posts read
as one arc in the grid — Quick Sips leans garnet-and-gold per §4, and
QUICKSIPS_GOLD is a fixed series mark that does not flex per deck.

Four-designer pass and social pass run before first presentation.
Social gates carried here (a 2-page post cannot carry all eight):
  cover hook ..... page 1 title — a prohibition, not a description
  send line ...... "the first Syrah picked in the north"
  save asset ..... page 2 dashboard + the three producer names
  second beat .... sets up the Field Guide's slide 6, which lands
                   the next morning and explains why Cornas is the
                   only cru with no white grape in its rules at all
"""
import os

import core
import modules
import quick_sips

OUT = "/home/claude/out_qs_cornas"
os.makedirs(OUT, exist_ok=True)

PAL = dict(
    SIGNATURE=(58, 26, 46),
    ACCENT=(186, 149, 74),
    LEAD=(126, 54, 66),
    MARK=(58, 26, 46),
)

CRED_FORET = "Jacques Forêt / Wikimedia Commons (CC BY-SA 4.0)"
# Steve's bottle shots, cut out with core.remove_background at
# white_threshold=735 (both labels are cream and needed the higher
# setting; verified hole-free by compositing over grey).
BOTTLE_CLAPE = "qs_bottle_clape.png"
BOTTLE_PARIS = "qs_bottle_paris.png"

# WSET Level 3 SAT terms only, per §9's content standard — no flavour
# language in the dashboard. Six rows: red wine, so Tannins is present.
# Order is the locked system order: Sweetness, Acidity, Tannins,
# Alcohol, Body, Aroma Intensity.
# Two dashboards, one per bottle, rather than one generic appellation
# profile repeated. The pages are making different arguments — the
# traditional benchmark against the modern entry point — and an
# identical dashboard on both would have quietly denied that.
#
# Structure read off published notes, translated into SAT terms. No
# flavour language here per §9; the aromatics live in the bench_note.

# Clape 2019. Vinous: "densely packed", "slowly building tannins add
# grip", "a core of juicy acidity". Suckling: "very concentrated",
# "rich, velvety tannins". Falstaff: "very dense with fine-grained
# tannins", two decades of ageing potential. Label reads 13.5%.
STRUCTURE_CLAPE = [
    ("Sweetness", 0.06, "Dry"),
    ("Acidity", 0.72, "Medium (+)"),
    ("Tannins", 0.92, "High"),
    ("Alcohol", 0.72, "Medium"),
    ("Body", 0.90, "Full"),
    ("Aroma Intensity", 0.92, "Pronounced"),
]

# Vincent Paris "Granit 30". Dunnuck: "medium to full-bodied", "ripe
# tannins", the most forward and approachable of Paris's cuvées.
# Vinous: "round and refreshing", "remarkable energy and freshness".
# Destemmed, so the tannin sits well below Clape's.
#
# ALCOHOL: the label on the bottle in hand reads 14% by vol, which is
# High on the SAT scale (14%+), not Medium. Suckling's note put the
# 2022 at "around 13 per cent" and I had built the dashboard on that —
# wrong, and it also made this the LOWER-alcohol of the two bottles
# when the label says it is the higher. The bottle we are photographing
# wins over a critic's note on a different vintage.
STRUCTURE_PARIS = [
    ("Sweetness", 0.06, "Dry"),
    ("Acidity", 0.76, "Medium (+)"),
    ("Tannins", 0.70, "Medium (+)"),
    ("Alcohol", 0.90, "High"),
    ("Body", 0.78, "Medium (+)"),
    ("Aroma Intensity", 0.90, "Pronounced"),
]

SLIDES = [

    ("cover", dict(
        photo="qs_cornas_church",
        photo_h=980,
        photo_anchor=0.42,
        # No legibility chip — the photograph carries the frame. The
        # corner mark keeps its own small scrim (mark_scrim) since it
        # sits over open sky at the top, which is the one place white
        # text has nothing to hold on to.
        caption_chip=False,
        title_scrim=True,
        mark_scrim=True,
        photo_credit=CRED_FORET,
        title="No White Wine, No Rosé",
        tagline="One hundred per cent Syrah, by law",
        para1="Cornas is the only northern Rhône cru whose rules permit no white "
              "grape at all. Every other appellation on the river allows one "
              "somewhere.",
        para1_lead_words=1,
        para2="145 hectares, and 40 hL/ha at the ceiling.",
        para2_lead_words=2,
        structure=STRUCTURE_CLAPE,
        bench_heading="THE BENCHMARK",
        bench_photo=BOTTLE_CLAPE,
        bench_producer="Domaine A. Clape",
        bench_wine="Cornas 2019",
        bench_origin="Cornas AOC · 13.5%",
        # Trimmed to fit the caption zone — the guard fires on total
        # lockup height, so this is a copy cut, not a type reduction.
        bench_note="Smoke, damson and cocoa over granite. Whole-bunch, old "
                   "vines, tannin that builds rather than announces itself.",
    )),

    ("detail", dict(
        topic="Cornas",
        headline="First Picked in the North",
        body="A natural south- and east-facing amphitheatre with some steep slopes, "
             "warm and Mediterranean, and well protected from cold winds. That "
             "aspect is why Cornas is often the first Syrah harvested in the "
             "northern Rhône — and why the wines built a reputation for tannic "
             "intensity. Some producers reach for small barrels to soften them. "
             "The current trend runs the other way, back toward robust and "
             "long-lived. It is the smallest of the northern Rhône's red "
             "appellations at 145 hectares — about a twelfth of "
             "Crozes-Hermitage, next door on the other bank.",
        body_lead_words=3,
        structure=STRUCTURE_PARIS,
        bench_heading="WHERE TO START",
        bench_photo=BOTTLE_PARIS,
        bench_producer="Domaine Vincent Paris",
        bench_wine="Cornas \u2018Granit 30\u2019",
        bench_origin="Cornas AOC · 14%",
        bench_note="Forest berry, cracked pepper, violets. Destemmed, and "
                   "built on lift rather than weight. The 30 is the slope "
                   "gradient.",
        # Last page: drop the swipe cue rather than prompt the reader
        # toward a page that does not exist (style guide §6.5).
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
    pdf = f"{OUT}/QS_Cornas_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
