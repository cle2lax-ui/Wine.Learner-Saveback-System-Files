# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 3 — The Growing Environment"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Three: The Growing Environment",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 3.1 Temperature and Sunlight \u2192 3.6 Climate Change")

s.append(P("The largest chapter in D1 and the one most often drawn on for whole questions. Its "
           "logic: the vine needs warmth, sunlight, water and nutrients <b>at the right time</b>; "
           "the growing environment sets how much of each it gets; the grower manages the "
           "vineyard to correct the shortfall or excess."))
s.append(P("Reliably examined: <b>how latitude, altitude, aspect, proximity to water or soil "
           "influence temperature and sunlight</b>; <b>the effects of too much and too little "
           "water</b>; and <b>climate classification</b>, where the GDD calculation and WSET GST "
           "bands are straight recall. Adopt the chapter's own caution \u2014 models give only a "
           "broad picture."))

# ================================================================ temperature
s.append(H2("1. The Effects of Temperature"))
s.append(P("Solar radiation is the main source of <b>both heat and sunlight</b> \u2014 why so many "
           "factors influence the two together.", "note"))
s.append(EXHIBIT("EXHIBIT 3.1 \u2014 TEMPERATURE THROUGH THE GROWTH CYCLE", [
    ["Stage", "Effect"],
    ["Winter", "Below <b>10\u00b0C / 50\u00b0F</b> ensures dormancy. Around <b>\u221220\u00b0C / \u22124\u00b0F</b> causes "
     "winter freeze"],
    ["Budburst", "Above <b>10\u00b0C / 50\u00b0F</b> stimulates it, more uniform with a sharp "
     "temperature rise. Warm soil also helps. Frost harms buds and new growth"],
    ["Shoot growth", "Photosynthesis optimal <b>18\u201333\u00b0C / 64\u201391\u00b0F</b> \u2014 so temperature is "
     "<b>not usually limiting</b> here"],
    ["Flowering &amp; fruit set", "Flowering above <b>17\u00b0C / 63\u00b0F</b>; fruit set "
     "<b>26\u201332\u00b0C / 79\u201390\u00b0F</b>. Cold, damp conditions reduce yield and potentially quality"],
    ["Bud fruitfulness", "Above <b>25\u00b0C / 77\u00b0F</b> is best \u2014 affects <i>next</i> season's yields"],
    ["Ripening", "Sugar accumulation faster when warm; malic degradation increased. Above "
     "<b>21\u00b0C / 70\u00b0F</b> mean in the final month \u2192 rapid acid loss; below <b>15\u00b0C / 59\u00b0F</b> "
     "\u2192 acidity too high. Anthocyanin synthesis optimal <b>15\u201325\u00b0C / 59\u201377\u00b0F</b>"],
    ["Extreme heat", "With dry conditions, photosynthesis slows or stops. Water stress closes "
     "stomata, limiting CO\u2082 \u2014 same result, second route"],
], [76, W - 76], keep=False))
s += BUL([
    "<b>Tannin synthesis</b> is <i>thought</i> to follow the same 15\u201325\u00b0C pattern as "
    "anthocyanins, but <b>more research is needed</b>. Reproduce that hedge.",
    "<b>Late-ripening</b> varieties need more heat across the season, for sugar and for aroma and "
    "tannin ripeness. <b>Early-ripening</b> varieties \u2014 <b>Pinot Noir, Chardonnay</b> \u2014 need "
    "less and ripen very early in warm climates.",
])

# ================================================================ sunlight
s.append(H2("2. The Effects of Sunlight"))
s.append(P("<b>Full sunshine is not essential.</b> Light limits photosynthesis only below "
           "<b>one third of full sunshine</b> \u2014 fog can slow it, an average cloudy day will not.",
           "note"))
s.append(H4("WHAT GRAPE EXPOSURE TO SUNSHINE DOES"))
s += BUL([
    "Enhances <b>anthocyanin</b> development in black grapes; <b>reduces methoxypyrazines</b>; "
    "increases some favourable aroma compounds \u2014 <b>terpenes</b>, e.g. the grapey aroma of Muscat.",
    "Greater <b>tannin accumulation pre-v\u00e9raison</b>; promotes <b>polymerisation post-v\u00e9raison</b>, "
    "reducing bitterness. Also <b>warms the grapes</b>, raising malic respiration and so "
    "<b>lowering acidity</b>.",
    "Prolonged sunshine with heat causes <b>sunburn</b>. In warm, hot or very sunny climates some "
    "shading is beneficial \u2014 aim for <b>one thin layer of leaves</b> giving dappled sunshine.",
    "Late spring / early summer sunshine aids <b>fruit set</b>, and exposure of compound buds "
    "promotes <b>bud fruitfulness next season</b>.",
])

# ================================================================ natural factors
s.append(H2("3. Natural Factors Affecting Temperature and Sunlight"))

s.append(H3("Latitude"))
s += BUL([
    ("Lower latitudes (<b>Mendoza, South Africa, New South Wales</b>) receive <b>more and more "
     "intense</b> solar radiation than higher ones (<b>northern France, Germany</b>), for two "
     "reasons:", [
        "Radiation is <b>absorbed</b> (water droplets, dust, ozone) and <b>scattered</b>; Earth's "
        "curvature means it crosses <b>more atmosphere</b> near the poles.",
        "It strikes at a <b>low angle</b> near the poles, spreading over a larger area; near the "
        "Equator it arrives nearer perpendicular and is more powerful.",
    ]),
    "<b>All other factors equal</b>, low-latitude grapes show higher sugar, lower acidity, riper "
    "aromas and \u2014 in black grapes \u2014 higher but riper tannins and more colour.",
    "<b>Daylight hours:</b> low latitudes are similar year-round; high latitudes have <b>longer "
    "summer days</b>, allowing a longer daily period of photosynthesis \u2014 useful given their "
    "cooler temperatures.",
    "Wine grapes generally grow between <b>30\u00b0 and 50\u00b0</b> either side of the Equator, with "
    "exceptions. Nearer the Equator is usually too hot by day (water stress, sunburn); nearer the "
    "poles is not warm enough for sufficient sugar despite long days.",
])

