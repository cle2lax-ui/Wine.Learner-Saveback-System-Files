import os
from fff_facts import fff_cover, fff_fact

OUT = "/home/claude/out_south_australia"
os.makedirs(OUT, exist_ok=True)

TOTAL = 6
paths = []

# 1 -- Cover
img = fff_cover({
    "photo": "gtr_mclarenvale_reveal_cube",
    "subject": "South Australia",
    "photo_anchor": 0.35,
    "photo_credit": "Tom Kennedy / Unsplash",
}, total=TOTAL)
p = f"{OUT}/01_cover.png"
img.save(p)
paths.append(p)

# 2 -- Fact 1: phylloxera-free
img = fff_fact({
    "photo": "gtr_mclarenvale_clue_bushvine",
    "number": 1,
    "headline": "The Pest That Never Made It Here",
    "body": ("Phylloxera wiped out vineyards across Europe, the Americas, and "
             "even eastern Australia in the 1800s. Strict quarantine has kept "
             "South Australia's vines free of it to this day, still growing "
             "on their own original roots."),
    "photo_anchor": 0.4,
    "photo_credit": "Ra\u00fal Mermans Garc\u00eda / Unsplash",
}, slide_no=2, total=TOTAL)
p = f"{OUT}/02_fact1.png"
img.save(p)
paths.append(p)

# 3 -- Fact 2: Langmeil 1843 Shiraz
img = fff_fact({
    "photo": "fffa_sa_photo_fact2_vinerows",
    "number": 2,
    "headline": "Its Oldest Shiraz Predates the Gold Rush",
    "body": ("Barossa Valley's Langmeil Freedom Vineyard has Shiraz vines "
              "planted in 1843, still bearing fruit today \u2014 among the "
              "oldest continuously producing Shiraz vines on Earth."),
    "photo_anchor": 0.5,
    "photo_credit": "Elijah Johansson / Pexels",
}, slide_no=3, total=TOTAL)
p = f"{OUT}/03_fact2.png"
img.save(p)
paths.append(p)

# 4 -- Fact 3: half the country's wine
img = fff_fact({
    "photo": "fffa_sa_photo_fact3_estate",
    "number": 3,
    "headline": "One State Makes Half the Country's Wine",
    "body": ("South Australia produces roughly half of Australia's total "
              "wine and about 80% of its premium wine \u2014 despite being "
              "just one of the country's six states."),
    "photo_anchor": 0.45,
    "photo_credit": "Fl\u00e1via Vicentini / Pexels",
}, slide_no=4, total=TOTAL)
p = f"{OUT}/04_fact3.png"
img.save(p)
paths.append(p)

# 5 -- Fact 4: Coonawarra terra rossa
img = fff_fact({
    "photo": "fffa_sa_photo_fact4_aerial",
    "number": 4,
    "headline": "A 2-Kilometre Strip of Dirt Built a Legacy",
    "body": ("Coonawarra's famous terra rossa \u2014 red clay over limestone "
              "\u2014 runs just 27 kilometres long and 2 wide, yet it's the "
              "benchmark for Australian Cabernet Sauvignon."),
    "photo_anchor": 0.5,
    "photo_credit": "Tobias Reinert / Pexels",
}, slide_no=5, total=TOTAL)
p = f"{OUT}/05_fact4.png"
img.save(p)
paths.append(p)

# 6 -- Fact 5 + Cheers close: Barossa Old Vine Charter
img = fff_fact({
    "photo": "fffa_sa_photo_fact5_toast",
    "number": 5,
    "headline": "Some Vines Have Their Own Official Titles",
    "body": ("The Barossa Old Vine Charter ranks vineyards by age \u2014 Old "
              "(35+), Survivor (70+), Centenarian (100+), and Ancestor "
              "(125+ years) \u2014 a formal register for vines that refuse "
              "to quit."),
    "photo_anchor": 0.45,
    "photo_credit": "Valeria Boltneva / Pexels",
}, slide_no=6, total=TOTAL, closing=True)
p = f"{OUT}/06_fact5_cheers.png"
img.save(p)
paths.append(p)

import core
pdf_path = f"{OUT}/FFFA_SouthAustralia_review.pdf"
core.assemble_pdf(paths, pdf_path)
print("PDF:", pdf_path)
print("PNGs:", paths)
