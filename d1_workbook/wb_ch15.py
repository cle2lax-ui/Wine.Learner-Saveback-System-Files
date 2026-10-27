# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 15: Finishing and Packaging."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("15", "Finishing and Packaging",
             ["name the agent or method for each problem",
              "tell depth from surface filtration",
              "list the four sources of package oxygen",
              "match each fault to its mechanism",
              "weigh bottle against bulk shipping"])

# ============================================================ PAGE 1
_p1 = [("Bentonite", "Unstable proteins that cause haze in whites and ros\u00e9"), ("Egg white", "Harsh tannins in fine reds"),
       ("Gelatin", "Astringency, and browning in whites"), ("Casein", "Browning in whites"),
       ("Isinglass", "Clarifies whites brightly"), ("PVPP", "Browning and astringency, mostly in whites"),
       ("Charcoal", "Brown color and off-odors")]
_d1 = [3, 0, 6, 1, 4, 2, 5]
_l1 = [chr(65 + _d1.index(i)) for i in range(7)]
ch.ex("MATCH", "Fining: what removes what", 7, "Name the right agent for the stated problem. Match each agent to what it removes.",
      match([p[0] for p in _p1], [_p1[i][1] for i in _d1], _l1),
      pairs([(str(i + 1), _l1[i]) for i in range(7)], ncols=7, width=COLW), mins=4, ref="1")

_r2 = ["Bentonite", "Egg white", "Gelatin", "Casein", "Isinglass", "Vegetable protein"]
_a2 = ["Suitable", "Not suitable", "Not suitable", "Not suitable", "Not suitable", "Suitable"]
ch.ex("TICK", "Vegan-suitable fining?", 6, "Dietary constraints decide the agent. Tick one for each.",
      tickgrid(_r2, ["Suitable for vegans", "Not suitable"], label_w=340),
      kp(" \u00b7 ".join("<b>%s</b> %s" % (r, a.lower()) for r, a in zip(_r2, _a2))), mins=3, ref="1")
ch.page()

# ============================================================ PAGE 2
_p3 = [("Sedimentation and racking", "Cool-cellar settling, then racking off the sediment; the number of rackings depends on container, volume and labor"),
       ("Centrifugation", "Spins wine rapidly; can replace depth filtration and allow early bottling; high-volume wineries only"),
       ("Diatomaceous earth", "Vacuum draws wine through inert silica; oxidative unless gas-flushed; disposal cost"),
       ("Sheet (pad)", "Wine passes through stacked filter sheets; needs a robust frame and trained operators"),
       ("Membrane (cartridge)", "Pores under 1 micron; the final pre-bottling step; slow; needs pre-filtering first"),
       ("Cross-flow", "Wine flows tangentially, self-cleaning; no consumables to buy, but an expensive machine")]
_d3 = [4, 0, 5, 2, 1, 3]
_l3 = [chr(65 + _d3.index(i)) for i in range(6)]
ch.ex("MATCH", "Clarifying wine", 6, "Settling and spinning, then depth filters (diatomaceous earth, sheet) and surface filters (membrane, cross-flow). Match each.",
      match([p[0] for p in _p3], [_p3[i][1] for i in _d3], _l3),
      pairs([(str(i + 1), _l3[i]) for i in range(6)], ncols=6, width=COLW), mins=4, ref="1")

_p4 = [("Cold stabilization", "Hold at \u22124\u00b0C for about 8 days, then filter out the crystals"),
       ("Contact process", "Add potassium bitartrate crystals to seed faster crystallization"),
       ("Electrodialysis", "A charged membrane removes ions; high upfront cost"),
       ("Ion exchange", "Swaps K+ and Ca2+ for H+ or Na+; banned in some territories"),
       ("CMC", "Wood-derived cellulose; white wine only"),
       ("Metatartaric acid", "Blocks crystal growth chemically; unstable over time and heat")]
_d4 = [4, 2, 0, 5, 1, 3]
_l4 = [chr(65 + _d4.index(i)) for i in range(6)]
ch.ex("MATCH", "Tartrate stabilization", 6, "Match each method to how it works or its limit.",
      match([p[0] for p in _p4], [_p4[i][1] for i in _d4], _l4),
      pairs([(str(i + 1), _l4[i]) for i in range(6)], ncols=6, width=COLW), mins=3, ref="2")