s.append(H3("Altitude"))
s += BUL([
    "Temperature falls approximately <b>0.6\u00b0C (1.1\u00b0F) per 100 m</b>.",
    "High altitude suits <b>low latitudes</b> otherwise too hot \u2014 <b>Salta</b> has vineyards to "
    "approximately <b>3,000 m</b>, where grapes may struggle to ripen every year. Conversely the "
    "best <b>Burgundy and Loire</b> sites sit at relatively <b>low</b> altitudes.",
    "Sunshine and <b>ultraviolet radiation</b> are more intense \u2014 both thought to promote "
    "<b>anthocyanin and tannin synthesis</b>.",
    "Thin air holds less moisture, so heat escapes rapidly at night \u2192 <b>high diurnal range</b>.",
])

s.append(H3("Slopes and Aspect"))
s.append(P("<b>Aspect</b> = the direction a slope faces. Sun-facing means <b>south</b> in the "
           "northern hemisphere, <b>north</b> in the southern. It matters most <b>at high "
           "latitudes</b>, where radiation arrives at a low angle and the slope raises it nearer "
           "perpendicular; the angle is lowest in <b>spring and autumn</b>, so a favourable slope "
           "<b>extends the season at both ends</b>.", "note"))
s.append(FIGURE("FIGURE 3.1 \u2014 ASPECT AND THE ANGLE OF INCIDENCE", SlopeDiagram()))
s += BUL([
    "<b>Towards the sun</b> \u2014 can decide viability, varieties growable and ripeness. "
    "<b>Burgundy and Alsace</b>: Grand Cru sites on <b>south-east facing</b> slopes, generic "
    "appellation on the flat.",
    "<b>Away from the sun</b> \u2014 limits heat and light; permits earlier-ripening varieties, lower "
    "alcohol, higher acidity. <b>Stellenbosch</b> plants whites on <b>south-facing</b> slopes to "
    "retain acidity.",
    "<b>East</b> \u2014 morning sun warms air when temperatures are lowest, extending daily ripening "
    "hours; dew dries earlier, <b>reducing fungal disease</b>.",
    "<b>West</b> \u2014 afternoon sun; may be too hot and raise sunburn risk, unless a westerly coast "
    "supplies cool breezes (<b>California, Western Australia</b>).",
])
s.append(P("Slopes also give shallower poorer soils, better drainage, shelter from wind and rain, "
           "and frost protection as air moves downslope \u2014 against <b>soil erosion</b> and the "
           "<b>inability to mechanise</b> steep sites.", "note"))

s.append(H3("Proximity to Water"))
s.append(P("Water heats and cools more slowly than dry land \u2014 the single property from which the "
           "whole moderating effect follows.", "note"))
s += BUL([
    "<b>By day:</b> air above land heats faster and rises; cool air is drawn in from above the "
    "water \u2192 <b>cool, humid afternoon breezes</b>.",
    "<b>By night:</b> the water retains its warmth while land cools quickly \u2192 the area stays "
    "<b>warmer</b>.",
    "<b>Across the year:</b> <b>cooler summers and milder winters</b>.",
])
s.append(EXHIBIT("EXHIBIT 3.3 \u2014 THE WORKED EXAMPLES", [
    ["Region", "What proximity to water does"],
    ["Finger Lakes, NY", "Deep lakes reduce <b>winter freeze</b> severity; air movement also "
     "protects against spring frosts"],
    ["Carneros, CA", "<b>San Pablo Bay</b> and cooling afternoon breezes allow early-ripening "
     "Chardonnay and Pinot Noir; late-ripening Cabernet Sauvignon grows further inland"],
    ["Willamette <i>vs</i> Margaux", "Both near <b>45\u00b0</b>, yet two climate bands apart \u2014 the "
     "<b>Gulf Stream</b> warms Margaux, the <b>California current</b> cools Willamette (see Figure "
     "3.3)"],
    ["Very close proximity", "<b>Reflected radiation</b> off the water \u2014 greatest at high "
     "latitudes, useful in cool, cloudy climates"],
], [76, W - 76], keep=False))
s.append(H4("EL NI\u00d1O-SOUTHERN OSCILLATION (ENSO)"))
s.append(P("<b>El Ni\u00f1o</b> (eastern Pacific warmer than average) brings high rainfall and "
           "hurricane risk to <b>S. America and California</b> \u2014 disrupting pollination and fruit "
           "set, and increasing vegetative growth at the expense of ripening; warmth and drought to "
           "<b>Australia</b>, causing extreme vine stress; and warmer, drier conditions to "
           "<b>Washington and Oregon</b>. <b>La Ni\u00f1a</b> inverts each. El Ni\u00f1o occurs typically "
           "<b>once every 3\u20137 years</b>, extreme events more rarely \u2014 though these are thought to "
           "be becoming more frequent as part of climate change.", "note"))

s.append(H3("Winds"))
s += BUL([
    "May <b>warm or cool</b> \u2014 valleys facing the coast (<b>Petaluma Gap</b>) funnel wind far "
    "inland; winds off hot land bring warmth (the <b>Zonda</b>, Mendoza). They reduce humid, "
    "stagnant canopy air (<b>less fungal disease</b>) but raise evapotranspiration and can damage "
    "vines and trellising.",
    "<b>Tree windbreaks</b> compete with the nearest vines for water and nutrients; <b>fences</b> "
    "avoid that but are less aesthetic and need maintenance.",
])

s.append(H3("Soil, Mist, Fog and Cloud"))
s += BUL([
    "<b>Free-draining</b> (sandy, stony) soils warm faster in spring, stimulating budburst and "
    "shoot growth \u2014 wanted in cool climates, but <b>raises frost risk</b>.",
    "<b>Light-coloured</b> chalk (<b>Sancerre, Champagne</b>) reflects radiation into the lower "
    "canopy, aiding cool cloudy climates; <b>dark</b> volcanic soils (<b>Etna</b>) and stony soils "
    "absorb heat and re-radiate it at night, letting colour and acid degradation continue.",
    "<b>Mist</b> (dense mist = <b>fog</b>) and <b>cloud</b> can limit photosynthesis and lower "
    "temperature, slowing sugar accumulation and acid degradation \u2014 beneficial in warm regions. "
    "Being water droplets, they raise humidity \u2192 fungal disease, or <b>noble rot</b> where "
    "afternoons are dry and sunny. Common mornings in <b>Sonoma, Napa, Leyda Valley, Sauternes</b>.",
])

