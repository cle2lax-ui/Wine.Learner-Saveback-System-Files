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
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import core
import modules
from core import (cover_fit, load_photo, font, text_w, paragraph, run_in, scrim,
                  tracked_text)
from tokens import W, H, M, PAPER, INK, LINE, FLOOR, CONTENT_BOTTOM, QUICKSIPS_GOLD, SCRIM
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


def wad_lockup(img, x, y, h, lines, size, text_fill, pal, gap=44, badge_alpha=0.92,
               note=None, note_size=64, note_fill=None, note_gap=18):
    """The logo lockup: the disc (question mark floating above the glass) with
    the title set right beside it, the text block centred on the disc by its
    real ink box (not its line box). Used on page 1 ("What am I Drinking?") and
    repeated on page 2 ("I'm / Drinking"), which answers the question.

    If `note` is given it is set in italics directly UNDER the title, its ink
    left-aligned with the title's ink, and the title + note stack is centred on
    the disc as ONE unit: the note is part of the lockup, not a caption hanging
    off it. (note_gap is the distance from the title's lowest ink, the "g"'s
    descender, to the note's top ink.) Without a note the drawing is exactly what
    it was before the note existed (page 2 depends on that).

    Returns (text_left, text_top, text_right, text_bottom, line_h, extras);
    text_right includes the note; text_bottom is the note's ink bottom when there
    is one; extras = dict(note_box=(x0, y0, x1, y1) or None, note_size=int)."""
    wad_logo(img, x, y, h, tone="white", badge=(pal["SIGNATURE"], badge_alpha))
    d = ImageDraw.Draw(img)
    tf = font("display_black", size)
    asc, desc = tf.getmetrics()
    line_h = int((asc + desc) * 0.90)
    tx = x + h + gap
    top = d.textbbox((tx, y), lines[0], font=tf)[1]
    title_bot = d.textbbox((tx, y + line_h * (len(lines) - 1)), lines[-1], font=tf)[3]
    bot = title_bot
    nf, nb0, note_dy = None, None, 0
    if note:
        nf, nsz = _fit_one_line(d, note, "italbold", note_size, 60, W - M - tx)
        nb0 = d.textbbox((0, 0), note, font=nf)
        note_dy = (title_bot + note_gap) - nb0[1]
        bot = note_dy + nb0[3]
    ty = int(y + (y + h / 2.0) - (top + bot) / 2.0)
    shift = ty - y
    for i, ln in enumerate(lines):
        d.text((tx, ty + i * line_h), ln, font=tf, fill=text_fill)
    right = tx + max(text_w(d, l, tf) for l in lines)
    extras = dict(note_box=None, note_size=None)
    text_bottom = ty + line_h * len(lines)
    if note:
        tb0 = d.textbbox((0, 0), lines[0], font=tf)
        nx = tx + tb0[0] - nb0[0]
        ny = int(note_dy + shift)
        d.text((nx, ny), note, font=nf, fill=note_fill or text_fill)
        extras = dict(note_box=(nx + nb0[0], ny + nb0[1], nx + nb0[2], ny + nb0[3]), note_size=nsz)
        right = max(right, nx + nb0[2])
        text_bottom = ny + nb0[3]
    return tx, ty, right, text_bottom, line_h, extras


def _fit_one_line(d, text, family, size, floor, max_w):
    f = font(family, size)
    while text_w(d, text, f) > max_w and size > floor:
        size -= 2
        f = font(family, size)
    if text_w(d, text, f) > max_w:
        raise ValueError(f"won't fit on one line: {text!r}")
    return f, size


