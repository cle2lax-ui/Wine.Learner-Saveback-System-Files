# CHANGELOG — save-back v2

Context: this save-back exists because `core.py`, `modules.py`, and
`quick_sips.py` were found to be **missing entirely from
/mnt/project** partway through this session, despite having been
included in the earlier `SAVEBACK_three_ways_v1.zip`. Cause unknown
from inside the session. This package restores all three, plus
`guess_the_region.py`, which has never been saved back at all this
session despite substantial changes (below).

`modules.py` is byte-identical to the v1 save-back — nothing has
changed in it since. `core.py` has exactly one addition. Everything
else new in this package is in `guess_the_region.py`.

## core.py

- **`cover_fit(..., x_anchor=0.5)`** — new param alongside the
  existing `y_anchor`/`zoom`. Controls horizontal crop position
  (0.0=left, 1.0=right, 0.5=center/original default). Added because a
  GTR cover's photo blade is narrow enough relative to a typical
  source photo that the width gets cropped hard, and a pure center
  crop clipped part of an off-center subject (a gnarled vine trunk,
  on the McLaren Vale deck) — needed a way to shift the crop window
  rather than just repositioning vertically.

## guess_the_region.py (never previously saved back)

- **`_us_flag()`** — flat US flag (13 stripes, solid navy canton, no
  stars — a starfield doesn't read at this render size). Added for a
  Sta. Rita Hills deck.
- **`_australian_flag()`** — went through two versions. First pass was
  hand-drawn (plain white cross for the Union Jack, dot-only Southern
  Cross) and didn't read well at render size, per direct feedback.
  Replaced with a real flag image: SVG sourced from
  `hampusborgos/country-flags` (public domain, the same source already
  used for the flag assets used elsewhere in this project), rasterized
  via `cairosvg`, pasted and scaled rather than redrawn from shapes.
  **Requires `photos/flag_australia_real.png`** to exist — see Assets
  below.
- **`gtr_cover()` new slot overrides**, all defaulting to prior
  behavior:
  - `title_color`, `letter_color`, `swipe_color` — override the
    header/clue-letter/swipe-cue color independently (previously all
    tied to `pal["ACCENT"]`). Added so a deck's typography can run a
    flag's actual colors (e.g. an Italian-tricolor or Australian-flag
    palette) instead of the fixed series gold.
  - `panel_bg` — the panel-side background color (previously hardcoded
    black). Needed when a chosen `title_color`/`letter_color` reads
    poorly against black (this happened: a navy headline was
    unreadable on the default black panel).
  - `icon_color`, `clue_text_color` — the map icon and clue-body-copy
    color, previously both hardcoded to PAPER/white. These **must** be
    overridden together with `panel_bg` if `panel_bg` is changed to
    something light, or the icon and all four clues become invisible.
  - `photo_anchor`, `photo_x_anchor`, `photo_zoom` — pass through to
    `cover_fit()`'s `y_anchor`/`x_anchor`/`zoom` for the blade photo.
    Use these together to reframe a subject that a pure center crop
    clips or crowds.
- **`gtr_reveal()` new slot overrides**:
  - `blurb_size` (default 84), `blurb_leading` (default 0.98) — the
    blurb's auto-shrink loop now starts from these instead of hardcoded
    values, and its own QA label check compares against `blurb_size`
    rather than a hardcoded 84 (this was a real bug: the QA exemption
    prefix logic would have silently mis-flagged any deck that set a
    custom starting size).
  - `photo_h` was already overridable before this session; noting it
    here because the McLaren Vale deck's fix combined a smaller
    `photo_h` (more room for the panel) with a larger `blurb_size`
    (using that room) — the two work together, not independently.

## Assets referenced by this package

`guess_the_region.py`'s `_australian_flag()` loads
`photos/flag_australia_real.png` via `load_photo_rgba()`. This file is
**not** part of this code save-back (it's a binary asset, not source);
regenerate it if missing:

```python
import cairosvg
# SVG source: https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/au.svg
cairosvg.svg2png(url="<path-to-fetched-au.svg>",
                  write_to="photos/flag_australia_real.png",
                  output_width=1200, output_height=600)
```

## Regression coverage

Before packaging, re-rendered end to end against the final files in
this zip: GTR (McLaren Vale, Puglia), Quick Sips (Piedmont), Three Ways
(Zinfandel), FFFA (South Australia). All passed QA clean.
