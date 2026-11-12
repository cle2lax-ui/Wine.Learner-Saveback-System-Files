# Reels: motion graphics for Instagram (9:16)

First Reel: **Germany in 30 Seconds** (`germany_reel.py` + `germany_audio.py`, toolkit in `reel_lib.py`).
1080 x 1920, 30 fps, 900 frames, H.264 High + AAC 48 kHz stereo, -14.1 LUFS, true peak -2.9 dBTP.

**v2, 30 s** (Steve: "it goes by too fast"). v1 was 20 s (commit `1d7892f`). Every scene is now a whole number of 2-second
bars, so every cut lands on a downbeat; each scene's reveals run slower by its own factor (the text-heavy Treppchen scene x1.45,
the dense reds scene x1.35, others x1.10-1.20), then the scene holds while its camera keeps drifting, and static backgrounds get
a slow push-in so no hold freezes. `SCENE_TABLE` in `germany_reel.py` is the single source of truth: the audio reads every
event time from it through `T(scene, u)`, so a sound cannot drift off its picture event when the timing changes.

## What it says, and where each fact comes from
Every on-screen fact comes from the four Germany posts, where it was sourced and reviewed:
| Time | Post | On screen |
|---|---|---|
| 0-2 s | (hook) | GERMANY, in 30 seconds |
| 2-6 s | Mosel Field Guide | the Mosel's course (Natural Earth river data, public domain), then "SLOPES UP TO 70%", "Riesling on slate, above a looping river." |
| 6-10 s | Mosel Field Guide | the Pradikat ladder (Kabinett to TBA): "FIVE RUNGS. NONE MEANS SWEET." "Ripeness at harvest, not sugar in the bottle." |
| 10-16 s | What Am I Drinking? | Dr. Loosen Erdener Treppchen Riesling Auslese 2020; "So steep, they built stone steps."; SWEET; 7.5-8% ALC. |
| 16-20 s | Guess the Region: Baden | "Known for red..." 61% OF ITS VINES ARE WHITE; the Kaiserstuhl, an extinct volcano |
| 20-26 s | Five Fascinating Facts | NEARLY A THIRD OF GERMAN VINES ARE RED (about 10% in 1980, 32% in 2021); Pinot Noir almost tripled; Dornfelder 0 to No. 2 red; Ahr 4 in 5 vines red |
| 26-30 s | (outro) | PROST. Germany, in four posts. Full stories on our grid |
**One addition not in the posts:** the translation of *Treppchen*, "little staircase" (diminutive of *Treppe*, stairs), which ties
the Loosen scene to the ladder before it.

## Licensing (a video is a derivative work)
Only freely usable images: Pexels (Bremm loop, tom analogicus; toast, RDNE Stock project), Unsplash (Kaiserstuhl terraces, Hanna
Schwichtenberg; red grapes, Sven Finger), and Steve's supplied bottle shot. **The two CC BY-SA photos used in the decks (Hatzenport,
the Ahr) are deliberately excluded:** share-alike would extend to the video. The river and the Rhine are Natural Earth (public domain).
The traced wine-region polygons (`anbaugebiete.geojson`) are **not** used: their source SVG's license is undocumented. The score is
original and synthesized in code: no library music.

## Rendering
`python3 germany_reel.py --preview 1.0,3.2,...` renders a contact sheet of chosen moments (about 0.5 s a frame).
**A full render is done in chunks:** the sandbox ends background processes when the tool call that started them returns (a `nohup`
render died at frame 150). Render in 150-frame chunks (`--render seg0.mp4 0 150`, then `150 300`, ... up to `750 900`; about 60 s each, two per call), join them with the
ffmpeg concat demuxer (`-c copy`; every chunk starts on a keyframe with identical settings), then mux:
`python3 germany_audio.py audio.wav` and `ffmpeg -i video.mp4 -i audio.wav -c:v copy -af volume=-3.7dB -c:a aac -b:a 192k`.
The -3.7 dB is measured, not guessed: the mix measures -10.3 LUFS (both versions) and Instagram normalizes to -14.

