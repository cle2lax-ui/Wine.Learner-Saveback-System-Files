# -*- coding: utf-8 -*-
from mindmap import Node as N

CH6 = [
    N("Soil Health", icon="soil", children=[
        N("Four factors", children=[
            N("Structure, organic matter/humus, living organisms, available nutrients"),
        ]),
        N("Testing", children=[
            N("Tested at establishment, then annually; correct as needed"),
        ]),
    ]),
    N("Fertilisers", icon="flask", children=[
        N("Organic", children=[
            N("Manure, green manure; needs breakdown; improves structure, cheap but bulky"),
        ]),
        N("Mineral", children=[
            N("Inorganic, immediate, precisely tailored; no soil benefit, costly"),
        ]),
        N("Risk", children=[
            N("Excess fertiliser risks excess vigour, unbalanced vine"),
        ]),
    ]),
    N("Weed Control", icon="leaf", children=[
        N("Why remove weeds", children=[
            N("Nutrient/water competition; bare moist soil cuts frost risk"),
        ]),
        N("Raises vigour", children=[
            N("Cultivation, herbicides, mulching \u2014 remove competition"),
        ]),
        N("Lowers vigour", children=[
            N("Cover crops add competition; grazing depends on intensity"),
        ]),
        N("Herbicide types", children=[
            N("Pre-emergence, contact, or systemic (whole-plant, via sap)"),
        ]),
    ]),
    N("Irrigation Systems", icon="droplet", children=[
        N("Drip", children=[
            N("Most common; economical, controllable, fertigation; no frost protection"),
        ]),
        N("Flood & channel", children=[
            N("Cheap but inefficient; needs flat land, abundant water"),
        ]),
        N("Overhead sprinkler", children=[
            N("Expensive, uses more water \u2014 but doubles as frost protection"),
        ]),
    ]),
    N("Water Quality", icon="scale", children=[
        N("Dissolved solids", children=[
            N("Mud blocks drip/sprinkler systems \u2014 needs settling, filtering"),
        ]),
        N("Salinity", children=[
            N("Impedes root uptake; worse under drip \u2014 salt accumulates at roots"),
        ]),
        N("Efficiency measures", children=[
            N("RDI, drought-tolerant varieties/rootstocks, mulch, weed removal"),
        ]),
    ]),
    N("RDI", icon="clock", children=[
        N("The window", children=[
            N("Fruit set to v\u00e9raison \u2014 precisely timed, not just less water"),
        ]),
        N("The result", children=[
            N("Smaller berries, higher skin-to-juice ratio, more anthocyanins/tannins"),
        ]),
        N("The trade-off", children=[
            N("Usually lowers yield; prolonged stress cuts yield and quality"),
        ]),
    ]),
    N("Drainage", icon="gear", children=[
        N("Timing", children=[
            N("Only practical before planting; retrofitting is very hard"),
        ]),
        N("Benefit", children=[
            N("Healthier vines, firmer surface for machinery"),
        ]),
    ]),
]

CH6_CROSSLINKS = [(1, 2, "cover crops double as green manure"),
                   (4, 5, "RDI is delivered via a dripper system too")]

CH6_INSET = dict(kind="spectrum", title="Weed control methods, by effect on vigour", w=300,
                  items=["Cover crops", "Grazing", "Mulching", "Cultivation", "Herbicides"])
