# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 8 — Hazards, Pests and Diseases"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps

W = L_W
s = []

s += H1("Chapter Eight: Hazards, Pests and Diseases",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 8.1 Hazards \u00b7 8.2 Pests \u00b7 8.3 Fungal "
        "Diseases \u00b7 8.4 Bacterial Diseases \u00b7 8.5 Viruses")

s.append(P("The largest chapter in D1 by sheer count of named threats \u2014 roughly two dozen "
           "hazards, pests and diseases, each with its own cause, symptoms and management. The "
           "exam does not expect every detail on every one; it expects <b>compare and "
           "evaluate</b> across a pair (powdery vs downy mildew; frost vs hail), and a "
           "recurring structural pattern worth learning once: cause \u2192 symptoms/consequence "
           "\u2192 management, and for anything spread by a vector, <b>controlling the vector "
           "is usually the only lever</b>, since there is often no direct cure."))
s.append(P("Reliably examined: <b>frost types and protection methods</b>, where only aspersion "
           "works against advective frost; <b>powdery versus downy mildew</b>, the classic "
           "confusion pair; and the <b>vector-control pattern</b> across nematodes, "
           "sharpshooters, leafhoppers and mealybugs. Learn the pattern, not just the list."))

# ================================================================ hazards
s.append(H2("1. Hazards"))
s.append(EXHIBIT("EXHIBIT 8.1 \u2014 WEATHER AND SITE HAZARDS", [
    ["Hazard", "Cause / mechanism", "Key management"],
    ["<b>Drought</b>", "Below ~500\u2013750 mm/yr (cool/warm). Stomata close to limit water "
     "loss \u2192 photosynthesis falls \u2192 growth impaired, grapes small, ripening slows; "
     "prolonged, leaves are lost and the vine dies", "Design irrigation in from the start; "
     "drought-tolerant rootstock (110R, 140R) or variety (Garnacha)"],
    ["<b>Excess water</b>", "Too much vegetative growth competes with ripening and shades "
     "fruit; humidity raises fungal risk; waterlogging starves roots of oxygen and compacts "
     "soil", "Plant on a slope or free-draining soil; install drainage"],
    ["<b>Untimely rainfall</b>", "At pollination/fruit set: millerandage or coulure. In "
     "summer: slows ripening. Near vintage: swollen, diluted grapes, splitting \u2192 grey "
     "rot, harvest difficulty", "Cannot control rainfall itself \u2014 site, soil, drainage and "
     "cover-crop choices mitigate; monitor forecasts and weigh early harvest against the risk "
     "of waiting"],
    ["<b>Freeze</b> (winter)", "Below <b>\u221220\u00b0C / \u22124\u00b0F</b> \u2014 dormant vines are "
     "otherwise hardy. The <b>graft</b> is most at risk if above ground, then canes/cordons",
     "Hillside sites (up to 5\u00b0C warmer than the valley floor); sites near large water "
     "bodies; deep snow cover for insulation; hardy varieties (Cabernet Franc, Riesling) or "
     "hardy hybrid parentage (V. amurensis; Concord to \u221230\u00b0C); hilling up soil over the "
     "graft; multiple trunks as insurance"],
    ["<b>Hail</b>", "Rips shoots/leaves; damages ripening grapes and opens a path for "
     "botrytis. Unpredictable, though some regions (Mendoza, Burgundy) suffer repeatedly",
     "Cloud seeding by rocket; netting (only where sunlight is plentiful, since netting "
     "shades); spreading risk across separate plots; crop insurance"],
], [80, (W - 80) * 0.48, (W - 80) * 0.52], keep=False))

s.append(H3("Frost"))
s.append(P("Cold air below <b>0\u00b0C / 32\u00b0F</b> collects at ground level and freezes water "
           "in growing buds and shoots. <b>Advective</b> frosts arrive as large volumes of cold "
           "air moving in; <b>radiative</b> frosts form on still, cool nights as the earth "
           "loses daytime heat \u2014 denser cold air then pools in valley bottoms. Both cool and "
           "warm climates are vulnerable, for opposite reasons: cool climates don't grow until "
           "10\u00b0C, but warm climates start growing early and are exposed to a later drop. "
           "Secondary buds replace killed primary growth, but are less fruitful and ripen "
           "later \u2014 itself a new risk.", "note"))
