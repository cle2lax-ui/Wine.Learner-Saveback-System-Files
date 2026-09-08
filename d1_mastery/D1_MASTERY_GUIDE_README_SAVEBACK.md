# D1 Chapter Mastery Guide — Save-back v1 (first package for this series)

This is the first save-back for the D1 Chapter Mastery Guide system — nothing from this
codebase exists in project files yet. Extract everything into the project files area
alongside the existing wine-deck system files (`core.py`, `modules.py`, `tokens.py`, etc.) —
no naming collisions, all files here are new.

## What's in this package

```
D1_MASTERY_GUIDE_STYLE_GUIDE.md     — NEW. Read this first, every future session.
D1_MASTERY_GUIDE_CHANGELOG.md       — NEW. This session's build history.
D1_MASTERY_GUIDE_README_SAVEBACK.md — NEW. This file.

mastery.py                          — NEW. Layout engine.
graphics.py                         — NEW. Diagram library (14 classes + drawing primitives).
examkit.py                          — NEW. MCQ/SWA section builders.
qa_orphans.py                       — NEW. Fast text-based QA pass.
qa_widows.py                        — NEW. Font-aware QA pass — the one that matters.

ch1.py                              — NEW. Chapter 1: The Vine (locked, 15 pages).
ch2.py                              — NEW. Chapter 2: The Vine Growth Cycle (locked, 16 pages).
ch3.py                              — NEW. Chapter 3: The Growing Environment (locked, 18 pages).
ch4.py                              — NEW. Chapter 4: Approaches to Grape Growing (locked, 15 pages).
ch5.py                              — NEW. Chapter 5: Vineyard Establishment (locked, 14 pages).
```

**Not included, regenerate per session per the documented font pipeline** (§2 of the style
guide): `fonts/raw_PlayfairDisplay[wght].ttf`, `fonts/raw_Archivo[wdth,wght].ttf`,
`fonts/raw_ArchivoItalic.ttf`, and the five static instances derived from them
(`Serif-Semi.ttf`, `Serif-Bold.ttf`, `Sans-Reg.ttf`, `Sans-Bold.ttf`, `Sans-Ital.ttf`). Same
convention as every other font this account's projects use — never stored, always
regenerated fresh. The exact fetch URLs and instancing weights are in the style guide and
have been verified to reproduce the working font set byte-for-byte.

## Where things go

All ten `.py` files → project root, as one flat set. A future Chapter 6 becomes `ch6.py`
living alongside these — no subfolder structure.

## Status: locked

Chapters 1–5 are final. This save-back exists specifically so a **new chat, opened later,**
can build Chapter 6 (and beyond) without re-deriving the visual system, the widow-prevention
mechanics, the graphics-device choices, or the editorial voice through another round of
iteration. The style guide is written for that reader — start there.

## Regression status

`qa_orphans.py` and `qa_widows.py` both report clean on all five locked guides as of this
save-back. Independently verified by a clean-room rebuild: fonts regenerated from scratch via
the documented procedure, all five chapters rendered from the exact files in this package,
QA re-run against that output — passed. This package is confirmed self-contained and
reproducible, not just "worked on my last build."

## Open items for whoever builds Chapter 6

- `ch2.py`'s duplicate "EXHIBIT 2.7" label (should be 2.8 on the second instance) — cosmetic,
  documented in the style guide §12, not fixed because the guide is locked. Fix opportunistically
  if that file gets reopened for another reason; don't reopen it just for this.
- The `Venn` class in `graphics.py` is present but unused — `InclusionRings` and
  `LineageChart` replaced every real case it was tried on. Kept in case a genuine
  partial-overlap relationship comes up in a later chapter; the style guide flags it as a
  last resort, not a first choice.
- No chapters beyond 5 have been scoped yet. Whoever starts Chapter 6 should confirm against
  the D1 textbook's own chapter list how many guides this series ultimately needs.

## Before next session touches mastery.py or graphics.py

Per standing practice across every project in this account: diff the working copy against
this save-back before assuming either is current. This package *is* the canonical copy as of
today, but the habit of checking doesn't change just because this is a new series.
