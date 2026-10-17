# The Field Guide: Mendocino ("The Fog Does the Work") -- review record

Classic carousel deck, 12 slides, `arc3/render_fg_mendocino_classic.py`. Benchmark rules (engine/variety.py): 12 distinct
layouts, no repeats, 5 graphic-led slides (2, 4, 5, 6, 8). Every slide passes QA.

## 1. Anna Wintour (claims)
- Every number traces to D3 Ch. 23.1, the CSW guide, the TTB/UC Davis AVA data, or a measurement from that data.
- Corrected: slide 6's numeral "1,000" -> "<1,000" (D3: "just under 1,000 ha"); slide 8's rain row "Burgundy" -> "Cote d'Or"
  (D3's ~700 mm figure is the Cote d'Or's; Chablis is 670 mm); slide 10, Cole Ranch "smallest AVA in the US" (CSW 2018)
  is OUT OF DATE -- Ulupalakua (Maui, 2021) took that title; now "California's smallest AVA, under 150 acres in all"
  (the 2023 CSW wording, per the Society of Wine Educators' CSW author).
- Dated, not stated as current: the organic share is "a quarter, in 2018".
- Not used: Cole Ranch's single owner (the AVA was for sale in 2019); "the only noncontiguous AVA" for Mendocino Ridge.
- Measured, not assumed: about 4 miles from the AVA to open ocean (4.2); Boonville and Philo verified inside the AVA.

## 2. Coco Chanel (editing)
- Slide 4: the standfirst lost "starts at the Russian River headwaters" (the river is on the slide 2 map) to make room for
  the decode line about Covelo, Dos Rios and Comptche.
- Slide 8: Champagne cut (D3 has no Champagne rainfall); Alsace and Burgundy latitudes merged into one honest bar
  (47-48 degrees) rather than shrinking type.

## 3. Jony Ive (craft)
- Slide 5: the sea is a pale filled region, so the map reads as one complete rectangle and its label is legible; the
  towns are gold markers with labels off the dark valley; the Anderson Valley label moved clear of the inset (which
  covered it); Yorkville Highlands' label sits inside its own region.
- Slide 8: the label column now fits "Anderson Valley" (an engine fix in chart_stack: the column fits its longest label,
  never narrower than 520px, so every earlier deck is pixel-identical -- regress 42/42).
- Cover: title over the vines measured 6.6:1 (median) / 3.0:1 (brightest leaves) at 300px; kicker chip cream 45%, 9.4:1.

## 4. Massimo Vignelli (grid)
- Slide 4: circles re-fit under a four-line standfirst; containment and non-overlap asserted in code.
- Slide 2: the map grew into the empty space (map_h 1680); Potter Valley labeled above its own shape (its column leader
  crossed two other AVAs).
- Pace: photo, map, photo, diagram, map, data, photo, chart, photo, tiles, cards + photo, closing photo.

## 5. Social Pass
| Gate | Where |
|---|---|
| Cover hook | "The Fog Does the Work" over the valley's vines |
| Second beat | Slide 2: every AVA in the county as its real shape |
| Decode layer | Slide 4: three Mendocino County AVAs sit outside the North Coast AVA; slide 10: Cole Ranch is no longer the US's smallest AVA |
| Save asset | Slides 2 and 6 (the AVA map; the six figures) |
| Send line | Caption: "Send this to whoever thinks California wine stops at Napa." |
| Open question | Caption: how Anderson Valley Pinot compares with Burgundy, for those who have tasted both |
| Callback | Slide 8: Alsace's grapes, nine degrees south (the Field Guide Reel's latitude scene) |
| Search surface | Caption and slides: Mendocino, Anderson Valley, Pinot Noir, AVA, Gewurztraminer |

---

# Round 2: the four-designer review and the brevity pass (Steve: run both before presenting; make the critical changes)

## Brevity pass
Counted EVERY visible word per slide (QA counts only what each module registers, so it can understate a table or a
tile). Before: 594 words, two slides over the 70-word budget (slide 6: 75, slide 10: 71). After: 561, none over
(largest: slide 10 at 68, slide 6 at 65). The Mosel benchmark, counted the same way: 725.

## Anna Wintour (claims)
- Slide 11's standfirst said "much of Mendocino's fruit leaves the county": D3 supports often blended and bought by
  wineries elsewhere, not "much". Now: "Good value, and wanted well beyond the county."
- Slide 6's 39 N stat duplicated slide 8's entire point: replaced with 1983, the AVA's establishment year, "one of the
  county's first three" (UC Davis/TTB: McDowell Valley Jan 1982, Cole Ranch May 1983, Anderson Valley Sept 1983).

## Coco Chanel (editing): every figure now appears once
- "About 4 miles" was on slides 5 and 6: kept on 6. "Thirty wineries" was on 6 and 9: kept on 6. Redwood Valley and
  Potter Valley with their grapes were on 3 and 10: slide 3 now says only cool vs warm and "at altitude"; the named
  AVAs live on slide 10. Slide 3 lost its "Climate" and "Example" rows (the headline and column heads say both).
- Trims: "Just under:" (the < says it), "early ripening", "for coast visitors", "Ripens"; Cole Ranch said "smallest"
  twice.

## Jony Ive (craft): every text-on-color pair measured, three failed
- Slide 12, gold subtitle on the signature block: 2.68:1 (needs 3:1). The signature deepened from the redwood green to
  the cover's canopy-shade green (52, 79, 16): 3.68:1. One color, one meaning: the valley's highlight on both maps and
  its bars on slide 8 moved with it; tile 3 (which used that shade) became the redwood green (paper on it 6.40:1).
- Slide 3, the "Further inland" column head in the house gold on paper: 2.39:1. Now sienna, 5.23:1.
- Slide 11, the card sub-lines (small text) in the house gold: 2.39:1 against the 4.5:1 small text needs. Now sienna.
- Engine: card_grid gained an optional `sub_color`, duel an optional `col_head_colors`; both default to the old colors,
  so every earlier deck renders identically (regress 42/42).
- SYSTEM FLAG for Steve: the house gold on paper is 2.39:1, so it fails as a text color wherever modules use it for text
  (e.g. the Mosel deck's card sub-lines). Not changed in locked decks; a system decision.

## Massimo Vignelli (grid)
- Slide 7: the facts ended two-thirds down, leaving a quarter of the page empty: the hero photo grew (1,340 -> 1,600px).
- Noted, not changed: slide 3's table is now two rows and leaves open paper below it (duel has no photo-size setting).

---

# Round 3 (Steve): five hashtags; the gold font readable in every instance; 13 slides stays; lock

- **Hashtags: five.** The Series System guide (s7) said ~15, the Social Pass guide (gate 7) said 5: now both say five.
  The caption carries five.
- **Length: 13 slides is fine.** 12 is not a hard cap for a Field Guide deck.
- **Gold, fixed in the engine, not per deck.** `core.legible` darkens (light backgrounds) or lightens (dark ones) the gold
  until it clears 4.5:1 against what is really behind it; marks, rules and fills keep the palette gold. Every place the
  engine draws the accent as text uses it. On paper the gold is (137, 111, 59), 4.54:1; on the signature green block
  (208, 177, 118), 4.50:1. The Mendocino deck's own sienna overrides were removed: it now uses the system's gold.
- **Measured, not assumed.** `engine/text_audit.py` hooks the text drawing and measures every piece of text against the
  pixels behind it. Baseline: 5 gold text groups below threshold across the Mendocino deck, locked Mosel, Cornas GTR,
  What Am I Drinking? and the specimen suite (Mosel's card sub-lines at 2.39:1, the GTR kicker at 2.39:1, and three in the
  specimen). After: zero.
- **It also caught four pale gray map labels on slide 5** (Yorkville Highlands 3.18:1, Pacific Ocean 3.23:1, Mendocino AVA
  4.01:1, Mendocino Ridge 4.32:1), which the earlier craft review missed: the atlas now darkens a label until it reads.
- **Blast radius:** exactly nine of the 42 regression renders changed (6 specimen, Mosel slides 1 and 10, Cornas reveal),
  each one containing gold text; the other 33 and all 26 locked Reel frames are identical. The reference was re-baselined.
  The delivered Mosel and Cornas PNGs are not altered; a re-render picks up the fix. Tags `fg-mosel-final` and the others
  still point at the earlier code.
- **Final audit of this deck:** every text group at or above threshold.
- Open dot on slide 13 (top right of the photo): the series' own closing mark, placed there by Steve's earlier direction.

---

# Addendum (FFFA research, Oct 2026): the Mendocino Ridge rename

While verifying facts for the FFFA deck, found that the TTB proposed renaming the Mendocino Ridge AVA "Mendocino Coast Ridge"
(NPRM 5 Jan 2024; comments closed 5 Mar 2024) and that its regulatory agenda targets a FINAL RULE for October 2026. No final rule was
published when checked, so "Mendocino Ridge" (slide 11) is correct today, with a two-year label transition if the rule lands.
**Check the Federal Register before posting this deck.** The locked deck's PNGs are unchanged.

