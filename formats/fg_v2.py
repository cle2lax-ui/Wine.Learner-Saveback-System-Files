"""FIELD GUIDE v2 -- the Reel's visual language on 2160x2700 carousel pages (Arc 3 onward).

Steve: "I really like the visual style of that Reel. Can we evolve our Field Guide, GTR, FFFA and WMID
decks to reflect that style more consistently? ... national flag colors for whatever country we're
featuring, or our standard burgundy or forest green for general topics."

WHAT CARRIES OVER FROM THE REEL
  dark grounds tinted by the theme; condensed black capitals for headlines; Playfair italic for the
  human line; a CHIP naming the series and the page's subject; flag-color bars as a motif; one big
  HERO number in the theme's hero color; data drawn as illustration (maps, bars) rather than prose;
  photos darkened under type with gradients toward the theme's ground.
  Drawn with the Reel's own toolkit (reels/reel_lib.py), so the decks and the Reels share one look.
WHAT STAYS FROM THE SERIES
  the QA harness (type floor 60px, hierarchy, collisions, the 2500px content limit, word budget,
  contrast measured on the rendered pixels); the READ MORE / credit / page-number footer; credits for
  every photo and the map data.

Pages so far: cover(), ava_map(), split(). Each returns a PIL image and raises on a QA failure.
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
for _p in (f"{ROOT}/engine", f"{ROOT}/reels"):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import core                                                               # noqa: E402
from tokens import W, H, M, CONTENT_BOTTOM                                # noqa: E402
from reel_lib import (Photo, chip, darken, fill_poly, fill_rect, finish,  # noqa: E402
                      stroke_path, text, text_width, vgrad)

FOOT_Y = 2632          # footer baseline

# Variety chips are color-coded by grape color (Steve): burgundy for red grapes, lemon for white grapes,
# with a legend on the page. The colors live in engine/themes.py (GRAPE), shared with the Reels.
from themes import GRAPE   # noqa: E402


def canvas(color):
    f = np.empty((H, W, 3), np.float32)
    f[:] = color
    return f


def _star(cx, cy, r):
    return [(cx + (r if k % 2 == 0 else r * 0.42) * math.cos(math.radians(-90 + 36 * k)),
             cy + (r if k % 2 == 0 else r * 0.42) * math.sin(math.radians(-90 + 36 * k))) for k in range(10)]


def flag_bars(f, th, x, y, w=240, h=16, gap=8):
    """The Reel's mini flag motif. Most flags read as three stacked bars of their colors (Germany:
    black, red, gold). The United States does NOT: red-white-blue bars read as the Dutch flag (Steve).
    Its motif is a blue band with white stars ON TOP, over red and white stripes."""
    if th.get("motif") == "stars_stripes":
        red, white, blue = th["bands"]
        w = max(w, 270)
        ch, n_stripes, sh = 46, 5, 9
        fill_rect(f, x, y, x + w, y + ch, blue)
        n = 5
        for i in range(n):
            fill_poly(f, _star(x + w * (i + 0.5) / n, y + ch / 2, 13), white)
        for j in range(n_stripes):
            fill_rect(f, x, y + ch + j * sh, x + w, y + ch + (j + 1) * sh, red if j % 2 == 0 else white)
        return y + ch + n_stripes * sh
    for j, col in enumerate(th["bands"]):
        fill_rect(f, x, y + j * (h + gap), x + w, y + j * (h + gap) + h, col)
    return y + 3 * (h + gap) - gap


def footer(f, qa, th, page, total, credit=None):
    text(f, "READ MORE \u2190", "condb", 46, th["text"], M, FOOT_Y, tracking=1)
    num = f"{page:02d}/{total:02d}"
    text(f, num, "condb", 46, th["text"], W - M, FOOT_Y, align="right")
    if credit:
        text(f, credit, "med", 32, th["muted"], W / 2, FOOT_Y - 4, align="center")
    qa.size("!footer", 46)
    qa.size("!credit", 32)
    qa.box("footer", (M, FOOT_Y - 50, W - M, FOOT_Y + 14))


def fit_size(txt, fname, max_w, start, tracking=0, floor=60):
    for sz in range(start, floor - 1, -2):
        if text_width(txt, fname, sz, tracking) <= max_w:
            return sz
    return floor


def to_image(f, fi=0):
    return Image.fromarray(finish(f, fi, grain=2.5, vignette=False))


# ============================================================================ COVER
def cover(slot, th, total):
    """Full-bleed photo; the sky is deepened into the theme's ground so the title reads in white;
    chip, kicker, title fitted to the width, flag bars, italic subtitle."""
    qa = core.QA(f"FG2 cover ({slot['title']})")
    ph = Photo(slot["photo"], cover=1.0, size=(W, H))
    f = ph.view(zoom=slot.get("zoom", 1.0), fx=0.5, fy=slot.get("anchor", 0.7))
    # HOLD the deep ground through the whole type zone, then fade into the photo. The first version
    # faded from the top edge, so the title's lower half sat on lighter sky (QA: bg 169 under white).
    darken(f, vgrad(slot.get("sky_hold", 1000), slot.get("sky_fade", 1600), 0.93, 0.0, height=H), th["ground"])
    darken(f, vgrad(2200, H, 0.0, 0.85, height=H), th["ground"])
    bg_before_type = f.copy()                       # for a true contrast check, without the letters
    chip(f, slot.get("chip", "THE FIELD GUIDE"), M, 262, 1.0, fill=th["chip"], ink=th["chip_ink"], size=60, align="left")
    qa.size("chip", 60)
    text(f, slot["kicker"], "black", 60, th["muted"], M, 452, tracking=6)
    qa.size("kicker", 60)
    tsz = fit_size(slot["title"], "cond", W - 2 * M, 420, tracking=6)
    text(f, slot["title"], "cond", tsz, th["text"], M - 6, 452 + tsz * 0.86, tracking=6)
    qa.size("title", tsz, headline=True)
    ty = 452 + tsz * 0.86
    by = flag_bars(f, th, M, int(ty + 46))
    text(f, slot["subtitle"], "serif_it", 100, th["text"], M, by + 130)
    qa.size("subtitle", 100)
    qa.add_words(" ".join([slot["kicker"], slot["title"], slot["subtitle"]]))
    qa.box("title_block", (M, 200, W - M, by + 160))
    footer(f, qa, th, 1, total, slot.get("credit"))
    img = to_image(f)
    qa.check_photo_contrast(img, (M, 452, M + text_width(slot["title"], "cond", tsz, 6), ty), 255, "title on sky")
    _true_contrast(qa, bg_before_type, (M, 380, W - M, by + 160), th["text"], 4.5, "title block (vs 90th-pct background)")
    print(qa.report(img))
    return img


def _true_contrast(qa, bg, box, fg, floor, label):
    """WCAG contrast of the type color against the 90th-percentile luminance of the background UNDER the
    type, measured before the type was drawn (core's photo check samples the region with the letters in it)."""
    x0, y0, x1, y1 = [int(v) for v in box]
    reg = bg[max(y0, 0):min(y1, H), max(x0, 0):min(x1, W)] / 255.0
    lin = np.where(reg <= 0.03928, reg / 12.92, ((reg + 0.055) / 1.055) ** 2.4)
    L = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
    lb = float(np.percentile(L, 90))
    c = (max(_lum(fg), lb) + 0.05) / (min(_lum(fg), lb) + 0.05)
    qa.notes.append(f"info {label}: {c:.1f}:1")
    if c < floor:
        qa.notes.append(f"FAIL true-contrast {label}: {c:.2f} < {floor}")


def _lum(c):
    v = np.array(c, np.float64) / 255.0
    v = np.where(v <= 0.03928, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2])


