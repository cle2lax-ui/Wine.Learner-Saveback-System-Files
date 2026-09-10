# -*- coding: utf-8 -*-
from mindmap import Node as N

CH1 = [
    N("Species", icon="vine", children=[
        N("Vitis vinifera", children=[
            N("1,000+ varieties known; vast majority are V. vinifera"),
            N("Indigenous to Eurasia"),
        ]),
        N("N. American species", children=[
            N("labrusca, riparia, berlandieri, rupestris species"),
            N("Main use: rootstock for grafted vinifera"),
        ]),
    ]),
    N("Grape", icon="grapes", children=[
        N("Bunch structure", children=[
            N("Tight bunches (Pinot N.) \u2192 splitting, disease risk"),
        ]),
        N("Pulp", children=[
            N("Colourless \u2014 except teinturier varieties"),
        ]),
        N("Skin", children=[
            N("High tannin, colour, aroma precursors"),
        ]),
        N("Seeds & stem", children=[
            N("Seeds: oils, tannins; stem tannins too"),
        ]),
    ]),
    N("Canopy", icon="sprout", children=[
        N("Buds", children=[
            N("Compound bud = latent; primary\u2192secondary\u2192tertiary if damaged"),
        ]),
        N("Lateral shoots", children=[
            N("Second crop risk \u2014 later ripening, higher acid (Pinot N.)"),
        ]),
        N("Leaves", children=[
            N("Stomata: water out, CO2 in; stress \u2192 closes"),
        ]),
        N("Inflorescence", children=[
            N("Usually 1\u20133 per shoot, variety-dependent"),
        ]),
    ]),
    N("Roots", icon="root", children=[
        N("One-year wood", children=[
            N("Last season's shoots; carries buds for next season"),
        ]),
        N("Permanent wood", children=[
            N("Trunk, cordon; carbohydrate + nutrient store"),
        ]),
        N("Roots", children=[
            N("Most roots in top 50cm; produce growth hormones"),
        ]),
    ]),
    N("Propagation", icon="gear", children=[
        N("Cuttings", children=[
            N("By far most common; allows grafting onto rootstock first"),
        ]),
        N("Layering", children=[
            N("Fills gaps using neighbour's cane; new vine is own-rooted"),
        ]),
        N("Both = clones", children=[
            N("Genetically identical to parent"),
        ]),
    ]),
    N("Clones", icon="helix", children=[
        N("Clonal selection", children=[
            N("PN 115: low yield, high quality; PN 521: high yield"),
        ]),
        N("S\u00e9lection massale", children=[
            N("Cuttings from grower's own best vines; diverse but costly"),
        ]),
        N("Mutation", children=[
            N("Pinot Noir \u2192 Meunier, Blanc, Gris are mutations"),
        ]),
    ]),
    N("Breeding", icon="flask", children=[
        N("Cross", children=[
            N("Same species parents \u2014 Pinotage = Pinot Noir \u00d7 Cinsaut"),
        ]),
        N("Hybrid", children=[
            N("Different species parents; mainly rootstocks"),
        ]),
        N("Chance cross", children=[
            N("Cab Sauvignon = Sauvignon Blanc \u00d7 Cabernet Franc"),
        ]),
        N("Current aims", children=[
            N("Disease resistance (Pierce's) and climatic extremes"),
        ]),
    ]),
]
