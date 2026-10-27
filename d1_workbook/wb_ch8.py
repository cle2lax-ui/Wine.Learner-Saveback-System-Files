# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- Chapter 8: Hazards, Pests and Diseases."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb_chapter import *

ch = Chapter("8", "Hazards, Pests and Diseases",
             ["choose frost protection by frost type",
              "tell powdery from downy mildew, and sulfur from copper",
              "follow the one-problem story of phylloxera and rootstock",
              "name the vector, not the pathogen, as the target",
              "learn the pattern: cause, symptoms, management"])

# ============================================================ PAGE 1
_r1 = ["Site selection (avoid frost pockets)", "Delayed pruning", "A late-budding variety",
       "Water sprinklers (aspersion)", "Wind machines", "Heaters and candles"]
_a1 = ["Reduce", "Reduce", "Reduce", "Combat", "Combat", "Combat"]
ch.ex("TICK", "Reduce the risk or combat the threat?", 6,
      "Some protection costs nothing when frost is not coming; some costs every time it is used. Tick one for each.",
      tickgrid(_r1, ["Reduces risk", "Combats active threat"], label_w=330),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a1))), mins=3, ref="1")

_p9 = [("Drought", "Stomata close and photosynthesis falls; choose a drought-tolerant rootstock (110R, 140R) and variety (Garnacha)"),
       ("Excess water", "Too much shoot growth, a humid canopy, waterlogging; plant on a slope or free-draining soil, or drain"),
       ("Untimely rain", "Coulure or millerandage at flowering; swollen, split grapes and gray rot near harvest"),
       ("Winter freeze", "Below \u221220\u00b0C the graft and canes are at risk; hill up soil, hardy varieties, warmer sites"),
       ("Hail", "Rips shoots and leaves, and wounds invite botrytis; netting in sunny Mendoza, silver iodide rockets, insurance")]
