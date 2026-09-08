import os
from fff_facts import fff_cover, fff_fact
import core

OUT = "/home/claude/out"
os.makedirs(OUT, exist_ok=True)

TOTAL = 6
paths = []

# 1 — Cover
img = fff_cover({
    "photo": "fff_cover",
    "subject": "Champagne",
    "photo_anchor": 0.42,
    "photo_credit": "Ntsikelelo Radebe / Pexels",
}, total=TOTAL)
p = f"{OUT}/01_cover.png"
img.save(p)
paths.append(p)

# 2 — Fact 1
img = fff_fact({
    "photo": "fff_fact1_risingbubbles",
    "number": 1,
    "headline": "The English Perfected the Bubbles",
    "body": "English merchants first added sugar deliberately, triggering the wine's second fermentation — a technique the Champenois later perfected.",
    "photo_anchor": 0.78,
    "photo_credit": "Heather Smith / Pexels",
}, slide_no=2, total=TOTAL)
p = f"{OUT}/02_fact1.png"
img.save(p)
paths.append(p)

# 3 — Fact 2
img = fff_fact({
    "photo": "fff_fact2_bottle",
    "number": 2,
    "headline": "Every Big Bottle Has a Royal Name",
    "body": "Champagne's oversized formats are named for Old Testament kings, largest to smallest — Nebuchadnezzar holds twenty standard bottles.",
    "photo_anchor": 0.4,
    "photo_credit": "Sleurink .JPEG / Pexels",
}, slide_no=3, total=TOTAL, diagram="bottle_sizes")
p = f"{OUT}/03_fact2.png"
img.save(p)
paths.append(p)

# 4 — Fact 3
img = fff_fact({
    "photo": "fff_fact4_vineyard",
    "number": 3,
    "headline": "The Houses Barely Own the Land",
    "body": "Champagne's famous houses produce two-thirds of the region's wine but own just a tenth of the vineyards.",
    "photo_anchor": 0.5,
    "photo_credit": "Dylan Valente / Unsplash",
}, slide_no=4, total=TOTAL)
p = f"{OUT}/04_fact3.png"
img.save(p)
paths.append(p)

# 5 — Fact 4
img = fff_fact({
    "photo": "fff_fact4_cellar",
    "number": 4,
    "headline": "Rome Built Champagne's Cellars, By Accident",
    "body": "Roman-era chalk quarries under Champagne became its cellars, holding bottles at a near-constant cool temperature and humidity year-round.",
    "photo_anchor": 0.5,
    "photo_credit": "Wes Guild / Pexels",
}, slide_no=5, total=TOTAL)
p = f"{OUT}/05_fact4.png"
img.save(p)
paths.append(p)

# 6 — Fact 5 + Cheers close
img = fff_fact({
    "photo": "fff_fact5_toast",
    "number": 5,
    "headline": "Champagne Has Seven Levels of Sweetness",
    "body": "Dosage runs seven official levels, bone-dry Brut Nature to lush Doux — yet Brut, in the middle, is by far the best-selling style.",
    "photo_anchor": 0.42,
    "photo_credit": "cottonbro studio / Pexels",
}, slide_no=6, total=TOTAL, closing=True, diagram="sweetness")
p = f"{OUT}/06_fact5_cheers.png"
img.save(p)
paths.append(p)

pdf_path = f"{OUT}/FFFA_Champagne_review.pdf"
core.assemble_pdf(paths, pdf_path)
print("PDF:", pdf_path)
print("PNGs:", paths)
