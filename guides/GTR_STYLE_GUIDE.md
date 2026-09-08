# GUESS THE WINE REGION — STYLE SYSTEM

**Reference/benchmark deck: `render_gtr_entre_deux_mers.py`** (Entre-Deux-Mers).
Every layout number in this document is what that deck actually renders
to. If `modules.py`/`guess_the_region.py` ever changes, rebuild the
reference deck and diff against `GTR_REFERENCE_HASHES.txt` before
trusting a new render — same convention as Quick Sips.

**The operating manual for every "Guess the Wine Region" 2-page post.**
Third series on this system, alongside **Field Guide** (`STYLE_GUIDE_v5.md`)
and **Quick Sips** (`QUICK_SIPS_STYLE_GUIDE.md`). Same canvas (2160×2700,
4:5 portrait @2x), same margin/floor tokens, same QA harness — its own
visual system, living in its own file (`guess_the_region.py`), not
`modules.py` or `quick_sips.py`.

---

## 1 · Format & purpose

A quiz card, not a deep-dive. Page 1 poses four clues about a region
without naming it; page 2 reveals the name and gives just enough context
to explain why it matters. Two pages, every time — this is not a
variable-length format like Field Guide.

Audience and register are identical to the rest of the system: WSET/CSW
students and serious enthusiasts; Wine Spectator / Condé Nast Traveler /
Rolex register. Deck copy is editorial — never mention exams, study
materials, or section numbers.

A new GTR deck is two dict literals and two function calls:

```python
from tokens import DEFAULT_PALETTE
from guess_the_region import gtr_cover, gtr_reveal

pal = dict(DEFAULT_PALETTE)
pal["ACCENT"] = (196, 158, 84)   # series gold — keep this fixed across decks

slot1 = dict(
    photo="some_photo_key",       # clue-side photo — atmosphere, not the reveal shot
    clues=["...", "...", "...", "..."],   # exactly 4, short (see §3)
    photo_credit=None,            # or "Photo: Name, License"
)
slot2 = dict(
    photo="some_photo_key",       # can be the same photo or a different one
    region="Region Name",
    blurb="2-3 sentences...",     # why it matters, not a fact dump
    caption="Short factual caption of what's in the photo",  # optional
    photo_credit=None,
)

gtr_cover(slot1, 1, 2, pal).save("p1.png")
gtr_reveal(slot2, 2, 2, pal).save("p2.png")
```

Both functions run the shared QA harness (`_start`/`_finish`, or a manual
equivalent — see §7) and raise on failure. A clean run prints
`QA pass` for both pages.

---

## 2 · Page 1 — vertical blade cover

**Locked branding, do not vary per deck:** the folded-map-with-pin icon
and the two-line title "Guess the / Wine Region". Only the photo and
the four clues change deck to deck.

**Layout — vertical blade, not full-bleed:**
- Left ~35% (`blade_w`, default 760px): full-height photo strip.
- Right ~65%: solid **black** panel (`(0,0,0)`), carrying all type.
- No seam line, no scrim anywhere on this page — the black panel is
  what solves legibility. (An earlier full-bleed-with-scrims version
  fought bright photo areas, e.g. white door frames; the blade sidesteps
  that failure mode entirely rather than patching it.)
- `panel_margin` 100px inset from the blade edge and the right margin
  for all panel content (`content_x0`, `content_w`).

**Header:**
- Folded-map icon (§4) inline with "Guess the" on row 1; "Wine Region"
  force-wrapped to row 2 (not left to auto-wrap — the break is fixed).
- Icon is **white**, scales directly off the title font size
  (`icon_size = hf_size * 120/140`) — if you change the title size,
  the icon follows automatically.
- Title font: `display_black` (Playfair Black, the heaviest weight —
  not `display_bold`), 170px, gold (`pal["ACCENT"]`), tight leading
  (0.86× line height between the two rows).
- Title top pinned at y=140 (not vertically centered — a fixed anchor).

**Clues:**
- Exactly 4, lettered A.–D. in gold serif (`display_bold`, 86px),
  copy in white sans (`body`, 88px).
- Anchored below the header with a 230px gap.
- Keep clues short — aim for one line, two at most, each. Long clues
  fighting the QA word budget is a signal to cut, not shrink type.

