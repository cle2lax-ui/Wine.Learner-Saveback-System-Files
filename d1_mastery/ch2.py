# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 2 — The Vine Growth Cycle"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Two: The Vine Growth Cycle",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 2.1 Dormancy \u2192 2.6 Other Changes in the Vine")

s.append(P("The most heavily examined chapter in the viticulture half of D1, and the one that "
           "rewards precision with numbers. Every later chapter \u2014 growing environment, canopy "
           "management, hazards, harvest \u2014 answers a problem defined here."))
s.append(P("The examiner's favourite constructions: <b>what the vine needs at stage X and what goes "
           "wrong without it</b>; <b>flowering and fruit set</b>, including coulure and "
           "millerandage; and <b>the four stages of grape development</b>, tracking sugar, acid, "
           "tannin, colour and aroma through each. Learn the temperature thresholds to the degree \u2014 "
           "the cheapest marks in the unit."))

# ---------------------------------------------------------------- overview
s.append(H2("1. The Cycle at a Glance"))
s.append(FIGURE("FIGURE 2.1 \u2014 THE VINE YEAR", CycleWheel([
    ("Dormancy", "Nov \u2013 Mar", "May \u2013 Sep"),
    ("Budburst", "Mar \u2013 Apr", "Sep \u2013 Oct"),
    ("Shoot & leaf growth", "Mar \u2013 Jun", "Sep \u2013 Dec"),
    ("Flowering & fruit set", "May \u2013 Jun", "Nov \u2013 Dec"),
    ("Grape development", "Jun \u2013 Sep", "Dec \u2013 Mar"),
    ("Harvest & leaf fall", "Aug \u2013 Nov", "Feb \u2013 May"),
])))
s.append(H4("WHAT THE VINE REQUIRES"))
s += BUL([
    "<b>Water, sunlight and warmth</b> \u2014 all required for <b>photosynthesis</b>.",
    "<b>Warmth</b> separately for <b>respiration</b>, releasing energy from sugar.",
    "<b>Nutrients</b> \u2014 cell structure and function, hence growth and reproduction.",
    "<b>Carbon dioxide</b> becomes the limiting factor once the rest are sufficient \u2014 but is "
    "<b>outside the grower's control</b>, so rarely the answer to a question.",
])

# ---------------------------------------------------------------- dormancy
s.append(H2("2. Dormancy"))
s.append(EXHIBIT("EXHIBIT 2.2 \u2014 DORMANCY: NEEDS AND THREATS", [
    ["Needs", "Adverse conditions"],
    ["Temperatures <b>below 10\u00b0C / 50\u00b0F</b> \u2014 too cold to grow, so the vine shuts down. "
     "Begins at leaf fall, ends at budburst. Without leaves it lives on <b>carbohydrate reserves, "
     "mostly starch</b>, stored in roots, trunk and branches",
     "<b>Extreme cold.</b> Below <b>\u221220\u00b0C / \u22124\u00b0F</b>, vines may be damaged or killed; "
     "below <b>\u221225\u00b0C / \u221213\u00b0F</b> most V. vinifera dies. Relevant to Canada, New York "
     "State, China.<br/><br/><b>Unusually mild spells.</b> A few warm winter days can trigger early "
     "budburst, exposing new growth to later frosts"],
], [W * 0.44, W * 0.56]))
s.append(P("Winter pruning happens now \u2014 and its <b>timing is itself a management lever</b>.",
           "note"))

# ---------------------------------------------------------------- budburst
s.append(H2("3. Budburst"))
s.append(P("Needs average air <b>and soil</b> temperatures above <b>10\u00b0C / 50\u00b0F</b>. Frost and "
           "cold soils are the threats. Four factors govern timing \u2014 name all four."))
s.append(FlowChart([
    ("AIR TEMPERATURE", "Compound buds burst as spring temperatures pass ~10\u00b0C / 50\u00b0F.",
     "<b>Continental</b>: sharp rise \u2192 <b>uniform</b> budburst \u2192 even ripening. "
     "<b>Maritime</b>: less contrast \u2192 <b>less synchronised</b>."),
    ("SOIL TEMPERATURE", "Warmer soil brings budburst forward.",
     "Free-draining sandy soils warm faster than clay-rich \u2014 an advantage in cool climates."),
    ("GRAPE VARIETY", "Each variety has its own threshold.",
     "<b>Early:</b> Chardonnay, Pinot Noir, Merlot, Grenache. <b>Late:</b> Sauvignon Blanc, "
     "Cabernet Sauvignon, Syrah \u2014 less at risk from spring frost."),
    ("HUMAN FACTORS", "Pruning date shifts budburst.",
     "<b>Late</b> winter pruning <b>postpones</b> budburst \u2014 used where spring frost is a known "
     "problem."),
], box_w=W * 0.40))
s.append(CALLOUT("THE TRAP INSIDE THIS SECTION", [
    P("Merlot buds slightly below 10\u00b0C, Ugni Blanc slightly above. But <b>time of budding is not "
      "linked to time of ripening</b>: <b>Grenache buds early and ripens late</b>.", "box"),
]))

