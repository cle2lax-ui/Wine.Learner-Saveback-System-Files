# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 18: Specific Options for Red Winemaking."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("18", "Specific Options for Red Winemaking",
             ["explain why anthocyanins need tannin for lasting color",
              "put cap management in order, gentlest to most extractive",
              "tell the whole-berry methods apart",
              "say what each pre-fermentation method extracts",
              "know which red wines skip oak, and why"])

# ============================================================ PAGE 1
_arts = [A2.CapRotary(120), A2.CapPunch(120), A2.CapRack(120), A2.CapPump(120)]
ch.ex("NAME", "Name the cap-management method", 5,
      "Name each drawing from the word bank, then answer the last question. <b>4 points for names, 1 for the last.</b>",
      [WordBank(["Pumping over", "Punching down", "Rack and return", "Rotary fermenter"], ncols=4), PanelFigure(_arts, gap=10),
       LineFill("The two gentlest of the four are punching down and:", w=W, h=19)],
      kp("<b>1</b> Rotary fermenter \u00b7 <b>2</b> Punching down \u00b7 <b>3</b> Rack and return (d\u00e9lestage) \u00b7 <b>4</b> Pumping over. "
         "Gentlest pair: punching down and <b>pumping over</b>."), mins=4, ref="1")

_o = ["Rack and return (d\u00e9lestage) \u2014 more extractive, used sparingly", "Punching down (pigeage) \u2014 the gentlest; labor-intensive by hand",
      "Rotary fermenter or Ganimede \u2014 the most extractive and most automatable", "Pumping over (remontage) \u2014 still gentle; aerobic or anaerobic"]
ch.ex("ORDER", "Gentlest to most extractive", 4, "Cap management is a ladder, not four equal options. Number the steps 1\u20134.",
      order(_o, [3, 1, 4, 2]), kp("Top to bottom: <b>3 \u00b7 1 \u00b7 4 \u00b7 2</b> (punching down, pumping over, rack and return, rotary)."), mins=2, ref="1")
ch.page()

# ============================================================ PAGE 2
_cur = A2.ExtractionCurves(280)
f, a = cloze(["Tannin dissolves best in {{alcohol}}; anthocyanins dissolve best in {{must}}."], width=60)
ch.ex("LABEL", "What is extracted, and when", 2 + len(a),
      "Label the two curves, then complete the sentence. <b>1 point per label and per blank.</b>",
      [LabelFigure(_cur, align="center")] + f,
      kp(label_key(_cur) + ".  " + ans_inline(a) + "  So cold soaking gives color with little tannin; once alcohol appears the reverse is true."), mins=3, ref="intro")

_r4 = ["Whole bunches held under added CO2", "No added CO2: the bottom grapes crush under the weight", "Intracellular fermentation reaches about 2% abv, then the grapes split",
       "Can continue on the skins afterward for more body and tannin", "Progressively crushed as the cap is punched down", "The Beaujolais Nouveau method"]
_a4 = ["Carbonic", "Semi-carbonic", "Carbonic", "Semi-carbonic", "Mixed with crushed", "Carbonic"]
ch.ex("TICK", "Which whole-berry method?", 6, "Tick one method for each statement.",
      tickgrid(_r4, ["Carbonic", "Semi-carbonic", "Mixed with crushed"], label_w=330),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a4))), mins=3, ref="2")
ch.page()

# ============================================================ PAGE 3
_p5 = [("Cold soak", "4\u201310\u00b0C for 3\u20137 days: gentle color, little tannin; common on Pinot Noir"),
       ("Thermovinification", "50\u201360\u00b0C and above: fast color, less tannin; denatures laccase"),
       ("Flash d\u00e9tente", "85\u201390\u00b0C for about 2 minutes, then vacuum-cooled; also fixes smoke taint"),
       ("Saign\u00e9e", "Draws off juice after crushing; the pale juice often becomes ros\u00e9"),
       ("Co-fermentation", "A little white grape added, often 5% or less, such as Viognier with Syrah")]
