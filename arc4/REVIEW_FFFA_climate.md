# Review: FFFA "Five Fascinating Facts About Climate Change", draft 1

Four-designer pass in the guide's order, then the Social Pass and the guards. All six pages were rendered and viewed after each round.

## Anna Wintour (claims, each against D1 section 3.6, pp. 44-45)
- Each fact traces to the book's own words (ledger in the renderer's docstring). The hedges are the book's: "may", "it is likely", "it is thought", "potential".
- Fact 4 is the riskiest. D1 says sites "in many of these regions" will be abandoned and gives parts of California and South Africa as examples; the copy says "regions with severe heat and drought, such as parts of California and South Africa, are thought likely to go". It does not say those regions will lose sites.
- Fact 2: D1 says grapes "may be picked with higher levels of sugar", so the copy says "may be picked riper".
- Fact 3: the pepper claim is hedged twice, in the headline ("May Fade") and the body ("may stop that aroma developing").

## Coco Chanel (edit)
- The plan's separate pH fact (D1 p. 44) is held: it is the second half of the same paragraph as fact 2 and would not fit a 15-20 word body without cutting the aroma and tannin point.
- Fact 3 (pepper) takes its place: the Syrah What Am I Drinking? post that was holding it became the Tondonia Rioja, so the pepper is free. Recorded as a change from the approved plan.
- Fact 5's headline and body were repeating the risk; the headline now carries the upside ("Once-Too-Cold Regions May Gain") and the body carries only the risk.

## Jony Ive (craft)
- Cover: the page number measured 3.26:1 and the credit 3.83:1 (needs 4.5:1) against the bright orange vine rows. A graded COPY (`build_fffa_climate_cover.py`; the original is untouched) darkens only the lower part with a smoothstep ramp. The floor was SWEPT: 0.66 gives 6.42 (worst pixel 5.0) and 7.21 (4.96); 0.58 gave 7.65 and 8.48. 0.66 is the lightest that clears 4.5 at the worst pixels, so the sky and mountain keep their color.
- Closing page: the first build's two-line headline and two-line body left "Cheers!" 56 px from the page edge (the guide: 217 good, 57 crowded; the QA does not catch it). One line of each gives 316 px.
- The audit's two remaining groups (the "5" in the checklist icon's badge, 1.98:1) are icon artwork, left as drawn per the guide.

## Massimo Vignelli (grid)
- Every fact page uses the same 1,450 px photo band and the series ink block; bodies are 14-21 words. The cover is photo-only, as the format requires.
- Open item: fact 4's photo (young vines in dry sandy soil, Stellenbosch) is the weakest match for "heat and drought"; no photo of a stressed or abandoned vineyard was found on Commons.

## Social Pass (fifth; the eight gates, with the format's two structural exemptions)
Gates 4 (a question on the last slide) and 6 (a cover hook) fail structurally on this format and are settled in the caption, by decision, as the Mendocino deck did. Gate 2 (save asset) has no chart slide by decision: D1 gives no numbers to chart. Gates 1, 3, 5, 7 and 8 are in the caption notes.

## Guards
Layout QA passes all six pages; text_audit 0 of 18 groups below threshold except the icon artwork; spelling 0 British forms. No engine files changed in this work, so the pixel regression is unaffected.

## LOCKED
Locked at Steve's word on 3 Nov 2026 as git tag `fffa-climate-final`. The renderer (`arc4/render_fffa_climate.py`) re-renders all six pages pixel for pixel from the pushed files (hashes of the decoded pixels: cover `5a2c89c0db883751`, fact 1 `e150805e959a01d4`, fact 2 `707af6b270ad7e3d`, fact 3 `5b56efc26c5054f1`, fact 4 `ee0a30d806ad2e88`, fact 5 `7a24906f54e58fd2`). The cover is the graded copy (`photos/fffa_climate_cover.jpg`, floor 0.66). The format's regression subject is unchanged; a change to `formats/fff_facts.py` that alters this deck should be checked against it before it ships.
Open item carried: fact 4's photo (young vines in dry sandy soil) is a weaker match than the others; replace under a new tag if a better one turns up.
