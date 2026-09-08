# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 10 — Viticulture Scenarios"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Ten: Viticulture Scenarios",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 10.1 Priorat \u00b7 10.2 Pauillac \u00b7 10.3 Finger "
        "Lakes \u00b7 10.4 Central Valley")

s.append(P("This chapter introduces no new mechanism \u2014 it is four real sites where every "
           "earlier chapter's principles collide and get answered concretely. The skill it "
           "tests is <b>application</b>: given a climate and an economic target, derive the "
           "variety, vigour, training and harvest decisions that follow, rather than recall "
           "them from a list."))
s.append(P("Reliably examined: <b>explaining a region's practices from its climate and "
           "economics</b>, and <b>comparing two contrasting regions</b> on the same decision "
           "axis \u2014 vigour, density, training or harvest method. The same principle can "
           "produce opposite decisions in different places; showing <i>why</i> is the mark, "
           "not naming the decision itself."))

s.append(FIGURE("FIGURE 10.0 \u2014 WHERE THE FOUR REGIONS SIT", LocationMap(
    -125, 5, 33, 48,
    [(1, 41, "PRIORAT", "Spain"), (-0.7, 45, "PAUILLAC", "Bordeaux, France"),
     (-77, 42.5, "FINGER LAKES", "New York State"),
     (-120, 37, "CENTRAL VALLEY", "California")]),
    note="Priorat and Pauillac sit within 4\u00b0 latitude of each other, both European; the "
         "two North American sites are the wider outliers \u2014 latitude alone predicts "
         "surprisingly little without also knowing ocean influence and continental effect "
         "(Chapter Three)."))

s.append(EXHIBIT("EXHIBIT 10.1 \u2014 THE FOUR REGIONS: CLIMATE, SOIL, VARIETY", [
    ["", "Priorat", "Pauillac", "Finger Lakes", "Central Valley"],
    ["Climate", "Hot, dry, sunny; cold winters", "Atlantic; mild, rain "
     "year-round", "Lake-cooled; cold winters", "Warm, dry, sunny"],
    ["Soil", "Slate/quartz; low nutrient", "Free-draining; poor "
     "nutrient", "Nutrient-rich", "Variable; fertilised as needed"],
    ["Variety", "Garnacha, Cari\u00f1ena \u2014 late, dry-hardy",
     "Cab. Sauvignon + Merlot (body, earlier)", "Riesling \u2014 winter-"
     "hardy, late bud", "Set by market demand/price per ton"],
], [58, (W - 58) * 0.25, (W - 58) * 0.25, (W - 58) * 0.25, (W - 58) * 0.25], keep=False))
s.append(EXHIBIT("EXHIBIT 10.2 \u2014 THE FOUR REGIONS: VIGOUR, TRAINING, YIELD, HARVEST", [
    ["", "Priorat", "Pauillac", "Finger Lakes", "Central Valley"],
    ["Vigour", "<b>Low</b> \u2014 water/nutrient scarce", "<b>Low</b> \u2014 poor soil",
     "<b>High</b> \u2014 nutrients + rain", "<b>High</b> \u2014 irrigation + fertiliser"],
    ["Training", "Bush vines", "VSP; head, cane-pruned", "Scott-Henry "
     "(split canopy)", "CA sprawl (cheap); Lyre if needed"],
    ["Density", "<b>Low</b> (~2.5\u20133k/ha)", "<b>High</b> (~10k/ha)", "<b>Low</b> "
     "(~2.8\u20133.2k/ha)", "<b>Low</b> (~1.2\u20131.8k/ha)"],
    ["Yield", "<b>V. low</b> (15\u201325 hl/ha)", "Moderate (50\u201360)", "Moderate "
     "(50\u201360)", "<b>V. high</b> (180\u2013200)"],
    ["Harvest", "Hand \u2014 rugged terrain", "Hand or machine", "Machine \u2014 labour "
     "scarce", "Machine \u2014 cost"],
    ["Price", "Premium+", "Premium", "Varies", "Inexpensive, high-volume"],
], [50, (W - 50) * 0.25, (W - 50) * 0.25, (W - 50) * 0.25, (W - 50) * 0.25], keep=False))
s.append(P("Read down a column and a region's logic holds together; read across a row and the "
           "same variable \u2014 vigour, say \u2014 produces opposite decisions depending on "
           "what's driving it.", "note"))
