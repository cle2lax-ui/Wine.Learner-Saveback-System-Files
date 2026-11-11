"""Prepare the Wine of Origin polygons and the coastline for the South Africa maps (writes data/geo/za_wo_winelands.geojson and ne_10m_sa_clip.geojson).

SOURCES (both recorded in data/geo/WO_SOURCE.md)
  Wine of Origin boundaries: the repository "Tolar-dio/wine-world" (Vitis Mundi), file docs/data/geo/za.geojson, which republishes the VinPro/SAWIS Wine of
    Origin layer (every feature is marked boundary quality "official"). It holds 32 districts and 102 wards, matching Wines of South Africa's own count
    ("32 districts and some 102 wards"), and was checked against the official SAWIS production-areas list (October 2023): 79 of 80 coastal, south coast and
    Breede district and ward names present, the other a spelling variant (Paardeberg/Perdeberg). LICENSE: the repository states that the VinPro/SAWIS layer
    has NO STATED LICENSE ("check before wide public promotion"). The boundaries are the public, statutory demarcations; this is used for a non-commercial
    educational carousel, credited to the Wine and Spirit Board / SAWIS, and Steve is told of the caveat.
  Coastline: Natural Earth 10 m land (public domain).
Usage: python3 prepare_wo_geo.py /path/to/za.geojson /path/to/ne_10m_land.geojson
"""
import json
import os
import sys

from shapely.geometry import box, mapping, shape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "geo")
BB = box(17.0, -35.1, 23.8, -31.2)          # the Western Cape winelands window

# the official region of each district (SAWIS production areas, October 2023); districts not listed here have no region
REGION = {}
for reg, ds in {"Coastal Region": ["Cape Town", "Darling", "Franschhoek", "Paarl", "Stellenbosch", "Swartland", "Tulbagh", "Wellington"],
                "Cape South Coast": ["Cape Agulhas", "Elgin", "Lower Duivenhoks River", "Overberg", "Plettenberg Bay", "Swellendam", "Walker Bay", "Still Bay"],
                "Breede River Valley": ["Breedekloof", "Robertson", "Worcester"],
                "Olifants River": ["Citrusdal Mountain", "Citrusdal Valley", "Lutzville Valley"],
                "Klein Karoo": ["Calitzdorp", "Langeberg-Garcia"]}.items():
    for d_ in ds:
        REGION[d_] = reg


def rnd(coords):
    return [[round(x, 4), round(y, 4)] for x, y in coords]


def main(za, ne):
    g = json.load(open(za))
    names = {f["properties"]["id"]: f["properties"]["name"] for f in g["features"]}
    out = []
    for f in g["features"]:
        p = f["properties"]
        if p.get("subcat") not in ("District", "Ward", "Region", "Overarching region", "Subregion"):
            continue
        geom = shape(f["geometry"])
        if not geom.intersects(BB):
            continue
        geom = geom.intersection(BB).simplify(0.0004, preserve_topology=True)
        if geom.is_empty:
            continue
        polys = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
        rings = [[rnd(pl.exterior.coords)] + [rnd(h.coords) for h in pl.interiors] for pl in polys if pl.geom_type == "Polygon" and pl.area > 1e-7]
        if not rings:
            continue
        parent = names.get(p.get("parent"))
        dist = p["name"] if p["subcat"] == "District" else (parent if parent in REGION else parent)
        out.append(dict(name=p["name"], level=p["subcat"], parent=parent, region=REGION.get(p["name"]) if p["subcat"] == "District" else REGION.get(parent), polys=rings))
    json.dump(dict(source="Wine of Origin boundaries: Wine and Spirit Board / SAWIS (VinPro layer), via Tolar-dio/wine-world; no stated license", features=out),
              open(os.path.join(OUT, "za_wo_winelands.geojson"), "w"), separators=(",", ":"))
    print("wine-of-origin features:", len(out), "| districts", sum(1 for o in out if o["level"] == "District"), "| wards", sum(1 for o in out if o["level"] == "Ward"))
    land = json.load(open(ne))
    lb = box(16.0, -35.6, 24.5, -30.5)
    rings = []
    for f in land["features"]:
        geom = shape(f["geometry"]).intersection(lb).simplify(0.0008)
        for pl in (geom.geoms if hasattr(geom, "geoms") else [geom]):
            if pl.geom_type == "Polygon" and pl.area > 1e-5:
                rings.append(rnd(pl.exterior.coords))
    json.dump(dict(source="Natural Earth 10 m land (public domain), clipped", rings=rings), open(os.path.join(OUT, "ne_10m_sa_clip.geojson"), "w"), separators=(",", ":"))
    print("coastline rings:", len(rings))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
