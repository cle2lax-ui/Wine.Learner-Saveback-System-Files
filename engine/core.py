"""
FIELD GUIDE STYLE SYSTEM v5 — CORE
Canvas, fonts, text & photo helpers, page furniture, product-photo
pipeline, and the QA harness that every module runs automatically.
Rules live in code, not on paper. See LESSONS_LEARNED_v5.md for why
each of these exists.
"""
import os
import zipfile
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageStat
import numpy as np
import cv2
from tokens import *

_font_cache = {}


def font(role, size):
    key = (role, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(f"{FONT_DIR}/{FONT_FILES[role]}", size)
    return _font_cache[key]

# ---------------- Canvas & furniture ----------------
def new_canvas(bg=None):
    return Image.new("RGB", (W, H), bg or PAPER)

def footer(d, slide_no, total, label="READ MORE  \u2190", page_pos="right", credit=None, fill=None, img=None,
           show_page_num=True, footer_size=None, credit_size=34):
    """Every slide's bottom furniture: the read-more cue, the page
    number, and (optionally) a small-print photo credit centered in
    the gutter between them.

    Label text changed from "SWIPE" to "READ MORE" system-wide (this
    default is what every module inherits unless it draws its own
    footer text independently -- see guess_the_region.py's swipe_txt
    and fff_facts.py's swipe_label param, both updated alongside this).

    The arrow still points LEFT (\u2190) deliberately -- it's the swipe
    *gesture* direction (a thumb moves left to advance a carousel), not
    an arrow toward where the next slide's content visually sits. That
    physical gesture didn't change when the label wording did, so the
    arrow direction doesn't either. This was wired backwards for a
    while; if you're ever tempted to "fix" it to \u2192, don't -- that's
    the bug, not a valid alternate style.

    page_pos="right" (default) puts the read-more label at the left
    margin and the page number at the right; "left" swaps them, keeping
    the page number near the label instead of opposite it (used by the
    Quick Sips series). credit, when given, is NOT drawn on the photo
    -- see photo_band()'s docstring for why that changed.

    fill overrides the default MUTED color -- pass a light color for
    slides with a solid dark block behind the footer (e.g. the Rand-
    style cover/closing flat color panel), where MUTED (built for a
    paper background) goes invisible. Found as a real, shipped bug on
    a flat-color cover before this param existed; don't remove it.

    img (optional) makes the footer luminance-adaptive: pass the actual
    rendered Image and each text run's real background is sampled
    (region_luminance()) and colored white-on-scrim or plain ink
    accordingly -- same pattern already proven on gtr_reveal's photo
    caption. Only engages when fill is NOT also passed (an explicit
    fill always wins, same precedence as before); every existing call
    site that doesn't pass img is completely unchanged. Added after a
    GTR page-1 footer sitting on a medium-brightness, busy photo blade
    read as low-contrast with the fixed MUTED default -- a fixed color
    was never going to be right for every photo, same lesson as the
    page-2 caption before it.

    footer_size overrides the page-number/read-more-cue font size
    (default TYPE["caption"]=60) -- Quick Sips calls with 76 for a
    slightly heavier footer row than Field Guide's default."""
    f = font("kicker", footer_size or TYPE["caption"])
    txt = f"{slide_no:02d}/{total:02d}"
    tw = d.textbbox((0, 0), txt, font=f)[2]
    adaptive = (img is not None) and (fill is None)
    col = fill or MUTED

    def _draw(pos, s, fnt):
        nonlocal d
        if not adaptive:
            d.text(pos, s, font=fnt, fill=col)
            return
        x, y = pos
        bbox = d.textbbox((x, y), s, font=fnt)
        pad = 10
        region = (bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad)
        lum = region_luminance(img, region)
        if lum > 150:
            d.text((x, y), s, font=fnt, fill=INK)
        else:
            chip(img, region, (10, 10, 10), opacity=0.55)
            d = ImageDraw.Draw(img)
            d.text((x, y), s, font=fnt, fill=(255, 255, 255))

    if page_pos == "left":
        _draw((M, FOOTER_Y - 4), txt, f) if show_page_num else None
        _draw((M + tw + 24, FOOTER_Y - 4) if show_page_num else (M, FOOTER_Y - 4), label, f)
    else:
        _draw((M, FOOTER_Y - 4), label, f)
        if show_page_num:
            _draw((W - M - tw, FOOTER_Y - 4), txt, f)
    if credit:
        # small print, centered in the gutter between the read-more cue
        # and the page number -- the footer row is the standard home for
        # any third-party photo credit, not an overlay on the photo itself
        # credit_size defaults to 34 (unchanged for every existing caller);
        # FFFA passes 28 -- at 2160px wide the credit line now carries a
        # photographer, "Wikimedia Commons" and a licence string, which at
        # 34 competed with the read-more cue instead of sitting under it.
        # The gutter is what is left between the read-more cue and the
        # page number, not the full canvas. A two-photo slide credits two
        # photographers plus two licences on one line, and at a fixed 34
        # that ran straight through both -- "Daniel CULSAN / Wikimedia
        # Commons (CC BY-SA 3.0) - Vive la Rosiere / ..." overprinted
        # READ MORE on the left and 09/12 on the right simultaneously.
        # Step the size down until it fits, then ellipsize only if even
        # the floor is too small. Credits are a licence obligation, so
        # the failure mode has to be "smaller", never "clipped in half
        # by the page number".
        label_w = d.textbbox((0, 0), label, font=f)[2]
        left_edge = M + label_w + 30
        right_edge = (W - M - tw - 30) if show_page_num else (W - M)
        avail = max(200, right_edge - left_edge)

        size = credit_size
        cf = font("body", size)
        while d.textbbox((0, 0), credit, font=cf)[2] > avail and size > 22:
            size -= 2
            cf = font("body", size)

        text = credit
        if d.textbbox((0, 0), text, font=cf)[2] > avail:
            while text and d.textbbox((0, 0), text + "\u2026", font=cf)[2] > avail:
                text = text[:-1]
            text += "\u2026"

        cw = d.textbbox((0, 0), text, font=cf)[2]
        cx = left_edge + (avail - cw) // 2
        cy = FOOTER_Y - 4 + (f.getmetrics()[0] - cf.getmetrics()[0]) // 2
        _draw((cx, cy), text, cf)

def kicker_block(d, text, pal, x=M, y=170, text_fill=None):
    """Rand filter (system default as of the v7 save-back): a filled
    dot -- the one recurring mark, reused as the leader-line target on
    atlas(), the event marker on timeline(), and the glossary/list
    bullet wherever a module has one -- followed by bold tracked caps
    in INK, not colored type. The dot carries pal['SIGNATURE'] (the
    primary mark color -- matches the cover/closing block and the
    headline underline's sibling use of SIGNATURE for major marks;
    ACCENT is reserved for secondary marks like map pins and subtitle
    text). Replaces the old gold-caps-plus-rule kicker system-wide.
    text_fill overrides the INK default -- for a dark-background slide
    where INK (built for paper) would be invisible."""
    r = 16
    cy = y + 34
    d.ellipse([x, cy - r, x + 2 * r, cy + r], fill=pal["SIGNATURE"])
    kf = font("kicker_bold", 62)
    tracked_text(d, (x + 2 * r + 22, y), text, kf, text_fill or INK, tracking=7)
    return y + 96

def headline(d, text, y, size_key="display_md", fill=INK, x=M, show_underline=True):
    avail_w = W - x - M
    size = TYPE[size_key]
    floor = TYPE["standfirst"] + HIERARCHY_GAP  # never shrink below the locked hierarchy margin
    f = font("display_black", size)
    while d.textbbox((0, 0), text, font=f)[2] > avail_w and size > floor:
        size -= 2
        f = font("display_black", size)
    d.text((x, y), text, font=f, fill=fill)
    asc, desc = f.getmetrics()
    new_y = y + int((asc + desc) * 1.02)
    # Rand filter: a short accent-color underline anchors the headline
    # to the system as a graphic element, not just colored type floating
    # on the page. Uses DEFAULT_PALETTE's ACCENT directly (not a `pal`
    # param headline() doesn't take) so it's stable regardless of which
    # fill color a given call passes for the headline text itself.
    # show_underline default True is backward compat for older decks;
    # DESIGN_PROCESS_v8.md locks new decks to show_underline=False since
    # color-coded hierarchy (pal["LEAD"] vs pal["SIGNATURE"]) now carries
    # the differentiation the underline used to provide.
    if show_underline:
        d.line([(x, new_y - 14), (x + 90, new_y - 14)], fill=DEFAULT_PALETTE["ACCENT"], width=6)
    return new_y

# ---------------- Text helpers ----------------
def text_w(d, t, f):
    return d.textbbox((0, 0), t, font=f)[2]

def tracked_text(d, xy, txt, f, fill, tracking=4):
    x, y = xy
    for ch in txt:
        d.text((x, y), ch, font=f, fill=fill)
        x += text_w(d, ch, f) + tracking
    return x

def tracked_w(d, txt, f, tracking=4):
    """Width of txt as tracked_text would actually render it (each glyph's
    width plus letter-spacing) -- plain text_w() undercounts tracked text,
    since it doesn't add the per-character tracking gap. Used for
    right-aligning or centering tracked labels against the same math the
    draw call uses, so alignment doesn't drift from the rendered width."""
    return sum(text_w(d, ch, f) + tracking for ch in txt)

def wrap_tracked(d, txt, f, max_w, tracking=4):
    """Like wrap(), but measures candidate lines with tracked_w() instead
    of text_w() -- required for any text that will be drawn with
    tracked_text, since tracking makes it wider than plain text at the
    same font size and plain wrap() would overflow the line."""
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tracked_w(d, t, f, tracking) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    if len(lines) > 1 and tracked_w(d, lines[-1], f, tracking) < max_w * 0.30:
        tail = lines[-2].split()
        if len(tail) > 1:
            lines[-2] = " ".join(tail[:-1])
            lines[-1] = tail[-1] + " " + lines[-1]
    return [l for l in lines if l]

def _split_long_word(d, word, f, max_w):
    """A single space-delimited word that's itself wider than max_w gets
    broken at internal hyphens (hyphen stays with the preceding piece,
    standard convention) instead of silently overflowing the line."""
    if text_w(d, word, f) <= max_w or "-" not in word:
        return [word]
    parts = word.split("-")
    pieces, cur = [], ""
    for i, p in enumerate(parts):
        candidate = p if i == len(parts) - 1 else p + "-"
        trial = cur + candidate
        if not cur or text_w(d, trial, f) <= max_w:
            cur = trial
        else:
            pieces.append(cur)
            cur = candidate
    if cur:
        pieces.append(cur)
    return pieces

def wrap(d, txt, f, max_w):
    words, lines, cur = txt.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(d, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            pieces = _split_long_word(d, w, f, max_w)
            for piece in pieces[:-1]:
                lines.append(piece)
            cur = pieces[-1]
    lines.append(cur)
    if len(lines) > 1 and text_w(d, lines[-1], f) < max_w * 0.30:
        tail = lines[-2].split()
        if len(tail) > 1:
            lines[-2] = " ".join(tail[:-1])
            lines[-1] = tail[-1] + " " + lines[-1]
    return lines


def wrap_around(d, x0, y0, max_w, text, f, fill, obstacle=None, leading=1.32,
                 lead_font=None, lead_fill=None, lead_words=0,
                 gap_before_obstacle=40):
    """Word-wrap `text` in the box (x0, y0) to (x0+max_w, ...), narrowing
    any line that vertically overlaps `obstacle` (x0,y0,x1,y1) so prose
    flows around it instead of under it -- e.g. body copy carving around
    a benchmark-bottle photo. Optionally renders the first `lead_words`
    words in a distinct lead_font/lead_fill (a bold serif lead-in,
    matching the run_in pattern), the rest in f/fill. Returns the y
    coordinate just below the last line.

    Lines mixing f and a larger lead_font are baseline-aligned: each
    line's true max ascent/descent (across whichever fonts actually
    appear on it) sets that line's baseline and its advance to the next
    line, and every word on the line is drawn relative to that shared
    baseline rather than a single top-left y -- so a bigger bold lead-in
    sitting next to smaller body text lands bottom-aligned with it
    instead of floating high with mismatched baselines.

    RECONSTRUCTION NOTE: this function was referenced by quick_sips.py
    but absent from every copy of core.py available this session,
    including the untouched original restored to project -- the gap
    predates this session's edits. Rebuilt from the call-site usage and
    docstrings in quick_sips.py (signature, obstacle-avoidance behavior,
    lead-word styling), not recovered from the original implementation.
    Two behaviors specifically called out in prior project notes as
    "fixed real production bugs" are addressed below (the sparse-line
    guard and ink-based line positioning) but the exact prior tuning
    could not be recovered -- verify against real content before
    trusting this at the same level as the rest of core.py.
    """
    words = text.split()
    asc, desc = f.getmetrics()
    default_line_h = int((asc + desc) * leading)
    min_usable_w = max_w * 0.35  # sparse-line guard: a line narrowed by the
                                  # obstacle to less than this is treated as
                                  # unusable -- push past the obstacle rather
                                  # than wrapping single words into a sliver

    def line_width_at(y_top, y_bot):
        if not obstacle:
            return max_w
        ox0, oy0, ox1, oy1 = obstacle
        if y_bot < oy0 or y_top > oy1:
            return max_w
        # obstacle sits to the right of the text column in every call
        # site this function is used from; narrow to its left edge
        avail = (ox0 - gap_before_obstacle) - x0
        return avail if avail >= min_usable_w else max_w if y_bot > oy1 else 0

    def word_font(idx):
        return lead_font if (lead_font and idx < lead_words) else f

    def measure(txt_words, start_idx):
        # each word measured in the font it will actually be drawn with
        # (lead words are wider in lead_font) -- the wrap pass must use
        # the same widths the draw pass will, or lines built against the
        # narrower regular-font estimate overflow once the bigger lead
        # font is actually rendered
        total = 0
        for k, w in enumerate(txt_words):
            wf = word_font(start_idx + k)
            total += text_w(d, w, wf)
            if k > 0:
                total += text_w(d, " ", wf)
        return total

    def line_metrics(start_idx, n_words):
        # max ascent/descent among the fonts actually used on this line
        # (usually just f, except a line whose start overlaps the
        # lead-in also carries lead_font's taller metrics)
        fonts_used = {word_font(start_idx + k) for k in range(n_words)}
        a = max(ff.getmetrics()[0] for ff in fonts_used)
        de = max(ff.getmetrics()[1] for ff in fonts_used)
        return a, de

    lines = []  # (text, start_idx)
    cur_words = []
    word_i = 0
    line_start_idx = 0
    y = y0
    while word_i < len(words):
        w = words[word_i]
        candidate_words = cur_words + [w]
        row_w = line_width_at(y, y + default_line_h)
        if row_w == 0:
            # obstacle fully blocks this row and the sparse-line guard
            # rejected the sliver -- drop straight to below the obstacle
            y = obstacle[3] + 10
            continue
        cw = measure(candidate_words, line_start_idx)
        if cw <= row_w or not cur_words:
            cur_words = candidate_words
            word_i += 1
        else:
            lines.append((" ".join(cur_words), line_start_idx))
            line_start_idx = word_i
            cur_words = []
            # advance by the body font's own rhythm, not this line's
            # possibly-taller metrics -- a line containing the bold
            # lead-in must not blow out the gap to the *next* line;
            # only its own baseline position (below) needs the taller
            # metrics, not the spacing that follows it
            y += default_line_h
    if cur_words:
        lines.append((" ".join(cur_words), line_start_idx))

    y = y0
    prev_baseline = None
    prev_ink_desc = None
    leading_pad = default_line_h - (asc + desc)  # the portion of default_line_h
                                                   # that's pure breathing room,
                                                   # beyond the body font's own
                                                   # natural ascent+descent
    for line_txt, start_idx in lines:
        x = x0
        words_on_line = line_txt.split()
        line_asc, line_desc = line_metrics(start_idx, len(words_on_line))
        if prev_baseline is None:
            baseline_y = y0 + line_asc
        else:
            # gap = previous line's REAL ink descent (not the font's
            # idealized descent metric) + this line's ascent + the same
            # breathing room every other line gets. Font metrics report
            # the full design descent regardless of which glyphs are
            # actually present -- "The Cascades" has no descenders at
            # all, so sizing the gap off the lead font's nominal
            # descent (meant for glyphs like g/y/p) overstated the
            # clearance this specific line needed.
            baseline_y = prev_baseline + prev_ink_desc + leading_pad + line_asc
        for k, w in enumerate(words_on_line):
            idx = start_idx + k
            use_lead = lead_font and idx < lead_words
            wf = lead_font if use_lead else f
            wfill = lead_fill if use_lead else fill
            w_asc, _ = wf.getmetrics()
            d.text((x, baseline_y - w_asc), w, font=wf, fill=wfill)
            x += text_w(d, w + " ", wf)
        # real ink descent for this line: the deepest any glyph actually
        # drawn on it reaches below the baseline, not the font's generic
        # descent metric (which assumes descenders like g/y/p that may
        # not be present in this specific line's text)
        ink_bottom = baseline_y
        for k, w in enumerate(words_on_line):
            idx = start_idx + k
            wf = lead_font if (lead_font and idx < lead_words) else f
            tb = d.textbbox((0, 0), w, font=wf)
            w_asc = wf.getmetrics()[0]
            ink_bottom = max(ink_bottom, baseline_y - w_asc + tb[3])
        line_ink_desc = max(ink_bottom - baseline_y, 0)
        prev_baseline, prev_ink_desc = baseline_y, line_ink_desc
    return int(prev_baseline + prev_ink_desc + leading_pad) if prev_baseline is not None else y0

def paragraph(d, xy, txt, f, fill, max_w, leading=1.32):
    x, y = xy
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * leading)
    for ln in wrap(d, txt, f, max_w):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y

def standfirst(d, xy, txt, max_w, hero=False, fill=MUTED, leading=1.18):
    size = TYPE["standfirst_hero"] if hero else TYPE["standfirst"]
    return paragraph(d, xy, txt, font("standfirst_italic", size), fill, max_w, leading)

def run_in(d, xy, lead_txt, body_txt, max_w, pal, lead_size=None, body_size=None, leading=1.34,
           justify=False, bold_words=None, bold_color=None, bold_serif=False, bold_size=None,
           body_font_role="body", max_gap_mult=1.9):
    """Serif inline section lead (v4 canonical): Playfair Bold lead + Archivo body,
    baseline-aligned, body wraps full-measure. justify=True distributes extra
    space between words so every line but the last hits max_w exactly (full
    justification) instead of ragged-right wrapping.

    bold_words: optional set/iterable of words to emphasise inside the body.
    Matching ignores surrounding punctuation and case, so "Syrah." and
    "syrah" both match "Syrah" -- otherwise every comma in the paragraph
    becomes a silent miss and the emphasis looks arbitrary rather than
    absent. Emphasised words render in body_bold, or display_bold when
    bold_serif=True, optionally in bold_color and/or at bold_size.

    body_font_role: font role for the non-emphasised body (default
    Archivo-Medium; pass "body_regular" for true 400 weight).

    max_gap_mult: justification safety valve. A line holding two long
    words can only reach max_w by opening rivers of white space between
    them; past max_gap_mult x the natural space width this stops reading
    as justified text and starts reading as a layout bug, so that line
    falls back to ragged setting. Only affects justify=True.

    These five keywords were being passed by map_atlas.lead_paragraph
    against a core.py that never grew them -- the call raised TypeError
    on every atlas slide with a description. Added here rather than
    stripped at the call site, since the map description is the one place
    a term like Syrah wants emphasis without a second paragraph.
    """
    lead_size = lead_size or TYPE["lead"]
    body_size = body_size or TYPE["body"]
    x, y = xy
    lf, bf = font("display_bold", lead_size), font(body_font_role, body_size)

    bold_set = {w.strip(".,;:!?()[]\u2014\u2013'\u2019\"").lower()
                for w in (bold_words or [])}
    bfont = font("display_bold" if bold_serif else "body_bold", bold_size or body_size)

    def wfont(w):
        return bfont if w.strip(".,;:!?()[]\u2014\u2013'\u2019\"").lower() in bold_set else bf

    def wfill(w):
        return (bold_color or INK) if wfont(w) is bfont else INK
    la, ld = lf.getmetrics(); ba, bd = bf.getmetrics()
    off = la - ba
    d.text((x, y), lead_txt, font=lf, fill=pal["LEAD"])
    ix = x + text_w(d, lead_txt, lf)
    inter = " "
    d.text((ix, y + off), inter, font=bf, fill=INK)
    bx = ix + text_w(d, inter, bf)
    first_w = max_w - (bx - x)
    # Line breaking measures each word in the font it will actually be
    # drawn in. Wrapping the whole candidate string in bf and then drawing
    # some of its words in a wider bold face is how a justified paragraph
    # ends up overshooting its measure by a word.
    space_w = text_w(d, " ", bf)

    def run_w(ws):
        if not ws:
            return 0
        return sum(text_w(d, w, wfont(w)) for w in ws) + space_w * (len(ws) - 1)

    words, lines, cur = body_txt.split(), [], []
    for w in words:
        lim = first_w if not lines else max_w
        if not cur or run_w(cur + [w]) <= lim:
            cur.append(w)
        else:
            lines.append(cur); cur = [w]
    lines.append(cur)
    lh = int((ba + bd) * leading)

    def draw_run(line_words, start_x, ly, gap):
        cx = start_x
        for i, w in enumerate(line_words):
            d.text((cx, ly), w, font=wfont(w), fill=wfill(w))
            cx += text_w(d, w, wfont(w)) + (gap if i < len(line_words) - 1 else 0)

    def draw_line(line_words, start_x, ly, target_w, do_justify):
        if do_justify and len(line_words) > 1:
            gap = (target_w - sum(text_w(d, w, wfont(w)) for w in line_words)) \
                / (len(line_words) - 1)
            # Rivers-of-whitespace guard: past max_gap_mult x a natural
            # space the line reads as broken, not as justified.
            if gap <= space_w * max_gap_mult:
                draw_run(line_words, start_x, ly, gap)
                return
        draw_run(line_words, start_x, ly, space_w)

    is_last = lambda i: i == len(lines) - 1
    draw_line(lines[0], bx, y + off, first_w, justify and not is_last(0))
    yy = y + off + lh
    for i, ln in enumerate(lines[1:], start=1):
        draw_line(ln, x, yy, max_w, justify and not is_last(i))
        yy += lh
    return max(yy, y + la + ld + 10)

def famous_names(d, xy, names, max_w, pal, size=None, label="FAMOUS NAMES"):
    """A labeled, tracked-caption strip of names separated by ' · ',
    e.g. notable producers. Wraps to as many lines as needed at a
    fixed, legible size -- does NOT shrink type to force a fit onto
    one line (a prior version shrank down to FLOOR and then simply
    let overflow run past the column edge once names still didn't
    fit at the floor size; wrapping is the actual fix, not a smaller
    floor). Returns the y coordinate just below the block."""
    x, y = xy
    size = size or TYPE["caption"]
    tracked_text(d, (x, y), label, font("kicker_bold", TYPE["caption"]), pal["ACCENT"], 5)
    d.line([(x, y + 76), (x + max_w, y + 76)], fill=pal["ACCENT"], width=3)
    nf = font("body_bold", size)
    text = "  \u00b7  ".join(names)
    na, nd = nf.getmetrics()
    line_h = int((na + nd) * 1.2)
    yy = y + 104
    for ln in wrap(d, text, nf, max_w):
        d.text((x, yy), ln, font=nf, fill=INK)
        yy += line_h
    return yy

# ---------------- Photo helpers ----------------
def load_photo(name):
    for ext in ("", ".jpg", ".jpeg", ".png", ".webp"):
        p = f"{PHOTO_DIR}/{name}{ext}"
        if os.path.exists(p):
            im = Image.open(p)
            im = ImageOps.exif_transpose(im)  # honor camera rotation metadata
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                im = im.convert("RGBA")
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[-1])  # composite onto white using alpha
                return bg
            return im.convert("RGB")
    raise FileNotFoundError(name)

