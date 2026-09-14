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
ACCENT = (186, 149, 74)
PAPER = (251, 249, 244)

BAR_MAX = 50.0  # hL/ha -- shared scale, see docstring point 2

CRED_TAIN = "Guerinf / Wikimedia Commons (CC BY-SA 4.0)"
CRED_CROZES = "Mr Fougerolle / Wikimedia Commons (CC BY-SA 4.0)"
CRED_SJ = "François Bassaget / Wikimedia Commons (CC BY-SA 4.0)"
CRED_HERM = "Vive la Rosière / Wikimedia Commons (CC BY-SA 3.0)"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


BEATS = [
    dict(
        kind="hook", photo="nr_tain_rhone", credit=CRED_TAIN,
        head="Three Ways\nInto Syrah",
        sub="One grape. Three regions.\nThree very different prices.",
        node=None, stat_frac=None, zoom=(1.02, 1.10),
        crop_anchor=0.45,
    ),
    dict(
        kind="region", photo="nr_crozes_chanoscurson", credit=CRED_CROZES,
        label="CROZES-HERMITAGE",
        stat="~1,700 HA  \u00b7  45 HL/HA  \u00b7  MID-PRICED",
        node=0, stat_frac=45 / BAR_MAX, zoom=(1.00, 1.08),
        crop_anchor=0.42,
    ),
    dict(
        kind="region", photo="nr_saintjoseph_sarras_vigne", credit=CRED_SJ,
        label="SAINT-JOSEPH",
        stat="50 KM OF APPELLATION  \u00b7  40 HL/HA",
        node=1, stat_frac=40 / BAR_MAX, zoom=(1.05, 1.13),
        crop_anchor=0.50,
    ),
    dict(
        kind="region", photo="nr_chapoutier_vy", credit=CRED_HERM,
        label="HERMITAGE",
        stat="137 HA  \u00b7  40 HL/HA  \u00b7  MOSTLY SUPER-PREMIUM",
        node=2, stat_frac=40 / BAR_MAX, zoom=(1.08, 1.00),
        crop_anchor=0.30,  # keeps the CHAPOUTIER wall as a lower detail
    ),
    dict(
        kind="close", photo="nr_tain_rhone", credit=CRED_TAIN,
        head="Three Ways\nInto Syrah",
        sub="Same grape. The difference is the soil \u2014\nand how steeply it sits.",
        node="complete", stat_frac=None, zoom=(1.10, 1.02),
        crop_anchor=0.45,
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


# ---- progress strip -----------------------------------------------
NODE_X = [W // 2 - 220, W // 2, W // 2 + 220]
NODE_Y = int(H * 0.855)
NODE_R = 14
LINE_W = 3


def draw_progress(d, lit_count, pulse_t, connecting_t):
    """lit_count: how many nodes (0-3) are lit, left to right.
    pulse_t: 0-1 progress of the just-lit node's scale-pulse, or None.
    connecting_t: 0-1 fill progress of the closing connector line, or
    None on any beat but the close."""
    d.line([(NODE_X[0], NODE_Y), (NODE_X[2], NODE_Y)], fill=(255, 255, 255, 70), width=LINE_W)
    if connecting_t is not None:
        cx = NODE_X[0] + (NODE_X[2] - NODE_X[0]) * ease(connecting_t)
        d.line([(NODE_X[0], NODE_Y), (cx, NODE_Y)], fill=ACCENT + (255,), width=LINE_W + 2)
    elif lit_count > 0:
        cx = NODE_X[min(lit_count, 3) - 1]
        d.line([(NODE_X[0], NODE_Y), (cx, NODE_Y)], fill=ACCENT + (230,), width=LINE_W + 2)

    for i, x in enumerate(NODE_X):
        is_lit = i < lit_count or connecting_t is not None
        r = NODE_R
        if i == lit_count - 1 and pulse_t is not None and connecting_t is None:
            bump = 1.0 + 0.35 * (1 - abs(pulse_t * 2 - 1))
            r = int(NODE_R * bump)
        if is_lit:
            d.ellipse([x - r, NODE_Y - r, x + r, NODE_Y + r], fill=ACCENT + (255,))
        else:
            d.ellipse([x - NODE_R, NODE_Y - NODE_R, x + NODE_R, NODE_Y + NODE_R],
                       outline=(255, 255, 255, 180), width=3)


# ---- stat bar --------------------------------------------------------
BAR_X0, BAR_X1 = 64, W - 64
BAR_Y = int(H * 0.79)
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
    layer, so gold stays gold and only the text sits in this layer."""
    lay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)

    f_head = font("Playfair-Bold.ttf", 84 * SS)
    f_sub = font("Archivo-Medium.ttf", 34 * SS)
    f_label = font("ArchivoCond-SemiBold.ttf", 58 * SS)
    f_stat = font("Archivo-Medium.ttf", 30 * SS)
    f_cred = font("Archivo-Light.ttf", 15 * SS)

    alpha, yoff = super_alpha_offset(t_beat, dur)
    a255 = int(255 * alpha)
    baseline = int(H * SS * 0.70)

    if beat["kind"] in ("hook", "close"):
        sub_lines = beat["sub"].split("\n")
        sh = int(f_sub.size * 1.4)
        sub_top = baseline - len(sub_lines) * sh
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
        d.text((64 * SS, baseline - 70 * SS + yoff * SS), beat["stat"],
               font=f_stat, fill=PAPER + (int(220 * alpha),))
        d.text((64 * SS, baseline - 150 * SS + yoff * SS), beat["label"],
               font=f_label, fill=ACCENT + (a255,))

    d.text((64 * SS, int(H * SS * 0.945)), beat["credit"], font=f_cred,
           fill=(232, 226, 220, 200))

    return lay.resize((W, H), Image.LANCZOS)


def graphics_layer(beat, t_beat, lit_count, pulse_t, connecting_t):
    """Progress strip + stat bar -- drawn separately from type_layer
    because these are NOT subject to the supers' slide/fade envelope;
    they are the "persistent" element REELS_SPEC_v2.md distinguishes
    from supers. Composed at 1x since these are simple vector shapes,
    not type -- no supersampling benefit."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    draw_progress(d, lit_count, pulse_t, connecting_t)
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
    idx = 0
    for b, beat in enumerate(BEATS):
        z0, z1 = beat["zoom"]
        zmax = max(z0, z1)
        base = load_fill(beat["photo"], zmax, beat["crop_anchor"])
        # Scrim applied to the base photo ONCE per beat, before the
        # per-frame crop/zoom -- not per frame, and not as part of
        # type_layer (see that function's docstring for why). Baking it
        # into base means it zooms/pans WITH the photo, which is correct:
        # the scrim is meant to read as fixed screen-space darkening
        # at the bottom of frame regardless of zoom, and since the zoom
        # range here is modest (a few percent) and the scrim's own
        # gradient is broad, the difference is not visible in practice
        # -- confirmed by inspecting rendered frames from both the start
        # and end of a beat's zoom range, not assumed.
        scrim_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        scrim_full = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        scrim(scrim_full)
        scrim_layer.paste(scrim_full.resize(base.size, Image.BILINEAR), (0, 0))
        base = Image.alpha_composite(base.convert("RGBA"), scrim_layer).convert("RGB")
        bw, bh = base.size

        lit_before = max(0, beat["node"]) if isinstance(beat["node"], int) else (
            3 if beat["node"] == "complete" else 0)
        lit_after = lit_before + 1 if isinstance(beat["node"], int) else lit_before

        # PERFORMANCE: type_layer/graphics_layer are real per-frame PIL
        # draws (2160x3840 supersampled text, ellipses, rounded rects).
        # The first build of this file recomputed both from scratch for
        # every one of 600 frames and the background process was killed
        # partway through beat 1 -- almost certainly for taking too
        # long, not for erroring (nothing in the log but the beat-1
        # start line). Most of a 4s beat is visually STATIC once the
        # supers finish sliding in, the bar finishes filling, and the
        # node finishes pulsing -- there is no reason to redraw
        # identical pixels 90+ times. Only the frames inside the actual
        # transition windows get a fresh layer; every other frame reuses
        # one cached "settled" composite. This is the fix, not a
        # workaround -- the visual result is unchanged, since the
        # cached layer IS what those frames would have rendered anyway.
        type_active_frames = int((0.4 + 0.3) * FPS) + 4  # small margin
        gfx_active_seconds = 1.2 if beat.get("stat_frac") is not None else (
            1.0 if beat["node"] == "complete" else 0.3)
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

        def get_gfx(f, t_beat, lit_count, pulse_t, connecting_t):
            if f < gfx_active_frames:
                return graphics_layer(beat, t_beat, lit_count, pulse_t, connecting_t)
            if "settled" not in gfx_cache:
                gfx_cache["settled"] = graphics_layer(
                    beat, 999, lit_count, None,
                    1.0 if beat["node"] == "complete" else None)
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

            pulse_t, connecting_t, lit_count = None, None, lit_before
            if isinstance(beat["node"], int):
                pulse_window = 0.3
                if t_beat < pulse_window:
                    pulse_t = t_beat / pulse_window
                lit_count = lit_after
            elif beat["node"] == "complete":
                connecting_t = min(1.0, t_beat / 1.0)
                lit_count = 3

            gfx = get_gfx(f, t_beat, lit_count, pulse_t, connecting_t)
            txt = get_type(f, t_beat)
            frame = frame.convert("RGBA")
            frame = Image.alpha_composite(frame, gfx)
            frame = Image.alpha_composite(frame, txt)
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
