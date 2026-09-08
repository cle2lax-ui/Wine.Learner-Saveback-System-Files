# -*- coding: utf-8 -*-
"""Chapter Mastery Guide 1 — The Vine"""
from mastery import *
from graphics import *
from examkit import mcq_section, swa_section, answer_head, examiner_note, exam_traps
from reportlab.platypus import PageBreak

W = L_W
s = []

s += H1("Chapter One: The Vine",
        "D1 Chapter Mastery Guide &nbsp;\u00b7&nbsp; 1.1 Anatomy of the Vine \u00b7 1.2 Vine Propagation")

s.append(P("Chapter One is small but load-bearing. Rarely a whole question, it supplies the "
           "vocabulary every later question depends on \u2014 compound versus prompt bud, one-year-old "
           "versus permanent wood \u2014 without which pruning, canopy management and yield cannot be "
           "discussed coherently."))
s.append(P("Two topics recur as questions in their own right: the <b>second crop</b> (composition, "
           "effect on the wine, management) and <b>propagation choices</b> \u2014 clonal versus mass "
           "selection, cross versus hybrid. Learn those to essay depth, the rest to definition depth."))

# ---------------------------------------------------------------- species
s.append(H2("1. Species"))
s.append(EXHIBIT("EXHIBIT 1.1 \u2014 THE SPECIES YOU MUST BE ABLE TO NAME", [
    ["Species", "Origin", "Role in wine production"],
    ["<b>Vitis vinifera</b>", "Eurasia", "Over <b>1,000</b> varieties; virtually all commercial "
     "wine"],
    ["V. labrusca", "N. America", "Rootstock; limited direct wine use"],
    ["V. riparia", "N. America", "Rootstock. Waterlogging tolerance; low vigour"],
    ["V. berlandieri", "N. America", "Rootstock. Lime and salinity tolerance"],
    ["V. rupestris", "N. America", "Rootstock. Drought tolerance; high vigour"],
], [78, 54, W - 132]))
s.append(P("North American species are used directly for wine in a few regions \u2014 New York State \u2014 "
           "but their principal global function is as <b>rootstock</b> for grafted V. vinifera.",
           "note"))

# ---------------------------------------------------------------- structure
s.append(H2("2. The Four Structural Zones"))
s.append(FIGURE("FIGURE 1.1 \u2014 THE FOUR STRUCTURAL ZONES", VineSchematic()))
s += BUL([
    "The shoot's main axis <b>transports water and solutes</b> and <b>stores carbohydrates</b>.",
    "<b>Nodes</b> are the swellings where structures attach; <b>internodes</b> the lengths between.",
    "In late summer shoots <b>lignify</b> \u2014 woody, rigid, brown \u2014 and are then called "
    "<b>canes</b>.",
])

# ---------------------------------------------------------------- buds
s.append(H2("3. Buds"))
s.append(EXHIBIT("EXHIBIT 1.2 \u2014 COMPOUND VERSUS PROMPT BUDS", [
    ["", "Compound (latent)", "Prompt"],
    ["Forms", "One growing season", "Current growing season"],
    ["Bursts", "The <i>next</i> season, if retained at pruning", "The <i>same</i> season"],
    ["Produces", "Next season's primary shoots", "Lateral shoots"],
    ["Structure", "Primary + smaller secondary and tertiary buds", "Single growing point"],
    ["Significance", "Secondary / tertiary grow only if the primary is damaged \u2014 e.g. spring "
     "frost", "The origin of the <b>second crop</b>"],
], [60, (W - 60) * 0.52, (W - 60) * 0.48]))
s.append(P("Buds form between petiole and stem, holding in miniature every future green "
           "structure of the vine.", "note"))

