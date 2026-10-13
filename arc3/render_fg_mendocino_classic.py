"""THE FIELD GUIDE: MENDOCINO -- "The Fog Does the Work". A classic-style carousel deck (2160x2700, 12 slides).

Steve (Oct 2026): the Reels-only approach cut views and engagement; return to the original Field Guide style for
Mendocino -- 10-12 pages, the old style guide (serif titles, off-white paper, high-fidelity AVA maps), varied layouts,
lots of graphics and illustrations, medium photo weight. Held to the visual benchmark (guides/VISUAL_BENCHMARK_v10.md,
the Mosel deck): 12 slides in 12 distinct layouts, 5 led by a map, diagram or data graphic, the cover full-bleed, chart
colors sampled from the cover (arc3/sample_fg_classic_palette.py), maps from real data (arc3/prepare_fg_classic_maps.py).

SOURCES (WSET first, DESIGN_PROCESS s12)
  D3 Ch. 23.1 (North Coast -- Mendocino County, Anderson Valley AVA): one million ha, 7,000 under vine; cooler coastal
    AVAs vs warmer inland (Redwood Valley: Zinfandel, Syrah, Petite Sirah, Cabernet Sauvignon; high Potter Valley:
    Sauvignon Blanc, Riesling); priced below Napa and Sonoma, often in multi-regional blends; the Mendocino AVA starts at
    the Russian River headwaters and covers six AVAs (named) and can be used for blends across them. Anderson Valley:
    NW-SE, a few miles from the Pacific; cold air and fog funnelled along the Navarro River; warm days, cold evenings
    and mornings; narrower and warmer inland; 900-2,000 mm of rain, mostly winter and spring, the NW wettest; most
    vineyards on slopes; spring frost in low-lying areas; just under 1,000 ha planted; early-ripening Pinot Noir and
    Chardonnay the two most planted, for sparkling and still; Pinot Noir fresh raspberry, cherry and plum, medium body,
    medium (+) acidity, good to outstanding, premium (some super-premium), style varies with site, clone and harvest
    timing; Alsace-style whites from Gewurztraminer, Riesling, Pinot Gris, Pinot Blanc; 30 wineries, many with cellar
    doors for coast tourism; wineries elsewhere buy the fruit for appellation- or vineyard-specific wines.
  CSW Study Guide (2018): about 17,000 acres; mostly mountainous and forested, vineyards confined largely to river
    valleys; 25% certified organic, the largest share in the US (dated "in 2018" on the slide); Anderson Valley one of
    the coolest areas of California; Mendocino Ridge only at 1,200 ft or higher, "Islands in the Sky", just over 250 of
    250,000 acres planted; Cole Ranch the smallest AVA in the US (its single-owner detail is NOT used: the AVA was put
    up for sale in 2019).
  TTB / UC Davis AVA data: creation dates; Covelo and Dos Rios lie outside the North Coast AVA (geometry), and Comptche
    (2024) was excluded from it by the TTB (T.D. TTB-192).
  Measured from the data: about 4 miles from the Anderson Valley AVA to open ocean; Boonville and Philo verified inside
    the AVA. Geography: Anderson Valley about 39 N; Champagne about 49 N, Alsace about 48 N, Burgundy about 47 N
    (Reims 49.3, Colmar 48.1, Beaune 47.0).
PHOTOS (location from each Commons file's own title; the Pexels fog photo has none, so its caption names no place):
  cover + close: Naotake Murayama (CC BY 2.0); Pinot hero, two-climates left: Ethan Prater (CC BY 2.0); two-climates
  right: Missvain (CC BY 4.0, Ukiah); blades: Missvain (CC0, Roederer Estate), No-till-vineyard (CC0, Husch, Philo),
  Mick Haupt (Pexels); business stripe: No-till-vineyard (CC0, Mendocino County).
"""
import glob
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
os.environ.setdefault("AMERICAN_ENGLISH", "1")
import core      # noqa: E402
import modules   # noqa: E402
import variety   # noqa: E402
import prepare_fg_classic_maps as pm   # noqa: E402
from tokens import W, M, INK, PAPER    # noqa: E402

