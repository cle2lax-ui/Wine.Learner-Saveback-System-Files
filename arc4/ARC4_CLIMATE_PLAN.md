# ARC 4: THE CLIMATE ARC (plan for Steve's approval, Oct 20, 2026)

The first topical arc (not regional). Anchor: WSET Diploma D1, Chapter 3, The Growing Environment (pp. 24-46). It follows the Mendocino arc on purpose: fog funnels, cold air pooling, a ridge above the fog and heat classes were all Chapter 3 ideas applied to one county. Arc 4 gives the audience the rules behind what they just saw.

**Thesis:** Climate is the first cause of wine style. Seven natural dials set it, thirty years define it, and a few degrees can erase a signature.

## 1. Shape and cadence
Two posts in week one, three in week two, a summary Reel last (the Arc 3 cadence).

| # | Slot | Format | Title (working) | Source |
|---|---|---|---|---|
| 1 | Week 1 | The Field Guide, 13 slides | Seven Dials, One Vineyard | D1 3.1, 3.4, 3.5, 3.6 |
| 2 | Week 1 | Guess the Wine Region, 2 pages | Same Latitude, Different Ocean | D1 3.1 (p. 30) |
| 3 | Week 2 | Five Fascinating Facts About Climate Change, 6 pages | (series title) | D1 3.6 (pp. 44-46) |
| 4 | Week 2 | Split Decision, 2 pages | Move Uphill or Change the Grape? | D1 3.1, 3.6 |
| 5 | Week 2 | What Am I Drinking?, 2 pages | A peppery Northern Rhone Syrah | D1 3.6 (p. 45) + D3 Northern Rhone |
| 6 | Last | Summary Reel (The Field Guide bumper) | Seven Dials | all of the above |

