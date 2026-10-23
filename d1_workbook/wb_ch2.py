# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 2: The Vine Growth Cycle."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb import *
import wb_art as A

CHAP, TITLE = "2", "The Vine Growth Cycle"
K = Key()
story = []
add = story.append


def page():
    add(PageBreak())


ITEMS = [("2.1", 12), ("2.2", 5), ("2.3", 16), ("2.4", 8), ("2.5", 8), ("2.6", 7), ("2.7", 9), ("2.8", 6),
         ("2.9", 5), ("2.10", 6), ("2.11", 12), ("2.12", 6), ("2.13", 5), ("2.14", 3)]


def ans_inline(answers):
    return " \u00b7 ".join('<b>(%d)</b> <font color="%s"><b>%s</b></font>' % (i + 1, hexc(ANS), a)
                           for i, a in enumerate(answers))


# =============================================================================== PAGE 1
add(Opener(CHAP, TITLE,
           ["place every growth stage on the calendar, in both hemispheres",
            "recall the temperature thresholds that matter, to the degree",
            "explain what drives budburst, flowering success and fruit set",
            "tell coulure from millerandage",
            "follow sugar, acid, tannin and color through the four stages of grape development"],
           "Mastery Guide Chapter 2"))

# ---- 2.1 calendar
add(ExHeader("2.1", "CALENDAR", "Build the vine year", 12, mins=5, ref="Guide \u00a71"))
add(instr("Shade the <b>Northern Hemisphere</b> months each stage covers (6 points), then write the "
          "<b>Southern Hemisphere</b> months beside it (6 points). Note which stages overlap."))
_g = [("Dormancy", 10, 2, "May\u2013Sep"),
      ("Budburst", 2, 3, "Sep\u2013Oct"),
      ("Shoot and leaf growth", 2, 5, "Sep\u2013Dec"),
      ("Flowering and fruit set", 4, 5, "Nov\u2013Dec"),
      ("Grape development", 5, 8, "Dec\u2013Mar"),
      ("Harvest", 7, 8, "Feb\u2013Apr")]
add(Gantt(_g))
K.add("2.1", "Build the vine year",
      [kp("<b>North \u2192 South:</b> " + " \u00b7 ".join(
          '%s <font color="%s"><b>%s</b></font> \u2192 <font color="%s"><b>%s</b></font>' % (
              n, hexc(ANS), ["Nov\u2013Mar", "Mar\u2013Apr", "Mar\u2013Jun", "May\u2013Jun", "Jun\u2013Sep", "Aug\u2013Sep"][i],
              hexc(ANS), g[3]) for i, (n, g) in enumerate(zip([x[0] for x in _g], _g))) +
          ".")])

# ---- 2.2 match
add(ExHeader("2.2", "MATCH", "What each stage needs and fears", 5, mins=3, ref="Guide \u00a72\u20136"))
add(instr("Match each stage to its needs and threats."))
_m2 = [("Dormancy", "Needs temperatures below 10\u00b0C; threatened by extreme cold and by unusually mild spells"),
       ("Budburst", "Needs air and soil temperatures above 10\u00b0C; threatened by frost and cold soils"),
       ("Shoot and leaf growth", "Runs on stored carbohydrates plus warmth, light, water, nutrients; threatened by low reserves and water stress"),
       ("Flowering and fruit set", "Needs warmth (minimum 17\u00b0C); threatened by rain, cloud, wind and cold"),
       ("Grape development", "Needs sunlight, warmth and mild water stress; threatened by excess water or nutrients, shading, extremes of heat or cold")]
_d2 = [3, 0, 4, 1, 2]
_l2 = [chr(65 + _d2.index(i)) for i in range(5)]
add(match([p[0] for p in _m2], [_m2[i][1] for i in _d2], _l2))
K.add("2.2", "Match", [pairs([(str(i + 1), _l2[i]) for i in range(5)], ncols=5, width=COLW)])
page()

# =============================================================================== PAGE 2
add(ExHeader("2.3", "RECALL", "Numbers that matter", 16, mins=6, ref="Guide \u00a79"))
add(instr("Fill in every number. These are the cheapest marks in the unit \u2014 know them <b>to the degree</b>. "
          "<b>1 point per blank.</b>"))
