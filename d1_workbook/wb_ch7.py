# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 7: Canopy Management."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("7", "Canopy Management",
             ["trace sunlight\u2019s effects on grape composition",
              "name the direction of a vine\u2019s imbalance",
              "calculate area yield from planting density",
              "match trellis to vigor, slope and mechanization",
              "order the season\u2019s seven summer corrections"])

# ============================================================ PAGE 1
_r1 = ["Anthocyanins in black grapes", "Methoxypyrazines (herbaceous character)", "Terpenes, e.g. the grapey aroma of Muscat",
       "Malic acid (warmer grapes respire more)", "Polymerization of tannin (less bitter)", "Bud fruitfulness for next year",
       "Fungal disease pressure (better air and spray coverage)"]
_a1 = ["Increases", "Reduces", "Increases", "Reduces", "Increases", "Increases", "Reduces"]
ch.ex("TICK", "What does sun exposure do?", 7,
      "Exposing the grapes and leaves to sunlight (without going as far as sunburn). Tick one for each.",
      tickgrid(_r1, ["Increases", "Reduces"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a1))), mins=3, ref="1")

_ch = [("Under-cropping", ["Too little fruit for the vine\u2019s vigor", Blank("Shoot growth continues, competing for sugars"),
                           Blank("Dense, shady canopy: lower quality fruit"), Blank("Shade cuts bud fruitfulness: low yield next year")]),
       ("Over-cropping", ["Too much fruit for the vine\u2019s vigor", Blank("Sugars drawn from carbohydrate reserves in trunk, cordons, roots"),
                          "A weaker vine in future years"])]
ch.ex("CHAIN", "Two kinds of imbalance", 4,
      "The mechanisms differ. One is a self-perpetuating cycle; the other a one-way depletion. Complete the dotted boxes.",
      [Chain(items, label=lab, box_h=46) for lab, items in _ch],
      kp("<b>Under-cropping:</b> shoots keep growing \u2192 dense shade \u2192 fewer inflorescences next year (and it recurs). "
         "<b>Over-cropping:</b> sugars drawn from stored reserves \u2192 weaker vine later."), mins=4, ref="2")
ch.page()

# ============================================================ PAGE 2
_r3 = ["A warm, well-watered, fertile site", "Limited water or poor soil", "A more vigorous variety (Cabernet Sauvignon)",
       "A virus infection", "A very old vine", "Ros\u00e9 rather than red"]
_a3 = ["Higher", "Lower", "Higher", "Lower", "Lower", "Higher"]
ch.ex("TICK", "What shifts \u2018balanced\u2019?", 6,
      "Balance is relative, not absolute. Does each factor raise or lower the yield a vine can ripen?",
      tickgrid(_r3, ["Higher yield", "Lower yield"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a3))), mins=3, ref="2")

_v = [("A", 1.2, 8000), ("B", 3.0, 3500), ("C", 0.8, 10000)]
rows = [[Paragraph("VINEYARD", WS["hdr"]), Paragraph("KG PER VINE", WS["hdr"]), Paragraph("VINES PER HA", WS["hdr"]),
         Paragraph("KG PER HA", WS["hdr"])]]
for (n, kg, d) in _v:
    rows.append([Paragraph(n, WS["cellb"]), Paragraph("%.1f" % kg, WS["cell"]), Paragraph(format(d, ","), WS["cell"]), FillCell(140, h=17)])
tb = Table(rows, colWidths=[110, 110, 110, 188], hAlign="LEFT")
tb.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                        ("LINEABOVE", (0, 0), (-1, 0), LINE_BOLD, INK), ("LINEBELOW", (0, 0), (-1, 0), LINE_RULE, INK),
                        ("LINEBELOW", (0, 1), (-1, -2), 0.3, FEINT), ("LINEBELOW", (0, -1), (-1, -1), LINE_BOLD, INK)]))
