"""WHAT AM I DRINKING? -- 2012 Lopez de Heredia Rioja Reserva "Vina Tondonia" (Rioja Alta). Arc 4 (the Climate arc), entry 5, in place of the planned
Northern Rhone Syrah (Steve chose this wine and supplied the bottle photo). Two pages per QUICK_SIPS_STYLE_GUIDE.md section 11. Page 1 names nothing.

THE CLIMATE TIE (D1 + D3; each claim traces to the book):
  * D3 p. 345: the Sierra de Cantabria protects Rioja "from the worst of the Atlantic weather". D3 p. 346: Rioja Alta "is generally continental with some maritime
    influences". D1 p. 43: "regions that are far inland or are protected from ocean influences have high continentality and tend to be categorised as
    'continental'". Page 1's paragraph is that chain, with no name in it.
  * D1 p. 44 (weather = the annual variation against the climatic average; vintage variation) and D3 p. 347 ("in any year, parts of Rioja may receive more or less
    influence from the Atlantic (cooler, wetter) and the Mediterranean (warmer, drier)"). The 2012 is the weather story: Wine Advocate (Luis Gutierrez, via Prima
    Vini) says it "comes from a very dry year, with 25% less rain than the average (at the time)". Page 2 uses it.
  * D3 p. 347: climate change "has made high altitude vineyards not just more viable, but more desirable" (the Field Guide's slide 15, "new sites"). Page 2.
D3 DETAIL USED: p. 330 (national aging law: a Reserva red needs at least 36 months in total, 12 of them in barrel; 225 L barriques in Rioja, p. 349); p. 349 (Graciano and
  Mazuelo each add high acidity to a Rioja blend; Tempranillo "is often of higher quality from Rioja Alta and Alavesa", p. 350); p. 351 (D3 names the producer's
  Vina Tondonia Gran Reserva white as a classic oxidative bottling; the red Reserva here is a different wine, so it is not claimed as one).
NOT USED: D3's Rioja Alta soils and 700 m southern sites (they do not describe Haro, where this vineyard is); the 450 m altitude (Prima Vini's figure only); any
  diurnal-range claim (D3 does not give one for Rioja Alta).

WINE (sources: Prima Vini's product page; JJ Buckley, K&L, Bin Ends listings; the critics' notes):
  Tempranillo-led (Decanter et al.: about 70% Tempranillo, 20% Garnacha, 10% Graciano and Mazuelo; Prima Vini's page says 75/15/10: it disagrees, so no
  percentages appear). Six years in barrel; the estate makes its own American-oak barrels (Prima Vini). The family estate (Prima Vini). 13% ABV (Tim Atkin).
  Score: James Suckling 96 (2024) for the 2012; also Wine Advocate 95, Vinous 95, Tim Atkin 95, Decanter 94. Tasting notes: Vinous, Wine Advocate, Tim Atkin.
STRUCTURE (WSET L3 terms; a READING of the reviews, not lab data; Sweetness is omitted: it is dry): Acidity High, Tannin Medium (+), Alcohol Medium (13%),
  Body Medium (+), Aroma Intensity Pronounced (WA: "aromatic with a developed profile"; Prima Vini: "pronounced dried red berry fruit"). Evidence for each is in tasting_sheet/render_ts_tondonia_2012.py.
HERO (page 1): "Vinas junto al Ebro en El Cortijo, La Rioja" (CC0, Wikimedia Commons): autumn vines on the Ebro with mountains behind. HONEST NOTE: El Cortijo is in La
  Rioja on the Ebro, not in Haro; the photo is uncaptioned and shows "Rioja", not the Tondonia vineyard. No signs or text in frame (checked by eye).
BOTTLE (page 2): Steve's own photo. A transparent cutout, 122 x 490 px (the Vivino watermark at the base was repainted). It is SMALL: the panel enlarges it about 4x,
  so it is soft; the label's large type reads, the fine print does not. A larger shot (1,500 px tall or more) would fix it.
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
sys.path.insert(0, os.path.join(HERE, "..", "formats"))
import core                                       # noqa: E402
from tokens import DEFAULT_PALETTE                # noqa: E402
from what_am_i_drinking import wad_page1, wad_page2   # noqa: E402

OUT = "/home/claude/out_wad_tondonia"
os.makedirs(OUT, exist_ok=True)
PAL = dict(DEFAULT_PALETTE)
PAL.update(SIGNATURE=(122, 30, 44), ACCENT=(196, 158, 84), LEAD=(140, 95, 58))     # the Climate arc's burgundy
PHOTOS = os.path.join(HERE, "..", "photos")

SLOT_1 = dict(
    hidden_terms=["Heredia", "Tondonia", "Vi\u00f1a", "Vina", "Rioja", "Haro", "Tempranillo", "Garnacha", "Graciano", "Mazuelo", "Spain", "Spanish",
                  "Ebro", "Cantabria", "Reserva", "Crianza"],
    photo="ts_rioja_ebro",
    photo_anchor=0.0,
    scrim_strength=float(os.environ.get("WAD_SCRIM", 0.62)),   # re-swept for this photo: 0.46 (the Mosel value) left the gold note at 3.4:1; 0.55 gave 4.35; 0.62 gives 5.36 (title 6.6)
    lockup_y=80,
    title_lines=["What am I Drinking?"],
    title_size=120,
    photo_h=1120,
    lockup_note="(Make a guess, then find out on the next page)",
    lockup_note_size=60,
    photo_credit="Bea.miau / Wikimedia Commons (CC0)",
    paragraph_lead="A mountain wall",
    paragraph="shelters these vineyards from the worst of the Atlantic weather, so the climate is mostly continental, with some maritime "
              "influence. The family estate makes its own barrels, and this red spent six years in them.",
    structure=[
        ("Acidity", 0.90, "High"),
        ("Tannin", 0.72, "Medium (+)"),
        ("Alcohol", 0.50, "Medium"),
        ("Body", 0.72, "Medium (+)"),
        ("Aroma Intensity", 0.90, "Pronounced"),
    ],
    notes=[
        ("Aromas", "Plum marmalade, red cherry, cedar, forest floor."),
        ("Palate", "Dry, bright, polished chalky tannins."),
        ("Finish", "Long, dry, spicy."),
    ],
    notes_source="Vinous, Wine Advocate",
)

SLOT_2 = dict(
    bottle=os.path.join(PHOTOS, "wad_tondonia_bottle.png"),
    bottle_top=100,
    lockup_size=110,           # the producer's name is long, so it fits at 158 px; the lockup steps down to keep the hierarchy (headline > lockup + 30)
    title_top=470,
    producer="L\u00f3pez de Heredia",
    region_year="Rioja Alta \u00b7 2012",
    wine_lines=["Vi\u00f1a Tondonia", "Reserva"],
    lead="Climate sets the stage.",     # kept short: a lead wider than the text column spills into the bottle panel (the first draft's did)
    body="That wall is the Sierra de Cantabria, but weather writes the vintage: Wine Advocate says 2012 had 25% less rain than the average "
         "at the time. A Reserva needs 36 months of aging, 12 in barrel; this one spent six years in barrel. As the climate warms, "
         "Rioja's higher sites are more prized. James Suckling gave this 2012 a\u00a096.",
    rule=False,
    body_anchor="bottom",
)

SLIDES = [("wad_page1", SLOT_1), ("wad_page2", SLOT_2)]


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)
    paths = []
    for i, (fn, slot) in enumerate([(wad_page1, SLOT_1), (wad_page2, SLOT_2)], start=1):
        img = fn(slot, i, 2, PAL)
        p = f"{OUT}/{i:02d}_page{i}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  page{i}")
    pdf = f"{OUT}/WAD_Tondonia_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
