# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 7 — Canopy Management"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Seven: Canopy Management",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 7.1 The Aims of Canopy Management \u00b7 7.2 "
        "Canopy Management Techniques")

s.append(P("Canopy management is where every earlier chapter converges into a single decision: "
           "the vine's shoots, leaves and fruit are physically arranged to control light, air "
           "and the balance between growth and cropping. Establishment decisions (density, "
           "orientation, training, trellising) set the canopy's shape for the vineyard's life; "
           "summer pruning then makes yearly corrections within that shape."))
s.append(P("Reliably examined: <b>how sunlight exposure changes grape composition</b>, with the "
           "full set of effects expected; <b>vine balance</b>, including the consequences of "
           "over- and under-cropping; and <b>comparing training/trellising systems</b> against "
           "vigour, topography and the need for mechanisation. Named techniques (VSP, Guyot, "
           "GDC, Scott-Henry) are gettable marks \u2014 learn the names with their defining "
           "feature."))

# ================================================================ aims
s.append(H2("1. The Aims of Canopy Management"))
s += BUL([
    "Maximise the effectiveness of <b>light interception</b> by the canopy.",
    "<b>Reduce shade</b> within the canopy.",
    "Keep the grapes' microclimate <b>as uniform as possible</b>, for even ripening.",
    "Promote <b>balance</b> between the vine's vegetative and reproductive functions.",
    "Arrange the canopy to <b>ease mechanisation and/or manual labour</b>.",
    "Promote <b>air circulation</b> through the canopy, to reduce disease incidence.",
])
s.append(P("<b>Sunlight exposure raises bud fruitfulness</b> \u2014 the number of inflorescences "
           "inside a latent bud \u2014 while shade favours vegetative structures (tendrils) over "
           "reproductive ones. The reason traces to the wild vine: fruit must be visible to "
           "birds for seed dispersal, so a vine reaching sunlight (an opening in the forest "
           "canopy) prioritises inflorescences and fruit. A well-exposed vineyard canopy "
           "therefore raises <i>next season's</i> yield potential. Exposure also raises "
           "photosynthetic capacity directly, via a larger sunlit leaf area, letting the vine "
           "ripen a larger crop.", "note"))
s.append(EXHIBIT("EXHIBIT 7.1 \u2014 THE EFFECT OF SUNLIGHT EXPOSURE ON GRAPE COMPOSITION", [
    ["Direction", "Component", "Why"],
    ["<b>Increases</b>", "Sugar", "Greater overall photosynthesis across a better-exposed leaf "
     "area"],
    ["<b>Increases</b>", "Tannin, and its polymerisation", "Less bitter as polymerisation "
     "advances"],
    ["<b>Increases</b>", "Anthocyanins (colour, black grapes)", "\u2014"],
    ["<b>Increases</b>", "Terpenes and other favourable aroma compounds", "Includes the "
     "grapey aroma of Muscat"],
    ["<b>Decreases</b>", "Malic acid", "Warmer grapes respire more of it \u2014 without this, "
     "cool-climate acidity could be unpleasantly high; tartaric acid is little affected"],
    ["<b>Decreases</b>", "Methoxypyrazines", "The herbaceous character in varieties such as "
     "Cabernet Sauvignon"],
], [70, 148, W - 70 - 148], keep=False))
s += BUL([
    "<b>Too much</b> is not always wanted: intense heat and sun on the grapes causes "
    "<b>sunburn</b>, cutting quality and yield \u2014 hot climates may deliberately manage "
    "<i>for</i> some canopy shade instead.",
    "Dense, shaded canopies <b>dry more slowly</b> after rain or dew (poor air circulation), "
    "raising fungal disease pressure, and make <b>fungicide spray coverage</b> less reliable.",
])

# ================================================================ vine balance
s.append(H2("2. Vine Balance"))
s.append(P("<b>Vine balance</b> = matching yield to the vine's vigour, so it can ripen the crop "
           "it carries and stay productive in future seasons. The optimal yield is the "
           "<b>maximum weight of grapes with the composition the intended wine style needs</b> "
           "\u2014 not simply the maximum weight.", "note"))
