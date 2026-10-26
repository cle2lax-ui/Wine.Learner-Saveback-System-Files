# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 21: Examples of Winemaking Choices for Different Styles of Wine."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("21", "Winemaking Choices by Style",
             ["fit each choice to one of four styles, and give the reason",
              "see one aim cascading into every later decision",
              "spot the same technique serving opposite goals",
              "name what premium white and premium red share",
              "never answer with the choice alone"])

# ============================================================ PAGE 1
_rc = [["Inexpensive", Blank("Aromatic variety; machine harvest, no skin contact, cool steel, avoid MLF and oak, screwcap. Volume and speed.", 3),
        Blank("Machine harvest, limited sorting, heat or carbonic extraction, MLF during fermentation, minimal maceration. Volume and speed.", 3)],
       ["Premium", Blank("Neutral variety; hand harvest, heavy sorting, gentle pressing, barrel and lees options, partial MLF for blending.", 3),
        Blank("Hand harvest, heavy sorting, warm extended maceration, small oak barrels, minimal-intervention finishing.", 3)]]
ch.ex("COMPARE", "Four styles, two axes", 4, "Summarize each style in the dotted cell. <b>1 point per cell with at least two correct choices and the aim.</b>",
      compare(["", "White", "Red"], _rc, [78, 220, 220]),
      kp("<b>Inexpensive white:</b> aromatic, machine harvest, no skin contact, cool steel, no MLF or oak, screwcap. <b>Inexpensive red:</b> machine harvest, light sorting, "
         "heat or carbonic, MLF during fermentation. <b>Premium white:</b> neutral, hand harvest, heavy sorting, gentle press, barrel and lees, partial MLF. "
         "<b>Premium red:</b> hand harvest, heavy sorting, warm extended maceration, small oak, minimal finishing."), mins=5, ref="intro")

ch.ex("FLOW", "One decision cascades", 3, "Complete the dotted boxes: one call drives all the rest.",
      VFlow(["Set the aim: volume and price, or quality and complexity?", Blank("Harvest and extraction: machine or hand; how gently to extract"),
             Blank("Fermentation and MLF: vessel, yeast, temperature, MLF timing"),
             Blank("Maturation and finishing: oak or none; intervention before bottling"), "Closure and packaging"], box_h=27, gap=14, width=440),
      kp("Aim \u2192 harvest and extraction \u2192 fermentation and MLF \u2192 maturation and finishing \u2192 closure. Everything follows from the first call."),
      mins=3, ref="intro")
ch.page()

# ============================================================ PAGE 2
_arts = [A2.HarvestHand(150), A2.HarvestMachine(150)]
ch.ex("NAME", "Name the harvest, and give the reason", 3,
      "Write <b>machine</b> or <b>hand</b> under each drawing, then give the reason that fits the inexpensive styles. <b>1 point each for the two names, 1 for the reason.</b>",
      [PanelFigure(_arts, gap=60), LineFill("Machine harvest suits the inexpensive styles because it is:", w=W, h=19)],
      kp("<b>1</b> Hand (small crates; premium) \u00b7 <b>2</b> Machine. Reason: <b>cheaper for large vineyards, keeping the price low</b>, trading a little quality risk for big cost savings."),
      mins=3, ref="1")

_r4 = ["Machine harvest; sorting for MOG only; no skin contact", "Hand harvest in small crates; heavy sorting; whole-bunch press option",
       "Machine harvest; carbonic or heat extraction", "Hand harvest; heavy sorting; cold soak or whole-bunch option"]
_a4 = ["Inexpensive white", "Premium white", "Inexpensive red", "Premium red"]
ch.ex("TICK", "Harvest and extraction", 4, "Tick the one style each row describes.",
      tickgrid(_r4, ["Inexp. white", "Prem. white", "Inexp. red", "Prem. red"], label_w=270),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a4))), mins=3, ref="1")
