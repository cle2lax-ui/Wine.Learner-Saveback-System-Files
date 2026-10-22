# Review: The Field Guide: Climate ("Climate's Impact on Wine") -- 15 slides, built, awaiting Steve's review

Files: `arc4/render_fg_climate.py` (the deck), `arc4/prepare_climate_maps.py` (the world map), `arc4/CAPTION_FG_climate.md`.
Output: `/home/claude/out_fg_climate/` (13 PNGs at 2160x2700 and `FG_Climate_review.pdf`).

## What was checked
- **Layouts:** 15 distinct layouts in 15 slides; five led by a graphic (the Factor wheel, world map, altitude cross-section, thermometer, climate bands).
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

## Restructure (Steve, Oct 21): Factors, a wheel, icons, a climate-change section
- "Dials" became "Factors" everywhere. New slide 2, the **Factor wheel** (new engine layout `factor_wheel`, M28): a hub with the seven Factors around it, each
  with a code-drawn icon (`engine/icons.py`) and a number. Slides 3-9 are the seven Factors in that order, right after the wheel, each carrying its icon and number as a
  badge (top right). Then the day-night gap, the vine's thermometer, naming the climate, and the closing slide "When a Factor Moves", which now leads into the
  last two slides, labeled **A Few Words on Climate Change** (climate vs weather, then the three ways growers adapt).
- The thermometer moved from slide 2 to slide 11 (the Factors must follow the wheel directly). The closing slide sits before the climate-change pair, as the lead-in.

## Slide 15 (Steve's request): a page on climate change and how the wine world adjusts
Titled "Longer-term climate trends are getting warmer" (Steve's wording, on two lines). Written as slide 4 and moved to the end (`feature_trio`): three columns, new grapes / new sites / new aspects, with the long-term shift as the footnote. All WSET:
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
0. `feature_trio` now accepts a two-line headline and raises an error if any line is too wide (a long title used to clip silently with no QA flag).
0. `thermometer`, `factor_wheel`, `cross_section` and the icons (`engine/icons.py`): new layouts and helpers (nothing else uses them).
1. `stat_wall`: an optional `famous_label` slot (the strip was hard-labeled "FAMOUS NAMES").
2. `chart_stack`: an empty second legend label now draws only the solid key (it drew an empty hatched swatch).

## Things to know
- Slide 4 (Factor 2, altitude) is a cross-section of an IMAGINARY region (new engine layout `cross_section`, M29): a seaside plain, gradual slopes, then steep slopes, with
  flagged vineyards at 0, 500, 1,000, 2,000 and 3,000 m, each marked "cooler" than the seaside baseline by D1's 0.6°C per 100 m (3.0, 6.0, 12.0, 18.0°C: our arithmetic, labeled).
  It replaced a bar chart whose bars grew with altitude while meaning "cooler" (Steve's note). Salta's real range (D1, about 1,280 to 3,000 m) is in the footnote.
  The layout keeps all text at 60 px or more and never lets two flags overlap.
- The Hermitage slide (now slide 5) uses a color photo, "Tain - Chapelle et vignoble" by Véronique Pagnier (public domain; the file says "Chapelle et vignes à Tain l'Hermitage, Drôme"), cropped to the hill and chapel, replacing the black-and-white postcard (Steve's request). It has four callouts: the photo does not say which way each slope faces, so nothing points at a slope and calls it shaded. The layout has no credit slot, so the credit is in the caption.
- Open for later: a sixth piece could use D1 3.2 Water (500 mm cool, 750 mm warm minimums) and 3.3 Nutrients, which this deck leaves out.


---

# Round 2: the four-designer review and the brevity pass (run before locking; Steve asked whether they had been run, and they had not)

Every slide was rendered and viewed in four review sheets, then re-viewed after the fixes.

## Brevity pass
Counted EVERY visible word per slide with `arc4/brevity_count.py` (new; merges letter-spaced text, drops duplicate blocks, leaves out only
READ MORE, page numbers and photo credits). Before: 1,032 words, EIGHT slides over the 70-word budget (3: 76, 4: 87, 7: 81, 9: 75, 10: 88,
11: 104, 14: 106, 15: 108). After: 827, none over (largest: slide 5 at 69). Mendocino: 561; Mosel: 725.

## Anna Wintour (claims, each checked against the D1 text)
- Slide 6: "it is the water" overstated D1 (the Gulf Stream is "at least partially" the cause). Now: "Ocean currents help explain the gap."
- Slide 10: "A big range helps" / "A small range helps" became "often helps" / "may help" (D1: "often thought to be favourable", "may be favourable").
- Slide 5, chip C: "count most" became "count for more" (D1: importance "increases at high latitudes").
- Slide 3: "often too cool" became "cooler temperatures" (D1's wording).
- Slide 15: "later-ripening, drought-tolerant varieties like Garnacha" implied Garnacha is later-ripening; D1 says only drought-tolerant. Split into two sentences.
- Checked, no change: Bordeaux 2013/2016 (every detail matches), mist and fog, the Wachau, chalk, the winds, the WSET bands in F.

## Coco Chanel (every figure once; cut what repeats)
- 0.6 C per 100 m was on slides 4 and 15: kept on 4. Willamette 15.9 C and Margaux 17.7 C were on slides 6 and 12: kept on 6 (slide 12 keeps the names).
  Stellenbosch was on slides 5 and 15: kept on 5.
- Cut: slide 3's pale latitude-line names (the bands already say 30-50); slide 4's axis labels and "Sea" (the flags carry the heights);
  slide 7's standfirst (repeated the headline); slide 9's "dense mist is fog"; slide 11's second F column and its wordy standfirst;
  slide 12's second example per climate pattern; slide 14's Picked-early and Result rows folded into two rows per year; slide 15's repeated footnote clauses.

## Jony Ive (craft)
- Slide 3: the latitude-line names were tiny, pale italic and collided with "Mendoza" and "South Africa": removed. "N. France, Germany" ran over
  the Scandinavian coast, then (after a first move) over the Gulf of Mexico: now on the open Russian plain, clear of every outline. The layout QA caught one
  collision on the way (it is why the label is where it is).
- Slide 12: the "Three Patterns" strip sat on the footer (no clearance). One example per pattern now keeps it to one line, and cell height is capped.
- Slide 15: the long title clipped silently (the headline helper never checked width): feature_trio now takes a line break and raises on any line too wide.

## Massimo Vignelli (grid)
- Slide 5: the legend ended two-thirds down. The hero photo grew (1,160 to 1,480 px); the four chips were re-placed on the hillside.
- Slide 3: the map was short for its page. Window and standard parallel adjusted (aspect 1.607): about 14 percent taller.
- Slide 12: with only four stats the cells stretched; capped at 650 px so the strip rises off the footer.
- Noted, not changed: slide 12's 2x2 cells still leave open paper inside each cell (the layout has no smaller-type setting).

## Engine changes (all default-preserving; regress 42/42, Reel frames 26/26)
`spotlight` optional `hero_h`; `stat_wall` optional `cell_max`; `cross_section` accepts empty `ticks` and `sea_label=None`; `feature_trio` takes a
line break in its headline and checks width; the map window and standard parallel are set in `prepare_climate_maps.py`.