OUT = "/home/claude/out_fg_mendocino_classic"
os.makedirs(OUT, exist_ok=True)

# ---- palette: sampled from the cover (arc3/sample_fg_classic_palette.py); house gold locked across every arc
REDWOOD, SKY, VINE, SHADE = (66, 101, 34), (112, 172, 246), (100, 133, 29), (52, 79, 16)
TAN, TAN_PALE = (178, 148, 119), (198, 180, 163)
PAL = dict(SIGNATURE=REDWOOD, ACCENT=(196, 158, 84), LEAD=(140, 95, 58), MARK=REDWOOD)
CHART = dict(
    ripe=[SHADE, VINE, (196, 158, 84), TAN, (140, 95, 58)],
    focus=REDWOOD,          # one color, one meaning: the redwood green is "Anderson Valley" on every slide
    cool=SKY, warm=TAN, vine=VINE, shade=SHADE,
    amber=TAN, gold=(196, 158, 84), grape=VINE, stone=(98, 91, 74), track=TAN_PALE,
    ice=SHADE, ice_fill=(225, 238, 250), ice_text=SHADE,
)

CRED_MURAYAMA = "Naotake Murayama / Wikimedia Commons (CC BY 2.0)"
CRED_PRATER = "Ethan Prater / Wikimedia Commons (CC BY 2.0)"

# ---- maps (real data)
pm.check_towns()
AVA_MAP = pm.build_ava_map()
MAP_H_ATLAS = 1180
ZOOM = pm.build_av_zoom(W - 2 * M, MAP_H_ATLAS)
INSET = pm.build_ca_inset()
COAST_MI = pm.coast_distance_miles()
assert 3.5 < COAST_MI < 5.0, COAST_MI          # "about 4 miles" stays true to the measurement


def _euler():
    """North Coast AVA > Mendocino AVA > D3's six. Long names are paired with short ones in each row so sibling labels
    cannot collide; the containment and non-overlap rules the module demands are asserted, not assumed."""
    root = ("North Coast AVA", 1080, 1640, 840, None, "above")
    mid = ("Mendocino AVA", 1080, 1715, 610, "North Coast AVA", "above")
    r = 175
    rows = [("Yorkville Highlands", "Cole Ranch"), ("Anderson Valley", "Potter Valley"), ("McDowell Valley", "Redwood Valley")]
    kids = []
    for j, (a, b) in enumerate(rows):
        cy = mid[2] - 360 + 360 * j
        kids += [(a, mid[1] - 205, cy, r, "Mendocino AVA", "in"), (b, mid[1] + 205, cy, r, "Mendocino AVA", "in")]
    for parent, child in [(root, mid)] + [(mid, k) for k in kids]:
        dist = math.hypot(child[1] - parent[1], child[2] - parent[2])
        assert dist + child[3] <= parent[3], (child[0], dist + child[3], parent[3])
    for i, a in enumerate(kids):
        for b in kids[i + 1:]:
            assert math.hypot(a[1] - b[1], a[2] - b[2]) >= a[3] + b[3], (a[0], b[0])
    return [root, mid] + kids


ATLAS_LABELS = {   # name shown, label position (normalized), side, which target -- placed against a render
    "Mendocino": ("Mendocino AVA", (0.985, 0.48), "left", (0.92, 0.56)),
    "Anderson Valley": ("Anderson Valley", (0.44, 0.10), "right", (0.58, 0.30)),
    "Mendocino Ridge": ("Mendocino Ridge", (0.315, 0.93), "left", None),
    "Yorkville Highlands": ("Yorkville Highlands", (0.70, 0.985), "left", (0.90, 0.92)),
}


