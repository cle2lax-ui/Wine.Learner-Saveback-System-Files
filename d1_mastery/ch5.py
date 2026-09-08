# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 5 — Vineyard Establishment"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Five: Vineyard Establishment",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 5.1 Site Selection \u00b7 5.2 Soil Preparation \u00b7 5.3 Planting Materials")

s.append(P("The chapter's own opening sentence is the exam thesis: decisions made at establishment "
           "are <b>difficult to rectify once the vineyard is planted</b>, so compromises here \u2014 "
           "through cost or time \u2014 cause problems for the vineyard's whole life. Frame every "
           "answer by irreversibility."))
s.append(P("Reliably examined: <b>the factors influencing site selection</b>, where as many marks "
           "sit in the logistical, legal and cost factors as in the natural ones; <b>rootstock "
           "selection</b>, where parentage maps to property; and <b>terroir</b>, which must be "
           "handled with the scientific caveat intact. A detailed <b>site assessment</b> determines "
           "suitability and what must be done before planting."))

# ---------------------------------------------------------------- site selection
s.append(H2("1. Site Selection"))
s.append(P("<b>The style, quality and price of the wines to be made is a key influence on site "
           "selection \u2014 and vice versa.</b> That reciprocal relationship is the analytical hinge.",
           "note"))
s.append(FIGURE("FIGURE 5.1 \u2014 SITE SELECTION: PRICE POINT AGAINST CLIMATE", Matrix2x2(
    "High volume / inexpensive", "Premium / super-premium", "Cool climate", "Warm climate",
    {"tl": ("Warm \u00b7 inexpensive",
            "<b>Flat, fertile, warm, dry</b> \u2014 Central Valley of Chile. Fertile soils, warmth and "
            "irrigation ripen high yields; dry climate cuts fungal disease, saving fungicide and "
            "winery sorting; flat land allows mechanisation."),
     "tr": ("Warm \u00b7 premium",
            "Seek <b>relatively cool</b> sites for balance \u2014 high altitude (L\u00fajan de Cuyo) or "
            "cooling sea breezes (Casablanca)."),
     "bl": ("Cool \u00b7 inexpensive",
            "The hardest square. Ripening risk plus low margin; consistent healthy yields are "
            "difficult to guarantee cheaply."),
     "br": ("Cool \u00b7 premium",
            "Maximise ripening potential \u2014 aspects receiving most sunshine through the day, as in "
            "the Rheingau.")},
    height=182, x_axis="the style, quality and price of the wine drives the choice \u2014 and vice versa")))
s.append(H4("LOGISTICAL, LEGAL AND COST FACTORS \u2014 WHERE MOST MARKS ARE LEFT ON THE TABLE"))
s += BUL([
    "<b>Land price.</b> Land in desirable GIs \u2014 Burgundy Grand Crus such as <b>Clos des "
    "Lambrays</b> \u2014 costs far more than land qualifying only as <b>Vin de France</b>.",
    "<b>Location, layout, topography.</b> A <b>frost pocket</b> gives less reliable yields and "
    "slower return on investment, or needs costlier frost protection. Sites known for particular "
    "diseases or pests pose the same problem.",
    "<b>Steep slopes</b> may be unsuitable for mechanisation, and labour can be <b>expensive, "
    "slow-paced and hard to attain</b>.",
    "<b>Irrigation</b> \u2014 the source of the water and its cost.",
    "<b>Access and distance from the winery</b>, so grapes arrive healthy with limited risk of "
    "<b>oxidation and microbial spoilage</b>.",
    "<b>Proximity to towns and cities</b> \u2014 labour, supplies, cellar door, retail, distribution.",
    "<b>Law.</b> <b>PDO</b> rules stipulate permitted <b>varieties, maximum yields, and viticultural "
    "and winemaking practices</b>. Buying expensive PDO land intending a wine that will be "
    "<b>declassified</b> is a business risk unlikely to return the investment.",
])
s.append(CALLOUT("THE COMMERCIAL TEST BEHIND ALL OF IT", [
    P("The producer must get a <b>return on investment</b> from selling the grapes, must or wine. "
      "If the site is expensive to buy, establish and manage, they must be confident the product "
      "will sell at a price that delivers one.", "box"),
]))

s.append(H3("The Idea of Terroir"))
s.append(P("From <i>terre</i>, \u2018land\u2019. An overarching concept claiming the distinctiveness of "
           "quality wines is due to their <b>sense of place</b>. <b>No precise and agreed "
           "definition exists</b>, and the term is commonly used without being defined.", "note"))
