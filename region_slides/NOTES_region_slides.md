# Region comparison slides: notes (draft)
Two landscape slides (16:9, 13.33 x 7.5 in PDF, rendered at 3200 x 1800 px): `render_region_slides.py` -> `Region_Comparison_Slides.pdf`.
Slide 1: Napa Valley, Left Bank Bordeaux, Right Bank Bordeaux. Slide 2: Burgundy, Willamette Valley, Tasmania.
Each column: photo with the region name and grapes, then HOW IT'S UNIQUE (soil, climate, viticulture, tradition) and IN THE GLASS (three traits). Rows are measured and aligned across the three columns.

## Sources
All facts from WSET Diploma D3 (Wines of the World); the page ledger is in the renderer's docstring. Chapters: Napa 23, Bordeaux 2, Burgundy 3, Oregon 24, Australia 31 (Tasmania, pp. 557-558).

## Decisions and caveats
- Tasmania, soil: D3 names informal sub-regions with "distinctive climates, topography and soil" but gives no soil types, so the slide says there is no single signature. Phylloxera-free is from D3 p. 529.
- D3 and D4 disagree on Tasmania's share of Australian wine (D3: under 1% by volume; D4: 7%). D3 is used, and no share is stated.
- Where D3 gives Oregon-wide figures (47% of vineyards certified sustainable), the slide says "Oregon's vineyards".
- "Quality and price" for the Right Bank is stated for Pomerol only, because that is the appellation D3 gives it for (Saint-Emilion has a "great range of quality").
- Napa and Willamette Valley are compared at the level D3 gives (Napa's wines vary by AVA; the slide uses the valley-floor Cabernet profile and notes mountain wines are firmer).

## Guards
Layout: content ends 1,684 px of a 1,716 px footer line. text_audit: 0 below threshold; worst pixel behind the names on photos 6.9:1. Spelling: 0 British forms. The measuring pass uses a no-op stand-in so the audit sees only the real slide.

## Photos (Wikimedia Commons, credited on each slide)
Napa: John Morgan (CC BY 2.0). Left Bank: Megan Mallen (CC BY 2.0). Right Bank: Megan Mallen (CC BY 2.0). Burgundy: Michal Osmenda (CC BY 2.0). Willamette Valley: Sheila Sund (CC BY 2.0). Tasmania: Stefano Lubiana Wines (CC BY 2.0).
