# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 1: The Vine."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb import *
import wb_art as A

CHAP, TITLE = "1", "The Vine"
K = Key()
story = []
add = story.append


def page():
    add(PageBreak())


# ---------------------------------------------------------------------------- tracker data
ITEMS = [("1.1", 8), ("1.2", 10), ("1.3", 8), ("1.4", 7), ("1.5", 6), ("1.6", 11), ("1.7", 5), ("1.8", 6),
         ("1.9", 9), ("1.10", 6), ("1.11", 5), ("1.12", 5), ("1.13", 12), ("1.14", 5), ("1.15", 3)]

# =============================================================================== PAGE 1
add(Opener(CHAP, TITLE,
           ["name the four structural zones of the vine and what each does",
            "label the shoot, the grape and the flower\u2019s parts from memory",
            "tell compound buds from prompt buds, and laterals from the main shoot",
            "choose between cuttings, layering, clonal and mass selection, and say why",
            "separate a cross from a hybrid"],
           "Mastery Guide Chapter 1"))

# ---- 1.1 brain dump
add(ExHeader("1.1", "RETRIEVE", "Brain dump", 8, mins=3, ref="Guide \u00a72\u20133"))
add(instr("Before you look at anything: write down everything you remember about the vine\u2019s four structural "
          "zones and what each one does. Add anything you know about buds. Set a 3-minute timer. "
          "<b>1 point per correct, separate fact (max 8).</b>"))
add(WriteBox(78, border=True, label="WRITE EVERYTHING YOU REMEMBER"))
K.add("1.1", "Brain dump \u2014 facts to look for (1 point each, max 8)", [
    kp("<b>Zones:</b> shoots (the canopy) \u00b7 one-year-old wood (cane or spur; carries the compound buds) \u00b7 "
       "permanent wood (trunk, cordons) \u00b7 roots (anchor; uptake; storage; hormones; top 50 cm, some beyond 6 m). "
       "<b>Buds:</b> compound (form one season, break the next) vs prompt (same season; make laterals)."),
])

# ---- 1.2 match
add(ExHeader("1.2", "MATCH", "Key terms", 10, mins=4, ref="Guide \u00a72\u20136"))
add(instr("Write the letter of the matching definition in each box. Each definition is used once."))
_pairs = [
    ("Node", "Swelling along a shoot where leaves, buds and tendrils attach"),
    ("Internode", "The length of shoot between two nodes"),
    ("Cane", "A shoot that has turned woody, rigid and brown"),
    ("Compound bud", "Forms in one season, breaks open in the next; holds a primary bud plus back-up buds"),
    ("Prompt bud", "Forms and breaks open in the same season, producing lateral shoots"),
    ("Lateral shoot", "Smaller, thinner shoot that lets the vine keep growing if the main tip is damaged"),
    ("Tendril", "Coils round trellis wires to hold the shoot up"),
    ("Stomata", "Pores on the underside of a leaf that let water out and carbon dioxide in"),
    ("Bloom", "Powdery, waxy coating on the surface of the grape"),
    ("Cordon", "A horizontal arm of permanent wood"),
]
_disp = [6, 2, 9, 4, 0, 7, 3, 8, 1, 5]            # display order of the definitions
_right = [_pairs[i][1] for i in _disp]
_letters = [chr(65 + _disp.index(i)) for i in range(10)]
add(match([p[0] for p in _pairs], _right, _letters))
K.add("1.2", "Match", [pairs([(str(i + 1), _letters[i]) for i in range(10)], ncols=5, width=COLW)])
page()

# =============================================================================== PAGE 2
add(ExHeader("1.3", "LABEL", "The vine\u2019s four structural zones", 8, mins=4, ref="Guide \u00a72, \u00a77"))
add(instr("Name each zone on the blanks, then write <b>one job</b> it does. "
          "(4 points for names, 4 for jobs.)"))
