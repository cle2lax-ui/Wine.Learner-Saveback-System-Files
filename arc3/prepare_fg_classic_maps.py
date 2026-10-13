"""Map data for The Field Guide: Mendocino (classic carousel deck). Every shape is real data; nothing is hand-drawn.

SOURCES
  AVA boundaries: UC Davis AVA Project (CC0), data/geo/mendocino_avas.geojson (built by prepare_mendocino_geo.py).
  County outlines: US Census cartographic boundaries (public domain), data/geo/mendocino_counties.geojson.
  California outline: dissolved from its 58 counties, data/geo/california.geojson.
  Rivers: Natural Earth (public domain), data/geo/ne_rivers_na.geojson (the Russian and the Eel; the Navarro is not in
    Natural Earth, so it is NAMED on the slides, never drawn).
  Towns: Boonville and Philo, coordinates from their published GNIS/Wikipedia positions -- each is VERIFIED to fall
    inside the Anderson Valley AVA polygon (point-in-polygon), or the build fails.
CONVENTIONS (as arc2/prepare_map_data.build_anbaugebiete_map): longitude scaled by cos(latitude); y runs down; every
  coordinate normalized to the map's own box; `aspect` = width / height.
"""
import json
import math
import os

from shapely.geometry import Point, box, shape
from shapely.ops import nearest_points, unary_union

GEO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "geo")
LAT0 = 39.3
K = math.cos(math.radians(LAT0))
MI_PER_DEG_LAT = 69.0
TOWNS = {"Boonville": (-123.3661, 39.0093), "Philo": (-123.4447, 39.0657)}
DISPLAY = {"Eagle Peak Mendocino County": "Eagle Peak", "Pine Mountain-Cloverdale Peak": "Pine Mtn\u2013Cloverdale Pk"}


def _load():
    avas = {f["properties"]["name"]: shape(f["geometry"]).buffer(0)
            for f in json.load(open(f"{GEO}/mendocino_avas.geojson"))["features"]}
    counties = {f["properties"]["name"]: shape(f["geometry"]).buffer(0)
                for f in json.load(open(f"{GEO}/mendocino_counties.geojson"))["features"]}
    state = shape(json.load(open(f"{GEO}/california.geojson"))["features"][0]["geometry"]).buffer(0)
    rivers = [f for f in json.load(open(f"{GEO}/ne_rivers_na.geojson"))["features"]
              if f["properties"].get("name") in ("Russian", "Eel")]
    return avas, counties, state, rivers


def _polys(g):
    return list(g.geoms) if g.geom_type == "MultiPolygon" else [g] if g.geom_type == "Polygon" else \
        [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]


def _lines(g):
    if g.is_empty:
        return []
    if g.geom_type == "LineString":
        return [g]
    return [l for l in getattr(g, "geoms", []) if l.geom_type == "LineString"]


def coast_distance_miles():
    """Shortest distance from the Anderson Valley AVA to open ocean (outside every county polygon), in miles."""
    avas, counties, _, _ = _load()
    av = avas["Anderson Valley"]
    x0, y0, x1, y1 = av.bounds
    land = unary_union(list(counties.values()))
    sea = box(x0 - 1.0, y0 - 1.0, x1 + 1.0, y1 + 1.0).difference(land)
    a, b = nearest_points(av, sea)
    return math.hypot((a.x - b.x) * K, a.y - b.y) * MI_PER_DEG_LAT


def check_towns():
    avas, _, _, _ = _load()
    for name, (lon, lat) in TOWNS.items():
        if not avas["Anderson Valley"].contains(Point(lon, lat)):
            raise ValueError(f"{name} does not fall inside the Anderson Valley AVA: its coordinates are wrong")
    return True


def build_ava_map():
    """The county's AVAs as real shapes for region_map (M20). The Mendocino AVA (which covers six of these) and the
    North Coast AVA are left off: on a flat-filled map a parent AVA only blurs its children's edges. Pine Mountain-
    Cloverdale Peak is clipped to the county (the Mendocino part). Mendocino Ridge's many islands become many entries
    under one name, so it labels and highlights as one AVA."""
    avas, counties, _, rivers = _load()
    county = max(_polys(counties["Mendocino"]), key=lambda p: p.area)
    minx, miny, maxx, maxy = county.bounds
    aspect = (maxx - minx) * math.cos(math.radians((miny + maxy) / 2)) / (maxy - miny)

    def project(lon, lat):
        return ((lon - minx) / (maxx - minx), 1 - (lat - miny) / (maxy - miny))

    outline = [project(x, y) for x, y in county.simplify(0.002).exterior.coords]
    regions, targets = [], {}
    for raw, g in avas.items():
        if raw in ("North Coast", "Mendocino"):
            continue
        name = DISPLAY.get(raw, raw)
        g = g.intersection(county)
        parts = [p for p in _polys(g) if p.area > 1e-6]
        for p in parts:
            regions.append((name, [project(x, y) for x, y in p.simplify(0.0008).exterior.coords]))
        biggest = max(parts, key=lambda p: p.area)
        rp = biggest.representative_point()
        targets[name] = project(rp.x, rp.y)
    riv = {}
    for f in rivers:
        clipped = shape(f["geometry"]).intersection(county)
        for ln in _lines(clipped):
            riv.setdefault(f["properties"]["name"] + " River", []).append([project(x, y) for x, y in ln.coords])
    return dict(aspect=aspect, outline=outline, islands=[], regions=regions, targets=targets, rivers=riv)


