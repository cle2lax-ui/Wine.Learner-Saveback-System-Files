# THREE WAYS — SERIES STYLE GUIDE (v1)

## Concept

A single-slide comparative format: one grape (or theme) shown through
three bottles side by side, each tied to a real region via a full-bleed
photo strip underneath. First deck: "The Three Faces of Zinfandel"
(Primitivo / Zinfandel / Tribidrag — three names for genetically
related grapes, three regions, three bottles).

One slide per deck. Not a swipeable carousel like GTR/Quick Sips/FFFA —
this is built to stand alone (a single Instagram post, not a carousel).

## System

Built entirely on the existing Field Guide module `showcase_shelf`
(`modules.py`, "M08"), not a new module. Three Ways is a *palette and
slot-recipe* on top of that shared module, plus a handful of new
`showcase_shelf` capabilities added specifically to make this deck
possible (see CHANGELOG_three_ways_v1.md for exactly what's new).

Canvas, fonts, QA harness: all shared with Field Guide/Quick Sips/GTR/
FFFA via `core.py` and `tokens.py`. Nothing series-specific at that
layer.

## Palette (the "Three Faces of Zinfandel" recipe — reuse or riff)

```python
pal = dict(DEFAULT_PALETTE)
pal["SIGNATURE"] = (183, 110, 121)  # dusty rose — kicker dot, producer line
pal["ACCENT"]    = (196, 158, 84)   # medium gold — wine-name line

slot = dict(
    bg_color=(0, 0, 0),                    # black page
    shelf_scrim_color=(245, 240, 232),     # off-white panel behind the text block
    mark_bg_color=(74, 20, 26),            # dark burgundy — top-left glass mark chip
    kicker_color=(255, 255, 255),          # white
    style_color=(0, 0, 0),                 # black — sits on the off-white scrim
    origin_color=(0, 0, 0),                # black
    note_color=(0, 0, 0),                  # black
    shelf_rule_color=(110, 90, 94),        # dim rose-gray hairline
    region_credit_color=(190, 185, 188),   # light gray, tiny print
)
```

This isn't locked the way GTR's gold or Quick Sips' garnet+gold are —
each Three Ways deck can run its own palette. What *is* the series
convention is the **structure**: black page, off-white scrim panel
for the reading copy, bottles reaching up out of the black into the
kicker row, region photos full-bleed at the bottom. Riff the colors
per deck; keep the structure.

## Anatomy (top to bottom)

1. **Top mark** — Quick Sips glass glyph + custom line (e.g. "Zinfandel
   3 Ways"), on a solid color patch, top-left. Optional; this deck uses
   it as the only "title" — there is no separate headline.
2. **Kicker** — small caps + dot, e.g. "ONE GRAPE, THREE NAMES."
3. **Headline** — optional. This deck's first build had one
   ("The Three Faces of Zinfandel:") and it was cut; the mark +
   kicker carry enough. Leave `slot["headline"]` unset/empty to skip
   it — the layout closes the gap automatically rather than leaving
   dead space.
4. **Three bottles**, lifted so their necks rise up into the kicker
   row (`bottle_lift`) for visual drama, sitting on a shared shelf
   line, each with: producer / wine name / style / origin / tasting
   note.
5. **Off-white scrim** spanning full width, from the shelf line down
   to the top of the region-photo strip — this is what makes black
   producer/name text and black body copy both legible in the same
   block without needing two different backgrounds.
6. **Region photo strip** — full-bleed, no gaps, one photo per
   bottle's home region, true canvas-edge-to-edge (uses
   `photo_stripe()`, same helper GTR's reveal photo uses). Bold
   caption per photo (e.g. "Puglia, Italy"), shrink-to-fit per
   caption so a long one (e.g. "Sonoma County, USA") doesn't collide
   with its neighbor.
7. **Tiny top-right credit line** — photo attributions, out of the
   footer entirely (this deck's footer only shows swipe/page-number
   furniture, both of which are usually turned off for a one-pager —
   see below).

## Slot reference (showcase_shelf, Three Ways-relevant keys)

All of these default to `showcase_shelf`'s original Field Guide
behavior when omitted — a plain deck that doesn't set any of them
renders exactly as before.

| Key | Purpose |
|---|---|
| `bg_color` | canvas fill (default PAPER) |
| `top_mark` | text for the glass-glyph mark patch, top-left |
| `mark_bg_color` | mark patch color (default `pal["SIGNATURE"]`) |
| `kicker_color`, `headline_color` | text color overrides (default INK / `pal["SIGNATURE"]`) |
| `headline` | omit/empty to skip the headline row entirely |
| `panel_gap` | vertical gap between kicker/headline and the product row (default 40) — raise this to push bottles + text down, e.g. to clear a lifted bottle top from the kicker |
| `bottle_lift` | extra px of bottle scale-height *only* — grows the bottle upward without moving the shelf line or anything below it. This is how a bottle neck reaches up behind the kicker row |
| `col_x_positions` | explicit list of left-edge x per column — overrides the default even-margin grid. **Use this whenever a region-photo strip sits below the products**, so text blocks align to something meaningful (the photo segments) instead of an unrelated margin grid — see "Column alignment" below |
| `col_w_override` | column width to pair with `col_x_positions` (the auto `col_w` assumes the default grid and can push the last column off-canvas otherwise) |
| `producer_color`, `name_color`, `style_color`, `origin_color`, `note_color`, `shelf_rule_color` | per-element text/rule color overrides |
| `shelf_scrim_color` | full-width panel from the shelf line down to the region-photo band (or page bottom if there's no photo strip) |
| `region_photos` | list of `(photo_filename, caption)` tuples, one per column — full-bleed strip at the bottom |
| `region_band_frac` | fraction of page height the photo strip occupies (default 0.25 — "bottom quartile") |
| `region_caption_font`, `region_caption_size` | caption typography (default `caption_italic` at `TYPE["caption"]`=60; this deck uses `italbold` at 72) |
| `region_credit`, `region_credit_color` | tiny top-right attribution line, separate from the footer |
| `footer_label` | `""` suppresses the swipe cue (this is a one-pager, nothing to swipe to) |
| `show_page_num` | `False` suppresses the page-number too |

## Column alignment — read this before adding a photo strip

`showcase_shelf`'s default column grid (`M + i*(col_w+gap)`) and a
`region_photos` strip's grid (`W // n`, true edge-to-edge) are **two
different grids**. If you don't set `col_x_positions`, the text blocks
will *not* line up with their photos below — column 0 might sit 120px
in from its photo's left edge, column 1 only 54px, column 2 could even
start slightly *before* its photo's left edge. This isn't a hypothetical:
it happened on the first build of this deck and had to be fixed.

**Do this instead:** decide a single left-margin offset (this deck uses
60px), then compute:

```python
n = len(products)          # must equal cols
seg = W // n                # exact for W=2160, n=3 → 720
col_x_positions = [i * seg + offset for i in range(n)]
col_w_override = seg - offset - right_margin   # e.g. 720-60-60=600
```

This guarantees every text block sits the same distance from its
photo's left edge *and* stays evenly spaced (both fall out of the same
math, they don't need separate tuning). Leave headroom on the last
column — `col_w_override` needs to fit inside `seg` minus your chosen
offset and a right margin, or the QA harness's off-canvas check will
catch it (it did, the first time).

## Bottle photos

Same discipline as Quick Sips' benchmark bottles:

- White/near-white studio background, `core.remove_background()`.
- **Check `hole_frac`.** A near-white label element (foil, printed
  highlight) can punch tiny holes through the label at the default
  `white_threshold=715` — this happened on this deck's first bottle.
  Raise the threshold (try 730–750) until `hole_frac` reads 0, then
  visually confirm the label is intact, not just that the number is
  zero.
- **Check the corners, not just the count.** A `hole_frac` near zero
  can still hide a real problem: a bottle photographed at a slight
  tilt can leave an isolated pocket of unremoved background in a
  corner that the flood-fill never reached (broken 4-connectivity from
  a dark edge cutting it off from the main background region). This
  is invisible against a paper-colored page and only became visible
  when this deck's background changed to black. **Composite every
  cutout onto a bright, unrealistic color (green, not white or the
  deck's actual background) before trusting it** — that's how this
  was actually caught, not by reasoning about connectivity in the
  abstract.
- If a real photo's lighting reads as a color-temperature mismatch
  next to the others (e.g. one bottle's glass reflection is
  distinctly cooler/warmer than the rest), a mild per-channel
  correction is fair game — document that it's an edit, don't pass it
  off as unretouched, and keep the original around in case a better
  source photo arrives (one did, on this deck, and made the
  correction moot).

## QA notes specific to this module

- `showcase_shelf` registers a `qa.box` per product (`prod{i}`) and one
  for the region-photo band (`!region_photos`, exempted from the
  content-bottom check since full bleed to the page edge is the
  point). These **do** collide-check against each other — a caption
  or note that runs long enough to physically overlap the photo band
  will fail the harness, not just look bad. Trim the copy or adjust
  `region_band_frac` / `panel_gap` rather than reaching for a "!"
  exemption; the collision is real.
- The kicker/headline redraw-on-top trick (see CHANGELOG) only fires
  when `bottle_lift > 0`. If you use `bottle_lift` without intending
  the neck to visually cross into the kicker row, use `panel_gap` to
  push the whole product row down until it clears — check actual box
  coordinates (`bottle top = panel_top - bottle_lift`) rather than
  eyeballing it in a screenshot; it's cheap to compute and the margin
  matters more than it looks like it does at this zoom level.
