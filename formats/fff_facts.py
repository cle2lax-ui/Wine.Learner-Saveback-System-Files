"""
"FIVE FASCINATING FACTS ABOUT..." SERIES — MODULE LIBRARY (v2)

Fixed format, not a module-sequence deck like Field Guide: every FFFA
post is exactly 6 pages -- fff_cover() once, then fff_fact() five times
(the fifth call with closing=True to fold in the "Cheers!" sign-off on
the same page, per spec: "the sixth page should ALSO include a Cheers
salutation," not a separate 7th page).

DESIGN NORTH STAR: Massimo Vignelli. Deliberately distinct from Field
Guide (Playfair-led, red accent, editorial warmth) and Quick Sips
(gold accent, dense infographic): grotesque sans as the dominant
display face (Archivo Black, not Playfair), a single flat cobalt blue
(FFFA_ACCENT, tokens.py) against ink and paper -- neither Field Guide's
red nor Quick Sips' gold -- hard-edged flat color (no gradients, no
scrims-as-default), short accent rules instead of underlines, and one
repeating grid mark (a small blue square, same position on every page)
as the series' only "logo."

v2 changes from v1, per Steve's first-round notes:
- Signature color moved off red (collided with Field Guide) to cobalt.
- Cover is photo-only now -- no flat color block. Kicker/icon sit
  directly on the photo, in the photo's naturally dark lower zone
  (checked, not assumed -- see fff_cover docstring), same DESIGN_PROCESS
  §7 discipline as every other cover-style photo layout in this system.
- Kicker + checklist icon are both substantially larger and the icon
  itself is a more distinctive mark (a numbered badge stands in for the
  checklist's first row, tying the glyph directly to "five" rather than
  reading as a generic to-do icon).
- fff_fact() gained an optional diagram="bottle_sizes" slot for a slide
  that needs to show scale rather than just state it (Fact 2,
  large-format bottles) -- draws a small graduated silhouette row from
  primitives, same "data claims should be visible in form" principle
  documented in DESIGN_PROCESS_v8.md section 3, since no stock photo
  actually shows five bottle formats side by side at true relative
  scale.

Checklist icon is drawn programmatically, not sourced as an asset, so
it never drifts off-brand and never needs an external SVG dependency.
"""
from PIL import ImageDraw
from tokens import *
import core
from core import (new_canvas, footer, font, text_w, tracked_text, wrap,
                   load_photo, cover_fit, QA, contrast, region_luminance)


def _start(name, slide_no, total):
    img = new_canvas()
    d = ImageDraw.Draw(img)
    qa = QA(f"{name} #{slide_no}")
    return img, d, qa


def _finish(img, d, qa, slide_no, total, credit=None, footer_fill=None, swipe_label=None):
    label_kwargs = {} if swipe_label is None else {"label": swipe_label}
    footer(d, slide_no, total, credit=credit, fill=footer_fill, **label_kwargs)
    print(qa.report(img))
    return img


def _grid_mark(d, x, y, size, color):
    """The series' one repeating brand device: a small flat cobalt
    square, same relative position on every page, top-right of
    whatever photo is on that page. Vignelli-style consistent grid
    mark, not a logo."""
    d.rectangle([x, y, x + size, y + size], fill=color)