s.append(EXHIBIT("EXHIBIT 5.2 \u2014 FOUR USES, AND THEIR STANDING", [
    ["Use", "The claim", "Standing"],
    ["<b>Physical</b>", "Characteristics relate to the place \u2014 climate, soil, aspect, elevation. "
     "On the <b>C\u00f4te d'Or</b>, wines from vines a few hundred metres apart differ by slope, "
     "soil, aspect and drainage", "The <b>physical definition</b>"],
    ["<b>Cultural</b>", "Includes <b>human interventions</b> \u2014 French PDOs stipulating planting "
     "density, trellising", "Includes the physical but <b>goes beyond</b> it"],
    ["<b>Geological</b>", "Direct soil-geology influence \u2014 e.g. Chardonnay's chalkiness from "
     "chalky soils, implying uptake of taste-affecting elements",
     "<b>Strongly contested by the scientific community</b>"],
    ["<b>Obscured by winemaking</b>", "Over-ripe fruit and new oak can mask inherent character",
     "A view about <b>expression</b>, not mechanism"],
], [66, (W - 66) * 0.66, (W - 66) * 0.34], keep=False))
s.append(CALLOUT("WHY THE GEOLOGICAL CLAIM IS CONTESTED \u2014 THREE GROUNDS", [
    P("<b>Photosynthesis is the primary driver of vine growth</b> \u00b7 <b>all aroma compounds are "
      "synthesised in the vine</b> \u00b7 <b>grape must is further transformed by fermentation</b>. "
      "Together these leave no established pathway from a soil element to a flavour in the glass.",
      "box"),
]))
s.append(P("Long associated with French and other classic European wines (the <b>Mosel</b>), the "
           "concept now interests winemakers worldwide exploring <b>single vineyards or specific "
           "locations</b>, strengthened by <b>soil mapping technology</b>.", "note"))

# ---------------------------------------------------------------- soil prep
s.append(H2("2. Soil Preparation"))
s.append(P("Assess and potentially rectify: <b>drainage and structure</b>, <b>mineral "
           "composition</b>, <b>pests or unwanted plants</b>, and sometimes <b>topography</b>. "
           "<b>In nearly all cases rectifying problems now is easier than after planting.</b>",
           "note"))
s.append(EXHIBIT("EXHIBIT 5.3 \u2014 THE PREPARATION OPERATIONS", [
    ["Operation", "Purpose"],
    ["<b>Remove very large rocks</b>", "Structure governs root penetration, drainage, nutrient "
     "holding and workability"],
    ["<b>Subsoiling</b>", "Breaks down a <b>plough pan</b> \u2014 an impervious layer formed by years "
     "of ploughing at the same depth. Promotes <b>drainage</b> and easier later cultivation"],
    ["<b>Remove and burn old roots</b>", "Where vines or crops have been uprooted \u2014 roots can "
     "otherwise <b>harbour disease</b>"],
    ["<b>Systemic herbicides</b>", "Advisable where weeds are a particular problem"],
    ["<b>Manure, compost, fertilisers</b>", "Increase nutrients and organic matter; <b>ploughing</b> "
     "incorporates them into the soil"],
    ["<b>Adjust pH</b>", "For <b>acidic</b> soils (<b>Beaujolais</b>), <b>lime</b> is spread and "
     "<b>ploughed in</b> \u2014 surface-applied lime takes a long time to act"],
    ["<b>Landscaping</b>", "Substantial and costly work to change topography. On steep slopes "
     "(<b>Douro Valley</b>), <b>terraces</b> provide flat land for planting"],
], [104, W - 104], keep=False))

# ---------------------------------------------------------------- planting materials
s.append(H2("3. Planting Materials"))
s.append(H3("Grape Varieties"))
s.append(P("Over <b>one thousand</b> varieties are in commercial use. Six ways they are more or "
           "less adapted to climate:", "note"))
