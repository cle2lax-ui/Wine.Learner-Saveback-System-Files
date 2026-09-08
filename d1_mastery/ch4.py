# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 4 — Approaches to Grape Growing"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Four: Approaches to Grape Growing",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 4.1 Conventional \u2192 4.6 Precision Viticulture")

s.append(P("This chapter is almost always examined as <b>compare and evaluate</b>, not recall. "
           "Every section has the same shape \u2014 what the approach is, what it does, advantages, "
           "disadvantages \u2014 and the examiner wants a judgement, not two listed columns."))
s.append(P("Two things separate the top answers. The approaches are <b>not mutually exclusive</b>: "
           "biodynamic includes organic practices, precision viticulture is often used within "
           "sustainable or organic viticulture, and several organic techniques appear in "
           "sustainable viticulture too. And the disadvantages are often <b>commercial or "
           "definitional</b> \u2014 unprotected terms, certification cost, standards set too low \u2014 "
           "not viticultural."))

# ---------------------------------------------------------------- conventional
s.append(FIGURE("FIGURE 4.1 \u2014 THE APPROACHES NEST, THEY DO NOT COMPETE", InclusionRings(
    rings=[
        ("SUSTAINABLE", "IPM / lutte raisonn\u00e9e \u2014 will use chemicals when necessary",
         COOL),
        ("ORGANIC", "No synthetic fertilisers, fungicides, herbicides or pesticides", LEAF),
        ("BIODYNAMIC", "Demeter requires organic certification as its baseline", BURGUNDY),
    ],
    tags=[
        ("PRECISION VITICULTURE", "\u2014 a tool often used inside sustainable or organic practice"),
        ("REGENERATIVE", "\u2014 goes further again: improves soil and water, not just maintains them"),
    ]))
)

s.append(H2("1. Conventional Viticulture"))
s.append(FlowChart([
    ("THE AIMS", "Raise production levels \u00b7 reduce labour requirements", None),
    ("THE MEANS", "<b>Mechanisation \u00b7 chemical inputs \u00b7 irrigation \u00b7 clonal selection</b>", None),
    ("THE RESULT", "Viticulture became a <b>monoculture</b> \u2014 weed-free by ploughing and "
     "herbicides, sharply increased agrochemical use, increased mineral fertiliser", None),
], box_w=W * 0.80))
s.append(EXHIBIT("EXHIBIT 4.1 \u2014 MONOCULTURE: ADVANTAGES AND DISADVANTAGES", [
    ["Advantages", "Disadvantages"],
    ["Ability to <b>mechanise</b> vineyard work",
     "More <b>prone to disease and pests</b> \u2014 fungal disease spreads faster and hits all "
     "plants at once"],
    ["<b>Reduced competition</b> from other plants",
     "<b>Nutrients depleted</b> \u2014 no natural ecosystem to replenish them, so more fertiliser"],
    ["Ability to tend the <b>specific needs of the variety</b> \u2014 irrigation, nutrition, "
     "treatments \u2014 <b>raising yields while cutting costs</b>",
     "<b>Residual chemicals</b> reach <b>groundwater</b> (water underground in soil spaces or "
     "bedrock cracks) or the air \u2014 environmental damage"],
], [W / 2, W / 2]))
s.append(P("By the late twentieth century routine spraying and mineral fertiliser use were seen as "
           "<b>harmful to soil quality, expensive, environmentally detrimental and potentially "
           "hazardous to workers and consumers</b>. Three main options exist for growers reducing "
           "chemical use.", "note"))

# ---------------------------------------------------------------- sustainable
s.append(H2("2. Sustainable Viticulture"))
s += BUL([
    "Three themes: <b>economic, social and environmental</b> sustainability. The focus here is "
    "environmental.",
    "Aims: promote <b>natural ecosystems</b>, maintain <b>biodiversity</b>, manage <b>waste</b>, "
    "minimise chemicals and <b>energy use</b>, reduce wider environmental impact.",
    "Method: <b>in-depth understanding of vine and pest lifecycles</b> plus weather monitoring, to "
    "predict and prevent an outbreak (downy mildew) <b>before it occurs</b> \u2014 replacing a "
    "<b>regimented spraying calendar</b> with well-timed applications. <b>Fewer applications are "
    "needed.</b>",
])
s.append(H4("INTEGRATED PEST MANAGEMENT (IPM / LUTTE RAISONN\u00c9E)"))
s.append(P("Builds on organic insights <b>but is prepared to use chemical interventions when "
           "necessary</b> \u2014 the distinction that defines it.", "note"))
