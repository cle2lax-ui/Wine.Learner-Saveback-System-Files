# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 9: Harvest."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("9", "Harvest",
             ["name what growers measure, and why tasting still matters",
              "argue machine versus hand from advantages and costs",
              "separate hand-harvest required from merely preferred",
              "state the night-picking benefit as fruit temperature",
              "recall the key figures"])

# ============================================================ PAGE 1
f, a = cloze([
    "The old rule: grapes ripen about {{100}} days after flowering begins.",
    "Potential alcohol minimums: Petit Chablis {{9.5}}%, Chablis {{10}}%, Bourgogne Blanc {{10.5}}%.",
    "Most dry still wine is picked at {{19\u201325}}\u00b0 Brix, roughly {{11\u201315}}% abv.",
    "Night picking can deliver fruit up to {{15\u00b0C}} cooler; machines cost about {{one-third}} of hand harvesting.",
    "Canadian Icewine needs harvest below {{\u22128\u00b0C}}; hand-harvest crates hold at most {{10\u201315 kg}}.",
], width=58)
ch.ex("RECALL", "Numbers that matter", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=3, ref="1\u20132")

_p2 = [("Handheld refractometer", "Sugar, in \u00b0Brix"),
       ("Titration", "Acid level, by adding a known-reacting substance in measured amounts"),
       ("pH meter", "pH directly"),
       ("Tasting the grapes", "Aroma and tannin ripeness; no routine instrument replaces it"),
       ("Near-infrared spectroscopy", "Several readings (sugar, acidity and more) at once; still emerging")]
