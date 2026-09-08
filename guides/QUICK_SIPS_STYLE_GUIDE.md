# QUICK SIPS STYLE SYSTEM

**As of this revision, `quick_sips_russian_river.py` is the new primary
reference deck for the series** (see §9). It's the only Quick Sips
deck built to date that exercises every current capability: aligned
tasting-notes/dashboard tops, a widened dashboard, WSET Level 3-only
tasting descriptors, cited critic reviews, a configurable title
treatment (color, contrast-checked against the real photo, optional
legibility chip), and a cleanly-suppressed footer swipe cue on the
last page. `quick_sips_volcanic_whites.py` and
`quick_sips_ridge_zinfandel.py` remain valid secondary references for
their specific dashboard shapes (5-row white / 6-row red) but predate
several of the fixes below — don't copy layout patterns from them
without checking against this section first.

**Seven real fixes and eleven new capabilities landed this revision,**
all in `qs_benchmark_bottle()`, `qs_tasting_dashboard()`,
`qs_mark_overlay()`, `quick_sip_cover()`, `quick_sip_detail()`, and
`modules._finish()`. Full detail in §6.5 and §8. The short version:

- **A real, shipped alignment bug is fixed.** The tasting dashboard's
  vertical position on the detail page was keyed to `obstacle_top`
  (`min(bottle_top, cap_y)`) instead of the caption's own actual top.
  Whenever the bottle photo's top edge sat higher than the caption
  text, the dashboard silently aligned to the *bottle*, not the
  caption — producing a visible mismatch that took two attempts to
  actually trace to its root cause. `qs_benchmark_bottle()` now
  returns the caption's true top as a third value; use it, not
  `obstacle_top`, for anything meant to align with the caption itself.
- **The benchmark-bottle heading does not auto-wrap.** It only breaks
  on a literal `\n` in the string. This isn't new behavior, but it
  caused real confusion this session (assumed-auto-wrap led to an
  unwrap regression when a manual `\n` was removed) and is worth
  stating plainly here so it doesn't happen again.
- Six new slot parameters on `qs_benchmark_bottle()` and
  `qs_tasting_dashboard()` that used to be hardcoded: `cap_gap`,
  `cap_y_override`, `text_bar_gap`, `bar_h`, plus the pre-existing
  `header_gap`/`pre_row_gap`/`row_gap` are now actually threaded
  through from both cover and detail page slots (`dash_header_gap`
  etc.) instead of being fixed at the call site.
- Title color, contrast reference, and an optional legibility chip are
  now configurable (`title_color`, `title_contrast_bg`, `title_chip`
  family) — previously the cover title was hardcoded to `PAPER` with
  no way to try a different color.
- The corner "Quick Sips" wordmark's scrim is now optional
  (`qs_mark_overlay(..., scrim_on=)`), and the title/tagline
  legibility chip is now sized to the actual rendered text block
  instead of a blind fixed height that could cover half the photo.
- `modules._finish()` gained a `footer_label` override, so a deck's
  last page can drop the "SWIPE ←" cue instead of prompting the reader
  toward nothing.
- **A real broken asset is fixed.** `QS_glass_icon.png` (the
  white-tone corner glass icon) was a flat, 100%-opaque white square
  with zero actual icon content — not a transparency bug, the artwork
  itself was empty. Rebuilt both icon variants from the ink version's
  real linework, verified via the alpha mask's own silhouette profile
  (bowl → stem → base).

All of the above are additive and backward-compatible — verified by
calling both `quick_sip_cover()` and `quick_sip_detail()` with zero of
the new slot keys and confirming identical output to before this
revision (see `CHANGELOG_quicksips_rrv.md` in the save-back package for
the exact test). This only loosens the effective limit going forward,
so it cannot break any deck that previously passed.

---

**As of v5.0, this series shares `core.py` with Field Guide's rebuild —
see `LESSONS_LEARNED_v5.md` and `STYLE_GUIDE_v5.md` §8/§8b for what
changed and why: two new automatic QA checks (edge-bounds, opt-in photo-
contrast sampling), a `chip()` primitive alongside `scrim()` for any
Quick Sips element that overlays text on a photo, and the locked
`core.remove_background()` product-photo pipeline if any Quick Sips
layout ever needs bottle/product cutouts. Nothing in this document's
Quick Sips-specific layout rules changed — only the shared foundation
underneath both series did.**

**The operating manual for every Quick Sips 2-page post.**
Quick Sips is the second series built on this system, alongside **Field
Guide** (see `STYLE_GUIDE_v4.md`). Same canvas, same safe zones, same
QA harness — a distinct visual language. Rules live in code
(`tokens.py`, `core.py`, `quick_sips.py`), not on paper: every number
below is enforced automatically at build time. A QA failure aborts the
build.