**Swipe cue:**
- "SWIPE TO SEE THE ANSWER ←" in gold, `kicker_bold` 88px, centered on
  the *panel* width (not the full page), 170px below the clue block.
- The arrow point is the swipe **gesture** direction, not "next page" —
  same convention as `core.footer()`'s default label.

**QA word budget:** 60 words (`qa.word_limit`), covering the locked
header text + all 4 clues combined. Tight on purpose — this is a quiz
card, not a fact sheet.

---

## 3 · Page 2 — reveal

**Layout — 66/34 split, not the earlier 2/3 or 50/50 versions tried
mid-project:**
- Top 66% (`photo_h`, default `int(H*0.66)`): full-bleed photo.
- Thin gold hairline seam at the boundary.
- Bottom 34%: white (`PAPER`) reveal panel.
- `bottom_margin` 200px (configurable via `slot["bottom_margin"]`) —
  nothing in the reveal panel may render below `H - bottom_margin`.
  This is enforced in code (see §7), not just documented.

**Photo caption (optional, `slot["caption"]`):**
- Top-right corner of the photo, `caption_italic` (Cormorant Italic) at
  the type floor (60px) — same family as `core.photo_band()`'s caption
  convention, just repositioned to stay clear of the text-heavy bottom
  panel.
- **Color is adaptive, not fixed.** The actual rendered luminance behind
  the caption's bounding box is sampled (`_region_luminance()`); above
  150 (light — sky, pale water) it draws in `INK` with **no scrim**;
  otherwise it falls back to white text over a top scrim (0.68 strength,
  170px band). A `qa.check_photo_contrast()` call verifies the choice
  against the *actual* rendered pixels — this is a real QA gate, not a
  guess, so it stays safe as photos change deck to deck.
- Photo *credit* (photographer/license) stays separate, in the footer
  gutter via `photo_credit` — never combine credit and caption.

**Kicker + region name + flag lockup:**
- "THE WINE REGION IS…" kicker, `kicker_bold` 60px, gold, 26px below
  the photo seam.
- Region name, `display_black` 140px, **burgundy** (`pal["SIGNATURE"]`,
  default `(114,47,55)`) — not `INK`. 18px below the kicker.
- A flat French tricolor flag (`_french_flag()`, no border, 3:2 ratio)
  sits to the right of the name, recentered as one group so the
  name+flag combo stays centered on the page.
- **Flag vertical alignment is x-height-based, not glyph-bbox-based:**
  centered against the bounding box of a lowercase "e" sampled in the
  same font/size, so it lines up with the lowercase letters rather than
  being pulled up by capital letters in the name. If a future region
  name is all-lowercase or has unusual capitalization, this still holds
  because it re-samples "e" fresh each time, not a hardcoded offset.
- Region font auto-shrinks (140px → floor of 90px) if the name is too
  wide, reserving 200px of margin for the flag+gap alongside it.

**Blurb paragraph:**
- 2–3 sentences on why the region matters — not a fact dump, not exam
  language. `display_light`, fully justified (first N-1 lines flush
  both edges via manual word-spacing distribution; last line
  left-aligned, standard typographic convention — see `_justify` logic
  inline in `gtr_reveal`).
- **Font size is shrink-to-fit, not fixed.** Starts at 84px, steps down
  in 2px increments (floor 60px) until the full block clears
  `bottom_limit`. This means the paragraph automatically adapts to
  whatever copy length or `bottom_margin` a future deck uses — you
  should not need to hand-tune this per deck.
- Leading 0.98× (tight, by design — this is a short reveal paragraph,
  not a reading-length passage).
- Column width: `W - 2*M - 100`, centered.

**No swipe cue on this page** — it's the last page of the pair. Only
the page-number footer prints (`core_footer(..., label="")`).

**QA word budget:** 90 words (`qa.word_limit`), covering kicker + region
name + blurb.

---

## 4 · The folded-map-with-pin icon

