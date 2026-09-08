# SAVE-BACK v2 — README

## Why this exists

Partway through this session, `core.py`, `modules.py`, and
`quick_sips.py` were found to be **completely absent from
/mnt/project**, despite being included in the earlier
`SAVEBACK_three_ways_v1.zip`. I don't have visibility into why (I
can't see anything outside this session) — but the practical effect is
that the project's actual render engine currently isn't saved
anywhere durable. This package fixes that, and also saves back
`guess_the_region.py`, which had accumulated real changes across the
whole session but had never been packaged before now.

## What's in this zip

- `core.py`, `modules.py`, `quick_sips.py`, `guess_the_region.py` —
  save these into the project, replacing whatever's currently there
  (or filling the gap, if they're still missing).
- `flag_australia_real.png` — save into your project's `photos/`
  folder. `guess_the_region.py`'s Australian flag now pastes this
  image rather than drawing shapes; without the file, any deck using
  `flag="australian"` will error.
- `CHANGELOG_saveback_v2.md` — exactly what changed and why, function
  by function.
- `render_gtr_mclarenvale_EXAMPLE.py`,
  `render_fff_southaustralia_EXAMPLE.py` — working reference scripts
  showing the new `gtr_cover`/`gtr_reveal` overrides and the FFFA
  pattern in use. Not meant to run as-is (they reference this
  session's temp photo paths) — read them as documentation.

## What to do with it

1. **First, check whether `core.py`/`modules.py`/`quick_sips.py` are
   actually still missing from your project.** If they somehow
   reappeared on your end, diff before overwriting — I have no way to
   know what state your project is in from in here.
2. Save the four `.py` files into the project.
3. Save `flag_australia_real.png` into `photos/`.
4. Keep the changelog for reference.

## Also flagging: the Wikimedia Commons access question

Separately from this save-back — if you want me to be able to search
and pull photos from Wikimedia Commons in a future session, that needs
two domains added to your network allowlist (Settings → Capabilities →
Code execution and file creation → Domain allowlist):

- `commons.wikimedia.org` (search, file info, licensing)
- `upload.wikimedia.org` (the actual image files)

Settings changes don't apply retroactively to an open conversation —
start a new chat after adding them.

## Regression coverage

Before packaging, re-rendered end to end against the final files in
this zip: GTR (McLaren Vale, Puglia), Quick Sips (Piedmont), Three Ways
(Zinfandel), FFFA (South Australia). All passed QA clean.