def _checklist_icon(d, x, y, size, color, badge_color=None, stroke=None):
    """Line-art checklist, distinctive version: rounded-square frame +
    three rows. Row 1 is a filled numeral badge ("5") standing in for
    a checkmark -- ties the icon directly to "Five Fascinating Facts"
    instead of reading as a generic to-do glyph. Rows 2-3 are ordinary
    check+line rows. Drawn from primitives so it's exactly reproducible
    on every future FFFA deck regardless of topic."""
    badge_color = badge_color or color
    stroke = stroke or max(int(size * 0.045), 6)
    r = int(size * 0.14)
    d.rounded_rectangle([x, y, x + size, y + size], radius=r, outline=color, width=stroke)
    pad = int(size * 0.15)
    row_h = (size - 2 * pad) / 3

    ry0 = y + pad
    badge_d = row_h * 0.78
    bx0 = x + pad
    by0 = ry0 + (row_h - badge_d) / 2
    d.ellipse([bx0, by0, bx0 + badge_d, by0 + badge_d], fill=badge_color)
    bf = font("sans_black", int(badge_d * 0.66))
    btxt = "5"
    bb = d.textbbox((0, 0), btxt, font=bf)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    d.text((bx0 + (badge_d - bw) / 2 - bb[0], by0 + (badge_d - bh) / 2 - bb[1]), btxt, font=bf, fill=INK)
    line_x0 = bx0 + badge_d + pad * 0.7
    line_x1 = x + size - pad
    d.line([(line_x0, ry0 + row_h / 2), (line_x1, ry0 + row_h / 2)], fill=color, width=max(stroke - 2, 4))

    for i in (1, 2):
        ry = y + pad + row_h * (i + 0.5)
        cm_x = x + pad
        cm_size = row_h * 0.5
        d.line([(cm_x, ry), (cm_x + cm_size * 0.36, ry + cm_size * 0.38),
                (cm_x + cm_size, ry - cm_size * 0.42)],
               fill=color, width=max(stroke - 2, 5), joint="curve")
        lx0 = cm_x + cm_size + pad * 0.7
        d.line([(lx0, ry), (line_x1, ry)], fill=color, width=max(stroke - 3, 4))


def _sweetness_glyph(d, cx, base_y, height, color, label, sub, lf, slf):
    """One bar in the sweetness-scale diagram: a simple flat bar,
    bottom-anchored at base_y, scaled to `height` px tall. Bars (not
    bottle silhouettes) are the right shape for an abstract dosage
    scale rather than a physical object."""
    w = 96
    x0, x1 = cx - w / 2, cx + w / 2
    d.rectangle([x0, base_y - height, x1, base_y], fill=color)
    lb = d.textbbox((0, 0), label, font=lf)
    lw = lb[2] - lb[0]
    # allow a second line if the (condensed) label is wider than the slot
    if lw > 210:
        parts = label.split(" ")
        if len(parts) > 1:
            mid = len(parts) // 2
            line1, line2 = " ".join(parts[:mid]), " ".join(parts[mid:])
        else:
            line1, line2 = label, ""
        for j, ln in enumerate((line1, line2)):
            if not ln:
                continue
            b = d.textbbox((0, 0), ln, font=lf)
            d.text((cx - (b[2] - b[0]) / 2, base_y + 20 + j * (b[3] - b[1] + 6)), ln, font=lf, fill=PAPER)
        label_h = 2 * (lb[3] - lb[1] + 6)
    else:
        d.text((cx - lw / 2, base_y + 20), label, font=lf, fill=PAPER)
        label_h = (lb[3] - lb[1]) + 6
    sb = d.textbbox((0, 0), sub, font=slf)
    d.text((cx - (sb[2] - sb[0]) / 2, base_y + 20 + label_h + 4), sub, font=slf, fill=(150, 148, 150))


def _sweetness_diagram(d, x0, x1, base_y, max_px=210):
    """The seven EU-defined Champagne dosage levels, Brut Nature through
    Doux, drawn at relative bar height by representative g/L of residual
    sugar -- the scale itself is the fascinating fact, so it needs to be
    seen, not just named. Returns the diagram's top y."""
    levels = [
        ("Brut Nature", "0–3 g/L", 3),
        ("Extra Brut", "0–6 g/L", 6),
        ("Brut", "0–12 g/L", 12),
        ("Extra Sec", "12–17 g/L", 17),
        ("Sec", "17–32 g/L", 32),
        ("Demi-Sec", "32–50 g/L", 50),
        ("Doux", "50+ g/L", 60),
    ]
    max_val = max(v[2] for v in levels)
    # Font floor for any chart/diagram label, this series and any future
    # FFFA deck: 35px minimum, never smaller even at the tightest slot
    # width -- legibility on a phone screen matters more than fitting a
    # few more columns.
    lf = font("kicker_bold", 36)
    slf = font("body", 35)
    n = len(levels)
    slot_w = (x1 - x0) / n
    top_y = base_y
    for i, (name, sub, val) in enumerate(levels):
        cx = x0 + slot_w * (i + 0.5)
        h = max(val / max_val * max_px, 20)
        _sweetness_glyph(d, cx, base_y, h, FFFA_ACCENT, name, sub, lf, slf)
        top_y = min(top_y, base_y - h)
    return top_y