s.append(H2("4. Diurnal Range"))
s.append(P("The average difference between day and night temperatures. <b>Continental and "
           "high-altitude</b> regions run high; regions <b>near large water</b> run low. The "
           "textbook is explicit that the precise effects are <b>not yet fully understood</b>.",
           "note"))
s += BUL([
    "<b>Warm / hot climates \u2014 HIGH range often favourable.</b> A cool night slows <b>malic "
    "respiration</b> and aids <b>anthocyanin formation</b>; day temperatures are too hot. "
    "<b>Mendoza, Ribera del Duero</b>.",
    "<b>Cool / moderate climates \u2014 LOW range may be favourable.</b> Night temperatures still "
    "allow ripening \u2014 acid degradation, anthocyanin synthesis \u2014 to continue. <b>Mornington "
    "Peninsula, Mosel</b>.",
])
s += BUL([
    "Night temperature also influences aroma: <b>warmer</b> nights break down more "
    "<b>methoxypyrazines</b> (valuable in cool climates); <b>cooler</b> nights retain more of some "
    "compounds such as <b>rotundone</b>.",
    "<b>Exceptions exist.</b> Cold nights <b>under 15\u00b0C / 59\u00b0F</b> appear beneficial in some cool "
    "climates \u2014 many top <b>Wachau</b> sites see cool days and cold nights, for reasons unknown.",
    "More certain: <b>extreme</b> growing-season cold or heat causes damage \u2014 spring frost or "
    "intense summer heat.",
])

# ================================================================ water
s.append(H2("5. Water"))
s.append(P("Minimum roughly <b>500 mm per year in cool climates, 750 mm in warm regions</b>. Water "
           "is needed for turgidity, photosynthesis and temperature regulation; it is the "
           "<b>solvent for nutrients</b> and the medium of all the vine's biochemical mechanisms.",
           "note"))
s.append(P("<b>Too little</b> water: stomata close <b>partially</b> to conserve it, but CO\u2082 entry "
           "falls too \u2014 photosynthesis is reduced or stopped, growth is stunted and ripening "
           "slows. Extreme stress brings leaf loss and vine death. <b>Too much</b> is a subtler "
           "problem, and is mostly a matter of <i>timing</i>.", "note"))
s.append(FIGURE("FIGURE 3.4 \u2014 WATER: THE EFFECT DEPENDS ON TIMING, NOT JUST AMOUNT", Matrix2x2(
    "Deficit", "Excess", "Pre-v\u00e9raison", "Post-v\u00e9raison",
    {"tl": ("Pre-v\u00e9raison \u00b7 deficit",
            "<b>Mild</b> stress is thought <b>beneficial</b> \u2014 checks vegetative growth, raises "
            "the skin-to-pulp ratio. <b>Severe</b> stress stunts growth before photosynthesis can "
            "fund it."),
     "tr": ("Pre-v\u00e9raison \u00b7 excess",
            "Prolongs vegetative growth into ripening, competing for the vine's sugars; the dense "
            "canopy shades bunches, cutting colour, tannin and aroma."),
     "bl": ("Post-v\u00e9raison \u00b7 deficit",
            "Early grape shrivel and reduced ability to reach the desired ripeness."),
     "br": ("Post-v\u00e9raison \u00b7 excess",
            "Dilutes sugars and can split the grapes, encouraging botrytis.")},
    height=182, x_axis="the optimum between v\u00e9raison and ripening is not clearly established")))
s += BUL([
    "Water also acts on the <b>environment</b>: damp soils are cold and delay budburst; hail damages "
    "green parts; rain at pollination and fruit set cuts yields or causes uneven ripening; rain "
    "raises canopy humidity \u2192 downy mildew and botrytis.",
    "<b>Low humidity</b> raises evapotranspiration and water-stress potential \u2014 but also grape "
    "transpiration and so <b>higher sugar accumulation</b>. Proximity to water raises humidity, "
    "which is why many <b>botrytised sweet wine</b> regions lie near it: <b>Sauternes, Tokaj, "
    "Mosel</b>.",
])
s.append(EXHIBIT("EXHIBIT 3.6 \u2014 THREE DETERMINANTS OF WATER SUPPLY", [
    ["Factor", "How it works, and the examples that carry marks"],
    ["<b>Rainfall</b>", "Mountains force moist winds upward \u2192 precipitation on one side, a "
     "<b>rain shadow</b> on the other. West of the <b>Cascades</b>, Puget Sound is cool and wet, "
     "and growers <b>dry farm</b>; east, Columbia Valley <b>requires irrigation</b>. Rain also "
     "wets the canopy and raises humidity \u2192 fungal disease"],
    ["<b>Soil and land</b>", "Depends on drainage, water-holding properties and <b>depth</b>. "
     "<b>Hawke's Bay</b>: ~<b>1,000 mm</b>, yet free-draining Gimblett Gravels often need "
     "irrigation. <b>Jerez</b>: <b>650 mm</b>, almost none in summer, yet needs none \u2014 "
     "<b>albariza</b> clay retains water, releases it slowly, crusts when dry. <b>Waterlogging</b> "
     "starves roots of oxygen. Slopes shed run-off \u2014 useful in high rainfall, but it <b>erodes "
     "soil and leaches nutrients</b>"],
    ["<b>Evapotranspiration</b>", "Vine transpiration plus soil evaporation. Depends on "
     "<b>temperature, humidity and wind</b>; hot, dry, windy conditions (<b>Mendoza, Patagonia</b>) "
     "are fastest \u2014 usually where rainfall is least, so irrigation may be needed"],
    ], [80, W - 80], keep=False))

# ================================================================ nutrients
s.append(H2("6. Nutrients"))
s.append(P("Vines need <b>low levels</b> of nutrients, so most soils sustain them unless "
           "over-cropped \u2014 but viticulture depletes them, so the grower must monitor for "
           "deficiency.", "note"))
