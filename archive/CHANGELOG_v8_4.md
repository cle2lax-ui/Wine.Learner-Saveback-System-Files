# CHANGELOG v8.4 — Field Guide "How Did All These Flavors Get Into
My Wine?" (aroma chemistry deck), two new modules, and five real bugs
found and fixed in shared modules while building it.

Locked and delivered this session: a 12-slide Field Guide on wine
aroma/flavor chemistry (`render_fg_aroma_chemistry.py`). Building it
surfaced a genuine module-level bug on almost every slide type it
touched — this changelog is organized by module, not by slide, since
every fix here is reusable by future decks, not just this one.

### `mosaic()`
- **Hero caption backing changed from `scrim()` to `chip()`.** `scrim()`
  is a gradient that fades to nothing at its far edge — fine when the
  photo underneath happens to be dark everywhere the fade needed
  coverage, but broke outright the moment part of that zone was bright
  (a photo with a white tabletop in the caption area left the white
  caption text sitting on the weak end of the fade, unreadable). This
  was working fine for every prior mosaic-hero photo purely by luck —
  they all happened to be dark in that specific zone. `chip()` is
  flat and uniform-opacity, so it's correct regardless of what's
  underneath, not just for photos that happen to suit a gradient.
  Caption font also bumped up (`TYPE["caption"] + 10`) for legibility.

## modules.py changes

### New module: `grid_cover()`
3×3 full-bleed studio-photo grid cover with the standard "color blade"
kicker/title/subtitle block below it, for decks that want an
ingredient-grid cover instead of a single hero photo. Kicker mark
lives as an on-photo overlay (luminance-adaptive, same discipline as
every other on-photo text in the system) rather than in the block,
freeing the block for a larger title. Subtitle renders as its own
solid chip directly under the kicker, sized to the width of the first
two grid tiles, with its own auto-shrink-to-fit sizing. Square cells
are enforced (grid height is derived from tile width × 3, not from an
input fraction) — letterboxed rectangular tiles were the very first
version and looked wrong immediately.

