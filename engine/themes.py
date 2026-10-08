"""Deck themes in the Reel's visual language (v11).

Steve's direction: decks evolve toward the Germany Reel's style, themed with the national flag of
the country featured, or the series' own burgundy or forest green for general topics. A theme is a
small set of roles, not a free palette; every role pairing that carries text is contrast-checked by
check_theme(), so a flag's own colors are used where they work and LIFTED (lightened) where the
raw flag color would fail on a dark ground.

ROLES
  ground     the dark page (the Reel's black, tinted toward the theme)
  ground_alt a second dark tone for panels
  text       primary type on ground
  muted      secondary type on ground
  hero       the highlight color for the one big number or key word (the Reel's gold)
  chip       fill of the series chip (FIELD GUIDE, ...); chip_ink is its text
  bands      the three flag-band colors, in flag order, for dividers and graphic motifs
  map_fill   a highlighted region on a map; map_line the other boundaries
  paper/ink  the light "paper" scene (bottles, products) and its type

SOURCES of the base colors. USA: Old Glory red (178, 34, 52) and Old Glory blue (60, 59, 110), the
colors usually given for the flag. Germany: black, red (221, 0, 0), gold (255, 206, 0), as in the
Germany Reel and FFFA. Burgundy (104, 26, 38): the deep oxblood of the Cote de Nuits Field Guide.
Forest green (21, 63, 40): the Saint-Peray Quick Sips. Gold (196, 158, 84): the series' ACCENT.
"""


def _lum(c):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


PAPER = (250, 246, 238)
INK = (28, 24, 26)

THEMES = {
    "usa": dict(
        name="United States (flag)",
        ground=(10, 12, 24), ground_alt=(20, 24, 46),
        text=(255, 255, 255), muted=(178, 184, 206),
        # Old Glory red is ~2.9:1 on this ground: under the 3:1 floor for large type. Lifted for the
        # hero role only; the raw flag red stays in the chip and the bands, where it is a fill.
        hero=(236, 82, 96),
        chip=(178, 34, 52), chip_ink=(255, 255, 255),
        bands=((178, 34, 52), (240, 240, 242), (60, 59, 110)),
        # Old Glory blue is near-invisible as a line on a dark ground; maps use a lifted blue.
        map_fill=(178, 34, 52), map_line=(138, 146, 206),
        paper=PAPER, ink=INK,
    ),
    "germany": dict(
        name="Germany (flag)",
        ground=(9, 9, 11), ground_alt=(28, 28, 33),
        text=(255, 255, 255), muted=(180, 180, 186),
        hero=(255, 206, 0),
        chip=(221, 0, 0), chip_ink=(255, 255, 255),
        bands=((34, 34, 40), (221, 0, 0), (255, 206, 0)),     # black lifted to charcoal to show on black
        map_fill=(221, 0, 0), map_line=(150, 150, 158),
        paper=PAPER, ink=INK,
    ),
    "burgundy": dict(
        name="Burgundy (series, general topics)",
        ground=(16, 8, 11), ground_alt=(40, 16, 24),
        text=(255, 255, 255), muted=(196, 178, 182),
        hero=(214, 178, 104),                                  # the series gold, lifted slightly
        # raw burgundy is a fill on paper and a band; as a chip on the dark ground it needs lifting
        chip=(150, 36, 56), chip_ink=(255, 255, 255),
        bands=((104, 26, 38), (196, 158, 84), (240, 232, 214)),
        map_fill=(150, 36, 56), map_line=(170, 150, 120),
        paper=PAPER, ink=INK,
    ),
    "forest": dict(
        name="Forest green (series, general topics)",
        ground=(8, 14, 11), ground_alt=(18, 36, 26),
        text=(255, 255, 255), muted=(176, 196, 184),
        hero=(214, 178, 104),
        chip=(36, 110, 70), chip_ink=(255, 255, 255),
        bands=((21, 63, 40), (196, 158, 84), (240, 232, 214)),
        map_fill=(36, 110, 70), map_line=(150, 170, 140),
        paper=PAPER, ink=INK,
    ),
}


def theme(name):
    return dict(THEMES[name])


def check_theme(name, verbose=True):
    """Contrast checks for every role pairing that carries text or must be seen. Floors: body text
    4.5:1, large display type 3:1, a filled shape against the ground 1.5:1. Returns the failures."""
    t = THEMES[name]
    checks = [
        ("text on ground (body, 4.5)", contrast(t["text"], t["ground"]), 4.5),
        ("muted on ground (body, 4.5)", contrast(t["muted"], t["ground"]), 4.5),
        ("hero on ground (display, 3.0)", contrast(t["hero"], t["ground"]), 3.0),
        ("chip ink on chip (body, 4.5)", contrast(t["chip_ink"], t["chip"]), 4.5),
        ("chip against ground (shape, 1.5)", contrast(t["chip"], t["ground"]), 1.5),
        ("map line on ground (shape, 3.0)", contrast(t["map_line"], t["ground"]), 3.0),
        ("map fill against ground (shape, 1.5)", contrast(t["map_fill"], t["ground"]), 1.5),
        ("ink on paper (body, 4.5)", contrast(t["ink"], t["paper"]), 4.5),
    ]
    fails = [c for c in checks if c[1] < c[2]]
    if verbose:
        print(f"{t['name']}:")
        for label, v, floor in checks:
            print(f"   {'PASS' if v >= floor else 'FAIL'}  {label:38s} {v:5.2f}:1")
    return fails


if __name__ == "__main__":
    bad = []
    for n in THEMES:
        bad += check_theme(n)
    raw = contrast((178, 34, 52), THEMES["usa"]["ground"])
    print(f"\n(for the record: raw Old Glory red on the USA ground is {raw:.2f}:1, which is why the hero is lifted)")
    print("ALL THEMES PASS" if not bad else f"{len(bad)} FAILURES")
