"""THE FIELD GUIDE: CLIMATE -- "Climate's Impact on Wine" (Steve's title). A classic carousel (2160x2700, 15 slides, 15 layouts).

Arc 4 entry 1 (plan: arc4/ARC4_CLIMATE_PLAN.md, approved Oct 2026; burgundy signature, per Steve). Spine: the seven natural Factors of
WSET Diploma D1 Chapter 3.1 (latitude, altitude, slopes and aspect, proximity to water, winds, soil, mist/fog/clouds), framed by what
the vine needs (3.1), climate vs weather (3.4, 3.5), naming a climate (3.4), and what happens when a Factor moves (3.6).

SOURCES -- every number below is D1 (page = the running header's page), or arithmetic from D1 and labeled so:
  p.24  vine thresholds: dormancy under 10 C (50 F), winter freeze around -20 C (-4 F) can DAMAGE the vine; budburst above 10 C
  p.25  flowering best above 17 C (63 F); fruit set 26-32 C (79-90 F); photosynthesis 18-33 C (64-91 F); last-month mean above
        21 C (70 F) loses acid quickly, below 15 C (59 F) keeps too much; extreme heat, especially dry, slows or stops photosynthesis
  p.25  light limits photosynthesis only below one third of full sunshine (fog slows it; an average cloudy day does not)
  p.26-27  latitude: more radiation nearer the Equator (Mendoza, South Africa, New South Wales) than nearer the poles (northern
        France, Germany); wine grapes grow between about 30 and 50 degrees each side of the Equator
  p.27  altitude: about 0.6 C (1.1 F) cooler per 100 m; Salta vineyards from about 1,280 to 3,000 m; Burgundy and the Loire sit low
  p.28  aspect: Hermitage's southerly aspect gives Syrah extra ripeness; Burgundy and Alsace grand crus on south-east slopes,
        generic vineyards on the flat; Stellenbosch whites on south-facing slopes for acidity; the effect grows with latitude
  p.29-30  water: lakes and seas moderate; Finger Lakes; Carneros; Willamette (about 45 N, 15.9 C growing-season mean, California
        current, early-ripening Pinot Noir) vs Margaux (about 45 N, 17.7 C, Gulf Stream, late-ripening Cabernet possible)
  p.30-31  winds: Petaluma Gap; the Zonda in Mendoza; less fungal disease; higher water needs; damage; windbreaks (Neuquen)
  p.31-32  soil temperature: free-draining soils warm sooner; light chalk (Sancerre, Champagne) reflects; dark volcanic (Etna) holds
        heat; stony soils store heat and release it at night; the gravelly soils of the Haut-Medoc are D1's stony example (p.38-40)
  p.32-33  mist and fog (Sonoma, Napa, Leyda Valley, Sauternes); diurnal range (Mendoza, Ribera del Duero big; Mosel, Mornington
        Peninsula small; the Wachau a cold-night exception)
  p.41  climate = the annual pattern averaged over about 30 years;  p.42-43 WSET bands by growing-season mean: cool 16.5 C or below,
        moderate 16.5-18.5, warm 18.5-21, hot above 21; maritime (Bordeaux), Mediterranean (Napa Valley, Coonawarra), continental
        (Burgundy, Alsace)
  p.44  weather: Bordeaux 2013 (cold wet spring, uneven flowering, rainy harvest picked early, low quantity and quality) vs 2016
  p.44-45  climate change: faster vine cycle, earlier budburst; sugar and acid race ahead of aroma and tannin
  p.44-46 (slide 4): rising temperatures; later-ripening varieties may be preferable; regions once too cold may improve; growers and wine
        businesses have already started to act. D1 (Garnacha: the drought-tolerant variety). D3 p.347 (Rioja: high-altitude vineyards more
        desirable), D3 p.269 (Tuscany: higher sites, less sunny aspects), D3 Bordeaux (hot, dry summers across Europe)
DERIVED, NOT STATED (labeled on the slide): the cooling for the imaginary region's 500, 1,000, 2,000 and 3,000 m sites (0.6 C per 100 m x 5, 10, 20, 30 = 3.0, 6.0, 12.0, 18.0).
NOT USED (D1 gives none): numeric Winkler (growing degree day) bands.
PHOTOS (location from each Commons file's own title; the sunset and the fog photo carry no place claim): cover, Zach Dischner (CC BY
  2.0); Bordeaux vines and Margaux, Megan Mallen (CC BY 2.0); Willamette, Sheila Sund (CC BY 2.0); Mendoza, Justin De La Ornellas;
  Etna, Neil Weightman; Haut-Medoc, Jonas Roux; Trepail (Champagne), Havang(nl) (CC0); Finger Lakes sunrise, Visit Finger Lakes
  (CC BY 2.0); Grenache, Stephan Ridgway; Cafayate, aaepstein; Chianti, Matthew Hutchinson (all CC BY 2.0); Hermitage hill, Veronique Pagnier (public domain, cropped to the hill and chapel); fog, Mick Haupt (Pexels).
"""
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
os.environ.setdefault("AMERICAN_ENGLISH", "1")
import core      # noqa: E402
import modules   # noqa: E402
import variety   # noqa: E402
import prepare_climate_maps as pcm   # noqa: E402
from tokens import W, M, INK, PAPER    # noqa: E402

