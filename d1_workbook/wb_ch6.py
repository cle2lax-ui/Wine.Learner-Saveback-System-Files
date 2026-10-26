# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 6: Managing Nutrients and Water."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("6", "Managing Nutrients and Water",
             ["compare organic and mineral fertilizers",
              "weigh the five weed-control methods",
              "say which methods raise or lower vigor and frost risk",
              "choose an irrigation system and a water source",
              "state RDI\u2019s window and its effects precisely"])

# ============================================================ PAGE 1
_r1 = ["Must be broken down by soil organisms before use", "Can supply a single nutrient: more tailored",
       "Improves soil structure and water retention", "Concentrated, so cheap to transport and spread",
       "Bulky, and must be incorporated into the soil", "Releases nutrients gradually"]
_a1 = ["Organic", "Mineral", "Organic", "Mineral", "Organic", "Organic"]
ch.ex("TICK", "Organic or mineral fertilizer?", 6, "Tick the type each statement describes.",
      tickgrid(_r1, ["Organic", "Mineral"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a1))), mins=3, ref="2")

_p2 = [("Cultivation", "Damages soil structure and buries seeds, encouraging regrowth"),
       ("Herbicides", "Not permitted in organic or biodynamic viticulture; resistance risk"),
       ("Animal grazing", "Needs high training or timed grazing; animal care and pesticide vulnerability"),
       ("Cover crops", "Unsuited to steep slopes; hard to mow near the trunk"),
       ("Mulching", "Bulky, so costly to transport; needs a thick layer to work")]
