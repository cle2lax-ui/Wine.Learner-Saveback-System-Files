"""FFFA — South Australia. Photos: Wikimedia Commons (CC BY / CC BY-SA)."""
import os
from fff_facts import fff_cover, fff_fact

OUT = "/home/claude/out_south_australia"
os.makedirs(OUT, exist_ok=True)
TOTAL = 6
paths = []

# 1 — Cover
img = fff_cover({
    "photo": "fffa_sa_cover",
    "subject": "South Australia",
    "photo_anchor": 0.55,
    "photo_credit": "Olivier Lemoine / Wikimedia Commons (CC BY-SA 4.0)",
}, total=TOTAL)
p = f"{OUT}/01_cover.png"; img.save(p); paths.append(p)

# 2 — Fact 1: phylloxera-free
img = fff_fact({
    "photo": "fffa_sa_fact1_ownroots",
    "number": 1,
    "headline": "The Pest That Never Made It Here",
    "body": ("Phylloxera razed Europe's vineyards, and eastern Australia's. Quarantine "
             "kept it out \u2014 these vines still stand on their own roots."),
    "photo_anchor": 0.48,
    "photo_credit": "Stephan Ridgway / Wikimedia Commons (CC BY 2.0)",
}, slide_no=2, total=TOTAL)
p = f"{OUT}/02_fact1.png"; img.save(p); paths.append(p)

# 3 — Fact 2: 1843 Shiraz
img = fff_fact({
    "photo": "fffa_sa_fact2_barossasea",
    "number": 2,
    "headline": "Its Oldest Shiraz Predates the Gold Rush",
    "body": ("Langmeil's Freedom Vineyard, planted in the Barossa in 1843, still bears "
             "fruit \u2014 among the oldest producing Shiraz anywhere."),
    "photo_anchor": 0.78,
    "photo_zoom": 1.45,
    "photo_credit": "Olivier Lemoine / Wikimedia Commons (CC BY-SA 4.0)",
}, slide_no=3, total=TOTAL)
p = f"{OUT}/03_fact2.png"; img.save(p); paths.append(p)

# 4 — Fact 3: half the country's wine
img = fff_fact({
    "photo": "fffa_sa_fact3_barrels",
    "number": 3,
    "headline": "One State Makes Half the Country's Wine",
    "body": ("Roughly half the national crush, and some 80 percent of Australia's "
             "premium wine, comes from one state."),
    "photo_anchor": 0.52,
    "photo_credit": "Olivier Lemoine / Wikimedia Commons (CC BY-SA 4.0)",
}, slide_no=4, total=TOTAL)
p = f"{OUT}/04_fact3.png"; img.save(p); paths.append(p)

# 5 — Fact 4: Coonawarra terra rossa
img = fff_fact({
    "photo": "fffa_sa_fact4_terrarossa",
    "number": 4,
    "headline": "A Two-Kilometre Strip of Dirt Built a Legacy",
    "body": ("Coonawarra's terra rossa \u2014 iron-red loam over limestone \u2014 runs "
             "27 kilometres by two, and sets the Cabernet benchmark."),
    "photo_anchor": 0.66,
    "photo_zoom": 1.40,
    "photo_credit": "Alpha / Wikimedia Commons (CC BY-SA 2.0)",
}, slide_no=5, total=TOTAL)
p = f"{OUT}/05_fact4.png"; img.save(p); paths.append(p)

# 6 — Fact 5 + Cheers close
img = fff_fact({
    "photo": "fffa_sa_fact5_oldvines",
    "number": 5,
    "headline": "Some Vines Hold an Official Rank",
    "body": ("Old at 35 years, Survivor at 70, Centenarian at 100, Ancestor at 125 "
             "\u2014 the Barossa Old Vine Charter."),
    "photo_anchor": 0.62,
    "photo_credit": "Stephan Ridgway / Wikimedia Commons (CC BY 2.0)",
}, slide_no=6, total=TOTAL, closing=True)
p = f"{OUT}/06_fact5_cheers.png"; img.save(p); paths.append(p)

import core
pdf_path = f"{OUT}/FFFA_SouthAustralia_review.pdf"
core.assemble_pdf(paths, pdf_path)
print("PDF:", pdf_path)