def _bottle_glyph(d, cx, base_y, height, color, label, sub, lf, slf):
    """One silhouette in the bottle-scale diagram: body + shoulder +
    neck, bottom-anchored at base_y, scaled to `height` px tall. Width
    scales with height so larger formats read as proportionally
    fatter, not just taller."""
    w = max(height * 0.34, 14)
    neck_w = w * 0.34
    neck_h = height * 0.22
    shoulder_h = height * 0.14
    x0, x1 = cx - w / 2, cx + w / 2
    nx0, nx1 = cx - neck_w / 2, cx + neck_w / 2
    body_top = base_y - height + neck_h + shoulder_h
    shoulder_top = base_y - height + neck_h
    neck_top = base_y - height
    pts = [
        (nx0, neck_top), (nx1, neck_top), (nx1, shoulder_top),
        (x1, body_top), (x1, base_y), (x0, base_y),
        (x0, body_top), (nx0, shoulder_top),
    ]
    d.polygon(pts, fill=color)
    lb = d.textbbox((0, 0), label, font=lf)
    d.text((cx - (lb[2] - lb[0]) / 2, base_y + 22), label, font=lf, fill=PAPER)
    sb = d.textbbox((0, 0), sub, font=slf)
    d.text((cx - (sb[2] - sb[0]) / 2, base_y + 22 + (lb[3] - lb[1]) + 8), sub, font=slf, fill=(150, 148, 150))


def _parentage_diagram(d, x0, x1, top_y, parent_a, parent_b, child, avail_h=280):
    """Simple genealogy diagram: two parent chips joined by "x", an
    arrow down to a child chip. Same "show the claim, don't just state
    it" principle as the bottle/sweetness diagrams, for a relational
    claim rather than a scalar one -- flat cobalt chips, paper text,
    no photo could show a cross like this. Returns the diagram's
    bottom y (for QA box registration)."""
    chip_h = min(int(avail_h * 0.34), 110)
    gap_y = int(avail_h * 0.18)
    pf = font("kicker_bold", 40)
    cf = font("kicker_bold", 44)
    xf = font("sans_black", 46)

    chip_w = (x1 - x0 - 90) / 2
    ax0, ax1 = x0, x0 + chip_w
    bx0, bx1 = x1 - chip_w, x1

    def _chip(cx0, cx1, cy0, cy1, label):
        d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=14, fill=FFFA_ACCENT)
        lb = d.textbbox((0, 0), label, font=pf)
        lw, lh = lb[2] - lb[0], lb[3] - lb[1]
        d.text(((cx0 + cx1) / 2 - lw / 2 - lb[0], (cy0 + cy1) / 2 - lh / 2 - lb[1]), label, font=pf, fill=PAPER)

    row1_y0, row1_y1 = top_y, top_y + chip_h
    _chip(ax0, ax1, row1_y0, row1_y1, parent_a)
    _chip(bx0, bx1, row1_y0, row1_y1, parent_b)

    xtxt = "×"
    xb = d.textbbox((0, 0), xtxt, font=xf)
    xw, xh = xb[2] - xb[0], xb[3] - xb[1]
    xc = (ax1 + bx0) / 2
    d.text((xc - xw / 2 - xb[0], (row1_y0 + row1_y1) / 2 - xh / 2 - xb[1]), xtxt, font=xf, fill=PAPER)

    arrow_top = row1_y1 + int(gap_y * 0.25)
    arrow_bottom = row1_y1 + gap_y
    d.line([(xc, arrow_top), (xc, arrow_bottom)], fill=FFFA_ACCENT, width=6)
    d.polygon([(xc - 16, arrow_bottom - 4), (xc + 16, arrow_bottom - 4), (xc, arrow_bottom + 20)], fill=FFFA_ACCENT)

    row2_y0 = arrow_bottom + 24
    row2_y1 = row2_y0 + chip_h
    child_w = chip_w * 1.15
    ccx0, ccx1 = xc - child_w / 2, xc + child_w / 2
    d.rounded_rectangle([ccx0, row2_y0, ccx1, row2_y1], radius=14, fill=FFFA_ACCENT)
    lb = d.textbbox((0, 0), child, font=cf)
    lw, lh = lb[2] - lb[0], lb[3] - lb[1]
    d.text((xc - lw / 2 - lb[0], (row2_y0 + row2_y1) / 2 - lh / 2 - lb[1]), child, font=cf, fill=PAPER)

    return row2_y1


