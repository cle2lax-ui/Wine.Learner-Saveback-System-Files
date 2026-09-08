# Save-back package — "Clash of the Titans" + "Ridge Zinfandel Blends" sessions

**This package supersedes the previous "Cava/Corpinnat/Clàssic
Penedès session" README (`save_back_package_v5.1`).** Everything in
that package is carried forward — nothing was reverted. This README
covers what changed **since**, across two separate sessions: a Field
Guide deck ("Clash of the Titans," Cabernet Sauvignon) and a Quick
Sips deck ("Ridge Zinfandel Blends"). Full narrative writeups of both
are in **LESSONS_LEARNED_v5.md §10–11** — read those before touching
`modules.py`, `core.py`, or `quick_sips.py` again.

## What changed and why

**`core.py` (shared by both series):**
- `wrap()` now breaks at internal hyphens when a single word is itself
  wider than the available column (was space-only, so a hyphenated
  compound or a spaceless em-dash pattern was one unbreakable token
  that either overflowed or bled into the next column — this recurred
  across several different slides before being fixed once here).
- `run_in()`: removed a hardcoded `"  ·  "` separator between the bold
  lead-in and body text (now a single space); added a `justify=True`
  parameter for full justification (off by default).

**`modules.py` (Field Guide):**
- `editorial_lead()`: new `grid_table` mode — a genuine cross-tabulated
  table (column headers, row labels, wrapped cells), distinct from the
  existing `table` mode (which is really a grouped list). `columns`
  mode's title sizing redesigned to shrink-then-wrap per-column instead
  of blanket-shrinking the whole row for one long title, plus an 8px
  safety margin on wrap width.
- `side_rail()`: `kicker` is now optional (was required). New
  `dashboard` slot reuses Quick Sips' tasting-dashboard component
  directly via a lazy import. Item lead/body sizes and gap are now
  configurable. **Headline had zero width-checking** (bare
  `.split("\n")`) — same bug class as the `core.headline()` fix from
  the last package, recurring independently here since this module
  draws its own headline; now wraps properly.
- `card_grid()`: new `photo_style="top"` — a large photo across the
  top of each card instead of the small 84px inline icon (default
  `"icon"` unchanged). Card subtitle font changed from serif italic to
  sans-serif bold.
- `showcase_shelf()`: `cols` is now configurable (was hardcoded to 3 —
  a 4th product silently wrapped to a second row that, at a large
  `zone_h`, ran thousands of pixels off-canvas). All wrapped text
  fields now carry a 14px safety margin between columns.
- `atlas()`: markers overhauled — dot radius doubled; labels can wrap
  (`wrap_w`); leader lines now anchor to the top-middle of the label's
  first word (or a specific letter via `anchor_letter`) instead of the
  raw label y-coordinate, which for any wrapped label fell *inside*
  the text's own vertical span and visibly cut through the letters;
  `no_leader=True` skips the line for markers close enough not to need
  one. New `lat_bands` (faded latitude bands, alpha-composited over
  both land and sea, not hidden behind the landmass fill). New
  `paragraph`/`paragraph_lead` — the module had no way to render
  flowing prose before, only a 3-column legend strip. New
  `map_top_pad`.
- `mosaic()`: new `kicker_serif=True` — keeps the colored chip but
  switches its font from sans to the deck's serif.
- `photo_quote()`: `quote_size` now configurable (was hardcoded to 150).

**`tokens.py` (shared, standing preference changes):**
- `CONTENT_BOTTOM`: `H-400` → `H-200` — smaller default bottom margin,
  more usable content area, across every layout.
- `MAX_BODY_WORDS`: 70 → 105 (+50%).
- Both changes mean content built and fitted under the *old* tighter
  boundary may now have unused room worth re-expanding on request —
  "fits" was measured against a limit that no longer applies.

**`quick_sips.py`:**
- `photo_caption` added to both `quick_sip_cover` and
  `quick_sip_detail` (neither had it before). Cover places it
  bottom-**right** specifically to avoid the left-aligned
  title/tagline stack already occupying the photo's bottom-left.
- `quick_sip_detail` gained `content_pad` (gap between the photo and
  the headline below it, was hardcoded to 60px).
- **The wine-glass icon assets themselves were broken** — every copy
  of `QS_glass_icon.png`/`QS_glass_icon_ink.png` anywhere in the
  project was flat RGB with no alpha channel, so the icon rendered as
  a solid white block. Re-copying the file from elsewhere did not fix
  this, because every copy was the same broken asset. Regenerated
  from the actual cited source (Lucide's `wine` icon, fetched fresh
  from lucide-icons/lucide on GitHub) with genuine transparency —
  included in this package at `photos/QS_glass_icon.png` and
  `photos/QS_glass_icon_ink.png`. **Replace these two files in the
  project's photo library; do not keep the old ones.**

