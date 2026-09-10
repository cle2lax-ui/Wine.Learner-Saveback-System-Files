# -*- coding: utf-8 -*-
from mindmap import Node as N

CH8 = [
    N("Weather", icon="droplet", children=[
        N("Drought", children=[
            N("Below ~500-750mm/yr; stomata close, growth impaired, vine may die"),
        ]),
        N("Excess water", children=[
            N("Growth competes with ripening; humidity raises fungal risk"),
        ]),
        N("Untimely rain", children=[
            N("At flowering: coulure/millerandage; near harvest: split grapes, grey rot"),
        ]),
    ]),
    N("Frost", icon="thermometer", children=[
        N("Types", children=[
            N("Advective (cold air mass moves in) vs radiative (still night, heat loss)"),
        ]),
        N("Threshold", children=[
            N("Below 0\u00b0C freezes buds; -20\u00b0C severe damage; -25\u00b0C vine death"),
        ]),
        N("Protection", children=[
            N("Aspersion only works on advective; wind machines need inversion layer"),
        ]),
        N("Risk reduction", children=[
            N("Site selection, delayed pruning, late-budding variety, bare soil"),
        ]),
    ]),
    N("Heat & Fire", icon="sun", children=[
        N("Sunburn", children=[
            N("Grapes transpire less than leaves, run hotter; worse under water stress"),
        ]),
        N("Fire", children=[
            N("More frequent with climate change; cover crops/mulch add fuel"),
        ]),
        N("Smoke taint", children=[
            N("Aroma compounds bind to sugars; only turn aromatic during fermentation"),
        ]),
    ]),
    N("Phylloxera", icon="root", children=[
        N("Damage", children=[
            N("Aphid-like insect feeds on roots; spread mainly by human movement"),
        ]),
        N("Timeline", children=[
            N("Stunting, yellowing by year 3; death by year 5"),
        ]),
        N("The fix", children=[
            N("Graft vinifera onto American rootstock, hybridised for lime tolerance"),
        ]),
    ]),
    N("Other Pests", icon="shield", children=[
        N("Nematodes", children=[
            N("Soil worms; some feed roots, others transmit viruses (dagger \u2192 fanleaf)"),
        ]),
        N("Grape moths & mites", children=[
            N("Wounds invite bacteria/fungi; mites thrive in dust, water stress"),
        ]),
        N("Birds & mammals", children=[
            N("Netting, scarers, falcons; fencing sunk against burrowing"),
        ]),
    ]),
    N("Mildews", icon="flask", children=[
        N("Powdery", children=[
            N("Surface, ~25\u00b0C, thrives in shade, no humidity needed; treat with sulfur"),
        ]),
        N("Downy", children=[
            N("Within tissue, needs rain + ~20\u00b0C warmth; treat with copper"),
        ]),
        N("Shared lever", children=[
            N("Open canopy \u2014 cuts shade for powdery, speeds drying for downy"),
        ]),
    ]),
    N("Other Fungal", icon="leaf", children=[
        N("Grey rot", children=[
            N("Needs entry point (rubbing, puncture); rain + humidity activate spores"),
        ]),
        N("Eutypa dieback", children=[
            N("Enters pruning wounds; kills over ~10 years if untreated"),
        ]),
        N("Phomopsis & Esca", children=[
            N("Phomopsis: canes whiten, snap. Esca: no chemical control, kills fast"),
        ]),
    ]),
    N("Vector-Borne", icon="helix", children=[
        N("The pattern", children=[
            N("No cure exists for any \u2014 management always targets the vector"),
        ]),
        N("Pierce's & Yellows", children=[
            N("Spread by sharpshooters / leafhoppers; remove habitat, insecticide"),
        ]),
        N("Fanleaf & Leafroll", children=[
            N("Spread by dagger nematode / mealybugs; remove & replant clean stock"),
        ]),
    ]),
]

CH8_CROSSLINKS = [(5, 6, "open canopy helps both"), (4, 7, "dagger nematode transmits fanleaf virus")]

CH8_INSET = dict(title="The phylloxera story \u2014 one continuous problem", w=300,
                  items=["1863: identified", "American rootstock", "Graft vinifera on it",
                         "Lime issue", "Hybridise"])
