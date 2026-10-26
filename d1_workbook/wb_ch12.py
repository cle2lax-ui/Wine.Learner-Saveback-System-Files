# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 12: Approaches to Winemaking."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("12", "Approaches to Winemaking",
             ["say what each approach allows, requires or bans",
              "see how the approaches nest by grape requirement",
              "name the country before answering on SO2",
              "treat \u2018natural\u2019 as undefined outside France",
              "avoid tying any approach to price or quality"])

# ============================================================ PAGE 1
_rings = [("Grapes: any", "Conventional"), ("Grapes: certified organic", "Organic"), ("Grapes: certified biodynamic", "Biodynamic")]
ch.ex("NAME", "What each approach asks of the grapes", 4,
      "Each ring asks more of the grapes than the one outside it. Write the approach on each dotted box. "
      "Then answer: which approach needs no certification at all? <b>3 points for rings, 1 for the last.</b>",
      [NestRings(_rings, key=False), LineFill("No certification needed (by choice, usually organic or biodynamic grapes):", w=W, h=19)],
      kp("<b>1</b> Conventional \u00b7 <b>2</b> Organic \u00b7 <b>3</b> Biodynamic. No certification needed: <b>Natural</b> (no widely agreed definition; "
         "France\u2019s Vin m\u00e9thode nature is the first national certification)."), mins=3, ref="intro")

_rc = [["SO2 in \u2018organic\u2019 wine", Blank("Regulated addition is allowed", 2), Blank("No addition; naturally occurring SO2 below 10 mg/L", 2)],
       ["US label \u2018wine made from organic grapes\u2019", "\u2014", Blank("Does permit added SO2", 2)]]
ch.ex("COMPARE", "Same word, different rules", 3, "Complete the dotted cells.",
      compare(["", "European Union", "United States"], _rc, [120, 199, 199]),
      kp("<b>EU:</b> regulated SO2 addition allowed. <b>USA:</b> no addition, under 10 mg/L natural. "
         "<b>US \u2018made from organic grapes\u2019:</b> added SO2 permitted."), mins=3, ref="2")
ch.page()

# ============================================================ PAGE 2
_r3 = ["Certifier: Ecocert, USDA or EU rules", "Certifier: Demeter, with a specification set per country",
       "No widely agreed definition: \u2018nothing added, nothing removed\u2019", "Builds on Pasteur\u2019s 1860s work on yeasts and bacteria",
       "Ambient-yeast fermentation and minimal or no SO2", "Bans raising alcohol by concentrating the whole must",
       "Excludes a short list, e.g. partial de-alcoholization", "Used for wine of all styles, quality levels and prices"]
_a3 = ["Organic", "Biodynamic", "Natural", "Conventional", "Natural", "Biodynamic", "Organic", "Conventional"]
ch.ex("TICK", "Which approach?", 8, "Tick the one approach each statement describes.",
      tickgrid(_r3, ["Conventional", "Organic", "Biodynamic", "Natural"], label_w=270),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a3))), mins=3, ref="1\u20134")

_e = ["The EU allows a regulated addition of SO2 in certified organic wine.",
      "The USA excludes added SO2, allowing only naturally occurring SO2 below 10 mg/L.",
      "A separate US category, \u2018wine made from organic grapes\u2019, does permit added SO2; so one word covers different products."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Name the country before the rule.",
      explain("Explain why <b>\u2018organic\u2019 on a wine label</b> can mean different things in the EU and the USA.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: EU regulated SO2 \u00b7 USA excludes added SO2 (under 10 mg/L natural) \u00b7 separate US \u2018organic grapes\u2019 category permits SO2."),
      mins=4, ref="2")
ch.page()

# ============================================================ PAGE 3
_tf = [("Organic wine is always additive-free.", False,
        "Organic rules allow many conventional additives: cultured yeast, yeast nutrients, added tannins."),
       ("Demeter\u2019s rules are identical worldwide.", False,
        "Demeter sets global principles; each country\u2019s certifier sets the specification (UK and USA differ on yeast)."),
       ("\u2018Natural wine\u2019 is a protected term.", False,
        "There is no widely agreed definition; France\u2019s Vin m\u00e9thode nature is the first national certification."),
       ("Conventional winemaking always means heavy manipulation.", False,
        "Techniques are options, not requirements; some premium producers choose not to filter."),
       ("Sterile filtering of residual-sugar wines is usually desirable.", True, ""),
       ("Organic wine is always more expensive than conventional.", False,
        "It sells at every price point; certification adds a small cost, and any premium depends on the market.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20134")
ch.page()

# ============================================================ PAGE 4
_mc = [("Pasteur\u2019s 1860s discovery that underpins modern winemaking was of:", ["Malolactic bacteria only", "Bacteria and yeasts",
                                                                                      "Sulfur dioxide", "Tannin polymerization"]),
       ("Which certifier issues an allowable list and excludes practices such as partial de-alcoholization?",
        ["Demeter", "Ecocert", "VinNatur", "Vin m\u00e9thode nature"]),
       ("On yeast, UK Demeter certification:", ["Bans all added yeast", "Encourages natural yeast but permits organic or commercial yeast if unavailable",
                                                  "Requires commercial yeast", "Is silent on yeast"]),
       ("France\u2019s first nationally recognized natural wine certification is:", ["VinNatur", "Ecocert", "Vin m\u00e9thode nature", "Demeter"]),
       ("Natural winemaking typically uses SO2:", ["At the legal maximum", "At an absolute minimum, often only at bottling, or none", "Only before fermentation",
                                                     "Freely, to fix faults"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 bacteria and yeasts"), ("2", "<b>B</b> \u2014 Ecocert"),
                ("3", "<b>B</b> \u2014 natural yeast encouraged, others permitted if unavailable"), ("4", "<b>C</b> \u2014 Vin m\u00e9thode nature"),
                ("5", "<b>B</b> \u2014 minimal, often only at bottling")]), mins=4, ref="1\u20134")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch12.pdf")