ch.page()

# ============================================================ PAGE 3
_r5 = ["Cool steel fermentation", "Barrel or egg, neutral or warm, with ambient or cultured yeast", "Mechanized or rotary cap management",
       "A hand-chosen mix of cap-management techniques", "MLF avoided", "Partial MLF, for blending options", "MLF during fermentation, for throughput"]
_a5 = ["Inexpensive white", "Premium white", "Inexpensive red", "Premium red", "Inexpensive white", "Premium white", "Inexpensive red"]
ch.ex("TICK", "Fermentation, vessel and MLF", 7, "Tick the one style each row describes.",
      tickgrid(_r5, ["Inexp. white", "Prem. white", "Inexp. red", "Prem. red"], label_w=270),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a5))), mins=4, ref="2")

_s7 = ["MLF during fermentation, to speed up throughput", "Partial MLF in white, to create blending options", "Rotary fermenters and mechanized pump-overs",
       "A hand-chosen mix of cap-management techniques", "Extended post-fermentation maceration", "Machine harvest with light sorting",
       "Blending lots and barrels for complexity and balance", "Blending for volume and consistency"]
ch.ex("DECIDE", "The same technique, opposite goals", 8, "Circle <b>V</b> if the aim is volume and price, or <b>Q</b> if quality and complexity.",
      choose(_s7, ["V", "Q"]),
      kp("<b>1</b> V \u00b7 <b>2</b> Q \u00b7 <b>3</b> V \u00b7 <b>4</b> Q \u00b7 <b>5</b> Q \u00b7 <b>6</b> V \u00b7 <b>7</b> Q \u00b7 <b>8</b> V. Automation tracks volume, not quality."), mins=4, ref="2")
ch.page()

# ============================================================ PAGE 4
_r6 = ["No maturation, or steel only", "Oak plus stirred lees, or none", "Oak alternatives in place of barrels", "Small oak and extended post-fermentation maceration"]
_a6 = ["Inexpensive white", "Premium white", "Inexpensive red", "Premium red"]
ch.ex("TICK", "Maturation", 4, "Tick the one style each row describes.",
      tickgrid(_r6, ["Inexp. white", "Prem. white", "Inexp. red", "Prem. red"], label_w=270),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a6))), mins=2, ref="3")

