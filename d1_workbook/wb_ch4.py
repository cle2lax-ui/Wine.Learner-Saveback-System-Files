# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 4: Approaches to Grape Growing."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("4", "Approaches to Grape Growing",
             ["tell the six approaches apart by what defines each",
              "see which approaches overlap rather than compete",
              "place every disadvantage: vineyard, environment, term or cost",
              "keep the biodynamic preparations straight",
              "write a balanced evaluation, not two lists"])

# ============================================================ PAGE 1
_p1 = [("Conventional", "Raises production and cuts labor: mechanization, chemical inputs, irrigation, clonal selection"),
       ("Sustainable", "Environmental, social and economic aims; chemicals only when thresholds are exceeded"),
       ("Organic", "Rejects synthetic fertilizers, fungicides, herbicides and pesticides; builds soil life"),
       ("Biodynamic", "Organic plus Steiner\u2019s cosmology: practices timed to lunar, planetary and stellar cycles"),
       ("Regenerative", "Improves soil and water rather than just maintaining them; the vineyard as an agroecosystem"),
       ("Precision", "Sensors, GPS and GIS map variation so interventions can be targeted row by row")]
_d1 = [3, 5, 1, 4, 0, 2]
_l1 = [chr(65 + _d1.index(i)) for i in range(6)]
ch.ex("MATCH", "The six approaches", 6, "Match each approach to what defines it.",
      match([p[0] for p in _p1], [_p1[i][1] for i in _d1], _l1),
      pairs([(str(i + 1), _l1[i]) for i in range(6)], ncols=6, width=COLW), mins=3, ref="1\u20136")

_o = ["Evaluate and control \u2014 only if thresholds are exceeded and prevention has failed",
      "Set thresholds \u2014 the levels at which action is needed",
      "Preventative measures \u2014 anticipate problems, boost the vine\u2019s own defenses",
      "Identify and monitor \u2014 what to look for, and when"]
ch.ex("ORDER", "The IPM cycle", 4, "Integrated pest management (lutte raisonn\u00e9e) runs in four steps. Number them 1\u20134.",
      order(_o, [4, 1, 3, 2]), kp("Top to bottom: <b>4 \u00b7 1 \u00b7 3 \u00b7 2</b> (thresholds, monitor, prevent, control)."), mins=2, ref="2")
ch.page()

# ============================================================ PAGE 2
_r3 = ["May use synthetic fungicides", "Uses sulfur and copper sprays", "Requires organic certification as a baseline",
       "The term is not protected", "Uses dynamized horn preparations", "Rejects manufactured fertilizers and pesticides",
       "Treats the vineyard as a weed-free monoculture"]
_a3 = ["Conventional, Sustainable", "Organic, Biodynamic", "Biodynamic", "Sustainable", "Biodynamic", "Organic, Biodynamic", "Conventional"]
ch.ex("TICK", "Which approaches?", 7,
      "Tick <b>every</b> approach that fits. The approaches overlap. <b>1 point per row with exactly the right ticks.</b>",
      tickgrid(_r3, ["Conventional", "Sustainable", "Organic", "Biodynamic"]),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a3))), mins=4, ref="1\u20134")

_r4 = ["Significant yield loss in wet years", "Copper builds up in the soil", "The term \u2018sustainable\u2019 is not protected",
       "Certification costs money", "Sensor and software costs", "Regenerative is not legally defined"]
_a4 = ["Vineyard", "Environmental", "Definitional", "Commercial", "Commercial", "Definitional"]
ch.ex("TICK", "Locate the disadvantage", 6,
      "Naming the <i>type</i> of a disadvantage is evaluation. Tick one type for each.",
      tickgrid(_r4, ["Vineyard", "Environmental", "Definitional", "Commercial"]),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a4))), mins=3, ref="3\u20136")
ch.page()

# ============================================================ PAGE 3
_p5 = [("500", "Cow-horn manure buried over winter; sprayed on soil to catalyze humus formation"),
       ("501", "Ground quartz in a horn, buried six months; sprayed on the vines to encourage growth"),
       ("502\u2013508", "Compost starters: yarrow, chamomile, nettle, oak bark, dandelion, valerian"),
       ("Moon ascending", "Summer, sap rising: take cuttings for grafting, avoid pruning"),
       ("Moon descending", "Winter, roots favored: the best time to plant or prune"),
       ("Ashing", "Spreading ashes of burnt weed seeds or harmful animals")]
_d5 = [4, 2, 5, 0, 3, 1]
_l5 = [chr(65 + _d5.index(i)) for i in range(6)]
ch.ex("MATCH", "Biodynamic preparations and calendar", 6, "Match each item to what it is or does.",
      match([p[0] for p in _p5], [_p5[i][1] for i in _d5], _l5),
      pairs([(str(i + 1), _l5[i]) for i in range(6)], ncols=6, width=COLW), mins=3, ref="4")

