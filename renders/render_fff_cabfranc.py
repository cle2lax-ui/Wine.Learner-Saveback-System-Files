import os
from fff_facts import fff_cover, fff_fact
import core

OUT = "/home/claude/out_cf"
os.makedirs(OUT, exist_ok=True)

TOTAL = 6
paths = []

# Deck-specific override: matched to the lightest/brightest saturated
# red sampled directly from the cover photo's wine splash (HSV-filtered
# for hue + saturation, averaged over the ~80 brightest matching
# pixels) rather than picked by eye -- overrides only the cover
# subject / fact headlines / "Cheers" -- kicker, numerals, rules, and
# diagram chips stay the series-standard cobalt.
RASPBERRY = (255, 53, 24)

# 1 — Cover
img = fff_cover({
    "photo": "cabfranc_cover",
    "subject": "Cabernet Franc",
    "photo_anchor": 0.45,
    "photo_credit": "Saman Taheri / Unsplash",
}, total=TOTAL, headline_color=RASPBERRY)
p = f"{OUT}/01_cover.png"
img.save(p)
paths.append(p)

# 2 — Fact 1: parentage (diagram removed per feedback -- photo + copy only)
img = fff_fact({
    "photo": "cabfranc_fact1_grapes",
    "number": 1,
    "headline": "Cabernet Sauvignon's Parent, Not Its Sibling",
    "body": "In 1997, UC Davis DNA testing proved Cabernet Sauvignon is a natural cross of Cabernet Franc and Sauvignon Blanc — not the other way around.",
    "photo_anchor": 0.4,
    "photo_credit": "Bonnie Hawkins / Unsplash",
}, slide_no=2, total=TOTAL, headline_color=RASPBERRY)
p = f"{OUT}/02_fact1.png"
img.save(p)
paths.append(p)

# 3 — Fact 2: Breton name
img = fff_fact({
    "photo": "cabfranc_fact2_chateau",
    "number": 2,
    "headline": "Locals Call It an Entirely Different Name",
    "body": "In the Loire Valley, Cabernet Franc goes by “Breton,” honoring the monk credited with bringing the vine to Chinon and Bourgueil.",
    "photo_anchor": 0.42,
    "photo_credit": "Shalev Cohen / Unsplash",
}, slide_no=3, total=TOTAL, headline_color=RASPBERRY)
p = f"{OUT}/03_fact2.png"
img.save(p)
paths.append(p)

# 4 — Fact 3: chameleon aromatics
img = fff_fact({
    "photo": "cabfranc_fact3_grapes2",
    "number": 3,
    "headline": "The Same Grape, Two Different Personalities",
    "body": "Cool climates coax out cranberry, bell pepper, and tea; warm ones bring raspberry and violet — same variety, opposite character.",
    "photo_anchor": 0.45,
    "photo_credit": "JOGphotos / Unsplash",
}, slide_no=4, total=TOTAL, headline_color=RASPBERRY)
p = f"{OUT}/04_fact3.png"
img.save(p)
paths.append(p)

# 5 — Fact 4: minor in Bordeaux, star in Loire
img = fff_fact({
    "photo": "cabfranc_fact4_rivervineyard",
    "number": 4,
    "headline": "A Minor Player in Bordeaux, a Star in the Loire",
    "body": "Cabernet Franc is a supporting blender in Bordeaux, but in Chinon and Bourgueil, it's nearly the only grape allowed in the glass.",
    "photo_anchor": 0.45,
    "photo_credit": "Patrick Langwallner / Unsplash",
}, slide_no=5, total=TOTAL, headline_color=RASPBERRY)
p = f"{OUT}/05_fact4.png"
img.save(p)
paths.append(p)

# 6 — Fact 5 + Cheers close
img = fff_fact({
    "photo": "cabfranc_fact5_rose",
    "number": 5,
    "headline": "It's More Than Just a Red Wine Grape",
    "body": "Beyond still reds, Cabernet Franc is a key player in Loire rosés and traditional-method sparkling wines, sold as Fines Bulles.",
    "photo_anchor": 0.5,
    "photo_credit": "Jameson Berrios / Unsplash",
}, slide_no=6, total=TOTAL, closing=True, headline_color=RASPBERRY)
p = f"{OUT}/06_fact5_cheers.png"
img.save(p)
paths.append(p)

pdf_path = f"{OUT}/FFFA_CabernetFranc_review.pdf"
core.assemble_pdf(paths, pdf_path)
print("PDF:", pdf_path)
print("PNGs:", paths)