**Fixed this revision:** both Quick Sips modules were setting
`qa.max_words = 130` to raise the word budget above Field Guide's
default 70 — but `core.py`'s `QA` class has never had a `max_words`
attribute; it checks `self.word_limit`. That line was silently creating
an unused attribute and doing nothing, meaning every Quick Sips deck
has actually been enforced against the default 70-word budget, not the
intended 130, since the override was introduced. Changed to
`qa.word_limit = 130` to match the real attribute (see `core.py` §8 in
the Field Guide guide for how the override mechanism works).

**Redesigned this revision (title/subtitle, text block, bottle
lockup):** the cover page's layout, established across the Santa Ynez
Valley deck, is now the standard for all future Quick Sips decks. See
§3 and §6 for the full spec. In short: a smaller, left-anchored title
sitting flush with the photo's bottom edge (not a large right-aligned
headline); two short run-in paragraphs with a bold baseline-aligned
lead-in instead of a standfirst+subtitle+facts-line stack; and the
benchmark-bottle caption listing the producer name above the wine name.
The old pattern (large right-aligned title, eyebrow, stat strip, single
body paragraph wrapping the bottle) still works — every old slot is
still supported — but is now the *legacy* path, not the default.

---

## 1 · Purpose & workflow

Field Guide is the 10–12 slide carousel deck for a full regional or
topical deep-dive, built from a menu of 17 modules. **Quick Sips is
the opposite move: exactly two slides, one narrow topic** (a single
appellation, grape, or style), done to a polished infographic/brochure
standard rather than an editorial-magazine one. Instagram carousel +
story, not a full lesson.

Audience: WSET/CMS/CSW students and serious enthusiasts, 35–60,
affluent, worldly. Style touchstones: Wine Spectator, Condé Nast
Traveler, Rolex, Cigar Aficionado, Four Seasons — restrained palette,
serif display type, stat-forward facts, generous white space.

A new Quick Sips deck is a **manifest**, exactly like Field Guide:

```python
from tokens import DEFAULT_PALETTE
from quick_sips import quick_sip_cover, quick_sip_detail

PALETTE = dict(DEFAULT_PALETTE)
PALETTE.update(dict(SIGNATURE=(96, 30, 30), ACCENT=(168, 130, 60), LEAD=(96, 30, 30)))

SLIDES = [
    (quick_sip_cover,  dict(photo=..., title=..., tagline=...,
                             para1=..., para1_lead_words=3,
                             para2=..., para2_lead_words=2,
                             structure=[...], bench_heading=..., ...)),
    (quick_sip_detail, dict(topic=..., headline=..., body=...,
                             body_lead_words=..., structure=[...], ...)),
]
```

See `quick_sips_russian_river.py` for the full worked reference deck
(the current primary reference — see §9) as the pattern to copy from.
No layout decisions, no font choices, no spacing judgment calls per
deck. If content doesn't fit, **cut copy** — never shrink type below
`FLOOR`, and never guess at spacing by eye (see §5).

---

## 2 · Canvas & safe zones

Shared with Field Guide — same file, same values (`tokens.py` §Canvas):
2160×2700 build canvas, 1080×1350 export, `M=120` margin,
`CONTENT_BOTTOM = H-400` (Instagram caption-preview risk zone).

**Quick Sips-specific relaxations, both deliberate:**
- The **benchmark bottle photo is allowed to bleed off the right and
  bottom canvas edges** for design impact — this is core to the
  series' look, not an exemption granted reluctantly. Its bounding box
  is *not* QA-tracked (only the caption text beside it is), so bleed
  never trips the caption-zone check.
- **Body text may run closer to the page bottom than
  `CONTENT_BOTTOM`** normally allows, tracked via the `"!"` QA-exemption
  prefix (`qa.box("!body", ...)`). This is an explicit, standing
  decision for this series — Quick Sips pages read as posters more than
  scrollable feed cards, and the deck owner has signed off on body copy
  running long. Don't remove the `!` prefix without checking first.

---

## 3 · Type

Quick Sips does **not** use the Field Guide `TYPE` ramp — a denser
infographic format doesn't fit one shared scale. Sizes are chosen per
element directly in `quick_sips.py`, but every one of them still obeys
`FLOOR = 60` from `tokens.py`, with **one explicit, documented
exception**:

| Element | Face | Size | Notes |
|---|---|---|---|
| Cover title | Playfair Black | **110** | Left-aligned, bottom edge of photo band. `title_size`/`title_align` overridable (legacy decks use 200/"right" — see §6). Now shrinks to fit the canvas width rather than running off the edge — was previously drawn at a fixed size with no width check (see §8) |
| Cover tagline | Playfair Bold Italic | **80** | Left-aligned, directly under title. `tagline_size` overridable (legacy: 60) |
| Detail headline | Playfair Black | 110 | Same shrink-to-fit protection as the cover title, added this session (see §8) |
| Body text (both pages) | **Archivo Light** (`body_light`) | **80** (cover) / 75 (detail) | Thin, magazine-column feel — see §3.1 |
| Body lead-in phrase | Playfair Bold (`display_bold`) | **105** (cover) / 100 (detail, optional) | Bold serif, deck `SIGNATURE`; first few words only — baseline-aligned with the body text on the same line, not top-aligned (see §5) |
| Benchmark-bottle heading | Playfair Bold, non-italic | 50 | Deck `SIGNATURE` |
| Benchmark-bottle producer | Playfair Bold Italic | 50 | `QUICKSIPS_GOLD` — now sits **above** the wine name (see §6.2) |
| Benchmark-bottle wine name | Playfair Bold Italic | 58 | `INK` |
| Benchmark-bottle note | **Playfair Regular** (`display_light`) | **50 — below FLOOR, intentional** | `INK`; see below |
| Tasting-dashboard labels | Playfair Bold Italic | 60 | |