f, a = cloze([
    "IPM acts only when pest damage would exceed the {{cost}} of intervening \u2014 the {{economic threshold}}.",
    "Organic growers use {{sulfur}} and {{copper sulfate}} against mildews; build-up of {{copper}} in soil is the main criticism.",
    "<i>Bacillus subtilis</i> competes with {{Botrytis cinerea}} for space on the grape.",
    "Pheromone tags create \u2018{{sexual confusion}}\u2019 in moths and mealy bugs.",
    "{{Demeter}} is the commonest biodynamic certifier; organic bodies should all meet {{IFOAM}} standards.",
], width=84)
ch.ex("COMPLETE", "Treatments and certifiers", len(a), "Fill each blank. <b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=4, ref="2\u20134")
ch.page()

# ============================================================ PAGE 4
_tf = [("Sustainable viticulture is chemical-free.", False,
        "IPM will use chemicals when necessary; it reduces and better times applications."),
       ("Organic growers never spray.", False, "They use sulfur and copper; what they reject is synthetic products."),
       ("Preparation 501 is horn manure.", False, "501 is horn silica; 500 is horn manure."),
       ("Regenerative viticulture is just another word for organic.", False,
        "It aims to improve soil and water, not merely maintain them, and is not legally defined."),
       ("Research comparing organic and biodynamic growing has been inconclusive.", True, ""),
       ("Precision viticulture is within reach of every grower.", False,
        "It needs large upfront investment: large-scale or high-value estates, mostly California and Australia.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="2\u20136")

_cw4 = cached_crossword(4)
_nw4 = len(_cw4["clues"]["A"]) + len(_cw4["clues"]["D"])
ch.ex("CROSSWORD", "Chapters 2\u20134 vocabulary", _nw4, "One point per word. Answers are single words, no spaces.",
      crossword_block(_cw4, key=False, cell=16.0), crossword_answers(_cw4), mins=6, ref="1\u20136")
ch.page()

# ============================================================ PAGE 5
_i9 = ["Rejects synthetic fertilizers and pesticides", "Limited tilling, so soils sequester carbon",
       "Variable-rate application technology", "A period of conversion before certification",
       "Mycorrhizal fungi partner with the vines", "Remote or proximal sensors",
       "Heavy-metal (copper) build-up is a concern", "The Rodale Institute coined the term in the 1980s"]
ch.ex("SORT", "Which approach?", 8, "Write each number under the approach it belongs to.",
      [sort_bank(_i9, ncols=2), Spacer(1, 6), sort_columns(["Organic", "Regenerative", "Precision"], h=58)],
      kp("<b>Organic:</b> 1, 4, 7 \u00b7 <b>Regenerative:</b> 2, 5, 8 \u00b7 <b>Precision:</b> 3, 6"), mins=4, ref="3, 5, 6")

_mc = [("IPM justifies a chemical spray only when:",
        ["The spray calendar says so", "Thresholds are exceeded and prevention has failed", "Any pest is seen", "A neighbor sprays"]),
       ("Which is true of Demeter?",
        ["It replaces organic certification", "It requires organic certification as a baseline", "It certifies sustainable growers", "It bans copper"]),
       ("Preparation 501 is:",
        ["Manure in a cow horn", "Ground quartz in a cow horn, buried six months", "Yarrow in a deer\u2019s bladder", "Burnt weed seeds"]),
       ("The Regenerative Organic Alliance measures:",
        ["Soil health, animal welfare and human empowerment", "Copper levels only", "Pest thresholds", "Yield per hectare"]),
       ("Most used in California and Australia, and needing heavy upfront investment:",
        ["Organic viticulture", "Biodynamic viticulture", "Precision viticulture", "Sustainable viticulture"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 thresholds exceeded, prevention failed"), ("2", "<b>B</b> \u2014 organic is its baseline"),
                ("3", "<b>B</b> \u2014 500 is manure, 501 is silica"), ("4", "<b>A</b> \u2014 three named measures"),
                ("5", "<b>C</b> \u2014 precision viticulture")]), mins=4, ref="2\u20136")
ch.page()

# ============================================================ PAGE 6
_e1 = ["Copper sulfate is effective against mildews.", "Frequent use builds up heavy-metal copper in the soil.",
       "So some argue longer-lasting synthetic sprays are better for the environment.",
       "Synthetics can also mean fewer tractor passes."]
ch.ex("EXPLAIN", "Evaluate: the copper argument", 3,
      "Three or four sentences, then self-mark. <b>Evaluation weighs both sides.</b>",
      explain("Explain why <b>copper sprays</b> are a double-edged choice for organic growers.", [], lines=3) + [Checklist(_e1)],
      kp("Any 3 of 4: effective against mildew \u00b7 copper builds up in soil \u00b7 synthetics argued better \u00b7 fewer tractor passes."),
      mins=4, ref="3")
_e2 = ["Knowing pest and vine lifecycles plus weather monitoring predicts outbreaks.",
       "Well-timed applications replace a regimented spray calendar.",
       "Fewer applications are needed.",
       "Intervening only before the economic threshold limits damage, chemicals and cost."]
ch.ex("EXPLAIN", "Evaluate: sustainable viticulture", 3,
      "Three or four sentences, then self-mark.",
      explain("Explain why <b>sustainable viticulture</b> can cut chemical use and cost at the same time.", [], lines=3) + [Checklist(_e2)],
      kp("Any 3 of 4: lifecycle knowledge and weather monitoring \u00b7 well-timed sprays \u00b7 fewer applications \u00b7 economic threshold."),
      mins=4, ref="2")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch4.pdf")
