# -*- coding: utf-8 -*-
from mindmap import Node as N

# Chapter 2 stays a cyclical wheel (it's a loop, not a category tree) but now
# uses the same keyword discipline + icon language as the radial chapters.
CH2_STAGES = [
    dict(name="1 \u00b7 Dormancy", timing="Nov\u2013Mar NH / May\u2013Sep SH", icon="calendar",
         needs="Temps below 10\u00b0C", risk="Extreme cold, unusually mild spells",
         bullets=["No leaves \u2192 no photosynthesis; vine lives on stored starch",
                  "Below -20\u00b0C: severe vine damage or death",
                  "Below -25\u00b0C kills most Vitis vinifera",
                  "Winter pruning is carried out now"]),
    dict(name="2 \u00b7 Budburst", timing="Mar\u2013Apr NH / Sep\u2013Oct SH", icon="leaf",
         needs="Air + soil temps above 10\u00b0C", risk="Frost, cold soils",
         bullets=["Continental climates \u2192 rapid, uniform budburst, even ripening",
                  "Early budding: Chardonnay, Pinot Noir, Merlot, Grenache",
                  "Late budding (less frost risk): Sauvignon Blanc, Cabernet Sauvignon, Syrah",
                  "Late winter pruning can delay budburst \u2014 frost avoidance"]),
    dict(name="3 \u00b7 Shoot & Leaf Growth", timing="Mar\u2013Jun NH / Sep\u2013Dec SH", icon="vine",
         needs="Stored carbs; warmth, N, K, P", risk="Low carb reserves, water stress",
         bullets=["Fastest growth phase between budburst and flowering",
                  "Vigour = shoot/leaf/lateral growth, set by resources and disease",
                  "Stunted growth \u2192 weak shoots, poor flowering, unripe bunches later"]),
    dict(name="4 \u00b7 Flowering & Fruit Set", timing="May\u2013Jun NH / Nov\u2013Dec SH", icon="sun",
         needs="Min. 17\u00b0C; warmth for next year's buds", risk="Rain, cloud, wind, cold",
         bullets=["Self-pollinating; typically ~30% of flowers set (range 0\u201360%)",
                  "Coulure: failed fruit set from carb imbalance (Grenache, Cab Sauv, Merlot)",
                  "Millerandage: seedless berries from cold/wet weather (Chardonnay, Merlot)",
                  "Also sets next year's bud fruitfulness \u2014 shading/cold/stress all limit it"]),
    dict(name="5 \u00b7 Grape Development", timing="Jun\u2013Sep NH / Dec\u2013Mar SH", icon="grapes",
         needs="Sunlight, warmth, mild water stress", risk="Excess water/nutrients, shading, extremes",
         bullets=["V\u00e9raison: lag phase, chlorophyll breaks down, anthocyanins form",
                  "Ripening: sugar and water rise, acid falls, tannin/colour/aroma develop",
                  "Above 21\u00b0C in final month \u2192 rapid acid loss, high pH",
                  "High diurnal range retains acidity (Central Otago, Washington State)"]),
    dict(name="6 \u00b7 Leaf Fall \u2192 Dormancy", timing="Autumn into winter", icon="root",
         needs="Cooling temperatures trigger senescence", risk="Extreme or erratic autumn weather",
         bullets=["Shoots lignify into canes; leaves fall",
                  "Reserves laid down in roots, trunk, and branches",
                  "Ripeness is sugar, acid, aroma AND tannin \u2014 not just one",
                  "Cycle then repeats: vine re-enters dormancy"]),
]

CH2_CROSSLINKS = [
    (2, 3, "carbs diverted \u2192 coulure risk"),
    (3, 4, "bud fruitfulness set now \u2192 next yr's yield"),
    (0, 5, "reserves built here fuel Stage 3"),
]
