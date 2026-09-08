# FIELD GUIDE STYLE SYSTEM — v5.0

**Rebuilt from first principles after the Super Zone (Southeast Australia)
build cycle.** Read `LESSONS_LEARNED_v5.md` before changing anything here —
every rule in this document exists because something specific broke without
it. This isn't a new design language; it's the same locked aesthetic with
the actual failure points closed.

**The operating manual for every Field Guide carousel deck.**
This is one of **two series** built on this system. Field Guide is the
10–12 slide deep-dive carousel documented here; **Quick Sips** is the
2-page focused-topic post — see `QUICK_SIPS_STYLE_GUIDE.md`. Both
share `tokens.py` and `core.py` (canvas, safe zones, fonts, the QA
harness, the product-photo pipeline); each has its own module file
(`modules.py` / `quick_sips.py`) and its own visual language. A change
to `tokens.py` or `core.py` affects both series — re-freeze both series'
reference hashes after any such change (§9 here, §9 there).

Rules live in code (`tokens.py`, `core.py`, `modules.py`), not on paper: every number
below is enforced automatically at build time. A QA failure aborts the build.

**A note on how this revision came about:** v4.2 was assembled by
merging two branches of work that had drifted apart without either
side knowing it — the v4.1 feature set (`editorial_lead.table`,
`side_rail.lists`, `atlas` markers/outlines/legend rebuild,
`mosaic.overlay_title`, `photo_quote`, `SHELF_RULE`, showcase_shelf
wrapping) and a full deck-build session's worth of fixes and new
capabilities that were never folded back into the project's canonical
`modules.py`. If you're starting a new working session, **diff your
working copy against the project's checked-in files before assuming
either one is current** — this exact gap is what produced v4.2's merge
work, and it will happen again if module edits stay session-local.

**v4.2 changelog** (this revision, on top of v4.1):
- **Headline color is now locked system-wide.** Every module's page
  headline renders in the deck's `SIGNATURE` color, not black —
  applies to all 18 modules, not a per-deck choice (§3).
- **`statement`'s cover/closing kicker is locked to "THE FIELD GUIDE"**
  in `ACCENT` (deep gold), not a per-deck slot value — the series'
  cover-to-close bookend branding (§3, §7).
- **The swipe arrow was fixed: `←`, not `→`.** It points in the
  swipe gesture direction, not toward the next slide's content (§6).