s.append(FlowChart([
    ("SET THRESHOLDS", "Levels at which action is needed \u2014 e.g. pest populations", None),
    ("IDENTIFY AND MONITOR", "<b>When</b> to look for a named pest (caterpillars, moths), "
     "<b>what signs</b> to look for, what the damage looks like", None),
    ("PREVENTATIVE MEASURES", "Anticipate problems; boost the vine's own defences", None),
    ("EVALUATE AND CONTROL", "Only if thresholds are exceeded <b>and</b> prevention has failed",
     None),
], box_w=W * 0.80))
s += BUL([
    "Intervention only before the <b>economic threshold</b> \u2014 the point at which damage will "
    "exceed the cost of intervening. This limits crop damage, cuts chemical use and cost, and "
    "<b>prevents weeds building resistance</b>.",
    "Institutions such as the <b>University of California's IPM department</b> issue detailed "
    "advice.",
    "National and regional standards vary with circumstance (dry versus wet climates) and are "
    "<b>more about a way of working</b> \u2014 identifying hazards, record keeping, calculating "
    "thresholds \u2014 <b>than absolute standards</b>. Examples: <b>LODI RULES</b>, <b>Sustainable "
    "Winegrowing NZ</b>, <b>Sustainable Winegrowing South Africa</b>.",
])
s.append(EXHIBIT("EXHIBIT 4.2 \u2014 SUSTAINABLE VITICULTURE EVALUATED", [
    ["Advantages", "Disadvantages"],
    ["Attends to <b>economic, social and environmental</b> impact",
     "<b>The term is not protected</b> \u2014 usable to promote wine without a clear set of standards"],
    ["<b>Scientific understanding</b> of pests and disease minimises interventions",
     "<b>National standards can be set too low.</b> New Zealand's near-universal uptake cut "
     "pesticide use, but drew criticism for too low a bar"],
    ["Reduced spraying of <b>synthetic and traditional</b> treatments", "\u2014"],
    ["The consequent <b>cost saving</b>, itself an incentive", "\u2014"],
], [W / 2, W / 2]))

# ---------------------------------------------------------------- organic
s.append(H2("3. Organic Viticulture"))
s.append(P("Seeks to improve the <b>soil</b> and the microbes and animals within it, and thereby "
           "the <b>health and disease-resistance of the vine</b>. Rejects <b>manufactured "
           "(synthetic) fertilisers, fungicides, herbicides and pesticides</b>.", "note"))
s.append(H4("KEY FEATURES"))
s += BUL([
    "<b>Compost</b> breaking down in the soil \u2014 slow nutrient release, improved structure, "
    "increased <b>biomass</b> (total quantity or weight of organisms in a given area or volume).",
    "<b>Natural fertilisers</b> \u2014 animal dung, natural calcium carbonate \u2014 to restore the "
    "vineyard's natural balance.",
    "<b>Cover crops</b> against erosion and for soil life, by ploughing in (<b>\u2018green manure\u2019</b>) "
    "or improving biodiversity.",
    "<b>Reduced monoculture</b> \u2014 cover crops, hedges, \u2018islands\u2019 of biodiversity. "
    "<i>These techniques are also often used in sustainable viticulture.</i>",
])
s.append(H4("TREATMENTS AND BIOLOGICAL CONTROLS"))
s += BUL([
    "<b>Sulfur and copper sulfate</b> against mildews, with close weather monitoring to determine "
    "when spraying is really necessary.",
    "<b>Bacillus subtilis</b> introduced against grey rot, competing with <b>Botrytis cinerea</b> "
    "for space on the grape.",
    "<b>\u2018Sexual confusion\u2019</b> \u2014 <b>pheromone tags or capsules</b> disrupting the mating of "
    "moths and mealy bugs.",
])
s.append(CALLOUT("THE COUNTER-ARGUMENT WORTH KNOWING", [
    P("Where frequent sprays are needed, <b>build-up of the heavy metal copper</b> in the soil has "
      "led some to conclude that careful use of <b>longer-lasting synthetic sprays is better for "
      "the environment</b>. The <b>reduced need for tractors</b> is a further bonus of synthetics.",
      "box"),
]))
s.append(H4("CERTIFICATION"))
s += BUL([
    "<b>Many bodies</b>, similar principles, <b>slightly different standards</b> \u2014 so some "
    "organic wines have met stricter rules than others. All <b>should meet IFOAM</b> standards.",
    "A <b>universal requirement</b>: a <b>period of conversion</b> to organic standards before "
    "certification.",
    "Certification <b>adds cost</b>, though it may bring promotional advantage depending on target "
    "consumer and market.",
    "Cost/benefit evaluation is <b>at a very early stage</b>: some studies find slightly lower "
    "yields, others attribute added cost to <b>additional labour</b>. Costs vary worldwide \u2014 cool "
    "wet climates are harder to manage without sprays, and labour costs differ.",
])
s.append(FIGURE("FIGURE 4.2 \u2014 VINEYARDS CERTIFIED ORGANIC, 2017", BarChart([
    ("Italy", 15.8), ("WORLD", 5.4), ("New Zealand", 4.3), ("USA", 2.7),
    ("Argentina", 2.5, "<2.5%"), ("Chile", 2.5, "<2.5%"), ("South Africa", 2.5, "<2.5%"),
    ], maxv=16, highlight=["WORLD"]),
    note="<b>Europe holds 84%</b> of the world's organic viticulture. <b>Italy</b> has both the "
         "highest percentage and is the largest producer and exporter of organic wines. Largest "
         "markets for organic still wine: <b>Germany, France, the UK, the USA, Sweden, Japan</b>."))