s.append(FIGURE("FIGURE 7.2 \u2014 THE BALANCED CYCLE (SMART & ROBINSON, 1991)", FlowChart([
    ("PRE-V\u00c9RAISON", "Sugars and nutrients go mainly to shoot and root growth", None),
    ("POST-V\u00c9RAISON", "Allocation shifts mainly to fruit; shoot growth is depressed", None),
    ("CONSEQUENCE", "Canopy stays less dense \u2192 better light exposure \u2192 "
     "<b>high quality fruit</b> and <b>enhanced bud fruitfulness</b> next year", None),
    ("THE CYCLE CONTINUES", "A vine in balance tends to stay in balance", None),
], box_w=W * 0.80)))
s.append(FIGURE("FIGURE 7.2a \u2014 WHEN IT BREAKS: THE VEGETATIVE CYCLE", FlowChart([
    ("TOO LITTLE FRUIT", "Not enough crop for the vine's vigour \u2014 shoot growth "
     "<b>continues</b> instead of slowing, competing with the fruit for sugars", None),
    ("DENSE, SHADY CANOPY", "Unchecked shoot growth thickens the canopy \u2192 <b>lower "
     "quality fruit</b>", None),
    ("REDUCED BUD FRUITFULNESS", "Shade signals fewer inflorescences for next year "
     "\u2192 <b>low yield</b>", None),
    ("UNDER-CROPPING RECURS", "The spiral feeds itself \u2014 once started, it tends to "
     "continue", None),
], box_w=W * 0.80)))
s.append(P("<b>Over-cropping</b> is not a cycle but a one-way depletion: too much fruit for "
           "the vine's vigour draws sugars from <b>carbohydrate reserves</b> stored in trunk, "
           "cordons and roots \u2014 reserves the vine needs over winter and into next spring. "
           "Repeated over-cropping weakens the vine in future years, even where the current "
           "season's yield is high.", "note"))
s.append(P("What counts as \u2018balanced\u2019 is not fixed \u2014 it depends on:", "note"))
s += BUL([
    "<b>Natural resources</b> \u2014 warm, well-watered, fertile sites support vigorous vines "
    "that can ripen large crops; limited water or poor soil means lower vigour and lower "
    "sustainable yield.",
    "<b>Planting material</b> \u2014 some varieties/clones are inherently more vigorous "
    "(Cabernet Sauvignon > Merlot in similar conditions); rootstock choice matters too.",
    "<b>Disease</b> \u2014 viruses can lower vigour. <b>Vine age</b> \u2014 very old vines are "
    "less vigorous than vines aged roughly 10\u201340 years.",
    "<b>Wine style</b> \u2014 ros\u00e9, needing very short maceration, tolerates a larger yield "
    "than red, where tannin ripeness is more critical.",
])
s.append(P("<b>Winter pruning</b> sets shoot number and potential yield for the coming season; "
           "<b>summer pruning</b> corrects balance within that season as needed.", "note"))
s.append(H3("Yield"))
s += BUL([
    "Measured <b>per vine</b> (kg/vine) or <b>per area</b> (kg/ha, tons/acre). Over- or "
    "under-cropped \u2014 out of balance \u2014 generally means lower quality, but the "
    "<i>balanced</i> yield itself varies by resources, planting material and style, so some "
    "vines are balanced at higher yields than others.",
    "Area yield = yield per vine \u00d7 <b>planting density</b> \u2014 a low per-vine yield can "
    "still deliver a high area yield if planted densely. <b>EU legislation typically caps "
    "yield per area</b>; excess fruit may need removing while ripening or leaving unpicked.",
])

# ================================================================ establishment decisions
s.append(H2("3. Establishment Decisions"))
s.append(P("Canopy management starts at establishment, since <b>density, training and "
           "trellising must be decided before planting</b> and are hard to change afterward. "
           "Summer pruning is the yearly correction layered on top.", "note"))

s.append(H3("Vine Density and Row Orientation"))
s += BUL([
    "<b>Vine density</b> ranges from a few hundred to over 10,000 vines/ha. Governed by vigour, "
    "trellis type and access needs. <b>Low-vigour, VSP-trellised vines</b> can be planted "
    "densely (small vines, no gaps) \u2014 valuable on expensive land (Grand Cru Burgundy). "
    "<b>High-vigour vines</b> need wider within-row spacing, or overlapping canopies increase "
    "shading; in dry, unirrigated regions, low density can also let roots spread for water "
    "even where vines themselves aren't large.",
    "<b>Between-row spacing</b> must stop one row shading the next \u2014 vigorous, high-trained "
    "vines need more of it \u2014 and must fit any machinery used. <b>Low-density, wide-spaced "
    "vineyards are cheaper</b> to establish and maintain, needing less planting material and "
    "easier mechanisation.",
    "<b>Row orientation</b>: north\u2013south generally gives the most even light exposure. "
    "West-facing bunches get hotter afternoon sun, needing more leaf shading against sunburn. "
    "Rows are often set at <b>90\u00b0 to the prevailing wind</b> for protection, and parallel to "
    "the vineyard's longest side for efficiency. <b>Slopes over 10%</b> must be planted "
    "up-and-down, not across, or machinery risks slipping (unless terraced).",
])

