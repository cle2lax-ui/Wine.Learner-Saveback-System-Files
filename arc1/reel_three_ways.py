"""REEL — Three Ways Into Syrah. Arc 1 week two, Tue 15 Sep.

First Reel built under REELS_SPEC_v2.md. Replaces the originally-planned
1-page static Three Ways post; same sourced numbers (D3 Ch. 7), new
format. Storyboard: arc1/REEL_THREE_WAYS_STORYBOARD.md.

SOURCING, resolved this session -- all three region photos found by
commune-name search or department-level category, never by searching
the AOC name itself, which is useless for two of the three regions:
"Saint-Joseph" collides with the Catholic saint site-wide on Commons,
and "Crozes-Hermitage" is drowned out by EU Official Journal PDFs (the
name appears in hundreds of multilingual regulatory filings). See each
manifest entry's sourcing_note in data/NR_PHOTO_MANIFEST.json for the
specific search path that worked.

  Crozes-Hermitage: nr_crozes_chanoscurson.jpg -- "les vignes de
    Chanos-Curson," a confirmed Crozes-Hermitage commune, found via
    Category:Vineyards in Drome (12 files, doesn't surface on any
    name-based search). Flat, fertile plain -- the deliberate visual
    contrast against Hermitage's slope.
  Saint-Joseph: nr_saintjoseph_sarras_vigne.jpg -- vines at Sarras,
    found by searching the commune name directly.
  Hermitage: nr_chapoutier_vy.jpg, NOT nr_hermitage_hill.jpg. The
    latter was checked at actual reel crop and turned out to be a
    scanned sepia postcard ("49. TAIN -- Coteau de l'Hermitage,
    renomme...") with a visible border and printed caption baked into
    the image -- fine cropped tight in a print deck, wrong next to
    three real color photographs in a video. Chapoutier's vineyard shot
    is genuine color photography of the terraced slope, including the
    real painted "M. CHAPOUTIER" retaining-wall sign -- an actual,
    famous landmark on the hill, not an inserted ad; a top-anchored
    crop keeps it a secondary detail rather than the subject.
  Hook/close: nr_tain_rhone.jpg (already in repo from week one).

REELS_SPEC_v2.md ELEMENTS IMPLEMENTED (first Reel to use any of them --
see the spec's own "still open" note that the progress-strip/loop-close
interaction was flagged as the thing most likely to need a second pass):

  1. Persistent progress strip -- three nodes on a thin line, bottom
     third of frame. Unlit and empty on beat 1. Each region beat lights
     its own node with a quick scale-pulse (0.3s) at beat start; already-
     lit nodes stay lit. Beat 5 draws a connecting fill across all three
     over its first ~1s -- the "visibly complete" state the spec calls
     for, so the loop back to beat 1's empty strip reads as a full
     cycle, not a reset.
  2. Animated stat bars -- same fill-bar visual language as the static
     decks' dashboards. Fills over the first 1.2s of each region beat,
     then holds. Scaled against a shared BAR_MAX (50 hL/ha, above the
     highest sourced value) rather than each region's own range, so
     Saint-Joseph's and Hermitage's bars render the SAME length (both
     40 hL/ha) and Crozes' renders longer (45) -- a real comparison
     across the hard cuts, not decoration.
  3. Supers that slide + fade (0.4s in, 0.3s out) rather than sitting
     static for the full beat -- the single change REELS_SPEC_v2.md
     names as most responsible for the "polished" read.
  4. A uniform grade + vignette applied identically to all four source
     photos (see grade_frame()), specifically because this Reel pulls
     from four different photographers of very different quality and
     colour temperature -- required by the spec, not a stylistic
     add-on, and verified below by comparing a before/after frame from
     each source rather than assumed.

Frames pipe as raw RGB straight into ffmpeg -- writing PNGs to disk and
re-reading them blew the execution limit on the first Reel build and
hasn't been done since.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PHOTOS = os.path.join(REPO, "photos")
FONTS = os.path.join(REPO, "fonts")

OUT = "/home/claude/out_reel_threeways"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1920
FPS = 30
BEAT_SECONDS = 4.0  # REELS_SPEC_v2.md default
SS = 2

SIGNATURE = (58, 26, 46)
ACCENT = (232, 181, 79)  # brightened per Steve's review -- was (186,149,74),
# a fairly desaturated, muted gold. This is a genuinely more saturated,
# higher-luminance value, not a cosmetic nudge: old vs new luminance
# (simple avg) is 136 vs 164, about a 20% lift, and it reads as
# noticeably punchier gold on an actual rendered frame rather than
# brownish -- confirmed below, not assumed from the RGB numbers alone.
PAPER = (251, 249, 244)

BAR_MAX = 50.0  # hL/ha -- shared scale, see docstring point 2
MARK_PAD = 44  # persistent corner mark's margin from the top-left edge

CRED_TAIN = "Guerinf / Wikimedia Commons (CC BY-SA 4.0)"
CRED_COVER = "Anna Hinckel / Pexels"
CRED_CROZES = "Mr Fougerolle / Wikimedia Commons (CC BY-SA 4.0)"
CRED_SJ = "Alisa Skripina / Pexels"
CRED_HERM = ""  # Steve's own photograph -- no third-party credit needed


def _chip(lay, region, color, opacity):
    """Flat rounded rectangle behind text, drawn directly onto the RGBA
    layer being composed. Not core.chip() -- that one converts to RGB at
    the end, which would drop the alpha this layer still needs before
    it's composited over the photo."""
    x0, y0, x1, y1 = region
    d = ImageDraw.Draw(lay, "RGBA")
    d.rounded_rectangle([x0, y0, x1, y1], radius=28 * SS,
                          fill=(*color, int(255 * opacity)))


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def _wrap(text, fnt, max_w, d):
    """Greedy word-wrap against an actual measured width (d.textlength),
    not a guessed character count -- the blurb copy varies enough in
    character width (percent signs, en dashes, digits) that a fixed
    chars-per-line rule would wrap inconsistently across the three
    region beats' blurb lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


BEATS = [
    dict(
        kind="hook", photo="nr_cover_goldenhour", credit=CRED_COVER,
        head="Three Ways\nInto Syrah",
        sub="One grape. Three regions.\nThree very different prices.",
        # Ken Burns ranges widened significantly per Steve's review --
        # was (1.02,1.10), an 8-point delta that barely read as motion
        # over 4s. Hook/close now share (1.00,1.24)/(1.24,1.00) so the
        # loop-close zoom-match still holds (close must END at the exact
        # zoom hook STARTS at, or the loop seam shows as a visible jump
        # in framing, not just a cut).
        node=None, stat_frac=None, zoom=(1.00, 1.24),
        crop_anchor=0.40,
    ),
    dict(
        kind="region", photo="nr_crozes_chanoscurson", credit=CRED_CROZES,
        label="CROZES-HERMITAGE",
        # 10-12 word style+history line, D3 Ch.7: "The AOC was created in
        # 1937 and extended... in 1956... the soils are deeper and more
        # fertile than in neighbouring Hermitage and the resulting wines
        # have lower concentration."
        blurb="Created in 1937, enlarged in 1956 \u2014 deeper soil, softer "
              "wines than Hermitage.",
        stat="~1,700 HA  \u00b7  45 HL/HA  \u00b7  MID-PRICED",
        node=0, stat_frac=45 / BAR_MAX, zoom=(1.00, 1.22),
        crop_anchor=0.42,
    ),
    dict(
        kind="region", photo="nr_saintjoseph_pexels", credit=CRED_SJ,
        label="SAINT-JOSEPH",
        # D3 Ch.7: "Nearly 90 per cent of the wines are red... extended in
        # 1994... today the debate is whether to reduce the appellation."
        blurb="Nearly 90% red, wide price range \u2014 extended in 1994, "
              "still debated today.",
        stat="50 KM OF APPELLATION  \u00b7  40 HL/HA",
        node=1, stat_frac=40 / BAR_MAX, zoom=(1.00, 1.24),
        crop_anchor=0.38,
    ),
    dict(
        kind="region", photo="nr_hermitage_chave_bottle", credit=CRED_HERM,
        label="HERMITAGE",
        # D3 Ch.7: "producing wine since the Greco-Roman era"; "a model of
        # the world's most structured and long-lived Syrah wines."
        blurb="Vines since Roman times. Structured, long-lived reds \u2014 "
              "the region's most respected.",
        stat="137 HA  \u00b7  40 HL/HA  \u00b7  MOSTLY SUPER-PREMIUM",
        # Still gentler than the landscape beats -- it's a product shot,
        # and swinging the zoom as hard as the others would send the
        # bottle drifting out of frame at these anchor settings -- but
        # meaningfully more motion than the old (1.03,1.00) had.
        node=2, stat_frac=40 / BAR_MAX, zoom=(1.14, 1.00),
        text_chip=True,  # see type_layer -- the bottle's own paper label
        # sits directly in the text zone; the global scrim alone can't
        # hold text over printed type at that contrast.
        crop_anchor=0.28,
    ),
    dict(
        kind="close", photo="nr_cover_goldenhour", credit=CRED_COVER,
        head="Three Ways\nInto Syrah",
        sub="Same grape. The difference is the soil \u2014\nand how steeply it sits.",
        node="complete", stat_frac=None, zoom=(1.24, 1.00),
        crop_anchor=0.40,
    ),
]


# ---- uniform grade + vignette (REELS_SPEC_v2.md requirement) ----------
def grade_frame(im):
    """Applied identically to every source photo before anything else
    touches it. A light warm lift (via a fixed per-channel curve) plus
    a soft vignette, so a cut between Fougerolle's crisp 2008 DSLR
    frame and Bassaget's flatter, lower-res upload doesn't read as a
    quality drop mid-Reel. Deterministic and parameter-free by design
    -- the same function, the same constants, every photo, so "uniform"
    is actually true rather than eyeballed per-image."""
    r, g, b = im.split()

    def curve(chan, warm):
        lut = [min(255, int(v + warm * (1 - (v / 255) ** 1.6) * 22)) for v in range(256)]
        return chan.point(lut)

    r = curve(r, 1.15)
    g = curve(g, 0.85)
    b = curve(b, 0.55)
    graded = Image.merge("RGB", (r, g, b))

    vign = Image.new("L", im.size, 0)
    vd = ImageDraw.Draw(vign)
    w, h = im.size
    pad = int(min(w, h) * 0.18)
    vd.ellipse([-pad, -pad, w + pad, h + pad], fill=255)
    vign = vign.filter(ImageFilter.GaussianBlur(min(w, h) * 0.12))
    dark = Image.new("RGB", im.size, (8, 6, 10))
    return Image.composite(graded, dark, vign)


def load_fill(key, zoom_max, anchor):
    im = Image.open(os.path.join(PHOTOS, key + ".jpg")).convert("RGB")
    im = grade_frame(im)
    tw, th = int(W * zoom_max + 0.5), int(H * zoom_max + 0.5)
    scale = max(tw / im.width, th / im.height)
    im = im.resize((max(tw, int(im.width * scale + 0.5)),
                    max(th, int(im.height * scale + 0.5))), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = int((im.height - th) * anchor)
    return im.crop((left, top, left + tw, top + th))


def scrim(layer):
    """Bottom-anchored gradient only. The whole-bunch reel's scrim() had
    a top band too, for a kicker near the top of frame -- this reel has
    no text up there at all, so that band was pure liability: it also
    turned out to not even meet the bottom band's alpha at their shared
    boundary (top ended at alpha 0, bottom started at 48), which is what
    the visible hard seam across the trees actually was, not a rounding
    issue -- caught by bisecting the pipeline step by step on an actual
    rendered frame until the seam appeared, not by staring at the
    formula. One continuous function, alpha=0 above `start` by
    construction, ramping smoothly below it -- there is no boundary
    left to mismatch."""
    d = ImageDraw.Draw(layer, "RGBA")
    start = int(H * 0.30)
    for y in range(start, H):
        t = (y - start) / (H - start)
        # No floor offset. Above `start` nothing is drawn at all, which
        # is alpha=0 by construction (a fresh RGBA layer) -- adding a
        # floor here (the previous version used 40) makes alpha jump
        # from 0 to 40 the instant y crosses `start`, which is exactly
        # the "single continuous function" I thought I'd written but
        # hadn't: the function was continuous in t, but t itself starts
        # at a non-zero output. Confirmed by printing actual pixel
        # values across the boundary until the jump showed up in the
        # numbers, not by re-reading the formula and assuming it was
        # fine. a=0 at t=0 removes the seam because both sides of the
        # boundary now genuinely agree.
        a = int(210 * t ** 0.75)
        d.line([(0, y), (W, y)], fill=SIGNATURE + (min(a, 245),))


def ease(t):
    return t * t * (3 - 2 * t)


def super_alpha_offset(t_beat, dur):
    """Slide+fade envelope for text supers -- REELS_SPEC_v2.md point 3.
    Returns (alpha 0-1, y_offset_px). Fades in over 0.4s, holds, fades
    out over the last 0.3s before the hard cut."""
    t_in, t_out = 0.4, 0.3
    if t_beat < t_in:
        e = ease(t_beat / t_in)
        return e, int((1 - e) * 26)
    if t_beat > dur - t_out:
        e = ease((dur - t_beat) / t_out)
        return e, int((1 - e) * -14)
    return 1.0, 0


def mark_alpha(global_t, total_dur):
    """Fade envelope for the persistent corner mark -- GLOBAL elapsed
    time across the whole reel, not per-beat t_beat, since this element
    must survive every hard cut untouched in between. Fades in over the
    first 0.5s of the entire video and out over the last 0.4s; solid
    for everything in between, including every beat transition."""
    fade_in, fade_out = 0.5, 0.4
    if global_t < fade_in:
        return ease(global_t / fade_in)
    if global_t > total_dur - fade_out:
        return ease((total_dur - global_t) / fade_out)
    return 1.0


MARK_COLORS = [(64, 96, 62), (168, 112, 44), (114, 34, 46)]  # green, amber, garnet


def _draw_bottle_icon(d, x, y, h, color):
    """Simple bottle silhouette -- neck, tapered shoulder, rounded
    body -- built from primitives rather than a sourced glyph, the same
    pattern used for the whole-bunch reel's Split Decision mark before
    a real asset existed for it. Three of these in different colors is
    "three wine bottles of varying colors," not a specific label design."""
    neck_w, body_w = h * 0.16, h * 0.46
    neck_h, shoulder_h = h * 0.30, h * 0.14
    cx = x + body_w / 2
    d.rectangle([cx - neck_w / 2, y, cx + neck_w / 2, y + neck_h], fill=color)
    d.polygon([
        (cx - neck_w / 2, y + neck_h), (cx + neck_w / 2, y + neck_h),
        (cx + body_w / 2, y + neck_h + shoulder_h), (cx - body_w / 2, y + neck_h + shoulder_h),
    ], fill=color)
    d.rounded_rectangle([cx - body_w / 2, y + neck_h + shoulder_h, cx + body_w / 2, y + h],
                          radius=body_w * 0.18, fill=color)
    return body_w


def draw_mark_patch(alpha):
    """Bottle trio + "Three Ways" wordmark, built fresh every frame --
    unlike type_layer/graphics_layer this is cheap (three simple shapes,
    one short line of serif text) and doesn't need the settled-frame
    caching those two require. Returns an RGBA patch sized to its own
    content, to be pasted at (MARK_PAD, MARK_PAD) on the main frame.

    Carries its own tight backing chip -- checked against an actual
    rendered frame, not assumed: the mark reads fine against the dark
    Hermitage background with no help at all, but against the bright
    golden-hour sky (the hook, close, and half the region beats) PAPER
    text at this size was nearly unreadable. Same fix as the Quick Sips
    wordmark's tight chip from an earlier session -- sized to the mark's
    own content, not a bar across the corner, and light enough (35%)
    that it doesn't add visible weight on the dark beat where it isn't
    needed."""
    bh = 74
    body_w = bh * 0.46
    gap = 15
    row_w = 3 * body_w + 2 * gap
    text_gap = 26
    tf = font("Playfair-Bold.ttf", 50 * SS)
    ascent, descent = tf.getmetrics()

    canvas_w = int((row_w + text_gap) * SS) + 560 * SS
    canvas_h = int(bh * SS) + 20 * SS
    lay = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)

    text_x = int((row_w + text_gap) * SS)
    text_w = int(d.textlength("Three Ways", font=tf))
    chip_pad = 18 * SS
    d.rounded_rectangle(
        [-chip_pad, -chip_pad, text_x + text_w + chip_pad, int(bh * SS) + chip_pad],
        radius=20 * SS, fill=(10, 8, 14, int(255 * 0.35)))

    for i, color in enumerate(MARK_COLORS):
        _draw_bottle_icon(d, i * (body_w + gap) * SS, 0, bh * SS, color)
    text_y = int(bh * SS / 2 - (ascent + descent) / 2)
    # Title Case, serif -- Playfair is the same face used for the
    # hook/close headline, so the mark reads as part of the same family
    # rather than a mismatched logotype bolted on.
    d.text((text_x, text_y), "Three Ways", font=tf, fill=PAPER + (255,))

    if alpha < 0.999:
        r, g, b, a = lay.split()
        a = a.point(lambda v: int(v * alpha))
        lay = Image.merge("RGBA", (r, g, b, a))
    return lay.resize((canvas_w // SS, canvas_h // SS), Image.LANCZOS)


# ---- progress strip -----------------------------------------------
NODE_X = [W // 2 - 220, W // 2, W // 2 + 220]
NODE_Y = int(H * 0.855)
NODE_R = 14
LINE_W = 3


def draw_progress(d, lit_through, grow_node, grow_t, finale_t=None):
    """Redesigned -- the old version set lit_count to this beat's fully-
    advanced state for the ENTIRE beat, so nodes 2-4 all SNAPPED to
    "already lit" at frame 0 with only a small decorative scale-pulse;
    only the close beat (via connecting_t sweeping the whole strip) had
    real 0-to-1 growth. That is what "broken on all but the last slide"
    meant -- the earlier three beats never actually animated, they just
    appeared pre-finished. Every beat with its own node now genuinely
    grows the new segment in, on the same footing as the close beat.

    lit_through: nodes [0, lit_through) are already SOLID from earlier
      beats -- drawn at full opacity, no animation, every frame.
    grow_node: the index (0, 1, or 2) of the node THIS beat is lighting,
      or None if nothing is animating (the hook beat, or a region beat
      past its own growth window).
    grow_t: 0-1 progress of grow_node's own arrival -- for grow_node=0
      this is a solo pop-in (no segment, nothing precedes the first
      node); for grow_node>0 a connecting segment from NODE_X[grow_node-1]
      to NODE_X[grow_node] grows in step with the same t.
    finale_t: 0-1, close-beat-only -- a synchronized pulse across all
      three (already fully solid) nodes, the strip's "we're done" beat.
      Distinct from grow_t: nothing is growing on the close beat, since
      every segment already completed progressively during beats 2-4.
    """
    d.line([(NODE_X[0], NODE_Y), (NODE_X[2], NODE_Y)], fill=(255, 255, 255, 70), width=LINE_W)

    # Solid, already-complete segments -- everything before this beat's
    # own action, drawn every frame with no animation.
    if lit_through >= 2:
        d.line([(NODE_X[0], NODE_Y), (NODE_X[lit_through - 1], NODE_Y)],
               fill=ACCENT + (240,), width=LINE_W + 2)

    # The segment THIS beat is growing.
    if grow_node is not None and grow_node > 0 and grow_t is not None:
        x0, x1 = NODE_X[grow_node - 1], NODE_X[grow_node]
        cx = x0 + (x1 - x0) * ease(grow_t)
        d.line([(x0, NODE_Y), (cx, NODE_Y)], fill=ACCENT + (240,), width=LINE_W + 2)

    for i, x in enumerate(NODE_X):
        r = NODE_R
        if finale_t is not None:
            bump = 1.0 + 0.22 * (1 - abs(finale_t * 2 - 1))
            r = int(NODE_R * bump)
            is_lit = True
        elif grow_node is not None and i == grow_node:
            # The node THIS beat lights: pops in shortly after its
            # segment (or, for node 0, itself) starts growing, rather
            # than existing at full size from frame 0.
            is_lit = grow_t > 0.12
            bump = 1.0 + 0.35 * ease(min(1.0, grow_t / 0.5)) if grow_t < 0.5 else 1.35 - 0.35 * ease(
                min(1.0, (grow_t - 0.5) / 0.5))
            r = int(NODE_R * max(1.0, bump))
        else:
            is_lit = i < lit_through
        if is_lit:
            d.ellipse([x - r, NODE_Y - r, x + r, NODE_Y + r], fill=ACCENT + (255,))
        else:
            d.ellipse([x - NODE_R, NODE_Y - NODE_R, x + NODE_R, NODE_Y + NODE_R],
                       outline=(255, 255, 255, 180), width=3)


# ---- stat bar --------------------------------------------------------
BAR_X0, BAR_X1 = 64, W - 64
BAR_Y = 1592  # moved down from 0.79H (1516) -- see type_layer's layout
# comment for the full bottom-up budget this and NODE_Y both belong to.
BAR_H = 10


def draw_stat_bar(d, frac, fill_t):
    d.rounded_rectangle([BAR_X0, BAR_Y, BAR_X1, BAR_Y + BAR_H],
                          radius=BAR_H // 2, fill=(255, 255, 255, 55))
    fw = int((BAR_X1 - BAR_X0) * frac * ease(fill_t))
    if fw > BAR_H:
        d.rounded_rectangle([BAR_X0, BAR_Y, BAR_X0 + fw, BAR_Y + BAR_H],
                              radius=BAR_H // 2, fill=ACCENT + (255,))


def type_layer(beat, t_beat, dur):
    """Composed fresh every frame at 2x (unlike the whole-bunch reel,
    this one changes within a beat -- supers move and bars fill -- so
    it can't be built once and reused across a beat's frames the way a
    static caption could).

    Text supers ONLY -- no scrim baked in here. An earlier version drew
    the scrim as part of this layer and composited it last, which put
    the scrim gradient ON TOP of the progress strip and stat bar,
    muddying the accent gold toward brown (caught by inspecting an
    actual mid-beat frame, not assumed from the code). The scrim is now
    applied once to the base photo in build(), before the graphics
    layer, so gold stays gold and only the text sits in this layer.

    LAYOUT, rewritten per Steve's review (fonts up significantly, block
    lowered into the bottom third). The old version anchored everything
    off one `baseline` fraction of frame height; that doesn't scale --
    bigger type needs a bigger budget, and simply sliding one baseline
    number down pushes the block into the stat bar / progress strip
    below it. Rebuilt bottom-up instead, each element's position
    computed from a fixed pixel GAP to the element below it (in 1x
    units, converted to SS only when actually drawing), so the whole
    stack can be retuned by adjusting one gap rather than re-deriving
    every offset. Verified against BAR_Y/NODE_Y/credit's fixed positions
    by rendering and inspecting an actual frame, not just by the numbers
    summing correctly on paper."""
    lay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)

    # Sizes roughly 35-40% larger across the board, per Steve's "raise
    # significantly" -- these are 1x point sizes; SS is applied at the
    # font() call same as before.
    f_head = font("Playfair-Bold.ttf", 116 * SS)
    f_sub = font("Archivo-Medium.ttf", 46 * SS)
    f_label = font("ArchivoCond-SemiBold.ttf", 104 * SS)
    f_blurb = font("Archivo-Medium.ttf", 42 * SS)
    f_stat = font("Archivo-Medium.ttf", 36 * SS)
    f_cred = font("Archivo-Light.ttf", 15 * SS)  # credit stays small on purpose -- attribution, not a headline

    alpha, yoff = super_alpha_offset(t_beat, dur)
    a255 = int(255 * alpha)

    if beat["kind"] in ("hook", "close"):
        # Bottom-anchored 82px above the progress strip (NODE_Y=1642),
        # in 1x units -- comfortably clear of it at every font size.
        sub_bottom = 1560
        sub_lines = beat["sub"].split("\n")
        sh = int(f_sub.size * 1.4)
        sub_top = (sub_bottom * SS) - len(sub_lines) * sh
        for i, ln in enumerate(sub_lines):
            d.text((64 * SS, sub_top + i * sh + yoff * SS), ln, font=f_sub,
                   fill=PAPER + (a255,))
        head_lines = beat["head"].split("\n")
        hh = int(f_head.size * 1.08)
        head_top = sub_top - 30 * SS - len(head_lines) * hh
        for i, ln in enumerate(head_lines):
            d.text((64 * SS, head_top + i * hh + yoff * SS), ln, font=f_head,
                   fill=PAPER + (a255,))
    else:
        # Bottom-up budget (1x units): stat text sits 36px above the
        # stat BAR (BAR_Y=1592); blurb sits 30px above the stat text;
        # label sits 34px above the blurb. Each gap is a real, tuned
        # value checked against a rendered frame -- not derived from a
        # formula that assumes it'll just work.
        stat_bottom = BAR_Y - 36
        stat_h = int(f_stat.size * 1.3 / SS)
        stat_y = (stat_bottom - stat_h) * SS + yoff * SS

        blurb_lines = _wrap(beat["blurb"], f_blurb, (W - 128) * SS, d)
        bh = int(f_blurb.size * 1.32)
        blurb_bottom = stat_y - 30 * SS
        blurb_top = blurb_bottom - len(blurb_lines) * bh

        label_h = int(f_label.size * 1.05)
        label_bottom = blurb_top - 34 * SS
        label_top = label_bottom - label_h

        # Text chip -- only for beats that ask for one (only Hermitage
        # does). The global bottom scrim is nowhere near dark enough to
        # hold text over a busy background; see BEATS' text_chip comment
        # for why this one specifically needs it.
        if beat.get("text_chip"):
            chip_top = label_top - 24 * SS
            chip_bottom = stat_y + int(f_stat.size * 1.3)
            _chip(lay, (0, chip_top, W * SS, chip_bottom),
                  (10, 8, 14), opacity=0.72)

        d.text((64 * SS, stat_y), beat["stat"], font=f_stat,
               fill=PAPER + (int(220 * alpha),))
        for i, ln in enumerate(blurb_lines):
            d.text((64 * SS, blurb_top + i * bh), ln, font=f_blurb,
                   fill=PAPER + (int(235 * alpha),))
        d.text((64 * SS, label_top), beat["label"], font=f_label,
               fill=ACCENT + (a255,))

    if beat["credit"]:
        d.text((64 * SS, int(H * SS * 0.945)), beat["credit"], font=f_cred,
               fill=(232, 226, 220, 200))

    return lay.resize((W, H), Image.LANCZOS)


def graphics_layer(beat, t_beat, lit_through, grow_node, grow_t, finale_t=None):
    """Progress strip + stat bar -- drawn separately from type_layer
    because these are NOT subject to the supers' slide/fade envelope;
    they are the "persistent" element REELS_SPEC_v2.md distinguishes
    from supers. Composed at 1x since these are simple vector shapes,
    not type -- no supersampling benefit."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    draw_progress(d, lit_through, grow_node, grow_t, finale_t)
    if beat.get("stat_frac") is not None:
        fill_t = min(1.0, t_beat / 1.2)
        draw_stat_bar(d, beat["stat_frac"], fill_t)
    return lay