### New module: `horizontal_trio()`
Three full-width horizontal photo bands stacked vertically, with
title+body overlaid on the left of each band. Built specifically
because two three-item slides back to back (both using
`feature_trio`'s vertical-column layout) read as the same slide.
Overlay legibility is a **guaranteed scrim**, not a luminance-average
branch — an earlier version chose ink-vs-paper text color from one
average luminance reading over the whole text zone, which read as
"bright enough" even when part of that zone was a black background
corner, leaving dark text invisible wherever it landed on the dark
patch (caught on a vanilla-orchid photo: white flower averaged
bright, but the top-left corner behind the kicker was pure black).
Always scrimming costs a little visual weight but is never wrong,
which a coarse average can be.

### `feature_trio()`
- **Per-column titles now support a letter-label hanging indent.**
  `"C. Creamier Texture"` used to wrap as `"C. Creamier" / "Texture"`
  (second line flush left under the "C."); now detects a leading
  `"X. "` label via regex, draws it once at the column's left edge,
  and wraps the remaining words with every line — first included —
  starting at the same x, aligned with the first word rather than the
  label.
- **Column headers now bottom-align across the row.** Wraps every
  header first, finds the tallest (most-wrapped) one, then draws each
  header so its *last* line lands on the same row — the underline and
  body text start at the same y in every column regardless of whether
  one header wrapped to 2 lines and its neighbors didn't. Previously
  each column's underline sat directly under its own header with no
  regard for the others.
- **Per-photo `zoom` override.** 4th optional element in a feature
  tuple: `(title, body, photo, zoom)`. Investigated as a fix for a
  photo needing to show more context in a narrow column; documented
  here because the investigation matters even though the fix itself
  wasn't the right lever for that specific case — see "Things tried
  and reverted" below.

### `card_grid()`
- **`top_margin=` param** (default 170, matches `kicker_block`'s own
  default) lets a deck pull the kicker/headline/standfirst block up
  toward the canvas top, reclaiming vertical room for a bottom photo
  stripe instead of crowding the footer.
- **Bottom photo stripe now stops short of the footer row** (`bottom
  = FOOTER_Y - 30`) instead of running to the canvas edge. Photos sit
  fully above the footer; the footer renders on plain paper beneath
  them instead of needing a scrim on top of a photo. This replaces an
  earlier fix (two turns prior) that gave the stripe caption its own
  scrim reaching down to the footer — which worked for the caption,
  but the caption's scrim and the footer's own adaptive scrim ended up
  as two independently-darkened rectangles abutting at slightly
  different opacities, visible as a seam/crease line at the boundary.
  The real fix was giving the photos and the footer their own
  separate territory, not tuning the two scrims to match.

### `duel()`
- **`photo_position=` param** (`"top"` default, `"bottom"` new).
  `"bottom"` renders kicker/headline/standfirst/content first, then
  the split photo band at the bottom instead of the top. The bottom
  band's vertical position is **derived from where the actual content
  ends** (`content_bottom + 70`), clamped to never run past the
  footer-safe max — not anchored to the footer by a fixed offset, which
  left a large dead gap between short content and the photos.
- **Column headers now wrap.** Previously assumed every header fit on
  one line and drew it unwrapped — a longer header (`"Tannins &
  Pigments Polymerize"`) ran straight off the edge of its column and
  into the neighbor's. Same wrap-then-bottom-align fix as
  `feature_trio`'s headers, applied here too.

### `process_map()`
- **Legend removed entirely** (diamond/rectangle key below the flow).
  Not needed per direct feedback; the vertical space it used is
  reclaimed for a taller flow instead of stopping ~260px short of
  `CONTENT_BOTTOM`.
- **Boxes and type sizes substantially increased** (rect_h 150→320,
  node_f 42→64, title_f 52→68, badge_f FLOOR→68) across several
  rounds of "bigger" direction.
- **Sequential number badges moved to float above each box's top-left
  corner**, entirely outside the box, instead of inset inside the
  corner. Two real collisions got fixed in sequence getting here:
  first the badge was inset and the *bigger* font made text run into
  it (badge sitting on top of the first letter of text); moving the
  badge to straddle the box's top edge fixed that but then collided
  with the column titles above; the working fix floats the badge fully
  above the box with the gap-before-first-row sized to clear the
  badge's full footprint, not just half the box height.
- **Hard 2-line cap on box text removed, raised to 3.** The old
  `[:2]` slice was *silently* dropping the tail of any line that
  needed a 3rd line — `"...bound and odorless"` was losing "odorless"
  with no visible sign anything had been cut. One box's copy still
  didn't fit in 3 lines even after the cap increase and was
  rephrased shorter (verified against the module's own `wrap()`
  before locking, not eyeballed).

### `editorial_lead()`
- **Per-item photo thumbnail support.** Items can now be a 3-tuple
  `(lead, body, photo)` instead of only `(lead, body)` — draws a
  square thumbnail (`item_thumb_size`, default 100) to the left of the
  run-in text. Fully backward compatible; existing 2-tuple items
  elsewhere in the system are unaffected.
- **Thumbnail top now aligns to the lead word's actual glyph ink**,
  measured via `textbbox()`, not to the nominal y coordinate text is
  drawn from. Playfair Bold's ascent leaves real padding above the
  cap-height, so same-y placement left the photo sitting visibly
  higher than the text it was meant to align with.

## core.py changes
*(carried over from earlier in this session, not yet in a save-back
until now)*

- **`footer()` gained an `img=` param.** Makes the footer
  luminance-adaptive: pass the actual rendered Image and each text
  run's real background gets sampled and colored white-on-scrim or
  plain ink accordingly, same pattern as the existing photo-caption
  adaptive logic. Only engages when `fill` is not also passed (`fill`
  always wins). Every existing call site that doesn't pass `img` is
  unchanged.

## Things tried and reverted
Kept here so the next session doesn't re-try the same dead end.

- **`cover_fit`'s `zoom` param for "show more of the photo" in a
  narrow column.** A tall, narrow target column against a roughly
  square source photo is *height-bound* — `zoom < 1` doesn't show more
  of the photo, it just fails to fully cover the target height,
  leaving a black gap at the bottom. Confirmed by direct test at
  zoom 0.8, 0.9, 0.95, 0.98 — all left a visible gap. There is no
  `cover_fit`-level fix for "I want a wider field of view in a
  fixed-aspect narrow crop with a roughly-square source"; the only
  real fixes are (a) a source photo with a different native aspect
  ratio, or (b) making the column itself wider (a real layout change,
  not a photo-fitting one).

## New deck: `render_fg_aroma_chemistry.py`
12 slides, CSW-grounded throughout. Full slide list and per-slide
photo credits are in the deck's own footer text; module used per
slide:

1. Cover — `grid_cover`
2. Three Layers of Aromas — `editorial_lead` (with item thumbnails)
3. Raw Materials — `mosaic`
4. Grape-derived impact compounds (pyrazines/rotundone) — `duel`
5. Fermentation temperature — `duel`, `photo_position="bottom"`
6. Fermentation's aroma exports — `card_grid`, `top_margin=100`
7. Malolactic fermentation (A/B/C) — `feature_trio`
8. Oak's contribution — `horizontal_trio`
9. Tertiary aromas / bottle aging chemistry — `duel`
10. Grape-to-glass process map — `process_map`
11. Aroma glossary — `fact_file`
12. Closing — `statement`

Two of Steve's own photos (a wine pour and a row of open-top
fermentation vats) are used directly rather than sourced from stock —
credited as "Steve's photo" in the relevant footers.
