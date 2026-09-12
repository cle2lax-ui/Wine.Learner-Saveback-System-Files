"""
FIELD GUIDE STYLE SYSTEM v4.2 — MODULE LIBRARY
18 wired layouts. Each module: fixed geometry, named slots, QA built in.
A deck manifest chooses modules and fills slots; nothing else is decided per-deck.

    M01 statement      full-bleed cover / quote / closing
    M02 editorial_lead photo band + headline + hero standfirst + run-ins,
                       OR a two-column data table (table slot)
    M03 side_rail      vertical split, text column + grouped lists + famous names
    M04 stat_wall      grid of big serif numerals + optional famous names
    M05 duel           split-image band + two-column comparison
    M06 process_map    photo stripe + aligned flowcharts w/ decision diamonds
    M07 card_grid      variable-row icon/flag cards (row_layout, default 2x2)
    M08 showcase_shelf product grid on shelf rules, configurable bottle size
    M09 atlas          schematic map/plan + legend + markers + outlines
    M10 timeline       chronology spine with nodes
    M11 ladder         classification pyramid/tiers (single-path only --
                       see euler_nesting for branching/nested-set content)
    M12 lexicon_cloud  scattered term+gloss cloud (shelf-packed, no overlaps)
    M13 spotlight      annotated hero with lettered callouts
    M14 feature_trio   three columns: mini-head + rule + blurb + image
    M15 fact_file      key-value data rail with hairline rules + famous names
    M16 mosaic         one large + small photos, captions only (pacing breather)
    M17 photo_quote    full-bleed photo, one large white sentence-case quote
    M18 euler_nesting  containment diagram for true nested-set relationships
                       (not a ladder: shows branching, siblings, and set
                       exceptions that a single-path pyramid can't)

Cover and closing (`statement`) carry "THE FIELD GUIDE" as the
kicker, in the deck's ACCENT (deep gold) — locked series branding, not
a per-deck slot. See `statement`'s docstring.
"""
import random
import re
from PIL import Image, ImageDraw, ImageFilter
from tokens import *
import core
from core import (new_canvas, footer, kicker_block, headline, font, text_w,
                  tracked_text, wrap, paragraph, standfirst, run_in, famous_names,
                  load_photo, load_photo_rgba, cover_fit, scrim, chip, photo_band, photo_stripe, photo_credit, QA,
                  contrast, region_luminance)


def _start(name, slide_no, total, pal, bg_color=None):
    img = new_canvas(bg=bg_color)
    d = ImageDraw.Draw(img)
    qa = QA(f"{name} #{slide_no}")
    return img, d, qa


def _finish(img, d, qa, slide_no, total, page_pos="right", credit=None, footer_fill=None,
            footer_adaptive=False, footer_label=None, show_page_num=True, footer_size=None):
    footer_kwargs = dict(page_pos=page_pos, credit=credit, fill=footer_fill,
                          img=img if footer_adaptive else None, show_page_num=show_page_num,
                          footer_size=footer_size)
    if footer_label is not None:
        footer_kwargs["label"] = footer_label
    footer(d, slide_no, total, **footer_kwargs)
    print(qa.report(img))
    return img



# ────────────────────────── M01 STATEMENT ──────────────────────────
def statement(slot, slide_no, total, pal):
    """slots: variant('cover'|'quote'|'closing'), photo, title(1-2 lines '\\n'),
    subtitle(optional), caption(optional), quote(for variant quote), attribution.

    Rand filter (system default, save-back v7): no gradient scrims on
    any variant. cover/closing use a hard-edged flat color block (pal
    SIGNATURE) instead -- photo and type live in separate zones, not
    blended through a gradient. cover and closing are a genuine bookend
    now, sharing the same block/dot/kicker system, not two different
    treatments.

    cover and closing show "THE FIELD GUIDE" as the kicker by default,
    in pal ACCENT. An optional `kicker` slot overrides the text -- use it
    to append the arc subject ("THE FIELD GUIDE: NORTHERN RHONE") on a
    cover whose headline withholds the region. The series name stays;
    this is not a licence to replace it. (quote doesn't show a kicker.)
    The kicker is the same dot + tracked-caps mark as
    core.kicker_block(), just set larger for the cover/close scale.

    photo_anchor (0.0-1.0, default 0.5) and photo_zoom (>=1.0, default
    1.0) pass through to cover_fit() for framing control -- e.g. a
    landscape photo with too much sky can be re-anchored toward its
    bottom without needing a bespoke crop function per deck.

    cover_layout="lower_left" is preserved for decks that already rely
    on it (kicker in the sky, title/subtitle anchored bottom-left) --
    it now uses a flat chip() bar behind the text instead of a
    gradient, but keeps its distinct positioning logic."""
    img, d, qa = _start("M01 statement", slide_no, total, pal)
    v = slot.get("variant", "cover")
    anchor = slot.get("photo_anchor", 0.5)
    zoom = slot.get("photo_zoom", 1.0)
    img.paste(cover_fit(load_photo(slot["photo"]), W, H, y_anchor=anchor, zoom=zoom), (0, 0))

    # The series mark was hardcoded to "THE FIELD GUIDE" in all four
    # statement variants. A per-deck kicker needs to override it -- the
    # cover is the one slide where naming the subject alongside the
    # series does real work, since the headline deliberately withholds
    # the region. Default is unchanged, so every existing deck is
    # untouched.
    kicker_txt = slot.get("kicker", "THE FIELD GUIDE")

    def _mark_kicker(x, y, dot_color, text_color, size=70, tracking=7):
        r = int(size * 0.23)
        cy = y + int(size * 0.5)
        d.ellipse([x, cy - r, x + 2 * r, cy + r], fill=dot_color)
        kf = font("kicker_bold", size)
        tracked_text(d, (x + 2 * r + 22, y), kicker_txt, kf, text_color, tracking=tracking)
        return y + int(size * 1.5)

    if v == "cover":
        layout = slot.get("cover_layout", "center")
        if layout == "sky":
            # Full-bleed photo, title set into the open sky at the top,
            # subtitle in ACCENT across the lower third. No colour block
            # and no full-width chip -- the photograph carries the whole
            # frame, which is the point of the treatment.
            #
            # Legibility is handled by sampling the actual pixels rather
            # than assuming: "sky" is bright on the Côte-Rôtie winter
            # terrace shot and would take INK, but an evening or overcast
            # cover would need PAPER, and a fixed choice is wrong half the
            # time. Where the sampled band is mid-luminance -- neither
            # safely light nor safely dark -- a soft gradient scrim goes
            # in behind the text instead of forcing a colour that will
            # sit at low contrast.
            kicker_y = slot.get("kicker_y", 150)

            title_size = slot.get("title_size", TYPE["display_xl"])
            tf = font("display_black", title_size)
            asc, desc = tf.getmetrics()
            title_lh = int((asc + desc) * slot.get("title_leading", 0.90))
            title_lines = []
            for raw_ln in slot["title"].split("\n"):
                title_lines.extend(wrap(d, raw_ln, tf, W - 2 * M))
            title_top = kicker_y + 130
            title_h = title_lh * len(title_lines)

            sky_lum = region_luminance(img, (M, kicker_y, W - M, title_top + title_h + 20))
            forced = slot.get("title_color")
            if forced is not None:
                # An explicit title_color overrides the sampled choice --
                # but a forced light title over a bright sky needs the
                # scrim the sampler would otherwise have skipped, or it
                # vanishes. Take the colour as given; still protect it.
                if sky_lum > 120 and sum(forced) / 3 > 150:
                    # A top-dark gradient is weakest at its own bottom
                    # edge, so ending it at the title block puts the LAST
                    # line -- the one most likely to have dropped out of
                    # the sky and onto the landscape -- in the unprotected
                    # end. Run it well past the title and hold the top
                    # section flat so every line gets the same cover.
                    # ONE gradient over the whole canvas, not a chip with
                    # a scrim under it. Any chip/scrim pair leaves a
                    # visible horizontal seam at the handover -- matching
                    # their strengths does not help, because chip
                    # composites flat and scrim composites through a 1.4
                    # gamma, so the two are only equal at the single
                    # boundary pixel and diverge immediately either side.
                    # A full-height gradient has no interior edge at all,
                    # and by the time it reaches the middle of the frame
                    # it has faded out, so it never fights the subtitle
                    # band below.
                    scrim(img, (0, 0, W, H), dark_at="top", strength=0.42, color=INK)
                    d = ImageDraw.Draw(img)
                sky_fill = forced
                sky_kicker = forced
            elif sky_lum > 165:
                sky_fill, sky_kicker = INK, INK
            elif sky_lum < 95:
                sky_fill, sky_kicker = PAPER, PAPER
            else:
                scrim(img, (0, 0, W, title_top + title_h + 90),
                      dark_at="top", strength=0.62)
                d = ImageDraw.Draw(img)
                sky_fill, sky_kicker = PAPER, PAPER

            qa.size("kicker", 70)
            _mark_kicker(M, kicker_y, pal["SIGNATURE"], sky_kicker)

            qa.size("title", title_size, headline=True)
            ty = title_top
            for ln in title_lines:
                d.text((M, ty), ln, font=tf, fill=sky_fill)
                ty += title_lh
            qa.box("title", (M, title_top, W - M, ty))

            sub_size = slot.get("subtitle_size", TYPE["standfirst_hero"])
            sf = font("italbold", sub_size)
            qa.size("subtitle", sub_size)
            raw_subtitle = slot.get("subtitle", "")
            sub_lines = (raw_subtitle.split("\n") if "\n" in raw_subtitle
                         else wrap(d, raw_subtitle, sf, W - 2 * M))
            sa, sd = sf.getmetrics()
            sub_lh = int((sa + sd) * 1.04)
            sub_h = sub_lh * len(sub_lines)
            sub_top = H - slot.get("bottom_margin", 300) - sub_h

            # Gold on a photograph is the one combination that reliably
            # disappears -- ACCENT sits mid-luminance, so it has nothing
            # to contrast against in either direction. The lower band
            # always gets protection, regardless of what is behind it.
            #
            # chip, not scrim, for the band the text actually sits in.
            # core.scrim's own docstring warns against exactly this
            # mistake: the gradient is at ZERO strength at one edge, so a
            # bottom-dark scrim gives least protection at its top edge --
            # which is where the first line of the subtitle sits. That is
            # how this cover first rendered gold over a sunlit dry-stone
            # wall at almost no contrast. Flat chip guarantees the band;
            # a scrim above it only softens the seam into the photo.
            band_top = sub_top - 70
            # color=INK so the gradient lands on the chip's exact tone at
            # the seam; core.SCRIM is a different colour and left a
            # visible hard line where the two met.
            scrim(img, (0, band_top - 300, W, band_top),
                  dark_at="bottom", strength=0.74, color=INK)
            chip(img, (0, band_top, W, H), INK, opacity=0.74)
            d = ImageDraw.Draw(img)
            d = ImageDraw.Draw(img)

            sy = sub_top
            sub_fill = slot.get("subtitle_color", pal["ACCENT"])
            for ln in sub_lines:
                d.text((M, sy), ln, font=sf, fill=sub_fill)
                sy += sub_lh
            qa.box("subtitle", (M, sub_top, W - M, sy))
            qa.add_words(slot["title"] + " " + raw_subtitle)
        elif layout == "lower_left":
            kf = font("kicker_bold", 70); qa.size("kicker", 70)
            series_kicker = kicker_txt
            kw = core.text_w(d, series_kicker, kf) + 5 * len(series_kicker)
            kicker_y = slot.get("kicker_y", 190)
            _mark_kicker((W - kw) // 2 - 40, kicker_y, pal["SIGNATURE"], PAPER)

            sub_size = TYPE["standfirst_hero"] + 40
            sf = font("italbold", sub_size)
            raw_subtitle = slot.get("subtitle", "")
            avail_w = W - 2 * M
            while text_w(d, raw_subtitle, sf) > avail_w and sub_size > 40:
                sub_size -= 2
                sf = font("italbold", sub_size)
            sub_prefix = "!" if sub_size < TYPE["standfirst_hero"] else ""
            qa.size(f"{sub_prefix}subtitle", sub_size)
            sub_lines = [raw_subtitle]
            sa, sd = sf.getmetrics()
            sub_lh = int((sa + sd) * 1.02)
            sub_h = sub_lh * len(sub_lines)
            bottom_margin = slot.get("bottom_margin", 320)
            sub_top = H - bottom_margin - sub_h

            tf = font("display_black", TYPE["display_xl"])
            qa.size("title", TYPE["display_xl"], headline=True)
            asc, desc = tf.getmetrics()
            title_lh = int((asc + desc) * 0.92)
            title_lines = []
            for raw_ln in slot["title"].split("\n"):
                title_lines.extend(wrap(d, raw_ln, tf, W - 2 * M))
            title_h = title_lh * len(title_lines)
            title_subtitle_gap = 50
            title_top = sub_top - title_subtitle_gap - title_h

            # flat chip bar behind the text block (Rand filter) instead
            # of a gradient -- sized to the actual text bounding area
            chip(img, (0, title_top - 30, W, sub_top + sub_h + 30), INK, opacity=0.86)
            d = ImageDraw.Draw(img)

            ty = title_top
            for ln in title_lines:
                d.text((M, ty), ln, font=tf, fill=PAPER)
                ty += title_lh
            qa.box("title", (M, title_top, W - M, ty))

            sy = sub_top
            for ln in sub_lines:
                d.text((M, sy), ln, font=sf, fill=slot.get("subtitle_color", pal["ACCENT"]))
                sy += sub_lh
            qa.box("!subtitle", (M, sub_top, W - M, sy))
            qa.add_words(slot["title"] + " " + slot.get("subtitle", ""))
        else:
            block_frac = slot.get("block_frac", 0.46)
            block_h = int(H * block_frac)
            block_top = H - block_h
            d.rectangle([0, block_top, W, H], fill=pal["SIGNATURE"])

            mark_r = 46
            d.ellipse([W - M - 2 * mark_r, 130, W - M, 130 + 2 * mark_r], fill=pal["SIGNATURE"])

            ky = block_top + 60
            kf = font("kicker_bold", 60); qa.size("kicker", 60)
            # dot_color was pal["SIGNATURE"] here, identical to this
            # block's own fill -- invisible against itself. PAPER matches
            # the kicker text color instead, same treatment the closing
            # variant already gets correctly (its block is INK, not
            # SIGNATURE, so the same SIGNATURE dot reads fine there).
            ky_end = _mark_kicker(M, ky, PAPER, PAPER, size=60)

            title_size = slot.get("title_size", 120)
            title_leading = slot.get("title_leading", 0.85)
            tf = font("display_black", title_size)
            qa.size("title", title_size, headline=True)
            asc, desc = tf.getmetrics()
            ty = ky_end + 40
            for ln in slot["title"].split("\n"):
                d.text((M, ty), ln, font=tf, fill=PAPER)
                ty += int((asc + desc) * title_leading)
            qa.box("title", (M, ky_end + 40, W - M, ty))

            sub_size = slot.get("subtitle_size", 100)
            sf = font("italbold", sub_size)
            qa.size("!subtitle", sub_size)
            raw_subtitle = slot.get("subtitle", "")
            lines = raw_subtitle.split("\n") if "\n" in raw_subtitle else wrap(d, raw_subtitle, sf, W - 2 * M)
            sa, sd = sf.getmetrics()
            lh = int((sa + sd) * 1.05)
            sy = ty + 30
            for ln in lines:
                d.text((M, sy), ln, font=sf, fill=pal["ACCENT"])
                sy += lh
            qa.box("!subtitle", (M, ty + 30, W - M, sy))
            qa.add_words(slot["title"] + " " + slot.get("subtitle", ""))
    elif v == "quote":
        block_h = int(H * 0.58)
        block_top = H - block_h
        chip(img, (0, block_top, W, H), INK, opacity=0.90)
        d = ImageDraw.Draw(img)
        qf = font("italbold", TYPE["display_lg"] - 40)
        qa.size("quote", TYPE["display_lg"] - 40, headline=True)
        y = paragraph(d, (M, block_top + 70), "\u201c" + slot["quote"] + "\u201d", qf, PAPER, W - 2 * M, 1.16)
        qa.box("quote", (M, block_top + 70, W - M, y))
        d.line([(M, y + 40), (M + 240, y + 40)], fill=pal["ACCENT"], width=6)
        af = font("caption_italic", TYPE["caption"] + 10)
        qa.size("attr", TYPE["caption"] + 10)
        d.text((M, y + 90), "\u2014 " + slot.get("attribution", ""), font=af, fill=pal["ACCENT"])
        qa.add_words(slot["quote"])
    else:  # closing -- same block/dot/kicker system as the cover, for a real bookend
        block_frac = slot.get("block_frac", 0.34)
        block_h = int(H * block_frac)
        block_top = H - block_h
        d.rectangle([0, block_top, W, H], fill=INK)

        mark_r = 40
        # Moved to match the cover variant's placement (top-right of the
        # photo) for a consistent bookend, per Steve's direction -- was
        # bottom-left just above the block seam.
        d.ellipse([W - M - 2 * mark_r, 130, W - M, 130 + 2 * mark_r], fill=pal["SIGNATURE"])

        ky = block_top + 44
        ky_end = _mark_kicker(M, ky, pal["SIGNATURE"], PAPER, size=56)

        title_size = slot.get("title_size", 130)
        tf = font("display_black", title_size)
        qa.size("title", title_size, headline=True)
        ty = ky_end + 30
        d.text((M, ty), slot["title"], font=tf, fill=pal["ACCENT"])
        tb = d.textbbox((M, ty), slot["title"], font=tf)
        qa.box("title", (M, ty, W - M, tb[3]))
        qa.add_words(slot["title"])
        if slot.get("subtitle"):
            # Was a single unwrapped d.text at a fixed size, with no
            # qa.box registered -- so any subtitle longer than the measure
            # ran straight off the right edge and the QA harness passed it
            # silently. Wrap to the measure, honour subtitle_size like the
            # cover variant already does, and register the box so the
            # harness catches an overrun instead of shipping it.
            sub_size = slot.get("subtitle_size", TYPE["standfirst_hero"] - 12)
            sf = font("italbold", sub_size)
            qa.size("subtitle", sub_size)
            sa, sd = sf.getmetrics()
            slh = int((sa + sd) * 1.06)
            raw = slot["subtitle"]
            sub_lines = raw.split("\n") if "\n" in raw else wrap(d, raw, sf, W - 2 * M)
            sy = tb[3] + 30
            for ln in sub_lines:
                d.text((M, sy), ln, font=sf, fill=PAPER)
                sy += slh
            qa.box("subtitle", (M, tb[3] + 30, W - M, sy))
            qa.add_words(raw)
    if slot.get("photo_caption"):
        # Chip behind it. This caption sits at the top of a full-bleed
        # photo, and on any image with a bright sky -- which is most of
        # them -- white on white simply is not there. photo_band and the
        # side rail both protect their captions; this one never did,
        # because until now nothing had passed a photo_caption to a
        # cover or closing statement.
        cf = font(core.CAPTION_FACE, core.CAPTION_SIZE)
        cw = text_w(d, slot["photo_caption"], cf)
        chip(img, (M - 20, 76, M + cw + 20, 90 + core.CAPTION_SIZE + 22), INK,
             opacity=0.62)
        d = ImageDraw.Draw(img)
        d.text((M, 90), slot["photo_caption"], font=cf, fill=PAPER)
        qa.add_words(slot["photo_caption"])
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"),
                   footer_fill=(PAPER if v in ("cover", "closing", "quote") else None))


