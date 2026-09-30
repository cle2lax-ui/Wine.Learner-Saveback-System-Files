"""Map data prep for the Mosel Field Guide (slide 3 + locator inset).

REBUILT after a container reset wiped the original local-only version
(never pushed to GitHub). Rebuilt from specs/FG_MOSEL_SPEC.md, which
was discovered only after the reset -- the first build never found it
and used a thinner village list and a locator inset that highlighted
Rhineland-Palatinate alone rather than showing all 13 Anbaugebiete.
This version follows the spec: villages upstream to down (Piesport,
Brauneberg, Bernkastel, Graach, Wehlen, Urzig, Erden), the Saar's
Scharzhofberg, and a locator inset with all 13 regions -- which is
also what directly satisfies Steve's separate request to rework the
map to show Germany's wine regions.

Per the spec's own "open build question": no public Einzellage or
Anbaugebiet polygon set is in hand. Option (a) -- real traced river
courses and a real traced state boundary, with verified labelled
points for villages and regions -- is what's built here, exactly as
the spec calls for. Nothing here is a hand-drawn shape.

SOURCES:
  data/geo/rhineland_palatinate.geojson, data/geo/germany.geojson --
  dissolved from dawidduraj/bundeslaender-geojson (16 German state
  files, municipal-level polygons, unioned per state with Shapely).
  That repo also ships an "EU-DE.geojson" file whose name suggests a
  Germany outline; NOT used -- its actual contents are pan-European
  (Russia, Turkey, Portugal, Iceland all appear in its bounds),
  confirmed by checking each feature's bounding box before trusting
  it. Germany's outline is instead built by dissolving all 16
  correctly-bounded state files together, verified against Germany's
  known real bounding box (5.87-15.04E, 47.27-55.06N).

  data/geo/mosel_river.geojson -- the Mosel's traced course, extracted
  from Natural Earth's 10m rivers_lake_centerlines (one feature only).

  Saar and Ruwer: NOT traced as rivers. Neither appears by name in
  Natural Earth's main rivers layer or its more detailed Europe
  supplement (which drops names from nearly every segment, making it
  unsearchable by river name). Represented only as verified confluence
  points (Konz for the Saar, Trier for the Ruwer) plus Scharzhofberg
  as the Saar's named vineyard landmark -- not fabricated tributary
  geometry.

  Town and region coordinates: standard, widely-documented locations
  (not hand-plotted vineyard geometry, which the spec explicitly rules
  out). Every point is checked with Shapely's contains() against the
  real Rhineland-Palatinate or Germany polygon before use, not assumed.
"""
import json
import math
import os

from shapely.geometry import shape, Point

GEO = os.path.join(os.path.dirname(__file__), "..", "data", "geo")

# Upstream to down, per the spec's own village list, plus Trier/Konz
# for the Saar/Ruwer confluences and Koblenz for the Mosel's own mouth.
TOWNS = {
    "Trier": (6.6371, 49.7499),
    "Konz": (6.5788, 49.6967),
    "Wiltingen": (6.6167, 49.6167),       # Scharzhofberg's village, Saar
    "Piesport": (6.9235, 49.9130),
    "Brauneberg": (7.0389, 49.9270),
    "Bernkastel-Kues": (7.0714, 49.9169),
    "Graach": (7.0611, 49.9424),
    "Wehlen": (7.0333, 49.9337),
    "\u00dcrzig": (6.9968, 49.9685),
    "Erden": (6.9792, 49.9779),
    "Zell": (7.1830, 50.0270),
    "Koblenz": (7.5890, 50.3569),
}

# Germany's 13 Anbaugebiete -- see module docstring for why these are
# single verified points, not traced boundaries.
ANBAUGEBIETE = {
    "Ahr": (7.09, 50.54),
    "Mittelrhein": (7.60, 50.32),
    "Mosel": (7.05, 49.95),
    "Nahe": (7.65, 49.80),
    "Rheingau": (7.95, 50.02),
    "Rheinhessen": (8.10, 49.85),
    "Pfalz": (8.10, 49.35),
    "Hessische Bergstra\u00dfe": (8.62, 49.65),
    "Baden": (7.68, 48.10),
    "W\u00fcrttemberg": (9.20, 49.00),
    "Franken": (9.93, 49.79),
    "Saale-Unstrut": (11.70, 51.20),
    "Sachsen": (13.65, 51.05),
}


def _dissolved_shape(name):
    return shape(json.load(open(os.path.join(GEO, name))))


def build_main_map(target_aspect=1920 / 1150, pad=0.18, pad_lat_frac=0.6):
    rp = _dissolved_shape("rhineland_palatinate.geojson")
    mosel_fc = json.load(open(os.path.join(GEO, "mosel_river.geojson")))
    mosel_geom = shape(mosel_fc["features"][0]["geometry"])

    # Padded a bit wider than the first build to comfortably include
    # Wiltingen/Scharzhofberg on the Saar, southwest of Trier/Konz.
    minx, miny, maxx, maxy = rp.bounds
    minx -= pad; maxx += pad
    miny -= pad * pad_lat_frac; maxy += pad * pad_lat_frac
    mean_lat = (miny + maxy) / 2
    lon_scale = math.cos(math.radians(mean_lat))

    box_w = (maxx - minx) * lon_scale
    box_h = maxy - miny
    if box_w / box_h < target_aspect:
        new_w = box_h * target_aspect
        extra = (new_w / lon_scale - (maxx - minx)) / 2
        minx -= extra; maxx += extra
    else:
        new_h = box_w / target_aspect
        extra = (new_h - (maxy - miny)) / 2
        miny -= extra; maxy += extra

    def project(lon, lat):
        return ((lon - minx) / (maxx - minx), 1 - (lat - miny) / (maxy - miny))

    rp_outline = [project(lon, lat) for lon, lat in rp.exterior.coords]

    parts = list(mosel_geom.geoms) if mosel_geom.geom_type == "MultiLineString" else [mosel_geom]
    longest = max(parts, key=lambda p: p.length)
    mosel_pts = [project(lon, lat) for lon, lat in longest.coords]

    town_pts = {}
    for name, (lon, lat) in TOWNS.items():
        assert rp.contains(Point(lon, lat)) or rp.distance(Point(lon, lat)) < 0.05, \
            f"{name} unexpectedly far from Rhineland-Palatinate"
        town_pts[name] = project(lon, lat)

    return dict(outline=rp_outline, mosel=mosel_pts, towns=town_pts,
                bbox=(minx, miny, maxx, maxy))