s.append(EXHIBIT("EXHIBIT 4.4 \u2014 ORGANIC VITICULTURE EVALUATED", [
    ["Advantages", "Disadvantages"],
    ["Improved <b>health and disease-resistance of the vine</b>",
     "A <b>possible small yield reduction</b>"],
    ["Improved <b>health of the soil</b>",
     "<b>Significant yield reductions in difficult years</b> \u2014 long rainfall or high humidity"],
    ["<b>Elimination of synthetic chemical spraying</b>",
     "Increased reliance on <b>copper sprays</b> \u2192 heavy metal build-up in soils"],
    ["<b>Saves the cost</b> of synthetic chemicals",
     "<b>Cost and time</b> of certification where sought"],
], [W / 2, W / 2]))

# ---------------------------------------------------------------- biodynamic
s.append(H2("4. Biodynamic Viticulture"))
s.append(P("Based on <b>Rudolf Steiner and Maria Thun</b>. <b>Includes organic practices</b> and "
           "adds philosophy and cosmology, treating the farm as an <b>organism</b> and the soil as "
           "part of a connected system with the Earth, planets and air. Practices are timed to "
           "planetary, lunar and stellar cycles.", "note"))
s.append(EXHIBIT("EXHIBIT 4.5 \u2014 THE LUNAR SCHEME", [
    ["Phase", "Mood", "Practice"],
    ["Moon <b>ascending</b>", "<b>Summer</b>; sap rising",
     "Take <b>cuttings for grafting</b>; <b>avoid pruning</b>"],
    ["Moon <b>descending</b>", "<b>Winter</b>; roots favoured", "Best time to <b>plant or prune</b>"],
], [74, 72, W - 146]))
s.append(P("<b>Maria Thun</b> and others developed calendars of <b>root, leaf, flower and fruit "
           "days</b> indicating the best days for particular activities.", "note"))
s.append(EXHIBIT("EXHIBIT 4.6 \u2014 THE PREPARATIONS", [
    ["Preparation", "Method", "Purpose"],
    ["<b>500</b><br/>horn manure", "Manure in a cow's horn, buried <b>over winter</b>, dug up and "
     "<b>dynamised</b> \u2014 stirred into water in alternating vortices so it \u2018memorises\u2019 the "
     "preparation \u2014 then sprayed on the <b>soil</b>",
     "Believed to <b>catalyse humus formation</b>"],
    ["<b>501</b><br/>horn silica", "Cow's horn filled with <b>ground quartz</b>, buried <b>six "
     "months</b>, dynamised, sprayed on the <b>vines</b>",
     "Thought to <b>encourage plant growth</b>"],
    ["<b>502\u2013508</b><br/>compost starters", "Compost is \u2018activated\u2019 by starters in tiny "
     "quantities \u2014 <b>yarrow, chamomile, nettle, oak bark, dandelion, valerian</b>; the yarrow is "
     "buried in a deer's bladder", "Assist <b>decomposition of the compost</b>"],
], [68, (W - 68) * 0.64, (W - 68) * 0.36], keep=False))
s += BUL([
    "Like organic growers, biodynamic growers use <b>sulfur and copper</b> sprays. Some practise "
    "<b>ashing</b> \u2014 spreading ashes of burnt weed seeds or harmful animals (rats, sparrows).",
    "<b>Demeter</b> is the most common certifier, setting international standards; it requires "
    "<b>organic certification as a baseline</b>, then specifies further principles interpreted "
    "locally by each national association.",
    "Additional costs are <b>little more than organic</b>, generally from <b>additional labour</b>.",
    "Mainly taken up by <b>smaller growers and estates</b>, including prestigious Burgundy domaines "
    "(<b>Domaine de la Roman\u00e9e-Conti</b>); particularly popular in the <b>Loire Valley</b>.",
])
s.append(CALLOUT("THE EVIDENCE POSITION \u2014 STATE IT PLAINLY", [
    P("Advantages and disadvantages <b>include those of organic growing</b>. Beyond that, research "
      "comparing organic and biodynamic \u2014 soil quality, wine composition \u2014 has been "
      "<b>limited and so far inconclusive</b>. Reproduce that neutrally; advocacy either way reads "
      "as untrained.", "box"),
]))