**Legacy-only elements** (still supported via the pre-para1/para2 slots,
not used in a standard new deck): eyebrow/kicker (Archivo Cond Bold,
60, tracked, `QUICKSIPS_GOLD`), stat-strip numerals (Playfair Black,
92) and labels (Archivo Cond Bold, 60, tracked, `MUTED`), standfirst
(Playfair Medium Italic, hero size), subtitle (Playfair Bold, ~95).
**As of this session, the eyebrow and stat-strip labels render in Title
Case as given rather than forced ALL CAPS** — the `.upper()` calls were
removed from `qs_stat_strip()` and `quick_sip_cover()`'s eyebrow
rendering, matching the same convention change made in the Field Guide
series (`core.kicker_block()` and five other call sites — see
STYLE_GUIDE_v5 §3). Supply eyebrow/label text in the case you want it
to render in.

**The one sub-floor exception:** the benchmark-bottle caption note runs
at 50px, tracked as `qa.size("!bench_caption_sz", ...)`. This was an
explicit, informed choice by the deck owner to fit a proper photo
caption beside a bottle neck rather than shrink the bottle or drop the
note. It is not a bug and should not be "fixed" back up to 60 without
checking — but don't extend this exception elsewhere by default. Keep
the note itself short (two flavor descriptors plus vintage/ABV is
usually the ceiling) — a longer note is the single most common cause of
the caption-zone QA failure, since it eats into the same vertical
budget the two run-in paragraphs and the bottle_h tuning depend on
(see §6).

### 3.1 · Two new font roles (added for this series, available system-wide)

Neither existed anywhere in the system before Quick Sips needed them.
Both were instanced from Google's variable-font sources and registered
in `tokens.py` `FONT_FILES` like any other role — any future module in
either series can use them:

- **`body_light`** → `Archivo-Light.ttf`, instanced at weight 330 from
  the Archivo variable font. The system had Medium and Bold only;
  nothing thin enough for a "clean, elegant magazine sans" read. This
  is what Quick Sips body text uses throughout.
- **`display_light`** → `Playfair-Regular.ttf`, instanced at weight
  400 (the lightest this family supports) from the Playfair Display
  variable font. The system had Black/XBold/Bold and two italics, but
  no plain non-italic light-weight serif. Used for the benchmark-bottle
  caption note.

If a future deck needs a genuinely lighter weight than 330/400, the
source variable fonts are `/tmp`-fetchable again from Google's font
repo (`google/fonts` on GitHub, `ofl/archivo` and `ofl/playfairdisplay`)
and can be re-instanced with `fontTools.varLib.instancer`.

---

## 4 · Color

Fixed neutrals (`PAPER`, `INK`, `MUTED`, `LINE`) are shared with Field
Guide — never change.

**Per-deck palette**, same mechanism as Field Guide (`SIGNATURE`,
`ACCENT`, `LEAD` in the manifest), but Quick Sips decks lean into a
**deep garnet + metallic gold** register rather than Field Guide's
default claret — see `quick_sips_volcanic_whites.py`'s palette for the
reference values.

**`QUICKSIPS_GOLD = (168, 130, 60)`** (`tokens.py`) is new: a fixed
series accent independent of each deck's `SIGNATURE`, used for stat-
strip hairlines, eyebrow labels, and the benchmark-bottle producer
name. It does not flex per deck — that's what makes it a *series*
identity mark rather than a topic accent.

---

## 5 · The wrap-around text engine

This is the load-bearing piece of new infrastructure this series
required, and it now lives in `core.py` as public API (`wrap_around`,
`justify_styled`, `tracked_w`, `wrap_tracked`) — available to Field
Guide modules too, not Quick-Sips-only.

**What it does:** flows a justified paragraph that narrows around a
rectangular obstacle (the benchmark bottle + its caption), producing a
carve-out — full width, then narrowed where it meets the obstacle, with
an inverted-L reading shape. Optionally styles the first N words of the
paragraph in a different font/color (the bold serif lead-in on page 1).

**Two specific, hard-won bugs are fixed inside this function. Do not
simplify it back toward a naive implementation** — both were shipped,
caught in review, and cost real iteration to diagnose:

