# "Five Fascinating Facts About..." (FFFA) — Style Guide v1

Third carousel series, alongside Field Guide and Quick Sips. Fixed
6-page format, not a module-sequence deck: `fff_cover()` once, then
`fff_fact()` five times (the fifth call with `closing=True` folds the
"Cheers!" sign-off into that same page — 6 pages total, never 7).

Module file: `fff_facts.py`. Uses `core.py` primitives (`new_canvas`,
`font`, `wrap`, `cover_fit`, `QA`, `region_luminance`, etc.) the same
way `modules.py` and `guess_the_region.py` do — it is a peer module
file, not a fork of the core system.

## Design north star: Massimo Vignelli

Deliberately distinct from both sibling series at a glance:

| | Field Guide | Quick Sips | FFFA |
|---|---|---|---|
| Display face | Playfair (serif) | Playfair (serif) | Archivo Black (grotesque sans) for numerals/kicker; **Playfair Black for the cover subject and every fact headline** (v3+, ties it back to the house type system without losing the sans/serif contrast) |
| Signature color | Red (`DEFAULT_PALETTE["SIGNATURE"]`) | Gold | Flat cobalt (`FFFA_ACCENT`, tokens.py) for numerals/rules/mark; golden yellow (`FFFA_YELLOW`, tokens.py) for the cover subject + every fact headline only |
| Cover | Flat color block + photo | Flat color block | **Photo-only** — no block. Kicker/icon sit directly on the photo's own dark zone, scrim added only if `region_luminance()` says the zone is too bright |
| Ornament | Gold rule, editorial warmth | Dense infographic | Hard-edged flat color, short accent rules, no gradients, no scrims-as-default |

## Fixed palette (tokens.py)

```python
FFFA_ACCENT = (28, 74, 172)   # flat cobalt -- numerals, rules, grid mark
FFFA_YELLOW = (255, 197, 47)  # golden yellow -- series DEFAULT for the
                               # cover subject + every page headline.
                               # Iterated three times before landing
                               # here: started canary (255,214,0, "too
                               # canary"), went too dark gold
                               # (255,179,0, "slightly too dark gold"),
                               # settled on this Brewers-gold-adjacent
                               # middle ground.
FFFA_SLIDE_COUNT = 6          # cover + 5 facts, fixed, not a range
```

**Per-deck headline color override (v3, added for Cabernet Franc):**
`fff_cover()` and `fff_fact()` both take an optional `headline_color=`
kwarg. When omitted, both fall back to `FFFA_YELLOW`. When a deck's
subject calls for it (a red wine deck, say), pass a deck-specific
color and it applies to the cover subject, every fact headline, and
the "Cheers" word on the closing page — the "!" stays cobalt either
way, and kicker/numerals/rules/diagram chips are never touched by this
override, so the series' cobalt identity stays intact regardless of
which headline color a given deck uses.

```python
img = fff_cover(slot, total=TOTAL, headline_color=RASPBERRY)
img = fff_fact(slot, slide_no, total=TOTAL, headline_color=RASPBERRY)
```

**Picking a deck override color from the actual cover photo, not by
eye:** for Cabernet Franc, the person asked for the headline color to
match "the lightest shade of red in the glass splash photo on the
cover." Don't eyeball this -- sample it:

```python
from PIL import Image
import numpy as np
import matplotlib.colors as mcolors

arr = np.array(Image.open(cover_photo_path).convert("RGB")).reshape(-1, 3) / 255.0
h, s, v = mcolors.rgb_to_hsv(arr).T
red_mask = ((h < 0.06) | (h > 0.95)) & (s > 0.6) & (v > 0.3)  # saturated red hues only
candidates = arr[red_mask]
brightest = candidates[np.argsort(-v[red_mask])[:80]] * 255   # top 80 brightest matches
color = tuple(int(x) for x in brightest.mean(axis=0))
```

