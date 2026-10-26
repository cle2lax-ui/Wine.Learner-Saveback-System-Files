# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 14: Maturation."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("14", "Maturation",
             ["state why small vessels age wine faster",
              "tell American from European oak by name",
              "know what a barrel has left by its fourth fill",
              "name all seven reasons to blend",
              "weigh lees as both a tool and a risk"])

# ============================================================ PAGE 1
_r1 = ["Impermeable vessels, SO2 and inert gas", "Barrel maturation, ullage and micro-oxygenation", "New Zealand Sauvignon Blanc, Veneto Pinot Grigio",
       "Oloroso Sherry, at the extreme", "Bottled soon after fermentation to keep primary aroma", "Primary aroma deliberately fades into tertiary character"]
_a1 = ["Protective", "Oxidative", "Protective", "Oxidative", "Protective", "Oxidative"]
ch.ex("TICK", "The fork after fermentation", 6, "Neither route is better; the style decides. Tick one for each.",
      tickgrid(_r1, ["Protective (reductive)", "Oxidative"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a1))), mins=3, ref="intro, 1")

_mb = [(6, 12, "#F0E2A0", "White wine", "6\u201312 months, stored at 8\u201312\u00b0C"),
       (12, 24, "#B04A5E", "Red wine", "12\u201324 months, stored at 12\u201316\u00b0C")]
ch.ex("SCALE", "Typical maturation", 4, "Write the typical length and storage temperature in each dotted box. <b>2 points each.</b>",
      BandScale(0, 24, _mb, [0, 6, 12, 18, 24], unit=" mo", box_h=48),
      kp("<b>White:</b> 6\u201312 months at 8\u201312\u00b0C \u00b7 <b>Red:</b> 12\u201324 months at 12\u201316\u00b0C. Whites are stored cooler and for less time: "
         "fewer anti-oxidative phenolics."), mins=2, ref="1")
ch.page()

# ============================================================ PAGE 2
_bar = A2.Barrel(330)
ch.ex("LABEL", "Anatomy of a barrel", 5,
      "Label the four parts. Then finish the sentence. <b>1 point per label, 1 for the sentence.</b>",
      [LabelFigure(_bar, align="center"),
       LineFill("Small vessels age wine faster because of their higher", w=W, h=19)],
      kp(label_key(_bar) + ".  <b>Surface-area-to-volume ratio</b> (not different wood)."), mins=4, ref="1\u20132")

_fb = [("1st fill (new)", 1.0, "100%"), ("2nd fill", 0.5, "about 50%"), ("4th fill and later", 0.08, "very little")]
ch.ex("CHART", "What a barrel has left to give", 3, "Write how much new-oak character remains in each bar. <b>1 point each.</b>",
      FillBars(_fb, width=330, height=122),
      kp("<b>100%</b> \u00b7 <b>about 50%</b> (half gone after one year) \u00b7 <b>very little</b>. Flavor fades, but a 4th-fill barrel admits oxygen as before."),
      mins=2, ref="2")
ch.page()

# ============================================================ PAGE 3
_rc = [["Key aroma", "Vanillin, shared with American oak", Blank("Vanillin plus higher lactones (coconut)", 2)],
       ["Character", "Subtler; more tannin", Blank("Greater intensity", 2)],
       ["Working the wood", "Must be split", Blank("Can be sawn: more vessels per tree", 2)],
       ["Growth and cost", "Slower growing; \u20ac600\u20131,200 a barrel", Blank("Faster growing; \u20ac300\u2013600 a barrel", 2)]]
ch.ex("COMPARE", "European or American oak?", 4, "Complete the American column. These are named, specific differences, not \u2018American is stronger\u2019.",
      compare(["", "European (French, Hungarian)", "American"], _rc, [88, 215, 215]),
      kp("<b>American:</b> vanillin plus higher lactones (coconut) \u00b7 greater intensity \u00b7 can be sawn \u00b7 faster growing, cheaper."),
      mins=3, ref="2")

_p6 = [("Light toast", "Subtlest spice and roasted-nut character"), ("Heavy toast", "Pronounced char and smoke"),
       ("Gross lees", "Settle within 24 hours; removed at the first racking"),
       ("Autolysis", "Dying yeast breaks down: body, texture, yogurt, dough and biscuit notes"),
       ("B\u00e2tonnage", "Stirring the lees; adds labor"), ("Micro-oxygenation", "Metered oxygen bubbled through a steel tank")]