1. **Sparse-line justification.** Stretching a 2-word line to fill a
   wide column puts all the slack into one gap between those two words
   — visually an obvious, ugly hole. Any line with ≤3 words, or whose
   natural width is under 75% of the available width, falls back to
   left-aligned instead of justifying.

2. **Equal baseline pitch ≠ equal visual gap.** Actual glyph ink varies
   line to line — a line with descenders (g/y/p) reaches lower than one
   without — so a mathematically uniform line-height does *not* produce
   a uniform-looking gap between lines, and gets worse once a bigger
   lead-styled font is mixed into just one row. The fix measures each
   line's *real* rendered ink extent via `textbbox` (not generic font
   ascent/descent) and positions every line so the gap from one line's
   actual ink-bottom to the next line's actual ink-top is identical
   throughout — always measured against the base body font, even on
   the row that also carries the bold lead-in, so regular-weight-word-
   to-regular-weight-word spacing matches exactly everywhere.

3. **Baseline alignment on mixed-size lines.** The lead-in font (105 on
   the cover page, 100 on the detail page) is deliberately *larger*
   than the body font (80 / 75) — not just bolder — so a naive
   same-top-y draw leaves the lead-in floating high with its baseline
   nowhere near the body text it's inline with. Each line's true max
   ascent/descent (across whichever fonts actually appear on it) sets
   that line's baseline, and every word is drawn relative to that
   shared baseline rather than a single top-left y. This is what makes
   "Ballard Canyon sits shielded..." read as one line of text at two
   sizes, not a bold word floating above a sentence.

If you're tempted to replace this with `core.paragraph()` for
simplicity: don't, unless the deck genuinely doesn't need the carve-out
shape — `paragraph()` doesn't take an obstacle and will overlap the
bottle.

**`para1`/`para2` on the cover page call `wrap_around` with
`obstacle=None`** — they're meant to sit entirely above the benchmark
bottle, not carve around it, so there's no obstacle to pass. That
means nothing stops them from silently running into the bottle if the
copy gets too long — Field Guide's `!body` box exemption pattern
wouldn't have caught this either. Two non-exempt QA checks close that
gap instead: one directly compares the paragraph text's final y against
the bottle's top edge, the other compares the dashboard's final y
against `CONTENT_BOTTOM`/the footer. Both raise a real `FAIL`, not a
silent pass — if you extend para1/para2 copy and the build starts
failing on `paragraph-overlap` or `dashboard-footer`, that's the system
working as designed, not a bug to route around. Shorten the copy, or
reduce `bottle_h` (see §6) and re-check both constraints together.

---

## 6 · The two modules

Slot schemas are authoritative in `quick_sips.py` docstrings.

| Function | Job | Signature slots |
|---|---|---|
| `quick_sip_cover` | Page 1: hero photo, left-anchored title+tagline, two run-in paragraphs, tasting dashboard, benchmark bottle bottom-right | `photo, photo_caption, photo_credit, title, tagline, para1, para1_lead_words, para2, para2_lead_words, structure[(label,frac,descriptor)], bottle_h, dashboard_gap, bench_*` |
| `quick_sip_detail` | Page 2: headline, body copy around a second benchmark bottle (optionally with its own bold lead-in), compact tasting/structure dashboard | `topic, headline, photo, photo_h, photo_caption, photo_credit, content_pad, body, body_lead_words, body_lead_size, bench_*, structure[(label,frac,descriptor)]` |

**Component builders** (used by both, documented in `quick_sips.py`):
`qs_mark_overlay` / `qs_mark_patch` (corner brand), `qs_stat_strip`
(legacy), `qs_benchmark_bottle`, `qs_tasting_dashboard`.

**Cover page defaults (the standard, as of this revision):**
`title_size=110`, `title_align="left"`, `tagline_size=80`
(`tagline_align` defaults to `title_align`), `bottle_h=1185`,
`dashboard_gap=70` (vertical gap between para2 and the tasting
dashboard). `para1_lead_words`/`para2_lead_words` default 3/2. None of
these need to be set explicitly for a deck that matches the reference
proportions — they're only there to override.

**The `dashboard_gap` / `bottle_h` / paragraph-length relationship is
the one real judgment call left in this layout**, and it's a closed
system: longer para1/para2 copy pushes the dashboard's start further
down; a larger `dashboard_gap` does too; and `bottle_h` controls how
much vertical room exists before the bottle lockup *and* how much room
its caption note has before the footer — shrinking the bottle buys
paragraph room but costs caption room, in opposite directions. There
is no formula to compute the right number in your head; when copy
changes, rebuild and let the two non-exempt QA guards (§5) tell you
whether it fits, and adjust `bottle_h` (or trim copy) from there. The
reference deck's working numbers (`bottle_h=1185`, two-sentence para1,
one-sentence para2, a two-line bottle note) are a good starting point
for a deck with similar copy length, not a guarantee for longer copy.