def load_photo_rgba(name):
    """Like load_photo() but preserves transparency instead of compositing
    onto white -- for product cutouts (e.g. showcase_shelf bottles) that
    get pasted onto a colored page background, where a flattened white
    box behind the product would look like a rendering bug."""
    for ext in ("", ".jpg", ".jpeg", ".png", ".webp"):
        p = f"{PHOTO_DIR}/{name}{ext}"
        if os.path.exists(p):
            im = Image.open(p)
            im = ImageOps.exif_transpose(im)
            return im.convert("RGBA")
    raise FileNotFoundError(name)

def cover_fit(im, tw, th, y_anchor=0.5, zoom=1.0):
    """y_anchor controls vertical crop position (0.0=top, 1.0=bottom,
    0.5=center/original default). zoom > 1.0 magnifies past the
    minimum cover-fit scale, for showing a tighter, closer-in slice of
    the source rather than just repositioning the same overall view.
    Both are additive, non-breaking: default args reproduce the
    original center-crop behavior exactly."""
    sw, sh = im.size
    s = max(tw / sw, th / sh) * zoom
    im = im.resize((int(sw * s) + 1, int(sh * s) + 1), Image.LANCZOS)
    x0 = (im.width - tw) // 2
    y0 = int((im.height - th) * y_anchor)
    y0 = max(0, min(y0, im.height - th))
    return im.crop((x0, y0, x0 + tw, y0 + th))

