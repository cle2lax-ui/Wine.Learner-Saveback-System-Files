# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 9 — Harvest"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Nine: Harvest",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 9.1 Choosing the Date of Harvest \u00b7 9.2 "
        "Harvesting Options")

s.append(P("Harvest closes every decision made in Chapters Two through Eight: ripeness "
           "measurement translates the vine's biology into a picking date, and the "
           "machine-versus-hand choice is where cost, quality intent and site constraint "
           "finally meet. Both are compare-and-evaluate territory, not recall."))
s.append(P("Reliably examined: <b>what growers actually measure</b> to set the harvest date, "
           "and why tasting still matters alongside instruments; <b>machine versus hand "
           "harvesting</b>, argued from advantages and disadvantages, not preference; and the "
           "narrower case of <b>when hand-harvesting is required</b>, not merely preferred."))

# ================================================================ choosing the date
s.append(H2("1. Choosing the Date of Harvest"))
s.append(P("The old rule of thumb \u2014 grapes ripen <b>100 days after flowering begins</b> \u2014 "
           "has been overtaken by direct measurement, historically via <b>potential alcohol</b> "
           "(the alcohol fermenting all the must's sugar would yield). French AOC minimums "
           "illustrate the principle: <b>Petit Chablis 9.5%</b>, <b>Chablis 10%</b>, "
           "<b>Bourgogne Blanc 10.5%</b> potential alcohol \u2014 adjustable upward within "
           "limits by chaptalisation.", "note"))
s += BUL([
    "The context has shifted: a <b>generally warmer climate</b> eases ripening in cool "
    "regions; <b>better viticulture</b> ripens grapes more reliably; and <b>aroma and tannin "
    "ripeness</b> is now often weighted above optimum sugar ripeness alone.",
    "<b>Rain risk near harvest overrides other considerations.</b> A forecast of rain forces "
    "a choice: pick underripe now, or wait and risk it. Late rain dilutes juice or, worse, "
    "splits skins as grapes swell rapidly \u2014 opening the door to grey rot and possible loss "
    "of the crop.",
])
s.append(EXHIBIT("EXHIBIT 9.1 \u2014 WHAT GROWERS MEASURE", [
    ["Component", "Tool", "Note"],
    ["<b>Sugar</b>", "Handheld <b>refractometer</b>", "Most dry still wine is picked "
     "<b>19\u201325\u00b0 Brix</b>, converting to roughly <b>11\u201315% abv</b>"],
    ["<b>Acidity</b>", "<b>Titration</b> (acid level); a <b>pH meter</b> (pH directly)",
     "Titration adds a known-reacting substance in measured amounts to find concentration"],
    ["<b>Aroma and tannin ripeness</b>", "Usually <b>taste</b>, with experience", "No "
     "reliable instrument substitute yet in routine use"],
    ["Multiple compounds at once", "Visible/near-infrared <b>spectroscopy</b> (emerging)",
     "Gives sugar, acidity and other readings together \u2014 but <b>tasting the grapes "
     "remains one of the most important methods</b>, instruments or not"],
], [128, 92, W - 128 - 92], keep=False))
s.append(FIGURE("FIGURE 9.1 \u2014 THE SUGAR-RIPENESS WINDOW FOR DRY STILL WINE",
    ThresholdScale(10, 30,
        bands=[(10, 19, "BELOW TYPICAL RANGE", COOL), (19, 25, "DRY STILL WINE \u2014 "
                "19\u201325\u00b0 BRIX", MILD), (25, 30, "ABOVE TYPICAL RANGE", WARM)],
        marks=[(19, "19\u00b0 \u2014 \u224811% ABV"), (25, "25\u00b0 \u2014 \u224815% ABV")],
        unit="\u00b0 Brix"),
    note="Converts to roughly 11\u201315% potential alcohol \u2014 the range most dry still "
         "wine is picked within, before any adjustment in the winery."))
s.append(H3("Harvest Date by Wine Style"))
s.append(FIGURE("FIGURE 9.1b \u2014 LOIRE CHENIN BLANC: ONE VARIETY, ONE 4\u20136 WEEK WINDOW",
    Timeline(0, 6, [
        (1, "Sparkling", "Picked earliest"),
        (3, "Dry / off-dry", "Mid-harvest"),
        (5.5, "Botrytis / late-harvest", "Picked last"),
    ], axis_label="", unit=" wk")))