Filtering for hue + saturation before ranking by brightness matters —
the single brightest "red" pixels in a wine-splash photo are usually
blown-out white/pink specular highlights, not the color a person means
by "the lightest red." Always run the result through
`core.contrast(color, INK)` afterward and raise brightness if it's
under the 3.0 floor for large text — the first Cabernet Franc attempt
at a plain "raspberry" guess (196,30,78) only scored 2.74 and had to
be adjusted.

## Fonts (tokens.py `FONT_FILES`, new roles added this series)

```python
"sans_black": "Archivo-Black.ttf",           # wght 900, wdth 100
"sans_cond_black": "ArchivoCond-Black.ttf",  # wght 900, wdth 62.5
```

Both are static instances generated from the Archivo variable font —
not shipped in the project photo/font store by default (per the
existing "font pipeline" convention, fonts are fetched live each
session via `codeload.github.com` / `raw.githubusercontent.com`, not
stored in project files). Regenerate with:

```python
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib import TTFont
f = TTFont("Archivo[wdth,wght].ttf")  # raw.githubusercontent.com/google/fonts/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf
instantiateVariableFont(f, {"wght": 900, "wdth": 100}, inplace=True)
f.save("Archivo-Black.ttf")
# repeat with wdth: 62.5 -> ArchivoCond-Black.ttf
```

`display_black` (Playfair-Black.ttf, already in the shared roster) is
used for the cover subject and every fact headline — the one deliberate
serif touchpoint that keeps FFFA legible as part of the same house
system despite the otherwise-sans treatment.

## Layout, cover (`fff_cover`)

- Full-bleed photo, no color block.
- Checklist icon (drawn from primitives, `_checklist_icon()`, never an
  asset) at `icon_size = 210`px+ — sized to match the two-line kicker
  block height so the pairing reads as one balanced unit, not an
  icon-then-oversized-label.
- Icon's first "row" is a filled numeral badge ("5") standing in for a
  checkmark — ties the glyph to "Five Fascinating Facts" specifically,
  not a generic to-do icon.
- Kicker "FIVE FASCINATING / FACTS ABOUT" at 130px, tracked caps,
  paper-colored, two lines, Archivo Condensed Black.
- Cover subject in **Title Case** (not caps), Playfair Black, golden
  yellow, auto-shrunk to fit width, `headline=True` in QA.
- Scrim logic: `region_luminance()` checks the actual rendered
  brightness under the text zone; only chips to ink if the photo is too
  bright there (>90) for paper-white/yellow text — never a default.

## Layout, fact page (`fff_fact`)

- Photo band (1450px tall, or 1200px when a diagram is present) + ink
  block below.
- Small checklist icon (same mark as the cover, `icon_size_small = int(
  num_size * 0.72)`) to the left of every numeral, aligned to the
  numeral's **actual glyph top** (measured via `textbbox`, not the
  font's nominal ascent box — Archivo Black leaves visible padding
  above the digits that made the first version look misaligned).
- Numeral (`01`–`05`) in cobalt, decorative/exempted from the headline-
  hierarchy check (`!numeral` label prefix).
- Headline in Playfair Black, golden yellow, contrast-checked against
  ink (`qa.check_contrast`).