_n, _na = cloze([
    "Dormancy: average air temperature below {{10\u00b0C}} (50\u00b0F).",
    "Winter damage: below {{\u221220\u00b0C}}; most <i>V. vinifera</i> is killed below {{\u221225\u00b0C}}.",
    "Budburst needs average air and soil temperatures above {{10\u00b0C}}.",
    "Flowering needs a minimum of {{17\u00b0C}} and normally starts within {{eight}} weeks of budburst.",
    "Typically {{30}}% of flowers become grapes (range 0 to {{60}}%).",
    "Pollen germination is best at {{26\u201332\u00b0C}}.",
    "Next year\u2019s bud fruitfulness is limited when temperatures are under {{25\u00b0C}}.",
    "Photosynthesis peaks at {{18\u201333\u00b0C}}, and needs more than one {{third}} of full sunlight.",
    "Mean temperature above {{21\u00b0C}} in the final month of ripening: rapid acid loss and a rise in pH.",
    "Mean temperature below {{15\u00b0C}} in the final month: acidity may stay too high.",
    "Anthocyanins build fastest between {{15\u00b0C}} and {{25\u00b0C}}.",
], width=62)
for f in _n:
    add(f)
K.add("2.3", "Numbers that matter", [kp(ans_inline(_na))])

add(ExHeader("2.4", "SORT", "Warm climate or cool climate?", 8, mins=3, ref="Guide \u00a76, \u00a78"))
add(instr("Which climate does each outcome belong to? Write the numbers in the column."))
_i4 = ["Sugar accumulates fastest", "Acidity is retained best", "Malic acid is lost fastest",
       "Methoxypyrazines persist longer", "Wines tend to be higher in alcohol", "Chardonnay: green and citrus fruit",
       "Chardonnay: stone and tropical fruit", "Respiration is slower"]
add(sort_bank(_i4, ncols=2))
add(Spacer(1, 6))
add(sort_columns(["Warm climate", "Cool climate"], h=64))
K.add("2.4", "Warm or cool?", [kp("<b>Warm:</b> 1, 3, 5, 7 \u00b7 <b>Cool:</b> 2, 4, 6, 8")])
page()

# =============================================================================== PAGE 3
add(ExHeader("2.5", "SORT", "What drives budburst?", 8, mins=4, ref="Guide \u00a73"))
add(instr("Four factors govern timing. Write each statement\u2019s number under the factor it illustrates."))
_i5 = ["Continental climates give fast, uniform budburst",
       "Sandy, free-draining soils warm up quickly",
       "Merlot buds a little under 10\u00b0C; Ugni Blanc a little over",
       "Late winter pruning postpones budburst",
       "A few unusually mild winter days can trigger early budburst",
       "Clay-rich, water-storing soils warm slowly",
       "Sauvignon Blanc, Cabernet Sauvignon and Syrah are late budding",
       "Maritime climates give less synchronized budburst"]
add(sort_bank(_i5, ncols=2))
add(Spacer(1, 6))
add(sort_columns(["Air temperature", "Soil temperature", "Grape variety", "Human factors"], h=72))
K.add("2.5", "What drives budburst?", [kp("<b>Air:</b> 1, 5, 8 \u00b7 <b>Soil:</b> 2, 6 \u00b7 <b>Variety:</b> 3, 7 \u00b7 <b>Human:</b> 4")])

add(ExHeader("2.6", "DECIDE", "Early or late budding?", 7, mins=3, ref="Guide \u00a73"))
add(instr("Circle <b>E</b> for early budding or <b>L</b> for late budding. Late-budding varieties need higher "
          "temperatures to burst, so are less exposed to spring frost."))
_v6 = ["Chardonnay", "Sauvignon Blanc", "Merlot", "Syrah", "Grenache", "Cabernet Sauvignon"]
add(choose(_v6, ["E", "L"]))
add(Spacer(1, 4))
add(LineFill("Which of these buds early but ripens late?", w=W, h=19))
K.add("2.6", "Early or late?", [kp("<b>E:</b> Chardonnay, Merlot, Grenache \u00b7 <b>L:</b> Sauvignon Blanc, Syrah, Cabernet "
                                    "Sauvignon. Early budding, late ripening: <b>Grenache</b> \u2014 budding time is not ripening time.")])
page()

# =============================================================================== PAGE 4
add(ExHeader("2.7", "LABEL", "A vine flower", 9, mins=4, ref="Guide \u00a75"))
add(instr("Label the eight parts. The pollen tube is following a path \u2014 trace it before you label it."))
_fl = A.Flower(300)
add(LabelFigure(_fl, align="center"))
add(LineFill("The anther and the filament together make up the", w=W, h=19))
K.add("2.7", "A vine flower", [kp(label_key(_fl) + ".  Anther + filament = the <b>stamen</b>.")])

