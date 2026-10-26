# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 3: The Growing Environment."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("3", "The Growing Environment",
             ["recall the key numbers and the climate bands",
              "explain what shapes heat and light at a site",
              "judge a high or low diurnal range, warm vs cool",
              "weigh too little or too much water, by timing",
              "calculate GDD and place a region in a band"])

# ============================================================ PAGE 1
f, a = cloze([
    "Light limits photosynthesis only below one {{third}} of full sunshine.",
    "Temperature falls by about {{0.6\u00b0C}} (1.1\u00b0F) for every {{100 m}} of altitude.",
    "Wine grapes generally grow between {{30\u00b0}} and {{50\u00b0}} either side of the Equator.",
    "Vines need at least {{500 mm}} of rain a year in cool climates and {{750 mm}} in warm ones.",
    "Climate is averaged over {{30}} years; El Ni\u00f1o recurs about every {{3\u20137}} years.",
    "GST bands: cool at or below {{16.5\u00b0C}}, moderate to {{18.5\u00b0C}}, warm to {{21\u00b0C}}, hot above.",
], width=58)
ch.ex("RECALL", "Numbers that matter", len(a), "Fill every blank. <b>1 point per blank.</b>", f,
      kp(ans_inline(a)), mins=4, ref="1\u20139")

_p2 = [("Latitude", "Lower latitudes get more intense radiation: higher sugar, lower acidity"),
       ("Altitude", "Cools about 0.6\u00b0C per 100 m; more UV; a large diurnal range"),
       ("Aspect", "The direction a slope faces; sun-facing is south in the northern hemisphere"),
       ("Proximity to water", "Water heats and cools slowly: cooler summers, milder winters"),
       ("Cloud and fog", "Water droplets limit photosynthesis and cool; raise humidity"),
       ("Light-colored chalk", "Reflects radiation into the lower canopy, helping cool climates"),
       ("Dark volcanic soil", "Absorbs heat and re-radiates it at night"),
       ("Wind", "Dries the canopy (less fungal disease) but raises evapotranspiration")]
_d2 = [4, 1, 6, 0, 3, 7, 2, 5]
_l2 = [chr(65 + _d2.index(i)) for i in range(8)]
ch.ex("MATCH", "What each factor does", 8, "Write the letter of the effect in each box.",
      match([p[0] for p in _p2], [_p2[i][1] for i in _d2], _l2),
      pairs([(str(i + 1), _l2[i]) for i in range(8)], ncols=4, width=COLW), mins=4, ref="3")
ch.page()

# ============================================================ PAGE 2
_r3 = ["A sun-facing slope (south in the northern hemisphere)", "A slope facing away from the sun",
       "A high diurnal range", "A low diurnal range", "Light-colored chalk reflecting radiation",
       "Morning mist and cloud slowing sugar and acid loss", "Free-draining soil that warms fast in spring",
       "A west-facing slope with cooling coastal breezes"]
_a3 = ["Cool", "Warm/hot", "Warm/hot", "Cool", "Cool", "Warm/hot", "Cool", "Warm/hot"]
ch.ex("TICK", "Warm or cool climate?", 8,
      "Tick the climate in which each feature is most often <b>wanted</b>. Each is wanted in one and not the other.",
      tickgrid(_r3, ["Warm / hot", "Cool"]),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, x) for i, x in enumerate(_a3))), mins=4, ref="3\u20134")

_w = [["Pre-v\u00e9raison", Blank("Mild stress is beneficial (checks growth, raises skin-to-pulp ratio); severe stress stunts growth", 3),
       Blank("Prolongs vegetative growth into ripening; dense canopy shades bunches, cutting color, tannin, aroma", 3)],
      ["Post-v\u00e9raison", "Early grape shrivel and reduced ability to reach the desired ripeness",
       Blank("Dilutes sugars and can split grapes, encouraging botrytis", 2)]]
ch.ex("COMPARE", "Water: timing, not just amount", 3, "Complete the dotted cells.",
      compare(["", "Too little water", "Too much water"], _w, [88, 215, 215]),
      kp("<b>Pre-v\u00e9raison deficit:</b> mild stress is beneficial; severe stunts growth. "
         "<b>Pre-v\u00e9raison excess:</b> prolongs vegetative growth, shades bunches, cuts color, tannin and aroma. "
         "<b>Post-v\u00e9raison excess:</b> dilutes sugars, can split grapes and encourage botrytis."), mins=4, ref="5")
ch.page()

# ============================================================ PAGE 3
_p5 = [("Nitrogen", "In proteins and chlorophyll; excess drives shading and disease, restricted N favors quality"),
       ("Potassium", "Essential for growth and water flow; excess blocks magnesium and raises must pH"),
       ("Phosphorus", "Needed in small amounts for photosynthesis; deficiency gives poor roots"),
       ("Calcium", "Cell structure and photosynthesis; deficiency is rare but harms fruit set"),
       ("Magnesium", "Part of chlorophyll; deficiency reduces yields and ripening")]