def _bottle_size_diagram(d, x0, x1, base_y, max_px=210):
    """The five canonical Champagne bottle formats, drawn at true
    relative height (approximate real-world bottle heights, cm) so the
    claim "every big bottle has a royal name" is visible in form, not
    just stated -- no stock photo actually shows this comparison at
    once. Returns the diagram's top y (for QA box registration)."""
    sizes = [
        ("Standard", "750 ml", 30),
        ("Magnum", "1.5 L", 35),
        ("Jeroboam", "3 L", 45),
        ("Methuselah", "6 L", 60),
        ("Nebuchadnezzar", "15 L", 90),
    ]
    max_cm = max(s[2] for s in sizes)
    # Same 35px chart-label floor as the sweetness diagram.
    lf = font("kicker_bold", 38)
    slf = font("body", 36)
    n = len(sizes)
    slot_w = (x1 - x0) / n
    top_y = base_y
    for i, (name, vol, cm) in enumerate(sizes):
        cx = x0 + slot_w * (i + 0.5)
        h = cm / max_cm * max_px
        _bottle_glyph(d, cx, base_y, h, FFFA_ACCENT, name, vol, lf, slf)
        top_y = min(top_y, base_y - h)
    return top_y


# ────────────────────────── FFFA COVER ──────────────────────────
def fff_cover(slot, total=FFFA_SLIDE_COUNT, headline_color=None):
    """slots: photo, subject (e.g. 'Champagne'), photo_anchor, photo_zoom,
    photo_credit.

    Photo-only cover (v2) -- no flat color block behind the type. Text
    sits directly on the photo's own dark lower zone. Per DESIGN_PROCESS
    section 7, that's a per-photo judgment call, not a system default:
    this function measures the actual rendered brightness under the
    text zone and only adds a scrim if the photo is too bright there
    for white text to sit cleanly."""
    img, d, qa = _start("FFFA cover", 1, total)
    hcolor = headline_color or FFFA_YELLOW
    anchor = slot.get("photo_anchor", 0.5)
    zoom = slot.get("photo_zoom", 1.0)
    photo = cover_fit(load_photo(slot["photo"]), W, H, y_anchor=anchor, zoom=zoom)
    img.paste(photo, (0, 0))

    _grid_mark(d, W - M - 64, 120, 64, FFFA_ACCENT)

    kicker_size = 130
    kf = font("sans_cond_black", kicker_size)
    kasc, kdesc = kf.getmetrics()
    klh = int((kasc + kdesc) * 1.02)
    k_total_h = klh * 2  # "FIVE FASCINATING" / "FACTS ABOUT"

    icon_size = k_total_h  # match the icon to the now-larger kicker block
    icon_x = M
    title_size_guess = TYPE["display_xl"] - 10
    text_block_h = icon_size + 70 + int(title_size_guess * 1.05) + 70
    text_top = H - 260 - text_block_h

    check_region = region_luminance(img, (M - 20, text_top - 40, W - M, H - 60))
    needs_scrim = check_region > 90
    if needs_scrim:
        core.chip(img, (0, text_top - 60, W, H), INK, opacity=0.55)
        d = ImageDraw.Draw(img)

    icon_y = text_top
    _checklist_icon(d, icon_x, icon_y, icon_size, PAPER, badge_color=FFFA_ACCENT)

    qa.size("kicker", kicker_size)
    kx = icon_x + icon_size + 44
    ktxt = "FIVE FASCINATING\nFACTS ABOUT"
    klines = ktxt.split("\n")
    ky = icon_y + (icon_size - k_total_h) // 2
    kyy = ky
    for ln in klines:
        tracked_text(d, (kx, kyy), ln, kf, PAPER, tracking=4)
        kyy += klh
    qa.box("kicker", (kx, ky, W - M, kyy))

    rule_y = icon_y + icon_size + 56
    d.line([(M, rule_y), (M + 320, rule_y)], fill=FFFA_ACCENT, width=7)

    title = slot["subject"]
    tf = font("display_black", title_size_guess)
    size = title_size_guess
    while text_w(d, title, tf) > W - 2 * M and size > TYPE["display_md"]:
        size -= 4
        tf = font("display_black", size)
    qa.size("title", size, headline=True)
    ty = rule_y + 54
    d.text((M, ty), title, font=tf, fill=hcolor)
    tb = d.textbbox((M, ty), title, font=tf)
    qa.box("title", (M, ty, tb[2], tb[3]))
    qa.add_words(title + " " + ktxt.replace("\n", " "))

    return _finish(img, d, qa, 1, total, credit=slot.get("photo_credit"), footer_fill=PAPER)