# ---------------------------------------------------------------- laterals
s.append(H2("4. Lateral Shoots and the Second Crop"))
s.append(H4("LATERAL SHOOTS \u2014 THINNER AND SMALLER, SAME STRUCTURES"))
s += BUL([
    "<b>Insurance:</b> allow growth to continue if the primary shoot tip is damaged or eaten.",
    "<b>Useful near shoot ends</b> \u2014 extra photosynthetic surface catching sunlight.",
    "<b>Undesirable near the base</b> \u2014 impede air flow, over-shade fruit. Removed in summer "
    "pruning.",
])
s.append(H4("THE SECOND CROP \u2014 BUNCHES FROM INFLORESCENCES ON LATERALS"))
s.append(FlowChart([
    ("Set later than the main crop", None, None),
    ("Therefore <b>ripen later</b>", None, None),
    ("If picked with the main crop:",
     "higher acidity \u00b7 lower sugar \u00b7 unripe tannins and aromas \u00b7 less colour in black grapes",
     None),
    ("Diluted, unbalanced, green-tasting must", None, None),
], box_w=W * 0.74))
s.append(EXHIBIT("EXHIBIT 1.3 \u2014 THE THREE MANAGEMENT ROUTES", [
    ["Route", "What it involves"],
    ["<b>Green harvesting</b>", "Remove the second crop in the growing season \u2014 thought to "
     "enhance ripening and even out the bunches that remain"],
    ["<b>Selective hand harvesting</b>", "Leave it unpicked, or pick and keep it separate"],
    ["<b>Accept it</b>", "The only option under <b>machine harvesting</b>, where selectivity is "
     "impossible \u2014 affecting the must and wine"],
], [104, W - 104]))
s.append(P("Susceptibility is variety- and canopy-dependent; <b>Pinot Noir</b> is the textbook "
           "example.", "note"))

# ---------------------------------------------------------------- other structures
s.append(H2("5. Tendrils, Leaves, Inflorescences, Bunches"))
s.append(EXHIBIT("EXHIBIT 1.4 \u2014 THE REMAINING SHOOT STRUCTURES", [
    ["Structure", "What you must be able to say"],
    ["Tendrils", "The shoot cannot support itself \u2014 tendrils curl around trellis wires, though "
     "growers still tie in canes and shoots"],
    ["Leaves", "Main site of <b>photosynthesis</b>. <b>Stomata</b> release water and admit CO\u2082; "
     "that loss drives <b>transpiration</b>, pulling water and nutrients from the soil. Under "
     "stress, stomata partly close \u2014 water saved, photosynthesis limited"],
    ["Inflorescences", "A cluster of flowers becoming a bunch at fruit set. Usually <b>one to "
     "three per shoot</b>, by variety"],
    ["Bunches", "A fertilised inflorescence; not all flowers become grapes. <b>Tight bunches</b> "
     "(Pinot Noir) raise fungal risk \u2014 skins split more readily, air cannot circulate"],
], [70, W - 70], keep=False))

# ---------------------------------------------------------------- grape
s.append(H2("6. The Grape"))
s.append(FIGURE("FIGURE 1.2 \u2014 THE GRAPE IN CROSS-SECTION", BerrySection()))
s.append(P("<b>Exception:</b> <b>teinturier</b> varieties have red-coloured pulp \u2014 Alicante "
           "Bouschet \u2014 but are uncommon.", "note"))

# ---------------------------------------------------------------- roots
s.append(H2("7. Roots and Older Wood"))
s += BUL([
    "<b>Roots:</b> anchor, take up water and nutrients, store carbohydrates, <b>produce "
    "hormones</b> for growth and ripening. Absorption occurs <b>at the root tips</b>.",
    "Root distribution follows <b>soil properties, irrigation, cultivation and rootstock type</b>.",
    "<b>Permanent wood</b> \u2014 trunk and cordons \u2014 supports, transports water and solutes, and "
    "stores carbohydrates and nutrients.",
    "<b>One-year-old wood</b> reflects the grower's pruning and training, and carries the "
    "compound buds for next season.",
])

# ---------------------------------------------------------------- propagation
s.append(H2("8. Propagation"))
s.append(P("Vines propagate by <b>cuttings</b> or <b>layering</b>, both normally producing plants "
           "<b>genetically identical to the parent</b>. Seed is not used \u2014 seedlings differ from "
           "their parents \u2014 except when deliberately creating new varieties."))
s.append(EXHIBIT("EXHIBIT 1.6 \u2014 CUTTINGS VERSUS LAYERING", [
    ["", "Cuttings", "Layering"],
    ["Method", "A shoot section is planted and grows as a new vine",
     "A cane from a neighbouring vine is bent down and partly buried, tip up; cut free once "
     "rooted"],
    ["Use", "The dominant technique; many can be propagated at once",
     "<b>Filling gaps</b> in an existing vineyard"],
    ["Rootstock", "<b>Permits grafting</b> before planting", "<b>Own roots</b> \u2014 no rootstock"],
    ["Consequence", "Nurseries can treat cuttings against disease spread",
     "<b>No phylloxera protection</b>, none of a rootstock's qualities (vigour, yield, drought "
     "tolerance)"],
], [52, (W - 52) * 0.44, (W - 52) * 0.56]))

