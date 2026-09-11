"""FIELD GUIDE — The Northern Rhône. "Seven Crus, One Grape"

Arc 1 pillar post, Tue 8 September. Spec: FG_NORTHERN_RHONE_SPEC.md.
Every factual claim is from D3 Ch. 7 unless marked; the three claims the
spec flagged unsourced (Viognier 1960s hectarage, Syrah parentage,
Hermitage/first-growth price parity) do not appear anywhere in this file.

Map geometry: INAO parcellaire (Licence Ouverte), cadastral-parcel
delimitation dissolved per appellation with Shapely — see
build_nrhone_geo.py. River after Natural Earth. Locator after the French
departmental boundaries, marker point-in-polygon verified. Nothing traced
from published cartography.

Photos: Wikimedia Commons, category-sourced so location is human-verified,
credited per slide. No caption makes a location claim the file's own
Commons metadata does not support.

Social pass (SOCIAL_PASS_STYLE_GUIDE.md, eight gates):
  1 decode layer ..... slide 11 (the third photo is Château-Grillet's own
                       house, uncaptioned and unnamed on a slide about
                       cellar chemistry — findable by anyone who knows the
                       estate, invisible to everyone else)
                       NOTE: the spec put the decode layer on slide 3, as
                       Château-Grillet drawn gold inside Condrieu. It is
                       drawn, and it is real, but at 3.5 ha on a map
                       spanning 74 km it renders about four pixels wide
                       and is indistinguishable from Condrieu's own gold
                       beside it. A decode layer nobody can decode is a
                       fake easter egg, which the style guide rates worse
                       than none — so it moved.
  2 save asset ....... slide 10 (the other five, size + yield + the one thing)
  3 send line ........ slide 3 ("six per cent")
  4 open question .... slide 12 (should Saint-Joseph shrink back?)
  5 callback ......... slide 7 (Côte de Nuits, mid-slope band)
  6 cover hook ....... slide 1 (the 70 ha collapse, region unnamed)
  7 search surface ... caption, drafted separately
  8 second beat ...... Saturday's Split Decision resolves slide 9
"""
import glob, json, os

import core
import modules
from map_atlas import regional_atlas

OUT = "/home/claude/out_northern_rhone"
os.makedirs(OUT, exist_ok=True)

# ── Palette ────────────────────────────────────────────────────────────
# Syrah-black-fruit signature: a cool, near-black purple-red, deliberately
# nothing like the Côte de Nuits oxblood so the two arcs do not read as one
# body of work in the grid. LEAD is set explicitly, never left to fall back
# to SIGNATURE (v8 standing rule).
PAL = dict(
    SIGNATURE=(58, 26, 46),        # deep Syrah purple-black
    ACCENT=(186, 149, 74),         # brass
    LEAD=(126, 54, 66),            # warm plum run-in
    MARK=(58, 26, 46),
)

GEO = json.load(open("/home/claude/styleguide/geo/nrhone_geo.json"))
LOC = json.load(open("/home/claude/styleguide/geo/nrhone_locator.json"))

# ── Photo credits ──────────────────────────────────────────────────────
CRED_KAREN = "Karen / Wikimedia Commons (CC BY 2.0)"
CRED_LEMOINE = "Olivier Lemoine / Wikimedia Commons (CC BY-SA 4.0)"
CRED_CULSAN = "Daniel CULSAN / Wikimedia Commons (CC BY-SA 3.0)"
CRED_VALENCE = "Médiathèques Valence Romans Agglo / Wikimedia Commons"
CRED_ROSIERE = "Vive la Rosière / Wikimedia Commons (CC BY-SA 3.0)"
CRED_GOUDAN = "Goudan07 / Wikimedia Commons (CC BY-SA 3.0)"
CRED_PHILDIC = "PHILDIC / Wikimedia Commons (CC0)"

# ── Map colour logic ───────────────────────────────────────────────────
# Colour by grape, not arbitrarily. Six reds in the arc signature, the
# three whites in brass. At thumbnail size the map should teach "one
# grape, three exceptions" before a single label is read.
RED = (108, 44, 62)
WHITE_WINE = (198, 162, 84)
WHITES = {"Condrieu", "Château-Grillet", "Saint-Péray"}