def scrim(img, region, dark_at="bottom", strength=0.75, color=None):
    """Gradient overlay for blending a photo into a caption zone. Do NOT use
    this for a kicker/label chip that needs guaranteed uniform contrast --
    the gradient is, by design, at ZERO strength at one edge of the region.
    A kicker drawn near that edge gets no protection at all (this is exactly
    how the mosaic kicker went unreadable: gradient scrim, text near the
    fading edge). For that job, use chip() instead."""
    x0, y0, x1, y1 = region
    rw, rh = x1 - x0, y1 - y0
    ov = Image.new("L", (1, rh), 0)
    for yy in range(rh):
        t = yy / max(rh - 1, 1)
        a = t if dark_at == "bottom" else 1 - t
        ov.putpixel((0, yy), int(255 * strength * a ** 1.4))
    ov = ov.resize((rw, rh))
    solid = Image.new("RGB", (rw, rh), color or SCRIM)
    reg = img.crop(region)
    reg.paste(solid, (0, 0), ov)
    img.paste(reg, (x0, y0))

def chip(img, region, color, opacity=1.0):
    """Flat, uniform-opacity rectangle -- the right tool any time text must
    read reliably regardless of what photo is underneath (kickers, corner
    marks, standalone labels over full-bleed images). Unlike scrim(), there
    is no gradient and therefore no weak edge. Use scrim() only when you
    specifically want a fade (blending a photo into a text zone below it);
    use chip() for everything else that sits on a photo."""
    x0, y0, x1, y1 = region
    if opacity >= 1.0:
        d = ImageDraw.Draw(img)
        d.rectangle([x0, y0, x1, y1], fill=color)
        return
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle([x0, y0, x1, y1], fill=(*color, int(255 * opacity)))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))