def band_scrim(img, y0, y1, strength, feather, x_hold=None, x_end=None, floor=0.0,
               limit_y=None, color=None):
    """A horizontal band of darkness across [y0, y1] with smoothstep-feathered
    top and bottom edges (`feather` px each), optionally fading out horizontally
    from x_hold to x_end down to `floor` of its strength. Applied only to rows
    above limit_y (the photo band), so it never touches the paper below.
    core.scrim() cannot do this: it is a one-sided gradient, zero at one edge."""
    W_, H_ = img.size
    H_ = min(H_, limit_y) if limit_y else H_
    ys = np.arange(H_, dtype=float)[:, None]
    up = np.clip((ys - (y0 - feather)) / float(feather), 0, 1)
    dn = np.clip(((y1 + feather) - ys) / float(feather), 0, 1)
    prof = np.minimum(up, dn)
    prof = prof * prof * (3 - 2 * prof)
    xs = np.arange(W_, dtype=float)[None, :]
    if x_hold is None:
        fx = np.ones((1, W_))
    else:
        t = np.clip((xs - x_hold) / float(max(x_end - x_hold, 1)), 0, 1)
        t = t * t * (3 - 2 * t)
        fx = 1 - (1 - floor) * t
    alpha = (strength * prof * fx)[..., None]
    reg = np.asarray(img.crop((0, 0, W_, H_))).astype(float)
    col = np.array(color or SCRIM, dtype=float)
    out = reg * (1 - alpha) + col * alpha
    img.paste(Image.fromarray(out.clip(0, 255).astype("uint8")), (0, 0))


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
    NOTES'), lockup_y(centred on the photo if omitted), lockup_note (an italic line set directly
    UNDER THE TITLE, part of the lockup), lockup_note_gap(18: title ink to note ink),
    scrim_strength(0.40), scrim_feather(100), scrim_pad(25), scrim_x_hold(1500),
    scrim_floor(0.30), disc_alpha(0.92). The lockup group (lockup + italic line)
    is centred vertically on the photo unless lockup_y is given."""
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
    # LOGO LOCKUP: the disc, the title beside it, and the italic instruction line
    # directly UNDER THE TITLE as part of the lockup (Steve). The title + note stack is
    # centred on the disc, so the whole lockup is exactly one disc tall.
    logo_h = slot.get("logo_h", 320)          # was 380; Steve: "a little" smaller
    lines = slot.get("title_lines", ["What am I", "Drinking?"])
    note = slot.get("lockup_note")
    ly = slot.get("lockup_y", int((ph - logo_h) / 2))

    # The dark band sits behind the lockup and feathers out, fading to the right where
    # the lockup ends so the rest of the hero keeps its colour. core.scrim() is a
    # one-sided gradient and cannot protect a lockup that is not at the photo's edge.
    # Strength is measured, not guessed (see the deck notes): a first attempt at
    # 0.80 met every target by a mile but kept only 41% of the photo's brightness.
    band_scrim(img, ly - slot.get("scrim_pad", 25), ly + logo_h + slot.get("scrim_pad", 25),
               strength=slot.get("scrim_strength", 0.40), feather=slot.get("scrim_feather", 100),
               x_hold=slot.get("scrim_x_hold", 1500), x_end=W, floor=slot.get("scrim_floor", 0.30),
               limit_y=ph)
    d = ImageDraw.Draw(img)

    # bright gold note, the same as the logo's "?" (Steve): see the contrast notes
    tx, ty, tr, tb, line_h, ex = wad_lockup(
        img, M, ly, logo_h, lines, slot.get("title_size", 160), PAPER, pal,
        gap=slot.get("lockup_gap", 44), badge_alpha=slot.get("disc_alpha", 0.92),
        note=note, note_size=slot.get("lockup_note_size", 64),
        note_fill=slot.get("lockup_note_fill", LOGO_MARK), note_gap=slot.get("lockup_note_gap", 18))
    d = ImageDraw.Draw(img)
    if tr > W - M:
        # Steve: the title must not wrap, and nothing in the lockup may pass the margin.
        # A line that runs past it fails the build: shrink the size or shorten the copy.
        qa.notes.append(f"FAIL lockup-width: the lockup ends at x={tr}, past the right margin {W - M}")
    qa.size("title", slot.get("title_size", 160), headline=True)
    qa.add_words(" ".join(lines))
    qa.box("logo", (M, ly, M + logo_h, ly + logo_h))
    qa.box("title", (tx, ty, tr, ty + line_h * len(lines)))
    if note:
        qa.size("lockup_note", ex["note_size"])
        qa.add_words(note)
        qa.box("lockup_note", ex["note_box"])
    qa.notes.append(f"info lockup: disc {logo_h}px at y={ly}; text stack ink y={ty}..{tb}")

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


def _bottle_panel(img, path, panel_x, bottle_h, top=None, sharpen=True, denoise=True, paper=PAPER):
    """Paint the right-hand panel in the PAPER colour and place the bottle in it.

    The bottle (found by its difference from the shot's own background, taken as
    the median of its border) is scaled to be bottle_h tall on the page, centred
    on the panel horizontally, with its TOP at `top` (default: centred on the page).
    The whole shot is then multiplied by paper/background so its near-white
    backdrop becomes exactly the page's cream: no seam between panel and page (a
    pure-white panel beside cream was only 4-6 levels apart, which reads as
    neither a deliberate panel nor a seamless page).

    denoise=True smooths the JPEG blocking before a two-step upscale; it is the
    better choice for the small shots this format gets (see the guide). Returns
    the scale and the bottle's top and bottom on the page."""
    src = Image.open(path).convert("RGB")
    a = np.asarray(src).astype(int)
    border = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3),
                             a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    diff = np.abs(a - bg).sum(2) > 40
    ys, xs = np.where(diff)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    s = bottle_h / float(by1 - by0)
    size = (int(src.width * s), int(src.height * s))
    if denoise:
        den = cv2.fastNlMeansDenoisingColored(np.asarray(src)[:, :, ::-1].copy(), None, 5, 5, 5, 15)[:, :, ::-1]
        big = Image.fromarray(den)
        big = big.resize((big.width * 2, big.height * 2), Image.LANCZOS).resize(size, Image.LANCZOS)
        if sharpen:
            big = big.filter(ImageFilter.UnsharpMask(radius=2.0, percent=80, threshold=2))
    else:
        big = src.resize(size, Image.LANCZOS)
        if sharpen:
            big = big.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=3))
    # Tone-match using the background AS IT IS AFTER processing: the denoise and the
    # sharpen shift the near-white backdrop slightly (the original's border is 255, the
    # processed backdrop was ~254), and scaling by the original's value left a 1-level
    # step against the page's paper.
    ba = np.asarray(big).astype(float)
    bg2 = np.median(np.concatenate([ba[:3].reshape(-1, 3), ba[-3:].reshape(-1, 3),
                                    ba[:, :3].reshape(-1, 3), ba[:, -3:].reshape(-1, 3)]), axis=0)
    arr = ba * (np.array(paper, float) / np.maximum(bg2, 1))
    big = Image.fromarray(np.rint(arr).clip(0, 255).astype("uint8"))
    pw = W - panel_x
    panel = Image.new("RGB", (pw, H), tuple(paper))
    top_y = int(top) if top is not None else int((H - bottle_h) / 2)
    cx_big = int((bx0 + bx1) / 2 * s)
    panel.paste(big, (pw // 2 - cx_big, top_y - int(by0 * s)))
    img.paste(panel, (panel_x, 0))
    return dict(scale=s, src_size=src.size, bottle_px=(int((bx1 - bx0) * s), int((by1 - by0) * s)),
                top=top_y, bottom=top_y + int(bottle_h), bg=tuple(int(v) for v in bg))


def wad_page2(slot, slide_no, total, pal):
    """slots: bottle (path), panel_frac(0.30), bottle_top(100), bottle_bottom
    (CONTENT_BOTTOM - 120: the base sits above the footer with room to breathe),
    producer, region_year, wine_lines[...], rule(True), lead, body,
    body_anchor('flow' | 'bottom': 'bottom' puts the body's last line on the
    bottle's base), and the lockup that repeats the page 1 logo, identical in
    size by default: lockup_lines(["I\u2019m", "Drinking"]), lockup_h(320),
    lockup_size(160), lockup_y(the bottle's top), lockup_gap(40).

    GRID: the lockup's top and the bottle's top are one line, and (with
    body_anchor='bottom') the body's last line and the bottle's base are another,
    so the text column and the bottle share a top and a bottom axis."""
    img, d, qa = modules._start("WAD-02 page2", slide_no, total, pal)
    qa.word_limit = WORD_LIMIT
    panel_x = int(W * (1 - slot.get("panel_frac", 0.30)))
    btop = slot.get("bottle_top", 100)
    # The bottle's base (and, when anchored, the body's last line) sits 120px ABOVE the
    # content limit, not on it: anchored on the limit itself the body ended 57px above
    # the page number (page 1 has 230px) and the two crowded each other.
    info = _bottle_panel(img, slot["bottle"], panel_x,
                         slot.get("bottle_h", slot.get("bottle_bottom", CONTENT_BOTTOM - 120) - btop),
                         top=btop, paper=PAPER)
    d = ImageDraw.Draw(img)
    qa.notes.append(f"info bottle enlarged x{info['scale']:.2f} from {info['src_size']}; top {info['top']}, base {info['bottom']}")

    # The lockup repeats here with the answer's lead-in: the same disc, "?" and
    # glass, set beside "I'm / Drinking" instead of "What am I / Drinking?".
    lock_h = slot.get("lockup_h", 320)          # = page 1's lockup: a repeated mark is identical
    lock_lines = slot.get("lockup_lines", ["I\u2019m", "Drinking"])
    lock_size = slot.get("lockup_size", 160)
    # The lockup's TOP-MOST INK (the title's capitals overshoot the disc by ~9px) sits on
    # the bottle's top line: measure the ink on a scratch canvas, then offset.
    sc = Image.new("RGB", (W, H), (255, 255, 255))
    wad_lockup(sc, M, 400, lock_h, lock_lines, lock_size, pal["SIGNATURE"], pal,
               gap=slot.get("lockup_gap", 40), badge_alpha=1.0)
    ink_top = int(np.where((np.abs(np.asarray(sc).astype(int) - 255).sum(2) > 60).any(1))[0].min())
    lock_y = slot.get("lockup_y", info["top"] - (ink_top - 400))
    lx, lty, lr, lb, _, _ = wad_lockup(img, M, lock_y, lock_h, lock_lines, lock_size,
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
    ink_bottom, y_body = None, -1
    if slot.get("body_anchor", "flow") == "bottom":
        # measure the body's real ink height on a scratch canvas, then place it so its
        # last line sits on the bottle's base (the content limit by default)
        scratch = Image.new("RGB", (W, H), (255, 255, 255))
        run_in(ImageDraw.Draw(scratch), (tx, 0), slot["lead"], slot["body"], tw_max, pal)
        ink = np.where((np.abs(np.asarray(scratch).astype(int) - 255).sum(2) > 60).any(1))[0]
        ink_bottom = int(ink.max())
        y_body = info["bottom"] - ink_bottom
        if y_body < y + 80:
            qa.notes.append(f"FAIL body-anchor: body would start at {y_body}, too close to the title stack ending {y}")
        else:
            qa.notes.append(f"info body anchored: top {y_body}, last-line ink bottom {y_body + ink_bottom} = bottle base {info['bottom']}")
            y = y_body
    end = run_in(d, (tx, y), slot["lead"], slot["body"], tw_max, pal)
    # run_in's end includes the line gap BELOW the last line (~41px). When the body is
    # anchored by its ink to the bottle's base, bound the box by the ink, which is what
    # the eye aligns and what the content-limit check is protecting.
    qa.box("body", (tx, y, tx + tw_max, (y + ink_bottom) if (ink_bottom is not None and y_body >= 0) else end))
    qa.size("body", core.TYPE["body"])
    qa.add_words(slot["body"])
    return modules._finish(img, d, qa, slide_no, total, page_pos="left",
                           footer_label=slot.get("footer_label", ""),
                           credit=slot.get("photo_credit"), footer_size=76)
