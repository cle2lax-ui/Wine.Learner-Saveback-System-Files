"""
map_atlas.py -- v8 save-back

Generic regional-map rendering engine, extracted and generalized from the
Oregon Field Guide build (2026-08). Prior to this, every deck that needed a
map (Oregon, Chile, Washington, GTR decks) either duplicated ad-hoc label
placement code or accepted labels that overlapped map linework, city names,
inset frames, or each other. The Oregon session burned a genuinely large
number of iterations discovering why each naive approach failed; this module
is the settled, battle-tested result. Read the docstrings below before
modifying the placement algorithm -- most of what looks like unnecessary
complexity here is a fix for a specific, previously-shipped visual bug.

Requires: core.py, modules.py (for _chaikin, _start, kicker_block, _finish).

USAGE
-----
For a single map panel (no inset), call draw_map_panel() directly inside a
deck-local slide function.

For the common "main map + zoomed inset with callout lines" composition
(the Oregon atlas pattern), call regional_atlas() as a MODULES entry, e.g.:

    from map_atlas import regional_atlas
    MODULES["regional_atlas"] = regional_atlas

    SLIDES = [
        ("regional_atlas", dict(
            kicker="APPELLATIONS",
            headline="...",
            main=dict(outline=..., aspect=..., regions=[...], rivers={...},
                      mountain_labels=[...], cities={...}, labels=[...]),
            inset=dict(outline=..., aspect=..., regions=[...], labels=[...]),
            inset_title="WILLAMETTE VALLEY",
            inset_zoom_region=[...],  # polygon (normalized 0-1 pts) the
                                       # zoom-lines anchor to on the main map
            description="...",
        )),
    ]

PANEL DICT SCHEMA (both "main" and "inset" use the same shape)
----------------------------------------------------------------
    outline: list[(x, y)] normalized 0-1 polygon, the panel's own boundary
    aspect: float, TRUE width/height ratio of the real geography (not the
        box it's drawn into) -- get this right or the map visibly stretches.
        1 degree of longitude covers less real ground than 1 degree of
        latitude away from the equator; correct for this before setting
        aspect, don't just use the raw lat/lon bounding box ratio.
    outline_smooth: int, Chaikin smoothing iterations for the outline
        (default 8). NEVER raise this per-iteration count alone to smooth a
        rough polygon further -- point count roughly doubles per iteration,
        which is fine at 8 but can blow up rendering time/memory well before
        you'd expect if pushed much higher. Simplify the source polygon
        first (fewer input points), then apply light smoothing, rather than
        over-smoothing a dense polygon.
    regions: list[(name, polygon_pts, fill_color)] -- sub-regions filled and
        outlined within the panel
    rivers: dict[name -> list[segment]], segment = list[(x,y)]
    mountain_labels: list[dict(x, y_start, y_end, text, bow)] -- curved
        labels following a north-south line (see curved_text())
    cities: dict[name -> (x, y)] -- keep this list SHORT. Every city label
        is another obstacle for region labels to collide with; the Oregon
        session had to drop two of four city labels entirely because their
        latitude band was too crowded for both city names and region names
        to coexist. Prefer 2-3 of the most essential reference points over
        a complete gazetteer.
    labels: list[(name, target_normalized_xy)] -- the region/AVA name labels
        this panel places automatically (see draw_map_panel())
    pinned_labels: set[str] -- label names that should sit directly AT their
        target (centered, no leader line) instead of going through the
        automatic side-assignment + packing algorithm. Use this for a label
        whose target is isolated enough that pinning is unambiguously better
        (see LABEL PLACEMENT ALGORITHM below for why this isn't the default).
    forced_side: dict[str -> "left"|"right"] -- override automatic side
        assignment for specific labels
    anchor_override: dict[str -> "top_middle"] -- override the leader-line
        attachment point for specific labels (currently only "top_middle" is
        implemented; extend as needed)
    left_margin_offset: (unused as of v8 -- see LABEL PLACEMENT ALGORITHM,
        left-side positioning is now fully adaptive per-label, not a single
        panel-wide margin. Left here as a documented no-op key in case a
        future deck's slot data still sets it from before this rewrite.)
    max_label_w: int, px, wrap width for label text (default ~220-280
        depending on panel size)
    ocean_label: dict(x, y_start, y_end, text, bow) -- same curved-text
        treatment as mountain_labels, rendered in a distinct blue

LABEL PLACEMENT ALGORITHM -- the actual hard-won part
-------------------------------------------------------
This went through several genuinely broken iterations before landing here.
Each rule below exists because removing it reintroduces a specific bug that
shipped and was caught by visual review, not because it "seemed thorough."

1. EACH LABEL STARTS AT ITS OWN NATURAL TARGET Y-POSITION.
   Never cascade/anchor from the first label in sorted order and pack the
   rest relative to it. An earlier version did exactly that (pack
   sequentially from the topmost label's position using a minimum gap) and
   it looked fine when all targets were close together vertically -- but
   for a panel spanning a wide latitude range, it dragged every subsequent
   label up toward the first one's position, producing 400-700px leader
   lines for labels whose real targets were far down the map. The fix:
   ly = target_y - label_height/2 for every label independently, THEN
   resolve collisions (see #2). This is the single most important rule in
   this file.

2. COLLISION RESOLUTION IS FORWARD-PASS ONLY, THEN CHAIN-CLAMPED.
   Sort same-side labels by target y. Walk down the list once: if a label
   would overlap the one above it, push it down (never up, never
   reorder). This preserves natural position everywhere except genuine
   overlaps. After the pass, if the last label's bottom edge fell past the
   panel's bottom margin, shift the WHOLE chain up by the overflow amount
   (preserves relative spacing rather than clamping labels individually,
   which would reintroduce local overlaps).

3. LEFT-SIDE LABEL X-POSITION IS ADAPTIVE PER LABEL, NEVER ONE FIXED MARGIN.
   lx = target_x - label_width - small_buffer, clamped to the panel's own
   left edge. A single fixed margin value seems simpler and worked for a
   while, but it breaks in two opposite ways depending on geography: at a
   latitude where the landmass is wide, a margin tuned to clear the
   coastline overshoots PAST the actual target, landing the label on top of
   or past the region it's naming. At a narrower latitude, the same fixed
   margin undershoots, leaving a large ugly gap between the label and its
   target. Per-label adaptive positioning is the only approach that's
   correct at every latitude simultaneously, and it applies identically to
   inset panels -- a separate "just move the inset's margin in a bit"
   fixed-value patch was tried and also failed for the same underlying
   reason.

4. OBSTACLE AVOIDANCE TRIES ALL FOUR DIRECTIONS, PICKS THE SMALLEST MOVE.
   When a label (including a pinned one) collides with a known obstacle
   bounding box (typically an inset's frame), compute the displacement
   needed to clear it in each of up/down/left/right (left/right only for
   the label's own side, i.e. a left-side label can move further left, a
   right-side label further right -- moving a label toward map-center to
   dodge an obstacle usually creates a worse collision than the one being
   fixed). Take whichever direction needs the least movement. An earlier
   version only ever considered up/down, which turned a small, easily-fixed
   sideways overlap into a 400+ px vertical jump for a label whose target
   happened to sit just past the obstacle's edge.

5. RUN A CROSS-SIDE BOX-OVERLAP CHECK, NOT JUST SAME-SIDE.
   Every check above resolves collisions WITHIN one side (left labels vs
   left labels, right vs right). But making every label sit close to its
   own target (rule #3) means a left-side and a right-side label can end up
   at the same height with their edges genuinely touching -- something a
   same-side-only check will never catch, because by construction it never
   compares a left label to a right label. Run one more pass: for every
   cross-side pair, check literal box overlap (not leader-line crossing --
   actual rectangle intersection), and if found, nudge the label with the
   larger target-y down by a small fixed amount.

6. ZOOM/CALLOUT LINES ANCHOR TO THE POLYGON'S ACTUAL EXTREME POINTS.
   When drawing a "zoomed out from here" indicator between a main map and
   an inset, anchor the lines to the region polygon's real topmost/
   bottommost points (min/max by y over the actual polygon vertices), NOT
   the bounding box's synthetic corners. For a tall, irregular polygon
   (most real geographic regions), the bbox's own corner routinely sits in
   empty space next to the shape rather than on it -- the earlier version
   used bbox corners and produced a callout line that visibly didn't touch
   the region it was supposedly indicating.

7. GLYPH LAYER SIZING FOR ROTATED/CURVED TEXT: ASCENT+DESCENT, NOT WIDTH.
   See curved_text() below. A per-character rotation layer sized from the
   character's rendered WIDTH clips most letters vertically before the
   rotation is even applied, since ascent+descent at a given font size is
   routinely 2-3x a single narrow character's width. This produced curved
   labels that looked like scattered fragments rather than legible text,
   and the bug was invisible in any pixel-count or bounding-box QA check --
   it was only caught by actually zooming into the rendered image.

8. NOT YET DONE (next refinement): side assignment currently uses a simple
   "which half of the panel is the target in" rule. A better version would
   choose whichever side puts a label closest to its own region's visual
   center, with leader-line necessity decided only AFTER side and position
   are set, biased toward the shortest possible line (including none).
   The current rule works well in practice but hasn't been generalized to
   optimize for this directly.

FOUR-DESIGNER REVIEW -- run this on every finished deck, every slide.
------------------------------------------------------------------------
See DESIGN_PROCESS_v8.md for the full standing instruction. In short: after
a deck is otherwise complete, do four full passes over every slide, one
lens at a time, in this order:

  1. Anna Wintour -- editorial authority. Does every slide make a clear,
     confident claim? Cut anything that hedges, pads, or dilutes the point.
  2. Coco Chanel -- "elegance is refusal." On each slide, is there one more
     thing that could come off without losing anything real? Only remove
     what's genuinely decorative; don't cut things that are load-bearing
     for clarity or navigation just because they look prunable.
  3. Jony Ive -- true simplicity. Does the page's FORM actually reveal its
     content's real claim, or does it just state the claim in text while
     the visual treatment stays neutral? (The grapes-data slide's
     proportional photo-stack is the reference example: the claim "one
     grape dominates" only became true simplicity once it was visible in
     the relative size of the images, not just asserted in a caption.)
  4. Massimo Vignelli -- grid discipline. Do parallel content blocks
     (columns, table rows, callouts) actually terminate together? Is
     whitespace doing structural work, or is it just left over because
     nothing filled it?

Each round should visually inspect every single slide -- not one example
slide standing in for the rest -- and make real edits where warranted, not
change things for the sake of demonstrating each round happened. It is
normal and expected for later rounds to find fewer issues than earlier ones
on a deck that's already been through prior polish; don't force a change
just to show effort.
"""