# ---------------------------------------------------------------- shoot growth
s.append(H2("4. Shoot and Leaf Growth"))
s += BUL([
    "<b>Fastest shoot growth occurs between budburst and flowering</b>; most energy goes to shoots "
    "until flowering begins.",
    "Early growth is funded by <b>stored carbohydrates</b>; once leaves develop, photosynthesis "
    "takes over.",
    ("<b>Vigour</b> = vegetative growth (shoots, leaves, laterals). It depends on:", [
        "Natural resources \u2014 <b>temperature, water, nutrients</b>.",
        "<b>Planting material</b> \u2014 variety, clone, rootstock.",
        "<b>Disease</b> \u2014 viruses, for example, can lower vigour.",
    ]),
])
s.append(EXHIBIT("EXHIBIT 2.3 \u2014 CAUSES AND CONSEQUENCES OF POOR SHOOT GROWTH", [
    ["Cause", "Consequence"],
    ["<b>Low carbohydrate reserves</b>, from the <i>previous</i> season's excessive leaf removal, "
     "water stress, mildew infection or excessively high yields",
     "Initial shoot growth impaired before photosynthesis can take over"],
    ["<b>Water stress</b> at this stage",
     "Limits photosynthesis and shoot growth; nutrient uptake also impaired in very dry soils"],
    ["<b>Nutrient shortfall</b> \u2014 nitrogen, potassium, phosphorus",
     "Demand rises as the vine grows; shortfall stunts development"],
], [W * 0.5, W * 0.5]))
s.append(P("Stunted growth gives small weak shoots, fewer or smaller leaves, poorly flowering "
           "inflorescences and bunches that fail to ripen \u2014 <b>poor quality and low yield "
           "together</b>.", "note"))

# ---------------------------------------------------------------- flowering
s.append(H2("5. Flowering and Fruit Set"))
s.append(FlowChart([
    ("FLOWERING", "Flowers open, exposing pollen-laden stamens (anther and filament)", None),
    ("POLLINATION", "Pollen lands on the moistened stigma surface", None),
    ("GERMINATION", "Each grain produces a <b>pollen tube</b> penetrating stigma then ovule", None),
    ("FERTILISATION", "Sperm cells fertilise the eggs in the ovule", None),
    ("FRUIT SET", "Fertilised ovules form <b>up to four seeds</b>; the ovary wall enlarges to form "
     "<b>skin and pulp</b>", None),
], box_w=W * 0.78))
s.append(P("Cultivated vines are normally <b>self-pollinating</b>; <b>insects and wind make little "
           "contribution</b>.", "note"))
s.append(EXHIBIT("EXHIBIT 2.4 \u2014 THE THRESHOLDS THAT CARRY MARKS", [
    ["Process", "Requirement", "Failure"],
    ["Flowering", "Typically within <b>8 weeks of budburst</b>; temperature-dependent. Minimum "
     "<b>17\u00b0C / 63\u00b0F</b>",
     "At 17\u00b0C+ an inflorescence flowers within days. Low temperatures stretch it over weeks \u2192 "
     "<b>uneven ripening</b>"],
    ["Fruit set", "Pollen germination optimal <b>26\u201332\u00b0C / 79\u201390\u00b0F</b>",
     "Cold, rainy or windy conditions impair pollen tube growth \u2014 the key cool-climate yield "
     "loss. Hot, dry, windy conditions cause water stress, also cutting yields"],
    ["Conversion", "Typically <b>30%</b> of flowers become grapes (range <b>0\u201360%</b>)",
     "Not all flowers are meant to set. Only a substantial shortfall is a problem"],
    ["Bud fruitfulness<br/>(<i>next</i> year)", "Warmth above <b>25\u00b0C / 77\u00b0F</b>, sunlight on "
     "the compound buds, adequate water and nutrients",
     "Shading, temperatures under 25\u00b0C, water stress and nutrient deficiency all reduce next "
     "season's inflorescences"],
], [64, (W - 64) * 0.42, (W - 64) * 0.58], keep=False))
s.append(P("<b>Riesling</b> forms fruitful buds at relatively low temperatures \u2014 part of why it "
           "suits cool climates. Conditions now substantially influence <b>next year's</b> yield.",
           "note"))
