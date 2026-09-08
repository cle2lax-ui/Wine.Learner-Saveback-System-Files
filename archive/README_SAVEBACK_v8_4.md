# Save-back v8.4

**Save these files into the project.** Without this, the next session
starts from `/mnt/project`'s last checked-in state and repeats the
divergence this save-back closes.

## What's in this package

```
core.py                          — REPLACE (adaptive footer, carried from earlier this session)
modules.py                       — REPLACE (see CHANGELOG_v8_4.md for full list)
render_fg_aroma_chemistry.py     — NEW (the locked 12-slide deck's render script)
photos/                          — NEW, 37 files (every photo the locked deck uses)
CHANGELOG_v8_4.md                — this session's full change list
README_SAVEBACK_v8_4.md          — this file
```

`tokens.py` is unchanged this session — not included.

## Where things go

- `core.py`, `modules.py`, `render_fg_aroma_chemistry.py` → project root,
  replacing/adding alongside the existing `build.py`, `specimen.py`,
  `fetch_unsplash.py`, etc.
- `photos/*.jpg` → your photo directory (same location as
  `faults_ladder_cellar.jpg` and the other existing deck photos).

## Before next session touches modules.py or core.py

Per standing rule: diff the working copy against this saved-back
version before assuming either is current. `core.py` in particular has
historically had no reliable canonical copy in the project — confirm
it's actually landed this time.

## Regression status

`specimen.py` was not re-run against this save-back before delivery —
recommend running it at the start of the next session that touches
`modules.py`, since this save-back changes six modules
(`grid_cover` new, `horizontal_trio` new, `feature_trio`, `card_grid`,
`duel`, `process_map`, `editorial_lead`, `mosaic` all modified) in one
pass.

## Open items for next session

- **`cover_fit` zoom-for-narrow-columns limitation** (documented in
  CHANGELOG under "Things tried and reverted") isn't fixed, just
  understood. If a future deck needs "show more of a roughly-square
  photo in a tall narrow column," the real fix is a wider column, not
  a `cover_fit` change.
- Every other per-deck pending item from prior save-backs (Cava/
  Corpinnat inset work, Quick Sips lead-in sizing, global leading
  pass) is unrelated to this session and still open as previously
  documented.