s.append(FIGURE("FIGURE 8.1a \u2014 TEMPERATURE AND FROST RISK", ThresholdScale(
    -30, 15,
    bands=[(-30, -25, "VINE DEATH LIKELY", HOT), (-25, -20, "SEVERE DAMAGE", WARM),
           (-20, 0, "FROST DAMAGES BUDS/SHOOTS", COOL), (0, 15, "NO FROST RISK", MILD)],
    marks=[(-25, "-25\u00b0C \u2014 DEATH"), (-20, "-20\u00b0C \u2014 DAMAGE"),
           (0, "0\u00b0C \u2014 FROST BEGINS"), (10, "10\u00b0C \u2014 GROWTH BEGINS")],
    unit="\u00b0C")))
s.append(EXHIBIT("EXHIBIT 8.2 \u2014 FROST PROTECTION, COMPARED", [
    ["Method", "How", "Note"],
    ["<b>Reducing risk (no active cost when frost isn't threatening)</b>", "", ""],
    ["Site selection", "Avoid frost pockets; choose hillside sites where cold air drains away",
     "Free, but fixed at establishment"],
    ["Delayed pruning", "Postpones budburst into warmer months; frosted cane-tip buds can be "
     "removed", "\u2014"],
    ["Late-budding variety", "E.g. Riesling", "\u2014"],
    ["High training / bare soil", "Coldest air sits near the ground; bare soil (vs cover "
     "crop) absorbs and radiates more heat", "\u2014"],
    ["<b>Combating an active threat (cost every time used)</b>", "", ""],
    ["Water sprinklers (aspersion)", "Freezing water releases latent heat, protecting the "
     "plant; must run until temperature rises", "<b>The only method effective against "
     "advective frost</b>"],
    ["Wind machines", "4\u20137 m fans pull warm air down from an inversion layer "
     "(+3\u20135\u00b0C, ~10 m up)", "Large upfront cost; judged worthwhile if a damaging "
     "radiative frost is likely <b>once every five years</b>. Helicopters do the same job, "
     "costlier, for severe short-term risk"],
    ["Heaters / candles", "Oil, propane or wax burners placed through the vineyard", "High "
     "fuel and labour cost, low efficiency, air pollution"],
], [122, 116, W - 122 - 116], keep=False))
s.append(FIGURE("FIGURE 8.1b \u2014 WHICH ACTIVE METHOD?", DecisionTree(
    "Advective frost (large cold air mass moving in) or radiative (still, clear night)?",
    [("ADVECTIVE", "Aspersion (water sprinklers) \u2014 the only method that works"),
     ("RADIATIVE", ("Is there a warm inversion layer above the vineyard?",
                     [("YES", "Wind machines pull it down \u2014 or helicopters, for severe "
                       "short-term risk"),
                      ("NO", "Heaters/candles, or accept the risk if uneconomical")]))])))

s.append(EXHIBIT("EXHIBIT 8.3 \u2014 SUNBURN, FIRE AND SMOKE TAINT", [
    ["Hazard", "Mechanism", "Key management"],
    ["<b>Sunburn</b>", "Grape transpiration is far less effective than leaf transpiration, so "
     "grapes reach higher temperatures than leaves \u2014 worse under water stress. Scars, "
     "browning, bitterness, rot susceptibility; affected fruit is sorted out",
     "Avoid east-west rows in hot Northern Hemisphere sites (avoids day-long/afternoon sun on "
     "one side); partial fruit-zone shading; extra irrigation before a heatwave; sunscreen "
     "spray or shade cloth/net"],
    ["<b>Fire</b>", "More frequent with warmer, drier climate-change weather (Australia, "
     "California, Chile). Nearby woodland/pasture, cover crops and mulch all add fuel; bare "
     "cultivated soil burns less readily", "Fire detectors and sprinklers; a maintained water "
     "tank; staff emergency training"],
    ["<b>Smoke taint</b>", "Aroma compounds absorbed from vineyard smoke bind with sugars into "
     "aroma-less precursors, which only turn aromatic during <b>fermentation</b> \u2014 and can "
     "strengthen further with age. Risk rises from <b>v\u00e9raison</b> onward",
     "Test must analytically or by micro-vinification pre-harvest; hand harvest, gentle/whole-"
     "bunch pressing, cooler ferments and shorter maceration cut uptake; flash d\u00e9tente or "
     "reverse osmosis help but don't fully remove it; blending with unaffected wine"],
], [76, (W - 76) * 0.52, (W - 76) * 0.48], keep=False))

# ================================================================ pests
s.append(H2("2. Pests"))
s.append(P("Some of the most damaging pests and diseases arrived by <b>importing organisms "
           "into territories whose vines had no natural resistance</b> \u2014 phylloxera and "
           "the two mildews were all native to North America, harmless there, devastating once "
           "in Europe. The recurring solution has been to borrow resistance from American "
           "species, typically via rootstock.", "note"))
