# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 17: Specific Options for Producing Wines with Residual Sugar."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("17", "Wines with Residual Sugar",
             ["name the route a wine used from its style, price and example",
              "say why concentration raises quality and price together",
              "keep noble rot, gray rot and cryoextraction apart",
              "state the legal limits on Icewine and on sweetening",
              "weigh control against complexity when stopping fermentation"])

# ============================================================ PAGE 1
_r1 = ["Sauternes", "Eiswein", "Recioto della Valpolicella", "Vin Santo", "Vendanges Tardives (Alsace)", "Juran\u00e7on (cane-cut)",
       "Trockenbeerenauslese", "Canadian Icewine"]
_a1 = ["Noble rot", "Frozen", "Dried off the vine", "Dried off the vine", "Dried on the vine", "Dried on the vine", "Noble rot", "Frozen"]
ch.ex("TICK", "Which way was the must concentrated?", 8, "Tick the method that made each wine.",
      tickgrid(_r1, ["Dried on vine", "Dried off vine", "Noble rot", "Frozen"], label_w=270),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a1))), mins=4, ref="1")

_rc = [["Control over final RS", "Low: nature and climate decide", Blank("High: halt whenever measured", 2), Blank("Highest: measured and trialled", 2)],
       ["Quality ceiling", "Very good to outstanding", Blank("Rarely outstanding", 1), Blank("Acceptable to good", 1)],
       ["Typical price", "Premium, super-premium", Blank("Inexpensive, mid-priced", 2), Blank("Inexpensive, high volume", 2)]]
ch.ex("COMPARE", "Three routes to residual sugar", 6, "Complete the dotted cells for the other two routes.",
      compare(["", "Concentrating the must", "Stopping fermentation", "Blending in sweetness"], _rc, [96, 140, 141, 141]),
      kp("<b>Stopping:</b> high control \u00b7 rarely outstanding \u00b7 inexpensive, mid-priced. <b>Blending:</b> highest control \u00b7 acceptable to good \u00b7 "
         "inexpensive, high volume."), mins=3, ref="intro")
ch.page()

# ============================================================ PAGE 2
_arts = [A2.ConcNobleRot(120), A2.ConcFrozen(120), A2.ConcOnVine(120), A2.ConcOffVine(120)]
ch.ex("NAME", "Name the method", 5,
      "Name each drawing from the word bank, then answer the last question. <b>4 points for names, 1 for the last.</b>",
      [WordBank(["Drying off the vine", "Drying on the vine", "Freezing", "Noble rot"], ncols=4), PanelFigure(_arts, gap=10),
       LineFill("The Italian word for drying picked grapes (Recioto, Vin Santo):", w=W, h=19)],
      kp("<b>1</b> Noble rot \u00b7 <b>2</b> Freezing \u00b7 <b>3</b> Drying on the vine \u00b7 <b>4</b> Drying off the vine. The Italian word: <b>appassimento</b>."),
      mins=4, ref="1")

_ch = [("Noble rot", ["Fully ripe grapes, humid mornings", Blank("Botrytis punctures the skins"), Blank("Dry afternoons evaporate the water"),
                       "Sugar, acid and flavor concentrate"]),
       ("Freezing", ["Winter-hardy vines (Riesling, Vidal) left on the vine", Blank("Water freezes in the berry, at \u22128\u00b0C or below"),
                     Blank("Pressed while frozen: the ice stays behind"), "A concentrated juice"])]
ch.ex("CHAIN", "Noble rot and freezing", 4, "Complete each chain with the missing links.",
      [Chain(items, label=lab, box_h=46) for lab, items in _ch],
      kp("<b>1</b> Botrytis punctures skins \u2192 dry afternoons evaporate water. <b>2</b> water freezes at \u22128\u00b0C or below \u2192 pressed frozen, ice stays behind."),
      mins=3, ref="1")
ch.page()

