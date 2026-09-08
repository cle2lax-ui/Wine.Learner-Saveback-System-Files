# Save-back v8.3 — what to do with this zip

Extract into the project files area, on top of v8.2 (this is
additive, not a rebase). `photos/` is a subfolder, everything else
is flat.

**Replace these existing files:**
- `fff_facts.py` (new `headline_color=` param on `fff_cover()` /
  `fff_fact()`, new `_parentage_diagram()` helper, "Cheers" position
  raised ~44px — full detail in `CHANGELOG_v8_3.md`)
- `FFFA_STYLE_GUIDE.md` (documents the color-override pattern, the
  photo-color-sampling technique, the third diagram type, and updates
  the open-items list)
- `DESIGN_PROCESS_v8.md` (section 9 updated in place — rest of the
  file unchanged from v8.2)

**Add these new files:**
- `render_fff_cabfranc.py`
- `CHANGELOG_v8_3.md`
- `photos/cabfranc_cover.jpg`
- `photos/cabfranc_fact1_grapes.jpg`
- `photos/cabfranc_fact2_chateau.jpg`
- `photos/cabfranc_fact3_grapes2.jpg`
- `photos/cabfranc_fact4_rivervineyard.jpg`
- `photos/cabfranc_fact5_rose.jpg`

**Unchanged from v8.2, not re-included here:** `tokens.py`,
`fetch_pexels.py`, `NEW_DECK_STARTER_v8_2_ADDENDUM.md`,
`render_fff_champagne.py`, the Champagne deck's photos. If a fresh
project rebuild is ever needed from scratch, pull those from the
v8.2 zip.

Short version of what changed: a second FFFA deck (Cabernet Franc),
plus two real generalizations the module needed once a second deck
actually used it — a per-deck headline color override (sampled from
the cover photo, not guessed) and a third diagram type for relational
claims — and one shared layout fix (the "Cheers" sign-off was sitting
too low on a page without a diagram above it).

Once saved, next session touching `fff_facts.py` or
`DESIGN_PROCESS_v8.md` should still diff against the project copy
first per the usual rule.