s.append(EXHIBIT("EXHIBIT 3.7 \u2014 THE FIVE NAMED NUTRIENTS", [
    ["Nutrient", "Role", "Excess / deficiency"],
    ["<b>Nitrogen</b>", "In proteins and chlorophyll; major impact on vigour and quality",
     "<b>Excess:</b> excessive vegetative growth, sugars diverted to shoots and leaves; shading of "
     "fruit and buds; poor ventilation \u2192 fungal disease. <b>Deficiency:</b> reduced vigour, "
     "yellowing leaves; problematic for fermentation. <b>Restricted nitrogen tends to give higher "
     "quality grapes</b>"],
    ["<b>Potassium</b>", "Essential for growth; regulates water flow",
     "<b>Excess:</b> impairs <b>magnesium</b> uptake \u2192 reduced yields, poor ripening; high soil "
     "\u2192 high grape potassium \u2192 <b>high must pH</b>. <b>Deficiency:</b> low sugar accumulation, "
     "reduced yields, poor growth"],
    ["<b>Phosphorus</b>", "Important for photosynthesis; small amounts, usually sufficient "
     "naturally", "<b>Deficiency:</b> poorly developed roots \u2192 diminished uptake; reduced growth; "
     "lower yields"],
    ["<b>Calcium</b>", "Cell structure and photosynthesis",
     "<b>Deficiency:</b> rare, but harms <b>fruit set</b>"],
    ["<b>Magnesium</b>", "In chlorophyll; key to photosynthesis",
     "<b>Deficiency:</b> reduced yields and poor ripening"],
], [56, 88, W - 144], keep=False))
s += BUL([
    "Others: <b>sulfur, manganese, boron, copper, iron, zinc</b>.",
    "Nutrients dissolve in soil water \u2014 <b>every soil factor affecting water also affects "
    "nutrients</b>.",
    ("<b>Soil pH</b> governs availability:", [
        "<b>Iron</b> is poorly available at <b>high pH</b> (calcium carbonate, limestone) \u2192 "
        "<b>chlorosis</b>: leaves yellow, photosynthesis stops, ripening and yields suffer.",
        "<b>Phosphorus</b> uptake is difficult in <b>highly acidic</b> soils.",
    ]),
    "<b>Mineralisation:</b> organic compounds (manure, compost) are unavailable to the vine until "
    "soil organisms \u2014 bacteria, fungi, earthworms \u2014 convert them to inorganic forms. "
    "Encouraging soil life is therefore thought highly beneficial.",
    "<b>Texture:</b> clay holds nutrients well, sand poorly; <b>humus</b> increases holding "
    "capacity. Soils on <b>slopes</b> are thinner and less fertile.",
])

# ================================================================ soil
s.append(H3("Soil: Texture, Structure and Humus"))
s.append(P("Soil = geological sediment from weathered bedrock + organic remains as <b>humus</b> + "
           "pores holding water and air. Often several layers of different ages, and "
           "<b>the sediment need not match the bedrock beneath</b> \u2014 it may have been transported "
           "by water, wind, glaciers or gravity.", "note"))
s.append(CALLOUT("THE CLAIM THE TEXTBOOK EXPLICITLY DECLINES TO MAKE", [
    P("<b>Scientific backing linking soil or bedrock chemistry to particular aromas or flavours is "
      "lacking.</b> What <i>is</i> well recognised is the importance of the soil's <b>physical "
      "parameters</b> on water availability, and so on vine growth and ripening.", "box"),
    P("Physical parameters also affect nutrient availability, but since vines need few nutrients "
      "and fertilisers are easy to apply, this is thought <b>less impactful</b>.", "box"),
]))
s.append(FIGURE("FIGURE 3.2 \u2014 SOIL TEXTURE: THE THREE MINERAL FRACTIONS", TextureTriangle()))
s += BUL([
    "<b>Structure</b> \u2014 how particles form <b>aggregates</b>. Very high clay is sticky, forming "
    "aggregates hard for roots to penetrate, so roots may be confined to cracks. Sandy or gravelly "
    "soils are loosely structured and <b>need some clay to bind them</b>.",
    "<b>Humus</b> \u2014 partial decomposition of plant and animal material by soil microbes and "
    "earthworms. Spongey, large surface area, adsorbs water and nutrients, binds soils.",
    "Suitability depends on texture and structure <b>plus how far roots can penetrate</b>. Very "
    "sandy or stony soils may suit if roots grow freely and deeply. Free-draining soils avoid "
    "excess water in rainy climates \u2014 the gravels of the <b>Haut-M\u00e9doc</b>. Excess water "
    "displaces the oxygen roots need; waterlogging eventually kills the vine.",
])

# ================================================================ climate
s.append(H2("7. Climate Classifications"))
s.append(P("<b>Climate</b> = the annual pattern of temperature, sunlight, rainfall, humidity and "
           "wind averaged over several years \u2014 <b>30 years</b> is the agreed timescale. It does "
           "not change year to year, though it can alter over decades.", "note"))