s.append(H3("Phylloxera"))
s += BUL([
    "An aphid-like insect feeding and laying eggs <b>on the roots</b>, spread by crawling "
    "but mostly by <b>human movement</b> \u2014 nursery roots, soil, equipment, irrigation "
    "water. Damaged roots lose nutrient/water uptake and become vulnerable to secondary "
    "bacterial/fungal attack \u2014 weakening, then death.",
    "Symptoms: drought-pattern death spreading in patches; insects and yellow eggs visible "
    "on roots; root swellings; pale green leaf galls; stunted growth and yellowing by year "
    "<b>three</b>, death by year <b>five</b>. Sandy soil gives natural immunity \u2014 no help "
    "elsewhere.",
])
s.append(FIGURE("FIGURE 8.2 \u2014 THE PHYLLOXERA STORY: ONE CONTINUOUS PROBLEM", FlowChart([
    ("1863 \u2014 IDENTIFIED IN EUROPE", "Destroys <b>two-thirds</b> of European vineyard by "
     "the century's end", None),
    ("FIRST FIX", "American species (<i>V. berlandieri, V. riparia, V. rupestris</i>) resist "
     "it, sealing egg wounds with a corky layer \u2014 but planted directly they give "
     "undesirable aromas", None),
    ("THE SOLUTION", "Graft European <i>vinifera</i> onto <b>American rootstock</b> instead "
     "\u2014 resistant roots, vinifera fruit", None),
    ("NEW PROBLEM", "Single-species American rootstocks can't tolerate Europe's "
     "<b>calcareous soils</b> \u2014 lime intolerance causes chlorosis", None),
    ("THE FIX THAT STUCK", "<b>Hybridise</b> the American species together, balancing "
     "phylloxera resistance against lime tolerance \u2014 the same rootstocks now also "
     "address nematodes, soil pH, water stress, salinity and vigour at once", None),
], box_w=W * 0.84)))
s.append(EXHIBIT("EXHIBIT 8.4 \u2014 OTHER PESTS", [
    ["Pest", "Damage", "Key management"],
    ["<b>Nematodes</b>", "Microscopic soil worms; some feed on roots (slow decline), others "
     "transmit viruses (dagger nematode \u2192 fanleaf virus). Can be managed, not eliminated",
     "Biofumigation (mustard cover crop ploughed in); nematode-resistant rootstock (Ramsey, "
     "Dog Ridge); heat-treated nursery stock"],
    ["<b>Grape moths</b>", "Feed on flowers, then grapes; wounds invite bacteria/fungi "
     "including botrytis", "Bacillus thuringiensis; pheromone \u2018sexual confusion\u2019; "
     "natural predators (parasitic wasps, lacewings, some spiders); insecticides"],
    ["<b>Spider mites</b>", "Feed on leaf surface cells \u2014 discolouration, less "
     "photosynthesis, delayed ripening, lower yield. Thrive in dust and on water-stressed "
     "vines", "Sprinklers/cover crops/mulch to cut dust; encourage predatory mites; targeted "
     "sprays (general pesticides kill the predators too)"],
    ["<b>Birds</b>", "Destroy ripening grapes wholesale; wounds invite rot. Isolated vineyards "
     "(sole local food source) most at risk", "Netting (justified in high-value areas); "
     "rotated scarers/noise; falcons"],
    ["<b>Mammals</b>", "Deer, rabbits, kangaroos, raccoons, wild boar, baboons \u2014 eat shoots/"
     "grapes/leaves, break skins (rot risk), damage trellising", "Fencing, high enough and "
     "sunk into the soil against burrowing"],
], [78, (W - 78) * 0.5, (W - 78) * 0.5], keep=False))

# ================================================================ fungal diseases
s.append(H2("3. Fungal Diseases"))
s.append(FIGURE("FIGURE 8.3 \u2014 IN THE FIELD: WHICH MILDEW?", DecisionTree(
    "Dull grey patches on the surface, or yellow 'oil spots' with white growth underneath?",
    [("SURFACE PATCHES", "Powdery mildew \u2014 treat with sulfur"),
     ("OIL SPOTS", "Downy mildew \u2014 treat with copper")])))
