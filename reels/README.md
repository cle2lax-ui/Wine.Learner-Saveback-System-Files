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