# ─────────────────────── M02 EDITORIAL LEAD ───────────────────────
# ─────────────────────── M01B GRID COVER ───────────────────────
def grid_cover(slot, slide_no, total, pal):
    """slots: photos[9] (3x3 grid, row-major, top-left to bottom-right),
    title(1-2 lines '\\n'), subtitle(optional), photo_credit(optional,
    combined string for the footer -- a 9-photo grid usually pulls from
    several sources).

    Grid cells are always square -- grid_h is derived from cell width
    (W//3 * 3), not from a block_frac input, so the block below is
    whatever's left over (roughly 20% of canvas height, not the ~46%
    a single-photo cover block gets).

    v3: the "THE FIELD GUIDE" kicker mark moved off the block and onto
    the top-left grid photo itself (overlaid, luminance-adaptive color
    same as every other on-photo text in this system) specifically to
    free up the block for a much larger title -- the block now carries
    title + subtitle only. This is a real, requested tradeoff: the
    kicker reads quieter sitting on a photo than it did as a standalone
    line, but the title gets roughly 60% more size to work with.

    Same "standard color blade" flat-panel treatment as statement()'s
    cover variant otherwise (duplicated rather than refactored out of
    statement() to avoid regression risk on every existing deck that
    calls it). The photo zone is a full-bleed 3x3 grid, no gutters, no
    borders, instead of one full-bleed hero photo."""
    img, d, qa = _start("M01b grid_cover", slide_no, total, pal)
    photos = slot["photos"]
    assert len(photos) == 9, "grid_cover needs exactly 9 photos for a 3x3 grid"
    cell_w = W // 3
    grid_h = cell_w * 3  # square cells -- block below gets whatever's left
    cell_h = cell_w
    for i, p in enumerate(photos):
        r, c = divmod(i, 3)
        x, y = c * cell_w, r * cell_h
        # last row/col absorbs the rounding remainder so the grid is
        # truly full-bleed with no gap at the right/bottom edge
        w = (W - x) if c == 2 else cell_w
        h = (grid_h - y) if r == 2 else cell_h
        img.paste(cover_fit(load_photo(p), w, h), (x, y))
    d = ImageDraw.Draw(img)

    # Kicker mark, overlaid on the top-left cell. Luminance-adaptive:
    # measure the actual pixels under the mark's footprint and scrim
    # only if needed, same discipline as every other on-photo text in
    # this system (never assume a fixed color reads against whatever
    # photo happens to land in that cell).
    kicker_size = 60
    kpad = 24
    kf = font("kicker_bold", kicker_size)
    r = int(kicker_size * 0.23)
    kregion = (0, 0, min(cell_w, kpad + 2 * r + 22 + text_w(d, "THE FIELD GUIDE", kf) + kpad), kpad * 2 + kicker_size)
    klum = region_luminance(img, kregion)
    if klum > 150:
        kdot_color = kbg_text = INK
    else:
        core.chip(img, kregion, (0, 0, 0), opacity=0.30)
        d = ImageDraw.Draw(img)
        kdot_color = kbg_text = PAPER
    kcy = kpad + int(kicker_size * 0.5)
    d.ellipse([kpad, kcy - r, kpad + 2 * r, kcy + r], fill=kdot_color)
    qa.size("kicker", kicker_size)
    tracked_text(d, (kpad + 2 * r + 22, kpad), "THE FIELD GUIDE", kf, kbg_text, tracking=7)
    kicker_bottom = kregion[3]

    # Subtitle chip, directly under the kicker "bug," spanning exactly
    # the width of the first two grid tiles (lemon + strawberry) -- a
    # solid backing bar rather than another luminance-adaptive scrim,
    # since it needs to read as a deliberate graphic element, not just
    # legible-on-a-photo furniture like the kicker above it.
    chip_x0, chip_x1 = 0, 2 * cell_w
    sub_size = slot.get("subtitle_size", 64)
    sf = font("italbold", sub_size)
    raw_subtitle = slot.get("subtitle", "")
    chip_pad_x, chip_pad_y = 24, 16
    while sub_size > 20:
        sf = font("italbold", sub_size)
        if text_w(d, raw_subtitle, sf) <= (chip_x1 - chip_x0) - 2 * chip_pad_x:
            break
        sub_size -= 2
    qa.size("!subtitle", sub_size)
    sa, sd = sf.getmetrics()
    chip_y0 = kicker_bottom + 8
    chip_y1 = chip_y0 + sa + sd + 2 * chip_pad_y
    d.rectangle([chip_x0, chip_y0, chip_x1, chip_y1], fill=pal["SIGNATURE"])
    d.text((chip_x0 + chip_pad_x, chip_y0 + chip_pad_y), raw_subtitle, font=sf, fill=PAPER)
    qa.box("!subtitle", (chip_x0, chip_y0, chip_x1, chip_y1))

    block_top = grid_h
    d.rectangle([0, block_top, W, H], fill=pal["SIGNATURE"])

    mark_r = 34
    d.ellipse([W - M - 2 * mark_r, 40, W - M, 40 + 2 * mark_r], fill=pal["SIGNATURE"])

    title_size = slot.get("title_size", 150)
    title_leading = slot.get("title_leading", 0.78)
    tf = font("display_black", title_size)
    qa.size("title", title_size, headline=True)
    asc, desc = tf.getmetrics()
    ty = block_top + 10
    for ln in slot["title"].split("\n"):
        d.text((M, ty), ln, font=tf, fill=PAPER)
        ty += int((asc + desc) * title_leading)
    qa.box("title", (M, block_top + 10, W - M, ty))
    qa.add_words(slot["title"] + " " + slot.get("subtitle", ""))

    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"), footer_fill=PAPER)


