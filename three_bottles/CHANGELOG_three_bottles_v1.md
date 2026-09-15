# CHANGELOG — Three Bottles v1

*This is a historical engineering log of the v1 build -- the format was called "Three Ways" at the time these changes were made, and the narrative below is left as it was written. Only the title and filename are updated, to match the format's current name (see THREE_BOTTLES_STYLE_GUIDE.md for why it changed) and the file's new name in this repo.*

New series, built entirely on the existing Field Guide `showcase_shelf`
module. No new module file; all changes are extensions to
`core.py` / `modules.py` (plus one small `quick_sips.py` addition made
earlier this session, unrelated to Three Ways (as the format was called at the time) itself but bundled here
since it touches the same file). Every change below defaults to prior
behavior — no existing deck's output changes unless it explicitly
opts into a new slot key.

## core.py

- **`new_canvas(bg=None)`** — optional background color, default
  unchanged (PAPER).
- **`footer(..., show_page_num=True)`** — new param; `False` drops the
  page-number text entirely (for one-page decks with no "01/02" to
  show).
- **`footer(..., footer_size=None)`** — new param, default unchanged
  (`TYPE["caption"]`=60). *This was already being called with
  `footer_size=76` from `quick_sips.py` before this save-back — that
  file had been updated in a prior session but `core.py`/`modules.py`
  never received the matching parameter, so every Quick Sips deck
  render was one save-back away from a hard crash
  (`TypeError: _finish() got an unexpected keyword argument
  'footer_size'`). Caught by this save-back's regression test, not
  by design — worth flagging in case other latent mismatches like
  this exist between files that get saved back independently.*
- **`kicker_block(..., text_fill=None)`** — new param, default
  unchanged (INK). Lets a kicker render in white/light text on a dark
  background.

## modules.py

- **`_start(..., bg_color=None)`** — threads through to `new_canvas`.
- **`_finish(..., show_page_num=True, footer_size=None)`** — threads
  through to `footer()`.
- **`showcase_shelf()`** — substantially extended. All new behavior is
  opt-in via slot keys; nothing changes for a slot dict that doesn't
  set them.
  - `bg_color`, `kicker_color`, `headline_color` — background/text
    color overrides.
  - `headline` is now optional — omit it and the layout closes the gap
    instead of leaving dead space where it would have been.
  - `top_mark` — draws the Quick Sips glass-glyph mark (via new helper
    `_glass_mark_patch()`, see below) above the kicker row.
  - `bottle_lift` — grows a bottle's rendered height *without* moving
    the shelf line/text below it, by decoupling the bottle's scale
    target from the value that drives `shelf_y`. This is what lets a
    bottle neck rise up into the kicker/headline row.
  - When `bottle_lift > 0`, the kicker (and headline, if present) are
    **redrawn a second time after the bottles are placed**, so the
    type renders in front of the bottle glass instead of getting
    silently painted over by the bottle image's `paste()` call. This
    only fires when `bottle_lift > 0`; zero-cost for every other deck.
  - `panel_gap` — configurable gap between the kicker/headline row and
    the product row (was a hardcoded `+40`). Use this together with
    `bottle_lift` to control exactly how far a lifted bottle neck
    reaches — increasing `panel_gap` pushes the whole product row
    (and therefore the bottle's fixed-relative-to-it top) down.
  - `col_x_positions`, `col_w_override` — explicit column left-edges
    and width, bypassing the default `M + i*(col_w+gap)` grid. Added
    specifically because that default grid does not line up with a
    `region_photos` strip's own `W//n` grid — see the style guide's
    "Column alignment" section. Without this override the two grids
    silently disagree and text blocks end up inconsistently offset
    from their photos (measured on this deck's first build: 120px,
    54px, and −12px — the third column's text started *before* its
    photo's left edge).
  - `producer_color`, `name_color`, `style_color`, `origin_color`,
    `note_color`, `shelf_rule_color` — per-element color overrides,
    each defaulting to the original hardcoded value
    (`pal["SIGNATURE"]`, `pal["ACCENT"]`, INK, MUTED, INK,
    SHELF_RULE respectively).
  - `shelf_scrim_color` — draws a full-width rectangle from the shelf
    line down to the top of the region-photo band (or page bottom, if
    there's no photo strip), *before* the product loop runs — so
    bottle images/shadows (which sit above the shelf line) paint over
    it normally, and all product text (drawn later in the same loop)
    lands on top of the scrim rather than under it.
  - `region_photos` — list of `(photo, caption)` tuples. Renders as a
    true full-bleed strip (via existing `photo_stripe()` helper) at
    the bottom of the page, `region_band_frac` of the page height
    (default 0.25). Forces `footer_adaptive` on automatically, since
    the footer row now likely sits on photo pixels.
  - Region captions: no scrim/chip — plain text, but each caption's
    color is chosen by sampling that exact patch's luminance
    (`region_luminance()`), so it stays legible without a scrim
    regardless of what's behind it. Each caption also gets its own
    shrink-to-fit pass (`region_caption_font`/`region_caption_size`
    as the starting point, stepping down if a caption is wider than
    its column) — a bold/larger caption font can overflow one segment
    even when the chosen size fits the others comfortably; sizing
    globally for the worst case would have made the other two smaller
    than they needed to be.
  - `region_credit`, `region_credit_color` — tiny print top-right,
    separate from the footer's own `credit` param.
- **New: `_glass_mark_patch(img, d, pal, text, bg_color=None)`** — the
  Quick Sips glass-glyph-on-a-colored-patch lockup, for a one-off
  Field Guide slide that wants the mark with custom text instead of
  the Quick Sips series name. Duplicated locally rather than imported
  from `quick_sips.py`, because `quick_sips.py` already imports
  `_start`/`_finish` from `modules.py` — importing back the other way
  would be circular. If this pattern gets reused a third time, it's
  probably worth promoting the shared drawing logic into `core.py` so
  there's one source of truth instead of two near-identical copies.

## quick_sips.py

- **`qs_mark_patch(..., text_override=None)`** — new param; when
  given, replaces the "Quick Sips[- topic]" text entirely. Used for a
  one-off Field Guide slide (see `_glass_mark_patch` above) but the
  Quick Sips function itself also gained this directly, in case a
  Quick Sips deck ever wants the mark with non-standard text.

  *Note: this file was rebuilt starting from the current
  `/mnt/project/quick_sips.py` (which already contained several
  unrelated improvements from a prior save-back —
  `cap_gap`/`footer_size`/`tagline_chip`/`qs_mark_overlay`
  `text_color`/body-size adjustments) rather than from this session's
  working copy, which had gone stale relative to it. Diffed against
  the current project file before packaging to confirm only the one
  intended change is present — see the regression test note below.*

## Regression testing

Before packaging, all four existing series were re-rendered end to
end against the final `core.py`/`modules.py`/`quick_sips.py` in this
save-back: Quick Sips (Piedmont), GTR (Puglia), FFFA (Santa Barbara
County), and the new Three Ways (Zinfandel) deck itself, as the format was called at the time. All passed
QA clean. This is also what caught the `footer_size` mismatch above —
it would not have surfaced from a Three Ways-only test. (Same historical naming note as above.)