def build_locator_inset(marker_town="Bernkastel-Kues", target_aspect=1.0):
    """Germany outline with all 13 Anbaugebiete marked, per the spec
    ("Locator inset: Germany, the 13 Anbaugebiete, Mosel filled").
    Mosel gets a highlighted marker (styled in the slide definition,
    not here); the other 12 are plain verified points."""
    germany = _dissolved_shape("germany.geojson")
    minx, miny, maxx, maxy = germany.bounds
    mean_lat = (miny + maxy) / 2
    lon_scale = math.cos(math.radians(mean_lat))
    box_w = (maxx - minx) * lon_scale
    box_h = maxy - miny
    if box_w / box_h < target_aspect:
        new_w = box_h * target_aspect
        extra = (new_w / lon_scale - (maxx - minx)) / 2
        minx -= extra; maxx += extra
    else:
        new_h = box_w / target_aspect
        extra = (new_h - (maxy - miny)) / 2
        miny -= extra; maxy += extra

    def project(lon, lat):
        return ((lon - minx) / (maxx - minx), 1 - (lat - miny) / (maxy - miny))

    germany_simplified = germany.simplify(0.03, preserve_topology=True)
    polys = list(germany_simplified.geoms) if germany_simplified.geom_type == "MultiPolygon" \
        else [germany_simplified]
    main_poly = max(polys, key=lambda p: p.area)
    outline = [project(lon, lat) for lon, lat in main_poly.exterior.coords]

    regions = {}
    for name, (lon, lat) in ANBAUGEBIETE.items():
        assert germany.contains(Point(lon, lat)), f"{name} unexpectedly outside Germany"
        regions[name] = project(lon, lat)

    lon, lat = TOWNS[marker_town]
    assert germany.contains(Point(lon, lat)), "inset marker must fall within Germany"
    marker = project(lon, lat)

    return dict(outline=outline, regions=regions, marker=marker)


if __name__ == "__main__":
    m = build_main_map()
    print("main map: outline pts", len(m["outline"]), "mosel pts", len(m["mosel"]))
    for name, pt in m["towns"].items():
        print(f"  {name:18s} {pt}")
    inset = build_locator_inset()
    print("inset: outline pts", len(inset["outline"]), "marker", inset["marker"])
    for name, pt in inset["regions"].items():
        print(f"  {name:22s} {pt}")


# ---------------------------------------------------------------------
# Full 13-Anbaugebiete map (slide 3, per Steve's review: "a standard
# wine region map of the 13 German Anbaugebiete"). Region shapes come
# from data/geo/anbaugebiete.geojson -- traced from a CC BY-SA Commons
# SVG and georeferenced against its own 33 city markers (RMS 3.0 km,
# max 5.8 km; see that file's source_note). Drawn over the full Germany
# outline dissolved from the 16 state files, because the source SVG
# itself is cropped to southern Germany (straight cut along its top
# edge) and can't supply a whole-country outline on its own.
# ---------------------------------------------------------------------
def build_anbaugebiete_map():
    germany = _dissolved_shape("germany.geojson")
    regions_fc = json.load(open(os.path.join(GEO, "anbaugebiete.geojson")))
    rivers_fc = json.load(open(os.path.join(GEO, "de_rivers.geojson")))
    minx, miny, maxx, maxy = germany.bounds
    pad = 0.15
    minx -= pad; maxx += pad; miny -= pad; maxy += pad
    lon_scale = math.cos(math.radians((miny + maxy) / 2))
    aspect = (maxx - minx) * lon_scale / (maxy - miny)

    def project(lon, lat):
        return ((lon - minx) / (maxx - minx), 1 - (lat - miny) / (maxy - miny))

    g = germany.simplify(0.02, preserve_topology=True)
    polys = list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
    main_poly = max(polys, key=lambda p: p.area)
    outline = [project(x, y) for x, y in main_poly.exterior.coords]
    islands = [[project(x, y) for x, y in p.exterior.coords]
               for p in polys if p is not main_poly and p.area > 0.02]

    regions, targets = [], {}
    for f in regions_fc["features"]:
        name = f["properties"]["name"]
        geom = shape(f["geometry"])
        parts = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
        for p in parts:
            regions.append((name, [project(x, y) for x, y in p.exterior.coords]))
        rp = max(parts, key=lambda p: p.area).representative_point()
        targets[name] = project(rp.x, rp.y)

    from shapely.geometry import box
    frame = box(minx, miny, maxx, maxy)
    rivers = {}
    for f in rivers_fc["features"]:
        geom = shape(f["geometry"]).intersection(frame)
        if geom.is_empty:
            continue
        lines = list(geom.geoms) if hasattr(geom, "geoms") else [geom]
        rivers.setdefault(f["properties"]["name"], []).extend(
            [[project(x, y) for x, y in ln.coords] for ln in lines if ln.geom_type == "LineString"])
    return dict(aspect=aspect, outline=outline, islands=islands,
                regions=regions, targets=targets, rivers=rivers)