s.append(CALLOUT("THE GDD CALCULATION \u2014 LEARN IT AS A PROCEDURE", [
    P("<b>1.</b> Subtract <b>10</b> (\u00b0C) or <b>50</b> (\u00b0F) from the average mean temperature of a "
      "month in the growing season.", "box"),
    P("<b>2.</b> Multiply by the number of days in that month.", "box"),
    P("<b>3.</b> Repeat for every month of the growing season \u2014 <b>April\u2013October</b> (NH), "
      "<b>October\u2013April</b> (SH) \u2014 and sum. <b>Negative months are not counted.</b>", "box"),
    P("Grouped into <b>five bands</b>: <b>Winkler Zone I</b> (cool) to <b>Zone V</b> (very hot). "
      "Updated relatively recently with new bands at both ends.", "box"),
]))
s.append(EXHIBIT("EXHIBIT 3.8 \u2014 THE FOUR MODELS", [
    ["Model", "Author, date", "Basis"],
    ["Growing Degree Days", "Amerine and Winkler, 1944",
     "Heat summation over the season; five Winkler bands. Originally for California"],
    ["Huglin Index", "Huglin, 1978", "Uses <b>mean and maximum</b> temperatures and accounts for "
     "<b>increased day length at higher latitudes</b>. Bands mapped to suitable varieties. "
     "<b>Widely used in Europe</b>"],
    ["Mean Temp. of Warmest Month (MJT)", "Smart and Dry, 1980",
     "Mean of <b>July</b> (NH) / <b>January</b> (SH), plus continentality, humidity and sunshine. "
     "<b>Six bands</b>, cold to very hot"],
    ["Growing Season Temperature (GST)", "\u2014",
     "Mean of the whole growing season. <b>Very closely correlated to GDD and easier to calculate</b>"],
], [82, 68, W - 150], keep=False))
s.append(EXHIBIT("EXHIBIT 3.9 \u2014 MARITIME, MEDITERRANEAN, CONTINENTAL (AFTER K\u00d6PPEN, 1900; TEMPERATE ZONES ONLY)", [
    ["Category", "Summer / winter difference", "Rainfall", "Examples"],
    ["Maritime", "Low", "Evenly spread through the year", "Bordeaux"],
    ["Mediterranean", "Low", "Falls in <b>winter</b> \u2014 dry summers", "Napa Valley, Coonawarra"],
    ["Continental", "<b>More extreme.</b> Often short summers, cold winters, rapid spring and "
     "autumn change", "\u2014", "Burgundy, Alsace"],
], [62, 88, 82, W - 232], keep=False))
s.append(H4("WHAT THE CATEGORIES PREDICT"))
s += BUL([
    "<b>Continental</b> extremes can bring winter freeze, but the rapid spring rise often gives "
    "<b>even budburst</b>; the rapid autumn drop gives a <b>shorter season</b>.",
    "<b>Warm summers</b> reduce the risk of insufficient sugar \u2014 but sugar may be high and acid "
    "low <i>before</i> aromas, colour and tannins ripen, giving high alcohol and low acid. "
    "<b>Cool</b> seasons risk the reverse, though maritime and Mediterranean climates often give "
    "<b>long autumns</b> that extend the season.",
    "<b>Even rainfall</b> makes extreme water stress less likely, but excess causes vigour, and "
    "rain raises humidity and disease near harvest. Cool, cloudy, rainy late spring brings <b>poor "
    "flowering and fruit set</b>.",
    "<b>Continentality</b> = the difference between the annual mean temperatures of the "
    "<b>hottest and coldest months</b>. Near large water = <b>low</b> (maritime / Mediterranean); "
    "far inland or shielded = <b>high</b> (continental).",
])

s.append(FIGURE("FIGURE 3.3 \u2014 THE WSET CLIMATE BANDS BY AVERAGE GROWING SEASON TEMPERATURE",
    ThresholdScale(14, 24,
        bands=[(14, 16.5, "COOL", COOL), (16.5, 18.5, "MODERATE", MILD),
               (18.5, 21, "WARM", WARM), (21, 24, "HOT", HOT)],
        marks=[(15.9, "Willamette 15.9"), (17.7, "Margaux 17.7"),
               (16.5, "16.5\u00b0C / 62\u00b0F"), (18.5, "18.5\u00b0C / 65\u00b0F"), (21, "21\u00b0C / 70\u00b0F")]),
    note="Willamette and Margaux sit at the same latitude \u2014 roughly 45\u00b0 \u2014 but two bands apart, "
         "because of the cold California current and the warming Gulf Stream respectively."))
# ================================================================ weather
s.append(H2("8. Weather and Vintage Variation"))
s.append(P("<b>Weather</b> = annual variation relative to the climatic average. <b>Bordeaux</b> "
           "shows the range: <b>2013</b> \u2014 cold wet spring, uneven flowering, reduced yields, "
           "rainy humid harvest forcing early picking \u2014 low quantity <i>and</i> quality. "
           "<b>2016</b> \u2014 good flowering, long warm dry summer and harvest \u2014 high quality and "
           "volume. <b>Central Valley, California</b> is hot and dry season after season.", "note"))
s += BUL([
    "Weather affects sugar, acid, tannin and aroma ripeness, and so winemaking \u2014 must or wine "
    "adjustments, or <b>greater extraction in warmer years</b> to balance higher alcohol.",
    "Vintage variation is <b>welcomed</b> in some styles; in <b>non-vintage sparkling</b> and "
    "high-volume inexpensive wines it is not, since consumers expect consistency.",
    "<b>Both yield directions are problematic.</b> Lower: disease or frost, and less wine to sell "
    "damages cash flow and customer relations. Higher: the winery may lack capacity or a "
    "profitable route to market. Some producers make <b>different styles in cooler years</b> \u2014 "
    "more sparkling or ros\u00e9.",
])

# ================================================================ climate change
s.append(H2("9. Climate Change"))
s += BUL([
    "Main measurable effect: <b>rising temperature</b> \u2192 <b>greater evapotranspiration</b> and "
    "water stress, plus changed rainfall distribution and more extreme events.",
    "Aroma profiles may be lost \u2014 <b>black pepper</b> in Syrah from the <b>Northern Rh\u00f4ne</b> may "
    "no longer develop \u2014 and some regions may need <b>later-ripening varieties</b>. "
    "<b>Potential upside:</b> production may improve in regions previously too cold.",
    "Already-dry regions (<b>California, South Africa</b>) risk <b>extreme water stress</b> and "
    "some sites are thought likely to be <b>abandoned in 50\u2013100 years</b>; even well-watered "
    "regions face more rain <b>just before harvest</b>. Storms, floods, frosts and heatwaves cut "
    "yields or quality <b>everywhere</b>.",
    "Producers act to <b>mitigate</b> (renewable energy, protecting ecosystems) and <b>adapt</b> "
    "(site selection, planting material, management).",
])