_zones = A.Zones(330)
add(LabelFigure(_zones, align="left", sub="Its job:"))
_zsubs = {"Shoots (the canopy)": "leaves photosynthesize; carry buds, flowers, bunches",
          "One-year-old wood": "carries compound buds for next season (cane or spur)",
          "Permanent wood": "support, transport, store carbohydrates and nutrients",
          "Roots": "anchor; take up water and nutrients; store; make hormones"}
K.add("1.3", "Label the four zones",
      [kp(label_key(_zones) + ".  <i>Jobs (any one each):</i> shoots \u2014 photosynthesis; carry buds, laterals, tendrils, "
          "bunches \u00b7 one-year-old wood \u2014 carries next season\u2019s compound buds (cane or spur) \u00b7 "
          "permanent wood \u2014 support, transport, storage \u00b7 roots \u2014 anchorage, uptake, storage, hormones.")])

add(ExHeader("1.4", "LABEL", "The grape in cross-section", 7, mins=3, ref="Guide \u00a76"))
add(instr("Label the five parts. Then answer the two quick questions underneath."))
_grape = A.Grape(330)
add(LabelFigure(_grape, align="left"))
add(LineFill("a)  Most of the grape\u2019s weight and volume is its", w=W, h=19))
add(LineFill("b)  Grapes with red-colored pulp (e.g. Alicante Bouschet) are called", w=W, h=19))
K.add("1.4", "Label the grape",
      [kp(label_key(_grape) + ".  <b>a)</b> pulp \u00b7 <b>b)</b> teinturier varieties.")])
page()

# =============================================================================== PAGE 3
add(ExHeader("1.5", "LABEL", "A shoot at flowering", 6, mins=3, ref="Guide \u00a73\u20135"))
add(instr("Label the six structures. One of them is the only part drawn in brown wood."))
_shoot = A.Shoot(252)
add(LabelFigure(_shoot, align="center"))
K.add("1.5", "Label the shoot", [kp(label_key(_shoot))])

add(ExHeader("1.6", "COMPLETE", "Structures and what they do", 11, mins=5, ref="Guide \u00a75"))
add(instr("Fill each numbered blank using the word bank. <b>Four words are distractors</b> and are not used."))
_bank = sorted(["canopy", "nodes", "internodes", "canes", "leaves", "stomata", "transpiration", "photosynthesis",
                "tendrils", "inflorescence", "bunch", "cordons", "respiration", "laterals", "bloom"])
add(WordBank(_bank, ncols=5))
_c, _a = cloze([
    "The shoots and all their structures are collectively called the {{canopy}}. The little swellings along a "
    "shoot are {{nodes}}, and the lengths between them are {{internodes}}. In late summer shoots lignify "
    "(turn woody) and are then called {{canes}}. The {{leaves}} are the main site of photosynthesis; pores "
    "called {{stomata}} on the underside let carbon dioxide in, and as water diffuses out, {{transpiration}} "
    "draws water and nutrients up from the soil. A water-stressed vine partly closes these pores, which saves "
    "water but limits {{photosynthesis}}. A shoot cannot support itself, so {{tendrils}} curl round the trellis "
    "wires. A cluster of flowers on a stem is an {{inflorescence}}; once fertilized it becomes a {{bunch}}.",
], width=72)
for f in _c:
    add(f)
K.add("1.6", "Complete", [kp(" \u00b7 ".join("<b>(%d)</b> <font color=\"%s\"><b>%s</b></font>" % (i + 1, hexc(ANS), a)
                                         for i, a in enumerate(_a)) +
                         ".  <i>Distractors:</i> cordons, respiration, laterals, bloom.")])
page()