add(ExHeader("2.8", "ORDER", "From pollen to grape", 6, mins=3, ref="Guide \u00a75"))
add(instr("Number the steps 1\u20136 in the order they happen."))
_o8 = ["The pollen tube delivers sperm cells, which fertilize the eggs in the ovule",
       "Pollen grains are shed from the anthers and land on the moist stigma",
       "The ovary wall swells into the skin and pulp \u2014 fruit set",
       "The pollen tubes penetrate the stigma, then the ovule in the ovary",
       "The fertilized ovules form seeds (up to four per grape)",
       "Each pollen grain germinates and grows a pollen tube"]
add(order(_o8, [4, 1, 6, 3, 5, 2]))
K.add("2.8", "From pollen to grape",
      [kp("Top to bottom: <b>4 \u00b7 1 \u00b7 6 \u00b7 3 \u00b7 5 \u00b7 2</b>.")])
page()

# =============================================================================== PAGE 5
add(ExHeader("2.9", "COMPARE", "Coulure and millerandage", 5, mins=4, ref="Guide \u00a75"))
add(instr("Two forms of irregular fruit set. Complete the dotted cells."))
_cw = [104, 207, 207]
_r9 = [
    ["What it is", Blank("Fruit set fails for a high proportion of flowers (ovules are not fertilized)", 2),
     "A high proportion of seedless grapes in the bunch"],
    ["Main cause", "A carbohydrate imbalance: low photosynthesis (cold and cloudy, or hot and arid) or vigorous shoot growth",
     Blank("Cold, wet, windy weather at fruit set", 2)],
    ["Susceptible varieties", Blank("Grenache, Cabernet Sauvignon, Merlot, Malbec", 2), Blank("Chardonnay, Merlot", 2)],
    ["Effect", "Excessive coulure can cut yield dramatically",
     Blank("Smaller grapes (some stay green, unripe): less wine, can hurt quality", 2)],
]
add(compare(["", "Coulure", "Millerandage"], _r9, _cw))
K.add("2.9", "Coulure and millerandage", [kp(
    "<b>Coulure \u2014 what:</b> fruit set fails for a high proportion of flowers (ovules not fertilized). "
    "<b>Millerandage \u2014 cause:</b> cold, wet, windy weather at fruit set. "
    "<b>Susceptible:</b> coulure \u2014 Grenache, Cabernet Sauvignon, Merlot, Malbec; millerandage \u2014 Chardonnay, Merlot. "
    "<b>Millerandage \u2014 effect:</b> smaller grapes (some stay green, unripe): less wine, can hurt quality.")])

add(ExHeader("2.10", "DECIDE", "True or false \u2014 then fix it", 6, mins=5, ref="Guide \u00a74\u20135"))
add(instr("Circle T or F. If false, correct it on the line. <b>1 point only if the call and the correction are both right.</b>"))
_tf = [
    ("Shoot growth is fastest between flowering and harvest.", False, "It is fastest between budburst and flowering."),
    ("Low stored carbohydrates can follow excessive leaf removal, water stress, mildew or very high yields the year before.", True, ""),
    ("Insects and wind make a major contribution to pollination in cultivated vines.", False,
     "Cultivated vines are self-pollinating; insects and wind contribute little."),
    ("Cold weather at flowering can lengthen it, making ripening less even.", True, ""),
    ("Vigorous shoot growth can contribute to coulure.", True, ""),
    ("Typically about half of all flowers become grapes.", False, "Typically about 30 percent (range 0 to 60)."),
]
for i, (t, v, fix) in enumerate(_tf):
    add(TFItem(i + 1, t))
K.add("2.10", "True or false", numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                                          ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fix)))
                                         for i, (t, v, fix) in enumerate(_tf)]))
page()

# =============================================================================== PAGE 6
add(ExHeader("2.11", "STAGE", "Which stage of grape development?", 12, mins=5, ref="Guide \u00a76"))
add(instr("Circle the stage: <b>1</b> early grape growth \u00b7 <b>2</b> v\u00e9raison \u00b7 <b>3</b> ripening \u00b7 <b>4</b> extra-ripening."))
_s11 = ["Hard green grapes grow; tartaric and malic acids accumulate",
        "Black grapes start to turn red as anthocyanins are made",
        "Sugar and water accumulate rapidly while acid falls",
        "Grapes shrivel; water loss concentrates the sugars",
        "Methoxypyrazines develop (herbaceous aromas)",
        "Growth slows for a few days \u2014 the lag phase",
        "Water arrives mainly through the xylem",
        "A sugar solution is delivered through the phloem",
        "The phloem imports no more sugar or water",
        "Tannins accumulate and are very bitter",
        "Tannins polymerize and become less bitter",
        "Cell walls turn stretchy; chlorophyll is broken down"]