s.append(EXHIBIT("EXHIBIT 5.4 \u2014 CLIMATIC ADAPTATION OF VARIETIES", [
    ["Factor", "Consequence and named examples"],
    ["<b>Time of budding</b>", "<b>Early</b> (<b>Chardonnay</b>) is more at risk from spring frost "
     "than <b>late</b> (<b>Riesling</b>)"],
    ["<b>Duration of life-cycle</b>", "<b>Early ripening</b> (<b>Chardonnay, Pinot Noir</b>) suits "
     "<b>cool</b> climates, ripening before wet cold late autumn. <b>Late ripening</b> "
     "(<b>Mourv\u00e8dre</b>) suits <b>warm and hot</b>; early ripeners there gain sugar and lose acid "
     "too fast, giving unbalanced wines"],
    ["<b>Drought tolerance</b>", "<b>Grenache</b> withstands high water stress \u2014 southern "
     "<b>Rh\u00f4ne</b>, inland <b>Spain</b>, <b>McLaren Vale</b>"],
    ["<b>Disease resistance</b>", "<b>Cabernet Sauvignon is less susceptible to grey rot than "
     "Merlot</b> \u2014 one reason they blend usefully in maritime <b>Bordeaux</b>"],
    ["<b>Winter hardiness</b>", "<b>Vidal and Riesling</b> tolerate very cold winters \u2014 "
     "<b>Ontario, Finger Lakes</b>"],
    ["<b>Vigour</b>", "High vigour (<b>Sauvignon Blanc</b>) on fertile, well-watered soils needs "
     "managing to avoid excess shoot growth"],
], [96, W - 96], keep=False))
s.append(H4("NON-CLIMATIC FACTORS"))
s += BUL([
    "<b>Style</b> \u2014 a low tannin fruity red for early drinking points to <b>Gamay or Grenache</b>, "
    "not <b>Nebbiolo or Aglianico</b>.",
    "<b>Yield</b> \u2014 high yielding varieties (<b>Grenache</b>) or clones allow more wine at a set "
    "cost; a prime concern for inexpensive wines.",
    "<b>Cost</b> \u2014 <b>Pinot Noir</b> is prone to disease and needs more monitoring and spraying.",
    "<b>Law</b> \u2014 EU legislation restricts plantings; <b>Prosecco</b> must be predominantly "
    "<b>Glera</b>.",
    "<b>Availability</b> \u2014 strict <b>quarantine procedures</b> on new planting material; some "
    "varieties or clones are unavailable or sold out.",
    "<b>Market demand</b> \u2014 identify the demand and <b>route to market</b> first; fashions are "
    "pronounced, e.g. the success of <b>Sauvignon Blanc</b>.",
])
s.append(CALLOUT("HEAD GRAFTING (TOP GRAFTING)", [
    P("Cut the original vine at the trunk and graft a bud of a new variety on top. <b>Benefit:</b> "
      "with an established root system the new variety fruits <b>much sooner than a new "
      "planting</b>. <b>Disadvantage:</b> the rootstock was chosen for the <i>original</i> variety "
      "and may not suit the new one.", "box"),
]))
s.append(H3("Clones"))
s.append(P("Nursery vines may offer a choice of clones. Many of the same factors apply, but clone "
           "choice is <b>less impactful than variety</b> and <b>much less affected by legislation "
           "and consumer popularity</b>.", "note"))
s.append(H3("Rootstocks"))
s.append(P("The <b>vast majority</b> of vines are grafted, principally to protect against "
           "<b>phylloxera</b>. Characteristics are <b>usually linked to parentage</b> \u2014 many "
           "rootstocks being <b>hybrids of two species</b>.", "note"))
s.append(EXHIBIT("EXHIBIT 5.5 \u2014 ROOTSTOCK SELECTION CRITERIA", [
    ["Criterion", "Property", "Rootstocks and parentage"],
    ["<b>Pests</b>", "Phylloxera; some also <b>root-knot nematodes</b>",
     "<b>Ramsey, Dog Ridge</b> \u2014 <i>V. champini</i>"],
    ["<b>Water</b>", "<b>Drought</b> \u2014 roots deeply and quickly",
     "<b>110R, 140R</b> \u2014 <i>V. rupestris</i> \u00d7 <i>V. berlandieri</i>"],
    ["<b>Water</b>", "<b>Waterlogged</b> soil \u2014 high rainfall, water-retaining soils",
     "<b>Riparia Gloire</b> \u2014 <i>V. riparia</i>"],
    ["<b>Water</b>", "<b>Salinity</b> \u2014 dissolved salt", "<b>1103P</b> \u2014 <i>V. berlandieri</i>"],
    ["<b>Soil pH</b>", "<b>Acidic</b> soils", "<b>99R, 110R</b> \u2014 <i>V. rupestris</i> \u00d7 "
     "<i>V. berlandieri</i>"],
    ["<b>Soil pH</b>", "<b>High lime</b> content (high pH)", "<b>41B</b> \u2014 <i>V. berlandieri</i>"],
    ["<b>Vigour</b>", "<b>Low</b> \u2014 can <b>advance ripening</b>, useful in cool climates",
     "<b>420A, 3309C</b> \u2014 <i>V. riparia</i>"],
    ["<b>Vigour</b>", "<b>High</b> \u2014 boosts growth and yields on unfertile soils, dry conditions",
     "<b>140R</b> \u2014 <i>V. rupestris</i>"],
], [50, (W - 50) * 0.50, (W - 50) * 0.50], keep=False))
s.append(FIGURE("FIGURE 5.2 \u2014 CHOOSING A ROOTSTOCK BY VIGOUR AND SITE", Matrix2x2(
    "Low vigour", "High vigour", "Dry / unfertile", "Damp / fertile",
    {"tl": ("Low vigour \u00b7 damp fertile site",
            "<b>Riparia Gloire</b> (<i>V. riparia</i>) tolerates waterlogging. <b>420A, 3309C</b> "
            "restrain vigour and can <b>advance ripening</b> \u2014 useful in cool climates."),
     "tr": ("High vigour \u00b7 damp fertile site",
            "Rarely wanted: vigour on top of fertility gives shading, poor ventilation and delayed "
            "ripening."),
     "bl": ("Low vigour \u00b7 dry unfertile site",
            "Risks stunting. Drought tolerance matters more here \u2014 <b>110R, 140R</b> "
            "(<i>rupestris</i> \u00d7 <i>berlandieri</i>) root deeply and quickly."),
     "br": ("High vigour \u00b7 dry unfertile site",
            "<b>140R</b> (<i>V. rupestris</i>) boosts growth and yields. Also the sparkling-wine "
            "choice, where high yields with delicate aromas and high acidity beat concentration.")},
    height=182, x_axis="rootstock vigour")))