s += BUL([
    "<b>California Zinfandel</b>: <b>early\u2013mid August</b> for White Zinfandel, "
    "<b>September</b> for red. Prone to <b>uneven ripeness within a bunch</b>, so quality "
    "needs careful selection, and hot-area growers must decide whether to include shrivelled "
    "grapes.",
    "<b>Residual-sugar wines</b> often harvest <b>late</b> to concentrate sugar. Botrytised "
    "wines typically need <b>hand-harvesting over several passes</b> to select only affected "
    "bunches. <b>Icewine/Eiswein</b> requires a specific cold threshold \u2014 below "
    "<b>\u22128\u00b0C / 18\u00b0F</b> for Canadian Icewine.",
    "<b>Extended \u2018hang time\u2019</b> is genuinely contested: critics link it to "
    "high-alcohol, low-acid, extra-ripe wines lacking balance; some growers respond that "
    "critics score them well and consumers like the style.",
])

# ================================================================ harvesting options
s.append(H2("2. Harvesting Options"))
s.append(P("\u2018Hand-picked\u2019 still signals quality in wine marketing, but the real "
           "decision is more complex than a quality proxy \u2014 it weighs wine style, "
           "logistics, legislation and cost together.", "note"))
s.append(EXHIBIT("EXHIBIT 9.2 \u2014 MACHINE VERSUS HAND HARVESTING", [
    ["", "Machine", "Hand"],
    ["Default for", "Inexpensive to mid-priced wine, large scale \u2014 especially where the "
     "vineyard was <b>designed for it</b> (even row spacing, end-row turning space, flat or "
     "gently graded land). Exception: South Africa, cheap available labour keeps hand-"
     "harvesting standard", "Premium wine; small vineyards; anywhere machine access fails"],
    ["Advantages", "<b>Far faster and cheaper</b> at scale \u2014 California studies put it "
     "at roughly <b>one-third</b> the cost of hand-harvesting. Avoids casual-labour "
     "availability/reliability risk. Can pick at <b>night</b>, up to 15\u00b0C / 59\u00b0F "
     "cooler \u2014 less microbial spoilage and oxidation, fresher aromatics in fruity whites, "
     "lower refrigeration cost. Timing is flexible: wait for exact ripeness, then move fast",
     "<b>Bunch-by-bunch selectivity</b> \u2014 removes diseased, under- or extra-ripe fruit at "
     "the point of picking. Handles <b>steep slopes, irregular rows, mixed plantings</b>. "
     "Small stackable crates (max 10\u201315 kg) avoid crushing \u2014 no premature juice "
     "release, so less oxidation/spoilage risk"],
    ["Disadvantages", "<b>Less gentle</b> \u2014 grapes shake off the stem, skins can rupture "
     "and release juice, so unsuited to whole-bunch styles or delicate whites avoiding "
     "oxidation/phenolic extraction. Not cost-effective for small vineyards. Struggles with "
     "mixed varieties ripening at different times in one plot, steep slopes or limited "
     "access. Quality depends on operator skill. Rental competition at peak timing; "
     "purchase is a major investment", "More expensive at medium\u2013large scale. Needs a "
     "<b>reliable, trained, supervised</b> workforce. Usually daylight work, so more heat "
     "exposure risk (some producers hand-harvest at night with torches to offset this)"],
], [76, (W - 76) * 0.5, (W - 76) * 0.5], keep=False))
s.append(P("<b>Quality improvement without switching to hand-harvest:</b> hand-select fruit "
           "before machine picking; use gentler <b>bow-rod shaking</b> machines (versus older "
           "beater types) for more selective removal; invest in machines with optical sorting "
           "and in-machine SO\u2082 dosing for white grapes; and sort rigorously on arrival, "
           "removing MOG (matter other than grapes), unripe and rotten fruit.", "note"))
s.append(P("Rising labour cost and scarcity are pushing <b>some premium producers toward "
           "machine harvesting</b>; conversely some inexpensive, high-volume wine is hand- or "
           "part-hand-harvested, as when cooperatives in France or Italy pool fruit from many "
           "small growers.", "note"))
