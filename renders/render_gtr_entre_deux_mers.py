import sys
sys.path.insert(0, "/home/claude/styleguide")
from tokens import DEFAULT_PALETTE
from guess_the_region import gtr_cover, gtr_reveal

pal = dict(DEFAULT_PALETTE)
pal["ACCENT"] = (196, 158, 84)  # series gold, contrasting against photo/panel

slot1 = dict(
    photo="entre_deux_mers_bistro_door",
    clues=[
        "Its namesake AOC allows white wines only.",
        "Enclaves inside it make red and sweet wine too.",
        "Clay-limestone soils between two tidal rivers.",
        "Its name means “between two seas.”",
    ],
    photo_credit=None,
)

slot2 = dict(
    photo="entre_deux_mers_gironde_aerial",
    region="Entre-Deux-Mers",
    caption="Where the Garonne and Dordogne meet to form the Gironde estuary",
    blurb=("Entre-Deux-Mers is the clay-limestone country between Bordeaux's two rivers, "
           "home to eight separate AOCs. Only its own namesake appellation is reserved "
           "for dry white wine, blended from Sauvignon Blanc, Sémillon, and Muscadelle."),
    photo_credit="Photo: Lantus, CC BY-SA 3.0",
)

img1 = gtr_cover(slot1, 1, 2, pal)
img1.save("/mnt/user-data/outputs/gtr_entre_deux_mers_p1.png")

img2 = gtr_reveal(slot2, 2, 2, pal)
img2.save("/mnt/user-data/outputs/gtr_entre_deux_mers_p2.png")

print("done")
