# -*- coding: utf-8 -*-
from mindmap import Node as N

CH7 = [
    N("Aims", icon="leaf", children=[
        N("Light & uniformity", children=[
            N("Maximise light interception; reduce shade; uniform ripening"),
        ]),
        N("Balance & practicality", children=[
            N("Balance vegetative/reproductive growth; ease mechanisation; airflow cuts disease"),
        ]),
    ]),
    N("Sunlight Exposure", icon="sun", children=[
        N("Increases", children=[
            N("Sugar, tannin polymerisation, anthocyanins, aroma terpenes"),
        ]),
        N("Decreases", children=[
            N("Malic acid (warmer grapes respire it); methoxypyrazines (herbaceous)"),
        ]),
        N("Limits", children=[
            N("Too much \u2192 sunburn; dense shade \u2192 slow drying, disease"),
        ]),
        N("Next year's yield", children=[
            N("Raises bud fruitfulness \u2014 light signals fruit over vegetation"),
        ]),
    ]),
    N("Vine Balance", icon="recycle", children=[
        N("Definition", children=[
            N("Match yield to vigour; varies by resources, material, disease, age"),
        ]),
        N("Balanced cycle", children=[
            N("Post-v\u00e9raison: less shoot growth \u2192 light \u2192 quality + fruitfulness"),
        ]),
        N("Under-cropping", children=[
            N("Shoots grow unchecked \u2192 dense canopy \u2192 low fruitfulness, self-perpetuating"),
        ]),
        N("Over-cropping", children=[
            N("Draws down trunk/root carbohydrate reserves; weakens future vines"),
        ]),
    ]),
    N("Yield", icon="scale", children=[
        N("Units", children=[
            N("kg/vine or kg/ha, tons/acre"),
        ]),
        N("Area yield", children=[
            N("= per-vine yield \u00d7 density; dense planting can offset low per-vine yield"),
        ]),
        N("Regulation", children=[
            N("EU legislation typically caps yield per area"),
        ]),
    ]),
    N("Vine Density", icon="map", children=[
        N("Density range", children=[
            N("Hundreds to 10,000+ vines/ha, set by vigour and trellis"),
        ]),
        N("Low vigour + VSP", children=[
            N("Plant densely, no gaps \u2014 e.g. Grand Cru Burgundy"),
        ]),
        N("Row spacing", children=[
            N("Avoid shading the next row; fit machinery; wide = cheaper"),
        ]),
        N("Row orientation", children=[
            N("North-south most even; 90\u00b0 to wind; steep slopes up-down"),
        ]),
    ]),
    N("Trellising", icon="gear", children=[
        N("Training", children=[
            N("Head (little wood) vs Cordon (permanent arms)"),
        ]),
        N("Winter pruning", children=[
            N("Spur (2-3 buds) vs cane/Guyot \u2014 paired with VSP"),
        ]),
        N("Trellis systems", children=[
            N("Bush / VSP / complex (GDC, Lyre, Scott-Henry) by vigour"),
        ]),
        N("Three factors", children=[
            N("Vigour, topography, mechanisation need"),
        ]),
    ]),
    N("Summer Pruning", icon="calendar", children=[
        N("Purpose", children=[
            N("Yearly corrections \u2014 ripening, disease pressure, easier management"),
        ]),
        N("Mechanisation", children=[
            N("All but disbudding and pinching can be mechanised"),
        ]),
    ]),
]

CH7_CROSSLINKS = [(1, 2, "bud fruitfulness links both"), (4, 5, "vigour + trellis set spacing together")]

CH7_INSET = dict(title="The season in seven corrections", w=290,
                  items=["Disbudding", "Shoot removal", "Shoot positioning", "Pinching",
                         "Shoot trimming", "Leaf removal", "Crop thinning"])