def editorial_lead(slot, slide_no, total, pal):
    """slots: photo, photo_caption, kicker, headline, standfirst,
    items[(lead, body)x2-4] (optional if table given), table (optional):
    dict(groups=[(title, [(name, metric, note), ...]) x2]) -- renders as
    two side-by-side compact tables with hairline row rules, e.g. for
    grape/varietal reference data."""
    img, d, qa = _start("M02 editorial_lead", slide_no, total, pal)
    band_h = slot.get("band_h", BAND_TALL)
    y = photo_band(img, slot["photo"], 0, band_h, slot.get("photo_caption"))
    d = ImageDraw.Draw(img)
    y = kicker_block(d, slot["kicker"], pal, y=y + 50); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y = standfirst(d, (M, y + 8), slot["standfirst"], W - 2 * M, leading=slot.get("standfirst_leading", 1.18)) + slot.get("standfirst_gap", 60)
    qa.size("standfirst", TYPE["standfirst"])

    if slot.get("table"):
        groups = slot["table"]["groups"]
        gutter = 80
        col_w = (W - 2 * M - gutter * (len(groups) - 1)) // len(groups)
        metric_px = slot["table"].get("metric_size", FLOOR)
        name_px = slot["table"].get("name_size", FLOOR)
        note_px = slot["table"].get("note_size", FLOOR)
        tf = font("kicker_bold", TYPE["caption"])
        nf = font("body_bold", name_px)
        mf = font("caption_italic", note_px)
        metricf = font("body_bold", metric_px)
        qa.size("table_title", TYPE["caption"])
        # name_px/note_px/metric_px are person-approved exceptions when <
        # FLOOR (mirrors the sanctioned 50px benchmark-caption precedent)
        # -- "!" makes each explicit and visible in the QA log rather
        # than silently bypassed
        qa.size("!table_name" if name_px < FLOOR else "table_name", name_px)
        qa.size("!table_metric" if metric_px < FLOOR else "table_metric", metric_px)
        qa.size("!table_note" if note_px < FLOOR else "table_note", note_px)
        if "word_limit" in slot:
            qa.word_limit = slot["word_limit"]
        bottoms = []
        for gi, (gtitle, rows) in enumerate(groups):
            gx = M + gi * (col_w + gutter)
            gy = y
            tracked_text(d, (gx, gy), gtitle, tf, pal["ACCENT"], 4)
            gy += 60
            d.line([(gx, gy), (gx + col_w, gy)], fill=pal["ACCENT"], width=3)
            gy += 20
            for name, metric, note in rows:
                d.text((gx, gy), name, font=nf, fill=INK)
                if metric:
                    mw = text_w(d, metric, metricf)
                    d.text((gx + col_w - mw, gy - 4), metric, font=metricf, fill=pal["ACCENT"])
                gy += int(name_px * 1.1)
                gy = paragraph(d, (gx, gy), note, mf, MUTED, col_w, 1.08) + 8
                d.line([(gx, gy), (gx + col_w, gy)], fill=LINE, width=2)
                gy += 10
                qa.add_words(f"{metric} {note}" if metric else note)
            qa.box(f"table{gi}", (gx, y, gx + col_w, gy))
            bottoms.append(gy)
        y = max(bottoms) + 20
        if slot["table"].get("source"):
            sf = font("caption_italic", FLOOR); qa.size("table_source", FLOOR)
            d.text((M, y), slot["table"]["source"], font=sf, fill=MUTED)
            y += int(FLOOR * 1.1)

    if slot.get("columns"):
        cols = slot["columns"]
        gutter = 70
        col_w = (W - 2 * M - gutter * (len(cols) - 1)) // len(cols)
        wrap_w = col_w - 8  # guarantee clearance from the next column's gutter
        body_size = slot.get("col_body_size", TYPE["body"])
        cbf = font("body", body_size)
        bprefix = "!" if body_size < FLOOR else ""
        qa.size(f"{bprefix}col_block_body", body_size)

        # Titles wrap onto multiple lines as needed -- only an unbreakable
        # single word (no space to wrap on) forces a shrink, and even then
        # not below body_size, so the title always reads larger than the
        # body copy underneath it.
        lead_size = slot.get("col_lead_size", TYPE["lead"] + 10)
        floor = body_size + 6
        ctf = font("display_bold", lead_size)
        def longest_word_w(f):
            return max(text_w(d, w, f) for ctitle, _ in cols for w in ctitle.split(" "))
        while longest_word_w(ctf) > wrap_w and lead_size > floor:
            lead_size -= 2
            ctf = font("display_bold", lead_size)
        prefix = "!" if lead_size < TYPE["lead"] else ""
        qa.size(f"{prefix}col_block_title", lead_size, headline=True)

        la, ld = ctf.getmetrics()
        title_lh = int((la + ld) * 1.0)
        bottoms = []
        for ci, (ctitle, cbody) in enumerate(cols):
            cx = M + ci * (col_w + gutter)
            cy = y
            if text_w(d, ctitle, ctf) <= wrap_w:
                title_lines = [ctitle]
            else:
                title_lines = wrap(d, ctitle, ctf, wrap_w)
            for ln in title_lines:
                d.text((cx, cy), ln, font=ctf, fill=pal["LEAD"])
                cy += title_lh
            cy += 20
            e = paragraph(d, (cx, cy), cbody, cbf, INK, wrap_w, 1.32)
            qa.add_words(cbody)
            qa.box(f"!colblock{ci}", (cx, y, cx + col_w, e))
            bottoms.append(e)
        y = max(bottoms) + 20

    if slot.get("grid_table"):
        gt = slot["grid_table"]
        col_heads = gt["col_heads"]
        rows = gt["rows"]  # [(row_label, [cell1, cell2, ...]), ...]
        label_w = gt.get("label_w", 340)
        n_cols = len(col_heads)
        gutter = gt.get("col_gutter", 70)
        data_w = (W - 2 * M - label_w - gutter * n_cols) // n_cols
        hf = font("kicker_bold", 44)
        rlf = font("display_bold", gt.get("row_label_size", 52))
        cf = font("body", gt.get("cell_size", 48))
        qa.size("!grid_head", 44)
        qa.size("!grid_row_label", gt.get("row_label_size", 52), headline=False)
        qa.size("!grid_cell", gt.get("cell_size", 48))
        y += 10
        hy = y
        col_x = [M + label_w + gutter + i * (data_w + gutter) for i in range(n_cols)]
        for i, head in enumerate(col_heads):
            tracked_text(d, (col_x[i], hy), head.upper(), hf, pal["ACCENT"], 3)
        hy += 56
        d.line([(M, hy), (W - M, hy)], fill=pal["ACCENT"], width=3)
        y = hy + 40
        row_gap = gt.get("row_gap", 46)
        for row_label, cells in rows:
            row_top = y
            label_lines = wrap(d, row_label, rlf, label_w)
            rla, rld = rlf.getmetrics()
            rl_lh = int((rla + rld) * 1.08)
            ly = y
            for ln in label_lines:
                d.text((M, ly), ln, font=rlf, fill=pal["SIGNATURE"])
                ly += rl_lh
            max_cell_bottom = ly
            ca, cd = cf.getmetrics()
            cell_lh = int((ca + cd) * 1.28)
            for i, cell in enumerate(cells):
                lines = wrap(d, cell, cf, data_w)
                cy2 = y
                for ln in lines:
                    d.text((col_x[i], cy2), ln, font=cf, fill=INK)
                    cy2 += cell_lh
                max_cell_bottom = max(max_cell_bottom, cy2)
                qa.add_words(cell)
            qa.box(f"!gridrow{row_label}", (M, row_top, W - M, max_cell_bottom))
            y = max_cell_bottom + row_gap
            d.line([(M, y - row_gap // 2), (W - M, y - row_gap // 2)], fill=LINE, width=1)

    for item in slot.get("items", []):
        y0 = y
        if len(item) == 3:
            # Optional third element: a small thumbnail photo run beside
            # the lead+body text instead of full-width, e.g. a fruit/
            # texture shot illustrating that specific item. Backward
            # compatible -- existing (lead, body) 2-tuples elsewhere in
            # the system are untouched, this only triggers on a 3-tuple.
            lead, body, item_photo = item
            thumb_size = slot.get("item_thumb_size", 200)
            # Align the photo's top edge to the lead word's actual glyph
            # ink top (measured via textbbox), not the nominal y coordinate
            # run_in draws from -- Playfair Bold's ascent leaves visible
            # padding above the cap-height, so a naive same-y placement
            # left the photo sitting visibly higher than the text.
            lead_size = slot.get("lead_size", TYPE["lead"])
            lf_probe = font("display_bold", lead_size)
            probe_bbox = d.textbbox((M, y), lead, font=lf_probe)
            photo_y = probe_bbox[1]
            thumb = cover_fit(load_photo(item_photo), thumb_size, thumb_size)
            img.paste(thumb, (M, photo_y))
            d = ImageDraw.Draw(img)
            text_x = M + thumb_size + 32
            text_max_w = W - M - text_x
            text_bottom = run_in(d, (text_x, y), lead, body, text_max_w, pal)
            y = max(text_bottom, photo_y + thumb_size) + slot.get("item_gap", 56)
        else:
            lead, body = item
            y = run_in(d, (M, y), lead, body, W - 2 * M, pal) + slot.get("item_gap", 56)
        qa.box(f"runin:{lead}", (M, y0, W - M, y - slot.get("item_gap", 56)))
        qa.add_words(body)
    qa.size("lead", TYPE["lead"]); qa.size("body", TYPE["body"])
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


# ───────────────────────── M03 SIDE RAIL ─────────────────────────
def side_rail(slot, slide_no, total, pal):
    """slots: photo, photo_caption, photo_credit(optional small-print
    attribution, rendered in the text column, not overlaid on the
    photo), side('left'|'right'), kicker, headline(may '\\n'),
    standfirst, items[(lead, body)], lists(optional), famous(optional list[str])"""
    img, d, qa = _start("M03 side_rail", slide_no, total, pal)
    rail_w = 860
    px = 0 if slot.get("side", "left") == "left" else W - rail_w
    tx = rail_w + 70 if px == 0 else M
    col_w = W - tx - M if px == 0 else W - rail_w - M - 70
    img.paste(cover_fit(load_photo(slot["photo"]), rail_w, H), (px, 0))
    d = ImageDraw.Draw(img)

    # The caption is measured BEFORE the scrim is drawn, so the gradient
    # can be sized to it. A fixed 320px scrim is bottom-dark, meaning it
    # is at zero strength at its own top edge -- so a two- or three-line
    # caption pushed its first line above the protected zone and onto
    # bare photograph. Starting the gradient a comfortable margin above
    # the caption block means every line gets cover regardless of how
    # many there are, without a chip sitting on the image.
    cap_lines, cf, cap_lh, cap_y0 = None, None, 0, H - 240
    if slot.get("photo_caption"):
        cf = font(core.CAPTION_FACE, core.CAPTION_SIZE); qa.size("cap", core.CAPTION_SIZE)
        cap_lines = wrap(d, slot["photo_caption"], cf, rail_w - 80)
        ca, cd = cf.getmetrics()
        cap_lh = int((ca + cd) * 1.10)
        cap_y0 = H - 240 - (len(cap_lines) - 1) * cap_lh

    # Long and soft rather than short and strong. A 240px ramp at 0.80
    # has a visible top edge running across the photograph, which reads
    # as an overlay sitting on the image; the same darkening spread over
    # ~600px reads as depth of field and has no discernible start.
    scrim_top = min(H - 340, cap_y0 - 620)
    scrim(img, (px, scrim_top, px + rail_w, H), "bottom", 0.88)
    d = ImageDraw.Draw(img)

    # Flat chip for the footer row when the photo is on the LEFT, which
    # is the side the swipe cue and page number sit on. scrim() fades to
    # zero at its far edge by design, so a light patch of photo right
    # under the label can still read weak; chip() gives a guaranteed
    # uniform patch.
    #
    # This runs HERE, before the caption, rather than just before
    # _finish() where it used to. Drawn afterwards it landed on top of
    # the finished caption and knocked the white back to grey -- which is
    # the "caption is shaded somehow" symptom, and it appeared only on
    # left-side photos, which is why the right-side slides looked clean.
    # Order is the whole fix; the chip itself was always correct.
    if px == 0:
        chip(img, (px, H - 320, px + rail_w, H), (0, 0, 0), opacity=0.55)
        d = ImageDraw.Draw(img)

    if cap_lines:
        # caption_chip is opt-in, not the default. It was added when
        # captions were still Cormorant Italic and the gradient alone
        # could not hold them; now that captions set in Archivo Bold at
        # CAPTION_SIZE over a correctly-sized gradient, the chip is
        # redundant and reads as a grey box on the photograph. Kept for a
        # genuinely bright or busy image where the gradient is not enough.
        if slot.get("caption_chip"):
            cap_w = max(text_w(d, ln, cf) for ln in cap_lines)
            chip(img, (px + 16, cap_y0 - 18, min(px + rail_w, px + 40 + cap_w + 28),
                       cap_y0 + cap_lh * len(cap_lines) + 6), INK, opacity=0.72)
            d = ImageDraw.Draw(img)
        cy = cap_y0
        for ln in cap_lines:
            d.text((px + 40, cy), ln, font=cf, fill=(255, 255, 255))
            cy += cap_lh
    if slot.get("photo_credit"):
        # credit lives in the text column, not on the photo -- side_rail's
        # photo occupies a full-height half of the canvas, so the generic
        # footer-gutter centering (which assumes a full-width photo-free
        # strip) would land the credit right at or on the image edge.
        # Wrapped here to the actual clear column width instead.
        cf2 = font("body", 34)
        credit_lines = wrap(d, slot["photo_credit"], cf2, col_w)
        ca2, cd2 = cf2.getmetrics()
        credit_lh = int((ca2 + cd2) * 1.1)
        # Sit the block ABOVE the footer row, not on it. The old baseline
        # put the last credit line on FOOTER_Y at the text column's x --
        # which, whenever the photo is on the right, is the left margin,
        # exactly where the read-more cue is drawn. A one-line credit then
        # overprinted the footer label on every right-side slide. Lifting
        # the whole block by one line height puts it in the gutter above,
        # clear of the footer furniture at either side setting.
        credit_y0 = FOOTER_Y - 4 - len(credit_lines) * credit_lh
        cy2 = credit_y0
        for ln in credit_lines:
            d.text((tx, cy2), ln, font=cf2, fill=MUTED)
            cy2 += credit_lh
    y = 170
    if slot.get("kicker"):
        y = kicker_block(d, slot["kicker"], pal, x=tx, y=170); qa.size("kicker", 70)
    hf = font("display_black", TYPE["display_md"])
    qa.size("headline", TYPE["display_md"], headline=True)
    ha, hd = hf.getmetrics()
    headline_lines = []
    for raw_ln in slot["headline"].split("\n"):
        headline_lines.extend(wrap(d, raw_ln, hf, col_w))
    for ln in headline_lines:
        d.text((tx, y), ln, font=hf, fill=pal["SIGNATURE"])
        y += int((ha + hd) * 0.96)
    y = standfirst(d, (tx, y + 16), slot["standfirst"], col_w, leading=1.2) + 56
    qa.size("standfirst", TYPE["standfirst"])
    # optional side-by-side lists: lists=[(title,[(name, gloss|None),...]) x2]
    if slot.get("lists"):
        # lists=[(title, [(subhead|None, [(name, gloss|None), ...]), ...]), ...]
        # groups let a column carry e.g. International (bare, light,
        # quick-scan) then Indigenous (bold, accent-dot, glossed) under
        # one heading -- the weight contrast IS the hierarchy, so a
        # reader doesn't need to parse the subhead labels to feel which
        # grapes are the ones worth remembering.
        lists = slot["lists"]
        gutter = 48
        lw = (col_w - gutter * (len(lists) - 1)) // len(lists)
        isz = slot.get("list_size", 56)
        tf2 = font("kicker_bold", TYPE["caption"])
        subf = font("kicker_bold", FLOOR)
        lightf = font("body_light", isz)
        nf2 = font("body_bold", isz)
        gf2 = font("caption_italic", max(FLOOR, isz - 4))
        qa.size("list_title", TYPE["caption"]); qa.size("list_item", isz)
        qa.size("list_sub", FLOOR); qa.size("list_gloss", max(FLOOR, isz - 4))
        bottoms = []
        for li, (ltitle, groups) in enumerate(lists):
            lx = tx + li * (lw + gutter)
            ly = y
            tracked_text(d, (lx, ly), ltitle, tf2, pal["ACCENT"], 4)
            d.line([(lx, ly + 72), (lx + lw, ly + 72)], fill=pal["ACCENT"], width=3)
            ly += 104
            for gi, (subhead, items) in enumerate(groups):
                if gi:
                    ly += 26
                bold_group = gi > 0  # first group per column = International
                if subhead:
                    tracked_text(d, (lx, ly), subhead, subf, MUTED, 3)
                    d.line([(lx, ly + 52), (lx + 64, ly + 52)], fill=MUTED, width=2)
                    ly += 92
                for iname, gloss in items:
                    if bold_group:
                        r = 6
                        d.ellipse([lx, ly + isz * 0.42 - r, lx + 2 * r, ly + isz * 0.42 + r],
                                  fill=pal["SIGNATURE"])
                        d.text((lx + 26, ly), iname, font=nf2, fill=INK)
                    else:
                        d.text((lx, ly), iname, font=lightf, fill=INK)
                    ly += int(isz * 1.14)
                    if gloss:
                        ly = paragraph(d, (lx + (26 if bold_group else 0), ly), gloss, gf2,
                                       MUTED, lw - (26 if bold_group else 0), 1.08) + 12
            qa.box(f"list{li}", (lx, y, lx + lw, ly))
            bottoms.append(ly)
        y = max(bottoms) + 44
    for lead, body in slot["items"]:
        y0 = y
        y = run_in(d, (tx, y), lead, body, col_w, pal,
                   lead_size=slot.get("item_lead_size", 68),
                   body_size=slot.get("item_body_size", TYPE["body"])) + slot.get("item_gap", 50)
        qa.box(f"runin:{lead}", (tx, y0, tx + col_w, y - 50))
        qa.add_words(body)
    if slot.get("famous"):
        y += 40
        fy = famous_names(d, (tx, y), slot["famous"], col_w, pal)
        qa.size("famous", TYPE["caption"])
        qa.box("famous", (tx, y, tx + col_w, fy))
        y = fy
    if slot.get("dashboard"):
        import quick_sips  # lazy import: quick_sips imports from this module, so
        y += 30            # importing it at module load time would be circular
        dash_kwargs = {k: slot[k] for k in ("header_gap", "pre_row_gap", "row_gap") if k in slot}
        y = quick_sips.qs_tasting_dashboard(d, y, tx, col_w, pal, qa, slot["dashboard"], **dash_kwargs)
    qa.size("lead", 68); qa.size("body", TYPE["body"])
    # NOTE: photo_credit is already drawn above (wrapped to the text
    # column, per this module's docstring) -- passing credit= to
    # _finish() here as well double-renders it via the default centered
    # footer treatment, colliding with the read-more label. Omit it.
    # The read-more/page-number label always sits bottom-left (x=M).
    # When the photo is on that side (side="left"), the existing bottom
    # scrim() gradient is sometimes not enough on its own -- scrim fades
    # to zero strength at its far edge by design (see scrim()'s
    # docstring), so a light patch of photo right where the label sits
    # can still read weak. chip() gives a flat, guaranteed-uniform patch
    # with no such weak edge; use it here instead of cropping the photo
    # to hide the light area (which was tried and cost real image
    # content -- see git history) or forcing a shared footer_fill color
    # (which would also wash out the page-number on the paper side).
    # (The px == 0 footer chip that used to sit here now runs earlier,
    # before the caption is drawn -- see the photo block above.)
    # footer_adaptive, so the page number picks its own colour from what
    # is actually behind it. The note above is right that a single forced
    # footer_fill is wrong -- but it assumed the page number always lands
    # on paper, which only holds when the photo is on the LEFT. With
    # side="right" the number sits at x=W-M, on the photo, over the dark
    # chip, and default MUTED left it barely legible. Per-element
    # luminance sampling gets both sides right without forcing either.
    return _finish(img, d, qa, slide_no, total, footer_adaptive=True)


# ───────────────────────── M04 STAT WALL ─────────────────────────
def stat_wall(slot, slide_no, total, pal):
    """slots: kicker, headline, standfirst, stats[(number, label2line, note)x4-8] grid 2xN,
    famous(optional list[str])"""
    img, d, qa = _start("M04 stat_wall", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y = standfirst(d, (M, y + 8), slot["standfirst"], W - 2 * M) + 70
    qa.size("standfirst", TYPE["standfirst"])
    stats = slot["stats"]
    cols, gap = 2, 80
    col_w = (W - 2 * M - gap) // 2
    rows = (len(stats) + 1) // 2
    famous_reserve = 230 if slot.get("famous") else 0
    cell_h = (CONTENT_BOTTOM - y - 20 - famous_reserve) // rows
    nf = font("display_bold", 150); lf = font("body_bold", 76)
    df = font("body", 64)
    qa.size("stat_num", 150, headline=True); qa.size("stat_label", 76); qa.size("stat_note", 64)
    for i, (num, label, note) in enumerate(stats):
        cx = M + (i % 2) * (col_w + gap)
        cy = y + (i // 2) * cell_h
        d.line([(cx, cy), (cx, cy + cell_h - 60)], fill=pal["SIGNATURE"], width=4)
        d.text((cx + 36, cy - 14), num, font=nf, fill=pal["SIGNATURE"])
        yy = cy + 172
        yy = paragraph(d, (cx + 36, yy), label, lf, INK, col_w - 40, 1.12)
        paragraph(d, (cx + 36, yy + 6), note, df, MUTED, col_w - 40, 1.18)
        qa.box(f"stat{i}", (cx, cy, cx + col_w, cy + cell_h - 60))
        qa.add_words(label + " " + note)
    if slot.get("famous"):
        fy = y + rows * cell_h + 30
        famous_names(d, (M, fy), slot["famous"], W - 2 * M, pal)
        qa.size("famous", TYPE["caption"])
    return _finish(img, d, qa, slide_no, total)


# ─────────────────────────── M05 DUEL ───────────────────────────
def duel(slot, slide_no, total, pal):
    """slots: photos(left,right), labels(left,right), kicker, headline, standfirst,
    mode('table'|'columns'); table: rows[(attr,l,r)]; columns: cols[(head,body)x2].
    photo_position('top'|'bottom', default 'top') -- 'bottom' flips the
    layout so kicker/headline/standfirst/content render first and the
    split photo band sits at the bottom of the slide instead of the
    top. The bottom band stops short of the footer row rather than
    running to the canvas edge, so the footer sits on plain paper
    underneath it instead of needing its own scrim on top of a photo."""
    img, d, qa = _start("M05 duel", slide_no, total, pal)
    # photos is optional. Split Decision's question slide wants the two
    # poles carried by the columns alone: a photo band there means
    # captioning two images with the names of processes neither of them
    # depicts, and duplicating the column heads while doing it. Omit
    # "photos" and the band is skipped entirely; every existing caller
    # passes it, so nothing changes for them.
    has_band = bool(slot.get("photos"))
    photo_position = slot.get("photo_position", "top")
    band_h = 900 if photo_position == "top" else 760
    half = W // 2

    def _draw_band(top):
        nonlocal d
        img.paste(cover_fit(load_photo(slot["photos"][0]), half, band_h), (0, top))
        img.paste(cover_fit(load_photo(slot["photos"][1]), W - half, band_h), (half, top))
        d = ImageDraw.Draw(img)
        d.line([(half, top), (half, top + band_h)], fill=(247, 244, 236), width=2)
        scrim(img, (0, top + band_h - 220, W, top + band_h), "bottom", 0.62)
        d = ImageDraw.Draw(img)
        llf = font("display_bold", 74); qa.size("band_label", 74)
        d.text((M, top + band_h - 150), slot["labels"][0], font=llf, fill=PAPER)
        rw = text_w(d, slot["labels"][1], llf)
        d.text((W - M - rw, top + band_h - 150), slot["labels"][1], font=llf, fill=PAPER)

    if has_band and photo_position == "top":
        _draw_band(0)
        y = kicker_block(d, slot["kicker"], pal, y=band_h + 46); qa.size("kicker", 70)
    else:
        y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y = standfirst(d, (M, y + 6), slot["standfirst"], W - 2 * M, leading=1.12) + 60
    qa.size("standfirst", TYPE["standfirst"])
    content_bottom = y
    if slot.get("mode", "table") == "table":
        label_w, gutter = 410, 60
        col_w = (W - 2 * M - label_w - gutter) // 2
        xl, xc, xr = M, M + label_w, M + label_w + col_w + gutter
        chf = font("display_bold", 78); qa.size("col_head", 78)
        d.text((xc, y), slot["col_heads"][0], font=chf, fill=pal["SIGNATURE"])
        d.text((xr, y), slot["col_heads"][1], font=chf, fill=pal["ACCENT"])
        cha, chd = chf.getmetrics()
        qa.box("col_heads", (xc, y, W - M, y + int((cha + chd) * 0.9)))
        ry = y + int((cha + chd) * 0.9) + 60
        rf = font("body", TYPE["body"]); rlf = font("body_bold", TYPE["body"])
        qa.size("row", TYPE["body"])
        rows = slot["rows"]
        ra, rd = rlf.getmetrics()
        row_lh = int((ra + rd) * 0.98)
        label_max_w = label_w - 24  # small clearance before the Clare Valley column starts
        wrapped_attrs = [wrap(d, attr, rlf, label_max_w) for attr, _, _ in rows]
        wrapped_lv = [wrap(d, lv, rf, col_w - 24) for _, lv, _ in rows]
        wrapped_rv = [wrap(d, rv, rf, col_w - 24) for _, _, rv in rows]
        val_lh = int((ra + rd) * 1.05)
        bottom_limit = (FOOTER_Y - 40 - band_h) if (has_band and photo_position == "bottom") else CONTENT_BOTTOM
        base_pitch = min(160, (bottom_limit - ry) // len(rows))
        for i, (attr, lv, rv) in enumerate(rows):
            attr_lines = wrapped_attrs[i]
            lv_lines = wrapped_lv[i]
            rv_lines = wrapped_rv[i]
            ly = ry
            for ln in attr_lines:
                d.text((xl, ly), ln, font=rlf, fill=INK)
                ly += row_lh
            lvy = ry
            for ln in lv_lines:
                d.text((xc, lvy), ln, font=rf, fill=INK)
                lvy += val_lh
            rvy = ry
            for ln in rv_lines:
                d.text((xr, rvy), ln, font=rf, fill=INK)
                rvy += val_lh
            row_bottom = max(ly, lvy, rvy)
            qa.add_words(attr + " " + lv + " " + rv)
            qa.box(f"row_label{i}", (xl, ry, xc - 24, ly))
            qa.box(f"row_val_l{i}", (xc, ry, xc + col_w, lvy))
            qa.box(f"row_val_r{i}", (xr, ry, xr + col_w, rvy))
            pitch = max(base_pitch, row_bottom - ry + 34)
            ry += pitch
            if i < len(rows) - 1:
                d.line([(M, ry - pitch // 2 + 34), (W - M, ry - pitch // 2 + 34)], fill=LINE, width=1)
        d.line([(xr - gutter // 2, y + 110), (xr - gutter // 2, ry - pitch + 80)], fill=LINE, width=1)
        content_bottom = ry - pitch + row_bottom - ry
    else:
        col_gap = 90
        col_w = (W - 2 * M - col_gap) // 2
        hf2 = font("display_bold", 66); qa.size("col_head", 66)
        # Column heads now wrap instead of assuming they always fit on
        # one line -- a long head used to run straight off the edge of
        # its column (and into the next one) with no indication
        # anything was wrong. Both heads bottom-align to the taller
        # one's line count, same fix as feature_trio's A/B/C headers,
        # so the underline and body start at the same row in both
        # columns regardless of whether one head wrapped and the
        # other didn't.
        ha, hd = hf2.getmetrics()
        head_lh = int((ha + hd) * 1.05)
        wrapped_heads = [wrap(d, head, hf2, col_w) for head, _b in slot["cols"]]
        max_head_lines = max(len(lines) for lines in wrapped_heads)
        for i, (head, body) in enumerate(slot["cols"]):
            x = M + i * (col_w + col_gap)
            accent = pal["SIGNATURE"] if i == 0 else pal["ACCENT"]
            lines = wrapped_heads[i]
            hy = y + (max_head_lines - len(lines)) * head_lh
            for ln in lines:
                d.text((x, hy), ln, font=hf2, fill=accent)
                hy += head_lh
            underline_y = y + max_head_lines * head_lh + 18
            d.line([(x, underline_y), (x + col_w, underline_y)], fill=accent, width=3)
            e = paragraph(d, (x, underline_y + 38), body, font("body", TYPE["body"]), INK, col_w, 1.34)
            qa.box(f"col{i}", (x, y, x + col_w, e))
            qa.add_words(body)
            content_bottom = max(content_bottom, e)
        qa.size("body", TYPE["body"])
    if has_band and photo_position == "bottom":
        # Band sits just below where the content actually ends, not
        # anchored to the footer -- anchoring to the footer left a big
        # empty gap between the text and the photos whenever the text
        # was shorter than the available space. Clamped so it can
        # never run past the footer-safe max, even if content is long.
        band_top = min(content_bottom + 70, FOOTER_Y - 30 - band_h)
        _draw_band(band_top)
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


# ──────────────────────── M06 PROCESS MAP ────────────────────────
def process_map(slot, slide_no, total, pal):
    """slots: photos[3], kicker, headline, columns[(title, steps[(text,is_decision)])x3]
    photo_credit(optional). Steps are numbered sequentially across all
    columns (1 at the first step of column 0, continuing through the
    last step of the final column) -- callers do not supply numbers,
    the module assigns them in column order. Columns may have
    different step counts; each column spaces its own steps evenly
    from flow_top to flow_bottom independently, so tops and bottoms
    still align across columns of different lengths."""
    img, d, qa = _start("M06 process_map", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y = photo_stripe(img, slot["photos"], int(y) + 20, 440)
    d = ImageDraw.Draw(img)
    cols = slot["columns"]
    col_gap = 30
    col_w = (W - 2 * M - (len(cols) - 1) * col_gap) // len(cols)
    title_f = font("display_bold", 68); qa.size("!col_title", 68)
    node_f = font("body_bold", 64); qa.size("!node", 64)
    badge_f = font("body_bold", 68); qa.size("badge", 68)
    tb_top = y + 24
    ta, td = title_f.getmetrics()
    title_lh = int((ta + td) * 1.05)
    tb_h = title_lh + 40
    rect_h, dia_h = 320, 360
    badge_r = 50
    # Badge now floats fully outside the box (above the top-left
    # corner) instead of inset inside it -- the gap before the first
    # row has to clear the badge's full footprint above the box, not
    # just half the box height, since nothing about the badge sits
    # inside the box anymore.
    flow_top = tb_top + tb_h + rect_h // 2 + 20 + (badge_r if slot.get("show_numbers", True) else 0)
    flow_bottom = CONTENT_BOTTOM - 160
    # No badge to dodge inside the box anymore, so the full column
    # width is available for text -- previously this was narrowed to
    # leave room for the badge in the corner.
    node_w = col_w - 10
    DIA = pal["LEAD"]
    step_no = 1
    for ci, (title, steps) in enumerate(cols):
        x = M + ci * (col_w + col_gap)
        cx = x + col_w // 2
        title_lines = wrap(d, title, title_f, col_w)
        ty = tb_top + (tb_h - len(title_lines) * title_lh) // 2
        for ln in title_lines:
            lw = text_w(d, ln, title_f)
            d.text((cx - lw // 2, ty), ln, font=title_f, fill=DIA)
            ty += title_lh
        n = len(steps)
        centers = ([flow_top] if n == 1 else
                   [flow_top + i * (flow_bottom - flow_top) / (n - 1) for i in range(n)])
        for i in range(1, n):
            y0, y1 = centers[i - 1] + rect_h // 2, centers[i] - rect_h // 2
            d.line([(cx, y0), (cx, y1 - 4)], fill=pal["SIGNATURE"], width=4)
            d.polygon([(cx - 12, y1 - 16), (cx + 12, y1 - 16), (cx, y1)], fill=pal["SIGNATURE"])
        for i, (text, dec) in enumerate(steps):
            cy = int(centers[i])
            # Up to 3 lines now, not a hard cap of 2 -- silently
            # slicing to [:2] was dropping the tail end of any line
            # that needed a 3rd line (e.g. "...build as it ripens"
            # was losing "ripens" with no indication anything had
            # been cut). rect_h is generous enough at this font size
            # to hold 3 full lines with room to spare.
            lines = wrap(d, text, node_f, node_w - 50)[:3]
            if dec:
                d.polygon([(cx, cy - dia_h // 2), (cx + node_w // 2, cy),
                           (cx, cy + dia_h // 2), (cx - node_w // 2, cy)], fill=DIA)
            else:
                d.rounded_rectangle([cx - node_w // 2, cy - rect_h // 2,
                                     cx + node_w // 2, cy + rect_h // 2],
                                    radius=14, fill=pal["SIGNATURE"])
            na, nd = node_f.getmetrics()
            line_h = int((na + nd) * 1.05)
            block_h = line_h * len(lines)
            # Full box height available now -- text centers on cy
            # directly since the badge no longer claims any of the
            # interior.
            ly0 = cy - block_h // 2
            for ln in lines:
                tb = d.textbbox((0, 0), ln, font=node_f)
                d.text((cx - (tb[2] - tb[0]) / 2, ly0 - tb[1]), ln, font=node_f, fill=PAPER)
                ly0 += line_h
            # Number badge floats above the box's top-left corner,
            # entirely outside its bounds -- reads as a tag rather
            # than competing with the text for the same interior
            # space, and means box size no longer has to compromise
            # between fitting the badge and fitting the words.
            # show_numbers=False for any process_map whose columns are
            # parallel rather than sequential. The badges number
            # continuously across all columns, so a three-column layout
            # showing a problem, a procedure and a contrast reads as one
            # eleven-step process that runs left to right -- which is not
            # what the diagram says. Arrows inside each column already
            # carry the order that does exist.
            if slot.get("show_numbers", True):
                bx = cx - node_w // 2 + badge_r
                by = cy - rect_h // 2 - badge_r - 14
                d.ellipse([bx - badge_r, by - badge_r, bx + badge_r, by + badge_r],
                          fill=pal["ACCENT"], outline=PAPER, width=3)
                num_s = str(step_no)
                ntb = d.textbbox((0, 0), num_s, font=badge_f)
                d.text((bx - (ntb[2] - ntb[0]) / 2, by - (ntb[3] - ntb[1]) / 2 - ntb[1]),
                       num_s, font=badge_f, fill=PAPER)
            qa.add_words(text)
            step_no += 1
        qa.box(f"flow{ci}", (x, tb_top, x + col_w, flow_bottom + rect_h // 2))
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


# ───────────────────────── M07 CARD GRID ─────────────────────────
def card_grid(slot, slide_no, total, pal):
    """slots: kicker, headline, standfirst, cards[(icon_photo|None, title, sub, body)xN],
    bottom_stripe(optional [photos]), stripe_captions(optional),
    photo_credit(optional small-print attribution for any card icon_photo
    or bottom_stripe photo that carries a license obligation -- rendered
    in the footer gutter via _finish(), same as every other photo-bearing
    module. Previously missing from this module's _finish() call, a real
    gap since bottom_stripe photos are full content images, not
    decoration; fixed rather than worked around.

    row_layout (optional list of ints, e.g. [3, 2]) controls how many
    cards sit in each row -- lets card counts other than 4 (e.g. 5
    cards as 3-over-2, grouping by some category) lay out cleanly
    instead of forcing a fixed 2-column grid. Defaults to 2-per-row
    (the original behavior) if omitted, so existing 4-card decks are
    unaffected. Column width is computed per-row from that row's own
    card count, so a 3-card row and a 2-card row on the same slide
    each get proportionally sized columns rather than one fixed width.
    Row heights are weighted by column count (a 3-col row gets more of
    the vertical budget than a 2-col row on the same slide), since a
    narrower column wraps its body text to more lines and needs the
    room -- for the original 2/2 case this weighting reduces to an
    even split, so existing decks render identically."""
    img, d, qa = _start("M07 card_grid", slide_no, total, pal)
    # top_margin lets a deck pull the kicker/headline/standfirst block
    # up toward the canvas top (default 170, matching kicker_block's
    # own default) -- useful when a bottom photo stripe needs the
    # vertical room reclaimed from a smaller top margin instead of
    # crowding the footer.
    top_margin = slot.get("top_margin", 170)
    y = kicker_block(d, slot["kicker"], pal, y=top_margin); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y = standfirst(d, (M, y + 6), slot["standfirst"], W - 2 * M, leading=1.14) + 60
    qa.size("standfirst", TYPE["standfirst"])
    stripe = slot.get("bottom_stripe")
    # Taller than the shared BAND_TALL constant when captions are
    # present -- the caption+footer scrim eats into the bottom of the
    # stripe, and at the shared default height that left too little of
    # each photo actually visible above the text. Local to this
    # module's stripe only; doesn't touch BAND_TALL itself since other
    # modules' photo bands are tuned for that height already.
    stripe_h = int(BAND_TALL * 1.15) if stripe else 0
    # The stripe now stops short of the footer row entirely (bottom =
    # FOOTER_Y - 30) instead of running to the canvas edge -- the
    # photos sit fully above the footer, and the footer renders on the
    # plain paper background below them, not on top of a photo. This
    # replaces the old approach of scrimming the photo to make footer
    # text legible on top of it.
    stripe_bottom = (FOOTER_Y - 30) if stripe else H
    stripe_top = stripe_bottom - stripe_h
    gap_x = 110
    cards = slot["cards"]
    row_layout = slot.get("row_layout") or ([2] * (len(cards) // 2) + ([len(cards) % 2] if len(cards) % 2 else []))
    assert sum(row_layout) == len(cards), "row_layout must account for every card"
    n_rows = len(row_layout)
    zone_bottom = (stripe_top - 40) if stripe else CONTENT_BOTTOM
    avail_h = zone_bottom - y
    weight_total = sum(row_layout)
    tf = font("display_bold", 66); pf = font("body_bold", TYPE["caption"])
    bf = font("body", FLOOR)
    qa.size("card_title", 66); qa.size("card_sub", TYPE["caption"]); qa.size("card_body", FLOOR)
    idx = 0
    row_top = y
    photo_style = slot.get("photo_style", "icon")
    for r, n_cols in enumerate(row_layout):
        row_h = int(avail_h * n_cols / weight_total)
        col_w = (W - 2 * M - gap_x * (n_cols - 1)) // n_cols
        cy = row_top
        for c in range(n_cols):
            icon, title, sub, body = cards[idx]
            cx = M + c * (col_w + gap_x)
            tx = cx
            if photo_style == "top" and icon:
                photo_h = int(row_h * 0.40)
                img.paste(cover_fit(load_photo(icon), col_w, photo_h), (cx, cy))
                d = ImageDraw.Draw(img)
                ty0 = cy + photo_h + 30
                d.text((cx, ty0 - 4), title, font=tf, fill=INK)
                sub_lines = wrap(d, sub, pf, col_w)
                pa, pd = pf.getmetrics()
                sub_line_h = int((pa + pd) * 0.94)
                sy = ty0 + 76
                for ln in sub_lines:
                    d.text((cx, sy), ln, font=pf, fill=pal["ACCENT"])
                    sy += sub_line_h
                divider_y = sy + 14
                d.line([(cx, divider_y), (cx + col_w, divider_y)], fill=LINE, width=2)
                e = paragraph(d, (cx, divider_y + 26), body, bf, INK, col_w, 1.28)
                qa.box(f"card{idx}", (cx, cy, cx + col_w, e))
                qa.add_words(body)
                idx += 1
                continue
            if icon:
                fl = load_photo(icon)
                fh = 84
                fw = int(fl.size[0] * fh / fl.size[1])
                img.paste(fl.resize((fw, fh), Image.LANCZOS), (cx, cy))
                tx = cx + fw + 26
            d.text((tx, cy - 4), title, font=tf, fill=INK)
            sub_lines = wrap(d, sub, pf, col_w - (tx - cx))
            pa, pd = pf.getmetrics()
            sub_line_h = int((pa + pd) * 0.94)
            sy = cy + 80
            for ln in sub_lines:
                d.text((tx, sy), ln, font=pf, fill=pal["ACCENT"])
                sy += sub_line_h
            divider_y = sy + (150 - 80 - sub_line_h)
            d.line([(cx, divider_y), (cx + col_w, divider_y)], fill=LINE, width=2)
            e = paragraph(d, (cx, divider_y + 28), body, bf, INK, col_w, 1.28)
            qa.box(f"card{idx}", (cx, cy, cx + col_w, e))
            qa.add_words(body)
            idx += 1
        row_top += row_h
    if stripe:
        photo_stripe(img, stripe, stripe_top, stripe_h)
        d = ImageDraw.Draw(img)
        if slot.get("stripe_captions"):
            # Captions sit inside the stripe's own bottom edge (still
            # over the photos, which is fine -- a caption on a photo is
            # normal), with a scrim reaching only to stripe_bottom, not
            # down into the footer row. The footer below renders on
            # plain paper, so it needs no scrim of its own.
            cf = font(core.CAPTION_FACE, core.CAPTION_SIZE)
            ca, cd = cf.getmetrics()
            cap_y = stripe_bottom - 20 - (ca + cd)
            scrim(img, (0, cap_y - 30, W, stripe_bottom), "bottom", 0.7)
            d = ImageDraw.Draw(img)
            d.text((40, cap_y), slot["stripe_captions"][0], font=cf, fill=(255, 255, 255))
            rc = slot["stripe_captions"][1]
            d.text((W - 40 - text_w(d, rc, cf), cap_y), rc, font=cf, fill=(255, 255, 255))
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


# ─────────────────────── M08 SHOWCASE SHELF ───────────────────────
def _glass_mark_patch(img, d, pal, text, bg_color=None):
    """Quick Sips glass-glyph + custom text, on a solid color patch,
    anchored top-left. Same visual lockup as quick_sips.py's
    qs_mark_patch (colored patch, white glass icon, white text) but
    duplicated locally rather than imported -- quick_sips.py imports
    from modules.py already, so the reverse import would be circular.
    bg_color overrides the patch color (default pal['SIGNATURE']) --
    for a one-off deck that wants the mark in a specific color
    independent of the rest of the palette's use of SIGNATURE."""
    pad, gap = 40, 26
    gh = 108
    tf = font("display_bold", 90)
    tw = text_w(d, text, tf)
    asc, desc = tf.getmetrics()
    content_h = max(gh, asc + desc)
    icon = Image.open(f"{PHOTO_DIR}/QS_glass_icon.png").convert("RGBA")
    gw = int(gh * icon.size[0] / icon.size[1])
    patch_w = pad + gw + gap + tw + pad
    patch_h = pad + content_h + pad
    d.rectangle([0, 0, patch_w, patch_h], fill=bg_color or pal["SIGNATURE"])
    gy = pad + (content_h - gh) // 2
    icon = icon.resize((gw, gh), Image.LANCZOS)
    img.paste(icon, (pad, gy), icon)
    d = ImageDraw.Draw(img)
    ink_top, _, _, ink_bot = d.textbbox((0, 0), text, font=tf)
    ink_center = ink_top + (ink_bot - ink_top) / 2
    icon_center = gy + gh / 2
    ty = int(icon_center - ink_center)
    d.text((pad + gw + gap, ty), text, font=tf, fill=PAPER)
    return patch_h


def showcase_shelf(slot, slide_no, total, pal):
    """slots: kicker, headline, products[(photo, producer, name, style, origin, note)x6] 3x2.
    producer renders smaller, above the wine name, in burgundy (SIGNATURE)
    mixed-case serif -- this is now the locked default for this module,
    not a per-deck choice. name stays the larger ACCENT (gold) line below it.

    zone_h (default 420) is the bottle image's vertical budget; width_frac
    (default 0.56) caps bottle width as a fraction of the column width.
    Both are overridable per-deck to run the bottles larger -- raising
    zone_h is what actually grows a bottle image, since these are tall,
    narrow product shots and nearly always end up height-constrained,
    not width-constrained (a wider column alone doesn't make a bottle
    look bigger). show_note (default True) can be set False to drop the
    tasting-note paragraph and return that vertical space to zone_h
    instead -- the real lever for a noticeably larger bottle, since the
    name/style/origin stack alone is much shorter than a wrapped note.
    note_size (default FLOOR=60, may go smaller e.g. 55 with an explicit
    deck-owner sign-off -- tracked via the "!" QA exemption) shrinks
    just the note paragraph to buy back a little more zone_h without
    losing the note entirely. stretch_lower (default False) exempts the
    product blocks from the usual caption-zone bottom boundary, for a
    deck owner who's explicitly OK with this slide running closer to
    the page bottom than most.

    region_photos (optional): list of photo names, one per column,
    parallel to products. When given, each renders as a true full-bleed
    strip under its column (no bottom margin), height region_band_frac
    of H (default 0.25 -- the "bottom quartile" case this was built
    for). Only sensible when the product text blocks end well clear of
    that zone. Forces footer_adaptive on automatically, since the
    footer now very likely sits on photo pixels in at least the outer
    columns rather than paper."""
    img, d, qa = _start("M08 showcase_shelf", slide_no, total, pal, bg_color=slot.get("bg_color"))
    kicker_y = 150
    kicker_color = slot.get("kicker_color")
    headline_color = slot.get("headline_color", pal["SIGNATURE"])
    top_mark = slot.get("top_mark")
    if top_mark:
        mark_h = _glass_mark_patch(img, d, pal, top_mark, bg_color=slot.get("mark_bg_color"))
        d = ImageDraw.Draw(img)
        kicker_y = mark_h + 60
    y = kicker_block(d, slot["kicker"], pal, y=kicker_y, text_fill=kicker_color); qa.size("kicker", 70)
    headline_y0 = y
    has_headline = bool(slot.get("headline"))
    if has_headline:
        y = headline(d, slot["headline"], y, fill=headline_color, show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    else:
        y += 40  # same breathing room a headline's absence should still leave
                  # before the product row, so the shelf doesn't crowd the kicker
    prods = slot["products"]
    cols = slot.get("cols", 3)
    gap_x = 44
    panel_top = y + slot.get("panel_gap", 40)
    col_w = slot.get("col_w_override", (W - 2 * M - (cols - 1) * gap_x) // cols)
    col_x_positions = slot.get("col_x_positions")
    show_note = slot.get("show_note", True)
    note_size = slot.get("note_size", FLOOR)
    note_prefix = "!" if note_size < FLOOR else ""
    stretch = slot.get("stretch_lower", False)
    text_budget = (650 if show_note else 320)
    zone_h = slot.get("zone_h", 260 if show_note else 680)
    bottle_lift = slot.get("bottle_lift", 0)  # extra px of scale-height ONLY -- shelf_y
                                                # (and everything below it) stays keyed to
                                                # zone_h alone, so this purely raises the
                                                # bottle's top further above panel_top; it's
                                                # how a bottle neck reaches up behind the
                                                # headline row without moving the shelf line,
                                                # caption block, or anything below it
    width_frac = slot.get("width_frac", 0.56)
    row_h = zone_h + text_budget
    producer_f = font("display_bold", FLOOR); qa.size("producer", FLOOR)
    name_f = font("display_bold", TYPE["caption"]); qa.size("name", TYPE["caption"])
    style_f = font("italbold", TYPE["caption"]); qa.size("style", TYPE["caption"])
    org_f = font("body", FLOOR); note_f = font("body", note_size)
    qa.size("origin", FLOOR)
    producer_color = slot.get("producer_color", pal["SIGNATURE"])
    name_color = slot.get("name_color", pal["ACCENT"])
    style_color = slot.get("style_color", INK)
    origin_color = slot.get("origin_color", MUTED)
    note_color = slot.get("note_color", INK)
    shelf_rule_color = slot.get("shelf_rule_color", SHELF_RULE)
    if show_note:
        qa.size(f"{note_prefix}note", note_size)
    shelf_scrim_color = slot.get("shelf_scrim_color")
    if shelf_scrim_color:
        # full-width scrim behind the text block only -- from the shelf
        # line (bottle bottom) down to wherever the region-photo strip
        # starts (or the page bottom, if there isn't one). Drawn before
        # the product loop so bottle images/shadows -- which sit above
        # shelf_y -- paint over it normally; text drawn later in the
        # loop then lands on top of the scrim, not the other way around.
        scrim_top = panel_top + zone_h
        if slot.get("region_photos"):
            scrim_bottom = H - int(H * slot.get("region_band_frac", 0.25))
        else:
            scrim_bottom = H
        d.rectangle([0, scrim_top, W, scrim_bottom], fill=shelf_scrim_color)
    for i, (photo, producer, name, style, origin, note) in enumerate(prods):
        cx = col_x_positions[i] if col_x_positions else M + (i % cols) * (col_w + gap_x)
        cy = panel_top + (i // cols) * (row_h + 24)
        shelf_y = cy + zone_h
        bim = load_photo_rgba(photo)
        bw, bh = bim.size
        s = min(col_w * width_frac / bw, (zone_h + bottle_lift) / bh)
        nw, nh = int(bw * s), int(bh * s)
        bx = cx + (col_w - nw) // 2
        # uniform synthetic shadow -- masks the fact that source photos
        # carry inconsistent studio/lifestyle lighting of their own
        shadow_w, shadow_h = int(nw * 0.8), 22
        shadow = Image.new("RGBA", (shadow_w * 3, shadow_h * 3), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).ellipse([shadow_w, shadow_h, shadow_w * 2, shadow_h * 2],
                                        fill=(20, 16, 18, 90))
        shadow = shadow.filter(ImageFilter.GaussianBlur(14))
        img.paste(shadow, (bx + nw // 2 - shadow.width // 2, shelf_y - shadow.height // 2), shadow)
        d = ImageDraw.Draw(img)
        text_w_budget = col_w - 14  # clearance from the next column, same fix as grid_table
        resized = bim.resize((nw, nh), Image.LANCZOS)
        img.paste(resized, (bx, shelf_y - nh), resized)
        d.line([(cx, shelf_y), (cx + col_w, shelf_y)], fill=shelf_rule_color, width=3)
        my = shelf_y + 22
        pa, pd = producer_f.getmetrics()
        for ln in wrap(d, producer, producer_f, text_w_budget):
            d.text((cx, my), ln, font=producer_f, fill=producer_color); my += int((pa + pd) * 0.95)
        my += 4
        na, nd = name_f.getmetrics()
        for ln in wrap(d, name, name_f, text_w_budget):
            d.text((cx, my), ln, font=name_f, fill=name_color); my += int((na + nd) * 0.92)
        sa2, sd2 = style_f.getmetrics()
        for ln in wrap(d, style, style_f, text_w_budget):
            d.text((cx, my), ln, font=style_f, fill=style_color); my += int((sa2 + sd2) * 0.94)
        my += 6
        oa2, od2 = org_f.getmetrics()
        for ln in wrap(d, origin, org_f, text_w_budget):
            d.text((cx, my), ln, font=org_f, fill=origin_color); my += int((oa2 + od2) * 1.0)
        if show_note and note:
            my += 4
            e = paragraph(d, (cx, my), note, note_f, note_color, text_w_budget, 1.18)
            qa.add_words(note)
        else:
            e = my
        box_label = f"!prod{i}" if stretch else f"prod{i}"
        qa.box(box_label, (cx, cy, cx + col_w, e))

    if bottle_lift > 0:
        # bottle necks now reach up into the kicker/headline row -- redraw
        # both on top so the type wins the overlap (renders in front of
        # the bottle glass) instead of getting silently painted over by
        # the later paste() calls above
        d = ImageDraw.Draw(img)
        if top_mark:
            pass  # mark patch is above the kicker row, never in the overlap zone
        kicker_block(d, slot["kicker"], pal, y=kicker_y, text_fill=kicker_color)
        if has_headline:
            headline(d, slot["headline"], headline_y0, fill=headline_color, show_underline=False)

    region_photos = slot.get("region_photos")
    if region_photos:
        band_h = int(H * slot.get("region_band_frac", 0.25))
        band_top = H - band_h
        names = [rp[0] if isinstance(rp, (tuple, list)) else rp for rp in region_photos]
        captions = [rp[1] if isinstance(rp, (tuple, list)) and len(rp) > 1 else None for rp in region_photos]
        photo_stripe(img, names, band_top, band_h)
        d = ImageDraw.Draw(img)
        n = len(names)
        xacc = 0
        cap_font_name = slot.get("region_caption_font", "caption_italic")
        cap_size_default = slot.get("region_caption_size", TYPE["caption"])
        for i, cap_txt in enumerate(captions):
            seg = (W - xacc) if i == n - 1 else W // n
            if cap_txt:
                # shrink-to-fit per caption -- a bold/larger caption font can
                # run wider than a given segment even when the default size
                # fits comfortably in the narrowest one; each caption gets
                # its own pass rather than one global size picked for the
                # worst case, so the other two don't render smaller than
                # they need to
                cap_size = cap_size_default
                cap_f = font(cap_font_name, cap_size)
                pad = 24
                tw = text_w(d, cap_txt, cap_f)
                while tw > seg - 2 * pad and cap_size > FLOOR:
                    cap_size -= 2
                    cap_f = font(cap_font_name, cap_size)
                    tw = text_w(d, cap_txt, cap_f)
                ca, cd = cap_f.getmetrics()
                cx0 = xacc + (seg - tw) // 2
                cap_y = H - 30 - (ca + cd)
                # no scrim/chip -- plain text, luminance-checked per spot so it
                # still reads against whatever that patch of photo happens to be
                lum = region_luminance(img, (cx0 - 10, cap_y - 10, cx0 + tw + 10, cap_y + ca + cd + 10))
                txt_fill = INK if lum > 150 else PAPER
                d.text((cx0, cap_y), cap_txt, font=cap_f, fill=txt_fill)
            xacc += seg
        qa.box("!region_photos", (0, band_top, W, H))
        if slot.get("region_credit"):
            photo_credit(img, (W - M, 60), slot["region_credit"], size=32, align="right",
                         fill=slot.get("region_credit_color", MUTED), qa=qa)

    return _finish(img, d, qa, slide_no, total, footer_label=slot.get("footer_label"),
                    footer_adaptive=bool(region_photos), show_page_num=slot.get("show_page_num", True))
def _chaikin(pts, iters=3, closed=True):
    for _ in range(iters):
        out = []
        n = len(pts)
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p, q = pts[i], pts[(i + 1) % n]
            out.append((0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]))
            out.append((0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1]))
        if not closed:
            out = [pts[0]] + out + [pts[-1]]
        pts = out
    return pts

def _darken(c, f=0.72):
    return tuple(int(v * f) for v in c)

RIVER_BLUE = (92, 148, 198)

def atlas(slot, slide_no, total, pal):
    """SWE-language cartography. All coordinates normalized 0-1 within the map box.
    slots:
      kicker, headline, map_h(optional, default 1150)
      outline: [pts]                       region/country boundary (white fill, ink line)
      regions: [dict(name, pts, fill, label(nx,ny), target(nx,ny), side('left'|'right'))]
      rivers:  [dict(pts, name, label(nx,ny), angle)]
      lakes:   [dict(pts, name(optional), label(nx,ny))]
      cities:  [(nx, ny, name)]
      context: [(nx, ny, text)]            muted italic province/neighbor names
      inset:   dict(outline=[pts], marker=(nx,ny))   locator, top-right (optional)
      legend:  [(name, note)]              key-value strip under the map
    """
    img, d, qa = _start("M09 atlas", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    map_top = y + slot.get("map_top_pad", 40)
    map_h = slot.get("map_h", 1150)
    mx0, mw = M, W - 2 * M

    def P(pt):
        return (mx0 + pt[0] * mw, map_top + pt[1] * map_h)

    # boundary outline: white ground, ink line, light Chaikin (1 pass --
    # just enough to soften pixel stair-stepping on a high-precision trace;
    # 3 passes rounds away the actual boundary shape, which is not what we
    # want when the source polygon IS the accurate geometry)
    # (optional `outlines` list draws extra landmasses, e.g. islands)
    _outl = ([slot["outline"]] if slot.get("outline") else []) + list(slot.get("outlines", []))
    for _o in _outl:
        pts = [P(p) for p in _chaikin(_o, 1, True)]
        d.polygon(pts, fill=(255, 255, 255), outline=INK)
        d.line(pts + [pts[0]], fill=INK, width=4, joint="curve")

    # optional faded latitude (or generic horizontal) bands, e.g. the
    # 30-50 degree "wine belt" in each hemisphere -- drawn over both
    # land and sea via alpha compositing, not hidden behind the outline
    for band in slot.get("lat_bands", []):
        ny_top, ny_bot = band["ny_top"], band["ny_bot"]
        color = band.get("color", pal["SIGNATURE"])
        alpha = band.get("alpha", 28)
        y0 = map_top + ny_top * map_h
        y1 = map_top + ny_bot * map_h
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([mx0, y0, mx0 + mw, y1], fill=color + (alpha,))
        img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))
        d = ImageDraw.Draw(img)

    # region polygons: fill + darker same-hue outline
    for r in slot.get("regions", []):
        pts = [P(p) for p in _chaikin(r["pts"], 1, True)]
        d.polygon(pts, fill=r["fill"])
        d.line(pts + [pts[0]], fill=_darken(r["fill"]), width=4, joint="curve")

    # lakes then rivers (tapering width), italic rotated river names
    for lk in slot.get("lakes", []):
        pts = [P(p) for p in _chaikin(lk["pts"], 3, True)]
        d.polygon(pts, fill=RIVER_BLUE)
    for rv in slot.get("rivers", []):
        pts = [P(p) for p in _chaikin(rv["pts"], 3, False)]
        n = len(pts)
        for i in range(n - 1):
            w = int(14 - 8 * (i / max(n - 2, 1)))
            d.line([pts[i], pts[i + 1]], fill=RIVER_BLUE, width=max(w, 5))
        if rv.get("name"):
            lf = font("caption_italic", FLOOR)
            tb = ImageDraw.Draw(Image.new("RGB", (10, 10))).textbbox((0, 0), rv["name"], font=lf)
            tw, th = tb[2] - tb[0] + 8, tb[3] - tb[1] + 10
            tmp = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
            ImageDraw.Draw(tmp).text((4, -tb[1] + 4), rv["name"], font=lf, fill=RIVER_BLUE)
            tmp = tmp.rotate(rv.get("angle", 0), expand=True, resample=Image.BICUBIC)
            lx, ly = P(rv["label"])
            img.paste(tmp, (int(lx), int(ly)), tmp)
            qa.size("river_label", FLOOR)
    d = ImageDraw.Draw(img)

    # cities: ink dot + label (optional 4th tuple element 'left'/'right',
    # default 'right', flips the label to the other side of the dot when
    # the default placement would collide with other map text)
    cf = font("body", FLOOR); qa.size("city", FLOOR)
    for city in slot.get("cities", []):
        nx, ny, name = city[0], city[1], city[2]
        side = city[3] if len(city) > 3 else "right"
        cx, cy = P((nx, ny))
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=INK)
        if side == "left":
            tw = text_w(d, name, cf)
            d.text((cx - 20 - tw, cy - 34), name, font=cf, fill=INK)
        else:
            d.text((cx + 20, cy - 34), name, font=cf, fill=INK)

    # context names: muted italic
    xf = font("caption_italic", 64); qa.size("context", 64)
    for (nx, ny, text) in slot.get("context", []):
        cx, cy = P((nx, ny))
        d.text((cx, cy), text, font=xf, fill=MUTED)

    # sub-region markers (optional, added for deck-level callouts like
    # Cafayate / Uco Valley): small accent dot + thin muted leader +
    # label at a staggered position. Backward-compatible: absent slot
    # renders nothing. slots: markers=[dict(name, target(nx,ny),
    # label(nx,ny), side('left'|'right'))]
    mf = font("display_bold", FLOOR + 4)
    ma, md = mf.getmetrics()
    mk_lh = int((ma + md) * 1.05)
    for mk in slot.get("markers", []):
        tx2, ty2 = P(mk["target"])
        lx2, ly2 = P(mk["label"])
        d.ellipse([tx2 - 22, ty2 - 22, tx2 + 22, ty2 + 22],
                  fill=pal["ACCENT"], outline=INK, width=4)
        name = mk["name"]
        wrap_w = mk.get("wrap_w")
        lines = wrap(d, name, mf, wrap_w) if wrap_w else [name]
        block_h = mk_lh * len(lines)
        twd = max(text_w(d, ln, mf) for ln in lines)
        side = mk.get("side", "right")
        top_y = ly2 - block_h / 2
        ty_cursor = top_y
        first_word = name.split()[0]
        anchor_letter = mk.get("anchor_letter")
        for i, ln in enumerate(lines):
            lw = text_w(d, ln, mf)
            lx_draw = (lx2 - lw) if side == "left" else lx2
            d.text((lx_draw, ty_cursor), ln, font=mf, fill=pal["SIGNATURE"])
            if i == 0:
                if anchor_letter and anchor_letter in first_word:
                    idx = first_word.index(anchor_letter)
                    x0 = text_w(d, first_word[:idx], mf)
                    x1 = text_w(d, first_word[:idx + 1], mf)
                else:
                    x0, x1 = 0, text_w(d, first_word, mf)
                anchor_x = lx_draw + (x0 + x1) / 2
                anchor_y = ty_cursor  # top of the first word's glyph box
            ty_cursor += mk_lh
        if not mk.get("no_leader"):
            d.line([(anchor_x, anchor_y), (tx2 + 13, ty2)], fill=MUTED, width=2)
        if side == "left":
            qa.box(f"mk:{name}", (lx2 - twd, top_y - 2, lx2, top_y + block_h))
        else:
            qa.box(f"mk:{name}", (lx2, top_y - 2, lx2 + twd, top_y + block_h))
        qa.size(f"mk:{name}", FLOOR + 4)

    # leader-line labels (the SWE signature)
    lbf = font("body_bold", 62); qa.size("leader_label", 62)
    for r in slot.get("regions", []):
        lx, ly = P(r["label"])
        tx, ty = P(r["target"])
        name = r["name"]
        tb = d.textbbox((0, 0), name, font=lbf)
        twd = tb[2] - tb[0]
        col = _darken(r["fill"], 0.55)
        if r.get("side", "right") == "left":
            d.text((lx - twd, ly - 34), name, font=lbf, fill=col)
            start = (lx + 12, ly)
        else:
            d.text((lx, ly - 34), name, font=lbf, fill=col)
            start = (lx - 12, ly)
        d.line([start, (tx, ty)], fill=_darken(r["fill"], 0.6), width=3)
        qa.box(f"lbl:{name}", (start[0] - twd - 12 if r.get("side") == "left" else lx,
                               ly - 36, start[0] if r.get("side") == "left" else lx + twd,
                               ly + 36))

    # state/zone header labels (v4.3): bold caps, drawn at exact map
    # positions, e.g. "SOUTH AUSTRALIA" -- distinct from region leader
    # labels (no leader line, no target dot). slot: [(nx, ny, text)]
    shf = font("body_bold", 68); qa.size("state_label", 68)
    for (nx, ny, text) in slot.get("state_labels", []):
        sx, sy = P((nx, ny))
        d.text((sx, sy), text, font=shf, fill=pal["SIGNATURE"])
        tb = d.textbbox((sx, sy), text, font=shf)
        qa.box(f"state:{text}", tb)

    # locator inset, top-right of map box. Backward compatible: plain
    # outline+marker still works. New (v4.3): optional highlight_rect
    # draws an ACCENT-stroked box over the inset ("area shown below")
    # instead of/alongside a single marker dot. New: 'outlines' (plural,
    # list of rings) for multipolygon countries with islands;
    # 'highlight_poly' (list of rings) fills a real sub-region shape in
    # SIGNATURE instead of just a marker dot or a crude axis-aligned
    # rect; 'label' draws a small caption under the frame; a bordered
    # frame is always drawn around the inset box.
    if slot.get("inset"):
        iw, ih = 340, 300
        pad = 14
        ix0, iy0 = mx0 + mw - iw, map_top
        # outer frame
        d.rectangle([ix0 - pad, iy0 - pad, ix0 + iw + pad, iy0 + ih + pad],
                    fill=(250, 248, 243), outline=INK, width=3)
        rings = slot["inset"].get("outlines") or [slot["inset"]["outline"]]
        for ring in rings:
            ipts = [(ix0 + p[0] * iw, iy0 + p[1] * ih) for p in _chaikin(ring, 3, True)]
            d.polygon(ipts, fill=(240, 236, 226), outline=INK)
            d.line(ipts + [ipts[0]], fill=INK, width=3, joint="curve")
        hp = slot["inset"].get("highlight_poly")
        if hp:
            for ring in hp:
                hpts = [(ix0 + p[0] * iw, iy0 + p[1] * ih) for p in _chaikin(ring, 2, True)]
                d.polygon(hpts, fill=pal["SIGNATURE"], outline=_darken(pal["SIGNATURE"], 0.7))
        mxp = slot["inset"].get("marker")
        if mxp:
            cx, cy = ix0 + mxp[0] * iw, iy0 + mxp[1] * ih
            mcolor = slot["inset"].get("marker_color", pal["SIGNATURE"])
            d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=mcolor, outline=PAPER, width=2)
        hl = slot["inset"].get("highlight_rect")
        if hl:
            (hx0, hy0), (hx1, hy1) = hl
            d.rectangle([ix0 + hx0 * iw, iy0 + hy0 * ih, ix0 + hx1 * iw, iy0 + hy1 * ih],
                        outline=pal["SIGNATURE"], width=4)
        if slot["inset"].get("label"):
            lf = font("kicker_bold", 44)
            lw = text_w(d, slot["inset"]["label"], lf)
            d.text((ix0 + iw - lw, iy0 + ih + pad + 14), slot["inset"]["label"],
                   font=lf, fill=MUTED)
            qa.size("!inset_label", 44)
            qa.box("inset_label", (ix0 + iw - lw, iy0 + ih + pad + 14, ix0 + iw, iy0 + ih + pad + 60))

    # legend: three text blocks (header + body), spread left / center /
    # right across the bottom of the page -- not a key-value strip
    ly2 = map_top + map_h + 56
    hf = font("display_bold", 70); bf = font("body", FLOOR)
    qa.size("legend_header", 70, headline=False); qa.size("legend_body", FLOOR)
    legend_items = slot.get("legend", [])[:3]
    n_blocks = max(len(legend_items), 1)
    block_gutter = 70
    block_w = (W - 2 * M - block_gutter * (n_blocks - 1)) // n_blocks
    bottoms = []
    for i, item in enumerate(legend_items):
        name, note = item[0], item[1]
        col = item[2] if len(item) > 2 else pal["SIGNATURE"]
        bx = M + i * (block_w + block_gutter)
        by = ly2
        d.text((bx, by), name, font=hf, fill=col)
        ha, hd = hf.getmetrics()
        by += int((ha + hd) * 0.92) + 10
        d.line([(bx, by), (bx + 70, by)], fill=col, width=3)
        by += 24
        e2 = paragraph(d, (bx, by), note, bf, INK, block_w, 1.2)
        qa.add_words(note)
        qa.box(f"legend{i}", (bx, ly2, bx + block_w, e2))
        bottoms.append(e2)
    ly2 = max(bottoms) if bottoms else ly2
    if slot.get("paragraph"):
        ly2 += slot.get("paragraph_gap", 100)
        if slot.get("paragraph_lead"):
            ly2 = run_in(d, (M, ly2), slot["paragraph_lead"], slot["paragraph"], W - 2 * M, pal,
                         lead_size=slot.get("paragraph_lead_size", TYPE["lead"]),
                         body_size=slot.get("paragraph_size", TYPE["body"]),
                         leading=slot.get("paragraph_leading", 1.34),
                         justify=slot.get("paragraph_justify", False))
        else:
            pf = font("body", slot.get("paragraph_size", TYPE["body"]))
            ly2 = paragraph(d, (M, ly2), slot["paragraph"], pf, INK, W - 2 * M, 1.32)
        qa.add_words(slot["paragraph"])
        qa.size("atlas_paragraph", slot.get("paragraph_size", TYPE["body"]))
    return _finish(img, d, qa, slide_no, total)


# ────────────────────────── M10 TIMELINE ──────────────────────────
def timeline(slot, slide_no, total, pal):
    """slots: bg_photo(ghosted full-bleed), kicker, headline, standfirst,
    events[(year, title, note)x4-6] vertical spine"""
    img, d, qa = _start("M10 timeline", slide_no, total, pal)
    if slot.get("bg_photo"):
        ghost = cover_fit(load_photo(slot["bg_photo"]), W, H)
        img.paste(Image.blend(ghost, Image.new("RGB", (W, H), PAPER), 0.90), (0, 0))
        d = ImageDraw.Draw(img)
    y = kicker_block(d, slot["kicker"], pal); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y = standfirst(d, (M, y + 6), slot["standfirst"], W - 2 * M, leading=1.14) + 70
    qa.size("standfirst", TYPE["standfirst"])
    events = slot["events"]
    spine_x = M + 340
    top, bottom = y + 20, CONTENT_BOTTOM - 200
    d.line([(spine_x, top), (spine_x, bottom)], fill=LINE, width=4)
    pitch = (bottom - top) // (len(events) - 1)
    yf = font("display_bold", 92); qa.size("year", 92, headline=True)
    tf = font("body_bold", TYPE["body"]); nf = font("body", FLOOR)
    qa.size("ev_title", TYPE["body"]); qa.size("ev_note", FLOOR)
    for i, (year, title, note) in enumerate(events):
        cy = top + i * pitch
        d.ellipse([spine_x - 16, cy - 16, spine_x + 16, cy + 16],
                  fill=pal["ACCENT"], outline=INK, width=4)
        yw = text_w(d, year, yf)
        d.text((spine_x - 60 - yw, cy - 58), year, font=yf, fill=pal["SIGNATURE"])
        d.text((spine_x + 60, cy - 48), title, font=tf, fill=INK)
        e = paragraph(d, (spine_x + 60, cy + 26), note, nf, MUTED, W - M - spine_x - 60, 1.2)
        qa.box(f"ev{i}", (M, cy - 60, W - M, e))
        qa.add_words(title + " " + note)
    return _finish(img, d, qa, slide_no, total)


# ─────────────────────────── M11 LADDER ───────────────────────────
def ladder(slot, slide_no, total, pal):
    """slots: kicker, headline, standfirst, tiers[(label, note)] top=best, drawn as pyramid,
    bg_photo(optional, ghosted full-bleed behind the whole diagram, same treatment as timeline())"""
    img, d, qa = _start("M11 ladder", slide_no, total, pal)
    if slot.get("bg_photo"):
        ghost = cover_fit(load_photo(slot["bg_photo"]), W, H)
        img.paste(Image.blend(ghost, Image.new("RGB", (W, H), PAPER), 0.78), (0, 0))
        d = ImageDraw.Draw(img)
    y = kicker_block(d, slot["kicker"], pal); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y = standfirst(d, (M, y + 6), slot["standfirst"], W - 2 * M, leading=1.14) + 80
    qa.size("standfirst", TYPE["standfirst"])
    tiers = slot["tiers"]
    n = len(tiers)
    band_h = 560 if slot.get("photo") else 0
    zone_top = y
    zone_bottom = (H - band_h - 80) if band_h else CONTENT_BOTTOM - 40
    tier_h = min(420, (zone_bottom - zone_top - (n - 1) * 30) // n)
    max_w = W - 2 * M
    min_w = max_w * 0.34
    lf = font("display_bold", TYPE["body"] + 8)
    # Tier color: bottom tier (worst, e.g. TCA) is solid black, fading
    # UP to pal["ACCENT"] (lightest) at the top (best) tier -- inverted
    # from this module's original top=SIGNATURE/bottom=ACCENT gradient
    # per Steve's explicit direction (2026-08 Wine Faults review): the
    # "no exceptions" tier should read as visually the heaviest/darkest,
    # not a mid-tone. s=1 at top (lightest) down to s=0 at bottom (black).
    def blend(c1, c2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))
    for i, (label, note) in enumerate(tiers):
        t = i / max(n - 1, 1)
        tw = int(min_w + (max_w - min_w) * t)
        x0 = (W - tw) // 2
        ty = zone_top + i * (tier_h + 30)
        s = 1 - t
        color = blend((0, 0, 0), pal["ACCENT"], s)
        # Pick label/note text color from actual contrast against this
        # tier's fill rather than assuming white always works -- the
        # lightest (gold) top tier is too light for white to read well.
        text_fill = (255, 255, 255) if contrast((255, 255, 255), color) >= contrast(INK, color) else INK
        note_fill = text_fill
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle([x0, ty, x0 + tw, ty + tier_h], radius=16, fill=color + (222,))
        img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))
        d = ImageDraw.Draw(img)
        label_max_w = tw - 80
        lsize = TYPE["body"] + 8
        lf_i = font("display_bold", lsize)
        while text_w(d, label, lf_i) > label_max_w and lsize > 36:
            lsize -= 2
            lf_i = font("display_bold", lsize)
        prefix = "!" if lsize < FLOOR else ""
        qa.size(f"{prefix}tier_label{i}", lsize)
        label_lines = [label] if text_w(d, label, lf_i) <= label_max_w else wrap(d, label, lf_i, label_max_w)
        la, ld = lf_i.getmetrics()
        label_lh = int((la + ld) * 1.0)
        ly0 = ty + 28
        for ln in label_lines:
            lw2 = text_w(d, ln, lf_i)
            d.text(((W - lw2) // 2, ly0), ln, font=lf_i, fill=text_fill)
            ly0 += label_lh
        nb_max_w = tw - 80
        avail_note_h = (ty + tier_h - 20) - (ly0 + 12)
        nsize = FLOOR
        nf_i = font("body", nsize)
        while nsize > 30:
            na, nd = nf_i.getmetrics()
            line_h = int((na + nd) * 1.0)
            max_lines = max(avail_note_h // line_h, 0)
            if max_lines >= 1:
                break
            nsize -= 4
            nf_i = font("body", nsize)
        else:
            na, nd = nf_i.getmetrics()
            line_h = int((na + nd) * 1.0)
            max_lines = 1
        nprefix = "!" if nsize < FLOOR else ""
        qa.size(f"{nprefix}tier_note{i}", nsize)
        nb_lines = wrap(d, note, nf_i, nb_max_w)[:max(max_lines, 1)]
        ny = ly0 + 12
        for ln in nb_lines:
            nw2 = text_w(d, ln, nf_i)
            d.text(((W - nw2) // 2, ny), ln, font=nf_i, fill=note_fill)
            ny += line_h
        qa.box(f"tier{i}", (x0, ty, x0 + tw, ty + tier_h))
        qa.add_words(label + " " + note)
    if band_h:
        img.paste(cover_fit(load_photo(slot["photo"]), W, band_h), (0, H - band_h))
        if slot.get("photo_caption"):
            scrim(img, (0, H - 160, W, H), "bottom", 0.66)
            d = ImageDraw.Draw(img)
            cf = font(core.CAPTION_FACE, core.CAPTION_SIZE); qa.size("cap", core.CAPTION_SIZE)
            cw2 = text_w(d, slot["photo_caption"], cf)
            d.text((W - M - cw2, H - 108), slot["photo_caption"], font=cf, fill=(255, 255, 255))
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


# ──────────────────────── M12 LEXICON CLOUD ────────────────────────
def lexicon_cloud(slot, slide_no, total, pal):
    """slots: kicker, headline, terms[(term, weight_px, gloss)x10-14]
    Shelf-packed scatter: unique baselines, staggered offsets, zero overlaps
    guaranteed. CAPACITY DEPENDS ON GLOSS LENGTH, NOT JUST TERM COUNT --
    each term's shelf-width is max(term_width, gloss_width), so a handful
    of long glosses can blow the available height even at 10 terms (this
    shipped once: the specimen's own placeholder copy needed 2674px against
    1810px available). Keep glosses to 2-4 words for a full 10-14 term
    cloud; longer glosses mean fewer terms fit. The module fails loudly
    with an exact px-needed-vs-available count rather than silently
    overflowing past the canvas -- if you hit this, shorten glosses or
    terms first, don't fight the packer."""
    img, d, qa = _start("M12 lexicon_cloud", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_lg"] if False else TYPE["display_md"], headline=True)
    palette = [pal["ACCENT"], pal["SIGNATURE"], pal["LEAD"], INK]
    gloss_f = font("body", FLOOR); qa.size("gloss", FLOOR)
    cloud_top, cloud_bottom = int(y) + 40, CONTENT_BOTTOM - 30
    avail_w = W - 2 * M
    units = []
    for i, (term, wt, gloss) in enumerate(slot["terms"]):
        wt = max(FLOOR + 4, min(wt, TYPE["display_md"] - HIERARCHY_GAP - 2))
        tf = font("display_xbold", wt)
        tb = d.textbbox((0, 0), term, font=tf)
        uw = max(tb[2] - tb[0], text_w(d, gloss, gloss_f))
        units.append(dict(term=term, tf=tf, wt=wt, gloss=gloss, tb=tb,
                          uw=uw, uh=(tb[3] - tb[1]) + 14 + 50,
                          color=palette[i % len(palette)]))
        qa.size(f"term:{term}", wt)
    random.seed(slot.get("seed", 4))
    order = sorted(range(len(units)), key=lambda i: -units[i]["wt"])
    anchor_ids = set(order[:2])
    mixed, lo, hi = [], 0, len(order) - 1
    while lo <= hi:
        mixed.append(order[lo]); lo += 1
        if lo <= hi:
            mixed.append(order[hi]); hi -= 1
    gap_x = 96
    shelves, cur, cw = [], [], 0
    for idx in mixed:
        add = units[idx]["uw"] + (gap_x if cur else 0)
        if cw + add > avail_w and cur:
            shelves.append(cur); cur, cw = [idx], units[idx]["uw"]
        else:
            cur.append(idx); cw += add
    if cur:
        shelves.append(cur)
    sh = [max(units[i]["uh"] for i in s) for s in shelves]
    extra = 190
    bh = [h + extra for h in sh]
    min_gap = 16
    needed_h = sum(bh) + min_gap * (len(shelves) + 1)
    avail_h = cloud_bottom - cloud_top
    if needed_h > avail_h:
        raise AssertionError(
            f"lexicon_cloud: {len(slot['terms'])} terms need {needed_h}px "
            f"({len(shelves)} shelves packed), only {avail_h}px available. "
            f"This used to overflow silently past the canvas edge -- now it "
            f"fails loudly instead. Reduce term count, lower weight_px values, "
            f"or shorten glosses (glosses set each shelf's minimum width).")
    gap_y = max((avail_h - sum(bh)) // (len(shelves) + 1), min_gap)
    yy = cloud_top + gap_y
    boxes = []
    for si, s in enumerate(shelves):
        gaps = [random.randint(40, 150) for _ in range(len(s) - 1)]
        row_w = sum(units[i]["uw"] for i in s) + sum(gaps)
        free = avail_w - row_w
        bias = (0.10, 0.55, 0.30, 0.70)[si % 4]
        x = M + (max(0, min(int(free * bias * random.uniform(0.5, 1.35)), free)) if free > 0 else 0)
        for k, idx in enumerate(s):
            u = units[idx]
            hr = max(bh[si] - u["uh"], 0)
            if idx in anchor_ids:
                # the deck's two most important terms sit on a clean,
                # near-fixed baseline -- editorial anchors, not scatter
                py = yy + int(hr * 0.12)
            else:
                base = int(hr * (0.02 if k % 2 == 0 else 0.62))
                span = int(hr * 0.36)
                py = yy + base + (random.randint(0, span) if span else 0)
            d.text((x, py - u["tb"][1]), u["term"], font=u["tf"], fill=u["color"])
            d.text((x, py + (u["tb"][3] - u["tb"][1]) + 14), u["gloss"], font=gloss_f, fill=INK)
            boxes.append((x, py, x + u["uw"], py + u["uh"], u["term"]))
            qa.box(f"unit:{u['term']}", boxes[-1][:4])
            x += u["uw"] + (gaps[k] if k < len(gaps) else 0)
        yy += bh[si] + gap_y
    return _finish(img, d, qa, slide_no, total)


# ────────────────────────── M13 SPOTLIGHT ──────────────────────────
def spotlight(slot, slide_no, total, pal):
    """slots: photo(hero), kicker, headline, callouts[(nx, ny, letter, title, note)x3-6]
    Lettered chips on the hero; legend column below."""
    img, d, qa = _start("M13 spotlight", slide_no, total, pal)
    hero_h = 1160
    img.paste(cover_fit(load_photo(slot["photo"]), W, hero_h), (0, 0))
    d = ImageDraw.Draw(img)
    chip_f = font("body_bold", FLOOR)
    for (nx, ny, letter, _t, _n) in slot["callouts"]:
        cx, cy = int(nx * W), int(ny * hero_h)
        d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=pal["SIGNATURE"],
                  outline=PAPER, width=5)
        lb = d.textbbox((0, 0), letter, font=chip_f)
        d.text((cx - (lb[2] - lb[0]) / 2, cy - (lb[3] - lb[1]) / 2 - lb[1]),
               letter, font=chip_f, fill=PAPER)
    y = kicker_block(d, slot["kicker"], pal, y=hero_h + 50); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y += 30
    lf = font("body_bold", TYPE["body"]); nf = font("body", FLOOR)
    qa.size("callout_title", TYPE["body"]); qa.size("callout_note", FLOOR)
    col_gap = 90
    col_w = (W - 2 * M - col_gap) // 2
    half = (len(slot["callouts"]) + 1) // 2
    ys = [y, y]
    for i, (_x, _y2, letter, title, note) in enumerate(slot["callouts"]):
        c = 0 if i < half else 1
        x = M + c * (col_w + col_gap)
        cy = ys[c]
        d.ellipse([x, cy + 6, x + 56, cy + 62], fill=pal["SIGNATURE"])
        lb = d.textbbox((0, 0), letter, font=chip_f)
        d.text((x + 28 - (lb[2] - lb[0]) / 2, cy + 34 - (lb[3] - lb[1]) / 2 - lb[1]),
               letter, font=chip_f, fill=PAPER)
        d.text((x + 80, cy), title, font=lf, fill=INK)
        e = paragraph(d, (x + 80, cy + 74), note, nf, MUTED, col_w - 80, 1.2)
        qa.box(f"co{i}", (x, cy, x + col_w, e))
        qa.add_words(title + " " + note)
        ys[c] = e + 44
    return _finish(img, d, qa, slide_no, total)


# ───────────────────────── M14 FEATURE TRIO ─────────────────────────
# ─────────────────── M14B HORIZONTAL TRIO ───────────────────
def horizontal_trio(slot, slide_no, total, pal):
    """slots: kicker, headline, standfirst(optional), rows[(title, body,
    photo)x3], footnote(optional).

    Three full-width horizontal photo bands stacked vertically, title+
    body overlaid on the left side of each band -- a deliberately
    different composition from feature_trio's three vertical columns,
    built because two three-item slides back to back with the same
    column layout read as the same slide. Overlay legibility is
    luminance-adaptive per band (sample the actual photo underneath,
    same discipline as every other on-photo text in this system)
    rather than assuming a fixed scrim strength works for every photo."""
    img, d, qa = _start("M14b horizontal_trio", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    if slot.get("standfirst"):
        y = standfirst(d, (M, y + 6), slot["standfirst"], W - 2 * M, leading=1.14) + 20
        qa.size("standfirst", TYPE["standfirst"])
    else:
        y += 30

    rows = slot["rows"]
    n = len(rows)
    gap_y = 22
    foot_reserve = 0
    foot_f = font("caption_italic", TYPE["caption"])
    foot_lines = []
    if slot.get("footnote"):
        foot_lines = wrap(d, slot["footnote"], foot_f, W - 2 * M)
        fa, fd = foot_f.getmetrics()
        foot_lh = int((fa + fd) * 1.15)
        foot_reserve = 30 + len(foot_lines) * foot_lh

    band_h = (CONTENT_BOTTOM - y - foot_reserve - (n - 1) * gap_y) // n
    tf = font("display_bold", TYPE["body"] + 4)
    bf = font("body", FLOOR)
    qa.size("row_title", TYPE["body"] + 4); qa.size("row_body", FLOOR)
    text_w_frac = slot.get("text_w_frac", 0.5)
    text_zone_w = int(W * text_w_frac)

    for i, (title, body, photo) in enumerate(rows):
        top = y + i * (band_h + gap_y)
        img.paste(cover_fit(load_photo(photo), W, band_h), (0, top))
        d = ImageDraw.Draw(img)
        # Always scrim, rather than choosing ink-no-scrim vs paper-with-
        # scrim from one averaged luminance reading over the whole text
        # zone -- a single average over a visually mixed region (e.g.
        # a bright flower against a black background corner) can read
        # as "bright enough" even when part of that region is dark,
        # leaving dark ink text invisible wherever it lands on the dark
        # patch. A guaranteed scrim costs a little visual weight but is
        # never wrong, which a coarse average can be.
        core.chip(img, (0, top, text_zone_w + 60, top + band_h), (10, 10, 10), opacity=0.45)
        d = ImageDraw.Draw(img)
        txt_color = PAPER
        pad = 44
        ty = top + pad
        # Line height and title-to-body gap both derive from the font's
        # actual ascent+descent rather than a fixed guess -- a flat 60px
        # line height didn't match this font's real metrics at this
        # size, which is what read as uneven vertical rhythm.
        ta, td = tf.getmetrics()
        title_lh = int((ta + td) * 1.08)
        for ln in wrap(d, title, tf, text_zone_w - 2 * pad):
            d.text((M, ty), ln, font=tf, fill=txt_color)
            ty += title_lh
        ba, bd = bf.getmetrics()
        ty += int((ba + bd) * 0.35)
        paragraph(d, (M, ty), body, bf, txt_color, text_zone_w - 2 * pad, 1.25)
        qa.add_words(title + " " + body)
        qa.box(f"row{i}", (0, top, W, top + band_h))

    band_bottom = y + n * band_h + (n - 1) * gap_y
    if foot_lines:
        fy = band_bottom + 30
        for ln in foot_lines:
            d.text((M, fy), ln, font=foot_f, fill=MUTED)
            fy += foot_lh
        qa.box("footnote", (M, band_bottom + 30, W - M, fy))
        qa.add_words(slot["footnote"])
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


def feature_trio(slot, slide_no, total, pal):
    """slots: kicker, headline, features[(title, body, photo)x3],
    footnote(optional small full-width text below the images, e.g. a
    "also permitted" list -- reserves its own space rather than
    competing with the photo band)"""
    img, d, qa = _start("M14 feature_trio", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y += 60
    col_gap = 70
    col_w = (W - 2 * M - 2 * col_gap) // 3
    tf = font("display_bold", TYPE["body"] + 4); bf = font("body", FLOOR)
    qa.size("feat_title", TYPE["body"] + 4); qa.size("feat_body", FLOOR)
    text_bottom = y
    # Titles that start with a letter label ("A. ", "B. ", "C. ") wrap
    # with a hanging indent: the label sits at the column's left edge
    # on its own, and every line of the actual text -- first line
    # included -- starts at the same x, aligned with the first word
    # rather than with the label. Without this, a wrapped title like
    # "C. Creamier Texture" broke after "Creamier", leaving "Texture"
    # flush left under the "C." instead of under "Creamier".
    _LETTER_PREFIX = re.compile(r"^([A-Z]\.)\s+(.*)$")

    def _wrap_title(title):
        m = _LETTER_PREFIX.match(title)
        if not m:
            return None, 0, wrap(d, title, tf, col_w)
        label_disp = m.group(1) + " "
        label_w = d.textbbox((0, 0), label_disp, font=tf)[2]
        return label_disp, label_w, wrap(d, m.group(2), tf, col_w - label_w)

    # Bottom-align the A/B/C headers: wrap every title first to find
    # the tallest (most-wrapped) one, then draw every column's title
    # so its LAST line lands on that same row -- the underline (and
    # therefore the body text below it) starts at the same y in every
    # column regardless of whether a given title wrapped to 1 or 2
    # lines. Previously each column's underline sat directly under its
    # own title with no regard for the others, so a 2-line title (e.g.
    # "Creamier Texture" wrapping) pushed that column's underline and
    # body noticeably lower than its neighbors.
    parsed_titles = [_wrap_title(feat[0]) for feat in slot["features"]]
    max_lines = max(len(lines) for _l, _lw, lines in parsed_titles)
    for i, feat in enumerate(slot["features"]):
        title, body = feat[0], feat[1]
        x = M + i * (col_w + col_gap)
        label, label_w, lines = parsed_titles[i]
        text_x = x + label_w if label else x
        ty = y + (max_lines - len(lines)) * 82
        if label:
            d.text((x, ty), label, font=tf, fill=INK)
        for ln in lines:
            d.text((text_x, ty), ln, font=tf, fill=INK)
            ty += 82
        d.line([(x, ty + 8), (x + col_w, ty + 8)], fill=pal["ACCENT"], width=3)
        e = paragraph(d, (x, ty + 40), body, bf, MUTED, col_w, 1.3)
        qa.add_words(title + " " + body)
        text_bottom = max(text_bottom, e)
    img_top = text_bottom + 120
    foot_f = font("caption_italic", TYPE["caption"])
    foot_reserve = 0
    foot_lines = []
    if slot.get("footnote"):
        foot_lines = wrap(d, slot["footnote"], foot_f, W - 2 * M)
        fa, fd = foot_f.getmetrics()
        foot_lh = int((fa + fd) * 1.15)
        foot_reserve = 30 + len(foot_lines) * foot_lh
    img_h = CONTENT_BOTTOM - img_top - foot_reserve
    for i, feat in enumerate(slot["features"]):
        photo = feat[2]
        # Optional 4th element: zoom override for this column's photo
        # (passed straight through to cover_fit). Default 1.0 keeps
        # existing behavior for every deck that doesn't set it.
        photo_zoom = feat[3] if len(feat) > 3 else 1.0
        x = M + i * (col_w + col_gap)
        img.paste(cover_fit(load_photo(photo), col_w, img_h, zoom=photo_zoom), (x, img_top))
        qa.box(f"feat{i}", (x, y, x + col_w, img_top + img_h))
    if foot_lines:
        fy = img_top + img_h + 30
        for ln in foot_lines:
            d.text((M, fy), ln, font=foot_f, fill=MUTED)
            fy += foot_lh
        qa.box("footnote", (M, img_top + img_h + 30, W - M, fy))
        qa.add_words(slot["footnote"])
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


# ────────────────────────── M15 FACT FILE ──────────────────────────
def fact_file(slot, slide_no, total, pal):
    """slots: photo(band), photo_caption, photo_credit(optional small-print
    attribution, e.g. photographer + license link -- rendered in the
    slide's footer gutter, not overlaid on the photo), kicker, headline,
    facts[(key, value)x5-8], famous(optional list[str])"""
    img, d, qa = _start("M15 fact_file", slide_no, total, pal)
    y = photo_band(img, slot["photo"], 0, BAND_TALL, slot.get("photo_caption"))
    d = ImageDraw.Draw(img)
    y = kicker_block(d, slot["kicker"], pal, y=y + 46); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y += 50
    facts = slot["facts"]
    kf = font("display_bold", TYPE["body"] + 6); vf = font("body", TYPE["body"])
    qa.size("key", TYPE["body"] + 6); qa.size("value", TYPE["body"])
    famous_reserve = 230 if slot.get("famous") else 0
    pitch = min(260, (CONTENT_BOTTOM - y - famous_reserve) // len(facts))
    key_w = max(text_w(d, k, kf) for k, _ in facts) + 80
    for i, (k, v) in enumerate(facts):
        d.text((M, y), k, font=kf, fill=pal["SIGNATURE"])
        e = paragraph(d, (M + key_w, y + 6), v, vf, INK, W - 2 * M - key_w, 1.2)
        qa.add_words(v)
        y += max(pitch, e - y + 30)
        if i < len(facts) - 1:
            d.line([(M, y - 34), (W - M, y - 34)], fill=LINE, width=1)
    qa.box("facts", (M, y - len(facts) * pitch, W - M, y))
    if slot.get("famous"):
        famous_names(d, (M, y + 20), slot["famous"], W - 2 * M, pal)
        qa.size("famous", TYPE["caption"])
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


# ─────────────────────────── M16 MOSAIC ───────────────────────────
def mosaic(slot, slide_no, total, pal):
    """slots: kicker(optional), hero_photo, small_photos[2-3], captions{photo->text},
    photo_credit(optional, rendered in the footer gutter -- required if any
    photo used here carries a license attribution obligation)
    Pacing breather: one large + small photos, captions only, no body text."""
    img, d, qa = _start("M16 mosaic", slide_no, total, pal)
    gut = 24
    hero_h = 1500
    img.paste(cover_fit(load_photo(slot["hero_photo"]), W, hero_h), (0, 0))
    smalls = slot["small_photos"]
    n = len(smalls)
    sm_top = hero_h + gut
    sm_h = H - sm_top - 210
    xacc = 0
    for i, p in enumerate(smalls):
        seg = (W - xacc) if i == n - 1 else (W - (n - 1) * gut) // n
        img.paste(cover_fit(load_photo(p), seg, sm_h), (xacc, sm_top))
        xacc += seg + gut
    d = ImageDraw.Draw(img)
    scrim(img, (0, hero_h - 170, W, hero_h), "bottom", 0.72, color=pal["SIGNATURE"])
    d = ImageDraw.Draw(img)
    # Font bumped up from TYPE["caption"] for legibility.
    cf = font("italbold", TYPE["caption"] + 10); qa.size("caption", TYPE["caption"] + 10)
    ca, cd = cf.getmetrics()
    cap_lh = int((ca + cd) * 1.1)
    cap = slot.get("captions", {}).get(slot["hero_photo"], "")
    if cap:
        cap_lines = wrap(d, cap, cf, W - 2 * M)
        need_h = 60 + len(cap_lines) * cap_lh
        cap_top = hero_h - need_h
        # chip(), not scrim(), for the caption backing -- scrim() is a
        # gradient that fades to nothing at its far edge, so a caption
        # that grew to 2+ lines had its TOP line sitting in the weak
        # end of the fade with barely any coverage. That read fine
        # against a photo that was already dark up there, but broke
        # outright against a photo with a bright area (e.g. a white
        # tabletop) in that same spot -- white caption text on
        # near-white photo, unreadable. A flat, uniform-opacity chip
        # has no weak edge, so this is correct regardless of what's
        # underneath, not just for photos that happen to be dark
        # everywhere the scrim's gradient was already strong.
        core.chip(img, (0, cap_top, W, hero_h), pal["SIGNATURE"], opacity=0.82)
        d = ImageDraw.Draw(img)
        cy = hero_h - 40 - len(cap_lines) * cap_lh
        for ln in cap_lines:
            d.text((W - M - text_w(d, ln, cf), cy), ln, font=cf, fill=(255, 255, 255))
            cy += cap_lh
        qa.box("!hero_caption", (M, cap_top, W - M, hero_h))
    # captions on small photos (from same captions dict)
    xacc2 = 0
    for i, p in enumerate(smalls):
        seg = (W - xacc2) if i == n - 1 else (W - (n - 1) * gut) // n
        scap = slot.get("captions", {}).get(p, "")
        if scap:
            cap_w = seg - 56
            scap_lines = wrap(d, scap, cf, cap_w)
            need_h = 76 + len(scap_lines) * cap_lh
            scrim(img, (xacc2, sm_top + sm_h - need_h, xacc2 + seg, sm_top + sm_h), "bottom", 0.70, color=pal["SIGNATURE"])
            d = ImageDraw.Draw(img)
            cy = sm_top + sm_h - 24 - len(scap_lines) * cap_lh
            for ln in scap_lines:
                d.text((xacc2 + 28, cy), ln, font=cf, fill=(255, 255, 255))
                cy += cap_lh
            qa.box(f"!small_caption{i}", (xacc2, sm_top + sm_h - need_h, xacc2 + seg, sm_top + sm_h))
        xacc2 += seg + gut
    if slot.get("overlay_title"):
        # 100px display title over the hero, top-left; replaces kicker
        scrim(img, (0, 0, W, 340), "top", 0.62)
        d = ImageDraw.Draw(img)
        otf = font("display_black", 100)
        qa.size("overlay_title", 100, headline=True)
        oy = 90
        oa, od = otf.getmetrics()
        for ln in wrap(d, slot["overlay_title"], otf, W - 2 * M):
            d.text((M, oy), ln, font=otf, fill=PAPER)
            oy += int((oa + od) * 0.98)
        qa.box("overlay_title", (M, 90, W - M, oy))
    else:
        if slot.get("kicker"):
            kf = font("display_bold", 74) if slot.get("kicker_serif") else font("kicker_bold", 70)
            kw = (text_w(d, slot["kicker"], kf) if slot.get("kicker_serif")
                  else core.tracked_w(d, slot["kicker"], kf, 5))
            chip_w = min(W, M + kw + 90)
            d.rectangle([0, 0, chip_w, 148], fill=pal["SIGNATURE"])
            d = ImageDraw.Draw(img)
            if slot.get("kicker_serif"):
                d.text((M, 60), slot["kicker"], font=kf, fill=(250, 240, 226))
            else:
                tracked_text(d, (M, 60), slot["kicker"], kf, (250, 240, 226), 5)
            qa.size("kicker", 74 if slot.get("kicker_serif") else 70)
        qa.size("mosaic_anchor", TYPE["display_md"], headline=True)  # image-led slide; satisfies law trivially
    return _finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


# ─────────────────────── M17 PHOTO QUOTE ───────────────────────
def photo_quote(slot, slide_no, total, pal):
    """slots: photo(full-bleed), quote(sentence case), attribution(optional)
    One large white serif quote, sentence case, over a full-bleed photograph."""
    img, d, qa = _start("M17 photo_quote", slide_no, total, pal)
    img.paste(cover_fit(load_photo(slot["photo"]), W, H), (0, 0))
    scrim(img, (0, 0, W, H), "top", 0.42)
    scrim(img, (0, int(H * 0.30), W, H), "bottom", 0.70)
    d = ImageDraw.Draw(img)
    quote_size = slot.get("quote_size", 150)
    qf = font("display_black", quote_size)
    qa.size("quote", quote_size, headline=True)
    lines = wrap(d, slot["quote"], qf, W - 2 * M)
    asc, desc = qf.getmetrics()
    lh = int((asc + desc) * 1.08)
    block_h = len(lines) * lh
    qy = max(int(H * 0.34), (H - 420) - block_h - 220)
    y0 = qy
    for ln in lines:
        d.text((M, qy), ln, font=qf, fill=PAPER)
        qy += lh
    qa.box("quote", (M, y0, W - M, qy))
    qa.add_words(slot["quote"])
    d.line([(M, qy + 44), (M + 260, qy + 44)], fill=pal["ACCENT"], width=5)
    if slot.get("attribution"):
        af = font("caption_italic", 66); qa.size("attr", 66)
        d.text((M, qy + 96), "\u2014 " + slot["attribution"], font=af, fill=(238, 232, 220))
    return _finish(img, d, qa, slide_no, total)


# ─────────────────────── M18 EULER NESTING ───────────────────────
def euler_nesting(slot, slide_no, total, pal):
    """slots: kicker, headline, standfirst, circles[(name, cx, cy, r,
    parent_name|None, label_pos('in'|'above'|'none'))], exceptions_label
    (optional text) + exceptions_label_pos (optional (x,y)) for a header
    over circles with parent=None that are NOT the main root -- e.g.
    "NOT PART OF COLUMBIA VALLEY". footnote(optional).

    True nested-set containment diagram, not a ranked pyramid (see
    `ladder`) -- use this when the real relationship is "B is entirely
    inside A" with actual branching (multiple children per parent) and
    possibly named exceptions that sit outside the main hierarchy
    entirely. circles are drawn in list order (draw parents before
    children so children render on top); caller is responsible for
    geometry (containment / non-overlap) -- this module does not
    compute layout, only renders it. Verify circle math before calling:
    a child circle's (distance from parent center + child radius) must
    be <= parent radius, and sibling circles must have center distance
    >= sum of their radii, or the diagram will misrepresent the very
    relationship it exists to show.

    label_pos="none" skips the label for a circle too small to carry
    one legibly (common for the tiniest nested circles in a dense
    diagram) -- the circle itself still renders; name it in footnote
    instead so it's not lost from the deck's factual content, just from
    the visual label.

    QA note: circle boxes are deliberately NOT registered for the
    generic pairwise-collision check (nested/sibling circles overlap
    or sit close together by design -- that's the entire point of the
    diagram, and the generic collision check has no notion of
    "intentional containment"). Only each label's actual text
    bounding box is registered, so real label-on-label collisions
    still fail the build, but circle-on-circle overlap never does."""
    img, d, qa = _start("M18 euler_nesting", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal); qa.size("kicker", 70)
    y = headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False); qa.size("headline", TYPE["display_md"], headline=True)
    y = standfirst(d, (M, y + 6), slot["standfirst"], W - 2 * M, leading=1.14) + 50
    qa.size("standfirst", TYPE["standfirst"])

    circles = slot["circles"]
    by_name = {c[0]: c for c in circles}

    def depth(name):
        d_ = 0
        parent = by_name[name][4]
        while parent:
            d_ += 1
            parent = by_name[parent][4]
        return d_

    for (name, cx, cy, r, parent, label_pos) in circles:
        dep = depth(name)
        outline_w = max(3, 7 - dep * 2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=pal["SIGNATURE"] if dep == 0 else MUTED,
                  width=outline_w, fill=None)
        if label_pos == "none":
            continue
        size = max(FLOOR - 10, 64 - dep * 14)
        prefix = "!" if size < FLOOR else ""
        lf = font("display_bold" if dep < 2 else "body_bold", size)
        tw = text_w(d, name, lf)
        if label_pos == "above":
            tx, ty = cx - tw // 2, cy - r - size - 14
        else:
            tx, ty = cx - tw // 2, cy - int(size * 0.4)
        d.text((tx, ty), name, font=lf, fill=INK if dep else pal["SIGNATURE"])
        qa.size(f"{prefix}circle_label_{name}", size)
        ta, td = lf.getmetrics()
        qa.box(f"lbl:{name}", (tx, ty, tx + tw, ty + ta + td))

    if slot.get("exceptions_label_pos") and slot.get("exceptions_label"):
        ex_x, ex_y = slot["exceptions_label_pos"]
        ef = font("kicker_bold", TYPE["caption"])
        tracked_text(d, (ex_x, ex_y), slot["exceptions_label"], ef, pal["ACCENT"], 4)
        qa.size("exceptions_label", TYPE["caption"])

    if slot.get("footnote"):
        ff = font("body", FLOOR)
        d.text((M, CONTENT_BOTTOM - 10), slot["footnote"], font=ff, fill=MUTED)
        qa.size("footnote", FLOOR); qa.add_words(slot["footnote"])

    return _finish(img, d, qa, slide_no, total)


def map_facsimile(slot, slide_no, total, pal):
    """M18 map_facsimile — source-faithful cartography (v4.3, LOCKED SOP).

    Renders a 1:1 trace of a reference wine map (e.g. an SWE PDF) in house
    palette and fonts. Every element — state fills, rivers, region blobs,
    leader lines, labels — is drawn at its exact source position under ONE
    uniform scale. This module exists because the atlas() marker system
    cannot faithfully reproduce a dense professional reference map; do NOT
    fall back to atlas() for "copy this map" requests.

    LOCKED PROCESS (see STYLE_GUIDE_v4.md "Source-Faithful Map SOP"):
      1. Extract source vectors with pymupdf: fills -> polygons (shapely
         buffer(0) to repair, simplify 0.15), colored strokes -> rivers /
         leader lines, text -> line-grouped label bboxes.
      2. Match label -> leader -> blob by nearest-endpoint distance and
         verify (< ~3pt). Never guess pairings from a second map source.
      3. ONE uniform fit over the label-inclusive bbox (+6pt pad). Never
         per-state transforms; never import shapes from a differently
         projected map.
      4. Collisions are resolved ONLY through slot['nudges'] (px offsets,
         persisted in the deck's data file) — never by silently moving,
         resizing, or dropping source elements.
      5. Off-scope areas are GHOSTED, not deleted: exact geometry kept,
         fills near paper, labels warm gray, leaders lightened.
      6. QA collision pass + explicit edge check (QA does not catch
         canvas overflow). When visual inspection is unavailable, verify
         with a numerical box/gap report.

    slot keys:
      kicker, headline
      states:   [{'name','pts','fill','ghost'?}]  drawn in list order
      regions:  {name: {'pts','fill','ghost'?}}
      rivers:   [[(x,y)...]]                       source stroke polylines
      leaders:  [{'start','end','ghost'?}]         exact source segments
      labels:   {'regions': {name: bbox}, 'states': {name: bbox},
                 'cities': {name: bbox}, 'ocean': (bbox, text)}
      city_dots: {name: (x,y)}
      display:  {name: text}    render-text overrides ('Hunter\\nValley')
      nudges:   {key: (dx,dy)}  px; city keys prefixed 'city:'
      sizes:    {name: px}      sub-floor entries auto-register with "!"
      map_top:  y of map area (default 470)
    All geometry in raw source-PDF coordinates; the module does the fit.
    """
    img, d, qa = _start("M18 map_facsimile", slide_no, total, pal)
    y = kicker_block(d, slot["kicker"], pal, y=150); qa.size("kicker", 70)
    headline(d, slot["headline"], y, fill=pal["SIGNATURE"], show_underline=False)
    qa.size("headline", TYPE["display_md"], headline=True)

    GHOST_FILL = (240, 236, 228)
    GHOST_EDGE = (203, 196, 185)
    GHOST_TEXT = (178, 168, 159)
    GHOST_LEADER = (198, 188, 182)
    RIVER = (139, 178, 198)
    LEADER = (122, 96, 102)
    NUDGE = slot.get("nudges", {})
    SIZES = slot.get("sizes", {})
    DISPLAY = slot.get("display", {})

    def dk(c, f=0.62):
        return tuple(int(v * f) for v in c)

    xs, ys = [], []
    for st in slot["states"]:
        for x, yy in st["pts"]: xs.append(x); ys.append(yy)
    for r in slot["regions"].values():
        for x, yy in r["pts"]: xs.append(x); ys.append(yy)
    lab = slot["labels"]
    for group in ("regions", "states", "cities"):
        for bb in lab.get(group, {}).values():
            xs += [bb[0], bb[2]]; ys += [bb[1], bb[3]]
    if lab.get("ocean"):
        bb = lab["ocean"][0]; xs += [bb[0], bb[2]]; ys += [bb[1], bb[3]]
    PAD = 6
    bx0, by0, bx1 = min(xs) - PAD, min(ys) - PAD, max(xs) + PAD
    MAP_TOP = slot.get("map_top", 470)
    SCALE = (W - 2 * M) / (bx1 - bx0)

    def P(x, yy):
        return (M + (x - bx0) * SCALE, MAP_TOP + (yy - by0) * SCALE)

    def PN(x, yy, key):
        dx, dy = NUDGE.get(key, (0, 0))
        px, py = P(x, yy)
        return (px + dx, py + dy)

    for st in slot["states"]:
        ghost = st.get("ghost")
        fill = GHOST_FILL if ghost else st["fill"]
        edge = GHOST_EDGE if ghost else dk(st["fill"], 0.55)
        pts = [P(x, yy) for x, yy in st["pts"]]
        d.polygon(pts, fill=fill, outline=edge)
        d.line(pts + [pts[0]], fill=edge, width=4, joint="curve")

    for pl in slot.get("rivers", []):
        d.line([P(x, yy) for x, yy in pl], fill=RIVER, width=4, joint="curve")

    for name, r in slot["regions"].items():
        ghost = r.get("ghost")
        fill = (226, 220, 211) if ghost else r["fill"]
        edge = GHOST_EDGE if ghost else dk(r["fill"])
        pp = [P(x, yy) for x, yy in r["pts"]]
        d.polygon(pp, fill=fill, outline=edge)
        d.line(pp + [pp[0]], fill=edge, width=3, joint="curve")

    for l in slot.get("leaders", []):
        if not l.get("start") or not l.get("end"):
            continue
        col = GHOST_LEADER if l.get("ghost") else LEADER
        d.line([P(*l["start"]), P(*l["end"])], fill=col, width=3)

    for name, bb in lab.get("regions", {}).items():
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        ghost = slot["regions"].get(name, {}).get("ghost")
        fill = GHOST_TEXT if ghost else dk(slot["regions"][name]["fill"], 0.52)
        sz = SIZES.get(name, FLOOR)
        f = font("body_bold", sz)
        text = DISPLAY.get(name, name)
        x, yy = PN(cx, cy, name)
        d.multiline_text((x, yy), text, font=f, fill=fill, anchor="mm", align="center")
        tb = d.multiline_textbbox((x, yy), text, font=f, anchor="mm", align="center")
        qa.size(("!" if sz < FLOOR else "") + f"r:{name}", sz); qa.box(f"lbl:{name}", tb)

    sf = font("body_bold", 74)
    ghost_states = {st["name"] for st in slot["states"] if st.get("ghost")}
    for name, bb in lab.get("states", {}).items():
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        fill = GHOST_TEXT if name in ghost_states else pal["SIGNATURE"]
        x, yy = PN(cx, cy, name)
        d.text((x, yy), name, font=sf, fill=fill, anchor="mm")
        tb = d.textbbox((x, yy), name, font=sf, anchor="mm")
        qa.size(f"s:{name}", 74); qa.box(f"state:{name}", tb)

    cf = font("body", FLOOR)
    ghost_cities = set(slot.get("ghost_cities", []))
    for name, (dx_, dy_) in slot.get("city_dots", {}).items():
        px, py = P(dx_, dy_)
        col = GHOST_TEXT if name in ghost_cities else INK
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=col)
    for name, bb in lab.get("cities", {}).items():
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        col = GHOST_TEXT if name in ghost_cities else INK
        x, yy = PN(cx, cy, "city:" + name)
        d.text((x, yy), name, font=cf, fill=col, anchor="mm")
        tb = d.textbbox((x, yy), name, font=cf, anchor="mm")
        qa.size(f"c:{name}", FLOOR); qa.box(f"city:{name}", tb)

    if lab.get("ocean"):
        bb, otext = lab["ocean"]
        of = font("caption_italic", 66)
        ox, oy = PN((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2, "ocean")
        d.text((ox, oy), otext, font=of, fill=(126, 156, 176), anchor="mm")
        tb = d.textbbox((ox, oy), otext, font=of, anchor="mm")
        qa.size("ocean", 66); qa.box("ocean", tb)

    # explicit edge check — QA's collision pass does not catch overflow
    for k, b in qa.boxes.items():
        if b[0] < 30 or b[2] > W - 30:
            print("EDGE WARNING:", k, [round(v) for v in b])

    return _finish(img, d, qa, slide_no, total)


MODULES = dict(
    statement=statement, editorial_lead=editorial_lead, side_rail=side_rail,
    stat_wall=stat_wall, duel=duel, process_map=process_map, card_grid=card_grid,
    showcase_shelf=showcase_shelf, atlas=atlas, timeline=timeline, ladder=ladder,
    lexicon_cloud=lexicon_cloud, spotlight=spotlight, feature_trio=feature_trio,
    fact_file=fact_file, mosaic=mosaic, photo_quote=photo_quote,
    euler_nesting=euler_nesting, map_facsimile=map_facsimile,
)
