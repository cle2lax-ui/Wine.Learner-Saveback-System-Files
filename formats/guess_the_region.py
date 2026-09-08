"""
GUESS THE WINE REGION — MODULE LIBRARY
2-page format, quiz-card register: page 1 is a full-bleed photo with a
headline, four clue lines, and a swipe cue; page 2 reveals the region
name over a 2/3-photo, 1/3-white split. Shares canvas, safe zones, and
QA harness with Field Guide / Quick Sips (tokens.py, core.py) but is
its own visual system.

    gtr_cover   page 1: full-bleed photo, "Guess the Wine Region"
                header + folded-map glyph, four clues, swipe cue
    gtr_reveal  page 2: 2/3 photo, 1/3 white reveal panel with region name
"""
import math
import os
from PIL import Image, ImageDraw, ImageStat
from tokens import *
from core import (font, text_w, tracked_text, wrap, load_photo, cover_fit,
                   scrim, chip, footer as core_footer, QA, region_luminance)
from modules import _start, _finish

SERIES_GOLD = (196, 158, 84)   # contrasting swipe-cue / accent color, fixed per series


def _lum_of(c):
    r, g, b = c
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _region_luminance(img, box):
    """Thin wrapper kept for call-site stability -- the implementation
    now lives in core.region_luminance() so modules.py's side_rail()
    can share it too (see core.py for the full docstring)."""
    return region_luminance(img, box)


# ------------------------------------------------------------- glyph ---
def _french_flag(img, x, y, height, width=None):
    """Simple flat French tricolor -- three vertical bands, no border,
    drawn fresh rather than loaded from an asset. width defaults to the
    standard 3:2 flag ratio."""
    if width is None:
        width = int(height * 1.5)
    d = ImageDraw.Draw(img)
    band_w = width / 3
    blue = (0, 85, 164)
    white = (255, 255, 255)
    red = (239, 65, 53)
    d.rectangle([x, y, x + band_w, y + height], fill=blue)
    d.rectangle([x + band_w, y, x + 2 * band_w, y + height], fill=white)
    d.rectangle([x + 2 * band_w, y, x + width, y + height], fill=red)
    return width, height

def _italian_flag(img, x, y, height, width=None):
    """Flat Italian tricolor -- same three-vertical-band construction as
    _french_flag, different colors/order (green, white, red)."""
    if width is None:
        width = int(height * 1.5)
    d = ImageDraw.Draw(img)
    band_w = width / 3
    green = (0, 146, 70)
    white = (255, 255, 255)
    red = (206, 43, 55)
    d.rectangle([x, y, x + band_w, y + height], fill=green)
    d.rectangle([x + band_w, y, x + 2 * band_w, y + height], fill=white)
    d.rectangle([x + 2 * band_w, y, x + width, y + height], fill=red)
    return width, height

def _image_flag(path):
    """Factory for a flag drawn from an actual flag image asset rather
    than a hand-built vector tricolor -- for flags too complex for the
    simple three-band construction (e.g. NZ's Union Jack + Southern
    Cross). Returns a function matching the _french_flag/_italian_flag
    signature so it drops straight into _FLAGS. Resizes with LANCZOS
    and pastes via alpha if the source has an alpha channel."""
    def _draw(img, x, y, height, width=None):
        if width is None:
            width = int(height * 1.5)
        flag_img = Image.open(path).convert("RGBA")
        flag_img = flag_img.resize((width, height), Image.LANCZOS)
        img.paste(flag_img, (int(x), int(y)), flag_img)
        return width, height
    return _draw


_NZ_FLAG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "flags", "nz.png")

_FLAGS = {"french": _french_flag, "italian": _italian_flag, "nz": _image_flag(_NZ_FLAG_PATH)}


# ------------------------------------------------------------- glyph ---
def _folded_map_icon_bbox(size):
    """Pure geometry calc (no drawing) so callers can center the icon
    against other elements before it's actually drawn."""
    w = size
    thickness = w * 0.59
    amp_peak = w * 0.644
    amp_dip = w * 0.57
    tip_y = amp_peak
    peak_y = 0.0
    dip_y = amp_peak - amp_dip
    pin_r = w * 0.155
    pin_tip_y = dip_y + thickness * 0.32
    pin_cy = pin_tip_y - pin_r * 2.05
    bbox_top = min(peak_y, pin_cy - pin_r)
    bbox_bottom = max(tip_y, dip_y + thickness)
    return w, bbox_bottom - bbox_top, -bbox_top  # width, height, top-offset (draw y += this to align bbox_top to 0)