# ---------------------------------------------------------------- regenerative
s.append(H2("5. Regenerative Viticulture"))
s.append(P("Term coined by the <b>Rodale Institute in the 1980s</b>. Uses methods similar to "
           "organic or sustainable farming, but works to <b>improve</b> resources such as soil and "
           "water <b>rather than merely maintain</b> them \u2014 the definitional distinction being "
           "tested.", "note"))
s += BUL([
    "Vineyards are viewed as <b>agroecosystems</b> \u2014 ecosystems modified for agriculture \u2014 "
    "rather than a system meeting the needs of one crop. A fully functioning agroecosystem meets "
    "its own needs, so inputs such as fertilisers are <b>significantly reduced</b>.",
    "<b>Soil health is the top priority</b>; healthy soils are packed with water, nutrients and "
    "biodiversity.",
    "<b>Biodiversity above and below ground</b> is essential. <b>Mycorrhizal fungi</b> form "
    "symbiotic relationships with vines, improving absorption of <b>phosphorus, nitrogen and "
    "water</b> and making the system <b>more resistant to drought and heat</b>.",
    "Growers <b>improve their own well-being</b> \u2014 lower input costs, less chemical exposure.",
    "<b>Common practices:</b> limited tilling (soils then <b>sequester carbon</b>), limited "
    "irrigation, added compost, cover crops against erosion and water loss, and animals as natural "
    "pest controls.",
    "<b>No universal standard</b>, but certifiers exist \u2014 the <b>Regenerative Organic Alliance "
    "(ROA)</b> measures soil health, animal welfare and human empowerment, and charges fees.",
])
s.append(EXHIBIT("EXHIBIT 4.7 \u2014 REGENERATIVE VITICULTURE EVALUATED", [
    ["Advantages", "Disadvantages"],
    ["Soils <b>rehabilitated</b>, decreasing synthetic inputs",
     "<b>Not legally defined</b> \u2014 claims may be exaggerated"],
    ["<b>Carbon sequestered</b>, helping fight climate change",
     "Growers must <b>experiment</b> to find the right approach \u2014 time, resources, delay"],
    ["Vineyards <b>more resilient</b> to climate change",
     "<b>Results take time</b>, making transition difficult and costly"],
    ["<b>Biodiversity</b> and animal welfare improve",
     "<b>Cannot rely on inputs</b> under disease or climate pressure \u2014 yields may fall"],
    ["<b>Less chemical exposure</b> for growers", "<b>Certification costs money</b> \u2014 a barrier"],
], [W / 2, W / 2], keep=False))

# ---------------------------------------------------------------- precision
s.append(H2("6. Precision Viticulture"))
s.append(P("Growers traditionally worked uniformly, but experience and research show <b>big "
           "variations in vine response even within the same plot</b>.", "note"))