# ---------------------------------------------------------------- clones
s.append(H2("9. Clones and Clonal Selection"))
s += BUL([
    "Random <b>mutation</b> at cell division creates diversity <i>within</i> a variety \u2014 berry "
    "size, skin thickness, disease resistance.",
    "Selecting and propagating favourable individuals is <b>clonal selection</b>, giving "
    "distinct <b>clones</b>.",
    "A major mutation may yield a new variety: <b>Pinot Noir, Meunier, Pinot Blanc and Pinot "
    "Gris are all mutations of Pinot</b>.",
])
s.append(EXHIBIT("EXHIBIT 1.7 \u2014 THE CLONE EXAMPLE THE EXAMINER EXPECTS", [
    ["Clone", "Characteristics", "Best suited to"],
    ["Pinot Noir <b>115</b>", "Low yields of small grapes", "High quality red wine"],
    ["Pinot Noir <b>521</b>", "Higher yields of bigger grapes",
     "Sparkling \u2014 high skin tannin and colour not required"],
], [66, (W - 66) * 0.44, (W - 66) * 0.56]))
s.append(H4("BUYING FROM A NURSERY \u2014 THE TRADE-OFF"))
s += BUL([
    "<b>For:</b> vines are <b>tested free of virus infection</b>.",
    "<b>Against:</b> often few clones are available, making plantings across a vineyard or "
    "region relatively uniform.",
    ("Uniformity cuts both ways:", [
        "<b>Advantage:</b> vines grow and ripen alike \u2014 simpler management.",
        "<b>Disadvantage:</b> less fruit diversity, so potentially less complexity; and "
        "greater disease risk, since identical vines are equally vulnerable.",
    ]),
    "Growers therefore often plant <b>several clones of the same variety</b> where available.",
])

# ---------------------------------------------------------------- mass selection
s.append(H2("10. Mass Selection (S\u00e9lection Massale)"))
s += BUL([
    "Clonal selection is recent \u2014 common only in the last <b>40 to 50 years</b>. Mass "
    "selection predates it and is regaining popularity.",
    "Cuttings come from <b>several of the grower's own best-performing vines</b>, chosen after "
    "<b>years of monitoring and recording</b>.",
    "Cuttings can go to a nursery for grafting onto rootstock where needed.",
])
s.append(EXHIBIT("EXHIBIT 1.8 \u2014 MASS SELECTION: THE BALANCE SHEET", [
    ["Advantages", "Disadvantages"],
    ["Increases <b>diversity</b> of planting material in vineyard and region",
     "<b>Costly in time and labour</b> to select and monitor"],
    ["<b>Unique planting material</b>, different from the local nursery's \u2014 can enhance fruit "
     "quality and/or yield",
     "A diseased parent vine, typically viral, is likely to pass it on \u2014 "
     "<b>increasing disease spread</b>"],
    ["Uniqueness usable as a <b>marketing asset</b>", "\u2014"],
], [W / 2, W / 2]))

# ---------------------------------------------------------------- new varieties
s.append(H2("11. Creating New Varieties"))
s.append(FlowChart([
    ("CROSS FERTILISATION", "Pollen from the stamens of vine A \u2192 stigmas of vine B", None),
    ("SEEDS PLANTED AND GROWN", "Like siblings, every seedling differs from the others and from "
     "both parents", None),
    ("LONG ASSESSMENT PERIOD", "A promising individual is evaluated over years", None),
    ("REGISTRATION ON THE OIV CATALOGUE", "Required before commercial release", None),
    ("PROPAGATION BY CUTTINGS", "Identical vines of the new variety", None),
], box_w=W * 0.70))
s.append(EXHIBIT("EXHIBIT 1.9 \u2014 WHY THE BREEDING AIM OFTEN MISSES", [
    ["", "Cross", "Hybrid"],
    ["Aim", "Combine favourable traits of two vinifera parents",
     "Combine non-vinifera resistance (disease, pests, climatic extremes) with vinifera fruit "
     "quality"],
    ["Reality", "Often disappoints \u2014 <b>M\u00fcller-Thurgau</b> delivered the yield, not the "
     "quality of its Riesling parent",
     "Many fall short on fruit quality, but are valuable as <b>rootstocks</b>"],
], [50, (W - 50) * 0.46, (W - 50) * 0.54], keep=False))
s.append(FIGURE("FIGURE 1.4 \u2014 THE SPECIES BOUNDARY DECIDES THE TERM", LineageChart(
    lanes=[("V. VINIFERA", BURGUNDY), ("NON-VINIFERA", LEAF)],
    rows=[
        ("Pinot Noir", "A", "Cinsaut", "A", "Pinotage", "CROSS \u2014 same lane", BURGUNDY),
        ("Ugni Blanc", "A", "Seibel family", "B", "Vidal Blanc", "HYBRID \u2014 crosses the lane",
         LEAF),
    ])))