s.append(EXHIBIT("EXHIBIT 8.5 \u2014 POWDERY VERSUS DOWNY MILDEW", [
    ["", "Powdery mildew", "Downy mildew"],
    ["Organism", "Erysiphe necator (Oidium) \u2014 on the <b>surface</b>",
     "Peronospora \u2014 a water mould living <b>within</b> vine tissue"],
    ["Conditions", "Optimum <b>~25\u00b0C / 77\u00b0F</b>; thrives in <b>shade</b>; "
     "<b>does not need high humidity</b> \u2014 spreads even in dry conditions",
     "Needs <b>rainfall + warmth (~20\u00b0C / 68\u00b0F)</b>; high-risk in warm springs or warm "
     "stormy summers"],
    ["Symptoms", "Dull grey patches \u2192 black as they advance; damages shoots, "
     "inflorescences, grapes (which can split at v\u00e9raison)",
     "Yellow circular \u2018oil spots\u2019, then white downy growth on leaf undersides; mainly "
     "defoliates via young leaves and flowers"],
    ["Susceptible", "Chardonnay, Cabernet Sauvignon <i>more</i>; Pinot Noir, Riesling "
     "<i>less</i>", "Most wine regions"],
    ["Treatment", "<b>Sulfur</b> (budburst to v\u00e9raison \u2014 prevention easier than "
     "cure); systemic fungicides (rain-fast, but resistance limits annual applications)",
     "<b>Copper</b> (Bordeaux mixture, copper sulfate + lime, standard since the 1880s; lasts "
     "only until 20 mm rain falls; the <b>only current organic option</b>, though the EU is "
     "moving to reduce/eliminate copper use); other fungicides"],
    ["Shared lever", "Open canopy \u2014 reduces shade for powdery, dries faster (less "
     "moisture) for downy", "As left"],
], [58, (W - 58) * 0.5, (W - 58) * 0.5], keep=False))
s.append(EXHIBIT("EXHIBIT 8.6 \u2014 FOUR MORE FUNGAL DISEASES", [
    ["Disease", "Conditions / cause", "Key management"],
    ["<b>Grey rot</b> (botrytis bunch rot)", "Needs an entry point \u2014 tight bunches "
     "rubbing, bird/insect puncture. Rainfall + high humidity activate dormant spores. Tight-"
     "bunch/thin-skin varieties (Semillon, Sauvignon Blanc, Pinot Noir) most at risk",
     "Thick-skinned small-grape varieties (Petit Verdot); open canopy, leaf removal around "
     "bunches; fungicide at flowering-end/formation-end/bunch closure/v\u00e9raison; "
     "antagonistic bacteria (Bacillus subtilis) \u2014 sulfur/copper are ineffective here"],
    ["<b>Eutypa dieback</b> (dead arm)", "Wind-spread spores enter through <b>pruning "
     "wounds</b> in moderate, wet conditions. Rotten wood, kills vines over ~10 years if "
     "untreated. Grenache, Cabernet Sauvignon, Sauvignon Blanc susceptible",
     "Prune late; fungicide on pruning wounds; cut affected trunk 5\u201310 cm beyond visible "
     "symptoms and treat, burn dead wood; retrain from a sucker (2 years' lost yield) or "
     "replant if severe"],
    ["<b>Phomopsis</b> (cane and leaf spot)", "Cool wet springs then humid, moderate weather. "
     "Canes whiten and snap; brown cracks at shoot bases. Grenache very susceptible, Cabernet "
     "Sauvignon less so", "Fungicide 3 weeks after budburst, then fortnightly if wet "
     "conditions persist; remove and destroy diseased wood at pruning; airflow-improving "
     "canopy management"],
    ["<b>Esca</b>", "A complex of organisms, prevalent in <b>warm, dry</b> climates (southern "
     "Europe, California); enters through pruning wounds. Tiger-striped leaves, spotted wood; "
     "kills within a few years", "<b>No chemical control.</b> Disease-free stock; new pruning "
     "techniques; never prune in rain; remove prunings promptly; disinfect wounds; biological "
     "agents (Bacillus subtilis) under research"],
], [96, (W - 96) * 0.42, (W - 96) * 0.58], keep=False))
s.append(P("Other named fungal diseases: black rot, black-foot disease, Bot canker, "
           "anthracnose.", "note"))

# ================================================================ bacterial + viral
s.append(H2("4. Bacterial Diseases and Viruses"))
s.append(P("<b>None of the four diseases below has a cure.</b> Every management strategy "
           "targets the <b>vector</b> that spreads it \u2014 the recurring pattern worth "
           "remembering across this whole section.", "note"))