s.append(H3("When Hand-Harvesting Is Required, Not Merely Preferred"))
s.append(FIGURE("FIGURE 9.1a \u2014 IS HAND-HARVESTING ACTUALLY REQUIRED?", DecisionTree(
    "Does the wine style need whole, intact bunches, or is picking selective by grape "
    "condition?",
    [("YES", "Hand-harvest required \u2014 whole-bunch sparkling/carbonic maceration, or "
      "selective picks like botrytised TBA"),
     ("NO", ("Is the site steep/uneven, or are the vines untrellised (bush vines)?",
             [("YES", "Hand-harvest required \u2014 no trellis or terrain a machine can "
               "work"),
              ("NO", "Either works \u2014 machine for cost/speed, hand for extra "
               "selectivity")]))])))
s += BUL([
    "<b>Whole-bunch styles</b> \u2014 premium sparkling wine needing whole bunches for whole-"
    "bunch pressing (Champagne, most bottle-fermented sparkling); carbonic or semi-carbonic "
    "maceration (Beaujolais and similar), which needs intact whole bunches.",
    "<b>Selective harvesting</b> \u2014 picking only specific grapes, such as botrytis-"
    "affected bunches for Trockenbeerenauslese Riesling in the Mosel, is only possible by "
    "hand.",
    "<b>Steep or uneven sites</b> \u2014 the Douro Valley and similar terrain.",
    "<b>Bush vines</b> \u2014 with no trellis to shake against, machine harvesting would "
    "damage both vine and fruit.",
])

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER NINE", [
    P("<b>1. Separate \u2018required\u2019 from \u2018preferred\u2019.</b> Premium wine often "
      "<i>chooses</i> hand-harvesting for quality; whole-bunch styles, selective picking, "
      "steep slopes and bush vines <i>require</i> it \u2014 the distinction is examinable on "
      "its own.", "box"),
    P("<b>2. Instruments inform, tasting decides.</b> Even with spectroscopy giving multiple "
      "readings at once, the textbook is explicit that tasting the grapes remains among the "
      "most important methods \u2014 don't present measurement as fully replacing judgement.",
      "box"),
    P("<b>3. Rain is the one factor that overrides a ripeness plan.</b> A forecast can force "
      "picking underripe fruit rather than risk dilution or, worse, splitting and grey rot "
      "\u2014 name this as the trump card in any harvest-timing answer.", "box"),
    P("<b>4. Machine harvesting's night-picking advantage is thermal, not just logistical.</b> "
      "Up to 15\u00b0C cooler fruit means less spoilage and oxidation risk <i>and</i> better "
      "preserved aromatics \u2014 state both consequences, not just \u2018it's cooler\u2019.",
      "box"),
    P("<b>5. \u2018Hand-picked\u2019 is a marketing signal, not a quality guarantee.</b> The "
      "chapter explicitly frames the real decision as multi-factor \u2014 style, logistics, "
      "legislation, cost \u2014 not simply better versus worse.", "box"),
]))

s.append(exam_traps([
 ("Treating potential alcohol thresholds as fixed across all AOCs.",
  "They vary by appellation \u2014 Petit Chablis 9.5%, Chablis 10%, Bourgogne Blanc 10.5% \u2014 "
  "name the specific figure a question asks for, not a generic one."),
 ("Assuming instruments have replaced tasting.",
  "Even with spectroscopy available, <b>tasting the grapes remains one of the most "
  "important</b> ways of deciding when to harvest."),
 ("Treating machine harvesting as inherently lower quality.",
  "Bow-rod shakers, optical sorting, in-machine SO\u2082 dosing and rigorous winery sorting "
  "have closed much of that gap \u2014 the old equation of machine-harvest with only "
  "acceptable quality is outdated."),
 ("Confusing 'hand-harvesting preferred' with 'hand-harvesting required'.",
  "Whole-bunch styles, selective picking (botrytis-affected bunches), steep slopes and bush "
  "vines <b>require</b> it \u2014 premium intent alone only <i>prefers</i> it."),
 ("Assuming night harvesting is only about avoiding heat for the pickers.",
  "The stated benefit is <b>fruit temperature</b> \u2014 up to 15\u00b0C cooler, cutting "
  "spoilage/oxidation and preserving aromatics \u2014 not primarily worker comfort."),
]))

# ================================================================ exam
exam = []