import math
from PIL import Image, ImageDraw

import core
import modules
from core import M, font, text_w, wrap


def curved_text(img, p_start, p_end, bow, text, f, fill, tracking=14):
    """Draws text along a gentle quadratic-Bezier arc from p_start to
    p_end (bow = perpendicular offset of the curve's control point, in
    px -- how much it bends), one character at a time, each rotated to
    the curve's local tangent. Used for mountain-range / ocean labels so
    they read as following a line's length rather than sitting as one
    flat rotated block.

    Glyph layer sizing uses font ascent+descent, NOT character width --
    see module docstring rule #7. Getting this wrong clips most letters
    before rotation and is invisible to any non-visual QA check.
    """
    d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    x0, y0 = p_start
    x2, y2 = p_end
    mx, my = (x0 + x2) / 2, (y0 + y2) / 2
    dx, dy = x2 - x0, y2 - y0
    length = math.hypot(dx, dy) or 1
    perp = (-dy / length, dx / length)
    cx, cy = mx + perp[0] * bow, my + perp[1] * bow

    def bez(t):
        omt = 1 - t
        x = omt**2 * x0 + 2 * omt * t * cx + t**2 * x2
        y = omt**2 * y0 + 2 * omt * t * cy + t**2 * y2
        return x, y

    def tangent_angle(t):
        eps = 0.001
        x1, y1 = bez(max(0, t - eps))
        x2_, y2_ = bez(min(1, t + eps))
        return math.degrees(math.atan2(y2_ - y1, x2_ - x1))

    char_widths = [text_w(d0, ch, f) for ch in text]
    total_w = sum(char_widths) + tracking * (len(text) - 1)
    t = 0.5 - (total_w / 2) / length if length else 0.5
    asc, desc = f.getmetrics()
    glyph_h = asc + desc  # the actual vertical room a glyph needs -- see rule #7
    pad = 12
    for ch, cw in zip(text, char_widths):
        t_pos = t + (cw / 2) / length
        px, py = bez(max(0, min(1, t_pos)))
        angle = -tangent_angle(max(0, min(1, t_pos)))
        layer = Image.new("RGBA", (cw + pad * 2, glyph_h + pad * 2), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((pad, pad), ch, font=f, fill=fill)
        rotated = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
        img.paste(rotated, (int(px - rotated.width / 2), int(py - rotated.height / 2)), rotated)
        t += (cw + tracking) / length


def draw_map_panel(img, d, pal, panel, box_x0, box_y0, box_w, box_h,
                    label_size=50, mark_r=9, avoid_bbox=None):
    """Draws one map panel (outline, regions, rivers, mountain labels,
    cities, leader-line labels) into the given box, fitting the map's
    TRUE aspect ratio (panel["aspect"]) via contain-style fitting rather
    than stretching to fill the box. Returns the actual (x0, y0, w, h)
    the map ended up drawn into, for a caller that needs to position
    something relative to it (e.g. an inset's frame).

    See module docstring for the full label-placement algorithm and why
    each piece of it exists.
    """
    aspect = panel["aspect"]
    if box_w / box_h > aspect:
        h = box_h
        w = h * aspect
    else:
        w = box_w
        h = w / aspect
    map_align = panel.get("map_align", "center")
    if map_align == "right":
        x0 = box_x0 + (box_w - w)
    elif map_align == "left":
        x0 = box_x0
    else:
        x0 = box_x0 + (box_w - w) / 2
    y0 = box_y0 + (box_h - h) / 2

    def P(pt):
        return (x0 + pt[0] * w, y0 + pt[1] * h)

    # water_color: fills the whole map box before any land is drawn, so
    # every gap between landmasses (an estuary, a strait between an
    # outline and an extra outlines[] piece) reads as shaded water for
    # free, rather than needing a hand-traced river/estuary polygon.
    # Added for the greater-Bordeaux overview (Médoc + Right Bank +
    # Entre-Deux-Mers as separate outline pieces around the Gironde/
    # Garonne/Dordogne) -- optional, default None leaves the box
    # untouched so existing single-landmass decks (Oregon, Chile) render
    # identically.
    if panel.get("water_color"):
        d.rectangle([box_x0, box_y0, box_x0 + box_w, box_y0 + box_h], fill=panel["water_color"])

    # outlines: extra landmass pieces beyond the primary `outline` --
    # each drawn identically (white fill, ink border). Lets one panel
    # depict multiple, geographically-separate landmasses (e.g. the
    # Médoc peninsula and the Right Bank, real pieces separated by the
    # Gironde) at their correct relative position/scale in the same
    # normalized coordinate space, rather than forcing everything into
    # one artificially-joined outline.
    for extra in panel.get("outlines", []):
        epts = [P(p) for p in modules._chaikin(extra, panel.get("outline_smooth", 8), True)]
        d.polygon(epts, fill=(255, 255, 255), outline=core.INK)
        d.line(epts + [epts[0]], fill=core.INK, width=2, joint="curve")

    if panel.get("outline"):
        pts = [P(p) for p in modules._chaikin(panel["outline"], panel.get("outline_smooth", 8), True)]
        d.polygon(pts, fill=(255, 255, 255), outline=core.INK)
        d.line(pts + [pts[0]], fill=core.INK, width=2, joint="curve")

    # zone_fills: broad colored landmass regions (e.g. Médoc / Graves /
    # Entre-Deux-Mers / Libournais tints on a full AOC-style overview map)
    # that together tile the whole visible land -- unlike `regions` below
    # (small named appellation blobs meant to sit as an accent ON TOP of
    # an already-drawn landmass), each zone_fills piece IS a landmass
    # piece and replaces the plain white outline/outlines fill for decks
    # that want the whole map area-colored rather than white-with-blobs.
    # Drawn with a lighter, thinner border than the primary outline so
    # zone seams read as subtle, not as competing landmass edges.
    for name, zone_pts, color in panel.get("zone_fills", []):
        if not zone_pts:
            continue
        zpts = [P(p) for p in modules._chaikin(zone_pts, panel.get("outline_smooth", 8), True)]
        d.polygon(zpts, fill=color, outline=(150, 140, 130))
        d.line(zpts + [zpts[0]], fill=(150, 140, 130), width=1, joint="curve")

    RIVER_BLUE = (140, 190, 220)
    # river_polygon: a real, filled river/estuary shape (a single polygon
    # ring, or a list of rings) -- draw as solid water instead of a thin
    # traced line, for the full AOC-style overview map where the Gironde/
    # Garonne/Dordogne should read as an actual body of water, not a
    # stroke. Falls back to nothing if absent; existing single-line
    # `rivers` usage below is unaffected.
    river_poly = panel.get("river_polygon")
    if river_poly:
        rings = river_poly if isinstance(river_poly[0][0], (list, tuple)) else [river_poly]
        for ring in rings:
            rpts = [P(p) for p in modules._chaikin(ring, panel.get("outline_smooth", 8), True)]
            d.polygon(rpts, fill=RIVER_BLUE, outline=(90, 145, 180))
            d = ImageDraw.Draw(img)

    for name, region_pts, color in panel["regions"]:
        rpts = [P(p) for p in modules._chaikin(region_pts, 8, True)]
        d.polygon(rpts, fill=color, outline=core.INK)
        d.line(rpts + [rpts[0]], fill=core.INK, width=2, joint="curve")

    # River stroke scales off the map's drawn width, which is right for a
    # broad panel and wrong for a tall narrow one: the Northern Rhône is a
    # 74 x 27 km strip, so it fits its box on height and comes out ~550px
    # wide, taking this expression down to its 3px floor. On a 2160px
    # canvas that is a hairline, and the river is the only basemap feature
    # the Wine Folly treatment allows -- it cannot be the faintest mark on
    # the map. river_width overrides it outright.
    river_w = panel.get("river_width") or max(3, int(6 * w / 2000))
    for river_name, segments in panel.get("rivers", {}).items():
        for seg in segments:
            rpts = [P(p) for p in seg]
            if len(rpts) > 1:
                d.line(rpts, fill=RIVER_BLUE, width=river_w, joint="curve")

    mtf = font("caption_italic", max(24, int(38 * w / 2000)))
    for m in panel.get("mountain_labels", []):
        p_start = P((m["x"], m["y_start"]))
        p_end = P((m["x"], m["y_end"]))
        curved_text(img, p_start, p_end, m.get("bow", 40), m["text"], mtf, core.MUTED)
        d = ImageDraw.Draw(img)

    if panel.get("ocean_label"):
        ol = panel["ocean_label"]
        otf = font("caption_italic", max(20, int(32 * w / 2000)))
        p_start = P((ol["x"], ol["y_start"]))
        p_end = P((ol["x"], ol["y_end"]))
        curved_text(img, p_start, p_end, ol.get("bow", 0), ol["text"], otf, (70, 120, 165))
        d = ImageDraw.Draw(img)

    # water_labels: like ocean_label but with two freely-chosen (x, y)
    # endpoints instead of a single shared x -- ocean_label can only
    # curve along a near-vertical line (same x, different y), which
    # can't track a diagonal river/estuary. Each entry's p0/p1 are
    # sampled along the actual centerline the water was buffered from,
    # so the text follows the real length/direction of that stretch of
    # water instead of sitting at an arbitrary fixed angle.
    for wl in panel.get("water_labels", []):
        wtf = font("caption_italic", max(18, int(wl.get("size", 32) * w / 2000)))
        p_start = P(wl["p0"])
        p_end = P(wl["p1"])
        curved_text(img, p_start, p_end, wl.get("bow", 0), wl["text"], wtf, wl.get("color", (70, 120, 165)))
        d = ImageDraw.Draw(img)

    # city_emphasis: names in this set render at a larger scale (bigger dot
    # + bigger label) than the rest of the city gazetteer -- e.g. the
    # region's own capital deserves more visual weight than a small
    # reference town on the same map. Default empty set leaves every city
    # at the shared label_size*0.62, unchanged from before.
    emphasized = panel.get("city_emphasis", set())
    for name, (nx, ny) in panel.get("cities", {}).items():
        cx, cy = P((nx, ny))
        emph = name in emphasized
        r = mark_r * (1.6 if emph else 1.0)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=core.INK)
        csize = int(label_size * (1.0 if emph else 0.68))
        # Cities set in the same family as the appellation labels, one
        # step lighter and smaller. display_black here put a serif on a
        # map whose every other label is bold sans -- with only two
        # cities on the panel that reads as an oversight rather than as
        # a level in the hierarchy. Size and weight carry the
        # distinction instead of a second typeface.
        cf = font("body" if not emph else "body_bold", csize)
        d.text((cx + r + 10, cy - int(csize * 0.4)), name, font=cf, fill=core.INK)

    lf = font("body_bold", label_size)
    label_lh = int(label_size * 1.08)
    max_label_w = panel.get("max_label_w", 260)
    panel_cx = box_x0 + box_w / 2
    min_gap = max(8, int(label_size * 0.25))

    boxes = []
    left_margin_x = box_x0 + panel.get("left_margin_offset", 4)
    pinned_names = panel.get("pinned_labels", set())
    forced_side = panel.get("forced_side", {})
    for name, target in panel["labels"]:
        tx, ty = P(target)
        lines = wrap(d, name, lf, max_label_w)
        widest = max(text_w(d, ln, lf) for ln in lines)
        h_box = label_lh * len(lines)
        side = forced_side.get(name, "right" if tx >= panel_cx else "left")
        # Left-side x is ADAPTIVE per label (rule #3): end close to the
        # target, never a single fixed margin for the whole panel.
        #
        # label_column_x (optional, 0-1 of the PANEL box) overrides that
        # for maps where rule #3's premise does not hold. Rule #3 assumes
        # the map is wide enough that a label placed just outside its
        # target clears the shape. On a long narrow ribbon -- the Côte de
        # Nuits, the Northern Rhône -- the anchor sits inside a shape only
        # a few dozen px wide, so "just outside the target" lands the
        # label on top of the appellation it names, at every latitude.
        # A flush column either side of the ribbon, with real leader lines
        # back to each shape, is both legible and a truer picture: the
        # column reads as a latitude index. Right-side labels start at the
        # column; left-side labels END at its mirror, so both edges align.
        col = panel.get("label_column_x")
        if col is not None:
            col_x = box_x0 + box_w * col
            lx = col_x if side == "right" else max(box_x0 + 4,
                                                   box_x0 + box_w * (1 - col) - widest)
        else:
            lx = tx if side == "right" else max(box_x0 + 4, tx - widest - 30)
        lx = max(box_x0 + 4, min(lx, box_x0 + box_w - widest - 4))
        pinned = name in pinned_names
        if pinned:
            lx = max(box_x0 + 4, min(tx - widest / 2, box_x0 + box_w - widest - 4))
        boxes.append({"name": name, "lines": lines, "tx": tx, "ty": ty,
                      "lx": lx, "ly": (ty - h_box / 2) if pinned else 0,
                      "w": widest, "h": h_box, "side": side, "pinned": pinned})

    # Each label anchors to ITS OWN natural target position (rule #1),
    # then forward-pass collision resolution + whole-chain clamp (rule #2).
    top_margin = box_h * 0.03
    bottom_limit = box_y0 + box_h - box_h * 0.03
    placed = [b for b in boxes if b["pinned"]]
    for side in ("left", "right"):
        side_boxes = sorted([b for b in boxes if b["side"] == side and not b["pinned"]], key=lambda b: b["ty"])
        if not side_boxes:
            continue
        for b in side_boxes:
            b["ly"] = b["ty"] - b["h"] / 2
        for i in range(1, len(side_boxes)):
            prev, cur = side_boxes[i - 1], side_boxes[i]
            min_y = prev["ly"] + prev["h"] + min_gap
            if cur["ly"] < min_y:
                cur["ly"] = min_y
        overflow = (side_boxes[-1]["ly"] + side_boxes[-1]["h"]) - bottom_limit
        if overflow > 0:
            for b in side_boxes:
                b["ly"] -= overflow
        underflow = (box_y0 + top_margin) - side_boxes[0]["ly"]
        if underflow > 0:
            for b in side_boxes:
                b["ly"] += underflow
        placed.extend(side_boxes)

    # Hard safety net: clamp every label fully inside the panel
    # regardless of anything above. This can never be violated.
    for b in placed:
        b["ly"] = max(box_y0 + 2, min(b["ly"], box_y0 + box_h - b["h"] - 2))

    # Obstacle avoidance: try all four directions, take the smallest
    # move (rule #4).
    if avoid_bbox:
        ax0, ay0, ax1, ay1 = avoid_bbox
        for b in placed:
            bx0, by0, bx1, by1 = b["lx"], b["ly"], b["lx"] + b["w"], b["ly"] + b["h"]
            if not (bx1 < ax0 or ax1 < bx0 or by1 < ay0 or ay1 < by0):
                up = by1 - ay0 + 8
                down = ay1 - by0 + 8
                left = bx1 - ax0 + 8
                right = ax1 - bx0 + 8
                moves = {"up": up, "down": down}
                if b["side"] == "left":
                    moves["left"] = left
                if b["side"] == "right":
                    moves["right"] = right
                best = min(moves, key=moves.get)
                if best == "up":
                    b["ly"] = max(box_y0 + 2, b["ly"] - up)
                elif best == "down":
                    b["ly"] = min(box_y0 + box_h - b["h"] - 2, b["ly"] + down)
                elif best == "left":
                    b["lx"] = max(box_x0 + 2, b["lx"] - left)
                else:
                    b["lx"] = min(box_x0 + box_w - b["w"] - 2, b["lx"] + right)

    def _seg_x(p1, p2, p3, p4):
        def ccw(a, b, c):
            return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

    def _anchor(b):
        lcx = (left_margin_x + max_label_w) if b["side"] == "left" else b["tx"]
        return (b["tx"], b["ty"]), (lcx, b["ly"] + b["h"] / 2)

    for _ in range(20):
        conflict = False
        for i, a in enumerate(placed):
            for c in placed[i+1:]:
                if a["side"] != c["side"]:
                    continue
                la = _anchor(a); lc = _anchor(c)
                if _seg_x(la[0], la[1], lc[0], lc[1]):
                    a["ly"], c["ly"] = c["ly"], a["ly"]
                    conflict = True
        if not conflict:
            break

    # Cross-side box overlap check (rule #5) -- same-side checks above
    # never compare a left label against a right label.
    for _ in range(10):
        conflict = False
        for i, a in enumerate(placed):
            for c in placed[i+1:]:
                if a["side"] == c["side"]:
                    continue
                ax0, ax1 = a["lx"], a["lx"] + a["w"]
                cx0, cx1 = c["lx"], c["lx"] + c["w"]
                ay0, ay1 = a["ly"], a["ly"] + a["h"]
                cy0, cy1 = c["ly"], c["ly"] + c["h"]
                if ax1 < cx0 or cx1 < ax0 or ay1 < cy0 or cy1 < ay0:
                    continue
                lower = a if a["ty"] >= c["ty"] else c
                lower["ly"] += 12
                conflict = True
        if not conflict:
            break

    anchor_override = panel.get("anchor_override", {})
    for b in placed:
        if b["name"] in anchor_override:
            mode = anchor_override[b["name"]]
            if mode == "top_middle":
                lcx, lcy = b["lx"] + b["w"] / 2, b["ly"]
            else:
                lcx = b["lx"] + (b["w"] if b["side"] == "left" else 0)
                lcy = b["ly"] + b["h"] / 2
        else:
            lcx = b["lx"] + (b["w"] if b["side"] == "left" else 0)
            lcy = b["ly"] + b["h"] / 2
        if abs(lcx - b["tx"]) + abs(lcy - b["ty"]) > label_lh * 0.5:
            d.line([(b["tx"], b["ty"]), (lcx, lcy)], fill=core.MUTED, width=2)
        ty_draw = b["ly"]
        for ln in b["lines"]:
            d.text((b["lx"], ty_draw), ln, font=lf, fill=core.INK)
            ty_draw += label_lh
        qa_dummy = None  # caller's qa.box(...) calls happen at the slide-function level, not here

    return (x0, y0, w, h)


