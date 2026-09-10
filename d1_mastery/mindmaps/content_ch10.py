# -*- coding: utf-8 -*-
from mindmap import Node as N

CH10 = [
    N("Priorat", icon="sun", children=[
        N("Climate & soil", children=[
            N("Hot, dry, sunny; free-draining slate/quartz; irrigation needs authorisation"),
        ]),
        N("Variety", children=[
            N("Garnacha, Cari\u00f1ena \u2014 late-ripening, drought-tolerant; rootstock 140R"),
        ]),
        N("Vigour & training", children=[
            N("Naturally low vigour; bush vines shade fruit without over-shading"),
        ]),
        N("Yield & price", children=[
            N("Low density, 15-25 hl/ha, hand-harvested \u2014 never inexpensive"),
        ]),
    ]),
    N("Pauillac", icon="droplet", children=[
        N("Climate & soil", children=[
            N("Atlantic, rain year-round; free-draining, nutrient-poor soil"),
        ]),
        N("Variety", children=[
            N("Cabernet Sauvignon blended with earlier-ripening Merlot"),
        ]),
        N("Vigour & training", children=[
            N("Low vigour suits VSP; rain still demands mildew/botrytis monitoring"),
        ]),
        N("Density & yield", children=[
            N("High density ~10,000/ha; moderate yield 50-60 hl/ha"),
        ]),
    ]),
    N("Finger Lakes", icon="thermometer", children=[
        N("Climate", children=[
            N("Lake-moderated but extremely cold; black grapes planted nearest lakes"),
        ]),
        N("Variety", children=[
            N("Riesling \u2014 winter-hardy, late-budding; hilled soil protects the graft"),
        ]),
        N("Vigour & training", children=[
            N("Nutrient-rich soil + rain = high vigour; Scott-Henry splits canopy"),
        ]),
        N("Density & harvest", children=[
            N("Low density; machine harvest \u2014 labour is scarce here"),
        ]),
    ]),
    N("Central Valley", icon="scale", children=[
        N("Climate", children=[
            N("Warm, dry, sunny; irrigation supplies water, fertiliser feeds vines"),
        ]),
        N("Goal", children=[
            N("Maximise yield at minimum cost for inexpensive, high-volume wine"),
        ]),
        N("Vigour & training", children=[
            N("High vigour; cheap California sprawl shades fruit from sunburn"),
        ]),
        N("Yield & harvest", children=[
            N("Very high yield 180-200 hl/ha; machine harvest, often picked early"),
        ]),
    ]),
]

CH10_CROSSLINKS = [(0, 3, "opposite vigour, same low-density result"),
                    (1, 2, "same rainfall, opposite vigour outcome")]
