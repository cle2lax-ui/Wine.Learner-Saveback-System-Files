# CHANGELOG — Northern Rhône session (Arc 1)

Working copies were diffed against `/mnt/project/` at session start.
`core.py` and `tokens.py` matched the recorded baseline hashes;
`modules.py` and `map_atlas.py` did **not** — they had moved on from the
hashes noted in the carry-forward, and now contain the Cava-session
save-back (statement/editorial_lead `photo_credit` passthroughs,
`cover_layout="lower_left"`, inset `marker_color`). Those hashes are
stale, not divergent. Everything below is built on top of the current
project files.

---

## core.py

**1. `run_in()` — five keyword arguments added.**
`map_atlas.lead_paragraph()` has been passing `bold_words`, `bold_color`,
`bold_serif`, `bold_size`, `body_font_role` and `max_gap_mult` to
`core.run_in()` against a `core.py` that never grew them. Every atlas
slide carrying a `description` raised `TypeError` on render. Added at
`run_in` rather than stripped at the call site.

Behaviour notes:
- Word matching for `bold_words` strips surrounding punctuation and
  folds case, so `"Syrah."` matches `Syrah`. Without that, every comma
  in the paragraph is a silent miss and the emphasis reads as arbitrary.
- Line breaking now measures each word in the font it will actually be
  drawn in. Wrapping a candidate string in the body face and then
  drawing some of its words in a wider bold face is how a justified
  paragraph overshoots its measure by a word.
- `max_gap_mult` is a justification safety valve: past that multiple of
  a natural space, the line falls back to ragged setting rather than
  opening a river of white space.

**2. `footer()` — credit line now fits the gutter.**
The credit was centred on the full canvas at a fixed size. A two-photo
slide credits two photographers plus two licences on one line, which
overprinted `SWIPE` on the left and the page number on the right
simultaneously (slide 9 of this deck). The credit now measures the
actual clear gutter between the swipe cue and the page number, steps
its size down to a floor of 22, and ellipsises only if even that will
not fit. Credits are a licence obligation, so the failure mode has to
be "smaller", never "clipped by the page number".

## modules.py

**3. `side_rail()` — credit lifted off the footer row.**
The credit block's last line sat on `FOOTER_Y` at the text column's x —
which, whenever the photo is on the right, is the left margin, exactly
where the swipe cue is drawn. A one-line credit overprinted `SWIPE` on
every right-side slide. The block now sits one line height above the
footer row, clear at either side setting.

**4. `side_rail()` — `footer_adaptive=True`.**
The existing comment argued against forcing `footer_fill` because the
page number "sits on the paper side regardless of which side the photo
is on". That only holds when the photo is on the left. With
`side="right"` the page number lands at `x=W-M`, on the photo, over the
darkening chip, and default `MUTED` left it barely legible. Per-element
luminance sampling gets both sides right without forcing either.

**5. `statement()` closing variant — subtitle wraps, and is QA'd.**
The closing subtitle was a single unwrapped `d.text` at a fixed size,
with no `qa.box` registered. Any subtitle longer than the measure ran
off the right edge mid-word **and the QA harness passed it silently**.
It now wraps to the measure, honours `subtitle_size` the way the cover
variant already does, and registers its box so the harness catches an
overrun instead of shipping it.

Worth checking other closing slides already shipped — this failure was
invisible to QA, so it will not have been flagged anywhere.

## map_atlas.py

**6. `draw_map_panel()` — `river_width` panel key.**
River stroke scaled off the map's drawn width, which is right for a
broad panel and wrong for a tall narrow one. The Northern Rhône is a
74 × 27 km strip, so it fits its box on height and renders ~550 px
wide, taking the expression to its 3 px floor — a hairline on a 2160 px
canvas, on the one feature the Wine Folly treatment allows as basemap.

**7. `draw_map_panel()` — `label_column_x` panel key.**
Rule 3 of the label algorithm (adaptive per-label left margin) assumes
the map is wide enough that a label just outside its target clears the
shape. On a long narrow ribbon the anchor sits inside a shape a few
dozen px wide, so "just outside the target" lands the label on top of
the appellation it names, at every latitude. `label_column_x` sets a
flush column either side with real leader lines back to each shape; the
column reads as a latitude index.

This is the feature `render_fg_cote_de_nuits.py` already calls. See the
gap note below.

**8. `regional_atlas()` — `inset_x_frac` / `inset_y_frac`.**
The inset was positioned relative to the drawn map, which suits a map
that fills its box. A tall narrow map leaves wide empty gutters, and
0.44 of a 550 px map put the inset directly on the southern crus while
the real free space sat unused. These position it against the panel box
instead.

---

## Gap: CDN-era changes that never landed

`render_fg_cote_de_nuits.py` cannot run against the current project
files. It calls, and `/mnt/project/` does not have:

- `regional_atlas(locator=..., locator_w=...)` — a locator panel
  distinct from `inset`
- `regional_atlas(legend=..., legend_size=...)`
- `statement(subtitle_size=[...], subtitle_font=[...])` — list-valued,
  for a two-scale cover subtitle
- `statement(mark_side=...)`

`label_column_x` was in the same group and is restored here (#7). The
other four are not — I worked around them rather than reconstruct them
from a call site and risk a different implementation under the same
name. The Côte de Nuits deck is unbuildable from the project until that
ZIP is found.

---

## Not a code change: doc conflict

`SERIES_SYSTEM_v9.md` §7 specifies roughly 5 broad / 8 niche / 2 owned
hashtags. `SOCIAL_PASS_STYLE_GUIDE.md` gate 7 states hashtags were
capped at five per post in December 2025 and confirmed not to improve
reach. Fifteen tags is not possible under a cap of five. Unresolved —
it affects every caption in every arc, so it wants a decision rather
than a per-deck guess.
