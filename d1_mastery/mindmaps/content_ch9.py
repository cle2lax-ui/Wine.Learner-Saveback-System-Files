# -*- coding: utf-8 -*-
from mindmap import Node as N

CH9 = [
    N("Ripeness", icon="flask", children=[
        N("Sugar", children=[
            N("Refractometer; dry wine picked ~19-25\u00b0 Brix (\u224811-15% abv)"),
        ]),
        N("Acidity", children=[
            N("Titration (level) or pH meter (pH directly)"),
        ]),
        N("Aroma & tannin", children=[
            N("Usually judged by taste \u2014 no reliable instrument substitute yet"),
        ]),
        N("Multi-compound", children=[
            N("Spectroscopy (emerging); tasting still among the most important methods"),
        ]),
    ]),
    N("Rain Risk", icon="droplet", children=[
        N("The override", children=[
            N("Forecast rain forces pick-underripe-now-or-wait decision"),
        ]),
        N("Late rain", children=[
            N("Dilutes juice or splits skins \u2192 grey rot risk, possible crop loss"),
        ]),
    ]),
    N("Harvest by Style", icon="calendar", children=[
        N("Loire Chenin Blanc", children=[
            N("One variety, 4-6 week window \u2014 sparkling earliest, botrytis last"),
        ]),
        N("California Zinfandel", children=[
            N("Early-mid Aug for White Zin; September for red; uneven ripening"),
        ]),
        N("Residual sugar & Icewine", children=[
            N("Late harvest concentrates sugar; Icewine needs below -8\u00b0C"),
        ]),
        N("Hang time debate", children=[
            N("Critics: unbalanced high-alcohol wine; growers: scores, consumer demand"),
        ]),
    ]),
    N("Machine Harvest", icon="gear", children=[
        N("Advantages", children=[
            N("~1/3 the cost; night picking up to 15\u00b0C cooler, less spoilage"),
        ]),
        N("Disadvantages", children=[
            N("Less gentle \u2014 ruptures skins; struggles with mixed varieties, steep slopes"),
        ]),
        N("Improving quality", children=[
            N("Bow-rod shakers, optical sorting, in-machine SO2 dosing"),
        ]),
    ]),
    N("Hand Harvest", icon="grapes", children=[
        N("Advantages", children=[
            N("Bunch-by-bunch selectivity; handles steep slopes, mixed plantings"),
        ]),
        N("Disadvantages", children=[
            N("More expensive at scale; needs reliable, trained, supervised workforce"),
        ]),
        N("Default for", children=[
            N("Premium wine, small vineyards \u2014 or cheap-labour markets (South Africa)"),
        ]),
    ]),
    N("When Required", icon="mountain", children=[
        N("Whole-bunch styles", children=[
            N("Premium sparkling, carbonic maceration need intact bunches"),
        ]),
        N("Selective picking", children=[
            N("Botrytis-affected bunches only \u2014 e.g. Mosel TBA Riesling"),
        ]),
        N("Site & vine", children=[
            N("Steep/uneven sites (Douro); bush vines have no trellis to shake"),
        ]),
    ]),
]

CH9_CROSSLINKS = [(1, 2, "rain risk overrides style-driven timing too"), (3, 4, "quality gap has narrowed between them")]

CH9_INSET = dict(title="Loire Chenin Blanc, one 4-6 week window", w=280,
                  items=["Sparkling (wk 1)", "Dry/off-dry (wk 3)", "Botrytis/late (wk 5.5)"])