_d9 = [3, 0, 4, 1, 2]
_l9 = [chr(65 + _d9.index(i)) for i in range(5)]
ch.ex("MATCH", "Weather hazards: effect and response", 5, "Match each hazard to its effect and management.",
      match([p[0] for p in _p9], [_p9[i][1] for i in _d9], _l9),
      pairs([(str(i + 1), _l9[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="1")
ch.page()

# ============================================================ PAGE 2
f, a = cloze(["Dormant vines are damaged below {{\u221220\u00b0C}} (\u22124\u00b0F). Frost begins at {{0\u00b0C}}; growth begins at {{10\u00b0C}}. "
              "Wind machines pull down warm air from an inversion layer about {{10 m}} up, which is {{3\u20135\u00b0C}} warmer; the fans stand "
              "{{4\u20137 m}} tall, and are judged worthwhile if damaging radiative frost is likely once every {{five}} years."], width=60)
ch.ex("COMPLETE", "Frost numbers", len(a), "<b>1 point per blank.</b>", f, kp(ans_inline(a)), mins=3, ref="1")

_ch = [("Smoke taint", ["Vineyard smoke", Blank("Aroma compounds absorbed by the grapes bind with sugars"),
                        Blank("Aroma-less precursors, aromatic only during fermentation"), "Smoke taint in the wine (can grow with age)"]),
       ("Sunburn", ["Grapes heat above leaf temperature (weaker transpiration)", Blank("Worse under water stress"),
                    Blank("Scars, browning, bitterness, rot susceptibility"), "Affected fruit is sorted out"])]
ch.ex("CHAIN", "Smoke taint and sunburn", 4, "Complete each chain with the missing links.",
      [Chain(items, label=lab, box_h=46) for lab, items in _ch],
      kp("<b>1</b> bound to sugars \u2192 aroma-less precursors turn aromatic in fermentation. <b>2</b> worse under water stress \u2192 "
         "scars, browning, bitterness, rot."), mins=3, ref="1")

_o = ["Single-species American rootstocks cannot tolerate Europe\u2019s lime-rich soils (chlorosis)",
      "1863: phylloxera is identified in Europe",
      "Hybridize the American species together to balance resistance and lime tolerance",
      "Graft European vinifera onto American rootstock instead",
      "American species resist it by sealing egg wounds, but give undesirable aromas if planted directly",
      "It destroys two-thirds of European vineyard by the century\u2019s end"]
ch.ex("ORDER", "The phylloxera story", 6,
      "One continuous problem, told as cause and correction. Number the steps 1\u20136.",
      order(_o, [5, 1, 6, 4, 3, 2]),
      kp("Top to bottom: <b>5 \u00b7 1 \u00b7 6 \u00b7 4 \u00b7 3 \u00b7 2</b>."), mins=4, ref="2")
ch.page()

# ============================================================ PAGE 3
_p6 = [("Nematodes", "Biofumigation (mustard cover crop plowed in); nematode-resistant rootstock (Ramsey, Dog Ridge)"),
       ("Grape moths", "<i>Bacillus thuringiensis</i>; pheromone \u2018sexual confusion\u2019; parasitic wasps and lacewings"),
       ("Spider mites", "Encourage predatory mites; targeted sprays, since general pesticides kill the predators too"),
       ("Birds", "Netting (justified in high-value areas); rotated scarers; falcons"),
       ("Deer, boar, rabbits", "Fencing, high enough and sunk into the soil against burrowing")]
_d6 = [3, 0, 4, 1, 2]
_l6 = [chr(65 + _d6.index(i)) for i in range(5)]
ch.ex("MATCH", "Pests and their management", 5, "Match each pest to its management.",
      match([p[0] for p in _p6], [_p6[i][1] for i in _d6], _l6),
      pairs([(str(i + 1), _l6[i]) for i in range(5)], ncols=5, width=COLW), mins=3, ref="2")

_r7 = ["Lives on the surface; dull gray patches", "A water mold living within the vine tissue", "Needs rainfall and warmth (about 20\u00b0C)",
       "Optimum about 25\u00b0C; thrives in shade; no high humidity needed", "Treated with sulfur, budburst to v\u00e9raison",
       "Treated with copper (Bordeaux mixture)", "Yellow \u2018oil spots\u2019 with white downy growth underneath"]
_a7 = ["Powdery", "Downy", "Downy", "Powdery", "Powdery", "Downy", "Downy"]
ch.ex("TICK", "Powdery or downy mildew?", 7, "The classic confusion pair. Tick one for each.",
      tickgrid(_r7, ["Powdery mildew", "Downy mildew"], label_w=340),
      kp(" \u00b7 ".join("<b>%d</b> %s" % (i + 1, a) for i, a in enumerate(_a7))), mins=3, ref="3")
ch.page()

# ============================================================ PAGE 4
_p8 = [("Gray rot", "Needs an entry point; rain and humidity activate spores; sulfur and copper are ineffective"),
       ("Eutypa dieback", "Spores enter pruning wounds; kills vines over about ten years; prune late"),
       ("Phomopsis", "Canes whiten and snap after a cool, wet spring; fungicide three weeks after budburst"),
       ("Esca", "Tiger-striped leaves; warm, dry climates; no chemical control")]
_d8 = [2, 0, 3, 1]
_l8 = [chr(65 + _d8.index(i)) for i in range(4)]
ch.ex("MATCH", "Four more fungal diseases", 4, "Match each disease to its clue.",
      match([p[0] for p in _p8], [_p8[i][1] for i in _d8], _l8),
      pairs([(str(i + 1), _l8[i]) for i in range(4)], ncols=4, width=COLW), mins=3, ref="3")

_r9 = ["Pierce\u2019s Disease", "Grapevine yellows", "Fanleaf virus", "Leafroll virus"]
_a9 = ["Sharpshooter", "Leafhopper", "Dagger nematode", "Mealybug"]
ch.ex("TICK", "Four diseases, no cures", 4,
      "None has a cure, so every real lever targets the carrier. Tick the vector for each disease.",
      tickgrid(_r9, ["Sharpshooter", "Leafhopper", "Dagger nematode", "Mealybug"], label_w=270),
      kp(" \u00b7 ".join("<b>%s</b> \u2192 %s" % (r, a) for r, a in zip(_r9, _a9))), mins=2, ref="4")
ch.ex("NAME", "Which mildew?", 2,
      "The classic confusion pair. Write <b>powdery</b> or <b>downy</b> and its treatment under each drawing. "
      "<b>1 point per drawing for the name and treatment together.</b>",
      [PanelFigure([A2.MildewPowdery(140), A2.MildewDowny(140)], gap=60)],
      kp("<b>1</b> Powdery mildew (gray-white bloom on the surface) \u2014 sulfur. <b>2</b> Downy mildew (yellow \u2018oil spots\u2019, white downy growth "
         "underneath) \u2014 copper."), mins=2, ref="3")
ch.page()

# ============================================================ PAGE 5
_tf = [("Powdery mildew needs high humidity to spread.", False, "It spreads even in dry conditions and thrives in shade."),
       ("Wind machines protect against advective frost.", False, "Only aspersion does; wind machines need an inversion layer."),
       ("Pierce\u2019s Disease can be cured with a fungicide.", False, "There is no cure; control the sharpshooter, or replant."),
       ("Netting against hail also shades the vines.", True, ""),
       ("Sandy soil gives natural immunity to phylloxera.", True, ""),
       ("Leafroll virus kills vines within a year or two.", False, "It does not kill; it cuts yield by up to half and delays ripening.")]
ch.ex("DECIDE", "True or false \u2014 then fix it", 6,
      "Circle T or F; correct any false statement. <b>1 point only if the call and the correction are both right.</b>",
      [TFItem(i + 1, t) for i, (t, v, fx) in enumerate(_tf)],
      numbered([(str(i + 1), ("<b><font color=\"%s\">T</font></b>" % hexc(ANS)) if v else
                 ("<b><font color=\"%s\">F</font></b> \u2014 %s" % (hexc(ANS), fx))) for i, (t, v, fx) in enumerate(_tf)]),
      mins=5, ref="1\u20134")

_e = ["American species resist phylloxera by sealing egg wounds with a corky layer.",
      "Planted directly they give undesirable aromas, so European vinifera is grafted on top.",
      "Single-species American rootstocks cannot tolerate Europe\u2019s calcareous soils: lime-induced chlorosis.",
      "Hybridizing the American species balanced phylloxera resistance with lime tolerance."]
ch.ex("EXPLAIN", "Write like an examiner", 3, "Tell it as cause and correction, not as two separate facts.",
      explain("Explain why grafting onto American rootstock <b>solved phylloxera but needed a second step</b>.", [], lines=3) + [Checklist(_e)],
      kp("Any 3 of 4: American species resist \u00b7 grafted for the fruit \u00b7 lime intolerance (chlorosis) \u00b7 hybridized to balance both."),
      mins=4, ref="2")
ch.page()

# ============================================================ PAGE 6
ch.ex("NAME", "Name the frost protection", 3,
      "Name each drawing from the word bank (one name is not drawn).",
      [WordBank(["Aspersion", "Heaters", "Helicopter", "Wind machine"], ncols=4),
       PanelFigure([A2.FrostHeaters(140), A2.FrostWindMachine(140), A2.FrostSprinklers(140)], gap=14)],
      kp("<b>1</b> Heaters (high fuel and labor cost, low efficiency, pollution) \u00b7 <b>2</b> Wind machine (pulls down warm inversion air; "
         "radiative frost) \u00b7 <b>3</b> Aspersion (the only method against advective frost)."), mins=3, ref="1")

_mc = [("The only method effective against advective frost is:", ["Wind machines", "Aspersion", "Heaters", "Helicopters"]),
       ("The Bordeaux mixture is:", ["Sulfur and lime, against powdery mildew", "Copper sulfate and lime, against downy mildew",
                                      "A systemic fungicide for gray rot", "A pheromone for moths"]),
       ("Which pest transmits fanleaf virus?", ["Mealybug", "Dagger nematode", "Sharpshooter", "Leafhopper"]),
       ("Gray rot most threatens:", ["Thick-skinned, small-grape varieties", "Tight-bunch, thin-skinned varieties such as Semillon",
                                       "Vines on sandy soil", "Very young vines only"]),
       ("Smoke-taint compounds become aromatic:", ["Instantly in the vineyard", "During fermentation", "Only in barrel", "Never"])]
ch.ex("CHOOSE", "Multiple choice", 5, "Circle one answer. The live D1 paper is written \u2014 use these to find gaps.",
      [MCQ(i + 1, q, o) for i, (q, o) in enumerate(_mc)],
      numbered([("1", "<b>B</b> \u2014 aspersion"), ("2", "<b>B</b> \u2014 copper sulfate and lime, against downy mildew"),
                ("3", "<b>B</b> \u2014 the dagger nematode"), ("4", "<b>B</b> \u2014 tight bunches, thin skins"),
                ("5", "<b>B</b> \u2014 during fermentation")]), mins=4, ref="1\u20134")

if __name__ == "__main__":
    ch.build(sys.argv[1] if len(sys.argv) > 1 else "/tmp/wb_ch8.pdf")