s.append(H3("Training, Pruning and Trellising"))
s.append(P("The right system depends on three factors: <b>vigour</b> (from resources, planting "
           "material, disease \u2014 also alterable by RDI or low-vigour rootstock choice), "
           "<b>topography</b> (many trellis systems fail on steep or windy sites \u2014 parts of "
           "the Northern Rh\u00f4ne and Mosel use individual stakes instead), and the "
           "<b>need for mechanisation</b> (VSP suits it, since fruit sits in one zone per vine; "
           "bush vines and individually staked vines do not).", "note"))
s.append(EXHIBIT("EXHIBIT 7.3 \u2014 TRAINING AND PRUNING CHOICES", [
    ["", "Option A", "Option B"],
    ["<b>Training</b>", "<b>Head</b> \u2014 little permanent wood, just the trunk (perhaps "
     "short stubs); spur- or replacement cane-pruned",
     "<b>Cordon</b> \u2014 trunk plus one or more permanent horizontal arms; usually "
     "spur-pruned. Takes longer to establish"],
    ["Trunk height", "<b>Low</b> \u2014 benefits from soil-retained heat, more wind protection",
     "<b>High</b> \u2014 better frost avoidance, easier manual work (e.g. harvesting)"],
    ["<b>Winter pruning</b>", "<b>Spur</b> \u2014 one-year-old wood cut to 2\u20133 buds. Easier, "
     "often mechanised", "<b>Replacement cane</b> \u2014 longer wood (8\u201320 buds), tied "
     "horizontally. More complex, needs skilled labour to select and train canes"],
], [56, (W - 56) * 0.5, (W - 56) * 0.5], keep=False))
s.append(P("Bud number left at winter pruning tracks vigour \u2014 more buds for more vigorous "
           "vines \u2014 and is checked against yield and pruning-cutting weight to judge "
           "whether the vine is in balance.", "note"))

s.append(H4("TRELLISING"))
s.append(FIGURE("FIGURE 7.3 \u2014 FOUR TRELLIS PROFILES", TrellisProfile()))
s.append(EXHIBIT("EXHIBIT 7.4 \u2014 THE FOUR SYSTEMS AT A GLANCE", [
    ["", "Bush", "VSP", "GDC / Lyre", "Scott-Henry"],
    ["Vigour", "Any \u2014 dry climate restrains it", "Low", "High", "High"],
    ["Advantage", "Cheap; shades fruit (La Mancha)", "Simple to run", "Max light, "
     "big canopy", "Splits vigour, one row width"],
    ["Drawback", "No machines; wet + vigour \u2192 disease", "Shades too much "
     "if vigorous", "Harder to run/machine", "Harder to run/machine"],
], [58, (W - 58) * 0.24, (W - 58) * 0.20, (W - 58) * 0.27, (W - 58) * 0.29], keep=False))
s.append(P("Replacement cane-pruned VSP is called <b>Guyot</b> \u2014 one cane retained is "
           "Single Guyot, two is Double Guyot. Trellising in general, whichever system, "
           "trades the bush vine's low cost for better light interception, airflow (lower "
           "disease risk) and, by concentrating fruit in one predictable zone, easier "
           "mechanisation.", "note"))

# ================================================================ summer pruning
s.append(H2("4. Summer Pruning Techniques"))
s.append(P("Corrections made through the season, roughly in this order, mostly enhancing "
           "ripening, cutting disease pressure, or easing vineyard management. All except "
           "disbudding and pinching can be mechanised on well-set-up (straight, trellised) "
           "vineyards \u2014 increasingly common where skilled labour is scarce.", "note"))