def build_av_zoom(box_w, box_h, pad=0.12):
    """Anderson Valley and its neighbors for atlas (M09), in a geographic window cut to the atlas box's exact aspect so
    the real shapes are not distorted. Returns the land outline(s), the AVA polygons, town points, the Pacific's label
    position, the measured coast-distance segment and a function mapping (lon, lat) into the box."""
    avas, counties, _, _ = _load()
    av = avas["Anderson Valley"]
    x0, y0, x1, y1 = av.bounds
    x0 -= pad * 2.2; x1 += pad * 0.6; y0 -= pad; y1 += pad * 0.7     # room for the coast to the west
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    want = box_w / box_h
    w_proj, h_deg = (x1 - x0) * K, (y1 - y0)
    if w_proj / h_deg < want:
        w_proj = h_deg * want
    else:
        h_deg = w_proj / want
    gx0, gx1 = cx - w_proj / K / 2, cx + w_proj / K / 2
    gy0, gy1 = cy - h_deg / 2, cy + h_deg / 2
    win = box(gx0, gy0, gx1, gy1)

    def N(lon, lat):
        return ((lon - gx0) / (gx1 - gx0), 1 - (lat - gy0) / (gy1 - gy0))

    land = unary_union(list(counties.values())).intersection(win)
    land_rings = [[N(x, y) for x, y in p.simplify(0.001).exterior.coords] for p in _polys(land) if p.area > 1e-5]
    land_rings.sort(key=lambda r: -len(r))
    ava_rings = {}
    for raw in ("Mendocino", "Comptche", "Yorkville Highlands", "Mendocino Ridge", "Anderson Valley"):
        g = avas[raw].intersection(win)
        ava_rings[raw] = [[N(x, y) for x, y in p.simplify(0.0006).exterior.coords] for p in _polys(g) if p.area > 2e-6]
    targets = {raw: N(*avas[raw].intersection(win).representative_point().coords[0]) for raw in ava_rings
               if not avas[raw].intersection(win).is_empty}
    sea = win.difference(unary_union(list(counties.values())))
    a, b = nearest_points(av, sea)
    seg = (N(a.x, a.y), N(b.x, b.y))
    towns = {n: N(*ll) for n, ll in TOWNS.items()}
    sea_pt = sea.representative_point()
    return dict(land=land_rings, avas=ava_rings, targets=targets, towns=towns, coast_seg=seg,
                sea_label=N(sea_pt.x, sea_pt.y), window=(gx0, gy0, gx1, gy1), N=N)


def build_ca_inset(iw=340, ih=300):
    """California, normalized to the atlas inset box (340 x 300 px) with ONE uniform scale, and the valley's marker."""
    avas, _, state, _ = _load()
    st = max(_polys(state), key=lambda p: p.area)
    minx, miny, maxx, maxy = st.bounds
    sx = iw / ((maxx - minx) * K)
    sy = ih / (maxy - miny)
    s = min(sx, sy) * 0.94
    ox = (iw - (maxx - minx) * K * s) / 2
    oy = (ih - (maxy - miny) * s) / 2

    def I(lon, lat):
        return ((ox + (lon - minx) * K * s) / iw, (oy + (maxy - lat) * s) / ih)

    outline = [I(x, y) for x, y in st.simplify(0.02).exterior.coords]
    c = avas["Anderson Valley"].centroid
    return dict(outline=outline, marker=I(c.x, c.y))


if __name__ == "__main__":
    check_towns()
    print("towns verified inside the Anderson Valley AVA:", ", ".join(TOWNS))
    print(f"Anderson Valley AVA to open ocean: {coast_distance_miles():.1f} miles")
    m = build_ava_map()
    print(f"AVA map: aspect {m['aspect']:.2f}, {len(set(n for n, _ in m['regions']))} AVAs in {len(m['regions'])} shapes, "
          f"rivers {list(m['rivers'])}")
