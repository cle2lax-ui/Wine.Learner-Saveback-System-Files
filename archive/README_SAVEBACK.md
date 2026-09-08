# Save-back v8.1 — what to do with this zip

Extract into the project files area, preserving the folder structure
(`photos/` and `assets/flags/` are subfolders, everything else is flat).

**Replace these existing files:**
- `core.py`
- `modules.py`
- `guess_the_region.py`
- `build.py`
- `DESIGN_PROCESS_v8.md` (has a new section appended at the end — PDF-
  first/ZIP-on-lock delivery rule — plus the rest is unchanged)

**Add these new files:**
- `render_gtr_marlborough.py`
- `render_wine_faults.py`
- `CHANGELOG_v8_1.md`
- `photos/*.jpg` (17 files — Marlborough GTR + Wine Faults source photos)
- `assets/flags/nz.png`

See `CHANGELOG_v8_1.md` for the full list of what changed and why. Full
detail is in the file itself, but the short version: six real bugs
fixed (invisible cover dot, missing `show_underline` wiring, two
different dead-space caps, a double-rendering photo credit, and a
swipe-cue contrast issue), plus a real NZ flag option for
`guess_the_region.py` and the PDF-first/ZIP-on-lock delivery pipeline
from earlier this session.

Once saved, next session touching `core.py` or `modules.py` should
still diff against the project copy first per the usual rule — this zip
*is* that canonical copy as of today, but the standing practice doesn't
change.