s.append(FIGURE("FIGURE 7.4 \u2014 THE SEASON IN SEVEN CORRECTIONS", FlowChart([
    ("1. DISBUDDING", "Late spring \u2014 removes buds left as frost insurance, corrects "
     "balance/yield", None),
    ("2. SHOOT REMOVAL", "Clears infertile or poorly positioned shoots \u2014 keeps the "
     "canopy open", None),
    ("3. SHOOT POSITIONING", "Tucks shoots into trellis wires \u2014 organises the canopy, "
     "aids mechanisation", None),
    ("4. PINCHING", "At flowering \u2014 removes shoot tips to improve fruit set", None),
    ("5. SHOOT TRIMMING", "Limits growth and canopy thickness \u2014 better airflow and "
     "spray penetration", None),
    ("6. LEAF REMOVAL", "Cuts shading to enhance ripening \u2014 excessive removal in hot "
     "climates risks sunburn", None),
    ("7. CROP THINNING", "Near v\u00e9raison \u2014 concentrates ripening, or removes the "
     "least-ripe bunches to even up harvest", None),
], box_w=W * 0.86)))

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER SEVEN", [
    P("<b>1. Trace sunlight's effect back to bud fruitfulness, not just this year's fruit.</b> "
      "A well-exposed canopy raises yield potential <i>next</i> season too \u2014 answers that "
      "only discuss the current crop miss half the mechanism.", "box"),
    P("<b>2. Name the direction of imbalance, not just \u2018imbalance\u2019.</b> "
      "Under-cropping triggers a self-perpetuating vegetative cycle via reduced bud "
      "fruitfulness; over-cropping draws down carbohydrate reserves, weakening future vines. "
      "Different mechanisms, different consequences.", "box"),
    P("<b>3. Balance is relative, not absolute.</b> The same yield can be balanced for one "
      "vine and not another \u2014 resources, planting material, disease, age and wine style "
      "all shift where balance sits.", "box"),
    P("<b>4. Match the trellis to the vigour, not the reverse.</b> VSP is the default for "
      "low-to-moderate vigour; complex systems exist specifically because a vigorous vine "
      "would over-shade a single VSP canopy.", "box"),
    P("<b>5. Distinguish techniques by when and why, not just what.</b> Disbudding (late "
      "spring, balance/regulation) and pinching (at flowering, fruit set) both remove plant "
      "material but for entirely different reasons at entirely different times.", "box"),
]))

s.append(exam_traps([
 ("Treating all sunlight effects as positive without limit.",
  "Excess heat and sun cause <b>sunburn</b>. Hot climates may manage <i>for</i> shade, and "
  "excessive leaf removal there risks the same problem."),
 ("Confusing under- and over-cropping's mechanisms.",
  "<b>Under-cropping:</b> too little fruit, shoot growth continues, competes with what fruit "
  "there is. <b>Over-cropping:</b> too much fruit, the vine draws on stored carbohydrate "
  "reserves instead."),
 ("Assuming denser planting is always better value.",
  "Dense planting suits <b>low-vigour</b> vines on valuable land. High-vigour vines planted "
  "too densely get overlapping, over-shaded canopies \u2014 lower quality, not higher."),
 ("Assuming north-south row orientation is universally correct.",
  "It gives the most <b>even</b> exposure generally, but wind direction, slope angle (>10% "
  "must run up-down) and logistics can all override it."),
 ("Calling Guyot a trellis system.",
  "Guyot is a <b>pruning</b> method (replacement cane, on a head-trained vine) commonly "
  "combined with <b>VSP</b> trellising \u2014 the two are not the same thing."),
]))

# ================================================================ exam
exam = []

