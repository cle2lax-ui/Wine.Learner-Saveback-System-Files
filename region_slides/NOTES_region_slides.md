# Region comparison slides: notes (draft)
Two landscape slides (16:9, 13.33 x 7.5 in PDF, rendered at 3200 x 1800 px): `render_region_slides.py` -> `Region_Comparison_Slides.pdf`.
Slide 1: Napa Valley, Left Bank Bordeaux, Right Bank Bordeaux. Slide 2: Burgundy, Willamette Valley, Tasmania.
Each column: photo with the region name and grapes, then HOW IT'S UNIQUE (soil, climate, viticulture, tradition) and IN THE GLASS (three traits). Rows are measured and aligned across the three columns.

## Sources
All facts from WSET Diploma D3 (Wines of the World); the page ledger is in the renderer's docstring. Chapters: Napa 23, Bordeaux 2, Burgundy 3, Oregon 24, Australia 31 (Tasmania, pp. 557-558).

## Decisions and caveats
- Brief edition: every row is a short fragment on one line (body words cut by about two thirds), body type 46 px (was 38), photos 600 px tall. The renderer's docstring still holds the fuller D3 ledger, so anything cut can be restored from it.
- Compressions were re-checked against D3: Napa's north is "warmer" (D3: warm to hot); the Right Bank says "small estates, some just 1 ha" (Saint-Emilion alone has a classification, so that claim was dropped); the Right Bank's price line is labeled "Top wines" because D3 gives Saint-Emilion a great range of quality.
- Tasmania, soil: D3 names informal sub-regions with distinctive soils but no soil types, so the row says "Varies by sub-region". Phylloxera-free is from D3 p. 529.
- D3 and D4 disagree on Tasmania's share of Australian wine (D3: under 1% by volume; D4: 7%); no share is stated.

## Guards
Layout: all 14 rows single-line; content ends 1,678 px of a 1,716 px footer line. text_audit: 0 below threshold; worst pixel behind the names on photos 10.5:1. Spelling: 0 British forms. The measuring pass uses a no-op stand-in so the audit sees only the real slide.

## Photos (Wikimedia Commons, credited on each slide)
Napa: John Morgan (CC BY 2.0). Left Bank: Megan Mallen (CC BY 2.0). Right Bank: Megan Mallen (CC BY 2.0). Burgundy: Michal Osmenda (CC BY 2.0). Willamette Valley: Sheila Sund (CC BY 2.0). Tasmania: Stefano Lubiana Wines (CC BY 2.0).
