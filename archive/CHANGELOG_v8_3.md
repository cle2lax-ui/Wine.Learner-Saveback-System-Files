# CHANGELOG v8.3 — FFFA second deck (Cabernet Franc) + module updates

Second FFFA deck built and locked this session (Cabernet Franc), plus
three real additions to `fff_facts.py` that came directly out of
building a second deck on the shared module — this is the point where
a few things that looked series-wide in v8.2 turned out to need a
per-deck knob, and one layout offset that was fine on deck 1 read as
too tight once a second person looked at deck 2's closing page.

## fff_facts.py changes

- **`headline_color=` param added to `fff_cover()` and `fff_fact()`.**
  Defaults to `FFFA_YELLOW` (unchanged behavior for the Champagne
  deck). When passed, overrides the color of the cover subject, every
  fact headline, and the "Cheers" word on the closing page — the "!"
  stays cobalt regardless, and kicker/numerals/rules/diagram chips are
  never touched. This is what let the Cabernet Franc deck use a red
  headline color instead of the series-default gold without forking
  the module.
- **`_parentage_diagram()` added.** Third diagram type (after bottle-
  scale and ranked-bar): two parent chips joined by "×", arrow down to
  a child chip. Generic via `slot["parent_a"]` / `slot["parent_b"]` /
  `slot["child"]`, not Cabernet-Franc-specific. Used once (Cabernet
  Franc's "parent of Cabernet Sauvignon" fact), then removed from that
  same slide in a later round per direct feedback ("get rid of the
  flowchart graphic") in favor of a plain photo + copy layout. The
  function stays in the module, proven and working, for whichever
  future deck has a genuine parentage/relational claim — it just isn't
  used in either deck's current locked state.
- **"Cheers" vertical position raised ~44px.** Was `diagram_bottom +
  34`; is now `diagram_bottom - 10`. On the Champagne deck this sat
  fine; on Cabernet Franc's closing page (no diagram, so a shorter
  page above the sign-off) it read as too close to the bottom edge.
  Fixed in the shared module, so both decks' closing pages moved up
  together — re-rendered and re-checked the Champagne deck after this
  change to confirm it still reads correctly there too.

## New files

- **`render_fff_cabfranc.py`** — Cabernet Franc's render script, kept
  as a second worked reference alongside `render_fff_champagne.py`.
  Useful specifically as an example of the `headline_color=` override
  pattern and the photo-color-sampling technique (see
  FFFA_STYLE_GUIDE.md).

## FFFA_STYLE_GUIDE.md

- Documents the `headline_color=` override and the HSV-based
  photo-color-sampling snippet (filter for hue+saturation before
  ranking by brightness — the naively "brightest red pixel" in a
  wine-splash photo is usually a blown-out white highlight, not a
  meaningful red).
- Documents `_parentage_diagram()` alongside the other two diagram
  types, and adds an explicit note that diagrams are per-fact judgment
  calls, not a quota — this deck's first draft used one, a later round
  removed it, and the slide is fine either way.
- Updates the "known open items" list: the bar-diagram generalization
  is less urgent now that three diagram shapes exist covering scalar/
  ranked/relational claims; two-word subjects ("Cabernet Franc")
  confirmed working against the cover auto-shrink loop; flags a future
  decision point on whether proven per-deck color overrides should
  graduate into named `tokens.py` constants.

## DESIGN_PROCESS_v8.md

- Section 9 updated: diagrams are now described as available per-fact
  for comparative/scalar/relational claims (not mandatory per-fact),
  and the headline-color-override pattern is added as a locked rule —
  sample from the photo, verify contrast, don't guess.

## Deck: Cabernet Franc (locked, shipped as PDF + ZIP)

Five facts, sourced from the CSW Study Guide and independently
corroborated: the 1997 UC Davis DNA finding that Cabernet Sauvignon is
a cross of Cabernet Franc and Sauvignon Blanc (not the reverse); the
Loire Valley's local name "Breton"; the grape's climate-driven aroma
shift (cranberry/bell pepper/tea cool-climate vs. raspberry/violet
warm-climate); its minor-blender role in Bordeaux versus star billing
in Chinon and Bourgueil; and its use beyond still red wine in Loire
rosés and traditional-method sparkling wine (Fines Bulles).

Cover headline color: sampled directly from the cover photo's wine-
splash highlights, `(255, 53, 24)` — see FFFA_STYLE_GUIDE.md for the
exact method.
