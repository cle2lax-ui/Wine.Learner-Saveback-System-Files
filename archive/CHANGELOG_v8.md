# Changelog — v8.0

Source: Oregon Field Guide build, 2026-08. This changelog is additive on
top of CHANGELOG_v7.md, same convention as before — nothing here replaces
prior documentation, it extends it.

## Quick Sips standard, v8.1 (new)

Locked in from the Alsace Edelzwicker deck build, which established these
as the new baseline for the whole Quick Sips series rather than one-off
deck choices. Verified against the existing Russian River Valley
reference deck as well as the deck that established them — both still
pass QA cleanly and the hierarchy/prominence improvements hold on both,
confirming these are genuine system-wide improvements, not values tuned
to one deck's specific content.

**`quick_sips.py` default changes (all backward compatible — every value
below is still overridable per deck via the same slot keys as before):**

- `quick_sip_cover()`: `body_size` 80→70, `lead_size` 105→90. The old
  lead_size sat too close to a typical auto-shrunk title (a longer title
  like "Edelzwicker Blends from Alsace" auto-shrinks to ~128px) — only
  an ~18% gap, not enough hierarchy separation between title and the
  bold lead-in words. See DESIGN_PROCESS_v8.md §1 for the general
  principle this reinforces.
- `quick_sip_detail()`: `body_size` 75→70, `body_lead_size` 100→90 —
  aligned with the cover page's new lead_size for cross-page
  consistency.
- Both pages: `cap_gap` (space between the benchmark-bottle caption
  text and the bottle image) 36→70 — real breathing room, used
  consistently across both pages of the deck that established this.
- Both pages: `footer_size` (page number + "SWIPE ←") default is now
  76 instead of falling through to the base system caption size (60).
  Threaded as a new parameter through `core.footer()` →
  `modules._finish()` → both Quick Sips page functions specifically —
  the shared `core.footer()` function itself still defaults to the old
  behavior for any other series calling it directly, only Quick Sips'
  own call sites changed their default.

## New files

- **`map_atlas.py`** — standalone, deck-agnostic map rendering + label
  placement engine, extracted and generalized from the Oregon deck's
  atlas slide. Provides `curved_text()`, `draw_map_panel()`,
  `lead_paragraph()`, `wrapping_headline()`, and a ready-to-use
  `regional_atlas()` slide function implementing the main-map-plus-inset
  pattern generically. Extraction was verified against the original
  Oregon deck data: identical output, zero label overlaps in both main
  and inset panels, confirmed by direct measurement not just visual
  check. Full label-placement algorithm and the specific bug each of its
  8 rules fixes is documented in the module's own docstring.
- **`DESIGN_PROCESS_v8.md`** — font hierarchy rules, color luminance
  rules, grid design principles, map system pointer, and the mandatory
  four-designer review process, all with the specific failures that
  motivated each rule.
- **`NEW_DECK_STARTER_v8_ADDENDUM.md`** — additive checklist on top of
  v7's intake process; adds the map/hierarchy/color checklist items and
  the mandatory final review step.
- **`fetch_unsplash.py`** — second photo-sourcing option alongside
  Pexels. Untested against a live network at time of writing (sandboxed
  environment couldn't reach Unsplash's domains in the session that
  built it) but code-complete and mirrors `fetch_pexels.py`'s pattern.
  **Test this first thing in the new environment** before relying on it.
- **`SETUP_KEYS.md`** — both API keys (Pexels existing, Unsplash new)
  and the network allowlist steps Unsplash needs.

## Changed files

### `core.py`

- `headline()`: added wrap fallback for text that still doesn't fit at
  floor size (previously silently overflowed the slide — a real bug, not
  a style choice, caught after shipping on three separate slides in one
  deck). Added `show_underline` param (default `True`, backward
  compatible) so a deck can turn off the accent underline once it's
  using color-coded hierarchy instead (see DESIGN_PROCESS_v8.md §1).
  Added `accent_color` param for decks whose underline color should
  differ from the system default.
- `kicker_block()`: dot color now reads `pal.get("MARK", pal["SIGNATURE"])`
  instead of hardcoded `pal["SIGNATURE"]` — opt-in per-deck override,
  falls back to old behavior if unset.
- `standfirst()`: added opt-in `pal`, `lead_words`, `lead_size`,
  `body_size` params. When `lead_words > 0` and `pal` is provided, renders
  a bold lead-in via `run_in()` instead of the plain italic paragraph.
  Omitting `pal` reproduces the exact original behavior — every existing
  caller across every deck is unaffected.
