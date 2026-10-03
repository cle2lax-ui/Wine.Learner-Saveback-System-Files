"""WHAT AM I DRINKING? -- the redesigned Quick Sips two-pager.

Page 1  hero photo of the wine's place, full bleed; a logo lockup -- the
        series' wine glass with a question mark floating above it, with the
        large title-case title right beside it -- over a scrim; one paragraph on the place / producer and why it
        matters; the TASTING & STRUCTURE dashboard (the series' own
        qs_tasting_dashboard, unchanged) beside tasting notes; the READ MORE
        footer.
Page 2  the right 30% is a bottle shot; at the top left the logo lockup
        repeats with "I'm Drinking" (the answer to page 1's question); below
        it, in the title font, the producer, region, year and wine name; a few
        more words on the wine.

Both pages run through the QA harness; the word budget is the series' 130.

REUSE, NOT COPY: the dashboard, glass icon, run-in paragraphs, scrim and
footer all come from quick_sips.py / core.py / modules.py. This file only
adds the two layouts and the logo.

THE LOGO is the series' Lucide wine glass (quick_sips._qs_glass) with a
question mark drawn in the bowl, above the wine-level line. The glass is
drawn in its icon coordinates (392px square; bowl centred near x=195, its
empty upper part y~30-150), so the mark scales cleanly with the logo height.

THE BOTTLE PANEL assumes the supplied shot has a PURE WHITE background (the
panel is filled pure white so there is no seam). It scales the bottle to a
target height and crops the sides to the panel, centring on the bottle's own
bounding box, then applies a light unsharp mask. If the source is small the
enlargement will look soft: bottle_h is the bottle's height in px on the
page, and a source under ~1,500px tall should be treated as a placeholder.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import core
import modules
from core import (cover_fit, load_photo, font, text_w, paragraph, run_in, scrim,
                  tracked_text)
from tokens import W, H, M, PAPER, INK, LINE, FLOOR, CONTENT_BOTTOM, QUICKSIPS_GOLD
from quick_sips import qs_tasting_dashboard, _qs_glass

GOLD = QUICKSIPS_GOLD
WORD_LIMIT = 130          # the Quick Sips series budget


LOGO_MARK = (255, 222, 128)   # bright gold for the "?" and the italic line under the lockup.
                              # A brighter sibling of the series gold (168,130,60), which was too
                              # dim on the dark badge. Was (244,206,122); nudged brighter so the
                              # italic line over the photo clears 3:1 (gold is dimmer than white).


def wad_logo(img, x, y, h, tone="white", mark_color=None, badge=None):
    """The logo lockup: a solid disc (diameter h) holding a LARGE question
    mark floating above the series' wine glass. Returns h.

    First version put a small gold "?" inside the bowl; on the first render it
    was too small and too dim to read, and its dot sat on the wine-level line.
    Floating it above the glass lets it be big and bright, and the disc keeps
    the whole mark legible on any photo (the glass is see-through line art).
    Geometry is fractions of h so the lockup scales cleanly:
      "?" glyph top at 0.07h, glyph height ~0.36h; glass rim at 0.47h, glass
      ~0.44h tall, centred horizontally on the disc."""
    d0 = ImageDraw.Draw(img)
    cx, cy = x + h / 2.0, y + h / 2.0
    if badge:
        col, alpha = badge
        layer = Image.new("RGBA", (int(h), int(h)), (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse([0, 0, int(h) - 1, int(h) - 1], fill=tuple(col) + (int(255 * alpha),))
        img.paste(layer, (int(x), int(y)), layer)
    # glass: the icon asset is 392px square; its drawn content spans y 20-371
    # (351px), centred on x=195.5.
    vis_h = 0.44 * h
    ib = int(vis_h / (351.0 / 392.0))
    gx = int(cx - 195.5 * ib / 392.0)
    gy = int(y + 0.47 * h - 20 * ib / 392.0)
    _qs_glass(img, gx, gy, ib, tone=tone)
    # the "?": size it from its real glyph box so it is exactly 0.36h tall
    d = ImageDraw.Draw(img)
    target = 0.36 * h
    f = font("display_black", int(target / 0.72))
    bb = d.textbbox((0, 0), "?", font=f)
    for _ in range(6):                      # converge on the target glyph height
        gh_ = bb[3] - bb[1]
        if abs(gh_ - target) <= 2:
            break
        f = font("display_black", max(10, int(f.size * target / gh_)))
        bb = d.textbbox((0, 0), "?", font=f)
    gw_, gh_ = bb[2] - bb[0], bb[3] - bb[1]
    d.text((cx - gw_ / 2 - bb[0], y + 0.07 * h - bb[1]), "?", font=f,
           fill=mark_color or LOGO_MARK)
    return h


def wad_lockup(img, x, y, h, lines, size, text_fill, pal, gap=44, badge_alpha=0.92):
    """The logo lockup: the disc (question mark floating above the glass) with
    the title set right beside it, the text block centred on the disc by its
    real ink box (not its line box). Used on page 1 ("What am I / Drinking?")
    and repeated on page 2 ("I'm / Drinking"), which answers the question.
    Returns (text_left, text_top, text_right, text_bottom, line_h)."""
    wad_logo(img, x, y, h, tone="white", badge=(pal["SIGNATURE"], badge_alpha))
    d = ImageDraw.Draw(img)
    tf = font("display_black", size)
    asc, desc = tf.getmetrics()
    line_h = int((asc + desc) * 0.90)
    tx = x + h + gap
    top = d.textbbox((tx, y), lines[0], font=tf)[1]
    bot = d.textbbox((tx, y + line_h * (len(lines) - 1)), lines[-1], font=tf)[3]
    ty = int(y + (y + h / 2.0) - (top + bot) / 2.0)
    for i, ln in enumerate(lines):
        d.text((tx, ty + i * line_h), ln, font=tf, fill=text_fill)
    tw = max(text_w(d, l, tf) for l in lines)
    return tx, ty, tx + tw, ty + line_h * len(lines), line_h


def _fit_one_line(d, text, family, size, floor, max_w):
    f = font(family, size)
    while text_w(d, text, f) > max_w and size > floor:
        size -= 2
        f = font(family, size)
    if text_w(d, text, f) > max_w:
        raise ValueError(f"won't fit on one line: {text!r}")
    return f, size


def _check_hidden(slot):
    """Page 1 is a "guess the wine" layout: it must not name the wine, producer,
    vineyard or region. slot["hidden_terms"] lists words that must NOT appear
    anywhere in page 1's text (case-insensitive); the build fails if one does.
    The photograph is checked by eye -- no readable signs."""
    terms = [t.lower() for t in slot.get("hidden_terms", [])]
    if not terms:
        return
    texts = list(slot.get("title_lines", ["What am I", "Drinking?"]))
    texts += [slot.get("paragraph_lead", ""), slot.get("paragraph", ""),
              slot.get("notes_source", ""), slot.get("photo_credit", ""),
              slot.get("notes_heading", ""), slot.get("lockup_note", "")]
    texts += [t for pair in slot.get("notes", []) for t in pair]
    texts += [str(x) for row in slot.get("structure", []) for x in (row[0], row[2])]
    hits = sorted({t for t in terms for s_ in texts if t in s_.lower()})
    if hits:
        raise ValueError(f"page 1 names the answer -- hidden term(s) found: {hits}")


def wad_page1(slot, slide_no, total, pal):
    """slots: photo, photo_anchor(0.5), photo_zoom(1.0), photo_h(1080),
    photo_credit, title_lines(['What am I', 'Drinking?']), title_size(200),
    paragraph_lead, paragraph, structure[(label, frac, descriptor)],
    notes[(lead, text)], notes_source, dash_w(950), notes_heading('TASTING
    NOTES'), lockup_y(90), lockup_note (an italic line under the lockup),
    scrim_h(1.0), scrim_strength(0.90), lockup_note_gap(44)."""
    _check_hidden(slot)
    img, d, qa = modules._start("WAD-01 page1", slide_no, total, pal)
    qa.word_limit = WORD_LIMIT
    ph = slot.get("photo_h", 1080)
    img.paste(cover_fit(load_photo(slot["photo"]), W, ph,
                        y_anchor=slot.get("photo_anchor", 0.5),
                        zoom=slot.get("photo_zoom", 1.0)), (0, 0))
    # a scrim at each end of the photo: the title sits low, the logo high.
    # First pass used 0.80 / 0.55 over 0.42 / 0.30: the vineyard went muddy and
    # the scrim ghosted the vineyard sign. Lighter, and the sign now sits in the
    # clear band between the two.
    # Measured on the Bremm hero: at 0.68 from 0.50 the brightest 10% of the pixels
    # behind the title's first line fell to 2.8:1 (golden field patches), so the
    # scrim starts earlier and is a little stronger. No text shadow -- not used on
    # this series' photos.
    # The lockup now sits in the TOP-LEFT corner (Steve), so the scrim moves to
    # the top and fades out down the photo: the lower half of the hero stays
    # untouched and colourful. Strength/height are measured against the
    # brightest background behind the title and the italic line (see the deck's
    # notes), not guessed.
    # Swept on the Bremm hero (brightest-10% contrast behind the italic line):
    # h .78 / s .78 -> 2.5:1;  .90 / .88 -> 3.0;  1.00 / .90 -> 3.4:1, for a ~12%
    # drop in the lower photo's brightness. A shorter scrim left the thin italic
    # strokes unreadable over the sunlit vineyard.
    scrim(img, (0, 0, W, int(ph * slot.get("scrim_h", 1.0))), dark_at="top",
          strength=slot.get("scrim_strength", 0.96))
    d = ImageDraw.Draw(img)

    # LOGO LOCKUP: the icon and the title side by side (title right next to the
    # glass and question mark), top-left of the photo, with an optional italic
    # instruction line beneath it. The title block is centred vertically on
    # the disc using its real ink box, not its line box.
    logo_h = slot.get("logo_h", 320)          # was 380; Steve: "a little" smaller
    lines = slot.get("title_lines", ["What am I", "Drinking?"])
    ly = slot.get("lockup_y", 90)
    tx, ty, tr, tb, line_h = wad_lockup(img, M, ly, logo_h, lines, slot.get("title_size", 160),
                                        PAPER, pal, gap=slot.get("lockup_gap", 44))
    d = ImageDraw.Draw(img)
    qa.size("title", slot.get("title_size", 160), headline=True)
    qa.add_words(" ".join(lines))
    qa.box("logo", (M, ly, M + logo_h, ly + logo_h))
    qa.box("title", (tx, ty, tr, tb))
    note = slot.get("lockup_note")
    if note:
        nf, ns = _fit_one_line(d, note, "italbold", slot.get("lockup_note_size", 64), 60, W - 2 * M)
        ny = ly + logo_h + slot.get("lockup_note_gap", 40)
        # bright gold, the same as the logo's "?" (Steve): see the contrast notes
        d.text((M, ny), note, font=nf, fill=slot.get("lockup_note_fill", LOGO_MARK))
        na, nd = nf.getmetrics()
        qa.size("lockup_note", ns)
        qa.add_words(note)
        qa.box("lockup_note", (M, ny, M + text_w(d, note, nf), ny + na + nd))

    # paragraph: why the place / producer matters
    y = ph + 60
    end = run_in(d, (M, y), slot["paragraph_lead"], slot["paragraph"], W - 2 * M, pal)
    qa.box("paragraph", (M, y, W - M, end))
    qa.size("paragraph", core.TYPE["body"])
    qa.add_words(slot["paragraph"])

    # dashboard (left) and tasting notes (right), tops aligned
    dy = end + 60
    dash_w = slot.get("dash_w", 950)
    dend = qs_tasting_dashboard(d, dy, M, dash_w, pal, qa, slot["structure"],
                                header_gap=56, pre_row_gap=22, row_gap=18)
    for _, _, desc_ in slot["structure"]:
        qa.add_words(desc_)

    nx = M + dash_w + 90
    nw = W - M - nx
    kf = font("kicker_bold", 60)
    tracked_text(d, (nx, dy), slot.get("notes_heading", "TASTING NOTES"), kf, pal["SIGNATURE"], tracking=4)
    ny = dy + 56
    d.line([(nx, ny), (nx + nw, ny)], fill=LINE, width=2)
    ny += 22
    for lead, txt in slot["notes"]:
        y0 = ny
        ny = run_in(d, (nx, ny), lead, txt, nw, pal, lead_size=60, body_size=60, leading=1.26) + 8
        qa.box(f"note:{lead}", (nx, y0, nx + nw, ny - 8))
        qa.add_words(txt)
    if slot.get("notes_source"):
        sf = font("italbold", 60)
        d.text((nx, ny + 4), slot["notes_source"], font=sf, fill=GOLD)
        sa, sd = sf.getmetrics()
        qa.box("notes_source", (nx, ny + 4, nx + text_w(d, slot["notes_source"], sf), ny + 4 + sa + sd))
        ny += sa + sd + 4
    bottom = max(dend, ny)
    if bottom > CONTENT_BOTTOM:
        qa.notes.append(f"FAIL structure-bottom: {bottom} > CONTENT_BOTTOM {CONTENT_BOTTOM}")
    return modules._finish(img, d, qa, slide_no, total, credit=slot.get("photo_credit"))


def _bottle_panel(img, path, panel_x, bottle_h, sharpen=True):
    """Paint the right-hand panel pure white and place the bottle in it,
    scaled so the BOTTLE (found by its difference from the white background)
    is bottle_h tall on the page, centred on the panel horizontally and the
    page vertically."""
    src = Image.open(path).convert("RGB")
    a = np.asarray(src).astype(int)
    diff = np.abs(a - 255).sum(2) > 40
    ys, xs = np.where(diff)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    s = bottle_h / float(by1 - by0)
    big = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    if sharpen:
        big = big.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=3))
    pw = W - panel_x
    panel = Image.new("RGB", (pw, H), (255, 255, 255))
    cx_big = int((bx0 + bx1) / 2 * s)
    cy_big = int((by0 + by1) / 2 * s)
    panel.paste(big, (pw // 2 - cx_big, H // 2 - cy_big))
    img.paste(panel, (panel_x, 0))
    return dict(scale=s, src_size=src.size, bottle_px=(int((bx1 - bx0) * s), int((by1 - by0) * s)))


def wad_page2(slot, slide_no, total, pal):
    """slots: bottle (path), panel_frac(0.30), bottle_h(2500), producer,
    region_year, wine_lines[...], rule(True), lead, body, and the lockup that
    repeats the page 1 logo: lockup_lines(["I\u2019m", "Drinking"]),
    lockup_h(300), lockup_size(150), lockup_y(110), lockup_gap(40)."""
    img, d, qa = modules._start("WAD-02 page2", slide_no, total, pal)
    qa.word_limit = WORD_LIMIT
    panel_x = int(W * (1 - slot.get("panel_frac", 0.30)))
    info = _bottle_panel(img, slot["bottle"], panel_x, slot.get("bottle_h", 2500))
    d = ImageDraw.Draw(img)
    qa.notes.append(f"info bottle enlarged x{info['scale']:.2f} from {info['src_size']}")

    # The lockup repeats here with the answer's lead-in: the same disc, "?" and
    # glass, set beside "I'm / Drinking" instead of "What am I / Drinking?".
    lock_h = slot.get("lockup_h", 300)
    lock_y = slot.get("lockup_y", 110)
    lock_lines = slot.get("lockup_lines", ["I\u2019m", "Drinking"])
    lock_size = slot.get("lockup_size", 150)
    lx, lty, lr, lb, _ = wad_lockup(img, M, lock_y, lock_h, lock_lines, lock_size,
                                    pal["SIGNATURE"], pal, gap=slot.get("lockup_gap", 40),
                                    badge_alpha=1.0)
    d = ImageDraw.Draw(img)
    qa.size("lockup_text", lock_size)
    qa.add_words(" ".join(lock_lines))
    qa.box("lockup", (M, lock_y, lr, max(lock_y + lock_h, lb)))

    tx = M
    tw_max = panel_x - M - 100
    y = slot.get("title_top", 250)

    pf, ps = _fit_one_line(d, slot["producer"], "display_black", 200, 120, tw_max)
    d.text((tx, y), slot["producer"], font=pf, fill=pal["SIGNATURE"])
    a, dsc = pf.getmetrics(); y += int((a + dsc) * 0.96)
    qa.size("producer", ps, headline=True)

    rf, rs = _fit_one_line(d, slot["region_year"], "display_bold", 110, 80, tw_max)
    d.text((tx, y), slot["region_year"], font=rf, fill=GOLD)
    a, dsc = rf.getmetrics(); y += int((a + dsc) * 1.15) + 40
    qa.size("region_year", rs)

    sizes = []
    for ln in slot["wine_lines"]:
        f, s_ = _fit_one_line(d, ln, "display_black", 124, 84, tw_max)
        sizes.append(s_)
    wsz = min(sizes)                               # one size for the whole name
    wf = font("display_black", wsz)
    for ln in slot["wine_lines"]:
        d.text((tx, y), ln, font=wf, fill=INK)
        a, dsc = wf.getmetrics(); y += int((a + dsc) * 0.98)
    qa.size("wine_name", wsz)
    qa.box("title_stack", (tx, slot.get("title_top", 250), tx + tw_max, y))
    qa.add_words(" ".join([slot["producer"], slot["region_year"]] + slot["wine_lines"]))

    y += 70
    if slot.get("rule", True):
        d.line([(tx, y), (tx + 260, y)], fill=GOLD, width=6)
        y += 70
    end = run_in(d, (tx, y), slot["lead"], slot["body"], tw_max, pal)
    qa.box("body", (tx, y, tx + tw_max, end))
    qa.size("body", core.TYPE["body"])
    qa.add_words(slot["body"])
    return modules._finish(img, d, qa, slide_no, total, page_pos="left",
                           footer_label=slot.get("footer_label", ""),
                           credit=slot.get("photo_credit"), footer_size=76)
