"""FIELD GUIDE — The Mosel. "Ripeness Was the Law"

REBUILT after a container reset wiped the original local-only build
(never pushed to GitHub -- see the recovery conversation for the full
account). This version is built from specs/FG_MOSEL_SPEC.md, a
complete 12-slide spec that the first build never found and had to
crudely reconstruct from the arc plan and caption alone. The spec is
followed closely; deviations are noted at each slide, and are almost
all about matching real content to the modules actually available in
engine/modules.py (a few module names in the spec, e.g. "spectrum",
don't exist -- editorial_lead substitutes throughout, since it
supports the same photo + kicker + headline + standfirst + items shape
every substituted slide needs).

Separately, Steve provided a detailed article on Germany's 2026 origin-
law reform and asked that the deck reflect it. This turned out to be
less of a bolt-on than expected: the spec's OWN slide 12 already
anticipated the reform in outline ("Grosslage is gone, replaced by
Region"), written before the June 2026 Bundesrat session that actually
implemented it. This version updates slide 12 with that session's
specifics (12 June 2026, the Komitee, classification still in
progress) verified independently against multiple sources (Deutsches
Weininstitut, Jancis Robinson, Wine Scholar Guild) before being written
in, and carries the same "Region, not Grosslage" correction into slide
10, which is where the deck actually explains the naming problem the
reform fixes.

Per Steve's separate design feedback: the cover is a custom full-bleed
treatment (see render_cover()) rather than the spec's original
grid_cover (a 9-photo grid this project doesn't have material for
regardless), and the map (slide 3) uses map_atlas.regional_atlas with
a Germany-wide locator inset showing all 13 Anbaugebiete -- the spec
already called for this inset; it directly satisfies Steve's separate
request to rework the map to show Germany's wine regions.

SOURCES: every claim traces to D3 Ch. 11, per the spec's own header,
except where the spec itself flags a gap (Mosel hectarage, the export
price in currency, the Sonnenuhr sundials, Scharzhofberg as a village-
prefix exception, "Mosel-Saar-Ruwer" as a former name -- none of these
appear here) and except the 2026 reform content, sourced and dated as
described above and in each affected slide's own comment.

PHOTOGRAPHY remains a real, disclosed constraint: three photos exist
for this arc (de_hatzenport_mosel.jpg, de_bernkastel_castle_view.jpg,
de_piesport_goldtropfchen_sign.jpg), reused across every slide that
needs a photo band. See MAP module's own docstring for the map's
sourcing; the spec's suggested 9-photo cover grid and per-slide photo
suggestions (budburst, a Fuder cask, a winch rail) were never
achievable with this library and are not attempted.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "engine"))
import core
import modules
import map_atlas
import prepare_map_data as pmd
from core import cover_fit, load_photo, font, footer as core_footer
from tokens import W, H, M, PAPER

OUT = "/home/claude/out_fg_mosel"
os.makedirs(OUT, exist_ok=True)

PAL = dict(
    SIGNATURE=(45, 58, 74),   # Mosel slate-blue
    ACCENT=(196, 158, 84),    # house gold, locked across every arc
    LEAD=(140, 95, 58),       # warm sienna run-in, distinct from both
    MARK=(45, 58, 74),
)

CRED_HATZENPORT = "Rolf Kranz / Wikimedia Commons (CC BY-SA 4.0)"
CRED_BERNKASTEL = "Roger W / Wikimedia Commons (CC BY-SA 2.0)"
CRED_PIESPORT = "J\u00e1nos Korom Dr. / Wikimedia Commons (CC BY-SA 2.0)"

MAP = pmd.build_main_map()
INSET = pmd.build_locator_inset()

# ---------------------------------------------------------------------
# Custom full-bleed cover. See module docstring for why this isn't the
# shared statement()'s "cover" variant (a hard color block under the
# photo, not full-bleed) or the spec's grid_cover (needs 9 photos this
# project doesn't have).
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# Deck-local renderers. Steve's second review asked for layouts the
# shared modules don't offer (a vertical blade layout, a numbered
# staircase ladder with the lowest tier at the bottom, a sweetness-
# scale graphic, a data graphic on the Mosel slide, a full 13-region
# map). Each lives here, scoped to this deck, rather than as edits to
# engine/modules.py -- promote one to the shared module set only once
# a second deck needs it.
# ---------------------------------------------------------------------
from core import kicker_block, paragraph, run_in, standfirst, text_w, wrap, photo_band
from tokens import CONTENT_BOTTOM, TYPE, INK, MUTED, LINE, FLOOR

REGIONS13 = pmd.build_anbaugebiete_map()


def _blend(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


# Chart palette. Round 3 first made the charts vivid (Steve: "more
# color"); round 3b re-based them on the cover photo (Steve: "match the
# colors in the cover photo"). Every colour below is sampled from the
# cover's own crop by sample_cover_palette.py -- the most saturated,
# mid-light pixels of a named feature -- not picked by eye:
#   vineyard gold (sunlit slope under the castle)   (201, 151, 3)
#   leaf yellow   (autumn leaves)                   (171, 142, 3)
#   lamp orange   (lamp reflections in the river)   (242, 145, 4)
#   window orange (lit windows along the quay)      (203, 114, 12)
#   brick red     (roofs)                           (179, 80, 63)
#   forest green  (the hillside)                    (50, 62, 25)
#   water teal    (the river, in shade)             (18, 32, 30)
#   sky           (top of frame)                    (225, 244, 248)
# Two values are NOT single-feature samples: `stone` is the cover's
# warm stone/plaster grey, taken from the 5th-largest k-means cluster of
# the whole crop (98, 91, 74), and `track` its pale sibling (203, 194,
# 165), another cluster. The ripeness ramp runs forest -> gold -> orange
# -> deep orange -> brick, i.e. the cover's own greens, golds and
# russets in the order grapes move through them.
CHART = dict(
    ripe=[(50, 62, 25), (201, 151, 3), (242, 145, 4), (203, 114, 12), (179, 80, 63)],
    mosel=(18, 32, 30),        # water: "this is the Mosel"
    amber=(242, 145, 4),       # lamp orange
    gold=(201, 151, 3),        # vineyard gold
    grape=(171, 142, 3),       # leaf yellow: white-grape share
    stone=(98, 91, 74),
    ice=(18, 32, 30),          # Eiswein outline/connector/title: water teal
    ice_fill=(225, 244, 248),  # Eiswein box fill: the cover's sky
    ice_text=(18, 32, 30),
    track=(203, 194, 165),
)


def _best_text(bg):
    """PAPER or INK, whichever has the higher real (WCAG) contrast on bg."""
    return PAPER if core.contrast(PAPER, bg) >= core.contrast(INK, bg) else INK


def _one_line_headline(d, text, y, pal, size=TYPE["display_md"], x=M, max_w=None):
    """Single-line headline -- Steve's standing ask on this deck is that
    titles don't wrap. Shrinks to fit the measure rather than breaking,
    never below the hierarchy floor; raises if it still can't fit, so a
    too-long title fails loudly instead of silently wrapping."""
    max_w = max_w or (W - x - M)
    floor = TYPE["standfirst"] + 30
    f = font("display_black", size)
    while text_w(d, text, f) > max_w and size > floor:
        size -= 2
        f = font("display_black", size)
    if text_w(d, text, f) > max_w:
        raise ValueError(f"headline won't fit on one line: {text!r}")
    d.text((x, y), text, font=f, fill=pal["SIGNATURE"])
    a, dsc = f.getmetrics()
    return y + int((a + dsc) * 1.02), size


def render_cover(slot, slide_no, total, pal):
    """Full-bleed photo, no scrim. Round-2 changes per Steve: no shadow
    under the kicker (flat type, dot kept), and the title lowered so it
    sits in the dark water of the river rather than over the town --
    the water is the one reliably dark field in this photo, so the
    title reads without any shadow help there either; the soft shadow
    on the title is kept only as insurance at its lighter upper edge."""
    img = cover_fit(load_photo(slot["photo"]), W, H,
                    y_anchor=slot.get("photo_anchor", 0.5),
                    zoom=slot.get("photo_zoom", 1.0))
    d = ImageDraw.Draw(img, "RGBA")

    kicker_size = 68
    kf = font("kicker_bold", kicker_size)
    dot_r = int(kicker_size * 0.19)
    ky = 120
    dot_cy = ky + int(kicker_size * 0.42)
    d.ellipse([M, dot_cy - dot_r, M + 2 * dot_r, dot_cy + dot_r], fill=pal["ACCENT"])
    d.text((M + 2 * dot_r + 20, ky), slot["kicker"], font=kf, fill=pal["ACCENT"])

    tf = font("display_black", 300)
    asc, desc = tf.getmetrics()
    line_h = int((asc + desc) * 0.88)
    ty = int(H * slot.get("title_top", 0.60))
    for ln in slot["title"].split("\n"):
        tb = d.textbbox((0, 0), ln, font=tf)
        pad = 45
        layer = Image.new("RGBA", (tb[2] + pad * 2, tb[3] + pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((pad, pad), ln, font=tf, fill=(0, 0, 0, 150))
        layer = layer.filter(ImageFilter.GaussianBlur(16))
        img.paste(layer, (M - pad + 4, ty - pad + 8), layer)
        d.text((M, ty), ln, font=tf, fill=PAPER)
        ty += line_h
    core_footer(d, slide_no, total, credit=slot.get("photo_credit"), img=img)
    return img


def render_region_map(slot, slide_no, total, pal):
    """Standard wine-region map: all 13 Anbaugebiete as real traced
    shapes on the full Germany outline, Mosel in SIGNATURE, the other
    twelve in a pale ACCENT tint (source + georeferencing error: see
    prepare_map_data.build_anbaugebiete_map and anbaugebiete.geojson).

    Labels are placed here, not by map_atlas's automatic placer. That
    algorithm is built for one region's sub-areas; on a national map
    with eight regions packed along the Rhine it put labels over
    Germany's own western edge and over each other, and ran Franken's
    label up the page on a long leader (checked in a render, not
    assumed). Instead: the map sits right-aligned, the nine western and
    south-western regions get a clean left-hand column with elbow
    leader lines, and the four isolated eastern regions are labelled
    directly beside their own shapes."""
    img, d, qa = modules._start("map13", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y, hs = _one_line_headline(d, slot["headline"], y, pal); qa.size("headline", hs, headline=True)
    m = REGIONS13
    pale = _blend(pal["ACCENT"], (255, 255, 255), 0.45)
    regions = [(n, pts, pal["SIGNATURE"] if n == "Mosel" else pale) for n, pts in m["regions"]]
    panel = dict(aspect=m["aspect"], outline=m["outline"], outlines=m["islands"],
                 regions=regions, rivers=m["rivers"], river_width=3, labels=[],
                 outline_smooth=2, map_align="right")
    map_top = y + 20
    map_h = slot.get("map_h", 1500)
    mx0, my0, mw, mh = map_atlas.draw_map_panel(img, d, pal, panel, M, map_top, W - 2 * M, map_h)
    d = ImageDraw.Draw(img)
    P = lambda p: (mx0 + p[0] * mw, my0 + p[1] * mh)
    lf = font("body_bold", FLOOR); mf = font("display_black", 76)
    qa.size("map_label", FLOOR)
    a, dsc = lf.getmetrics(); lh = a + dsc

    def dot(x, y_, col):
        d.ellipse([x - 9, y_ - 9, x + 9, y_ + 9], fill=col, outline=PAPER, width=3)

    # Left column: right-aligned at a fixed edge just outside the map.
    col_x = mx0 - 40
    left = [n for n in slot["left_labels"]]
    items = sorted(((n, P(m["targets"][n])) for n in left), key=lambda t: t[1][1])
    gap = 22
    rows, prev = [], None
    for n, (tx, ty) in items:
        f = mf if n == "Mosel" else lf
        fa, fd = f.getmetrics(); h = fa + fd
        ly = ty - h / 2
        if prev is not None and ly < prev + gap:
            ly = prev + gap
        rows.append((n, tx, ty, ly, h, f)); prev = ly + h
    # Chain clamp (same rule as map_atlas #2): if the forward push ran
    # the column past the map's bottom, lift the whole column by the
    # overflow rather than clamping one label onto its neighbour.
    over = prev - (my0 + mh)
    if over > 0:
        rows = [(n, tx, ty, ly - over, h, f) for n, tx, ty, ly, h, f in rows]
    for n, tx, ty, ly, h, f in rows:
        col = pal["SIGNATURE"]
        tw = text_w(d, n, f)
        d.text((col_x - tw, ly), n, font=f, fill=col if n == "Mosel" else INK)
        mid = ly + h / 2 + 4
        ex = col_x + 24
        d.line([(col_x + 10, mid), (ex, mid), (tx, ty)], fill=MUTED, width=3)
        dot(tx, ty, col)
        qa.box(f"lbl:{n}", (col_x - tw, ly, col_x, ly + h))
    # Direct labels for the isolated eastern regions: (dx, dy) offset
    # from the target in px, chosen against a render.
    for n, (dx, dy) in slot["direct_labels"].items():
        tx, ty = P(m["targets"][n])
        dot(tx, ty, pal["SIGNATURE"])
        d.text((tx + dx, ty + dy), n, font=lf, fill=INK)
        qa.box(f"lbl:{n}", (tx + dx, ty + dy, tx + dx + text_w(d, n, lf), ty + dy + lh))
    # No qa.box for the map itself: its bounding rectangle is mostly
    # empty space, and the direct labels sit inside it by design.
    ty = map_top + map_h + 50
    end = run_in(d, (M, ty), slot["summary_lead"], slot["summary"], W - 2 * M, pal)
    qa.box("summary", (M, ty, W - M, end)); qa.size("summary", TYPE["body"])
    qa.add_words(slot["summary"])
    return modules._finish(img, d, qa, slide_no, total, credit=slot.get("credit"))


def render_blades(slot, slide_no, total, pal):
    """Vertical blade layout: three tall, narrow photo strips side by
    side across the top of the page, separated by thin paper gutters,
    each with its own caption tab; text runs full-width beneath. The
    middle blade drops lower than the outer two so the row reads as a
    stepped composition rather than a flat three-up grid."""
    img, d, qa = modules._start("blades", slide_no, total, pal)
    blades = slot["blades"]
    gut = 18
    bw = (W - gut * (len(blades) - 1)) // len(blades)
    base_h = slot.get("blade_h", 1250)
    drops = slot.get("blade_drop", [0, 110, 0])
    cf = font("kicker_bold", FLOOR)
    for i, b in enumerate(blades):
        x0 = i * (bw + gut)
        h = base_h + drops[i]
        im = cover_fit(load_photo(b["photo"]), bw, h, y_anchor=b.get("anchor", 0.5),
                       zoom=b.get("zoom", 1.0))
        img.paste(im, (x0, 0))
        d = ImageDraw.Draw(img)
        tw = text_w(d, b["caption"], cf)
        d.rectangle([x0, h - 96, x0 + tw + 60, h], fill=INK)
        d.text((x0 + 30, h - 86), b["caption"], font=cf, fill=PAPER)
    qa.size("caption", FLOOR)
    y = base_h + max(drops) + 70
    y = kicker_block(d, slot["kicker"], pal, y=y); qa.size("kicker", 70)
    y, hs = _one_line_headline(d, slot["headline"], y, pal); qa.size("headline", hs, headline=True)
    y += 40
    for lead, body in slot["items"]:
        y0 = y
        y = run_in(d, (M, y), lead, body, W - 2 * M, pal) + slot.get("item_gap", 50)
        qa.box(f"runin:{lead}", (M, y0, W - M, y - slot.get("item_gap", 50)))
        qa.add_words(body)
    return modules._finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


def render_stair_ladder(slot, slide_no, total, pal):
    """Numbered staircase: rung 1 (Kabinett) at the BOTTOM of the page,
    rung 5 (TBA) at the top -- ripeness climbs the page, per Steve.
    Treads are right-aligned and shorten as they rise, so the whole
    graphic reads as a literal staircase. Eiswein is deliberately NOT a
    numbered rung: it shares Beerenauslese's minimum must weight and is
    defined by a harvest condition (frozen on the vine), so it sits in a
    dashed box beside rung 4 -- a parallel track, per the D3 framing and
    the DWI-based article Steve supplied, not a sixth step."""
    img, d, qa = modules._start("stair_ladder", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y, hs = _one_line_headline(d, slot["headline"], y, pal); qa.size("headline", hs, headline=True)
    y = standfirst(d, (M, y + 8), slot["standfirst"], W - 2 * M, leading=1.14) + 50
    qa.size("standfirst", TYPE["standfirst"])
    rungs = slot["rungs"]  # listed bottom (1) to top (n)
    n = len(rungs)
    zone_top, zone_bot = y, CONTENT_BOTTOM - 20
    gap = 26
    step_h = (zone_bot - zone_top - gap * (n - 1)) // n
    dx = slot.get("step_dx", 230)
    nf = font("display_black", 96); lf = font("display_bold", 78); bf = font("body", FLOOR + 4)
    qa.size("rung_name", 78); qa.size("rung_note", FLOOR + 4)
    rung_boxes = []
    for i, (name, note) in enumerate(rungs):
        t = i / max(n - 1, 1)
        color = CHART["ripe"][i] if n == len(CHART["ripe"]) else _blend(CHART["ripe"][0], CHART["ripe"][-1], t)
        x0 = M + i * dx
        y1 = zone_bot - i * (step_h + gap)
        y0 = y1 - step_h
        d.rounded_rectangle([x0, y0, W - M, y1], radius=14, fill=color)
        fg = _best_text(color)
        badge_r = 62
        bcx, bcy = x0 + 40 + badge_r, (y0 + y1) // 2
        d.ellipse([bcx - badge_r, bcy - badge_r, bcx + badge_r, bcy + badge_r], fill=pal["SIGNATURE"])
        num = str(i + 1)
        nw = text_w(d, num, nf); na, nd = nf.getmetrics()
        d.text((bcx - nw / 2, bcy - (na + nd) / 2 + 4), num, font=nf, fill=PAPER)
        tx = bcx + badge_r + 40
        d.text((tx, y0 + 26), name, font=lf, fill=fg)
        paragraph(d, (tx, y0 + 26 + 100), note, bf, fg, W - M - tx - 30, 1.16)
        qa.add_words(note)
        rung_boxes.append((x0, y0, W - M, y1))
    qa.box("ladder", (M, zone_top, W - M, zone_bot))
    if slot.get("side_note"):
        # Box spans the height of its own rung AND the one above -- the
        # first render sized it to one rung and the note overflowed it.
        bi = slot["side_note"]["beside"]
        rx0, ry0, rx1, ry1 = rung_boxes[bi]
        top = rung_boxes[bi + 1][1] if bi + 1 < len(rung_boxes) else ry0
        bx0, bx1 = M, rx0 - 60
        d.rounded_rectangle([bx0, top, bx1, ry1], radius=14, fill=CHART["ice_fill"], outline=CHART["ice"], width=6)
        ry0 = top
        cy = (rung_boxes[bi][1] + ry1) // 2
        for xx in range(bx1, rx0, 22):
            d.line([(xx, cy), (min(xx + 11, rx0), cy)], fill=CHART["ice"], width=6)
        sn = slot["side_note"]
        d.text((bx0 + 36, ry0 + 26), sn["title"], font=lf, fill=CHART["ice_text"])
        paragraph(d, (bx0 + 36, ry0 + 126), sn["note"], bf, INK, bx1 - bx0 - 64, 1.16)
        qa.add_words(sn["note"])
    return modules._finish(img, d, qa, slide_no, total)


def _hatch(d, box, color, step=26, width=4):
    x0, y0, x1, y1 = box
    for k in range(int(x0 - (y1 - y0)), int(x1), step):
        a = (max(k, x0), y1 - max(0, max(k, x0) - k))
        b = (min(k + (y1 - y0), x1), y1 - (min(k + (y1 - y0), x1) - k))
        d.line([a, b], fill=color, width=width)


def render_dry_scale(slot, slide_no, total, pal):
    """Two data graphics in place of a run-in list, per Steve's ask for a
    more visually impactful page 7: (1) the legal residual-sugar bands
    for trocken and halbtrocken on one g/L axis -- solid for the base
    limit, hatched for the acid-dependent extension -- and (2) the 2021
    share of wine labelled trocken, Baden vs Germany vs the Mosel. Every
    number is from D3 Ch. 11; nothing is interpolated beyond what the
    chapter states (Germany's share is drawn at 49% and labelled "just
    under half," the chapter's own wording, not a precise figure)."""
    img, d, qa = modules._start("dry_scale", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y, hs = _one_line_headline(d, slot["headline"], y, pal); qa.size("headline", hs, headline=True)
    y = standfirst(d, (M, y + 8), slot["standfirst"], W - 2 * M, leading=1.14) + 90
    qa.size("standfirst", TYPE["standfirst"]); qa.add_words(slot["standfirst"])

    capf = font("kicker_bold", FLOOR); lf = font("display_bold", 76); tick = font("body_bold", FLOOR)
    qa.size("chart_label", FLOOR)
    d.text((M, y), "RESIDUAL SUGAR, GRAMS PER LITRE", font=capf, fill=MUTED)
    y += 100
    x_label_w = 520
    ax0, ax1, gmax = M + x_label_w, W - M, 20
    X = lambda g: ax0 + (ax1 - ax0) * g / gmax
    row_h, row_gap = 190, 60
    halb = CHART["amber"]
    rows = [("trocken", CHART["mosel"], 0, 4, 9), ("halbtrocken", halb, 4, 12, 18)]
    for name, col, g0, gbase, gext in rows:
        d.text((M, y + 30), name, font=lf, fill=INK)
        d.rectangle([X(g0), y, X(gbase), y + row_h], fill=col)
        d.rectangle([X(gbase), y, X(gext), y + row_h], outline=col, width=5)
        _hatch(d, (X(gbase), y, X(gext), y + row_h), col)
        y += row_h + row_gap
    ay = y - row_gap + 20
    d.line([(ax0, ay), (ax1, ay)], fill=INK, width=3)
    for g in (0, 4, 9, 12, 18):
        d.line([(X(g), ay), (X(g), ay + 20)], fill=INK, width=3)
        tw = text_w(d, str(g), tick)
        d.text((X(g) - tw / 2, ay + 28), str(g), font=tick, fill=INK)
    y = ay + 120
    kf = font("body", FLOOR)
    d.rectangle([M, y + 8, M + 70, y + 58], fill=INK)
    d.text((M + 90, y), "base limit", font=kf, fill=INK)
    hx = M + 90 + text_w(d, "base limit", kf) + 80
    d.rectangle([hx, y + 8, hx + 70, y + 58], outline=INK, width=4)
    _hatch(d, (hx, y + 8, hx + 70, y + 58), INK, step=16, width=3)
    d.text((hx + 90, y), "allowed only if sugar doesn't outrun acid", font=kf, fill=INK)
    qa.box("scale", (M, ay - 2 * (row_h + row_gap), W - M, y + 70))
    y += 190

    d.text((M, y), "SHARE OF WINE LABELLED TROCKEN, 2021", font=capf, fill=MUTED)
    y += 100
    bars = slot["shares"]
    bh, bg = 180, 56
    big = font("display_black", 120)
    qa.size("share_value", 120, headline=True)
    for name, pct, shown, is_focus in bars:
        col = CHART["mosel"] if is_focus else {"Baden": CHART["amber"]}.get(name, CHART["gold"])
        d.text((M, y + 30), name, font=lf, fill=INK)
        d.rectangle([ax0, y, ax0 + (ax1 - ax0 - 380) * pct / 100, y + bh], fill=col)
        vx = ax0 + (ax1 - ax0 - 380) * pct / 100 + 30
        d.text((vx, y + 2), shown, font=big if is_focus else lf, fill=CHART["mosel"] if is_focus else INK)
        y += bh + bg
    qa.box("shares", (M, y - len(bars) * (bh + bg), W - M, y - bg))
    return modules._finish(img, d, qa, slide_no, total)


def _donut(img, cx, cy, r, thick, pct, color, track, ss=3):
    lay = Image.new("RGBA", (2 * r * ss, 2 * r * ss), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    R = r * ss
    ld.ellipse([0, 0, 2 * R, 2 * R], fill=track + (255,))
    ld.pieslice([0, 0, 2 * R, 2 * R], -90, -90 + 360 * pct / 100, fill=color + (255,))
    t = thick * ss
    ld.ellipse([t, t, 2 * R - t, 2 * R - t], fill=(0, 0, 0, 0))
    lay = lay.resize((2 * r, 2 * r), Image.LANCZOS)
    img.paste(lay, (cx - r, cy - r), lay)


def render_valley_stats(slot, slide_no, total, pal):
    """Side-rail layout (photo right, full height) with a data graphic
    added per Steve's ask: two ring charts -- share of the Mosel planted
    to white varieties (91%) and to Riesling alone (62%), both from D3
    Ch. 11 -- replacing the standfirst that previously stated those two
    numbers in a sentence."""
    img, d, qa = modules._start("valley_stats", slide_no, total, pal)
    rail_x = slot.get("rail_x", 1420)
    img.paste(cover_fit(load_photo(slot["photo"]), W - rail_x, H, y_anchor=slot.get("anchor", 0.5)), (rail_x, 0))
    d = ImageDraw.Draw(img)
    col_w = rail_x - M - 90
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    hf = font("display_black", TYPE["display_md"])
    for ln in slot["headline"].split("\n"):
        d.text((M, y), ln, font=hf, fill=pal["SIGNATURE"])
        a, dsc = hf.getmetrics(); y += int((a + dsc) * 1.02)
    qa.size("headline", TYPE["display_md"], headline=True)
    y += 60
    r, thick = 250, 70
    track = CHART["track"]
    big = font("display_black", 120); cap = font("kicker_bold", FLOOR)
    qa.size("ring_value", 120, headline=True); qa.size("ring_label", FLOOR)
    for i, (pct, label, col) in enumerate(slot["rings"]):
        cx = M + r + i * (col_w // 2 + 20)
        cy = y + r
        _donut(img, cx, cy, r, thick, pct, CHART[col], track)
        d = ImageDraw.Draw(img)
        txt = f"{pct}%"
        tw = text_w(d, txt, big); a, dsc = big.getmetrics()
        d.text((cx - tw / 2, cy - (a + dsc) / 2 + 6), txt, font=big, fill=pal["SIGNATURE"])
        lw = text_w(d, label, cap)
        d.text((cx - lw / 2, cy + r + 30), label, font=cap, fill=MUTED)
    y += 2 * r + 150
    for lead, body in slot["items"]:
        y0 = y
        y = run_in(d, (M, y), lead, body, col_w, pal) + 50
        qa.box(f"runin:{lead}", (M, y0, M + col_w, y - 50))
        qa.add_words(body)
    # Caption tab carries the photo credit as a second line: the footer
    # centres credits on the page, and on this layout that centre point
    # falls on the photo rail, clipping the credit (seen in a render).
    cap_txt = slot.get("photo_caption")
    if cap_txt:
        crf = font("body", 34)
        cr = slot.get("photo_credit", "")
        cw = max(text_w(d, cap_txt, cap), text_w(d, cr, crf))
        d.rectangle([W - cw - 60, H - 370, W, H - 234], fill=INK)
        d.text((W - cw - 30, H - 360), cap_txt, font=cap, fill=PAPER)
        d.text((W - cw - 30, H - 285), cr, font=crf, fill=PAPER)
    return modules._finish(img, d, qa, slide_no, total, footer_adaptive=True)


def render_hero_facts(slot, slide_no, total, pal):
    """Photo-led layout for page 11, per Steve: a tall hero (well over
    half the page) of the subject itself, with the text reduced to a
    kicker, a one-line headline and a compact 2x2 fact grid underneath.
    No scrim or overlay on the photo -- the caption sits in its own
    solid tab so the image stays untouched."""
    img, d, qa = modules._start("hero_facts", slide_no, total, pal)
    hero_h = slot.get("hero_h", 1500)
    img.paste(cover_fit(load_photo(slot["photo"]), W, hero_h,
                        y_anchor=slot.get("anchor", 0.5), zoom=slot.get("zoom", 1.0)), (0, 0))
    d = ImageDraw.Draw(img)
    cf = font("kicker_bold", FLOOR)
    if slot.get("photo_caption"):
        tw = text_w(d, slot["photo_caption"], cf)
        d.rectangle([0, hero_h - 96, M + tw + 50, hero_h], fill=INK)
        d.text((M, hero_h - 86), slot["photo_caption"], font=cf, fill=PAPER)
    qa.size("caption", FLOOR)
    y = kicker_block(d, slot["kicker"], pal, y=hero_h + 60); qa.size("kicker", 70)
    y, hs = _one_line_headline(d, slot["headline"], y, pal); qa.size("headline", hs, headline=True)
    y += 40
    gut = 80
    col_w = (W - 2 * M - gut) // 2
    lf = font("display_bold", 72); bf = font("body", FLOOR + 4)
    qa.size("fact_label", 72); qa.size("fact_body", FLOOR + 4)
    facts = slot["facts"]
    row_y = y
    for r in range(0, len(facts), 2):
        bottoms = []
        for c, (label, body) in enumerate(facts[r:r + 2]):
            x = M + c * (col_w + gut)
            d.line([(x, row_y), (x + col_w, row_y)], fill=pal["ACCENT"], width=4)
            d.text((x, row_y + 22), label, font=lf, fill=pal["SIGNATURE"])
            bottoms.append(paragraph(d, (x, row_y + 122), body, bf, INK, col_w, 1.18))
            qa.add_words(body)
        row_y = max(bottoms) + 50
    qa.box("facts", (M, y, W - M, row_y - 50))
    return modules._finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


def render_four_tiles(slot, slide_no, total, pal):
    """Page 4, round 2: four solid tiles filling the whole content area
    in a 2x2 checkerboard (slate / pale gold), each carrying a large
    numeral, a title, a gold sub-line and the body. The shared
    card_grid() leaves its cards floating in open paper, which is what
    read as flat in the first pass of this revision."""
    img, d, qa = modules._start("four_tiles", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y, hs = _one_line_headline(d, slot["headline"], y, pal); qa.size("headline", hs, headline=True)
    y = standfirst(d, (M, y + 8), slot["standfirst"], W - 2 * M, leading=1.14) + 60
    qa.size("standfirst", TYPE["standfirst"]); qa.add_words(slot["standfirst"])
    gut = 30
    tw_ = (W - 2 * M - gut) // 2
    th_ = (CONTENT_BOTTOM - 20 - y - gut) // 2
    pale = _blend(pal["ACCENT"], (255, 255, 255), 0.62)
    nf = font("display_black", 160); tf = font("display_bold", 80)
    sf = font("kicker_bold", FLOOR + 4); bf = font("body", 66)
    qa.size("tile_title", 80); qa.size("tile_sub", FLOOR + 4); qa.size("tile_body", 66)
    for k, (title, sub, body) in enumerate(slot["tiles"]):
        c, rr = k % 2, k // 2
        x0 = M + c * (tw_ + gut); y0 = y + rr * (th_ + gut)
        # Round 3 (Steve: more color): each tile takes the colour of its
        # own subject from CHART -- river blue, sun gold, slate charcoal,
        # autumn orange -- instead of the slate/pale-gold checkerboard.
        # Body text colour picked by measured contrast.
        fill, accent = slot["tile_colors"][k] if slot.get("tile_colors") else (
            (pal["SIGNATURE"], pal["ACCENT"]) if (c + rr) % 2 == 0 else (pale, pal["LEAD"]))
        fg = _best_text(fill)
        d.rounded_rectangle([x0, y0, x0 + tw_, y0 + th_], radius=18, fill=fill)
        pad = 60
        d.text((x0 + pad, y0 + 30), f"0{k + 1}", font=nf, fill=accent)
        ty = y0 + 250
        d.text((x0 + pad, ty), title, font=tf, fill=fg); ty += 110
        d.text((x0 + pad, ty), sub.upper(), font=sf, fill=accent); ty += 100
        end = paragraph(d, (x0 + pad, ty), body, bf, fg, tw_ - 2 * pad, 1.2)
        qa.box(f"tile{k}", (x0, y0, x0 + tw_, max(end, y0 + th_)))
        qa.add_words(body)
    return modules._finish(img, d, qa, slide_no, total)


RENDERERS = dict(cover=render_cover, map13=render_region_map, blades=render_blades,
                 stair_ladder=render_stair_ladder, dry_scale=render_dry_scale,
                 valley_stats=render_valley_stats,
                 hero_facts=render_hero_facts,
                 four_tiles=render_four_tiles)

SLIDES = [

    # ── 1 · COVER ──────────────────────────────────────────────────
    ("cover", dict(
        photo="de_cochem_mosel",
        # zoom + low anchor: the source is landscape, so without a zoom
        # there's no vertical slack to move; this brings more of the
        # dark river into frame so the whole title can sit on water.
        photo_anchor=0.80,
        photo_zoom=1.12,
        kicker="THE FIELD GUIDE: THE MOSEL",
        title="Ripeness is\nEverything",
        title_top=0.655,  # round 2: lowered fully into the dark water of the river
        photo_credit="Philipp / Unsplash",
    )),

    # ── 2 · TWO GERMANYS ─────────────────────────────────────────────
    # Round 2: single-line headline (was a 2-line "The Same Country /
    # Sold Both of These"); the reclaimed line goes back as white space
    # between the standfirst and the items and between each item.
    ("editorial_lead", dict(
        # Round 3: replaced the old Bernkastel photo, a scan of an aged
        # film slide with a heavy cyan cast (mean blue exceeded red by
        # ~97 levels; saturation ~2x a normal photo). This one measures
        # neutral and is ~6x the resolution.
        photo="de_bernkastel_aerial",
        photo_caption="The Mosel at Bernkastel",
        photo_credit="sajid shiper / Pexels",
        kicker="THE REPUTATION PROBLEM",
        headline="Two Germanys",
        standfirst="Germany is the world's largest producer of Riesling, "
                   "and the country most people still associate with "
                   "sugared brand wine. Both are true.",
        standfirst_gap=110,
        item_gap=110,
        items=[
            ("Riesling", "Nearly a quarter of German plantings -- close "
                          "to 40% of the world's Riesling vineyard area."),
            ("Liebfraumilch", "By the 1980s, roughly 60% of all German "
                               "wine exports, under brands like Black "
                               "Tower and Blue Nun."),
            ("The fall, and the fix", "Export volume has nearly halved "
                                       "since, while price per hectolitre "
                                       "has risen by about half again."),
        ],
    )),

    # ── 3 · THE MAP ──────────────────────────────────────────────────
    # Round 2: a standard wine-region map of all 13 Anbaugebiete (real
    # traced shapes, georeferenced -- see render_region_map()), and the
    # text is now a summary of what makes the Mosel special rather than
    # a caption for the village map this slide used to carry. Every
    # clause traces to D3 Ch. 11 via the spec's slides 4 and 8.
    ("map13", dict(
        kicker="THE PLACE",
        headline="Thirteen Regions. One Mosel.",
        map_h=1590,
        summary_lead="Why it stands apart",
        summary="Riesling on slopes up to 70%, above a looping river at "
                "50\u00b0N. Slate stores the day's heat, and the wines come "
                "out paler, lighter and higher in acid than any other "
                "German Riesling.",
        left_labels=["Ahr", "Mittelrhein", "Mosel", "Rheingau", "Nahe",
                     "Rheinhessen", "Hessische Bergstra\u00dfe", "Pfalz", "Baden"],
        direct_labels={"Saale-Unstrut": (-190, -95), "Sachsen": (20, 18),
                       "Franken": (30, -80), "W\u00fcrttemberg": (40, 10)},
        credit="Region shapes after Wikimedia Commons, CC BY-SA 3.0",
    )),

    # ── 4 · WHY ANYONE FARMS A CLIFF ──────────────────────────────────
    # Round 2: four cards, one per corrective, instead of a photo band +
    # run-in list; single-line headline.
    ("four_tiles", dict(
        kicker="THE SLOPE",
        # (fill, accent for numeral + sub-line), in tile order
        tile_colors=[(CHART["mosel"], CHART["gold"]),       # The River: the water
                     (CHART["gold"], CHART["mosel"]),         # The Aspect: sunlit vineyard (water-teal accent; brick measured 1.9:1)
                     (CHART["stone"], CHART["track"]),       # The Slate: the cover's stone (plaster-cream accent; amber measured 2.8:1)
                     (CHART["ripe"][3], (50, 22, 8))],       # The Autumn: window orange
        headline="Four Fixes for Latitude",
        standfirst="The Mosel sits near 50\u00b0N, far enough north that "
                   "ripening Riesling takes help from the land.",
        tiles=[
            ("The River", "Warmth by reflection",
             "Radiates heat, moderates temperature and stretches the "
             "growing season."),
            ("The Aspect", "Face the sun",
             "The best sites are steep and south-facing -- gradients "
             "reach 70%."),
            ("The Slate", "A storage heater",
             "Dark rock takes heat in by day and gives it back at night."),
            ("The Autumn", "Time on the vine",
             "Long and dry, which lets sugar keep building before "
             "harvest."),
        ],
    )),

    # ── 5 · THE COST OF THE CORRECTION ────────────────────────────────
    # Round 2: vertical blade layout; photos of people working steep
    # slopes. The two worker photos carry no location data (Pexels has
    # none), so their captions describe the work, not a place; only the
    # Bremm blade names a location, per its photographer's own title.
    ("blades", dict(
        blades=[
            dict(photo="de_steep_stairs_climber", caption="Stairs, not rows", anchor=0.45),
            dict(photo="de_harvest_pickers_slope", caption="Picked by hand", anchor=0.40),
            dict(photo="de_bremm_mosel_loop", caption="The Mosel at Bremm", anchor=0.5, zoom=1.0),
        ],
        blade_h=1180,
        kicker="THE LABOR",
        headline="The Price of a Cliff",
        items=[
            ("Erosion", "Constant enough that winching soil back up the "
                         "slope is routine maintenance, not an emergency."),
            ("Spraying", "Often only practicable by helicopter -- which "
                          "also makes organic certification hard."),
            ("The blunt version", "On these slopes, often only Riesling "
                                   "commands a price that makes the "
                                   "farming pay."),
        ],
        photo_credit="Peter Dyllong, Nico Becker, tom analogicus / Pexels",
    )),

    # ── 6 · THE LADDER ───────────────────────────────────────────────
    # Round 2: numbered, lowest ripeness at the bottom of the page.
    ("stair_ladder", dict(
        kicker="THE RIPENESS LADDER",
        headline="Five Rungs. None Means Sweet.",
        standfirst="Pr\u00e4dikat levels climb by must weight -- sugar in the "
                   "grape at harvest, not sugar in the bottle.",
        rungs=[
            ("Kabinett", "Lightest, highest in acid. Dry to medium-sweet."),
            ("Sp\u00e4tlese", "\"Late picked\" -- riper, fuller."),
            ("Auslese", "Extra-ripe bunches. The last level that can "
                        "still be dry."),
            ("Beerenauslese", "Selected berries. Always sweet."),
            ("TBA", "Shrivelled, botrytised berries. Germany's rarest."),
        ],
        side_note=dict(beside=3, title="Eiswein",
                       note="Same must weight as BA -- but frozen on the "
                            "vine. A parallel track, not a rung."),
    )),

    # ── 7 · DRY IS A MEASUREMENT ─────────────────────────────────────
    # Round 2: two data graphics replace the run-in list.
    ("dry_scale", dict(
        kicker="THE WORD ON THE LABEL",
        headline="Dry Is a Measurement",
        standfirst="Below Beerenauslese, any Pr\u00e4dikat can be made at "
                   "any sweetness. The label terms are numbers.",
        shares=[
            ("Baden", 64, "64%", False),
            ("Germany", 49, "Just under half", False),
            ("Mosel", 26, "26%", True),
        ],
    )),

    # ── 8 · THE MOSEL ─────────────────────────────────────────────────
    # Round 2: ring-chart graphic added (91% white, 62% Riesling).
    ("valley_stats", dict(
        photo="de_hatzenport_mosel",
        anchor=0.5,
        photo_caption="The Mosel at Hatzenport",
        photo_credit="Rolf Kranz / Commons, CC BY-SA 4.0",
        kicker="THE MAIN VALLEY",
        headline="Pale, Light,\nBuilt to\nOutlive You",
        rings=[(91, "WHITE GRAPES", "grape"), (62, "RIESLING", "amber")],
        items=[
            ("In the glass", "Paler, lighter, lower in alcohol and higher "
                              "in acid than German Riesling from anywhere "
                              "else."),
            ("Village first", "Bernkastel (Doctor), Piesport "
                               "(Goldtr\u00f6pfchen), \u00dcrzig "
                               "(W\u00fcrzgarten)."),
        ],
    )),


    # ── 9 · THE SAAR AND THE RUWER ─────────────────────────────────────
    # Round 3: new photo with people, per Steve (Febe Vanermen / Unsplash,
    # Unsplash location data: Bernkastel-Kues). Searched Pexels, Unsplash
    # and Commons for people in the Saar or Ruwer themselves first; the
    # real Saar/Ruwer photos found (Kanzem vineyards and cycle path,
    # the Scharzhofberg panorama, the Ruwer-Hochwald cycle path at Kasel)
    # had nobody in them. So this is honest Middle Mosel, captioned as
    # Bernkastel, not passed off as a tributary.
    # Layout moved from side_rail to a wide top band: side_rail centre-
    # crops a narrow 860px strip, and in this photo the vineyard slope is
    # on the left and the couple on the right -- no narrow slice holds
    # both. The wide band keeps them together and frees the headline to
    # run on one line.
    ("editorial_lead", dict(
        photo="de_bernkastel_bridge_couple",
        band_h=1060,
        photo_caption="Bernkastel, Middle Mosel",
        photo_credit="Febe Vanermen / Unsplash",
        kicker="THE TRIBUTARIES",
        headline="Colder Water, Higher Acid",
        standfirst="The Saar and the Ruwer join the Mosel near Trier, "
                   "inside the same Anbaugebiet. Neither tastes like the "
                   "main valley.",
        items=[
            ("The sites that matter", "Sheltered side valleys facing "
                                       "south, south-east or south-west."),
            ("Why they're different", "Slightly higher and cooler than "
                                       "the Middle Mosel -- and acidity "
                                       "can run higher still."),
            ("The name to know", "Scharzhofberg, on the Saar."),
        ],
    )),

    # ── 10 · TWO WINES CALLED PIESPORTER ──────────────────────────────
    # Round 3: photo added, per Steve -- the actual Piesporter
    # Goldtropfchen sign standing in the vines, as a bottom stripe (pages
    # 9 and 11 both lead with top photos; this varies the rhythm).
    # Also fixes a silent drop found this round: card_grid() has no
    # footnote support, so the Grosslage-vs-Grosse-Lage footnote this
    # slide carried never rendered. It's now a third card, so it renders
    # and runs through QA. The distinction is one the 2026 origin-reform
    # article singles out as routinely examined and got wrong.
    ("card_grid", dict(
        kicker="THE LABEL TRAP",
        headline="Same Village. Not the Same Wine.",
        standfirst="Under the 1971 law, every vineyard was registered as "
                   "an Einzellage or a Grosslage -- and both could say "
                   "\"Piesporter.\"",
        row_layout=[3],
        cards=[
            (None, "Einzellage", "2,658 sites",
             "One real vineyard, under 1 ha to over 200. Piesport's is "
             "Goldtr\u00f6pfchen."),
            (None, "Grosslage \u2192 Region", "167 zones",
             "600-1,800 ha. Piesport's is Michelsberg. From 2026 it must "
             "say Region."),
            (None, "Grosse Lage", "Not the same thing",
             "The VDP's own top-site tier -- one letter from Grosslage, "
             "opposite in meaning."),
        ],
        bottom_stripe=["de_piesport_goldtropfchen_sign"],
        stripe_captions=["Piesporter Goldtr\u00f6pfchen, in the vines", ""],
        photo_credit=CRED_PIESPORT,
    )),

    # ── 11 · EISWEIN ──────────────────────────────────────────────────
    # Round 2: photo-led layout with a hero of frozen white grapes still
    # on the vine (Ivonne Arceo / Pexels -- no location data, so the
    # caption describes the subject, not a place). The bird netting
    # visible behind the cluster is standard practice for fruit left
    # hanging into winter, which ties to the "real gamble" fact below.
    ("hero_facts", dict(
        photo="de_eiswein_frozen_cluster",
        anchor=0.38,
        hero_h=1340,
        photo_caption="Frozen on the vine",
        photo_credit="Ivonne Arceo / Pexels",
        kicker="THE RUNG THAT ISN'T ABOUT SUGAR",
        headline="Defined by Temperature",
        facts=[
            ("Since 1982", "Eiswein has been its own Pr\u00e4dikat since "
                           "this year."),
            ("Same must weight as BA", "A parallel track to "
                                        "Beerenauslese, not a step "
                                        "above it."),
            ("Below \u20137\u00b0C", "Picked frozen solid and pressed "
                                  "while still frozen."),
            ("A real gamble", "Waiting for the freeze often costs part "
                              "of the crop to rot or birds."),
        ],
    )),

    # ── 12 · CLOSE ────────────────────────────────────────────────────
    # Substantially updated from the spec's own version, which was
    # written before the reform's implementing decision. Verified
    # independently (Deutsches Weininstitut, Wine Scholar Guild, Jancis
    # Robinson) before adding the June 2026 specifics: the Bundesrat
    # session date, the Komitee, and the "still in progress" caveat --
    # the actual site classification isn't finished, and the deck
    # shouldn't imply otherwise.
    ("statement", dict(
        # variant="closing" is documented in statement()'s own docstring
        # ("cover and closing are a genuine bookend... sharing the same
        # block/dot/kicker system") but isn't actually implemented --
        # the function's if/elif chain only branches on "cover" and
        # "quote"; "closing" matches neither and silently produced a
        # broken layout (identical overflow numbers no matter how much
        # the subtitle text was trimmed, which is what exposed this --
        # a real text-length problem would have responded to trimming).
        # "cover" is the correct value for this closing bookend slide
        # too, confirmed by testing directly rather than guessing.
        variant="cover",
        photo="de_hatzenport_mosel",
        photo_anchor=0.35,
        title="The Law Changed\nIts Mind in 2026",
        # Round 2: trimmed for brevity, and the Saturday teaser removed --
        # the series is dropping to 2-3 posts a week, so the close no
        # longer promises a specific next post.
        subtitle="Since June 2026, Grosses Gew\u00e4chs has national legal "
                 "standing. Which sites qualify is still being decided.",
        photo_credit=CRED_HATZENPORT,
    )),
]


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    paths = []
    total = len(SLIDES)
    for i, (name, slot) in enumerate(SLIDES, start=1):
        if name in RENDERERS:
            fn = RENDERERS[name]
        elif name == "regional_atlas":
            fn = map_atlas.regional_atlas
        else:
            fn = modules.MODULES[name]
        img = fn(slot, i, total, PAL)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  {name}")
    pdf = f"{OUT}/FG_Mosel_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