s.append(EXHIBIT("EXHIBIT 2.5 \u2014 COULURE VERSUS MILLERANDAGE", [
    ["", "Coulure", "Millerandage"],
    ["Definition", "Fruit set <b>fails</b> for a high proportion of flowers \u2014 fertilisation "
     "unsuccessful, no grape develops",
     "A high proportion of <b>seedless</b> grapes within the bunch"],
    ["Cause", "An <b>imbalance in carbohydrate levels</b>", "Cold, wet, windy weather at fruit set"],
    ["Triggers", "Low photosynthesis from cold cloudy weather, or hot arid conditions under water "
     "stress; or vigorous shoot growth diverting carbohydrate from the inflorescence \u2014 fertile "
     "soils, heavy fertiliser, vigorous rootstocks", "\u2014"],
    ["Effect", "Some is normal; excessive coulure reduces yield dramatically",
     "Seedless grapes can ripen normally but are <b>smaller</b>, reducing volume. Some stay small, "
     "green and unripe \u2014 negative for quality"],
    ["Susceptible", "<b>Grenache, Cabernet Sauvignon, Merlot, Malbec</b>", "<b>Chardonnay, Merlot</b>"],
], [56, (W - 56) * 0.53, (W - 56) * 0.47], keep=False))

# ---------------------------------------------------------------- grape development
s.append(H2("6. Grape Development"))
s.append(P("The vine needs sunlight, warmth and <b>mild water stress</b>. Too much water and "
           "nutrients, excessive shading, and very cold or very hot conditions are adverse."))
s.append(FlowChart([
    ("STAGE 1 \u00b7 EARLY GRAPE GROWTH", "Hard green grapes enlarge. Acids and bitter tannins "
     "accumulate. Water arrives via the <b>xylem</b>", None),
    ("STAGE 2 \u00b7 V\u00c9RAISON", "Growth pauses (lag phase). Chlorophyll breaks down; anthocyanins "
     "synthesised in black varieties", None),
    ("STAGE 3 \u00b7 RIPENING", "Cells expand. Sugar and water accumulate via the <b>phloem</b>; acid "
     "falls; tannin, colour and aroma develop", None),
    ("STAGE 4 \u00b7 EXTRA-RIPENING", "Grapes shrivel. <b>No phloem import</b>; transpiration "
     "concentrates existing sugars", None),
], box_w=W * 0.80))

s.append(H4("STAGE 1 \u2014 EARLY GRAPE GROWTH"))
s += BUL([
    "<b>Tartaric and malic acids accumulate</b>; sugar stays low throughout.",
    "Aroma compounds and precursors form, including <b>methoxypyrazines</b> \u2014 herbaceous "
    "character in Sauvignon Blanc, Cabernet Sauvignon, Cabernet Franc.",
    "<b>Tannins accumulate, very bitter.</b> Sunshine promotes tannin accumulation.",
    ("Water and nitrogen management shapes the whole ripening period:", [
        "<b>Too much water and nitrogen prolongs this stage</b>, favouring shoot growth over "
        "ripening \u2014 delaying ripening, possibly past the point the weather allows.",
        "<b>Mild water stress speeds it up</b>: smaller grapes, lower juice yield, greater "
        "<b>skin-to-pulp ratio</b> \u2014 in reds, better colour, tannin and aroma.",
    ]),
])
s.append(H4("STAGE 2 \u2014 V\u00c9RAISON"))
s.append(P("Growth slows for a few days \u2014 the <b>lag phase</b>. Cell walls become supple, skin "
           "chlorophyll breaks down, and black varieties colour as <b>anthocyanins</b> are "
           "synthesised.", "note"))
s.append(H4("STAGE 3 \u2014 RIPENING"))
s.append(EXHIBIT("EXHIBIT 2.6 \u2014 WHAT EACH COMPONENT DOES DURING RIPENING", [
    ["Component", "Behaviour and the numbers that matter"],
    ["Sugar", "Rapid at first, slowing later. Photosynthesis optimal <b>18\u201333\u00b0C (64\u201391\u00b0F)</b> "
     "and above <b>one third of full sunshine</b>. Transported by <b>phloem</b>; uptake correlates "
     "with grape transpiration, so faster in warm dry than cool humid conditions. Extreme water "
     "stress <b>stops</b> photosynthesis"],
    ["Tartaric acid", "Total amount generally unchanged; concentration <b>falls by dilution</b>"],
    ["Malic acid", "Falls <b>further</b> \u2014 it is <b>metabolised in respiration</b>. Respiration "
     "is slower when cool, hence cool-climate acidity"],
    ["Acid thresholds", "Mean above <b>21\u00b0C (70\u00b0F)</b> in the final month \u2192 rapid acid loss, "
     "rising pH. Below <b>15\u00b0C (59\u00b0F)</b> \u2192 must acidity may be too high. Cool nights preserve "
     "malic acid \u2014 <b>Central Otago, Washington State</b>"],
    ["Methoxypyrazines", "<b>Fall.</b> Cool temperatures and limited sunlight hinder that decrease, "
     "leaving markedly herbaceous wines"],
    ["Other aromas", "Increase \u2014 <b>terpenes</b>, giving floral and citrus character, e.g. the "
     "grapey aroma of Muscat"],
    ["Tannins", "High at v\u00e9raison, decreasing slightly. They <b>polymerise</b>, becoming less "
     "bitter. Sunshine promotes accumulation pre-v\u00e9raison and polymerisation after"],
    ["Anthocyanins", "Increase, most rapidly with plentiful sunlight at <b>15\u201325\u00b0C (59\u201377\u00b0F)</b>"],
], [76, W - 76], keep=False))
s.append(P("Warmer, sunnier climates give riper-seeming aromas \u2014 <b>Chardonnay</b> shows green and "
           "citrus fruit when cool, stone and tropical when warm. The textbook is careful not to "
           "overclaim the link to individual aroma compounds. Say so.", "note"))