## Audio, and its limit
120 BPM in A minor (Am-F-C-G), one chord per 2-second bar so the music's bars are the picture's scenes. Sound effects are placed
at the picture's own event times; measured, the strongest transient lands on each of the seven cuts at **0 ms** error (re-verified at 30 s). **It was
checked by measurement, not by ear** (I can't listen to audio). Instagram's audio library can replace it at posting time.

## Lessons from the first Reel
- **Fit headline type to the width, don't assume it.** GERMANY at 232 px ran off the frame; it is now fitted (198 px).
- **Measure what a framing buys** (the cover-zoom lesson again) and **check the encoded file**, not the renderer: QA frames are decoded
  from the final MP4, including both sides of every chunk seam.
- **A pattern behind a product reads as an artifact.** A faint diagonal stair motif behind the bottle looked like a stray ribbon; a
  deliberate stone-steps illustration that builds with the copy replaced it.
- **Name the post on screen.** The same red chip (FIELD GUIDE, WHAT AM I DRINKING?, GUESS THE REGION, FIVE FASCINATING FACTS)
  tells a new viewer this is four posts, which is what the closing call to action asks them to go and find.

## Toolkit: any canvas size (October 2026)
`reel_lib.py` now clips every drawing operation to the canvas it is given, `Photo(size=...)` and `vgrad(height=...)` take a size,
and the grain and vignette are built per canvas size, so the same primitives draw a 2160x2700 deck page. For the Reel's own
1080x1920 the computations are unchanged: seven reference frames of the finished Germany Reel hash identically before and after.
Themes for decks in this language are in `engine/themes.py` (USA, Germany, burgundy, forest green), each contrast-checked.

## The Field Guide: Mendocino (Arc 3; all entries are Reels) -- LOCKED, tag `fg-mendocino-reel-final`
`mendo_fg_reel.py` + `mendo_fg_audio.py` (theme `usa`); shared instruments in `reel_audio.py`; the bumper in `tfg_bumper.py`.
74 s: bumper, hook, the place (the AVAs appear in creation order, 1982-2024), two climates (one-row chips that wrap inside
themselves, `fit_chips`; a white "Altitude flips it" card), the fog machine (fog flows from the real coastline into the real
Anderson Valley AVA; the Navarro is named, not drawn), Islands in the Sky (CSW; ridges illustrative), by the numbers, the Pinot
Noir, sparkling and Alsace's grapes 9 degrees further south (a latitude ruler), the business, end card, outro bug. Caption with
the required CC BY 2.0 credit: `CAPTION_FG_mendocino.md`; voiceover script: `VO_mendo_fg.md`.
**Regression guard for Reels:** `check_reels.py` compares 13 reference frames (`REEL_HASHES.json`). Run it after any change to
`reel_lib.py`, `reel_audio.py`, `tfg_bumper.py` or a Reel module.

### The Field Guide bumper (`tfg_bumper.py`) -- opens and closes every Field Guide Reel
A white line-art book opens (a page turns, text writes itself) beside a white line-art glass that fills with burgundy wine
(86, 14, 40, measured); a small white-on-red THE FIELD GUIDE chip in the arc's chip color. **Identical on every Reel**; the arc
shows only in the ribbon bookmark and the chip color. `bumper_outro()` mirrors it: the wine drains, the lines erase, the book
swings closed. Sonic logo: swish, cover thup, page flutter, glass ting, pour, bells A-E-A (descending in the outro).
One renderer (`_frame`) driven by two timelines (`_intro_state`, `_outro_state`).

### Restored after a container reset (October 2026)
The local repository was lost before these commits were pushed. Everything was rebuilt by replaying every change from the
conversation record, in order, onto the last pushed state (`4f1ae0c`), and verified against the locked deliverable already in
Steve's hands: 17 frames re-rendered from the rebuilt code vs the same frames decoded from the locked MP4 -- PSNR 35.9-43.0 dB,
worst 32px block 8.8 levels of 255 (compression noise; a missing element would be 40+); the rebuilt soundtrack correlates
0.998 with the locked file's audio. **Lesson: push as soon as a token is available; unpushed work lives only in a container
that can reset.**
**Environment setup after a reset** (not in the repo, so it must be recreated): `pip install shapely --break-system-packages`;
`mkdir -p /home/claude/styleguide && ln -s /home/claude/repo/photos /home/claude/styleguide/photos && ln -s
/home/claude/repo/fonts /home/claude/styleguide/fonts` (tokens.py reads both paths). Then `python3 engine/regress.py` (42 decks)
and `python3 reels/check_reels.py` (13 Reel frames) must both pass. Note: 20 Arc 1 (Northern Rhone) photos listed in the photo
manifest are not in the repo; their Commons URLs are in the manifest if those decks are ever re-rendered.

## Guess the Region: Anderson Valley (Arc 3, entry 2) -- LOCKED, tag `gtr-anderson-valley-final`
`mendo_gtr_reel.py` + `mendo_gtr_audio.py`; reuses the Field Guide Reel's toolkit by import (theme colors, the stripes wipe,
whip, map data and cameras, chips, type helpers), so `check_reels.py` must keep passing. **The Guess the Region ident**
(`gtr_ident.py`, `ident(t, accent=)`, `ident_audio()`): same family as The Field Guide bumper (white line art, warm dark
ground, the arc's chip color), its own emblem (compass and map pin) and sonic logo (a rising fifth: a question). The points
meter is an OVERLAY drawn after the transitions, so it stays fixed while the clues push past underneath. Lessons: take the
LATEST meter mark, not the largest value (the first version never dropped); fit long reveal titles to the width.
**v2 (Steve):** the ident now animates the series' own logo, the FOLDED MAP AND PIN (geometry recomputed from
`guess_the_region._folded_map_icon`'s parameters, so it ends on the exact mark): the open map draws itself while swiveling
in from about -38 degrees, the dashed route draws, the pin drops in and bounces (filled, so the map's edge doesn't show
through it at Reel size), its inner ring pops, a ripple, the chip. Clue B is now real geography: the coastline from the
US Census county polygons filled as land WITHOUT county lines (they would hint at the county), the actual Anderson Valley
AVA polygon (UC Davis, CC0) unlabeled, its NW-SE axis from the polygon's minimum rotated rectangle through its area
centroid, and the distance to open ocean MEASURED (about 4 miles), confirming the clue's "a few miles".
**v3 (Steve):** clue A is viticulture (rain in inches, spring frost in the low spots), not the dialect; the countdown reads
MAKE YOUR GUESS, THE ANSWER IS COMING IN. Lessons: `out_back(0)` returns 2.2e-16, not 0 -- guard any stroke whose length
scales with an easing (the snowflake drew a dot, as the bumper's text lines once did); when replacing a function, cut by the
NEXT TOP-LEVEL definition and diff the module's top-level names afterwards (a nested `def` and a plain module-level
assignment were both caught that way).
**v4 (Steve):** no rules page, no points (CLUE #1 .. #4; HOW MANY CLUES DID YOU NEED?); the reveal holds 9 s; the ident's map
unfolds from folded while it spins. The score's sections are now READ FROM THE PICTURE (QUIZ/PAUSE/ANSWER from T()), so
timeline changes cannot strand the music. Lesson (true peak): with the clues starting at 3.0 s, a full kick landed on each
stripes wipe's big impact; the AAC encoder overshot to +0.6 dBTP on the stacked low end, and a pre-encode limiter could not
catch it. Fix at the source: the wipe's impact REPLACES the kick on its beat. Result -14.7 LUFS, -1.6 dBTP.
**v5 (Steve):** the ident is 1.5x faster (2 s; `SPEED` scales its original 3-second timeline, and the sonic logo with it);
GUESS THE / REGION is a two-line chip sized to the width; the pin is red (the arc's accent) with a white inner ring. The
Reel's SCENE_TABLE and cut lists are now built from the scene lengths, so a change to one scene moves everything after it.
Render note: keep render calls to two or three 150-frame chunks; four ran past the 300-second tool limit and left two
chunks half-written (caught by counting each chunk's frames before joining).
**v6 and LOCKED:** larger CLUE chips (60px). `check_reels.py` now guards both locked Reels (13 + 12 reference frames).
**v7, re-locked:** the ident holds 0.5 s longer (2.5 s); CLUE chips 96px; the reveal's kick at 0.85 to keep true peak
under -1 dBTP after encoding (check true peak again whenever timing moves: AAC overshoot depends on where transients fall).
**v8, re-locked:** the series title is GUESS THE WINE REGION; vines are drawn as trunk + lobed leaf + grape bunch (`_vine`).
Lesson for small icons: a vine must show its FRUIT to read as a vine; canopy shapes alone read as trees.


## COMING UP: a 30-second trailer (November 2026)
`trailer_reel.py` + `trailer_audio.py` (assets in `trailer_assets/`, caption in `CAPTION_TRAILER_coming_up.md`). 1080 x 1920, 30 fps, 900 frames, H.264 High + AAC 48 kHz, -14.0 LUFS, -3.6 dBFS peak.
It trails the next two weeks of posts: the four locked Arc 4 posts as their real pages (cards that slide in, drift and swipe), then a six-second tease of Arc 5 (South Africa), then FOLLOW.
| Time | Beat |
|---|---|
| 0-2 s | COMING UP (on frame 1) |
| 2-8 s | The Field Guide, "Climate's Impact on Wine": cover, then three swipes |
| 8-12 s | Guess the Wine Region: the clues page and a pulsing "?" |
| 12-18 s | Five Fascinating Facts: the cover, then all five facts |
| 18-22 s | What Am I Drinking?: the mystery page and a pulsing "?" |
| 22-28 s | THEN, A NEW ARC: Wines of South Africa (tease from the Arc 5 plan; removable) |
| 28-30 s | FOLLOW; fades to black so the Reel loops into its opening |
**The progress element** (spec category 1): five nodes, one per beat, empty on frame 1 and complete on the last beat, so the loop reads as continuous.
**Safe zone:** the sub-line and the strip sit above y = 1650 (the bottom 270 px is Instagram's own interface); the first build had them at y = 1700 and 1587 and they were moved up.
**Render:** six 150-frame chunks (`--render segN.mp4 START END`), joined with the concat demuxer, then muxed. QA was run on the encoded file: the step across each chunk seam matches the steps on either side (2.0-2.5), every cut jumps exactly on its scene-start frame, and the impact stem starts at 0.00 ms on every cut (measured by subtracting a build with silent impacts, same seed).
**Lessons:** (1) type over a photo needs measured contrast against the *brightest 5%* of the background, not a glance: the tease headline measured 3.1:1 white and about 2.5:1 gold at first; the darkening was swept (0.28 to 0.52 at the top of the ramp) until white was 6.0:1, gold 3.5:1 and the bullets 11.7:1. (2) Bullets must fade in with their text, not before it. (3) An envelope detector adds 15-50 ms of lag to an onset: to verify a sound's start, subtract a silent-event build instead.
**Guard:** eight trailer frames are in `REEL_HASHES.json` (34 of 34 now match).

## WATCH OUR PAGE FOR THESE POSTS: the Wines of South Africa trailer (November 2026)
`sa_trailer_reel.py` + `sa_trailer_audio.py` (photos `photos/sa_*.jpg`, graphics `trailer_assets/sa_fg_*.jpg`, caption `CAPTION_SA_TRAILER.md`). 1080 x 1920, 30 fps, 900 frames, H.264 High + AAC 48 kHz stereo, -16.0 LUFS, -3.2 dBFS peak.
It replaces the Arc 4 trailer (`trailer_reel.py`, kept but unused). Brief: all about the South Africa arc; titled "Watch our Page for These Posts"; posted with the South Africa Field Guide; tease the posts that follow; photography and motion immediately.
**Version 2 (Steve, after the Field Guide locked, tag `sa-field-guide-final`):** (1) graphics from the final Field Guide: its Africa line drawing (South Africa in gold, `data/geo/africa_countries.geojson`) on the opening and closing frames, a swipe through four of its real slides (cover, climate, Sauvignon Blanc and Chardonnay, the Simonsberg wards) for "out now", and its real district map with every name masked for "Guess the Wine Region"; (2) natural-color photos (the Field Guide cover's Overberg vineyards replace the pink-graded sunset); (3) the score is a quiet synthesized acoustic piano (G major, one chord per 2-second bar so the cuts land on chord changes, starts on frame 1, the last chord rings under the fade so it loops G to G), about -16 LUFS; (4) the whimsical effects are gone: no drums, bass, pad, ticks, pops, claps, hats, risers or impacts; the only effect is a very soft page-turn swish at each of the six cuts. Text contrast re-measured against the brightest 5% of the picture behind it (14 checks: gold 3.2:1 to 5.4:1 on large type, white 5.6:1 to 11.8:1). Chunk seams verified invisible; the six hard cuts jump as they should.
**Guard:** nine `sa_trailer_reel` frames are in `REEL_HASHES.json` (re-registered for version 2).
**Guard caveat (November 2026):** the reference hashes are sensitive to library versions. The original build environment is gone; in the current one (Pillow 13, NumPy 2.5) the guard passes 41 of 43 under OpenCV 4.10 or 4.11 and 23 of 43 under OpenCV 5.0, with the same code (no older Reel file changed: 0 differences from the pushed code). The two straggler frames (`mendo_fg_reel` @ 34.50 s, `mendo_gtr_reel` @ 17.00 s) are library drift, not code changes, and were left alone. The `sa_trailer_reel` hashes were registered under OpenCV 4.11. Run the guard with OpenCV 4.10 or 4.11 until the older hashes are deliberately re-registered. OpenCV 5.0 versus 4.11 moves the trailer's pixels by under 0.05 of 255 on average.
**Animated title (from the first draft, kept):** the hook's title and subline and the outro's "FOLLOW" are kinetic type (`kinetic()`, `karaoke()`): on frame 1 the whole line is readable but each letter starts 40 px low, 14% large and 3 degrees off, then springs into place left to right; once settled the letters ride a slow wave, and two light sweeps pass through the title; a highlight travels word by word through the subline. Legibility on frame 1 is the Reel spec's rule, so letters are never faded in from nothing (alpha floor 0.9).