# Photo captions, system-wide. Cormorant Italic at TYPE["caption"] was
# the old setting and did not survive contact with a dark photograph --
# a fine-stroked display serif reversed out small is the least legible
# combination in the kit. Archivo Bold, four points up, holds together
# over any image and still reads as a caption rather than as body copy.
# These are deliberately module-agnostic constants: photo captions were
# being set independently in six places and had drifted apart.
CAPTION_FACE = "body_bold"
CAPTION_SIZE = TYPE["caption"] + 6


def photo_band(img, name, top, h, caption_txt=None, cap_align="left"):
    """caption_txt anchors inside the image, bottom-left by default (pass
    cap_align="right" for the rare case a caption needs the other
    corner). Photo credits (photographer/license attribution) are NOT
    handled here -- they belong in the slide's footer gutter (see
    footer()'s credit param / _finish()'s credit passthrough), not
    overlaid on the photo itself.

    Caption legibility is a flat chip() bar, not a gradient scrim (Rand
    filter, system-wide as of v7) -- sized to the text, not a full-width
    banner, so it reads as a label, not photographic mood.

    Caption face is CAPTION_FACE / CAPTION_SIZE (see below), not
    Cormorant Italic. Cormorant is a display serif with fine strokes; at
    caption size, reversed white out of a photograph, the thin strokes
    part-dissolve into whatever is behind them and the caption stops
    being readable at thumbnail scale."""
    im = cover_fit(load_photo(name), W, h)
    img.paste(im, (0, top))
    if caption_txt:
        d = ImageDraw.Draw(img)
        f = font(CAPTION_FACE, CAPTION_SIZE)
        tw = text_w(d, caption_txt, f)
        pad = 20
        bar_w = tw + 2 * pad
        cap_y = top + h - 118
        x = W - M - bar_w if cap_align == "right" else M
        chip(img, (x, cap_y - 14, x + bar_w, cap_y + CAPTION_SIZE + 22), INK)
        d = ImageDraw.Draw(img)
        d.text((x + pad, cap_y), caption_txt, font=f, fill=PAPER)
    return top + h