s.append(FIGURE("FIGURE 10.1 \u2014 YIELD ACROSS THE FOUR REGIONS", RangeCompare(
    0, 220,
    [(15, 25, "Priorat", HOT), (50, 60, "Pauillac", COOL),
     (50, 60, "Finger Lakes", MILD), (180, 200, "Central Valley", WARM)],
    ticks=[0, 50, 100, 150, 200], unit=" hl/ha"),
    note="Pauillac and Finger Lakes land at the <b>same yield</b> despite opposite vigour "
         "\u2014 low vigour recovered through density in one, high vigour reined back "
         "through training in the other. Priorat and Central Valley anchor the extremes."))

# ================================================================ priorat
s.append(H2("1. Priorat, Catalunya"))
s += BUL([
    "Hot, dry, sunny summers and cold winters; best vineyards face <b>north-east</b> to "
    "escape the worst afternoon heat. <b>High evapotranspiration</b> on free-draining, "
    "nutrient-poor slate/quartz soil leaves the vine short of water \u2014 but the same "
    "dryness keeps <b>disease pressure low</b>. Irrigation needs advance authorisation, "
    "granted only for vine survival or quality.",
    "Water and nutrient scarcity naturally cap vigour, keeping vines small \u2014 <b>bush "
    "vines</b> suit this: their shoots and leaves shade the grapes usefully in such intense "
    "sun, without the vine ever being vigorous enough to over-shade. <b>Low density</b> "
    "(2,500\u20133,000/ha) lets roots range widely for water and nutrients.",
    "<b>Garnacha and Cari\u00f1ena</b> \u2014 late-ripening (won't rush to sugar ripeness in "
    "this heat) and drought-tolerant \u2014 are the natural fit; a drought-tolerant rootstock "
    "such as <b>140R</b> reinforces the same logic.",
    "Rugged terrain and largely untrellised vines force <b>hand work throughout</b>, "
    "harvest included. Combined with very low yield (15\u201325 hl/ha, partly from old "
    "vines) and heavy manual labour, the wines are <b>never inexpensive</b> \u2014 premium "
    "or super-premium pricing is the only economics that work.",
])

s.append(H2("2. Pauillac, Bordeaux"))
s += BUL([
    "Atlantic-moderated: moderate summers, mild winters, <b>rain year-round</b>. Free-"
    "draining, nutrient-poor soil.",
    "<b>Cabernet Sauvignon</b>, medium-to-late ripening, can struggle for body and aromatic "
    "range in cooler sites or years \u2014 blended with earlier-ripening <b>Merlot</b> for "
    "both.",
    "Poor soil naturally limits vigour, so <b>VSP</b> suits the vines without over-shading; "
    "typically <b>head-trained, replacement cane-pruned</b>. VSP's single, well-exposed "
    "canopy plane maximises leaf area and airflow \u2014 reducing fungal risk \u2014 but "
    "<b>rain and humidity still demand regular monitoring</b> for downy mildew and botrytis.",
    "<b>High density</b> (around 1m \u00d7 1m, ~10,000/ha): reliable rainfall means "
    "competition between vines isn't a problem, and expensive land makes maximising yield "
    "per hectare (not per vine) the economic priority. <b>Average yield 50\u201360 hl/ha</b>.",
    "Trellising allows <b>machine trimming and weeding</b> (specialist straddle machines "
    "work even tight rows); harvest may be by hand or machine.",
])

s.append(H2("3. Finger Lakes, New York State"))
s += BUL([
    "Deep lakes moderate temperature enough for <i>V. vinifera</i> to survive at all here \u2014 "
    "without them it couldn't. Still, winters are <b>extremely cold</b>. Black varieties "
    "(Cabernet Franc) are planted <b>nearest the lakes</b> for the extra warmth, extending "
    "their viable ripening window for tannins and aromas.",
    "<b>Riesling</b> is the main variety: winter-hardy against harsh cold, and "
    "<b>late-budding</b>, which protects against spring frost. Growers still <b>hill up soil "
    "over the graft</b>, the part most at risk from winter freeze. Multiple clones are "
    "typically planted for blending options and portfolio differentiation.",
    "Nutrient-rich soil plus plentiful rainfall gives <b>naturally vigorous</b> vines \u2014 "
    "the opposite problem to Priorat or Pauillac. <b>Scott-Henry</b> trellising splits the "
    "canopy to manage that vigour and keep light interception adequate; summer pruning "
    "(e.g. leaf stripping) helps further.",
    "Rainfall raises fungal risk, <b>botrytis</b> particularly; Scott-Henry's divided canopy "
    "improves airflow, but fungicide spraying is usually still needed.",
    "Large vines need room \u2014 <b>low density</b> (2,800\u20133,200/ha), wide between-row "
    "spacing (also easing mechanisation, since <b>labour is scarce</b> here). Each vine "
    "nonetheless ripens a large crop: yield <b>50\u201360 hl/ha</b>.",
])