s.append(FlowChart([
    ("WARMER TEMPERATURES", "The vine cycle runs faster \u2014 earlier budburst, every stage quicker",
     None),
    ("DIVERGENCE OPENS", "Sugar accumulation and acid reduction speed up \u2014 but the ripening of "
     "<b>most aroma and tannin compounds does not</b>", None),
    ("THE GROWER MUST CHOOSE", "Grapes are picked at <b>higher sugar</b> to protect aroma, tannin "
     "and colour \u2192 <b>higher alcohol, lower acidity, higher pH</b>", None),
], box_w=W * 0.78))
s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER THREE", [
    P("<b>1. Derive the mechanism, then name the example.</b> Water heats and cools more slowly "
      "than land \u2014 <i>then</i> Carneros.", "box"),
    P("<b>2. Say \u2018all other factors being equal\u2019 \u2014 then show one that isn't.</b> Willamette "
      "and Margaux sit at the same 45\u00b0 latitude yet differ, via the Gulf Stream and California "
      "current.", "box"),
    P("<b>3. Separate physical from chemical on soil.</b> Physical parameters have well-recognised "
      "effects; chemical links to specific aromas <b>lack scientific backing</b>.", "box"),
    P("<b>4. Answer warm and cool cases separately.</b> Aspect, diurnal range, soil colour and mist "
      "are each wanted in one climate and not the other.", "box"),
    P("<b>5. Carry climate through to the glass.</b> Sugar and acid ripeness diverge from aroma and "
      "tannin ripeness in warm conditions \u2014 explaining warm-climate alcohol, diurnal range, "
      "altitude at low latitude, and climate change alike.", "box"),
]))

s.append(exam_traps([
 ("Saying vines need full sunshine.",
  "Light limits photosynthesis only <b>below one third of full sunshine</b>. In warm climates some "
  "shading is <i>beneficial</i> \u2014 one thin layer of leaves, dappled sunshine."),
 ("Getting aspect backwards, or forgetting the southern hemisphere.",
  "Sun-facing = <b>south</b> (NH), <b>north</b> (SH). <b>Stellenbosch</b> plants whites on "
  "south-facing slopes deliberately, to retain acidity."),
 ("Claiming soil chemistry produces flavours.",
  "Scientific backing <b>is lacking</b>. Argue from <b>physical</b> parameters \u2014 water "
  "availability, drainage, heat retention."),
 ("Treating high diurnal range as universally good.",
  "Effects are <b>not fully understood</b>. High suits warm climates (Mendoza); <b>low</b> may suit "
  "cool ones (Mosel). The <b>Wachau</b> contradicts both."),
 ("Fumbling the GDD calculation.",
  "Subtract <b>10\u00b0C / 50\u00b0F</b> from the month's mean, multiply by days, sum across the "
  "season. <b>Negative months are not counted.</b>"),
]))

# ================================================================ exam
exam = []

