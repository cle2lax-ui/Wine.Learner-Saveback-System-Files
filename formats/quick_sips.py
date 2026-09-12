import core
"""
QUICK SIPS SERIES — MODULE LIBRARY
2-page format: a focused wine topic in exactly two slides. Elegant,
polished infographic/brochure register — Wine Spectator / Conde Nast
Traveler / Rolex / Four Seasons as visual touchstones. Restrained
palette, serif display type, generous white space, stat-forward facts.
Shares the canvas, safe zones, and QA harness with the Field Guide
series (tokens.py, core.py) but is its own visual system — see
QUICK_SIPS_STYLE_GUIDE.md for the full spec.

    quick_sip_cover   page 1: hero photo, title, stat strip, body copy
                      that carves around a corner-bled benchmark bottle
    quick_sip_detail  page 2: headline, body copy around a second
                      benchmark bottle, tasting/structure dashboard
"""
from PIL import Image, ImageDraw, ImageOps
from tokens import *
from core import (font, text_w, tracked_text, wrap, paragraph,
                   load_photo, cover_fit, scrim, chip, tracked_w, wrap_tracked,
                   wrap_around, QA)
from modules import _start, _finish

GOLD = QUICKSIPS_GOLD  # fixed series accent, independent of each deck's SIGNATURE


# ---------------------------------------------------------------- glyph ---
def _qs_glass(img, gx, gy, gh, tone="white"):
    """Lucide 'wine' icon (lucide.dev), ISC licensed, free for commercial
    use, no attribution required. Two pre-rendered tones: white (for
    photo/dark backgrounds) and ink (for the plain paper background —
    a white icon there is invisible)."""
    fname = "QS_glass_icon.png" if tone == "white" else "QS_glass_icon_ink.png"
    icon = Image.open(f"{PHOTO_DIR}/{fname}").convert("RGBA")
    s = gh / icon.size[1]
    gw = int(icon.size[0] * s)
    icon = icon.resize((gw, gh), Image.LANCZOS)
    img.paste(icon, (gx, gy), icon)
    return gw


def qs_mark_overlay(img, d, pal, scrim_on=True, text_color=None, qa=None):
    """Corner brand for photo backgrounds (page 1 / cover use): glass
    glyph + wordmark, soft top scrim for legibility, anchored top-left.
    scrim_on=False skips the full-width chip -- safe only when the
    photo already has natural contrast under the wordmark color
    without it, OR when fill is light enough to need its own tight
    backing chip (see below); pass qa to get a real pixel-sampled
    check rather than trusting either case by eye.
    text_color overrides the wordmark's default PAPER fill.

    scrim_on=False + a light fill (PAPER/white) is a real combination,
    not a contradiction: dropping the full-width top scrim doesn't mean
    dropping ALL legibility backing, it means dropping the specific
    "black bar across the top of the image" look. When fill is light
    and the scrim is off, this draws a small chip sized tightly to the
    icon+wordmark's own footprint instead -- enough for the text to
    read against a bright or midtone sky, without reintroducing a
    full-width bar. This is a REAL rendered rectangle (core.chip()),
    not a text shadow -- it actually darkens the pixels the QA contrast
    check below samples, unlike a shadow trick that would look better
    but not register as legible on the actual sampled luminance."""
    pad, gap = 40, 32
    gh = 144
    tf = font("display_bold", 120)
    txt = "Quick Sips"
    asc, desc = tf.getmetrics()
    content_h = max(gh, asc + desc)
    scrim_h = pad + content_h + pad + 20
    fill = text_color or PAPER
    is_light = sum(fill[:3]) / 3 > 128
    tw_probe = text_w(d, txt, tf)
    # Icon tone/width need to be known before the chip is drawn (the
    # chip must sit UNDER both the icon and the text), so peek at the
    # source PNG's aspect ratio here rather than calling _qs_glass yet
    # -- _qs_glass pastes immediately as a side effect, which would put
    # the chip on top of the icon instead of behind it.
    icon_tone = "white" if is_light else "ink"
    icon_fname = "QS_glass_icon.png" if icon_tone == "white" else "QS_glass_icon_ink.png"
    with Image.open(f"{PHOTO_DIR}/{icon_fname}") as _probe:
        gw = int(_probe.size[0] * (gh / _probe.size[1]))
    if scrim_on:
        chip(img, (0, 0, W, scrim_h), (10, 10, 10), opacity=0.62)
    elif is_light:
        tight_pad = 24
        chip(img, (pad - tight_pad, pad - tight_pad,
                    pad + gw + gap + tw_probe + tight_pad,
                    pad + content_h + tight_pad),
             (10, 10, 10), opacity=0.55)
    d = ImageDraw.Draw(img)
    gy = pad + (content_h - gh) // 2
    # Glass glyph tone follows the wordmark: "white" is the light outline
    # (right for a scrim/tight chip or a dark photo); anything else falls
    # through to _qs_glass's pre-rendered ink tone, for a dark wordmark
    # on an unprotected light sky. _qs_glass only has these two
    # pre-rendered tones -- it is not pal-tintable -- so this does not
    # attempt to match the wordmark's exact forest green, only its
    # darkness.
    gw = _qs_glass(img, pad, gy, gh, tone=icon_tone)
    d = ImageDraw.Draw(img)
    ink_top, _, _, ink_bot = d.textbbox((0, 0), txt, font=tf)
    ink_center = ink_top + (ink_bot - ink_top) / 2
    icon_center = gy + gh / 2
    ty = int(icon_center - ink_center)
    d.text((pad + gw + gap, ty), txt, font=tf, fill=fill)
    if qa is not None and not scrim_on:
        # Real pixel check under the wordmark text band -- the whole
        # point of dropping the scrim is that this needs to hold up
        # against the actual photo, not an assumed dark background.
        qa.check_photo_contrast(
            img, (pad + gw + gap, ty, pad + gw + gap + text_w(d, txt, tf), ty + asc + desc),
            sum(fill[:3]) / 3, "qs_mark_wordmark")
    return pad + content_h