s.append(H3("Vine Age"))
s.append(FlowChart([
    ("FIRST 2\u20133 YEARS", "Inflorescences commonly <b>removed</b> so the vine concentrates on "
     "growth. Some GIs restrict fruit from very young vines", None),
    ("UP TO ~5 YEARS", "<b>Low yields</b> \u2014 root system not yet established", None),
    ("~10 TO 40 YEARS", "<b>Maximum yields</b>, depending on variety and conditions", None),
    ("BEYOND 40 YEARS", "Yield <b>decreases</b> as vigour decreases \u2014 the grower judges when it "
     "is <b>no longer profitable</b>", None),
    ("50 YEARS OR MORE", "Profitable in famous old vineyards \u2014 <b>Burgundy, Eden Valley</b> \u2014 at "
     "<b>super-premium</b> prices. Where medium to high yields are needed, old vines are "
     "<b>replaced</b>", None),
], box_w=W * 0.80))
s.append(H4("WHY OLD VINES MIGHT GIVE BETTER FRUIT \u2014 FOUR THEORIES, NOT A RULE"))
s += BUL([
    "They may have become <b>better balanced</b> and adapted to their environment.",
    "<b>Lower yields</b> may concentrate each grape \u2014 resources shared among fewer berries.",
    "More <b>old wood</b> means a bigger <b>carbohydrate store</b> for early season or stress.",
    "They may have <b>survived because they were well sited</b> \u2014 and growers keep the best vines "
    "longest before grubbing up and replanting.",
])
s.append(FIGURE("FIGURE 5.3 \u2014 AGE IS NOT THE VARIABLE THAT DECIDES QUALITY", Matrix2x2(
    "Young vine", "Old vine", "Poor site / badly maintained", "Well sited / well managed",
    {"tl": ("Young \u00b7 poor site or upkeep", "The weakest combination \u2014 neither age nor site "
            "is working in the vine's favour."),
     "tr": ("Young \u00b7 well sited and managed", "Can outperform an old vine on a poor site: "
            "<b>not a definitive rule</b> that age alone predicts quality."),
     "bl": ("Old \u00b7 poor site or upkeep", "Age and low yield do not compensate for a bad site \u2014 "
            "the popular assumption breaks down here."),
     "br": ("Old \u00b7 well sited and managed", "The classic premium expectation \u2014 Barossa, "
            "famous old Burgundy parcels \u2014 but site and management, not age alone, are doing "
            "much of the work.")},
    height=182, x_axis="too many confounding variables \u2014 clone, rootstock, irrigation, "
                        "training \u2014 for a clean comparison")))
s.append(P("<b>\u2018Old vines\u2019</b> \u2014 <i>vieilles vignes</i>, <i>vi\u00f1as viejas</i> \u2014 is <b>not "
           "regulated</b>: 30 years to one producer, 100 to another. Some regions classify them \u2014 "
           "<b>The Historic Vineyard Society</b> (California), <b>The Barossa Old Vine Charter</b> \u2014 "
           "often specifying a minimum age.", "note"))

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER FIVE", [
    P("<b>1. Frame everything by irreversibility.</b> Decisions here are hard to rectify after "
      "planting; soil problems are easier to fix before. That frame turns a list of operations into "
      "an argument about risk and sequencing.", "box"),
    P("<b>2. Answer site selection in two halves.</b> Natural factors decide whether the grapes can "
      "be grown; logistical, legal and cost factors decide whether it returns a profit.", "box"),
    P("<b>3. Map rootstock parentage to property.</b> <i>rupestris</i> \u00d7 <i>berlandieri</i> for "
      "drought and acidity \u00b7 <i>riparia</i> for waterlogging and low vigour \u00b7 <i>berlandieri</i> "
      "for lime and salinity \u00b7 <i>champini</i> for nematodes. Parentage <i>explains</i> the "
      "property.", "box"),
    P("<b>4. Handle terroir with the caveat intact.</b> Physical definition, cultural extension, "
      "then the three scientific grounds for contesting the geological claim.", "box"),
    P("<b>5. Present old vines as contested.</b> Four theories, confounding variables, not a "
      "definitive rule, unregulated term.", "box"),
]))