MCQ = [
 dict(q="Light becomes the limiting factor on the rate of photosynthesis only when levels fall below:",
      opts=["Two thirds of full sunshine", "One half of full sunshine",
            "One third of full sunshine", "One tenth of full sunshine"],
      ans=2, why="Below one third of full sunshine. This is why fog can slow photosynthesis but "
                 "an average cloudy day does not."),
 dict(q="Temperature falls by approximately how much for every 100 m increase in altitude?",
      opts=["0.2\u00b0C / 0.4\u00b0F", "0.6\u00b0C / 1.1\u00b0F", "1.2\u00b0C / 2.2\u00b0F", "2.0\u00b0C / 3.6\u00b0F"],
      ans=1, why="0.6\u00b0C per 100 m \u2014 the figure that makes high-altitude sites viable at low "
                 "latitudes, as in Salta at up to approximately 3,000 m."),
 dict(q="A vineyard in Stellenbosch planted on a south-facing slope is most likely intended to:",
      opts=["Maximise solar radiation to ripen late-ripening varieties",
            "Limit heat and light so that white grapes retain refreshing acidity",
            "Reduce the risk of spring frost damage to young buds",
            "Increase reflected radiation into the lower canopy"],
      ans=1, why="Stellenbosch is in the southern hemisphere, so south-facing faces away from "
                 "the sun \u2014 the textbook's example of deliberately limiting heat and light."),
 dict(q="The minimum annual rainfall the vine generally needs in a WARM region is approximately:",
      opts=["350 mm", "500 mm", "650 mm", "750 mm"],
      ans=3, why="At least 750 mm in warm regions, against ~500 mm in cool climates. 650 mm is "
                 "the Jerez figure \u2014 a deliberate distractor."),
 dict(q="Chlorosis in the vine is caused by:",
      opts=["Poor availability of iron in soils of high pH",
            "Poor availability of phosphorus in highly acidic soils",
            "Excessive potassium impairing magnesium uptake",
            "Calcium deficiency at fruit set"],
      ans=0, why="Iron is poorly available in high-pH soils (calcium carbonate, limestone). "
                 "Leaves yellow and photosynthesis stops. The other three are real, but not "
                 "chlorosis."),
 dict(q="Which statement about soil texture is correct?",
      opts=["Sand particles have a large surface area relative to volume and hold nutrients well",
            "Clay particles are very small, with a large surface area relative to volume, and hold water and nutrients effectively",
            "Loam describes a soil consisting almost entirely of silt",
            "Gravel and pebbles improve both drainage and water-holding capacity"],
      ans=1, why="Clay is finely textured, holding water and nutrients well. Sand is the "
                 "reverse; loam mixes all three; larger fragments improve drainage but LOWER "
                 "holding capacity."),
 dict(q="In the Growing Degree Days calculation, months returning a negative value are:",
      opts=["Counted as zero and included in the total",
            "Not counted at all",
            "Counted at half their absolute value",
            "Subtracted from the running total"],
      ans=1, why="Negative months are not counted. The base is 10\u00b0C / 50\u00b0F, growing season "
                 "April\u2013October in the northern hemisphere."),
 dict(q="Under the WSET bands, a region with an average growing season temperature of 19\u00b0C is classified as:",
      opts=["Cool", "Moderate", "Warm", "Hot"],
      ans=2, why="Warm is 18.5\u201321\u00b0C (65\u201370\u00b0F). Cool is 16.5\u00b0C or below, moderate 16.5\u201318.5\u00b0C, "
                 "and hot exceeds 21\u00b0C."),
 dict(q="A Mediterranean climate is distinguished from a maritime climate principally by:",
      opts=["A greater difference between summer and winter temperatures",
            "Rainfall concentrated in the winter months, giving dry summers",
            "Consistently higher growing season temperatures",
            "Its location outside the temperate zones"],
      ans=1, why="Both have low annual temperature differences. The distinction is rainfall: "
                 "Mediterranean falls in winter, maritime is spread evenly."),
 dict(q="Rising temperatures under climate change tend to produce wines higher in alcohol because:",
      opts=["Yeasts become more efficient at fermenting sugar at higher temperatures",
            "Sugar accumulation accelerates but aroma and tannin ripening does not, so grapes are picked at higher sugar",
            "Warmer conditions increase the total quantity of tartaric acid in the grape",
            "Higher evapotranspiration concentrates sugars during the extra-ripening stage"],
      ans=1, why="Increased temperatures speed sugar accumulation and acid reduction but do not "
                 "quicken the ripening of most aroma and tannin compounds. To protect those, "
                 "growers pick later and therefore at higher sugar."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) How the growing environment influences temperature and sunlight"),
 P("Solar radiation is the main source of both heat and sunlight, so the factors governing one "
   "generally govern the other. Six natural factors matter."),
 P("<b>Latitude</b> is the primary control. Lower latitudes receive more, and more intense, "
   "radiation, for two reasons: radiation is absorbed by water droplets, dust and ozone and "
   "scattered as it crosses the atmosphere, and Earth's curvature means a greater depth of "
   "atmosphere near the poles; it also strikes at a lower angle there, spreading over a larger "
   "area, versus nearer-perpendicular at the Equator. All else equal, lower-latitude grapes show "
   "higher sugar, lower acidity, riper aromas and, in black varieties, higher but riper tannins "
   "and more colour. Latitude also sets daylight hours: high latitudes have longer summer days, "
   "extending daily photosynthesis and partly offsetting their cooler temperatures."),
 P("<b>Altitude</b> cuts temperature by about 0.6\u00b0C per 100 metres. This makes high-altitude "
   "sites viable at low latitudes otherwise too hot, as in Salta, where vineyards up to around "
   "3,000 metres may still struggle to ripen. The reverse holds too: Burgundy and the Loire "
   "Valley's best sites sit at relatively low altitude, since higher would be too cold. Sunshine "
   "and UV are both more intense at altitude, thought to promote anthocyanin and tannin "
   "synthesis, and thin air gives a large diurnal range since heat escapes fast at night."),
 P("<b>Slope and aspect</b> matter most at high latitudes, where a slope raises the low-angled "
   "radiation toward perpendicular; the angle is lowest in spring and autumn, so a sun-facing "
   "slope extends the season at both ends. Burgundy and Alsace show it directly: Grand Cru sites "
   "sit on south-east facing slopes, generic appellation on the flat. In warm climates the logic "
   "inverts \u2014 Stellenbosch plants whites on south-facing slopes to retain acidity. East-facing "
   "slopes gain morning sun when temperatures are lowest, extending ripening hours and drying dew "
   "early to cut fungal disease; west-facing slopes risk sunburn from afternoon sun, unless a "
   "westerly coast (California, Western Australia) supplies cool breezes."),
 P("<b>Proximity to water</b> works because water heats and cools more slowly than land: by day, "
   "warm rising air over land draws in cool air from the water, giving humid afternoon breezes; "
   "by night the water holds its warmth while land cools fast. The same applies seasonally \u2014 "
   "cooler summers, milder winters. The Finger Lakes reduce winter freeze severity; Carneros "
   "permits early-ripening Chardonnay and Pinot Noir, with Cabernet Sauvignon further inland "
   "where afternoons warm up. Ocean currents extend this: Margaux and the Willamette Valley both "
   "sit near 45\u00b0 latitude, yet Margaux ripens Cabernet Sauvignon at 17.7\u00b0C, warmed by the Gulf "
   "Stream, while Willamette at 15.9\u00b0C, cooled by the California current, grows Pinot Noir."),
 P("<b>Winds</b> warm or cool depending on what they cross \u2014 the Zonda brings warm air into "
   "Mendoza \u2014 and valleys funnel and strengthen them, as the Petaluma Gap carries maritime "
   "influence far inland. <b>Soil</b> acts directly: free-draining soils warm faster in spring, "
   "lengthening the season but raising frost risk; light chalk soils (Sancerre, Champagne) "
   "reflect light into the canopy; dark volcanic soils (Etna) absorb heat and re-radiate it at "
   "night, letting colour and acid degradation continue. <b>Mist, fog and cloud</b> reduce "
   "sunlight and temperature, slowing sugar accumulation and acid degradation \u2014 useful in warm "
   "regions \u2014 while raising humidity and so fungal disease, or noble rot where afternoons turn "
   "dry and sunny."),

 answer_head("Part b) Diurnal range"),
 P("Diurnal range is the average day-night temperature difference. Continental and "
   "high-altitude regions run high; regions near large water bodies run low. The precise effects "
   "are not yet fully understood \u2014 schools of thought favour both constant temperatures and "
   "significant night-time difference \u2014 and the outcome depends on average day and night "
   "temperatures, variety, timing and water availability."),
 P("In warm or hot climates a large range is often favourable \u2014 Mendoza and Ribera del Duero "
   "are the standard examples. Day temperatures there are too hot for optimal ripening, so the "
   "value lies in the night: a cool night slows malic respiration, preserving acidity, and "
   "benefits anthocyanin synthesis, optimal at 15\u201325\u00b0C rather than the day's higher "
   "temperatures."),
 P("In cool and moderate climates the reverse may apply \u2014 Mornington Peninsula and the Mosel "
   "are cited. Here the limit is total ripening, not acid retention, so warmer nights let acid "
   "degradation and anthocyanin synthesis continue overnight rather than halt at dusk."),
 P("Night temperature is also thought to affect aroma: warmer nights break down more "
   "methoxypyrazines, useful in cool climates where herbaceous character would otherwise "
   "persist, while cooler nights retain more of compounds like rotundone. Given the number of "
   "aroma compounds and their interactions, these relationships are complex and not settled."),
 P("Exceptions exist. Cold nights under 15\u00b0C appear beneficial in some cool climates \u2014 many "
   "top Wachau sites see cool days and cold nights, for unknown reasons, perhaps the extended "
   "season cool nights bring. More certain: extremely cold or hot growing-season temperatures "
   "cause damage, by spring frost or intense summer heat \u2014 the extremes are unambiguous even "
   "where the moderate cases are not."),
 examiner_note([
   P("Part a) derives each mechanism before naming the example, so examples serve as evidence, "
     "not decoration. The Willamette/Margaux comparison is the strongest single move: it takes "
     "the latitude rule from paragraph one and shows a case where another factor overrides it.",
     "box"),
   P("Part b) leads with the textbook's own uncertainty and organises by climate, not range, "
     "forcing real analysis. Naming the Wachau as a contradiction of both cases, and admitting "
     "the reasons are unknown, is exactly the calibrated confidence examiners reward.", "box"),
 ]),
]

