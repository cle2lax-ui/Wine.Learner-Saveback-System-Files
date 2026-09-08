# CHANGELOG v8.1 — Marlborough GTR + Wine Faults Field Guide session

Two decks built this session (Guess the Region: Marlborough, NZ; Field
Guide: Wine Faults) surfaced six real, previously-shipped defects in the
shared core system. All are fixed and verified against `specimen.py`
(stable at 6/18 modules passing cleanly throughout — the 12 failures are
pre-existing missing demo-fixture photos, unrelated to any change below).

## core.py

- **`headline(show_underline=True)` parameter added.** `DESIGN_PROCESS_v8.md`
  had documented `show_underline=False` as locked, mandatory system
  behavior since the Oregon build — but the parameter never actually
  existed in code, so every headline since has still been drawing the
  old underline. Added the parameter (default `True` for backward
  compat); every call site in `modules.py` now passes `False` (see
  below). Default stays `True` so any deck outside this project that
  calls `headline()` without the new arg is unaffected.
- **`region_luminance(img, box)` added** (promoted from a local
  duplicate that lived in `guess_the_region.py`). Mean grayscale
  luminance of a region of the actual rendered image — for picking
  readable text color against whatever photo happens to be underneath,
  rather than assuming a fixed color always has enough contrast.
- **`assemble_pdf()` / `lock_deck_zip()` added.** Standing delivery rule
  (per Steve): review rounds are shared as a single merged PDF, never
  loose PNGs; a ZIP of source PNGs is only produced after explicit
  lock/sign-off. Two separate functions, not one call with a mode flag,
  so the ZIP (one-directional, "this is final") can never accidentally
  fire during routine iteration. Full rationale in both functions'
  docstrings and in `DESIGN_PROCESS_v8.md`.

## modules.py

- **Cover kicker dot was invisible.** `statement()`'s default "center"
  cover layout filled its bottom block with `pal["SIGNATURE"]` and then
  drew the kicker dot in that same `pal["SIGNATURE"]` — identical color
  on identical color, so the dot never rendered on any cover slide using
  the default layout. Now uses `PAPER`, matching the kicker text color
  (same treatment the closing variant already had correct, since its
  block is `INK` not `SIGNATURE`).
- **Closing variant's dot moved to top-right of the photo**, matching
  the cover variant's placement, for a consistent bookend. Was
  bottom-left just above the block seam.
- **All 15 `headline()` call sites now pass `show_underline=False`**,
  making the documented v8 rule actually true in shipped output.
- **`ladder()` tier blocks were capped at 240px regardless of available
  space**, leaving large dead zones below on slides with few tiers. Cap
  raised to 420px. Also **tier notes were silently truncating mid-
  sentence** — the module clips overflow text to whatever line count
  fits with no QA error; this is a structural trap (top tiers are much
  narrower than bottom ones in the pyramid, so a note tuned to fit the
  bottom tier can silently lose words at the top). No code fix for this
  half — flagging as a known sharp edge: write tier notes short enough
  to fit *the narrowest tier's* column, always verify by rendering.
- **`ladder()` color gradient made configurable in direction**: was
  hardcoded top=SIGNATURE→bottom=ACCENT. Per Steve's direction on the
  Wine Faults "Fault or Feature?" slide, inverted so the bottom (worst)
  tier is solid black fading up to `pal["ACCENT"]` (lightest) at top.
  Text color per tier is now chosen via `core.contrast()` against that
  tier's actual fill rather than assumed white — the lightest tier
  needs dark text.
- **`fact_file()` row pitch was capped at 190px**, same dead-space issue
  as `ladder()`. Raised to 260px.
- **`side_rail()` photo credit was double-rendering.** The module draws
  its own credit in the text column (by design, since the generic
  footer-gutter centering breaks for a full-height half-canvas photo)
  but was *also* passing `credit=` to `_finish()`, which draws a second
  copy via the default footer treatment — the two visibly overlapped.
  Fixed by no longer passing `credit=` to `_finish()` from this module.
- **`side_rail()` swipe-cue contrast when the photo is on the left.**
  The swipe-cue label always sits bottom-left (x=M); when `side="left"`
  that's on the photo, and the existing bottom `scrim()` gradient isn't
  always enough (scrim is zero-strength at its far edge by design, and
  some photos are light enough that even the strong end is marginal).
  Added a flat `chip()` at 55% opacity, matched to the *exact same box*
  `scrim()` already uses (not a smaller box) so it darkens uniformly
  rather than creating its own visible edge on top of the gradient.
  Two rejected approaches, for the record: (1) forcing a single shared
  `footer_fill` color for the whole footer row doesn't work because the
  page number sits on the paper side regardless of which side the photo
  is on — a fix for the photo side breaks the paper side; (2) pre-
  cropping the photo to move a dark area under the label costs real
  image content (a wine label went half off-frame) for a problem that's
  purely about text contrast, not composition.
- **`editorial_lead()` gained optional `standfirst_gap` / `item_gap`
  slot params** (defaults unchanged at 60/56) for decks that want more
  breathing room between blocks without a code change.

## guess_the_region.py

- **New `"nz"` flag option in `_FLAGS`** via a new `_image_flag(path)`
  factory — for flags too complex for the existing hand-drawn tricolor
  pattern (NZ's Union Jack + Southern Cross). Asset at
  `assets/flags/nz.png` (sourced from `lipis/flag-icons` via
  `raw.githubusercontent.com`, rasterized with cairosvg). `"french"` and
  `"italian"` still use the original drawn-tricolor path.
- **Cover-page footer contrast fix**, same category of bug as
  `side_rail()` above: the swipe-cue label on the photo blade used a
  fixed `MUTED` color that went nearly illegible against busy/light
  photo textures (dry gold grass, specifically). Now samples the actual
  rendered pixels via `region_luminance()` and picks ink or white.
- **`_region_luminance()` is now a thin wrapper around
  `core.region_luminance()`** instead of a local duplicate, so
  `modules.py` could use the same implementation.

## build.py

- Split `build_deck()` (PNGs + review PDF, safe to call every iteration)
  from a new `lock_deck()` (ZIP, call only after explicit sign-off).
  Both now delegate to `core.assemble_pdf()` / `core.lock_deck_zip()`.

## New render scripts (not previously in the project)

- `render_gtr_marlborough.py` — Marlborough, NZ Guess the Region deck.
- `render_wine_faults.py` — Wine Faults Field Guide deck (11 slides).

## New assets

- `assets/flags/nz.png` — real NZ flag, for `guess_the_region.py`'s new
  `"nz"` flag option.
- `photos/` — all photos actually referenced by the two new decks (see
  the two render scripts for the authoritative list). Photographer
  credits are in each deck's rendered footer/credit line, not repeated
  here.
