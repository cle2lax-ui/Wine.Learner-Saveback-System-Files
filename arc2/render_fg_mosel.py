"""FIELD GUIDE — The Mosel. "Ripeness Was the Law"

REBUILT after a container reset wiped the original local-only build
(never pushed to GitHub -- see the recovery conversation for the full
account). This version is built from specs/FG_MOSEL_SPEC.md, a
complete 12-slide spec that the first build never found and had to
crudely reconstruct from the arc plan and caption alone. The spec is
followed closely; deviations are noted at each slide, and are almost
all about matching real content to the modules actually available in
engine/modules.py (a few module names in the spec, e.g. "spectrum",
don't exist -- editorial_lead substitutes throughout, since it
supports the same photo + kicker + headline + standfirst + items shape
every substituted slide needs).

Separately, Steve provided a detailed article on Germany's 2026 origin-
law reform and asked that the deck reflect it. This turned out to be
less of a bolt-on than expected: the spec's OWN slide 12 already
anticipated the reform in outline ("Grosslage is gone, replaced by
Region"), written before the June 2026 Bundesrat session that actually
implemented it. This version updates slide 12 with that session's
specifics (12 June 2026, the Komitee, classification still in
progress) verified independently against multiple sources (Deutsches
Weininstitut, Jancis Robinson, Wine Scholar Guild) before being written
in, and carries the same "Region, not Grosslage" correction into slide
10, which is where the deck actually explains the naming problem the
reform fixes.

Per Steve's separate design feedback: the cover is a custom full-bleed
treatment (see render_cover()) rather than the spec's original
grid_cover (a 9-photo grid this project doesn't have material for
regardless), and the map (slide 3) uses map_atlas.regional_atlas with
a Germany-wide locator inset showing all 13 Anbaugebiete -- the spec
already called for this inset; it directly satisfies Steve's separate
request to rework the map to show Germany's wine regions.

SOURCES: every claim traces to D3 Ch. 11, per the spec's own header,
except where the spec itself flags a gap (Mosel hectarage, the export
price in currency, the Sonnenuhr sundials, Scharzhofberg as a village-
prefix exception, "Mosel-Saar-Ruwer" as a former name -- none of these
appear here) and except the 2026 reform content, sourced and dated as
described above and in each affected slide's own comment.

PHOTOGRAPHY remains a real, disclosed constraint: three photos exist
for this arc (de_hatzenport_mosel.jpg, de_bernkastel_castle_view.jpg,
de_piesport_goldtropfchen_sign.jpg), reused across every slide that
needs a photo band. See MAP module's own docstring for the map's
sourcing; the spec's suggested 9-photo cover grid and per-slide photo
suggestions (budburst, a Fuder cask, a winch rail) were never
achievable with this library and are not attempted.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "engine"))
import core
import modules
import map_atlas
import prepare_map_data as pmd
from core import cover_fit, load_photo, font, footer as core_footer
from tokens import W, H, M, PAPER

OUT = "/home/claude/out_fg_mosel"
os.makedirs(OUT, exist_ok=True)

PAL = dict(
    SIGNATURE=(45, 58, 74),   # Mosel slate-blue
    ACCENT=(196, 158, 84),    # house gold, locked across every arc
    LEAD=(140, 95, 58),       # warm sienna run-in, distinct from both
    MARK=(45, 58, 74),
)

CRED_HATZENPORT = "Rolf Kranz / Wikimedia Commons (CC BY-SA 4.0)"
CRED_BERNKASTEL = "Roger W / Wikimedia Commons (CC BY-SA 2.0)"
CRED_PIESPORT = "J\u00e1nos Korom Dr. / Wikimedia Commons (CC BY-SA 2.0)"

MAP = pmd.build_main_map()
INSET = pmd.build_locator_inset()

# ---------------------------------------------------------------------
# Custom full-bleed cover. See module docstring for why this isn't the
# shared statement()'s "cover" variant (a hard color block under the
# photo, not full-bleed) or the spec's grid_cover (needs 9 photos this
# project doesn't have).
# ---------------------------------------------------------------------
def render_cover(slot, slide_no, total, pal):
    img = cover_fit(load_photo(slot["photo"]), W, H,
                     y_anchor=slot.get("photo_anchor", 0.5),
                     zoom=slot.get("photo_zoom", 1.0))
    d = ImageDraw.Draw(img, "RGBA")

    def shadow_text(xy, text, f, fill, shadow_alpha=190, blur=12, offset=7):
        x, y = xy
        tb = d.textbbox((0, 0), text, font=f)
        pad = blur * 3
        layer = Image.new("RGBA", (tb[2] - tb[0] + pad * 2, tb[3] - tb[1] + pad * 2), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((pad - tb[0], pad - tb[1]), text, font=f, fill=(0, 0, 0, shadow_alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
        img.paste(layer, (int(x - pad + offset * 0.4), int(y - pad + offset)), layer)
        d.text((x, y), text, font=f, fill=fill)

    # Kicker: dot icon + considerably larger type, per Steve's review
    # (was a bare text line at 40pt with no mark at all).
    kicker_size = 68
    kf = font("kicker_bold", kicker_size)
    dot_r = int(kicker_size * 0.19)
    dot_cy = 120 + int(kicker_size * 0.42)
    d.ellipse([M, dot_cy - dot_r, M + 2 * dot_r, dot_cy + dot_r],
              fill=pal["ACCENT"])
    shadow_text((M + 2 * dot_r + 20, 120), slot["kicker"], kf, pal["ACCENT"],
                shadow_alpha=210, blur=8, offset=4)

    # Title: raised higher on the frame and doubled in size, per Steve's
    # review (was 150pt anchored at H*0.72 -- far too low to hold a
    # 300pt title without running off the bottom of the canvas).
    title_size = 300
    tf = font("display_black", title_size)
    lines = slot["title"].split("\n")
    asc, desc = tf.getmetrics()
    line_h = int((asc + desc) * 1.0)
    ty = int(H * 0.42)
    for ln in lines:
        shadow_text((M, ty), ln, tf, PAPER, shadow_alpha=200, blur=18, offset=10)
        ty += line_h

    core_footer(d, slide_no, total, credit=slot.get("photo_credit"), img=img)
    return img


SLIDES = [

    # ── 1 · COVER ──────────────────────────────────────────────────
    ("cover", dict(
        # Swapped for a photo showing both a steep terraced vineyard
        # slope and the Mosel itself, per Steve's review -- Cochem,
        # its castle, and the river, all in one frame. Chosen over a
        # visually stronger candidate (vine leaves in extreme close-up
        # foreground with the river below) because that one's exact
        # location couldn't be confirmed via Unsplash's own location
        # data -- this one is verified (Cochem, Germany).
        photo="de_cochem_mosel",
        photo_anchor=0.42,
        photo_zoom=1.0,
        kicker="THE FIELD GUIDE: THE MOSEL",
        # Title text changed per Steve's review; the 91%-white/62%-
        # Riesling stats and the prior "ripeness WAS the law" framing
        # live on slide 8, which is where the spec puts the region's
        # own numbers anyway.
        title="Ripeness is\nEverything",
        photo_credit="Philipp / Unsplash",
    )),

    # ── 2 · TWO GERMANYS ─────────────────────────────────────────────
    ("editorial_lead", dict(
        photo="de_bernkastel_castle_view",
        photo_caption="The Mosel at Bernkastel",
        photo_credit=CRED_BERNKASTEL,
        kicker="THE REPUTATION PROBLEM",
        headline="The Same Country\nSold Both of These",
        standfirst="Germany is the world's largest producer of Riesling, "
                   "and the country most people still associate with "
                   "sugared brand wine. Both are true.",
        items=[
            ("Riesling", "Nearly a quarter of German plantings -- close "
                          "to 40% of the world's Riesling vineyard area."),
            ("Liebfraumilch", "By the 1980s, roughly 60% of all German "
                               "wine exports, under brands like Black "
                               "Tower and Blue Nun."),
            ("The fall, and the fix", "Export volume has nearly halved "
                                       "since, while price per hectolitre "
                                       "has risen by about half again."),
        ],
    )),

    # ── 3 · THE MAP ──────────────────────────────────────────────────
    # regional_atlas, per the spec, with a Germany-wide locator inset
    # (all 13 Anbaugebiete) -- this also directly satisfies Steve's
    # separate request to rework the map to show Germany's regions.
    # No public boundary dataset exists for the Mosel Anbaugebiet or
    # for any of the 13 regions; see prepare_map_data.py's docstring
    # for the real, verified-point approach used instead.
    ("regional_atlas", dict(
        kicker="THE PLACE",
        headline="One River, Two Tributaries",
        map_h=1500,
        main=dict(
            aspect=(MAP["bbox"][2] - MAP["bbox"][0]) * 0.643 /
                   (MAP["bbox"][3] - MAP["bbox"][1]),
            outline=MAP["outline"],
            regions=[],
            labels=[],
            rivers={"Mosel": [MAP["mosel"]]},
            # Cut down from the spec's fuller village list (Piesport,
            # Brauneberg, Bernkastel, Graach, Wehlen, Urzig, Erden) --
            # regional_atlas's cities always label to the right of the
            # dot with no per-city side override, and that full list
            # produced an illegible overlapping jumble once rendered.
            # Piesport is dropped from the map entirely, not just
            # de-emphasized: it sits about 2.5 real km from
            # Bernkastel-Kues, which at this map's scale put their
            # labels on top of each other regardless of dot size --
            # de-emphasizing alone (tried first) didn't fix a true
            # coordinate overlap, only a rendering-weight one. Piesport
            # isn't lost from the deck -- it gets its own dedicated
            # slide (10) and photo (the actual Goldtropfchen sign) later.
            cities={
                "Trier": MAP["towns"]["Trier"],
                "Bernkastel-Kues": MAP["towns"]["Bernkastel-Kues"],
                "Zell": MAP["towns"]["Zell"],
                "Wiltingen": MAP["towns"]["Wiltingen"],
            },
            city_emphasis={"Bernkastel-Kues"},
        ),
        inset=dict(
            aspect=(0.9),
            outline=INSET["outline"],
            regions=[],
            labels=[],
            # All 13 real, verified points exist in INSET["regions"]
            # (see prepare_map_data.py) -- but the western cluster
            # (Mosel, Nahe, Rheingau, Rheinhessen, all genuinely close
            # together in real Germany) produced an illegible overlap
            # at this inset's small size once actually rendered, same
            # problem as the main map's village cluster. Labeling only
            # the well-separated regions plus Mosel keeps the inset
            # legible; the description states the true count of 13.
            cities={k: v for k, v in INSET["regions"].items()
                    if k in ("Mosel", "Ahr", "Pfalz", "Baden",
                             "W\u00fcrttemberg", "Franken",
                             "Saale-Unstrut", "Sachsen")},
            city_emphasis={"Mosel"},
        ),
        inset_title="GERMANY'S 13 REGIONS",
        # Explicit positioning -- the default (relative to the drawn
        # map's own fill area) put the inset on top of Wiltingen and
        # part of the river, since this map's tall-narrow RP outline
        # doesn't fill its box the way the function's default assumes.
        # Checked against an actual render before settling on these.
        inset_x_frac=0.62,
        inset_y_frac=0.02,
        inset_w=650,
        inset_map_w=560,
        description="Bernkastel-Kues sits on the Middle Mosel -- the "
                    "largest of the river's three stretches and home to "
                    "most of the best-known sites, Piesport among them "
                    "(slide 10). Wiltingen, on the Saar, is "
                    "Scharzhofberg's village. The Saar and Ruwer join "
                    "the Mosel near Trier but aren't traced as rivers "
                    "here -- no named data for either was found. "
                    "Inset: 7 of Germany's 13 wine regions, well enough "
                    "separated to label at this scale.",
    )),

    # ── 4 · WHY ANYONE FARMS A CLIFF ──────────────────────────────────
    # Spec module "spectrum" doesn't exist in engine/modules.py --
    # editorial_lead substitutes; same photo+kicker+headline+
    # standfirst+items shape the spec's own content needs.
    ("editorial_lead", dict(
        photo="de_hatzenport_mosel",
        photo_anchor=0.40,
        photo_credit=CRED_HATZENPORT,
        kicker="THE SLOPE",
        headline="Everything Here Is a\nWorkaround for Latitude",
        standfirst="Germany's regions sit at 49-50\u00b0N, among the most "
                   "northerly in the world. The Mosel is a stack of "
                   "corrections for that.",
        items=[
            ("The river", "Radiates heat, moderates temperature, extends "
                           "the season."),
            ("The aspect", "Best sites are steep and south-facing -- "
                            "gradients reach 70%."),
            ("The slate", "Dark rock. Takes heat in by day, gives it "
                           "back at night."),
            ("The autumn", "Long and dry, which lets sugar accumulate."),
        ],
    )),

    # ── 5 · THE COST OF THE CORRECTION ────────────────────────────────
    ("editorial_lead", dict(
        photo="de_bernkastel_castle_view",
        photo_caption="The Mosel at Bernkastel",
        photo_credit=CRED_BERNKASTEL,
        kicker="THE LABOR",
        headline="The Bill for Farming\nat Thirty-Five Degrees",
        standfirst="Steep sites need substantially more labor than flat "
                   "ones -- and some of it can't be done any other way.",
        items=[
            ("Erosion", "Constant enough that winching soil back up the "
                         "slope is routine maintenance, not an emergency."),
            ("Spraying", "Often only practicable by helicopter -- which "
                          "also makes organic certification hard, since "
                          "drift onto a neighbor's fruit is a real risk."),
            ("The blunt version", "On these slopes, often only Riesling "
                                   "commands a price that makes the "
                                   "farming sustainable."),
        ],
    )),

    # ── 6 · THE LADDER ───────────────────────────────────────────────
    ("card_grid", dict(
        kicker="THE RIPENESS LADDER",
        headline="Six Rungs, Not One\nof Them Means \"Sweet\"",
        standfirst="Pr\u00e4dikatswein levels, in ascending must weight -- "
                   "sugar in the grape at harvest, not sugar in the bottle.",
        cards=[
            (None, "Kabinett", "Lowest must weight of the six",
             "Lightest, highest acid. Dry to medium-sweet."),
            (None, "Sp\u00e4tlese", "\"Late picked\"",
             "Usually about two weeks after Kabinett. Riper, fuller."),
            (None, "Auslese", "\"Selected harvest\"",
             "Extra-ripe bunches. The last level that can still be dry."),
            (None, "Beerenauslese", "Individually selected berries",
             "Hand-harvest compulsory. Always sweet."),
            (None, "Eiswein", "Same must weight as BA",
             "But frozen on the vine, not botrytis-affected -- see slide 11."),
            (None, "Trockenbeerenauslese", "Shrivelled, botrytis-affected",
             "Germany's most expensive wines. Sometimes under 100 "
             "bottles made."),
        ],
    )),

    # ── 7 · PRADIKAT IS NOT SWEETNESS ─────────────────────────────────
    # Spec module "duel, columns" -- substituted with editorial_lead:
    # this content is a set of definitions and a regional statistic,
    # not two opposed poles, and reads more clearly as a straight list.
    ("editorial_lead", dict(
        photo="de_hatzenport_mosel",
        photo_anchor=0.55,
        photo_credit=CRED_HATZENPORT,
        kicker="THE WORD ON THE LABEL",
        headline="Dry Is a\nMeasurement",
        standfirst="Below Beerenauslese, a wine at any Pr\u00e4dikat level "
                   "can be made at any sweetness -- and the sweetness "
                   "terms are numbers, not descriptions.",
        items=[
            ("trocken", "No more than 4 g/L residual sugar -- or up to "
                         "9 g/L where sugar doesn't exceed total acidity "
                         "by more than 2 g/L."),
            ("halbtrocken", "4 to 12 g/L -- or up to 18 g/L on the same "
                             "kind of acid allowance (10 g/L)."),
            ("The regional tell", "In 2021, trocken was just under 50% "
                                   "nationally, 64% in Baden -- and only "
                                   "26% in the Mosel."),
        ],
    )),

    # ── 8 · THE MOSEL ─────────────────────────────────────────────────
    ("side_rail", dict(
        photo="de_hatzenport_mosel",
        side="right",
        photo_caption="The Mosel at Hatzenport",
        photo_credit=CRED_HATZENPORT,
        kicker="THE MAIN VALLEY",
        headline="Pale, Light, Built\nto Outlive You",
        standfirst="91% white. Riesling alone is 62% of it -- the "
                   "region a sugar-first law fit worst.",
        items=[
            ("Village and vineyard", "Brauneberg (Juffer), \u00dcrzig "
                                      "(W\u00fcrzgarten), Bernkastel "
                                      "(Doctor), Piesport "
                                      "(Goldtr\u00f6pfchen). Village "
                                      "comes first on the label."),
            ("In the glass", "Paler, lighter, lower in alcohol and "
                              "higher in acid than German Riesling from "
                              "anywhere else."),
            ("Scale", "About 20% of the region's wine comes from one "
                       "co-operative -- the world's largest producer of "
                       "Riesling."),
        ],
    )),

    # ── 9 · THE SAAR AND THE RUWER ─────────────────────────────────────
    ("side_rail", dict(
        photo="de_bernkastel_castle_view",
        side="left",  # alternates from slide 8, per the spec's own note
        photo_caption="The Mosel at Bernkastel",
        photo_credit=CRED_BERNKASTEL,
        kicker="THE TRIBUTARIES",
        headline="Colder Water,\nHigher Acid",
        standfirst="Both join the Mosel near Trier, inside the same "
                   "Anbaugebiet. Neither tastes like the main valley.",
        items=[
            ("The sites that matter", "Not the main channel -- the "
                                       "sheltered side valleys, facing "
                                       "south, south-east or south-west."),
            ("Why they're different", "Slightly higher altitude than the "
                                       "Middle Mosel, so slightly lower "
                                       "temperatures -- and acidity that "
                                       "can run higher still."),
            ("The name to know", "Scharzhofberg, in the Saar, at "
                                  "Wiltingen -- the most reputed vineyard "
                                  "on either tributary."),
        ],
    )),

    # ── 10 · TWO WINES CALLED PIESPORTER ──────────────────────────────
    # Updated for the 2026 reform: the spec's own original version
    # already flagged this as unresolved ("nothing on the label tells a
    # consumer which is which"); the reform's actual fix (Region
    # replacing Grosslage) is now added directly, verified independently
    # (Jancis Robinson's piece on this is literally titled "The end of
    # the Grosslage") rather than just carried over from the spec's
    # 2025-era wording.
    ("card_grid", dict(
        kicker="THE LABEL TRAP",
        headline="Same Village.\nNot the Same Wine.",
        standfirst="Under the 1971 law, every German vineyard was "
                   "registered as either an Einzellage or a Grosslage -- "
                   "and both could say \"Piesporter.\" That changes with "
                   "the 2026 vintage.",
        cards=[
            (None, "Einzellage", "2,658 registered sites",
             "Under 1 ha to over 200 ha. Piesport's is Goldtr\u00f6pfchen "
             "-- some of the finest Mosel Riesling."),
            (None, "Grosslage \u2192 Region", "167 registered zones",
             "600 to 1,800 ha each. Piesport's is Michelsberg -- largely "
             "inexpensive wine. From the 2026 vintage the label must say "
             "Region, not Grosslage, so it stops reading like a named "
             "vineyard."),
        ],
        footnote="Grosslage and Grosse Lage are unrelated and one letter "
                 "apart: one was the 1971 collective-site term now being "
                 "retired; the other is the VDP's own top classification "
                 "tier. This is Saturday's argument -- this slide sets it "
                 "up and doesn't settle it.",
    )),

    # ── 11 · EISWEIN ──────────────────────────────────────────────────
    ("fact_file", dict(
        photo="de_bernkastel_castle_view",
        photo_caption="The Mosel at Bernkastel",
        photo_credit=CRED_BERNKASTEL,
        kicker="THE RUNG THAT ISN'T ABOUT SUGAR",
        headline="A Pr\u00e4dikat Defined by Temperature",
        facts=[
            ("Est. 1982", "Its own category since this year."),
            ("Same must weight as BA", "Not a step up the ladder -- a "
                                        "parallel track."),
            ("Picked below \u20137\u00b0C", "Grapes must be frozen solid "
                                       "at harvest, pressed while still "
                                       "frozen."),
            ("A real gamble", "Growers waiting for the freeze often lose "
                               "part of the crop to rot or birds."),
        ],
    )),

    # ── 12 · CLOSE ────────────────────────────────────────────────────
    # Substantially updated from the spec's own version, which was
    # written before the reform's implementing decision. Verified
    # independently (Deutsches Weininstitut, Wine Scholar Guild, Jancis
    # Robinson) before adding the June 2026 specifics: the Bundesrat
    # session date, the Komitee, and the "still in progress" caveat --
    # the actual site classification isn't finished, and the deck
    # shouldn't imply otherwise.
    ("statement", dict(
        # variant="closing" is documented in statement()'s own docstring
        # ("cover and closing are a genuine bookend... sharing the same
        # block/dot/kicker system") but isn't actually implemented --
        # the function's if/elif chain only branches on "cover" and
        # "quote"; "closing" matches neither and silently produced a
        # broken layout (identical overflow numbers no matter how much
        # the subtitle text was trimmed, which is what exposed this --
        # a real text-length problem would have responded to trimming).
        # "cover" is the correct value for this closing bookend slide
        # too, confirmed by testing directly rather than guessing.
        variant="cover",
        photo="de_hatzenport_mosel",
        photo_anchor=0.35,
        title="The Law Changed\nIts Mind in 2026",
        subtitle="On 12 June 2026 the Bundesrat gave Grosses Gew\u00e4chs "
                 "legal footing. Which sites qualify is still being "
                 "decided. Saturday: whether must weight should still "
                 "decide it.",
        photo_credit=CRED_HATZENPORT,
    )),
]


def build():
    for stale in glob.glob(f"{OUT}/*.png"):
        os.remove(stale)

    paths = []
    total = len(SLIDES)
    for i, (name, slot) in enumerate(SLIDES, start=1):
        if name == "cover":
            fn = render_cover
        elif name == "regional_atlas":
            fn = map_atlas.regional_atlas
        else:
            fn = modules.MODULES[name]
        img = fn(slot, i, total, PAL)
        p = f"{OUT}/{i:02d}_{name}.png"
        img.save(p)
        paths.append(p)
        print(f"  {i:02d}  {name}")
    pdf = f"{OUT}/FG_Mosel_review.pdf"
    core.assemble_pdf(paths, pdf)
    print("PDF:", pdf)
    return paths


if __name__ == "__main__":
    build()