# =============================================================================== PAGE 4
add(ExHeader("1.7", "COMPARE", "Compound buds and prompt buds", 5, mins=4, ref="Guide \u00a73"))
add(instr("Complete the profile: some cells are given, the dotted ones are yours."))
_cw = [112, 203, 203]
_rows = [
    ["Forms and breaks open", "Forms in one growing season; breaks open in the next",
     Blank("Forms and breaks open in the same growing season", 2)],
    ["Produces", Blank("The shoots of the next growing season", 2), "Lateral shoots"],
    ["What is inside / where it forms", Blank("A primary bud (main growing point) plus smaller secondary and tertiary buds", 2),
     Blank("Forms on the primary shoot that has just grown from a compound bud", 2)],
    ["Also called", Blank("Latent bud"), "(no other name needed)"],
]
add(compare(["", "Compound bud", "Prompt bud"], _rows, _cw))
K.add("1.7", "Compare the buds", [compare(["", "Compound bud", "Prompt bud"], _rows, [58, 96, 96], key=True, compact=True)])

add(ExHeader("1.8", "DECIDE", "True or false \u2014 then fix it", 6, mins=5, ref="Guide \u00a74\u20136"))
add(instr("Circle T or F. If a statement is false, rewrite it correctly on the line. "
          "<b>1 point only if both the call and the correction are right.</b>"))
_tf = [
    ("Lateral shoots grow from compound buds.", False, "They grow from prompt buds."),
    ("Lateral shoots near the base of a shoot are desirable because they improve air flow.", False,
     "They are undesirable: they impede air flow and shade the fruit."),
    ("A second crop ripens later than the main crop, so if picked together it brings higher acidity and lower sugar.", True, ""),
    ("Machine harvesting lets a grower leave the second crop unpicked.", False,
     "Hand harvesting allows selective picking; a machine cannot separate the second crop."),
    ("Tight bunches, as in Pinot Noir, are more prone to fungal disease.", True, ""),
    ("The pulp of most grapes is red.", False, "It is colorless; only teinturier varieties have red pulp."),
]
for i, (t, v, fix) in enumerate(_tf):
    add(TFItem(i + 1, t))
K.add("1.8", "True or false", [numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                                          ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fix)))
                                         for i, (t, v, fix) in enumerate(_tf)])])
page()

# =============================================================================== PAGE 5
add(ExHeader("1.9", "SORT", "Cutting, layering or seed?", 9, mins=4, ref="Guide \u00a78"))
add(instr("Write each item\u2019s number in the column it describes. Every item belongs in exactly one column."))
_items9 = [
    "A cane is bent down and part of it is buried",
    "Lets the young vine be grafted onto a rootstock before planting",
    "Offspring are not genetically identical to the parent",
    "The most common technique in modern viticulture",
    "Fills a gap using a shoot from a neighboring vine",
    "Used to breed new grape varieties",
    "Nurseries can treat the material to stop disease spreading",
    "The new vine grows on its own roots, with no rootstock",
    "Not used to propagate existing vines in viticulture",
]
add(sort_bank(_items9, ncols=3))
add(Spacer(1, 6))
add(sort_columns(["Cuttings", "Layering", "Seed"], h=52))
K.add("1.9", "Sort", [kp("<b>Cuttings:</b> 2, 4, 7 \u00b7 <b>Layering:</b> 1, 5, 8 \u00b7 <b>Seed:</b> 3, 6, 9")])

add(ExHeader("1.10", "DECIDE", "Clonal selection or mass selection?", 6, mins=3, ref="Guide \u00a79\u201310"))
add(instr("Circle <b>A</b> if the statement describes clonal selection (buying clones from a nursery) or <b>B</b> if it "
          "describes mass selection (taking cuttings from your own best vines)."))
_s10 = [
    "Cuttings come from a nursery that has tested the vines to be free of virus.",
    "Cuttings are taken from several of the grower\u2019s own best-performing vines.",
    "Risk: if the parent vine carries a virus, every new vine inherits it.",
    "Only a few clones may be available, so vineyards can end up very uniform.",
    "Gives the estate planting material that is uniquely its own \u2014 a possible marketing asset.",
    "Became common only in the last 40\u201350 years.",
]
_a10 = [0, 1, 1, 0, 1, 0]
add(choose(_s10, ["A", "B"]))
K.add("1.10", "Clonal or mass?", [kp("<b>1</b> A \u00b7 <b>2</b> B \u00b7 <b>3</b> B \u00b7 <b>4</b> A \u00b7 <b>5</b> B \u00b7 <b>6</b> A")])