s.append(H2("4. Central Valley, California"))
s += BUL([
    "Warm, dry, sunny growing season inland; rainfall is limiting, so <b>irrigation supplies "
    "the vine's water</b>, and fertiliser corrects nutrients where needed. The grower's "
    "central concern is <b>maximising yield at minimum cost</b> for inexpensive, high-volume "
    "wine.",
    "Irrigation and fertiliser let vines grow <b>large and vigorous</b> \u2014 since vines "
    "are expensive to buy, the cost-effective answer is <b>low density</b> (1,200\u20131,800/"
    "ha) of big, high-yielding vines (<b>180\u2013200 hl/ha</b>). Variety choice follows "
    "<b>market demand and price per ton</b>, not site suitability in the way other regions "
    "show.",
    "<b>California sprawl</b> \u2014 a single wire above the cordon, shoots simply flopping "
    "over it \u2014 is cheap and high-trained; the hanging shoots incidentally shade fruit "
    "from intense afternoon sun, cutting sunburn risk. Vines are <b>spur-pruned, cordon-"
    "trained</b> (cheaper than the skilled labour cane-pruning needs). Complex systems "
    "(Lyre) appear where vigour specifically needs managing.",
    "Labour-intensive summer pruning (leaf pulling, and especially <b>green harvesting</b>, "
    "which would cut yield) is <b>generally skipped</b> \u2014 the resulting lack of "
    "individual attention gives more variable ripeness and so <b>lower quality</b>, an "
    "accepted trade-off at this price point.",
    "<b>Machine harvest</b> is the cost-effective default; night picking is used where "
    "possible to keep fruit cool, but high volume over a short window doesn't always allow "
    "it. Grapes may be picked <b>relatively early</b> to dodge autumn rain risk, sometimes "
    "ahead of optimum ripeness \u2014 a deliberate risk-versus-ripeness trade-off, sharper "
    "still where a grower is also chasing higher quality fruit from the same site.",
])

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER TEN", [
    P("<b>1. The same variable can drive opposite decisions.</b> Low vigour (Priorat, "
      "Pauillac) and high vigour (Finger Lakes, Central Valley) each justify a specific, "
      "opposite training choice \u2014 state <i>which</i> vigour case you're in before naming "
      "the system.", "box"),
    P("<b>2. Density follows the scarce resource, not a fixed rule.</b> Pauillac plants "
      "densely because rainfall removes vine-to-vine competition and land is expensive; "
      "Priorat, Finger Lakes and Central Valley all plant sparsely, but for three different "
      "reasons \u2014 water competition, vine size, and vine cost respectively.", "box"),
    P("<b>3. Yield and price point are two ends of one argument.</b> Priorat's scarcity-"
      "driven low yield demands premium pricing; Central Valley's abundance-driven high "
      "yield demands low pricing \u2014 neither region could survive with the other's yield "
      "at its own price point.", "box"),
    P("<b>4. Rain does two different jobs depending on the region.</b> In Pauillac and "
      "Finger Lakes it removes competition and disease risk becomes the cost; in Priorat "
      "its <i>absence</i> is the defining constraint, and disease pressure is correspondingly "
      "low.", "box"),
    P("<b>5. Harvest method tracks labour availability as much as wine style.</b> Priorat "
      "hand-harvests from terrain and trellising constraints, Finger Lakes and Central "
      "Valley machine-harvest partly because <i>labour is scarce or expensive</i>, not solely "
      "because of intended quality.", "box"),
]))

