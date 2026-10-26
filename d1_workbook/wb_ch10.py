# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 10: Viticulture Scenarios."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("10", "Viticulture Scenarios",
             ["explain a region\u2019s practices from climate and economics",
              "see one principle give opposite decisions in different places",
              "compare two regions on vigor, density, training or harvest",
              "tie yield to price point",
              "recall each region\u2019s signature figures"])

# ============================================================ PAGE 1
_p1 = [("Priorat", "Bush vines, low density, hand harvest, 15\u201325 hl/ha, premium pricing"),
       ("Pauillac", "About 10,000 vines/ha on VSP; Cabernet Sauvignon blended with Merlot"),
       ("Finger Lakes", "Riesling; hilled-up grafts; Scott-Henry to tame vigor; lake-moderated"),
       ("Central Valley", "Irrigation and fertilizer, California sprawl, 180\u2013200 hl/ha, machine harvest")]
_d1 = [2, 0, 3, 1]
_l1 = [chr(65 + _d1.index(i)) for i in range(4)]
ch.ex("MATCH", "Four regions, four signatures", 4, "Match each region to its profile.",
      match([p[0] for p in _p1], [_p1[i][1] for i in _d1], _l1),
      pairs([(str(i + 1), _l1[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="1\u20134")

_r2 = ["Irrigation needs advance authorization", "Variety chosen by market demand and price per ton",
       "Deep lakes make <i>V. vinifera</i> viable at all", "Highest density, about 10,000 vines/ha", "Lowest yields: 15\u201325 hl/ha",
       "Soil hilled up over the graft", "Machine harvest is the cost-effective default",
       "Cabernet Sauvignon blended with earlier-ripening Merlot"]
_a2 = ["Priorat", "Central Valley", "Finger Lakes", "Pauillac", "Priorat", "Finger Lakes", "Central Valley", "Pauillac"]
ch.ex("TICK", "Which region?", 8, "Tick the one region each statement describes.",
      tickgrid(_r2, ["Priorat", "Pauillac", "Finger Lakes", "Central Valley"], label_w=270),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a2))), mins=3, ref="1\u20134")
ch.page()

# ============================================================ PAGE 2
_rc = [["Vigor", "Low: poor, free-draining soil limits it", Blank("High: nutrient-rich soil and plentiful rainfall", 2)],
       ["Density and why", Blank("High, about 10,000/ha: rain removes vine competition and land is expensive", 2),
        "Low, 2,800\u20133,200/ha: large vines need room"],
       ["Training", "VSP, head-trained, replacement cane-pruned", Blank("Scott-Henry splits the canopy to manage vigor", 2)]]
ch.ex("COMPARE", "Same yield, opposite routes", 3,
      "Both reach 50\u201360 hl/ha. Low vigor is recovered through density in one; high vigor is reined in through training in the other. "
      "Complete the dotted cells.",
      compare(["", "Pauillac", "Finger Lakes"], _rc, [88, 215, 215]),
      kp("<b>Finger Lakes vigor:</b> high. <b>Pauillac density:</b> high, about 10,000/ha. <b>Finger Lakes training:</b> Scott-Henry."),
      mins=3, ref="2\u20133")

f, a = cloze(["Priorat\u2019s best vineyards face {{north-east}} to escape afternoon heat; scarcity of water and nutrients keeps vigor low, so "
              "{{bush vines}} suit the site, planted at just {{2,500\u20133,000}} vines per hectare.",
              "In the Central Valley, irrigation and fertilizer give vigorous vines. Because vines are expensive, density is only "
              "{{1,200\u20131,800}}/ha, trained as {{California sprawl}}: a single wire above the {{cordon}}."], width=60)
ch.ex("COMPLETE", "Vigor decides the system", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=3, ref="1, 4")

ch.page()

# ============================================================ PAGE 2b
_bank = sorted(["Central Valley", "Finger Lakes", "Pauillac", "Priorat"])
ch.ex("NAME", "Whose vine is it?", 4,
      "Each region trains its vines to suit its vigor, labor and economics. Write the region beside each drawing. <b>1 point each.</b>",
      [WordBank(_bank, ncols=4), PanelFigure([A.TrellisSH(120), A.TrellisBush(120), A2.TrellisSprawl(120), A.TrellisVSP(120)], gap=10)],
      kp("<b>1</b> Finger Lakes (Scott-Henry splits a vigorous canopy) \u00b7 <b>2</b> Priorat (bush vines, low vigor) \u00b7 "
         "<b>3</b> Central Valley (California sprawl, cheap) \u00b7 <b>4</b> Pauillac (VSP, dense plantings)."), mins=3, ref="1\u20134")

_p5 = [("Pauillac: dense", "Rain removes vine-to-vine competition, and land is expensive"),
       ("Priorat: sparse", "Roots must range widely for scarce water and nutrients"),
       ("Finger Lakes: sparse", "Large, vigorous vines need room; wide rows ease mechanization"),
       ("Central Valley: sparse", "Vines are expensive to buy; big vines give high yields")]
_d5 = [1, 3, 0, 2]
_l5 = [chr(65 + _d5.index(i)) for i in range(4)]
ch.ex("MATCH", "Density follows the scarce resource", 4,
      "Three regions plant sparsely, for three different reasons. Match each choice to its reason.",
      match([p[0] for p in _p5], [_p5[i][1] for i in _d5], _l5),
      pairs([(str(i + 1), _l5[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="2\u20134")
ch.page()

# ============================================================ PAGE 3
_cw = cached_crossword(10)
_nw = len(_cw["clues"]["A"]) + len(_cw["clues"]["D"])
ch.ex("CROSSWORD", "Chapters 8\u201310 vocabulary", _nw, "One point per word. Answers are single words, no spaces.",
      crossword_block(_cw, key=False, cell=16.0), crossword_answers(_cw), mins=6, ref="1\u20134")

_tf = [("Priorat\u2019s best vineyards face south-west to capture the most heat.", False,
        "They face north-east, to escape the worst afternoon heat."),
       ("Low vigor is a viticultural failure in Priorat.", False,
        "It is the right fit for the site: bush vines suit it and nothing is over-shaded."),
       ("Pauillac\u2019s high density is a universal marker of premium intent.", False,
        "It is an economic response to expensive land, with rain removing competition."),
       ("Finger Lakes growers hill up soil over the graft.", True, ""),
       ("Central Valley growers generally skip labor-intensive summer pruning.", True, ""),
       ("Pauillac and Finger Lakes reach the same yield by the same route.", False,
        "Pauillac through density on low-vigor vines; Finger Lakes by reining in high vigor through training.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20134")
ch.page()

# ============================================================ PAGE 4
_e = ["Priorat\u2019s scarcity gives very low yields (15\u201325 hl/ha) and heavy hand labor, so only premium or super-premium prices work.",
      "The Central Valley\u2019s irrigation and fertilizer give 180\u2013200 hl/ha at minimum cost, so only inexpensive, high-volume wine works.",
      "Neither region could survive with the other\u2019s yield at its own price point."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Compare on one axis, and tie it to the economics.",
      explain("Compare how <b>Priorat and the Central Valley</b> each match yield to price point.", [], lines=4) + [Checklist(_e)],
      kp("1 mark each: Priorat low yield \u2192 premium price \u00b7 Central Valley high yield \u2192 low price \u00b7 neither works with the other\u2019s yield."),
      mins=5, ref="1, 4")

_mc = [("The main variety of the Finger Lakes, winter-hardy and late-budding, is:", ["Cabernet Franc", "Riesling", "Garnacha", "Merlot"]),
       ("Which profile fits Priorat?", ["VSP, 10,000 vines/ha, machine harvest", "Bush vines, hand harvest, 15\u201325 hl/ha",
                                          "Scott-Henry, 180\u2013200 hl/ha", "California sprawl, irrigated"]),
       ("California sprawl is:", ["A single wire above the cordon with shoots flopping over it", "A split canopy on two wires",
                                    "A bush vine without a trellis", "A form of Guyot"]),
       ("Pauillac blends Cabernet Sauvignon with Merlot because Cabernet can struggle for:",
        ["Winter hardiness", "Body and aromatic range in cooler sites or years", "Drought tolerance", "Disease resistance"]),
       ("Central Valley grapes may be picked relatively early mainly to:", ["Raise sugar", "Dodge autumn rain risk", "Save irrigation", "Meet a legal minimum"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 Riesling"), ("2", "<b>B</b> \u2014 bush vines, hand harvest, 15\u201325 hl/ha"),
                ("3", "<b>A</b> \u2014 single wire, shoots flop over"), ("4", "<b>B</b> \u2014 body and aromatic range"),
                ("5", "<b>B</b> \u2014 dodge autumn rain risk")]), mins=4, ref="1\u20134")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch10.pdf")