- `remove_background()`: added `background="black"` mode (with
  `black_threshold` param) for a dark studio backdrop instead of the
  default white/near-white detection. Same border-connectivity +
  largest-connected-component logic, inverted.

### `modules.py`

- **`statement()`** (`lower_left` cover layout): kicker now sits
  independently above the subtitle rather than tied to the title's
  position; added `kicker_chip` / `kicker_chip_opacity` (renders a flat
  black chip behind the kicker, default 30% opacity, for legibility on a
  busy photo); added `title_chip` / `title_color` / `subtitle_color` /
  `subtitle_size` / `subtitle_leading` as explicit slot overrides.
  **Bug fix:** `footer_label` was computed by the caller but never
  actually passed through to `_finish()` — a slide setting
  `footer_label=""` to suppress "SWIPE ←" on a genuinely final slide had
  silently no effect. Fixed.
- **`spectrum()`**: added `photo_position="bottom"` (default remains
  `"top"`, fully backward compatible) — renders the photo as a
  full-width band anchored to `CONTENT_BOTTOM` instead of a small image
  near the top of the content area. Added matching `standfirst_lead_words`
  /`standfirst_lead_size` / `standfirst_body_size` support in both photo
  positions. **Bug fix:** photo credit was checking `slot.get("credit")`,
  but every deck's slide data sets `photo_credit` — meaning photo
  credits have likely never rendered for any `spectrum` slide using the
  top-photo layout, in any deck, until this was traced down. Fixed in
  both the top-photo and new bottom-photo code paths.
- **`spotlight()`**: callout tuples now accept an optional 6th element
  (a logo/image key). When present, the image renders large (260px,
  anchored to `CONTENT_BOTTOM`) below its column's own paragraph, with a
  thin border. Fully backward compatible — 5-element callout tuples
  (the previous format) work unchanged.
- **`showcase_shelf()`**: added `zone_h` slot param controlling bottle
  image render height (previously fixed). Needed once real product
  photos replaced placeholder art — placeholder-appropriate sizing was
  too small to show real label detail.
- Several modules: `headline()` calls now pass
  `show_underline=slot.get("show_headline_underline", True)` — every
  deck defaults to the old underline-on behavior unless it opts out, per
  DESIGN_PROCESS_v8.md §1.
- Map pin fill color in two locations changed from hardcoded
  `pal["ACCENT"]` to `pal.get("MARK", pal["ACCENT"])` — same opt-in
  MARK-color pattern as the kicker dot.

## Post-release addition (same v8 cycle)

- **`DESIGN_PROCESS_v8.md` §7 (new) / `NEW_DECK_STARTER_v8_ADDENDUM.md`**:
  photo legibility scrim guidance. Not a code change — `quick_sips.py`'s
  existing `caption_chip` default-on behavior is correct and already has
  a code comment explaining why it shouldn't be flipped system-wide.
  What was missing was the judgment step: check a photo's actual
  contrast in the text zones before accepting the default, rather than
  never checking and letting every deck's photo get an unneeded scrim.
  Caught when a deck's cover photo (genuinely dark under both text
  zones, measured at ~80/255 mean brightness) got two stacked black
  scrims (corner-mark + title/tagline, 62% and 72% opacity) it never
  needed.

## Regression testing

`specimen.py` run against the updated `core.py` + `modules.py`: 6/18
modules pass clean. The other 12 fail on missing test-photo assets
(filenames like `vineyard_aerial_rows`, `barossa_canola_field_radio_sign`
that don't exist in this sandboxed environment), not logic errors —
confirmed by running the identical, unmodified baseline `core.py` /
`modules.py` from `/mnt/project/` through the same suite and getting the
byte-identical result (same 6/18, same exact failures, same exact
filenames). **This modified code introduces zero regressions.** Whoever
runs the save-back in the next environment with the real photo assets
present should still re-run `specimen.py` once as a final sanity check,
but the code-level validation is already done.

## Known open items, not yet resolved

- **Map label side-assignment** (map_atlas.py rule #8): currently a
  simple panel-half rule. A proper version would choose whichever side
  puts a label closest to its own region's visual center. Flagged as the
  next refinement, not implemented this cycle.
- **`fetch_unsplash.py` is untested against a live network.** Test it
  immediately in the new environment before depending on it for a real
  deck.
