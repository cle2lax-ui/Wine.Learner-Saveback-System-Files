"""FIELD GUIDE — The Côte de Nuits.

Photos: Wikimedia Commons (CC BY / CC BY-SA), credited per slide.
Map geometry: real INSEE commune boundaries for Côte-d'Or (dept 21),
dissolved and normalised in build_cdn_geo.py — no schematic silhouettes.

Content engineered against SOCIAL_PASS_STYLE_GUIDE.md:
  gate 1 decode layer .... slide 3 (Flagey-Echézeaux, gold, unexplained)
  gate 2 save asset ...... slide 5 (grand cru roll call)
  gate 3 send line ....... slide 8 ("one per cent")
  gate 4 open question ... slide 12 (Les Saint-Georges)
  gate 5 callback ........ slide 12 (Barossa Old Vine Charter)
  gate 6 cover hook ...... slide 1 (fact-led, template exemption)
"""
import json, os

import core
import modules
from map_atlas import regional_atlas

OUT = "/home/claude/out_cote_de_nuits"
os.makedirs(OUT, exist_ok=True)

# ── Palette ────────────────────────────────────────────────────────────
# Oxblood signature per direction. LEAD is a warmer brick, deliberately
# separated from SIGNATURE so the serif run-ins never read as the same
# colour as the headline (v8 standing rule -- set both explicitly, never
# let them fall back).
PAL = dict(
    SIGNATURE=(104, 26, 38),      # deep oxblood
    ACCENT=(176, 137, 60),        # antique gold
    LEAD=(150, 66, 48),           # warm brick run-in
    MARK=(104, 26, 38),
)

GEO = json.load(open("/home/claude/styleguide/geo/cdn.json"))
LOCATOR = json.load(open("/home/claude/styleguide/geo/france_locator.json"))

CRED_DRC = "© Pierre André / Wikimedia Commons (CC BY-SA 4.0)"
CRED_JDA = "Jean de l'Auxois / Wikimedia Commons (CC BY-SA 4.0)"
CRED_GO69 = "GO69 / Wikimedia Commons (CC BY-SA 4.0)"
CRED_MO = "Michal Osmenda / Wikimedia Commons (CC BY 2.0)"

VILLAGES = ["Marsannay-la-Côte", "Fixin", "Gevrey-Chambertin", "Morey-Saint-Denis",
            "Chambolle-Musigny", "Vougeot", "Vosne-Romanée", "Nuits-Saint-Georges"]
CONTEXT = ["Chenôve", "Couchey", "Brochon", "Premeaux-Prissey", "Comblanchien", "Corgoloin"]

LABEL = {"Marsannay-la-Côte": "Marsannay", "Nuits-Saint-Georges": "Nuits-St-Georges",
         "Morey-Saint-Denis": "Morey-St-Denis", "Flagey-Echézeaux": "Flagey-Echézeaux"}

FILL_VILLAGE = (196, 176, 168)
FILL_CONTEXT = (226, 221, 214)
FILL_EGG = (176, 137, 60)          # the decode layer, gold, never explained


def _regions():
    out = []
    for n in CONTEXT:
        out.append((n, GEO["communes"][n], FILL_CONTEXT))
    for n in VILLAGES:
        out.append((n, GEO["communes"][n], FILL_VILLAGE))
    out.append(("Flagey-Echézeaux", GEO["communes"]["Flagey-Echézeaux"], FILL_EGG))
    return out