s.append(P("Both parents in <b>one</b> lane makes a <b>cross</b>; one parent from <b>each</b> "
           "lane makes a <b>hybrid</b>. The species boundary decides the term, not the breeding "
           "intent.", "note"))

s += BUL([
    "Many long-established varieties arose from <b>chance cross fertilisation</b>: Cabernet "
    "Sauvignon is very likely <b>Sauvignon Blanc \u00d7 Cabernet Franc</b>.",
    "Current breeding aims: resistance to <b>disease</b> (Pierce's Disease in California), "
    "<b>pests</b>, and <b>climatic extremes</b> such as drought.",
    "<b>Genetic markers</b> now identify offspring with wanted traits without waiting for the "
    "vine to grow and fruit, speeding programmes considerably.",
    "New varieties still rarely reach market \u2014 the main reason is <b>consumer resistance</b>.",
])

s.append(CALLOUT("DISTINCTION DIFFERENTIATORS \u2014 CHAPTER ONE", [
    P("<b>1. Never state a structure without its consequence.</b> Lateral shoots grow from prompt "
      "buds \u2014 <i>and</i> near the shoot base they shade fruit and block airflow, which is why "
      "they are summer-pruned.", "box"),
    P("<b>2. Second-crop answers need three stages.</b> Composition \u2192 effect on the wine \u2192 "
      "management, including that machine harvesting removes the option to be selective.", "box"),
    P("<b>3. Tie every propagation choice to risk.</b> Cuttings buy rootstock and clean material; "
      "layering forfeits both. Nursery clones buy sanitary security and uniformity; mass selection "
      "buys diversity at the cost of labour and virus transmission.", "box"),
    P("<b>4. Deploy the named examples.</b> Pinot Noir (tight bunches, second crop) \u00b7 PN 115 and "
      "521 (clones) \u00b7 Alicante Bouschet (teinturier) \u00b7 Pinotage (cross) \u00b7 Vidal (hybrid) \u00b7 "
      "M\u00fcller-Thurgau (the programme that half-worked).", "box"),
]))

s.append(exam_traps([
 ("\u201cCompound bud\u201d and \u201cprompt bud\u201d are routinely swapped under pressure.",
  "Compound = formed one season, bursts the <i>next</i>, holds primary/secondary/tertiary. "
  "Prompt = forms and bursts in the <i>same</i> season, gives lateral shoots. Mnemonic: a "
  "prompt bud is prompt."),
 ("Assuming the second crop is simply \u201cunripe fruit\u201d.",
  "Name all five consequences \u2014 higher acid, lower sugar, unripe tannins, unripe aromas, "
  "and less colour in black grapes. Answers that stop at \u201cunripe\u201d forfeit most of the marks."),
 ("Calling Pinotage a hybrid.",
  "Both parents are V. vinifera, so it is a <i>cross</i>. Vidal Blanc is the hybrid. Species "
  "boundary, not geography, decides the term."),
 ("Treating Pinot Gris, Pinot Blanc and Meunier as clones of Pinot Noir.",
  "They are <i>mutations of Pinot</i> significant enough to be classified as separate varieties. "
  "Clones are 115 and 521."),
 ("Claiming mass selection reduces disease risk because it avoids nurseries.",
  "The reverse. Nursery material is virus-tested; mass selection can <i>propagate</i> a virus "
  "from an infected parent. Mass selection buys diversity, not sanitary security."),
]))

exam = []