s.append(exam_traps([
 ("Assuming low vigour always means poor viticulture.",
  "In Priorat and Pauillac, low vigour is the <b>correct fit</b> for the site \u2014 it "
  "matches training choice (bush vines, VSP) and avoids over-shading. Low vigour is a "
  "constraint to design around, not a failure."),
 ("Assuming high density always signals quality intent.",
  "Pauillac's high density is an <b>economic response to expensive land</b> plus rainfall "
  "removing competition \u2014 not a universal marker of premium wine."),
 ("Assuming irrigation is unavailable wherever it's restricted.",
  "Priorat <b>permits</b> irrigation with authorisation, for vine survival or quality \u2014 "
  "it is restricted, not banned outright."),
 ("Treating Central Valley's lower quality as accidental.",
  "It follows directly from <b>skipping labour-intensive summer pruning</b> to protect "
  "yield and cost \u2014 an accepted, deliberate trade-off, not an oversight."),
 ("Forgetting that Riesling's frost defence in Finger Lakes is twofold.",
  "<b>Late budding</b> protects against spring frost; <b>hilling up soil over the graft</b> "
  "separately protects against winter freeze \u2014 two different threats, two different "
  "fixes."),
]))

# ================================================================ exam
exam = []

MCQ = [
 dict(q="Priorat's best vineyards typically face north-east chiefly to:",
      opts=["Maximise total sunlight hours across the season",
            "Protect vines from the most extreme afternoon heat",
            "Align with the direction of the prevailing wind",
            "Comply with regional appellation rules on aspect"],
      ans=1, why="North-east aspect avoids the worst of the afternoon sun in Priorat's very "
                 "hot, sunny climate \u2014 protection from heat, not maximised exposure, is "
                 "the goal here."),
 dict(q="Bush vines suit Priorat particularly well because:",
      opts=["They are the cheapest possible option regardless of climate",
            "Their shoots and leaves shade the grapes usefully, without the vine ever being "
            "vigorous enough to over-shade", "They require the most skilled labour available",
            "They are mandated by Priorat's appellation rules"],
      ans=1, why="Naturally low vigour from water/nutrient scarcity means the shading bush "
                 "vines provide is beneficial rather than excessive."),
 dict(q="Cabernet Sauvignon is blended with Merlot in Pauillac principally because Merlot:",
      opts=["Is more drought-tolerant", "Ripens earlier and adds body and fruit character",
            "Is exclusively used for its colour", "Requires no trellising"],
      ans=1, why="Merlot's earlier ripening and its body/fruit contribution offset Cabernet "
                 "Sauvignon's tendency to lack these in cooler sites or years."),
 dict(q="Pauillac's high planting density makes economic sense chiefly because:",
      opts=["Vines there are naturally very small regardless of density",
            "Reliable rainfall removes vine-to-vine water competition, and expensive land "
            "rewards maximising yield per hectare", "Machine harvesting requires high "
            "density", "It is required by law throughout Bordeaux"],
      ans=1, why="With rainfall removing competition as a constraint, dense planting on "
                 "costly land maximises the yield the land can produce."),
 dict(q="In the Finger Lakes, black grape varieties such as Cabernet Franc are planted:",
      opts=["Furthest from the lakes, for maximum sun exposure",
            "Nearest the lakes, to benefit from the moderating effect and extend the viable "
            "ripening window", "Only on north-facing slopes",
            "In the same density as Riesling throughout the region"],
      ans=1, why="Proximity to the lake's moderating effect extends the period over which "
                 "tannins and aromas in black varieties can ripen."),
 dict(q="Riesling's two natural defences against Finger Lakes' winter climate are:",
      opts=["High vigour and dense planting", "Winter hardiness and late budding (protecting "
            "against spring frost)", "Drought tolerance and thick skins",
            "Early ripening and high yield"],
      ans=1, why="Winter hardiness resists the cold directly; late budding protects the "
                 "vine from spring frost after budburst."),
 dict(q="Scott-Henry trellising is used in the Finger Lakes principally to:",
      opts=["Reduce vine vigour directly", "Split the canopy of naturally vigorous vines to "
            "maintain adequate light interception", "Allow denser planting",
            "Eliminate the need for fungicide spraying"],
      ans=1, why="Nutrient-rich soil and plentiful rainfall make Finger Lakes vines "
                 "vigorous; splitting the canopy manages that vigour's shading effect "
                 "without reducing the vigour itself."),
 dict(q="California sprawl trellising in the Central Valley incidentally helps protect "
        "against:",
      opts=["Frost", "Sunburn, since the hanging shoots shade the fruit from afternoon sun",
            "Phylloxera", "Downy mildew"],
      ans=1, why="The shoots flopping over the single wire shade the fruit, cutting sunburn "
                 "risk in the intense Central Valley sun."),
 dict(q="Green harvesting is generally avoided in the Central Valley because it:",
      opts=["Is illegal under Californian regulations",
            "Would reduce yield, working against the goal of maximising volume at low cost",
            "Requires irrigation infrastructure the region lacks",
            "Only works on VSP-trellised vines"],
      ans=1, why="Since the priority is maximum yield at minimum cost, deliberately dropping "
                 "fruit through green harvesting works directly against that goal."),
 dict(q="Central Valley grapes are sometimes picked earlier than optimum ripeness chiefly "
        "to:",
      opts=["Comply with a fixed regional calendar date",
            "Avoid the risk of autumn rain as the season progresses",
            "Maximise potential alcohol specifically", "Allow same-day replanting"],
      ans=1, why="Picking ahead of forecast autumn rain protects the crop from rot and "
                 "dilution risk, even at some cost to ripeness."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) Vigour, density and training in Priorat and Central Valley"),
 P("Priorat and Central Valley sit at opposite ends of the vigour spectrum, and both "
   "regions' training and density decisions follow directly from that difference."),
 P("In <b>Priorat</b>, hot, dry conditions and free-draining, nutrient-poor slate and quartz "
   "soil produce a high evapotranspiration rate that leaves the vine genuinely short of "
   "water; irrigation is permitted only with advance authorisation, for survival or quality, "
   "not routine use. Vigour is therefore naturally <b>low</b>. <b>Bush vines</b> exploit "
   "this directly: their shoots and leaves shade the grapes usefully in such intense sun, "
   "without the vine ever growing vigorous enough to over-shade the fruit. Low vigour also "
   "caps how large each vine can be, so vines are planted at <b>low density</b> (2,500\u2013"
   "3,000/ha), letting roots spread widely for the water and nutrients the soil doesn't "
   "readily supply."),
 P("<b>Central Valley</b> inverts every part of this. Irrigation supplies the water Priorat "
   "lacks, and fertiliser corrects any nutrient shortfall, so vines grow <b>large and "
   "vigorous</b> by design. Because vines are expensive to buy, the economic answer to high "
   "vigour is <b>low density</b> planting (1,200\u20131,800/ha) of big vines that can each "
   "ripen a large crop \u2014 the same low-density outcome as Priorat, reached for the "
   "opposite reason. Training reflects the same logic at lower cost: <b>California "
   "sprawl</b>, a single wire the shoots flop over, is cheap, and the hanging shoots "
   "incidentally shade fruit from sunburn; spur-pruning and cordon-training avoid the more "
   "skilled labour replacement cane-pruning would need."),

 answer_head("Part b) Wine style, price point, yield and harvest"),
 P("Priorat's constraints and Central Valley's abundance each make economic sense only at "
   "their own price point, and each region's harvest method follows the same logic."),
 P("Priorat's water and nutrient scarcity, combined with old vines in the region, gives "
   "very low yields (<b>15\u201325 hl/ha</b>). Rugged terrain and largely untrellised vines "
   "force hand work throughout, harvest included, adding labour cost on top of already low "
   "volume. Together, low yield and high labour cost mean the wine can <b>never be "
   "inexpensive</b> \u2014 only premium or super-premium pricing recovers the cost of "
   "production."),
 P("Central Valley's irrigation- and fertiliser-driven vigour supports very high yields "
   "(<b>180\u2013200 hl/ha</b>), and the stated priority is maximising that yield at minimum "
   "cost for inexpensive, high-volume wine. <b>Machine harvesting</b> is the cost-effective "
   "default at this scale; night-picking keeps fruit cool and limits oxidation where "
   "possible, though high volume over a short window doesn't always allow it. Grapes may be "
   "picked <b>relatively early</b> to avoid autumn rain risk, sometimes ahead of optimum "
   "ripeness \u2014 an acceptable trade-off given the price point, in a way it would not be "
   "for Priorat."),
 examiner_note([
   P("Part a) uses the vigour axis to organise the whole comparison, showing that Priorat "
     "and Central Valley reach the <i>same</i> low-density outcome via opposite mechanisms \u2014 "
     "exactly the kind of structural insight that separates application from description.",
     "box"),
   P("Part b) connects yield directly to price point in both directions, and ties harvest "
     "method to the same economic logic rather than treating it as a separate, unconnected "
     "fact.", "box"),
 ]),
]

