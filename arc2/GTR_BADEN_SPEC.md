# Guess The Region — Baden
**Arc 2** · 2 pages · every clue verified against D3 Ch. 11 (Aug 2026 edition)

Brief (Steve): subject Baden; focus on red wines as well as white.

## Answer
**Baden.** Not named anywhere on page 1 or in the caption.

## Page 1 — clues
- **A.** Germany's warmest, sunniest region.
- **B.** Across the Rhine from Alsace.
- **C.** Known for red, yet 61% of its vines are white.
- **D.** An extinct volcano shapes its fullest wines.

Photo: red grapes on the vine, Waltershofen (Freiburg im Breisgau) — Sven Finger / Unsplash. Vertical crop centred on the cluster. Carries the "red" half of the brief on the cover; clue C and the blurb carry the white.

## Page 2 — reveal
**Baden**, German flag (new: horizontal black/red/gold at 5:3). Blurb: warmest, sunniest region on the Rhine's eastern bank; Spätburgunder its most planted grape and among Germany's finest reds, yet 61 per cent of vines white; 64 per cent trocken in 2021. Caption: *Terraced vineyards on the Kaiserstuhl, an extinct volcano.*

Photo: terraced vineyards, photographer-tagged `kaiserstuhl` — Hanna Schwichtenberg / Unsplash. Cropped tight on the terraces (the frame was half sky).

## Source trace
| Claim | D3 Ch. 11 |
|---|---|
| warmest, sunniest | "Germany's warmest, sunniest and one of the driest wine-producing regions" |
| across the Rhine from Alsace | main vineyard area is "on the eastern side of the Rhine opposite Alsace" |
| Spätburgunder most planted; 61% white | "Spätburgunder is the most planted variety"; "61 per cent of Baden's plantings are white" |
| extinct volcano / fullest wines | steep, south-facing slopes around Kaiserstuhl, "an extinct volcano, produce the fullest-bodied wines" |
| 64% trocken | 2021: just under 50 per cent nationally, 64 per cent in Baden |

## Cut at the claims/length pass
- **Grauburgunder + Weissburgunder clue** — true and on-brief, but the panel holds ~24 characters a line, and the volcano is the more placeable fact. The whites are carried by clue C and the blurb.
- **Co-operatives ~75% of production** — true, doesn't help place the region.
- **Zone B enrichment** — true, and would hand the answer to a specialist before the clues do.

## Format changes this deck required (formats/guess_the_region.py, engine)
1. **`flag="german"`** — horizontal tricolour at its true 5:3 ratio (the others are 3:2; a German flag at 3:2 would be visibly squashed). Existing decks unchanged.
2. **Cover credit colour** — the footer chose one colour from the photo under the *label* and applied it to the credit too, which sits on the black panel. A bright blade bottom made the credit near-invisible (a licence-credit problem). The credit now samples the panel. Verified pixel-identical on the Cornas deck.
