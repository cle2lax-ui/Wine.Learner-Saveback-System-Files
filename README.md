# Wine.Learner — Saveback System Files

Instagram wine-education deck system (Python/PIL, 2160×2700 built @2x) for
WSET / CSW audiences, plus the D1 Mastery Guide system.

## Start here

| If you want to… | Read |
|---|---|
| Build a Field Guide to the current standard | `guides/VISUAL_BENCHMARK_v10.md` — **the Mosel Field Guide is the benchmark** (git tag `fg-mosel-final`) |
| Know what every slide module does | `guides/STYLE_GUIDE_v5.md` §7 (M01–M26) |
| Understand the series and cadence | `guides/SERIES_SYSTEM_v9.md` |
| Understand a past bug before repeating it | `guides/LESSONS_LEARNED_v5.md` (v10 section: the Mosel build) |
| Check the engine hasn't drifted | `python3 engine/regress.py` |

## Layout

```
engine/    shared rendering: tokens, core, modules (M01–M26), map_atlas, build,
           specimen (regression suite), variety, palette, regress
formats/   per-series layouts (GTR, FFFA, Split Decision, …)
arc1/ arc2/ renders/   per-arc build scripts and captions
specs/     per-deck specs — look here BEFORE building a deck
guides/    style guides and process docs
data/      photo manifest, geographic data (data/geo)
reference/ frozen pixel hashes for the regression guard
photos/ fonts/ sourcing/ d1_mastery/ archive/
```
