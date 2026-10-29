"""TASTING SHEET -- 2012 Lopez de Heredia Rioja Reserva "Vina Tondonia". One page, US Letter (8.5 x 11 in, 2160 x 2795 px at 254 dpi). Private use: no photo credits.

SCORES (critic named; vintage 2012):
  James Suckling 96 (Zekun Shuai, 2024: "Very bright, juicy and structured ... Beautiful now."); Wine Advocate 95 (Luis Gutierrez, 29 Feb 2024; "[$65 list]");
  Vinous 95 (Joaquin Hidalgo, Dec 2023 / Apr 2024; drink 2024-2035); Tim Atkin MW 95 (Feb 2024; drink 2025-2032; 13%); Decanter 94 (Ines Salpico, 2024).
  Not featured: John Gilman 93+, Wine Spectator 92 (JJ Buckley's listing), the CellarTracker community average 91.3.
NOTES (critic language, shortened): nose, Vinous "ash and plum marmalade, a faintly herbal core, hints of oaky cedar"; Tim Atkin "sweet red cherry compote";
  Wine Advocate "spicy and tertiary (forest floor, a touch of brick dust and iodine)"; palate, WA "full and round, with polished tannins and a long, dry
  finish", Vinous "dry and lean, the fairly chalky texture", Suckling "savory ... minerals"; color, Vinous "garnet" (the brick-orange rim is a retailer's
  profile); pairing and "spicy finish", Prima Vini's note; drinking window, Vinous 2024-2035 (Atkin 2025-2032; Suckling "beautiful now").
STRUCTURE (WSET L3 terms; a READING of the reviews, not lab data): Sweetness Dry; Acidity High ("very bright" JS; "dry and lean" Vinous; "energetic ... verve"
  Decanter); Tannin Medium (+) ("polished" WA; "muscular yet very elegant" Decanter); Alcohol Medium (13%); Body Medium (+) ("full and round" WA vs "lean" Vinous);
  Finish Long (WA, "long, dry").
FACTS: blend Tempranillo 70 / Garnacha 20 / Graciano and Mazuelo 10 (Decanter via JJ Buckley, Bin Ends, CellarTracker; Prima Vini's page says 75/15/10: it
  disagrees, so the majority is used); six years in American oak (the estate's own cooperage); vineyard Vina Tondonia, Haro, Rioja Alta, on the Ebro, planted 1913
  (Prima Vini); 250,000 bottles (Wine Advocate).
PRICES, checked 28 Oct 2026: Binny's $54.99 regular, $48.99 Binny's Rewards price (binnys.com page, 96 points); Prima Vini $59.99 regular / $49.99 sale (sold out);
  K&L $59.99 (out of stock); JJ Buckley $64.94; Flatiron NYC $69.99 (sold out); Bin Ends $84 / $67.20 sale; Wine Advocate "[$65 list]". Approximate range $55-$65.
PHOTO: Vinas junto al Ebro en El Cortijo, La Rioja (CC0, Wikimedia Commons). It is captioned as Rioja and the Ebro, NOT as Haro: no Haro photo was found.
BOTTLE: Steve's own photo (a 122 x 490 px cutout inside a 500 px file, so it is soft at 2x). The file was already a transparent cutout; a small Vivino watermark at the
  base was repainted with the surrounding dark glass (the gold netting line there has a hairline break).
"""
import os
import sys

os.environ.setdefault("CANVAS_H", "2795")          # US Letter proportions
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
sys.path.insert(0, os.path.join(HERE, "..", "formats"))
from PIL import Image, ImageDraw, ImageFilter      # noqa: E402
import core                           # noqa: E402
import modules                        # noqa: E402
import quick_sips                     # noqa: E402
from tokens import W, H, M, PHOTO_DIR            # noqa: E402

OUT = "/home/claude/out_ts_tondonia"
BURG, GOLD = (122, 30, 44), (196, 158, 84)
PAL = dict(SIGNATURE=BURG, ACCENT=GOLD, LEAD=(140, 95, 58), MARK=BURG)
BG = (245, 240, 232)
INK = (24, 20, 22)

TITLE = "2012 L\u00f3pez de Heredia Vi\u00f1a Tondonia Reserva"
SUB = "RIOJA ALTA  \u00b7  TEMPRANILLO-LED RED  \u00b7  13% ABV"
BAND_H = 300
LEFT_W = 1100
GAP = 60

SCORES_TOP = ("96", "James Suckling")
SCORES_GRID = [("95", "Wine Advocate"), ("95", "Vinous"), ("95", "Tim Atkin"), ("94", "Decanter")]
NOTES = [
    ("Look.", "Garnet with a brick-orange rim."),
    ("Nose.", "Plum marmalade, red cherry compote and cedar, with forest floor, ash and a touch of iodine."),
    ("Palate.", "Dry and bright, with polished, chalky tannins and a savory, mineral core."),
    ("Finish.", "Long, dry and spicy."),
    ("Pair with.", "Roast lamb or beef, or aged cheese and dried fruit."),
    ("Drink.", "Now to about 2035."),
]
STRUCTURE = [("Sweetness", 0.08, "Dry"), ("Acidity", 0.90, "High"), ("Tannin", 0.72, "Medium (+)"),
             ("Alcohol", 0.50, "Medium"), ("Body", 0.72, "Medium (+)"), ("Finish", 0.90, "Long")]
FACTS = [
    ("Blend.", "About 70% Tempranillo, with Garnacha, Graciano and Mazuelo."),
    ("Made.", "Six years in American oak; the vineyard in Haro was planted in 1913."),
]


