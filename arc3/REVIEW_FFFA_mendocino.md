# Five Fascinating Facts About Mendocino: review record

Six pages (cover plus five facts), `arc3/render_fffa_mendocino.py`, format `formats/fff_facts.py`. All six pages pass QA.
The Field Guide had spent the obvious Mendocino facts, so these five are new and each was checked against WSET first
(D1, D3, D4), then the primary regulatory text (TTB), then outside sources. The full trace, including what conflicted, is
in the script's docstring.

## Anna Wintour (claims)
| Page | Fact | Sources |
|---|---|---|
| 2 | A Champagne house founded Roederer Estate in Anderson Valley (1982); many outside wineries buy the grapes for sparkling | D4 s17.1 and s17.3; the producer's technical sheet |
| 3 | Even Anderson Valley is only about 4% vines; under 1% across the county | D3 (just under 1,000 ha; 7,000 of ~1,000,000 ha) and the AVA's measured area (UC Davis polygon, ~23,300 ha) |
| 4 | The frost risk sits on the valley floor; most vineyards sit on the slopes | D3 (slopes; frost in low-lying areas) and D1 s8.1 (cold air collects in valley bottoms; hillside sites drain it) |
| 5 | Mendocino Ridge sits above the fog; the only non-contiguous AVA | TTB T.D. ATF-392 (1997); CSW (unique, noncontiguous, above the fog line); Decanter and Wikipedia for "only" |
| 6 | In six miles the heat class changes (Philo I, Boonville II, Ukiah II to III) | TTB T.D. ATF-139 (1983); D1 s3.4 for the Winkler scale |

Checked and settled:
- **The "250,000 acres" and "87,466 acres" apparent conflict** (CSW against the TTB figure): the CSW's 250,000 is the Ridge's OUTER
  boundary (the TTB's 262,400 acres); the AVA itself is the 87,466 acres at or above 1,200 ft. The polygon method's 83,500 acres
  agrees with 87,466 within 5%, which also bounds the "about 4 percent" at 4.1 to 4.5%.
- **Wording kept to what the sources say:** page 2 says "many wineries" (D4 says many); page 5 says "1,200 feet or higher" (CSW)
  where an earlier draft said "above"; page 4 states D3's two facts and D1's principle and does NOT say growers chose slopes
  to avoid frost, which neither source claims.
- **"Philo is among California's coolest grape areas":** the 1983 rule records the petition's description ("one of the coolest
  grape growing areas in California") and classifies Philo Region I, the lowest class.

Left out, on purpose (full list in the script): McDowell Valley "first single-vineyard AVA" (TTB dates it 12/4/1981, two sites
say 4 Jan 1982, and "first" rests on retail pages); any Mendocino Ridge island count (the TTB names 24 ridges; the polygons
split it into 73 pieces; neither is "the number of islands"); the Ridge's 20 F against 40-50 F day-night swing (Wikipedia only,
not in the 1997 rule); anything on cannabis; Boontling.

## Coco Chanel (editing)
- Every figure appears once. The Field Guide's figures (12 AVAs, 7,000 ha, 1983, the 4-mile coast distance) are not repeated;
  the two that touch them (7,000 ha, "just under 1,000 ha") are used for a NEW computed comparison.
- Bodies: 18, 19, 20, 20 words, and 8 on the chart page (the format allows a tighter budget for a diagram slide).
- Page 6 first had a two-line headline and a two-line body, which left "Cheers!" 16px from the page edge. A headline of one line
  and a body that adds something the chart cannot (Philo is among California's coolest grape areas), with the distances moved
  into the chart's labels, gave 230px.

## Jony Ive (craft)
- **Contrast audited per size (engine/text_audit.py).** Every piece of copy clears its threshold. Findings and what was done:
  - The series cobalt numerals "01 to 05" and the closing "!" are 1.98:1 on the ink block, under the 3:1 floor for large type.
    This is true of EVERY FFFA deck, not just this one. The format's opt-in `accent_text_color` takes a lighter blue of the same
    hue for this deck: (69, 107, 187)-family, 3.3:1. The cobalt grid mark, rules and chart bars are untouched. DECISION FOR STEVE:
    whether to make this the series default.
  - The cover kicker measured 3.46:1 at its median but 2.90:1 against the brightest water pixels, and the yellow subject 2.31:1
    at its worst. Cover anchors do nothing for a landscape source (it fills the page height), so the cover is a graded COPY of the
    photo (arc3/build_fffa_mendocino_cover.py; original untouched): a smooth ramp darkening the lake from 50% down, floor 0.58.
    Result: 3.66:1 and 4.45:1 at the worst pixels. Ramps of 0.50/0.45/0.40 were swept; the lightest was kept to keep the lake vivid.
  - Left as drawn: the "5" inside the checklist icon's badge (1.98:1) is the series' fixed icon artwork, not copy.
- **Photo bands measured against each other** (mean luminance 0.18 to 0.35); the guide's failure case was 0.04 against 0.19 to 0.30.
  No band needed grading.
- **Closing page margin measured** (the guide: QA does not catch it): 230px, against 217px in the guide. And a format bug fixed,
  below.
- **A format bug, fixed narrowly:** on a closing page that carries a BARS chart, the short cobalt rule above "Cheers!" was drawn at
  `diagram_bottom - 10`, but the bars helper returns the last bar's own bottom, so the rule underlined the last label like a link.
  It now sits 36px below the chart. Only closing pages with a bars chart take the branch; every earlier deck is unchanged.
- The credit on the closing page uses the format's credit chip (it prints top-right over a busy photo).

## Massimo Vignelli (grid)
The format fixes the grid (photo band 1,450px, or 1,200px with a diagram; numeral, headline, body, footer). The deck stays inside
it: one diagram, on the last page, and no page asks the grid for more than it gives. Order runs from the place, to the land, the
cold, the height and the heat, ending on the Winkler classes that open the Climate arc.

## Brevity
Bodies 18 to 20 words (8 on the chart page); headlines 6 to 9 words. Nothing cut beyond the closing page above.

## Social Pass
Gates 4 and 6 fail structurally on this format and are settled by decision (the open question and the hook live in the
caption). The other six are answered in `arc3/CAPTION_FFFA_mendocino.md`.

## Known and left
- **The Mendocino Ridge rename is pending.** TTB proposed "Mendocino Coast Ridge" (5 Jan 2024; comments closed 5 Mar 2024) and
  its regulatory agenda targets a FINAL RULE for October 2026. No final rule was published when this deck was built, so "Mendocino
  Ridge" is the legal name. Check the Federal Register before posting. The locked Field Guide's slide 11 names the AVA the same way.
- Fact 4's photo is a generic fog-and-redwoods Pexels image (no place claimed); no Commons photo of ridgetops above fog was found.
- The cover photo's place is not asserted (the Commons file title does not state one).
