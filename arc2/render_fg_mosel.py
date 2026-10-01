"""FIELD GUIDE — The Mosel. "Ripeness Was the Law"

REBUILT after a container reset wiped the original local-only build
(never pushed to GitHub -- see the recovery conversation for the full
account). This version is built from specs/FG_MOSEL_SPEC.md, a
complete 12-slide spec that the first build never found and had to
crudely reconstruct from the arc plan and caption alone. The spec is
followed closely; deviations are noted at each slide, and are almost
all about matching real content to the modules actually available in
engine/modules.py (a few module names in the spec, e.g. "spectrum",
don't exist -- editorial_lead substitutes throughout, since it
supports the same photo + kicker + headline + standfirst + items shape
every substituted slide needs).

Separately, Steve provided a detailed article on Germany's 2026 origin-
law reform and asked that the deck reflect it. This turned out to be
less of a bolt-on than expected: the spec's OWN slide 12 already
anticipated the reform in outline ("Grosslage is gone, replaced by
Region"), written before the June 2026 Bundesrat session that actually
implemented it. This version updates slide 12 with that session's
specifics (12 June 2026, the Komitee, classification still in
progress) verified independently against multiple sources (Deutsches
Weininstitut, Jancis Robinson, Wine Scholar Guild) before being written
in, and carries the same "Region, not Grosslage" correction into slide
10, which is where the deck actually explains the naming problem the
reform fixes.

Per Steve's design feedback the deck went through several review rounds
and became the system's visual benchmark (guides/VISUAL_BENCHMARK_v10.md,
tag fg-mosel-final). The cover is a full-bleed treatment (cover_bleed,
M19) rather than the spec's original grid_cover (a 9-photo grid this
project has no material for), and slide 3 is a map of all 13 Anbaugebiete
as real traced shapes (region_map, M20), replacing the first build's
zoomed Mosel map with a village list. The layouts live in
engine/modules.py; this file holds only the Mosel's data, palette, slide
order and copy.

SOURCES: every claim traces to D3 Ch. 11, per the spec's own header,
except where the spec itself flags a gap (Mosel hectarage, the export
price in currency, the Sonnenuhr sundials, Scharzhofberg as a village-
prefix exception, "Mosel-Saar-Ruwer" as a former name -- none of these
appear here) and except the 2026 reform content, sourced and dated as
described above and in each affected slide's own comment.

PHOTOGRAPHY remains a real, disclosed constraint: three photos exist
for this arc (de_hatzenport_mosel.jpg, de_bernkastel_castle_view.jpg,
de_piesport_goldtropfchen_sign.jpg), reused across every slide that
needs a photo band. See MAP module's own docstring for the map's
sourcing; the spec's suggested 9-photo cover grid and per-slide photo
suggestions (budburst, a Fuder cask, a winch rail) were never
achievable with this library and are not attempted.
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "engine"))
import core
import modules
import variety
import prepare_map_data as pmd

OUT = "/home/claude/out_fg_mosel"
os.makedirs(OUT, exist_ok=True)

PAL = dict(
    SIGNATURE=(45, 58, 74),   # Mosel slate-blue
    ACCENT=(196, 158, 84),    # house gold, locked across every arc
    LEAD=(140, 95, 58),       # warm sienna run-in, distinct from both
    MARK=(45, 58, 74),
)

CRED_HATZENPORT = "Rolf Kranz / Wikimedia Commons (CC BY-SA 4.0)"
CRED_BERNKASTEL = "Roger W / Wikimedia Commons (CC BY-SA 2.0)"
CRED_PIESPORT = "J\u00e1nos Korom Dr. / Wikimedia Commons (CC BY-SA 2.0)"

MAP = pmd.build_main_map()
INSET = pmd.build_locator_inset()

# The layouts used below (cover_bleed, region_map, blades, stair_ladder,
# chart_stack, rail_rings, hero_facts, tile_grid) began as deck-local
# renderers in this file and now live in engine/modules.py as M19-M26,
# promoted unchanged in output once this deck became the system's visual
# benchmark (guides/VISUAL_BENCHMARK_v10.md). This file now holds only
# what is specific to the Mosel: its data, palette, slide order and copy.
# cover_bleed exists because statement()'s "cover" variant isn't
# full-bleed (a hard colour block under the photo) and the spec's
# grid_cover needs nine photos this project doesn't have.

# Slide 3's national region shapes: real traced data, see prepare_map_data.
REGIONS13 = pmd.build_anbaugebiete_map()


# Chart palette. Round 3 first made the charts vivid (Steve: "more
# color"); round 3b re-based them on the cover photo (Steve: "match the
# colors in the cover photo"). Every colour below is sampled from the
# cover's own crop by sample_cover_palette.py -- the most saturated,
# mid-light pixels of a named feature -- not picked by eye:
#   vineyard gold (sunlit slope under the castle)   (201, 151, 3)
#   leaf yellow   (autumn leaves)                   (171, 142, 3)
#   lamp orange   (lamp reflections in the river)   (242, 145, 4)
#   window orange (lit windows along the quay)      (203, 114, 12)
#   brick red     (roofs)                           (179, 80, 63)
#   forest green  (the hillside)                    (50, 62, 25)
#   water teal    (the river, in shade)             (18, 32, 30)
#   sky           (top of frame)                    (225, 244, 248)
# Two values are NOT single-feature samples: `stone` is the cover's
# warm stone/plaster grey, taken from the 5th-largest k-means cluster of
# the whole crop (98, 91, 74), and `track` its pale sibling (203, 194,
# 165), another cluster. The ripeness ramp runs forest -> gold -> orange
# -> deep orange -> brick, i.e. the cover's own greens, golds and
# russets in the order grapes move through them.
CHART = dict(
    ripe=[(50, 62, 25), (201, 151, 3), (242, 145, 4), (203, 114, 12), (179, 80, 63)],
    focus=(18, 32, 30),        # water: the highlighted subject ("this is the Mosel")
    amber=(242, 145, 4),       # lamp orange
    gold=(201, 151, 3),        # vineyard gold
    grape=(171, 142, 3),       # leaf yellow: white-grape share
    stone=(98, 91, 74),
    ice=(18, 32, 30),          # Eiswein outline/connector/title: water teal
    ice_fill=(225, 244, 248),  # Eiswein box fill: the cover's sky
    ice_text=(18, 32, 30),
    track=(203, 194, 165),
)


SLIDES = [

    # ── 1 · COVER ──────────────────────────────────────────────────
    ("cover_bleed", dict(
        photo="de_cochem_mosel",
        # zoom + low anchor: the source is landscape, so without a zoom
        # there's no vertical slack to move; this brings more of the
        # dark river into frame so the whole title can sit on water.
        photo_anchor=0.80,
        photo_zoom=1.12,
        kicker="THE FIELD GUIDE: THE MOSEL",
        # Round 3: larger (68 -> 104pt). Round 4: back at the upper left on
        # a chip. Steve chose the dark chip with the gold text over the
        # cream chip with dark text (both were rendered and compared).
        # Measured over the real cover pixels behind it, the dark chip
        # only works dense: a translucent dark chip at 25-55% makes gold
        # text WORSE (it tints the pale sky to a mid-tone as bright as
        # the gold; contrast bottoms at 1.0:1), and gets to 3.07:1 at
        # 75%, 3.64:1 at 80% (this setting), 4.30:1 at 85%. 3:1 is the
        # large-text minimum and this is 104pt type. Chip colour is the
        # cover's own water teal. The cream-chip alternative, if ever
        # wanted: kicker_chip=dict(color=(250, 246, 236), alpha=0.45,
        # text=CHART["focus"]) -- 5.7:1 worst case.
        kicker_size=104,
        kicker_chip=dict(color=CHART["focus"], alpha=0.80, text=PAL["ACCENT"]),
        title="Ripeness is\nEverything",
        title_top=0.655,  # round 2: lowered fully into the dark water of the river
        photo_credit="Philipp / Unsplash",
    )),

    # ── 2 · TWO GERMANYS ─────────────────────────────────────────────
    # Round 2: single-line headline (was a 2-line "The Same Country /
    # Sold Both of These"); the reclaimed line goes back as white space
    # between the standfirst and the items and between each item.
    ("editorial_lead", dict(
        # Round 3: replaced the old Bernkastel photo, a scan of an aged
        # film slide with a heavy cyan cast (mean blue exceeded red by
        # ~97 levels; saturation ~2x a normal photo). This one measures
        # neutral and is ~6x the resolution.
        photo="de_bernkastel_aerial",
        photo_caption="The Mosel at Bernkastel",
        photo_credit="sajid shiper / Pexels",
        kicker="THE REPUTATION PROBLEM",
        headline="Two Germanys",
        standfirst="Germany is the world's largest producer of Riesling, "
                   "and the country most people still associate with "
                   "sugared brand wine. Both are true.",
        standfirst_gap=110,
        item_gap=110,
        items=[
            ("Riesling", "Nearly a quarter of German plantings -- close "
                          "to 40% of the world's Riesling vineyard area."),
            ("Liebfraumilch", "By the 1980s, roughly 60% of all German "
                               "wine exports, under brands like Black "
                               "Tower and Blue Nun."),
            ("The fall, and the fix", "Export volume has nearly halved "
                                       "since, while price per hectolitre "
                                       "has risen by about half again."),
        ],
    )),

    # ── 3 · THE MAP ──────────────────────────────────────────────────
    # Round 2: a standard wine-region map of all 13 Anbaugebiete (real
    # traced shapes, georeferenced -- see render_region_map()), and the
    # text is now a summary of what makes the Mosel special rather than
    # a caption for the village map this slide used to carry. Every
    # clause traces to D3 Ch. 11 via the spec's slides 4 and 8.
    ("region_map", dict(
        map=REGIONS13,
        highlight="Mosel",
        kicker="THE PLACE",
        headline="Thirteen Regions. One Mosel.",
        map_h=1590,
        summary_lead="Why it stands apart",
        summary="Riesling on slopes up to 70%, above a looping river at "
                "50\u00b0N. Slate stores the day's heat, and the wines come "
                "out paler, lighter and higher in acid than any other "
                "German Riesling.",
        left_labels=["Ahr", "Mittelrhein", "Mosel", "Rheingau", "Nahe",
                     "Rheinhessen", "Hessische Bergstra\u00dfe", "Pfalz", "Baden"],
        direct_labels={"Saale-Unstrut": (-190, -95), "Sachsen": (20, 18),
                       "Franken": (30, -80), "W\u00fcrttemberg": (40, 10)},
        credit="Region shapes after Wikimedia Commons, CC BY-SA 3.0",
    )),

    # ── 4 · WHY ANYONE FARMS A CLIFF ──────────────────────────────────
    # Round 2: four cards, one per corrective, instead of a photo band +
    # run-in list; single-line headline.
    ("tile_grid", dict(
        kicker="THE SLOPE",
        # (fill, accent for numeral + sub-line), in tile order
        tile_colors=[(CHART["focus"], CHART["gold"]),       # The River: the water
                     (CHART["gold"], CHART["focus"]),         # The Aspect: sunlit vineyard (water-teal accent; brick measured 1.9:1)
                     (CHART["stone"], CHART["track"]),       # The Slate: the cover's stone (plaster-cream accent; amber measured 2.8:1)
                     (CHART["ripe"][3], (50, 22, 8))],       # The Autumn: window orange
        headline="Four Fixes for Latitude",
        standfirst="The Mosel sits near 50\u00b0N, far enough north that "
                   "ripening Riesling takes help from the land.",
        tiles=[
            ("The River", "Warmth by reflection",
             "Radiates heat, moderates temperature and stretches the "
             "growing season."),
            ("The Aspect", "Face the sun",
             "The best sites are steep and south-facing -- gradients "
             "reach 70%."),
            ("The Slate", "A storage heater",
             "Dark rock takes heat in by day and gives it back at night."),
            ("The Autumn", "Time on the vine",
             "Long and dry, which lets sugar keep building before "
             "harvest."),
        ],
    )),

    # ── 5 · THE COST OF THE CORRECTION ────────────────────────────────
    # Round 2: vertical blade layout; photos of people working steep
    # slopes. The two worker photos carry no location data (Pexels has
    # none), so their captions describe the work, not a place; only the
    # Bremm blade names a location, per its photographer's own title.
    ("blades", dict(
        blades=[
            dict(photo="de_steep_stairs_climber", caption="Stairs, not rows", anchor=0.45),
            dict(photo="de_harvest_pickers_slope", caption="Picked by hand", anchor=0.40),
            dict(photo="de_bremm_mosel_loop", caption="The Mosel at Bremm", anchor=0.5, zoom=1.0),
        ],
        blade_h=1180,
        kicker="THE LABOR",
        headline="The Price of a Cliff",
        items=[
            ("Erosion", "Constant enough that winching soil back up the "
                         "slope is routine maintenance, not an emergency."),
            ("Spraying", "Often only practicable by helicopter -- which "
                          "also makes organic certification hard."),
            ("The blunt version", "On these slopes, often only Riesling "
                                   "commands a price that makes the "
                                   "farming pay."),
        ],
        photo_credit="Peter Dyllong, Nico Becker, tom analogicus / Pexels",
    )),

    # ── 6 · THE LADDER ───────────────────────────────────────────────
    # Round 2: numbered, lowest ripeness at the bottom of the page.
    ("stair_ladder", dict(
        chart=CHART,
        kicker="THE RIPENESS LADDER",
        headline="Five Rungs. None Means Sweet.",
        standfirst="Pr\u00e4dikat levels climb by must weight -- sugar in the "
                   "grape at harvest, not sugar in the bottle.",
        rungs=[
            ("Kabinett", "Lightest, highest in acid. Dry to medium-sweet."),
            ("Sp\u00e4tlese", "\"Late picked\" -- riper, fuller."),
            ("Auslese", "Extra-ripe bunches. The last level that can "
                        "still be dry."),
            ("Beerenauslese", "Selected berries. Always sweet."),
            ("TBA", "Shrivelled, botrytised berries. Germany's rarest."),
        ],
        side_note=dict(beside=3, title="Eiswein",
                       note="Same must weight as BA -- but frozen on the "
                            "vine. A parallel track, not a rung."),
    )),

    # ── 7 · DRY IS A MEASUREMENT ─────────────────────────────────────
    # Round 2: two data graphics replace the run-in list.
    ("chart_stack", dict(
        chart=CHART,
        kicker="THE WORD ON THE LABEL",
        headline="Dry Is a Measurement",
        standfirst="Below Beerenauslese, any Pr\u00e4dikat can be made at "
                   "any sweetness. The label terms are numbers.",
        # Every number is from D3 Ch. 11. Germany's share is drawn at 49%
        # and labelled with the chapter's own words ("just under half"),
        # not a precise figure the chapter doesn't give.
        band_chart=dict(
            title="RESIDUAL SUGAR, GRAMS PER LITRE",
            axis_max=20, ticks=[0, 4, 9, 12, 18],
            rows=[("trocken", "focus", 0, 4, 9),
                  ("halbtrocken", "amber", 4, 12, 18)],
            legend=("base limit", "allowed only if sugar doesn't outrun acid"),
        ),
        bar_chart=dict(
            title="SHARE OF WINE LABELLED TROCKEN, 2021",
            bars=[("Baden", 64, "64%", "amber", False),
                  ("Germany", 49, "Just under half", "gold", False),
                  ("Mosel", 26, "26%", "focus", True)],
        ),
    )),

    # ── 8 · THE MOSEL ─────────────────────────────────────────────────
    # Round 2: ring-chart graphic added (91% white, 62% Riesling).
    ("rail_rings", dict(
        chart=CHART,
        photo="de_hatzenport_mosel",
        anchor=0.5,
        photo_caption="The Mosel at Hatzenport",
        photo_credit="Rolf Kranz / Commons, CC BY-SA 4.0",
        kicker="THE MAIN VALLEY",
        headline="Pale, Light,\nBuilt to\nOutlive You",
        rings=[(91, "WHITE GRAPES", "grape"), (62, "RIESLING", "amber")],
        items=[
            ("In the glass", "Paler, lighter, lower in alcohol and higher "
                              "in acid than German Riesling from anywhere "
                              "else."),
            ("Village first", "Bernkastel (Doctor), Piesport "
                               "(Goldtr\u00f6pfchen), \u00dcrzig "
                               "(W\u00fcrzgarten)."),
        ],
    )),


    # ── 9 · THE SAAR AND THE RUWER ─────────────────────────────────────
    # Round 3: new photo with people, per Steve (Febe Vanermen / Unsplash,
    # Unsplash location data: Bernkastel-Kues). Searched Pexels, Unsplash
    # and Commons for people in the Saar or Ruwer themselves first; the
    # real Saar/Ruwer photos found (Kanzem vineyards and cycle path,
    # the Scharzhofberg panorama, the Ruwer-Hochwald cycle path at Kasel)
    # had nobody in them. So this is honest Middle Mosel, captioned as
    # Bernkastel, not passed off as a tributary.
    # Layout moved from side_rail to a wide top band: side_rail centre-
    # crops a narrow 860px strip, and in this photo the vineyard slope is
    # on the left and the couple on the right -- no narrow slice holds
    # both. The wide band keeps them together and frees the headline to
    # run on one line.
    ("editorial_lead", dict(
        photo="de_bernkastel_bridge_couple",
        band_h=1060,
        photo_caption="Bernkastel, Middle Mosel",
        photo_credit="Febe Vanermen / Unsplash",
        kicker="THE TRIBUTARIES",
        headline="Colder Water, Higher Acid",
        standfirst="The Saar and the Ruwer join the Mosel near Trier, "
                   "inside the same Anbaugebiet. Neither tastes like the "
                   "main valley.",
        items=[
            ("The sites that matter", "Sheltered side valleys facing "
                                       "south, south-east or south-west."),
            ("Why they're different", "Slightly higher and cooler than "
                                       "the Middle Mosel -- and acidity "
                                       "can run higher still."),
            ("The name to know", "Scharzhofberg, on the Saar."),
        ],
    )),

    # ── 10 · TWO WINES CALLED PIESPORTER ──────────────────────────────
    # Round 3: photo added, per Steve -- the actual Piesporter
    # Goldtropfchen sign standing in the vines, as a bottom stripe (pages
    # 9 and 11 both lead with top photos; this varies the rhythm).
    # Also fixes a silent drop found this round: card_grid() has no
    # footnote support, so the Grosslage-vs-Grosse-Lage footnote this
    # slide carried never rendered. It's now a third card, so it renders
    # and runs through QA. The distinction is one the 2026 origin-reform
    # article singles out as routinely examined and got wrong.
    ("card_grid", dict(
        kicker="THE LABEL TRAP",
        headline="Same Village. Not the Same Wine.",
        standfirst="Under the 1971 law, every vineyard was registered as "
                   "an Einzellage or a Grosslage -- and both could say "
                   "\"Piesporter.\"",
        row_layout=[3],
        cards=[
            (None, "Einzellage", "2,658 sites",
             "One named vineyard, under 1 ha to over 200. On the label: "
             "Piesporter Goldtr\u00f6pfchen."),
            (None, "Grosslage \u2192 Region", "167 zones",
             "600\u20131,800 ha each. On the label: Piesporter "
             "Michelsberg. From 2026 it must say Region."),
            (None, "Grosse Lage", "Not the same thing",
             "The VDP's own top-site tier -- one letter from Grosslage, "
             "opposite in meaning."),
        ],
        bottom_stripe=["de_piesport_goldtropfchen_sign"],
        stripe_captions=["Piesporter Goldtr\u00f6pfchen, in the vines", ""],
        photo_credit=CRED_PIESPORT,
    )),

    # ── 11 · EISWEIN ──────────────────────────────────────────────────
    # Round 2: photo-led layout with a hero of frozen white grapes still
    # on the vine (Ivonne Arceo / Pexels -- no location data, so the
    # caption describes the subject, not a place). The bird netting
    # visible behind the cluster is standard practice for fruit left
    # hanging into winter, which ties to the "real gamble" fact below.
    ("hero_facts", dict(
        photo="de_eiswein_frozen_cluster",
        anchor=0.38,
        hero_h=1340,
        photo_caption="Frozen on the vine",
        photo_credit="Ivonne Arceo / Pexels",
        kicker="THE RUNG THAT ISN'T ABOUT SUGAR",
        headline="Defined by Temperature",
        facts=[
            ("Since 1982", "Eiswein has been its own Pr\u00e4dikat since "
                           "this year."),
            ("Same must weight as BA", "A parallel track to "
                                        "Beerenauslese, not a step "
                                        "above it."),
            ("Below \u20137\u00b0C", "Picked frozen solid and pressed "
                                  "while still frozen."),
            ("A real gamble", "Waiting for the freeze often costs part "
                              "of the crop to rot or birds."),
        ],
    )),

    # ── 12 · CLOSE ────────────────────────────────────────────────────
    # Substantially updated from the spec's own version, which was
    # written before the reform's implementing decision. Verified
    # independently (Deutsches Weininstitut, Wine Scholar Guild, Jancis
    # Robinson) before adding the June 2026 specifics: the Bundesrat
    # session date, the Komitee, and the "still in progress" caveat --
    # the actual site classification isn't finished, and the deck
    # shouldn't imply otherwise.
    ("statement", dict(
        # variant="closing" is documented in statement()'s own docstring
        # ("cover and closing are a genuine bookend... sharing the same
        # block/dot/kicker system") but isn't actually implemented --
        # the function's if/elif chain only branches on "cover" and
        # "quote"; "closing" matches neither and silently produced a
        # broken layout (identical overflow numbers no matter how much
        # the subtitle text was trimmed, which is what exposed this --
        # a real text-length problem would have responded to trimming).
        # "cover" is the correct value for this closing bookend slide
        # too, confirmed by testing directly rather than guessing.
        variant="cover",
        photo="de_hatzenport_mosel",
        photo_anchor=0.35,
        title="The Law Changed\nIts Mind in 2026",
        # Round 2: trimmed for brevity, and the Saturday teaser removed --
        # the series is dropping to 2-3 posts a week, so the close no
        # longer promises a specific next post.
        subtitle="Since June 2026, Grosses Gew\u00e4chs has national legal "
                 "standing. Which sites qualify is still being decided.",
        photo_credit=CRED_HATZENPORT,
    )),
]


def build():
    # The benchmark rules, enforced: see engine/variety.py.
    variety.report([name for name, _ in SLIDES])
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    paths = []
    total = len(SLIDES)
    for i, (name, slot) in enumerate(SLIDES, start=1):
        fn = modules.MODULES[name]
        img = fn(slot, i, total, PAL)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  {name}")
    pdf = f"{OUT}/FG_Mosel_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