def section(d, x, y, w, label):
    kf = core.font("kicker_bold", 60)
    core.tracked_text(d, (x, y), label, kf, BURG, tracking=4)
    y += sum(kf.getmetrics()) + 4
    d.line([(x, y), (x + w, y)], fill=(190, 170, 150), width=3)
    return y + 24


def build():
    os.makedirs(OUT, exist_ok=True)
    img, d, qa = modules._start("TS-01 tasting sheet", 1, 1, PAL, bg_color=BG)
    mark_h = modules._glass_mark_patch(img, d, PAL, TITLE, bg_color=(74, 20, 26), size=90, max_w=W, full_w=True)
    d = ImageDraw.Draw(img)
    y = mark_h + 44
    kf = core.font("kicker_bold", 60)
    core.tracked_text(d, (M, y), SUB, kf, BURG, tracking=4)
    y += sum(kf.getmetrics()) + 40
    band_bot = core.photo_band(img, "ts_rioja_ebro_band", y, BAND_H, caption_txt="Vineyards along the Ebro, La Rioja")
    d = ImageDraw.Draw(img)
    top = band_bot + 56

    # ---- left: scores, tasting notes
    x0, yl = M, top
    yl = section(d, x0, yl, LEFT_W, "REVIEW SCORES")
    big = core.font("display_black", 190)
    ba, bd = big.getmetrics()
    lf = core.font("body", 60)
    la = lf.getmetrics()[0]
    nw = core.text_w(d, SCORES_TOP[0], big)
    d.text((x0, yl), SCORES_TOP[0], font=big, fill=BURG)
    d.text((x0 + nw + 26, yl + ba - la), SCORES_TOP[1], font=lf, fill=INK)
    yl += ba + bd + 6
    sf = core.font("display_black", 84)
    sa = sf.getmetrics()[0]
    for k, (num, src) in enumerate(SCORES_GRID):
        cx = x0 + (k % 2) * (LEFT_W // 2 + 10)
        cy = yl + (k // 2) * 104
        w_ = core.text_w(d, num, sf)
        d.text((cx, cy), num, font=sf, fill=BURG)
        d.text((cx + w_ + 14, cy + sa - la), src, font=lf, fill=INK)
    yl += 2 * 104 + 52
    yl = section(d, x0, yl, LEFT_W, "TASTING NOTES")
    for lead, body in NOTES:
        yl = core.run_in(d, (x0, yl), lead, body, LEFT_W, PAL, lead_size=60, body_size=60, leading=1.3) + 14
    qa.box("left", (x0, top, x0 + LEFT_W, yl))

    # ---- right: structure + price beside the bottle, then the facts across the column
    x1 = M + LEFT_W + GAP
    wr = W - M - x1
    bottle = Image.open(f"{PHOTO_DIR}/ts_tondonia_bottle.png").convert("RGBA")
    BH = 1020
    bw = round(BH * bottle.width / bottle.height)
    bottle = bottle.resize((bw, BH), Image.LANCZOS)
    wd = wr - bw - 36                                  # the text stack beside the bottle
    yr = top
    yr = quick_sips.qs_tasting_dashboard(d, yr, x1, wd, PAL, qa, STRUCTURE, header="STRUCTURE", label_font="body_light", label_size=44,
                                         header_size=44, desc_color=(118, 88, 34), bar_h=10, text_bar_gap=6, header_gap=40,
                                         pre_row_gap=12, row_gap=10) + 34
    price_top = yr
    yr = section(d, x1, yr, wd, "PRICE")                 # a longer header ("APPROXIMATE PRICE") would run under the bottle
    af = core.font("body", 44)
    d.text((x1, yr), "Approximately", font=af, fill=(110, 100, 104))
    yr += sum(af.getmetrics()) + 2
    pf = core.font("display_black", 105)
    pa, pd_ = pf.getmetrics()
    d.text((x1, yr), "$55\u2013$65", font=pf, fill=BURG)
    yr += pa + pd_ + 6
    yr = core.paragraph(d, (x1, yr), "Binny's $54.99", lf, INK, wd, 1.3) + 10
    yr = core.paragraph(d, (x1, yr), "Elsewhere about $60\u2013$70.", lf, INK, wd, 1.3) + 10
    qa.box("price", (x1, price_top, x1 + wd, yr))
    bx, by = x1 + wr - bw, top
    shadow = Image.new("RGBA", (bw + 100, 70), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([30, 18, bw + 70, 52], fill=(0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(11))
    img.paste(shadow, (bx - 50, by + BH - 34), shadow)
    img.paste(bottle, (bx, by), bottle)
    qa.box("bottle", (bx, by, bx + bw, by + BH))
    d = ImageDraw.Draw(img)
    yr = max(yr, by + BH) + 40
    facts_top = yr
    yr = section(d, x1, yr, wr, "ABOUT THE WINE")
    for lead, body in FACTS:
        yr = core.run_in(d, (x1, yr), lead, body, wr, PAL, lead_size=60, body_size=60, leading=1.3) + 14
    qa.box("facts", (x1, facts_top, x1 + wr, yr))

    # a small dated note on the prices (credit-sized, bottom left)
    nf = core.font("body", 34)
    d.text((M, H - 92), "Prices checked Oct 28, 2026; retail prices vary by store and vintage availability.", font=nf, fill=(110, 100, 104))
    img = modules._finish(img, d, qa, 1, 1, footer_label="", show_page_num=False)
    p = f"{OUT}/tasting_sheet_tondonia_2012.png"
    img.save(p)
    img.convert("RGB").save(f"{OUT}/TastingSheet_Tondonia2012_USLetter.pdf", "PDF", resolution=W / 8.5)
    print("PNG:", p, img.size)


if __name__ == "__main__":
    build()
