# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 11: Wine Components."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("11", "Wine Components",
             ["keep total acidity and pH apart",
              "classify aromatic compounds by origin",
              "give context before a verdict: virtue or fault",
              "apply the EU sweetness rule, acidity allowance included",
              "recall the key figures"])

# ============================================================ PAGE 1
f, a = cloze([
    "Wine is about {{85}}% water. At {{14.5}}% abv and above, alcohol cuts the volatility of aromas and raises bitterness.",
    "In warm climates tartaric and malic acid make up about {{two-thirds}} of total acidity, typically {{5.5\u20138.5}} g/L; "
    "wine pH is typically {{3\u20134}}, and pH 3 is {{ten}} times more acidic than pH 4.",
    "French total acidity as sulfuric acid is at a ratio of 1:{{1.5}} to the tartaric figure.",
    "Dry wines usually carry {{2\u20133}} g/L residual sugar; Sauternes can reach {{150}} g/L and Pedro Xim\u00e9nez up to {{400}} g/L.",
], width=56)
ch.ex("RECALL", "Numbers that matter", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=4, ref="1\u20135")

_r2 = ["The sum of all acids present, in g/L", "An inverse, logarithmic scale", "Additive: more acid, higher figure",
       "Typically between 3 and 4 in wine", "Can be expressed as sulfuric acid in France",
       "Low value: SO2 works better, red color is brighter, wine ages well"]
_a2 = ["Total acidity", "pH", "Total acidity", "pH", "Total acidity", "pH"]
ch.ex("TICK", "Total acidity or pH?", 6, "Related, not interchangeable: buffering (e.g. by potassium) breaks the link. Tick one for each.",
      tickgrid(_r2, ["Total acidity", "pH"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a2))), mins=3, ref="3")
ch.page()

# ============================================================ PAGE 2
_i3 = ["Esters", "Rotundone", "Vanillin", "Thiols (4MMP)", "Acetaldehyde", "Methoxypyrazines", "Terpenes", "Diacetyl",
       "Eucalyptol", "Reductive sulfur compounds"]
ch.ex("SORT", "The four sources of aroma", 10,
      "Classify by <i>origin</i>, not by chemical family. Write each number under its source.",
      [sort_bank(_i3, ncols=2), Spacer(1, 6),
       sort_columns(["From the grape", "Fermented precursors", "Fermentation by-products", "Other sources"], h=62)],
      kp("<b>Grape:</b> 2, 6 \u00b7 <b>Precursors:</b> 4, 7 \u00b7 <b>By-products:</b> 1, 5, 8, 10 \u00b7 <b>Other:</b> 3, 9"), mins=5, ref="4")

_p4 = [("Methoxypyrazines", "Grassy, green pepper"), ("Rotundone", "Pepper (Syrah, Gr\u00fcner Veltliner)"),
       ("Thiols (e.g. 4MMP)", "Box tree (Sauvignon Blanc)"), ("Esters", "Banana, as in Beaujolais Nouveau"),
       ("Diacetyl", "Buttery, from malolactic conversion"), ("Vanillin", "Vanilla, from new oak barrels")]
_d4 = [4, 0, 5, 2, 1, 3]
_l4 = [chr(65 + _d4.index(i)) for i in range(6)]
ch.ex("MATCH", "Compound and aroma", 6, "Match each compound to its aroma.",
      match([p[0] for p in _p4], [_p4[i][1] for i in _d4], _l4),
      pairs([(str(i + 1), _l4[i]) for i in range(6)], ncols=6, width=COLW), mins=3, ref="4")
ch.page()

# ============================================================ PAGE 3
_s5 = ["Acetaldehyde in Fino sherry", "Acetaldehyde in a fresh white table wine", "Reductive sulfur smelling of struck match, in moderation",
       "Reductive sulfur smelling of rotten eggs", "Acetic acid at a low level", "Ethyl acetate (nail-varnish remover) in excess"]
ch.ex("DECIDE", "Virtue or fault?", 6,
      "The same compound can be either. Circle <b>V</b> if acceptable in that context or <b>F</b> if a fault.",
      choose(_s5, ["V", "F"]),
      kp("<b>1</b> V (defines Fino) \u00b7 <b>2</b> F \u00b7 <b>3</b> V (sometimes desirable) \u00b7 <b>4</b> F \u00b7 <b>5</b> V (present in all wines) \u00b7 "
         "<b>6</b> F. Give the context before the verdict."), mins=3, ref="3\u20134")