**New reference deck:** `quick_sips_ridge_zinfandel.py` — a red-wine
Quick Sips deck (full six-row tasting dashboard including Tannin),
structured identically to `quick_sips_volcanic_whites.py` (white wine,
five-row dashboard, no Tannin). Use whichever matches the new deck's
wine color as the starting template — building red-wine decks by
pattern-matching against the white-wine reference is exactly how the
Tannin row got dropped on the first pass of the Ridge deck (see
LESSONS_LEARNED §11).

**Documentation:**
- `STYLE_GUIDE_v5.md`: updated the module table for every module
  listed above; documented the `wrap()`/`run_in()` fixes; updated
  `CONTENT_BOTTOM`/`MAX_BODY_WORDS` to their new values with the
  standing-preference rationale; noted that the headline-overflow bug
  pattern recurred independently in `side_rail()` and `mosaic()`.
- `QUICK_SIPS_STYLE_GUIDE.md`: documented `photo_caption`/
  `content_pad`; corrected an earlier claim that the glass-icon bug
  was "caught in review" — it was not, the asset itself stayed broken;
  documented the new second reference deck and flagged both reference
  decks' hashes as stale again (this package touched `core.py` and
  `quick_sips.py` directly, neither re-frozen against either deck).
- `LESSONS_LEARNED_v5.md`: two new sections (§10 Titans, §11 Ridge
  Zinfandel) covering everything above in full narrative detail,
  including the bespoke four-bottle cover techniques (flag-filled
  traced-boundary labels, matte-paper shading via a blurred glass-
  highlight profile, canvas-padding-before-erosion for edge cleanup),
  a corrected-not-just-relabeled regional swap (Barossa → Coonawarra),
  a file-mislabeling catch, and the Judgment of Paris factual
  correction (Monte Bello placed *fifth* in 1976 — Stag's Leap won
  that day; Monte Bello's real win was the 2006 30th-anniversary
  rematch).

## What's verified vs. what isn't

**Verified this session:**
- `core.py`, `modules.py`, `tokens.py`, and `quick_sips.py` — taken
  from their respective most-current project copies (the Field Guide
  fixes were made in one project, the Quick Sips fixes in a separate
  one that had started from the *previous* save-back and therefore
  never received the Field Guide session's `core.py`/`modules.py`
  fixes) — were diffed against each other, merged onto the more
  complete Field Guide versions, and confirmed to import cleanly
  together.
- Both Quick Sips reference decks (`quick_sips_volcanic_whites.py`,
  `quick_sips_ridge_zinfandel.py`) render against the merged
  environment with no errors beyond expected missing photo files
  (confirmed by exception type, not assumed).
- `specimen.py` (Field Guide regression suite) runs clean on every
  module that doesn't require a photo; the photo-dependent modules
  fail only on missing stock images in this environment, same
  confirmation method as prior packages.
- The regenerated glass-icon PNGs were checked directly: alpha channel
  range is `(0, 255)`, not a flat constant, confirming real
  transparency this time.

**Not verified / still open:**
- `QUICK_SIPS_REFERENCE_HASHES.txt` and `reference_quick_sips/` are
  stale (flagged in QUICK_SIPS_STYLE_GUIDE.md §9) and need rebuilding
  against the merged `core.py`/`quick_sips.py` before the next Quick
  Sips deck starts. Not done as part of this package. Field Guide's
  `REFERENCE_HASHES.txt` likely needs the same treatment given the
  scope of `atlas()`/`showcase_shelf()`/`side_rail()` changes, but
  wasn't checked.
- The photo-dependent `specimen.py` modules were not exercised
  end-to-end with real images in this environment.
- `NEW_DECK_STARTER_v5.md` and `build.py` were reviewed and found to
  need no changes (confirmed identical to the prior package via diff)
  — lighter pass than the line-by-line audit given to the core system
  files.
- The bespoke cover-build techniques from the Titans session (flag-
  filled labels, curved-label rejection, matte-paper shading) are
  documented as narrative technique in LESSONS_LEARNED §10, not as
  reusable code in `modules.py` — they were one-off PIL scripts
  outside the module system, not a new module or slot. If a future
  deck needs another multi-bottle lineup cover, treat that section as
  a recipe to follow, not a function to call.

## To make this durable

Replace every file in this package over the project's current
versions — complete drop-in replacement, not a diff to reconcile by
hand. Pay particular attention to `photos/QS_glass_icon.png` and
`photos/QS_glass_icon_ink.png` — these must overwrite the existing
(broken) files, not just add alongside them. After replacing: rebuild
both Quick Sips reference decks and both Field Guide/Quick Sips
reference-hash files per the notes above before starting the next real
deck build.