MCQ = [
 dict(q="Potential alcohol is best defined as:",
      opts=["The alcohol level after chaptalisation has been applied",
            "The amount of alcohol that would result from fermenting all the sugar in the "
            "grape must", "The maximum legal alcohol level for a given appellation",
            "The alcohol level measured after malolactic conversion"],
      ans=1, why="Potential alcohol is a calculation from must sugar content, historically "
                 "used across much of Europe as the harvest-readiness benchmark."),
 dict(q="Which factor most often overrides a planned harvest date?",
      opts=["The availability of a mobile laboratory for sugar testing",
            "The threat of rain, which can dilute juice or split skins and invite grey rot",
            "The cost of secateurs for hand-picking teams",
            "The distance between the vineyard and the winery"],
      ans=1, why="Rain risk near harvest is described as an overriding factor, forcing a "
                 "choice between picking underripe or risking the weather."),
 dict(q="Most dry still wine is harvested in a sugar range of approximately:",
      opts=["10\u201315\u00b0 Brix", "19\u201325\u00b0 Brix", "30\u201335\u00b0 Brix",
            "5\u201310\u00b0 Brix"],
      ans=1, why="19\u201325\u00b0 Brix converts to roughly 11\u201315% abv, the stated range for "
                 "most dry still wine."),
 dict(q="Aroma and tannin ripeness are, in practice, usually assessed by:",
      opts=["Titration", "A refractometer", "Taste, with experience",
            "Near-infrared spectroscopy exclusively"],
      ans=2, why="Unlike sugar (refractometer) or acidity (titration/pH meter), aroma and "
                 "tannin ripeness are usually judged by taste."),
 dict(q="California studies cited in the textbook suggest machine harvesting costs "
        "approximately:",
      opts=["The same as hand-harvesting", "Twice as much as hand-harvesting",
            "One-third the cost of hand-harvesting", "Ten times the cost of hand-harvesting"],
      ans=2, why="The stated California figure is roughly one-third the cost of "
                 "hand-harvesting, though the exact ratio depends on local labour and "
                 "machine costs."),
 dict(q="A key thermal advantage of night machine-harvesting is that fruit can be kept:",
      opts=["Up to 15\u00b0C / 59\u00b0F cooler, reducing spoilage and oxidation risk",
            "Exactly at ambient daytime temperature", "Frozen solid for transport",
            "Warm enough to begin spontaneous fermentation in the vineyard"],
      ans=0, why="Night-picked fruit can be up to 15\u00b0C cooler than day-picked, cutting "
                 "microbial spoilage and oxidation risk and preserving aromatics."),
 dict(q="A style requiring whole, intact bunches at the winery \u2014 such as for whole-bunch "
        "pressing or carbonic maceration \u2014 requires:",
      opts=["Machine harvesting with a bow-rod shaker", "Hand-harvesting",
            "Night harvesting by machine only", "Harvesting only after rain"],
      ans=1, why="Machine harvesters shake grapes off the stem, breaking up whole bunches \u2014 "
                 "styles needing intact bunches require hand-harvesting."),
 dict(q="Bush vines are harvested by hand principally because:",
      opts=["They are always found on steep slopes",
            "They have no trellis for a machine to shake against, risking vine and fruit "
            "damage", "Their grapes are always destined for botrytised wine",
            "Regulations universally forbid machine harvesting of bush vines"],
      ans=1, why="Machine harvesting depends on a trellis to shake; without one, the vine "
                 "and grapes would be damaged."),
 dict(q="Which is a stated disadvantage of hand-harvesting?",
      opts=["It cannot be selective at the bunch level",
            "It requires a reliable, trained and supervised workforce, and is more expensive "
            "at scale", "It always damages grape skins",
            "It cannot be used on steep slopes"],
      ans=1, why="Hand-harvesting is more costly at medium-large scale and depends on "
                 "workforce availability, training and supervision \u2014 it is, if anything, "
                 "better suited to steep slopes than machines."),
 dict(q="Selective picking of only botrytis-affected bunches, as for Trockenbeerenauslese, "
        "requires:",
      opts=["Machine harvesting with optical sorting", "Hand-harvesting",
            "A single harvest pass only", "Harvesting strictly by calendar date"],
      ans=1, why="Selecting specific bunches by condition is only achievable by hand, often "
                 "over several passes through the vineyard."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) Factors influencing the choice of harvest date"),
 P("Harvest date decisions combine direct measurement of the grapes with external "
   "constraints the grower cannot control."),
 P("Historically, readiness was judged by <b>potential alcohol</b> \u2014 the alcohol level "
   "fermenting all the must's sugar would produce \u2014 with European appellations setting "
   "explicit minimums: Petit Chablis at 9.5%, Chablis at 10%, Bourgogne Blanc at 10.5%, "
   "adjustable upward within limits by chaptalisation. Today growers measure several "
   "components directly: <b>sugar</b> by refractometer, typically targeting 19\u201325\u00b0 Brix "
   "(roughly 11\u201315% abv) for dry still wine; <b>acidity</b> by titration or pH meter; and "
   "<b>aroma and tannin ripeness</b>, usually judged by taste even where instruments such as "
   "near-infrared spectroscopy are available, since tasting remains one of the most "
   "important methods regardless of technology."),
 P("The context has shifted: a generally warmer climate and better viticulture make full "
   "ripening easier even in cool regions, and aroma and tannin ripeness is now often "
   "weighted above sugar ripeness alone \u2014 sometimes extending \u2018hang time\u2019 well past "
   "the point sugar alone would suggest, a practice some critics link to unbalanced, overly "
   "alcoholic wine and others defend on scoring and consumer grounds."),
 P("<b>Weather is the overriding constraint</b>: forecast rain near harvest can force "
   "picking underripe fruit rather than risk dilution or, worst case, split skins inviting "
   "grey rot and losing part or all of the crop. Intended wine style narrows the decision "
   "further \u2014 Loire Chenin Blanc is picked across 4\u20136 weeks by style (early for "
   "sparkling, late for botrytis), and residual-sugar styles may require picking "
   "deliberately late, or in the case of Icewine, only once temperature falls below a fixed "
   "threshold."),

 answer_head("Part b) Evaluating machine versus hand harvesting"),
 P("The choice is not a simple quality ranking; it weighs cost, gentleness, flexibility and "
   "site constraint against the specific wine being made."),
 P("<b>Machine harvesting</b> is far cheaper and faster at scale \u2014 roughly one-third the "
   "cost of hand-harvesting by California estimates \u2014 avoids dependence on casual labour "
   "availability, and permits night picking, keeping fruit up to 15\u00b0C cooler, reducing "
   "spoilage and oxidation risk and preserving delicate aromatics in fruity whites while "
   "saving refrigeration cost. Its central weakness is gentleness: shaking ruptures some "
   "skins and releases juice, unacceptable for whole-bunch styles or delicate whites "
   "avoiding early phenolic extraction, and it's impractical on steep slopes, mixed-variety "
   "plots ripening unevenly, or small vineyards where owning or renting a machine isn't "
   "cost-effective."),
 P("<b>Hand-harvesting</b> allows genuine bunch-by-bunch selectivity, removing diseased, "
   "under- or extra-ripe fruit as it's picked, and handles steep slopes, irregular rows and "
   "mixed plantings machines cannot. Careful handling in small, stackable crates avoids "
   "premature crushing and its oxidation and spoilage risk. Its costs are labour: more "
   "expensive at scale, dependent on a reliable, trained and supervised workforce, and "
   "typically carried out in daylight, raising heat-exposure risk unless growers commit to "
   "night-picking with torches."),
 P("Quality is no longer a simple proxy for the choice: bow-rod shaking machines, optical "
   "sorting, in-machine SO\u2082 dosing and rigorous winery sorting have closed much of the gap "
   "machine harvesting once had, and rising labour costs are pushing some premium producers "
   "toward machines, while some inexpensive wine remains hand-picked where cheap labour is "
   "available, as in South Africa. The one place the comparison isn't really optional is "
   "where a wine style, a selective pick, or the site itself \u2014 steep slopes, bush vines \u2014 "
   "requires hand-harvesting outright."),
 examiner_note([
   P("Part a) treats potential alcohol and direct measurement as complementary, not "
     "competing, and closes on the styles that override the general logic \u2014 exactly the "
     "layered structure a Distinction answer needs.", "box"),
   P("Part b) evaluates rather than lists, naming what has changed (machine quality "
     "improvements, labour cost pressure) rather than presenting the comparison as fixed, "
     "and closes by separating genuine choice from cases where the decision isn't really "
     "optional.", "box"),
 ]),
]