# ------------------------------------------------------------------ MCQ
MCQ = [
 dict(q="Which four structures are collectively referred to as the vine's canopy?",
      opts=["Trunk, cordons, canes and spurs",
            "The shoots and all their major structures \u2014 buds, leaves, lateral shoots, tendrils and inflorescences/bunches",
            "Leaves, tendrils, roots and permanent wood",
            "One-year-old wood, permanent wood, roots and shoots"],
      ans=1, why="The canopy is the shoots plus everything they carry. Options C and D wrongly "
                 "include below-ground or older woody structures."),
 dict(q="A prompt bud differs from a compound bud principally because it:",
      opts=["Contains a primary, secondary and tertiary growing point",
            "Forms in one growing season and bursts in the next",
            "Forms and bursts within the same growing season, producing lateral shoots",
            "Only bursts if the primary bud has been damaged by frost"],
      ans=2, why="A and B describe the compound (latent) bud; D describes the behaviour of "
                 "secondary and tertiary buds within a compound bud."),
 dict(q="Compared with the main crop harvested at the same time, second-crop bunches are typically:",
      opts=["Lower in acidity and higher in sugar",
            "Higher in acidity and lower in sugar, with unripe tannins and aromas",
            "Identical in composition but smaller in berry size",
            "Higher in sugar with more advanced colour development"],
      ans=1, why="The second crop sets and ripens later. In black grapes it also shows less "
                 "colour development."),
 dict(q="Approximately what proportion of the soil profile holds most of a vine's roots?",
      opts=["The top 15 cm", "The top 50 cm", "Between 1 and 2 m", "Below 6 m"],
      ans=1, why="Most roots sit in the top 50 cm, although roots have been found more than "
                 "six metres down."),
 dict(q="Which statement about layering is correct?",
      opts=["It is the most common propagation method because many plants can be raised at once",
            "It allows the grower to select a rootstock suited to the site",
            "It produces a vine growing on its own roots, with no phylloxera protection",
            "It is used chiefly to raise virus-free material in nurseries"],
      ans=2, why="Layering fills gaps in an existing vineyard. On its own roots, the new vine "
                 "has no phylloxera protection or rootstock benefit."),
 dict(q="Pinot Noir clone 521 is better suited to sparkling wine production than clone 115 because it:",
      opts=["Gives higher yields of bigger grapes, and high skin tannin and colour are not required",
            "Ripens substantially earlier and so retains higher acidity",
            "Has markedly thicker skins and greater disease resistance",
            "Is the only Pinot Noir clone permitted for sparkling wine"],
      ans=0, why="Clone 115 gives low yields of small grapes, suiting quality red wine. The "
                 "textbook distinguishes yield and berry size, not ripening date."),
 dict(q="Which is a genuine disadvantage of mass selection relative to buying clones from a nursery?",
      opts=["It reduces the diversity of planting material in the vineyard",
            "It prevents the use of rootstocks entirely",
            "Disease present in a parent vine is likely to be passed to the new vines",
            "It cannot be used for varieties with a long history of cultivation"],
      ans=2, why="Mass selection increases diversity (A is inverted) and can still use a "
                 "nursery for grafting (B is false). Virus transmission is the real risk."),
 dict(q="Pinotage is correctly described as:",
      opts=["A hybrid of a vinifera and an American species",
            "A cross of Pinot Noir and Cinsaut",
            "A clone of Pinot Noir selected in South Africa",
            "A mutation of Pinot"],
      ans=1, why="Both parents are V. vinifera, so it's a cross, not a hybrid. Vidal Blanc is "
                 "the hybrid; Pinot Gris, Pinot Blanc and Meunier are mutations of Pinot."),
 dict(q="Tannin and colour compounds are concentrated principally in the:",
      opts=["Pulp", "Skin", "Bloom", "Pulp of teinturier varieties only"],
      ans=1, why="The skin carries tannins, colour and most aroma compounds. Teinturier "
                 "varieties are the uncommon exception, with coloured pulp too."),
 dict(q="The principal reason newly bred grape varieties rarely reach the commercial market is:",
      opts=["Prohibitive cost of registration on the OIV catalogue",
            "The impossibility of propagating them true to type",
            "Consumer resistance",
            "A legal prohibition on planting hybrids outside North America"],
      ans=2, why="Registration and propagation are both routine. Consumer resistance is the "
                 "barrier the textbook identifies."),
]
exam += mcq_section(MCQ)

