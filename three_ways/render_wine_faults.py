import sys
sys.path.insert(0, "/home/claude/styleguide")
from tokens import DEFAULT_PALETTE
from modules import (statement, editorial_lead, card_grid, spotlight, duel,
                      ladder, lexicon_cloud, feature_trio, fact_file, side_rail)

pal = dict(DEFAULT_PALETTE)
TOTAL = 11
slides = []

# 1 — Cover
slides.append((statement, dict(
    variant="cover",
    photo="faults_cover",
    photo_anchor=0.28,
    title="Wine Faults",
    title_size=260,
    block_frac=0.38,
    subtitle="Sometimes, Things Just Go Wrong…",
    photo_credit="Photo: cottonbro studio, Pexels",
)))

# 2 — Editorial lead / intro
slides.append((editorial_lead, dict(
    photo="faults_intro_swirl_band",
    kicker="FIELD NOTES",
    headline="When Good Wine Goes Rogue",
    standfirst=("A wine's aroma comes from the grapes, fermentation, aging, or oak — but "
                "errors, poor storage, or bad luck can sneak in too. Spotting them is a "
                "skill, not a failure of taste."),
    standfirst_gap=90,
    item_gap=80,
    items=[
        ("Not Shameful.", "These off-notes turn up even at serious wineries — recognizing them is part of wine literacy."),
        ("Not Always Fatal.", "Some faults are subtle and only mute a wine's flavor rather than ruin it outright."),
        ("Not Always Universal.", "The very same aroma can be a flaw in one wine and a hallmark of style in another."),
    ],
    photo_credit="Photo: Jana Ohajdova, Pexels",
)))

# 3 — Card grid: the three families
slides.append((card_grid, dict(
    kicker="THE LINEUP",
    headline="Three Ways Wine Goes Wrong",
    standfirst="Nearly every off-aroma in this deck traces back to one of three sources.",
    row_layout=[3],
    photo_style="top",
    cards=[
        ("faults_card_cork", "Cork Taint", "TCA & Friends",
         "A musty, moldy odor from a compound that can infect corks, barrels, or the winery itself."),
        ("faults_card_sulfur", "Sulfur Compounds", "SO₂ & Friends",
         "Burnt matches, rotten eggs, or garlic — sulfur is essential to winemaking until there's too much."),
        ("faults_card_microbial", "Bacteria", "The Acid Trio",
         "Wine's toughest bacteria turn sugar, alcohol, or acid into vinegar, rancid butter, or sauerkraut."),
    ],
)))

# 4 — TCA fact file
slides.append((fact_file, dict(
    photo="faults_tca_hero",
    kicker="FAULT FILE · TCA",
    headline="Cork Taint, Unmasked",
    facts=[
        ("Full Name", "2,4,6-Trichloroanisole — TCA for short."),
        ("The Culprit", "A mold on cork bark — or in the winery itself — reacts with other compounds to form it."),
        ("The Smell", "A musty, moldy odor, like a dank basement. Milder cases just taste muted and less fruity."),
        ("The Threshold", "Most people detect it at just 2 to 7 parts per trillion — an extremely low bar."),
        ("How Common?", "Estimates run from 1% to 8% of all bottles produced each year — no consensus figure exists."),
    ],
    photo_credit="Photo: Stas Knop, Pexels",
)))

# 5 — Duel: Reduction vs Oxidation
slides.append((duel, dict(
    photos=["faults_duel_reduction", "faults_duel_oxidation"],
    labels=["REDUCTION", "OXIDATION"],
    kicker="OPPOSITE ENDS OF THE SPECTRUM",
    headline="Too Little Air vs. Too Much",
    standfirst="Redox chemistry sits behind two very different, very opposite faults.",
    mode="table",
    col_heads=["REDUCTION", "OXIDATION"],
    rows=[
        ("Cause", "Wine sits too long with no oxygen — often sediment at the bottom of a sealed vessel.",
         "Oxygen dissolves into wine and reacts with its phenolic compounds."),
        ("Smells Like", "Rotten eggs, garlic, struck matches, or burnt rubber.",
         "Nutty, caramelized notes — desirable in Sherry, a flaw almost anywhere else."),
        ("Watch For", "Cabbage-like aromas as concentration builds.",
         "Browning color and a fading fruit character."),
    ],
    photo_credit="Photos: ROCCO STOPPOLONI; Andrew Schwark, Pexels",
)))

