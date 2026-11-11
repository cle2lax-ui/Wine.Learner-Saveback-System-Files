"""Africa's countries, simplified, for the line-drawing map on the cover (writes data/geo/africa_countries.geojson).
Source: Natural Earth 1:50m Admin 0 Countries (public domain), features with CONTINENT == "Africa". Simplified to 0.04 degrees, coordinates rounded to 3 decimals.
Usage: python3 prepare_africa_geo.py /path/to/ne_50m_admin_0_countries.geojson"""
import json
import os
import sys

from shapely.geometry import shape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "geo", "africa_countries.geojson")


def main(src):
    g = json.load(open(src))
    out = []
    for f in g["features"]:
        if f["properties"].get("CONTINENT") != "Africa":
            continue
        geom = shape(f["geometry"]).simplify(0.04, preserve_topology=True)
        polys = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
        rings = [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords] for p in polys if p.geom_type == "Polygon" and p.area > 0.002]
        if rings:
            out.append(dict(name=f["properties"]["NAME"], rings=rings))
    json.dump(dict(source="Natural Earth 1:50m Admin 0 Countries (public domain), Africa", countries=out), open(OUT, "w"), separators=(",", ":"))
    print("countries:", len(out), "| rings:", sum(len(c["rings"]) for c in out))


if __name__ == "__main__":
    main(sys.argv[1])
