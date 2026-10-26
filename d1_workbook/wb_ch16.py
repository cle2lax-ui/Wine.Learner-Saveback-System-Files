# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 16: Specific Options for White Winemaking."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("16", "Specific Options for White Winemaking",
             ["set skin contact against hyperoxidation",
              "say why hyperoxidation fits Chardonnay, not Sauvignon Blanc",
              "state the solids target as a range with two risks",
              "compare free-run and press juice on four measures",
              "treat MLF, oak and lees as deliberate style choices"])

# ============================================================ PAGE 1
_r1 = ["Extracts aroma precursors and a little tannin", "Browns the must, then precipitates out during fermentation",
       "Suits aromatic varieties such as Riesling, Muscat and Viognier", "Suits non-aromatic Chardonnay",
       "Would strip the thiols that Sauvignon Blanc depends on", "Taken to the extreme gives orange or amber wine",
       "Its main cost is extra labor to run and monitor", "Carried out below 15\u00b0C to slow extraction and oxidation"]
_a1 = ["Skin contact", "Hyperoxidation", "Skin contact", "Hyperoxidation", "Hyperoxidation", "Skin contact", "Hyperoxidation", "Skin contact"]
ch.ex("TICK", "Skin contact or hyperoxidation?", 8, "They do opposite jobs: one extracts, one strips. Tick one for each.",
      tickgrid(_r1, ["Skin contact", "Hyperoxidation"], label_w=330),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a1))), mins=4, ref="1\u20132")

_sb = [(0, 0.5, "#E9E2C8", "Below 0.5%", "Risk of a stuck fermentation: yeast lack nutrients"),
       (0.5, 2, "#9CC987", "0.5\u20132%", "The typical target range"),
       (2, 3, "#E8A44A", "Above 2%", "More texture and complexity, but a risk of reductive faults")]
ch.ex("SCALE", "The solids target is a range", 3, "Write the consequence in each dotted box. Both ends carry a risk.",
      BandScale(0, 3, _sb, [0, 0.5, 1, 2, 3], unit="%", box_h=54),
      kp("<b>Below 0.5%:</b> stuck-fermentation risk \u00b7 <b>0.5\u20132%:</b> typical target \u00b7 <b>above 2%:</b> texture and complexity, "
         "but reductive-fault risk. Below about 1% needs enzymes or centrifugation."), mins=3, ref="3")
ch.page()

# ============================================================ PAGE 2
ch.ex("FLOW", "Grape to fermentation: the optional steps", 3, "Complete the dotted boxes, in order.",
      VFlow(["Skin contact (optional): skipped for most white wine", Blank("Press: free-run is gentlest; later fractions are more tannic"),
             Blank("Hyperoxidation (optional, and variety-specific)"), Blank("Clarification: solids brought to a target range"),
             "Fermentation"], box_h=23, gap=10, width=430),
      kp("Press \u2192 hyperoxidation (optional) \u2192 clarification to a solids target \u2192 fermentation."), mins=3, ref="intro")

_rc = [["Solids", "Low", Blank("Higher", 1)], ["Tannin", "Low", Blank("Progressively more tannic (may be blended back or discarded)", 2)],
       ["Acidity", "Higher", Blank("Lower", 1)], ["pH", "Lower", Blank("Higher", 1)]]
ch.ex("COMPARE", "Free-run against press juice", 4, "They differ on four measures at once. Complete the press column.",
      compare(["", "Free-run juice", "Later press fractions"], _rc, [90, 150, 278]),
      kp("<b>Press fractions:</b> higher solids \u00b7 more tannic \u00b7 lower acidity \u00b7 higher pH."), mins=3, ref="intro")
f, a = cloze(["Skin contact lasts roughly {{1\u201324+}} hours; chilling below {{15\u00b0C}} slows extraction and oxidation. Must is clarified to "
              "{{0.5\u20132}}% solids; below about {{1}}% needs enzymes or centrifugation. Sedimentation chills to about {{4\u00b0C}} for "
              "{{12\u201324}} hours. White fermentation is cooler than red, about {{15\u00b0C}}, to retain esters."], width=72)
ch.ex("COMPLETE", "White winemaking numbers", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=3, ref="1, 3, 4")

ch.page()

# ============================================================ PAGE 3
_arts = [A2.ClarFlotation(150), A2.ClarCentrifuge(150), A2.ClarSediment(150)]
ch.ex("NAME", "Name the clarification method", 4,
      "Name each drawing from the word bank (one name is not drawn), then answer the last question. <b>3 points for names, 1 for the last.</b>",
      [WordBank(["Centrifugation", "Enzymes", "Flotation", "Sedimentation"], ncols=4), PanelFigure(_arts, gap=14),
       LineFill("The one not drawn, which works on must but not on wine:", w=W, h=19)],
      kp("<b>1</b> Flotation (gas carries solids up) \u00b7 <b>2</b> Centrifugation \u00b7 <b>3</b> Sedimentation (chilled about 4\u00b0C, 12\u201324 hours). "
         "Not drawn: <b>enzymes</b> (pectolytic; break down pectins)."), mins=4, ref="3")