s.append(H4("WHAT DETERMINES THE LENGTH OF RIPENING"))
s += BUL([
    "<b>Variety</b> \u2014 early: Chardonnay, Pinot Noir. Late: Cabernet Sauvignon, Grenache. "
    "<b>Zinfandel</b> ripens <b>unevenly</b>.",
    "<b>Climate</b> \u2014 quickest when warm and dry, but very hot or dry shuts the vine down.",
    "<b>Vineyard management</b> \u2014 high yields, canopy shading and still-growing shoots all slow it.",
    "<b>Time of harvest</b> \u2014 human (style, logistics) or natural (rain, disease onset).",
])
s.append(H4("STAGE 4 \u2014 EXTRA-RIPENING"))
s.append(P("Grapes shrivel; no further phloem import. Transpiration concentrates existing sugars "
           "and extra-ripe aromas develop. Most likely in hot, sunny, dry climates; <b>Syrah is "
           "particularly susceptible</b>. Weather and disease pressure decide whether it is an "
           "option at all.", "note"))

# ---------------------------------------------------------------- closing cycle
s.append(H2("7. Closing the Cycle"))
s.append(P("Late summer: shoots <b>lignify</b>, becoming <b>canes</b>. Autumn: leaves fall and "
           "<b>carbohydrate reserves are laid down</b> in roots, trunk and branches, carrying next "
           "spring's growth into dormancy.", "note"))

# ---------------------------------------------------------------- ripeness
s.append(H2("8. Defining Ripeness"))
s.append(EXHIBIT("EXHIBIT 2.7 \u2014 THE FOUR PARAMETERS", [
    ["Parameter", "Why it decides the picking date"],
    ["Sugar", "In dry wines, directly linked to finished alcohol; in sweet wines, to both "
     "sweetness and alcohol"],
    ["Acidity", "Significant impact on taste. High acidity particularly wanted in <b>sparkling and "
     "sweet</b> wines"],
    ["Aromas and flavours", "Highly individual to producer and style. Broadly: underripe and "
     "herbaceous \u2192 fresh fruit \u2192 riper fruit \u2192 jammy or cooked"],
    ["Tannin ripeness", "Essential in reds. Tannins accumulate bitter, then polymerise and soften. "
     "Residual sugar makes tannins seem softer; bone dry high acid wines make them seem more "
     "astringent"],
], [78, W - 78]))
s.append(CALLOUT("THE ANALYTICAL POINT THIS SECTION EXISTS TO MAKE", [
    P("The four parameters <b>do not move together</b>. Sugar accumulates fastest in warm, dry "
      "climates; acidity falls fastest in exactly those conditions. Aroma and tannin ripeness "
      "follow neither pattern reliably.", "box"),
    P("So in warm climates sugar and acidity often reach target <b>before</b> aromas and tannins "
      "are ripe. Growers wait \u2014 hence the higher alcohol of warm-climate wines.", "box"),
    P("The decisive judgement: it is <b>easier to adjust sugar, alcohol or acid in the winery than "
      "to work with unripe tannins and aromas</b>. If you write one sentence of analysis in a "
      "ripeness question, write that one.", "box"),
]))

# ---------------------------------------------------------------- numbers
s.append(H2("9. The Numbers, Consolidated"))
s.append(FIGURE("FIGURE 2.4 \u2014 THE TEMPERATURE THRESHOLDS ON ONE SCALE", ThresholdScale(
    -30, 40,
    bands=[(-30, -25, "", colors.HexColor("#3E5C7A")),
           (-25, -20, "KILL", colors.HexColor("#5B7FA6")),
           (-20, 10, "DORMANT \u2014 NO GROWTH", COOL),
           (10, 17, "GROWTH", MILD),
           (17, 25, "FLOWERING", LEAF),
           (25, 33, "FRUIT SET \u00b7 PHOTOSYNTHESIS", WARM),
           (33, 40, "SHUTDOWN", HOT)],
    marks=[(-25, "\u221225\u00b0C kills vinifera"), (-20, "\u221220\u00b0C damage"),
           (10, "10\u00b0C budburst"), (15, "15\u00b0C acid floor"),
           (17, "17\u00b0C flowering"), (21, "21\u00b0C acid loss"),
           (25, "25\u00b0C bud fruitfulness"), (33, "33\u00b0C photosynthesis ceiling")])))
