# Review: The Field Guide, South Africa, "Two Currents, One Wind", draft 1

Four-designer pass in the guide's order, then the Social Pass and the guards. All 15 slides were rendered and viewed after each round.

## Anna Wintour (claims; every claim re-read against D3 or D4 before it was written)
- The source ledger is in the renderer's docstring, slide by slide, with page numbers.
- Caught on review: slide 10 first said "5 themes"; D3's Swartland list has six. Fixed.
- The history (6) quotes D3's wording for the dop system ("a reward until 1994, and in some places beyond") and keeps the KWV's role plain: it set volumes and prices and backed segregation.
- D3 contradicts itself on Swartland's rainfall (400 mm on p. 506, "around 500 mm" on p. 516): the slides say 400 to 500.
- Slide 4's bars: a range is drawn at its midpoint and the chart's own title says so. Constantia's 1,000 mm is "about", Stellenbosch's "over 700".
- Slide 11 calls Elgin "the coolest area" because D3 says "the coolest wine-growing area of South Africa"; Constantia's "no Pinot Noir: too windy" is D3's "fares less well in the windy conditions".
- Pinotage is not named anywhere (Steve's steer).

## Coco Chanel (edit)
- The history slide was 80 words (limit 70). The KWV's end was folded into the 1994 entry and the 1997 row dropped: 68 words, nothing lost.
- Slide 7's photos are decorative, and the labels name the categories ("High volume", "Small volume"), not the photos.
- Slide 11's standfirst said "three" over four tiles: fixed to four.

## Jony Ive (craft)
- The map (2) is cut from the 10 m Natural Earth coastline, clipped exactly to its frame. The first version showed the crop's cut edges as heavy ink lines, white land spilling past the frame, and a stray diagonal (the layout's corner smoothing cutting long straight edges). Fixed in the layout with two default-preserving options, `sea` and `open_edges`, and by densifying the frame edges.
- Slide 4: the biggest bar's large label ("about 1,000") was clipped by the page edge; the scale was reduced to 70%.
- Slide 5: "Table Mountain sandstone" overflowed its tile: now "Sandstone", with "Table Mountain" beneath.
- Slide 12: the footnote collided with the footer: the diagram was reduced and the footnote removed (the Breede circle now labels itself).
- Slide 15: a crop of the glass was hidden by the layout's text panel (it covers the lower half) and pixelated; the cover's sunset vineyard is used as a bookend.
- Slide 14's first photo showed a painting above a bottle stack: replaced with a Franschhoek vineyard.

## Massimo Vignelli (grid)
- 11 distinct layouts across 15 slides (the `variety` report), graphic-led slides 2, 4, 6, 10, 12 and 13. The forest-green signature carries the covers, the tiles and the rules.
- Open items: slides 1, 14 and 15 share the warm sunset palette (the bookend is deliberate, 14 is a coincidence of the photo available); no photographs for Swartland, Constantia, Robertson or Elgin.

## Guards
Layout QA passes on all 15 slides; `text_audit` 0 of 136 text groups below threshold; spelling 0 British forms; every slide at or under 68 words. **Engine change:** the atlas layout gained `sea` and `open_edges` (documented in its docstring), both default-off; the regression guard re-rendered every locked deck and **42 of 42 match the reference**.
