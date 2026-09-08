import sys
sys.path.insert(0, "/home/claude/styleguide")
from tokens import DEFAULT_PALETTE
from guess_the_region import gtr_cover, gtr_reveal

pal = dict(DEFAULT_PALETTE)
pal["ACCENT"] = (196, 158, 84)    # series gold, fixed across all GTR decks
pal["SIGNATURE"] = (114, 47, 55)  # burgundy/claret for region name, per GTR_STYLE_GUIDE.md \u00a75

slot1 = dict(
    photo="gtr_mclarenvale_clue_bushvine",
    photo_anchor=0.2,
    photo_x_anchor=0.7,
    clues=[
        "Shiraz alone makes up half of what grows here.",
        "Sea breezes off a gulf cool this warm climate.",
        "More than 40 soil types sit within one small region.",
        "Its Grenache bush vines can be over a century old.",
    ],
    photo_credit="Photo: Ra\u00fal Mermans Garc\u00eda, Unsplash",
    panel_bg=(255, 255, 255),    # white panel, per feedback -- navy title was
                                   # unreadable against the old black panel
    title_color=(1, 33, 105),    # Australian flag navy
    letter_color=(228, 0, 43),   # Australian flag red
    swipe_color=(1, 33, 105),    # Australian flag navy
    icon_color=(1, 33, 105),     # navy -- was PAPER/white, invisible on white
    clue_text_color=(38, 33, 38),  # INK -- was PAPER/white, invisible on white
)

slot2 = dict(
    photo="gtr_mclarenvale_reveal_cube",
    photo_h=int(2700 * 0.55),  # reframed shorter than the 0.66 default to give the
                                # bottom panel more room -- lets the blurb's auto-shrink
                                # loop land at the full 84px size instead of shrinking to 62
    blurb_size=78,   # a few pt down from the 84 default, per feedback
    blurb_leading=0.88,  # tighter line spacing, down from the 0.98 default
    region="McLaren Vale",
    flag="australian",
    caption="The d'Arenberg Cube among the vineyard rows",
    blurb=("McLaren Vale sits on South Australia's Fleurieu Peninsula, cooled "
           "by sea breezes off Gulf St Vincent. Vines have grown here since "
           "1838, some of its Grenache bush vines over a century old. Its "
           "own name is disputed \u2014 some credit David McLaren, the colony's "
           "manager, others John McLaren, the surveyor who mapped the area "
           "in 1839, two unrelated men who happened to share a surname."),
    photo_credit="Photo: Tom Kennedy, Unsplash",
)

img1 = gtr_cover(slot1, 1, 2, pal)
img1.save("/mnt/user-data/outputs/gtr_mclarenvale_p1.png")

img2 = gtr_reveal(slot2, 2, 2, pal)
img2.save("/mnt/user-data/outputs/gtr_mclarenvale_p2.png")

from core import assemble_pdf
pdf_path = assemble_pdf(
    ["/mnt/user-data/outputs/gtr_mclarenvale_p1.png", "/mnt/user-data/outputs/gtr_mclarenvale_p2.png"],
    "/mnt/user-data/outputs/GTR_McLarenVale.pdf",
)
print(f"REVIEW PDF -> {pdf_path}")
print("done")
