import sys
sys.path.insert(0, "/home/claude/styleguide")
from tokens import DEFAULT_PALETTE
from guess_the_region import gtr_cover, gtr_reveal

pal_cover = dict(DEFAULT_PALETTE)
pal_cover["ACCENT"] = (200, 16, 46)  # NZ flag red, per-deck override for page 1

pal = dict(DEFAULT_PALETTE)
pal["ACCENT"] = (196, 158, 84)  # series gold, fixed across all GTR decks (page 2 unchanged)

slot1 = dict(
    photo="clue_marlborough_sounds",
    panel_bg=(0, 36, 125),  # NZ flag blue
    title_color=(255, 255, 255),  # title white; clue letters/swipe cue stay red via ACCENT
    clues=[
        "It sits on a Pacific nation's South Island tip.",
        "First planted in 1973, it built a pungent style.",
        "Two valleys, split by low hills, differ in style.",
        "Named for a British duke, it tastes purely Pacific.",
    ],
    photo_credit="Photo: Petra Reid, Pexels",
)

slot2 = dict(
    photo="reveal_marlborough_vineyard",
    region="Marlborough",
    flag="nz",
    caption="Vine rows on wire trellising, backed by clay-loam hill country",
    blurb=("Marlborough is New Zealand's largest wine region, its stony soils and cool "
           "Pacific climate built for bright acidity. Cloudy Bay's mid-1980s arrival turned "
           "its pungent Sauvignon Blanc into a global benchmark, though Pinot Noir and "
           "sparkling wine thrive here too."),
    photo_credit="Photo: Mitchell Henderson, Pexels",
)

img1 = gtr_cover(slot1, 1, 2, pal_cover)
img1.save("/mnt/user-data/outputs/gtr_marlborough_p1.png")

img2 = gtr_reveal(slot2, 2, 2, pal)
img2.save("/mnt/user-data/outputs/gtr_marlborough_p2.png")

from core import assemble_pdf
pdf_path = assemble_pdf(
    ["/mnt/user-data/outputs/gtr_marlborough_p1.png", "/mnt/user-data/outputs/gtr_marlborough_p2.png"],
    "/mnt/user-data/outputs/GTR_Marlborough.pdf",
)
print(f"REVIEW PDF -> {pdf_path}")
print("done")
