# Save-back v8.2 — what to do with this zip

Extract into the project files area, preserving the folder structure
(`photos/` is a subfolder, everything else is flat).

**Replace these existing files:**
- `tokens.py` (new FFFA constants + two new font roles — everything
  else in the file is unchanged)
- `DESIGN_PROCESS_v8.md` (new section 9 appended before the delivery
  section, which stays last — rest of the file is unchanged)

**Add these new files:**
- `fff_facts.py`
- `fetch_pexels.py`
- `render_fff_champagne.py`
- `FFFA_STYLE_GUIDE.md`
- `NEW_DECK_STARTER_v8_2_ADDENDUM.md`
- `CHANGELOG_v8_2.md`
- `photos/fff_cover.jpg`
- `photos/fff_fact1_risingbubbles.jpg`
- `photos/fff_fact2_bottle.jpg`
- `photos/fff_fact4_vineyard.jpg`
- `photos/fff_fact4_cellar.jpg`
- `photos/fff_fact5_toast.jpg`

**Not included, regenerate per session per the existing font pipeline
convention:**
- `Archivo-Black.ttf`, `ArchivoCond-Black.ttf` — static instances of
  the Archivo variable font, referenced by `tokens.py`'s new
  `sans_black` / `sans_cond_black` roles. Generation snippet is in
  `FFFA_STYLE_GUIDE.md`. Not stored in the project photo/font store,
  same as every other font this system uses.

See `CHANGELOG_v8_2.md` for the full list of what changed and why.
Short version: a new third carousel series (FFFA — "Five Fascinating
Facts About...", fixed 6-page format), first deck built and locked
(Champagne), plus two real layout bugs fixed along the way (checklist-
icon alignment measured off the wrong font metric, and a diagram/
closing-sign-off vertical collision on the last page).

Once saved, next session touching `tokens.py` or `DESIGN_PROCESS_v8.md`
should still diff against the project copy first per the usual rule —
this zip *is* that canonical copy as of today, but the standing
practice doesn't change.