# ────────────────────────── FFFA FACT ──────────────────────────
def fff_fact(slot, slide_no, total=FFFA_SLIDE_COUNT, closing=False, diagram=None, headline_color=None):
    """slots: photo, number(1-5), headline, body(15-20 words),
    photo_anchor, photo_zoom, photo_credit. closing=True on the last
    call folds "Cheers!" into this same page. diagram="bottle_sizes"
    adds the graduated bottle-format silhouette row instead of leaving
    the scale claim as text alone -- shrinks the photo band and the
    numeral to buy the extra vertical room the row needs, since that's
    still less intrusive than crowding the diagram against the footer."""
    img, d, qa = _start("FFFA fact", slide_no, total)
    hcolor = headline_color or FFFA_YELLOW
    photo_h = 1200 if diagram else 1450
    anchor = slot.get("photo_anchor", 0.5)
    zoom = slot.get("photo_zoom", 1.0)
    img.paste(cover_fit(load_photo(slot["photo"]), W, photo_h, y_anchor=anchor, zoom=zoom), (0, 0))

    _grid_mark(d, W - M - 64, 90, 64, FFFA_ACCENT)
    if closing and slot.get("photo_credit"):
        # "Cheers!" is allowed to drift down into the footer row on this
        # page, so its credit moves up here (small print under the grid
        # mark) instead of colliding with the bigger sign-off word.
        crf = font("body", 34)
        ctxt = slot["photo_credit"]
        cw = text_w(d, ctxt, crf)
        cy = 90 + 64 + 16
        # PAPER-on-photo with nothing behind it. On any closing photo
        # with a bright top-right corner -- sky, most of the time -- the
        # credit rendered white on near-white and effectively vanished,
        # which is a licence-attribution failure, not a styling one.
        # Sample what is actually there and either chip behind the white
        # or drop to INK, the same adaptive approach the reveal caption
        # in guess_the_region already uses.
        cbox = (W - M - cw - 16, cy - 10, W - M + 8, cy + 46)
        if region_luminance(img, cbox) > 150:
            d.text((W - M - cw, cy), ctxt, font=crf, fill=INK)
        else:
            d.text((W - M - cw, cy), ctxt, font=crf, fill=PAPER)

    block_top = photo_h
    d.rectangle([0, block_top, W, H], fill=INK)

    num_size = 150 if diagram else 200
    nf = font("sans_black", num_size)
    qa.size("!numeral", num_size)
    num_txt = f"0{slot['number']}"
    ny = block_top + 70

    # Small checklist icon (same mark as the cover, scaled down) to the
    # left of every fact number -- ties every page back to the cover's
    # branding instead of just the numeral standing alone. Aligned to
    # the numeral's actual glyph top (measured via textbbox), not the
    # font's nominal line-box top, since Archivo Black's ascent leaves
    # visible padding above the digits themselves.
    icon_size_small = int(num_size * 0.72)
    num_bbox_probe = d.textbbox((M, ny), num_txt, font=nf)
    glyph_top = num_bbox_probe[1]
    icon_y = glyph_top
    _checklist_icon(d, M, icon_y, icon_size_small, PAPER, badge_color=FFFA_ACCENT)
    qa.box("!numeral_icon", (M, icon_y, M + icon_size_small, icon_y + icon_size_small))

    num_x = M + icon_size_small + 28
    d.text((num_x, ny), num_txt, font=nf, fill=FFFA_ACCENT)
    nb = d.textbbox((num_x, ny), num_txt, font=nf)
    qa.box("!numeral", (num_x, ny, nb[2], nb[3]))

    rule_y = max(nb[3], icon_y + icon_size_small) + 36
    d.line([(M, rule_y), (M + 140, rule_y)], fill=FFFA_ACCENT, width=6)

    hf = font("display_black", TYPE["display_md"])
    qa.size("headline", TYPE["display_md"], headline=True)
    hy = rule_y + 46
    lines = wrap(d, slot["headline"], hf, W - 2 * M)
    asc, desc = hf.getmetrics()
    lh = int((asc + desc) * 1.06)
    for ln in lines:
        d.text((M, hy), ln, font=hf, fill=hcolor)
        hy += lh
    qa.box("headline", (M, rule_y + 46, W - M, hy))
    qa.add_words(slot["headline"])
    qa.check_contrast(hcolor, INK, large=True, label="headline")

    bf = font("body", TYPE["body"])
    qa.size("body", TYPE["body"])
    by = hy + 20
    blines = wrap(d, slot["body"], bf, W - 2 * M)
    basc, bdesc = bf.getmetrics()
    blh = int((basc + bdesc) * 1.30)
    body_bottom = by
    for ln in blines:
        d.text((M, by), ln, font=bf, fill=(214, 208, 200))
        by += blh
        body_bottom = by
    qa.box("body", (M, hy + 20, W - M, body_bottom))
    qa.add_words(slot["body"])
    qa.check_contrast((214, 208, 200), INK, label="body")

    tail_top = body_bottom + 40
    diagram_bottom = tail_top
    if diagram == "bottle_sizes":
        label_h = 108
        max_px = max(min(230, CONTENT_BOTTOM - label_h - tail_top), 90)
        base_y = tail_top + max_px
        diag_top = _bottle_size_diagram(d, M, W - M, base_y, max_px=max_px)
        qa.box("!diagram", (M, diag_top, W - M, base_y + label_h))
        diagram_bottom = base_y + label_h
    elif diagram == "sweetness":
        label_h = 112
        # tighter budget when this slide also closes the deck -- the
        # "Cheers!" sign-off still needs real room below the chart.
        cap = 150 if closing else 230
        max_px = max(min(cap, CONTENT_BOTTOM - label_h - tail_top), 80)
        base_y = tail_top + max_px
        diag_top = _sweetness_diagram(d, M, W - M, base_y, max_px=max_px)
        qa.box("!diagram", (M, diag_top, W - M, base_y + label_h))
        diagram_bottom = base_y + label_h
    elif diagram == "parentage":
        avail_h = max(min(300, CONTENT_BOTTOM - tail_top - 20), 200)
        diag_bottom = _parentage_diagram(
            d, M, W - M, tail_top,
            slot.get("parent_a", "Parent A"), slot.get("parent_b", "Parent B"),
            slot.get("child", "Child"), avail_h=avail_h)
        qa.box("!diagram", (M, tail_top, W - M, diag_bottom))
        diagram_bottom = diag_bottom

    if closing:
        cheers_size = 230
        cf = font("display_black", cheers_size)
        qa.size("!cheers", cheers_size)
        cy = diagram_bottom - 10
        d.line([(M, cy), (M + 140, cy)], fill=FFFA_ACCENT, width=6)
        cy += 40
        d.text((M, cy), "Cheers", font=cf, fill=hcolor)
        word_b = d.textbbox((M, cy), "Cheers", font=cf)
        d.text((word_b[2], cy), "!", font=cf, fill=FFFA_ACCENT)
        cb = d.textbbox((M, cy), "Cheers!", font=cf)
        qa.box("!cheers", (M, cy, cb[2], cb[3]))
        qa.add_words("Cheers!")

    return _finish(img, d, qa, slide_no, total,
                    credit=None if closing else slot.get("photo_credit"),
                    footer_fill=PAPER, swipe_label="" if closing else None)