The cover page's dashboard also renders at slightly tighter internal
spacing (`header_gap=50, pre_row_gap=18, row_gap=12`, hardcoded in
`quick_sip_cover`) than the detail page's default
(`header_gap=58, pre_row_gap=26, row_gap=22`) — this is what makes room
for `dashboard_gap=70` without pushing past the footer. If a deck's
cover-page copy is short enough that the compact spacing isn't needed,
it's fine to loosen it, but the two pages are allowed to look slightly
different here; they don't need to match each other's dashboard
rhythm exactly.

**Legacy slots** (pre-dating this revision, still fully supported):
`eyebrow`, `stats[3x(num,label)]`, `standfirst`, `subtitle`,
`facts_line`, and the single `body`+`lead_words` path (used only when
`para1`/`para2` are both absent — wraps around the bottle obstacle
instead of sitting above it, and defaults to the old `title_size=200`,
`title_align="right"` look *only if you also pass those explicitly* —
the coded defaults are now 110/"left" regardless of which body path is
used, so a legacy-style deck should set `title_size=200,
title_align="right", tagline_size=60` explicitly to reproduce the
original series look).

**`qs_tasting_dashboard`** — a tight, spec-sheet-style stack: thin
hairline-track bars (not thick pills), one row per attribute, sized to
sit compactly beside the bottle lockup rather than stretching down the
page. Takes optional `header_gap`/`pre_row_gap`/`row_gap` overrides
(see above). The detail-page dashboard positions itself at
`max(end_y + 40, obstacle_top)` so it never collides with wrapped body
copy above it.

**`footer(..., page_pos=...)`** — page-number position is configurable
("left"/"right"); both Quick Sips pages currently use `page_pos="left"`
to keep the page number near the swipe cue rather than opposite it.

### 6.1 · Corner mark — standing rule

The Quick Sips wordmark + wine-glass glyph (top-left, every page) is
the one piece of visual identity that must never change deck to deck.
**Page 2 onward always reads `"Quick Sips - {topic}"`** via
`qs_mark_patch(..., topic=slot["topic"])` — this is how the topic name
is displayed on interior pages. Do not add a separate topic
heading/eyebrow elsewhere on the page; the mark carries it. Page 1 uses
`qs_mark_overlay` (photo-background variant, no topic suffix — the big
title below it already carries the topic).

The glyph is the Lucide `wine` icon (lucide.dev, ISC licensed, free for
commercial use, no attribution required), rasterized in two tones —
white for photo/dark backgrounds, ink for the plain paper background
(a white icon there would be invisible). **See §6.4 — the actual PNG
assets were broken (flat RGB, no transparency) as of this revision,
independent of the white/ink tone logic described here; that's now
fixed at the asset level, not just in this tone-selection code.**

### 6.2 · Benchmark bottle

Every Quick Sips deck names one benchmark bottle per page — "The
Classic" on page 1, a second angle (e.g. "Top Value") on page 2, or
whatever framing suits the topic. Sourced bottle photos should have (or
be keyed to have) a transparent background; `qs_benchmark_bottle` crops
to the opaque bounding box automatically so bleed math is measured
against the real bottle silhouette, not a padded product-photo canvas.

**Caption stack order (as of this revision): heading, then producer,
then wine name, then note** — producer (italic, `QUICKSIPS_GOLD`) reads
above the wine name (italic bold, `INK`), not below it. This was a
deliberate reversal from the original layout (wine name first);
`qs_benchmark_bottle` is a shared function, so this order applies to
every deck automatically, on both pages, with no per-deck flag needed.

### 6.3 · Photo captions and content spacing (new this revision)

Neither page had any way to caption its hero photo before — added
`photo_caption` to both. On the cover, it renders bottom-**right**
inside the photo (not bottom-left, the usual Field Guide default —
the cover's title/tagline stack is left-aligned and already occupies
the photo's bottom-left, so a bottom-left caption would collide with
it). On the detail page, it renders bottom-right too, with its own
small scrim behind it for legibility, independent of whatever else is
happening in that photo.

`quick_sip_detail` also gained `content_pad` — the vertical gap
between the photo (or corner mark, if no photo) and the headline that
follows it. Previously hardcoded to 60px; now a slot override, for
decks that want more separation between the photo and the text below
it. Both additions are purely additive — omitting them reproduces the
exact previous layout.

### 6.4 · The wine-glass icon asset was genuinely broken, not missing

`_qs_glass()`'s docstring calls the icon "the Lucide `wine` icon
(lucide.dev), ISC licensed" and describes two pre-rendered tones. As
of this revision, **every copy of both `QS_glass_icon.png` and
`QS_glass_icon_ink.png` across the whole project was a flat RGB file
with no alpha channel at all** — not a missing-file problem, a broken
one. The rendering code does `Image.open(path).convert("RGBA")` and
pastes using the result's own alpha as the mask; converting a
flat-RGB image to RGBA just adds a fully-opaque alpha channel, so the
entire bounding box pastes as a solid rectangle — this is what "the
glass icon is just a white block" actually was. Re-copying the file
from elsewhere in the project does not fix this, because every copy
was the same broken asset.