s.append(FlowChart([
    ("COLLECT DATA", "Soil, vine vigour, topography, plant growth \u2014 sensors on aircraft "
     "(<b>remote</b>) or on a tractor or harvester (<b>proximal</b>)", None),
    ("MAP IT", "<b>GPS</b> and <b>GIS</b> present the data visually as maps", None),
    ("TARGET THE INTERVENTION", "<b>Variable-rate application technology</b> \u2014 plot to plot, row "
     "to row", None),
    ("THE INTERVENTIONS", "Pruning \u00b7 leaf removal \u00b7 treatments \u00b7 irrigation \u00b7 crop thinning \u00b7 "
     "harvesting", None),
], box_w=W * 0.80))
s += BUL([
    "Worked examples: <b>changing rootstock halfway along a row</b> as soil fertility changes; "
    "<b>more leaf-stripping</b> where vigour is high.",
    "Requires <b>considerable upfront investment</b>, so it suits <b>large scale viticulture or "
    "high-value smaller estates</b> \u2014 most used in <b>California and Australia</b>.",
    "Most effective where data is used <b>systematically</b> to control treatment or irrigation "
    "rates. It seeks not only to <b>respond</b> to variation but to <b>reduce</b> it, and can "
    "<b>identify quality zones</b> within one vineyard.",
    "<b>Often used as part of sustainable or organic viticulture.</b>",
])
s.append(EXHIBIT("EXHIBIT 4.8 \u2014 PRECISION VITICULTURE EVALUATED", [
    ["Advantages", "Disadvantages"],
    ["Understanding of variations <b>between and within vineyards</b> affecting yield and "
     "quality", "Initial cost of <b>remote data collection</b>"],
    ["Tailoring of interventions \u2014 variety and rootstock choice, canopy management, treatments, "
     "harvest dates \u2014 to <b>individual blocks or rows</b>",
     "Cost of <b>sensors and software</b>, and of <b>consultancy or trained staff</b> to interpret "
     "the data and act on it"],
], [W / 2, W / 2]))

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER FOUR", [
    P("<b>1. Treat the approaches as overlapping, not competing.</b> Biodynamic <i>includes</i> "
      "organic; Demeter requires organic certification as a baseline; precision viticulture is "
      "often used <i>within</i> sustainable or organic viticulture.", "box"),
    P("<b>2. Locate each disadvantage correctly.</b> Viticultural (yield loss in wet years) \u00b7 "
      "environmental (copper accumulation) \u00b7 definitional (unprotected terms) \u00b7 commercial "
      "(certification cost, upfront investment). Naming the <i>type</i> is evaluation.", "box"),
    P("<b>3. Use the copper argument.</b> That heavy metal build-up leads some to judge synthetic "
      "sprays better for the environment is the most useful counter-intuitive point available.",
      "box"),
    P("<b>4. Report the evidence base honestly.</b> Organic cost/benefit is at a very early stage; "
      "organic-versus-biodynamic research is inconclusive. That is accuracy, not fence-sitting.",
      "box"),
    P("<b>5. Remember the economic threshold.</b> It explains why sustainable viticulture cuts "
      "chemicals <i>and</i> cost simultaneously \u2014 and so appeals commercially, not only "
      "ethically.", "box"),
]))

s.append(exam_traps([
 ("Describing sustainable viticulture as chemical-free.",
  "IPM explicitly <b>is prepared to use chemical interventions when necessary</b>. It reduces the "
  "number and improves the timing of applications; it does not eliminate them. <b>Organic</b> "
  "rejects synthetic treatments \u2014 but still uses sulfur and copper."),
 ("Assuming organic and biodynamic use no sprays at all.",
  "Both use <b>traditional chemicals</b>, principally <b>sulfur and copper</b>. The organic "
  "objection is to <i>manufactured</i> (synthetic) fertilisers, fungicides, herbicides and "
  "pesticides, not to treatment as such."),
 ("Confusing preparation 500 with 501.",
  "<b>500 = horn manure</b>, buried <b>over winter</b>, sprayed on the <b>soil</b>, catalyses "
  "<b>humus formation</b>. <b>501 = horn silica</b> (ground quartz), buried <b>six months</b>, "
  "sprayed on the <b>vines</b>, encourages <b>plant growth</b>. 502\u2013508 are compost starters."),
 ("Treating regenerative viticulture as a synonym for organic.",
  "The stated distinction is that regenerative works to <b>improve</b> resources such as soil and "
  "water rather than merely <b>maintain</b> them, viewing the vineyard as an <b>agroecosystem</b>. "
  "It is also <b>not legally defined</b>."),
 ("Presenting precision viticulture as universally available.",
  "It needs <b>considerable upfront investment</b> in sensors and software, so it is only an "
  "option in <b>large scale viticulture or on high-value, smaller estates</b> \u2014 most widely used "
  "in California and Australia."),
]))

# ---------------------------------------------------------------- exam
exam = []