s.append(exam_traps([
 ("Answering site selection with natural factors only.",
  "Half the marks sit in the <b>logistical, legal and cost</b> factors: land price within "
  "desirable GIs, frost pockets and slower return on investment, mechanisation on steep slopes, "
  "irrigation water cost, distance from winery (oxidation and microbial spoilage), proximity to "
  "labour and markets, and PDO rules with the risk of <b>declassification</b>."),
 ("Stating that soil chemistry gives wine its flavour.",
  "The scientific community <b>strongly contests</b> this: photosynthesis is the primary driver of "
  "vine growth, <b>all aroma compounds are synthesised in the vine</b>, and must is further "
  "transformed by fermentation. Use the <b>physical</b> definition of terroir instead."),
 ("Muddling budding time with ripening time \u2014 again.",
  "<b>Chardonnay</b> is both early budding and early ripening; <b>Riesling</b> is <b>late "
  "budding</b> (frost-avoiding) and is cited here for <b>winter hardiness</b>, alongside "
  "<b>Vidal</b>. <b>Mourv\\u00e8dre</b> is the late-ripening example."),
 ("Assuming low vigour rootstocks are always the quality choice.",
  "Low vigour (420A, 3309C, <i>V. riparia</i>) advances ripening \u2014 useful in cool climates. But a "
  "<b>high vigour</b> rootstock may be deliberately chosen for <b>sparkling wine</b>, where high "
  "yields with delicate aromas and high acidity beat concentration."),
 ("Treating 'old vines' as a defined quality guarantee.",
  "The term is <b>not regulated</b> \u2014 30 years to one producer, 100 to another. The quality claim "
  "rests on <b>four theories</b>, and there are too many variables for direct comparison. A "
  "well-sited, well-trained young vine will likely beat a badly maintained old one."),
]))

# ---------------------------------------------------------------- exam
exam = []