s.append(FIGURE("FIGURE 2.5 \u2014 THE OPTIMUM WINDOWS DO NOT COINCIDE", RangeCompare(
    10, 40, [
        (15, 25, "Anthocyanins", colors.HexColor("#7E3B57")),
        (18, 33, "Photosynthesis", MILD),
        (26, 32, "Pollen germination", WARM),
        (17, 40, "Flowering (min)", LEAF),
    ], ticks=[10, 15, 20, 25, 30, 35, 40]),
    note="Colour develops in a <b>cooler, narrower</b> band than photosynthesis \u2014 which is why "
         "very hot sites can accumulate sugar faster than they develop colour."))
s.append(EXHIBIT("EXHIBIT 2.7 \u2014 THE NON-TEMPERATURE NUMBERS", [
    ["Figure", "Significance"],
    ["<b>One third of full sunshine</b>", "Below this, light limits photosynthesis"],
    ["<b>8 weeks</b>", "Typical budburst to flowering interval"],
    ["<b>30% (range 0\u201360%)</b>", "Proportion of flowers becoming grapes"],
    ["<b>Up to 4</b>", "Seeds per grape, from fertilised ovules"],
], [116, W - 116]))

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER TWO", [
    P("<b>1. Answer across seasons.</b> Conditions at flowering set <i>next</i> year's bud "
      "fruitfulness; this autumn's carbohydrate reserves fund <i>next</i> spring's growth. See the "
      "cycle as a loop, not a line.", "box"),
    P("<b>2. Name the transport tissue.</b> <b>Xylem</b> in early growth \u00b7 <b>phloem</b> in "
      "ripening \u00b7 <b>neither</b> in extra-ripening. Three sentences, three marks, almost nobody "
      "writes them.", "box"),
    P("<b>3. Distinguish dilution from metabolism.</b> Tartaric falls by <b>dilution</b>; malic is "
      "<b>respired</b>, and respiration is temperature-dependent. That one distinction explains "
      "cool-climate acidity and diurnal range together.", "box"),
    P("<b>4. Treat water stress as double-edged.</b> Mild stress before v\u00e9raison checks vegetative "
      "growth and raises skin-to-pulp ratio; severe stress closes stomata and halts ripening. "
      "State which you mean.", "box"),
    P("<b>5. Concede the complexity on aroma.</b> The textbook declines to draw firm links between "
      "ripening conditions and individual aroma compounds. Acknowledging that, then offering "
      "Chardonnay across climates, reads as informed rather than merely confident.", "box"),
]))

s.append(exam_traps([
 ("Treating early budding as early ripening.",
  "They are independent. <b>Grenache buds early and ripens late.</b> Early budding: Chardonnay, "
  "Pinot Noir, Merlot, Grenache. Early ripening: Chardonnay, Pinot Noir. Late ripening: Cabernet "
  "Sauvignon, Grenache."),
 ("Confusing coulure with millerandage.",
  "Coulure = fruit set <i>fails</i>, no grape forms, caused by <b>carbohydrate imbalance</b>. "
  "Millerandage = grapes form but are <b>seedless and small</b>, caused by cold, wet, windy "
  "weather at fruit set. Merlot is susceptible to both, which is why they get muddled."),
 ("Saying acidity falls during ripening without saying how.",
  "Tartaric falls by <b>dilution</b>; malic falls further because it is <b>respired</b>. "
  "Undifferentiated answers lose the marks that separate the grades."),
 ("Claiming warm conditions always speed ripening.",
  "Up to a point. Very hot or dry conditions cause water stress, the stomata close, "
  "photosynthesis slows or stops, and ripening <i>halts</i>. The relationship is not linear."),
 ("Reciting the 30% fruit set figure as though a shortfall is always a fault.",
  "Typically 30% of flowers become grapes, ranging from <b>0 to 60%</b>. Not all flowers are "
  "meant to set, and <i>some</i> coulure is normal. Only excessive failure is a problem."),
]))

# ---------------------------------------------------------------- exam
exam = []