s.append(FIGURE("FIGURE 8.4 \u2014 THE SHARED PATTERN, EVERY TIME", FlowChart([
    ("PATHOGEN IN AN INFECTED VINE", "Bacterium or virus present, often silently, in "
     "sap or tissue", None),
    ("A VECTOR FEEDS OR MOVES", "Sharpshooter, leafhopper, nematode or mealybug carries "
     "it \u2014 or infected grafting material does", None),
    ("A HEALTHY VINE IS INFECTED", "No cure exists once this happens", None),
    ("MANAGEMENT = VECTOR CONTROL", "Reduce the carrier, not the pathogen \u2014 or remove "
     "and replant with clean stock", None),
], box_w=W * 0.84)))
s.append(FIGURE("FIGURE 8.5 \u2014 FOUR DISEASES, ZERO CURES", Pictogram(
    4, 4, grape_icon,
    label="Pierce's Disease \u00b7 grapevine yellows \u00b7 fanleaf virus \u00b7 leafroll virus "
          "\u2014 not one has a chemical cure")))
s.append(EXHIBIT("EXHIBIT 8.7 \u2014 VECTOR-BORNE BACTERIAL AND VIRAL DISEASE", [
    ["Disease", "Vector", "Symptoms / impact", "Vector control"],
    ["<b>Pierce's Disease</b> (bacterial)", "<b>Sharpshooter insects</b> (glassy-winged "
     "sharpshooter accelerated spread from the 1980s)", "Bacterium clogs sap channels \u2014 "
     "shrivelling, leaf drop, death in 1\u20135 years. Chardonnay, Pinot Noir vulnerable. "
     "Needs lab testing to confirm", "Remove vines near rivers (blue-green sharpshooter "
     "habitat); insecticide; predatory wasp on sharpshooter eggs; quarantine on plant "
     "movement"],
    ["<b>Grapevine yellows</b> (bacterial)", "<b>Leafhoppers</b>; also untreated nursery "
     "stock", "Delayed budburst, drooping unwoody shoots, canopy yellows (white varieties) "
     "or reddens (black). Chardonnay, Riesling vulnerable. Some strains fatal, others allow "
     "recovery", "Insecticide against leafhoppers; remove host plants including cover crops; "
     "hot-water bath for nursery pruning wood"],
    ["<b>Fanleaf virus</b>", "<b>Dagger nematode</b>; historically spread fastest via infected "
     "grafted material after phylloxera", "Stunted early growth, distorted canes, pale "
     "fan-shaped malformed leaves. Cabernet Sauvignon can lose most of its crop",
     "Soil-test for dagger nematode before replanting; virus-tested clean planting material; "
     "no cure \u2014 remove and replace"],
    ["<b>Leafroll virus</b>", "<b>Mealybugs</b> (South Africa, Mediterranean, Argentina, parts "
     "of California) and grafting", "Doesn't kill, but cuts yield by up to half; slower root/"
     "shoot growth, delayed ripening, more acid/less colour/less sugar, less stored "
     "carbohydrate. Leaves roll and redden (black) or yellow (white) in autumn",
     "Remove and replant with virus-free stock; nursery screening; open canopy (mealybugs "
     "favour humidity); encourage predators (ladybugs, lacewings) \u2014 spraying is hard "
     "given the mealybug's waxy coating"],
], [78, 100, (W - 78 - 100) * 0.5, (W - 78 - 100) * 0.5], keep=False))

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER EIGHT", [
    P("<b>1. For anything vector-borne, name the vector, not the pathogen, as the "
      "management target.</b> Pierce's, grapevine yellows, fanleaf and leafroll all lack a "
      "cure \u2014 every real lever controls the sharpshooter, leafhopper, nematode or "
      "mealybug instead.", "box"),
    P("<b>2. Powdery and downy mildew are opposites on humidity and location.</b> Powdery "
      "sits on the surface and spreads in dry shade; downy lives within the tissue and needs "
      "rain and warmth. Sulfur treats one, copper the other \u2014 do not swap them.", "box"),
    P("<b>3. Aspersion is the only defence against advective frost.</b> Wind machines need an "
      "inversion layer that advective (mass cold-air) events don't necessarily provide \u2014 "
      "state which frost type before naming a fix.", "box"),
    P("<b>4. Netting against hail trades protection for shade.</b> It only makes sense where "
      "sunlight is abundant (Mendoza), not in already-marginal light climates (Burgundy).",
      "box"),
    P("<b>5. The rootstock story is one continuous problem, not two.</b> American species "
      "solved phylloxera but introduced lime intolerance in Europe's calcareous soils; "
      "hybridising the American species solved both at once \u2014 tell it as cause and "
      "correction, not two separate facts.", "box"),
]))