q2 = [
 answer_head("Part a) Soil, vigour and density in Pauillac and Finger Lakes"),
 P("Pauillac and Finger Lakes both receive plentiful rainfall through the growing season, "
   "yet reach opposite vigour and density decisions \u2014 because rainfall is not the only "
   "variable driving vigour."),
 P("Pauillac's soil is <b>free-draining and poor in nutrients</b>, which caps vine vigour "
   "regardless of how much rain falls; the rain matters mainly for removing water "
   "<i>competition</i> between closely spaced vines, not for feeding growth. With vigour "
   "naturally restrained, high-density planting (around 1m \u00d7 1m, roughly 10,000 vines/"
   "ha) is viable and, on expensive Bordeaux land, economically the right choice \u2014 it "
   "maximises yield per hectare from vines that will never grow large enough to compete "
   "destructively with their neighbours."),
 P("Finger Lakes soil is <b>nutrient-rich</b>, and combined with the same plentiful rainfall "
   "this produces <b>vigorous</b> vines \u2014 rainfall here is feeding growth directly, not "
   "simply removing competition. Vigorous vines need more room each, so density is "
   "correspondingly <b>low</b> (2,800\u20133,200/ha), with wide between-row spacing that also "
   "happens to suit mechanisation, valuable where labour is scarce. The same climatic input "
   "\u2014 reliable rain \u2014 therefore produces opposite density outcomes once soil fertility "
   "is factored in."),

 answer_head("Part b) Shared disease pressure, different canopy responses"),
 P("Both regions face elevated fungal disease risk from their rainfall, and both manage it "
   "through canopy architecture, though the specific system differs."),
 P("In Pauillac, rain and humidity in damper years raise the risk of <b>downy mildew and "
   "botrytis</b>, requiring regular monitoring and preventive spraying. <b>VSP</b> trellising "
   "helps directly: a single, well-exposed canopy plane maximises leaf area exposed to "
   "sunlight and improves air circulation, both reducing the conditions fungal disease "
   "needs, though rain still forces active monitoring rather than replacing it entirely."),
 P("In Finger Lakes, growing-season rainfall makes <b>botrytis</b> a particular concern. "
   "Here the canopy management challenge is compounded by the vines' own vigour: a dense, "
   "vigorous canopy would trap humidity regardless of rainfall. <b>Scott-Henry</b> "
   "trellising, which splits the canopy vertically, addresses both problems simultaneously \u2014 "
   "improving light interception for a naturally vigorous vine <i>and</i> improving airflow "
   "against fungal risk \u2014 though fungicide spraying is still usually necessary on top of "
   "this."),
 P("The shared principle is that canopy architecture is chosen to solve <b>more than one "
   "problem at once</b>: Pauillac's VSP simultaneously ripens fruit and controls disease "
   "given naturally low vigour; Finger Lakes' Scott-Henry simultaneously manages vigour and "
   "controls disease given naturally high vigour. Neither region relies on trellising alone, "
   "but in both cases the trellis choice is the first line of defence before chemical "
   "intervention."),
 examiner_note([
   P("Part a) isolates soil fertility as the variable that explains why identical rainfall "
     "produces opposite vigour outcomes, rather than treating \u2018plentiful rain\u2019 as a "
     "single undifferentiated fact about both regions.", "box"),
   P("Part b) names the specific disease pressures for each region individually before "
     "showing how each trellis choice solves two problems at once \u2014 disease and vigour "
     "together in Finger Lakes' case \u2014 which is the connective reasoning a Distinction "
     "answer needs.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="Priorat and Central Valley represent opposite ends of the yield spectrum.",
      parts=[("Explain how climate and soil in each region shape vine vigour and the "
              "resulting choices in vine density and training.", "15%"),
             ("Explain how wine style and price point in each region influence yield and "
              "harvesting method.", "10%")],
      answer=q1),
 dict(stem="Pauillac and Finger Lakes both receive plentiful rainfall throughout the growing "
           "season, yet make very different vine density and training decisions.",
      parts=[("Explain why soil and vigour differ between the two regions despite their "
              "similar rainfall, and how this shapes planting density.", "15%"),
             ("Explain the disease management challenge both regions share, and how each "
              "addresses it through canopy management.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch10_Viticulture_Scenarios.pdf",
      "Chapter Ten \u00b7 Viticulture Scenarios", s, exam, maxpages=18)