**Look:** the standard house burgundy as the arc signature (Steve's rule: burgundy or forest green for general topics; Arc 3 used green). All text colors through `core.legible`; run `engine/text_audit.py` on every deck before locking.

## 2. Entry 1: The Field Guide, "Seven Dials, One Vineyard" (13 slides)
The seven natural factors in D1 3.1 are the spine (the chapter lists exactly these: latitude, altitude, slopes and aspect, proximity to water, winds, characteristics of the soil, mist/fog/clouds). Five of the 13 slides are graphic-led.

| # | Slide | Content (all from D1) | Layout idea |
|---|---|---|---|
| 1 | Cover | Seven dials, one vineyard; hook: the same latitude, 1.8 C apart (Willamette 15.9 C vs Bordeaux 17.7 C growing-season mean) | cover_bleed |
| 2 | What the vine needs | 10 C wakes it (dormancy ends, budburst); flowering best above 17 C; fruit set 26-32 C; photosynthesis 18-33 C; last-month mean above 21 C loses acid fast, below 15 C keeps too much (pp. 24-25) | graphic: a vine-year thermometer |
| 3 | Climate is not weather | climate = the pattern averaged over 30 years; weather = the year (Bordeaux 2013 cold and wet vs 2016 warm and dry) (pp. 41, 44) | duel |
| 4 | Dial 1: Latitude | more radiation nearer the Equator; vines grow roughly 30-50 degrees each side (pp. 26-27) | graphic: world map with the two bands |
| 5 | Dial 2: Altitude | falls about 0.6 C per 100 m; Salta vines up to about 3,000 m; Burgundy and the Loire sit low (p. 27) | graphic: elevation staircase |
| 6 | Dial 3: Slope and aspect | sun-facing slopes gain ripeness (Hermitage); Burgundy and Alsace grand crus on south-east slopes; Stellenbosch whites on south-facing slopes to keep acidity (p. 28) | graphic: compass over a hillside |
| 7 | Dial 4: Water | lakes and seas moderate temperature; Carneros vs inland; Finger Lakes; ocean currents: Willamette (15.9 C, California current) vs Margaux (17.7 C, Gulf Stream), both about 45 degrees (pp. 29-30) | duel (the hero comparison) |
| 8 | Dial 5: Wind | Petaluma Gap funnels coastal wind inland; the Zonda warms Mendoza; windbreaks in Neuquen (pp. 30-31) | hero_facts |
| 9 | Dial 6: Soil | free-draining soils warm sooner; light chalk (Sancerre, Champagne) reflects; dark volcanic (Etna) re-radiates at night (pp. 31-32) | blades |
| 10 | Dial 7: Fog and cloud | fog slows photosynthesis only below one third of full sun; Sonoma, Napa, Leyda, Sauternes (pp. 25, 32-33). A callback to Mendocino, no new claim | photo and stat |
| 11 | Diurnal range | big range suits warm regions (Mendoza, Ribera del Duero); small range suits cool-moderate (Mosel, Mornington Peninsula); the Wachau is an exception (p. 33) | chart_stack |
| 12 | Name the climate | WSET bands by growing-season mean: cool 16.5 C or below, moderate 16.5-18.5, warm 18.5-21, hot above 21; maritime, Mediterranean, continental with D1's examples (p. 43) | graphic: a gauge with Willamette and Bordeaux marked |
| 13 | When a dial moves | climate change speeds the cycle and splits sugar from aroma and tannin (pp. 44-45); bridges to the rest of the arc | statement |

*Update (Oct 21, Steve):* slide 2 became a thermometer, and a new slide 4 ("Three Ways Growers Adapt": new grapes, new sites, new aspects, from D1 and D3) follows slide 3, so the Field Guide is 14 slides.

## 3. Entries 2-6
**2. Guess the Wine Region, "Same Latitude, Different Ocean."** Page 1 (no names): a map with the 45 degrees North line, clues about an early-ripening red, a cold ocean current, 15.9 C. Page 2: Willamette Valley, then the Margaux contrast (same latitude, Gulf Stream, 17.7 C, late-ripening Cabernet). D1 p. 30; cross-check D3's Oregon material at build.

**3. Five Fascinating Facts About Climate Change** (cover plus five): (1) the vine cycle speeds up, budburst comes earlier (p. 44); (2) sugar and acid race ahead of aroma and tannin, so grapes are picked riper (p. 44); (3) faster acid loss means higher pH, a winemaking problem (p. 44); (4) some vineyard sites in parts of California and South Africa will likely be abandoned in the next 50-100 years (p. 45); (5) cold regions may improve, but extreme weather and altered rainfall remain a risk (p. 45). Pepper is held for entry 5 so the two posts do not repeat.

**4. Split Decision, "Move Uphill or Change the Grape?"** Side A: go higher (cooler by about 0.6 C per 100 m, brighter UV, a wider day-night range that helps acidity in warm regions; but Salta's high vines may not ripen every year, pp. 27-28). Side B: switch to later-ripening varieties (D1 p. 45 says it may be preferable); early-ripening Pinot Noir and Chardonnay ripen very early in warm climates (p. 25). D1 p. 46 notes site selection, planting material and management are all under review. Both sides stay inside D1; no outside statistics.

**5. What Am I Drinking?** A peppery Northern Rhone Syrah. The reveal: D1 p. 45 names black pepper as a hallmark of Syrah in moderate climates such as the Northern Rhone and says it may no longer develop as temperatures rise. Needs Steve's bottle photo and producer sheet (appellation to be agreed so it does not repeat Arc 1). Facts to check in D3's Northern Rhone chapter at build.

**6. Summary Reel** (60 s or more allowed for Field Guide Reels): the standard glass-and-books bumper, then the seven dials as seven fast beats, ending on the dial that moves. Built on the Arc 3 pipeline (`reel_lib`, rock score, chunked render).

## 4. Rules for this arc
- Only numbers that are in D1 (or derived from D1 by arithmetic, and labeled as derived). The chapter gives **no numeric Winkler (growing degree day) bands**, so no graphic prints them; the dial uses WSET's growing-season-mean bands. D1 notes the Winkler bands were recently extended at both ends, so say "Zone I to V" only with that caveat.
- Derived, not stated: Willamette-to-Bordeaux gap 1.8 C (17.7 minus 15.9); a 3,000 m site is about 18 C cooler than sea level, all else equal.
- Photos: location-verified Wikimedia Commons only; probe category names first (wrong names return zero). Needs: Hermitage hill, Salta, Finger Lakes, Carneros, Sonoma Coast fog, Etna, Willamette. Maps: Natural Earth for the world map.
- American English throughout; five hashtags per post; "The Field Guide" always with "The"; gold text via `core.legible`.
- Not used from Chapter 3 (kept for later): 3.2 Water (500 mm cool and 750 mm warm minimums), 3.3 Nutrients.

## 5. Decisions for Steve (defaults in bold)
1. Arc signature: **burgundy**, or forest green.
2. Order and cadence as in the table: **yes**.
3. Field Guide title: **"Seven Dials, One Vineyard"** (alt. "Climate Is Not a Place").
4. Entry 5: which Northern Rhone Syrah, and send the bottle photo and producer sheet when ready (not needed before entry 1).
5. Entry 6: **Field Guide summary Reel**, or a climate-change FFFA Reel in the rock style.

## 6. Build order and what carries over
Order: 1, 2, 3, 4, 5, 6. From Arc 3: `core.legible`, `text_audit.py`, the 42/42 and 26/26 regression guards, the Reel pipeline (chunked render, measured loudness, no grain). Entry 1 is the heavy build (world map, three diagrams, photos); entries 2-4 reuse existing formats.
