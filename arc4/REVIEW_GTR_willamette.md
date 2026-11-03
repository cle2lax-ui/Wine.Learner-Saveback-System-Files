# Review: GTR "Same Latitude, Different Ocean" (Willamette Valley), draft 1

Run before presenting: the four-designer pass (in the guide's order), then the guards. Both pages were rendered and viewed.

## Anna Wintour (claims, each against the D1 / D3 text)
- Every clue and every reveal claim traces to D1 p. 30 or D3 Ch. 24 (ledger in the renderer's docstring). "80 km (50 miles) from the Pacific" and "one of the coolest areas in Oregon" are D3.
- The Field Guide's hedge is kept: the Gulf Stream is not asserted (D1: "at least partially"). The California Current is not named (D1 names it; the clue does not).
- The 1.8°C gap is derived, so it is not on the slides; D1's own 15.9 and 17.7 are.

## Coco Chanel (edit)
- First blurb overflowed its safe zone by 15 px at the 60 px floor. Cut copy, not type: "level with Margaux" and "45° N" went (clue D already says it), "only" went, and the two sentences about the cold current were merged.
- The awkward "yet cooled by a cold current it averages ..." became "A cold current cools it to 15.9°C, while Margaux, at the same latitude, averages 17.7°C."

## Jony Ive (craft)
- Legibility audit: 0 of 12 text groups below threshold. Cover blade (changed twice at Steve's request: the first photo had been used in other posts, and the second, a Pacific coast, became an actual Willamette Valley shot): vineyard rows and forested hills, "Willamette Valley view from King Estate Winery", RickObst, CC BY 4.0. Reveal crop keeps the red house and the vine rows. US flag drawn at 4x and reduced; it sits level with the name's x-height.

## Massimo Vignelli (grid)
- Page 1: clue block ends at 68% of the page and the cue at 77%, the same rhythm as Baden. Page 2: photo 66%, name and flag centered as one group, blurb justified inside the 200 px bottom margin.

## Social Pass (fifth; the eight gates)
Decode layer: clue D's "Margaux" (a Field Guide figure) rewards the careful reader. Save asset: the two numbers on page 2. Send line: the caption's hook. Open question: "How many clues did you need?" Callback: slide 6 of The Field Guide. Cover hook: the 81-character first line (inside the fold). Search surface: the caption names Pinot Noir, Margaux and Bordeaux, never the answer. Second beat: swipe to the reveal.

## Guards
regress 42/42; Reel frames 26/26; spelling 0 British forms; text_audit 0 below threshold; QA word budgets (60 / 90) pass.

## LOCKED
Approved by Steve and locked on 3 Nov 2026 as git tag `gtr-willamette-final`. The renderer (`arc4/render_gtr_willamette.py`) re-renders both pages pixel for pixel from the pushed files (hashes of the decoded pixels: page 1 `b49dc6a65dee8e03`, page 2 `0962ddfab4c7e0a8`). The cover is the Willamette Valley photo with its bottom burned for footer contrast (`photos/gtr_willamette_blade.jpg`); the reveal carries the new US flag (`formats/guess_the_region.py`, option `"us"`). The format's regression subject (the Cornas GTR) is unchanged; a change to `formats/guess_the_region.py` that alters this deck should be checked against it before it ships.
