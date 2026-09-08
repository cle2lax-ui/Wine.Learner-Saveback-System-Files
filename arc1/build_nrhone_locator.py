"""Build nrhone_locator.json — the France locator inset for slide 3.

Real traced geometry throughout, per the atlas standard: metropolitan
France dissolved from the departmental boundaries, and the Northern
Rhône's four departments (Rhône 69, Loire 42, Drôme 26, Ardèche 07)
dissolved as the highlighted region.

The marker dot is placed at the centroid of the actual dissolved cru
geometry from nrhone_geo.json and then verified by point-in-polygon
against the traced France outline — a marker that has not been checked
against the shape it sits on is how a locator ends up with a dot in the
sea.
"""
import json, math

from shapely.geometry import shape, Point
from shapely.ops import unary_union

DEPTS = "/home/claude/work/inao/depts.geojson"
CRUS = "/home/claude/work/nrhone_geo.json"
OUT = "/home/claude/work/nrhone_locator.json"

NR_DEPTS = {"69", "42", "26", "07"}


def biggest_ring(geom, simp):
    g = geom.simplify(simp, preserve_topology=True)
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    return max(polys, key=lambda p: p.area)


def main():
    fc = json.load(open(DEPTS))
    feats = [(f["properties"]["code"], shape(f["geometry"])) for f in fc["features"]]

    # Corsica is a separate landmass; including it in the dissolved outline
    # gives a mainland silhouette with an island welded on by the convex
    # bridge the union produces. Drop it — this is a locator, not an atlas.
    mainland = unary_union([g for c, g in feats if c not in ("2A", "2B")]).buffer(0)
    region = unary_union([g for c, g in feats if c in NR_DEPTS]).buffer(0)

    lon0, lat0, lon1, lat1 = mainland.bounds
    pad = 0.25
    lon0 -= pad; lon1 += pad; lat0 -= pad; lat1 += pad

    latm = (lat0 + lat1) / 2
    aspect = (((lon1 - lon0) * 111.320 * math.cos(math.radians(latm)))
              / ((lat1 - lat0) * 110.574))

    def N(pt):
        return (round((pt[0] - lon0) / (lon1 - lon0), 5),
                round((lat1 - pt[1]) / (lat1 - lat0), 5))

    outline = [N(p) for p in biggest_ring(mainland, 0.035).exterior.coords]
    reg = [N(p) for p in biggest_ring(region, 0.012).exterior.coords]

    # Marker: centroid of the real cru geometry, mapped back out of the
    # slide-3 normalized space into lon/lat, then into locator space.
    crus = json.load(open(CRUS))
    clon0, clat0, clon1, clat1 = crus["bounds"]
    xs, ys = [], []
    for name in crus["order"]:
        for ring in crus["regions"][name]:
            for x, y in ring:
                xs.append(clon0 + x * (clon1 - clon0))
                ys.append(clat1 - y * (clat1 - clat0))
    mlon, mlat = sum(xs) / len(xs), sum(ys) / len(ys)

    if not mainland.contains(Point(mlon, mlat)):
        raise SystemExit(f"BLOCKER — marker {mlon:.3f},{mlat:.3f} outside France outline")
    if not region.contains(Point(mlon, mlat)):
        raise SystemExit(f"BLOCKER — marker outside the highlighted departments")

    data = {
        "aspect": round(aspect, 6),
        "outline": outline,
        "region": reg,
        "marker": N((mlon, mlat)),
        "marker_lonlat": [round(mlon, 4), round(mlat, 4)],
    }
    json.dump(data, open(OUT, "w"), ensure_ascii=False)
    print(f"aspect {aspect:.4f}  outline {len(outline)} pts  region {len(reg)} pts")
    print(f"marker {mlon:.4f},{mlat:.4f} -> {data['marker']}  (in France ✓, in region ✓)")


if __name__ == "__main__":
    main()
