# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 6 — Managing Nutrients and Water"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Six: Managing Nutrients and Water",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 6.1 Managing Soil Health \u00b7 6.2 Nutrient "
        "Management \u00b7 6.3 Water Management")

s.append(P("This chapter is the grower's toolkit for two problems set up earlier: the vine "
           "needs water and nutrients <b>at the right time</b>, and the environment rarely "
           "supplies exactly the right amount. Almost every technique here does more than "
           "one job \u2014 a weed control method also changes vigour, frost risk and soil "
           "structure at once \u2014 and the exam rewards naming all of them."))
s.append(P("Reliably examined: <b>compare and evaluate weed control methods</b>, including "
           "organic/biodynamic compatibility; <b>irrigation system choice and water "
           "quality</b>; and <b>regulated deficit irrigation</b> as a named, precisely timed "
           "technique, not just \u2018less water\u2019. Treat every method as a trade-off with a "
           "stated cost."))

# ================================================================ soil health
s.append(H2("1. Managing Soil Health"))
s.append(P("<b>Soil health</b> = the continued capacity of the soil to act as a living "
           "ecosystem sustaining plants, animals and humans. Four related factors:", "note"))
s += BUL([
    "<b>Structure</b> \u2014 good drainage, sufficient water-holding capacity and oxygen, "
    "resistance to erosion, roots able to penetrate to depth.",
    "<b>Organic matter and humus</b> \u2014 decomposing matter supplies nutrients; humus improves "
    "structure and water-holding capacity.",
    "<b>Living organisms</b> \u2014 earthworms and microbes break organic matter into humus and "
    "the inorganic nutrients the vine can use.",
    "<b>Total available nutrients</b> the vine needs to grow and ripen fruit successfully.",
])
s.append(P("Poor soil health causes poor nutrient and water availability and uptake, and so "
           "poor growth and ripening. Growers test soil at establishment and then "
           "<b>annually</b>, correcting structure or nutrient levels as needed.", "note"))

# ================================================================ nutrient management
s.append(H2("2. Nutrient Management"))
s.append(P("Techniques split three ways: <b>direct nutrient application</b>, <b>promoting "
           "biological activity and structure</b>, and <b>weed management</b> \u2014 unwanted "
           "plants competing with the vine for both nutrients and water. Most techniques serve "
           "more than one of these at once.", "note"))

s.append(H3("Fertilisers"))
s.append(P("Applied before planting to help young vines establish, or to established vineyards "
           "to correct a detected deficiency. <b>Excess fertiliser risks excess vigour and an "
           "unbalanced vine.</b>", "note"))
s.append(EXHIBIT("EXHIBIT 6.1 \u2014 ORGANIC VERSUS MINERAL FERTILISERS", [
    ["", "Organic", "Mineral (inorganic / synthetic)"],
    ["Source", "Fresh or composted plant or animal material \u2014 manure, slurry; or a mown "
     "cover crop turned into the soil (<b>green manure</b>)", "Minerals extracted from the "
     "ground, or manufactured synthetic chemicals"],
    ["Nutrient form", "<b>Organic</b> \u2014 must be broken down by soil organisms before the "
     "vine can use it", "<b>Inorganic already</b> \u2014 more readily available to the vine"],
    ["Precision", "Broad \u2014 harder to target a single deficiency",
     "Can supply a single nutrient or several \u2014 more tailored"],
    ["Soil benefit", "Often high in humus \u2014 improves structure and water retention; feeds "
     "soil organisms", "No benefit to soil organisms or structure"],
    ["Cost", "Cheap or free to obtain, but bulky \u2014 <b>expensive to transport and spread</b>, "
     "and must be incorporated into the soil (labour)", "More expensive to buy, but "
     "concentrated \u2014 <b>cheap to transport and distribute</b>"],
    ["Release", "Gradual, as organisms break it down \u2014 can be an advantage", "Immediate"],
], [56, (W - 56) * 0.48, (W - 56) * 0.52], keep=False))

s.append(H3("Weed Control"))
s.append(P("Removing weeds is usually wanted beyond the nutrient/water competition itself: "
           "<b>bare, moist soil</b> absorbs heat by day and releases it at night, "
           "<b>reducing frost risk</b> \u2014 weeds, cover crops and mulches all raise it. Some "
           "weeds also block machinery and personnel (stinging nettles, brambles).", "note"))
