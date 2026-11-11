"""Builders for the Wine of Origin maps (slot dicts for engine/modules.py wo_map). Reads data/geo/za_wo_winelands.geojson and ne_10m_sa_clip.geojson
(see prepare_wo_geo.py and data/geo/WO_SOURCE.md for the source and its license caveat)."""
import json
import math
import os

from shapely.geometry import Point, Polygon, box
from shapely.ops import polylabel

HERE = os.path.dirname(os.path.abspath(__file__))
GEO = json.load(open(os.path.join(HERE, "..", "data", "geo", "za_wo_winelands.geojson")))["features"]
LAND = json.load(open(os.path.join(HERE, "..", "data", "geo", "ne_10m_sa_clip.geojson")))["rings"]
CREDIT = "Wine of Origin boundaries: Wine and Spirit Board / SAWIS (VinPro layer). Coast: Natural Earth."
SEA = (222, 233, 240)
REGION_FILL = {"Coastal Region": (176, 208, 158), "Cape South Coast": (158, 194, 222), "Breede River Valley": (236, 214, 150),
               "Olifants River": (224, 180, 150), "Klein Karoo": (208, 198, 186), None: (234, 232, 226)}
WARD_TINTS = [(196, 214, 176), (230, 208, 150), (176, 198, 214), (226, 184, 168), (206, 190, 218), (222, 222, 150), (170, 210, 190), (218, 172, 196),
              (200, 204, 150), (214, 184, 140), (164, 192, 220), (224, 204, 204)]
SEA_FILL = SEA


def feats(level=None, name=None, parent=None):
    return [f for f in GEO if (level is None or f["level"] == level) and (name is None or f["name"] == name) and (parent is None or f["parent"] == parent)]


def _poly_geoms(f):
    return [Polygon(r[0], r[1:]) for r in f["polys"]]


def anchor(f, bbox):
    """The most interior point of the feature's largest piece inside the map window."""
    win = box(bbox[0], bbox[2], bbox[1], bbox[3])
    best = None
    for g in _poly_geoms(f):
        c = g.intersection(win)
        for pc in (c.geoms if hasattr(c, "geoms") else [c]):
            if pc.geom_type == "Polygon" and (best is None or pc.area > best.area):
                best = pc
    if best is None or best.area < 1e-6:
        return None
    p = polylabel(best, tolerance=0.0004)
    return (p.x, p.y), best


def relax(items, bbox, map_w=1920, min_px=104, iters=400):
    """Nudge badge anchors until no two badge BOXES (squares, as the QA tests them) are closer than min_px on both axes at once."""
    mid = math.radians((bbox[2] + bbox[3]) / 2)
    kx = map_w / (bbox[1] - bbox[0])                      # px per degree of longitude
    ky = kx / math.cos(mid)                               # px per degree of latitude (a degree of longitude is cos(lat) as long)
    pos = {k: [v[0][0], v[0][1]] for k, v in items.items()}
    keys = list(pos)
    for _ in range(iters):
        moved = False
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                dx, dy = (pos[b][0] - pos[a][0]) * kx, (pos[b][1] - pos[a][1]) * ky
                if abs(dx) < min_px and abs(dy) < min_px:
                    if abs(dx) >= abs(dy):                # separate along the axis that is already further apart
                        sgn = 1.0 if dx >= 0 else -1.0
                        step = (min_px - abs(dx)) / 2 + 0.5
                        pos[a][0] -= sgn * step / kx
                        pos[b][0] += sgn * step / kx
                    else:
                        sgn = 1.0 if dy >= 0 else -1.0
                        step = (min_px - abs(dy)) / 2 + 0.5
                        pos[a][1] -= sgn * step / ky
                        pos[b][1] += sgn * step / ky
                    moved = True
        if not moved:
            break
    return {k: tuple(v) for k, v in pos.items()}


def tip_for(items, pos, k, bbox, map_w=1920, min_move_px=14):
    """The true anchor, when the badge was moved far enough from it to need a leader; otherwise None."""
    mid = math.radians((bbox[2] + bbox[3]) / 2)
    kx = map_w / (bbox[1] - bbox[0]); ky = kx / math.cos(mid)
    (ax, ay), (px, py) = items[k][0], pos[k]
    return items[k][0] if math.hypot((px - ax) * kx, (py - ay) * ky) > min_move_px else None


def _area_dict(f, fill, number=None, at=None, highlight=False, width=2):
    return dict(rings=f["polys"][0] if len(f["polys"]) == 1 else None, _polys=f["polys"], fill=fill, number=number, at=at, highlight=highlight, width=width)


def _expand(areas):
    """A feature can be several polygons: one area dict per polygon, the badge only on the first."""
    out = []
    for a in areas:
        polys = a.pop("_polys")
        for i, rings in enumerate(polys):
            b = dict(a)
            b["rings"] = rings
            if i:
                b["number"], b["at"], b["tip"] = None, None, None
            out.append(b)
    return out