MCQ = [
 dict(q="The aims of the shift to conventional, intensive viticulture in the later twentieth century were principally to:",
      opts=["Improve wine quality and express terroir more precisely",
            "Raise production levels and reduce labour requirements",
            "Reduce agrochemical use and protect groundwater",
            "Increase biodiversity while maintaining yields"],
      ans=1, why="Raising production and reducing labour, achieved through mechanisation, chemical "
                 "inputs, irrigation and clonal selection."),
 dict(q="Which is given as a disadvantage of monoculture?",
      opts=["It prevents the grower tending to the specific needs of the variety planted",
            "It increases competition from other plants",
            "Nutrients can be depleted, as there is no natural ecosystem to replenish them",
            "It makes mechanisation of vineyard work impossible"],
      ans=2, why="The other three invert monoculture's stated advantages: mechanisation, "
                 "reduced competition, tending the variety's specific needs."),
 dict(q="Integrated pest management is distinguished from organic viticulture principally because it:",
      opts=["Requires certification by IFOAM",
            "Is prepared to use chemical interventions when necessary",
            "Prohibits the use of sulfur and copper",
            "Operates on a fixed calendar of preventative spraying"],
      ans=1, why="IPM builds on organic insight but will use chemicals when necessary. Option D "
                 "describes the practice IPM replaces."),
 dict(q="Under IPM, the 'economic threshold' is the point at which:",
      opts=["The vineyard becomes profitable for the season",
            "Pest populations reach the maximum permitted by certification",
            "The level of damage will exceed the cost of intervention",
            "The cost of certification exceeds the price premium obtainable"],
      ans=2, why="The grower monitors the scale of potential problems and intervenes only before "
                 "damage will exceed the cost of intervening."),
 dict(q="Which body sets the standards that all organic certification bodies should meet?",
      opts=["Demeter", "IFOAM", "The Regenerative Organic Alliance", "LODI RULES"],
      ans=1, why="IFOAM \u2014 International Federation of Organic Agriculture Movements. Demeter "
                 "is biodynamic; the ROA certifies regenerative farming; LODI RULES is a "
                 "sustainability scheme."),
 dict(q="In 2017, the percentage of the world's vineyards certified organic was approximately:",
      opts=["2.5%", "5.4%", "15.8%", "84%"],
      ans=1, why="5.4% of world vineyards. 15.8% is Italy's figure and 84% is Europe's share of "
                 "world organic viticulture \u2014 both deliberate distractors."),
 dict(q="Biodynamic preparation 501 is made by:",
      opts=["Stuffing cow manure into a cow's horn and burying it over winter",
            "Filling a cow's horn with ground quartz and burying it for six months",
            "Burying yarrow in a deer's bladder",
            "Spreading the ashes of burnt weed seeds on the vineyard"],
      ans=1, why="501 is horn silica. Option A is preparation 500 (horn manure); C is one of the "
                 "compost starters 502\u2013508; D describes ashing."),
 dict(q="According to biodynamic practice, when the moon is descending it is the best time to:",
      opts=["Take cuttings for grafting", "Spray preparation 501 onto the vines",
            "Plant vines or prune", "Harvest fruit for sparkling wine"],
      ans=2, why="A descending moon evokes winter, favouring roots \u2014 best for planting or "
                 "pruning. An ascending moon suits taking cuttings; pruning is then avoided."),
 dict(q="Regenerative viticulture is distinguished from organic and sustainable farming principally because it:",
      opts=["Prohibits all forms of certification",
            "Works to improve resources such as soil and water rather than only maintain them",
            "Permits synthetic fertilisers where soil tests justify them",
            "Was defined in law by the Rodale Institute in the 1980s"],
      ans=1, why="Improving, not just maintaining, resources is the stated distinction. The "
                 "Rodale Institute coined the term \u2014 it was never legally defined."),
 dict(q="Data collected by sensors mounted on a tractor or harvester in the vineyard is described as:",
      opts=["Remote", "Proximal", "Variable-rate", "Geospatial"],
      ans=1, why="Proximal, versus 'remote' data from sensors on aircraft. Variable-rate "
                 "technology then targets the interventions."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) Sustainable, organic and biodynamic viticulture compared"),
 P("The three approaches sit on a continuum, not in opposition \u2014 each incorporates elements of "
   "the one before it."),
 P("<b>Sustainable viticulture</b> has three themes \u2014 economic, social, environmental \u2014 though "
   "environmental is the primary concern here. It aims to promote natural ecosystems, maintain "
   "biodiversity, manage waste, minimise chemicals and energy use, and reduce viticulture's wider "
   "impact. Its method is knowledge-led timing: growers understand vine and pest lifecycles and "
   "monitor weather, so an outbreak like downy mildew is predicted and prevented rather than "
   "treated on a fixed calendar \u2014 fewer applications result. Integrated pest management (lutte "
   "raisonn\u00e9e) is central: thresholds are set, pests monitored, prevention established, and "
   "control used only if thresholds are exceeded and prevention has failed. The governing idea is "
   "the economic threshold \u2014 intervene only before damage exceeds the cost of intervening. IPM "
   "builds on organic insight but <i>will use chemicals when necessary</i>, and that willingness "
   "is what distinguishes it."),
 P("<b>Organic viticulture</b> shares techniques with sustainable \u2014 cover crops, compost, "
   "hedges, biodiversity \u2014 but prohibits synthetic fertilisers, fungicides, herbicides and "
   "pesticides outright. It is soil-oriented: compost gives slow nutrient release and improves "
   "structure and biomass, while natural fertilisers like animal dung restore balance, all aimed "
   "at vine health and disease resistance. Treatment continues: sulfur and copper sulfate against "
   "mildew, Bacillus subtilis competing with Botrytis cinerea for space on the grape, and "
   "pheromone-based sexual confusion disrupting moth and mealybug mating."),
 P("<b>Biodynamic viticulture</b>, from Rudolf Steiner and Maria Thun, includes organic practice "
   "and adds philosophy and cosmology, treating the farm as an organism connected to Earth, "
   "planets and air. Practices follow lunar cycles \u2014 cuttings on an ascending moon, "
   "planting and pruning on a descending one \u2014 with homeopathic preparations: 500, horn manure "
   "buried over winter and sprayed on soil to catalyse humus formation; 501, horn silica buried "
   "six months and sprayed on vines to encourage growth; 502\u2013508, compost starters. Demeter, the "
   "main certifier, requires organic certification as a baseline, making the hierarchy explicit."),
 P("The evidence must be reported honestly. Organic cost/benefit evaluation is at a very early "
   "stage \u2014 some studies show slightly lower yields, others attribute extra cost to labour, and "
   "cost varies by region since cool wet climates are harder to manage without sprays. "
   "Organic-versus-biodynamic research has been limited and inconclusive. Biodynamic advantages "
   "and disadvantages are said to include organic's, with costs little higher, mainly from "
   "labour."),

 answer_head("Part b) The case for and against certification"),
 P("Certification converts practice into a claim a buyer can rely on; the argument turns on "
   "whether that reliability is worth its cost."),
 P("The case for: <b>sustainable</b> is not a protected term and can promote wine without any "
   "real standard; <b>regenerative</b> is similarly undefined, so claims may be exaggerated. "
   "Certification closes that gap, and offers commercial advantage \u2014 the largest organic still "
   "wine markets (Germany, France, the UK, the USA, Sweden, Japan) are substantial. It is also "
   "procedural: organic certification requires a conversion period, so the label attests to "
   "sustained practice, not one good season."),
 P("The case against is cost and the limits of what certification proves. It adds cost \u2014 listed "
   "among organic's disadvantages \u2014 and the Regenerative Organic Alliance, like most bodies, "
   "charges fees. Consistency is a second problem: many organic bodies share principles but set "
   "slightly different standards, so some organically farmed wines face stricter rules than "
   "others, even though all should meet IFOAM standards. Demeter standards are similarly "
   "interpreted per national association."),
 P("The most serious objection: a standard can be set too low to mean much. New Zealand's scheme "
   "has near-universal grower uptake and is praised for cutting pesticide use \u2014 but criticised "
   "for too low a certification bar. High uptake and rigorous standards are in tension; a scheme "
   "cannot easily maximise both."),
 P("On balance, certification is most defensible where the term would otherwise be meaningless "
   "and the market will pay for the assurance. Where neither holds, a grower may reasonably adopt "
   "the practices without the label \u2014 the position many sustainable and regenerative growers "
   "occupy."),
 examiner_note([
   P("Part a) is organised around the relationship between the three approaches, not as separate "
     "systems, stating explicitly that biodynamic includes organic practice and Demeter requires "
     "organic certification as a baseline. It refuses to advocate: reporting the cost/benefit "
     "evidence as early-stage and the comparative research as inconclusive is the accurate "
     "position.", "box"),
   P("Part b) reaches a conditional judgement \u2014 certification is worth it under two named "
     "conditions \u2014 rather than listing pros and cons. New Zealand identifies a real tension "
     "between uptake and rigour: analysis, not recall.", "box"),
 ]),
]