f, a = cloze(["Target free SO2 at bottling: white {{25\u201345}} mg/L, red {{30\u201355}} mg/L, sweet {{30\u201360}} mg/L. Flash pasteurization "
              "briefly heats to {{80\u201390}}\u00b0C; cold bottling uses {{sterile}} filtration. Too-high dissolved oxygen is corrected by "
              "{{sparging}}. Bottles are steam-cleaned at {{82}}\u00b0C for {{20}} minutes; bottle aging is best at {{10\u201315}}\u00b0C."], width=70)
ch.ex("COMPLETE", "Finishing numbers", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=3, ref="3, 6")
ch.page()

# ============================================================ PAGE 3
_p6 = [("Cloudiness", "Microbial growth with poor filtering, or a protein haze from bad fining"),
       ("Tartrates", "Natural crystallization: harmless, but often mistaken for glass"),
       ("Re-fermentation", "Live yeast plus residual sugar left in the wine"),
       ("Cork taint (TCA)", "A contaminated natural cork: moldy, wet-cardboard smell"),
       ("Oxidation", "Excess oxygen in winemaking or in bottle: poor closure, faulty bottling"),
       ("Volatile acidity", "Acetic acid bacteria with low SO2 and oxygen exposure"),
       ("Light strike", "UV and visible light reacting with wine compounds: \u2018dirty drains\u2019"),
       ("Brettanomyces", "A spoilage yeast, hard to eradicate once wood is infected"),
       ("Reduction", "Sulfur compounds from stressed, low-nitrogen yeast, or from near-total oxygen exclusion in closed vessels or tight closures")]
_d6 = [5, 2, 7, 0, 8, 3, 6, 1, 4]
_l6 = [chr(65 + _d6.index(i)) for i in range(9)]
ch.ex("MATCH", "Faults: the named mechanism", 9, "The exam wants the cause, not just the name. Match each fault to its cause.",
      match([p[0] for p in _p6], [_p6[i][1] for i in _d6], _l6),
      pairs([(str(i + 1), _l6[i]) for i in range(9)], ncols=9, width=COLW), mins=4, ref="4")

_arts = [A2.NeckScrewcap(100), A2.NeckCork(100), A2.NeckGlassStopper(100), A2.NeckSynthetic(100)]
ch.ex("NAME", "Name the closure", 5,
      "Name each drawing from the word bank (one name is not drawn), then answer the last question. <b>4 points for names, 1 for the last.</b>",
      [WordBank(["Glass stopper", "Natural cork", "Screwcap", "Synthetic closure", "Technical cork"], ncols=5), PanelFigure(_arts, gap=14),
       LineFill("Which two of the four carry no risk of cork taint?", w=W, h=19)],
      kp("<b>1</b> Screwcap \u00b7 <b>2</b> Natural cork \u00b7 <b>3</b> Glass stopper \u00b7 <b>4</b> Synthetic closure. No TCA risk: <b>screwcap and synthetic</b> "
         "(a glass stopper has none either; natural cork has TCA in 3\u20135% of bottles)."), mins=4, ref="5")
ch.page()

# ============================================================ PAGE 4
_neck = A2.NeckCork(100)
f, a = cloze(["Total package oxygen = {{dissolved}} oxygen in the wine + oxygen in the {{headspace}} (usually the biggest) + oxygen already "
              "in the {{closure}} + the closure\u2019s oxygen transmission rate, or {{OTR}}."], width=70)
ch.ex("LABEL", "Package oxygen", 4 + len(a),
      "Label the four parts, then complete the sum. <b>1 point per label and per blank.</b>",
      [LabelFigure(_neck, align="center")] + f,
      kp(label_key(_neck) + ".  " + ans_inline(a) + "  Choosing a low-OTR closure alone does not protect the wine if headspace and dissolved oxygen are not also controlled."),
      mins=4, ref="5")

_rc = [["Producer control", "The entire product: wine, bottle, label, packaging", Blank("Only the wine itself", 1)],
       ["Cost and carbon", "Higher: pays to ship the glass weight too", Blank("Lower: one container \u2248 32,000 bottles\u2019 worth of wine against about 12,500 filled bottles", 2)],
       ["Temperature risk", "Higher: less thermal mass, more fluctuation", Blank("Lower: a full container has much greater thermal inertia", 2)],
       ["Shelf-life clock", "Starts at origin: shorter by the time taken to sell", Blank("Starts at bottling near the final market: effectively longer", 2)],
       ["Best suited to", "Premium and super-premium wine", Blank("Inexpensive and mid-priced, long-haul, high volume", 2)]]
