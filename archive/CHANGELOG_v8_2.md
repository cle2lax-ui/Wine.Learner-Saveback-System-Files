# CHANGELOG v8.2 — FFFA series (Champagne deck, first build)

New carousel series built this session: "Five Fascinating Facts
About..." (FFFA), first deck Champagne, locked and shipped as PDF +
ZIP. This is a new module file and a new set of system-locked rules,
not a bugfix session — see `DESIGN_PROCESS_v8.md` section 9 and
`FFFA_STYLE_GUIDE.md` for the full design system.

## New files

- **`fff_facts.py`** — the series' module library: `fff_cover()`,
  `fff_fact()`, plus private helpers for the checklist icon
  (`_checklist_icon`), the repeating grid mark (`_grid_mark`), and two
  diagram drawers (`_bottle_size_diagram`, `_sweetness_diagram`). Peer
  file to `modules.py`, not a fork of it — imports and uses `core.py`
  primitives the same way.
- **`fetch_pexels.py`** — Pexels search + download helper, paired with
  the existing `fetch_unsplash.py`. Same curl-subprocess pattern as the
  rest of the photo pipeline. No per-photo tracking ping required
  (Pexels' terms don't mandate one, unlike Unsplash's download-location
  ping).
- **`FFFA_STYLE_GUIDE.md`** — dedicated style guide for the series,
  same pattern as `QUICK_SIPS_STYLE_GUIDE.md` / `GTR_STYLE_GUIDE.md`.
- **`NEW_DECK_STARTER_v8_2_ADDENDUM.md`** — kickoff checklist for the
  next FFFA deck, additive on the v8 addendum the same way that was
  additive on v7.
- **`render_fff_champagne.py`** — the Champagne deck's render script,
  kept as a worked reference for the next FFFA deck's script.

## tokens.py

- **`FFFA_ACCENT`, `FFFA_YELLOW`, `FFFA_SLIDE_COUNT` added.** Series
  constants, same pattern as any other cross-deck constant already in
  this file. `FFFA_YELLOW` went through three iterations before
  landing at `(255, 197, 47)` — see FFFA_STYLE_GUIDE.md for the exact
  history if a future session needs to explain why it isn't a "pure"
  yellow.
- **`FONT_FILES` gained two roles**: `sans_black` (Archivo-Black.ttf)
  and `sans_cond_black` (ArchivoCond-Black.ttf). Static instances of
  the Archivo variable font at `wght=900`, generated via `fonttools`
  instancing — not stored in the project photo/font store, regenerated
  live per session per the existing font-pipeline convention.
  Generation snippet is in `FFFA_STYLE_GUIDE.md`.

## DESIGN_PROCESS_v8.md

- **New section 9** appended (before the delivery section, which stays
  last): the subset of FFFA rules that are system-locked rather than
  deck-specific — fixed 6-page format, own palette, photo-only cover
  with measured (not assumed) scrim logic, primitive-drawn checklist
  icon aligned to actual glyph top, 35px chart-label floor, diagrams
  over stock photos for comparative claims.

## Fixed this session (real layout bugs, not style choices)

- **Checklist icon top-alignment.** The small icon next to each fact
  numeral was originally aligned to the numeral font's nominal ascent
  box, which left it sitting visibly high — Archivo Black has real
  padding above the digit glyphs themselves. Fixed by measuring the
  numeral's actual rendered top via `textbbox` before positioning the
  icon, not assuming the font metrics box equals the visible glyph
  top. Same class of bug section 2's luminance rule was written to
  prevent for color; this is the equivalent lesson for vertical
  alignment.
- **Diagram + closing-sign-off collision.** The sweetness diagram and
  the enlarged "Cheers!" sign-off both wanted the same vertical budget
  on the closing page. Fixed by computing the diagram's actual bottom
  y and anchoring "Cheers!" relative to that (not a fixed offset from
  the body text), and by giving the diagram a tighter height cap
  specifically when `closing=True`.
- **Closing-page credit collision.** Once "Cheers!" was enlarged and
  allowed to drift down into the former swipe-cue zone, the photo
  credit (previously bottom-center) started colliding with it. Moved
  the closing page's credit to a small line under the top-right grid
  mark instead of suppressing it — attribution stays, just relocated.

## Photo sourcing notes from this session

Five photo swaps on Fact 1 alone chasing "warm, moody, bubbles actually
rising through the glass, no logos" — worth a callout since it's a
real pattern, not a one-off:
1. A cool-toned rosé flute — rejected as reading "winter."
2. A candlelit pour with a decorative Pegasus etched into the glass —
   rejected as an unwanted logo-like mark, only visible at full
   resolution, not the search thumbnail.
3. An abstract macro of condensation bubbles on the *outside* of a
   glass — rejected because the person specifically wanted bubbles
   rising *through* the liquid, and this wasn't that despite matching
   "bubbles" and "warm" as search terms.
4. Landed on a genuine bubble-stream shot, tightly cropped via
   `photo_anchor` to avoid a too-bright section of the original frame.

Lesson for the next session: "bubbles" as a search term returns
condensation, soap bubbles, and glass-etching artifacts about as often
as it returns actual carbonation — confirm the specific visual claim
(rising through liquid vs. on a surface) at full resolution before
committing, not just at thumbnail size.
