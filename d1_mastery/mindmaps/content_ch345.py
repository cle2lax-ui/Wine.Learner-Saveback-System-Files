# -*- coding: utf-8 -*-
from mindmap import Node as N

# Chapter 3 is the largest chapter in the book -- too intricate for one map
# without either shrinking text past readability or hiding the structure.
# Split into two focused maps instead.

CH3A_HEAT_LIGHT = [
    N("Temperature", icon="thermometer", children=[
        N("Across the vine cycle", children=[
            N("Photosynthesis optimum 18\u201333\u00b0C; flowering needs 17\u00b0C+"),
            N("Below -20\u00b0C: winter freeze damage to the vine"),
        ]),
        N("Ripening", children=[
            N("Above 21\u00b0C in final month \u2192 rapid acid loss"),
        ]),
    ]),
    N("Sunlight", icon="sun", children=[
        N("Photosynthesis", children=[
            N("Limited only below one third of full sunshine"),
        ]),
        N("Phenolics", children=[
            N("Boosts anthocyanins, tannin ripening; reduces green methoxypyrazine notes"),
        ]),
    ]),
    N("Latitude", icon="map", children=[
        N("Viable band", children=[
            N("Roughly 30\u201350\u00b0 latitude each side of the Equator"),
        ]),
        N("Effect", children=[
            N("Lower latitude \u2192 more intense sun \u2192 riper, lower-acid grapes"),
        ]),
    ]),
    N("Altitude", icon="mountain", children=[
        N("Cooling effect", children=[
            N("Roughly -0.6\u00b0C per 100m of elevation gain"),
        ]),
        N("Example", children=[
            N("Salta, Argentina \u2014 vines planted to nearly 3,000m"),
        ]),
    ]),
    N("Aspect/Slopes", icon="mountain", children=[
        N("Sun-facing slopes", children=[
            N("South-facing in NH, north-facing in SH get most sun"),
        ]),
        N("Trade-off", children=[
            N("Slopes aid drainage and frost protection but raise erosion, cost"),
        ]),
    ]),
    N("Water Proximity", icon="droplet", children=[
        N("Moderates range", children=[
            N("Willamette Valley vs Margaux \u2014 same latitude, different currents"),
        ]),
        N("ENSO", children=[
            N("El Ni\u00f1o / La Ni\u00f1a swing rainfall and temperature patterns"),
        ]),
    ]),
    N("Wind & Soil", icon="wind", children=[
        N("Wind", children=[
            N("Lowers fungal disease risk but raises evapotranspiration"),
        ]),
        N("Soil colour", children=[
            N("Dark soils absorb heat and re-radiate it at night"),
        ]),
    ]),
    N("Diurnal Range", icon="clock", children=[
        N("High range", children=[
            N("Retains acidity in warm climates \u2014 Mendoza, high altitude"),
        ]),
        N("Low range", children=[
            N("Aids ripening in cool, maritime climates \u2014 Mosel"),
        ]),
    ]),
]

CH3A_CROSSLINKS = [(4, 7, "both drive the diurnal swing")]

CH3B_WATER_SOIL_CLIMATE = [
    N("Water", icon="droplet", children=[
        N("Minimum needs", children=[
            N("Roughly 500mm/yr cool climates, 750mm/yr warm climates"),
        ]),
        N("Timing matters", children=[
            N("Mild pre-v\u00e9raison water stress is actually beneficial"),
        ]),
    ]),
    N("Nutrients", icon="leaf", children=[
        N("Key nutrients", children=[
            N("Nitrogen, potassium, phosphorus, calcium, magnesium"),
        ]),
        N("Availability", children=[
            N("Driven mainly by soil pH, not just fertiliser use"),
        ]),
    ]),
    N("Soil", icon="soil", children=[
        N("Texture", children=[
            N("Clay holds water/nutrients well; sand drains freely"),
        ]),
        N("Role in quality", children=[
            N("Drainage and depth matter far more than soil chemistry"),
        ]),
    ]),
    N("Climate Models", icon="gear", children=[
        N("GDD", children=[
            N("Amerine & Winkler, 1944 \u2014 heat summation, five zones"),
        ]),
        N("Huglin Index", children=[
            N("1978; adds max temp + day length"),
        ]),
    ]),
    N("Climate Bands", icon="thermometer", children=[
        N("WSET GST bands", children=[
            N("Cool, Moderate, Warm, Hot \u2014 by growing season temperature"),
        ]),
        N("Broad types", children=[
            N("Maritime, Mediterranean, continental \u2014 by annual temperature range"),
        ]),
    ]),
    N("Weather & CC", icon="clock", children=[
        N("Vintage variation", children=[
            N("Bordeaux 2013 (cold, poor) vs 2016 (warm, strong)"),
        ]),
        N("Climate change", children=[
            N("Earlier harvests, faster ripening, rising alcohol levels"),
        ]),
    ]),
]