_a11 = [1, 2, 3, 4, 1, 2, 1, 3, 4, 1, 3, 2]
add(choose(_s11, ["1", "2", "3", "4"]))
K.add("2.11", "Which stage?", [pairs([(str(i + 1), str(a)) for i, a in enumerate(_a11)], ncols=6, width=COLW)])

add(ExHeader("2.12", "CHAIN", "Cause, effect, consequence", 6, mins=4, ref="Guide \u00a76, \u00a78"))
add(instr("Complete each chain with the missing links \u2014 <b>the dotted boxes</b>."))
_ch = [
    ("Acidity and cool nights", ["Cool night temperatures", Blank("Respiration is slower"), Blank("Less malic acid is lost"),
                                 "Higher acidity in the wine"]),
    ("Acidity and heat", ["Mean temperature above 21\u00b0C in the final month", Blank("Rapid loss of acidity"), Blank("A rise in pH")]),
    ("Herbaceous aromas", ["Cool temperatures and limited sunlight (e.g. shaded bunches)",
                           Blank("Methoxypyrazines fall less during ripening"), Blank("Particularly herbaceous aromas and flavors")]),
]
for lab, items in _ch:
    add(Chain(items, key=False, label=lab, box_h=46))
K.add("2.12", "Chains", [kp("<b>1</b> slower respiration \u2192 less malic acid lost. <b>2</b> rapid acid loss \u2192 higher pH. "
                           "<b>3</b> methoxypyrazines fall less \u2192 herbaceous aromas and flavors.")])
page()

# =============================================================================== PAGE 7
add(ExHeader("2.13", "CHOOSE", "Multiple choice", 5, mins=4, ref="Guide \u00a73\u20138"))
add(instr("Circle one answer. The live D1 paper is written, not multiple choice \u2014 use these to find gaps."))
_mc = [
    ("Budburst can be delayed by:",
     ["Warm soils", "Late winter pruning", "Planting early-budding varieties", "Sandy, free-draining soil"], 1),
    ("Which statement is correct?",
     ["Grenache buds early and ripens late", "Sauvignon Blanc is an early-budding variety",
      "Chardonnay is a late-ripening variety", "Syrah is an early-budding variety"], 0),
    ("A warm region with a high diurnal range can still make high-acid wines because cool nights:",
     ["Increase tartaric acid", "Reduce the malic acid lost in respiration", "Stop sugar accumulating", "Raise the pH"], 1),
    ("Millerandage is a high proportion of:",
     ["Flowers that failed to set", "Seedless grapes", "Botrytis-infected grapes", "Grapes with red pulp"], 1),
    ("During extra-ripening, grapes shrivel and sugars concentrate because:",
     ["The phloem imports more sugar", "Water is lost through the grape while nothing more is imported",
      "Xylem flow increases", "Anthocyanins break down"], 1),
]
for i, (q, o, a) in enumerate(_mc):
    add(MCQ(i + 1, q, o))
K.add("2.13", "Multiple choice", numbered([
    ("1", "<b>B</b> \u2014 late pruning postpones budburst"),
    ("2", "<b>A</b> \u2014 budding \u2260 ripening time"),
    ("3", "<b>B</b> \u2014 cool nights slow respiration"),
    ("4", "<b>B</b> \u2014 seedless grapes"),
    ("5", "<b>B</b> \u2014 water loss, no new imports")]))

add(ExHeader("2.14", "EXPLAIN", "Write like an examiner", 3, mins=5, ref="Guide \u00a78"))
add(instr("Answer in three or four sentences, then self-mark. <b>Cause and effect earns marks</b>; a list does not."))
for f in explain("Explain why wines from <b>warm climates</b> tend to have higher alcohol levels.", [], lines=4):
    add(f)
_pts = ["Sugar accumulates fastest in warm, dry conditions (faster grape transpiration), and acidity falls fastest too.",
        "So the desired sugar and acid levels can be reached before aroma and tannin ripeness.",
        "Growers wait for aroma and tannin ripeness because these are harder to adjust in the winery than sugar or acid.",
        "In dry wine the grapes\u2019 own sugar is directly linked to alcohol, so extra sugar means extra alcohol."]
add(Checklist(_pts))
K.add("2.14", "Explain \u2014 any 3 of the 4 checklist points",
      [kp("Sugar and acid change fastest when warm and dry \u00b7 sugar and acid ripen before aroma and tannin \u00b7 "
          "growers wait for aroma and tannin, which are harder to fix \u00b7 the grapes\u2019 own sugar sets alcohol.")])

for f in K.flowables(CHAP, TITLE, ITEMS):
    add(f)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch2.pdf"
    n = build_pdf(out, CHAP, TITLE, story)
    print("Chapter 2 workbook: %d pages -> %s" % (n, out))