Built parametrically in `_folded_map_icon()` / `_folded_map_icon_bbox()`
— not a static asset — so it scales cleanly to any size. Proportions
were measured directly off a reference icon the client supplied (photo
upload, not a stock-site fetch — that domain wasn't reachable), by
tracing the actual pixel silhouette:

| Measurement | Value (× icon width `w`) |
|---|---|
| Overall height | ~0.666×w (peaks to tip) |
| Ribbon thickness | 0.59×w |
| Peak rise above tip line | 0.644×w |
| Dip rise above tip line | 0.57×w |
| Pin outer radius | 0.155×w |

Shape: a ribbon with **pointed left/right ends** (not flat), a
peak-dip-peak zigzag top edge at the quarter-points, rounded joins at
every vertex (`joint="curve"`), a crease line at each interior fold, a
dashed route line drifting across it at mid-thickness, and a teardrop
pin with an inner ring sitting over the dip — nudged down and right
(`+0.11×w` horizontal, `+0.32×thickness` vertical) so it isn't sitting
dead-center on the fold.

`_folded_map_icon_bbox(size)` returns geometry only (no drawing) so
callers can vertically center the icon against other elements (the
title row, in `gtr_cover`) *before* it's drawn — this avoids the
draw-then-guess-then-redraw problem that caused misalignment earlier in
the project.

---

## 5 · Palette

| Token | Value | Use |
|---|---|---|
| `pal["ACCENT"]` | `(196,158,84)` gold | Title, icon, clue letters, swipe cue, kicker, flag-adjacent gold accents. **Fixed across all GTR decks** — this is series branding, not a per-deck variable like Quick Sips' `ACCENT`. |
| `pal["SIGNATURE"]` | `(114,47,55)` burgundy/claret | Region name headline only. |
| Panel black | `(0,0,0)` | Page 1 panel background. Pure black, not `INK` — deliberately heavier than the rest of the system's near-black. |
| `PAPER` | `(251,249,244)` | Page 2 reveal panel background (system default, unchanged). |
| `MUTED` | `(110,96,104)` | Blurb paragraph body color (system default, unchanged). |

---

## 6 · What changed across the build (for future-me context)

In rough order: full-bleed photo + scrims on page 1 → replaced with the
vertical blade (scrim approach couldn't handle bright photo regions
like door frames). Bullet-dot clues → lettered A–D. Fixed clue-column
width tied to one specific photo's dark/light zones → removed once the
blade made that irrelevant (clues live on a flat black panel now, no
photo-dependent legibility logic needed on page 1 at all). Page 2's
photo/panel split moved twice (56% → 48% → 66%) as body-text size and
leading changed — the shrink-to-fit blurb logic exists specifically so
this kind of change doesn't require hand re-tuning next time. Photo
caption moved from bottom-left (page 1 style) to top-right (page 2,
to stay clear of the text-heavy bottom third), then got luminance-
adaptive color after the first photo's bright sky made white-on-scrim
the wrong call.

---

## 7 · QA specifics unique to this series

- Page 1 uses `modules._start`/`_finish` normally.
- Page 2 does **not** call `modules._finish` — it needs to suppress the
  default "SWIPE ←" footer label (this is the last page of the pair),
  so it calls `core.footer()` directly with `label=""` and replicates
  `_finish`'s `qa.report(img)` call manually. If you add a third page to
  a future GTR deck, decide explicitly whether it wants the swipe label.
- `bottom_limit` (page 2) and the blurb shrink-loop are a **harder**
  guarantee than the system default `CONTENT_BOTTOM` (`H-200`) safe
  zone — the blurb box is deliberately labeled `!blurb` to bypass the
  generic caption-zone check and rely on the page's own explicit
  `bottom_margin` logic instead. This is an intentional `!`-prefix
  exception, not an oversight — don't "fix" it by removing the `!`
  without re-reading this section.
- `qa.check_photo_contrast()` is used for the adaptive caption (§3) —
  reuse this pattern for any other text-on-photo element a future GTR
  page might need, rather than assuming a fixed color is safe.

---

## 8 · Files

- `guess_the_region.py` — the module library (`gtr_cover`, `gtr_reveal`,
  and their private glyph helpers). Import from here for every new deck.
- `render_gtr_entre_deux_mers.py` — the reference/benchmark deck. Copy
  this file as the starting point for a new GTR deck; don't start from
  a blank script.
- `GTR_REFERENCE_HASHES.txt` — sha256 of the benchmark deck's two
  rendered pages. Rebuild + rehash after any change to `guess_the_region.py`,
  `core.py`, or `tokens.py`.
