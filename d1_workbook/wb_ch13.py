# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 13: General Winemaking Options."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("13", "General Winemaking Options",
             ["see oxygen as both a threat and a tool",
              "explain where added SO2 actually goes",
              "match each technique to the problem it solves",
              "know which options are legally restricted (EU zones)",
              "treat every technique as a choice with a cost"])

# ============================================================ PAGE 1
_r1 = ["Thiols in Sauvignon Blanc break down", "Needed at the start of fermentation for a healthy yeast population",
       "Drives the color-stabilizing anthocyanin\u2013tannin reaction in reds", "Builds the complexity of Oloroso, Madeira and Tawny Port",
       "Favors acetic acid bacteria and Brettanomyces"]
_a1 = ["Threat", "Needed", "Needed", "Needed", "Threat"]
ch.ex("TICK", "Oxygen: threat or tool?", 5, "Timing and amount decide. Tick one for each.",
      tickgrid(_r1, ["A threat", "Needed"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a1))), mins=3, ref="1")

_rings = [("Everything added: gas, liquid or solid", "Total SO2"), ("Unreacted; the rest is bound and ineffective", "Free SO2"),
          ("The small, active fraction", "Molecular SO2")]
ch.ex("NAME", "Where added SO2 goes", 4,
      "Only the innermost ring does the protective work. Name each ring, then finish the sentence. <b>3 points for rings, 1 for the sentence.</b>",
      [NestRings(_rings, key=False, height=160),
       LineFill("A high-pH must needs a (bigger / smaller) addition for the same protection:", w=W, h=19)],
      kp("<b>1</b> Total SO2 \u00b7 <b>2</b> Free SO2 \u00b7 <b>3</b> Molecular SO2. <b>Bigger:</b> lower pH pushes more free SO2 into the active "
         "molecular form, so a high pH leaves less of it active."), mins=3, ref="1")
ch.page()

# ============================================================ PAGE 2
_p3 = [("Chilling", "Slows oxidation and spoilage in warm grapes"),
       ("Sorting (triage)", "Removes unripe or rotten fruit and MOG"),
       ("Destemming", "Removes stem tannins; skipped for whole-bunch styles"),
       ("Crushing", "Breaks the skins just enough, without crushing the seeds"),
       ("Pressing", "Separates juice or wine from skins and seeds")]