MCQ = [
 dict(q="A vine canopy well exposed to sunlight raises bud fruitfulness principally because:",
      opts=["Sunlight sterilises fungal spores that would otherwise damage buds",
            "In the wild, a vine reaching sunlight prioritises fruit so its seeds are visible "
            "to birds",
            "Shade physically prevents inflorescences from forming",
            "Sunlight raises soil temperature, which alone determines bud fruitfulness"],
      ans=1, why="The stated evolutionary rationale: a wild vine finding an opening in the "
                 "forest canopy prioritises reproductive structures over vegetative ones."),
 dict(q="Which is a stated effect of increased sunlight exposure on grape composition?",
      opts=["Increased malic acid", "Increased methoxypyrazines", "Decreased tannin "
            "polymerisation", "Decreased malic acid"],
      ans=3, why="Warmer grapes respire more malic acid. Methoxypyrazines and tannin "
                 "polymerisation move the other way \u2014 pyrazines fall, polymerisation rises "
                 "with exposure."),
 dict(q="Dense, shaded canopies raise fungal disease pressure chiefly because they:",
      opts=["Attract more insects that carry disease",
            "Dry more slowly after rain or dew due to poor air circulation",
            "Absorb more UV radiation, weakening the vine's natural defences",
            "Retain more nitrogen in the soil beneath them"],
      ans=1, why="Poor air circulation slows drying after rain or morning dew, and also makes "
                 "fungicide spray coverage less reliable."),
 dict(q="Under-cropping tends to trigger a self-perpetuating 'vegetative cycle' because:",
      opts=["Excess fruit draws down the vine's carbohydrate reserves",
            "Continued shoot growth competes with the limited fruit, densifying the canopy "
            "and lowering next year's bud fruitfulness",
            "The vine responds by increasing its own yield automatically",
            "Winter pruning becomes impossible on an under-cropped vine"],
      ans=1, why="Too little fruit for the vine's vigour lets shoot growth continue "
                 "unchecked, shading the canopy and reducing next season's bud fruitfulness "
                 "\u2014 which causes further under-cropping."),
 dict(q="Over-cropping weakens a vine in future years principally because:",
      opts=["It exhausts carbohydrate reserves stored in trunk, cordons and roots that the "
            "vine needs over winter and next spring",
            "It permanently reduces the vine's root system",
            "It causes irreversible loss of leaf surface area",
            "It always introduces viral disease"],
      ans=0, why="The vine draws sugars from its own stored reserves to ripen an "
                 "over-large crop, reserves it needs for the following dormant and spring "
                 "periods."),
 dict(q="Low-vigour, VSP-trellised vines are typically planted at high density chiefly to:",
      opts=["Reduce the risk of frost damage", "Maximise use of the vineyard land, avoiding "
            "gaps in the canopy since individual vines are small",
            "Improve access for large machinery", "Increase the vine's natural disease "
            "resistance"],
      ans=1, why="Small, low-vigour vines leave gaps if spaced too widely \u2014 dense planting "
                 "uses the land fully, valuable on expensive sites like Grand Cru Burgundy."),
 dict(q="A vineyard on a slope steeper than 10% should generally be planted:",
      opts=["Across the slope, to slow water run-off",
            "Up and down the slope, unless terraced, to avoid machinery slipping",
            "In a north-south orientation regardless of slope direction",
            "Only with bush vines, since trellising is impossible on any slope"],
      ans=1, why="Steep slopes (over 10%) risk machinery slipping if rows run across the "
                 "slope; up-and-down planting (or terracing) avoids this."),
 dict(q="Guyot is best described as a:",
      opts=["Trellising system distinct from VSP",
            "Replacement cane pruning method, commonly used with VSP trellising",
            "Type of complex, split canopy used for high-vigour vines",
            "Row orientation optimised for afternoon sun protection"],
      ans=1, why="Guyot describes the pruning (Single or Double, by canes retained), not the "
                 "trellis itself \u2014 it is commonly combined with VSP."),
 dict(q="Complex trellis systems such as Scott-Henry or Geneva Double Curtain exist mainly to:",
      opts=["Reduce establishment cost compared to VSP",
            "Split the canopy of a vigorous vine to reduce shading and maximise light "
            "interception",
            "Allow bush vines to be mechanised",
            "Eliminate the need for summer pruning"],
      ans=1, why="Vigorous vines produce enough shoots that a single VSP canopy would be "
                 "too dense; splitting it horizontally (GDC, Lyre) or vertically (Scott-Henry, "
                 "Smart-Dyson) reduces shading."),
 dict(q="Pinching, as a summer pruning technique, is carried out:",
      opts=["In late spring, to correct vine balance", "At flowering, to improve fruit set",
            "Near v\u00e9raison, to even up ripening", "At harvest, to ease picking"],
      ans=1, why="Pinching removes shoot tips specifically at flowering to improve fruit set "
                 "\u2014 distinct from disbudding (late spring) and crop thinning (near "
                 "v\u00e9raison)."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) Sunlight exposure and grape composition"),
 P("Canopy management shapes how much sunlight reaches the leaves and grapes, and that "
   "exposure changes grape composition in several distinct, well-established ways."),
 P("<b>Sugar</b> rises, through greater overall photosynthesis across a better-exposed leaf "
   "area. <b>Tannins</b> increase and polymerise further, reducing bitterness. Black grapes "
   "show enhanced <b>anthocyanin</b> (colour) development. <b>Malic acid falls</b>, since "
   "warmer grape temperatures raise the rate of malic acid breakdown in cellular respiration; "
   "without this, cool-climate wines could show unpleasantly high acidity, since tartaric acid "
   "itself is little affected. Favourable aroma compounds such as <b>terpenes</b> \u2014 "
   "responsible for the grapey aroma of Muscat, among other floral and fruity characters \u2014 "
   "increase, while <b>methoxypyrazines</b>, which give herbaceous character in varieties such "
   "as Cabernet Sauvignon, decrease."),
 P("These effects aren't unconditionally desirable. In hot climates or very sunny sites, "
   "intense sun and heat on the grapes causes <b>sunburn</b>, damaging quality and yield \u2014 "
   "canopy management there may deliberately manage <i>for</i> some shading instead of "
   "maximising exposure. A well-exposed canopy also raises <b>bud fruitfulness</b> for the "
   "following season, since sunlight signals the vine \u2014 as in the wild, reaching an "
   "opening in a forest canopy \u2014 to prioritise reproductive structures over vegetative "
   "ones, so the benefit outlasts the current vintage."),
 P("Exposure also affects disease pressure independently of composition: dense, shaded "
   "canopies dry more slowly after rain or dew, favouring fungal disease, and make fungicide "
   "spray coverage less reliable throughout the canopy."),

 answer_head("Part b) Vine balance and the consequences of imbalance"),
 P("Vine balance means matching the fruit the vine carries to its vigour, so it can ripen "
   "that fruit to the composition the intended wine style needs while staying productive in "
   "future seasons \u2014 not simply maximising yield."),
 P("In a balanced vine, the cycle is self-reinforcing: before v\u00e9raison, sugars and "
   "nutrients go mainly to shoot and root growth; after, allocation shifts to the fruit and "
   "shoot growth is depressed. Because shoots stop competing for growth resources, the "
   "canopy stays less dense, light exposure improves, fruit quality rises, and bud "
   "fruitfulness for next season is enhanced \u2014 so the cycle tends to repeat."),
 P("<b>Under-cropping</b> breaks this the other way: with too little fruit for the vine's "
   "vigour, shoot growth continues through the season, competing with the limited fruit for "
   "sugars. The canopy becomes dense and shady, fruit quality falls, and \u2014 critically \u2014 "
   "bud fruitfulness for next year is reduced, giving a low yield the following season too: "
   "the <b>\u2018vegetative cycle\u2019</b>, which once started tends to perpetuate itself."),
 P("<b>Over-cropping</b> works through a different mechanism: with too much fruit for the "
   "vine's vigour, it draws additional sugars from carbohydrate reserves stored in trunk, "
   "cordons and roots \u2014 reserves needed over winter and into next spring. Repeated over-"
   "cropping weakens the vine in future years, even where the current season's yield is "
   "high."),
 P("What counts as balanced is not fixed: it depends on natural resources (warmer, wetter, "
   "more fertile sites support higher sustainable yields), planting material (variety, clone "
   "and rootstock vigour \u2014 Cabernet Sauvignon more vigorous than Merlot in similar "
   "conditions), disease (viruses lower vigour), vine age (very old vines are less vigorous "
   "than those aged roughly 10\u201340 years), and wine style (ros\u00e9, with very short "
   "maceration, tolerates higher yields than red, where tannin ripeness matters more)."),
 examiner_note([
   P("Part a) states each compositional change and its mechanism together \u2014 not just "
     "\u2018tannin increases\u2019 but why \u2014 and closes by extending the effect into next "
     "season's bud fruitfulness, which most answers omit entirely.", "box"),
   P("Part b) gives under- and over-cropping <i>different</i> mechanisms rather than treating "
     "\u2018imbalance\u2019 as one problem, and names the five factors that make balance "
     "relative rather than absolute \u2014 exactly the structure a Distinction answer needs.",
     "box"),
 ]),
]

