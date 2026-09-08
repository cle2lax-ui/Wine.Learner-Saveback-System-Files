# v7.3 — guess_the_region.py update

Fixes a real gap: the version currently in the project is missing the
changes made to build the Veneto deck. Without this file, that deck's
build script fails (no _italian_flag, no panel_bg support).

## What's new here vs. what's in the project now
- `_italian_flag()` added alongside `_french_flag()` (same flat
  three-band construction, Italy's colors). `_FLAGS` dict added so
  `gtr_reveal()` can pick a flag by name.
- `gtr_reveal()` gained a `flag` slot key ("french" default, for
  backward compat with the Entre-Deux-Mers deck; "italian" also
  available now). No longer hardcoded to always draw France.
- `gtr_cover()` gained a `panel_bg` slot key (default unchanged: pure
  black) so a deck can set its own panel color instead of always black.

## Open question, not resolved in this file
gtr_cover()/gtr_reveal() don't call core.kicker_block() or
core.headline() -- they never have. That means neither function picks
up the dot-mark kicker or the gold headline-underline from the Rand
filter save-back; GTR's own folded-map icon remains its recurring
mark instead. Whether that should change (folded-map icon replaced by
the dot mark, for literal cross-series consistency) is a real design
decision, not something to silently pick a side on here.