# ============================================================================ AVA MAP
def _proj(bounds, box):
    lon0, lat0, lon1, lat1 = bounds
    k = math.cos(math.radians((lat0 + lat1) / 2))
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / ((lon1 - lon0) * k), (by1 - by0) / (lat1 - lat0))
    ox = bx0 + ((bx1 - bx0) - s * (lon1 - lon0) * k) / 2
    oy = by0 + ((by1 - by0) - s * (lat1 - lat0)) / 2
    return lambda lon, lat: (ox + s * (lon - lon0) * k, oy + s * (lat1 - lat))


def _rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [poly[0] for poly in polys]                       # exterior rings (holes ignored at this scale)


def ava_map(slot, th, total, page):
    """A county's AVAs drawn from real boundary data. slot: headline lines, focus AVA, labels column,
    inset of the state, a hero stat block."""
    from shapely.geometry import shape
    qa = core.QA(f"FG2 map ({slot['chip']})")
    f = canvas(th["ground"])
    avas = json.load(open(slot["avas"]))["features"]
    counties = json.load(open(slot["counties"]))["features"]
    state = json.load(open(slot["state"]))["features"][0]
    home = next(c for c in counties if c["properties"]["name"] == slot["county"])
    hb = shape(home["geometry"]).bounds
    pad = 0.03
    P = _proj((hb[0] - pad, hb[1] - pad, hb[2] + pad, hb[3] + pad), slot["map_box"])
    # neighbors (context) and the home county
    for c in counties:
        for ring in _rings(c["geometry"]):
            pts = [P(*q) for q in ring]
            if c is home:
                fill_poly(f, pts, th["ground_alt"])
                stroke_path(f, pts + [pts[0]], th["text"], 4, alpha=0.55)
            else:
                stroke_path(f, pts + [pts[0]], th["map_line"], 2, alpha=0.30)
    # neighbors are context AROUND the county, not page-wide lines: repaint everything outside the map's
    # frame (the first render ran them behind the headline and through the state inset)
    bx0, by0, bx1, by1 = slot["map_box"]
    e = slot.get("context_margin", 60)
    gx0, gy0, gx1, gy1 = max(int(bx0 - e), 0), max(int(by0 - e), 0), min(int(bx1 + e), W), min(int(by1 + e), H)
    g = np.array(th["ground"], np.float32)
    f[:gy0] = g; f[gy1:] = g; f[:, :gx0] = g; f[:, gx1:] = g
    # the parent AVA, then the others, then the focus on top
    order = sorted(avas, key=lambda a: (a["properties"]["name"] != slot["parent"], a["properties"]["name"] == slot["focus"]))
    rep = {}
    for a in order:
        nm = a["properties"]["name"]
        if nm in slot.get("skip", ()):
            continue
        style = slot["styles"].get(nm, "other")
        for ring in _rings(a["geometry"]):
            pts = [P(*q) for q in ring]
            if style == "parent":
                fill_poly(f, pts, (255, 255, 255), 0.05)
                stroke_path(f, pts + [pts[0]], th["map_line"], 3, alpha=0.55)
            elif style == "focus":
                fill_poly(f, pts, th["map_fill"], 0.92)
                stroke_path(f, pts + [pts[0]], (255, 255, 255), 3, alpha=0.9)
            elif style == "ridge":
                fill_poly(f, pts, slot["ridge_color"], 0.80)
            else:
                fill_poly(f, pts, (255, 255, 255), 0.12)
                stroke_path(f, pts + [pts[0]], th["map_line"], 3, alpha=0.85)
        g = shape(a["geometry"])
        rp = g.representative_point()
        rep[nm] = P(rp.x, rp.y)
    # ocean label, rotated along the coast
    oc = slot.get("ocean")
    if oc:
        text(f, oc["text"], "black", 60, th["muted"], oc["x"], oc["y"], tracking=10, rot=90, alpha=0.75)
        qa.size("ocean", 60)
    # LABELS. Diagnosis of the first layout (Steve: "too long and should never cross"): one column on the
    # far right, ordered by height alone, with elbow leaders -- 7 crossing pairs, mean 410px, max 550px.
    # The western AVAs had to cross the whole county, and two AVAs at a similar height on opposite sides
    # had to cross each other. Now: AVAs west of the county's center line are labeled in a LEFT column
    # (over the Pacific), the rest on the RIGHT; within a column the slots are packed as before, and
    # anchors are assigned to slots by MINIMUM TOTAL LEADER LENGTH (Hungarian algorithm). A minimum-length
    # matching cannot contain two crossing straight segments (swapping their ends would be shorter, by
    # the triangle inequality), and no leader can cross between columns because each side's anchors lie
    # on its own side of the center line. Leaders are straight. Crossings are a hard QA failure.
    from scipy.optimize import linear_sum_assignment
    cols = slot["columns"]
    split_x = cols.get("split_x") or (P(hb[0], hb[1])[0] + P(hb[2], hb[1])[0]) / 2
    top, bot = slot["label_top"], slot["label_bottom"]
    LH1, LH2 = 92, 152                                          # slot height: one line, two lines
    leaders = []
    for side in ("left", "right"):
        names = [n for n in slot["labels"] if n in rep and ((rep[n][0] < split_x) == (side == "left"))]
        if not names:
            continue
        hts = {n: (LH2 if "\n" in slot["labels"][n] else LH1) for n in names}
        order = sorted(names, key=lambda n: rep[n][1])
        need = sum(hts[n] for n in order) - hts[order[-1]]
        if need > bot - top:
            raise ValueError(f"{side} column: {len(order)} labels need {need}px; it has {bot - top}px")
        def pack(desired, heights):
            ys = []
            for i, (d, h) in enumerate(zip(desired, heights)):
                ys.append(max(d, top, ys[-1] + heights[i - 1] if ys else top))
            ys[-1] = min(ys[-1], bot)
            for i in range(len(ys) - 2, -1, -1):
                ys[i] = min(ys[i], ys[i + 1] - heights[i])
            return ys
        x_edge = cols["left_x"] if side == "left" else cols["right_x"]
        att_x = x_edge + 18 if side == "left" else x_edge - 18
        # The no-crossing guarantee needs an UNCONSTRAINED minimum-length assignment (any label may take any
        # slot). The first version restricted two-line labels to two-line slots, and the hard check caught
        # the crossing that allowed (Yorkville Highlands x Pine Mountain-Cloverdale Peak). So: assign freely,
        # re-pack the slots with the heights in the order the assignment produced, and repeat until stable.
        seq = order[:]
        ys = pack([rep[n][1] for n in seq], [hts[n] for n in seq])
        for _ in range(12):
            cost = np.array([[math.dist(rep[n], (att_x, y - 22)) for y in ys] for n in seq])
            ri, ci = linear_sum_assignment(cost)
            new_seq = [None] * len(seq)
            for i, j in zip(ri, ci):
                new_seq[j] = seq[i]
            new_ys = pack(ys, [hts[n] for n in new_seq])
            if new_seq == seq and new_ys == ys:
                break
            seq, ys = new_seq, new_ys
        ri, ci = list(range(len(seq))), list(range(len(seq)))
        order = seq
        for i, j in zip(ri, ci):
            n = order[i]
            y = ys[j]
            lines = slot["labels"][n].split("\n")
            col = th["hero"] if n == slot["focus"] else slot["ridge_label"] if slot["styles"].get(n) == "ridge" else th["text"]
            al = "right" if side == "left" else "left"
            wmax = 0
            for k, ln in enumerate(lines):
                text(f, ln, "cond" if k == 0 else "condb", 62 if k == 0 else 60, col if k == 0 else th["muted"],
                     x_edge, y + k * 64, align=al)
                wmax = max(wmax, text_width(ln, "cond" if k == 0 else "condb", 62 if k == 0 else 60))
            room = (x_edge - M) if side == "left" else (W - M - x_edge)
            if wmax > room:
                raise ValueError(f"label '{lines[0]}' is {wmax:.0f}px; its column has {room:.0f}px")
            x0b, x1b = (x_edge - wmax, x_edge) if side == "left" else (x_edge, x_edge + wmax)
            qa.box(f"label {n}", (x0b, y - 52, x1b, y + 14 + 64 * (len(lines) - 1)))
            qa.size(f"label {n}", 60)
            qa.add_words(" ".join(lines))
            leaders.append((n, rep[n], (att_x, y - 22)))
    for n, a_, b_ in leaders:
        stroke_path(f, [a_, b_], th["muted"], 2, alpha=0.75)
        fill_poly(f, [(a_[0] + 7 * math.cos(t), a_[1] + 7 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 16)], th["text"])

    def _x(p1, p2, p3, p4):
        def o(a, b, c):
            v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            return (v > 1e-9) - (v < -1e-9)
        return o(p1, p2, p3) * o(p1, p2, p4) < 0 and o(p3, p4, p1) * o(p3, p4, p2) < 0
    crossings = [(u[0], v[0]) for i, u in enumerate(leaders) for v in leaders[i + 1:] if _x(u[1], u[2], v[1], v[2])]
    lengths = [math.dist(a_, b_) for _, a_, b_ in leaders]
    qa.notes.append(f"info leaders: {len(crossings)} crossings; length max {max(lengths):.0f}px, mean {sum(lengths) / len(lengths):.0f}px")
    if crossings:
        qa.notes.append(f"FAIL leader crossings: {crossings}")
    if max(lengths) > slot.get("leader_max", 480):
        qa.notes.append(f"FAIL leader length: {max(lengths):.0f}px > {slot.get('leader_max', 480)}")
    # inset: the state, the county highlighted
    sb = shape(state["geometry"]).bounds
    Pi = _proj(sb, slot["inset_box"])
    for ring in _rings(state["geometry"]):
        pts = [Pi(*q) for q in ring]
        fill_poly(f, pts, th["ground_alt"])
        stroke_path(f, pts + [pts[0]], th["map_line"], 2, alpha=0.7)
    for ring in _rings(home["geometry"]):
        fill_poly(f, [Pi(*q) for q in ring], th["map_fill"])
    text(f, slot["inset_label"], "black", 60, th["muted"], (slot["inset_box"][0] + slot["inset_box"][2]) / 2,
         slot["inset_box"][3] + 80, align="center", tracking=4)
    qa.size("inset label", 60)
    # headline block
    chip(f, slot["chip"], M, 262, 1.0, fill=th["chip"], ink=th["chip_ink"], size=60, align="left")
    qa.size("chip", 60)
    l1, l2 = slot["headline"]
    text(f, l1, "cond", 236, th["text"], M - 4, 570, tracking=2)     # 236 > the 190px stat + the 30px hierarchy gap
    text(f, l2, "cond", 150, th["hero"], M - 2, 725, tracking=2)
    qa.size("headline", 236, headline=True)
    qa.size("headline 2", 150)
    text(f, slot["subline"], "med", 62, th["muted"], M, 815)
    qa.size("subline", 62)
    qa.add_words(" ".join([l1, l2, slot["subline"]]))
    qa.box("headline", (M, 200, W - M, 840))
    # hero stat strip along the bottom: the big number, then its unit and two lines beside it
    sx, sy = slot["stat_xy"]
    st = slot["stat"]
    fill_rect(f, M, sy - 250, W - M, sy - 246, th["muted"], 0.5)
    text(f, st["big"], "cond", 190, th["hero"], sx, sy)
    cx = sx + text_width(st["big"], "cond", 190) + 60
    text(f, st["unit"], "black", 64, th["text"], cx, sy - 130, tracking=3)
    for i, line in enumerate(st["lines"]):
        text(f, line, "med", 60, th["muted"], cx, sy - 55 + i * 70)
        qa.add_words(line)
    qa.size("stat", 190)
    qa.size("stat lines", 60)
    qa.add_words(st["big"] + " " + st["unit"])
    qa.box("stat", (M, sy - 240, W - M, sy + 30))
    footer(f, qa, th, page, total, slot.get("credit"))
    img = to_image(f)
    print(qa.report(img))
    for n in qa.notes:
        if n.startswith("info"):
            print("  " + n)
    return img