def _folded_map_icon(img, x, y, size, color, width=6):
    """Folded-paper-map-with-pin glyph, matched to a reference icon the
    client supplied (photo upload): a ribbon with pointed left/right
    ends and a peak-dip-peak zigzag top edge (proportions measured off
    that reference: overall h:w ~ 0.666, ribbon thickness ~0.59*w, peak
    rise ~0.644*w above the tip line, dip rise ~0.57*w), rounded joins
    at each vertex, a dashed route line drifting across it, and a
    teardrop location pin with an inner ring sitting over the dip."""
    d = ImageDraw.Draw(img)
    w = size
    thickness = w * 0.59
    amp_peak = w * 0.644
    amp_dip = w * 0.57
    tip_y = y + amp_peak
    peak_y = y
    dip_y = y + (amp_peak - amp_dip)

    fold_x = [x, x + 0.25 * w, x + 0.50 * w, x + 0.75 * w, x + w]
    top_y = [tip_y, peak_y, dip_y, peak_y, tip_y]
    bot_y = [tip_y, peak_y + thickness, dip_y + thickness, peak_y + thickness, tip_y]

    top_pts = list(zip(fold_x, top_y))
    bot_pts = list(zip(fold_x, bot_y))

    lw = max(3, int(width * 0.85))
    d.line(top_pts, fill=color, width=lw, joint="curve")
    d.line(bot_pts, fill=color, width=lw, joint="curve")
    # round off the two open ends (tip points) so the taper doesn't
    # look clipped where top/bottom meet
    r_end = lw / 2
    for (px, py) in (top_pts[0], top_pts[-1]):
        d.ellipse([px - r_end, py - r_end, px + r_end, py + r_end], fill=color)

    # crease line at each interior fold
    for i in (1, 2, 3):
        d.line([top_pts[i], bot_pts[i]], fill=color, width=max(2, lw - 2))

    # dashed route line, drifting gently across the ribbon at roughly
    # mid-thickness height, following the same zigzag centerline
    dash_y = [(t + b) / 2 for t, b in zip(top_y, bot_y)]
    route_pts = []
    n_seg = 40
    for i in range(n_seg + 1):
        t = i / n_seg
        seg = min(int(t * 4), 3)
        local_t = t * 4 - seg
        x0, x1 = fold_x[seg], fold_x[seg + 1]
        y0, y1 = dash_y[seg], dash_y[seg + 1]
        route_pts.append((x0 + (x1 - x0) * local_t, y0 + (y1 - y0) * local_t))
    dash_len, gap_len = 10, 8
    dist_acc = 0
    draw_on = True
    for i in range(len(route_pts) - 1):
        p0, p1 = route_pts[i], route_pts[i + 1]
        seg_len = ((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2) ** 0.5
        if draw_on:
            d.line([p0, p1], fill=color, width=max(2, lw - 3))
        dist_acc += seg_len
        threshold = dash_len if draw_on else gap_len
        if dist_acc >= threshold:
            dist_acc = 0
            draw_on = not draw_on

    # teardrop location pin, nudged down and to the right so it isn't
    # sitting dead-center on the fold
    pin_cx = fold_x[2] + w * 0.11
    pin_tip_y = dip_y + thickness * 0.32
    pin_r = w * 0.155
    pin_cy = pin_tip_y - pin_r * 2.05
    plw = max(3, int(width * 0.8))
    d.ellipse([pin_cx - pin_r, pin_cy - pin_r, pin_cx + pin_r, pin_cy + pin_r], outline=color, width=plw)
    inner_r = pin_r * 0.42
    d.ellipse([pin_cx - inner_r, pin_cy - inner_r, pin_cx + inner_r, pin_cy + inner_r], outline=color, width=max(2, plw - 1))
    tangent_deg = 38
    rad = math.radians(tangent_deg)
    lx = pin_cx - pin_r * math.sin(rad)
    ly = pin_cy + pin_r * math.cos(rad)
    rx = pin_cx + pin_r * math.sin(rad)
    ry = pin_cy + pin_r * math.cos(rad)
    d.line([(lx, ly), (pin_cx, pin_tip_y)], fill=color, width=plw, joint="curve")
    d.line([(rx, ry), (pin_cx, pin_tip_y)], fill=color, width=plw, joint="curve")

    bbox_top = min(peak_y, pin_cy - pin_r)
    bbox_bottom = max(tip_y, dip_y + thickness)
    return w, bbox_bottom - bbox_top


# ---------------------------------------------------------- page 1 ----
def gtr_cover(slot, slide_no, total, pal):
    """PAGE 1. slots: photo, clues (list of exactly 4 short strings),
    photo_credit (optional), panel_bg (optional, default pure black --
    override for a deck-specific panel color; header/clue-letter/swipe
    text stays pal ACCENT regardless, so keep panel_bg dark enough for
    that to read).

    Vertical blade layout: a narrow full-height photo strip on the left,
    a solid black panel on the right carrying all type. Replaces an
    earlier full-bleed-photo-with-scrims treatment, which fought
    legibility against bright areas in some photos (e.g. door frames) --
    putting every line of text on a flat panel instead sidesteps that
    entirely, at the cost of the photo reading smaller.

    Header is locked series branding: folded-map glyph + "Guess the
    Wine Region" in serif title case, stacked two lines, gold by default
    (or slot["title_color"] override, independent of the clue-letter/
    swipe-cue ACCENT color for decks that want the two to differ) -- do
    not vary the wording per deck, only the photo and clues change.
    Clues are lettered A-D in gold with white sans-serif copy. Swipe cue
    sits directly under the clues, centered on the panel (not the full
    page), in the same gold."""
    img, d, qa = _start("GTR-01 cover", slide_no, total, pal)
    qa.word_limit = 60

    blade_w = slot.get("blade_w", 760)
    panel_margin = 100
    gold = pal.get("ACCENT", SERIES_GOLD)
    panel_bg = slot.get("panel_bg", (0, 0, 0))

    # photo blade, full height, left edge
    img.paste(cover_fit(load_photo(slot["photo"]), blade_w, H), (0, 0))
    d = ImageDraw.Draw(img)
    # solid color panel, full height, right of the blade
    d.rectangle([blade_w, 0, W, H], fill=panel_bg)
    d = ImageDraw.Draw(img)

    content_x0 = blade_w + panel_margin
    content_w = W - blade_w - 2 * panel_margin

    # ---- header: icon inline with the first line of the title ("Guess
    # the"), title force-wrapped so "Wine Region" starts the second
    # line -- title gold, icon white and scaled off the title size ----
    hf_size = 170
    icon_size = int(hf_size * 120 / 140)
    icon_gap = 36
    hf = font("display_black", hf_size)
    qa.size("header", hf_size, headline=True)
    ha, hdsc = hf.getmetrics()
    title_lh = int((ha + hdsc) * 0.86)

    row1_y = 140
    icon_w, icon_h, icon_top_off = _folded_map_icon_bbox(icon_size)
    icon_target_top = row1_y + int(((ha + hdsc) - icon_h) // 2)
    icon_draw_y = icon_target_top + icon_top_off
    iw, ih = _folded_map_icon(img, content_x0, icon_draw_y, icon_size, PAPER, width=7)
    d = ImageDraw.Draw(img)

    line1_txt, line2_txt = "Guess the", "Wine Region"
    line1_x = content_x0 + icon_size + icon_gap
    title_color = slot.get("title_color", gold)
    d.text((line1_x, row1_y), line1_txt, font=hf, fill=title_color)
    line2_y = row1_y + title_lh
    d.text((content_x0, line2_y), line2_txt, font=hf, fill=title_color)
    header_bottom = line2_y + ha + hdsc

    qa.box("header", (content_x0, row1_y, content_x0 + content_w, header_bottom))
    qa.add_words("Guess the Wine Region")

    # ---- four clues, lettered A-D ----
    clues = slot["clues"]
    assert len(clues) == 4, "gtr_cover requires exactly 4 clues"
    letters = ["A.", "B.", "C.", "D."]
    cf_size = 88
    cf = font("body", cf_size)
    line_gap = 1.26
    ca, cd = cf.getmetrics()
    row_lh = int((ca + cd) * line_gap)
    lf = font("display_bold", 86)
    letter_col_w = 120
    text_x = content_x0 + letter_col_w
    max_text_w = content_w - letter_col_w

    clue_blocks = []
    total_h = 0
    for c in clues:
        lines = wrap(d, c, cf, max_text_w)
        block_h = row_lh * len(lines)
        clue_blocks.append((lines, block_h))
        total_h += block_h
    clue_gap = 34
    total_h += clue_gap * (len(clues) - 1)

    y = header_bottom + 230
    clues_bottom = y + total_h

    qa.box("clues", (content_x0, y, content_x0 + content_w, clues_bottom))
    for letter, (lines, block_h) in zip(letters, clue_blocks):
        by = y
        la, ld = lf.getmetrics()
        letter_y = by + (row_lh - (la + ld)) // 2
        d.text((content_x0, letter_y), letter, font=lf, fill=gold)
        for ln in lines:
            d.text((text_x, by), ln, font=cf, fill=PAPER)
            by += row_lh
        y += block_h + clue_gap
    qa.size("body", cf_size)
    qa.add_words(" ".join(clues))

    # ---- swipe cue: centered on the panel, right under the clues ----
    sf = font("kicker_bold", 88)
    swipe_txt = "SWIPE TO SEE THE ANSWER  ←"
    sw = text_w(d, swipe_txt, sf) + 4 * len(swipe_txt)
    swipe_y = clues_bottom + 170
    swipe_x = content_x0 + (content_w - sw) // 2
    tracked_text(d, (swipe_x, swipe_y), swipe_txt, sf, gold, tracking=4)
    sa, sd = sf.getmetrics()
    qa.box("!swipe_cue", (swipe_x, swipe_y, swipe_x + sw, swipe_y + sa + sd))
    qa.size("!swipe_cue", 88)
    if swipe_y + sa + sd > CONTENT_BOTTOM:
        qa.notes.append(f"FAIL swipe-footer: swipe cue bottom {swipe_y + sa + sd} > CONTENT_BOTTOM {CONTENT_BOTTOM}")

    # The footer's swipe-cue/page-number label sits over the photo blade
    # here (unlike other series where it's on paper/panel), so MUTED's
    # fixed gray can go illegible against busy or warm-toned photo areas
    # (e.g. dry gold grass) -- sample the actual pixels under the label
    # zone and pick a readable color rather than assuming MUTED works.
    footer_sample = (M - 20, FOOTER_Y - 20, M + 340, FOOTER_Y + 50)
    footer_fill = INK if _region_luminance(img, footer_sample) > 150 else (255, 255, 255)
    return _finish(img, d, qa, slide_no, total, page_pos="left", credit=slot.get("photo_credit"),
                   footer_fill=footer_fill)


# ---------------------------------------------------------- page 2 ----
def gtr_reveal(slot, slide_no, total, pal):
    """PAGE 2. slots: photo, region (region name, rendered large in
    serif title case), blurb (2-3 sentences on why the region matters --
    rendered centered below the region name in a light serif), photo_credit
    (optional), flag (optional, one of _FLAGS.keys() -- "french"
    (default, for backward compat with existing decks), "italian", or
    "nz" (real flag image asset, not a drawn tricolor -- see
    _image_flag)).

    Top 66% is the full-bleed photo; bottom third is the reveal panel:
    "The Wine Region Is..." kicker, region name, then the blurb, all
    compressed to fit the shallower panel with at least a 200px bottom
    margin (bottom_margin, currently 200 -- pass slot["bottom_margin"]
    to override per-deck if a photo needs a different crop). No swipe
    cue on this page -- it's the last page of the pair, so only the
    page-number footer prints."""
    img, d, qa = _start("GTR-02 reveal", slide_no, total, pal)
    qa.word_limit = 90

    bottom_margin = slot.get("bottom_margin", 200)
    bottom_limit = H - bottom_margin

    photo_h = slot.get("photo_h", int(H * 0.66))
    img.paste(cover_fit(load_photo(slot["photo"]), W, photo_h), (0, 0))
    d = ImageDraw.Draw(img)

    # photo caption: top-right inside the image, kept away from the
    # text-heavy bottom panel. Color adapts to what's actually behind
    # it -- a light patch of photo (sky, pale water) gets black ink and
    # no scrim; anything else gets the usual white-on-scrim treatment.
    # Same base type treatment as core.photo_band() (caption_italic,
    # floor size); photo credit stays separate, in the footer gutter.
    caption_txt = slot.get("caption")
    if caption_txt:
        capf = font("caption_italic", TYPE["caption"])
        cap_w = text_w(d, caption_txt, capf)
        cap_x = W - M - cap_w
        cap_y = 60
        sample_box = (cap_x - 20, cap_y - 15, W - M + 20, cap_y + TYPE["caption"] + 15)
        bg_lum = _region_luminance(img, sample_box)

        if bg_lum > 150:
            text_color, text_lum = INK, _lum_of(INK)
        else:
            chip(img, (cap_x - 20, cap_y - 15, W - M + 20, cap_y + TYPE["caption"] + 15), (10, 10, 10))
            d = ImageDraw.Draw(img)
            text_color, text_lum = (255, 255, 255), 255

        d.text((cap_x, cap_y), caption_txt, font=capf, fill=text_color)
        qa.size("!caption", TYPE["caption"])
        qa.check_photo_contrast(img, (cap_x, cap_y, W - M, cap_y + TYPE["caption"]),
                                 text_lum, "caption", min_delta=70)

    d.rectangle([0, photo_h, W, H], fill=PAPER)
    d.line([(0, photo_h), (W, photo_h)], fill=pal.get("ACCENT", SERIES_GOLD), width=6)
    d = ImageDraw.Draw(img)

    panel_top = photo_h

    kf = font("kicker_bold", 60)
    kicker_txt = "THE WINE REGION IS…"
    kw = text_w(d, kicker_txt, kf) + 5 * len(kicker_txt)
    ky = panel_top + 26
    tracked_text(d, ((W - kw) // 2, ky), kicker_txt, kf, pal.get("ACCENT", SERIES_GOLD), tracking=5)
    qa.size("kicker", 60)
    ka, kd = kf.getmetrics()

    rf_size = 140
    rf = font("display_black", rf_size)
    region_txt = slot["region"]
    avail_w = W - 2 * M - 200  # reserve room for the flag + gap alongside it
    while text_w(d, region_txt, rf) > avail_w and rf_size > 90:
        rf_size -= 2
        rf = font("display_black", rf_size)
    qa.size("region" if rf_size == 140 else "!region", rf_size, headline=True)
    rw = text_w(d, region_txt, rf)
    ra, rd = rf.getmetrics()
    ry = ky + ka + kd + 18

    # country flag sits beside the name, centered against the name's
    # actual rendered glyph extent (not the font's full ascent box,
    # which includes headroom above the cap-height) so it lines up
    # visually with the letters rather than sitting high
    glyph_l, glyph_t, glyph_r, glyph_b = d.textbbox((0, 0), region_txt, font=rf)
    glyph_h = glyph_b - glyph_t
    flag_h = int(glyph_h * 0.82)
    flag_w = int(flag_h * 1.5)
    flag_gap = 34
    group_w = rw + flag_gap + flag_w
    group_x0 = (W - group_w) // 2
    d.text((group_x0, ry), region_txt, font=rf, fill=pal.get("SIGNATURE", (114, 47, 55)))
    # center vertically on the x-height band (lowercase letters), not the
    # full glyph extent, so the flag sits with "ntre-eux-ers" rather than
    # being pulled up by the capital E/D/M
    lc_l, lc_t, lc_r, lc_b = d.textbbox((0, 0), "e", font=rf)
    lc_center = (lc_t + lc_b) / 2
    flag_y = int(ry + lc_center - flag_h / 2)
    flag_fn = _FLAGS.get(slot.get("flag", "french"), _french_flag)
    flag_fn(img, group_x0 + rw + flag_gap, flag_y, flag_h, flag_w)
    d = ImageDraw.Draw(img)
    qa.box("region", (group_x0, ry, group_x0 + group_w, ry + ra + rd))

    # ---- blurb: 2-3 sentences, fully justified, light serif -- shrunk
    # as needed so it clears the bottom_margin safe zone in the shallower
    # bottom-third panel ----
    blurb_txt = slot.get("blurb", "")
    if blurb_txt:
        max_w = W - 2 * M - 100
        col_x0 = (W - max_w) // 2
        col_x1 = col_x0 + max_w
        leading = 0.98
        by_top = ry + ra + rd + 40

        bf_size = 84
        while True:
            bf = font("display_light", bf_size)
            lines = wrap(d, blurb_txt, bf, max_w)
            ba, bd = bf.getmetrics()
            line_lh = int((ba + bd) * leading)
            block_bottom = by_top + line_lh * len(lines)
            if block_bottom <= bottom_limit or bf_size <= 60:
                break
            bf_size -= 2

        by = by_top
        for i, ln in enumerate(lines):
            words = ln.split(" ")
            is_last = (i == len(lines) - 1)
            if is_last or len(words) == 1:
                d.text((col_x0, by), ln, font=bf, fill=MUTED)
            else:
                word_widths = [text_w(d, w, bf) for w in words]
                gaps = len(words) - 1
                extra = (col_x1 - col_x0) - sum(word_widths)
                space_w = extra / gaps
                x = float(col_x0)
                for j, w in enumerate(words):
                    d.text((x, by), w, font=bf, fill=MUTED)
                    x += word_widths[j] + space_w
            by += line_lh
        qa.box("!blurb", (col_x0, by_top, col_x1, by))
        qa.size("blurb" if bf_size == 84 else "!blurb", bf_size)
        if by > bottom_limit:
            qa.notes.append(f"FAIL blurb-margin: blurb bottom {by} > bottom_limit {bottom_limit} ({bottom_margin}px margin)")

    qa.add_words(kicker_txt + " " + region_txt + " " + blurb_txt)

    # page 2 is the last page of the pair -- no swipe cue or arrow needed,
    # just the page-number footer
    core_footer(d, slide_no, total, label="", page_pos="left", credit=slot.get("photo_credit"))
    print(qa.report(img))
    return img
