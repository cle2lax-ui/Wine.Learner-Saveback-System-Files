# Review: The Field Guide: Climate ("Climate's Impact on Wine") -- 14 slides, built, awaiting Steve's review

Files: `arc4/render_fg_climate.py` (the deck), `arc4/prepare_climate_maps.py` (the world map), `arc4/CAPTION_FG_climate.md`.
Output: `/home/claude/out_fg_climate/` (13 PNGs at 2160x2700 and `FG_Climate_review.pdf`).

## What was checked
- **Layouts:** 14 distinct layouts in 14 slides; four led by a graphic (thermometer, world map, altitude charts, climate bands).
- **Layout QA harness:** every slide passes (it caught and forced fixes for a staircase side-note, a legend overflow on the Hermitage
  slide, and two map-label collisions).
- **Text legibility** (`engine/text_audit.py`): 116 text groups, 0 below threshold (paper text on the first slate blue measured 4.04:1;
  the slate was deepened to about 5:1).
- **Regression:** the two engine changes below are default-preserving; `regress.py` 42 of 42 and `check_reels.py` 26 of 26 after them.
- **Claims:** every number is D1 Chapter 3 (the page ledger is in the renderer's docstring) or arithmetic from D1, labeled on the
  slide. No numeric Winkler (growing degree day) bands appear, because D1 gives none.
- **Photos:** every photo's license and author resolved on Commons; share-alike files were excluded (Douro fog, Monte Bello fog,
  Bordeaux autumn, Epernay, Mendoza banner), so every photo can also go in the Reel. Locations come from each file's own title; the sunset
  and the fog photo carry no place claim.

## Slide 4 (Steve's request): a page on climate change and how the wine world adjusts
New, right after slide 3 (`feature_trio`): three columns, new grapes / new sites / new aspects, with the long-term shift as the footnote. All WSET:
D1 p.44-46 (rising temperatures; later-ripening varieties may be preferable; once-too-cold regions may improve), D1 (Garnacha, drought-tolerant),
D1 p.27-28 (0.6 C per 100 m; shade-facing slopes, Stellenbosch), D3 p.347 (Rioja: high-altitude vineyards more desirable), D3 p.269 (Tuscany: higher
sites, less sunny aspects), D3 Bordeaux (hot, dry European summers). Three new CC BY 2.0 photos (Grenache, Cafayate in Salta Province, Chianti), each
location from its own Commons description. The closing slide's line changed so it no longer repeats slide 4 (and Syrah pepper stays reserved for entry 5).

## Slide 2 (Steve's request): a thermometer
The staircase became a vertical thermometer with the text boxes climbing up the side (a new engine layout, `thermometer`, M27). Cold is at the
bottom, heat at the top; the glass tube is a cold-to-hot gradient and each box takes the color at its own reading. Six readings from D1 p.24-25:
winter freeze, wakes at 10, flowers above 17, works 18-33, sets fruit 26-32, extreme heat. Wording corrected on this pass: D1 says winter freeze
"can damage the vine" (the staircase version said "kill"). The layout raises an error if any note overflows its box.

## Engine changes (all default-preserving)
0. `thermometer`: a new layout (nothing else uses it).
1. `stat_wall`: an optional `famous_label` slot (the strip was hard-labeled "FAMOUS NAMES").
2. `chart_stack`: an empty second legend label now draws only the solid key (it drew an empty hatched swatch).

## Things to know
- The altitude bars are scaled so the longest (18°C) is the full width; all three stay proportional.
- The Hermitage slide uses the 1900s postcard of the hill (the Arc 1 photo); the layout has no credit slot, so it is credited in the caption.
- The benchmark asks for five graphic-led slides; this deck has four. A fifth (a diurnal-range graphic) would need numbers D1 does not give.
- Open for later: a sixth piece could use D1 3.2 Water (500 mm cool, 750 mm warm minimums) and 3.3 Nutrients, which this deck leaves out.
