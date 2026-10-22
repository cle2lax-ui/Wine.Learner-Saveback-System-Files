"""Factor icons (Arc 4): seven simple one-color line icons for the natural Factors of WSET D1 3.1 -- latitude, altitude, slope and aspect,
water, wind, soil, fog and cloud. Drawn in code at 4x and downsampled, so they are crisp at any size and need no image files.
icon(key, size, color) -> an RGBA PIL image."""
import math

from PIL import Image, ImageChops, ImageDraw

KEYS = ("latitude", "altitude", "aspect", "water", "wind", "soil", "fog")


def icon(key, size=256, color=(104, 26, 38)):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = max(4, int(S * 0.062))
    r = w / 2
    col = tuple(color) + (255,)

    def P(x, y):
        return (x * S, y * S)

    def line(pts):
        pp = [P(*p) for p in pts]
        d.line(pp, fill=col, width=w, joint="curve")
        for (x, y) in pp:                                   # round caps and joints
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)

    def circle(cx, cy, rad, fill=False):
        b = [(cx - rad) * S, (cy - rad) * S, (cx + rad) * S, (cy + rad) * S]
        d.ellipse(b, fill=col) if fill else d.ellipse(b, outline=col, width=w)

    if key == "latitude":                                   # a globe with two parallels and a meridian
        circle(.5, .5, .40)
        for dy in (-.17, .17):
            half = math.sqrt(.40 ** 2 - dy ** 2) - .02
            line([(.5 - half, .5 + dy), (.5 + half, .5 + dy)])
        d.ellipse([(.5 - .15) * S, (.5 - .40) * S, (.5 + .15) * S, (.5 + .40) * S], outline=col, width=w)
    elif key == "altitude":                                 # two peaks, a snow cap
        line([(.08, .80), (.36, .30), (.50, .52), (.64, .36), (.92, .80), (.08, .80)])
        line([(.27, .47), (.32, .42), (.36, .47), (.40, .42)])
    elif key == "aspect":                                   # a slope facing the sun
        line([(.08, .86), (.30, .76), (.55, .58), (.78, .44), (.92, .42)])
        line([(.08, .86), (.92, .86)])
        circle(.30, .27, .10)
        for a in range(0, 360, 45):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            line([(.30 + .16 * ca, .27 + .16 * sa), (.30 + .22 * ca, .27 + .22 * sa)])
    elif key == "water":                                    # three waves
        for y0 in (.33, .52, .71):
            line([(.10 + .80 * t / 40, y0 + .05 * math.sin(t / 40 * 4 * math.pi)) for t in range(41)])
    elif key == "wind":                                     # three streaks that hook
        for y0, x1 in ((.30, .66), (.54, .84), (.78, .54)):
            line([(.10, y0), (x1, y0)])
            d.arc([(x1 - .08) * S, (y0 - .16) * S, (x1 + .08) * S, y0 * S], 270, 450, fill=col, width=w)
    elif key == "soil":                                     # strata with stones
        d.rounded_rectangle([.10 * S, .16 * S, .90 * S, .84 * S], radius=.06 * S, outline=col, width=w)
        line([(.14, .40), (.86, .40)])
        line([(.14, .62), (.86, .62)])
        circle(.28, .74, .045, True); circle(.52, .735, .05, True); circle(.74, .74, .04, True)
    elif key == "fog":                                      # a cloud and two fog lines
        def cloud(dr, g):
            for cx, cy, rad in ((.30, .42, .13), (.50, .31, .18), (.70, .42, .13)):
                dr.ellipse([(cx - rad - g) * S, (cy - rad - g) * S, (cx + rad + g) * S, (cy + rad + g) * S], fill=255)
            dr.rectangle([(.17) * S, .42 * S, (.83) * S, (.55 + g) * S], fill=255)
        outer = Image.new("L", (S, S), 0); inner = Image.new("L", (S, S), 0)
        cloud(ImageDraw.Draw(outer), w / S / 2); cloud(ImageDraw.Draw(inner), -w / S / 2)
        ring = ImageChops.subtract(outer, inner)
        im.paste(Image.new("RGBA", (S, S), col), (0, 0), ring)
        line([(.14, .70), (.80, .70)])
        line([(.26, .85), (.90, .85)])
    return im.resize((size, size), Image.LANCZOS)