add(ExHeader("1.11", "COMPLETE", "The Pinot family", 5, mins=2, ref="Guide \u00a79"))
add(instr("Write the missing word or number in each blank. No word bank this time."))
_c, _a = cloze([
    "Pinot Noir Clone {{115}} gives low yields of small grapes, suited to high-quality red wine. Clone {{521}} "
    "gives higher yields of bigger grapes, better for {{sparkling}} wine because high levels of {{tannin}} and "
    "color are not needed. Pinot Noir, Meunier, Pinot Blanc and Pinot Gris are all {{mutations}} of one variety, Pinot.",
], width=56)
for f in _c:
    add(f)
K.add("1.11", "The Pinot family", [kp(" \u00b7 ".join("<b>(%d)</b> <font color=\"%s\"><b>%s</b></font>" % (i + 1, hexc(ANS), a)
                                                    for i, a in enumerate(_a)))])
page()

# =============================================================================== PAGE 6
add(ExHeader("1.12", "MATCH", "Who are the parents?", 5, mins=3, ref="Guide \u00a711"))
add(instr("Match each variety to its parentage. A <b>cross</b> has two parents of the same species; a "
          "<b>hybrid</b> has parents of different species."))
_p12 = [("Pinotage", "Pinot Noir \u00d7 Cinsaut \u2014 a cross"),
        ("Vidal Blanc", "Ugni Blanc (<i>V. vinifera</i>) \u00d7 a Seibel variety of American parentage"),
        ("M\u00fcller-Thurgau", "Riesling \u00d7 Madeleine Royale \u2014 bred for Riesling\u2019s quality plus high yield"),
        ("Cabernet Sauvignon", "Probably a chance cross of Sauvignon Blanc and Cabernet Franc")]
_d12 = [2, 3, 0, 1]
_r12 = [_p12[i][1] for i in _d12]
_l12 = [chr(65 + _d12.index(i)) for i in range(4)]
add(match([p[0] for p in _p12], _r12, _l12))
add(Spacer(1, 3))
add(LineFill("Which of the four is a hybrid?", w=W, h=19))
K.add("1.12", "Who are the parents?", [kp("<b>1</b> %s \u00b7 <b>2</b> %s \u00b7 <b>3</b> %s \u00b7 <b>4</b> %s. "
                                          "The hybrid is <b>Vidal Blanc</b> (two species)." % tuple(_l12))])

# ---- 1.13 crossword
_words = [
    ("NODE", "Swelling on a shoot where leaves and buds attach"),
    ("INTERNODE", "Length of shoot between two nodes"),
    ("TENDRIL", "Coils round a trellis wire for support"),
    ("STOMATA", "Pores on the underside of a leaf"),
    ("CORDON", "Horizontal arm of permanent wood"),
    ("CLONE", "A group of vines with identical characteristics, from one selected vine"),
    ("HYBRID", "Offspring of parents from two different species"),
    ("BLOOM", "Powdery, waxy coating on a grape"),
    ("CANE", "A lignified shoot"),
    ("PINOTAGE", "Cross of Pinot Noir and Cinsaut"),
    ("LAYERING", "Burying a cane so it roots and fills a gap"),
    ("LATERAL", "Shoot that grows from a prompt bud"),
    ("CUTTING", "The most common propagation method"),
    ("ROOTSTOCK", "What a <i>V. vinifera</i> cutting is grafted onto"),
    ("LIGNIFY", "Turn woody, rigid and brown"),
    ("CANOPY", "Shoots plus all their structures"),
    ("PETIOLE", "A leaf stalk"),
    ("SPUR", "Short length of one-year-old wood"),
]
_cw1 = make_crossword(_words, size=13, seed=11, tries=500)
_nw = len(_cw1["clues"]["A"]) + len(_cw1["clues"]["D"])
add(ExHeader("1.13", "CROSSWORD", "Chapter 1 vocabulary", _nw, mins=6, ref="Guide \u00a72\u201311"))
add(instr("One point per word. Answers are single words, no spaces."))
add(crossword_block(_cw1, key=False, cell=17.0))
K.add("1.13", "Crossword", crossword_answers(_cw1))
ITEMS[12] = ("1.13", _nw)
page()