def region_luminance(img, box):
    """Mean grayscale luminance of a region of the actual rendered image
    (0=black, 255=white). Used to decide footer/caption text color
    against whatever the underlying photo happens to be, rather than
    assuming a fixed color (e.g. MUTED) always has enough contrast --
    it doesn't against every photo (e.g. light napkin fabric, dry gold
    grass). Shared by any module drawing text directly on photo area;
    was previously duplicated per-module before being promoted here."""
    x0, y0, x1, y1 = [int(v) for v in box]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    if x1 <= x0 or y1 <= y0:
        return 128
    region = img.convert("L").crop((x0, y0, x1, y1))
    return ImageStat.Stat(region).mean[0]

def photo_credit(img, xy, text, size=35, align="left", fill=(235, 228, 214), qa=None):
    """Small-print photo credit (photographer name, license link, etc.)
    overlaid near a photo's edge. Deliberately runs below FLOOR --
    real copyright/license attribution text is conventionally tiny and
    unobtrusive, not body-reading text -- so it's tracked via the "!"
    QA-exemption prefix rather than forced up to the normal type floor.
    xy is the anchor point; align="left"/"right" controls which side
    of that point the text extends from. qa is optional -- pass it
    when called from inside a module (before _finish), omit when
    applied as a post-hoc overlay after a module's image is returned."""
    d = ImageDraw.Draw(img)
    f = font("body", size)
    tw = text_w(d, text, f)
    x, y = xy
    if align == "right":
        x -= tw
    d.text((x, y), text, font=f, fill=fill)
    if qa is not None:
        qa.size("!photo_credit", size)