def qs_mark_patch(img, d, pal, topic=None, text_override=None):
    """Corner brand for flat backgrounds (page 2+ / detail use). STANDARD
    RULE for every Quick Sips interior page: pass the deck's topic and
    the lockup reads 'Quick Sips - {topic}' — this is how the topic
    name is displayed on page 2 onward. Do not add a separate topic
    heading elsewhere on the page; the mark carries it.

    text_override, when given, replaces the 'Quick Sips[- topic]' text
    entirely (topic is then ignored) -- for one-off slides that want the
    recognizable glass mark but a custom lockup line instead of the
    series name (e.g. a slide title standing in for it)."""
    pad, gap = 40, 26
    gh = 108
    tf = font("display_bold", 90)
    txt = text_override if text_override else (f"Quick Sips - {topic}" if topic else "Quick Sips")
    tw = text_w(d, txt, tf)
    asc, desc = tf.getmetrics()
    content_h = max(gh, asc + desc)
    icon_probe = Image.open(f"{PHOTO_DIR}/QS_glass_icon.png")
    gw = int(gh * icon_probe.size[0] / icon_probe.size[1])
    patch_w = pad + gw + gap + tw + pad
    patch_h = pad + content_h + pad
    d.rectangle([0, 0, patch_w, patch_h], fill=pal["SIGNATURE"])
    gy = pad + (content_h - gh) // 2
    gw = _qs_glass(img, pad, gy, gh, tone="white")
    d = ImageDraw.Draw(img)
    ink_top, _, _, ink_bot = d.textbbox((0, 0), txt, font=tf)
    ink_center = ink_top + (ink_bot - ink_top) / 2
    icon_center = gy + gh / 2
    ty = int(icon_center - ink_center)
    d.text((pad + gw + gap, ty), txt, font=tf, fill=PAPER)
    return patch_h


