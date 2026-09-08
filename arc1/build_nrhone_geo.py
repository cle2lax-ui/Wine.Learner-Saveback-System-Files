"""Build nrhone_geo.json — normalized map geometry for the Northern Rhône
Field Guide slide 3.

Source: INAO Délimitation Parcellaire des AOC Viticoles, as mirrored in
lm-wr/carte-aoc (tippecanoe vector tiles, z13, layer `aocexport`, attribute
`denom`). Real cadastral-parcel delimitation, dissolved per appellation with
Shapely — no schematic silhouettes, nothing traced from published cartography.

River: Natural Earth 10m river centerlines, Rhône feature, clipped to the
map window.

Output coordinate space: normalized 0-1 within the map bounding box, y
flipped (north at top), with `aspect` corrected for longitude convergence
at ~45.2°N so the map does not stretch.
"""
import json, math, os, collections

import mapbox_vector_tile
from shapely.geometry import shape, box, LineString, MultiLineString
from shapely.affinity import affine_transform
from shapely.ops import unary_union

TILES = "/home/claude/work/inao/carte-aoc-main/aoc-tiles/13"
RIVERS = "/home/claude/work/inao/rivers.geojson"
OUT = "/home/claude/work/nrhone_geo.json"

Z, EXTENT = 13, 4096

# INAO official denominations -> house label. The right-hand names are what
# the deck says; the left-hand ones are what the parcellaire calls them, and
# three of them are not what anyone actually writes on a label.
DENOM = {
    "Côte Rôtie": "Côte-Rôtie",
    "Condrieu": "Condrieu",
    "Château-Grillet": "Château-Grillet",
    "Saint-Joseph": "Saint-Joseph",
    "Crozes-Hermitage ou Crozes-Ermitage": "Crozes-Hermitage",
    "Hermitage ou Ermitage ou l'Hermitage ou l'Ermitage": "Hermitage",
    "Cornas": "Cornas",
    "Saint-Péray": "Saint-Péray",
}

ORDER = ["Côte-Rôtie", "Condrieu", "Château-Grillet", "Saint-Joseph",
         "Crozes-Hermitage", "Hermitage", "Cornas", "Saint-Péray"]

# Painter's order. These appellations genuinely overlap on the ground —
# the same delimited slopes carry Saint-Joseph for red and Condrieu for
# white, and Hermitage sits inside Crozes-Hermitage's envelope. Drawn in
# north-south order the later, larger reds bury the exact three shapes the
# slide exists to show. So: broad reds first, Hermitage over Crozes, and
# the three whites last and on top.
DRAW = ["Saint-Joseph", "Crozes-Hermitage", "Côte-Rôtie", "Cornas",
        "Hermitage", "Saint-Péray", "Condrieu", "Château-Grillet"]

# Anchor towns, real coordinates.
TOWNS = {
    "Vienne": (4.8742, 45.5254),
    "Ampuis": (4.8103, 45.4906),
    "Tain-l'Hermitage": (4.8556, 45.0700),
    "Tournon-sur-Rhône": (4.8331, 45.0669),
    "Valence": (4.8920, 44.9333),
}


def tile_bounds(x, y, z):
    n = 2 ** z
    lon0 = x / n * 360 - 180
    lon1 = (x + 1) / n * 360 - 180
    lat0 = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    lat1 = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / n))))
    return lon0, lat1, lon1, lat0


def collect():
    parts = collections.defaultdict(list)
    for x in range(4194, 4216):
        for y in range(2912, 2968):
            p = f"{TILES}/{x}/{y}.pbf"
            if not os.path.exists(p):
                continue
            data = mapbox_vector_tile.decode(open(p, "rb").read())
            lon0, lat0, lon1, lat1 = tile_bounds(x, y, Z)
            sx = (lon1 - lon0) / EXTENT
            sy = (lat1 - lat0) / EXTENT
            for layer in data.values():
                for f in layer["features"]:
                    name = DENOM.get(f["properties"].get("denom", ""))
                    if not name:
                        continue
                    g = shape(f["geometry"])
                    if g.is_empty:
                        continue
                    parts[name].append(
                        affine_transform(g.buffer(0), [sx, 0, 0, sy, lon0, lat0]))
    return {k: unary_union(v).buffer(0) for k, v in parts.items()}