_d6 = [3, 0, 5, 1, 4, 2]
_l6 = [chr(65 + _d6.index(i)) for i in range(6)]
ch.ex("MATCH", "Toast, lees and oxygen", 6, "Match each term to its meaning.",
      match([p[0] for p in _p6], [_p6[i][1] for i in _d6], _l6),
      pairs([(str(i + 1), _l6[i]) for i in range(6)], ncols=6, width=COLW), mins=3, ref="1\u20133")
ch.page()

# ============================================================ PAGE 4
_p7 = [("Balance", "Merlot softening under-ripe Cabernet Sauvignon"), ("Consistency", "Matching a house style across vintages (Sherry, NV sparkling)"),
       ("Style", "Red plus white to reach a precise ros\u00e9 color"), ("Complexity", "More parcels give a wider range of flavors"),
       ("Minimize faults", "Diluting a faulty batch into a larger sound volume"), ("Volume", "Reaching a viable, sellable volume from small holdings"),
       ("Price", "Blending in a cheaper variety (e.g. Trebbiano) to hit a price point")]
_d7 = [4, 0, 6, 2, 5, 1, 3]
_l7 = [chr(65 + _d7.index(i)) for i in range(7)]
ch.ex("MATCH", "Seven reasons to blend", 7, "Balance is only one. Match each named reason to its example.",
      match([p[0] for p in _p7], [_p7[i][1] for i in _d7], _l7),
      pairs([(str(i + 1), _l7[i]) for i in range(7)], ncols=7, width=COLW), mins=4, ref="4")

_tf = [("Larger wooden vessels age wine faster than small ones.", False,
        "Small vessels do: a higher surface-area-to-volume ratio, not a different wood."),
       ("Red wines tolerate more oxygen than whites, thanks to more anti-oxidative phenolics.", True, ""),
       ("A fourth-fill barrel gives almost no flavor but the same oxygen.", True, ""),
       ("Blending only fixes problems.", False, "Only one of the seven reasons (minimizing faults) is about fixing anything."),
       ("Lees contact is always beneficial.", False,
        "Too thick a layer, especially gross lees, can tip reductive sulfur compounds from struck match into rotten egg."),
       ("Micro-oxygenation raises the risk of spoilage organisms.", True, "")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20134")
ch.page()

# ============================================================ PAGE 5
_e = ["A small barrel has a higher surface-area-to-volume ratio, so more oxygen reaches the wine through staves and bung.",
      "The same ratio means more evaporative loss, so more topping up, and each topping-up is another oxygen exposure.",
      "More of the wood\u2019s tannins and aroma compounds reach each liter of wine."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "The answer is a ratio, not the age or thickness of the wood.",
      explain("Explain why a <b>small barrel matures wine faster</b> than a large tank or vat.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: higher surface-area-to-volume \u00b7 more evaporation and topping up \u00b7 more wood extraction per liter."), mins=4, ref="1\u20132")

_r11 = ["Much cheaper than a barrel", "Large surface area, so a quick effect", "Staves fixed inside a tank, or left floating",
        "Chips placed in a permeable sack", "Often paired with micro-oxygenation to integrate the oak", "Gentle oxidation through the wood itself"]
_a11 = ["Alternatives", "Alternatives", "Alternatives", "Alternatives", "Alternatives", "Barrel"]
ch.ex("TICK", "Barrel or oak alternative?", 6, "Inexpensive and mid-priced wines often use alternatives to get oak flavor. Tick one for each.",
      tickgrid(_r11, ["Oak barrel", "Oak alternatives"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a11)) + ".  Effects vary with species, size, toast and micro-oxygenation."), mins=3, ref="2")
ch.page()

_mc = [("American oak differs from European oak in having:", ["Higher lactones (coconut)", "Tighter grain", "Less intensity", "Higher cost"]),
       ("Oak staves are seasoned outdoors for 2\u20133 years to:", ["Raise bitterness", "Lower bitterness and raise some aromatics such as clove",
                                                                   "Remove all tannin", "Add toast"]),
       ("Autolysis in white wine tends to add:", ["Coconut", "Yogurt, dough and biscuit notes", "Green pepper", "Vanilla"]),
       ("Which reason to blend does Sherry or NV sparkling illustrate?", ["Price", "Volume", "Consistency", "Minimizing faults"]),
       ("Cool temperature and humidity above about 70% in a cellar:", ["Speed oxidation", "Slow loss and oxidation", "Raise ullage", "Kill lees"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>A</b> \u2014 higher lactones"), ("2", "<b>B</b> \u2014 lowers bitterness, raises clove"), ("3", "<b>B</b> \u2014 yogurt, dough, biscuit"),
                ("4", "<b>C</b> \u2014 consistency"), ("5", "<b>B</b> \u2014 slow loss and oxidation")]), mins=4, ref="1\u20134")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch14.pdf")