s.append(EXHIBIT("EXHIBIT 6.2 \u2014 FIVE METHODS OF WEED CONTROL, COMPARED", [
    ["Method", "Chemical?", "Effect on vigour", "Standout advantage", "Standout disadvantage"],
    ["<b>Cultivation</b>", "No", "<b>Raises</b> — removes competition",
     "Incorporates fertiliser/cover crop in the same pass",
     "Damages soil structure; buries seeds, encouraging regrowth"],
    ["<b>Herbicides</b>", "<b>Yes</b>", "<b>Raises</b> — removes competition",
     "Cheap, highly effective, less damaging to structure than cultivation",
     "<b>Not permitted organic/biodynamic</b>; resistance risk (glyphosate-resistant ryegrass)"],
    ["<b>Animal grazing</b>", "No", "Not stated — depends on grazing intensity",
     "Provides manure; a meat source", "Vines need high training or timed grazing; animal "
     "care and pesticide vulnerability"],
    ["<b>Cover crops</b>", "No", "<b>Lowers</b> — adds competition",
     "Also fights erosion, adds biodiversity, gives a driving surface",
     "Unsuited to steep slopes (slippery wet); hard to mow near the trunk"],
    ["<b>Mulching</b>", "No", "<b>Raises</b> — removes competition",
     "Cuts evaporation; eventual nutrient/humus source",
     "Bulky — costly to transport; needs a thick layer to work"],
], [78, 46, 92, W - 78 - 46 - 92], keep=False))
s.append(P("All five reduce nutrient/water competition from weeds. What differs is what each "
           "substitutes — a chemical for the weed, or more competition for less.", "note"))
s.append(EXHIBIT("EXHIBIT 6.3 \u2014 THE THREE HERBICIDE TYPES", [
    ["Type", "Mechanism"],
    ["<b>Pre-emergence</b>", "Sprayed before weeds establish; persists in the surface soil, "
     "absorbed by roots, inhibits seedling germination"],
    ["<b>Contact</b>", "Sprayed on established weeds; kills only the green parts it touches"],
    ["<b>Systemic</b>", "Sprayed on established weeds, taken in by the leaves; travels through "
     "the sap and kills the <b>whole plant</b>"],
], [88, W - 88], keep=False))

# ================================================================ water management
s.append(H2("3. Water Management"))
s.append(P("Irrigation is necessary, and should be designed into establishment, where growing-"
           "season rainfall is low or soils are very free-draining. Retrofitting an established "
           "vineyard is far harder \u2014 pipes disrupt existing rows. <b>Some EU GIs ban "
           "irrigation outright, or allow it only for emergencies</b> \u2014 establishing young "
           "vines, drought threatening livelihoods.", "note"))
s.append(H3("Water Quality and Efficient Use"))
s += BUL([
    "<b>High dissolved solids</b> (mud) block drip and sprinkler systems \u2014 needs settling "
    "and filtering first.",
    "<b>High salinity</b> (common in parts of Australia) raises soil salt, impeding root water "
    "uptake \u2014 the vine dehydrates, green parts wilt and eventually die. Worse under "
    "<b>drip</b> irrigation, where salt accumulates at the root zone rather than being washed "
    "deeper, as flood irrigation would.",
    "Efficiency measures: <b>dripper systems + regulated deficit irrigation</b>; drought-"
    "tolerant varieties (Grenache) and rootstocks (140R); mulch to cut evaporation; weed "
    "removal to cut competition; humus to improve retention; deep-rooting cultivation. Winery "
    "wash water can sometimes be reused for irrigation too.",
])
s.append(FIGURE("FIGURE 6.1 \u2014 HOW EACH SYSTEM DELIVERS WATER", IrrigationProfile()))
s.append(EXHIBIT("EXHIBIT 6.4 \u2014 TYPES OF IRRIGATION", [
    ["Type", "Method", "Notes"],
    ["<b>Drip</b>", "Narrow pipes along each row, drippers spaced away from the trunk so roots "
     "grow out to seek water", "By far the <b>most common</b>. Economical, controllable "
     "row-by-row, can carry fertiliser (<b>fertigation</b>), usable on slopes. High "
     "installation cost, needs clean water and maintenance against blockage. <b>Cannot give "
     "frost protection</b> \u2014 drippers sit below the green parts of the vine"],
    ["<b>Flood</b>", "Water stored behind a sluice, released to flood the vineyard", "Cheap to "
     "install and run, but <b>inefficient</b> \u2014 much water is never taken up. Flat or "
     "gently sloping land only"],
    ["<b>Channel</b>", "Water flows down furrows dug between rows", "More efficient than flood. "
     "Common in <b>Argentina</b>, fed by abundant Andean water; unsuited where supply is "
     "limited"],
    ["<b>Overhead sprinkler</b>", "Pumped and showered over the vineyard", "Expensive to install "
     "and run (high pressure needed), uses more water than drip \u2014 but <b>doubles as frost "
     "protection</b>"],
], [96, (W - 96) * 0.46, (W - 96) * 0.54], keep=False))