**This is the second time this exact bug has been found and "fixed."**
A prior revision of this document claimed it was caught and repaired
by fetching the real SVG from `lucide-icons/lucide`'s GitHub repo. By
this session, both files were broken again — either that fix never
actually got saved back, or it got overwritten by an older asset copy
somewhere along the way. **This time the fix used a different, more
verifiable method:** rather than re-fetching an external SVG (which
worked before and evidently didn't stick), the white-tone icon was
reconstructed *from the ink-tone file*, which still had real content
(dark linework on a white background) even though the white-tone copy
didn't. Built a genuine alpha mask by thresholding the ink variant's
grayscale value (dark pixels → opaque, white background → transparent)
and used that same mask to generate both a corrected ink version and a
corrected white version. **Verified the fix actually worked** by
checking the resulting alpha mask's per-row width profile forms a
real glass silhouette (narrow base → wide bowl → narrow stem → wide
foot, not a uniform rectangle) — not just that the alpha channel
existed, since a broken mask with *some* transparency could still pass
a shallower check. If this breaks a third time, check whether
something in the save-back or asset-sync process is reintroducing an
older flat-RGB copy, since two independent fixes have now failed to
persist.

### 6.5 · Caption/dashboard alignment and the widened-dashboard geometry model

Two elements sit side by side on both pages: the benchmark-bottle
caption (heading/producer/wine/note, drawn by `qs_benchmark_bottle()`)
and the tasting-structure dashboard (drawn by `qs_tasting_dashboard()`).
Making their tops align, narrowing the caption to a fixed width, and
widening the dashboard into the freed space required real restructuring
on both pages — the two pages solve it differently because of a
structural difference between them, not by choice:

**Cover page (`quick_sip_cover`, the para1/para2 path):** para1/para2
render with `obstacle=None` — they don't wrap around the bottle, they
just have to end before it. This means the dashboard's vertical
position can be computed *first*, from `end_y + dashboard_gap`, with no
dependency on the bottle at all. The fix: compute that position
(`shared_top`) before calling `qs_benchmark_bottle()`, then pass it in
as `cap_y_override` so the caption is drawn starting at that exact y
instead of computing its own position from the bottle's geometry. Both
elements now share one anchor by construction — there's no way for them
to drift apart on this page.

**Detail page (`quick_sip_detail`):** the body paragraph *does* wrap
around the bottle obstacle (`wrap_around(..., obstacle=obstacle)`) —
a real dependency the cover page doesn't have. The bottle has to be
positioned *before* the body text can even be laid out, so the
cover page's "compute the anchor first" approach doesn't work here.
Instead, `qs_benchmark_bottle()` now returns the caption's actual
rendered top as a third value (`cap_y`, distinct from `obstacle_top`),
and the dashboard is positioned at exactly that value. This is where
the real bug was: the dashboard used to be positioned via
`max(end_y + gap, obstacle_top)`, and `obstacle_top` is
`min(bottle_top, cap_y)` — the smaller of the caption's top *and* the
bottle image's own top edge, computed that way specifically so
`wrap_around()` has a single rectangle to carve body text around
(which correctly needs to account for the bottle's full extent, not
just the caption). Using that same combined value to position the
*dashboard* was the mistake — whenever the bottle's own top sat higher
than the caption text (common with a tall, narrow bottle), the
dashboard aligned to the bottle instead of the caption, and the two
visibly diverged. `obstacle_top` is correct for wrap-around carving and
wrong for caption alignment; they are not interchangeable, despite
both nominally meaning "top of the bottle-adjacent stuff."

**Width limit and widened dashboard:** `cap_w` (default 500, this
reference deck runs 400) controls the caption column's width directly.
`qs_tasting_dashboard()`'s own width (`dash_w = obstacle[0] - M - 40`)
is derived from where the caption sits — narrowing `cap_w` moves the
caption's left edge right, which automatically grows `dash_w` into the
freed space with no separate width parameter needed. Confirmed via
direct instrumentation (not visual inspection) that dropping `cap_w`
from ~650–1050 down to 400 grew the dashboard from roughly 500–650px
to 836–1081px on the two pages of the reference deck.

**`cap_gap` (default 36) is the horizontal buffer between the caption
column and the bottle photo itself.** This reference deck runs it at
120. Widen this first if a caption is crowding a bottle's neck — the
neck is narrower than the body/shoulder the caption's clearance is
calculated against, so a collision there usually means the *vertical*
position of the caption has shifted into the neck's height range, not
that the horizontal gap is literally insufficient; widening the gap is
a safe first response but check the vertical positioning too if it
doesn't fully resolve it. **`qs_benchmark_bottle()`'s heading argument
does not auto-wrap** — `for ln in heading.split("\n")` is the entire
line-break logic. If a heading is crowding the bottle, the fix is
either a manual `\n` at a specific word (which changes which words
occupy which vertical rows, potentially moving the collision), or
accept that a word already on its own natural line won't move by
adding a no-op `\n` in the same place text already breaks.

**`bottle_h` direction is easy to get backwards.** Both pages
bottom-anchor the bottle (`bottle_bottom = page_bottom + bleed_bottom`,
fixed), so **larger `bottle_h` moves `bottle_top` UP** (a bigger bottle
extends further up the page) and **smaller `bottle_h` moves it DOWN**
(a smaller bottle sits lower, closer to the page bottom). This is the
opposite of the intuitive "bigger number, lower/later" assumption, and
got reversed by mistake multiple times this session. On the cover page
specifically, since the caption now aligns to `shared_top` (paragraph-
driven) rather than the bottle, changing `bottle_h` no longer affects
caption/dashboard position at all — it only changes the bottle's own
size and, on the detail page, the paragraph-overlap headroom. Don't
reach for `bottle_h` to fix a caption/dashboard positioning issue on
the cover page; it does nothing there anymore.

---

## 7 · Content discipline

- **Exactly two slides.** Not a range like Field Guide's 8–12 — Quick
  Sips is always a cover + a detail page.
- Word budget is **130 per slide**, not Field Guide's 70 (denser
  infographic format): set via `qa.max_words = 130` at the top of each
  module function.