s.append(exam_traps([
 ("Treating all frost protection methods as interchangeable.",
  "Only <b>aspersion</b> works against <b>advective</b> frost. Wind machines need an "
  "inversion layer and suit <b>radiative</b> frost."),
 ("Confusing powdery and downy mildew's moisture needs.",
  "<b>Powdery</b> spreads in dry shade, no humidity required. <b>Downy</b> needs rainfall and "
  "warmth. Swapping sulfur/copper treatment between them is the same error."),
 ("Assuming grape moths, spider mites and mildew are unrelated problems.",
  "Wounds from moths and mites <b>open the door</b> to secondary fungal attack, including "
  "botrytis \u2014 pest and disease pressure compound each other."),
 ("Assuming a cure exists for bacterial and viral diseases.",
  "<b>None of the four</b> covered here \u2014 Pierce's, grapevine yellows, fanleaf, leafroll \u2014 "
  "has a cure. Management is vector control or replanting, not treatment."),
 ("Forgetting why grafting onto American rootstock alone wasn't enough.",
  "Single-species American rootstocks resisted phylloxera but couldn't tolerate Europe's "
  "<b>lime-rich soils</b> (chlorosis) \u2014 the fix was <b>hybridising</b> American species "
  "together."),
]))

# ================================================================ exam
exam = []

MCQ = [
 dict(q="A prolonged lack of water first impairs the vine chiefly by causing it to:",
      opts=["Shed all its leaves immediately", "Close its stomata, reducing photosynthesis",
            "Increase malic acid production", "Accelerate bud fruitfulness"],
      ans=1, why="Stomatal closure to limit water loss is the first response, and it directly "
                 "cuts photosynthesis \u2014 leaf loss and death only follow if drought "
                 "continues."),
 dict(q="Radiative frost is best described as:",
      opts=["Cold air arriving in large volumes from a distant cold region",
            "Heat lost from the earth on a still, cool night, pooling as cold air near the "
            "ground", "A frost caused only by wind chill", "A frost that only affects "
            "irrigated vineyards"],
      ans=1, why="Radiative frost forms from the earth's own heat loss on still nights; "
                 "advective frost is the incoming cold air mass."),
 dict(q="Which frost protection method is effective against advective frost specifically?",
      opts=["Wind machines", "Water sprinklers (aspersion)", "Oil heaters", "Delayed pruning"],
      ans=1, why="Aspersion is the only method the textbook identifies as effective against "
                 "advective frost; wind machines rely on an inversion layer more typical of "
                 "radiative events."),
 dict(q="Netting a vineyard against hail is most appropriate in a region such as:",
      opts=["Burgundy, due to its reliably sunny climate", "Mendoza, where sunlight is "
            "abundant enough to offset the shading netting causes", "Any cool climate region",
            "Only regions with no history of hail damage"],
      ans=1, why="Netting shades the fruit, so it suits sunny regions like Mendoza; in a "
                 "marginal-light climate like Burgundy the shading cost is less acceptable."),
 dict(q="Phylloxera was brought under control in Europe principally by:",
      opts=["Widespread use of systemic insecticides",
            "Grafting European vinifera onto hybridised American rootstocks",
            "Planting American vine species directly for wine production",
            "Switching all vineyards to sandy soils"],
      ans=1, why="Direct American plantings gave undesirable aromas, so European varieties "
                 "were grafted onto American rootstock instead \u2014 later hybridised to also "
                 "handle Europe's lime-rich soils."),
 dict(q="Rootstocks derived from single American species initially struggled in Europe "
        "because:",
      opts=["They were not resistant to phylloxera", "They had little tolerance of "
            "lime-rich, calcareous soils, causing chlorosis", "They could not be grafted",
            "They were more expensive than own-rooted vines"],
      ans=1, why="Chlorosis from lime intolerance was the new problem, solved by hybridising "
                 "American species together to balance phylloxera resistance with lime "
                 "tolerance."),
 dict(q="Powdery mildew differs from downy mildew in that it:",
      opts=["Requires high humidity to spread", "Can spread in relatively dry conditions and "
            "thrives in shade", "Lives within vine tissue rather than on the surface",
            "Is treated with copper-based sprays"],
      ans=1, why="Powdery mildew is unusual among mildews in not needing high humidity, and "
                 "favours shady conditions; downy mildew needs rain and warmth, and is treated "
                 "with copper, not sulfur."),
 dict(q="Sulfur and copper sprays are ineffective against which fungal disease?",
      opts=["Powdery mildew", "Downy mildew", "Grey rot (botrytis bunch rot)", "Phomopsis"],
      ans=2, why="Traditional sulfur and copper sprays don't work against grey rot; other "
                 "fungicides and biological controls (Bacillus subtilis) are used instead."),
 dict(q="Pierce's Disease and grapevine yellows share which management characteristic?",
      opts=["Both are cured with a systemic fungicide",
            "Neither has a chemical or other direct cure \u2014 management targets the insect "
            "vector", "Both are prevented by copper spraying",
            "Both can be eliminated by soil fumigation"],
      ans=1, why="Both are vector-borne bacterial diseases with no direct cure; control works "
                 "through reducing sharpshooters (Pierce's) or leafhoppers (grapevine "
                 "yellows)."),
 dict(q="Leafroll virus is principally spread by:",
      opts=["The dagger nematode", "Mealybugs and grafting", "Wind-blown fungal spores",
            "Contaminated irrigation water alone"],
      ans=1, why="Mealybugs and grafting are the stated vectors for leafroll virus; the "
                 "dagger nematode is specifically associated with fanleaf virus."),
]
exam += mcq_section(MCQ)

