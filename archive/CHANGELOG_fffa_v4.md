# FFFA v4 — changelog

Session: "Five Fascinating Facts About… South Australia" (third FFFA deck,
first sourced entirely from Wikimedia Commons).

## `core.py`

**`footer()` gains `credit_size=34`.** The photo-credit small print was
hardcoded at 34px. It is now a keyword defaulting to 34, so every existing
call site in `modules.py`, `quick_sips.py`, `guess_the_region.py` and
`fff_facts.py` is byte-identical unless it opts in.

## `fff_facts.py`

**1. Series credit size drops to 28px.** New module constant
`FFFA_CREDIT_SIZE = 28`, passed by `_finish()` into `footer()`. An FFFA
credit line routinely carries photographer + archive + licence — far longer
than the single-name Pexels/Unsplash credits the 34px default was set for —
and at 34 it competed with the swipe cue and page number either side of it
instead of sitting quietly under them.

**2. Closing page credit moves to the footer.** Previously the closing
page lifted its credit up onto the photo, under the top-right grid mark,
on the assumption that "Cheers!" needed the whole footer row to itself.
It doesn't: the sign-off is left-aligned at the margin and the credit is
centred in the gutter, so the two never actually collided. Sitting on the
photo also meant the credit needed a luminance check and a chip to stay
readable — furniture the series doesn't otherwise carry, and which had
been masked on the Champagne and Cabernet Franc decks only because both
happened to have a dark photo in that corner.

The closing page now routes its credit through the standard `footer()`
slot like every other page, which is where photo credits belong per the
house rule. The swipe-label suppression on this page is unchanged.

This supersedes the luminance-chip fix drafted earlier in the same
session — the chip solved a problem that only existed because the credit
was in the wrong place.

## Notes for the style guide

- Add to "Photo sourcing notes specific to this series": Wikimedia Commons
  is now a proven third source alongside Pexels and Unsplash, and is
  markedly better for named wine regions — Commons category trees
  (`Category:Vineyards in Barossa Valley`, `Vineyards in Limestone Coast`,
  `Wynns Coonawarra Estate`) return location-verified images that the two
  stock libraries simply do not carry. Attribution is mandatory and the
  licence must be named in the credit line, not just the photographer.
- Commons API is aggressively rate-limited (HTTP 429 with `retry-after`).
  A 3-second inter-request floor plus backoff is required; without it the
  JSON parse fails opaquely on an HTML error body.
- `photo_anchor` is inert when the source aspect ratio already matches the
  1450px band (2160×1450 ≈ 1.49). Several Commons images land at exactly
  1.49–1.50 and need `photo_zoom` (1.35–1.45) to gain any crop latitude.
  Worth a line in DESIGN_PROCESS §3.
