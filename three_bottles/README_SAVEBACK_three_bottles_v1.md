# SAVE-BACK — Three Bottles v1

*Format renamed from "Three Ways" to "Three Bottles" after this save-back landed -- see THREE_BOTTLES_STYLE_GUIDE.md. File names below reflect the current, renamed files in the repo, not the literal names as originally delivered in this save-back's zip.*

## What's in this zip

- `core.py`, `modules.py` — updated. Save these into the project,
  replacing the current versions.
- `quick_sips.py` — updated, but **rebuilt from the current
  `/mnt/project/quick_sips.py`**, not from this session's working
  copy (which had gone stale — see CHANGELOG for what that means and
  why it mattered). Safe to save over the current file; it contains
  everything currently in the project plus one small addition.
- `THREE_BOTTLES_STYLE_GUIDE.md` — the series style guide. Save into the
  project alongside `GTR_STYLE_GUIDE.md`, `QUICK_SIPS_STYLE_GUIDE.md`,
  `FFFA_STYLE_GUIDE.md`.
- `NEW_DECK_STARTER_three_bottles.md` — kickoff checklist for the next
  Three Bottles deck.
- `CHANGELOG_three_bottles_v1.md` — exactly what changed in the code and
  why, function by function.
- `render_three_bottles_EXAMPLE_zinfandel.py` — the finished "Three Faces
  of Zinfandel" render script, as a working template for the next
  deck. Not meant to be run as-is against your project (it references
  photo filenames from this session's working directory) — copy it
  and swap in new content per the New Deck Starter doc.

## What to do with it

1. Save `core.py`, `modules.py`, `quick_sips.py` over the current
   project versions.
2. Add `THREE_BOTTLES_STYLE_GUIDE.md` and
   `NEW_DECK_STARTER_three_bottles.md` to the project files.
3. Keep `CHANGELOG_three_bottles_v1.md` for reference; doesn't need to be
   "used," just useful if a future session needs to know what changed
   and when.
4. `render_three_bottles_EXAMPLE_zinfandel.py` is a reference, not
   something to run directly — the bottle/region photos it points to
   only exist in this session's temp workspace.

## One thing worth your attention

While regression-testing this save-back against the existing series,
I found that `quick_sips.py` (as it currently exists in the project)
already calls a `_finish()` parameter — `footer_size` — that
`modules.py` doesn't define. That means **any Quick Sips deck
rendered against the current project files would crash** with
`TypeError: _finish() got an unexpected keyword argument
'footer_size'`. This wasn't something I introduced — it's a leftover
from `quick_sips.py` and `modules.py` having been saved back on
different occasions without a joint regression test. I added the
missing `footer_size` param to `core.py`/`modules.py` in this
save-back and re-tested a real Quick Sips deck against it to confirm
it's fixed. Worth double-checking that this is genuinely what
`footer_size` was meant to do (it now controls the footer text's
point size, defaulting to the same 60px as before) — I inferred the
intent from context since there was no changelog entry for the
original addition.

## Regression coverage

Re-rendered end to end before packaging: Quick Sips (Piedmont), GTR
(Puglia), FFFA (Santa Barbara County), Three Bottles (Zinfandel). All
four passed QA clean against the final files in this zip.