MCQ = [
 dict(q="Which is given as a reason a flat, fertile site in a warm, dry climate suits high volume, inexpensive wine production?",
      opts=["It maximises the skin-to-pulp ratio of the fruit",
            "The dry climate reduces fungal disease, saving on fungicide and on sorting in the winery",
            "It guarantees a high diurnal range and therefore acid retention",
            "PDO rules generally require flat sites for high yielding varieties"],
      ans=1, why="Reduced fungal disease saves money on spraying and on grape sorting, and flat "
                 "land allows cheaper, quicker mechanisation."),
 dict(q="A vineyard sited in a frost pocket is principally a concern at site selection because it:",
      opts=["Cannot be certified organic",
            "May give less reliable yields and so slower return on investment, or need more expensive frost protection",
            "Will always require irrigation",
            "Is excluded from Protected Designation of Origin status"],
      ans=1, why="The textbook frames this as cost and return-on-investment, alongside sites "
                 "prone to particular pests or diseases."),
 dict(q="The claim that the perceived chalkiness of Chardonnay comes from vines grown in chalky soils is:",
      opts=["The physical definition of terroir",
            "The cultural definition of terroir",
            "Strongly contested by the scientific community",
            "Accepted where soil mapping technology has confirmed it"],
      ans=2, why="Photosynthesis drives vine growth, all aroma compounds are synthesised in "
                 "the vine, and must is further transformed by fermentation."),
 dict(q="Subsoiling is carried out before planting in order to:",
      opts=["Incorporate lime into acidic soils",
            "Break down a plough pan formed by years of ploughing at the same depth",
            "Remove old roots that could harbour disease",
            "Construct terraces on steep slopes"],
      ans=1, why="A plough pan is an impervious layer; breaking it aids drainage and later "
                 "cultivation. The other options are separate operations."),
 dict(q="Old roots removed before replanting must be burnt because they:",
      opts=["Would otherwise compete with new vines for nutrients",
            "Can harbour disease", "Interfere with subsoiling equipment",
            "Would raise the pH of the soil as they decompose"],
      ans=1, why="Harbouring disease is the reason \u2014 removal alone isn't enough; the roots "
                 "must be burnt."),
 dict(q="Which pair of varieties is cited for winter hardiness, suiting Ontario and the Finger Lakes?",
      opts=["Chardonnay and Pinot Noir", "Vidal and Riesling",
            "Grenache and Mourv\u00e8dre", "Cabernet Sauvignon and Merlot"],
      ans=1, why="Vidal and Riesling tolerate very cold winters. Riesling is also the late "
                 "budding example \u2014 a separate property."),
 dict(q="Rootstocks 110R and 140R are highly tolerant of drought because they:",
      opts=["Are based on Vitis champini",
            "Are hybrids of V. rupestris and V. berlandieri, able to root deeply and quickly",
            "Are based on V. riparia and therefore low in vigour",
            "Tolerate soils with high levels of dissolved salt"],
      ans=1, why="Parentage confers deep, quick rooting. V. champini gives nematode tolerance "
                 "(Ramsey, Dog Ridge); V. riparia gives waterlogging tolerance and low vigour; "
                 "1103P handles salinity."),
 dict(q="A grape grower might deliberately select a HIGH vigour rootstock in order to:",
      opts=["Advance ripening in a cool climate",
            "Produce high yields of grapes with delicate aromas and high acidity for sparkling wine",
            "Increase concentration of colour and tannin in a premium red",
            "Improve tolerance of soils with high lime content"],
      ans=1, why="Low vigour advances ripening in cool climates. High vigour suits sparkling "
                 "wine, where yield with delicate aromas and acidity outranks concentration."),
 dict(q="A vine typically produces its maximum yields between approximately:",
      opts=["3 and 10 years", "10 and 40 years", "40 and 60 years", "50 years and above"],
      ans=1, why="Vines up to about five years yield little; beyond roughly 40 years, yield "
                 "declines as vigour falls."),
 dict(q="The principal disadvantage of head grafting is that:",
      opts=["The new variety takes longer to fruit than a new planting",
            "The rootstock was selected for the original variety and may not suit the new one",
            "It cannot be used on vines older than ten years",
            "The resulting wine must be declassified under PDO rules"],
      ans=1, why="The benefit is speed \u2014 an established root system fruits much sooner than a "
                 "new planting, so option A inverts the true position."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) Factors influencing site selection"),
 P("Site selection determines a vineyard's growing environment, and because decisions at "
   "establishment are hard to rectify once vines are planted, the assessment must weigh natural, "
   "logistical, legal and commercial factors together. The governing relationship: the style, "
   "quality and price of the wine influence site selection \u2014 and site selection influences what "
   "wines are possible."),
 P("For <b>high volume, inexpensive or mid-priced wines</b>, the need is high yields of healthy "
   "grapes produced consistently and cheaply. A flat, fertile site in a warm, dry climate \u2014 "
   "Central Valley, Chile \u2014 may be ideal: fertile soils, warmth and irrigation ripen high "
   "yields; the dry climate cuts fungal disease, saving on fungicide and sorting; flat land allows "
   "cheaper, faster mechanisation."),
 P("For <b>premium or super-premium wines</b> the priority shifts to optimum composition \u2014 "
   "sugar, acidity, colour, tannins, aroma \u2014 not lowest cost. In cool climates, producers seek "
   "sites maximising ripening, such as the sunniest aspects in the Rheingau. In warm climates the "
   "logic inverts: relatively cool sites bring better balance \u2014 high altitude (L\u00fajan de Cuyo, "
   "Mendoza) or cooling sea breezes (Casablanca, Chile)."),
 P("Natural resources are not the whole assessment. <b>Logistical and cost</b> factors bear on "
   "it: land price varies enormously, with desirable GIs like Burgundy Grand Crus (Clos des "
   "Lambrays) far pricier than land qualifying only as Vin de France. Location, layout and "
   "topography carry costs, often tied to natural factors \u2014 a frost pocket means less reliable "
   "yields, slower return, or costly frost protection; pest- or disease-prone sites pose the same "
   "problem. Steep slopes may resist mechanisation, and labour can be expensive or scarce. "
   "Irrigation water source and cost need assessing. Access and distance from the winery matter, "
   "so grapes arrive with little oxidation or spoilage risk, and proximity to towns affects labour, "
   "supplies, cellar door, retail and distribution."),
 P("Finally, <b>legal</b> factors constrain the land. Many regions, especially in the EU, fall "
   "under law, and PDO wines follow rules on permitted varieties, maximum yields, and "
   "viticultural and winemaking practice. Buying expensive PDO land intending a wine that won't "
   "meet those rules \u2014 and so faces declassification \u2014 is a business risk unlikely to pay off. "
   "The underlying test: the producer needs a return from selling grapes, must or wine, so an "
   "expensive site demands confidence the product will sell at a price that delivers one."),

 answer_head("Part b) Terroir"),
 P("Terroir, from the French <i>terre</i> (land), is an overarching concept claiming the "
   "distinctiveness of quality wines comes from their sense of place, heavily used in discussion "
   "and marketing. No precise, agreed definition exists, and the term is often used undefined. "
   "Several distinct uses can be separated, and they do not stand on equal evidential footing."),
 P("The <b>physical</b> definition holds that a wine shows characteristics tied to where it "
   "grows \u2014 climate, soil, aspect, elevation. The standard illustration is the C\u00f4te d'Or, where "
   "wines from vines a few hundred metres apart taste different from slope position and small "
   "differences in soil, aspect and drainage. This use is well supported, since these physical "
   "parameters demonstrably govern water availability, heat and light."),
 P("A <b>cultural</b> definition extends it to human interventions \u2014 French PDOs stipulating "
   "planting density or trellising type. This includes the physical elements but goes beyond "
   "them, legitimate provided it is declared, since it changes the claim being made."),
 P("A third use, especially in marketing, claims wines are directly shaped by soil geology \u2014 "
   "that Chardonnay's perceived chalkiness comes from chalky soils, implying the vine takes up "
   "elements that directly affect taste. <b>This is strongly contested by the scientific "
   "community</b>, on three grounds: photosynthesis drives vine growth; all aroma compounds are "
   "synthesised in the vine; and must is further transformed by fermentation. No established "
   "pathway runs from a soil element to a flavour in the glass, so asserting one asserts what the "
   "evidence does not support."),
 P("A fourth strand concerns expression, not mechanism: many believe overly zealous winemaking \u2014 "
   "picking over-ripe fruit, heavy new oak \u2014 can mask a wine's terroir."),
 P("Terroir has long been tied to French and other classic European wines like the Mosel, but "
   "winemakers worldwide now explore single-vineyard expression, aided by soil mapping "
   "technology. The concept stays genuinely useful \u2014 provided the physical claim is kept "
   "separate from the geological one."),
 examiner_note([
   P("Part a) divides cleanly into natural, logistical/cost, and legal factors, closing on the "
     "return-on-investment test that unifies them. Most candidates write only the first section; "
     "marks spread across all three.", "box"),
   P("Part b) opens by stating no agreed definition exists, then rates each use for evidential "
     "standing rather than treating terroir as one idea. Giving the three scientific grounds "
     "against the geological claim in one sentence is precise and unmistakably informed.", "box"),
 ]),
]