_p6 = [("Sedimentation", "The cheapest; needs no equipment, but slow and ties up tank space"),
       ("Flotation", "Fast; needs fining agents and gas, but no chilling cost"),
       ("Centrifugation", "Fast and continuous; an expensive machine that needs gas-flushing"),
       ("Enzymes", "The only agent that works on must but not on wine")]
_d6 = [2, 0, 3, 1]
_l6 = [chr(65 + _d6.index(i)) for i in range(4)]
ch.ex("MATCH", "Clarification: the trade-off", 4, "Match each method to its trade-off.",
      match([p[0] for p in _p6], [_p6[i][1] for i in _d6], _l6),
      pairs([(str(i + 1), _l6[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="3")

ch.page()

# ============================================================ PAGE 4
_r8 = ["Malolactic conversion often chosen, for complexity", "Malolactic conversion usually avoided, to protect aromatics",
       "Hyperoxidation suits it", "Skin contact is often used", "Oak would add unwanted vanilla and toast", "Higher solids acceptable if closely monitored"]
_a8 = ["Chardonnay", "Riesling / Sauvignon Blanc", "Chardonnay", "Riesling / Sauvignon Blanc", "Riesling / Sauvignon Blanc", "Chardonnay"]
ch.ex("TICK", "Chardonnay or the aromatics?", 6, "Tick the variety group each choice suits.",
      tickgrid(_r8, ["Chardonnay", "Riesling / Sauv. Blanc"], label_w=330),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a8))), mins=3, ref="1\u20134")

_tf = [("Most white wine gets significant skin contact.", False, "Most uses zero or minimal contact: the desirable compounds sit mainly in the pulp."),
       ("Hyperoxidation permanently browns the wine.", False,
        "The browned compounds precipitate out during fermentation; the lasting effect is oxidative stability."),
       ("Riesling and Sauvignon Blanc skip MLF because they are low in acid.", False,
        "They are high-acid varieties; MLF is skipped to preserve their primary aromas."),
       ("Higher must solids are always a quality risk.", False,
        "A little solids content feeds yeast and adds complexity; the risks sit at both ends of the range."),
       ("B\u00e2tonnage releases lees compounds faster but adds oxygen whenever the vessel is opened.", True, ""),
       ("Lees ageing matters more for white wine than for red.", True, "")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20134")
ch.page()

# ============================================================ PAGE 5
_cw = cached_crossword(16)
_nw = len(_cw["clues"]["A"]) + len(_cw["clues"]["D"])
ch.ex("CROSSWORD", "Chapters 14\u201316 vocabulary", _nw, "One point per word. Answers are single words, no spaces.",
      crossword_block(_cw, key=False, cell=15.0), crossword_answers(_cw), mins=7, ref="14\u201316")

_e = ["Oxidation destroys the most volatile aromas.",
      "Sauvignon Blanc\u2019s style depends on volatile thiols and methoxypyrazines, which hyperoxidation would strip.",
      "Chardonnay has fewer prized volatile aromas to lose, so it gains the oxidative stability at little cost."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "The fit is about volatility, not intensity.",
      explain("Explain why <b>hyperoxidation suits Chardonnay but not Sauvignon Blanc</b>.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: oxidation destroys volatile aromas \u00b7 Sauvignon Blanc depends on thiols and methoxypyrazines \u00b7 Chardonnay has fewer to lose."),
      mins=4, ref="2")
ch.page()

# ============================================================ PAGE 6
_mc = [("Most white wine is made with:", ["Long skin contact", "Zero or minimal skin contact", "Hyperoxidation", "Full fermentation on skins"]),
       ("The usual solids target for white must is about:", ["0\u20130.1%", "0.5\u20132%", "5\u201310%", "Exactly 1%"]),
       ("Which clarification method works on must but not on wine?", ["Sedimentation", "Flotation", "Centrifugation", "Enzymes"]),
       ("Orange wine is made by:", ["Adding red grapes", "Fermenting white grapes fully on their skins", "Hyperoxidizing the must", "Aging in cask"]),
       ("The drawback of b\u00e2tonnage is that it:", ["Strips body", "Adds oxygen whenever the vessel opens", "Lowers acidity", "Raises solids"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 zero or minimal contact"), ("2", "<b>B</b> \u2014 0.5\u20132% solids"), ("3", "<b>D</b> \u2014 enzymes"),
                ("4", "<b>B</b> \u2014 white grapes fermented on skins"), ("5", "<b>B</b> \u2014 adds oxygen when the vessel opens")]), mins=4, ref="1\u20134")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch16.pdf")