- Body in light gray (`214,208,200`), 15–20 words as a target (some
  flex allowed for a diagram slide's tighter budget).
- Optional `diagram=` slot — see below.
- `closing=True` on the last call only: draws "Cheers" in the deck's
  headline color + "!" in cobalt, Playfair Black, sized to **drift
  down past the normal content bottom** into the space the swipe cue
  vacated (swipe label is suppressed on this page only — see Footer
  below). Positioned at `diagram_bottom - 10` (v3; was `+ 34` in v2 and
  sat too close to the bottom edge per direct feedback — raised ~44px).

## Diagrams: show the claim, don't just state it

Three diagram helpers exist now, all following the same principle
documented in DESIGN_PROCESS_v8.md section 3 ("data claims should be
visible in form"): when a fact's claim is fundamentally comparative,
scalar, or relational, and no real stock photo can show that
comparison at true scale, draw it.

- `_bottle_size_diagram()` — five Champagne bottle-format silhouettes
  (Standard through Nebuchadnezzar) at true relative height. Used on
  the "every big bottle has a royal name" fact; no stock photo shows
  five formats side by side.
- `_sweetness_diagram()` — seven EU dosage levels (Brut Nature through
  Doux) as bar heights scaled to representative g/L residual sugar.
  Used on the Champagne deck's closing fact.
- `_parentage_diagram()` (v3, added for Cabernet Franc) — two parent
  chips joined by "×", an arrow down to a child chip. Used on the
  Cabernet Franc "Cabernet Sauvignon's parent, not its sibling" fact
  (Cabernet Franc × Sauvignon Blanc → Cabernet Sauvignon). Generic
  enough to reuse for any grape-parentage fact, not Cabernet-Franc-
  specific: `diagram="parentage"` with `slot["parent_a"]`,
  `slot["parent_b"]`, `slot["child"]` strings.

**Not every fact needs one.** The Cabernet Franc deck's first draft
gave the parentage fact a diagram, and it worked well and stayed in
the final deck — but a later round removed the diagram from the same
slide as an explicit style choice ("get rid of the flowchart graphic")
and the slide reads perfectly well as photo + copy alone. Treat a
diagram as available for comparative/scalar/relational claims, not as
a default to reach for on every fact — the standing rule is judgment,
not a quota.

**Locked rule: 35px minimum font size for any chart/diagram label** —
sits below the body-text floor deliberately (charts pack tighter than
prose) but is still a hard floor. Applies to any current or future
FFFA diagram.

Both `_bottle_size_diagram()` and `_sweetness_diagram()` size
themselves to whatever vertical budget is left after headline+body,
capped against `CONTENT_BOTTOM`, and return their own bottom/top y so
the caller can register a `!`-prefixed QA box (exempted from the
caption-zone and hierarchy checks, same convention as every other
piece of cover/closing furniture in this system). `_parentage_diagram()`
follows the same return-your-own-bounds convention.

## Footer

Standard `footer()` on every page **except** the closing page, where
the swipe cue is suppressed (`swipe_label=""`) to leave room for the
larger "Cheers!" sign-off, and the photo credit moves from the bottom
row up to a small line under the top-right grid mark (`_finish()`'s
`swipe_label` param and the closing-specific credit placement in
`fff_fact()` handle this).

## Photo sourcing notes specific to this series

- Check both Pexels and Unsplash; prefer whichever gives the more
  literal shot of the fact (e.g. genuine bubble streams rising through
  liquid, not condensation on the outside of a glass — an easy
  mismatch at thumbnail size, confirm at full resolution before
  committing).
- Watch for glassware etchings/logos (a decorative Pegasus mark cost a
  reshoot this session) and holiday props (string lights, ornaments)
  that read as a different occasion than the deck's editorial tone.
- `fetch_pexels.py` (new this session, paired with the existing
  `fetch_unsplash.py`) — same curl-subprocess pattern, no per-photo
  tracking ping required (unlike Unsplash's mandatory download-location
  ping, which `fetch_unsplash.py` already handles).

## Known open items for the next FFFA deck

- `_bar_diagram`-style generalization is now less urgent than it was
  after v2 — `_bottle_size_diagram()`, `_sweetness_diagram()`, and
  `_parentage_diagram()` cover scalar, ranked, and relational claims
  respectively, which is most of what a wine fact needs. Still worth
  collapsing the first two into a shared helper before a third
  scalar-diagram deck shows up needing its own hardcoded data table.
- `fff_cover()` / `fff_fact()` assume a single-word subject
  ("Champagne") or a short two-word one ("Cabernet Franc," confirmed
  working in v3 — the auto-shrink loop handled it without issue).
  Longer subjects (a full appellation name, say) still untested.
- Per-deck `headline_color` is now a proven pattern (v3) — worth
  deciding, before a fourth or fifth deck, whether it's worth
  promoting specific proven overrides (e.g. a "red wine" palette, a
  "white wine" palette) into named constants in `tokens.py` rather
  than re-deriving a color from a cover photo each time. Not urgent at
  two decks.
