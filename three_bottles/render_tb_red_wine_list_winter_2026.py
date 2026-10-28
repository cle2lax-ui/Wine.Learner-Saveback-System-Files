"""THREE BOTTLES -- "Wade and Eric's Winter 2026 / 2027 Red Wine List" (Steve's kicker). One slide, 2160x2700, built on showcase_shelf.

THE THREE BOTTLES (Steve's picks and photos): Catena Malbec High Mountain Vines 2024 (Steve chose the 2024 over the 2023, which Binny's no longer has),
Sanford Pinot Noir Sanford & Benedict Vineyard 2022, Carlo Giacosa Barbaresco 2021.
TITLE: "Eric and Wade's Winter 2026 / 2027 Red Wine List" sits in the logo patch beside the glass icon (Steve); there is no kicker. Off-white page. Critics are
spelled out in 40 px (below the floor with Steve's sign-off), one score per line; no abbreviation key.

SCORES (each must name the critic and match the vintage on the bottle -- QUICK_SIPS_STYLE_GUIDE):
  Catena 2024      Vinous 92 (James Hidalgo, March 2026; Binny's tags the 2024 at 92 too). NOT featured: a James Suckling 91 for the 2024 appears on two
                   retailer pages only, unconfirmed on jamessuckling.com (paywalled).
  Sanford 2022     Wine Advocate 94; Vinous 94 (both as listed on Wine.com for the 2022 Sanford & Benedict Vineyard).
  Giacosa 2021     Wine Enthusiast 93 (Kerin O'Keefe); Wine Spectator 92 (April 2025, as listed by K&L).

TASTING NOTES (critic language, shortened; the Giacosa's "dog rose" is "rose" at Steve's direction):
  Catena    Vinous: "expressive red fruit, a touch of fresh plum, a faint balsamic note and violets ... juicy and agile with integrated freshness".
  Sanford   Vinous: "Floral and savory overtones meld into a core of red/purplish fruit."
  Giacosa   Wine Enthusiast: scents of botanical herb, hay, dog rose, camphor and spice; flavors of star anise, red cherry, cranberry and blood orange;
            "a black tea finish"; "taut, fine-grained tannins and bright acidity".

STRUCTURE (WSET Level 3 SAT terms only; these are READINGS of the reviews and the technical data, not lab measurements; sweetness omitted: all three are dry):
  Catena 2024  Acidity Medium (+): "juicy and agile with integrated freshness"; producer sheet: bright acidity. Tannin Medium: "plush and round with fine-grained
               tannins" (retailer-quoted Suckling). Alcohol Medium: 13.5%. Body Medium: Vinous "slightly slimmer and more lithe" than the 2023.
  Sanford 2022 Acidity Medium (+): "racy" (winery); cool Sta. Rita Hills, east-west valley open to the Pacific (CSW). Tannin Medium (-): "silky and seamless",
               "sensual". Alcohol Medium: 13.5%. Body Medium: "medium-bodied richness".
  Giacosa 2021 Acidity High: "bright acidity" (Wine Enthusiast); CSW calls Nebbiolo "tannic, high-acid". Tannin High: "taut, fine-grained tannins". Alcohol High:
               14.5%. Body Medium (+): "fleshy, succulent" (Wine Spectator).

REGIONS (CSW Study Guide): Mendoza, high-elevation Uco Valley and Tupungato; Sta. Rita Hills sits on the western edge of the Santa Ynez Valley, where the
  coastline and ranges run east-west, "a much cooler climate than the inland areas"; Piedmont's autumn fog, cold winters, warm dry summers.

PHOTOS (no on-slide credits: private use, per Steve): Mendoza, Juan Pelizzatti (CC BY 3.0); Sta. Rita Hills, Bradfordschultze (public domain); Barbaresco, Giorgio Galeotti (CC BY 4.0), all via Wikimedia
  Commons, location confirmed by Commons category. Bottle photos are Steve's (the Catena is only 134x514 px: soft at shelf size).

PRICES (Binny's), on the slide at Steve's request: Catena 2024 regular price $19.99 (sale $16.99); Sanford $49.99 (Steve's figure); Giacosa $36.99.
STRUCTURE GRID: Archivo Light 44 px, thin bars, below the 60 px floor with Steve's sign-off ("!dashboard_label").
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
sys.path.insert(0, os.path.join(HERE, "..", "formats"))
import core        # noqa: E402
import modules     # noqa: E402
from tokens import W   # noqa: E402

CANVAS_H = int(os.environ.get("CANVAS_H", 2700))       # CANVAS_H=2795 renders US Letter proportions (8.5x11 at 2160 px wide)
LETTER = CANVAS_H != 2700
OUT = "/home/claude/out_tb_red_list" + ("_letter" if LETTER else "")
BURG = (122, 30, 44)
GOLD = (196, 158, 84)
PAL = dict(SIGNATURE=BURG, ACCENT=GOLD, LEAD=(140, 95, 58), MARK=BURG)

OFFSET, SEG = 60, W // 3
COL_X = [i * SEG + OFFSET for i in range(3)]
COL_W = SEG - OFFSET - 60

SLOT = dict(
    bg_color=(245, 240, 232), shelf_scrim_color=(245, 240, 232), mark_bg_color=(74, 20, 26),
    top_mark="Eric and Wade's Winter 2026 / 2027 Red Wine List", top_mark_max_w=W, top_mark_full=True,
    producer_color=BURG, style_color=(0, 0, 0), origin_color=(70, 64, 66), note_color=(0, 0, 0),
    shelf_rule_color=(110, 90, 94),
    products=[
        ("bb_catena_mhv", "Catena", "High Mountain Vines", "Malbec \u00b7 2024", "Mendoza, Argentina",
         "Red fruit, fresh plum, violets and a faint balsamic note. Juicy and ready to drink."),
        ("bb_sanford_sb", "Sanford", "Sanford & Benedict Vineyard", "Pinot Noir \u00b7 2022", "Sta. Rita Hills, CA",
         "Floral and savory overtones around a core of red and purple fruit. A beautiful wine."),
        ("bb_giacosa_barbaresco", "Carlo Giacosa", "Barbaresco", "Nebbiolo \u00b7 2021", "Piedmont, Italy",
         "Rose, star anise, red cherry and blood orange, then a black tea finish. Perfect food wine."),
    ],
    scores=[[("92", "Vinous")], [("94", "Wine Advocate"), ("94", "Vinous")], [("93", "Wine Enthusiast"), ("92", "Wine Spectator")]],
    score_stack=True, score_label_size=40,
    structure_header="STRUCTURE",
    structure=[
        [("Acidity", 0.72, "Medium (+)"), ("Tannin", 0.50, "Medium"), ("Alcohol", 0.50, "Medium"), ("Body", 0.50, "Medium")],
        [("Acidity", 0.72, "Medium (+)"), ("Tannin", 0.35, "Medium (-)"), ("Alcohol", 0.50, "Medium"), ("Body", 0.50, "Medium")],
        [("Acidity", 0.90, "High"), ("Tannin", 0.90, "High"), ("Alcohol", 0.90, "High"), ("Body", 0.72, "Medium (+)")],
    ],
    header_gap=40, pre_row_gap=12, row_gap=10, band_gap=22, score_size=88,
    prices=["$19.99", "$49.99", "$36.99"], price_label="Binny's", name_color=(121, 92, 36),
    dash_label_font="body_light", dash_label_size=44, dash_header_size=44, dash_desc_color=(118, 88, 34), dash_bar_h=10, dash_text_bar_gap=6,
    region_caption_shade=170,
    cols=3, col_x_positions=COL_X, col_w_override=COL_W,
    zone_h=480 + int((CANVAS_H - 2700) * 0.65), bottle_lift=70, panel_gap=50, width_frac=0.9,
    region_photos=[("bb_mendoza_andes", "Mendoza, Argentina"), ("bb_sta_rita_hills", "Sta. Rita Hills, CA"),
                   ("bb_barbaresco_tower", "Barbaresco, Italy")],
    region_band_frac=0.12, region_caption_font="italbold", region_caption_size=46,
    footer_label="", show_page_num=False,
)


SLIDES = [("showcase_shelf", SLOT)]   # for brevity_count.py


def build():
    os.makedirs(OUT, exist_ok=True)
    img = modules.MODULES["showcase_shelf"](dict(SLOT), 1, 1, PAL)
    p = f"{OUT}/three_bottles_red_wine_list.png"
    img.save(p)
    if LETTER:
        from PIL import Image
        pdf = f"{OUT}/TB_RedWineList_USLetter.pdf"                      # resolution = width / 8.5 in, so the page is exactly 8.5 x 11 in
        Image.open(p).convert("RGB").save(pdf, "PDF", resolution=W / 8.5)
    else:
        core.assemble_pdf([p], f"{OUT}/TB_RedWineList_review.pdf")
    print("PNG:", p)


if __name__ == "__main__":
    build()
