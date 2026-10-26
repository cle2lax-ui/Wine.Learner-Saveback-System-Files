# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 19: Specific Options for Rose Winemaking."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("19", "Specific Options for Ros\u00e9 Winemaking",
             ["tell the three methods apart, and which gives predictable color",
              "see how ros\u00e9 viticulture inverts red-wine priorities",
              "treat red-into-white blending as a legal question",
              "say why MLF is usually avoided in ros\u00e9",
              "remember that color keeps falling during fermentation"])

# ============================================================ PAGE 1
_r1 = ["Black grapes pressed at once, then fermented like white wine", "Hours to days of skin contact before pressing",
       "A little red wine blended into much more white wine", "The palest method (vin gris, pale Provence styles)",
       "Often a by-product of red-wine sa\u00ecgn\u00e9e", "Banned in most EU geographical indications",
       "The only method with fully predictable final color", "Traditional Spanish ros\u00e9 and Tavel"]
_a1 = ["Direct pressing", "Short maceration", "Blending", "Direct pressing", "Short maceration", "Blending", "Blending", "Short maceration"]
ch.ex("TICK", "Which method?", 8, "Tick the one method each statement describes.",
      tickgrid(_r1, ["Direct pressing", "Short maceration", "Blending"], label_w=330),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a1))), mins=4, ref="intro")

f, a = cloze(["Ros\u00e9 ferments cool, at {{12\u201316\u00b0C}}, mostly in {{steel}}. Yields are often kept {{higher}} than for red, and grapes are harvested "
              "{{earlier}} than red from the same site. Short maceration lasts {{hours}} to {{days}}. MLF is usually {{avoided}}, because buttery "
              "flavors would mask the fresh {{fruit}}."], width=70)
ch.ex("COMPLETE", "Ros\u00e9 numbers and choices", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=3, ref="1\u20132")
ch.page()

# ============================================================ PAGE 2
_arts = [A2.RoseBlend(150), A2.RoseDirect(150), A2.RoseShortMac(150)]
ch.ex("NAME", "Name the method", 4,
      "Name each drawing from the word bank, then answer the last question. <b>3 points for names, 1 for the last.</b>",
      [WordBank(["Blending", "Direct pressing", "Short maceration"], ncols=3), PanelFigure(_arts, gap=14),
       LineFill("The method that gives the most predictable color:", w=W, h=19)],
      kp("<b>1</b> Blending \u00b7 <b>2</b> Direct pressing (palest) \u00b7 <b>3</b> Short maceration (usually deeper). "
         "Most predictable color: <b>blending</b>, because both components are already finished wines."), mins=4, ref="intro")

_rc = [["Yield", "Lower, for concentration", Blank("Often higher, to limit concentration", 2)],
       ["Harvest", "Fully ripe, with ripe tannins", Blank("Earlier than red from the same site", 2)],
       ["Variety", "High color and tannin", Blank("Low-to-medium color and tannin", 2)],
       ["Target wine", "Concentrated and structured", Blank("Medium-high acidity, low-medium alcohol, fresh fruit", 2)]]
ch.ex("COMPARE", "Ros\u00e9 viticulture inverts red", 4, "Complete the ros\u00e9 column.",
      compare(["", "Red wine", "Ros\u00e9"], _rc, [90, 205, 223]),
      kp("<b>Ros\u00e9:</b> higher yields \u00b7 earlier harvest \u00b7 lower color and tannin varieties \u00b7 medium-high acidity, low-medium alcohol, fresh fruit."),
      mins=3, ref="1")
ch.page()

# ============================================================ PAGE 3
_cw = cached_crossword(19)
_nw = len(_cw["clues"]["A"]) + len(_cw["clues"]["D"])
ch.ex("CROSSWORD", "Chapters 17\u201319 vocabulary", _nw, "One point per word. Answers are single words, no spaces.",
      crossword_block(_cw, key=False, cell=15.0), crossword_answers(_cw), mins=7, ref="17\u201319")

_e = ["Direct pressing and short maceration both lose color during fermentation, so the final shade is a moving target.",
      "Blending starts from two finished wines, so the color is set by adjusting the ratio.",
      "That makes blending the only method with fully predictable color."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Colors keep falling after pressing; say what that does.",
      explain("Explain why <b>blending</b> gives more predictable color than direct pressing or short maceration.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: color falls during fermentation \u00b7 blending starts from finished wines \u00b7 adjust the ratio to hit the shade."), mins=4, ref="intro")
ch.page()

# ============================================================ PAGE 4
_tf = [("All ros\u00e9 is made the same way.", False, "There are three methods: direct pressing, short maceration and blending."),
       ("Ros\u00e9 grapes are grown like red-wine grapes.", False,
        "Ros\u00e9 viticulture inverts red priorities: higher yields, cooler sites or earlier picking, lower-tannin varieties."),
       ("Color is fixed once pressing or maceration ends.", False, "Color keeps decreasing during fermentation."),
       ("A saign\u00e9e ros\u00e9 is free of trade-offs.", False,
        "It is cheap, but the grapes were grown and picked for red wine, so may suit ros\u00e9 less well, e.g. on acidity."),
       ("MLF is usually avoided in ros\u00e9.", True, ""),
       ("Most ros\u00e9 is fined and filtered because it is often bottled in clear glass.", True, "")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20132")

_s = ["Champagne ros\u00e9", "Franciacorta ros\u00e9", "Most other EU geographical indications"]
ch.ex("DECIDE", "Red into white: allowed or banned?", 3, "Circle <b>A</b> if blending red into white to make ros\u00e9 is allowed, or <b>B</b> if banned.",
      choose(_s, ["A", "B"]), kp("<b>1</b> A \u00b7 <b>2</b> A \u00b7 <b>3</b> B. Champagne and Franciacorta are the named exceptions."), mins=2, ref="intro")
ch.page()

# ============================================================ PAGE 5
_mc = [("Which method gives the palest ros\u00e9?", ["Blending", "Short maceration", "Direct pressing", "Sa\u00ecgn\u00e9e"]),
       ("Ros\u00e9 is usually fermented at:", ["12\u201316\u00b0C, as for white", "25\u201330\u00b0C", "35\u00b0C", "Any temperature"]),
       ("MLF is usually avoided in ros\u00e9 because:", ["It lowers pH", "Buttery flavors mask the fresh fruit", "It raises sugar", "It is banned"]),
       ("Hand harvest enables which ros\u00e9 technique?", ["Whole-bunch pressing, giving the lowest color", "Machine blending", "Flash d\u00e9tente", "Carbonic maceration"]),
       ("Blending near the end for ros\u00e9 made by pressing is:", ["Illegal", "Common, to adjust color and flavor or keep batches consistent", "Required", "Rare"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>C</b> \u2014 direct pressing"), ("2", "<b>A</b> \u2014 12\u201316\u00b0C"), ("3", "<b>B</b> \u2014 buttery flavors mask fruit"),
                ("4", "<b>A</b> \u2014 whole-bunch pressing"), ("5", "<b>B</b> \u2014 adjusts color and flavor")]), mins=4, ref="1\u20132")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch19.pdf")