def rings(geom, simp, close=0.0022, min_area=None):
    """Generalize a parcel-level appellation into readable map blobs.

    The parcellaire is cadastral: Saint-Joseph alone comes out of the tiles
    as 756 separate exterior rings, most of them a single field. Drawn at
    the ~470px panel width this slide gets, that is not a map, it is noise —
    and every ring is also a Chaikin smoothing pass, so it is slow noise.

    Two operations, in order:

    1. Close-and-open buffer (+close, -close) merges parcels that are
       neighbours on the ground into one shape. This is generalization for
       legibility, the same thing tippecanoe does at low zoom; it does NOT
       invent land, but it does mean the drawn outline is a simplification
       of the delimitation rather than the delimitation itself. Say so in
       the caption.
    2. Drop rings below `min_area`. An outlier parcel two valleys away
       from the rest of its appellation is true and unreadable; keeping it
       costs a speck of ink and buys nothing at this size.

    Interior rings are dropped for the same reason — a hole inside
    Saint-Joseph is a few pixels across and reads as a printing defect.
    """
    g = geom.buffer(close).buffer(-close * 0.72)
    g = g.simplify(simp, preserve_topology=True)
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    polys.sort(key=lambda p: p.area, reverse=True)
    if min_area:
        keep = [p for p in polys if p.area >= min_area] or polys[:1]
    else:
        keep = polys
    return [list(p.exterior.coords) for p in keep]


def main():
    aocs = collect()
    missing = [n for n in ORDER if n not in aocs or aocs[n].is_empty]
    if missing:
        raise SystemExit(f"BLOCKER — absent from parcellaire: {missing}")

    all_geom = unary_union(list(aocs.values()))
    lon0, lat0, lon1, lat1 = all_geom.bounds

    # Padding: room for the river to run past the northern and southern
    # ends, and for Vienne/Valence, neither of which is inside a cru.
    padx, pady = 0.050, 0.030
    lon0 -= padx; lon1 += padx; lat0 -= pady; lat1 += pady

    latm = (lat0 + lat1) / 2
    kx = 111.320 * math.cos(math.radians(latm))
    ky = 110.574
    aspect = ((lon1 - lon0) * kx) / ((lat1 - lat0) * ky)

    def N(pt):
        return (round((pt[0] - lon0) / (lon1 - lon0), 5),
                round((lat1 - pt[1]) / (lat1 - lat0), 5))

    # Simplification tolerance in degrees. Tight enough that Hermitage's
    # 145 ha still reads as a distinct block against Crozes around it,
    # loose enough that Saint-Joseph's 75 parcel groups don't turn the
    # ribbon into noise at 700px wide.
    SIMP = 0.00045
    # Minimum drawn ring, in square degrees (~roughly 25 ha at this
    # latitude). Château-Grillet is 3.5 ha and must survive, so it is
    # exempt — it is the whole point of that part of the map.
    MIN_A = 0.0000030
    EXEMPT = {"Château-Grillet", "Hermitage"}

    regions, anchors, areas = {}, {}, {}
    for name in ORDER:
        g = aocs[name]
        regions[name] = [[N(p) for p in r] for r in
                         rings(g, SIMP, min_area=None if name in EXEMPT else MIN_A)]
        # Anchor on the representative point of the largest part — the
        # centroid of a multipart ribbon like Saint-Joseph lands in the
        # river.
        polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
        big = max(polys, key=lambda p: p.area)
        anchors[name] = N((big.representative_point().x,
                           big.representative_point().y))
        latc = g.centroid.y
        areas[name] = round(
            g.area * (111320 * math.cos(math.radians(latc))) * 110540 / 10000, 1)

    win = box(lon0, lat0, lon1, lat1)
    riv = json.load(open(RIVERS))
    rhone = [f for f in riv["features"]
             if (f["properties"].get("name") or "") == "Rhône"][0]
    rg = shape(rhone["geometry"]).intersection(win)
    segs = []
    if not rg.is_empty:
        lines = [rg] if rg.geom_type == "LineString" else list(rg.geoms)
        for ln in lines:
            ln = ln.simplify(0.0015, preserve_topology=True)
            if ln.length > 0.01:
                segs.append([N(p) for p in ln.coords])

    data = {
        "aspect": round(aspect, 6),
        "bounds": [lon0, lat0, lon1, lat1],
        "order": ORDER,
        "draw": DRAW,
        "regions": regions,
        "anchors": anchors,
        "ha_delimited": areas,
        "rivers": {"Rhône": segs},
        "towns": {k: N(v) for k, v in TOWNS.items()},
        "source": ("after INAO parcellaire data (Licence Ouverte); river after "
                   "Natural Earth"),
    }
    json.dump(data, open(OUT, "w"), ensure_ascii=False)

    print(f"aspect {aspect:.4f}  bbox {lon0:.4f},{lat0:.4f} -> {lon1:.4f},{lat1:.4f}")
    print(f"N-S span {(lat1 - lat0) * ky:.1f} km   E-W {(lon1 - lon0) * kx:.1f} km")
    print(f"river segments: {len(segs)}")
    for n in ORDER:
        print(f"  {n:<18} {len(regions[n]):>3} rings  {areas[n]:>8,.0f} ha delimited")


if __name__ == "__main__":
    main()
