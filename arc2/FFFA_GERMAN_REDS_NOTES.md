# FFFA: Five Fascinating Facts About Red Wines of Germany (Arc 2)
6 pages · cobalt/ink series look with a red headline colour sampled from the cover · not locked

## The deck
| # | Headline | Visual |
|---|---|---|
| 1 | Cover: **Red Wines of Germany** | two glasses of red wine, cropped tight (Steve's photo), graded build |
| 2 | Nearly a Third of German Vines Are Red | Rheinhessen vineyard at sunrise + **bar chart** (1980 vs 2021) |
| 3 | Germany's Pinot Noir Almost Trebled | red grapes, Baden |
| 4 | Dornfelder Went From Nothing to No. 2 Red | dark grapes, Rheinland-Pfalz |
| 5 | Four in Five Ahr Vines Are Red | autumn slate terraces at Mayschoss + **bar chart** (Germany / Württemberg / Ahr) |
| 6 | Württemberg Is Two-Thirds Red, then **Cheers!** | terraced vineyards, Stuttgart |

## Sources, and where they disagree
D3 Ch. 11 (Aug 2026 edition) is the primary source. Every figure was checked against the
current official statistics (Wines of Germany; the German Wine Society's 2022 tables). **They
disagree in three places, and the copy is worded to be true under both rather than to pick one:**

| Claim | D3 | Current official | What the deck says |
|---|---|---|---|
| Ahr red share | 81% | 79% (2025), still the highest of any region | "Four in Five"; chart bar "about 80%" |
| Ahr size | 560 ha | 535 ha | not stated |
| Württemberg's top reds | Trollinger, Lemberger, Schwarzriesling | 2022: Trollinger 16.7%, Lemberger 15.5%, **Spätburgunder 11.5% > Schwarzriesling 10.5%** | "Trollinger and Lemberger lead, not Pinot Noir" (true in both) |

Not disputed: 90% white (1980) → 32% black (2021); Spätburgunder 11.5% of plantings and
"almost trebled"; Dornfelder "from nothing" to second most planted black in 30 years and
the leading black in Rheinhessen and Pfalz; Württemberg 66% black.
**One derived figure:** the chart's 1980 bar, "about 10%". D3 says only "90 per cent white", so black is the remainder.

**Left out on purpose:** "Germany is the world's third-largest Pinot Noir grower after France
and the USA" is real but single-sourced to one DWI-affiliated site: a strong candidate if you
want a second source found. Also out: Dornfelder bred in 1955 (not D3), Frühburgunder, Regent, any prices.

## Four-designer review (run during the build; the fixes are in)
**Wintour (claims).** Every claim traced (above). Two wording fixes: "Number Two" could read as
second overall, so it is "No. 2 Red"; and "Not Pinot" would have been wrong, since
Schwarzriesling *is* a Pinot (Meunier), so page 6 now says "not Pinot **Noir**" in the body.
**Chanel (editing).** Page 5's body ended on an orphaned "it possible."; recut to two lines.
Page 6's two-line headline became one.
**Ive (craft, measured).** (1) "Cheers!" ended **57 px** from the page edge (margin 120)
because of the two-line headline; with it on one line, **217 px**. (2) Page 6's photo band
averaged **0.040** luminance against 0.19-0.30 on the other pages; a gamma lift of 0.6
(to 0.095) makes the terraces legible and keeps the dusk. The original is untouched; the
graded copy is built by `build_fffa_reds_cover.py`. (3) The cover glass's base came within ~50 px of the
kicker icon, so it was raised 40 px. (4) Headline red sampled by the guide's method, not by eye:
(246, 31, 13), **3.86:1** against INK (floor 3.0); the three single brightest "reds" were
blown-out pinks, as the guide warns.
**Vignelli (grid, measured).** Every text block starts at the 120 px margin (within 2 px)
on all five fact pages; pages 2-5 clear the footer by 259-319 px; both charts' left edges sit on the
margin; the highlighted bar is paper-white so the eye goes to it without touching the headline colour.

## Format work this deck needed
`fff_facts.py` gained a general **`diagram="bars"`** (the style guide's open item: "collapse the
scalar diagrams into a shared helper"). It takes `slot["bars"] = [(label, value, shown, highlight)]`.
Labels and values are >= 35 px. It is the first FFFA diagram that isn't hard-coded to one deck.
The cover is a graded build because the photo's glass ran into the type zone.

## Cover change (round 2)
Steve supplied a photograph of two glasses of red wine and asked for it as the cover, cropped
closely on the glasses. It replaced the red-wine splash.
- **The source is 612 x 408 px.** A close crop around both glasses is 334 px wide, so filling the 2160 px cover is a
  **6.5x enlargement**, which no treatment can make sharp. I tested three on the real output: plain Lanczos showed blocky
  JPEG stair-steps along the rims; denoising first, then two 2x steps and a light unsharp, was clean; adding fine
  film grain made the remaining softness read as photographic texture. The grain version is in. It is still soft up close; at
  the size it is seen on a phone it reads as a warm, candlelit close-up.
- The stems and table **fade into near-black** under the wine so the type has a dark ground: measured behind the type
  zone, mean luminance 0.0006, so the white kicker has 19:1 even against the brightest pixel there.
- **No credit is printed**: the file has no photographer, agency or licence data, and none was supplied. **612 x 408 is
  typical of a stock site's preview image. If it is a comp, it needs a licence before this posts**; the full-size
  version would also fix the softness.
- (The scarlet headline colour sampled from the old splash cover was **superseded by the flag colours**: see the next section.)

## Text colours: the German flag (round 3)
Steve asked for the font colour scheme to match the German flag (black, red 221/0/0, gold 255/206/0).
- **Gold** is the cover subject, every fact headline and "Cheers": **10.60:1** on the ink block (the scarlet it
  replaced was 3.86:1). **Red** is the cover kicker, the 01-05 numerals and the closing "!": **3.07:1** on ink
  (floor 3.0), and the cobalt numerals it replaced were **1.98:1**, so they are more legible too.
- **Black stays the ground**, not a font colour: black on the ink block is 1.33:1, invisible. The cover is already pure
  black, so the cover reads black / red / gold from the ground up.
- The cover's red kicker is 3.46:1 against the photo behind it at the 98th percentile; the very faintest stem
  remnants (about 2% of that zone) dip to 2.1:1. It reads clearly.
- **Not changed, and your call:** the cobalt grid mark (top right of every photo), the short cobalt rules, and the chart
  bars. They are not fonts, and cobalt is what makes FFFA read as FFFA. Say if you want them in flag colours too.
- Format: `fff_cover(kicker_color=)` and `fff_fact(accent_text_color=)` are new optional overrides (numerals and the "!");
  with them unset, every existing deck renders exactly as before (verified pixel-identical).

## Open
- **Caption**: not written. **Social Pass**: not run. **Not locked.**
- **Cover photo licence and a larger file**: see "Cover change" above.
- "about 80%" on the chart: say if you'd rather show D3's 81% (or the official 79%).
- The Ahr photo has people under a red tent in the lower right; it reads as a harvest or tasting stand, not a distraction, but it is a choice.

**Photography** (location-verified): cover, Steve's supplied photo (no credit data; the earlier splash cover was Saman Taheri); fact 1 Jugenheim (Rheinhessen), Sven
Wilhelm; fact 2 Waltershofen (Baden), Sven Finger; fact 3 Rheinland-Pfalz, Luca J; fact 4
Mayschoss (Ahr), Superbass (Wikimedia Commons, CC BY-SA 3.0; Mayschoss is the village D3 names for the
world's oldest co-operative); fact 5 Stuttgart, Heliao. Grape varieties are not asserted for any photograph.
