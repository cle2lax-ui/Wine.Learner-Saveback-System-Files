import os
from tokens import DEFAULT_PALETTE
from modules import (statement, grid_cover, editorial_lead, mosaic, process_map, duel,
                      card_grid, spotlight, feature_trio, horizontal_trio, fact_file)
import core

OUT = "/home/claude/out_aroma"
os.makedirs(OUT, exist_ok=True)

# Deck-specific override: forest green instead of the Field Guide
# default red, per direction -- highlight color (headlines, cover/
# closing block, dot icons) all key off pal SIGNATURE, so a single
# override reaches all of them without touching the shared default.
pal = dict(DEFAULT_PALETTE)
pal["SIGNATURE"] = (30, 74, 48)

TOTAL = 12
paths = []


def save(fn, slot, n, extra=None, name=""):
    kwargs = dict(extra or {})
    img = fn(slot, n, TOTAL, pal, **kwargs) if fn not in (statement, grid_cover) else fn(slot, n, TOTAL, pal)
    p = f"{OUT}/{n:02d}_{name}.png"
    img.save(p)
    paths.append(p)


# 1 — Cover: 3x3 studio-photography grid + standard color blade
save(grid_cover, dict(
    photos=[
        "grid_lemon", "grid_strawberry", "grid_vanilla",
        "grid_butter", "grid_rose", "grid_cinnamon",
        "grid_pepper", "grid_toast", "grid_yogurt",
    ],
    title="How Did All These Flavors\nGet Into My Wine?",
    subtitle="Wine Aroma & Flavor Chemistry — The Basics",
    photo_credit="Multiple photographers / Unsplash",
), 1, name="cover")

# 2 — Editorial lead: three origins of aroma
save(editorial_lead, dict(
    photo="aroma_lead_handglass",
    kicker="THE SCIENCE OF SMELL",
    headline="Three Layers of Aromas",
    standfirst="Every wine carries three layers of scent — one from the grape, one from fermentation, one from time.",
    items=[
        ("Primary", "Aromas from the grape itself and its first fermentation — fruit, flowers, varietal character.", "item_raspberry"),
        ("Secondary", "Aromas built by the winemaking process itself — yeast, malolactic fermentation, oak.", "item_cream"),
        ("Tertiary", "Aromas that emerge with age — TDN gives aged Riesling its telltale petrol note.", "item_mushroom"),
    ],
    photo_credit="Dorien Beernink / Unsplash",
), 2, name="three_origins")

# 3 — Mosaic breather
save(mosaic, dict(
    kicker="RAW MATERIALS",
    hero_photo="aroma_mosaic_hero_glass",
    small_photos=["aroma_mosaic_grape", "aroma_mosaic_vanilla", "aroma_mosaic_oak"],
    captions={"aroma_mosaic_hero_glass": "Each Bottle is a chemistry experiment that starts in the vineyard and ends in the glass"},
    photo_credit="Steve's photo; Meg von Haartman / Unsplash; Ben Bramhall / Unsplash",
), 3, name="raw_materials")

# 4 — Duel: grape-derived impact compounds (pyrazines / rotundone)
save(duel, dict(
    photos=("aroma_impact_pyrazine", "aroma_impact_rotundone"),
    labels=("PYRAZINES", "ROTUNDONE"),
    kicker="GRAPE-BORN SIGNATURES",
    headline="When One Molecule Runs the Show",
    standfirst="Some aroma compounds skip fermentation and oak entirely — they're already in the grape, and just one is enough to define a wine's character.",
    mode="columns",
    cols=[
        ("Green Pepper", "Marks cool-climate Sauvignon Blanc and Cabernet Sauvignon — grassy, herbaceous, unmistakable."),
        ("Black Pepper", "Found in Syrah and Grüner Veltliner — some tasters detect it at vanishingly low levels, others not at all."),
    ],
    photo_credit="HisArt Photos / Unsplash; Chimpanzeee / Unsplash",
), 4, name="impact_compounds")

# 5 — Duel: fermentation temperature, photos flipped to the bottom
save(duel, dict(
    photos=("aroma_duel_cool", "aroma_duel_warm"),
    labels=("COOL", "WARM"),
    photo_position="bottom",
    kicker="FERMENTATION TEMPERATURE",
    headline="Cooler Ferments Keep the Florals",
    standfirst="Temperature during fermentation is one of the single biggest levers a winemaker has over a wine's aromatics.",
    mode="columns",
    cols=[
        ("12–16°C (54–61°F)", "Cool ferments protect delicate esters — the base for crisp, floral whites."),
        ("20–32°C (68–90°F)", "Warmer ferments extract more color and tannin, pulling darker, riper fruit out of red skins."),
    ],
    photo_credit="Meg von Haartman / Unsplash; Steve's photo",
), 5, name="temperature")

# 6 — Card grid: fermentation's aroma exports
save(card_grid, dict(
    kicker="FERMENTATION'S OTHER EXPORTS",
    top_margin=100,
    headline="Aromas Created During Fermentation",
    standfirst="Fermentation makes its own aroma compounds — some borrowed from the grape, some built from scratch.",
    cards=[
        (None, "Esters", "Banana, pear, tropical fruit", "Formed when fermentation acids meet alcohol — the largest group of aroma compounds in wine."),
        (None, "Thiols", "Passionfruit, grapefruit", "Released from odorless grape precursors by yeast enzymes — Sauvignon Blanc's calling card."),
        (None, "Terpenes", "Muscat, Riesling's perfume", "Grape-derived floral compounds that largely survive fermentation intact."),
        (None, "Higher Alcohols", "Background lift", "Minor fermentation by-products that round out a wine's overall aromatic complexity."),
    ],
    bottom_stripe=["aroma_card_banana", "aroma_card_citrus", "aroma_card_tropical"],
    stripe_captions=["Esters: banana, pear", "Thiols: passionfruit, citrus"],
    photo_credit="Atlantic Ambience; Karolina Kołodziejczak / Unsplash; Nina Ganci / Unsplash",
), 6, name="ferment_exports")

