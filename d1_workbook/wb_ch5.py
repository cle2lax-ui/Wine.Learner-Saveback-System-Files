# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 5: Vineyard Establishment."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("5", "Vineyard Establishment",
             ["frame every answer by irreversibility",
              "split site selection into natural and commercial halves",
              "handle terroir with its scientific caveat",
              "map rootstock parentage to property",
              "treat old vines as contested, not guaranteed"])

# ============================================================ PAGE 1
_r1 = ["Land price in a desirable GI", "Distance from the winery", "Aspect and altitude", "PDO rules on varieties and yields",
       "Whether the climate is warm or cool", "Source and cost of irrigation water", "Soil depth and drainage",
       "A steep slope that cannot be mechanized"]
_a1 = ["Logistical/legal/cost", "Logistical/legal/cost", "Natural", "Logistical/legal/cost", "Natural", "Logistical/legal/cost",
       "Natural", "Logistical/legal/cost"]
ch.ex("TICK", "Two halves of site selection", 8,
      "Natural factors decide whether the grapes <i>can</i> be grown; logistical, legal and cost factors decide whether they pay. Tick one half for each.",
      tickgrid(_r1, ["Natural", "Logistical, legal, cost"], label_w=330),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a.split("/")[0] if a == "Natural" else "LLC") for i, a in enumerate(_a1)) +
         ".  <i>LLC = logistical, legal and cost.</i>"), mins=3, ref="1")

_p2 = [("Warm \u00b7 inexpensive", "Flat, fertile, warm and dry: Central Valley of Chile; irrigation, mechanization"),
       ("Warm \u00b7 premium", "Seek cooler sites: altitude (L\u00fajan de Cuyo) or sea breezes (Casablanca)"),
       ("Cool \u00b7 inexpensive", "The hardest square: ripening risk plus low margin"),
       ("Cool \u00b7 premium", "Maximize ripening: aspects with most sunshine, as in the Rheingau")]
