# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 20: Specific Options for No- and Low-Alcohol Winemaking."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("20", "No- and Low-Alcohol Winemaking",
             ["say why quality is set before dealcoholization",
              "match each removal method to its trade-off",
              "explain why 0.0% abv always loses volatile aroma",
              "recall the UK labeling thresholds",
              "list what a dealcoholized wine needs afterward"])

# ============================================================ PAGE 1
_p1 = [("Reverse osmosis", "The most common and economical for small adjustments; up to 1.5% abv per pass, so several passes; wastes water"),
       ("Vacuum distillation", "Boils alcohol off at about 48\u00b0C under vacuum; some lost aroma can be captured and blended back"),
       ("Spinning cone", "A thin film of wine: aroma is extracted first, then alcohol, then aroma is blended back; viable only at large volume")]
_d1 = [1, 2, 0]
_l1 = [chr(65 + _d1.index(i)) for i in range(3)]
ch.ex("MATCH", "Three ways to remove alcohol", 3, "Each method trades a different pair of things. Match each to its profile.",
      match([p[0] for p in _p1], [_p1[i][1] for i in _d1], _l1),
      pairs([(str(i + 1), _l1[i]) for i in range(3)], ncols=3, width=COLW), mins=3, ref="2")

_arts = [A2.DealcCone(150), A2.DealcRO(150), A2.DealcVacuum(150)]
ch.ex("NAME", "Name the technology", 4,
      "Name each drawing from the word bank, then answer the last question. <b>3 points for names, 1 for the last.</b>",
      [WordBank(["Reverse osmosis", "Spinning cone", "Vacuum distillation"], ncols=3), PanelFigure(_arts, gap=14),
       LineFill("The old heat-evaporation methods needed what temperature to boil off alcohol?", w=W, h=19)],
      kp("<b>1</b> Spinning cone \u00b7 <b>2</b> Reverse osmosis \u00b7 <b>3</b> Vacuum distillation. Old heat evaporation: <b>78\u00b0C</b>, which cooked the wine and lost aroma."),
      mins=4, ref="2")
ch.page()

# ============================================================ PAGE 2
_ub = [(0, 0.05, "#9CC3D9", "Up to 0.05%", "Alcohol free"), (0.05, 0.5, "#9CC987", "Up to 0.5%", "Non-alcoholic"), (0.5, 1.2, "#E8A44A", "Up to 1.2%", "Low alcohol")]
ch.ex("SCALE", "UK labeling thresholds", 3, "Name each band. Terms and limits vary by country; these are the UK\u2019s.",
      BandScale(0, 1.5, _ub, [0, 0.5, 1.2, 1.5], unit="%", box_h=44),
      kp("<b>\u22640.05%:</b> alcohol free \u00b7 <b>\u22640.5%:</b> non-alcoholic \u00b7 <b>\u22641.2%:</b> low alcohol. Below about 5.5% abv some countries no longer call it wine."),
      mins=2, ref="4")

_r4 = ["Body", "Astringency", "Perceived acidity", "Aroma intensity", "Microbial stability", "Phenolic concentration", "Shelf life"]
_a4 = ["Decreases", "Increases", "Increases", "Decreases", "Decreases", "Increases", "Decreases"]
ch.ex("TICK", "What dealcoholization does", 7, "Removing alcohol removes its contribution to texture and stability. Tick one for each.",
      tickgrid(_r4, ["Increases", "Decreases"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a4))), mins=3, ref="3")
ch.page()

# ============================================================ PAGE 3
_p5 = [("Sugar (usually RCGM)", "Mimics the lost mouthfeel and offsets heightened acidity and astringency"),
       ("Flavor enhancements", "Natural, grape-derived flavorings from specialist houses"),
       ("Tannin (powder or liquid)", "Restores texture if the wine was diluted before fermentation"),
       ("Glycerol", "Boosts body through its own viscous texture"),
       ("DMDC or pasteurization", "Restores microbial stability to a wine more open to contamination")]
