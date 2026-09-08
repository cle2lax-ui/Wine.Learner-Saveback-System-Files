# Save-back — FFFA v4 (South Australia session)

Save these into project files manually.

| File | Action |
|---|---|
| `core.py` | **Replace** — `footer()` gains `credit_size=34`; default unchanged, no other caller affected |
| `fff_facts.py` | **Replace** — credit size 28, closing-page credit moved to footer |
| `render_fff_southaustralia.py` | **New** — replaces `render_fff_southaustralia_EXAMPLE.py` |
| `FFFA_SA_PHOTO_CREDITS.json` | **New** — Commons file titles, artists, licences, description URLs |
| `CHANGELOG_fffa_v4.md` | **New** |

Photos are not included (per the standing convention that photo and font
assets are re-fetched each session). `FFFA_SA_PHOTO_CREDITS.json` carries
every Commons file title and description URL needed to re-fetch them.

`specimen.py` was re-run after the `core.py` change: no code regressions.
The 12 modules reported failing all fail on missing photo assets in a
fresh session, not on QA or geometry; every module that renders without a
photo passes clean.

Still pending from earlier sessions and **not** touched here: the six
Cava-session `modules.py` changes, the `quick_sips.py` lead-in size
defaults, the global tighter-leading default, and the Letter Wine List v1
roll-in.