_d2 = [2, 0, 3, 1]
_l2 = [chr(65 + _d2.index(i)) for i in range(4)]
ch.ex("MATCH", "Price point against climate", 4, "Match each square of the grid to its strategy.",
      match([p[0] for p in _p2], [_p2[i][1] for i in _d2], _l2),
      pairs([(str(i + 1), _l2[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="1")
ch.page()

# ============================================================ PAGE 2
_p3 = [("Physical definition", "Characteristics relate to the place: climate, soil, aspect, elevation"),
       ("Cultural extension", "Also includes human interventions, such as planting density and trellising in French PDOs"),
       ("Geological claim", "Soil geology directly gives flavor; strongly contested by the scientific community"),
       ("Obscured by winemaking", "Over-ripe fruit and new oak can mask a site\u2019s inherent character")]
_d3 = [2, 0, 3, 1]
_l3 = [chr(65 + _d3.index(i)) for i in range(4)]
ch.ex("MATCH", "Four uses of \u2018terroir\u2019", 4, "Match each use of the word to its meaning and standing.",
      match([p[0] for p in _p3], [_p3[i][1] for i in _d3], _l3),
      pairs([(str(i + 1), _l3[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="1")

f, a = cloze(["The geological claim is contested because {{photosynthesis}} is the primary driver of vine growth, all {{aroma}} "
              "compounds are synthesized in the {{vine}}, and must is further transformed by {{fermentation}}."], width=76)
ch.ex("COMPLETE", "Why the geological claim is contested", len(a), "Three grounds. <b>1 point per blank.</b>", f, kp(ans_inline(a)),
      mins=2, ref="1")

_p5 = [("A plough pan", "Break it down: promotes drainage and easier later cultivation"),
       ("Roots of uprooted vines", "Remove and burn: they can harbor disease"),
       ("A serious weed problem", "Apply systemic herbicides before planting"),
       ("Acidic soil (Beaujolais)", "Spread lime and plough it in; surface lime acts slowly"),
       ("A steep slope (Douro)", "Build terraces to give flat land for planting"),
       ("Low nutrients and organic matter", "Manure, compost and fertilizers, ploughed in")]
_d5 = [4, 2, 0, 5, 1, 3]
_l5 = [chr(65 + _d5.index(i)) for i in range(6)]
ch.ex("MATCH", "Soil preparation: problem and fix", 6, "Rectifying now is easier than after planting. Match each problem to its fix.",
      match([p[0] for p in _p5], [_p5[i][1] for i in _d5], _l5),
      pairs([(str(i + 1), _l5[i]) for i in range(6)], ncols=6, width=COLW), mins=3, ref="2")
ch.page()

# ============================================================ PAGE 3
_p6 = [("Chardonnay", "Early budding (spring frost risk) and early ripening"),
       ("Riesling", "Late budding, and winter hardy"),
       ("Mourv\u00e8dre", "Late ripening: suits warm and hot climates"),
       ("Grenache", "Withstands high water stress: drought tolerant"),
       ("Cabernet Sauvignon", "Less susceptible to grey rot than Merlot"),
       ("Vidal", "Tolerates very cold winters (Ontario, Finger Lakes)")]
_d6 = [3, 5, 0, 2, 4, 1]
_l6 = [chr(65 + _d6.index(i)) for i in range(6)]
ch.ex("MATCH", "Variety and climatic adaptation", 6, "Match each variety to the trait that makes it suit a climate.",
      match([p[0] for p in _p6], [_p6[i][1] for i in _d6], _l6),
      pairs([(str(i + 1), _l6[i]) for i in range(6)], ncols=6, width=COLW), mins=3, ref="3")

_p7 = [("<i>V. champini</i> (Ramsey, Dog Ridge)", "Tolerates root-knot nematodes as well as phylloxera"),
       ("<i>V. rupestris</i> \u00d7 <i>V. berlandieri</i> (110R)", "Drought: roots deeply and quickly"),
       ("<i>V. riparia</i> (Riparia Gloire)", "Tolerates waterlogged soil and high rainfall"),
       ("<i>V. berlandieri</i> (41B)", "Tolerates high lime content (high pH)"),
       ("<i>V. riparia</i> (420A, 3309C)", "Low vigor: can advance ripening in cool climates"),
       ("<i>V. berlandieri</i> (1103P)", "Tolerates salinity (dissolved salt)")]
_d7 = [5, 2, 0, 4, 1, 3]
_l7 = [chr(65 + _d7.index(i)) for i in range(6)]
ch.ex("MATCH", "Rootstock parentage and property", 6, "Parentage explains the property. Match each rootstock to what it tolerates or does.",
      match([p[0] for p in _p7], [_p7[i][1] for i in _d7], _l7),
      pairs([(str(i + 1), _l7[i]) for i in range(6)], ncols=6, width=COLW), mins=4, ref="3")
ch.page()

# ============================================================ PAGE 4
_r8 = [["Low vigor", Blank("Riparia Gloire tolerates waterlogging; 420A, 3309C restrain vigor and can advance ripening", 3),
        "Risks stunting: drought tolerance matters more (110R, 140R)"],
       ["High vigor", "Rarely wanted: shading, poor ventilation, delayed ripening",
        Blank("Boosts growth and yields; also the sparkling-wine choice (high yields, delicate aromas, high acidity)", 3)]]
ch.ex("COMPARE", "Choosing a rootstock by vigor and site", 2, "Complete the dotted cells.",
      compare(["Rootstock", "Damp, fertile site", "Dry, unfertile site"], _r8, [88, 215, 215]),
      kp("<b>Low vigor, damp site:</b> Riparia Gloire; 420A, 3309C restrain vigor. <b>High vigor, dry site:</b> boosts growth and yields; "
         "the sparkling-wine choice."), mins=3, ref="3")

_r9 = [["Young", Blank("The weakest combination: neither age nor site is helping", 2),
        Blank("Can outperform an old vine on a poor site", 2)],
       ["Old", "Age and low yield do not compensate for a bad site",
        "The classic premium expectation, but site and management do much of the work"]]
ch.ex("COMPARE", "Age is not what decides quality", 2, "Four combinations of age and site. Complete the dotted cells.",
      compare(["Vine age", "Poor site or upkeep", "Well sited and managed"], _r9, [88, 215, 215]),
      kp("<b>Young, poor:</b> weakest combination. <b>Young, well sited:</b> can outperform an old vine on a poor site."), mins=3, ref="3")

_tb = [(0, 3, "#E8D9B0", "Years 0\u20133", "Inflorescences are commonly removed so the vine concentrates on growth"),
       (3, 6, "#F0D58A", "Up to about 5", "Low yields: the root system is not yet established"),
       (10, 40, "#9CC987", "About 10 to 40", "Maximum yields, depending on variety and conditions"),
       (40, 50, "#E8A44A", "Beyond 40", "Yield decreases as vigor decreases"),
       (50, 60, "#C8553D", "50 years or more", "Profitable in famous old vineyards at super-premium prices")]
ch.ex("SCALE", "A vine\u2019s working life", 5, "Write what happens in each dotted box.",
      BandScale(0, 60, _tb, [0, 10, 20, 30, 40, 50, 60], unit=" yrs", box_h=58),
      kp("<b>0\u20133:</b> inflorescences removed \u00b7 <b>to ~5:</b> low yields, roots not established \u00b7 <b>~10\u201340:</b> maximum yields \u00b7 "
         "<b>beyond 40:</b> yield falls with vigor \u00b7 <b>50+:</b> profitable in famous old vineyards, at super-premium prices."), mins=3, ref="3")
ch.page()

# ============================================================ PAGE 5
_tf = [("With head grafting, a new variety fruits later than a new planting.", False,
        "It fruits sooner, because the root system is already established."),
       ("\u2018Old vines\u2019 is a regulated term meaning at least 50 years.", False,
        "It is not regulated: 30 years to one producer, 100 to another."),
       ("Low-vigor rootstocks are always the quality choice.", False,
        "A high-vigor one may be chosen for sparkling wine, where high yields of delicate, acidic fruit beat concentration."),
       ("Terroir has a precise, agreed definition.", False, "No precise definition is agreed; it is often used undefined."),
       ("Lime spread on the surface of acidic soil takes a long time to act.", True, ""),
       ("Most vines are grafted, principally to protect against phylloxera.", True, "")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20133")

_e = ["These decisions are difficult to rectify once the vineyard is planted.",
      "Compromises through cost or time cause problems for the vineyard\u2019s whole life.",
      "Soil problems are far easier to fix before planting than after.",
      "Site, variety and rootstock lock in the style, quality and price of the wine."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Three or four sentences, then self-mark. <b>Frame it by irreversibility.</b>",
      explain("Explain why decisions made at <b>vineyard establishment</b> matter so much.", [], lines=3) + [Checklist(_e)],
      kp("Any 3 of 4: hard to rectify \u00b7 compromises last the vineyard\u2019s life \u00b7 soil easier to fix before planting \u00b7 "
         "locks in style, quality, price."), mins=4, ref="intro")
ch.page()

# ============================================================ PAGE 6
_sp = A2.SoilProfile(330)
f, a = cloze(["Breaking down a plough pan promotes {{drainage}} and easier later {{cultivation}}."], width=70)
ch.ex("LABEL", "Soil profile: the plough pan", 5 + len(a),
      "Label the five features. A plough pan is an impervious layer formed by years of ploughing at the same depth. <b>1 point per label and per blank.</b>",
      [LabelFigure(_sp, align="left")] + f,
      kp(label_key(_sp) + ".  " + ans_inline(a)), mins=4, ref="2")

_mc = [("The hardest square of the price-and-climate grid is:",
        ["Warm and inexpensive", "Warm and premium", "Cool and inexpensive", "Cool and premium"]),
       ("A plough pan is:",
        ["An impervious layer from ploughing at one depth", "A weed", "A rootstock", "A fungal disease"]),
       ("Chardonnay is:",
        ["Late budding and late ripening", "Early budding and early ripening", "Early budding and late ripening",
         "Late budding and early ripening"]),
       ("One ground on which the geological claim for terroir is contested:",
        ["Soils contain no minerals", "All aroma compounds are synthesized in the vine", "Fermentation does not change must",
         "Vines do not photosynthesize"]),
       ("A high-vigor rootstock for a dry, unfertile site making sparkling base wine:",
        ["420A", "Riparia Gloire", "<i>V. rupestris</i> (140R)", "41B"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>C</b> \u2014 ripening risk plus low margin"), ("2", "<b>A</b> \u2014 impervious layer"),
                ("3", "<b>B</b> \u2014 early budding and early ripening"), ("4", "<b>B</b> \u2014 aroma compounds are made in the vine"),
                ("5", "<b>C</b> \u2014 high vigor rootstock (<i>V. rupestris</i>)")]), mins=4, ref="1\u20133")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch5.pdf")