# 6 — Ladder: Fault or Feature
slides.append((ladder, dict(
    kicker="CONTEXT IS EVERYTHING",
    headline="Fault… or Feature?",
    standfirst="The same aroma can be condemned in one glass and celebrated in the next.",
    bg_photo="faults_ladder_cellar",
    tiers=[
        ("Yeasty or Leesy", "Expected in bubbly."),
        ("A Touch of Brett", "Some love it. Others won't touch it."),
        ("Maderization", "A flaw — unless it's literally Madeira."),
        ("TCA / Cork Taint", "Never acceptable. No exceptions, ever."),
    ],
)))

# 7 — Lexicon cloud
slides.append((lexicon_cloud, dict(
    kicker="FIELD NOTES",
    headline="The Fault Vocabulary",
    terms=[
        ("Corked", 80, "TCA, musty basement"),
        ("Reductive", 78, "rotten egg, struck match"),
        ("Volatile Acidity", 76, "vinegar-like sourness"),
        ("Acescence", 74, "the vinegar-spoilage process"),
        ("Wet Cardboard", 72, "papery, filter-related"),
        ("Maderized", 70, "cooked, baked odor"),
        ("Barnyard", 70, "earthy, Brett-associated note"),
        ("Mercaptan", 68, "garlic or onion"),
        ("Green", 66, "underripe grape aroma"),
        ("Moldy", 66, "moldy grapes or barrels"),
        ("Rubbery", 64, "low acid, excess sulfur"),
        ("Stagnant", 64, "stale water odor"),
        ("Stemmy", 64, "bitter, green stems"),
    ],
)))

# 8 — Feature trio: bacterial faults
slides.append((feature_trio, dict(
    kicker="BACTERIA'S CALLING CARDS",
    headline="The Bacterial Trio",
    features=[
        ("Acetic Acid", "The smell of vinegar — acetobacter converting alcohol into acetic acid.", "faults_feature_acetic"),
        ("Butyric Acid", "Rancid butter or spoiled cheese, a sign lactic bacteria have gone too far.", "faults_feature_butyric"),
        ("Lactic Acid", "Sauerkraut, or wet goat — malolactic fermentation's less charming cousin.", "faults_feature_lactic_goat"),
    ],
    footnote="Most bacteria can't survive wine's acidity — lactic bacteria and acetobacter are the rare exceptions that can.",
    photo_credit="Photos: horst; Felicity Tai; Denys Gromov, Pexels",
)))

# 9 — Brett fact file
slides.append((fact_file, dict(
    photo="faults_brett_horse",
    kicker="FAULT FILE · BRETTANOMYCES",
    headline="Meet Brett",
    facts=[
        ("Full Name", "Brettanomyces — a wild yeast, not a bacteria."),
        ("Descriptors", "“Sweaty,” “horsy,” “Band-Aid-like,” or medicinal."),
        ("At Low Levels", "Some tasters embrace a touch of Brett as complexity."),
        ("At High Levels", "Others consider any amount of Brett a dealbreaker."),
        ("The Real Effect", "Often it just deadens a wine's primary fruit flavors."),
    ],
    photo_credit="Photo: Afitab, Pexels",
)))

# 10 — Side rail: corked wine service
slides.append((side_rail, dict(
    photo="faults_siderail_sommelier",
    side="left",
    kicker="AT THE TABLE",
    headline="Your Wine Is Corked.\nNow What?",
    standfirst="Formal service still follows a ritual centuries old — here's how it plays out.",
    items=[
        ("The Pour.", "The server pours a small taste, 1 to 2 ounces, for the host to evaluate first."),
        ("The Tell.", "A musty, wet-cardboard smell means cork taint. A sharp vinegar note means volatile acidity."),
        ("The Fix.", "Flag it without confrontation — a good restaurant swaps the bottle, no drama required."),
    ],
    photo_credit="Photo: Filipp Romanovski, Pexels",
)))

# 11 — Closing
slides.append((statement, dict(
    variant="closing",
    photo="faults_closing_sommelier",
    photo_anchor=0.35,
    title="Context Is Everything",
    subtitle="Context decides fault versus character.",
    photo_credit="Photo: Pavel Danilyuk, Pexels",
)))

import os
from core import assemble_pdf
os.makedirs("/mnt/user-data/outputs/wine_faults", exist_ok=True)
paths = []
for i, (fn, slot) in enumerate(slides, start=1):
    img = fn(slot, i, TOTAL, pal)
    path = f"/mnt/user-data/outputs/wine_faults/faults_{i:02d}.png"
    img.save(path)
    paths.append(path)
    print(f"slide {i:2d} saved -> {path}")

pdf_path = assemble_pdf(paths, "/mnt/user-data/outputs/wine_faults/Wine_Faults.pdf")
print(f"REVIEW PDF -> {pdf_path}")
print("ALL DONE")