q2 = [
 answer_head("Part a) The effects of water availability on the vine"),
 P("The vine needs a minimum of roughly 500 mm of rainfall a year in cool climates, 750 mm in "
   "warm regions. Water is needed for turgidity, photosynthesis and temperature regulation; it is "
   "the solvent that carries nutrients from the soil, and the medium for all the vine's "
   "biochemical processes. Both deficit and excess are damaging, and timing within the growth "
   "cycle determines how much."),
 P("<b>Insufficient water</b> acts through the stomata: water vapour diffuses out through these "
   "underside pores, and that loss pulls water up from the soil \u2014 transpiration. With enough "
   "water the stomata stay open all day, letting CO\u2082 and oxygen diffuse in and out; a shortage "
   "causes partial closure, conserving water but reducing or stopping photosynthesis, since CO\u2082 "
   "can no longer enter \u2014 so growth stalls and ripening slows. Extreme stress causes leaf loss "
   "and vine death. Lack of growing-season rainfall is a live issue in Argentina, California, "
   "South Africa and Australia, where irrigation is often what makes viticulture possible at "
   "all."),
 P("<b>Excess water</b> is subtler, mostly a matter of timing. Plentiful spring water is "
   "positive, building a large leaf surface area. But water too easily available into late "
   "spring and early summer prolongs vegetative growth into ripening, competing for the vine's "
   "sugars \u2014 why mild water stress before v\u00e9raison is thought beneficial, checking further "
   "vegetative growth. The knock-on effect is canopy density: excess shoots and leaves shade "
   "bunches, cutting anthocyanins, tannins and aroma compounds, reducing tannin polymerisation "
   "and raising methoxypyrazines, unless managed. Dense canopies also ventilate poorly, "
   "encouraging fungal disease in rainy or humid climates."),
 P("Between v\u00e9raison and ripening the optimum isn't clear, though neither severe stress nor "
   "plentiful water is favourable. Too much water late in ripening dilutes sugars and can split "
   "grapes, encouraging botrytis; a deficit brings early shrivel and limits ripeness."),
 P("Water also acts on the growing environment directly. Damp soils are often cold, delaying "
   "budburst and shortening the season; warm soils promote budburst and root growth. Rain at "
   "pollination and fruit set causes uneven ripening or lower yields, and raises canopy humidity, "
   "bringing downy mildew and botrytis. Low humidity does the opposite \u2014 raising "
   "evapotranspiration and water-stress potential, but also grape transpiration and so higher "
   "sugar accumulation."),

 answer_head("Part b) Natural factors governing water availability"),
 P("Three factors determine how much water reaches the roots."),
 P("<b>Rainfall</b> is the natural source, its amount and timing moderated by soil water-holding "
   "capacity and depth. Topography shapes distribution: mountains force moist air upward, "
   "cooling it so vapour condenses and precipitates on the windward side, leaving a rain shadow "
   "leeward. Washington State shows this cleanly \u2014 west of the Cascades, Puget Sound is cool and "
   "wet enough to dry farm; east of them, Columbia Valley needs irrigation to survive at all. "
   "Rain also wets the canopy and raises humidity, so frequent-rainfall regions are more prone to "
   "fungal disease."),
 P("<b>Soil characteristics</b> determine how much of that rainfall is retained \u2014 drainage, "
   "water-holding properties (texture, organic matter), and depth. Two contrasts make the point "
   "better than any rule. Hawke's Bay gets around 1,000 mm a year, yet the free-draining Gimblett "
   "Gravels often need irrigation. Jerez gets only 650 mm, almost none in summer, yet needs none: "
   "albariza clay retains water, releases it slowly and crusts when dry to cut evaporation \u2014 "
   "irrigation there is permitted only under extreme hydric stress. Rainfall totals alone are "
   "therefore a poor guide. At the other extreme, waterlogged soils starve roots of oxygen, "
   "slowing growth and eventually killing the vine. Topography intervenes again: slopes shed more "
   "surface run-off, useful where rainfall is high, but that run-off erodes soil and leaches "
   "nutrients, and slope soils are generally thin, limiting the vine's reach."),
 P("<b>Evapotranspiration rate</b> \u2014 vine transpiration plus soil evaporation \u2014 is the rate "
   "water stops being available. It depends on temperature, humidity and wind, fastest in hot, "
   "dry, windy conditions like Mendoza and Patagonia. The compounding problem: high "
   "evapotranspiration means the vine needs <i>more</i> water, yet such regions usually have the "
   "least rainfall \u2014 making irrigation a precondition of viticulture there, not a refinement."),
 examiner_note([
   P("Part a) explains water stress through the stomatal mechanism rather than asserting dry "
     "vines ripen poorly, and treats excess water as a timing and sugar-competition problem \u2014 "
     "the point most candidates miss.", "box"),
   P("Part b) pairs Hawke's Bay and Jerez to show rainfall totals alone don't predict water "
     "availability \u2014 a genuine argument, not a list. Closing on evapotranspiration and rainfall "
     "coinciding at their worst identifies the compounding effect, exactly the synthesis that "
     "separates the top band.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="The growing environment determines the resources available to the vine.",
      parts=[("Explain how natural factors in the growing environment influence the temperature "
              "and sunlight available to a vineyard, giving examples.", "15%"),
             ("Explain what is meant by diurnal range and evaluate its influence on grape "
              "ripening in different climates.", "10%")],
      answer=q1),
 dict(stem="Water availability shapes both vine growth and grape ripening.",
      parts=[("Explain the effects on the vine of both insufficient and excessive water "
              "availability at different points in the growing season.", "15%"),
             ("Explain the natural factors that determine how much water is available to the "
              "vine.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch3_The_Growing_Environment.pdf",
      "Chapter Three \u00b7 The Growing Environment", s, exam, maxpages=19)