# ------------------------------------------------------------------ SWA
q1_ans = [
 answer_head("Part a) Structures of the shoot and their functions"),
 P("The shoot is the current season's green growth; together with what it carries, it forms the "
   "canopy. Its main axis transports water and solutes \u2014 sugars and minerals \u2014 and stores "
   "carbohydrate. Structures attach at nodes, separated by internodes."),
 P("<b>Buds</b> form between the petiole and stem and hold, in miniature, the future green parts "
   "of the vine. Compound buds form in one season and burst the next if retained at winter "
   "pruning, producing next year's primary shoots; each holds a primary growing point plus "
   "secondary and tertiary buds that grow only if the primary is damaged, by spring frost for "
   "example \u2014 the vine's insurance against frost loss. Prompt buds form and burst the same season, "
   "producing lateral shoots."),
 P("<b>Lateral shoots</b> are thinner than primary shoots but carry the same structures. Their "
   "role is insurance: growth continues if the primary tip is damaged or eaten. Value depends on "
   "position \u2014 laterals near primary shoot ends add useful photosynthetic capacity, while those "
   "near the base impede airflow and over-shade fruit, so are removed in summer pruning."),
 P("<b>Tendrils</b> exist because the shoot cannot support itself; in the vineyard they curl "
   "around trellis wires, though growers still tie in canes and shoots as needed."),
 P("<b>Leaves</b> are the main site of photosynthesis. Stomata on the underside admit CO\u2082 and "
   "release water vapour; that loss drives transpiration, drawing water and nutrients up from the "
   "soil. Under water stress the stomata partially close, conserving water but limiting "
   "photosynthesis since CO\u2082 can no longer enter \u2014 a trade-off recurring throughout the growing "
   "environment."),
 P("<b>Inflorescences</b>, usually one to three per shoot by variety, become bunches at fruit "
   "set. A <b>bunch</b> is a fertilised inflorescence; not all flowers become grapes, and bunch "
   "architecture varies by variety and clone. Tight bunches, as in Pinot Noir, raise fungal risk: "
   "skins split more readily and air cannot circulate within the bunch."),

 answer_head("Part b) The second crop: nature, effect and management"),
 P("The second crop is bunches from inflorescences on lateral rather than primary shoots. "
   "Laterals develop later, so these bunches set and ripen later. Whether a vine produces a "
   "significant second crop depends on variety and canopy management; Pinot Noir is notably "
   "prone to it."),
 P("Harvested alongside the main crop, second-crop bunches sit at an earlier point on the "
   "ripening curve: higher acidity, lower sugar, unripe tannins and aromas, and \u2014 in black "
   "grapes \u2014 less colour. Blended into the must they dilute sugar, depress potential alcohol, "
   "raise acidity, add green bitter phenolics and reduce colour \u2014 pulling the wine toward a "
   "herbaceous profile the producer did not intend."),
 P("Three management routes exist. <b>Green harvesting</b> removes the second crop during summer "
   "pruning, thought to enhance ripening and even out the bunches that remain, since the vine's "
   "resources are no longer split between two cohorts. <b>Selective hand harvesting</b> leaves it "
   "on the vine or picks it separately. The third option is simply to accept it."),
 P("The decisive constraint is harvest method. Only hand picking allows selectivity; a machine "
   "cannot distinguish second-crop bunches from main-crop ones, so mechanised harvest always lets "
   "the second crop into the must. A producer committed to machine harvesting must therefore "
   "address it earlier, in the canopy, through green harvesting \u2014 or accept the consequences in "
   "the glass."),
 examiner_note([
   P("The answer never names a structure without its consequence \u2014 the stomata line converts "
     "anatomy into the water-stress trade-off underpinning Chapter Three. Part b) runs "
     "composition \u2192 effect on wine \u2192 management, and closes by naming the harvest decision as "
     "the constraint governing which route is even available. That final move \u2014 a dependency, not "
     "a parallel list \u2014 is the Distinction marker.", "box"),
 ]),
]