def district_overview(bbox, key_groups, headline, kicker, standfirst):
    """Districts at true shape, colored by region; the districts in `numbered` get a badge and a key entry."""
    win = box(bbox[0], bbox[2], bbox[1], bbox[3])
    areas, items = [], {}
    for f in feats("District"):
        if not any(g.intersects(win) for g in _poly_geoms(f)):
            continue
        fill = REGION_FILL.get(f["region"], REGION_FILL[None])
        areas.append(_area_dict(f, fill))
    nums = {}
    n = 0
    for _, names in key_groups:
        for nm in names:
            n += 1
            nums[nm] = n
    for a_, f in zip(areas, [f for f in feats("District") if any(g.intersects(win) for g in _poly_geoms(f))]):
        if f["name"] in nums:
            an = anchor(f, bbox)
            if an:
                items[f["name"]] = an
    pos = relax(items, bbox)
    for a_, f in zip(areas, [f for f in feats("District") if any(g.intersects(win) for g in _poly_geoms(f))]):
        if f["name"] in nums and f["name"] in pos:
            a_["number"], a_["at"], a_["tip"] = nums[f["name"]], pos[f["name"]], tip_for(items, pos, f["name"], bbox)
    key = []
    for gi, (hdr, names) in enumerate(key_groups):
        if gi and slot_break(gi):
            key.append({"colbreak": True})
        key.append(dict(header=hdr))
        for nm in names:
            f = feats("District", nm)[0]
            key.append(dict(number=nums[nm], name=nm, fill=REGION_FILL.get(f["region"], REGION_FILL[None])))
    return dict(kicker=kicker, headline=headline, standfirst=standfirst, bbox=bbox, sea=SEA, land=LAND, areas=_expand(areas), key=key, credit=CREDIT)


def slot_break(gi):
    return gi == 1        # the second region group starts the second column


def ward_map(bbox, numbered, headline, kicker, standfirst, highlight=None, context_districts=(), ctx_font=None, focus_district=None):
    """Wards at true shape. `numbered` is [(parent_district, ward_name), ...] in key order: each is tinted, numbered and keyed (the badge sits at the ward's
    most interior point, or offset with a leader when the ward is too small to hold it). Every district in the window is drawn underneath in its region's
    color; the districts in `context_districts` are named quietly (muted italic) in the open ground between the wards."""
    win = box(bbox[0], bbox[2], bbox[1], bbox[3])
    mw = 1920
    areas, items = [], {}
    dist_feats = [f for f in feats("District") if any(g.intersects(win) for g in _poly_geoms(f))]
    for f in dist_feats:        # the focus district in its region's color; its neighbors neutral, so the district a ward sits in reads at once
        fill = REGION_FILL.get(f["region"], REGION_FILL[None]) if (focus_district is None or f["name"] == focus_district) else (236, 234, 228)
        areas.append(_area_dict(f, fill, width=3))
    meta = []
    for n, (par, nm) in enumerate(numbered, start=1):
        f = [x for x in feats("Ward", nm) if x["parent"] == par][0]
        fill = WARD_TINTS[(n - 1) % len(WARD_TINTS)]
        an = anchor(f, bbox)
        if an:
            items[nm] = an
        meta.append((n, par, f, fill))
    pos = relax(items, bbox)
    ward_areas = []
    for n_, par, f, fill in meta:
        a_ = _area_dict(f, fill, number=n_, at=pos.get(f["name"]), highlight=(f["name"] == highlight), width=3)
        if f["name"] in pos:
            a_["tip"] = tip_for(items, pos, f["name"], bbox)
        ward_areas.append(a_)
    key, last = [], None
    for n_, par, f, fill in meta:
        if par != last:
            key.append(dict(header=par.upper()))
            last = par
        key.append(dict(number=n_, name=f["name"], fill=fill, highlight=(f["name"] == highlight)))
    # quiet district names, set in ground not covered by a numbered ward or badge
    ctx = []
    if context_districts and ctx_font is not None:
        from shapely.ops import unary_union
        taken = unary_union([g.buffer(0.012) for _, _, f, _ in meta for g in _poly_geoms(f)])
        mid = math.radians((bbox[2] + bbox[3]) / 2)
        kx = mw / (bbox[1] - bbox[0]); ky = kx / math.cos(mid)
        for nm in context_districts:
            f = feats("District", nm)[0]
            geom = unary_union(_poly_geoms(f)).intersection(win).difference(taken)
            best = max((g for g in (geom.geoms if hasattr(geom, "geoms") else [geom]) if g.geom_type == "Polygon"), key=lambda g: g.area, default=None)
            if best is None or best.area < 1e-5:
                continue
            p = polylabel(best, tolerance=0.0005)
            tw = ctx_font.getlength(nm)
            nx0 = (p.x - bbox[0]) / (bbox[1] - bbox[0]) - tw / 2 / mw
            nx0 = min(max(nx0, 0.015), 0.985 - tw / mw)                    # always inside the frame
            ctx.append((nx0, (bbox[3] - p.y) / (bbox[3] - bbox[2]) - 32 / (mw / ((bbox[1] - bbox[0]) * math.cos(mid) / (bbox[3] - bbox[2]))), nm))
    return dict(kicker=kicker, headline=headline, standfirst=standfirst, bbox=bbox, sea=SEA, land=LAND, areas=_expand(areas) + _expand(ward_areas), key=key, context=ctx, credit=CREDIT)


def slot_break_ward(n_sofar):
    return False
