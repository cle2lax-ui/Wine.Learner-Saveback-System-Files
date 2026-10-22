"""Arc 4 maps: the world's land (Natural Earth 110m, public domain) and the 30-50 degree vine belts, normalized 0-1 for atlas.

D1 3.1 (pp. 26-27): grapes for wine grow between about 30 and 50 degrees latitude on each side of the Equator; regions nearer the
Equator (Mendoza, South Africa, New South Wales) get more, and more intense, solar radiation than regions nearer the poles
(northern France, Germany). The bands are drawn CLIPPED TO LAND (atlas fills regions opaquely, so a plain rectangle would paint
over the sea). Projection: equirectangular with the standard parallel at 45 degrees, so shapes are nearly undistorted where the vineyards
are. Window: 150 W to 180 E, 72 N to 56 S (no Antarctica, no polar cap)."""
import json
import math
import os
import subprocess

from shapely.geometry import MultiPolygon, Polygon, box, shape
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, "..", "data", "geo", "ne_110m_land.geojson")
URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson"
LON0, LON1, LAT_TOP, LAT_BOT, STD = -140.0, 180.0, 72.0, -56.0, 50.0
KX = math.cos(math.radians(STD))
SPAN_X, SPAN_Y = (LON1 - LON0) * KX, LAT_TOP - LAT_BOT
ASPECT = SPAN_X / SPAN_Y


def N(lon, lat):
    return ((lon - LON0) * KX / SPAN_X, (LAT_TOP - lat) / SPAN_Y)


def _land():
    if not os.path.exists(GEO):
        subprocess.run(["curl", "-sSL", "-m", "60", "-o", GEO, URL], check=True)
    gj = json.load(open(GEO))
    g = unary_union([shape(f["geometry"]).buffer(0) for f in gj["features"]])
    return g.intersection(box(LON0, LAT_BOT, LON1, LAT_TOP))


def _parts(g):
    ps = [g] if isinstance(g, Polygon) else list(getattr(g, "geoms", []))
    ps = [p for p in ps if isinstance(p, Polygon) and p.area > 0.4]
    return sorted(ps, key=lambda p: -p.area)


def _ring(p):
    return [N(x, y) for x, y in p.exterior.coords]


def build():
    land = _land()
    parts = _parts(land)
    out = dict(land=[_ring(p) for p in parts], aspect=ASPECT)
    for key, (a, b) in dict(north=(30, 50), south=(-50, -30)).items():
        band = _parts(land.intersection(box(LON0, a, LON1, b)))
        out[key] = [_ring(p) for p in band]
    out["lines"] = {name: lat for name, lat in (("50\u00b0 N", 50), ("30\u00b0 N", 30), ("Equator", 0), ("30\u00b0 S", -30), ("50\u00b0 S", -50))}
    out["N"] = N
    # D1's own examples: lower latitudes (Mendoza, South Africa, New South Wales) and higher (northern France, Germany)
    out["cities"] = [(N(-68.85, -32.89), "Mendoza"), (N(18.86, -33.93), "South Africa"), (N(151.3, -32.75), "New South Wales"),
                     (N(5.5, 49.6), "Northern France, Germany")]
    return out


if __name__ == "__main__":
    d = build()
    print("aspect", round(d["aspect"], 3), "| land parts", len(d["land"]), "| north pieces", len(d["north"]), "| south pieces", len(d["south"]))
    for n, (xy, name) in enumerate(d["cities"]):
        print(f"  {name:26s} nx={xy[0]:.3f} ny={xy[1]:.3f}")