q2 = [
 answer_head("Part a) Comparing trellising systems"),
 P("The choice between no trellis, VSP and a complex split-canopy system turns principally "
   "on vine vigour, with mechanisation and cost as secondary factors."),
 P("<b>Untrellised (bush) vines</b> \u2014 head-trained, spur-pruned, no support structure \u2014 "
   "are simple and cheap to establish, and their drooping shoots usefully shade the fruit in "
   "hot, sunny regions such as La Mancha. They are not mechanisable, and depend on dry "
   "conditions restraining vigour: a too-vigorous bush vine develops an over-dense, over-"
   "shading canopy, and wet conditions in that dense canopy favour disease."),
 P("<b>VSP (vertical shoot positioning)</b> is the most common and simplest trellised "
   "system: shoots are trained vertically into a single narrow canopy, usable on either "
   "head-trained, replacement cane-pruned vines (commonly called <b>Guyot</b> \u2014 Single or "
   "Double by canes retained) or cordon-trained, spur-pruned vines. It suits <b>low to "
   "moderate vigour</b>: a more vigorous vine forced into a single VSP canopy becomes too "
   "dense, over-shading leaves and fruit."),
 P("<b>Complex systems</b> \u2014 Geneva Double Curtain and Lyre splitting the canopy "
   "horizontally, Smart-Dyson and Scott-Henry vertically \u2014 exist specifically to solve "
   "that problem for vigorous vines, spreading the same leaf and shoot volume over a larger "
   "surface to cut shading and maximise light interception. They make the best use of "
   "vineyard space and resources for large yields of quality fruit, but are correspondingly "
   "harder to manage and mechanise than VSP."),
 P("Trellising in general \u2014 whichever system \u2014 trades the bush vine's low cost for "
   "better light interception, airflow (lower disease risk) and, by concentrating fruit in "
   "one predictable zone, easier mechanisation."),

 answer_head("Part b) Factors in choosing a training and trellising system"),
 P("Three factors govern the choice, and they interact rather than apply independently."),
 P("<b>Vigour</b> comes first: set by natural resources (especially temperature, water and "
   "nutrients), planting material (variety, clone, rootstock) and disease (viruses lower "
   "it), but also partly within the grower's control \u2014 regulated deficit irrigation or a "
   "low-vigour rootstock can restrain it deliberately. Low-vigour vines suit VSP and dense "
   "planting; high-vigour vines need wider spacing, a complex split-canopy system, or both, "
   "to avoid over-shading."),
 P("<b>Topography</b> can override vigour-based logic entirely: many trellising systems "
   "fail on steep or windy sites, which is why some steep sites in the Northern Rh\u00f4ne and "
   "the Mosel use individual stakes for each vine rather than a wired trellis, regardless of "
   "what vigour alone would suggest."),
 P("The <b>need for mechanisation</b> favours systems that concentrate fruit in one "
   "predictable zone per vine \u2014 VSP is well suited, while bush vines and individually "
   "staked vines, being far less uniform, are not. Where skilled labour is scarce, this "
   "factor increasingly outweighs the others in practice."),
 P("These three factors also interact with density and row orientation decided at the same "
   "time: spacing depends on vigour and trellis type together, and row orientation must "
   "additionally balance even light exposure (typically north\u2013south) against wind "
   "protection and logistics \u2014 all fixed at establishment and difficult to revisit."),
 examiner_note([
   P("Part a) compares three systems on the same four criteria \u2014 cost, mechanisation, "
     "light/airflow, vigour suited \u2014 rather than describing each in isolation, and names "
     "the specific named systems (GDC, Lyre, Smart-Dyson, Scott-Henry) the mark scheme rewards.",
     "box"),
   P("Part b) treats the three factors as interacting, not independent \u2014 topography can "
     "override vigour, mechanisation need can override both \u2014 and connects the answer "
     "back to density and orientation decided at the same establishment moment.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="Canopy management aims to control the vine's exposure to light and its balance "
           "between vegetative growth and cropping.",
      parts=[("Explain how sunlight exposure affects the composition of the grape, and the "
              "circumstances in which maximising exposure is not desirable.", "15%"),
             ("Explain the concept of vine balance, including the consequences of "
              "under-cropping and over-cropping.", "10%")],
      answer=q1),
 dict(stem="The choice of training and trellising system shapes a vineyard for its whole "
           "productive life.",
      parts=[("Compare untrellised, VSP-trellised and complex-trellised vineyards.", "15%"),
             ("Explain the factors a grape grower considers when choosing a training and "
              "trellising system.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch7_Canopy_Management.pdf",
      "Chapter Seven \u00b7 Canopy Management", s, exam, maxpages=18)