q2 = [
 answer_head("Part a) Conventional viticulture and the monoculture it produced"),
 P("In the second half of the twentieth century viticulture, like other production-oriented "
   "farming, became in effect intensive fruit farming, widely adopted worldwide aside from "
   "small-scale artisan growing. Its aims were to raise production and cut labour, achieved "
   "through four means: mechanisation, chemical inputs, irrigation and clonal selection. Vineyards "
   "were kept weed-free by ploughing and herbicides, agrochemical use against pests and disease "
   "rose sharply, and mineral fertiliser use increased. The result: viticulture became a "
   "monoculture."),
 P("That monoculture brought real advantages: mechanised vineyard work, reduced competition from "
   "other plants, and the ability to tend one variety's specific needs \u2014 irrigation, nutrition, "
   "treatments \u2014 raising yields while cutting costs. For high-volume production these are not "
   "trivial gains."),
 P("The disadvantages follow the same uniformity. Monoculture plants are far more prone to "
   "disease and pests, needing more treatment: fungal disease spreads faster where every plant is "
   "identical, and all are hit simultaneously, not sequentially. Nutrients deplete with no natural "
   "ecosystem to replenish them, demanding more fertiliser \u2014 a self-reinforcing dependency. "
   "Residual chemicals can reach groundwater (water held underground in soil or bedrock) or the "
   "air, damaging the environment beyond the vineyard."),
 P("By the late twentieth century it was clear that regular pesticide spraying and routine "
   "mineral fertiliser use harmed soil quality, cost money, damaged the environment and risked "
   "harm to workers and consumers. Pressure came from growers, consumers and legislators alike, "
   "so the response has been both practical and regulatory."),

 answer_head("Part b) Precision viticulture: contribution and limits"),
 P("Precision viticulture, a branch of precision agriculture, answers a specific finding: "
   "experience and research show big variation in vine response even within one vineyard or "
   "plot, though growers have traditionally treated soil, pruning and treatment uniformly."),
 P("It works in three stages. Sensors collect data on soil, vine vigour, topography and growth \u2014 "
   "on aircraft (\u2018remote\u2019) or mounted on a tractor or harvester (\u2018proximal\u2019). GPS and GIS "
   "then map that data visually. Variable-rate application technology targets interventions "
   "accordingly, down to plot level or smaller. Every key intervention can work this way \u2014 "
   "pruning, leaf removal, treatments, irrigation, thinning, harvesting \u2014 aiming at best quality "
   "and yield, lower environmental impact and, where possible, lower cost. Examples: changing "
   "rootstock halfway along a row as soil fertility shifts, or more leaf-stripping where vigour "
   "runs high."),
 P("Its environmental contribution is direct, not incidental: matching treatment and irrigation "
   "rates to local need, rather than applying them uniformly, cuts total input use, most "
   "effectively where data drives rates systematically. It is consequently often used within "
   "sustainable or organic viticulture rather than as an alternative. It also seeks to reduce "
   "variation, not just respond to it, and can identify quality zones within one vineyard, with "
   "implications for selective harvest and blending."),
 P("The limits are economic, not technical. Precision viticulture needs considerable upfront "
   "investment in sensors and software, viable only at large scale or on high-value smaller "
   "estates \u2014 hence its concentration in California and Australia. Remote data collection, "
   "sensors, software, and the consultancy or trained staff to interpret the data all cost money. "
   "That last point is most overlooked: data has no value until someone competent turns it into "
   "action, so expertise is as real a barrier as equipment."),
 examiner_note([
   P("Part a) derives monoculture's disadvantages from its uniformity rather than listing them, "
     "and notes the self-reinforcing fertiliser dependency. Defining groundwater in passing costs "
     "one clause and shows precision.", "box"),
   P("Part b) separates technical capability from economic accessibility \u2014 the right axis here \u2014 "
     "and flags the interpretation cost as the under-recognised barrier. Noting precision "
     "viticulture is often used <i>within</i> sustainable or organic viticulture avoids treating "
     "it as a rival system.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="Grape growers seeking to reduce chemical use have three main options available to them.",
      parts=[("Compare sustainable, organic and biodynamic viticulture, explaining the "
              "distinctive features of each.", "15%"),
             ("Evaluate the case for and against seeking certification.", "10%")],
      answer=q1),
 dict(stem="Approaches to grape growing have changed considerably since the mid-twentieth century.",
      parts=[("Explain what is meant by conventional viticulture and evaluate the advantages and "
              "disadvantages of the monoculture it produced.", "15%"),
             ("Explain how precision viticulture works, and assess its contribution and its "
              "limits.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch4_Approaches_to_Grape_Growing.pdf",
      "Chapter Four \u00b7 Approaches to Grape Growing", s, exam, maxpages=19)