- Include a couple of named producers/bottles when the topic is a
  region — the benchmark-bottle lockup is built for exactly this.
  Include stats/figures an Advanced Sommelier or CSW exam would expect
  (DOCa/DO status and dates, ABV range, key distances — not filler
  numbers).
- Facts sourced from the CSW Study Guide / WSET L3 references in
  project knowledge, same as Field Guide. Producer and bottle names are
  common industry knowledge, same convention as Field Guide's Famous
  Names.

---

## 8 · QA harness

Same `QA` class, same mechanism as Field Guide (`core.py`) — sizes,
boxes, words, contrast, all enforced automatically. Two exemption
patterns are used deliberately and consistently in this series:

- **`"!"`-prefixed size labels** (e.g. `"!bench_caption_sz"`) — exempt
  from *both* the type-floor check and the headline-vs-body hierarchy
  check (`core.py`'s `report()` filters `"!"`-prefixed labels out of
  both). Used for the bottle caption note (floor exemption), and for
  the cover-page title/lead-in sizes (`"!title"`, `"!para1_lead"`,
  `"!body_lead"` on the detail page) — the new standard intentionally
  runs the headline-vs-body gap tighter than Field Guide's default
  margin, so these are exempted from the hierarchy check specifically.
  A "!"-prefixed size is still a real number rendered at that size —
  the prefix only tells the QA harness not to flag it; it's not a way
  to silently shrink type below what the deck actually needs.
- **`"!"`-prefixed box labels** (e.g. `"!body"`, `"!dashboard"`) —
  exempt from the caption-zone check. Used for the wrapped body text
  (allowed to run close to the page bottom) and the tasting dashboard.

**Two checks added this revision are deliberately *not* exempt**, since
they exist specifically to catch the failure modes that showed up
building the reference deck:

- **`paragraph-overlap`** (cover page only) — fails if para1/para2's
  combined text extends past the benchmark bottle's top edge. Because
  those paragraphs render with `obstacle=None` (§5), nothing else would
  catch this.
- **`dashboard-footer`** (cover page only) — fails if the tasting
  dashboard's bottom edge passes `CONTENT_BOTTOM`. The dashboard's own
  box is `"!dashboard"`-exempt (shared with the detail page, which can
  legitimately run close to the bottom), so the cover page checks this
  directly rather than relying on that box.

If either of these fires, the fix is the same either way: shorten
para1/para2, or reduce `bottle_h` — see the relationship note in §6.
Do not silence either check with an exemption prefix; that's exactly
the silent-overflow failure mode they were added to prevent.

`qa.word_limit` is overridden to 130 per module (vs. the `MAX_BODY_WORDS
= 70` default in `tokens.py`) — this override mechanism already existed
in `QA.__init__` before Quick Sips needed it.

**Three fixes made this session, same root causes as the Field Guide
fixes logged in LESSONS_LEARNED_v5 §9:**
- **Cover title and detail headline had no overflow protection at all**
  — both drew a single unbounded line at a fixed size (`title_size`/110
  respectively) with no width check, so a long title/headline could run
  straight off the canvas edge. Both now shrink in small steps until they
  fit `W - 2*M`, with a floor at `FLOOR` (60) — mirrors the identical fix
  applied to `core.headline()` (which Quick Sips does *not* use; it has
  its own separate renderers, so this had to be fixed independently here).
- **`qs_benchmark_bottle()`'s photo loading bypassed `core.load_photo()`
  entirely** (`Image.open(...).convert("RGBA")` directly, not through the
  shared loader), so it never got the EXIF-rotation fix made to
  `load_photo()` this session. A phone-photographed bottle with rotation
  metadata would render sideways. Fixed by applying
  `ImageOps.exif_transpose()` directly at this call site too.
