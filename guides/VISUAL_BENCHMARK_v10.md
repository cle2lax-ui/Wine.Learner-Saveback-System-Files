# Visual Benchmark — v10

**The Mosel Field Guide is the system's benchmark for visual quality.**
Reference implementation: `arc2/render_fg_mosel.py`. Locked as git tag
`fg-mosel-final`. Every Field Guide from here on is held to the standard
below, and the engine now enforces the measurable parts of it.

What made it a step up from earlier decks was not any one slide. It was
**variety**: twelve pages, eleven different layouts, and each page built
around a different *kind of visual thinking* — a map, a staircase, range
bars, ring charts, a hero photograph, vertical photo blades, coloured
tiles — instead of a photo band over running text. The reader never sees
the same page twice, and the data is *drawn*, not described.

---

## 1. The deck at a glance

| # | Layout (module) | What carries the slide |
|---|---|---|
| 1 | `cover_bleed` (M19) | Full-bleed photo, no scrim; kicker on a translucent chip |
| 2 | `editorial_lead` (M02) | Photo band over run-in text — the one text-led page |
| 3 | `region_map` (M20) | **Map:** all 13 German regions as real traced shapes, one picked out |
| 4 | `tile_grid` (M26) | **Four solid tiles**, each in the colour of its own subject |
| 5 | `blades` (M21) | **Three vertical photo blades** — detail / figure / wide view |
| 6 | `stair_ladder` (M22) | **Numbered staircase**, lowest rung at the bottom, a parallel-track side box |
| 7 | `chart_stack` (M23) | **Range bands** with a hatched conditional extension, plus **bar chart** |
| 8 | `rail_rings` (M24) | **Ring charts** beside a full-height photo rail |
| 9 | `editorial_lead` (M02) | Wide photo band with people in it |
| 10 | `card_grid` (M07) | Three cards over a photo stripe |
| 11 | `hero_facts` (M25) | **Hero photograph** over half the page, 2×2 facts beneath |
| 12 | `statement` (M01) | Closing |

11 distinct layouts in 12 slides; the only repeat (`editorial_lead`, 2 and 9)
is non-adjacent. Data-, diagram- or map-led slides: **3, 6, 7, 8**.

## 2. The rules (checked at build time by `engine/variety.py`)

For a 10–12 slide Field Guide:

1. **At least 8 distinct layouts.** (Mosel: 11.)
2. **Never the same layout twice in a row.**
3. **No layout more than twice.**
4. **At least 4 slides led by a data graphic, diagram or map** — not a photo
   band over text. (Mosel: 3, 6, 7, 8.) The graphic modules are listed in
   `variety.GRAPHIC_MODULES`; add a module there when you add one.

A deck that fails any of these fails its build, like any QA failure. The fix
is a different layout, never an exemption.

Rules that aren't machine-checkable but are part of the standard:

5. **Every slide has one visual idea; the text supports it.** Cut copy before
   shrinking type. Where a first draft was text, ask what the *shape* of the
   content is and draw that.
6. **One-line titles.** `core.one_line_headline` shrinks to fit and raises if
   it can't — so a too-long title fails the build rather than wrapping.
7. **Pace the deck.** Alternate photo-led, graphic-led and text-led pages;
   never three text-led pages running.
8. **The cover is full-bleed.** No scrim, no colour block. Legibility comes
   from position, or from a chip chosen by *measurement* (§4).

### Choosing the graphic — what shape is the content?

| The content is… | Use |
|---|---|
| A ranking, lowest to highest | `stair_ladder` — lowest rung at the **bottom**; a parallel track goes in the side box, never as a rung |
| A numeric range, with a condition that extends it | `chart_stack` band chart (solid base, hatched extension) |
| A comparison of shares | `chart_stack` bar chart; draw a number the source only gives in words at its word value ("just under half") |
| Two or three headline percentages | `rail_rings` |
| Geography at country scale | `region_map` |
| Four parallel points | `tile_grid` — each tile the colour of its subject |
| Three views at different scales | `blades` |
| A subject that *is* the story | `hero_facts` (no scrim over the hero) |
| Nested containment | `euler_nesting` · sequence: `timeline` · process: `process_map` |