_d5 = [2, 4, 0, 3, 1]
_l5 = [chr(65 + _d5.index(i)) for i in range(5)]
ch.ex("MATCH", "Post-dealcoholization adjustments", 5, "Match each adjustment to its job.",
      match([p[0] for p in _p5], [_p5[i][1] for i in _d5], _l5),
      pairs([(str(i + 1), _l5[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="4")

f, a = cloze(["Vacuum distillation boils alcohol off at about {{48\u00b0C}}; reverse osmosis removes up to {{1.5}}% abv per pass. Yield loss is "
              "{{15\u201330}}%. Shelf life: {{two}} years in glass, {{one}} year in cans. Below about {{5.5}}% abv many countries do not call it wine. "
              "UK low alcohol is {{1.2}}% or less, non-alcoholic {{0.5}}% or less, alcohol free {{0.05}}% or less. Heat evaporation needs the wine to reach {{78}}\u00b0C, hence cooked flavors."], width=72)
ch.ex("COMPLETE", "No- and low-alcohol numbers", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=4, ref="2\u20134")
ch.page()

# ============================================================ PAGE 4
_tf = [("Dealcoholization can rescue poor fruit.", False, "Quality is set before it begins; flawed wine goes in and comes out flawed, minus the alcohol."),
       ("At 0.0% abv the right method can preserve volatile aroma completely.", False,
        "Alcohol and the volatile compounds cannot be fully separated, so none can."),
       ("Diluting must with water is permitted in the EU.", False, "It is banned in the EU, though common in the US and Australia."),
       ("Removing alcohol can make underripe tannins more astringent.", True, ""),
       ("Reverse osmosis is the most common and most economical option for minor adjustments.", True, ""),
       ("A \u2018dealcoholized\u2019 label needs the wine to have started full-strength and gone through a real removal process.", True, ""),
       ("Yield loss of 15\u201330% is one reason dealcoholizing adds cost.", True, ""),
       ("Reverse osmosis is the most sustainable option.", False, "It wastes a lot of water: each pass removes up to 1.5% abv, so most adjustments need several passes.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 8,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20134")

ch.page()

# ============================================================ PAGE 5
_p13 = [("Cooler site", "Slows sugar accumulation, so lower potential alcohol"),
        ("Less leaf area", "Less photosynthesis, so less sugar"),
        ("Early harvest", "Less sugar, but unripe phenolics risk a poor balance, especially in reds"),
        ("Interrupted fermentation", "Cooling stops it early: lower alcohol, but residual sugar and a need to stabilize"),
        ("Non-Saccharomyces yeast", "Ferments less sugar into alcohol, alone or sequentially with S. cerevisiae"),
        ("Reverse osmosis on the must", "Removes sugar before fermentation; may also strip color and volatile aroma")]
_d13 = [4, 1, 5, 0, 3, 2]
_l13 = [chr(65 + _d13.index(i)) for i in range(6)]
_e = ["Volatile compounds such as terpenes and esters boil at temperatures similar to alcohol.",
      "They are often lost alongside it.",
      "At 0.0% abv alcohol and these compounds cannot be fully separated, so no method preserves them."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "The cause is physical, not a failing of one method.",
      explain("Explain why <b>0.0% abv wine always loses volatile aroma</b>, whichever method is used.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: volatiles boil near alcohol \u00b7 lost with it \u00b7 cannot be fully separated at 0.0%."), mins=4, ref="3")
ch.ex("MATCH", "Levers before the still", 6, "Lower alcohol starts in the vineyard and the fermenter. Match each lever to its effect.",
      match([p[0] for p in _p13], [_p13[i][1] for i in _d13], _l13),
      pairs([(str(i + 1), _l13[i]) for i in range(6)], ncols=6, width=COLW), mins=4, ref="1\u20132")
ch.page()

# ============================================================ PAGE 5
_mc = [("Which grapes suit no- and low-alcohol wine best?", ["High-sugar Grenache and Zinfandel", "Aromatic Sauvignon Blanc and Riesling", "Thick-skinned reds", "Neutral varieties"]),
       ("The most popular EU way to limit potential alcohol, besides early harvest, is:", ["Adding water", "Blending less-ripe with ripe fruit", "Adding sugar", "Chaptalization"]),
       ("Non-Saccharomyces yeast such as <i>Metschnikowia pulcherrima</i> is used to:", ["Raise alcohol", "Ferment less sugar to alcohol", "Remove SO2", "Add color"]),
       ("A dealcoholized wine is recommended to be drunk within:", ["Six months", "Two years in glass, one year canned", "Ten years", "Any time"]),
       ("Which preservative may restore stability?", ["Sorbic acid only", "DMDC (Velcorin)", "Sugar", "Tannin"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 aromatic Sauvignon Blanc, Riesling"), ("2", "<b>B</b> \u2014 blending less-ripe with ripe"), ("3", "<b>B</b> \u2014 ferments less sugar to alcohol"),
                ("4", "<b>B</b> \u2014 two years in glass, one canned"), ("5", "<b>B</b> \u2014 DMDC")]), mins=4, ref="1\u20134")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch20.pdf")