_d2 = [3, 0, 4, 1, 2]
_l2 = [chr(65 + _d2.index(i)) for i in range(5)]
ch.ex("MATCH", "Weed control: the standout disadvantage", 5, "Match each method to its main drawback.",
      match([p[0] for p in _p2], [_p2[i][1] for i in _d2], _l2),
      pairs([(str(i + 1), _l2[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="2")
ch.page()

# ============================================================ PAGE 2
_r3 = ["Cultivation", "Herbicides", "Mulching", "Cover crops"]
ch.ex("TICK", "What does it do to vigor?", 4,
      "Removing weed competition tends to raise vigor; adding competition lowers it. Tick one for each.",
      tickgrid(_r3, ["Raises vigor", "Lowers vigor"], label_w=340),
      kp("<b>Raise:</b> cultivation, herbicides, mulching \u00b7 <b>Lower:</b> cover crops (they add competition)."), mins=2, ref="2")

_r4 = ["Bare, moist soil", "Weeds", "A cover crop", "Mulch"]
ch.ex("TICK", "What does it do to frost risk?", 4,
      "Bare moist soil absorbs heat by day and releases it at night. Tick one for each.",
      tickgrid(_r4, ["Raises frost risk", "Lowers frost risk"], label_w=340),
      kp("<b>Lowers:</b> bare, moist soil \u00b7 <b>Raise:</b> weeds, cover crops and mulches."), mins=2, ref="2")

_p5 = [("Pre-emergence", "Sprayed before weeds establish; persists in the surface soil and inhibits germination"),
       ("Contact", "Sprayed on established weeds; kills only the green parts it touches"),
       ("Systemic", "Taken in by the leaves; travels through the sap and kills the whole plant")]
_d5 = [2, 0, 1]
_l5 = [chr(65 + _d5.index(i)) for i in range(3)]
ch.ex("MATCH", "The three herbicide types", 3, "Match each herbicide to how it works.",
      match([p[0] for p in _p5], [_p5[i][1] for i in _d5], _l5),
      pairs([(str(i + 1), _l5[i]) for i in range(3)], ncols=3, width=COLW), mins=2, ref="2")
ch.page()

# ============================================================ PAGE 3
_bank = sorted(["Drip", "Flood", "Furrow", "Overhead sprinkler"])
ch.ex("NAME", "Name the irrigation system", 5,
      "Name each drawing from the word bank, then answer the last question. <b>4 points for names, 1 for the last.</b>",
      [WordBank(_bank, ncols=4), PanelFigure([A2.IrrFurrow(118), A2.IrrSprinkler(118), A2.IrrDrip(118), A2.IrrFlood(118)], gap=10),
       LineFill("Which of the four also gives frost protection?", w=W, h=19)],
      kp("<b>1</b> Furrow \u00b7 <b>2</b> Overhead sprinkler \u00b7 <b>3</b> Drip \u00b7 <b>4</b> Flood. Frost protection: <b>overhead sprinkler</b> "
         "(drip sits below the green parts)."), mins=4, ref="3")

f, a = cloze(["Regulated deficit irrigation imposes a deliberate water deficit between {{fruit set}} and {{v\u00e9raison}}. "
              "Mild to moderate stress halts {{shoot}} growth and redirects the vine toward the grapes. Berries are {{smaller}}, "
              "with a higher {{skin-to-juice}} ratio, concentrating {{anthocyanins}} and {{tannins}}. It is delivered by a "
              "{{drip}} system and usually lowers {{yield}}."], width=74)
ch.ex("COMPLETE", "Regulated deficit irrigation", len(a), "State the window precisely. <b>1 point per blank.</b>", f, kp(ans_inline(a)),
      mins=4, ref="3")

f, a = cloze(["Soil health has four related factors: {{structure}}, organic matter and {{humus}}, living {{organisms}} "
              "(earthworms, microbes) and total available {{nutrients}}."], width=76)
ch.ex("COMPLETE", "Soil health", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=2, ref="1")
ch.page()

# ============================================================ PAGE 4
_tf = [("Water high in dissolved solids suits drip irrigation well.", False,
        "Dissolved solids (mud) block drip and sprinkler systems; water needs settling and filtering."),
       ("Salinity is worse under drip irrigation than under flood irrigation.", True, ""),
       ("Regulated deficit irrigation simply means giving the vines less water.", False,
        "It is deliberately timed, controlled stress between fruit set and v\u00e9raison."),
       ("All EU GIs ban irrigation outright.", False, "Many restrict rather than ban; emergency use is often permitted."),
       ("Synthetic herbicides are permitted in organic viticulture.", False, "They are not permitted."),
       ("Artificial drainage is practical only before planting.", True, "")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="2\u20133")

_p6 = [("Drip", "By far the most common; controllable row by row; carries fertilizer; no frost protection"),
       ("Flood", "Cheap but inefficient; flat or gently sloping land only"),
       ("Furrow", "More efficient than flood; common in Argentina where Andean water is abundant"),
       ("Overhead sprinkler", "Expensive and uses more water than drip, but doubles as frost protection")]
_d6 = [1, 3, 0, 2]
_l6 = [chr(65 + _d6.index(i)) for i in range(4)]
ch.ex("MATCH", "Irrigation systems", 4, "Match each system to its profile.",
      match([p[0] for p in _p6], [_p6[i][1] for i in _d6], _l6),
      pairs([(str(i + 1), _l6[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="3")

ch.page()

# ============================================================ PAGE 5
_ch = [("Salinity", ["High salinity (parts of Australia)", Blank("Soil salt rises; roots struggle to take up water"),
                      Blank("The vine dehydrates; green parts wilt"), "Eventually the vine dies"]),
       ("RDI", ["Deficit between fruit set and v\u00e9raison", Blank("Shoot growth halts"),
                Blank("Smaller berries, higher skin-to-juice ratio"), "More concentrated anthocyanins and tannins"])]
ch.ex("CHAIN", "Cause, effect, consequence", 4, "Complete each chain with the missing links.",
      [Chain(items, label=lab, box_h=44) for lab, items in _ch],
      kp("<b>1</b> soil salt rises \u2192 vine dehydrates and wilts. <b>2</b> shoot growth halts \u2192 smaller berries, higher "
         "skin-to-juice ratio."), mins=3, ref="3")

_mc = [("Which weed-control method also fights erosion and gives a driving surface?",
        ["Cultivation", "Cover crops", "Herbicides", "Mulching"]),
       ("Which irrigation system also gives frost protection?",
        ["Drip", "Flood", "Furrow", "Overhead sprinkler"]),
       ("Regulated deficit irrigation is imposed:",
        ["Before budburst", "Between fruit set and v\u00e9raison", "After harvest", "During flowering"]),
       ("A herbicide taken in by the leaves that kills the whole plant is:",
        ["Pre-emergence", "Contact", "Systemic", "Residual"]),
       ("Compared with mineral fertilizers, organic fertilizers:",
        ["Are more concentrated", "Must be broken down by soil organisms first", "Are cheaper to transport", "Supply a single nutrient"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 cover crops"), ("2", "<b>D</b> \u2014 overhead sprinkler"),
                ("3", "<b>B</b> \u2014 fruit set to v\u00e9raison"), ("4", "<b>C</b> \u2014 systemic"),
                ("5", "<b>B</b> \u2014 broken down by soil organisms")]), mins=4, ref="2\u20133")

ch.page()

# ============================================================ PAGE 6
_e = ["It lowers vigor by adding competition for water and nutrients.", "It fights erosion.",
      "It adds biodiversity.", "It gives a firmer driving surface (but raises frost risk and suits flat ground)."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Name every function. <b>The exam rewards naming them all.</b>",
      explain("Explain why a <b>cover crop</b> is more than a weed-control method.", [], lines=3) + [Checklist(_e)],
      kp("Any 3 of 4: lowers vigor \u00b7 fights erosion \u00b7 adds biodiversity \u00b7 driving surface."), mins=4, ref="2")


if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch6.pdf")