def _regions():
    """Painter's order matters here — these appellations overlap on the
    ground. Saint-Joseph's delimited slopes carry Condrieu for white;
    Hermitage sits inside Crozes-Hermitage's envelope. Drawn north to
    south, the later reds bury the three shapes the slide exists to
    show, so GEO["draw"] puts the broad reds down first and the whites
    last."""
    out = []
    for name in GEO["draw"]:
        color = WHITE_WINE if name in WHITES else RED
        for ring in GEO["regions"][name]:
            out.append((name, ring, color))
    return out


# Only the crus with room for a label beside their own latitude get one.
# Château-Grillet is deliberately unlabelled: it is the decode layer, and
# at 4 ha it would need a leader line longer than the shape is wide.
MAP_LABELS = ["Côte-Rôtie", "Condrieu", "Saint-Joseph", "Crozes-Hermitage",
              "Hermitage", "Cornas", "Saint-Péray"]


SLIDES = [

    # ── 1 · COVER — hook is the collapse, region unnamed ───────────────
    ("statement", dict(
        variant="cover",
        cover_layout="sky",
        kicker="THE FIELD GUIDE: NORTHERN RHÔNE",
        photo="nr_cover_coterotie",
        photo_anchor=0.62,
        photo_zoom=1.10,
        title="In 1971 This Slope\nWas Nearly Abandoned",
        title_size=168,
        title_color=(255, 255, 255),
        subtitle="Seventy hectares left. Now one of the\nmost expensive addresses in France.",
        subtitle_size=104,
        subtitle_color=(244, 214, 140),
        photo_credit=CRED_KAREN,
    )),

    # ── 2 · THE MAP — real parcellaire ────────────────────────────────
    ("regional_atlas", dict(
        kicker="THE SEVEN CRUS",
        headline="North to South, Along One River",
        map_h=1540,
        main_label_size=44,
        main=dict(
            aspect=GEO["aspect"],
            outline_smooth=3,
            regions=_regions(),
            rivers={"Rhône": GEO["rivers"]["Rhône"]},
            river_width=9,
            # Two cities, both at the extremes. Tain-l'Hermitage was the
            # third and had to go: it sits at the same latitude as the
            # Hermitage, Crozes-Hermitage and Cornas labels, and a city
            # label is a fixed obstacle the packer cannot move, so it
            # collided with all three at once. The Hermitage label names
            # the same spot anyway.
            cities={k: tuple(v) for k, v in GEO["towns"].items()
                    if k in ("Vienne", "Valence")},
            labels=[(n, tuple(GEO["anchors"][n])) for n in MAP_LABELS],
            # Side follows the bank. The southern four sit within a few
            # km of each other's latitude, so letting the packer choose
            # stacked all of them into one column and blew the leader
            # lines across the map.
            forced_side={"Côte-Rôtie": "left", "Condrieu": "left",
                         "Saint-Joseph": "left", "Cornas": "left",
                         "Crozes-Hermitage": "right", "Hermitage": "right",
                         "Saint-Péray": "right"},
            label_column_x=0.68,
            max_label_w=500,
        ),
        inset=dict(
            aspect=LOC["aspect"],
            outline=LOC["outline"],
            outline_smooth=2,
            regions=[("Northern Rhône", LOC["region"], (198, 162, 84))],
            cities={"": tuple(LOC["marker"])},
            labels=[],
        ),
        inset_title="FRANCE",
        inset_w=400,
        inset_map_w=330,
        # Top-right. The map is a 550px ribbon in a 1920px box, so the
        # default position lands the inset on Cornas and Saint-Péray —
        # two of the three shapes this slide exists for. Moving it into
        # the right gutter at mid-height then collided with the Hermitage
        # and Crozes-Hermitage labels: obstacle avoidance pushed both up
        # by the same amount and stacked them on each other. The whole
        # upper right is empty (every northern label is on the left bank
        # side), so the inset goes there and clashes with nothing.
        inset_x_frac=0.76,
        inset_y_frac=0.02,
        # "SYRAH" alone said the red appellations are Syrah
        # appellations. They are not — Hermitage is a third white,
        # Crozes whites are 9% of production, Saint-Joseph is "nearly
        # 90 per cent red". Slide 8 states the Hermitage figure
        # outright, so the old legend contradicted the deck six
        # slides later. "RED — SYRAH" is what the fill actually means.
        legend=[(RED, "RED — SYRAH"), (WHITE_WINE, "WHITE ONLY")],
        legend_size=46,
        # NOT "bigger than every other cru combined" — that was wrong.
        # Crozes is 1,700 ha planted; Saint-Joseph alone is well over a
        # thousand, so the others together clear Crozes comfortably.
        description="Côte-Rôtie and Hermitage are the two great names — 250 and 137 "
                    "hectares. Crozes-Hermitage, the largest at 1,700, wraps around "
                    "Hermitage on the same bank. Condrieu and Saint-Péray make no red; "
                    "Cornas permits no white.",
        description_body_size=58,
        description_bold_words=["Côte-Rôtie", "Hermitage", "Crozes-Hermitage",
                                "Condrieu", "Saint-Péray", "Cornas"],
        description_bold_color=(108, 44, 62),
    )),

    # ── 3 · SEND LINE — the scale ─────────────────────────────────────
    ("stat_wall", dict(
        kicker="NORTH VS SOUTH",
        headline="Six Per Cent",
        standfirst="Two wine regions, 50 km apart, with almost nothing in common. "
                   "The famous half is the small one.",
        standfirst_leading=1.04,
        stats=[
            ("6%", "of the Rhône's AOC\nproduction", "the northern crus, by volume, 2021"),
            ("49%", "is Côtes du Rhône", "that one appellation, by volume"),
            ("4,200 ha", "in the north", "steep granite, worked by hand"),
            ("65,000 ha", "in the south", "blends built on Grenache Noir"),
            ("50 km", "of near-empty valley", "separates the two"),
            ("7", "crus in the north", "one black grape runs through six of them"),
        ],
    )),

    # ── 4 · THE MISTRAL ───────────────────────────────────────────────
    ("side_rail", dict(
        photo="nr_echalas",
        side="right",
        photo_caption="A vine tied in to its échalas",
        photo_credit=CRED_LEMOINE,
        kicker="THE MISTRAL",
        headline="Better Wine,\nWorse Business",
        standfirst="A cold, dry northerly that funnels down the Rhône corridor, sometimes "
                   "for days. Everything it does for quality, it does by taking volume away.",
        items=[
            ("What it gives", "Dry air suppresses fungal disease. A vine under wind stress "
                              "runs lower vigour — smaller crop, more concentrated fruit."),
            ("What it costs", "Lower yields are lower yields. Less wine to sell."),
            ("What it forces", "No wire trellis on the steepest terraces. Vines are tied to "
                               "poles — échalas — and worked entirely by hand."),
        ],
    )),

    # ── 5 · SYRAH, ALONE ──────────────────────────────────────────────
    ("duel", dict(
        photos=("nr_harvest_hands", "nr_syrah_bunch"),
        labels=("PICKED BY HAND", "SYRAH"),
        photo_credit="Nico Becker / Pexels · Chrisada Sookdhis / Wikimedia Commons (CC BY 2.0)",
        photo_position="bottom",
        kicker="SYRAH, THE ONLY BLACK GRAPE",
        headline="Seven Appellations, No Second Opinion",
        standfirst="The only black variety permitted in the northern crus. Everything "
                   "that varies here is site, not variety.",
        standfirst_leading=1.04,
        mode="columns",
        cols=[
            ("IN THE GLASS",
             "Violet, plum, blackberry, black pepper. Acidity and tannin both medium to "
             "high. Red plum in cooler sites, black in warmer — the same grape reporting "
             "its site back to you."),
            ("IN THE VINEYARD",
             "Vigorous, and needs tying in against the wind. Prone to mites and botrytis. "
             "And to Syrah decline: leaves redden, the graft union breaks up, the vine "
             "dies."),
        ],
    )),

    # ── 6 · THE 20% NOBODY USES ───────────────────────────────────────
    ("fact_file", dict(
        photo="nr_echalas_condrieu",
        photo_anchor=0.45,
        photo_caption="Échalas-trained vines in Condrieu",
        photo_credit=CRED_LEMOINE,
        kicker="CO-FERMENTATION",
        headline="The Rule That Mostly Goes Unused",
        facts=[
            ("Côte-Rôtie", "Up to 20% Viognier permitted in the red"),
            ("In practice", "Often zero, and normally no more than 8%"),
            ("The condition", "The two must be co-fermented, not blended afterwards"),
            ("Why bother", "Viognier contributes floral lift and fruit"),
            ("Elsewhere", "Marsanne and Roussanne, in small proportions, rarely used"),
            ("Nowhere", "Cornas permits no white grape at all"),
        ],
    )),

    # ── 7 · CÔTE-RÔTIE — callback to the Côte de Nuits ────────────────
    ("side_rail", dict(
        photo="nr_coterotie_chaillees",
        side="left",
        photo_caption="Chaillées, long abandoned",
        photo_credit=CRED_LEMOINE,
        kicker="CÔTE-RÔTIE",
        headline="250 Hectares,\nBack From 70",
        standfirst="Commercial interest had collapsed and the work was punishing. What "
                   "revived it happened outside the vineyard.",
        items=[
            ("The revival", "Guigal's single-vineyard bottlings — La Mouline, then La "
                            "Landonne — and the scores Parker gave them."),
            ("The site", "East and south-east terraces. 10,000 vines per hectare, 40 hL/ha."),
            ("Sound familiar", "As in the Côte de Nuits, the best of it sits in a band on "
                               "the slope. Here the terraces are built, not found."),
        ],
    )),

    # ── 8 · HERMITAGE ─────────────────────────────────────────────────
    ("side_rail", dict(
        photo="nr_hermitage_hill",
        # The source is a period print with its own engraved caption
        # along the bottom plate. Anchored low it sat directly behind our
        # caption; anchor high and zoom past it so only the hill is in
        # frame.
        photo_anchor=0.16,
        photo_zoom=1.55,
        side="right",
        photo_caption="The hill, named for a crusader turned hermit",
        photo_credit=CRED_VALENCE,
        kicker="HERMITAGE",
        headline="137 Hectares,\nOne Hill",
        standfirst="A south-facing slope on the left bank above Tain. Virtually all of it "
                   "is planted, and a third of that is white.",
        items=[
            ("The ground", "Thin stony soils, hot and dry. Pronounced intensity, high "
                           "tannin, longevity. Le Méal runs the hottest."),
            ("The split", "Chapoutier works parcels separately. Chave blends across the "
                          "whole appellation. The co-op owns 15%."),
            ("The rarity", "In very ripe years, a Vin de Paille."),
        ],
    )),

    # ── 9 · SETS UP SATURDAY, DOES NOT RESOLVE ────────────────────────
    ("duel", dict(
        photos=("nr_ampuis_parcelles", "nr_chapoutier_vy"),
        labels=("Côte-Rôtie", "Hermitage"),
        photo_credit=f"{CRED_CULSAN} · {CRED_ROSIERE}",
        kicker="TWO HILLS",
        headline="Aromatics or Structure",
        standfirst="Both Syrah, both steep, and not making the same argument. The north "
                   "has never settled it.",
        standfirst_leading=1.04,
        mode="table",
        col_heads=("Côte-Rôtie", "Hermitage"),
        rows=[
            ("Size", "250 ha", "137 ha"),
            ("The slope", "Terraces, built by hand", "One hill, south-facing"),
            ("Reputation", "Perfume, lift, finesse", "Structure, tannin"),
            # "In the red" and "White wine" were split apart during the
            # Wintour pass because the old single row compared unlike
            # things. At the larger body size five rows no longer fit, so
            # the two halves are recombined — but LABELLED, so the
            # distinction that split them survives.
            ("White grapes", "20% Viognier in the red",
                             "A third of the AOC is white"),
        ],
    )),

    # ── 10 · SAVE ASSET — the other five ──────────────────────────────
    ("card_grid", dict(
        kicker="THE OTHER FIVE",
        headline="Everything Else on the River",
        standfirst="Six entries, not five — Château-Grillet is an estate that is also an "
                   "appellation of its own.",
        standfirst_leading=1.04,
        row_layout=[2, 2, 2],
        row_even=True,
        body_leading=1.12,
        row_gap=52,
        col_gap=130,
        card_border=True,
        cards=[
            (None, "Condrieu", "197 HA · 41 hL/ha",
             "100% Viognier, and the world's reference point for the grape."),
            (None, "Château-Grillet", "3.5 HA",
             "A single estate that is also an appellation, enclosed by Condrieu."),
            (None, "Saint-Joseph", "50 KM LONG · 40 hL/ha",
             "Extended in 1994, and now arguing about shrinking back to the slopes."),
            (None, "Crozes-Hermitage", "1,700 HA · 45 hL/ha",
             "Deeper, more fertile soils than the hill it wraps around, and lower "
             "concentration for it."),
            (None, "Cornas", "145 HA · 40 hL/ha",
             "A south-facing amphitheatre. Usually the first Syrah picked in the north."),
            (None, "Saint-Péray", "45 hL/ha",
             "Whites only, Marsanne-dominant, grown on limestone and granite."),
        ],
    )),

    # ── 11 · CELLAR LOGIC ─────────────────────────────────────────────
    ("process_map", dict(
        photos=("nr_grillet", "nr_cellar_foudre", "nr_cellar_pour"),
        photo_credit=f"{CRED_PHILDIC} · {CRED_LEMOINE} · Rachel Claire / Pexels",
        show_numbers=False,
        kicker="IN THE CELLAR",
        headline="Syrah Reduces, Grenache Oxidises",
        columns=[
            ("THE PROBLEM", [
                ("Syrah is prone to reduction", False),
                ("So it is pumped over more often", False),
                ("And aged in oak for gentle oxygenation", False),
                ("Which costs money", False),
            ]),
            ("THE CRU RED", [
                ("Hand-harvested into small crates", False),
                # Was a decision diamond. It was the only shape variation
                # in the deck, and being a different height from the
                # rectangles it knocked the middle column out of
                # alignment with its neighbours from row two down. The
                # question survives as a question; the grid holds.
                ("Whole bunch, or destemmed?", False),
                ("Warm ferment, 20–30 day maceration", False),
                ("12–24 months in small barrels, typically 20–30% new", False),
            ]),
            ("THE CONTRAST", [
                ("Grenache has the opposite fault", False),
                ("Prone to oxidation, not reduction", False),
                ("So: concrete and steel, not barrel", False),
            ]),
        ],
    )),

    # ── 12 · CLOSING — open question ──────────────────────────────────
    ("statement", dict(
        variant="closing",
        photo="nr_condrieu_pano",
        photo_anchor=0.5,
        # No Saint-Joseph photograph exists on Commons — the AOC category
        # holds no files under any spelling, and the commune categories
        # are empty too. Rather than leave a river view sitting silently
        # under a Saint-Joseph question and let it read as Saint-Joseph,
        # the caption names the place it actually is. The river is the
        # connection the slide needs; the appellation runs 50 km of it.
        photo_caption="The Rhône at Condrieu",
        title="Should Saint-Joseph\nShrink Back?",
        subtitle="Extended in 1994, it now runs 50 km. Pull it back to the "
                 "hillsides — or leave thirty years of growers alone?",
        subtitle_size=64,
        photo_credit=CRED_GOUDAN,
    )),
]


def build():
    # Clear stale renders first. Filenames encode both position and
    # module ("03_stat_wall.png"), so reordering slides leaves the old
    # names behind -- after the 2/3 swap the directory held both
    # 02_regional_atlas and 02_stat_wall. The PDF is built from the
    # returned path list so it stayed correct, but anything that globs
    # this directory (a lock ZIP, a contact sheet) would silently pick
    # up a slide that is no longer in the deck.
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    reg = dict(modules.MODULES)
    reg["regional_atlas"] = regional_atlas
    paths = []
    total = len(SLIDES)
    for i, (name, slot) in enumerate(SLIDES, start=1):
        fn = reg.get(name) or getattr(modules, name)
        img = fn(slot, i, total, PAL)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  {name}")
    pdf = f"{OUT}/FG_NorthernRhone_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