# ============================================================================ SPLIT (two climates)
def split(slot, th, total, page):
    """Two stacked photo panels joined by a temperature strip: each panel has a kicker, a heading
    and variety chips. A closing 'twist' line sits on the lower panel."""
    qa = core.QA(f"FG2 split ({slot['chip']})")
    f = canvas(th["ground"])
    seam = slot.get("seam", 1310)
    panels = [(0, seam - 30, slot["top"]), (seam + 30, CONTENT_BOTTOM + 200, slot["bottom"])]
    for y0, y1, p in panels:
        ph = Photo(p["photo"], cover=1.0, size=(W, y1 - y0))
        img = ph.view(zoom=p.get("zoom", 1.0), fx=0.5, fy=p.get("anchor", 0.5))
        darken(img, np.float32(0.18), th["ground"])
        darken(img, vgrad(int((y1 - y0) * 0.35), y1 - y0, 0.0, 0.88, height=y1 - y0), th["ground"])
        f[y0:y1] = img
    darken(f, vgrad(0, 480, 0.85, 0.0, height=H), th["ground"])
    # the temperature strip between the panels (the theme's blue -> its red)
    cold, warm = slot["cold"], slot["warm"]
    for i in range(60):
        t = i / 59
        col = tuple(cold[k] + (warm[k] - cold[k]) * t for k in range(3))
        fill_rect(f, W * t, seam - 30, W * (t + 1 / 59) + 1, seam + 30, col)
    text(f, slot["strip_left"], "black", 60, (255, 255, 255), M, seam + 22, tracking=4)
    text(f, slot["strip_right"], "black", 60, (255, 255, 255), W - M, seam + 22, align="right", tracking=4)
    qa.size("strip", 60)
    chip(f, slot["chip"], M, 262, 1.0, fill=th["chip"], ink=th["chip_ink"], size=60, align="left")
    qa.size("chip", 60)
    # legend for the grape colors, top right
    lx = W - M
    for label, kind in (("WHITE GRAPES", "white"), ("RED GRAPES", "red")):
        w = text_width(label, "black", 60, 1) + 64
        lx -= w
        chip(f, label, lx, 262, 1.0, fill=GRAPE[kind][0], ink=GRAPE[kind][1], size=60, align="left", tracking=1)
        lx -= 22
    qa.box("legend", (lx, 200, W - M, 325))
    qa.box("chip", (M, 200, M + text_width(slot["chip"], "black", 60, 2) + 64, 325))
    low = CONTENT_BOTTOM - (520 if slot.get("twist") else 360)   # room for a wrapped chip row above the twist
    for (y0, y1, p), base in ((panels[0], seam - 330), (panels[1], low)):
        text(f, p["kicker"], "black", 60, p["kicker_color"], M, base - 190, tracking=6)
        text(f, p["heading"], "cond", 196, th["text"], M - 4, base - 30)
        qa.size("panel heading", 196, headline=True)
        qa.size("panel kicker", 60)
        qa.add_words(p["kicker"] + " " + p["heading"])
        # chips WRAP to a second row; they are never dropped (a silent drop is the card_grid bug)
        x, row = M, 0
        for v, kind in p["chips"]:
            w = text_width(v, "black", 62, 1) + 64
            if x + w > W - M:
                x, row = M, row + 1
            fillc, inkc = GRAPE[kind]
            chip(f, v, x, base + 70 + row * 130, 1.0, fill=fillc, ink=inkc, size=62, align="left", tracking=1)
            x += w + 22
            qa.add_words(v)
        qa.size("variety chips", 62)
        qa.box(f"panel {p['heading']}", (M, base - 250, W - M, base + 140 + row * 130))
    tw = slot.get("twist")
    if tw:
        text(f, tw[0], "serif_it", 70, th["text"], M, CONTENT_BOTTOM - 70)
        text(f, tw[1], "serif_it", 70, th["text"], M, CONTENT_BOTTOM - 0)
        qa.size("twist", 70)
        qa.add_words(" ".join(tw))
        qa.box("twist", (M, CONTENT_BOTTOM - 140, W - M, CONTENT_BOTTOM))
    footer(f, qa, th, page, total, slot.get("credit"))
    img = to_image(f)
    print(qa.report(img))
    return img