q2_ans = [
 answer_head("Part a) Clonal selection and mass selection compared"),
 P("Both techniques propagate by cuttings, so both normally produce plants genetically identical "
   "to their parent. They differ in <i>which</i> parent material is chosen, and by whom."),
 P("Genetic diversity within a variety arises from random mutation at cell division. Most have no "
   "effect, but some alter berry size, skin thickness or disease resistance. <b>Clonal "
   "selection</b> propagates individuals carrying favourable mutations, giving distinct clones. "
   "Pinot Noir 115, low yields of small grapes, suits high quality red wine; Pinot Noir 521, "
   "higher yields of bigger grapes, suits sparkling, where high skin tannin and colour are not "
   "wanted. Clonal selection is recent \u2014 widespread only in the last forty to fifty years \u2014 and "
   "its commercial form is the nursery vine."),
 P("<b>Mass selection</b>, or s\u00e9lection massale, predates it and is regaining popularity. The "
   "owner takes cuttings from several of their own best-performing vines, chosen after years of "
   "monitoring, and may send them to a nursery for grafting where a rootstock is needed."),
 P("Nursery clones are tested virus-free, and let the grower match a clone to the intended style. "
   "Their disadvantage is availability: often only a few clones exist per variety, so plantings "
   "become relatively uniform \u2014 simpler to manage, since vines grow and ripen alike, but narrower "
   "in fruit diversity and more exposed to disease, since identical vines are equally vulnerable. "
   "Growers therefore often plant several clones where they can."),
 P("Mass selection inverts that balance. It increases diversity in the vineyard and region, and "
   "gives material distinct from the local nursery's \u2014 useful for fruit quality, yield or "
   "marketing. Its costs are labour-intensive selection and monitoring, and disease: an infected "
   "parent vine, typically viral, is likely to pass it on, actively spreading disease."),
 P("The choice is a judgement about priorities: nursery clones buy sanitary security and "
   "predictability; mass selection buys diversity and distinctiveness, at the cost of labour and "
   "sanitary risk."),

 answer_head("Part b) Crosses, hybrids and the barrier to market"),
 P("New varieties come from seed by cross fertilisation: pollen from one vine's stamens "
   "transfers to another's stigmas, seeds develop and are planted. Like siblings, the resulting "
   "vines all differ from each other and their parents. A promising individual is assessed over "
   "years and, if commercially valuable, registered on the OIV catalogue before release."),
 P("A <b>cross</b> has both parents from the same species \u2014 Pinotage, from Pinot Noir and "
   "Cinsaut, is the standard example. A <b>hybrid</b> has parents from different species; Vidal "
   "Blanc, from Ugni Blanc (V. vinifera) and a Seibel family member of American parentage, is the "
   "best-known wine hybrid."),
 P("The two programmes have different ambitions. Crosses combine favourable traits of two "
   "vinifera parents, though the outcome often disappoints: M\u00fcller-Thurgau, bred from Riesling "
   "and Madeleine Royale to unite Riesling's quality with Madeleine Royale's yield, delivered the "
   "yield but rarely the quality. Hybrids combine non-vinifera resistance \u2014 disease, pests, "
   "climatic extremes \u2014 with vinifera fruit quality. Many fall short on quality, with exceptions, "
   "but prove valuable as rootstocks. Disease resistance (Pierce's Disease in California), pest "
   "resistance and drought tolerance remain central breeding aims."),
 P("Breeding has accelerated: genetic markers now identify offspring with wanted "
   "characteristics without waiting for the vine to mature and fruit. Yet new varieties still "
   "rarely reach market, and the reason is commercial, not technical \u2014 <b>consumer "
   "resistance</b>. Buyers navigate by variety name, and an unfamiliar name carries no equity, a "
   "route-to-market problem better breeding technology cannot solve."),
 examiner_note([
   P("Part a) does not just list pros and cons. It names the underlying axis \u2014 sanitary "
     "security and predictability against diversity and distinctiveness \u2014 and frames the "
     "comparison around it, which is what an evaluative command word requires.", "box"),
   P("Part b) uses M\u00fcller-Thurgau as evidence that breeding aims and outcomes diverge, then "
     "closes by separating a technical constraint from a commercial one \u2014 the analytical step a "
     "pass-level answer omits.", "box"),
 ]),
]

exam += swa_section([
 dict(stem="The structure of the vine determines what the grape grower is able to manipulate.",
      parts=[("Describe the structures found on a vine shoot and explain the function of each.", "10%"),
             ("Explain what is meant by the 'second crop', the effect it can have on the finished "
              "wine, and the options available to the grape grower for managing it.", "15%")],
      answer=q1_ans),
 dict(stem="A grower establishing a new vineyard must decide where their planting material will "
           "come from.",
      parts=[("Compare clonal selection and mass selection, evaluating the advantages and "
              "disadvantages of each.", "15%"),
             ("Explain the difference between a cross and a hybrid, and explain why new grape "
              "varieties rarely reach the commercial market.", "10%")],
      answer=q2_ans),
])

build("/mnt/user-data/outputs/D1_Mastery_Guide_Ch1_The_Vine.pdf",
      "Chapter One \u00b7 The Vine", s, exam)