_tf = [("Heat extraction appears in premium red.", False, "Carbonic and heat extraction are inexpensive-red choices; premium red uses cold soak or whole-bunch options."),
       ("Premium white and premium red share hand harvest, heavy sorting and minimal-intervention finishing.", True, ""),
       ("A technique is inherently either a quality choice or a budget choice.", False, "Most serve either goal depending on context: MLF timing, blending and mechanization appear in both."),
       ("Extended post-fermentation maceration is skipped in inexpensive red to save tank space.", True, ""),
       ("Inexpensive red is just premium red done cheaply.", False, "It is a different set of choices for a different aim entirely."),
       ("Naming the correct choice alone earns full marks.", False, "D1 marking rewards the reason and its influence, not just the choice.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20133")
ch.page()

# ============================================================ PAGE 5
_p14 = [("Night or early transport", "Cool grapes resist oxidation and microbial spoilage, keeping the fruity style"),
        ("Pneumatic press, flushed with inert gas", "Takes large loads cheaply and protects against oxidation"),
        ("Flotation or centrifugation", "Fast clarification to a low-solids must, for a clean aromatic style and lower cost"),
        ("No hyperoxidation", "It would strip the aromatic compounds the style depends on"),
        ("Screwcap", "Low OTR, little cork-taint risk and cheap: suits a wine drunk young")]
_d14 = [3, 0, 4, 2, 1]
_l14 = [chr(65 + _d14.index(i)) for i in range(5)]
ch.ex("MATCH", "Inexpensive aromatic white: the reasons", 5, "Match each choice to its reason.",
      match([p[0] for p in _p14], [_p14[i][1] for i in _d14], _l14),
      pairs([(str(i + 1), _l14[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="1")

_p15 = [("Whole-bunch press", "Less oxidation, low tannin and a smoother mouthfeel; slow and costly"),
        ("Sedimentation, with some solids kept", "Adds aromatic complexity; may bring low reductive sulfur compounds and less fruit"),
        ("Optional hyperoxidation", "Removes bitter compounds for a smoother, less oxidation-prone wine, at extra cost"),
        ("Barrel fermentation", "Deeper color, fuller body, better oak integration, plus blending options"),
        ("Moderate temperature, 17\u201325\u00b0C", "Retains fruit and avoids low-temperature esters (Pinot Gris to 20\u00b0C, barrel Chardonnay to 25\u00b0C)")]
_d15 = [2, 4, 0, 3, 1]
_l15 = [chr(65 + _d15.index(i)) for i in range(5)]
ch.ex("MATCH", "Premium neutral white: the effects", 5, "Match each choice to its effect.",
      match([p[0] for p in _p15], [_p15[i][1] for i in _d15], _l15),
      pairs([(str(i + 1), _l15[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="2")

_r16 = ["Pneumatic press during or at the end of fermentation, to limit tannin", "At most 3\u20135 days of post-fermentation maceration, or none",
        "Fermentation at about 30\u00b0C to promote extraction", "Longer maceration to polymerize tannins and build ageing potential",
        "Metatartaric acid: quicker and cheaper than cold stabilization", "Glass only: impermeable to oxygen, so the wine can age"]
_a16 = ["Inexpensive red", "Inexpensive red", "Premium red", "Premium red", "Inexpensive red", "Premium red"]
ch.ex("TICK", "Inexpensive or premium red?", 6, "Tick the one style each statement describes.",
      tickgrid(_r16, ["Inexp. red", "Prem. red"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a16))), mins=3, ref="3\u20134")
ch.page()

_e = ["Both cut cost and time.", "Machine harvest is cheaper for large vineyards, keeping the price low.",
      "Carbonic or heat extraction is fast, and does not tie up tanks in long macerations.", "Both serve the same aim: volume and speed."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Give the choice <b>and</b> the reason. A choice alone earns little.",
      explain("Explain why <b>machine harvest and carbonic maceration</b> both suit inexpensive red wine.", [], lines=3) + [Checklist(_e)],
      kp("Any 3 of 4: lower cost and time \u00b7 cheaper for large vineyards, price kept low \u00b7 fast extraction, tanks not tied up \u00b7 shared aim of volume and speed."),
      mins=5, ref="1")

_mc = [("Which set best marks an inexpensive aromatic white?", ["Hand harvest, skin contact, barrel", "Machine harvest, no skin contact, cool steel, screwcap",
                                                                "Whole-bunch press, oak, cork", "Carbonic maceration, oak"]),
       ("The clearest single marker of ageing-focused red is:", ["Screwcap closure", "Extended post-fermentation maceration", "Cultured yeast", "Machine harvest"]),
       ("Rotary fermenters and mechanized pump-overs suit:", ["Premium red", "High-volume inexpensive red", "Premium white", "Ros\u00e9 only"]),
       ("Partial MLF in premium white serves:", ["Throughput", "Blending options for complexity", "Lower cost", "Higher alcohol"]),
       ("Inexpensive red often uses what in place of oak barrels?", ["Alternatives such as chips or staves", "New French barrels", "Amphorae", "Nothing, ever"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 machine harvest, no skin contact, cool steel, screwcap"), ("2", "<b>B</b> \u2014 extended post-fermentation maceration"),
                ("3", "<b>B</b> \u2014 high-volume inexpensive red"), ("4", "<b>B</b> \u2014 blending options"), ("5", "<b>A</b> \u2014 chips or staves")]), mins=4, ref="1\u20133")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch21.pdf")