def photo_stripe(img, names, top, h, seam=(247, 244, 236)):
    """N photos running into each other, full-bleed, hairline seams."""
    n = len(names)
    xacc = 0
    d = ImageDraw.Draw(img)
    for i, nm in enumerate(names):
        seg = (W - xacc) if i == n - 1 else W // n
        img.paste(cover_fit(load_photo(nm), seg, h), (xacc, top))
        if i:
            d.line([(xacc, top), (xacc, top + h)], fill=seam, width=2)
        xacc += seg
    return top + h

# ---------------- QA harness ----------------
def _lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def contrast(c1, c2):
    l1, l2 = sorted((_lum(c1), _lum(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

class QA:
    """Collected per-slide. Modules register sizes/boxes/words; report() raises on FAIL."""
    def __init__(self, name):
        self.name = name
        self.sizes = []          # (label, px, is_headline)
        self.boxes = {}          # label -> (x0,y0,x1,y1)
        self.words = 0
        self.notes = []
        self.word_limit = MAX_BODY_WORDS  # override via qa.word_limit = N for a
                                            # specific data-dense slide; default
                                            # unchanged for every other module

    def size(self, label, px, headline=False):
        self.sizes.append((label, px, headline))

    def box(self, label, b):
        self.boxes[label] = b

    def add_words(self, txt):
        self.words += len(txt.split())

    def check_contrast(self, fg, bg, large=False, label=""):
        need = CONTRAST_LARGE if large else CONTRAST_BODY
        c = contrast(fg, bg)
        if c < need:
            self.notes.append(f"FAIL contrast {label}: {c:.2f} < {need}")

    def check_photo_contrast(self, img, box, text_lum, label, min_delta=90):
        """Samples ACTUAL rendered luminance under a text box drawn on a
        photo, not a theoretical fg/bg pair. Use this any time text sits on
        a photo rather than a flat color -- a scrim can look adequate in
        code and still fail in practice (see: duel's white label text on a
        near-white product photo, measured at 175 luminance before this
        check existed). text_lum: the luminance of the text color itself
        (0=black, 255=white). Call explicitly after drawing, since it needs
        the rendered pixels; report() cannot infer photo brightness itself.
        """
        x0, y0, x1, y1 = [int(v) for v in box]
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(W, x1), min(H, y1)
        if x1 <= x0 or y1 <= y0:
            return
        region = np.array(img.convert("L").crop((x0, y0, x1, y1)))
        bg_lum = region.mean()
        delta = abs(text_lum - bg_lum)
        if delta < min_delta:
            self.notes.append(
                f"FAIL photo-contrast {label}: text_lum={text_lum} bg_lum={bg_lum:.0f} "
                f"delta={delta:.0f} < {min_delta} (text will be hard to read)")

    def report(self, img=None):
        fails = []
        for lb, px, _ in self.sizes:
            if px < FLOOR and not lb.startswith("!"):
                fails.append(f"type floor: {lb}={px} < {FLOOR}")
        heads = [px for lb, px, h in self.sizes if h and not lb.startswith("!")]
        others = [px for lb, px, h in self.sizes if not h and not lb.startswith("!")]
        if heads and others and max(heads) < max(others) + HIERARCHY_GAP:
            fails.append(f"hierarchy: headline {max(heads)} !> {max(others)}+{HIERARCHY_GAP}")
        keys = list(self.boxes)
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = self.boxes[keys[i]], self.boxes[keys[j]]
                if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
                    fails.append(f"collision: {keys[i]} x {keys[j]}")
        for lb, b in self.boxes.items():
            # '!' prefix = spec-sanctioned exemption (full-bleed statement furniture)
            if b[3] > CONTENT_BOTTOM and "footer" not in lb and not lb.startswith("!"):
                fails.append(f"caption-zone: {lb} bottom {b[3]} > {CONTENT_BOTTOM}")
            # edge-bounds: nothing should sit off-canvas. This was a real,
            # undetected defect (labels ran off both edges of the facsimile
            # map while every other QA check reported clean) because no
            # check compared boxes against the page's own physical extent.
            if not lb.startswith("!"):
                if b[0] < -2 or b[2] > W + 2:
                    fails.append(f"off-canvas x: {lb} spans {b[0]:.0f}-{b[2]:.0f}, page is 0-{W}")
                if b[1] < -2 or b[3] > H + 2:
                    fails.append(f"off-canvas y: {lb} spans {b[1]:.0f}-{b[3]:.0f}, page is 0-{H}")
        if self.words > self.word_limit:
            fails.append(f"word budget: {self.words} > {self.word_limit}")
        fails += [n for n in self.notes if n.startswith("FAIL")]
        if img is not None:
            L = np.array(img.convert("L"))
            last = np.where((L[:CONTENT_BOTTOM, :] < 245).any(axis=1))[0]
            if len(last) and last.max() > CONTENT_BOTTOM - 10:
                pass  # informational only; boxes are authoritative
        if fails:
            raise AssertionError(f"[{self.name}] QA FAILED:\n  " + "\n  ".join(fails))
        return f"[{self.name}] QA pass  (words={self.words}, elements={len(self.boxes)})"


# ─────────────────── PRODUCT PHOTO PIPELINE (locked SOP) ───────────────────
# Six separate ad-hoc attempts at bottle-photo background removal happened
# in one build cycle before this was written down as one tested function.
# Do not write a new flood-fill script per deck -- use this, or extend it.

def _true_hole_check(opaque_mask):
    """Correct interior-hole detector. The naive version (flood-fill from
    pixel (0,0) of a TIGHTLY CROPPED image) has a seeding bug: after a tight
    crop, (0,0) often sits right at the subject's edge, not truly outside
    it, so the flood mis-fills and reports near-everything as a false hole.
    This cost a wasted diagnosis once already -- a real bug was invented
    and reported as fact based on this exact mistake. Pad first so the seed
    pixel is guaranteed exterior, THEN flood-fill, THEN check.
    Returns the true interior-hole fraction (0.0 = clean)."""
    padded = np.pad(opaque_mask.astype(np.uint8), 5, mode="constant", constant_values=0)
    h, w = padded.shape
    flood = (padded * 255).astype(np.uint8)
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, mask, (0, 0), 128)
    exterior = flood == 128
    interior_bg = (~exterior) & (padded == 0)
    return interior_bg.sum() / padded.size

def remove_background(path_or_image, white_threshold=715, out_path=None):
    """Locked product-photo pipeline: isolate the subject from a white or
    near-white studio background, trim to its true bounds, verify no holes
    were punched through the subject (a real failure mode when a label's
    own near-white background bridges to the true exterior background and
    both get erased together), and save as a tight RGBA PNG.

    white_threshold: sum of R+G+B above which a pixel is a background
    CANDIDATE (max 765). Only the single largest connected candidate
    region -- and only if it touches the image border -- is treated as
    real background. This prevents two failure modes seen this cycle:
    (a) tiny bright specks inside label artwork (highlights, white text)
    being erased individually, and (b) the whole label being erased
    because its cream background was close enough to white to qualify,
    which a naive per-pixel threshold cannot distinguish from the true
    background without the border-connectivity + largest-component step.

    Returns (PIL.Image RGBA, hole_fraction). If hole_fraction > 0.001,
    the result was NOT saved and the caller must not use it silently --
    surface this to the person, don't paper over it with a smaller crop.
    """
    im = path_or_image if isinstance(path_or_image, Image.Image) else Image.open(path_or_image)
    im = im.convert("RGB")
    arr = np.array(im)

    candidate = (arr.astype(int).sum(axis=2) > white_threshold).astype(np.uint8) * 255
    num, labels, stats, _ = cv2.connectedComponentsWithStats(candidate, connectivity=8)
    if num <= 1:
        raise ValueError("no background candidate found -- is this actually a white-background photo?")
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    h, w = candidate.shape
    touches_border = (
        np.any(labels[0, :] == largest) or np.any(labels[-1, :] == largest) or
        np.any(labels[:, 0] == largest) or np.any(labels[:, -1] == largest)
    )
    if not touches_border:
        raise ValueError("largest near-white region doesn't touch the image border -- "
                          "this photo may not have a plain background; do not auto-process")
    bg = labels == largest

    rgba = np.dstack([arr, np.where(bg, 0, 255).astype(np.uint8)])
    out = Image.fromarray(rgba, "RGBA")
    bbox = out.getbbox()
    if bbox is None:
        raise ValueError("nothing left after background removal")
    trimmed = out.crop(bbox)

    hole_frac = _true_hole_check(np.array(trimmed)[:, :, 3] > 10)
    if hole_frac <= 0.001 and out_path:
        trimmed.save(out_path)
    return trimmed, hole_frac


# ──────────────────── DELIVERY: PDF-first, ZIP-on-lock ────────────────────
# Standing delivery rule (per Steve, 2026-08): review rounds are presented
# as a single merged PDF, never loose PNGs -- a PNG-per-slide dump makes a
# deck in review feel like scattered assets instead of one document, and
# it's easy to lose track of slide order or accidentally review a stale
# PNG. A ZIP of individual PNGs is only handed over once the deck is
# LOCKED (the person has explicitly signed off and needs the source
# images for actual production use -- posting, further editing, etc.).
# Until then, PDF only. This split is intentionally two separate function
# calls rather than one build_deck(..., deliverable="pdf"/"zip") flag --
# the PDF call is safe to run repeatedly during iteration, while the ZIP
# call is a deliberate, one-directional "this is final" action, and
# collapsing them into one call with a mode switch makes it too easy to
# pass the wrong flag out of habit and ship a ZIP mid-review.
def assemble_pdf(png_paths, pdf_path):
    """Merge an ordered list of PNG paths into a single multi-page PDF.
    Use this for every in-review share -- present_files() should receive
    the PDF this returns, not the individual PNGs. Safe to call on every
    iteration; produces no ZIP and makes no claim the deck is final."""
    pages = [Image.open(p).convert("RGB") for p in png_paths]
    if not pages:
        raise ValueError("assemble_pdf: no PNG paths given")
    pages[0].save(pdf_path, save_all=True, append_images=pages[1:])
    return pdf_path


def lock_deck_zip(png_paths, zip_path):
    """Package the individual PNGs into a ZIP -- call this ONLY after the
    person has explicitly confirmed the deck is locked/final. Do not call
    this proactively alongside assemble_pdf() during a review round; the
    two are deliberately decoupled (see module-level note above)."""
    with zipfile.ZipFile(zip_path, "w") as z:
        for p in png_paths:
            z.write(p, os.path.basename(p))
    return zip_path