s.append(H3("Regulated Deficit Irrigation (RDI)"))
s.append(P("Deliberately timed, controlled water stress \u2014 not simply \u2018less water\u2019.",
           "note"))
s.append(FlowChart([
    ("THE WINDOW", "Deficit imposed specifically <b>between fruit set and v\u00e9raison</b>",
     None),
    ("THE MECHANISM", "Mild to moderate stress halts further shoot growth, redirecting the "
     "vine toward grape development", None),
    ("THE RESULT", "<b>Smaller berries</b> \u2014 higher skin-to-juice ratio \u2014 more "
     "concentrated <b>anthocyanins and tannins</b>, often read as a quality signal. Favoured "
     "for black grapes", None),
], box_w=W * 0.80))
s += BUL([
    "Delivered by a <b>dripper system</b> for precise control. Easiest in <b>dry-season, "
    "sandy or loam soil</b> regions that dry and re-wet quickly; much harder with heavy spring "
    "rain or heavy clay soils that stay wet.",
    "Timing and soil-moisture monitoring are critical \u2014 mild stress in the window helps, "
    "but <b>prolonged or extreme stress cuts both yield and quality</b>.",
    "Even done well, RDI <b>usually lowers yield</b>: the grower must be confident the quality "
    "gain justifies the smaller crop. Extra cost is the monitoring equipment, assuming drip "
    "irrigation already exists.",
    "<b>Dry farming</b> \u2014 not irrigating at all, in a low-rainfall growing season \u2014 is "
    "a distinct choice, sometimes forced rather than chosen, with the same yield-down/quality-"
    "up trade-off.",
])

s.append(H3("Drainage"))
s.append(P("Where rainfall is plentiful and soil is not free-draining, artificial drainage may "
           "be needed \u2014 practical <b>only before planting</b>. Cost is usually offset by "
           "healthier, better-balanced vines that ripen consistently, plus a firmer surface for "
           "machinery (better grip, less compaction from driving on wet soil). Water can also be "
           "regulated by <b>cover crops competing for it</b>, or by <b>removing plough pans</b> "
           "that impede drainage.", "note"))

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER SIX", [
    P("<b>1. Name every function, not just the obvious one.</b> A cover crop is a weed "
      "control method, a vigour lever, an erosion control, a biodiversity measure and a "
      "driving surface at once \u2014 state as many as the question rewards.", "box"),
    P("<b>2. Track vigour by what each method substitutes.</b> Removing weed competition "
      "(cultivation, herbicides, mulching) tends to <i>raise</i> vigour; adding competition "
      "(cover crops) <i>lowers</i> it. This is the axis the exam tests, not \u2018good vs "
      "bad\u2019.", "box"),
    P("<b>3. State RDI's window precisely.</b> Fruit set to v\u00e9raison, not \u2018during "
      "ripening\u2019 \u2014 the timing is the mechanism, and vague timing loses the mark.",
      "box"),
    P("<b>4. Use the frost-risk counter-intuition.</b> Bare moist soil <i>reduces</i> frost "
      "risk by absorbing and releasing heat; weeds, cover crops and mulch all <i>raise</i> it "
      "\u2014 a genuinely surprising, testable point.", "box"),
    P("<b>5. Separate water quantity from water quality.</b> Salinity is an independent "
      "problem from drought, worse under drip than flood irrigation specifically because of "
      "where the salt accumulates.", "box"),
]))