_ay = [kg * d for (_, kg, d) in _v]
ch.ex("CALCULATE", "Area yield", 4,
      "Area yield = yield per vine \u00d7 planting density (illustrative figures). A low per-vine yield can still give a high area yield. "
      "<b>1 point per vineyard, 1 for the last question.</b>",
      [tb, Spacer(1, 4), LineFill("Which vineyard crops the most per hectare?", w=W, h=19)],
      kp("A <b>%s</b> \u00b7 B <b>%s</b> \u00b7 C <b>%s</b> kg/ha. Highest per hectare: <b>B</b>, though A and C have lower per-vine yields." %
         tuple(format(int(v), ",") for v in _ay)), mins=3, ref="2\u20133")

_p5 = [("North\u2013south rows", "Generally the most even light exposure"),
       ("West-facing bunches", "Hotter afternoon sun: need more leaf shading against sunburn"),
       ("A slope over 10%", "Plant up-and-down, not across, unless terraced"),
       ("High-vigor vines", "Need wider within-row spacing or overlapping canopies shade")]
_d5 = [2, 0, 3, 1]
_l5 = [chr(65 + _d5.index(i)) for i in range(4)]
ch.ex("MATCH", "Density and row orientation", 4, "Match each to its consequence.",
      match([p[0] for p in _p5], [_p5[i][1] for i in _d5], _l5),
      pairs([(str(i + 1), _l5[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="3")
ch.page()

# ============================================================ PAGE 3
_arts = [A.TrellisBush(120), A.TrellisVSP(120), A.TrellisGDC(120), A.TrellisSH(120)]
_names = ["Bush vine", "VSP", "Geneva Double Curtain", "Scott-Henry"]
_bank = sorted(["Bush vine", "Geneva Double Curtain", "Lyre", "Scott-Henry", "Smart-Dyson", "VSP"])
ch.ex("NAME", "Name the system", 8,
      "Name each drawing from the word bank (two names are not drawn), then answer the last two questions. "
      "<b>4 points for names, 4 for the splits.</b>",
      [WordBank(_bank, ncols=3), PanelFigure(_arts),
       LineFill("Split horizontally: Geneva Double Curtain and", w=W, h=19),
       LineFill("Split vertically: Scott-Henry and", w=W, h=19)],
      kp("<b>1</b> Bush vine \u00b7 <b>2</b> VSP \u00b7 <b>3</b> Geneva Double Curtain \u00b7 <b>4</b> Scott-Henry. "
         "Horizontal split: GDC and <b>Lyre</b>. Vertical split: Scott-Henry and <b>Smart-Dyson</b>."), mins=4, ref="3")

_r7 = ["Best for low or moderate vigor", "Cheap and simple, but cannot be mechanized", "Invented to split the canopy of vigorous vines",
       "Fruit in one zone per vine, aiding mechanization", "Suits dry conditions that restrict vigor",
       "Large yields of quality fruit, but harder to manage"]
_a7 = ["VSP", "Bush vine", "Complex", "VSP", "Bush vine", "Complex"]
ch.ex("TICK", "Match the trellis to the vine", 6, "Tick the system each statement fits best.",
      tickgrid(_r7, ["Bush vine", "VSP", "Complex"], label_w=330),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a7))), mins=3, ref="3")
ch.page()

# ============================================================ PAGE 4
_o = ["Shoot trimming \u2014 limits growth and canopy thickness",
      "Disbudding \u2014 late spring, removes buds left as frost insurance",
      "Leaf removal \u2014 cuts shading to enhance ripening",
      "Shoot positioning \u2014 tucks shoots into the trellis wires",
      "Crop thinning \u2014 near v\u00e9raison, evens up ripening",
      "Pinching \u2014 at flowering, removes shoot tips to improve fruit set",
      "Shoot removal \u2014 clears infertile or poorly placed shoots"]
ch.ex("ORDER", "The season in seven corrections", 7,
      "Summer pruning corrects the canopy through the season. Number the steps 1\u20137 in the order they happen.",
      order(_o, [5, 1, 6, 3, 7, 4, 2]),
      kp("Top to bottom: <b>5 \u00b7 1 \u00b7 6 \u00b7 3 \u00b7 7 \u00b7 4 \u00b7 2</b>. Order: disbudding, shoot removal, shoot positioning, pinching, "
         "shoot trimming, leaf removal, crop thinning."), mins=4, ref="4")

_p9 = [("Disbudding", "Late spring: removes buds left as frost insurance; corrects balance and yield"),
       ("Pinching", "At flowering: removes shoot tips to improve fruit set"),
       ("Leaf removal", "Cuts shading to enhance ripening; too much in hot climates risks sunburn"),
       ("Crop thinning", "Near v\u00e9raison: concentrates ripening or removes the least-ripe bunches")]
_d9 = [3, 1, 0, 2]
_l9 = [chr(65 + _d9.index(i)) for i in range(4)]
ch.ex("MATCH", "When and why", 4, "The same act (removing material) serves different aims at different times. Match each.",
      match([p[0] for p in _p9], [_p9[i][1] for i in _d9], _l9),
      pairs([(str(i + 1), _l9[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="4")
ch.page()

# ============================================================ PAGE 5
_tf = [("Sunlight exposure raises bud fruitfulness, while shade favors tendrils.", True, ""),
       ("Over-cropping triggers a self-perpetuating vegetative cycle.", False,
        "That is under-cropping; over-cropping draws down carbohydrate reserves."),
       ("North\u2013south rows generally give the most even light exposure.", True, ""),
       ("A spur has 8\u201320 buds.", False, "A spur is cut to 2\u20133 buds; replacement canes carry 8\u201320."),
       ("VSP is best for very vigorous vines.", False, "It suits low to moderate vigor; vigorous vines need complex systems that split the canopy."),
       ("Excess sun and heat can cause sunburn, so hot climates may manage for some shade.", True, "")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20134")

_e = ["Too little fruit for the vine\u2019s vigor means shoot growth continues and competes with the fruit for sugars.",
      "The dense, shady canopy lowers fruit quality.",
      "Shade reduces bud fruitfulness, so fewer inflorescences form for next year: low yield.",
      "The spiral feeds itself: once started it tends to continue."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Name the direction of the imbalance. <b>Cause and effect earns marks.</b>",
      explain("Explain how <b>under-cropping</b> can lower both quality and future yield.", [], lines=3) + [Checklist(_e)],
      kp("Any 3 of 4: shoots compete with fruit \u00b7 dense shady canopy \u00b7 reduced bud fruitfulness \u00b7 self-perpetuating cycle."),
      mins=4, ref="2")
ch.page()

# ============================================================ PAGE 6
_cw7 = cached_crossword(7)
_nw7 = len(_cw7["clues"]["A"]) + len(_cw7["clues"]["D"])
ch.ex("CROSSWORD", "Chapters 5\u20137 vocabulary", _nw7, "One point per word. Answers are single words, no spaces.",
      crossword_block(_cw7, key=False, cell=16.0), crossword_answers(_cw7), mins=6, ref="1\u20134")

_mc = [("The optimal yield is:",
        ["The maximum weight of grapes", "The maximum weight with the composition the wine style needs", "The minimum the law allows", "A fixed figure per region"]),
       ("Replacement cane-pruned VSP is usually called:", ["Geneva Double Curtain", "Guyot", "Scott-Henry", "Bush vine"]),
       ("At winter pruning, more buds are left on:", ["Weak vines", "More vigorous vines", "Only very old vines", "Every vine alike"]),
       ("Slopes over 10% should normally be planted:", ["Across the slope", "Up and down the slope (unless terraced)", "In circles", "Any way"]),
       ("Removing shoot tips at flowering to improve fruit set is:", ["Disbudding", "Pinching", "Leaf removal", "Crop thinning"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 weight with the right composition"), ("2", "<b>B</b> \u2014 Guyot"),
                ("3", "<b>B</b> \u2014 more buds for more vigor"), ("4", "<b>B</b> \u2014 up and down"), ("5", "<b>B</b> \u2014 pinching")]),
      mins=4, ref="2\u20134")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch7.pdf")