# --------------------------------------------------------- stat strip -----
def qs_stat_strip(d, y, stats, pal, qa, x0, content_w):
    """A Rolex-spec-sheet style row: big serif numerals over small-caps
    labels, separated by thin gold hairlines. stats: list of (num,
    label) tuples, typically 3."""
    n = len(stats)
    col_w = content_w // n
    num_f = font("display_black", 92)
    lab_f = font("kicker_bold", 60)
    max_h = 0
    for i, (num, label) in enumerate(stats):
        cx = x0 + i * col_w
        nw = text_w(d, num, num_f)
        d.text((cx + (col_w - nw) // 2, y), num, font=num_f, fill=pal["SIGNATURE"])
        na, nd = num_f.getmetrics()
        ly = y + int((na + nd) * 0.92) + 18
        lines = wrap_tracked(d, label, lab_f, col_w - 40, 3)
        la, ld = lab_f.getmetrics()
        llh = int((la + ld) * 1.25)
        for ln in lines:
            lw = tracked_w(d, ln, lab_f, 3)
            tracked_text(d, (cx + (col_w - lw) // 2, ly), ln, lab_f, MUTED, tracking=3)
            ly += llh
        max_h = max(max_h, ly - y)
        if i > 0:
            d.line([(cx, y + 6), (cx, y + max_h - 10)], fill=GOLD, width=2)
        qa.box(f"stat{i}", (cx, y, cx + col_w, y + max_h))
    qa.size("stat_num", 92, headline=True); qa.size("stat_label", 60)
    qa.add_words(" ".join(l for _, l in stats))
    return y + max_h


# ---------------------------------------------------- benchmark bottle ----
def qs_benchmark_bottle(img, d, pal, qa, heading, photo, wine, producer, origin, note,
                         x0, content_w, page_bottom, bottle_h=1050, bleed_right=60,
                         bleed_bottom=140, cap_w=500, cap_size=50, cap_y_override=None, cap_gap=36):
    """Bottle anchored to the bottom-right corner, bleeding past both the
    right and bottom edges of the canvas by design (crop the source
    image to its opaque bounding box first via .crop(bim.getbbox()) or
    the bleed math will be measuring transparent margin, not the
    bottle). A small italic-serif caption block (heading, wine,
    producer, note) nestles beside the neck rather than running the
    full width below the bottle:
      - heading: non-italic bold serif (display_bold), pal SIGNATURE
      - wine name: italic bold serif (italbold), INK, one size up
      - producer: italic serif (italbold), GOLD
      - note: light-weight non-italic serif (display_light), INK
    cap_size (default 50) sits below the system's usual 60px type
    floor — that's an intentional, explicit exception for this one
    element (tracked via the "!" QA-exemption prefix), not a mistake;
    don't "fix" it back up to 60 without checking with the deck owner.

    cap_y_override, when given, replaces the default "just above the
    bottle's neck" vertical position with an exact y -- used to align
    the caption's top with the tasting dashboard's top on the same
    page. Pass the dashboard's own start y here, not the other way
    around: the dashboard's position is the one driven by paragraph/
    body copy length, so it's the anchor the caption should match.

    Returns (obstacle, top_y): obstacle is the rectangle the caller
    should pass to wrap_around() so body prose carves around the whole
    lockup (heading + bottle + caption) rather than overlapping it."""
    bim = Image.open(f"{PHOTO_DIR}/{photo}")
    bim = ImageOps.exif_transpose(bim).convert("RGBA")  # honor camera rotation metadata
    bim = bim.crop(bim.getbbox())
    bw, bh = bim.size
    s = bottle_h / bh
    nw, nh = int(bw * s), int(bh * s)
    bottle_bottom = page_bottom + bleed_bottom
    bottle_top = bottle_bottom - nh
    bottle_x = x0 + content_w - nw + bleed_right
    resized = bim.resize((nw, nh), Image.LANCZOS)
    img.paste(resized, (bottle_x, bottle_top), resized)
    d = ImageDraw.Draw(img)

    cap_x = bottle_x - cap_w - cap_gap
    cap_y = cap_y_override if cap_y_override is not None else bottle_top + int(nh * 0.05) + 60
    hf = font("display_bold", cap_size)
    ha, hd = hf.getmetrics(); hlh = int((ha + hd) * 1.24)
    cy = cap_y
    cap_top = cap_y
    for ln in heading.split("\n"):
        d.text((cap_x, cy), ln, font=hf, fill=pal["SIGNATURE"])
        cy += hlh

    # Caption stack order (v5 redesign): heading, then producer, then wine
    # name, then note -- producer (italic, GOLD) reads above the wine name
    # (italic bold, INK), not below it. Deliberate reversal from the
    # original layout; applies to every deck automatically, both pages.
    of = font("italbold", cap_size)
    tag_lines = wrap(d, producer, of, cap_w)
    oa, od = of.getmetrics(); olh = int((oa + od) * 1.24)
    for ln in tag_lines:
        d.text((cap_x, cy), ln, font=of, fill=GOLD)
        cy += olh
    cy += 2

    wf = font("italbold", 58)
    w_lines = wrap(d, wine, wf, cap_w)
    wa, wd = wf.getmetrics(); wlh = int((wa + wd) * 1.2)
    for ln in w_lines:
        d.text((cap_x, cy), ln, font=wf, fill=INK)
        cy += wlh
    cy += 4

    nf = font("display_light", cap_size)
    cy = paragraph(d, (cap_x, cy), note, nf, INK, cap_w, leading=1.26)
    qa.box("bench_caption", (cap_x, cap_top, cap_x + cap_w, cy))
    qa.add_words(f"{heading} {wine} {producer} {origin} {note}")
    qa.size("!bench_caption_sz", cap_size)

    obstacle_top = min(bottle_top, cap_y)
    obstacle = (cap_x - 100, obstacle_top, x0 + content_w, min(bottle_bottom, page_bottom))
    return obstacle, obstacle_top, cap_y


# ----------------------------------------------------- tasting dashboard --
def qs_tasting_dashboard(d, y0, x0, w, pal, qa, attributes,
                          header_gap=58, pre_row_gap=26, row_gap=22, text_bar_gap=8, bar_h=14):
    """A compact structure profile: label + descriptor + a slim filled
    bar, one row per attribute. attributes: list of (label, frac 0-1,
    descriptor) tuples, e.g. ("Tannin", 0.75, "Medium+"). Redesigned as
    a tight, Rolex-spec-sheet style stack — thin hairline-track bars
    rather than thick pills — so 5 rows read as one compact block
    beside the bottle lockup instead of stretching down the page.

    header_gap/pre_row_gap/row_gap default to the detail-page rhythm.
    quick_sip_cover calls this with the tighter cover-page values
    (50/18/12) to make room for dashboard_gap without pushing past the
    footer -- the two pages are allowed to look slightly different here.

    Label and descriptor are drawn on the same line (label left,
    descriptor right-aligned) ONLY when they actually fit side by side
    in `w` with a minimum gap; otherwise the descriptor drops to its
    own line below the label. A real bug shipped here once: label and
    descriptor were always assumed to fit on one line, so a narrow `w`
    (e.g. a wide benchmark-bottle lockup eating most of the column)
    silently overlapped them into unreadable text. Don't remove this
    fit check."""
    kf = font("kicker_bold", 60)
    tracked_text(d, (x0, y0), "TASTING & STRUCTURE", kf, pal["SIGNATURE"], tracking=4)
    y = y0 + header_gap
    d.line([(x0, y), (x0 + w, y)], fill=LINE, width=2)
    y += pre_row_gap
    val_f = font("italbold", 60)
    va, vd = val_f.getmetrics()
    line_h = va + vd
    min_gap = 40
    for label, frac, descriptor in attributes:
        lw = text_w(d, label, val_f)
        dw = text_w(d, descriptor, val_f)
        d.text((x0, y), label, font=val_f, fill=INK)
        if lw + min_gap + dw <= w:
            d.text((x0 + w - dw, y), descriptor, font=val_f, fill=GOLD)
            y += line_h + text_bar_gap
        else:
            y += line_h + 4
            d.text((x0, y), descriptor, font=val_f, fill=GOLD)
            y += line_h + text_bar_gap
        d.rounded_rectangle([x0, y, x0 + w, y + bar_h], radius=bar_h // 2, fill=LINE)
        fill_w = max(bar_h, int(w * frac))
        d.rounded_rectangle([x0, y, x0 + fill_w, y + bar_h], radius=bar_h // 2, fill=pal["SIGNATURE"])
        y += bar_h + row_gap
    qa.box("!dashboard", (x0, y0, x0 + w, y))
    qa.size("dashboard_label", 60)
    return y


# --------------------------------------------------------------- cover ----
def quick_sip_cover(slot, slide_no, total, pal):
    """PAGE 1. slots: photo, title, tagline, para1, para1_lead_words,
    para2, para2_lead_words, bench_heading, bench_photo, bench_wine,
    bench_producer, bench_origin, bench_note.

    v5 STANDARD (as of the Santa Ynez redesign): a smaller, left-anchored
    title (title_size=110, title_align="left") sitting flush with the
    photo's bottom edge, tagline_size=80 directly beneath it; two short
    run-in paragraphs (para1/para2) each with their own bold baseline-
    aligned lead-in (para1_lead_words default 3, para2_lead_words
    default 2), sitting entirely ABOVE the benchmark bottle (rendered
    via wrap_around with obstacle=None -- see the two non-exempt QA
    guards below); optional structure dashboard under para2, separated
    by dashboard_gap (default 70); benchmark bottle bottom-right,
    caption reads producer above wine name.

    LEGACY PATH (pre-redesign, still fully supported): omit para1/para2
    and pass eyebrow, stats[3x(num,label)], body, lead_words instead --
    renders the old stat-strip + single wrap-around-the-bottle paragraph
    layout. Set title_size=200, title_align="right", tagline_size=60
    explicitly to reproduce the original look (the coded defaults are
    now 110/"left"/80 regardless of which body path is used).

    Optional overrides either path accepts: title_size, title_align,
    tagline_size, tagline_align (defaults to title_align), bottle_h
    (default 1185), dashboard_gap (default 70, para1/para2 path only)."""
    img, d, qa = _start("QS-01 cover", slide_no, total, pal)
    qa.word_limit = 130
    # photo_h is overridable. At the fixed 850 the legibility chip --
    # which is sized to the title+tagline block and runs to the photo's
    # bottom edge -- ate most of the frame on a two-line title, leaving
    # a hero photograph with only a strip of sky visible above it.
    photo_h = slot.get("photo_h", 850)
    im = cover_fit(load_photo(slot["photo"]), W, photo_h)
    img.paste(im, (0, 0))
    d = ImageDraw.Draw(img)
    # mark_scrim is separate from caption_chip. One flag used to drive
    # both the corner mark's own scrim and the title/tagline legibility
    # chip, so switching off a chip that covered too much photo also
    # stripped the protection from the "Quick Sips" wordmark at the top
    # of the frame -- two different elements, at opposite ends of the
    # page, over completely different pixels. Default follows
    # caption_chip so nothing changes for existing decks.
    qs_mark_overlay(img, d, pal,
                    scrim_on=slot.get("mark_scrim", slot.get("caption_chip", True)),
                    text_color=slot.get("mark_color"), qa=qa)

    title_size = slot.get("title_size", 110)
    title_align = slot.get("title_align", "left")
    tagline_size = slot.get("tagline_size", 80)
    tagline_align = slot.get("tagline_align", title_align)

    # "!" prefix: the v5 redesign intentionally runs the title/tagline
    # gap tighter than the hierarchy check's default margin -- exempted
    # from both the type-floor and headline-vs-body hierarchy checks,
    # same pattern as the detail page's "!title"/"!body_lead".
    # Multi-line titles. The shrink-to-fit loop and every measurement
    # below used to treat slot["title"] as one string, so a title
    # containing a literal "\n" measured as a single very wide line --
    # it shrank far more than it needed to, then drew both lines on one
    # baseline, and the tagline (positioned from a single line height)
    # printed straight through the second line. Split first, measure the
    # widest line, and let the block's real height drive what sits under
    # it.
    tf = font("display_black", title_size)
    title_lines = slot["title"].split("\n")
    avail_title_w = W - 2 * M
    while (max(text_w(d, ln, tf) for ln in title_lines) > avail_title_w
           and title_size > 60):
        title_size -= 2
        tf = font("display_black", title_size)
    qa.size("!title", title_size, headline=True)
    tw = max(text_w(d, ln, tf) for ln in title_lines)
    tx = M if title_align == "left" else (W - M - tw)

    tgf = font("italbold", tagline_size)
    tgw = text_w(d, slot["tagline"], tgf)
    tgx = M if tagline_align == "left" else (W - M - tgw)

    # Bottom-anchor the whole title+tagline block to the photo block:
    # tagline sits a fixed pad above the photo's bottom edge, title sits
    # directly above the tagline (not independently positioned), so the
    # two always read as one anchored unit regardless of title length.
    # Overridable so a deck that reclaims vertical space elsewhere on the
    # photo (e.g. moving photo_caption off the bottom-right corner) can
    # sit the title/tagline block lower, closer to the photo's true
    # bottom edge, rather than leaving that space empty.
    bottom_pad = slot.get("title_bottom_pad", 60)
    block_gap = 20
    tga, tgd = tgf.getmetrics()
    tgy = photo_h - bottom_pad - (tga + tgd)
    tasc, tdesc = tf.getmetrics()
    title_lh = int((tasc + tdesc) * 0.92)
    ty = tgy - block_gap - title_lh * len(title_lines)

    # legibility chip sized to the ACTUAL title+tagline block (plus a
    # little padding), not a blind fixed-height guess -- a fixed 460px
    # flat block shipped here once and covered roughly half the photo
    # regardless of how much text there actually was; don't reintroduce
    # a fixed height here. Applied before the caption/eyebrow/title/
    # tagline text so nothing gets painted over afterward.
    # Legibility chip is opt-out (caption_chip=False) not opt-in: most
    # photos need SOME protection for white title/tagline text, so the
    # safe default keeps it. This deck's photo has natural contrast
    # under the text and turned it off explicitly -- don't flip this
    # default off system-wide on the strength of one photo working
    # fine without it.
    if slot.get("caption_chip", True):
        chip(img, (0, ty - 40, W, photo_h), (10, 10, 10), opacity=0.72)
    elif slot.get("title_scrim", False):
        # Middle setting between the flat chip and nothing. Same region
        # the chip covered, but as a gradient that is fully transparent
        # at the top of the title block and strongest at the photo's
        # bottom edge -- so the photograph reads through where the
        # picture actually is (sky, horizon, whatever the subject is)
        # and the type still has a footing where it sits. The flat chip
        # protects text that does not need it, which is what makes it
        # look like it is blocking the image.
        scrim(img, (0, ty - 60, W, photo_h), "bottom",
              slot.get("title_scrim_strength", 0.78))
    d = ImageDraw.Draw(img)

    if slot.get("photo_caption"):
        # Was Cormorant Italic at 44 per the style guide's type table.
        # Reversed out white over a photograph at that size the fine
        # strokes dissolve -- the same failure the Field Guide series hit
        # and fixed by moving photo captions to core.CAPTION_FACE. Same
        # face here, so the two series' photo captions match, and one
        # size down from the shared constant since this one sits inside
        # the title chip rather than on bare photo.
        #
        # photo_caption_pos: "bottom_right" (default, unchanged) sits
        # inside the title/tagline legibility zone as before. "top_right"
        # pairs it with the top-left wordmark instead -- for decks that
        # move the caption up to reclaim bottom-of-photo space for a
        # larger title/tagline block. Vertically centred on the mark's
        # own band (pad=40, content_h=144 from qs_mark_overlay) so the
        # two read as a matched top-left/top-right pair.
        pcf = font(core.CAPTION_FACE, core.CAPTION_SIZE - 8)
        pcw = text_w(d, slot["photo_caption"], pcf)
        pc_color = slot.get("photo_caption_color", (240, 235, 224))
        pos = slot.get("photo_caption_pos", "bottom_right")
        pasc, pdesc = pcf.getmetrics()
        if pos == "top_right":
            mark_band_center = 40 + 144 // 2
            pc_y = mark_band_center - (pasc + pdesc) // 2
        else:
            pc_y = photo_h - 66
        # Tight chip, same reasoning as qs_mark_overlay's: top_right sits
        # outside both the caption_chip and title_scrim zones (those only
        # cover the bottom of the photo), so a light caption color there
        # has no backing at all unless this deck also lit up mark_scrim.
        # Only fires for top_right + a light color -- bottom_right is
        # unaffected, it already sits inside the protected zone above.
        is_light_caption = sum(pc_color[:3]) / 3 > 128
        if pos == "top_right" and is_light_caption:
            tight_pad = 20
            chip(img, (W - M - pcw - tight_pad, pc_y - tight_pad,
                        W - M + tight_pad, pc_y + pasc + pdesc + tight_pad),
                 (10, 10, 10), opacity=0.55)
            d = ImageDraw.Draw(img)
        d.text((W - M - pcw, pc_y), slot["photo_caption"], font=pcf, fill=pc_color)
        qa.size("!photo_caption", core.CAPTION_SIZE - 8)
        # Real pixel check, not an assumed background -- a scrim can look
        # fine in code and still fail against the actual photo underneath
        # (region_luminance's own docstring). Now meaningful even with a
        # chip present: the chip is a real rendered rectangle, so this
        # samples ITS luminance, not the raw photo's, and correctly
        # reflects whether the chip actually did its job.
        qa.check_photo_contrast(
            img, (W - M - pcw, pc_y, W - M, pc_y + pasc + pdesc),
            sum(pc_color[:3]) / 3, "photo_caption")

    if slot.get("eyebrow"):
        ey_f = font("kicker_bold", 60)
        ey = slot["eyebrow"]
        tracked_text(d, (M, photo_h - 380), ey, ey_f, GOLD, tracking=6)
        qa.size("eyebrow", 60)

    if slot.get("title_chip", False):
        pad = 24
        chip(img, (tx - pad, ty - pad, tx + tw + pad,
                   ty + title_lh * len(title_lines) + pad),
             slot.get("title_chip_color", (255, 255, 255)),
             opacity=slot.get("title_chip_opacity", 0.16))
        d = ImageDraw.Draw(img)

    _ty = ty
    for _ln in title_lines:
        _lx = M if title_align == "left" else (W - M - text_w(d, _ln, tf))
        d.text((_lx, _ty), _ln, font=tf, fill=slot.get("title_color", PAPER))
        _ty += title_lh
    qa.check_contrast(slot.get("title_color", PAPER), slot.get("title_contrast_bg", (40, 38, 34)), large=True, label="title")

    if slot.get("tagline_chip", False):
        tgb = d.textbbox((tgx, tgy), slot["tagline"], font=tgf)
        pad = 20
        chip(img, (tgb[0] - pad, tgb[1] - pad, tgb[2] + pad, tgb[3] + pad),
             slot.get("tagline_chip_color", (255, 255, 255)),
             opacity=slot.get("tagline_chip_opacity", 0.16))
        d = ImageDraw.Draw(img)

    d.text((tgx, tgy), slot["tagline"], font=tgf, fill=slot.get("tagline_color", (235, 228, 214)))
    qa.size("tagline", tagline_size)

    y = photo_h + 60
    bottle_h = slot.get("bottle_h", 1185)

    if "para1" in slot:
        # --- v5 standard path: two run-in paragraphs above the bottle ---
        # v8.1: body/lead sizes lowered from 80/105 to 70/90. The old
        # lead_size=105 sat too close to a typical auto-shrunk title
        # (~128px for a longer title like "Edelzwicker Blends from
        # Alsace") -- only an ~18% gap, not enough hierarchy separation
        # between title and lead-in. Confirmed on a real deck before
        # locking in; still overridable per deck via body_size/lead_size.
        body_size = slot.get("body_size", 70)
        lead_size = slot.get("lead_size", 90)
        bf = font("body_light", body_size)
        bf_bold = font("display_bold", lead_size)
        qa.size("!para1_lead", lead_size); qa.size("!para2_lead", lead_size)

        # para1/para2 render with obstacle=None -- they're meant to sit
        # entirely above the benchmark bottle, not carve around it, so
        # nothing here stops them from silently running into the bottle
        # if the copy gets too long. The paragraph-overlap check below
        # closes that gap with a real, non-exempt FAIL.
        para_leading = slot.get("para_leading", 1.22)
        y = wrap_around(d, M, y, W - 2 * M, slot["para1"], bf, INK, obstacle=None, leading=para_leading,
                         lead_font=bf_bold, lead_fill=pal["SIGNATURE"],
                         lead_words=slot.get("para1_lead_words", 3))
        y += slot.get("para_gap", 36)
        end_y = wrap_around(d, M, y, W - 2 * M, slot["para2"], bf, INK, obstacle=None, leading=para_leading,
                             lead_font=bf_bold, lead_fill=pal["SIGNATURE"],
                             lead_words=slot.get("para2_lead_words", 2))
        qa.add_words(slot["para1"] + " " + slot["para2"]); qa.size("body", body_size)

        # Tasting notes and dashboard now share one top: the dashboard's
        # position (paragraph end + gap) is the anchor, and the bottle
        # caption is pinned to match it via cap_y_override, rather than
        # each computing its own independent vertical position.
        dashboard_gap = slot.get("dashboard_gap", 70)
        shared_top = end_y + dashboard_gap

        obstacle, obstacle_top, cap_y_actual = qs_benchmark_bottle(
            img, d, pal, qa, slot["bench_heading"], slot["bench_photo"],
            slot["bench_wine"], slot["bench_producer"], slot["bench_origin"], slot["bench_note"],
            M, W - 2 * M, H, bottle_h=bottle_h, bleed_right=60, bleed_bottom=66,
            cap_w=slot.get("cap_w", 500), cap_y_override=shared_top, cap_gap=slot.get("cap_gap", 70))
        d = ImageDraw.Draw(img)

        if end_y > obstacle[1]:
            qa.notes.append(f"FAIL paragraph-overlap: para1/para2 bottom {end_y} "
                             f"> bottle-lockup top {obstacle[1]}")

        if "structure" in slot:
            dash_w = obstacle[0] - M - 40
            dash_y = shared_top
            dash_bottom = qs_tasting_dashboard(d, dash_y, M, dash_w, pal, qa, slot["structure"],
                                                header_gap=slot.get("dash_header_gap", 48),
                                                pre_row_gap=slot.get("dash_pre_row_gap", 14),
                                                row_gap=slot.get("dash_row_gap", 10),
                                                text_bar_gap=slot.get("dash_text_bar_gap", 8),
                                                bar_h=slot.get("dash_bar_h", 14))
            if dash_bottom > CONTENT_BOTTOM:
                qa.notes.append(f"FAIL dashboard-footer: dashboard bottom {dash_bottom} "
                                 f"> CONTENT_BOTTOM {CONTENT_BOTTOM}")
    else:
        # --- legacy path: stat strip + single paragraph wrapping the bottle ---
        y = qs_stat_strip(d, y, slot["stats"], pal, qa, M, W - 2 * M) + 50
        d.line([(M, y), (W - M, y)], fill=LINE, width=2)
        y += 40

        obstacle, _ = qs_benchmark_bottle(
            img, d, pal, qa, slot["bench_heading"], slot["bench_photo"],
            slot["bench_wine"], slot["bench_producer"], slot["bench_origin"], slot["bench_note"],
            M, W - 2 * M, H, bottle_h=bottle_h, bleed_right=60, bleed_bottom=66)
        d = ImageDraw.Draw(img)
        bf = font("body_light", 70)
        bf_bold = font("display_bold", 85)
        end_y = wrap_around(d, M, y, W - 2 * M, slot["body"], bf, INK, obstacle=obstacle, leading=1.18,
                             lead_font=bf_bold, lead_fill=pal["SIGNATURE"], lead_words=slot.get("lead_words", 4),
                             gap_before_obstacle=slot.get("body_gap_before_obstacle", 50))
        qa.box("!body", (M, y, M + 200, end_y))
        qa.add_words(slot["body"]); qa.size("body", 70)

        if "structure" in slot:
            dash_w = obstacle[0] - M - 40
            qs_tasting_dashboard(d, end_y + 50, M, dash_w, pal, qa, slot["structure"])

    return _finish(img, d, qa, slide_no, total, page_pos="left", credit=slot.get("photo_credit"),
                   footer_size=slot.get("footer_size", 76))


# ---------------------------------------------------------------- detail --
def quick_sip_detail(slot, slide_no, total, pal):
    """PAGE 2. slots: topic, headline, body, bench_heading, bench_photo,
    bench_wine, bench_producer, bench_origin, bench_note,
    structure[list of (label, frac, descriptor) for the dashboard].

    Optional: photo / photo_h (default 620) — an optional hero band at
    the top of the page, same cover_fit treatment as the cover page but
    shorter. The corner mark still uses qs_mark_patch (self-painted
    colored rectangle, not the photo-overlay variant) per the standing
    corner-mark rule -- it reads fine over a photo since it paints its
    own background first. Everything below (headline, body, bottle,
    dashboard) shifts down to clear the photo. Omit photo for the
    original flat-background detail page.

    Optional: body_lead_words / body_lead_size (default 90) — an
    optional bold serif lead-in on the body paragraph, same run-in
    pattern as the cover page's para1/para2, sized one notch below the
    cover's 105 since the detail page's body font itself is a touch
    larger (75 vs 80 -- see STYLE_GUIDE_v5 §3). Omit body_lead_words
    (or leave it 0) for a plain, non-lead-in paragraph.
    bottle_h (default 1320) overridable per deck.

    topic drives the corner mark's 'Quick Sips - {topic}' lockup — see
    qs_mark_patch. Do not add a separate topic heading elsewhere on
    this page."""
    img, d, qa = _start("QS-02 detail", slide_no, total, pal)
    qa.word_limit = 130

    if slot.get("photo"):
        photo_h = slot.get("photo_h", 620)
        im = cover_fit(load_photo(slot["photo"]), W, photo_h)
        img.paste(im, (0, 0))
        d = ImageDraw.Draw(img)
        mark_h = qs_mark_patch(img, d, pal, topic=slot["topic"])
        if slot.get("photo_caption"):
            pcf = font("caption_italic", 44)
            pcw = text_w(d, slot["photo_caption"], pcf)
            chip(img, (0, photo_h - 110, W, photo_h), (10, 10, 10), opacity=0.55)
            d = ImageDraw.Draw(img)
            d.text((W - M - pcw, photo_h - 60), slot["photo_caption"], font=pcf, fill=(240, 235, 224))
            qa.size("!photo_caption", 44)
        y = max(mark_h, photo_h) + slot.get("content_pad", 60)
    else:
        mark_h = qs_mark_patch(img, d, pal, topic=slot["topic"])
        y = mark_h + slot.get("content_pad", 60)

    # Multi-line headlines -- same fix as the cover title above. A
    # headline containing a literal "\n" measured as one wide string,
    # over-shrank, drew both lines on a single baseline, and advanced y
    # by one line height, so the body paragraph printed through the
    # second line.
    hf_size = 110
    hf = font("display_black", hf_size)
    avail_hw = W - 2 * M
    head_lines = slot["headline"].split("\n")
    while (max(text_w(d, ln, hf) for ln in head_lines) > avail_hw
           and hf_size > 60):
        hf_size -= 2
        hf = font("display_black", hf_size)
    qa.size("!headline", hf_size, headline=True)
    ha, hd = hf.getmetrics()
    head_lh = int((ha + hd) * 0.98)
    for _ln in head_lines:
        d.text((M, y), _ln, font=hf, fill=INK)
        y += head_lh
    y += 30

    obstacle, obstacle_top, cap_y_actual = qs_benchmark_bottle(
        img, d, pal, qa, slot["bench_heading"], slot["bench_photo"],
        slot["bench_wine"], slot["bench_producer"], slot["bench_origin"], slot["bench_note"],
        M, W - 2 * M, H, bottle_h=slot.get("bottle_h", 1320), bleed_right=slot.get("bleed_right", 60),
        bleed_bottom=slot.get("bleed_bottom", 40), cap_w=slot.get("cap_w", 500), cap_gap=slot.get("cap_gap", 70))
    d = ImageDraw.Draw(img)
    body_size = slot.get("body_size", 70)
    bf = font("body_light", body_size)
    lead_words = slot.get("body_lead_words", 0)
    if lead_words:
        bf_bold = font("display_bold", slot.get("body_lead_size", 90))
        qa.size("!body_lead", slot.get("body_lead_size", 90))
        end_y = wrap_around(d, M, y, W - 2 * M, slot["body"], bf, INK, obstacle=obstacle, leading=1.1,
                             lead_font=bf_bold, lead_fill=pal["SIGNATURE"], lead_words=lead_words)
    else:
        end_y = wrap_around(d, M, y, W - 2 * M, slot["body"], bf, INK, obstacle=obstacle, leading=1.1)
    qa.box("!body", (M, y, M + 200, end_y))
    qa.add_words(slot["body"]); qa.size("body", body_size)

    dash_w = obstacle[0] - M - 40
    # Dashboard top is pinned to the caption's OWN top (cap_y_actual),
    # not obstacle_top -- obstacle_top is min(bottle_top, cap_y) and
    # exists for body-text wrap-around purposes (it has to account for
    # the bottle image's own extent too), so using it here silently
    # misaligned the dashboard whenever the bottle photo's top edge
    # sat higher on the page than the caption text itself.
    dash_y = cap_y_actual
    dash_bottom = qs_tasting_dashboard(d, dash_y, M, dash_w, pal, qa, slot["structure"],
                                        header_gap=slot.get("dash_header_gap", 48),
                                        pre_row_gap=slot.get("dash_pre_row_gap", 16),
                                        row_gap=slot.get("dash_row_gap", 12),
                                        text_bar_gap=slot.get("dash_text_bar_gap", 8),
                                        bar_h=slot.get("dash_bar_h", 14))
    # Non-exempt guard (mirrors the cover page's dashboard-footer check,
    # §8 QUICK_SIPS_STYLE_GUIDE): a long body paragraph pushing end_y
    # late, combined with the standard 5-row dashboard, was silently
    # running the dashboard into the footer/swipe-cue zone -- the
    # dashboard's own box is "!dashboard"-exempt from the caption-zone
    # check, so nothing else caught this. Fix is the same as the cover
    # page: shorten body copy, or reduce bottle_h/photo_h.
    if dash_bottom > CONTENT_BOTTOM:
        qa.notes.append(f"FAIL dashboard-footer: dashboard bottom {dash_bottom} "
                         f"> CONTENT_BOTTOM {CONTENT_BOTTOM}")
    return _finish(img, d, qa, slide_no, total, page_pos="left", credit=slot.get("photo_credit"),
                   footer_label=slot.get("footer_label"), footer_size=slot.get("footer_size", 76))