_d3 = [3, 0, 4, 1, 2]
_l3 = [chr(65 + _d3.index(i)) for i in range(5)]
ch.ex("MATCH", "Grape reception: what each step does", 5, "Match each step to its purpose.",
      match([p[0] for p in _p3], [_p3[i][1] for i in _d3], _l3),
      pairs([(str(i + 1), _l3[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="2\u20134")

_bank = ["Basket press", "Continuous screw press", "Horizontal screw press", "Pneumatic press"]
ch.ex("NAME", "Name the press", 4,
      "Name each drawing from the word bank (one name is not drawn), then answer the last question. <b>3 points for names, 1 for the last.</b>",
      [WordBank(_bank, ncols=2), PanelFigure([A.PressPneumatic(150), A.PressBasket(150), A.PressContinuous(150)], gap=14),
       LineFill("Fast and less gentle, for high-volume inexpensive wine:", w=W, h=19)],
      kp("<b>1</b> Pneumatic press (most popular worldwide; medium\u2013large wineries) \u00b7 <b>2</b> Basket press (small wineries, premium; "
         "gentle but no oxygen protection) \u00b7 <b>3</b> Continuous screw press. Fast and less gentle: <b>continuous screw press</b>."), mins=4, ref="4")
ch.page()

# ============================================================ PAGE 3
_r5 = ["Minimum potential alcohol 8%", "Maximum enrichment +3%", "Acidification not permitted", "Maximum enrichment +1.5%",
       "Acidification up to +2.5 g/L allowed", "Minimum potential alcohol 9%"]
_a5 = ["Zone A", "Zone A", "Zone A", "Zone CIIIb", "Zone CIIIb", "Zone CIIIb"]
ch.ex("TICK", "EU zones: cooler or warmer?", 6,
      "Cooler zones enrich more and cannot acidify; warmer zones enrich less and may acidify. Zone A (e.g. Germany, UK) or Zone CIIIb (e.g. southern Spain).",
      tickgrid(_r5, ["Zone A", "Zone CIIIb"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a5)) + ".  Chaptalization and acidification of the same must are not both permitted."),
      mins=3, ref="5")

_bands = [(12, 16, "#9CC3D9", "12\u201316\u00b0C", "Fresh, fruity whites and ros\u00e9: esters promoted and retained"),
          (17, 25, "#E6D28A", "17\u201325\u00b0C", "Easy-drinking fruity reds; top end for barrel whites"),
          (26, 32, "#E8A44A", "26\u201332\u00b0C", "Concentrated, high-tannin reds: maximum color and tannin"),
          (35, 40, "#C8553D", "Above 35\u00b0C", "Fermentation risks slowing or sticking")]
ch.ex("SCALE", "Fermentation temperature and style", 4, "Write the typical use or effect in each dotted box.",
      BandScale(10, 40, _bands, [10, 20, 30, 40], key=False),
      kp("<b>12\u201316\u00b0C</b> fresh, fruity whites and ros\u00e9 (esters) \u00b7 <b>17\u201325\u00b0C</b> easy-drinking fruity reds; top end for barrel whites \u00b7 "
         "<b>26\u201332\u00b0C</b> concentrated, high-tannin reds (maximum color and tannin) \u00b7 <b>above 35\u00b0C</b> risk of slowing or sticking."), mins=3, ref="6")

_p7 = [("Chaptalization", "Adds dry sugar (or concentrated must) before fermentation to raise potential alcohol"),
       ("Acidification", "Adds acid, usually tartaric, when grapes are low in acidity, as in warm climates"),
       ("Deacidification", "Adds calcium or potassium carbonate: acidity falls as tartrates precipitate; allow for MLF"),
       ("Color adjustment", "Fining removes unwanted tints; grape-derived MegaPurple deepens some reds, but is banned in some regions")]
_d7 = [2, 0, 3, 1]
_l7 = [chr(65 + _d7.index(i)) for i in range(4)]
ch.ex("MATCH", "Adjusting the must or wine", 4, "Match each adjustment to what it does.",
      match([p[0] for p in _p7], [_p7[i][1] for i in _d7], _l7),
      pairs([(str(i + 1), _l7[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="5")
ch.page()

# ============================================================ PAGE 4
_rc = [["Advantages", "Complexity from multiple species; free; regionally distinctive",
        Blank("Reliable, fast fermentation to dryness; consistent; low VA", 2)],
       ["Disadvantages", Blank("Slow start risks VA and spoilage; stuck-fermentation risk; no consistency guarantee", 3),
        Blank("Cost; some argue it homogenizes fruit expression", 2)]]
ch.ex("COMPARE", "Ambient or cultured yeast?", 3, "Complete the dotted cells.",
      compare(["", "Ambient (wild)", "Cultured (selected)"], _rc, [88, 215, 215]),
      kp("<b>Cultured advantage:</b> reliable, fast, consistent, low VA. <b>Ambient disadvantage:</b> slow start risks VA and spoilage, "
         "stuck-fermentation risk. <b>Cultured disadvantage:</b> cost, possible homogenizing."), mins=3, ref="6")

_tf = [("Oxygen is always a threat in winemaking.", False,
        "It is needed at the start of fermentation, drives color stability in reds and defines oxidative styles."),
       ("Chaptalization and acidification of the same must are both permitted in the EU.", False, "They are not both permitted."),
       ("Fewer, larger SO2 additions are more effective than many small ones.", True, ""),
       ("Destemming is skipped for carbonic maceration.", True, ""),
       ("A pneumatic press is the most popular worldwide.", True, ""),
       ("A lower pH makes a given SO2 addition less protective.", False,
        "Lower pH pushes more free SO2 into the active molecular form: more protective.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20135")
ch.page()

# ============================================================ PAGE 5
_cw = cached_crossword(13)
_nw = len(_cw["clues"]["A"]) + len(_cw["clues"]["D"])
ch.ex("CROSSWORD", "Chapters 11\u201313 vocabulary", _nw, "One point per word. Answers are single words, no spaces.",
      crossword_block(_cw, key=False, cell=15.0), crossword_answers(_cw), mins=7, ref="1\u20138")

_e = ["Only molecular SO2 does the protective work.", "Lower pH pushes more of the free SO2 into the active molecular form.",
      "At high pH less of the free SO2 is active, so a bigger addition is needed for the same protection."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Name the active form first.",
      explain("Explain why a <b>high-pH must needs a larger SO2 addition</b>.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: only molecular SO2 protects \u00b7 lower pH shifts free SO2 to molecular \u00b7 high pH needs a bigger addition."), mins=4, ref="1")
ch.page()

# ============================================================ PAGE 6
_s = ["Cool-climate, high-acid Chardonnay in the style of Chablis", "An already low-acid Chardonnay", "A very pale red where color loss matters",
      "A red wine, as a matter of routine", "A wine that needs greater microbial stability before bottling"]
ch.ex("DECIDE", "Induce or block MLF?", 5, "Circle <b>I</b> to induce malolactic conversion or <b>B</b> to block it.",
      choose(_s, ["I", "B"]),
      kp("<b>1</b> I \u00b7 <b>2</b> B \u00b7 <b>3</b> B \u00b7 <b>4</b> I \u00b7 <b>5</b> I. Reds routinely undergo it; for whites it is the winemaker\u2019s choice."), mins=3, ref="7")

_mc = [("The press most popular worldwide, suited to medium and large wineries, is the:",
        ["Basket press", "Pneumatic press", "Continuous screw press", "Horizontal screw press"]),
       ("Destemming is typically skipped for:", ["Fresh, fruity whites", "Carbonic maceration and whole-bunch pressing", "All reds", "Machine-harvested fruit"]),
       ("The EU maximum SO2 for red wine is:", ["100 mg/L", "150 mg/L", "200 mg/L", "250 mg/L"]),
       ("<i>Saccharomyces cerevisiae</i> is the standard wine yeast because it:",
        ["Needs no nitrogen", "Tolerates high acidity and rising alcohol and ferments reliably to dryness", "Is killed by SO2", "Makes buttery notes"]),
       ("Fermentation above which temperature risks slowing or sticking?", ["25\u00b0C", "30\u00b0C", "35\u00b0C", "40\u00b0C"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 pneumatic"), ("2", "<b>B</b> \u2014 carbonic maceration, whole-bunch pressing"), ("3", "<b>B</b> \u2014 150 mg/L (white 200)"),
                ("4", "<b>B</b> \u2014 acid- and alcohol-tolerant, reliably dry"), ("5", "<b>C</b> \u2014 above 35\u00b0C")]), mins=4, ref="1\u20136")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch13.pdf")