q1 = [
 answer_head("Part a) Comparing frost and hail as hazards"),
 P("Frost and hail are both weather hazards largely outside the grower's control, but they "
   "act through different mechanisms and call for different responses."),
 P("<b>Frost</b> occurs when air below 0\u00b0C collects at ground level and freezes water in "
   "growing buds and shoots, killing them outright. Two distinct types demand different "
   "protection: <b>advective</b> frost arrives as a mass of cold air moving in, defended "
   "against only by <b>water sprinklers</b>, where the latent heat released as the water "
   "freezes protects the plant; <b>radiative</b> frost forms locally on still, cool nights as "
   "the earth loses its daytime heat, and can additionally be countered by <b>wind "
   "machines</b>, which pull warmer air down from an inversion layer roughly 10 m up. Risk-"
   "reduction is available in both cases without an active response cost: hillside site "
   "selection, late-budding varieties, delayed pruning and bare soil (which absorbs and "
   "radiates more heat than a cover crop) all lower exposure before frost threatens."),
 P("<b>Hail</b> physically rips shoots and leaves and damages ripening grapes, opening entry "
   "points for botrytis; unlike frost, it strikes unpredictably, though some regions "
   "(Mendoza, Burgundy) suffer repeatedly. Response is largely reactive rather than "
   "preventive: cloud seeding to encourage rain instead of hail, netting the fruit zone \u2014 "
   "viable only where sunlight is abundant enough to absorb the shading cost, hence more "
   "suited to Mendoza than Burgundy \u2014 spreading risk across separate plots, and crop "
   "insurance."),
 P("The key contrast for evaluation: frost protection can be economically modelled (a wind "
   "machine is judged worthwhile against roughly one damaging radiative frost every five "
   "years), while hail's unpredictability makes insurance and diversification, rather than "
   "physical defence, the more realistic strategy in many regions."),

 answer_head("Part b) Why bacterial and viral disease management focuses on the vector"),
 P("None of the bacterial diseases or viruses covered \u2014 Pierce's Disease, grapevine "
   "yellows, fanleaf virus, leafroll virus \u2014 has a chemical or other direct cure. This "
   "single fact explains why management strategy for all four converges on the same target: "
   "the organism that <b>transmits</b> the pathogen between vines, not the pathogen itself."),
 P("Pierce's Disease is spread by <b>sharpshooter insects</b>; control removes habitat "
   "(vines near rivers, home to the blue-green sharpshooter), uses insecticide, and has "
   "introduced a predatory wasp that feeds on sharpshooter eggs. Grapevine yellows spreads "
   "via <b>leafhoppers</b> and untreated nursery stock; control reduces leafhopper "
   "populations and removes host plants, including cover crops, alongside a hot-water bath "
   "for nursery pruning wood. <b>Fanleaf virus</b> spreads via the dagger nematode, so pre-"
   "planting soil testing and virus-tested clean planting material are the only levers. "
   "<b>Leafroll virus</b> spreads via mealybugs and grafting; since mealybugs favour humid "
   "conditions, an open canopy helps, and their waxy coating makes spraying largely "
   "ineffective, so natural predators (ladybugs, lacewings) are preferred instead."),
 P("Where infection has already taken hold, the only option in every case is the same: "
   "remove the affected vine and replant with clean, virus-tested material \u2014 confirming "
   "these are diseases managed by prevention and vector suppression, never by treatment."),
 examiner_note([
   P("Part a) names the frost/hail contrast on mechanism (freezing vs physical impact) and on "
     "predictability, and correctly restricts aspersion to advective frost rather than "
     "treating all frost protection as interchangeable.", "box"),
   P("Part b) states the unifying fact \u2014 no cure exists \u2014 <i>before</i> working "
     "through the four examples, so the vector-control pattern reads as the answer's "
     "organising idea rather than four disconnected facts.", "box"),
 ]),
]

