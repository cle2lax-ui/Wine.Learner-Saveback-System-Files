# SAVE-BACK — Quick Sips: Russian River Valley as new primary reference

`quick_sips_russian_river.py` is promoted to the primary reference
deck for the Quick Sips series (explicit instruction, not an inferred
convention). This package updates every shared file it touches so the
next Quick Sips deck starts from a clean, documented baseline instead
of re-deriving these fixes from scratch.

## Files in this package
- `quick_sips.py` — extensively modified, see below
- `modules.py` — one addition (`_finish()`'s `footer_label` param),
  shared with Field Guide
- `quick_sips_russian_river.py` — the new primary reference deck
- `QUICK_SIPS_STYLE_GUIDE.md` — updated with a new §6.5 and revised §9
- `photos/QS_glass_icon.png`, `photos/QS_glass_icon_ink.png` —
  rebuilt from scratch (see below)

Diff `quick_sips.py` and `modules.py` against the checked-in project
versions before merging — don't replace wholesale without review.

## Verified before packaging
- Both `quick_sip_cover()` and `quick_sip_detail()` called with **zero**
  of the new slot keys produce clean QA passes identical to pre-revision
  behavior — every change here is additive, not breaking.
- The reference deck itself rebuilds clean (`python3
  quick_sips_russian_river.py`, both pages QA pass).
- No debug instrumentation leaked into any shipped file (checked via
  `grep -rn DEBUG`).

## What changed and why

### `qs_benchmark_bottle()`
- **Return signature changed from `(obstacle, obstacle_top)` to
  `(obstacle, obstacle_top, cap_y)`.** This is the one technically
  breaking change in this package — any existing caller unpacking only
  two values will raise. Both call sites in `quick_sips.py` itself are
  already updated; check for any other callers before merging.
  `cap_y` is the caption's own actual rendered top, distinct from
  `obstacle_top` (`min(bottle_top, cap_y)`, which exists for
  `wrap_around()`'s obstacle-carving and is *not* safe to use for
  aligning anything to the caption specifically — see the real bug
  this caused, described in the style guide §6.5).
- New `cap_y_override` param: force the caption to start at an exact y
  instead of computing one from bottle geometry. Used to align the
  cover page's caption with its dashboard.
- New `cap_gap` param (default 36, unchanged): the horizontal buffer
  between the caption and the bottle photo, now configurable instead
  of hardcoded.

### `qs_tasting_dashboard()`
- New `text_bar_gap` (default 8) and `bar_h` (default 14) params,
  previously hardcoded. Needed this revision to fit a 6-row (Tannin-
  inclusive) structure into a tightened vertical budget without
  breaking the requested minimum gap between the dashboard's title and
  its first row.

### `qs_mark_overlay()`
- New `scrim_on` param (default True). Lets a deck disable the corner
  wordmark's protective scrim when the photo already has natural
  contrast under white text — was previously always-on with no
  override.

### `quick_sip_cover()`
- **Restructured the para1/para2 code path**: the dashboard's position
  (`shared_top = end_y + dashboard_gap`) is now computed *before*
  `qs_benchmark_bottle()` is called, and passed in as `cap_y_override`.
  This guarantees the caption and dashboard share one top by
  construction on this page — see style guide §6.5 for why the cover
  and detail pages needed different fixes here.
- New `para_leading` (default 1.22, unchanged) — was hardcoded.
- New `title_color` (default `PAPER`, unchanged) and
  `title_contrast_bg` (default `(40,38,34)`, unchanged) — the cover
  title's fill and the QA contrast check's reference background are
  both now overridable. `title_contrast_bg` matters: the default is a
  generic dark-background assumption that will falsely fail a light-
  on-light-photo title. Measure the actual photo pixels behind the
  title and pass the real value, as this reference deck does, rather
  than disable the check.
- New `title_chip`/`title_chip_color`/`title_chip_opacity` (all
  optional, default off): draws a flat, low-opacity chip sized to the
  title's own text bounding box for a light legibility boost, distinct
  from the heavier `caption_chip` behind the full title+tagline block.
- New `caption_chip` toggle (default True, unchanged): the title/
  tagline legibility chip is now opt-out. **Also fixed while adding
  this**: the chip used to be a blind fixed-460px-tall block drawn
  *before* the title/tagline geometry was computed, so it darkened
  roughly half the photo regardless of how much text was actually
  there. It's now drawn after that geometry is known, sized tight to
  the real text block.
- New `dash_header_gap`/`dash_pre_row_gap`/`dash_row_gap`/
  `dash_text_bar_gap`/`dash_bar_h` slot overrides threaded through to
  `qs_tasting_dashboard()`.

### `quick_sip_detail()`
- **Fixed the real alignment bug**: dashboard position changed from
  `max(end_y + gap, obstacle_top)` to `cap_y_actual` (the caption's
  true top, now returned by `qs_benchmark_bottle()`). See style guide
  §6.5 for the full explanation of why the old formula could silently
  diverge from the caption's actual position.
- Same `cap_gap` and `dash_*` overrides as the cover page.

### `modules.py` — `_finish()`
- New `footer_label` param (default `None`, meaning "use `footer()`'s
  own default"), forwarded through. Lets a deck's last page suppress
  the "SWIPE ←" cue instead of prompting toward nothing. Shared with
  Field Guide since `_finish()` is common code — verify this doesn't
  need equivalent documentation added to the Field Guide style guide.

### Assets — `QS_glass_icon.png` / `QS_glass_icon_ink.png`
Both files were flat, 100%-opaque RGB images with **zero actual icon
content** — not a transparency bug, empty artwork. This is a repeat of
a bug a prior revision claimed was already fixed; it evidently didn't
persist. This time's fix is more resilient to describe and re-verify:
rebuilt the white-tone icon from the ink-tone file (which still had
real linework), by thresholding grayscale value into an alpha mask,
and regenerated both variants from that one mask. Verified via the
alpha mask's per-row width profile forming an actual glass silhouette
(bowl → stem → base), not just "some transparency exists." If this
breaks a third time, the save-back or asset-sync process itself is the
more likely place to look, not the fix method.

## Content standard set by this deck (not code, but worth carrying
forward deliberately)
- Tasting-dashboard descriptors use WSET Level 3 SAT terms only — no
  flavor language in the dashboard itself (that belongs in the prose
  note).
- Any cited score names the critic or publication. If the cited score
  doesn't exactly match the vintage pictured, say so explicitly (this
  deck's Chardonnay note does).

## Known limitation, not resolved in this pass
`QUICK_SIPS_REFERENCE_HASHES.txt` and `reference_quick_sips/` are now
stale against all three reference decks and were not re-frozen as part
of this package — that requires rebuilding and re-hashing against the
actual project environment, which wasn't done here. Do this before
trusting a regression diff against any of the three reference decks.