f, a = cloze([
    "<b>Dry:</b> up to {{4}} g/L, or up to {{9}} g/L if total acidity is no more than {{2}} g/L below the RS figure.",
    "<b>Medium-dry:</b> {{4}}\u2013{{12}} g/L, or up to {{18}} g/L if total acidity is no more than {{10}} g/L below the RS figure.",
    "<b>Medium:</b> {{12}}\u2013{{45}} g/L. <b>Sweet:</b> at least {{45}} g/L.",
], width=60)
ch.ex("COMPLETE", "EU sweetness: the thresholds", len(a), "Still wines. <b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=4, ref="5")

_s7 = ["RS 3 g/L, total acidity 6 g/L", "RS 9 g/L, total acidity 7 g/L", "RS 9 g/L, total acidity 5 g/L",
       "RS 15 g/L, total acidity 6 g/L", "RS 50 g/L, total acidity 7 g/L", "RS 14 g/L, total acidity 3 g/L"]
ch.ex("DECIDE", "Which EU term?", 6,
      "Circle <b>D</b> dry, <b>MD</b> medium-dry, <b>M</b> medium or <b>S</b> sweet. Check the acidity allowance first.",
      choose(_s7, ["D", "MD", "M", "S"]),
      kp("<b>1</b> D \u00b7 <b>2</b> D (9\u22127 = 2) \u00b7 <b>3</b> MD (9\u22125 = 4, too far for dry) \u00b7 <b>4</b> MD (15\u22126 = 9, within 10) \u00b7 "
         "<b>5</b> S \u00b7 <b>6</b> M (14\u22123 = 11, too far)"), mins=4, ref="5")
ch.page()

# ============================================================ PAGE 4
_tf = [("Total acidity and pH are two ways of saying the same thing.", False,
        "They are related, not interchangeable: buffering breaks a clean conversion."),
       ("Esters are a permanent feature of a wine\u2019s aroma.", False, "Most are unstable and break down within a few months."),
       ("Anthocyanins and tannins are the same compound.", False, "Anthocyanins are color pigments; tannins cause the drying sensation."),
       ("A little residual sugar can make tannins seem softer.", True, ""),
       ("Glycerol is the third most abundant component of dry wine.", True, ""),
       ("Aroma precursors are themselves aromatic.", False, "They are building blocks, aromatic only after fermentation.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="3\u20137")

_e = ["Perceived dryness depends on the balance of acidity and residual sugar, not the sugar figure alone.",
      "The wine\u2019s elevated acidity matches the sugar.",
      "The EU allows \u2018dry\u2019 up to 9 g/L if total acidity is no more than 2 g/L below the RS figure."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Balance, not a flat ceiling.",
      explain("Explain why a German Riesling with up to about <b>9 g/L residual sugar</b> can taste dry.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: balance of acidity and sugar \u00b7 elevated acidity matches the sugar \u00b7 the EU acidity allowance."), mins=4, ref="3, 5")
ch.page()

# ============================================================ PAGE 5
_sb = [(0, 4, "#E9E2C8", "Up to 4 g/L", "Dry (sec, trocken)"), (4, 12, "#F0D58A", "4\u201312 g/L", "Medium-dry (demi-sec, halbtrocken)"),
       (12, 45, "#E8A44A", "12\u201345 g/L", "Medium (moelleux, lieblich)"), (45, 60, "#C8553D", "At least 45 g/L", "Sweet (doux, s\u00fcss)")]
ch.ex("SCALE", "The EU sweetness scale", 4, "Name each band, in English. (The acidity allowance can shift a wine up one band: see the earlier exercise.)",
      BandScale(0, 60, _sb, [0, 4, 12, 45, 60], unit=" g/L", box_h=46),
      kp("<b>Up to 4:</b> dry \u00b7 <b>4\u201312:</b> medium-dry \u00b7 <b>12\u201345:</b> medium \u00b7 <b>at least 45:</b> sweet."), mins=2, ref="5")

_mc = [("At 14.5% abv and above, alcohol tends to:", ["Raise the volatility of aromas", "Reduce aroma volatility and raise bitterness",
                                                      "Lower pH", "Remove tannin"]),
       ("A low pH:", ["Reduces the effectiveness of SO2", "Gives red wines a brighter red color and aids aging",
                      "Lowers microbiological stability", "Raises total acidity"]),
       ("Vanillin comes mainly from:", ["The grape skin", "New oak barrels", "Yeast autolysis", "Malolactic conversion"]),
       ("Eucalyptol in a wine is detected via:", ["Nearby eucalyptus trees, absorbed into grape skin wax", "Fermentation by-products",
                                                    "New oak", "Aroma precursors"]),
       ("Higher glycerol levels occur in wines made from:", ["Frozen grapes", "Botrytis-affected grapes", "Early-picked grapes", "Dried grapes only"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 less volatile, more bitter"), ("2", "<b>B</b> \u2014 brighter red, ages well"), ("3", "<b>B</b> \u2014 new oak"),
                ("4", "<b>A</b> \u2014 nearby eucalyptus, via skin wax"), ("5", "<b>B</b> \u2014 botrytis (e.g. Tokaji)")]), mins=4, ref="2\u20136")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch11.pdf")