CH3B_CROSSLINKS = [(0, 1, "soil water availability drives nutrient uptake"),
                    (3, 4, "GDD and Huglin are what build these bands")]


CH4 = [
    N("Conventional", icon="gear", children=[
        N("Post-war model", children=[
            N("Mechanisation, agrochemicals, irrigation \u2014 became a monoculture"),
        ]),
        N("Trade-off", children=[
            N("Higher yield, lower cost, but chemical dependency"),
        ]),
    ]),
    N("Sustainable", icon="hourglass", children=[
        N("IPM", children=[
            N("Lutte raisonn\u00e9e \u2014 thresholds, monitoring, targeted spraying only"),
        ]),
        N("Standards vary", children=[
            N("LODI Rules, Sustainable Winegrowing NZ \u2014 no single global standard"),
        ]),
    ]),
    N("Organic", icon="sprout", children=[
        N("Bans synthetic inputs", children=[
            N("No synthetic fertiliser, fungicide, herbicide, or pesticide"),
        ]),
        N("Scale", children=[
            N("5.4% of world vineyards certified as of 2017"),
        ]),
    ]),
    N("Biodynamic", icon="moon", children=[
        N("Method", children=[
            N("Steiner's philosophy; farms as an organism, lunar/planetary calendar"),
        ]),
        N("Preparations", children=[
            N("500 horn manure for soil; 501 horn silica for growth"),
        ]),
    ]),
    N("Regenerative", icon="recycle", children=[
        N("Focus", children=[
            N("Soil health, mycorrhizal fungi, carbon sequestration, minimal tilling"),
        ]),
        N("Certification", children=[
            N("Regenerative Organic Alliance \u2014 soil, animal welfare, workers"),
        ]),
    ]),
    N("Precision", icon="caliper", children=[
        N("Method", children=[
            N("Remote/proximal sensors map vigour \u2192 variable-rate action"),
        ]),
        N("Limit", children=[
            N("High upfront cost limits it to large, high-value estates"),
        ]),
    ]),
]

CH4_CROSSLINKS = [(3, 2, "biodynamic = organic + cosmology layered on top"),
                   (1, 5, "precision viticulture often sits inside sustainable systems")]

CH5 = [
    N("Site Selection", icon="map", children=[
        N("Style drives the site", children=[
            N("Cool, sunny aspect for premium; warm flat land for volume"),
        ]),
        N("Legal constraints", children=[
            N("PDO rules constrain variety, yield, and permitted practices"),
        ]),
    ]),
    N("Terroir", icon="mountain", children=[
        N("Physical basis", children=[
            N("Climate, soil, aspect, and elevation together \u2014 sense of place"),
        ]),
        N("Contested idea", children=[
            N("Direct soil-to-flavour claims are scientifically disputed"),
        ]),
    ]),
    N("Soil Prep", icon="soil", children=[
        N("Site works", children=[
            N("Subsoiling for drainage; pH correction with lime before planting"),
        ]),
        N("Terracing", children=[
            N("Creates plantable flat land on steep slopes (Douro Valley)"),
        ]),
    ]),
    N("Variety Choice", icon="grapes", children=[
        N("Climatic fit", children=[
            N("Budding and ripening timing must suit the local climate"),
        ]),
        N("Commercial factors", children=[
            N("Law, market demand, and cost of farming also decide it"),
        ]),
    ]),
    N("Rootstocks", icon="root", children=[
        N("Primary reason", children=[
            N("Phylloxera resistance \u2014 the main reason vinifera is grafted"),
        ]),
        N("Also selects for", children=[
            N("Water availability, soil pH tolerance, and vigour"),
        ]),
    ]),
    N("Vine Age", icon="clock", children=[
        N("Yield curve", children=[
            N("Peak yield roughly 10\u201340 years, depending on variety"),
        ]),
        N("'Old vines' claim", children=[
            N("Unregulated term \u2014 30 years for one producer, 100 for another"),
        ]),
    ]),
]

CH5_CROSSLINKS = [(0, 1, "the site's growing environment IS terroir's physical basis"),
                   (3, 4, "variety and rootstock are chosen together")]