MCQ = [
 dict(q="Average air temperatures below which figure are too cold for the vine to grow?",
      opts=["5\u00b0C / 41\u00b0F", "10\u00b0C / 50\u00b0F", "15\u00b0C / 59\u00b0F", "17\u00b0C / 63\u00b0F"],
      ans=1, why="10\u00b0C / 50\u00b0F is the growth threshold \u2014 also what triggers budburst in "
                 "spring. 17\u00b0C is the flowering minimum."),
 dict(q="Most Vitis vinifera will be killed by winter temperatures below:",
      opts=["\u221210\u00b0C / 14\u00b0F", "\u221215\u00b0C / 5\u00b0F", "\u221220\u00b0C / \u22124\u00b0F", "\u221225\u00b0C / \u221213\u00b0F"],
      ans=3, why="Below \u221220\u00b0C vines may be damaged or killed; below \u221225\u00b0C most "
                 "V. vinifera dies. The question asks for the kill threshold."),
 dict(q="Which group of varieties is correctly identified as late budding?",
      opts=["Chardonnay, Pinot Noir, Merlot", "Sauvignon Blanc, Cabernet Sauvignon, Syrah",
            "Grenache, Merlot, Chardonnay", "Riesling, Pinot Noir, Grenache"],
      ans=1, why="Late budding needs higher temperatures, so less spring frost risk. The others "
                 "listed are early budding."),
 dict(q="Coulure is caused principally by:",
      opts=["Cold, wet, windy weather at fruit set",
            "An imbalance in carbohydrate levels",
            "Boron deficiency in the soil",
            "Excessive shading of the compound buds"],
      ans=1, why="Carbohydrate imbalance is the cause \u2014 from low photosynthesis, or vigorous "
                 "shoot growth diverting carbohydrate from the inflorescence. Option A describes "
                 "millerandage."),
 dict(q="Optimum temperatures for pollen germination at fruit set are:",
      opts=["17\u201320\u00b0C / 63\u201368\u00b0F", "20\u201325\u00b0C / 68\u201377\u00b0F",
            "26\u201332\u00b0C / 79\u201390\u00b0F", "33\u201338\u00b0C / 91\u2013100\u00b0F"],
      ans=2, why="17\u00b0C is the flowering minimum, not the fruit set optimum. Pollen germination "
                 "is optimal at 26\u201332\u00b0C."),
 dict(q="During ripening, the concentration of tartaric acid in the grape falls mainly because:",
      opts=["It is metabolised in respiration",
            "It is diluted as sugar and water accumulate",
            "It is converted to malic acid",
            "It migrates from the pulp into the skin"],
      ans=1, why="Tartaric acid's total amount is roughly unchanged; concentration falls by "
                 "dilution. Malic acid is the one metabolised in respiration, so it falls "
                 "further."),
 dict(q="Anthocyanin synthesis proceeds most rapidly at temperatures of approximately:",
      opts=["10\u201315\u00b0C / 50\u201359\u00b0F", "15\u201325\u00b0C / 59\u201377\u00b0F",
            "18\u201333\u00b0C / 64\u201391\u00b0F", "26\u201332\u00b0C / 79\u201390\u00b0F"],
      ans=1, why="15\u201325\u00b0C with plentiful sunlight. 18\u201333\u00b0C is the photosynthesis optimum \u2014 a "
                 "deliberately tempting distractor."),
 dict(q="In the extra-ripening stage, sugar concentration in the grape rises because:",
      opts=["The phloem continues to deliver sugar solution at an increased rate",
            "Photosynthesis accelerates in the warmer late-season conditions",
            "Water is lost through grape transpiration while phloem import has ceased",
            "Malic acid is converted into fermentable sugar"],
      ans=2, why="No further sugar or water is imported at this stage \u2014 concentration is purely "
                 "transpirational water loss, and the grape shrivels."),
 dict(q="Bud fruitfulness for the following season is reduced by all of the following EXCEPT:",
      opts=["Shading of the compound buds", "Temperatures below 25\u00b0C / 77\u00b0F",
            "Water stress", "Winter pruning carried out late in the dormant period"],
      ans=3, why="Late winter pruning postpones budburst \u2014 a frost-avoidance technique. It is not "
                 "a determinant of bud fruitfulness. The other three are."),
 dict(q="A mean temperature above 21\u00b0C / 70\u00b0F during the final month of ripening tends to produce:",
      opts=["Rapid loss of acidity and a rise in pH",
            "Retention of acidity to a point where the must is too tart",
            "A marked increase in methoxypyrazine concentration",
            "Cessation of anthocyanin synthesis"],
      ans=0, why="Above 21\u00b0C, acidity is lost rapidly and pH rises. Below 15\u00b0C, acid loss is "
                 "so reduced that must acidity can be too high."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) Conditions required for successful flowering and fruit set"),
 P("Flowering and fruit set together determine the current season's yield, and the conditions "
   "required for each are distinct."),
 P("Flowering typically occurs within eight weeks of budburst, though warmth brings it forward. "
   "Success needs a minimum of 17\u00b0C (63\u00b0F): at or above that, an inflorescence flowers within a "
   "few days; below it, flowering drags on over weeks. The consequence is more than delay \u2014 "
   "flowers opening at widely separated times leave the resulting grapes at different "
   "developmental stages, so the bunch ripens unevenly. That unevenness persists to harvest, "
   "forcing the producer to accept underripe fruit or sort at a cost."),
 P("Fruit set needs more heat: pollen germination is optimal between 26 and 32\u00b0C (79\u201390\u00b0F). "
   "The vine is normally self-pollinating, with insects and wind contributing little, so success "
   "depends on the pollen tube growing from stigma to ovule. That growth is impaired by cold, "
   "rainy or windy conditions \u2014 the key cause of poor cool-climate yields \u2014 and equally by hot, "
   "dry, windy conditions causing water stress. A complete answer names both failure modes, not "
   "just cold."),
 P("Around 30 per cent of flowers become grapes, though the range runs zero to 60 per cent. Not "
   "all flowers are meant to set; only a substantial shortfall is a real problem."),
 P("This stage also sets <i>next</i> season's potential. Compound buds forming now become next "
   "year's shoots, and their fruitfulness \u2014 how many inflorescences they develop \u2014 depends on "
   "conditions now: shading, temperatures below 25\u00b0C (77\u00b0F), water stress and nutrient "
   "deficiency all reduce it. Since each inflorescence becomes a bunch, poor conditions depress "
   "yield across two vintages. Riesling forms fruitful buds at relatively low temperatures, part "
   "of why it suits cool climates."),

 answer_head("Part b) Coulure and millerandage"),
 P("Both are disorders of fruit set, and both reduce yield, but their mechanisms, causes and "
   "consequences differ."),
 P("<b>Coulure</b> is fruit set failing for a high proportion of flowers: fertilisation is "
   "unsuccessful and no grape develops. Its cause is a carbohydrate imbalance, arising from low "
   "photosynthesis \u2014 cold cloudy conditions, or hot arid conditions where the vine closes its "
   "stomata to retain water \u2014 or from vigorous shoot growth diverting carbohydrate from the "
   "inflorescence, driven by fertile soils, heavy fertiliser or vigorous rootstocks. That second "
   "pathway matters because it sits under the grower's control: site, rootstock and restrained "
   "fertilising are genuine preventatives. Some coulure is normal; excessive coulure cuts yield "
   "dramatically. Grenache, Cabernet Sauvignon, Merlot and Malbec are notably susceptible."),
 P("<b>Millerandage</b> is a high proportion of seedless grapes in the bunch, from cold, wet, "
   "windy weather at fruit set \u2014 Chardonnay and Merlot are particularly susceptible. Its yield "
   "effect is subtler: grapes do form, and seedless ones ripen normally, but are smaller, "
   "reducing volume. The quality effect is less predictable \u2014 some seedless berries stay small, "
   "green and unripe, contributing that character to the must if harvested with the rest."),
 P("Coulure is fundamentally a vine-balance problem, provoked by either climatic extreme or the "
   "grower's own decisions; millerandage is essentially a weather event at one moment. That "
   "difference decides what, if anything, can be done about each."),
 examiner_note([
   P("The answer separates flowering from fruit set with its own threshold for each, rather than "
     "blurring them into 'warm weather is needed', and names both the cold and hot failure "
     "pathways at fruit set, where weaker answers name only cold.", "box"),
   P("It treats the 30 per cent figure correctly \u2014 a normal conversion rate, not a deficiency \u2014 "
     "and carries the argument into next season via bud fruitfulness. Part b) closes by "
     "classifying the two disorders by <i>type</i> of cause, which decides whether the grower can "
     "act. That is evaluation, not description.", "box"),
 ]),
]