s.append(exam_traps([
 ("Assuming cultivation and herbicides are risk-free just because they're effective.",
  "Cultivation <b>damages soil structure</b> and buries seeds, encouraging weeds back; "
  "herbicides risk <b>resistance</b> and are <b>banned in organic/biodynamic</b> viticulture."),
 ("Treating vigour effects as uniform across weed control methods.",
  "Methods that <b>remove</b> competition (cultivation, herbicides, mulching) tend to "
  "<b>raise</b> vigour; <b>cover crops</b>, which <b>add</b> competition, <b>lower</b> it."),
 ("Treating EU GI irrigation rules as a blanket ban.",
  "Many restrict rather than ban outright \u2014 emergency use for young vines or "
  "livelihood-threatening drought is often permitted."),
 ("Assuming any irrigation system can double as frost protection.",
  "<b>Drip cannot</b> \u2014 drippers sit below the green parts. <b>Overhead sprinklers "
  "can.</b>"),
 ("Assuming successful RDI maintains yield.",
  "It <b>usually lowers yield</b> even when done well \u2014 the grower is trading volume for "
  "concentration, and must be confident the trade is worth it."),
]))

# ================================================================ exam
exam = []

MCQ = [
 dict(q="Soil health is best described as:",
      opts=["The absence of any weeds or pests in the vineyard soil",
            "The continued capacity of the soil to act as a living ecosystem sustaining plants, "
            "animals and humans",
            "A soil's total nutrient content measured by laboratory test",
            "A soil's suitability for mechanisation"],
      ans=1, why="The textbook's own definition. The other options are single components, not "
                 "the whole picture."),
 dict(q="A key advantage of organic fertilisers over mineral fertilisers is that they:",
      opts=["Release nutrients to the vine immediately",
            "Can be precisely tailored to a single detected deficiency",
            "Are often high in humus, improving soil structure and water retention",
            "Never need to be incorporated into the soil"],
      ans=2, why="Humus content and the soil-organism benefit are organic fertiliser's "
                 "distinguishing advantages. Mineral fertilisers are the more tailored, "
                 "immediately available option."),
 dict(q="Removing weeds from the vineyard floor reduces frost risk chiefly because:",
      opts=["Weeds attract frost-carrying insects",
            "Bare, moist soil absorbs more heat by day and releases it at night",
            "Weeds block cold air drainage down a slope",
            "Weed roots compete with vine roots for antifreeze compounds"],
      ans=1, why="The stated mechanism is heat absorption and night-time release from bare "
                 "moist soil. Weeds, cover crops and mulches all work against this."),
 dict(q="A stated disadvantage of cultivation as a weed control method is that it:",
      opts=["Is not permitted in organic or biodynamic viticulture",
            "Cannot incorporate fertiliser into the soil",
            "Buries weed seeds, which encourages them to grow back",
            "Increases the risk of glyphosate-resistant weeds"],
      ans=2, why="Burying seeds while disturbing the soil is cultivation's specific "
                 "disadvantage. It IS permitted in organic/biodynamic viticulture, unlike "
                 "herbicides, and CAN incorporate fertiliser."),
 dict(q="A systemic herbicide differs from a contact herbicide in that it:",
      opts=["Is sprayed only before weeds establish",
            "Kills only the green parts of the weed it touches",
            "Travels through the sap to kill the whole plant",
            "Cannot be used on established weeds"],
      ans=2, why="Systemic herbicides are taken in by the leaves and travel through the sap, "
                 "killing the whole plant. Contact herbicides kill only what they touch."),
 dict(q="Cover crops are generally unsuited to steeply sloping vineyards because they:",
      opts=["Compete too strongly for sunlight",
            "Are slippery underfoot when wet",
            "Cannot be mown near the vine trunks",
            "Increase vine vigour excessively on slopes"],
      ans=1, why="The stated reason is that cover crops become slippery when wet on steep "
                 "slopes \u2014 a safety and workability issue, not a competition one."),
 dict(q="A material with a high nutrient content might specifically be chosen as mulch in:",
      opts=["A nutrient-poor vineyard",
            "A vineyard already showing excess vigour",
            "A vineyard using regulated deficit irrigation",
            "A vineyard on steeply sloping land"],
      ans=0, why="The textbook gives this as the reasoning: nutrient-poor vineyards can choose "
                 "a higher-nutrient mulch material deliberately."),
 dict(q="Which irrigation type cannot be used to protect the vine from frost?",
      opts=["Overhead sprinklers", "Flood irrigation", "Drip irrigation", "Channel irrigation"],
      ans=2, why="Drip lines sit below the green parts of the vine, so they cannot deliver the "
                 "aspersion effect frost protection needs. Overhead sprinklers can."),
 dict(q="Regulated deficit irrigation (RDI) imposes water stress principally during which "
        "window?",
      opts=["Budburst to flowering", "Flowering to fruit set", "Fruit set to v\u00e9raison",
            "V\u00e9raison to harvest"],
      ans=2, why="Fruit set to v\u00e9raison is the stated window \u2014 timed to halt further "
                 "shoot growth and favour grape development."),
 dict(q="Artificial vineyard drainage is best installed:",
      opts=["At any point in the vineyard's productive life",
            "Only before the vineyard is planted",
            "Only after a season of waterlogging is observed",
            "Only in vineyards using drip irrigation"],
      ans=1, why="The textbook states this can only practically be done before planting \u2014 "
                 "installing drainage under established vines is not viable."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) Comparing weed control methods for organic/biodynamic suitability"),
 P("Five methods are available, and they split cleanly by whether they use chemicals \u2014 "
   "the line that decides organic and biodynamic eligibility."),
 P("<b>Cultivation</b> (ploughing to disturb weed roots) and <b>mulching</b> (spreading "
   "biodegradable matter to suppress growth) use no chemicals and are both permitted. "
   "Cultivation also incorporates fertiliser and mown cover crops in the same pass, but "
   "repeated tillage damages soil structure and ecology, disturbing earthworm habitats and "
   "burying weed seeds \u2014 encouraging the very regrowth it aims to prevent. Mulch "
   "ultimately supplies nutrients and humus, but is bulky and costly to transport, and only "
   "effective applied thickly."),
 P("<b>Cover crops</b> and <b>animal grazing</b> are likewise chemical-free and permitted. "
   "Cover crops add competition for water and nutrients \u2014 useful to restrain vigour "
   "deliberately, and they also fight erosion, add biodiversity and improve the driving "
   "surface in high-rainfall climates \u2014 but that same competition can excessively reduce "
   "vigour on poor, dry soils, mowing near the trunk is difficult, and steep slopes become "
   "slippery when wet. Grazing needs vines trained high enough that animals cannot reach the "
   "fruit, or timed outside the growing season, and the animals need care and are vulnerable "
   "to vineyard pesticides."),
 P("<b>Herbicides</b> are the exception: cheap, highly effective, less damaging to soil "
   "structure than cultivation \u2014 but <b>not permitted in organic or biodynamic "
   "viticulture</b> at all, and risk operator, consumer and environmental poisoning, plus "
   "resistance, as with glyphosate-resistant ryegrass in South Africa."),
 P("A second axis cuts across the first: methods that <i>remove</i> weed competition "
   "(cultivation, herbicides, mulching) risk pushing vigour <i>too high</i>, since nothing "
   "competes with the vine \u2014 not a problem on naturally low-vigour sites, but a real one "
   "on fertile soil. Cover crops alone add competition back."),

 answer_head("Part b) Timing water to influence quality"),
 P("Water's effect on quality depends less on total volume than on <i>when</i> it is "
   "available, since the vine's needs shift through the cycle."),
 P("A plentiful spring supply builds a large leaf surface area to support later yield. From "
   "<b>fruit set to v\u00e9raison</b>, the calculus reverses \u2014 mild water stress here is "
   "often desirable, halting further shoot growth and redirecting the vine toward grape "
   "development rather than vegetative growth competing for the same sugars."),
 P("<b>Regulated deficit irrigation</b> formalises this: a dripper system precisely times "
   "and regulates mild-to-moderate stress within that window. Smaller berries result, "
   "raising the skin-to-juice ratio and so the concentration of anthocyanins and tannins \u2014 "
   "often read as a quality signal, particularly favoured for black grapes. The technique is "
   "easiest on sandy or loam soils in a dry growing season, since they dry and re-wet "
   "quickly under control; heavy clay or frequent rain makes precise timing far harder."),
 P("The trade-off must be stated plainly: even successful RDI usually <b>lowers yield</b>, "
   "so the grower needs confidence the quality gain is worth the smaller crop. Timing isn't "
   "forgiving either \u2014 prolonged or extreme stress, rather than the intended mild dose, "
   "cuts yield and quality together. Growers without irrigation at all may achieve a similar "
   "effect, deliberately or not, through <b>dry farming</b>."),
 examiner_note([
   P("Part a) uses two crossing axes \u2014 chemical/non-chemical for eligibility, remove/add "
     "competition for the vigour effect \u2014 rather than five isolated pro/con lists, which "
     "is what turns recall into a structured comparison.", "box"),
   P("Part b) answers the question actually asked (timing, not just \u2018water helps quality\u2019) "
     "by naming the fruit-set-to-v\u00e9raison window explicitly and tying RDI's mechanism to a "
     "named consequence \u2014 skin-to-juice ratio \u2014 rather than asserting quality "
     "improves without saying why.", "box"),
 ]),
]