OUT = "/home/claude/out_fg_climate"
os.makedirs(OUT, exist_ok=True)

# ---- palette: the series burgundy (engine/themes.py), the house gold, and a temperature ramp from cool slate to burgundy
BURG = (104, 26, 38)
GOLD = (196, 158, 84)
SLATE, SAGE, TERRA = (84, 110, 134), (132, 140, 120), (168, 86, 64)      # slate deepened: paper text on it measured 4.04:1, now about 5:1
PAL = dict(SIGNATURE=BURG, ACCENT=GOLD, LEAD=(140, 95, 58), MARK=BURG)
CHART = dict(
    ripe=[SLATE, SAGE, GOLD, TERRA, BURG],           # one step per rung: cool to hot
    focus=BURG, cool=SLATE, warm=GOLD, vine=(86, 104, 70), shade=BURG, amber=TERRA, gold=GOLD, grape=(120, 22, 62),
    stone=(110, 100, 92), track=(220, 208, 196), ice=SLATE, ice_fill=(226, 234, 240), ice_text=(54, 78, 100),
)


def credit(*pairs):
    return "; ".join(f"{who} / {src}" for who, src in pairs)


C_DISCHNER = "Zach Dischner / Wikimedia Commons (CC BY 2.0)"
C_MALLEN = "Megan Mallen / Wikimedia Commons (CC BY 2.0)"
C_SUND = "Sheila Sund / Wikimedia Commons (CC BY 2.0)"
C_FINGER = "Visit Finger Lakes / Wikimedia Commons (CC BY 2.0)"

MAP = pcm.build()
MAP_H = int((W - 2 * M) / MAP["aspect"])


def _atlas():
    px = 12 / (W - 2 * M)
    N = pcm.N
    band_fill = (216, 176, 184)
    regions = []
    # each belt: the biggest piece carries the label (in open ocean, east of the Americas); every other piece gets a zero-length leader
    for key, name, lab, tgt in (("north", "30\u00b0\u201350\u00b0 N", N(-60, 38), N(-82, 40)),
                                ("south", "30\u00b0\u201350\u00b0 S", N(-58, -43), N(-68, -40))):
        rings = MAP[key]
        cen = [(sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r)) for r in rings]
        main = min(range(len(rings)), key=lambda i: (cen[i][0] - tgt[0]) ** 2 + (cen[i][1] - tgt[1]) ** 2)
        for i, ring in enumerate(rings):
            if i == main:
                regions.append(dict(name=name, pts=ring, fill=band_fill, label=lab, target=tgt, side="right"))
            else:
                regions.append(dict(name="", pts=ring, fill=band_fill, label=(ring[0][0] + px, ring[0][1]), target=ring[0], side="right"))
    lines = []
    for name, lat in MAP["lines"].items():
        y = (pcm.LAT_TOP - lat) / pcm.SPAN_Y
        lines.append(dict(pts=[(0.0, y), (1.0, y)], name="", label=(0.012, y - 0.017), angle=0))
    markers = [dict(name="Mendoza", target=N(-68.85, -32.89), label=N(-100, -26), side="left"),
               dict(name="South Africa", target=N(18.86, -33.93), label=N(14, -26.5), side="right"),
               dict(name="New South Wales", target=N(151.3, -32.75), label=N(160, -53), side="left"),
               dict(name="N. France, Germany", target=N(5.5, 49.6), label=N(30, 56), side="right")]
    return dict(
        kicker="FACTOR 1 \u00b7 LATITUDE", headline="Between 30\u00b0 and 50\u00b0", map_h=MAP_H,
        outline=MAP["land"][0], outlines=MAP["land"][1:], regions=regions, rivers=lines, markers=markers,
        legend=[("30\u00b0 to 50\u00b0", "Wine grapes grow between about 30\u00b0 and 50\u00b0 on each side of the Equator."),
                ("Nearer the Equator", "More solar radiation, and more intense."),
                ("Nearer the poles", "Longer summer days, cooler temperatures.")],
    )