q2 = [
 answer_head("Part a) The four stages of grape development"),
 P("Grape development divides into four stages, and each grape component behaves differently "
   "across them."),
 P("<b>Stage one, early grape growth</b>, begins soon after fruit set. Hard green grapes enlarge "
   "as tartaric and malic acids accumulate. Aroma compounds form, including methoxypyrazines, "
   "giving herbaceous character to Sauvignon Blanc, Cabernet Sauvignon and Cabernet Franc. "
   "Tannins accumulate, very bitter, promoted by sunshine on the grapes; sugar stays low "
   "throughout. Water arrives mainly via the xylem. The grower's water and nitrogen choices "
   "matter here: too much of either prolongs the stage, favouring shoot growth over ripening and "
   "risking too little time before autumn. Mild water stress does the opposite \u2014 smaller "
   "grapes, less juice, but a greater skin-to-pulp ratio, which in reds means higher colour, "
   "tannin, aroma and quality."),
 P("<b>Stage two, v\u00e9raison</b>, is brief \u2014 growth slows for a few days, the lag phase. Cell "
   "walls turn supple, skin chlorophyll breaks down, and black varieties begin colouring as "
   "anthocyanins are synthesised."),
 P("<b>Stage three, ripening</b>, most determines final quality, and shoot growth should have "
   "slowed substantially by now. Cells expand rapidly; sugar and water accumulate as acid falls, "
   "and tannin, colour and aroma develop. The transport route changes: xylem flow slows and a "
   "sugar solution arrives instead via the phloem, uptake tracking grape transpiration and so "
   "faster in warm dry conditions than cool humid ones. Sugar accumulates fast at first, then "
   "slows. Tartaric acid falls by dilution, its total amount roughly unchanged; malic falls "
   "further, since it is metabolised in respiration. Tannins polymerise and soften, aided by "
   "sunshine; anthocyanins increase; methoxypyrazines fall while terpenes and other floral/citrus "
   "compounds increase."),
 P("<b>Stage four, extra-ripening</b>, occurs only if grapes stay on the vine. They shrivel: no "
   "further phloem import, so transpiration concentrates existing sugars and extra-ripe aromas "
   "develop \u2014 desirable in some styles, not others. Most likely in hot, sunny, dry climates; "
   "Syrah is particularly susceptible. Weather and disease pressure decide whether it is even an "
   "option."),

 answer_head("Part b) The influence of ripening temperature on grape composition"),
 P("Temperature acts on each grape component differently during ripening, and that divergence, "
   "not any single effect, shapes the harvest decision."),
 P("Sugar accumulation depends on photosynthesis, at maximum rate between 18 and 33\u00b0C "
   "(64\u201391\u00b0F) given light above one third of full sunshine. Warmth also raises grape "
   "transpiration, driving the sugar solution from phloem into berry \u2014 so warm, dry conditions "
   "accumulate sugar fastest. The relationship is not linear: very hot, dry conditions cause "
   "water stress, closing the stomata, blocking CO\u2082 entry, and slowing or stopping "
   "photosynthesis. Beyond a point, more heat means less ripening."),
 P("Acidity moves the other way, by two mechanisms. Tartaric acid falls through dilution as "
   "sugar and water accumulate, its total amount roughly constant; malic falls further, "
   "metabolised in respiration, which is temperature-dependent \u2014 slower when cool, why cooler "
   "climates retain higher natural acidity. Two thresholds matter: a mean above 21\u00b0C (70\u00b0F) in "
   "the final month causes rapid acid loss and rising pH; below 15\u00b0C (59\u00b0F), acid loss is so "
   "restricted that must acidity may be excessive. Night temperature is a separate lever \u2014 cool "
   "nights specifically slow malic respiration, why high-diurnal-range regions like Central "
   "Otago and Washington State retain acidity despite warm days."),
 P("Colour and tannin follow their own optima. Anthocyanin synthesis is fastest with plentiful "
   "sunlight at 15\u201325\u00b0C (59\u201377\u00b0F) \u2014 narrower and cooler than the photosynthetic optimum, "
   "which is why very hot sites accumulate sugar faster than colour. Tannins, high at v\u00e9raison, "
   "decrease slightly and polymerise through ripening, softening, aided by sunshine."),
 P("Aroma is least tractable. Methoxypyrazines fall during ripening, but cool temperatures and "
   "limited sunlight slow that fall, leaving herbaceous wines; terpenes and other compounds "
   "increase. Beyond this the textbook stays cautious: the range of aroma compounds is huge and "
   "temperature affects each differently. What holds is the broad pattern \u2014 Chardonnay shows "
   "green and citrus fruit when cool, stone and tropical fruit when warm."),
 P("In practice, warm climates often reach desired sugar and acidity before aromas and tannins "
   "ripen. Since sugar, alcohol and acid are easier to adjust in the winery than unripe tannins "
   "and aromas, growers wait for phenolic and aromatic ripeness and correct the rest afterward \u2014 "
   "the direct cause of higher alcohol in warm-climate wines."),
 examiner_note([
   P("Part a) names the transport tissue at each stage \u2014 xylem in early growth, phloem in "
     "ripening, neither in extra-ripening \u2014 which most candidates omit, and treats stage one as "
     "a grower decision point, not passive description.", "box"),
   P("Part b) is organised by component, not temperature band, showing the optima diverge. It "
     "separates dilution from respiration for the two acids, day from night temperature, and "
     "closes on the harvest-timing consequence. Admitting the aroma relationship isn't firmly "
     "established reads as command of the material, not hedging.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="Flowering and fruit set determine both the current season's yield and the next.",
      parts=[("Explain the conditions required for successful flowering and fruit set, and the "
              "consequences when they are not met.", "15%"),
             ("Explain what is meant by coulure and millerandage, identifying the causes of each "
              "and their effects on yield and quality.", "10%")],
      answer=q1),
 dict(stem="The composition of the grape at harvest is the product of its development.",
      parts=[("Describe the four stages of grape development, explaining the changes that occur "
              "in each.", "15%"),
             ("Explain how temperature during ripening influences the composition of the grape "
              "at harvest.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch2_The_Vine_Growth_Cycle.pdf",
      "Chapter Two \u00b7 The Vine Growth Cycle", s, exam, maxpages=19)
