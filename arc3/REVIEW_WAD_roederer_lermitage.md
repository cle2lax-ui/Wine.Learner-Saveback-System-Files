# What Am I Drinking? -- Roederer Estate L'Ermitage Brut 2019: review record

Two-page POST (not a Reel, per Steve), `arc3/render_wad_roederer_lermitage.py`, format `formats/what_am_i_drinking.py`.
Page 1 is a guess page that names nothing (the build fails if it does); page 2 is the answer. QA passes: 74 and 60 words
against the 130-word budget.

## Decision flagged: the wine is the L'Ermitage 2019, not the Brut NV
The Arc 3 plan said Roederer Estate Brut NV. Steve's bottle photo is the L'Ermitage 2019 (its label reads "2019 Brut
L'Ermitage"), and he asked for that photo, so the deck is about that wine. A Brut NV deck would need its own photo.

## Anna Wintour (claims)
Every claim traces to the producer's technical sheet (read in full), a named critic, D3 or D1; the trace is in the script's
docstring. Checked and kept: 100 points from Wine Enthusiast, "the first it has given an American sparkling wine" (K&L's
wording; Roederer's 5 June 2025 press release says "first-ever perfect score for an American-made sparkling wine from a
major wine publication"). Steve's direction (round 2): "use the lees aging time and alcohol from the producer's tech sheet."
- **Alcohol:** 12.9%, from the sheet, now printed on page 2 (the importer and Wine.com list 13.2%; the sheet is the source).
- **Aging:** the sheet states NO lees time (read in full at both addresses on the producer's site, and the rose's sheet).
  It gives "disgorged February 2024" and "an additional seven months on the cork"; both are now on page 2. No lees figure
  is printed, because the producer gives none: reviewers say five years (Wine Enthusiast, K&L), a retailer says four, and a
  2019 harvest disgorged in February 2024 points to about four. FLAGGED to Steve: if he wants a lees figure, it needs a named
  source and the sources conflict.
- Page 2 had to be cut to fit (the layout check failed at ~78 words): the reviewer-sourced "lowest dosage the wine has ever
  had" (Vinous) went, not the producer-sheet facts.
- Left out: any Jeb Dunnuck score (retailers show both 95 and 96).
- **D4 (the WSET sparkling-wine unit) is NOT in the project files** and could not be checked for Anderson Valley facts; the
  only Anderson Valley sparkling content available is D3's line (Pinot Noir and Chardonnay are used in both sparkling and
  still wines). OPEN until Steve adds D4.
Three dashboard rows are INFERRED and labeled so in the script: Acidity (Medium (+): the producer calls 2019 a lower-acidity
vintage, "less classic, taut", while reviewers say "bright", "vibrant"), Body, and Aroma Intensity.

## Coco Chanel (editing)
- "estate-grown" appeared on both pages: cut from page 2 (page 1 says "one estate's own grapes").
- The page-1 note source ("Wine Spectator, Wine Enthusiast, the producer") ran off the page; now "Critics and the producer",
  which the guide allows for page 1 and which is accurate: the notes draw on several critics and the producer's sheet.
- "lingering" came from a critic not credited: replaced with the producer's own "pear skin".
- Page 2's "its first for an American sparkling wine" was ambiguous (whose first?): now "the first it has given".

## Jony Ive (craft)
- **The gold:** the Quick Sips series gold measured 3.37:1 on paper and was drawn as small text (dashboard descriptors,
  producer names, the source line, the region line). Fixed in the format code through `core.legible` (Steve's standing
  rule). Every text group in this deck now clears its threshold (4.5:1 small, 3:1 for text 100px and larger).
- **The audit tool had a blind spot:** it merged text of one color and background into a single group and judged it by its
  LARGEST member, so small gold text hid behind a 110px line. Groups are now per size. Re-run on every deck, it found six
  failing gold groups, all in the Quick Sips gold: both Quick Sips decks, the locked Loosen deck and this one. All fixed.
- **Scrim, swept not guessed:** 0.46 was the Loosen photo's value. On this blue sky, 0.30 is enough: title 6.6:1, gold note
  4.62:1 against the BRIGHTEST background pixels (need 4.5), and the hero keeps 86% of its brightness (81% at 0.46).
- **Page-2 hierarchy:** the producer's name is the headline and shrank to 174px to fit one line, under the format's 190px
  rule against the lockup (160px). The lockup is now 130px rather than shrinking the producer; page 1's is 120px.
- "6 g/L" stays on one line (the wrapper splits on every space); checked on the render.
- The bottle panel's background deviates 0 levels from the paper above and below the bottle: no seam.
- The hero was checked by eye for readable signs: none.

## Massimo Vignelli (grid)
Measured on rendered pixels: text top y=100 / bottle top y=101; last body line y=2,380 / bottle base y=2,382; footer
clearance 177px. Identical to the Loosen deck's grid.

## Brevity
Page 1: 74 words. Page 2: 62. Budget 130. Page 2 was cut once to fit the layout check (see the Wintour section).

## Social Pass
All eight gates are answered in `arc3/CAPTION_WAD_roederer_lermitage.md`. The decode layer is the dosage (6 g/L, page 2)
against the label's "BRUT": the EU's extra brut range is 0 to 6 g/L of sugar (Regulation (EU) 2019/33 Annex III). The dosage
is not the same as the finished wine's sugar, so the pinned comment asks where the wine sits and does not call it extra brut.

## Known and left
- The bottle shot is 400 x 1,376 px, enlarged about 1.8x (the guide asks for 1,500 px; the Loosen shot was 3.5x).
- The hero is the same vineyard photo as slide 13 of the Mendocino Field Guide.
- The caption's "our last Field Guide" line assumes the Mendocino Field Guide has posted first.
- The Northern Rhone Field Guide could not be audited in this environment (its map data is unreachable); its modules are
  covered by the specimen suite and the other decks.