_d5 = [4, 1, 3, 0, 2]
_l5 = [chr(65 + _d5.index(i)) for i in range(5)]
ch.ex("MATCH", "Before and during fermentation", 5, "Match each technique to what it does.",
      match([p[0] for p in _p5], [_p5[i][1] for i in _d5], _l5),
      pairs([(str(i + 1), _l5[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="1")

f, a = cloze(["Cold soaking runs at {{4\u201310\u00b0C}} for {{3\u20137}} days; flash d\u00e9tente at {{85\u201390\u00b0C}} for about {{2}} minutes. Fruity reds ferment "
              "near {{20\u00b0C}}, structured reds near {{30\u00b0C}}. Carbonic maceration reaches about {{2}}% abv before the grapes are pressed; "
              "intracellular fermentation can cut malic acid by up to {{50}}%. Oak maturation for red is typically {{6 months\u20132 years}}."], width=70)
ch.ex("COMPLETE", "Red winemaking numbers", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=4, ref="1\u20133")
ch.page()

# ============================================================ PAGE 4
_tf = [("Tannin extracts best before fermentation begins.", False, "Anthocyanins extract in must; tannin needs alcohol."),
       ("Gentle oxidation damages the color of red wine.", False,
        "Oxygen drives anthocyanin\u2013tannin binding, which gives stable color."),
       ("Carbonic maceration gives low tannin by the winemaker\u2019s choice.", False,
        "It is chemistry: tannin needs alcohol, and the grapes are pressed at only about 2% abv."),
       ("Punching down is the most extractive cap-management method.", False, "It is the gentlest; rotary fermenters are the most extractive."),
       ("Malolactic conversion is a real yes-or-no choice for red wine.", False, "It is routine for red; only vessel and timing are choices."),
       ("Heat-based macerations denature the laccase enzyme of botrytis.", True, "")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20133")

_e = ["Anthocyanins alone are unstable: lees aging or SO2 can strip them and they fade toward brown.",
      "Binding with tannin gives a far more stable compound.",
      "Oxygen drives that reaction, so gentle oxidation (micro-oxygenation, barrels) supports red color."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Oxygen helps here; it is the reverse of white wine\u2019s usual story.",
      explain("Explain why <b>anthocyanins need tannin</b> for lasting color in red wine.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: anthocyanins alone are unstable \u00b7 binding with tannin is far more stable \u00b7 oxygen drives the reaction."), mins=4, ref="intro")
ch.page()

# ============================================================ PAGE 5
_mc = [("Cold soaking is common on which grape, because of its naturally low anthocyanins?", ["Cabernet Sauvignon", "Pinot Noir", "Syrah", "Malbec"]),
       ("Which cap-management method is the most extractive and most automatable?", ["Punching down", "Pumping over", "Rack and return", "Rotary fermenters"]),
       ("Semi-carbonic maceration is distinguished by:", ["Added CO2", "No added CO2: the bottom grapes crush and blanket the rest", "Heat", "Cold soaking"]),
       ("Saign\u00e9e is:", ["Adding white grapes", "Drawing off juice after crushing, concentrating the must", "Adding sugar", "Flash heating"]),
       ("Which reds deliberately skip oak for primary fruit?", ["Unoaked Loire Cabernet Franc, Menc\u00eda, Argentine Malbec", "All premium Bordeaux", "All premium red wines", "Only wines above 15% abv"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 Pinot Noir"), ("2", "<b>D</b> \u2014 rotary fermenters"), ("3", "<b>B</b> \u2014 no added CO2"),
                ("4", "<b>B</b> \u2014 drawing off juice after crushing"), ("5", "<b>A</b> \u2014 unoaked Loire Cabernet Franc, Menc\u00eda, Malbec")]), mins=4, ref="1\u20133")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch18.pdf")
