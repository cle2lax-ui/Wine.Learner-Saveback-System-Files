# Save-back package v8.0 — read this first

Source: Oregon Field Guide build, 2026-08. Start here, then go to
`DESIGN_PROCESS_v8.md` for the full rationale behind everything.

## What's in this package

| File | What it is |
|---|---|
| `core.py` | Updated shared rendering primitives. Merge over the existing project `core.py`. |
| `modules.py` | Updated shared slide modules. Merge over the existing project `modules.py`. |
| `map_atlas.py` | **New file.** Standalone map rendering + label-placement engine. Add to the project alongside `core.py`/`modules.py`. |
| `quick_sips.py` | Updated Quick Sips module — new font hierarchy and spacing defaults, locked in as the v8.1 series standard. Merge over the existing project `quick_sips.py`. |
| `DESIGN_PROCESS_v8.md` | **New file.** Font hierarchy, color luminance, grid design principles, map system pointer, and the mandatory four-designer review process. |
| `NEW_DECK_STARTER_v8_ADDENDUM.md` | **New file.** Additive checklist on top of `NEW_DECK_STARTER_v7.md`. |
| `CHANGELOG_v8.md` | Full changelog: every function changed, every bug fixed, regression test results. |
| `fetch_unsplash.py` | **New file.** Second photo-sourcing option alongside Pexels. **Untested against a live network** — verify first in the new environment. |
| `SETUP_KEYS.md` | Both API keys (Pexels + new Unsplash) and the network allowlist steps Unsplash needs. |

## Install order

1. Merge `core.py`, `modules.py`, and `quick_sips.py` over the existing
   project versions. Every change in all three is backward compatible —
   no existing deck's render should change unless it opts into a new
   parameter, EXCEPT Quick Sips decks specifically pick up the new
   default font sizes/spacing/footer prominence automatically (this is
   intentional — see CHANGELOG_v8.md's "Quick Sips standard" section).
2. Add `map_atlas.py` as a new file alongside them.
3. Add `fetch_unsplash.py`, set `UNSPLASH_ACCESS_KEY` per `SETUP_KEYS.md`,
   confirm network allowlist, and **test it** before relying on it —
   it was built and code-reviewed but never actually reached Unsplash's
   servers in the session that built it (network block in that sandbox).
4. Read `DESIGN_PROCESS_v8.md` in full at least once. It's the reference
   for *why* each rule exists, not just what the rule is — several of
   these look like unnecessary complexity in isolation and only make
   sense once you know the specific bug they fix.
5. Fold `NEW_DECK_STARTER_v8_ADDENDUM.md` into the intake process for the
   next new deck.

## Validation already done

- `map_atlas.py`'s extraction was verified against the original Oregon
  deck's live data: identical rendered output, zero label overlaps in
  both the main map and inset panel, confirmed by direct measurement.
- `core.py` and `modules.py` were run through the project's own
  `specimen.py` regression suite. Result: 6/18 modules pass clean; the
  other 12 fail on missing test-photo assets that don't exist in this
  sandboxed environment, not on any logic error — confirmed by running
  the exact same suite against the untouched baseline files and getting
  a byte-identical result. Zero regressions introduced.
- `quick_sips.py`'s updated defaults were tested against BOTH the deck
  that established them (Alsace Edelzwicker) and the existing Russian
  River Valley reference deck — both build cleanly, pass QA, and the
  hierarchy/prominence improvements hold visually on both, confirming
  these are genuine system-wide improvements rather than values tuned
  to fit one deck's specific content.
- All three Python files (`core.py`, `modules.py`, `map_atlas.py`) import
  together cleanly with no conflicts.

## What's still open

- `fetch_unsplash.py` needs a live network test in the new environment.
- Map label side-assignment (map_atlas.py rule #8) is flagged as a good
  next refinement, not implemented this cycle — see `DESIGN_PROCESS_v8.md`
  §4.