_d5 = [3, 0, 4, 2, 1]
_l5 = [chr(65 + _d5.index(i)) for i in range(5)]
ch.ex("MATCH", "The five named nutrients", 5, "Match each nutrient to its role and its problem.",
      match([p[0] for p in _p5], [_p5[i][1] for i in _d5], _l5),
      pairs([(str(i + 1), _l5[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="6")

_ch = [("Soil pH", ["High soil pH (limestone)", Blank("Iron is poorly available"), Blank("Chlorosis: leaves yellow, photosynthesis stops"),
                    "Poor ripening and low yields"]),
       ("Excess nitrogen", ["Excess nitrogen", Blank("Excess shoot growth; sugars diverted"), Blank("Fruit shaded, poor ventilation"),
                            "More fungal disease"])]
ch.ex("CHAIN", "Cause, effect, consequence", 4, "Complete each chain with the missing links.",
      [Chain(items, label=lab, box_h=44) for lab, items in _ch],
      kp("<b>1</b> iron poorly available \u2192 chlorosis (yellow leaves, photosynthesis stops). "
         "<b>2</b> excess shoot growth, sugars diverted \u2192 shaded fruit, poor ventilation."), mins=3, ref="6")

_r7 = ["Bordeaux", "Napa Valley", "Coonawarra", "Burgundy", "Alsace"]
_a7 = ["Maritime", "Mediterranean", "Mediterranean", "Continental", "Continental"]
ch.ex("TICK", "Maritime, Mediterranean or continental?", 5, "Tick one type for each region.",
      tickgrid(_r7, ["Maritime", "Mediterranean", "Continental"]),
      kp(" \u00b7 ".join("<b>%s</b> %s" % (r, a) for r, a in zip(_r7, _a7))), mins=2, ref="7")
ch.page()

# ============================================================ PAGE 4
_p8 = [("Growing degree days", "Heat summation (Amerine and Winkler); five Winkler zones"),
       ("Huglin Index", "Mean and maximum temperatures plus day length; used in Europe"),
       ("MJT", "Mean July/January temperature plus continentality, humidity, sunshine"),
       ("GST", "Mean of the whole growing season; tracks GDD, easier to find"),
       ("Continentality", "Gap between hottest and coldest month means; low near water")]
_d8 = [3, 0, 4, 1, 2]
_l8 = [chr(65 + _d8.index(i)) for i in range(5)]
ch.ex("MATCH", "Four climate models and continentality", 5, "Match each model, or measure, to what makes it distinctive.",
      match([p[0] for p in _p8], [_p8[i][1] for i in _d8], _l8),
      pairs([(str(i + 1), _l8[i]) for i in range(5)], ncols=5, width=COLW), mins=4, ref="7")

_m = [("April", 11, 30), ("May", 14, 31), ("June", 17, 30), ("July", 19, 31), ("August", 18, 31), ("September", 15, 30),
      ("October", 9, 31)]
_gdd = []
for (mo, t, d) in _m:
    v = (t - 10) * d
    _gdd.append(v)
_tot = sum(v for v in _gdd if v > 0)
rows = [[Paragraph("MONTH", WS["hdr"]), Paragraph("MEAN \u00b0C", WS["hdr"]), Paragraph("DAYS", WS["hdr"]),
         Paragraph("(MEAN \u2212 10) \u00d7 DAYS", WS["hdr"])]]
for (mo, t, d) in _m:
    rows.append([Paragraph(mo, WS["cellb"]), Paragraph(str(t), WS["cell"]), Paragraph(str(d), WS["cell"]), FillCell(150, h=17)])
rows.append([Paragraph("<b>GDD for the season</b>", WS["cellb"]), "", "", FillCell(150, h=17)])
tb = Table(rows, colWidths=[130, 70, 70, 200], hAlign="LEFT")
tb.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                        ("LINEABOVE", (0, 0), (-1, 0), LINE_BOLD, INK), ("LINEBELOW", (0, 0), (-1, 0), LINE_RULE, INK),
                        ("LINEBELOW", (0, 1), (-1, -2), 0.3, FEINT), ("LINEBELOW", (0, -1), (-1, -1), LINE_BOLD, INK)]))
ch.ex("CALCULATE", "Growing degree days", 8,
      "A northern-hemisphere vineyard (hypothetical monthly means). For each month: mean \u221210\u00b0C, times the days; then add the months, leaving out negative ones. "
      "<b>1 point per month, 1 for the total.</b>",
      tb,
      kp("Apr <b>%d</b> \u00b7 May <b>%d</b> \u00b7 Jun <b>%d</b> \u00b7 Jul <b>%d</b> \u00b7 Aug <b>%d</b> \u00b7 Sep <b>%d</b> \u00b7 "
         "Oct <b>%d</b> (negative: not counted). <b>GDD = %s.</b>" % (_gdd[0], _gdd[1], _gdd[2], _gdd[3], _gdd[4], _gdd[5], _gdd[6],
                                                                  format(_tot, ","))), mins=5, ref="7")

_s10 = ["Willamette Valley: 15.9\u00b0C (61\u00b0F)", "A region at 17.4\u00b0C", "A region at 19.6\u00b0C", "A region at 22.3\u00b0C"]
ch.ex("DECIDE", "Which WSET climate band?", 4,
      "Circle <b>C</b> cool (\u226416.5\u00b0C), <b>M</b> moderate, <b>W</b> warm or <b>H</b> hot (&gt;21\u00b0C) by average growing season temperature.",
      choose(_s10, ["C", "M", "W", "H"]),
      kp("<b>1</b> C \u00b7 <b>2</b> M \u00b7 <b>3</b> W \u00b7 <b>4</b> H"), mins=2, ref="7")
ch.page()

# ============================================================ PAGE 5
_tf = [("Vines need full sunshine to photosynthesize well.", False, "Light limits photosynthesis only below one third of full sunshine."),
       ("In the southern hemisphere a sun-facing slope faces north.", True, ""),
       ("Willamette and Margaux sit at about the same latitude, so share a climate band.", False,
        "They sit about two bands apart: the cold California current cools Willamette, the Gulf Stream warms Margaux."),
       ("Scientific backing links soil chemistry to particular wine aromas.", False,
        "Backing is lacking; the physical parameters (water, drainage, heat) are what is well recognized."),
       ("Rain at flowering and fruit set can cut yields or cause uneven ripening.", True, ""),
       ("Sunlight and UV are weaker at high altitude.", False, "They are more intense at altitude."),
       ("Vintage variation is unwanted in every wine style.", False,
        "It is welcomed in some styles, but unwanted in non-vintage sparkling and many high-volume, inexpensive wines.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 7,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="2\u20137")

ch.ex("FLOW", "Climate change in the glass", 3,
      "Complete the chain from warming to the wine in the glass \u2014 <b>the dotted boxes</b>.",
      VFlow(["Warmer temperatures", Blank("The vine cycle runs faster"),
             Blank("Sugar rises and acid falls fast; aroma and tannin ripening do not keep pace"),
             Blank("Growers pick at higher sugar to protect aroma, tannin and color"),
             "Higher alcohol, lower acidity, higher pH"], box_h=27, gap=14, width=400),
      kp("Cycle runs faster \u2192 sugar and acid change faster than aroma and tannin ripen \u2192 pick later at higher sugar "
         "\u2192 higher alcohol, lower acidity, higher pH."), mins=3, ref="9")
ch.page()

# ============================================================ PAGE 6
_mc = [("All other factors equal, grapes from lower latitudes tend to show:",
        ["Higher sugar and lower acidity", "Lower sugar and higher acidity", "More methoxypyrazines", "Less color in black grapes"]),
       ("A high diurnal range often helps warm climates because cool nights:",
        ["Speed up malic acid respiration", "Slow malic respiration and aid anthocyanin formation", "Stop photosynthesis",
         "Raise soil temperature"]),
       ("Jerez needs no irrigation despite dry summers because albariza soil:",
        ["Drains very fast", "Retains water and releases it slowly", "Reflects radiation", "Is rich in nitrogen"]),
       ("In the GDD calculation, a month whose mean is below 10\u00b0C is:",
        ["Counted as a negative", "Not counted", "Counted as zero degrees", "Counted double"]),
       ("Iron chlorosis is most likely in a soil that is:",
        ["Highly acidic", "High in pH (calcium carbonate)", "Rich in humus", "Free draining"])]
_amc = [0, 1, 1, 1, 1]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written, not multiple choice \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>A</b> \u2014 low latitude: more, stronger radiation"),
                ("2", "<b>B</b> \u2014 cool nights slow respiration"),
                ("3", "<b>B</b> \u2014 retains water, releases slowly"),
                ("4", "<b>B</b> \u2014 negative months are not counted"),
                ("5", "<b>B</b> \u2014 iron is unavailable at high pH")]), mins=4, ref="4\u20137")

_pts = ["Water heats and cools more slowly than land.",
        "By day, air over land heats and rises, drawing cool humid air in from over the water.",
        "By night the water holds its warmth while land cools fast, so the area stays warmer (smaller diurnal range).",
        "Across the year: cooler summers and milder winters."]
ch.ex("EXPLAIN", "Write like an examiner", 3,
      "Answer in three or four sentences, then self-mark. <b>Cause and effect earns marks</b>; a list does not.",
      explain("Explain how <b>proximity to a large body of water</b> moderates temperature in a wine region.", [], lines=4) +
      [Checklist(_pts)],
      kp("Any 3 of the 4 checklist points: slow heating and cooling of water \u00b7 cool humid afternoon breezes \u00b7 warm nights "
         "\u00b7 cooler summers and milder winters."), mins=5, ref="3")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch3.pdf")