# =============================================================================== PAGE 7
add(ExHeader("1.14", "CHOOSE", "Multiple choice", 5, mins=4, ref="Guide \u00a77\u201311"))
add(instr("Circle one answer. The live D1 paper is written, not multiple choice \u2014 use these to find gaps."))
_mc = [
    ("A grower wants to fill a gap left by a dead vine, using a shoot from a neighboring vine. Which method is this?",
     ["Layering", "Mass selection", "Cross fertilization", "Clonal selection"], 0),
    ("A second crop on a lateral shoot, harvested with the main crop, tends to bring:",
     ["Lower acidity and higher sugar", "Higher acidity and lower sugar", "More color in black grapes", "Riper tannins"], 1),
    ("Most of a vine\u2019s roots are found in roughly the top:",
     ["5 cm of soil", "50 cm of soil", "2 m of soil", "6 m of soil"], 1),
    ("Why are vines not propagated from seed in viticulture?",
     ["Vine seeds are sterile", "Seedlings are not genetically identical to the parent, so they differ in character",
      "Seeds cannot be registered with the OIV", "Seeds cannot be grafted"], 1),
    ("A hybrid differs from a cross in that its two parents:",
     ["Are the same species", "Are different species", "Are both rootstocks", "Are both clones"], 1),
]
for i, (q, o, a) in enumerate(_mc):
    add(MCQ(i + 1, q, o))
K.add("1.14", "Multiple choice", [numbered([
    ("1", "<b>A</b> \u2014 layering buries a cane from a neighbor"),
    ("2", "<b>B</b> \u2014 later ripening: higher acid, lower sugar"),
    ("3", "<b>B</b> \u2014 top 50 cm (a few reach 6 m)"),
    ("4", "<b>B</b> \u2014 seedlings differ from the parent"),
    ("5", "<b>B</b> \u2014 a cross is within a species")])])

add(ExHeader("1.15", "EXPLAIN", "Write like an examiner", 3, mins=5, ref="Guide \u00a79"))
add(instr("Answer in three or four sentences, then self-mark against the checklist. <b>Cause and effect earns marks</b>; a list does not."))
for f in explain("Explain why a grower might plant <b>several different clones</b> of one grape variety rather than a single clone.", [], lines=4):
    add(f)
_pts = ["Clones differ slightly (for example in yield, grape size, skin thickness or disease resistance), so planting several adds diversity to the fruit.",
        "More diversity can give a wine more complexity and balance, if that suits the style.",
        "Identical vines are likely to be equally susceptible to the same disease or pest, so mixing clones spreads the risk.",
        "Trade-off: one clone ripens uniformly and is simpler to manage, but loses the benefits above."]
add(Checklist(_pts))
K.add("1.15", "Explain \u2014 mark points (any 3 of 4 = full marks)", [kp("\u2022 " + p) for p in _pts])

# =============================================================================== PAGE 8: ANSWER KEY  (the key supplies its own page break)
for f in K.flowables(CHAP, TITLE, ITEMS):
    add(f)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch1.pdf"
    n = build_pdf(out, CHAP, TITLE, story)
    print("Chapter 1 workbook: %d pages -> %s" % (n, out))