q2 = [
 answer_head("Part a) Choosing planting material: variety, clone and rootstock"),
 P("Three decisions arise at establishment, each hard to reverse once vines are in the ground."),
 P("<b>Grape variety</b> comes first. With over a thousand varieties in commercial use, the "
   "grower weighs a longer list than the consumer, mainly concerned with aroma and flavour. Six "
   "traits govern climatic adaptation. Budding time sets frost exposure \u2014 early budders like "
   "Chardonnay risk spring frost more than late budders like Riesling. Life-cycle length sets "
   "climatic fit \u2014 early-ripening Chardonnay and Pinot Noir suit cool climates, ripening before "
   "wet late-autumn weather, while late-ripening Mourv\u00e8dre suits warm and hot climates, where an "
   "early ripener would gain sugar and lose acidity too fast for balance. Drought tolerance "
   "matters in dry climates \u2014 Grenache suits the southern Rh\u00f4ne, inland Spain, McLaren Vale. "
   "Disease resistance cuts monitoring in damp climates \u2014 Cabernet Sauvignon resists grey rot "
   "better than Merlot, one reason they blend well in maritime Bordeaux. Winter hardiness matters "
   "where winters are severe \u2014 Vidal and Riesling suit Ontario and the Finger Lakes. And vigour "
   "must be anticipated: high-vigour Sauvignon Blanc on fertile, well-watered soil needs managing "
   "to avoid excess shoot growth."),
 P("Beyond climate, variety choice answers to style, yield, cost, law, availability and market. "
   "Characteristics must suit the wine \u2014 a low-tannin, fruity red for early drinking points to "
   "Gamay or Grenache, not Nebbiolo or Aglianico. High-yielding varieties like Grenache give more "
   "wine per cost, a prime concern for inexpensive wines. Some cost more to grow \u2014 Pinot Noir is "
   "disease-prone, needing more monitoring and spraying. Law constrains choice in many EU "
   "countries \u2014 Prosecco must be predominantly Glera. Availability is limited by quarantine on "
   "new material and demand outstripping supply. And the producer must identify demand and route "
   "to market first, since fashions are pronounced, as Sauvignon Blanc's success shows. To "
   "capitalise on a trend after planting, head grafting cuts the vine at the trunk and grafts a "
   "new variety's bud on top: the established root system fruits much sooner than a new planting, "
   "though that rootstock was chosen for the original variety and may not suit the new one "
   "equally."),
 P("<b>Clone</b> choice follows similar logic but matters less than variety, and is far less "
   "affected by law or consumer fashion."),
 P("<b>Rootstock</b> choice matters because most vines are grafted, chiefly against phylloxera, "
   "and rootstock traits usually trace to parentage \u2014 many are hybrids of two species combining "
   "both's advantages. Against pests, Ramsey and Dog Ridge (both <i>V. champini</i>) tolerate "
   "root-knot nematodes too. For water: <i>V. rupestris</i> \u00d7 <i>V. berlandieri</i> hybrids like "
   "110R and 140R are highly drought tolerant, rooting deep and fast; <i>V. riparia</i>-based "
   "Riparia Gloire tolerates waterlogging; <i>V. berlandieri</i>-based 1103P tolerates salinity. "
   "For soil pH: 99R and 110R tolerate acidic soils, 41B (<i>V. berlandieri</i>) tolerates high "
   "lime. For vigour: low-vigour <i>V. riparia</i> types like 420A and 3309C can advance ripening "
   "in cool climates, while high-vigour <i>V. rupestris</i>-based 140R boosts growth on unfertile, "
   "dry soils. Vigour may also follow style: a high-vigour rootstock suits sparkling wine, where "
   "high yields with delicate aromas and acidity beat lower yields with more concentration."),

 answer_head("Part b) Vine age and the old-vine claim"),
 P("Vine age affects yield, and, by common assertion, quality \u2014 though the second is far less "
   "settled than the first."),
 P("The yield curve is reasonably clear. In the first two or three years growers commonly remove "
   "inflorescences as they form, so the young vine focuses on growth; some GIs also restrict fruit "
   "from very young vines. Vines up to about five years give relatively low yields, since roots "
   "aren't yet established. Between roughly ten and forty years, depending on variety and "
   "conditions, the vine gives maximum yields. Beyond that, yield falls as vigour declines, and "
   "the grower judges when declining yield stops being profitable \u2014 a commercial, not "
   "horticultural, judgement: vines of fifty years or more may stay profitable in famous old "
   "vineyards commanding super-premium prices (Burgundy, Eden Valley), while inexpensive or "
   "mid-priced producers, needing medium to high yields, replace them."),
 P("The quality claim is more cautious than popular use suggests. Older vines are often said to "
   "give higher quality fruit and more balanced, concentrated wines than young or middle-aged "
   "ones, with four theories offered: better balance and environmental adaptation with age; lower "
   "yields concentrating each grape among fewer berries; more old wood giving a larger "
   "carbohydrate reserve for early season or stress; or simply survival, since favourably sited "
   "vines always fruited well and growers keep the best vines longest before replanting."),
 P("None of this is established. Too many variables \u2014 clone, rootstock, irrigation, training, "
   "trellising \u2014 usually block direct comparison between young and old vines. It is explicitly "
   "not a definitive rule: a young vine well sited and trained will likely beat a badly maintained "
   "old one on a poor site. Site and management, in other words, plausibly explain much of what "
   "gets credited to age."),
 P("Commercially the term carries weight regardless. \u2018Old vines\u2019 and its equivalents \u2014 "
   "<i>vieilles vignes</i>, <i>vi\u00f1as viejas</i> \u2014 appear widely on labels for their quality "
   "connotation, but the term is unregulated: thirty years to one producer, a hundred to another. "
   "Some regions have responded with protective classifications \u2014 The Historic Vineyard Society "
   "in California, The Barossa Old Vine Charter \u2014 often specifying a minimum age."),
 examiner_note([
   P("Part a) explains rootstock properties <i>through</i> parentage rather than listing codes, "
     "converting recall into understanding, and includes the style-driven case for a high vigour "
     "rootstock, which candidates almost always omit.", "box"),
   P("Part b) separates the well-established yield curve from the contested quality claim, "
     "presents the four theories as theories, and flags the confounding-variables problem. The "
     "closing point \u2014 that site and management may explain what's credited to age \u2014 is analysis "
     "the chapter invites but doesn't spell out.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="Decisions taken during vineyard establishment are difficult to rectify once vines are "
           "planted.",
      parts=[("Explain the factors that influence the selection of a vineyard site.", "15%"),
             ("Explain what is meant by terroir, and discuss the different ways in which the term "
              "is used.", "10%")],
      answer=q1),
 dict(stem="The choice of planting material shapes the vineyard for its whole productive life.",
      parts=[("Explain the factors a grape grower considers when selecting grape variety, clone "
              "and rootstock.", "15%"),
             ("Explain the influence of vine age on yield and quality.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch5_Vineyard_Establishment.pdf",
      "Chapter Five \u00b7 Vineyard Establishment", s, exam, maxpages=19)
