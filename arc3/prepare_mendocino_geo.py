"""Map data for the Mendocino Field Guide (Arc 3). Reproducible: downloads its sources if missing.

SOURCES (both public domain, so usable in the decks and in the Reel):
  AVA boundaries -- UC Davis AVA Project (UCDavisLibrary/ava), avas_aggregated_files/avas.geojson, CC0 1.0.
  County outlines -- plotly/datasets geojson-counties-fips.json, derived from US Census cartographic boundaries.
OUTPUTS (data/geo/):
  mendocino_avas.geojson    the 13 AVAs touching Mendocino County (12 wholly within + Pine Mountain-Cloverdale Peak, shared
                            with Sonoma), plus the North Coast AVA for context
  mendocino_counties.geojson Mendocino County and its neighbors
  california.geojson        California's outline, dissolved from its 58 counties
ONE DATA CORRECTION: UC Davis lists Comptche as 'within' the North Coast AVA; the TTB's own ruling (T.D. TTB-192, April 2024)
specifically EXCLUDED it from the North Coast AVA. The TTB is the authority on its own AVAs, so the output records Comptche's
'within' as none, with a note.
"""
import json, os, subprocess
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = "/home/claude/geo_src"
URLS = {"avas.geojson": "https://raw.githubusercontent.com/UCDavisLibrary/ava/master/avas_aggregated_files/avas.geojson",
        "counties.json": "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"}
NEIGHBORS = {"06045": "Mendocino", "06023": "Humboldt", "06105": "Trinity", "06103": "Tehama", "06021": "Glenn",
             "06033": "Lake", "06097": "Sonoma", "06011": "Colusa"}

os.makedirs(SRC, exist_ok=True)
for f, u in URLS.items():
    if not os.path.exists(f"{SRC}/{f}"):
        subprocess.run(["curl", "-s", "-m", "300", "-o", f"{SRC}/{f}", u], check=True)

avas = json.load(open(f"{SRC}/avas.geojson"))
keep = []
for ft in avas["features"]:
    p = ft["properties"]
    if "Mendocino" in str(p.get("county", "")) and p.get("removed") in (None, "", "NA"):
        props = {k: p.get(k) for k in ("name", "created", "county", "within")}
        if p["name"] == "Comptche":
            props["within"] = None
            props["note"] = "TTB T.D. TTB-192 (2024) excluded Comptche from the North Coast AVA; UC Davis lists it as within."
        keep.append({"type": "Feature", "properties": props, "geometry": ft["geometry"]})
json.dump({"type": "FeatureCollection", "features": keep}, open(f"{ROOT}/data/geo/mendocino_avas.geojson", "w"))

cty = json.load(open(f"{SRC}/counties.json"))
nb, ca = [], []
for ft in cty["features"]:
    fips = ft["properties"].get("STATE", "") + ft["properties"].get("COUNTY", "") if "STATE" in ft["properties"] else ft.get("id", "")
    if str(fips).startswith("06"):
        ca.append(shape(ft["geometry"]))
        if fips in NEIGHBORS:
            nb.append({"type": "Feature", "properties": {"fips": fips, "name": NEIGHBORS[fips]}, "geometry": ft["geometry"]})
json.dump({"type": "FeatureCollection", "features": nb}, open(f"{ROOT}/data/geo/mendocino_counties.geojson", "w"))
state = unary_union(ca).simplify(0.01)
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "California"},
           "geometry": mapping(state)}]}, open(f"{ROOT}/data/geo/california.geojson", "w"))
print(f"{len(keep)} AVAs, {len(nb)} counties, California from {len(ca)} counties")
for f in keep:
    print(f"   {f['properties']['name']:32s} {f['properties']['created']}")