ch.ex("COMPARE", "Bottle or bulk?", 5, "Complete the bulk column. Bulk is a genuine trade-off, not an inferior shortcut.",
      compare(["", "Shipped in bottle", "Shipped in bulk"], _rc, [90, 214, 214]),
      kp("<b>Bulk:</b> only the wine \u00b7 lower cost and carbon \u00b7 lower temperature risk \u00b7 shelf-life clock starts near the market \u00b7 "
         "inexpensive, mid-priced, long-haul, high volume. Real cost: it moves bottling jobs away from the producer\u2019s country."), mins=4, ref="9")
ch.page()

# ============================================================ PAGE 5
ch.ex("FLOW", "The ISO certification chain", 3, "Complete the dotted boxes, from the standard down to the consumer.",
      VFlow(["ISO standard: sets internationally recognized standards", Blank("Wine company: self-audits, then commissions an external audit"),
             Blank("Certification body: conducts the external audit and issues certification"),
             Blank("Retailer: buys with that assurance; may require its own audit"),
             "Consumer: buys with assurance; the retailer looks to recover the cost"], box_h=27, gap=14, width=420),
      kp("Wine company self-audits, then commissions an external audit \u2192 certification body audits and certifies \u2192 retailer buys with assurance "
         "(and may add its own audit)."), mins=3, ref="8")

_tf = [("Sterile filtration means every particle is removed.", False,
        "Pores can exceed 1 micron; the point is removing yeast and bacteria for microbiological stability."),
       ("Bentonite is suitable for vegans.", True, ""),
       ("Ion exchange removes the tartrate itself.", False,
        "It swaps ions (K+, Ca2+ for H+ or Na+) and is banned in some territories."),
       ("Headspace is usually the biggest single contributor to package oxygen.", True, ""),
       ("Cork taint and oxidation have the same cause.", False, "TCA is contamination of the cork; oxidation is excess oxygen."),
       ("Bulk shipping is simply an inferior shortcut.", False,
        "It can cut carbon cost, steady temperature and lengthen effective shelf life, traded against producer control and origin jobs.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20139")
ch.page()

# ============================================================ PAGE 6
_mc = [("Which agent removes unstable proteins that could cause haze in white and ros\u00e9?", ["Egg white", "Bentonite", "Gelatin", "Charcoal"]),
       ("Cold stabilization holds wine at about:", ["+10\u00b0C for 2 days", "\u22124\u00b0C for about 8 days", "0\u00b0C for 1 hour", "\u221220\u00b0C for a week"]),
       ("A natural cork carries which two real problems?", ["TCA taint and inconsistent OTR", "Low cost and high OTR", "Scalping and sulfites", "Weight and fragility"]),
       ("Bulk shipping\u2019s real cost is chiefly that it:", ["Raises carbon emissions", "Moves bottling jobs and relationships away from the producer\u2019s country",
                                                              "Shortens shelf life", "Is banned in the EU"]),
       ("HACCP differs from ISO certification in that it is:", ["Audited externally", "Run by the company itself, with no external audit",
                                                                    "Only for retailers", "A consumer label"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 bentonite"), ("2", "<b>B</b> \u2014 \u22124\u00b0C for about 8 days"), ("3", "<b>A</b> \u2014 TCA taint and inconsistent OTR"),
                ("4", "<b>B</b> \u2014 jobs and relationships move"), ("5", "<b>B</b> \u2014 run by the company, no external audit")]), mins=4, ref="2\u20139")

_e = ["Total package oxygen has four sources: dissolved oxygen, headspace oxygen, oxygen in the closure, and the closure\u2019s OTR.",
      "Headspace is usually the biggest single contributor.",
      "So headspace and dissolved oxygen must also be controlled at filling; the closure is only part of the answer."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Name the four sources.",
      explain("Explain why choosing a <b>low-OTR closure alone</b> does not guarantee good protection.", [], lines=3) + [Checklist(_e)],
      kp("1 mark each: four sources of package oxygen \u00b7 headspace is usually biggest \u00b7 control headspace and dissolved oxygen at filling too."),
      mins=4, ref="5")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch15.pdf")
