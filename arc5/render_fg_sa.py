"""THE FIELD GUIDE: SOUTH AFRICA -- "Two Currents, One Wind". A classic carousel (2160x2700, 15 slides). Arc 5 entry 1 (arc5/ARC5_SOUTH_AFRICA_PLAN.md).
Forest-green arc signature (the plan's default). Steve's steer: less Pinotage (it is not named on any slide), more Bordeaux blends and Cap Classique.

SOURCES: WSET Diploma D3 ch. 30 (South Africa) and D4 ch. 20 (Cap Classique). Every claim below was re-read against the book before it was written.
  1  cover.
  2  D3 p.505: vineyards between 32 and 35 S (comparable with the central band of Chile's vineyards and much of Mendoza); most main regions within about 50 km (30 miles)
     of the coast. THE MAP is drawn from the real Wine of Origin polygons (data/geo/za_wo_winelands.geojson; see data/geo/WO_SOURCE.md), colored by region, with 16 districts numbered.
     Region membership of each district is the official SAWIS production-areas list (October 2023).
  3  D3 p.505: the cold Benguela Current flows north from Antarctica up the west coast; the warmer Agulhas flows south down the east coast; they meet at
     Cape Agulhas; early morning coastal fog; the Cape Doctor, a strong south-easterly, in spring and summer: cools, helps inhibit vineyard disease, can compromise
     flowering and fruit set and lower yields.
  4  D3 p.505-506 (climate) and the district entries, pp.513-519: Constantia 1,000 mm; Paarl 800-900 mm; Franschhoek 800 mm; Stellenbosch more than 700 mm;
     Durbanville about 500 mm; Swartland 400 mm (climate section) but "around 500 mm" in its own entry (p.516), so the bar says 400-500; Olifants River 150-250 mm.
     Ranges are drawn at their midpoint and say so. Winter rainfall pattern (p.506). The 2015-18 drought (p.506).
  5  D3 p.506: three main soils: Table Mountain sandstone (sandy, low nutrient and water retention; higher slopes, e.g. Stellenbosch and Constantia); granite (good
     water retention, dry farming; lower slopes, e.g. Paarl); shale (good nutrients and water retention; e.g. Swartland). Many soils acidic: lime at planting.
  6  D3 p.504: 1652; "more than 370 years"; slavery abolished in the 1860s; the 'dop' system (workers paid in low-quality alcohol), formally abolished in 1961 but
     continued as a reward until 1994 "and in some places beyond"; the KWV (regulatory powers over volumes and prices; supported apartheid; Chenin Blanc, Colombard
     and Cinsaut required for brandy; under a third of wine grapes made into wine); 1994 the first democratic elections; the KWV ceased as a cooperative in 1997;
     by 2017 around 85% of wine grapes were used for wines marketed as such.
  7  D3 p.507-508: Chenin Blanc 16,000 ha, double the Loire's; the high-volume vs small-volume comparison (high yields, regular spraying against botrytis, minimal sorting,
     up to 15% Colombard / low yields, unirrigated old vines, careful hand sorting, a little botrytis if wanted, 100% Chenin Blanc).
  8  D3 p.514-515: Stellenbosch: warm climate favors Cabernet Sauvignon, Merlot; reputation on very good to outstanding, premium-priced Cabernet and related blends;
     vineyards from about 100 to 500 m; Simonsberg peak 1,390 m; cooler, higher slopes with granite- or shale-derived soils; False Bay winds cool the lower sites;
     Simonsberg-Stellenbosch ward (Cabernet-based blends; Kanonkop, Rustenberg); Rust en Vrede and Raats at district level; Stellenbosch University, the only oenology degree.
  9  D3 p.511 (three main blends: white Cape, red Bordeaux, red Cape), p.515 (Paarl: warmer, "a distinct ripeness and fuller body compared to those of Stellenbosch";
     Vilafonte at super-premium prices; Simonsberg-Paarl: higher, greater diurnal range) and Franschhoek (wrapped by mountains; Sauvignon Blanc, Cabernet Sauvignon and
     Shiraz most grown; fruit prized for freshness as a blending component; some leading Cap Classique producers).
  10 D3 p.516: Swartland: warm Mediterranean; "around 500 mm"; irrigation for most vineyards; low-fertility granite and shale; a significant share of the country's
     old vines (over 35 years), tending to be unirrigated; since 2000 the movement began by Charles Back at Spice Route, then Eben Sadie and Chris and Andrea Mullineux;
     themes: low yields, dry farming, often organic or biodynamic, old vines, ambient yeasts, old oak.
  13 (map) Stellenbosch's eight wards (Banghoek, Bottelary, Devon Valley, Jonkershoek Valley, Papegaaiberg, Polkadraai Hills, Simonsberg-Stellenbosch, Vlottenburg), the Paarl wards
     and Durbanville in the window, and the Franschhoek district; D3 p.514-515.
  11 D3 p.513 Constantia (history from 1685; revived Vin de Constance; east-facing slopes; False Bay 10 km; about 1,000 mm; no Pinot Noir: it fares less well in the wind);
     p.520 Elgin (inland plateau 250-500 m; coast about 20 km south; "the coolest wine-growing area of South Africa"); p.521 Walker Bay (Hermanus; about 800 mm;
     Hamilton-Russell planted Chardonnay and Pinot Noir in the Hemel-en-Aarde Valley from 1975; clay up to 55%).
  12 D3 p.511-512: the four-tier Wine of Origin hierarchy and its examples; 100% from the place named; 85% for a stated vintage or variety; a tasting by the Wine
     Certification Authority; Western Cape accounts for nearly all South African wine by volume.
  14 D4 p.115-116: traditional-method production began in 1971 (Simonsig); the CCPA founded 1992 (members over 90% of traditional-method production); whole-bunch pressing
     mandatory; at least three bars of pressure after disgorgement; at least 12 months on the lees; the Cap Classique extended-lees aging tier from 2022 (Chardonnay, Pinot Noir
     and Pinot Meunier only; at least 36 months).
  15 D4 p.116-117: Robertson and Bonnievale (Breede River Valley): significant limestone, "argued to be beneficial"; narrow, shaded valleys; cool ocean breezes up the Breede
     River; the biggest diurnal range; picking about 90 days after flowering with extra foliage; 9.5-11% potential alcohol, about 12% abv finished; medium (+) acidity, ripe
     apple and citrus; good to very good; mid- to premium-priced.
  16 D4 p.119: 2021-2023 an average of 3.9 million bottles of Cap Classique a year, 40% of all sparkling wine sold; nearly 70% exported.
NOT USED: Pinotage (Steve's steer); the CSW guide's older figures (D3 and D4 win where they differ).
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
os.environ.setdefault("AMERICAN_ENGLISH", "1")
import core      # noqa: E402
import modules   # noqa: E402
import variety   # noqa: E402
from tokens import W, M, INK, PAPER    # noqa: E402

OUT = "/home/claude/out_fg_sa"
os.makedirs(OUT, exist_ok=True)

# ---- the arc's forest green (engine/themes.py), the house gold, and a warm-to-dry ramp for the rain chart
GREEN = (28, 70, 48)
GOLD = (196, 158, 84)
PAL = dict(SIGNATURE=GREEN, ACCENT=GOLD, LEAD=(128, 88, 40), MARK=GREEN)
SEA, SAGE, OCHRE, TERRA, CLAY = (74, 118, 140), (112, 140, 104), (190, 150, 70), (168, 96, 60), (130, 70, 48)
CHART = dict(
    ripe=[SEA, SAGE, OCHRE, TERRA, CLAY], focus=GREEN, cool=SEA, warm=GOLD, vine=(86, 104, 70), shade=GREEN, amber=TERRA, gold=GOLD,
    grape=(120, 22, 62), stone=(110, 100, 92), track=(220, 208, 196), ice=SEA, ice_fill=(226, 234, 240), ice_text=(54, 78, 100),
)

C_SAT = "South African Tourism / Wikimedia Commons (CC BY 2.0)"
C_YEO = "yeowatzup / Wikimedia Commons (CC BY 2.0)"
C_FAB = "fabulousfabs / Wikimedia Commons (CC BY 2.0)"
C_ROO = "rooymans2000 / Wikimedia Commons (CC BY 2.0)"


# ------------------------------------------------------------------------------------------ the maps: REAL Wine of Origin polygons (arc5/wo_maps.py)
import wo_maps as WM      # noqa: E402

DISTRICT_MAP = WM.district_overview(
    bbox=(17.2, 21.4, -34.95, -32.95),
    key_groups=[("COASTAL REGION", ["Cape Town", "Stellenbosch", "Paarl", "Franschhoek", "Wellington", "Tulbagh", "Swartland", "Darling"]),
                ("CAPE SOUTH COAST", ["Elgin", "Walker Bay", "Overberg", "Cape Agulhas", "Swellendam"]),
                ("BREEDE RIVER VALLEY", ["Breedekloof", "Worcester", "Robertson"])],
    kicker="WHERE IT GROWS", headline="The Winelands, by District",
    standfirst="Vineyards lie between 32\u00b0 and 35\u00b0 S, mostly near the sea.")
DISTRICT_MAP["key_pitch"] = 1.15
DISTRICT_MAP["context"] = [(0.03, 0.60, "Atlantic Ocean"), (0.72, 0.925, "Indian Ocean")]
import core as _core     # noqa: E402
STELL_MAP = WM.ward_map(
    bbox=(18.670, 19.010, -34.012, -33.790),
    numbered=[("Stellenbosch", "Simonsberg-Stellenbosch"), ("Stellenbosch", "Banghoek"), ("Stellenbosch", "Devon Valley"), ("Stellenbosch", "Bottelary"),
              ("Stellenbosch", "Jonkershoek Valley"), ("Stellenbosch", "Papegaaiberg"), ("Stellenbosch", "Polkadraai Hills"), ("Stellenbosch", "Vlottenburg"),
              ("Paarl", "Simonsberg-Paarl")],
    kicker="WARD BY WARD", headline="Stellenbosch Up Close",
    standfirst=None,
    highlight="Simonsberg-Stellenbosch", context_districts=("Stellenbosch", "Paarl", "Franschhoek", "Cape Town"), ctx_font=_core.font("caption_italic", 64),
    focus_district="Stellenbosch")
STELL_MAP["key_pitch"] = 1.2


# ------------------------------------------------------------------------------------------ the Wine of Origin circles (page pixels)
def _euler():
    return [("Western Cape", 1080, 1650, 760, None, "above"),
            ("Coastal Region", 852, 1707, 513, "Western Cape", "above"),
            ("Breede River Valley", 1590, 1530, 235, "Western Cape", "in"),
            ("Stellenbosch", 814, 1783, 361, "Coastal Region", "above"),
            ("Simonsberg-Stellenbosch", 814, 1821, 276, "Stellenbosch", "in")]


SLIDES = [
    # 1 -- COVER: vine rows and mountains in the Stellenbosch winelands (Mister-E), natural color. The first version used a sunset photo whose pink grade was baked into the file.
    ("cover_bleed", dict(
        photo="sa_cape_vineyards_stell", photo_anchor=0.5, photo_zoom=1.0,
        kicker="THE FIELD GUIDE: SOUTH AFRICA", kicker_size=84,
        kicker_chip=dict(color=(250, 246, 236), alpha=0.45, text=INK),
        title="Two Currents,\nOne Wind", title_top=0.44,
        photo_credit="Mister-E / Wikimedia Commons (CC BY 2.0)",
    )),

    # 2 -- WHERE IT GROWS: D3 p.505 (latitude, distance from the sea) on REAL Wine of Origin district polygons (see the ledger above).
    ("wo_map", DISTRICT_MAP),

    # 3 -- TWO CURRENTS, ONE WIND: D3 p.505. Cape Point has no place claim in the copy.
    ("hero_facts", dict(
        photo="sa_cape_point", anchor=0.5, hero_h=1340, photo_caption="Cape Point", photo_credit=C_YEO,
        kicker="THE CLIMATE ENGINE", headline="Two Oceans Cool the Cape",
        facts=[("The Benguela", "A cold current from Antarctica, up the west coast: the main cooling influence."),
               ("The Agulhas", "A warmer current down the east coast. The two meet at Cape Agulhas."),
               ("Morning fog", "Warm, moist air meets the cold sea and forms fog that clears by mid-morning."),
               ("The Cape Doctor", "A strong south-easter in spring and summer: it cools and curbs disease, but can cut yields.")],
    )),

    # 4 -- THE RAIN GRADIENT: D3 p.505-506 and the district entries. Ranges are drawn at their midpoint and the chart says so.
    ("chart_stack", dict(
        chart=CHART, kicker="HOW MUCH RAIN", headline="From Wet Peninsula to Dry North",
        standfirst="Rain falls mainly in winter, and thins out to the north. The 2015\u201318 drought made water a top priority.",
        bar_chart=dict(title="ANNUAL RAINFALL IN MILLIMETERS (A RANGE IS DRAWN AT ITS MIDPOINT)",
                       bars=[("Constantia", 70, "about 1,000", "cool", True),
                             ("Paarl", 60, "800\u2013900", "vine", False),
                             ("Franschhoek", 56, "about 800", "vine", False),
                             ("Stellenbosch", 49, "over 700", "vine", False),
                             ("Swartland", 32, "400\u2013500", "warm", False),
                             ("Olifants River", 14, "150\u2013250", "amber", True)]),
    )),

    # 5 -- THREE SOILS: D3 p.506.
    ("tile_grid", dict(
        kicker="THREE SOILS", headline="Sandstone, Granite and Shale",
        standfirst="Soils are varied and complex, but three types dominate the Western Cape.",
        tile_colors=[((196, 158, 84), INK), (GREEN, PAPER), ((110, 100, 92), PAPER), ((168, 96, 60), PAPER)],
        tiles=[("Sandstone", "Table Mountain", "Sandy and poor, on higher slopes, as in Stellenbosch and Constantia. Holds little water or nutrient."),
               ("Granite", "Holds water", "On foothills and lower slopes, as in Paarl. Good for dry farming."),
               ("Shale", "Fertile and holds water", "Common in Swartland. Good nutrients, and good for dry farming."),
               ("Acidic", "Lime at planting", "Many Western Cape soils are acidic enough to limit nutrients.")],
    )),

    # 6 -- FROM 1652 TO 1994: D3 p.504. Stated plainly, once.
    ("timeline", dict(
        kicker="THE HISTORY", headline="From 1652 to 1994",
        standfirst="Over 370 years of winemaking, and a very recent freedom.",
        events=[("1652", "Europeans settle the Cape", "Grapes are grown for wine ever since."),
                ("1860s", "Slavery abolished", "Wine had relied on enslaved labor."),
                ("1961", "The \u2018dop\u2019 system abolished", "Workers were paid in low-quality alcohol. It continued as a reward to 1994, and in places beyond."),
                ("1994", "Apartheid ends", "The KWV co-op, which set volumes and prices and backed segregation, loses its powers."),
                ("2017", "About 85% made into wine", "Before the 1990s, under a third was.")],
    )),

    # 7 -- CHENIN BLANC: D3 p.507-508. Two ways to make one grape. The photos are decorative; the labels are the categories.
    ("duel", dict(
        photos=("fffa_climate_young_vines", "sa_muratie_vines"), labels=("High volume", "Small volume"),
        kicker="CHENIN BLANC", headline="One Grape, Two Worlds",
        standfirst="Chenin covers 16,000 ha, double the Loire's area, and is made two ways.",
        mode="table", col_heads=("Inexpensive", "Premium"),
        rows=[("In the vineyard", "High yields, sprayed against botrytis", "Low yields, old unirrigated vines"),
              ("At harvest", "Minimal or no sorting", "Careful hand sorting"),
              ("In the bottle", "May include up to 15% Colombard", "100% Chenin Blanc")],
        photo_credit="Mister-E; South African Tourism / Wikimedia Commons (CC BY 2.0)",
    )),

    # 8 -- CABERNET COUNTRY: D3 p.514-515.
    ("hero_facts", dict(
        photo="sa_stell_valley", anchor=0.5, hero_h=1340, photo_caption="Stellenbosch", photo_credit=C_SAT,
        kicker="CABERNET COUNTRY", headline="Stellenbosch Wears Cabernet",
        facts=[("The reputation", "Very good to outstanding, premium-priced Cabernet and related blends."),
               ("The mountains", "Simonsberg peaks at 1,390 m. Vineyards climb from about 100 to 500 m."),
               ("The slopes", "Higher, cooler slopes on granite or shale help make better grapes."),
               ("The wind", "Cool False Bay winds reach the lower sites.")],
    )),

    # 9 -- THE BORDEAUX BLEND, CAPE-STYLE: D3 p.511, 515.
    ("side_rail", dict(
        photo="sa_boschendal_meadow", photo_caption="Boschendal, Franschhoek", side="right", photo_credit=C_SAT,
        kicker="THE BORDEAUX BLEND", headline="Three Valleys,\nOne Blend",
        standfirst="",
        items=[("One of three", "South Africa's main blends: white Cape, red Bordeaux and red Cape."),
               ("Stellenbosch", "Cabernet-based blends carry the name. Simonsberg: Kanonkop, Rustenberg."),
               ("Paarl", "Warmer: a distinct ripeness and fuller body. Vilaf\u00f4nt\u00e9 sells at super-premium prices."),
               ("Franschhoek", "Ringed by mountains. Its fresh fruit is prized for blending.")],
    )),

    # 10 -- SWARTLAND: D3 p.516.
    ("stat_wall", dict(
        kicker="THE NEW WAVE", headline="Swartland Starts Over",
        standfirst="A warm, dry district whose old vines inspired a new generation.",
        stats=[("35+", "YEARS OLD", "A large share of the country's old vines, mostly unirrigated."),
               ("2000", "THE TURNING POINT", "Charles Back at Spice Route, then Eben Sadie, and Chris and Andrea Mullineux."),
               ("400\u2013500", "MM OF RAIN", "Low for a warm climate: most vineyards need irrigation."),
               ("6", "COMMON THEMES", "Low yields, dry farming, organic farming, old vines, ambient yeasts, old oak.")],
        famous=["Granite and shale soils", "Very good to outstanding quality", "Premium to super-premium prices"], famous_label="ALSO", cell_max=650,
    )),

    # 11 -- THE COOL SOUTH: D3 p.513, 520, 521.
    ("tile_grid", dict(
        kicker="THE COOL SOUTH", headline="Where the Ocean Takes Over",
        standfirst="Four cooler places, all within reach of the sea.",
        tile_colors=[(GREEN, PAPER), (SEA, PAPER), ((196, 158, 84), INK), ((110, 100, 92), PAPER)],
        tiles=[("Constantia", "Wine since 1685", "False Bay is 10 km away. About 1,000 mm of rain. No Pinot Noir: too windy."),
               ("Elgin", "The coolest area", "An inland plateau at 250\u2013500 m, with cloud cover and fresh, high-acid wines."),
               ("Hemel-en-Aarde", "Burgundy-inspired", "Hamilton-Russell planted Chardonnay and Pinot Noir here from 1975."),
               ("Walker Bay", "Cool maritime", "Hermanus is its town. About 800 mm of rain, all year.")],
    )),

    # 12 -- WINE OF ORIGIN: D3 p.511-512.
    ("euler_nesting", dict(
        kicker="THE LABEL", headline="Four Tiers of Place",
        standfirst="A place named on the label means 100% of the grapes. A stated vintage or grape needs 85%.",
        circles=_euler(),
    )),

    # 13 -- STELLENBOSCH UP CLOSE: D3 p.514-515 and the official production-areas list; real polygons; Simonsberg-Stellenbosch is D3's example ward.
    ("wo_map", STELL_MAP),

    # 14 -- CAP CLASSIQUE: THE RULES: D4 p.115-116.
    ("stat_wall", dict(
        kicker="CAP CLASSIQUE", headline="Bubbles With Rules",
        standfirst="South Africa's traditional-method sparkling wine, made to its own regulations.",
        stats=[("1971", "THE FIRST", "Simonsig starts traditional-method production."),
               ("12", "MONTHS ON LEES", "The legal minimum, in the bottle."),
               ("36", "MONTHS, EXTENDED", "Since 2022: only Chardonnay, Pinot Noir and Pinot Meunier."),
               ("1992", "THE ASSOCIATION", "Its members make over 90% of the traditional-method wine.")],
        famous=["Whole-bunch pressing is mandatory", "Three bars of pressure after disgorgement"], famous_label="ALSO REQUIRED", cell_max=650,
    )),

    # 15 -- CAP CLASSIQUE: THE GRAPES: D4 p.116-117. Young vines in Stellenbosch (D4: Stellenbosch is one of the principal sources of Cap Classique grapes), natural color.
    ("side_rail", dict(
        photo="sa_young_vines_stell", photo_caption="Young vines, Stellenbosch", side="right", photo_credit="Mister-E / Wikimedia Commons (CC BY 2.0)",
        kicker="CAP CLASSIQUE", headline="Picked for\nFreshness",
        standfirst="",
        items=[("Slow ripening", "Growers wait about 90 days after flowering, with extra leaf cover for shade."),
               ("Low sugar", "Picked at 9.5\u201311% potential alcohol: about 12% in the finished wine."),
               ("Limestone and cool air", "Robertson and Bonnievale: limestone, shaded valleys, river breezes."),
               ("In the glass", "Medium (+) acidity, ripe apple and citrus. Good to very good.")],
    )),

    # 16 -- CLOSE: D4 p.119. The cover's vineyard again, a bookend (the layout's text panel covers the lower half of the photo).
    ("statement", dict(
        variant="cover", photo="sa_cape_vineyards_stell", photo_anchor=0.30,
        title="The Cape in\nthe Glass",
        subtitle="Cap Classique is now 40% of the sparkling wine sold in South Africa, and nearly 70% of it is exported.",
        photo_credit="Mister-E / Wikimedia Commons (CC BY 2.0)",
    )),
]


def build():
    variety.report([name for name, _ in SLIDES])
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)
    paths = []
    total = len(SLIDES)
    for i, (name, slot) in enumerate(SLIDES, start=1):
        img = modules.MODULES[name](dict(slot), i, total, PAL)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d} {name}")
    core.assemble_pdf(paths, f"{OUT}/FG_SA_review.pdf")
    print("PDF:", f"{OUT}/FG_SA_review.pdf")


if __name__ == "__main__":
    build()