SLIDES = [
    # 1 -- COVER: a vineyard at sunset (no place claimed). D1 3.1: the sun, the Factor behind all the others.
    ("cover_bleed", dict(
        photo="cl_vineyard_sunset_dischner", photo_anchor=0.5, photo_zoom=1.0,
        kicker="THE FIELD GUIDE: CLIMATE", kicker_size=96,
        kicker_chip=dict(color=(250, 246, 236), alpha=0.45, text=INK),
        title="Climate\u2019s\nImpact\non Wine", title_top=0.44,
        photo_credit=C_DISCHNER,
    )),

    # 2 -- THE SEVEN FACTORS: the overview graphic. D1 3.1 lists exactly these seven natural factors (pp. 26-33), in this order.
    ("factor_wheel", dict(
        kicker="THE NATURAL FACTORS", headline="Seven Factors, One Climate",
        standfirst="Latitude, altitude, slope, water, wind, soil and fog set a vineyard's climate. We take them in this order.",
        hub=("A vineyard's", "climate"),
        nodes=[("Latitude", "latitude"), ("Altitude", "altitude"), ("Slope & Aspect", "aspect"), ("Water", "water"),
               ("Wind", "wind"), ("Soil", "soil"), ("Fog & Cloud", "fog")],
    )),

    # 3 -- FACTOR 1, LATITUDE: D1 p.26-27 (see prepare_climate_maps.py). Natural Earth land (public domain), clipped bands.
    ("atlas", dict(_atlas(), _factor=("latitude", 1))),

    # 4 -- FACTOR 2, ALTITUDE: D1 p.27 (about 0.6 C cooler per 100 m). Steve: the bars read as increasing when they mean "cooler", so show a cross-
    # section of an IMAGINARY region (seaside vineyards, gradual slopes, then steep slopes) with each site flagged by how much cooler it is than the
    # seaside one. Every figure is arithmetic from D1's rate (500 m x 0.006 = 3.0 C; 1,000 m = 6.0; 2,000 m = 12.0; 3,000 m = 18.0), labeled as such.
    # Salta (D1: vineyards from about 1,280 to 3,000 m) is real and is named in the footnote for scale.
    ("cross_section", dict(_factor=("altitude", 2),
        kicker="FACTOR 2 \u00b7 ALTITUDE", headline="Cooler by 0.6\u00b0C Every 100 m",
        standfirst="Height can rescue a hot, low-latitude site.",
        elev_max=3900, ticks=[], sea_label=None,
        profile=[(0.14, 0), (0.40, 40), (0.66, 1000), (0.88, 3000), (1.0, 3080)],
        zones=[(0.14, 0.40, "Coastal plain", (214, 196, 150)), (0.40, 0.66, "Gradual slopes", (172, 160, 128)), (0.66, 0.88, "Steep slopes", (96, 92, 82))],
        sites=[(0, 0.25, "Seaside", "the baseline", (196, 158, 84)),
               (500, None, "500 m", "3.0\u00b0C cooler", (176, 194, 208)),
               (1000, None, "1,000 m", "6.0\u00b0C cooler", (132, 158, 180)),
               (2000, None, "2,000 m", "12.0\u00b0C cooler", (84, 110, 134)),
               (3000, None, "3,000 m", "18.0\u00b0C cooler", (58, 84, 110))],
        footnote="An imaginary region; the cooling is our arithmetic from D1's 0.6\u00b0C per 100 m. Salta's real vineyards run from about 1,280 to 3,000 m.",
        chart=CHART,
    )),

    # 5 -- FACTOR 3, SLOPE AND ASPECT: D1 p.28. The Hermitage hill in color (Steve: not the black-and-white postcard). "Tain - Chapelle et
    # vignoble" by Veronique Pagnier, public domain; the file's own description: "Chapelle et vignes a Tain l'Hermitage, Drome". The layout has no
    # credit slot, so the credit is in the caption. Four callouts only: the photo does not say which way each slope faces, so nothing here points
    # at a slope and calls it shaded.
    ("spotlight", dict(_factor=("aspect", 3),
        photo="cl_hermitage_hill_crop", hero_h=1480, kicker="FACTOR 3 \u00b7 SLOPE AND ASPECT", headline="Face the Sun",
        callouts=[(0.65, 0.58, "A", "The sun side", "Slopes facing the sun get more radiation. Warm regions pick shade-facing slopes for acidity, as in Stellenbosch."),
                  (0.31, 0.50, "B", "Hermitage", "A southerly aspect gives Syrah extra ripeness."),
                  (0.10, 0.66, "C", "Low sun, steep slope", "At high latitude, aspect and slope count for more."),
                  (0.88, 0.78, "D", "Slope over flat", "Burgundy and Alsace grand crus sit on south-east slopes, not the flat.")],
    )),

    # 6 -- FACTOR 4, WATER: D1 p.30. The hero comparison.
    ("duel", dict(_factor=("water", 4), 
        photos=("cl_willamette_sund", "cl_margaux_mallen"), labels=("Willamette Valley", "Margaux"),
        kicker="FACTOR 4 \u00b7 WATER", headline="Two Oceans at 45\u00b0",
        standfirst="Both sit near 45\u00b0 N. Ocean currents help explain the gap.",
        mode="table", col_heads=("Oregon", "Bordeaux"),
        rows=[("Ocean current", "The cold California current", "The warm Gulf Stream"),
              ("Growing-season mean", "15.9\u00b0C (61\u00b0F)", "17.7\u00b0C (64\u00b0F)"),
              ("Grape", "Early-ripening Pinot Noir", "Late-ripening Cabernet Sauvignon")],
        photo_credit=f"{C_SUND}; {C_MALLEN}",
    )),

    # 7 -- FACTOR 5, WIND: D1 p.30-31. The Mendoza portrait on a side rail (D1 names the Zonda in Mendoza).
    ("side_rail", dict(_factor=("wind", 5),
        photo="cl_mendoza_vineyard", photo_caption="Vines in Mendoza", side="right",
        photo_credit="Justin De La Ornellas / Wikimedia Commons (CC BY 2.0)",
        kicker="FACTOR 5 \u00b7 WIND", headline="Wind Cools,\nHeats and Dries",
        standfirst="",
        items=[("Funneled", "Coastal valleys, like the Petaluma Gap, pull cool wind far inland."),
               ("Heated", "Wind from hot land brings warm air, as the Zonda does in Mendoza."),
               ("Healthier", "Moving air stops damp, stagnant canopy air: less fungal disease."),
               ("Costly", "Wind raises water needs and can damage vines. Windbreaks help, as in Neuqu\u00e9n.")],
    )),

    # 8 -- FACTOR 6, SOIL: D1 p.31-32 (and p.38-40 for the Haut-Medoc gravel).
    ("blades", dict(_factor=("soil", 6), 
        blades=[dict(photo="cl_champagne_trepail", caption="Champagne, Tr\u00e9pail", anchor=0.5),
                dict(photo="cl_etna_passopisciaro", caption="Etna", anchor=0.5),
                dict(photo="cl_haut_medoc", caption="Haut-M\u00e9doc, gravel", anchor=0.5)],
        blade_h=1180, kicker="FACTOR 6 \u00b7 SOIL", headline="Soil Sets the Temperature Too",
        items=[("Light and reflective", "Chalk, as in Champagne and Sancerre, bounces light up into the canopy."),
               ("Dark and heat-holding", "Volcanic soil, as on Etna, soaks up heat and gives it back at night."),
               ("Free-draining and stony", "Gravel warms sooner in spring, and stony soil releases heat at night.")],
        photo_credit="Havang(nl) / Wikimedia Commons (CC0); Neil Weightman, Jonas Roux / Wikimedia Commons (CC BY 2.0)",
    )),

    # 9 -- FACTOR 7, FOG AND CLOUD: D1 p.25, p.32-33. The Pexels fog photo carries no place claim.
    ("fact_file", dict(_factor=("fog", 7), 
        photo="us_mendo_fog_redwoods_pexels", photo_caption="Fog among redwoods", photo_credit="Mick Haupt / Pexels",
        kicker="FACTOR 7 \u00b7 FOG AND CLOUD", headline="Fog Slows the Clock",
        facts=[("What it is", "Tiny drops of water near the ground."),
               ("Where", "Most often in the morning: Sonoma, Napa, Leyda Valley, Sauternes."),
               ("The limit", "Light limits photosynthesis only below one third of full sun."),
               ("The effect", "Slower ripening: it can help in warm regions."),
               ("The risk", "More humidity: fungal disease, or noble rot where afternoons are dry.")],
    )),

    # 10 -- THE DAY-NIGHT GAP: D1 p.27-28, p.33.
    ("tile_grid", dict(
        kicker="THE DAY\u2013NIGHT GAP", headline="Diurnal Range",
        standfirst="Whether it helps depends on the climate.",
        tile_colors=[(BURG, PAPER), (SLATE, PAPER), (GOLD, INK), (TERRA, PAPER)],
        tiles=[("Warm climates", "A big range often helps", "Mendoza, Ribera del Duero: cool nights slow acid loss."),
               ("Cool climates", "A small range may help", "Mosel, Mornington Peninsula: warmer nights aid ripening."),
               ("The Wachau", "A cold-night exception", "Top sites see cold nights; reasons unknown."),
               ("High and inland", "Bigger ranges", "Thin air holds less heat.")],
    )),

    # 11 -- WHAT THE VINE NEEDS: D1 p.24-25 (Steve: a thermometer, with the text boxes climbing up the side). Winter freeze: D1 says
    # "can cause winter freeze and damage the vine" (around -20 C / -4 F), so the slide says damage, not kill.
    ("thermometer", dict(
        chart=dict(CHART, ripe=[(58, 84, 110), SLATE, SAGE, GOLD, TERRA, BURG]),
        kicker="WHAT THE VINE NEEDS", headline="The Vine's Thermometer",
        standfirst="Each reading, and what it does.",
        scale=dict(min=-25, max=40, ticks=[-20, 0, 20, 40]),
        marks=[("Winter freeze", "\u201320\u00b0C (\u20134\u00b0F) can damage the vine.", -20, None),
               ("It wakes: 10\u00b0C", "Budburst begins. Spring frost cuts yields.", 10, None),
               ("It flowers: 17\u00b0C+", "Cold, damp weather hurts flowering.", 17, None),
               ("It works: 18\u201333\u00b0C", "The best range for photosynthesis.", 18, 33),
               ("It sets fruit: 26\u201332\u00b0C", "The optimum range.", 26, 32),
               ("It stalls: extreme heat", "Photosynthesis slows or stops, especially when dry.", 33, "top")],
    )),

    # 12 -- NAME THE CLIMATE: D1 p.42-43.
    ("stat_wall", dict(
        kicker="NAME THE CLIMATE", headline="Cool, Moderate, Warm, Hot",
        standfirst="WSET sorts climates by the mean temperature of the growing season, then by pattern.",
        stats=[("\u226416.5\u00b0", "COOL", "62\u00b0F or below. Willamette Valley."),
               ("16.5\u201318.5\u00b0", "MODERATE", "62\u201365\u00b0F. Margaux."),
               ("18.5\u201321\u00b0", "WARM", "65\u201370\u00b0F."),
               (">21\u00b0", "HOT", "Above 70\u00b0F.")],
        famous=["Maritime: Bordeaux", "Mediterranean: Napa Valley, Coonawarra", "Continental: Burgundy, Alsace"], famous_label="THREE PATTERNS", cell_max=650,
    )),

    # 13 -- CLOSE: D1 p.44-45. A Finger Lakes sunrise (D1's water-moderated example).
    ("statement", dict(
        variant="cover", photo="cl_finger_lakes_sunrise", photo_anchor=0.5,
        title="When a Factor\nMoves",
        subtitle="Rising temperatures are already showing, and growers have started to act.",   # D1 p.44, p.46
        photo_credit=C_FINGER,
    )),    # 14 -- CLIMATE IS NOT WEATHER: D1 p.41, p.44. Bordeaux 2013 vs 2016.
    ("editorial_lead", dict(
        photo="cl_margaux_cabernet_mallen", photo_caption="Chateau Margaux",
        kicker="A FEW WORDS ON CLIMATE CHANGE", headline="The Pattern and the Year",
        standfirst="Same Bordeaux climate; two very different years.",
        items=[("Climate", "Temperature, sunlight, rain and wind, averaged over about 30 years."),
               ("Weather", "One year's variation from that pattern.")],
        table=dict(groups=[("2013", [("Spring", "Cold and wet", "Uneven flowering"), ("Harvest", "Rainy, humid", "Low quantity and quality")]),
                           ("2016", [("Flowering", "Good weather", "Warm, dry summer"), ("Harvest", "Warm and dry", "High quality and volume")])]),
        photo_credit=C_MALLEN,
    )),

    # 15 -- WHEN THE CLIMATE SHIFTS (Steve: a page on long-term change and how the wine world adjusts: new varieties, new sites, changing aspect).
    # Every claim is WSET: D1 p.44-45 (3.6: rising temperatures, a faster cycle, sugar ahead of aroma and tannin; later-ripening varieties may be
    # preferable; regions once too cold may improve), D1 p.27 (0.6 C per 100 m), D1 p.28 (shade-facing slopes in warm regions; Stellenbosch
    # whites), D1 (Garnacha as the drought-tolerant variety), D3 p.347 (Rioja: climate change has made high-altitude vineyards "not just more
    # viable, but more desirable"), D3 p.269 (Tuscany: "growers are looking to plant on higher sites or those with less sunny aspects"), and
    # D3 Bordeaux (climate change has led to hot, dry summers across Europe).
    ("feature_trio", dict(
        kicker="A FEW WORDS ON CLIMATE CHANGE", headline="Longer-term climate trends\nare getting warmer",
        features=[("New grapes", "Later-ripening varieties may suit warming regions. Garnacha copes with drought.", "cl_grenache_old_vines"),
                  ("New sites", "In Rioja, high vineyards are now more desirable. Once-too-cold places may ripen grapes.", "cl_cafayate_aaepstein"),
                  ("New aspects", "In Tuscany, growers are looking at higher sites and less sunny aspects.", "cl_chianti_hutchinson")],
        footnote="Rising temperatures speed the vine cycle and push sugar ahead of aroma and tannin.",
        photo_credit="Stephan Ridgway, aaepstein, Matthew Hutchinson / Wikimedia Commons (CC BY 2.0)",
    )),


]


def _badge(img, key, num):
    """The Factor's icon and its number, top right, so the pages that follow the wheel carry the same mark."""
    import icons
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    cx, cy, r = W - M - 104, 158, 104
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PAPER, outline=BURG, width=9)
    ic = icons.icon(key, 140, BURG)
    img.paste(ic, (cx - 70, cy - 70), ic)
    bx, by = cx - 76, cy + 76
    d.ellipse([bx - 38, by - 38, bx + 38, by + 38], fill=GOLD, outline=PAPER, width=4)
    d.text((bx, by + 2), str(num), font=core.font("display_bold", 48), fill=INK, anchor="mm")


def build():
    variety.report([name for name, _ in SLIDES])
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)
    paths = []
    total = len(SLIDES)
    for i, (name, slot) in enumerate(SLIDES, start=1):
        slot = dict(slot)
        fac = slot.pop("_factor", None)
        img = modules.MODULES[name](slot, i, total, PAL)
        if fac:
            _badge(img, *fac)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d} {name}")
    core.assemble_pdf(paths, f"{OUT}/FG_Climate_review.pdf")
    print("PDF:", f"{OUT}/FG_Climate_review.pdf")


if __name__ == "__main__":
    build()