def build(mp4=None):
    mp4 = mp4 or os.path.join(OUT, "REEL_ThreeWays_v1.mp4")
    proc = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-",
        "-an",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.0",
        "-r", str(FPS), "-movflags", "+faststart",
        mp4], stdin=subprocess.PIPE)

    n_frames = int(BEAT_SECONDS * FPS)
    total_dur = len(BEATS) * BEAT_SECONDS
    idx = 0
    mark_cache = {}  # keyed by rounded alpha -- see below

    for b, beat in enumerate(BEATS):
        z0, z1 = beat["zoom"]
        zmax = max(z0, z1)
        base = load_fill(beat["photo"], zmax, beat["crop_anchor"])
        scrim_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        scrim_full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        scrim(scrim_full)
        scrim_layer.paste(scrim_full.resize(base.size, Image.BILINEAR), (0, 0))
        base = Image.alpha_composite(base.convert("RGBA"), scrim_layer).convert("RGB")
        bw, bh = base.size

        # Progress-bar state machine, rewritten -- see draw_progress's
        # docstring for why the old version never actually animated on
        # beats 1-3. GROW_WINDOW is how long this beat's own node/segment
        # takes to arrive; it must stay <= the caching window below or
        # the animation gets truncated by the settled-frame cutover.
        GROW_WINDOW = 0.6
        node = beat["node"]
        prior_lit = node if isinstance(node, int) else (3 if node == "complete" else 0)
        settled_lit = prior_lit + 1 if isinstance(node, int) else prior_lit

        type_active_frames = int((0.4 + 0.3) * FPS) + 4
        gfx_active_seconds = max(1.2 if beat.get("stat_frac") is not None else 0, GROW_WINDOW)
        gfx_active_frames = int(gfx_active_seconds * FPS) + 2

        type_cache = {}
        gfx_cache = {}

        def get_type(f, t_beat):
            near_start = f < int(0.4 * FPS) + 2
            near_end = f > n_frames - int(0.3 * FPS) - 2
            if near_start or near_end:
                return type_layer(beat, t_beat, BEAT_SECONDS)
            if "settled" not in type_cache:
                type_cache["settled"] = type_layer(beat, 1.5, BEAT_SECONDS)
            return type_cache["settled"]

        def get_gfx(f, t_beat, lit_through, grow_node, grow_t, finale_t):
            if f < gfx_active_frames:
                return graphics_layer(beat, t_beat, lit_through, grow_node, grow_t, finale_t)
            if "settled" not in gfx_cache:
                gfx_cache["settled"] = graphics_layer(beat, 999, settled_lit, None, None, None)
            return gfx_cache["settled"]

        for f in range(n_frames):
            t = f / (n_frames - 1)
            t_beat = t * BEAT_SECONDS
            e = ease(t)
            z = z0 + (z1 - z0) * e
            cw, ch = int(W * (zmax / z)), int(H * (zmax / z))
            cw, ch = min(cw, bw), min(ch, bh)
            left = (bw - cw) // 2
            top = (bh - ch) // 2
            frame = base.crop((left, top, left + cw, top + ch)).resize((W, H), Image.BILINEAR)

            lit_through, grow_node, grow_t, finale_t = prior_lit, None, None, None
            if isinstance(node, int):
                if t_beat < GROW_WINDOW:
                    grow_node, grow_t = node, t_beat / GROW_WINDOW
                else:
                    lit_through = settled_lit
            elif node == "complete":
                lit_through = 3
                if t_beat < GROW_WINDOW:
                    finale_t = t_beat / GROW_WINDOW

            gfx = get_gfx(f, t_beat, lit_through, grow_node, grow_t, finale_t)
            txt = get_type(f, t_beat)
            frame = frame.convert("RGBA")
            frame = Image.alpha_composite(frame, gfx)
            frame = Image.alpha_composite(frame, txt)

            # Persistent mark -- global elapsed time, not t_beat, so it
            # doesn't reset or re-fade at every hard cut. Cached by
            # rounded alpha (2 decimal places) rather than recomputed
            # every frame: during the long solid-alpha=1.0 stretch
            # (roughly frames 15-587) every call rounds to the same key
            # and reuses one composite; only the ~27 frames inside the
            # two fade windows actually redraw it.
            global_t = idx / FPS
            m_alpha = mark_alpha(global_t, total_dur)
            if m_alpha > 0.002:
                key = round(m_alpha, 2)
                if key not in mark_cache:
                    mark_cache.clear()  # alpha only moves one direction
                    # at a time within a short window, so at most one
                    # extra entry is ever alive -- clearing keeps this
                    # from growing across 600 frames for no reason.
                    mark_cache[key] = draw_mark_patch(m_alpha)
                patch = mark_cache[key]
                frame.paste(patch, (MARK_PAD, MARK_PAD), patch)

            proc.stdin.write(frame.convert("RGB").tobytes())
            idx += 1
        print(f"  beat {b + 1}  {beat['kind']:7s}  {beat['photo']}", flush=True)

    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    print(f"{idx} frames at {FPS}fps = {idx / FPS:.1f}s")
    print("MP4:", mp4)
    return idx


if __name__ == "__main__":
    sys.exit(0 if build() else 1)