# ============================================================ PAGE 3
_r3 = ["Water loss concentrates acid and flavor with the sugar", "Precise control of final RS, with nothing else concentrated",
       "Dry wine is stored and sweetness is added at bottling", "Premium and super-premium prices", "Quality ceiling: acceptable to good",
       "Chilling below 10\u00b0C and/or high SO2, then sterile filtering", "S\u00fcssreserve or RCGM may be used", "White Zinfandel (about 35 g/L RS)"]
_a3 = ["Concentrating", "Stopping", "Blending", "Concentrating", "Blending", "Stopping", "Blending", "Stopping"]
ch.ex("TICK", "Which route?", 8, "Tick the route each statement describes.",
      tickgrid(_r3, ["Concentrating", "Stopping", "Blending"], label_w=330),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a3))), mins=4, ref="1\u20133")

f, a = cloze(["Canadian Icewine needs harvest at {{\u22128\u00b0C}} or below. Noble rot needs humid {{mornings}} and dry {{afternoons}}; its enzyme "
              "{{laccase}} oxidizes the must and resists {{SO2}}. Stopping fermentation usually chills below {{10\u00b0C}}; White Zinfandel has about "
              "{{35}} g/L RS and about {{10}}% abv. Sweeteners include sugar (banned in the EU), {{RCGM}} and {{S\u00fcssreserve}}."], width=70)
ch.ex("COMPLETE", "Residual-sugar numbers and terms", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=4, ref="1\u20133")
ch.page()

# ============================================================ PAGE 4
_tf = [("Cryoextraction wines may be labeled Icewine.", False,
        "Icewine and Eiswein are protected: grapes must freeze naturally on the vine. Cryoextraction is winery-based."),
       ("Noble rot and gray rot are caused by different fungi.", False,
        "Same fungus (<i>Botrytis cinerea</i>); the conditions decide, and wrong ones give gray rot."),
       ("Sugar may be used to sweeten EU wines at bottling.", False, "The EU bans sugar for this use."),
       ("Concentration methods are costly chiefly because of low juice yield.", True, ""),
       ("Stopping fermentation earlier leaves less residual sugar.", False, "An earlier halt leaves more sugar and less alcohol."),
       ("Noble rot is mostly used on black grapes.", False, "It is rarely used on black grapes.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20133")

_e = ["Removing water concentrates sugar, acid and flavor together, so the balance holds.",
      "Low juice yield, from water loss, is the shared cost driver.",
      "Difficult pressing and extra labor (often several hand-pickings) add cost.",
      "So these wines reach premium and super-premium prices."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Concentration is not just \u2018sweeter\u2019.",
      explain("Explain why <b>concentration methods</b> tend to give outstanding quality and premium prices together.", [], lines=3) + [Checklist(_e)],
      kp("Any 3 of 4: sugar, acid and flavor concentrate together \u00b7 low yield \u00b7 difficult pressing and labor \u00b7 premium prices."), mins=4, ref="1")
ch.page()

# ============================================================ PAGE 5
_mc = [("Appassimento is:", ["Freezing grapes on the vine", "Drying picked grapes, in the sun or a humidity-controlled room",
                              "Stopping fermentation with SO2", "Fortifying with spirit"]),
       ("Which sweetener adds grape-juice character?", ["Beet sugar", "RCGM", "S\u00fcssreserve", "Honey"]),
       ("Icewine and cryoextraction are:", ["Different physics, same status", "The same physics, different legal status",
                                            "Both protected terms", "Both banned in Canada"]),
       ("Cane-cutting is used to:", ["Raise acidity", "Shorten hang time for high sugar without extra-ripe flavors", "Stop fermentation", "Prevent noble rot"]),
       ("Sweetening rules for PDO wines can require the juice to:", ["Be imported", "Come from the same region", "Be frozen", "Be botrytized"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 drying picked grapes"), ("2", "<b>C</b> \u2014 S\u00fcssreserve"), ("3", "<b>B</b> \u2014 same physics, different status"),
                ("4", "<b>B</b> \u2014 shorter hang time, high sugar"), ("5", "<b>B</b> \u2014 same region")]), mins=4, ref="1\u20133")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch17.pdf")