# 7 — Feature trio: MLF / butter, three labeled photos
save(feature_trio, dict(
    kicker="WHERE'S THE BUTTER?",
    headline="Malolactic Fermentation",
    features=[
        ("A. Malic → Lactic", "Bacteria convert the grape's sharp malic acid into softer lactic acid.", "item_milk"),
        ("B. Diacetyl", "A by-product ester of MLF — the compound directly responsible for a buttery aroma.", "aroma_spotlight_butter"),
        ("C. Creamier Texture", "The same conversion softens mouthfeel, not just scent.", "item_woman_wine"),
    ],
    photo_credit="Mehrshad Rajabi / Unsplash; Polina Tankilevitch / Pexels; Steve's photo",
), 7, name="butter_mlf")

# 8 — Horizontal trio: oak / vanilla, three stacked photo bands
save(horizontal_trio, dict(
    kicker="WHERE'S THE VANILLA?",
    headline="Oak's Contribution",
    rows=[
        ("Vanillin", "The same aromatic compound found in vanilla beans — present naturally in oak wood itself.", "aroma_trio_vanilla"),
        ("Species & Grain", "French oak's tight grain gives subtle spice; American oak's looser grain gives bolder vanilla and coconut.", "aroma_trio_oak"),
        ("Toast Level", "Charring the barrel's interior develops toast, smoke, and clove — heavier toast, bolder char.", "aroma_trio_toast"),
    ],
    footnote="New barrels give the most flavor; after about four years, most of a barrel's aromatic compounds have leached out.",
    photo_credit="Steve's photo; Marina Reich / Unsplash; Kris Møklebust / Pexels",
), 8, name="oak_vanilla")

# 9 — Duel: how tertiary aromas develop
save(duel, dict(
    photos=("aroma_tertiary_color", "aroma_tertiary_driedfruit"),
    labels=("TEXTURE", "AROMA"),
    kicker="THE THIRD LAYER",
    headline="What Actually Changes as Wine Ages?",
    standfirst="Tertiary aromas — a wine's bouquet — aren't made by the grape or by fermentation. They're built slowly, in bottle, by two chemical processes working at once.",
    mode="columns",
    cols=[
        ("Tannins & Pigments Polymerize", "Tannin and color molecules link into longer chains and drop out as sediment — the wine softens in the mouth and its color fades from purple toward brick and garnet."),
        ("Slow Oxidation Builds New Aromas", "Tiny amounts of oxygen seep in through the cork over years, slowly forming new compounds — the source of dried fruit, leather, and forest floor notes."),
    ],
    photo_credit="Steve's photo; Mustafa Akın / Unsplash",
), 9, name="tertiary_aromas")

# 10 — Process map: grape to glass (moved to right before the glossary)
save(process_map, dict(
    kicker="FROM VINE TO GLASS",
    headline="Sources of Aromas and Flavors",
    photos=["aroma_process_grape", "aroma_process_tank", "aroma_process_glass"],
    columns=[
        ("In the Grape", [("Aroma precursors form in the skin", False),
                           ("Sugars, acids, and phenolics build as it ripens", False),
                           ("Thiols, terpenes stay bound and scentless", False)]),
        ("During Fermentation", [("Yeast enzymes free the bound aromas", False),
                                  ("New esters form from acids and alcohol", False),
                                  ("Malolactic fermentation adds its own layer", False)]),
        ("In the Glass", [("Volatile molecules evaporate into the air", False),
                           ("Swirling increases surface area and lift", False),
                           ("Body heat releases even more in the mouth", False)]),
    ],
    photo_credit="Renata Kurtveliieva-Berezhna; Meg von Haartman; Mauro Lima / Unsplash",
), 10, name="vine_to_glass")

# 11 — Glossary
save(fact_file, dict(
    photo="aroma_glossary_spices",
    kicker="SPEAK THE LANGUAGE",
    headline="A Short Aroma Glossary",
    facts=[
        ("Diacetyl", "Butter — a by-product of MLF."),
        ("Vanillin & Lactones", "Vanilla and coconut, from oak."),
        ("Furfural", "Toast and smoke, from barrel charring."),
        ("Thiols", "Passionfruit and grapefruit."),
        ("Esters", "Banana and pear."),
        ("Sulfur Compounds", "Struck match — too little oxygen."),
        ("Volatile Phenols", "Barnyard, band-aid — Brettanomyces."),
        ("Acetic Acid", "Vinegar — bacterial spoilage."),
    ],
    photo_credit="Steve's photo",
), 11, name="glossary")

# 12 — Closing
save(statement, dict(
    variant="closing",
    photo="aroma_closing_glass",
    title="Primary, Secondary,\nor Tertiary?",
    subtitle="Next glass, ask which one you're smelling.",
    photo_anchor=0.45,
), 12, name="closing")

pdf_path = f"{OUT}/FieldGuide_AromaChemistry_review.pdf"
core.assemble_pdf(paths, pdf_path)
print("PDF:", pdf_path)
print("PNGs:", paths)
