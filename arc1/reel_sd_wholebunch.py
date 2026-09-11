"""REEL TEST CUT — Split Decision: Whole Bunch or Destemmed. Arc 1.

Per REELS_SPEC_v1.md: 1080x1920, five beats of ~3s, frame 1 carries the
complete hook, the final beat closes the loop back to frame 1, silent-
legible throughout, audio left empty, hard cuts only, motion limited to
a slow scale on a still.

WHY THIS IS A STANDALONE COMPOSER AND NOT A MODULE CALL.

The spec is explicit that vertical is re-composed on a 1080x1920 canvas
and never cropped from the 2160x2700 render. `duel` and `side_rail`
have no vertical layout mode, and writing one into shared modules to
answer a question that is still "is this format worth committing to"
would be building the road before choosing the destination. This file
composes the five beats directly from the same palette, the same fonts
and the same Split Decision mark the deck uses, so the cut looks like
the series without touching engine code. If the format is approved, the
right move is a vertical mode on the modules and this file is thrown
away.

FRAMES ARE PIPED STRAIGHT TO FFMPEG. Writing 450 PNGs to disk and
re-reading them cost more than the whole render; raw RGB frames go down
a pipe instead, so nothing intermediate touches the filesystem.

TYPE IS RENDERED AT 2x AND DOWNSAMPLED. Drawing 96px Playfair straight
onto a 1080px canvas gives visibly coarse stems at the weights this
series uses. Each beat's type layer is composed once at 2160x3840 and
LANCZOS-reduced, then composited over the moving photo every frame. The
photo itself moves, so it is resampled per frame; the type does not
move, so it is resampled once.

SOURCE COPY is lifted from render_sd_wholebunch.py without rewriting
the argument. A reel is a distribution treatment, not new editorial.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PHOTOS = os.path.join(REPO, "photos")
FONTS = os.path.join(REPO, "fonts")
OUT = "/home/claude/out_reel_sd"

W, H = 1080, 1920
FPS = 30
BEAT_SECONDS = 3.0
SS = 2  # type supersample factor

# Arc 1 signature palette, identical to render_sd_wholebunch.py.
SIGNATURE = (58, 26, 46)
ACCENT = (186, 149, 74)
PAPER = (251, 249, 244)

CRED_LEMOINE = "Olivier Lemoine / Wikimedia Commons (CC BY-SA 4.0)"

# The two poles, and nothing else, carry these.
POLE_COLOUR = {"STEMS IN": ACCENT, "STEMS OUT": PAPER}
CRED_AGNE = "Agne27 / Wikimedia Commons (CC BY-SA 3.0)"
CRED_BECKER = "Nico Becker / Pexels"
CRED_LEMOINE_PT = ("Olivier Lemoine (Photo-Terroir.fr) / "
                   "Wikimedia Commons (CC BY-SA 4.0)")


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


# ── The five beats ────────────────────────────────────────────────────
#
# kind="hook"   : kicker + big question + one line of setup
# kind="pole"   : a labelled side of the argument
# kind="turn"   : the mechanism
# kind="reopen" : re-poses the question verbatim so the replay is seamless
BEATS = [
    dict(
        kind="hook",
        photo="nr_syrah_bunch",
        credit=CRED_AGNE,
        kicker="SPLIT DECISION",
        head="Whole Bunch\nor Destemmed?",
        body="Northern Rhone cru reds are made both ways.\nThe choice changes the wine more than the\nvintage does.",
        zoom=(1.02, 1.10),
    ),
    dict(
        kind="pole",
        photo="nr_harvest_hands",
        credit=CRED_BECKER,
        label="STEMS IN",
        head="Bunches go in\nintact.",
        body="Aeration of the must. Perfume, freshness,\nfine tannin \u2014 if the stems are ripe.",
        zoom=(1.00, 1.07),
    ),
    dict(
        kind="pole",
        # NOT nr_syrah_bunch. v1 used it here and the beat arguing for
        # destemming was illustrated with a whole intact bunch on the
        # vine -- the wrong side of the argument, on the slide making
        # that side's case. A cellar vessel is neutral: it asserts
        # nothing about stems either way.
        photo="nr_demimuid",
        credit=CRED_LEMOINE_PT,
        label="STEMS OUT",
        head="Destemmed,\nchilled, soaked.",
        body="Cold soak of one to three days to draw out\ncolour. Nothing green can reach the wine.",
        zoom=(1.10, 1.02),
    ),
    dict(
        kind="turn",
        photo="nr_cellar_foudre",
        credit=CRED_LEMOINE,
        kicker="THE MECHANISM",
        head="It turns on\nstem ripeness.",
        body="Not style. Not tradition. Unripe stems give\ngreen tannin and lower acidity \u2014 least\nwelcome in a warm vintage.",
        zoom=(1.02, 1.11),
    ),
    dict(
        kind="reopen",
        # Returns to beat 1's photograph, and ends on beat 1's opening
        # zoom, so the replay is continuous in image as well as words.
        # v1 re-posed the question over the cellar shot: the type
        # matched on loop and the picture jumped.
        photo="nr_syrah_bunch",
        credit=CRED_AGNE,
        kicker="AND YET",
        # Three lines, matching beat 1, because the type block is
        # bottom-anchored: a two-line body pushes the headline ~60px
        # down and the loop seam shows it. The third line is the deck's
        # own closing question, which the reel wanted anyway -- v1
        # stated a fact where the style guide requires a re-opening.
        body="Burgundy destemmed after Jayer.\nThen came back.\n"
             "Which of those was the fashion?",
        head="Whole Bunch\nor Destemmed?",
        zoom=(1.10, 1.02),
    ),
]


def load_fill(key, zoom_max):
    """Photo scaled to fill 1080x1920 at the beat's maximum zoom."""
    im = Image.open(os.path.join(PHOTOS, key + ".jpg")).convert("RGB")
    tw, th = int(W * zoom_max + 0.5), int(H * zoom_max + 0.5)
    scale = max(tw / im.width, th / im.height)
    im = im.resize((max(tw, int(im.width * scale + 0.5)),
                    max(th, int(im.height * scale + 0.5))), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    return im.crop((left, top, left + tw, top + th))


def scrim(layer):
    """Top and bottom gradients so type is legible over any photo.

    Heavier at the bottom than a 4:5 slide needs: a reel is read on a
    phone in sunlight with sound off, and the type block is the only
    thing carrying the argument.
    """
    d = ImageDraw.Draw(layer, "RGBA")
    for y in range(int(H * 0.30)):
        a = int(150 * (1 - y / (H * 0.30)) ** 1.5)
        d.line([(0, y), (W, y)], fill=SIGNATURE + (a,))
    start = int(H * 0.34)
    for y in range(start, H):
        t = (y - start) / (H - start)
        a = int(28 + 227 * t ** 0.85)
        d.line([(0, y), (W, y)], fill=SIGNATURE + (min(a, 246),))


def sd_glasses(d, x, y, size):
    """Two tilted bowls, drawn from primitives.

    The deck's mark composites the real Quick Sips glass PNG. At reel
    scale that glyph reduces to mush, and the mark's own docstring warns
    the asset has shipped broken twice. Two simple bowls in the two pole
    colours carry the same "clink" idea legibly at 40px.
    """
    for i, col in enumerate((ACCENT, PAPER)):
        cx = x + i * int(size * 0.78)
        lean = -1 if i == 0 else 1
        d.ellipse([cx, y, cx + size, y + int(size * 0.78)], outline=col, width=4)
        d.line([(cx + size // 2 + lean * 4, y + int(size * 0.72)),
                (cx + size // 2 + lean * int(size * 0.22), y + size + 12)],
               fill=col, width=4)


def type_layer(beat):
    """Composed once per beat at 2x, returned at 1080x1920 RGBA."""
    lay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    big = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    scrim(big)
    lay = big.resize((W * SS, H * SS), Image.BILINEAR)
    d = ImageDraw.Draw(lay)

    f_kick = font("ArchivoCond-SemiBold.ttf", 34 * SS)
    f_head = font("Playfair-Bold.ttf", 92 * SS)
    f_body = font("Archivo-Medium.ttf", 40 * SS)
    f_cred = font("Archivo-Light.ttf", 17 * SS)

    sd_glasses(d, 64 * SS, 92 * SS, 44 * SS)

    # Everything above the fold-line is set from the bottom up, so the
    # block sits on a fixed baseline regardless of how many lines the
    # copy runs to. A reel that shifts its type block between beats
    # reads as unstable on replay.
    baseline = int(H * SS * 0.885)

    body_lines = beat["body"].split("\n")
    bh = int(f_body.size * 1.42)
    body_top = baseline - len(body_lines) * bh
    for i, ln in enumerate(body_lines):
        d.text((64 * SS, body_top + i * bh), ln, font=f_body, fill=PAPER)

    head_lines = beat["head"].split("\n")
    hh = int(f_head.size * 1.10)
    head_top = body_top - 34 * SS - len(head_lines) * hh
    for i, ln in enumerate(head_lines):
        d.text((64 * SS, head_top + i * hh), ln, font=f_head, fill=PAPER)

    tag = beat.get("kicker") or beat.get("label")
    if tag:
        # SPLIT_DECISION_STYLE_GUIDE.md: the poles are distinguished by
        # colour and never by size or weight, so neither can look like
        # the favoured side before it has been read. v1 set both poles
        # in PAPER on an ACCENT rule, which distinguished them by
        # nothing at all. Same face, same size, same weight, same rule
        # width -- only the hue moves.
        col = POLE_COLOUR.get(tag, ACCENT)
        d.text((64 * SS, head_top - 52 * SS), tag, font=f_kick, fill=col)
        tw = d.textlength(tag, font=f_kick)
        d.line([(64 * SS, head_top - 14 * SS),
                (64 * SS + tw, head_top - 14 * SS)],
               fill=col, width=3 * SS)

    d.text((64 * SS, int(H * SS * 0.945)), beat["credit"], font=f_cred,
           fill=(232, 226, 220, 205))

    return lay.resize((W, H), Image.LANCZOS)


def build(mp4=None):
    os.makedirs(OUT, exist_ok=True)
    mp4 = mp4 or os.path.join(OUT, "REEL_SD_WholeBunch_testcut.mp4")

    # Audio is deliberately absent: the spec has trending audio attached
    # at upload, because it cannot be chosen days ahead and stay current.
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
    for b, beat in enumerate(BEATS, start=1):
        z0, z1 = beat["zoom"]
        zmax = max(z0, z1)
        base = load_fill(beat["photo"], zmax)
        overlay = type_layer(beat)
        bw, bh = base.size
        for f in range(n_frames):
            t = f / (n_frames - 1)
            # Ease in-out so the push never appears to start or stop.
            e = t * t * (3 - 2 * t)
            z = z0 + (z1 - z0) * e
            cw, ch = int(W * (zmax / z)), int(H * (zmax / z))
            cw, ch = min(cw, bw), min(ch, bh)
            left = (bw - cw) // 2
            top = (bh - ch) // 2
            frame = base.crop((left, top, left + cw, top + ch)).resize(
                (W, H), Image.BILINEAR)
            frame = Image.alpha_composite(frame.convert("RGBA"), overlay)
            proc.stdin.write(frame.convert("RGB").tobytes())
            idx += 1
        print(f"  beat {b}  {beat['kind']:6s}  {beat['photo']}", flush=True)

    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("ffmpeg failed")
    print(f"{idx} frames at {FPS}fps = {idx / FPS:.1f}s")
    print("MP4:", mp4)
    return idx


if __name__ == "__main__":
    sys.exit(0 if build() else 1)