def lead_paragraph(d, xy, text, max_w, pal, lead_words=2, lead_size=150, body_size=90,
                    leading=1.28, justify=False, bold_words=None, bold_color=None, bold_serif=False,
                    bold_size=None, body_font_role="body", max_gap_mult=1.9):
    """First `lead_words` words in bold serif at lead_size (color =
    pal["LEAD"]), then the rest of the paragraph in regular body weight
    at body_size. Standard prose treatment for a description paragraph
    under a map. bold_words: optional set of words to render body_bold
    (or, with bold_serif=True, serif display_bold) within the regular-
    weight portion, optionally in bold_color and/or a distinct bold_size
    (see core.run_in). body_font_role picks the font for the non-bold
    portion (default Archivo-Medium; pass "body_regular" for true 400
    weight)."""
    words = text.split()
    lead_txt = " ".join(words[:lead_words])
    body_txt = " ".join(words[lead_words:])
    return core.run_in(d, xy, lead_txt, body_txt, max_w, pal,
                        lead_size=lead_size, body_size=body_size, leading=leading, justify=justify,
                        bold_words=bold_words, bold_color=bold_color, bold_serif=bold_serif,
                        bold_size=bold_size, body_font_role=body_font_role, max_gap_mult=max_gap_mult)


def wrapping_headline(d, text, y, fill, accent_color, size=85, x=M):
    """Like core.headline() but wraps to multiple lines instead of only
    ever shrinking font size. core.headline() (as of this same v8
    save-back) now ALSO has a wrap fallback for the case where even its
    floor size doesn't fit -- but this variant is still useful when you
    want a headline that wraps by DEFAULT at a fixed, deliberately
    modest size (e.g. a long map title) rather than only wrapping as a
    last resort after shrinking. No underline -- see the font hierarchy
    principle in DESIGN_PROCESS_v8.md: color-coded hierarchy (headline
    color vs lead-in color vs body) does the differentiation work, an
    underline is redundant decoration once that's in place.
    """
    f = font("display_black", size)
    avail_w = core.W - x - M
    lines = []
    for raw_ln in text.split("\n"):
        lines.extend(wrap(d, raw_ln, f, avail_w))
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 0.88)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def regional_atlas(slot, slide_no, total, pal):
    """Generic version of the Oregon deck's atlas slide: a main regional
    map, an optional zoomed inset with "zoomed out from here" callout
    lines back to the main map, and a description paragraph. See module
    docstring for the full panel dict schema.

    slot keys beyond the panel schema:
      kicker, headline: as usual
      main: panel dict (required)
      inset: panel dict (optional -- omit for a single-map slide)
      inset_title: str, printed above the inset frame
      inset_zoom_region: list[(x,y)] normalized polygon on the MAIN map
          that the zoom-lines anchor to (typically the same region the
          inset is a close-up of)
      inset_w, inset_map_w: inset frame width / inner map render width
      map_h: main map panel height (default 1500)
      description: paragraph under the map, rendered via lead_paragraph
    """
    img, d, qa = modules._start("regional_atlas", slide_no, total, pal)
    y = modules.kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y = wrapping_headline(d, slot["headline"], y, pal["SIGNATURE"], pal["ACCENT"])
    qa.size("!headline", 85, headline=True)
    y += 40

    map_top = y
    map_h = slot.get("map_h", 1500)
    mx0, mw = M, core.W - 2 * M

    inset = slot.get("inset")
    inset_bbox = None
    if inset:
        aspect = slot["main"]["aspect"]
        if mw / map_h > aspect:
            _h, _w = map_h, map_h * aspect
        else:
            _w, _h = mw, mw / aspect
        mx0f, my0f = mx0 + (mw - _w) / 2, map_top + (map_h - _h) / 2
        mwf, mhf = _w, _h

        inset_w = slot.get("inset_w", 620)
        inset_aspect = inset["aspect"]
        map_render_w = slot.get("inset_map_w", 520)
        inset_h = map_render_w / inset_aspect + 70
        # Default: positioned relative to the drawn map, which suits a map
        # that fills its box. A tall narrow map does not -- it leaves wide
        # empty gutters either side, and 0.44 of a 550px-wide map puts the
        # inset directly on top of the southern crus while the real free
        # space sits unused outside the map. inset_x_frac / inset_y_frac
        # reposition against the PANEL box instead, so the inset can be
        # parked in that gutter.
        if slot.get("inset_x_frac") is not None:
            inset_x = mx0 + mw * slot["inset_x_frac"]
        else:
            inset_x = mx0f + mwf * 0.44
        if slot.get("inset_y_frac") is not None:
            inset_y = map_top + map_h * slot["inset_y_frac"]
        else:
            inset_y = my0f + mhf * 0.70
        if inset_x + inset_w > mx0 + mw:
            inset_x = mx0 + mw - inset_w
        if inset_y + inset_h > map_top + map_h:
            inset_y = map_top + map_h - inset_h
        inset_bbox = (inset_x - 16, inset_y - 16, inset_x + inset_w + 16, inset_y + inset_h + 16)

    map_box = draw_map_panel(img, d, pal, slot["main"], mx0, map_top, mw, map_h,
                              label_size=slot.get("main_label_size", 42), avoid_bbox=inset_bbox)
    mx0f, my0f, mwf, mhf = map_box

    if inset:
        d.rectangle([inset_x - 16, inset_y - 16, inset_x + inset_w + 16, inset_y + inset_h + 16],
                    fill=(255, 255, 255), outline=(140, 95, 20), width=4)

        if slot.get("inset_zoom_region"):
            zoom_poly = slot["inset_zoom_region"]
            zoom_pixel = [(mx0f + px * mwf, my0f + py * mhf) for px, py in zoom_poly]
            zoom_xs = [p[0] for p in zoom_pixel]
            zx0, zx1 = min(zoom_xs), max(zoom_xs)
            # Actual polygon extreme points, not bbox corners (rule #6).
            top_pt = min(zoom_pixel, key=lambda p: p[1])
            bottom_pt = max(zoom_pixel, key=lambda p: p[1])
            zy0, zy1 = top_pt[1], bottom_pt[1]
            zoom_color = (140, 95, 20)
            d.line([top_pt, (inset_x - 16, inset_y - 16)], fill=zoom_color, width=2)
            d.line([bottom_pt, (inset_x - 16, inset_y + inset_h + 16)], fill=zoom_color, width=2)
            tick = 18
            for cx, cy in [(zx0, zy0), (zx1, zy0), (zx0, zy1), (zx1, zy1)]:
                sx = tick if cx == zx0 else -tick
                sy = tick if cy == zy0 else -tick
                d.line([(cx, cy), (cx + sx, cy)], fill=zoom_color, width=2)
                d.line([(cx, cy), (cx, cy + sy)], fill=zoom_color, width=2)

        d.rectangle([inset_x - 16, inset_y - 16, inset_x + inset_w + 16, inset_y + inset_h + 16],
                    fill=(255, 255, 255), outline=(140, 95, 20), width=4)
        if slot.get("inset_title"):
            itf = font("display_black", 46)
            d.text((inset_x, inset_y - 4), slot["inset_title"], font=itf, fill=pal["SIGNATURE"])
        draw_map_panel(img, d, pal, inset, inset_x, inset_y + 46, inset_w, inset_h - 60,
                        label_size=slot.get("inset_label_size", 28), mark_r=6)

    map_bottom = map_top + map_h

    if slot.get("legend"):
        # legend: list of (swatch_color, label) drawn as a single row of
        # swatch+label pairs under the map, centred on the panel.
        #
        # The Wine Folly treatment argues against legends, and it is right
        # when a map's colours are self-evident. This one's are not: the
        # whole point of the fill colours here is that they encode grape
        # colour rather than geography, and there is nowhere on a map of
        # eight ribbons to say so in situ without a leader line to a
        # 4 ha shape.
        lg = slot["legend"]
        lf = font("kicker_bold", slot.get("legend_size", 46))
        sw = slot.get("legend_swatch", 40)
        gap_in, gap_out = 20, 76
        widths = [sw + gap_in + core.text_w(d, lab, lf) for _c, lab in lg]
        total_w = sum(widths) + gap_out * (len(lg) - 1)
        lx = (core.W - total_w) // 2
        ly = map_bottom + 26
        la, ld = lf.getmetrics()
        for (color, label), wdt in zip(lg, widths):
            d.rectangle([lx, ly + (la - sw) // 2, lx + sw, ly + (la - sw) // 2 + sw],
                        fill=color)
            core.tracked_text(d, (lx + sw + gap_in, ly), label, lf, core.INK, tracking=4)
            lx += wdt + gap_out
        map_bottom = ly + la + ld + 18

    if slot.get("description"):
        dy = map_bottom + 50
        dy = lead_paragraph(d, (M, dy), slot["description"], core.W - 2 * M, pal,
                             lead_words=slot.get("description_lead_words", 1),
                             lead_size=slot.get("description_lead_size", 90),
                             body_size=slot.get("description_body_size", 68),
                             leading=1.0, justify=True,
                             bold_words=slot.get("description_bold_words"),
                             bold_color=slot.get("description_bold_color"),
                             bold_serif=slot.get("description_bold_serif", False),
                             bold_size=slot.get("description_bold_size"),
                             body_font_role=slot.get("description_body_font", "body"),
                             max_gap_mult=slot.get("description_max_gap_mult", 1.9))
        qa.size("!description_lead", slot.get("description_lead_size", 90))
        qa.size("!description", slot.get("description_body_size", 68))
        qa.add_words(slot["description"])

    qa.box("map", (M, map_top, core.W - M, map_bottom))
    qa.add_words(slot["headline"] + " " + " ".join(n for n, _, _ in slot["main"]["regions"]))
    return modules._finish(img, d, qa, slide_no, total)