def _atlas_regions():
    """Region polygons for atlas (M09). One piece of each AVA carries its label; every other piece (Mendocino Ridge has
    28 in this window) gets a zero-length leader that disappears inside its own fill (atlas draws a leader for every
    region)."""
    fills = {"Mendocino": (236, 232, 218), "Yorkville Highlands": (226, 220, 206),
             "Mendocino Ridge": (214, 222, 236), "Anderson Valley": REDWOOD}
    px = 12 / (W - 2 * M)                                   # atlas starts a right-side leader 12px left of the label
    out = []
    for raw in ("Mendocino", "Yorkville Highlands", "Mendocino Ridge", "Anderson Valley"):
        rings = ZOOM["avas"][raw]
        name, lab, side, tgt = ATLAS_LABELS[raw]
        if tgt is None:                                     # label the piece nearest the label position
            import numpy as np
            tgt = min((tuple(np.mean(np.array(r), 0)) for r in rings), key=lambda c: (c[0] - lab[0]) ** 2 + (c[1] - lab[1]) ** 2)
        main = min(range(len(rings)), key=lambda i: min((x - tgt[0]) ** 2 + (y - tgt[1]) ** 2 for x, y in rings[i]))
        for i, ring in enumerate(rings):
            c = ring[0]
            if i == main:
                out.append(dict(name=name, pts=ring, fill=fills[raw], label=lab, target=tgt, side=side))
            else:
                out.append(dict(name="", pts=ring, fill=fills[raw], label=(c[0] + px, c[1]), target=c, side="right"))
    # draw order: the parent first, then the neighbors, then the valley on top
    order = {"Mendocino AVA": 0, "Yorkville Highlands": 1, "Mendocino Ridge": 2, "Anderson Valley": 3}
    return sorted(out, key=lambda r: order.get(r["name"], 2 if r["fill"] == fills["Mendocino Ridge"] else
                                              0 if r["fill"] == fills["Mendocino"] else 1))