## 3. Chart colour comes from the cover photo

Steve's note on the first pass was that the charts looked washed out — they
were pale blends of the brand slate and gold. The standard is the opposite:
**every chart colour is sampled from the deck's own cover photograph**, so the
charts and the cover read as one piece.

`engine/palette.py` is the method: for each named feature of the exact cover
crop (the sunlit vineyard, the lamp reflections, the roofs, the hillside, the
river), take the most saturated mid-light pixels of that hue family. That
gives the colour *where the light hits it*, not a shadow-muddied average —
which matters on a moody photo, where "the foliage" averages to brown.
`arc2/sample_cover_palette.py` is a worked example; re-run it if the cover
photo or its crop ever changes.

The Mosel's palette (cover feature → RGB):

| Key | Cover feature | RGB |
|---|---|---|
| `gold` | sunlit vineyard | (201,151,3) |
| `grape` | autumn leaves | (171,142,3) |
| `amber` | lamp reflections in the river | (242,145,4) |
| ripe[3] | lit windows | (203,114,12) |
| ripe[4] | roofs | (179,80,63) |
| ripe[0] | hillside forest | (50,62,25) |
| `focus` | the river, in shade | (18,32,30) |
| `ice_fill` | sky | (225,244,248) |
| `stone`, `track` | stone/plaster (k-means clusters of the whole crop) | (98,91,74), (203,194,165) |

`ripe` is a 5-step ramp in the order grapes move through: forest → gold →
orange → deep orange → brick.

**One colour, one meaning, across the deck.** The river's near-black teal
(`focus`) is "the Mosel" on every slide that highlights it — the map, the
trocken bar, the 26% figure.

**Measure every pairing; never judge contrast by eye.** `core.contrast` is
WCAG: ≥ 4.5:1 for body text, ≥ 3:1 for large type. Text on any chart fill is
chosen by `core.best_text_color`. The Mosel deck's first attempts failed
three times: brick numerals on the gold tile measured 1.9:1 and amber on the stone
tile 2.8:1, and a pale-yellow accent on the orange tile 2.9:1 — all three
changed to cover colours that pass.

Decks that don't set `slot["chart"]` get a neutral default from
`modules.chart_palette` — good enough for a specimen, not for a real deck.

## 4. The cover chip — measure before you choose

The Mosel cover's kicker sits over a castle tower and pale sky. A translucent
**dark** chip behind **light** text is counter-intuitive: at low opacity it
tints the pale sky to a mid-tone with the same brightness as the text, and
contrast bottoms out near **1:1** (25–55% opacity); it only reaches 3:1 at
about 75% and 3.6:1 at 80%. A **light** chip with **dark** text works at low
opacity (cream at 45% → 5.7:1). Sample the real pixels behind the chip and
compute contrast across candidate opacities before choosing — the Mosel
cover did, and Steve picked the dark chip at 80% with gold text. Never fix
legibility with a shadow or scrim on the cover.

## 5. Honest data graphics

A chart is a claim, so it follows the same sourcing discipline as the text.