q2 = [
 answer_head("Part a) Choosing an irrigation system"),
 P("Four systems are available, and the choice weighs cost, control, water efficiency and "
   "site constraints against each other \u2014 no system wins on every criterion."),
 P("<b>Drip irrigation</b> is by far the most common: narrow pipes along each row deliver "
   "water through drippers positioned away from the trunk, encouraging roots to grow out "
   "and seek it. It is economical, controllable row by row or block by block \u2014 supporting "
   "tailored management and so potentially higher yield and quality \u2014 usable on slopes, "
   "and can double as a fertiliser delivery system (<b>fertigation</b>). Its costs are high "
   "installation, a need for clean water, and gradual blockage by algae, bacteria or "
   "minerals even with clean water. Critically, <b>it cannot protect against frost</b>, "
   "since the drippers sit below the green parts of the vine."),
 P("<b>Flood</b> and <b>channel</b> irrigation are cheaper to install and maintain but far "
   "less efficient, since much of the water is never taken up; both need flat or gently "
   "sloping land, and channel irrigation \u2014 water run down furrows between rows \u2014 is "
   "somewhat more efficient than flooding the whole vineyard. Both depend on abundant, "
   "reliable water, as in Argentina's Andean-fed systems, and are unsuited where supply is "
   "limited. <b>Overhead sprinklers</b> are expensive to install and run, given the pressure "
   "required, and use more water than drip \u2014 but uniquely <b>double as frost "
   "protection</b>."),
 P("The decision turns on the site: water scarcity and a need for precision point to drip; "
   "abundant cheap water and flat land make flood or channel viable; frost risk may justify "
   "overhead sprinklers despite the cost, or drip installed alongside a separate frost-"
   "protection method."),

 answer_head("Part b) Water quality and drip efficiency"),
 P("Water quality is a separate axis from water quantity, and can undermine an irrigation "
   "system regardless of how much water is available."),
 P("Water carrying <b>high dissolved solids</b>, such as mud, blocks drip and sprinkler "
   "systems and needs settling and filtering first. <b>High salinity</b> \u2014 a significant "
   "problem in parts of Australia \u2014 raises soil salt, making it harder for roots to take up "
   "water; the vine dehydrates and its green parts wilt and eventually die. The problem is "
   "<b>worse specifically under drip</b>, because salt accumulates at the root zone rather "
   "than being washed deeper, as flood irrigation would achieve simply through the volume "
   "applied."),
 P("Growers using drip can still improve efficiency: pairing it with <b>regulated deficit "
   "irrigation</b> and careful monitoring of vine water take-up; choosing drought-tolerant "
   "varieties (Grenache) or rootstocks (140R); mulch to cut evaporation; removing weeds to "
   "eliminate competing water use; building humus for better natural retention; and "
   "encouraging deep root growth through cultivation, so vines draw on a larger soil water "
   "reserve. Winery wash water may also be treated and reused for irrigation."),
 examiner_note([
   P("Part a) organises around genuine trade-offs \u2014 cost against control against site "
     "constraint \u2014 and closes with a decision rule linking system choice back to site "
     "conditions, rather than four unconnected system descriptions.", "box"),
   P("Part b) keeps quality and quantity separate throughout, and explains <i>why</i> drip "
     "makes salinity worse (accumulation at the root zone) rather than simply asserting that "
     "it does \u2014 the mechanism is what earns the mark.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="Most techniques for managing nutrients and water in the vineyard serve more than "
           "one purpose at once.",
      parts=[("Compare the methods of weed control available to a grape grower, and evaluate "
              "their suitability for organic and biodynamic viticulture.", "15%"),
             ("Explain how the timing of irrigation, or its deliberate withholding, can be used "
              "to influence grape quality.", "10%")],
      answer=q1),
 dict(stem="Water availability significantly influences vine growth and grape quality.",
      parts=[("Explain the factors a grape grower should consider when choosing an irrigation "
              "system.", "15%"),
             ("Explain the causes and consequences of poor water quality in irrigation, and how "
              "a grower using drip irrigation can improve the efficiency of water use.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch6_Managing_Nutrients_and_Water.pdf",
      "Chapter Six \u00b7 Managing Nutrients and Water", s, exam, maxpages=18)