q2 = [
 answer_head("Part a) Comparing powdery and downy mildew"),
 P("Powdery and downy mildew are the two fungal diseases most often confused, precisely "
   "because they sound similar but behave almost as opposites."),
 P("<b>Powdery mildew</b> (Erysiphe necator) lives on the vine's <b>surface</b>. It grows "
   "fastest around <b>25\u00b0C</b>, thrives in <b>shade</b>, and \u2014 unusually for a mildew "
   "\u2014 <b>doesn't need high humidity</b>, so it spreads even in dry conditions. Affected "
   "tissue shows dull grey patches darkening to black, damaging shoots, inflorescences and "
   "grapes, which can split at v\u00e9raison. Chardonnay and Cabernet Sauvignon are notably "
   "susceptible, Pinot Noir and Riesling less so. Sulfur, applied from shortly after "
   "budburst through v\u00e9raison, is standard preventive treatment, since the disease is far "
   "easier to prevent than to contain once established."),
 P("<b>Downy mildew</b> (Peronospora) is a water mould living <b>within</b> vine tissue, and "
   "needs the opposite conditions: <b>rainfall plus warmth</b> around 20\u00b0C, with warm "
   "springs or warm, stormy summers the highest-risk periods. It attacks young leaves and "
   "flowers, mainly damaging yield through <b>defoliation</b>, shown as yellow \u2018oil "
   "spots\u2019 followed by white downy growth on leaf undersides. <b>Copper</b> \u2014 "
   "traditionally Bordeaux mixture, copper sulfate and lime \u2014 is standard treatment and "
   "the only option currently available to organic growers, though protection lasts only "
   "until 20 mm of rain has fallen, and EU policy is moving to reduce copper use given soil "
   "and water build-up concerns."),
 P("The shared lever is an <b>open canopy</b>: it reduces the shade powdery mildew favours, "
   "and speeds the drying that denies downy mildew the moisture it needs \u2014 the same "
   "intervention working through two different mechanisms."),

 answer_head("Part b) Compounding pest and disease pressure"),
 P("Several pests and diseases in this chapter don't act independently \u2014 damage from one "
   "creates the conditions or entry point for another, so evaluating them in isolation "
   "understates the real risk."),
 P("Wounds from <b>grape moths</b> feeding on flowers and grapes, and from <b>spider mites</b> "
   "damaging leaf surfaces, both open entry points that bacteria and fungi \u2014 including "
   "<b>botrytis</b> \u2014 can then exploit. <b>Hail</b> damage works the same way: physical "
   "injury to ripening grapes is itself an entry point for grey rot. <b>Grey rot</b> is "
   "explicit about this mechanism \u2014 grapes are vulnerable wherever there is any point of "
   "entry, from bunches rubbing in tight formation or bird or insect puncture, with spores "
   "already present in the vineyard simply waiting for rainfall and high humidity to "
   "activate."),
 P("This compounding effect has a practical consequence: canopy interventions aimed at one "
   "problem often help with several at once. An open canopy reduces shade (against powdery "
   "mildew), speeds drying (against downy mildew and grey rot), and improves spray "
   "penetration generally \u2014 so a grower managing canopy density for disease control "
   "is, in effect, managing several compounding risks with a single intervention rather than "
   "treating each threat as separate."),
 examiner_note([
   P("Part a) compares the two mildews on the same four criteria \u2014 location on the vine, "
     "conditions, symptoms, treatment \u2014 and closes by identifying that the shared "
     "\u2018open canopy\u2019 lever works through different mechanisms for each, which is the "
     "kind of synthesis a straight list of facts doesn't reach.", "box"),
   P("Part b) draws a connection across sections the chapter doesn't state explicitly \u2014 "
     "that wound-causing pests and hail both function as disease entry points \u2014 and then "
     "uses it to explain why a single canopy intervention has compounding value, which is "
     "exactly the kind of independent synthesis Distinction-level answers are expected to "
     "produce.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="Weather hazards and vine diseases both significantly affect yield and quality, "
           "and management strategies vary by cause.",
      parts=[("Compare frost and hail as vineyard hazards, and the management options "
              "available for each.", "15%"),
             ("Explain why the management of bacterial and viral diseases in the vineyard "
              "typically focuses on controlling the vector rather than treating the disease "
              "itself.", "10%")],
      answer=q1),
 dict(stem="Fungal diseases are a major source of yield and quality loss across virtually all "
           "wine regions.",
      parts=[("Compare powdery mildew and downy mildew.", "15%"),
             ("Explain how pest damage can compound the risk from fungal disease, and how "
              "this affects canopy management decisions.", "10%")],
      answer=q2),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch8_Hazards_Pests_and_Diseases.pdf",
      "Chapter Eight \u00b7 Hazards, Pests and Diseases", s, exam, maxpages=19)