* **Every number traces to the source** (the Mosel's: D3 Ch. 11). Where the
  source gives a figure only in words, draw it at that word's value and label
  it with the words.
* **Maps come from real data**, never hand-drawn: the 13 region shapes were
  traced from a CC BY-SA Commons SVG and georeferenced against its own city
  markers (RMS 3.0 km, max 5.8 km) onto an outline dissolved from state data.
  Disclose approximations on the slide or the credit: region shapes are
  illustrative regional extent, not legal boundaries.
* **Verify a photo's location from its metadata, not its caption.** A
  "steep vineyard river Germany" hit on the cover search was, per Unsplash's
  own location data, Andernach on the **Rhine**. Where there's no location
  data (Pexels has none), caption by what the picture shows, not where.
* **Don't claim a place you can't confirm** — the Saar/Ruwer photo with
  people is captioned "Bernkastel, Middle Mosel" because no peopled
  Saar/Ruwer photo existed.

## 6. How to build a deck to this standard

1. **Pick the cover, then sample its palette** (`engine/palette.py`).
2. **List the slides by module** and run `variety.report(names)` *before*
   building. Fix the rhythm on paper.
3. **Choose each graphic by the shape of its content** (§2 table).
4. **Build.** QA aborts on overflow — cut copy, never silence a check.
5. **Look at every slide, at a crop where problems show.** QA missed real
   defects on this deck: a map description running into the footer, label
   crowding, a card-grid footnote silently dropped. QA passing ≠ looking right.
6. **Measure every text/fill pair** (§3).
7. **Refactors must be pixel-identical.** Diff every page against the locked
   PNGs; run `python3 engine/regress.py`.
8. **Lock:** tag the commit, ZIP the PNGs with `build.lock_deck`.

## 7. The modules

M19–M26 are in `engine/modules.py` with full slot schemas in their
docstrings and in `STYLE_GUIDE_v5.md` §7. They are exercised by
`engine/specimen.py` (slots 20–27).

| # | Module | Job |
|---|---|---|
| M19 | `cover_bleed` | Full-bleed cover with optional translucent kicker chip |
| M20 | `region_map` | Country-scale region map, one highlighted, deliberate label column |
| M21 | `blades` | Vertical photo blades, stepped, with caption tabs |
| M22 | `stair_ladder` | Numbered staircase ranking, lowest at the bottom, parallel-track box |
| M23 | `chart_stack` | Range-band chart (with hatched extension) and/or bar chart |
| M24 | `rail_rings` | Photo rail with ring charts |
| M25 | `hero_facts` | Hero photograph over half the page + compact fact grid |
| M26 | `tile_grid` | 2×2 solid tiles, per-subject colours |

Helpers promoted to `core.py`: `blend_rgb`, `best_text_color`,
`one_line_headline`, `hatch_fill`, `donut`. New engine files: `palette.py`,
`variety.py`, `regress.py`.

## 8. Known gaps found while building the benchmark

Not fixed here; each is a trap for the next deck.

* `statement(variant="closing")` is documented but not implemented — the
  function branches only on `"cover"` and `"quote"`. Use `"cover"` for the
  closing slide. (Found because trimming text didn't change the overflow
  numbers, which a real length problem always does.)
* `card_grid` has no `footnote` slot and drops it **silently**. Put the
  content in a card or a standfirst.
* `regional_atlas` passes QA even when its description paragraph runs into the
  footer. Check it by eye.
* `map_atlas`'s automatic label placement suits one region's sub-areas, not a
  national map — use `region_map`.
* `sourcing/fetch_pexels.py` returns empty results where the Pexels API has
  thousands; call the API directly. Pexels carries no geodata.
* The specimen suite's placeholder photos were never in this repo, so 12 of
  its original 18 modules had never actually been tested; it now substitutes
  a stand-in and says so.
* The deck's custom cover (`cover_bleed`) is full-bleed by design and does not
  run through the QA harness — check it in a render.

## 9. Files

```
arc2/render_fg_mosel.py      reference implementation (data, palette, slide order, copy only)
arc2/prepare_map_data.py     builds the region/Mosel map data from real sources
arc2/sample_cover_palette.py the Mosel's configuration of engine/palette.py
data/geo/                    anbaugebiete.geojson (+ source SVG), germany, rivers
engine/variety.py            the variety rules, enforced at build time
engine/palette.py            cover-photo palette sampler
engine/regress.py            pixel-hash regression guard
reference/PIXEL_HASHES.json  frozen hashes: 26 specimen renders + 12 Mosel pages
```