SLIDES = [
    # 1 -- COVER: the Anderson Valley hillside. Title over the vine canopy (white measured 6.6:1 against the median
    # background, 3.0:1 against the brightest leaves -- the 3:1 large-type minimum at 300px); kicker on a cream chip
    # over the sky, 45% (ink text measured 9.4:1; dark green with gold reached only 4.0:1 at 80%).
    ("cover_bleed", dict(
        photo="us_mendo_av_hillside_murayama", photo_anchor=0.5, photo_zoom=1.0,
        kicker="THE FIELD GUIDE: MENDOCINO", kicker_size=96,
        kicker_chip=dict(color=(250, 246, 236), alpha=0.45, text=INK),
        title="The Fog Does\nthe Work", title_top=0.60,
        photo_credit=CRED_MURAYAMA,
    )),

    # 2 -- THE PLACE: every AVA in the county as its real shape (UC Davis), Anderson Valley picked out. D3 + CSW.
    ("region_map", dict(
        map=AVA_MAP, highlight="Anderson Valley",
        kicker="THE PLACE", headline="Twelve AVAs, One Famous Valley", map_h=1480,
        summary_lead="Mostly forest",
        summary="Of about one million hectares, 7,000 are vines (about 17,000 acres), confined largely to river "
                "valleys. Pine Mountain\u2013Cloverdale Peak is shared with Sonoma.",
        left_labels=["Covelo", "Dos Rios", "Eagle Peak", "Potter Valley", "Redwood Valley", "Comptche",
                     "Mendocino Ridge", "McDowell Valley", "Cole Ranch", "Anderson Valley", "Yorkville Highlands",
                     "Pine Mtn\u2013Cloverdale Pk"],
        direct_labels={},
        credit="AVA boundaries: UC Davis AVA Project (CC0) \u00b7 county: US Census \u00b7 the Mendocino AVA is not drawn",
    )),

    # 3 -- TWO CLIMATES: D3 (and the Potter Valley twist). Photos: Anderson Valley under cloud; an inland vineyard at Ukiah.
    ("duel", dict(
        photos=("us_mendo_av_esterlina_view_prater", "us_mendo_ukiah_vineyard_missvain"),
        labels=("Anderson Valley", "Ukiah, inland"),
        kicker="TWO CLIMATES", headline="Cool Coast, Warm Inland",
        standfirst="Distance from the Pacific decides what ripens, and altitude can flip it.",
        mode="table", col_heads=("Near the Pacific", "Further inland"),
        rows=[("Climate", "Cooler", "Warmer"),
              ("Example", "Anderson Valley", "Redwood Valley"),
              ("Reds", "Pinot Noir", "Zinfandel, Syrah, Petite Sirah, Cabernet Sauvignon"),
              ("Whites", "Chardonnay, Alsace-style aromatics", "Sauvignon Blanc and Riesling, at altitude (Potter Valley)")],
        photo_credit=f"{CRED_PRATER}; Missvain / Wikimedia Commons (CC BY 4.0)",
    )),

    # 4 -- THE APPELLATIONS: containment, from D3 (the six) and the AVA data/TTB (what sits outside).
    ("euler_nesting", dict(
        kicker="THE APPELLATIONS", headline="Six AVAs Inside One",
        standfirst="The Mendocino AVA starts at the Russian River headwaters and covers six AVAs, so a blend across them "
                   "can still say Mendocino. Covelo, Dos Rios and Comptche sit outside even the North Coast AVA.",
        circles=_euler(),
    )),

    # 5 -- THE FOG FUNNEL: Anderson Valley at its real shape and position, with its neighbors and the coast. D3.
    ("atlas", dict(
        kicker="ANDERSON VALLEY", headline="The Fog Funnel", map_h=MAP_H_ATLAS,
        outline=ZOOM["land"][0], outlines=ZOOM["land"][1:],
        regions=_atlas_regions(),
        cities=[(*ZOOM["towns"]["Boonville"], "Boonville"), (*ZOOM["towns"]["Philo"], "Philo", "left")],
        context=[(ZOOM["sea_label"][0] - 0.08, ZOOM["sea_label"][1], "Pacific Ocean")],
        inset=dict(outline=INSET["outline"], marker=INSET["marker"], label="CALIFORNIA"),
        legend=[("Northwest end", "About 4 miles from the Pacific. Cold air and fog funnel in along the Navarro River."),
                ("Southeast end", "Narrower and warmer, with less breeze and fog."),
                ("Day and night", "Warm days; cold evenings and mornings.")],
    )),

    # 6 -- BY THE NUMBERS: D3, plus the measured coast distance and geography.
    ("stat_wall", dict(
        kicker="BY THE NUMBERS", headline="Anderson Valley in Six Figures",
        standfirst="A small valley, and a wet one.",
        stats=[("1,000", "HECTARES\nPLANTED", "Just under: about 2,500 acres."),
               ("35\u201379", "INCHES OF RAIN\nA YEAR", "900\u20132,000 mm, mostly winter and spring."),
               ("30", "WINERIES", "Many with cellar doors for coast visitors."),
               ("4", "MILES TO\nTHE PACIFIC", "At the valley's northwest end."),
               ("2", "LEADING\nGRAPES", "Pinot Noir and Chardonnay, early ripening."),
               ("39\u00b0N", "LATITUDE", "About nine degrees south of Alsace.")],
    )),

    # 7 -- THE PINOT NOIR: D3. Photo: young vines on an Anderson Valley slope (Prater).
    ("hero_facts", dict(
        photo="us_mendo_av_slope_prater", anchor=0.55, hero_h=1340,
        photo_caption="Vines on an Anderson Valley slope", photo_credit=CRED_PRATER,
        kicker="THE GRAPE THAT MADE THE NAME", headline="The Pinot Noir",
        facts=[("Fresh red fruit", "Raspberry, cherry and plum."),
               ("Medium body", "With medium (+) acidity."),
               ("Site, clone, harvest", "The three things that move the style."),
               ("Good to outstanding", "Premium priced, some super-premium.")],
    )),

    # 8 -- THE OLD WORLD'S GRAPES, FURTHER SOUTH: latitudes (geography); D3 for the grapes and the cold Pacific.
    ("chart_stack", dict(
        chart=CHART,
        kicker="THE LATITUDE", headline="Old World Grapes, Further South",
        standfirst="Pinot Noir, Chardonnay and the Alsace whites ripen here eight to ten degrees nearer the equator "
                   "than at home. The cold Pacific makes up the difference.",
        bar_chart=dict(title="LATITUDE, DEGREES NORTH",
                       bars=[("Champagne", 49, "about 49\u00b0", "cool", False),
                             ("Alsace", 48, "about 48\u00b0", "cool", False),
                             ("Burgundy", 47, "about 47\u00b0", "cool", False),
                             ("Anderson Valley", 39, "about 39\u00b0", "focus", True)]),
    )),

    # 9 -- IN THE VALLEY: three blades -- a detail, a row, a wide view. D3.
    ("blades", dict(
        blades=[dict(photo="us_mendo_roederer_flute_cc0", caption="Sparkling, Philo", anchor=0.55),
                dict(photo="us_mendo_husch_philo_cc0", caption="Gewurztraminer", anchor=0.5),
                dict(photo="us_mendo_fog_redwoods_pexels", caption="Coastal fog", anchor=0.5)],
        blade_h=1180,
        kicker="IN THE VALLEY", headline="Bubbles, Aromatics, Cellar Doors",
        items=[("Sparkling", "Pinot Noir and Chardonnay go into sparkling as well as still wine."),
               ("Alsace-style whites", "Gewurztraminer, Riesling, Pinot Gris and Pinot Blanc."),
               ("Cellar doors", "Thirty wineries, many open to visitors bound for the coast.")],
        photo_credit="Missvain, No-till-vineyard / Wikimedia Commons (CC0); Mick Haupt / Pexels",
    )),

    # 10 -- BEYOND THE VALLEY: D3 (Redwood Valley, Potter Valley); CSW (Mendocino Ridge, Cole Ranch).
    ("tile_grid", dict(
        kicker="BEYOND THE VALLEY", headline="Four More Names to Know",
        standfirst="Inland, the county runs warmer, and in places much higher.",
        tile_colors=[(TAN, SHADE), (SKY, SHADE), (SHADE, SKY), (VINE, PAPER)],
        tiles=[("Redwood Valley", "Inland warmth", "Ripens Zinfandel, Syrah, Petite Sirah and Cabernet Sauvignon."),
               ("Potter Valley", "Altitude flips it", "High enough for Sauvignon Blanc and Riesling."),
               ("Mendocino Ridge", "Islands in the sky", "Only land at 1,200 ft or higher counts."),
               ("Cole Ranch", "Smallest of all", "The smallest AVA in the United States.")],
    )),

    # 11 -- THE BUSINESS: D3, plus CSW's organic share (dated). Stripe: a Mendocino County vineyard.
    ("card_grid", dict(
        kicker="THE BUSINESS", headline="The Quiet Supplier",
        standfirst="Much of Mendocino's fruit leaves the county, one way or another.",
        row_layout=[2, 2],
        cards=[(None, "Priced below", "Napa and Sonoma", "Mendocino grapes generally sell for less."),
               (None, "Blended away", "Multi-regional", "Often blended with fruit from other regions."),
               (None, "Bought in", "By wineries elsewhere", "For Anderson Valley- or vineyard-named wines."),
               (None, "Grown organic", "A quarter, in 2018", "The largest certified-organic share in the US.")],
        bottom_stripe=["us_mendo_garzini_cc0"],
        stripe_captions=["Mendocino County", ""],
        photo_credit="No-till-vineyard / Wikimedia Commons (CC0)",
    )),

    # 12 -- CLOSE: CSW ("one of the coolest winegrowing areas of California"); D3 for the wines.
    ("statement", dict(
        variant="cover", photo="us_mendo_av_vineyard_murayama", photo_anchor=0.45,
        title="One of California's\nCoolest Corners",
        subtitle="Fog-cooled Pinot Noir, sparkling and Alsace-style whites, a few miles from the Pacific.",
        photo_credit=CRED_MURAYAMA,
    )),
]


def build():
    variety.report([name for name, _ in SLIDES])
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)
    paths = []
    total = len(SLIDES)
    for i, (name, slot) in enumerate(SLIDES, start=1):
        img = modules.MODULES[name](slot, i, total, PAL)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d} {name}")
    core.assemble_pdf(paths, f"{OUT}/FG_Mendocino_review.pdf")
    print("PDF:", f"{OUT}/FG_Mendocino_review.pdf")


if __name__ == "__main__":
    build()
