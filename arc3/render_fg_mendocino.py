"""FIELD GUIDE: MENDOCINO (Arc 3, post 1). First deck in Field Guide v2 (the Reel's visual language),
theme: usa. Pages so far: 1 cover, 2 the AVA map, 3 two climates -- the style proof for Steve's
approval before the rest of the deck is built.

SOURCES (DESIGN_PROCESS_v8 s12: WSET first)
  D3 Ch. 23.1 (North Coast: Mendocino and Lake Counties): about 7,000 ha under vine in a county of about
    one million ha; cooler AVAs near the Pacific (Anderson Valley: Pinot Noir, Chardonnay, aromatic whites)
    and warmer inland AVAs (Redwood Valley: Zinfandel, Syrah, Petite Sirah, Cabernet Sauvignon), while
    high inland Potter Valley grows Sauvignon Blanc and Riesling; the Mendocino AVA covers six AVAs;
    Anderson Valley is the best known.
  CSW Study Guide: about 17,000 acres of vineyards (the acre figure for US readers; it agrees with D3's ha).
  TTB (current): 12 AVAs wholly within the county plus Pine Mountain-Cloverdale Peak, shared with Sonoma.
    D3's own count (12) predates Comptche (2024); see arc3/ARC3_MENDOCINO_PLAN.md.
MAP DATA: UC Davis AVA Project (CC0); counties from US Census boundaries (public domain). Comptche drawn as
  the TTB defines it (outside the North Coast AVA), not as the UC Davis 'within' field says.
PHOTOS (Wikimedia Commons, location in the uploader's title): cover, 'Hillside Vineyards in Anderson Valley',
  Naotake Murayama, CC BY 2.0; page 3 top, 'Vineyard in Anderson Valley', Naotake Murayama, CC BY 2.0; page 3
  bottom, 'Garzini vineyard mendocino ca', CC0. The bottom panel is headed INLAND AVAs, not with a specific
  AVA's name, because the photo's exact location within the county is not stated.
"""
import glob
import os
import sys

os.environ.setdefault("AMERICAN_ENGLISH", "1")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
for _p in (f"{ROOT}/engine", f"{ROOT}/formats", f"{ROOT}/reels"):
    sys.path.insert(0, _p)
import core                      # noqa: E402
from fg_v2 import ava_map, cover, split   # noqa: E402
from themes import theme         # noqa: E402

OUT = "/home/claude/out_fg_mendocino"
os.makedirs(OUT, exist_ok=True)
TH = theme("usa")
TOTAL = 10                       # provisional: the full outline is 10 pages
GEO = f"{ROOT}/data/geo"

COVER = dict(
    photo="us_mendo_av_hillside_murayama.jpg", anchor=0.72,
    kicker="CALIFORNIA \u00b7 NORTH COAST", title="MENDOCINO",
    subtitle="Anderson Valley and its neighbors",
    credit="Naotake Murayama / Wikimedia Commons (CC BY 2.0)",
)

MAP = dict(
    chip="THE PLACE",
    headline=("TWELVE AVAs.", "ONE FAMOUS VALLEY."),
    subline="Plus Pine Mountain\u2013Cloverdale Peak, shared with Sonoma.",
    avas=f"{GEO}/mendocino_avas.geojson", counties=f"{GEO}/mendocino_counties.geojson", state=f"{GEO}/california.geojson",
    county="Mendocino", parent="Mendocino", focus="Anderson Valley", skip=("North Coast",),
    styles={"Mendocino": "parent", "Anderson Valley": "focus", "Mendocino Ridge": "ridge"},
    ridge_color=(110, 118, 200), ridge_label=(150, 160, 236),
    # map centered, a label column on EACH side (western AVAs labeled over the Pacific); see fg_v2.ava_map
    map_box=(700, 900, 1460, 2140),
    columns=dict(left_x=650, right_x=1510),
    label_top=930, label_bottom=2120, leader_max=420,
    labels={
        "Covelo": "Covelo", "Dos Rios": "Dos Rios", "Eagle Peak Mendocino County": "Eagle Peak",
        "Potter Valley": "Potter Valley", "Redwood Valley": "Redwood Valley", "Comptche": "Comptche (2024)",
        "Mendocino": "Mendocino AVA\ncovers six of these", "Mendocino Ridge": "Mendocino Ridge",
        "McDowell Valley": "McDowell Valley", "Cole Ranch": "Cole Ranch", "Anderson Valley": "Anderson Valley",
        "Yorkville Highlands": "Yorkville Highlands", "Pine Mountain-Cloverdale Peak": "Pine Mountain\u2013\nCloverdale Peak",
    },
    inset_box=(1700, 250, 2040, 640), inset_label="CALIFORNIA",
    stat_xy=(120, 2450),
    stat=dict(big="7,000 ha", unit="UNDER VINE", lines=["about 17,000 acres, in a county", "of about one million hectares"]),
    credit="AVA boundaries: UC Davis AVA Project (CC0) \u00b7 counties: US Census",
)

CLIMATES = dict(
    chip="TWO CLIMATES",
    top=dict(photo="us_mendo_av_vineyard_murayama.jpg", anchor=0.62, kicker="COOLER \u00b7 NEAR THE PACIFIC",
             kicker_color=(160, 186, 240), heading="ANDERSON VALLEY",
             chips=[("PINOT NOIR", "red"), ("CHARDONNAY", "white"), ("AROMATIC WHITES", "white")]),
    bottom=dict(photo="us_mendo_garzini_cc0.jpg", anchor=0.55, kicker="WARMER \u00b7 FURTHER INLAND",
                kicker_color=(240, 150, 140), heading="INLAND AVAs",
                chips=[("ZINFANDEL", "red"), ("SYRAH", "red"), ("PETITE SIRAH", "red"), ("CABERNET SAUVIGNON", "red")]),
    cold=(70, 110, 210), warm=(205, 50, 60), strip_left="PACIFIC", strip_right="INLAND",
    twist=("Altitude flips it: high, inland Potter Valley", "grows Sauvignon Blanc and Riesling."),
    credit="Naotake Murayama (CC BY 2.0); No-till-vineyard (CC0) / Wikimedia Commons",
)


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)
    pages = [cover(COVER, TH, TOTAL), ava_map(MAP, TH, TOTAL, 2), split(CLIMATES, TH, TOTAL, 3)]
    paths = []
    for i, im in enumerate(pages, 1):
        p = f"{OUT}/{i:02d}.png"
        im.save(p)
        paths.append(p)
    core.assemble_pdf(paths, f"{OUT}/FG_Mendocino_style_proof.pdf")
    print("PDF:", f"{OUT}/FG_Mendocino_style_proof.pdf")


if __name__ == "__main__":
    build()
