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
- Slide 2: the map grew into the empty space (map_h 1680); Potter Valley labelled above its own shape (its column leader
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