_d2 = [3, 0, 4, 1, 2]
_l2 = [chr(65 + _d2.index(i)) for i in range(5)]
ch.ex("MATCH", "What growers measure", 5, "Match each method to what it tells the grower.",
      match([p[0] for p in _p2], [_p2[i][1] for i in _d2], _l2),
      pairs([(str(i + 1), _l2[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="1")
ch.page()

# ============================================================ PAGE 2
_r3 = ["About one-third the cost at scale", "Can pick at night, up to 15\u00b0C cooler", "Bunch-by-bunch selectivity",
       "Handles steep slopes and irregular rows", "Less gentle: skins can rupture and release juice",
       "Small crates (10\u201315 kg) avoid crushing", "Needs a trained, supervised workforce", "Not cost-effective for small vineyards"]
_a3 = ["Machine", "Machine", "Hand", "Hand", "Machine", "Hand", "Hand", "Machine"]
ch.ex("TICK", "Machine or hand?", 8, "Tick the method each statement describes.",
      tickgrid(_r3, ["Machine", "Hand"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a3))), mins=3, ref="2")

_s4 = ["Premium sparkling wine needing whole-bunch pressing (Champagne)", "A premium red on a flat, trellised site, picked by hand for extra selection",
       "Botrytis-affected bunches for Trockenbeerenauslese", "Carbonic maceration (Beaujolais)", "Bush vines", "Steep sites such as the Douro",
       "A premium white where machines could reach but selection is wanted"]
ch.ex("DECIDE", "Required or merely preferred?", 7,
      "Circle <b>R</b> if hand-harvesting is <i>required</i>, or <b>P</b> if it is only <i>preferred</i>.",
      choose(_s4, ["R", "P"]),
      kp("<b>1</b> R \u00b7 <b>2</b> P \u00b7 <b>3</b> R \u00b7 <b>4</b> R \u00b7 <b>5</b> R \u00b7 <b>6</b> R \u00b7 <b>7</b> P. Whole-bunch styles, selective picking, "
         "steep sites and bush vines require it."), mins=3, ref="2")
ch.page()

# ============================================================ PAGE 3
_ch = [("Rain near harvest", ["Rain forecast near harvest", Blank("Grapes swell fast: juice dilutes, skins split"),
                               Blank("Gray rot sets in; the crop may be lost"), "Pick underripe now, or wait and risk it"])]
ch.ex("CHAIN", "The trump card", 2, "Rain is the one factor that can override a ripeness plan. Complete the dotted boxes.",
      [Chain(items, label=lab, box_h=46) for lab, items in _ch],
      kp("Grapes swell, juice dilutes and skins split \u2192 gray rot and possible loss of the crop."), mins=2, ref="1")

_p6 = [("White Zinfandel", "Early to mid August"), ("Red Zinfandel", "September"),
       ("Botrytised wines", "Hand-harvested over several passes to select only affected bunches"),
       ("Icewine / Eiswein", "Needs a specific cold threshold: below \u22128\u00b0C for Canadian Icewine"),
       ("Residual-sugar wines", "Often harvested late, to concentrate sugar")]
_d6 = [4, 0, 2, 1, 3]
_l6 = [chr(65 + _d6.index(i)) for i in range(5)]
ch.ex("MATCH", "Harvest date by wine style", 5, "Match each style to its harvest practice.",
      match([p[0] for p in _p6], [_p6[i][1] for i in _d6], _l6),
      pairs([(str(i + 1), _l6[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="1")
ch.page()

# ============================================================ PAGE 4
_tf = [("Instruments have replaced tasting the grapes.", False, "Tasting remains among the most important methods."),
       ("Machine harvesting is inherently lower quality.", False,
        "Bow-rod shakers, optical sorting, in-machine SO2 dosing and winery sorting have closed much of the gap."),
       ("Rain is the one factor that can override a ripeness plan.", True, ""),
       ("Potential alcohol minimums are the same for every AOC.", False, "Petit Chablis 9.5%, Chablis 10%, Bourgogne Blanc 10.5%."),
       ("Night harvesting is mainly for the pickers\u2019 comfort.", False,
        "The benefit is fruit temperature: up to 15\u00b0C cooler, less spoilage and oxidation, fresher aromatics."),
       ("\u2018Hand-picked\u2019 on a label guarantees quality.", False,
        "It is a marketing signal; the real decision weighs style, logistics, legislation and cost.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20132")

_e = ["The fruit arrives up to 15\u00b0C cooler.", "Less microbial spoilage and less oxidation.",
      "Fresher aromatics in fruity white wines.", "Lower refrigeration cost, with flexible timing."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "State the benefit as <b>fruit temperature</b>, not worker comfort.",
      explain("Explain why <b>night-time machine harvesting</b> can improve wine quality.", [], lines=3) + [Checklist(_e)],
      kp("Any 3 of 4: up to 15\u00b0C cooler fruit \u00b7 less spoilage and oxidation \u00b7 fresher aromatics \u00b7 lower refrigeration cost."),
      mins=4, ref="2")
ch.page()

# ============================================================ PAGE 5
_mc = [("Most dry still wine is picked at about:", ["12\u201315\u00b0 Brix", "19\u201325\u00b0 Brix", "30\u201335\u00b0 Brix", "8\u201310\u00b0 Brix"]),
       ("Which instrument gives pH directly?", ["Refractometer", "Titration", "pH meter", "Hydrometer"]),
       ("Which of these requires hand harvesting?",
        ["Inexpensive trellised white", "Carbonic maceration", "Any wine at a premium price", "Still Chardonnay on flat land"]),
       ("A benefit of in-machine SO2 dosing is that it:",
        ["Protects white grapes from oxidation", "Raises sugar", "Removes MOG", "Replaces tasting"]),
       ("Critics link extended hang time to:",
        ["High alcohol, low acid, extra-ripe wines lacking balance", "Thin skins", "Low pH", "Green flavors"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 19\u201325\u00b0 Brix"), ("2", "<b>C</b> \u2014 pH meter"), ("3", "<b>B</b> \u2014 carbonic maceration"),
                ("4", "<b>A</b> \u2014 protects whites from oxidation"), ("5", "<b>A</b> \u2014 high alcohol, low acid")]), mins=4, ref="1\u20132")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch9.pdf")