SLIDES = [

    # ── 1 · COVER (fact-led, template exemption approved) ──────────────
    ("statement", dict(
        variant="cover",
        photo="cdn_cover_drc",
        photo_anchor=0.58,
        photo_zoom=1.12,
        title="24 of Burgundy's\n33 Grands Crus",
        title_size=152,
        # explicit break keeps the region name whole on line two
        subtitle="Sit on one narrow strip of limestone.\nThe Côte de Nuits.",
        subtitle_size=[86, 152],   # setup line quiet, region name at title scale
        subtitle_font=["body_bold", "italbold"],  # sans setup, serif payoff
        subtitle_color=(238, 206, 138),   # brighter than ACCENT on oxblood
        mark_side="left",                 # off the Romanée-Conti cross
        photo_credit=CRED_DRC,
    )),

    # ── 2 · SEND LINE (moved up: the scale frames everything after it) ─────────────────────────────────────────────────
    ("stat_wall", dict(
        kicker="THE SCALE",
        headline="One Per Cent",
        standfirst="Grand cru is one per cent of everything Burgundy makes. Every argument "
                   "about Burgundy is an argument about that one per cent.",
        standfirst_leading=1.04,
        stats=[
            ("1%", "of Burgundy's\nproduction", "is grand cru"),
            ("52%", "is regional\nappellation", "Bourgogne and its kin"),
            ("24", "grands crus in the\nCôte de Nuits", "of Burgundy's 33"),
            ("0.84 ha", "La Romanée,\nthe smallest", "grand cru in France"),
            ("90%", "of the Côte de Nuits", "is planted to Pinot Noir"),
            ("640", "premiers crus\nin Burgundy", "not one is its own appellation"),
        ],
    )),

    # ── 2 · ORIENTATION ───────────────────────────────────────────────
    ("editorial_lead", dict(
        photo="cdn_chambolle_combe",
        photo_caption="Chambolle-Musigny, and the combe that cuts the slope above it",
        photo_credit=CRED_JDA,
        kicker="ORIENTATION",
        headline="Twenty Minutes, End to End",
        standfirst="Marsannay to Corgoloin is a drive you could make before lunch. Pinot "
                   "Noir is close to ninety per cent of what grows on it.",
        standfirst_size=62,
        standfirst_leading=1.06,
        lead_size=76,
        items=[
            ("The aspect", "East and south-east facing, hills behind blocking the "
                           "westerlies. Shelter peaks between Gevrey-Chambertin and "
                           "Nuits-Saint-Georges, and so does ripeness."),
            ("The rock", "Limestone dominates the mix here. The Côte de Beaune carries "
                         "more clay and deeper soil, and grows the better Chardonnay for "
                         "that reason."),
            ("The band", "Grands crus sit mid-slope. Above, too little soil to farm. "
                         "Below, clay and vigour."),
        ],
    )),

    # ── 3 · THE COMMUNES (real boundary data) ─────────────────────────
    ("regional_atlas", dict(
        kicker="THE COMMUNES",
        headline="Nine Names, North to South",
        map_h=1430,
        main=dict(
            outline=GEO["outline"],
            aspect=GEO["aspect"],
            outline_smooth=4,
            regions=_regions(),
                # Anchor each label on the commune's EASTERN flank, not its
            # centroid. These communes run a long way west up into the
            # Hautes Côtes, so the centroid sits out in country with no
            # vines on it -- and, drawn on a strip this narrow, pulled
            # every label onto the map body. The east flank is both
            # where the appellation vineyards actually are and where the
            # leader lines want to start.
            # One shared anchor x, each commune's own latitude. The
            # strip bends west as it runs south, so per-commune east
            # edges put the southern labels back on top of the map. A
            # common x east of the whole ribbon gives a flush label
            # column and leader lines that read as a latitude index.
            # Targets sit on each commune's own east flank; the labels
            # are pulled out to a flush column, so every name gets a real
            # leader line back to the shape it belongs to.
            labels=[(LABEL.get(n, n), GEO["anchors"][n])
                    for n in VILLAGES + ["Flagey-Echézeaux"]],
            label_column_x=0.80,
            # Every label to the right, deliberately. The automatic
            # left/right split assumes a map wide enough that a
            # left-side label clears the shape; the Côte de Nuits is a
            # 20km ribbon rendered barely 700px wide, so every "left"
            # label landed on top of the commune it was naming. One
            # clean column of names beside the strip is both legible and
            # a truer picture of the geography.
            forced_side={n: "right" for n in
                         ["Marsannay", "Fixin", "Gevrey-Chambertin",
                          "Morey-St-Denis", "Chambolle-Musigny", "Vougeot",
                          "Vosne-Romanée", "Nuits-St-Georges",
                          "Flagey-Echézeaux"]},
            max_label_w=340,
        ),
        locator=dict(outline=LOCATOR["outline"], aspect=LOCATOR["aspect"],
                     box=LOCATOR["box"], region=LOCATOR["burgundy"],
                     title="BURGUNDY, FRANCE"),
        locator_w=330,
        legend=[
            (FILL_VILLAGE, "Village appellation"),
            (FILL_EGG, "Grand cru, but no village appellation of its own"),
            (FILL_CONTEXT, "Vines, sold under broader appellations"),
        ],
        legend_size=44,
        description="Flagey-Echézeaux is the odd one out: two grand cru vineyards, but its "
                    "village wine is sold as Vosne-Romanée. Boundaries traced from the "
                    "commune cadastre.",
    )),

    # ── 4 · TIMELINE (moved up: chronology before classification) ─────────────────────────────────────────────────
    ("timeline", dict(
        kicker="HOW IT WAS DRAWN",
        headline="Nine Centuries of Boundary-Making",
        standfirst="The map was not designed. It accumulated — monks, then merchants, "
                   "then lawyers.",
        standfirst_leading=1.04,
        bg_photo="cdn_bg_burgundy_bottle",
        bg_fade=0.85,   # slightly more visible than the previous 0.93
        bg_anchor=0.5,
        events=[
            ("1098", "Cîteaux is founded",
             "Cistercian monks begin farming the slope plot by plot, and recording which "
             "plots taste different from their neighbours."),
            ("1336", "Clos de Vougeot is enclosed",
             "The wall the monks finish still defines the vineyard's boundary today."),
            ("1861", "The Beaune committee classifies",
             "A three-tier ranking of the Côte d'Or's vineyards — the direct ancestor of "
             "the hierarchy still in use."),
            ("1936", "Appellation law arrives",
             "The Côte d'Or's crus are written into the first generation of French AOCs, "
             "each grand cru its own appellation."),
            ("2015", "UNESCO inscribes the climats",
             "The named parcels are recognised as World Heritage — the boundaries "
             "themselves, not the wine."),
        ],
    )),

    # ── 4 · THE HIERARCHY (the exception is the point) ────────────────
    ("euler_nesting", dict(
        kicker="CLASSIFICATION",
        headline="Grand Cru Sits Outside the Village",
        standfirst="Every student draws this as a pyramid. It isn't one. Premier cru sits "
                   "inside the village appellation; grand cru is an appellation of its own.",
        standfirst_leading=1.04,
        circles=[
            ("Bourgogne AOC", 700, 1560, 520, None, "above"),
            ("Village AOC", 700, 1660, 380, "Bourgogne AOC", "top"),
            ("Premier Cru", 700, 1830, 190, "Village AOC", "in"),
            ("Grand Cru AOC", 1690, 1660, 260, None, "in"),
        ],
        # Real bottle photos, one per tier -- user-supplied product shots,
        # background removed, sized by height at true aspect, deliberately
        # allowed to cross their circle's boundary: these are specimens
        # pinned ON the diagram, not content boxed inside it. Regnard's
        # Bourgogne Pinot Noir is, as before, the one tier where "from the
        # Côte de Nuits" doesn't strictly apply -- Bourgogne AOC is the
        # region-wide appellation, not a Côte de Nuits designation.
        bottles=[
            ("cdn_bottle_regnard", 1120, 1150, 360),      # Régnard, Bourgogne Pinot Noir
            ("cdn_bottle_marsannay", 700, 1540, 360),     # Louis Latour, Marsannay (village)
            ("cdn_bottle_gevrey1er", 700, 2010, 360),     # Gérard Seguin, Gevrey-Chambertin 1er Cru Craipillot
            ("cdn_bottle_echezeaux", 1690, 1910, 360),    # Domaine de la Romanée-Conti, Échézeaux (grand cru)
        ],
        exceptions_label="ITS OWN APPELLATION",
        exceptions_label_pos=(1450, 1300),
        footnote="A Côte d'Or grand cru is labelled by vineyard name alone.",
    )),

    # ── 5 · SAVE ASSET · the roll call ────────────────────────────────
    ("card_grid", dict(
        kicker="THE TWENTY-FOUR",
        headline="Every Grand Cru, by Commune",
        standfirst="Bonnes-Mares splits across two communes and is counted once — hence "
                   "twenty-five parts below, not twenty-four.",
        standfirst_leading=1.04,
        row_layout=[2, 2, 3],
        row_even=True,
        body_leading=1.12,   # tighter than the 1.28 default
        row_gap=56,          # widened further with the standfirst now two lines
        col_gap=140,         # a bit more air between columns than the 110 default
        card_border=True,
        cards=[
            # Ranked by grand cru count, most to least, reading left to
            # right then down. Morey counts five (four plus the larger
            # part of Bonnes-Mares); Chambolle and Flagey both count two.
            (None, "Gevrey-Chambertin", "NINE",
             "Chambertin · Clos de Bèze · Chapelle · Charmes · Griotte · "
             "Latricières · Mazis · Mazoyères · Ruchottes"),
            (None, "Vosne-Romanée", "SIX",
             "Romanée-Conti · La Romanée · La Tâche · Richebourg · "
             "Romanée-St-Vivant · La Grande Rue"),
            (None, "Morey-St-Denis", "FOUR, PLUS MOST OF A FIFTH",
             "Clos de la Roche · Clos St-Denis · Clos des Lambrays · Clos de Tart · "
             "Bonnes-Mares (the larger part — the rest is Chambolle's)"),
            (None, "Chambolle-Musigny", "ONE, PLUS THE REST OF A SECOND",
             "Musigny · Bonnes-Mares (the smaller part — most of it is Morey's)"),
            (None, "Flagey-Echézeaux", "TWO",
             "Échezeaux · Grands Échezeaux"),
            (None, "Vougeot", "ONE",
             "Clos de Vougeot, bigger than the village AOC around it"),
            (None, "Nuits-St-Georges", "NONE",
             "Les Saint-Georges leads the premiers crus"),
        ],
    )),

    # ── 6 · THE DUEL ──────────────────────────────────────────────────
    ("duel", dict(
        photos=("cdn_gevrey_clos_st_jacques", "cdn_chambolle_slope"),
        labels=("GEVREY-CHAMBERTIN", "CHAMBOLLE-MUSIGNY"),
        photo_credit="GO69 · Jean de l'Auxois / Wikimedia Commons (CC BY-SA 4.0)",
        kicker="TWO COMMUNES",
        headline="Power and Perfume",
        standfirst="Morey-Saint-Denis sits between them. Each has a premier cru — Clos "
                   "Saint-Jacques, Les Amoureuses — that outsells most grands crus.",
        standfirst_leading=1.02,
        mode="table",
        col_heads=("GEVREY", "CHAMBOLLE"),
        rows=[
            ("Grands crus", "Nine, more than any commune in Burgundy", "One, plus a share of a second"),
            ("Soil", "Deeper, more clay, more iron", "Thinner, stonier limestone"),
            ("Reputation", "Structure, depth, dark fruit", "Lift, red fruit, fine tannin"),
        ],
    )),

    # ── 7 · CLOS DE VOUGEOT ───────────────────────────────────────────
    ("fact_file", dict(
        photo="cdn_clos_vougeot",
        # No zoom: at 1.15 the horizontal crop cut the château off the
        # right-hand side, which is where it sits in this frame.
        photo_anchor=0.06,
        photo_zoom=1.0,
        band_h=880,                      # taller band: the buildings need room
        photo_caption_align="right",     # caption off the château
        photo_caption="Clos de Vougeot, the château at the head of the slope",
        photo_credit=CRED_MO,
        kicker="ONE VINEYARD",
        headline="Fifty Hectares, One Label",
        facts=[
            ("Size", "Just over 50 ha — some sixty times La Romanée"),
            ("Enclosed", "By the Cistercians of Cîteaux, walled by the 14th century"),
            ("Owners", "Around eighty separate growers"),
            ("Top of the slope", "Steeper, poorer soil, the wines with grip"),
            ("Foot of the slope", "Flatter, richer, more clay, more vigour"),
            ("On the label", "Clos de Vougeot. Nothing distinguishes the two."),
        ],
    )),

    # ── 9 · THE SLOPE ─────────────────────────────────────────────────
    ("ladder", dict(
        kicker="THE SLOPE",
        headline="Why the Middle Wins",
        standfirst="The classification is, more than anything else, a map of altitude. "
                   "Read it from the top of the hill down.",
        standfirst_leading=1.04,
        pastel=True,
        uniform_type=True,
        tiers=[
            ("MID-SLOPE — Grand Cru", "Thin soil over limestone, full sun, free drainage. "
                                      "A narrow band."),
            ("UPPER AND LOWER FLANKS — Premier Cru", "Immediately above and below, named "
                                                     "vineyard by vineyard."),
            ("THE FOOT — Village", "Deeper soil, more clay, poorer drainage, more vigour."),
            ("BEYOND THE SLOPE — Regional", "Flat land past the top and out onto the plain. "
                                            "Hautes Côtes de Nuits and Bourgogne."),
        ],
    )),

    # ── 11 · VOCABULARY ───────────────────────────────────────────────
    ("lexicon_cloud", dict(
        kicker="THE VOCABULARY",
        headline="Burgundy: Words to Know",
        terms=[
            ("Climat", 96, "A named parcel"),
            ("Lieu-dit", 74, "A place name"),
            ("Clos", 82, "Walled vineyard"),
            ("Monopole", 66, "One owner only"),
            ("Cuvée", 58, "A single blend"),
            ("Domaine", 70, "Grows its own"),
            ("Négociant", 62, "Buys fruit or wine"),
            ("Combe", 54, "Side valley"),
            ("Tastevin", 50, "Cup, and a brotherhood"),
            ("Hautes Côtes", 56, "Above the slope"),
        ],
    )),

    # ── 12 · CLOSING · open question + callback ───────────────────────
    ("statement", dict(
        variant="closing",
        photo="cdn_chambolle_slope",
        photo_anchor=0.62,
        title="Should Les Saint-Georges\nBe Promoted?",
        subtitle="The Barossa ranks vines by age. Burgundy ranks them by address. "
                 "Nuits-Saint-Georges has no grand cru at all — should it?",
        photo_credit=CRED_JDA,
    )),
]


def build():
    reg = dict(modules.MODULES) if hasattr(modules, "MODULES") else {}
    reg["regional_atlas"] = regional_atlas
    paths = []
    total = len(SLIDES)
    for i, (name, slot) in enumerate(SLIDES, start=1):
        fn = reg.get(name) or getattr(modules, name)
        img = fn(slot, i, total, PAL)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
    pdf = f"{OUT}/FG_CoteDeNuits_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