- **Photo credits moved off the photo, into the footer gutter**
  (`footer`'s `credit` param, threaded through `_finish`) — a
  photographer/license line no longer overlays the image itself.
  `side_rail` is the one exception (photo occupies a full-height rail,
  so its credit renders in the text column instead — see its
  docstring) (§5, §7).
- **Photo captions default to bottom-left, inside the image** (was
  right-aligned) (§5).
- **`card_grid` gained `row_layout`** for card counts other than a
  clean 2×2 (e.g. 5 cards as 3-over-2), with row heights weighted by
  column density (§7).
- **`showcase_shelf` gained `zone_h`/`width_frac`/`show_note`/
  `note_size`/`stretch_lower`** for running product photos
  meaningfully larger than the v4.1 default (§7).
- **New module: `euler_nesting` (M18)** — true nested-set containment
  diagrams (branching, siblings, named exceptions), which `ladder`'s
  single-path pyramid can't represent (§7).
- **New shared helper: `famous_names()`** — fixes a real bug where the
  old inline famous-names code shrank type toward the floor and then
  let text overflow anyway once it still didn't fit; now wraps to
  multiple lines instead (§7, §8).
- `stat_wall` and `fact_file` gained `famous` support (previously
  `side_rail`-only).

**v4.1 changelog** (prior revision): `editorial_lead` gained a `table`
slot and a `band_h` override; `side_rail` gained a `lists` slot; `atlas`
gained `outlines`, `markers`, `map_h`, and a rebuilt three-block legend
with optional per-entry color; `mosaic` gained `overlay_title` and
captions on small photos; `showcase_shelf` now wraps product name/
style/origin instead of truncating, and draws a synthetic shelf shadow;
the QA harness gained a per-slide `word_limit` override and extended
its `!`-exemption convention to the type floor. Full detail in §7 and §8.

---

## 1 · Purpose & workflow

A new deck is a **manifest**, not a design project. The workflow:

1. Choose modules from the 17-layout menu (see §7 / the Specimen Deck).
2. Fill each module's named slots with text and photo filenames.
3. `python3 build.py` → QA runs inside every module → PNG set + PDF.

No layout decisions, no font choices, no spacing judgment calls per deck.
If content doesn't fit, **cut copy** — never shrink type or squeeze geometry,
*unless* the person explicitly approves a specific exception (§8, `!`-exemptions).

```python
from build import build_deck
MANIFEST = dict(
    palette=dict(SIGNATURE=(114,47,55), ACCENT=(168,122,36), LEAD=(140,92,24)),
    slides=[("statement", {...}), ("editorial_lead", {...}), ...],
)
build_deck(MANIFEST, out_dir="out", name="My_Deck")
```

---

## 2 · Canvas & safe zones

| Token | Value | Rationale |
|---|---|---|
| Build canvas | **2160 × 2700** (4:5) | Portrait earns 12–15% more feed engagement |
| Export | 1080 × 1350 PNG | PNG for text-heavy slides |
| Side/top margin `M` | **120 px** (60 @1080) | Published safe-zone standard |
| `CONTENT_BOTTOM` | **H − 200** (was H−400) | Instagram caption preview can cover the bottom ~200 @1080. Content never below; footer furniture only. **Changed from H−400 per standing preference** — the person explicitly asked for a smaller default bottom margin (more usable content area) across all layouts; exceptions to *this* new boundary still use the `!`-prefix convention. |
| Grid-crop zone | central 2160² | Profile grid crops 4:5 → 1:1; covers keep the title payload central |
| Deck length | 8–12 slides | 7–10 is the engagement sweet spot; hard bounds enforced |

Full-bleed photography may run to the canvas edge (statement slides, stripes,
mosaic); *text content* may not cross `CONTENT_BOTTOM` (QA: `caption-zone`).

---

## 3 · Type ramp (locked)

One ramp, no per-deck drift. All sizes at build scale.

| Role | Face | Size | Use |
|---|---|---|---|
| `display_xl` | Playfair Black | 220 | Cover title only |
| `display_lg` | Playfair Black | 168 | Statement words, closing toast |
| `display_md` | Playfair Black | **112** | Standard page headline |
| `standfirst_hero` | Playfair Medium Italic | 92 | Hero standfirst (one per deck max) |
| `standfirst` | Playfair Medium Italic | 74 | Standard standfirst |
| `lead` | Playfair Bold | 74 | Serif run-in lead |
| `body` | Archivo Medium | 64 | Body text |
| `caption` | Cormorant Italic / Archivo Cond | **60 = FLOOR** | Captions, footer, micro-labels |

**Laws (QA-enforced):**
- `FLOOR = 60` — nothing renders smaller, ever, *without an explicit, visible,
  person-approved exception* (see §8 — the `!`-prefix convention now covers
  type size as well as caption-zone placement).
- `HIERARCHY_GAP = 30` — the page headline must exceed every other *text* size
  by ≥30 px. Display-class numerals (stat walls, timeline years) are exempt.
- **`core.headline()` now protects against overflow.** It used to draw at a
  fixed size with zero width-checking — a long headline would silently run
  past the canvas edge. It now shrinks in small steps until it fits the
  available width, with a floor at `standfirst size + HIERARCHY_GAP` so it
  can't collapse the hierarchy. This is a `core.py` change and applies to
  every module that calls `headline()`, not a per-slide fix. Quick Sips'
  own separate title/headline renderers (`quick_sip_cover`'s title,
  `quick_sip_detail`'s headline — neither goes through `core.headline()`)
  got the equivalent shrink-to-fit logic added directly in `quick_sips.py`.
  **This bug pattern recurred independently in `side_rail()`'s headline**
  (drew via a bare `.split("\n")` with zero width-checking) and in
  `mosaic()`'s `overlay_title` — each module that draws its own headline
  outside `core.headline()` needs its own copy of this fix; there is no
  single shared code path that catches all of them.
- **`core.wrap()` now breaks at internal hyphens when a single word is
  itself wider than the available column.** It previously only split on
  spaces, so a hyphenated compound (`"mountain-structured"`) or an
  em-dash pattern with no surrounding spaces (`"champion—blending"`) was
  treated as one unbreakable token — it would either overflow the column
  outright or, worse, silently bleed into the next column with nothing
  to stop it. `wrap()` now falls back to splitting at hyphens (keeping
  the hyphen with the preceding fragment, standard convention) whenever
  a single word doesn't fit. This recurred across several different
  slides/modules before being fixed once at the source in `core.py`
  rather than patched per-instance — check any future word-wrap-adjacent
  bug against this fix before re-deriving it.
- **`core.run_in()` had a hardcoded `"  ·  "` (double-space, middle-dot,
  double-space) separator** between the bold lead-in and the body text —
  removed; it's now a single space, matching the plain "Lead: body"
  pattern used everywhere else. `run_in()` also gained a `justify=True`
  parameter for full justification (distributes extra space between
  words so every line but the last hits the right margin exactly,
  instead of ragged-right wrapping) — off by default, so existing calls
  are unaffected.
- **All headings are mixed-case serif.** Tracked all-caps condensed sans was
  formerly reserved for kickers and micro-labels; **as of this session,
  kickers render in Title Case as given, not forced uppercase** — the
  `.upper()` call was removed from `core.kicker_block()` system-wide, plus
  the equivalent forced-caps calls in `atlas()` (state labels, inset label),
  `mosaic()`, `euler_nesting()` (exceptions label), `editorial_lead()`/
  `side_rail()` (table/list group titles), and Quick Sips' stat-strip
  labels and cover eyebrow. Supply kicker/label text in the case you want
  it to render in. The one exception below (THE FIELD GUIDE bookend) is
  still hardcoded ALL CAPS and unaffected by this change.
- **Title/headline copy is authored in Title Case, never ALL CAPS (v5.1).**
  This extends the rule above to `statement`'s cover/closing `title` slot
  and any other manifest copy a person types directly — the system
  doesn't force-uppercase these, so a deck author typing
  `"A RANKING FROM 1855."` ships shouting-case type because nothing
  catches it, not because the design calls for it. Supply title copy in
  the case you want it to render in (Title Case for headline-weight
  type). The `THE FIELD GUIDE` cover/closing kicker remains the one
  deliberate, hardcoded, locked exception (see above).
- **Every page headline renders in the deck's `SIGNATURE` color, not
  black.** Locked as of v4.2, system-wide, across all 18 modules — not
  a per-deck or per-module choice. If you add a 19th module, its
  `headline()` call needs `fill=pal["SIGNATURE"]` explicitly; the
  shared `headline()` helper's own default is still black, by design,
  so this has to be passed at every call site rather than flipped
  globally in `core.py` (a module that genuinely wants a black
  headline — unlikely, but not impossible — can still get one by
  omitting the `fill` argument).
- Cover/closing subtitles: Playfair **Bold Italic**.
- The serif **run-in** is the canonical body pattern: Playfair Bold lead +
  interpunct + Archivo body, baseline-aligned, body wraps full measure.
- **`statement`'s cover and closing variants always show "THE FIELD
  GUIDE" as the kicker, in `ACCENT` (deep gold).** This is the series'
  cover-to-close bookend branding — locked in the module itself as of
  v4.2, not read from a per-deck `kicker` slot at all. See §7.

---

## 4 · Color

**Fixed neutrals — never change:**
`PAPER (251,249,244) · INK (38,33,38) · MUTED (110,96,104) · LINE (231,222,207)`

**New in v4.1:** `SHELF_RULE (196,190,182)` — a light warm grey, deliberately
softer than INK, used specifically for the horizontal shelf line in
`showcase_shelf`. Locked in project-wide: every showcase_shelf slide, in
every deck, uses this rule color going forward, not a one-off per-deck choice.

**Per-deck slots (set once in the manifest):**
- `SIGNATURE` — the deck's identity color (headlines' accents, nodes, tiers)
- `ACCENT` — secondary warmth (kickers, rules, famous-names furniture)
- `LEAD` — serif run-in lead color (a bronze/deep tone near SIGNATURE)

WCAG contrast is a QA check: 4.5:1 body, 3:1 display. Text over photography
always sits on a graduated scrim; pale tints (e.g. pale sage `(200,224,194)`,
cream `(233,206,152)`) are the approved photo-overlay text colors.

The **tri-band flag stripe is reserved for country-guide decks** and is off by
default. Corner ticks are retired permanently.

**Region/legend color-coding (atlas):** when a map groups regions into
families (e.g. north/central/south), give each family one base color and
express sibling regions as tints/shades of that same hue — don't assign
arbitrary distinct colors per region. Tie any legend header directly to its
family's base color so the reader can match map to legend by color alone.
Check header text against `PAPER` at whatever size you use it — a color
that reads fine as a small map fill can fail contrast at headline size.

---

## 5 · Photography

- Band heights: **720** (tall band, default) or full-bleed. A module may
  expose a `band_h` override (currently `editorial_lead`) for a data-dense
  slide where the photo is a secondary accent rather than the subject —
  use sparingly; a photo under ~200px stops reading as a real image.
- Multi-image rows are **continuous stripes** — images run into each other with
  2 px paper seams; no gutters, no floating thumbnails.
- **Captions are geographically honest.** No regional attribution without
  confirmed provenance; generic captions ("New World vineyard") when unsure.
- Aim 33–40% of slides people-forward; always show the *subject* (a winemaker
  visible at the tanks, not an ambiguous machinery crop).
- Every photo caption: Cormorant Italic 60, on-scrim white, **bottom-left
  default** as of v4.2 (was right-aligned in v4.1 — flip `cap_align="right"`
  only for the rare case a caption genuinely needs the other corner).
  Captions wrap to the photo's own width; a caption that doesn't wrap
  will run past the image edge on any band narrower than full-canvas
  (e.g. `side_rail`'s rail) — this was a real bug, not a hypothetical.
- **Photo credits (photographer name, license link) do NOT overlay the
  photo.** As of v4.2 they render in the slide's footer gutter,
  centered between the swipe cue and the page number, via `footer()`'s
  `credit` param (threaded through `_finish(..., credit=...)`). Small
  print, 34px, `MUTED`. The one exception is `side_rail`: its photo
  occupies a full-height half of the canvas, so a credit centered on
  the *full* canvas width can land on or right at the image edge —
  `side_rail` instead draws its credit directly in the text column,
  wrapped to that column's width. If you add photo-credit support to a
  new module, check whether its photo is full-width (use the generic
  footer gutter) or occupies only part of the canvas (confine the
  credit to the clear area instead, the way `side_rail` does).
- **`load_photo()` now handles EXIF rotation and transparency correctly —
  fixed at the source, not a manual workaround.** Two real bugs shipped
  and were fixed this session: (1) phone photos with EXIF rotation
  metadata were displayed sideways/upside-down because PIL doesn't
  auto-apply it; `load_photo()` now calls `ImageOps.exif_transpose()`
  on every load. (2) `load_photo()` used to force RGB via a bare
  `.convert("RGB")`, which drops alpha and keeps whatever RGB value sat
  underneath a transparent pixel — for a plain white-background photo
  this is invisible, but a PNG with true alpha transparency would show
  its raw (often black or garbage-colored) underlying pixels as a solid
  box. `load_photo()` now detects RGBA/LA/palette-with-transparency
  images and properly composites them onto white before converting.
  **For product cutouts that get pasted onto a colored page background
  (e.g. `showcase_shelf` bottles), use `load_photo_rgba()` instead** —
  it preserves transparency rather than compositing onto white, and the
  caller pastes with the returned image's own alpha channel as the mask
  (`img.paste(resized, (x,y), resized)`), so the page background shows
  through instead of a flattened white box. `core.remove_background()`
  (§8b) is unaffected by this — it already produced clean alpha.
- **Chip vs. scrim, use the right one.** `scrim()` is a gradient — correct
  for blending a photo into a caption zone below it, and *wrong* for a
  kicker or label chip that needs guaranteed contrast: the gradient is by
  design at zero strength at one edge, and a kicker drawn near that edge
  gets no protection (this exact mistake shipped once — a kicker measured
  at 184 luminance under light text, i.e. functionally invisible).
  `chip()` is a flat, uniform-opacity rectangle with no weak edge — use it
  for any standalone text that must read reliably regardless of the photo
  underneath.
- **A consistent grade across a deck's photography is a real, worthwhile
  pass**, not a nice-to-have: mixed source photos (different white balance,
  exposure, uploader) read as visibly inconsistent side by side. A single
  subtle grade — small warm shift, softened highlights above ~200, mild
  desaturation, small contrast lift — applied to every photo in the deck
  gives a "one photographer" feel. Do this once per deck, on the actual
  files, not per-slide.

---

## 6 · Content discipline

- **One idea per slide.**
- Cover hook ≤ **12 words** (a slide gets a two-second audition in feed).
- Body budget ≤ **70 words per slide** by default (QA: `word budget`) —
  overridable per-slide via `word_limit` (see §8) when a person explicitly
  wants a data-dense page to carry more.
- ~50–60% of every slide is photography or whitespace. Never fill vertical
  space because it exists.
- Page furniture on every slide: kicker top-left with accent rule (content
  slides), footer `SWIPE ←` left / `NN/NN` right at 60 px — the arrow
  points in the swipe *gesture* direction (finger moves left to advance
  a carousel), not toward where the next content visually sits. This
  was wired backwards for a while (`→`); if you ever see a `→` default
  anywhere in `core.py`, that's the bug, not a valid alternate style.
- **Facts and figures need a named, dated source.** When a slide states
  acreage, production figures, or similar hard data, cite the source
  (organization + report + year) in a caption-sized line on the slide
  itself, not just in production notes. `editorial_lead`'s `table` slot
  has a dedicated `source` field for this.

---

## 7 · The nineteen modules

Slot schemas are authoritative in `modules.py` docstrings; the Specimen Deck
renders one slide per module and doubles as the visual menu + regression
baseline. **The full, code-verified slot list for every module is below** —
extracted directly from what each function reads, not reconstructed from
memory, so it won't drift out of sync with the code again.

| # | Module | Job | Slots (complete) |
|---|---|---|---|
| M01 | `statement` | Full-bleed cover / pull-quote / closing. Cover/closing kicker is locked to "THE FIELD GUIDE" in `ACCENT` — not a slot. `cover_layout="lower_left"` (kicker in the sky, title Title Case lower-left, subtitle flows below, left-aligned, both auto-wrap/shrink to fit). `cover_layout="full_bleed"` (full-page photo, no color block, kicker+title centered in the sky, subtitle across the lower portion; text color for each zone is picked from actual rendered luminance, not assumed) — default `"center"` layout unchanged. `photo_credit` reaches the footer. Closing-variant title protected against overflow. | `variant, photo, title, subtitle, quote, attribution, kicker_y(closing only), title_size(closing only), cover_layout, photo_credit, subtitle_color, subtitle_size, bottom_margin` |
| M02 | `editorial_lead` | Workhorse: band + headline + hero standfirst + run-ins, **or** a two-column data table, **or** N side-by-side vertical text blocks (`columns` mode: title stands alone, larger serif, no rule, body paragraph below), **or** a genuine cross-tabulated grid table (new `grid_table` mode: column headers across the top, row labels down the left, wrapped cells — distinct from the 2-col `table` mode above, which is really a grouped list, not a true grid). `columns` mode titles now shrink-then-wrap per-column instead of blanket-shrinking the whole row when just one title overflows, and wrap width carries an 8px safety margin so text never sits flush against the next column's gutter | `photo, photo_caption, kicker, headline, standfirst, items[(lead,body)], columns[(title,body)], col_lead_size, grid_table{col_heads, rows[(label,[cells])], label_w, col_gutter, row_gap, row_label_size, cell_size}, band_h, table, photo_credit` |
| M03 | `side_rail` | Vertical split (left **or** right rail); text column + grouped lists + Famous Names. `kicker` is now optional (was required). New `dashboard` slot reuses Quick Sips' tasting-dashboard component directly (via lazy import — `quick_sips` imports from this module, so the reverse import has to happen at call time, not load time). Item lead/body sizes and inter-item gap are now configurable (`item_lead_size`/`item_body_size`/`item_gap`) instead of hardcoded, so a text-dense slide can shrink them to fit. **Headline previously only split on manual `\n` with zero width-checking** — a long headline just ran off the text column; now wraps properly to the available width | `photo, photo_caption, photo_credit, side, kicker, headline, standfirst, items, item_lead_size, item_body_size, item_gap, lists, list_size, famous[], dashboard[(label,frac,descriptor)], header_gap, pre_row_gap, row_gap` |
| M04 | `stat_wall` | 2×N grid of display numerals, optional Famous Names | `kicker, headline, standfirst, stats[(num, label, note)], famous[]` |
| M05 | `duel` | Split-image band + 2-col table or twin columns. Table mode's `lv`/`rv` values now wrap to their own column width instead of being drawn as a single unbounded line that could visually collide with the neighboring column | `photos, kicker, headline, standfirst, labels, mode, cols, col_heads, rows, photo_credit` |
| M06 | `process_map` | Photo stripe (now 440px, `standfirst` removed to make room) + aligned flowcharts, decision diamonds, sequential number badges across all columns (caller no longer supplies numbers). Per-column pitch so columns with different step counts still align top-to-bottom. Node text shrunk + wraps within its shape instead of overflowing | `photos[3], kicker, headline, columns[(title, steps[(text,is_decision)])], photo_credit` |
| M07 | `card_grid` | Variable-row icon/flag cards (default 2×2), optional bottom stripe. New `photo_style="top"` swaps the small 84px inline icon for a large photo across the top of each card (default `"icon"` unchanged). Card subtitle/nickname font changed from serif italic to sans-serif bold | `kicker, headline, standfirst, cards[], photo_style, row_layout, bottom_stripe[], stripe_captions` |
| M08 | `showcase_shelf` | Product grid on `SHELF_RULE` shelf lines, 3×N by default, wrapped name/style/origin, synthetic drop shadow, configurable size. Bottles load via `load_photo_rgba()` and paste with their own alpha as mask (previously flattened to a white box behind any transparent PNG). **`cols` is now configurable** (was hardcoded to 3 — a 4th product silently wrapped to a second row, and with a large `zone_h` that second row could run thousands of pixels off-canvas; use `cols=4` for a single-row four-bottle lineup instead). All wrapped text fields (producer/name/style/origin/note) now carry a 14px safety margin so wrapped lines don't sit flush against the next column's gutter | `kicker, headline, products[(photo,producer,name,style,origin,note)], cols, zone_h, width_frac, show_note, note_size, stretch_lower` |
| M09 | `atlas` | Cartography: boundary, regions, leader-line labels, rivers, cities, markers, three-block legend. Cities accept an optional 4th tuple element `'left'/'right'` to flip the label off the dot. Locator inset extended: `outlines`(plural), `highlight_poly`, `label`, `marker_color`, bordered frame. **Markers overhauled**: dot radius doubled (11→22px); labels can wrap via a per-marker `wrap_w`; leader line now anchors to the top-middle of the label's first word by default (previously used the raw, unadjusted label y-coordinate, which for any wrapped label fell *inside* the text's own vertical span — visibly cutting through the letters), or a specific character via `anchor_letter` (e.g. `anchor_letter='t'` targets the actual rendered position of that letter, not just the word's center); `no_leader=True` skips the line entirely for markers that don't need one. New `lat_bands` — faded semi-transparent horizontal bands (e.g. the 30°–50° "wine belt" per hemisphere) composited over both land and sea, not hidden behind the landmass fill. New `paragraph`/`paragraph_lead` — a flowing explanatory paragraph below the map/legend (optionally with the deck's standard bold-serif lead-in via `run_in()`, including `justify` and `leading` passthroughs), which the map didn't have any way to render before (`legend` is a 3-column key-value strip, not prose). New `map_top_pad` nudges the whole map down from the title | `kicker, headline, outline, outlines[], regions[], rivers[], lakes[], cities[(nx,ny,name,side?)], context[], markers[(name,target,label,side,wrap_w,anchor_letter,no_leader)], inset{...}, legend[], lat_bands[(ny_top,ny_bot,color,alpha)], paragraph, paragraph_lead, paragraph_lead_size, paragraph_size, paragraph_gap, paragraph_justify, paragraph_leading, map_h, map_top_pad` |
| M10 | `timeline` | Chronology spine over a ghosted full-page image | `bg_photo, kicker, headline, standfirst, events[(year, title, note)]` |
| M11 | `ladder` | Classification pyramid + photo band below — single-path only, see M18 for branching. New `bg_photo` ghosts a full-bleed image behind the whole diagram, tiers drawn semi-transparent so it shows through. Tier labels shrink-then-wrap to fit their own tier width (was fixed-size, overflowed narrower top tiers); tier notes measure real remaining vertical space instead of assuming two lines always fit | `photo, photo_caption, kicker, headline, standfirst, tiers[(label, note)], bg_photo, photo_credit` |
| M12 | `lexicon_cloud` | Scattered term+gloss cloud; shelf-packed, zero overlaps, top-2 terms anchored | `kicker, headline, terms[(term, weight, gloss)], seed` |
| M13 | `spotlight` | Annotated hero, lettered chips + legend | `photo, kicker, headline, callouts[(nx,ny,letter,title,note)]` |
| M14 | `feature_trio` | Three columns: head + rule + blurb + image. New optional `footnote` reserves its own space below the images for a small full-width caption instead of competing with the photo band | `kicker, headline, features[(title, body, photo)], footnote, photo_credit` |
| M15 | `fact_file` | Key–value data rail with hairline rules, optional Famous Names | `photo, photo_caption, photo_credit, kicker, headline, facts[(key, value)], famous[]` |
| M16 | `mosaic` | One hero + 2–3 smalls, pacing breather — plain kicker chip **or** large serif overlay title (mutually exclusive — `overlay_title` skips the chip entirely; these are two different slots, not one). New `kicker_serif=True` keeps the colored chip *and* switches its font from sans (Archivo Cond Bold) to the deck's serif (Playfair Bold), for decks that want the chip treatment with serif type | `kicker, kicker_serif, hero_photo, small_photos[], captions{photo: text}, overlay_title` |
| M17 | `photo_quote` | Full-bleed photo, one large white sentence-case serif quote. `quote_size` now configurable (was hardcoded to 150) | `photo, quote, attribution, quote_size` |
| M18 | `euler_nesting` | True nested-set containment diagram — branching, siblings, named exceptions a single-path pyramid can't show | `kicker, headline, standfirst, circles[(name,cx,cy,r,parent,label_pos)], exceptions_label, exceptions_label_pos, footnote` |

### New/changed slot detail (v4.2)

**Headline color, everywhere.** Every module's page headline now
renders in `pal["SIGNATURE"]`, not black. See §3.

**`statement` cover/closing kicker.** No longer a slot — hardcoded to
"THE FIELD GUIDE" in `pal["ACCENT"]` inside the module itself, for both
the `cover` and `closing` variants (`quote` doesn't show a kicker at
all). `closing` gained two new overrides: `kicker_y` (default 1660 —
move it if your closing photo's clear/legible area sits somewhere
else, e.g. up into a sky) and `title_size` (default 198 = `display_lg`
+ 30 — the module's original toast-word size; raise it for a shorter,
punchier closing word like "Cheers!").

**`side_rail.photo_credit`.** Renders in the text column (not on the
photo — see §5), wrapped to that column's width, anchored to sit just
above the footer row.

**`card_grid.row_layout`** — e.g. `[3, 2]` for 5 cards as 3-over-2
instead of forcing a 2×2 grid. Row heights are weighted by column
count (a 3-column row gets more of the vertical budget than a 2-column
row on the same slide), since a narrower column wraps its body text to
more lines and needs the room. Omit `row_layout` for the original
even-2-per-row behavior — existing 4-card decks are unaffected.

**`showcase_shelf` sizing controls** — `zone_h` (bottle image's
vertical budget; this is the actual lever for a bigger-looking bottle,
since these are tall narrow shots that are almost always
height-constrained — a wider column alone barely changes anything),
`width_frac` (bottle width cap as a fraction of column width),
`show_note` (set `False` to drop the tasting-note paragraph and hand
that space back to `zone_h` — the biggest single lever if you want
genuinely large product photos and can live without notes),
`note_size` (shrink just the note text, e.g. to 55, to buy back a
little room without losing it — needs the `!`-exemption since it's
sub-floor), `stretch_lower` (let the product blocks run past the usual
`CONTENT_BOTTOM` boundary for decks that are explicitly fine with this
slide sitting closer to the page bottom than most).

**M18 `euler_nesting`** — for true nested-set relationships, not a
ranked hierarchy. Use this instead of `ladder` when the real content
has *branching* (a parent with multiple children) and/or named items
that sit *outside* the main containment tree entirely — a single-path
pyramid literally cannot represent either of those. Caller supplies
final circle geometry (`circles=[(name, cx, cy, r, parent_name_or_None,
label_pos)]`) — the module renders it but does not compute layout, so
verify containment (child's `distance from parent + own radius <=
parent's radius`) and sibling non-overlap (`distance >= sum of radii`)
before calling. `label_pos="none"` skips a circle too small to carry a
legible label; name it in `footnote` instead so it isn't lost from the
slide's factual content. **QA deliberately does not collision-check
circle boxes against each other** — nested/sibling circles overlapping
or sitting close together is the entire point of the diagram; only
each label's actual text bounding box is checked, so real label-on-
label collisions still fail the build.

### New/changed slot detail (v4.1)

**`editorial_lead.table`** — an alternative to `items` for data-dense
content (e.g. a grape/varietal reference). Structure:
```python
table=dict(
    source="Source: <organization>, <report>, <year>.",   # optional citation line
    metric_size=50,   # optional, defaults to FLOOR; see !-exemption, §8
    name_size=60, note_size=60,  # optional, same convention
    groups=[
        ("Group Title", [(name, metric_or_None, note), ...]),
        ("Group Title 2", [...]),
    ],
)
```
Renders as up to N side-by-side columns, each with a tracked-caps group
title, an accent rule, then rows of name (bold) + right-aligned metric +
italic note, hairline-separated. Pair with `band_h` to shrink the photo
band when the table needs the vertical room — 140–200px keeps a thin but
real photo strip; below ~140px the photo stops reading as an image at all.

**`side_rail.lists`** — grouped columns (e.g. "International" vs.
"Indigenous" grape names) within the rail. Built and QA-tested; not
currently used in a live deck, kept available for reuse:
```python
lists=[
    ("Column Title", [(subhead_or_None, [(name, gloss_or_None), ...]), ...]),
    ("Column Title 2", [...]),
]
```

**`atlas.outlines`** — a list of additional closed polygons drawn the same
way as `outline` (white ground, ink border), for extra landmasses like an
offshore island. `outline` remains the primary/mainland shape.

**`atlas.markers`** — sub-region callouts distinct from the main `regions`
(e.g. a named sub-appellation inside a labeled province): small accent dot
+ thin leader + label, no fill polygon.
```python
markers=[dict(name="Cafayate", target=(nx, ny), label=(nx, ny), side="left"|"right")]
```

**`atlas.map_h`** — override the map's rendered height (default fits the
standard layout); use when a longer legend or extra markers need the map
compressed to keep the whole slide inside `CONTENT_BOTTOM`.

**`atlas` legend** — rebuilt as **up to three side-by-side text blocks**
(header + accent rule + body paragraph), not a name/value strip. Optional
third element per entry sets that block's header + rule color:
```python
legend=[("Header", "Body sentence.", (r,g,b)), ...]  # color optional, defaults to pal["ACCENT"]
```

**`mosaic.overlay_title`** — when present, replaces the plain kicker with
a 100px display headline set directly over the hero photo (top-left, with
a scrim). Use for a mosaic that needs to carry a real title rather than
just a topic label.

**`mosaic.captions`** — now applies to **any** photo in the slide (hero or
small), keyed by filename: `captions={"photo_name": "Caption text."}`.
Small-photo captions render bottom-left of their frame with a scrim.

**`showcase_shelf`** — product name/style/origin now **wrap** instead of
truncating to one line (a real fix — full producer names were being cut
off). Draws a soft synthetic drop shadow under every product before
pasting it, so mismatched source-photo lighting doesn't show. See §5 for
the mandatory pre-flattened-photo requirement.

**Pacing guidance:** open M01, close M01(closing). Alternate text-dense modules
(M02/M04/M15) with visual ones (M16/M13/M07-with-stripe). Avoid the same module
twice in a row — and avoid two data-dense modules back to back even with a
different module number (e.g. `atlas` immediately followed by an
`editorial_lead` table is still two dense pages in a row). Two consecutive
decks should share ≤3 modules.

---

## 7b · Source-Faithful Map SOP (M18 `map_facsimile`) — LOCKED v4.3

Born from the Super Zone Australia build. When a deck needs a map that
reproduces a professional reference (SWE PDF or equivalent), use
`map_facsimile`, not `atlas`. `atlas` is for schematic marker maps we
compose ourselves; `map_facsimile` is a 1:1 trace re-skinned in house
palette and fonts. The failure mode this SOP exists to prevent: importing
shapes from a second, differently-projected map and fighting alignment
errors, or redesigning label layout that the source already solved.

**The locked process, in order:**

1. **Extract vectors from the source PDF with pymupdf.** Fills → region /
   state polygons (repair with shapely `buffer(0)`, simplify 0.15pt);
   colored strokes → rivers and leader lines (match by stroke color);
   text → line-grouped label bboxes. Rasterize only for visual QA, never
   for geometry.
2. **Match label → leader → blob by nearest-endpoint distance** and
   verify each match is < ~3pt. The source's own leader lines are the
   authority on which label points at which shape. Never pair by guess,
   OCR, or a second map.
3. **One uniform fit** over the label-inclusive bounding box (+6pt pad),
   scaled to full content width. Never per-state or per-cluster
   transforms — a whole session was lost to that. Anchor sanity check:
   city dots must land inside their state outlines after the fit (use the
   source's vector dot coordinates, not its text label positions).
4. **Draw order:** state fills → rivers → region blobs → exact leader
   segments (source vectors, not recomputed) → labels centered on source
   bbox centers.
5. **Collisions are resolved only through the `nudges` dict** (px
   offsets, persisted in the deck's data file, e.g.
   `facsimile_nudges.json`) — never by silently moving, resizing, or
   dropping source elements. Phone type floor makes our labels ~1.3×
   proportionally larger than print sources, so a handful of nudges is
   expected and must be disclosed. Wide labels boxed in on 3 sides break
   to two lines (`display` override) before any sub-floor size; sub-floor
   sizes go through `sizes` and auto-register with the `"!"` exemption.
6. **Off-scope areas are ghosted, not deleted.** Exact geometry kept;
   fills drop to near-paper, labels to warm gray (`GHOST_TEXT`), leaders
   lightened, city dots muted (`ghost` flags per state/region/leader,
   `ghost_cities` list). Deleting a state changes the map's proportions
   and invalidates every position downstream.
7. **Verification is two-part:** the QA collision pass, plus the module's
   explicit edge check (QA does not catch canvas overflow — labels ran
   off both edges once while QA reported clean). When the image viewer is
   unavailable, verify numerically: box/gap report for every touched
   label, pixel sampling for fills and ink colors.

Deck files for a facsimile map: `facsimile_data.json` (all source
geometry + label bboxes), `rivers_raw.json`, `leaders.json`,
`facsimile_nudges.json`, and a short build script that assembles the slot
(see `build_slide04_map.py`, Super Zone deck). Re-extraction from the
source PDF must be reproducible from these scripts alone.

---

## 8 · QA harness (what the build enforces)

Every module registers its sizes, bounding boxes, and word counts; `QA.report()`
raises on any failure — **a deck cannot build with a violation.**

1. **Type floor** — any registered size < 60, *unless* its label is
   prefixed `!`. The `!` prefix is a person-approved exception, made
   explicit and visible in the QA log rather than silently bypassed — it
   must be a deliberate choice for a specific element on a specific slide,
   not a default. Current sanctioned exceptions: the 50px benchmark-bottle
   caption, `editorial_lead.table`'s optional `metric_size`/`name_size`/
   `note_size` when set below 60, `photo_credit`'s 34-35px footer/gutter
   text (small-print attribution is conventionally tiny, not body-reading
   text), and `showcase_shelf.note_size` when explicitly set below 60.
2. **Hierarchy law** — headline < (largest other text + 30).
3. **Collision** — any two registered boxes intersect. **Not every
   visual overlap gets registered as a box in the first place** —
   `euler_nesting`'s circles are deliberately never registered for this
   check (nested/sibling circles overlapping is the entire point of a
   containment diagram; only each circle's *label* text box is
   registered, so real label-on-label collisions still fail normally).
   If a future module has a similar "overlap is intentional" geometry,
   follow that pattern rather than disabling the check module-wide.
4. **Caption zone** — any content box crosses `CONTENT_BOTTOM`
   (`!`-prefixed boxes are spec-sanctioned exemptions, e.g. cover subtitle,
   or `showcase_shelf`'s product boxes when `stretch_lower=True`).
5. **Word budget** — body words > the slide's word limit. Defaults to 105
   (`MAX_BODY_WORDS`, raised from 70 — **+50% per standing preference**,
   same session as the `CONTENT_BOTTOM` change above) for every slide; a
   module can set `qa.word_limit = N`
   when a manifest slot explicitly requests more room (e.g.
   `editorial_lead`'s `word_limit` slot). The override is per-slide and
   visible in the QA log (`word budget: N > limit`) — it does not change
   the default for any other slide or module.
6. **Contrast** — registered fg/bg pairs below WCAG minimums.
7. **Edge bounds** (v5, automatic) — any non-`!` box extending past the
   canvas (x<0, x>W, y<0, y>H). This did not exist in v4 and a facsimile
   map shipped with labels running off both edges while every other check
   reported clean — the collision checker only compares boxes to each
   other, never to the page itself. Now automatic in every `report()` call,
   no module code required.
8. **Photo contrast** (v5, opt-in via `qa.check_photo_contrast()`) —
   samples the *actual rendered luminance* under a text box drawn on a
   photo and compares it to the text color. This is not automatic (it
   needs the rendered image, which isn't available until after drawing)
   but any module drawing text directly on a photo should call it after
   that draw. Catches what `check_contrast()`'s flat fg/bg comparison
   cannot: a scrim that looks adequate in code and measures at 175
   luminance in practice (this exact case shipped once, on white-label
   product photography where a dark theoretical scrim strength did nothing
   near-white to near-white).

**On exemptions in general:** every `!`-prefixed exemption should be a
real, deliberate choice made for a specific reason on a specific slide —
never a way to make a QA failure go away without addressing it. When in
doubt, cut copy or adjust geometry instead of reaching for `!`.

**A real bug this caught, worth knowing about:** the original inline
famous-names code (in `side_rail`, before it was extracted into the
shared `famous_names()` helper) tried to fit a joined name string onto
one line by shrinking its font down toward `FLOOR`, then simply gave up
once it hit the floor — if the names still didn't fit at 60px, the text
ran straight off the slide edge, uncaught, because the collision check
only sees registered boxes, not raw overflow past the canvas or past a
photo's edge. `famous_names()` wraps to as many lines as needed instead
of shrinking-then-overflowing. The lesson generalizes: **a shrink-to-fit
loop that stops at a floor without verifying it actually fits is not a
fallback, it's a silent failure mode** — prefer wrapping, or fail loudly,
over shrinking past the point where you've confirmed the content fits.

**Fixed-budget spacing is the single most common bug source (v5 note):**
`showcase_shelf`, `duel`'s table mode, and `mosaic`'s captions all shipped
collisions this cycle from the same root pattern — a hardcoded pixel
budget for a text stack that didn't account for every field actually
being rendered (adding a producer line broke showcase_shelf; a label
wider than its column broke duel; captions weren't wrapped at all in
mosaic). When writing a new module, measure actual rendered text height
before trusting a fixed budget, or make the budget generous enough that
realistic copy can't exceed it — don't tune it to the exact minimum that
today's placeholder copy happens to need.

### 8b · Product photo pipeline (v5, locked)

Six inconsistent ad-hoc background-removal scripts were written this
cycle before this became one tested function. **Use `core.remove_background()`
for every bottle/product photo — do not write a new flood-fill script.**

```python
from core import remove_background
trimmed, hole_frac = remove_background("build/photos/bottle_name.jpg",
                                        out_path="build/photos/bottle_name_clean.png")
if hole_frac > 0.001:
    # do NOT use the result silently -- surface this. A background that's
    # bridging into the label (common when a label's own near-white
    # background is close in value to the true background) will punch a
    # hole through the subject if you trust a naive per-pixel threshold.
    ...
```

The function already handles the two real failure modes found this cycle:
tiny bright specks inside label artwork (ignored — only the single largest
border-touching region counts as background), and a label bridging to the
true background (caught by the hole-fraction check, which itself had to be
rebuilt once — the naive version flood-fills from `(0,0)` of a *tightly
cropped* image, and after a tight crop that pixel is often right at the
subject's edge rather than truly outside it, producing false holes on
otherwise-clean images. `core._true_hole_check()` pads before flooding so
the seed pixel is guaranteed exterior. This bug once produced a confident,
wrong, and fully "verified" explanation for a defect that turned out not
to exist — trust the check, but know what it actually checks.)

If `remove_background()` raises (no candidate found, or the candidate
doesn't touch the border), the photo doesn't have a plain background —
don't force it through this pipeline; it needs manual handling and a note
to the deck owner, not a fragile workaround.

## 9 · Regression protocol

`reference/` holds the frozen specimen renders. At the start of any session that
touches the system: rebuild the specimen deck and diff against `reference/`
(pixel-difference tolerance ~1%). Divergence = environment or code drift —
resolve before building a real deck. After an approved system change, re-freeze.

**Outstanding as of v4.1:** the specimen deck's manifest (`specimen.py`)
references nine named photo assets (`grape_cluster_gold`,
`burgundy_vineyard_domaine`, `margaret_river_aerial`, `winemaker_crop`,
`tank_hall`, `champagne_pour_bollinger`, `toast_sunset`,
`dormant_vineyard_hills`, `margaret_band`) that are not present in this
project's asset library. The specimen deck cannot currently be rebuilt or
re-hashed, and `REFERENCE_HASHES.txt` reflects an older code state. Until
those assets are supplied (or the specimen manifest is rebuilt against
different reference photos), §9's regression check cannot run — this is a
real gap, not a formality being skipped. Module changes in v4.1 were
verified by building an actual deck end-to-end and checking output
numerically (pixel presence, contrast, aspect ratios, collision-free
layout) instead.

**v4.2 note — a bigger process gap than the missing assets:** v4.2 exists
because an entire deck-build session's worth of fixes to `modules.py` and
`core.py` were made against a local working copy that was never saved
back to this project, while a *separate* prior session's v4.1 work *was*
saved back — so the two diverged silently, and this revision is the
manual merge of both. `core.py` in particular has no canonical copy in
this project at all as of v4.2; the version delivered alongside this
revision is the only complete one. **Concretely, this means:** at the
start of any session that will touch `modules.py` or `core.py`, diff the
working copy against this project's checked-in files before changing
anything, even if the working copy "looks right" — don't assume the
project's files are current, and don't assume your working copy is
either. When a session ends having changed either file, the corrected
files need to actually be saved back into this project (not just
delivered as downloads) or the next session repeats this problem.

## 10 · File map

```
LESSONS_LEARNED_v5.md  ← read this FIRST — the reasoning behind every
                          decision in this document, one build cycle's
                          worth of real bugs and their actual root causes

styleguide/
  tokens.py     ← every number in this spec — SHARED with Quick Sips
  core.py       ← canvas, fonts, text/photo helpers, QA, product-photo
                  pipeline (§8b) — SHARED with Quick Sips
  modules.py    ← the nineteen wired Field Guide layouts
  build.py      ← manifest → deck (QA-gated)
  specimen.py   ← the Field Guide specimen manifest — THE REGRESSION
                  SUITE, not a reference doc. Re-render it before any
                  module change ships (§9). A module can drift from its
                  own documented contract with nothing noticing until a
                  real deck hits the gap — that already happened once.
  reference/    ← frozen Field Guide regression renders
  fonts/  photos/   ← shared assets

  quick_sips.py            ← the Quick Sips series — see QUICK_SIPS_STYLE_GUIDE.md
  quick_sips_priorat.py    ← Quick Sips reference deck / regression baseline
  reference_quick_sips/    ← frozen Quick Sips regression renders
```

**Standing rule, restated because it's easy to forget mid-flow:** diff the
working copy against this project's checked-in files at the start of any
session touching `modules.py` or `core.py`. When a session changes either
file, save the corrected files back into the project before the session
ends — a delivered zip that never gets saved back means the next session
repeats the same gap from scratch.