q2 = [
 answer_head("Part a) Designing and managing a vineyard for machine harvesting"),
 P("Vineyards intended for machine harvesting are increasingly designed for it from the "
   "outset, rather than adapted afterward."),
 P("Design choices include <b>even row spacing</b>, a <b>turning space at the end of "
   "rows</b> for the machine, and siting on <b>flat land or a small, regular gradient</b> "
   "\u2014 steep or uneven land defeats machine access regardless of other preparation. "
   "Trellising is also a precondition in practice: a trellis gives the machine something "
   "consistent to shake against, which is exactly why bush vines, having none, must be hand-"
   "harvested instead."),
 P("Fruit quality can be safeguarded at several points, each at its own cost. Before "
   "harvest, undesirable fruit can be <b>hand-selected out</b>. The machine itself matters: "
   "<b>bow-rod shaking</b> machines are gentler and more selective than older beater-type "
   "machines, and the newest machines add <b>optical sorting</b> and can crush white grapes "
   "and dose <b>SO\u2082</b> in-machine to limit oxidation as fruit is picked. After harvest, "
   "<b>rigorous sorting on arrival</b> at the winery \u2014 removing MOG (matter other than "
   "grapes), unripe and rotten fruit \u2014 catches what earlier stages missed. Together these "
   "have substantially closed the gap between machine- and hand-harvested fruit quality, "
   "though machine harvesting remains inherently less gentle, since grapes are shaken from "
   "the stem rather than kept as intact bunches."),

 answer_head("Part b) Wine style and harvest timing"),
 P("Beyond the general ripeness measures common to all wine, the specific style targeted "
   "shapes harvest timing directly, sometimes decisively."),
 P("In the <b>Loire</b>, Chenin Blanc is picked across <b>4\u20136 weeks</b> according to "
   "style: early for sparkling wine, mid-harvest for dry and off-dry styles, and late for "
   "botrytis or late-harvest wines \u2014 a single variety, several distinct picking windows. "
   "In <b>California</b>, Zinfandel may be picked <b>early to mid-August</b> for White "
   "Zinfandel or held to <b>September</b> for red wine; because Zinfandel tends to ripen "
   "unevenly even within a bunch, growers aiming for consistent quality must select "
   "carefully, and in hot sites must also decide whether to include shrivelled grapes in the "
   "pick."),
 P("<b>Residual-sugar styles</b> often demand picking later than a dry wine would, to "
   "concentrate sugar in the grape; botrytised wines typically require hand-harvesting over "
   "<b>several passes</b> through the vineyard to select only affected bunches as they "
   "develop. <b>Icewine</b> is the most extreme case: grapes may only be picked once "
   "temperature falls below a fixed threshold \u2014 below \u22128\u00b0C / 18\u00b0F for "
   "Canadian Icewine \u2014 meaning the calendar date is dictated by weather, not ripeness "
   "measurement at all."),
 P("These examples share a pattern: the more distinctive or extreme the intended style, the "
   "more harvest timing (and often method) is dictated by that style specifically, rather "
   "than by general ripeness indicators alone."),
 examiner_note([
   P("Part a) treats vineyard design, machine choice and winery sorting as three separate, "
     "sequential safeguards rather than one undifferentiated \u2018use better technology\u2019 "
     "claim \u2014 naming where in the process each intervention sits is what earns the mark.",
     "box"),
   P("Part b) uses three genuinely different examples \u2014 a style range within one variety "
     "(Chenin Blanc), a red/ros\u00e9 split within one variety (Zinfandel), and a hard weather "
     "threshold (Icewine) \u2014 to show the pattern generalises rather than resting on a "
     "single anecdote.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="Harvest timing and method both significantly influence the style, quality and "
           "cost of the finished wine.",
      parts=[("Explain the factors a grape grower considers when choosing the date of "
              "harvest.", "15%"),
             ("Compare machine and hand harvesting, evaluating the circumstances in which "
              "each is preferred.", "15%")],
      answer=q1),
 dict(stem="Harvest decisions are shaped by both the vineyard's design and the wine style "
           "being targeted.",
      parts=[("Explain how a vineyard can be designed and managed to make machine "
              "harvesting more suitable, and how fruit quality can be safeguarded when "
              "grapes are machine-harvested.", "10%"),
             ("With reference to specific examples, explain how the target wine style "
              "influences the timing of harvest.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch9_Harvest.pdf",
      "Chapter Nine \u00b7 Harvest", s, exam, maxpages=18)