- **Stat-strip labels and the cover eyebrow were forced ALL CAPS** via
  `.upper()`, independent of the Field Guide series' own kicker
  convention. Removed to match the system-wide Title Case change (see
  §3 above and STYLE_GUIDE_v5 §3).
- Both `quick_sip_cover` and `quick_sip_detail` now accept an optional
  `photo_credit` slot, threaded through to `_finish()` — neither did
  before, so a licensed benchmark-bottle photo had no way to carry
  attribution.

---

## 9 · Regression protocol

Same protocol as Field Guide, parallel files: `reference_quick_sips/`
holds frozen reference renders, `QUICK_SIPS_REFERENCE_HASHES.txt` holds
their SHA256. At the start of any session touching `core.py`,
`tokens.py`, or `quick_sips.py`: rebuild the reference deck and diff
against `reference_quick_sips/` — any divergence is drift, resolve
before starting real deck work. After an approved system change,
re-freeze both this hash file *and* Field Guide's `REFERENCE_HASHES.txt`,
since `core.py`/`tokens.py` are shared — a Quick Sips change can
silently affect Field Guide and vice versa.

**Hashes are stale again as of this save-back and need re-freezing
before the next Quick Sips build.** This revision touched
`quick_sips.py` extensively (§6.5, §8) and `modules.py`
(`_finish()`'s new `footer_label` param, shared with Field Guide).
None of this has been re-frozen against any reference deck. Rebuild
all three reference decks and re-freeze before trusting a diff against
them.

**`quick_sips_russian_river.py` is now the primary reference deck**,
promoted explicitly this revision — not a silent convention, a direct
instruction. It's the only deck exercising the full current feature
set: aligned caption/dashboard tops (§6.5), the narrowed-caption/
widened-dashboard geometry, `title_color`/`title_contrast_bg`/
`title_chip`, `footer_label` suppression on the last page, WSET Level
3-only tasting descriptors (no flavor language — see below), and cited
critic reviews. Copy its structure for the next new Quick Sips deck
before reaching for either older reference.

`quick_sips_volcanic_whites.py` (white wine, 5-row dashboard, no
Tannin) and `quick_sips_ridge_zinfandel.py` (red wine, 6-row dashboard
with Tannin) remain valid **secondary** references specifically for
their dashboard row shape — use whichever's wine color matches the new
deck. Both predate the alignment fix and the narrowed-caption geometry
in §6.5, so don't copy their `cap_w`/`bottle_h`/positioning values
directly; copy `quick_sips_russian_river.py`'s approach to sizing
those instead, and only fall back to the older decks for the row-count
question.

**Tasting-note content standard, set by this revision:** structure-
dashboard descriptors use WSET Level 3 Systematic Approach to Tasting
terms only (Dry/Off-Dry/Medium-Dry/Medium-Sweet/Sweet/Luscious;
Low/Medium-/Medium/Medium+/High for Acidity, Tannin, Body, Intensity;
Low/Medium/High for Alcohol) — not descriptive flavor language like
"zesty" or "nearly full." Keep flavor language in the prose note
instead. Any specific score cited in a bench_note must name the critic
or publication, and must be honest about which vintage it actually
applies to if it doesn't exactly match the bottle pictured — this
reference deck's Chardonnay note cites a score from a different
vintage than the one shown, and says so explicitly rather than implying
otherwise.

If `quick_sips_priorat.py` or `quick_sips_santa_ynez.py` still exist
anywhere in the project, neither is a valid current reference —
`santa_ynez` never actually existed despite being documented as the
reference in earlier revisions of this file (a real, undetected gap,
not a renaming), and `priorat` reflects the pre-v5 legacy layout
(large right-aligned title, single wrap-around body path, wine-name-
before-producer caption).

## 10 · File map

```
styleguide/
  tokens.py               ← every number in this spec AND STYLE_GUIDE_v4.md — shared
  core.py                 ← canvas, fonts, text/photo helpers, QA, wrap-around engine — shared
  modules.py               ← Field Guide's 17 layouts + _start/_finish (shared by both series)
  quick_sips.py            ← the 2 Quick Sips modules + component builders
  quick_sips_russian_river.py   ← PRIMARY reference deck / regression baseline (current)
  quick_sips_volcanic_whites.py ← secondary reference (5-row/white dashboard shape)
  quick_sips_ridge_zinfandel.py ← secondary reference (6-row/red dashboard shape)
  quick_sips_priorat.py    ← superseded reference deck (pre-v5 legacy layout, if present)
  build.py                 ← Field Guide manifest → deck (QA-gated)
  reference/                ← Field Guide frozen regression renders
  reference_quick_sips/     ← Quick Sips frozen regression renders
  REFERENCE_HASHES.txt            ← Field Guide hash freeze
  QUICK_SIPS_REFERENCE_HASHES.txt ← Quick Sips hash freeze
  fonts/  photos/           ← shared assets
```
