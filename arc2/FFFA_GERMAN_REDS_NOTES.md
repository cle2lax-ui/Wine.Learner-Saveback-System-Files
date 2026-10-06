# FFFA: Five Fascinating Facts About Red Wines of Germany (Arc 2)
6 pages · cobalt/ink series look with a red headline color sampled from the cover · not locked

## The deck
| # | Headline | Visual |
|---|---|---|
| 1 | Cover: **Red Wines of Germany** | the whole vineyard photo, zoomed out so the bunches show (Steve's photo, Pexels), graded build |
| 2 | Nearly a Third of German Vines Are Red | Rheinhessen vineyard at sunrise + **bar chart** (1980 vs 2021) |
| 3 | Germany's Pinot Noir Almost Tripled | red grapes, Baden |
| 4 | Dornfelder Went From Nothing to No. 2 Red | dark grapes, Rheinland-Pfalz |
| 5 | Four in Five Ahr Vines Are Red | autumn slate terraces at Mayschoss + **bar chart** (five regional rows: Nahe, Germany, Baden, Württemberg, Ahr) |
| 6 | Württemberg Focuses Mostly on Regional Red Varieties, then **Cheers!** | a toast with red wine (Steve's pick) |

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
because of the two-line headline; with it on one line, **217 px**. (2) *(superseded in round 6: page 6 now has the toast photo.)* Page 6's photo band
averaged **0.040** luminance against 0.19-0.30 on the other pages; a gamma lift of 0.6
(to 0.095) makes the terraces legible and keeps the dusk. The original is untouched; the
graded copy is built by `build_fffa_reds_cover.py`. (3) The cover glass's base came within ~50 px of the
kicker icon, so it was raised 40 px. (4) Headline red sampled by the guide's method, not by eye:
(246, 31, 13), **3.86:1** against INK (floor 3.0); the three single brightest "reds" were
blown-out pinks, as the guide warns.
**Vignelli (grid, measured).** Every text block starts at the 120 px margin (within 2 px)
on all five fact pages; pages 2-5 clear the footer by 259-319 px; both charts' left edges sit on the
margin; the highlighted bar is paper-white so the eye goes to it without touching the headline color.

## Format work this deck needed
`fff_facts.py` gained a general **`diagram="bars"`** (the style guide's open item: "collapse the
scalar diagrams into a shared helper"). It takes `slot["bars"] = [(label, value, shown, highlight)]`.
Labels and values are >= 35 px. It is the first FFFA diagram that isn't hard-coded to one deck.
The cover is a graded build because the photo's glass ran into the type zone.

## Page 6: the origins check (round 4)
Steve asked for the heading "Würtemberg Focuses Mostly on Local Red Varieties" and for the facts to be checked,
specifically that **Trollinger and Lemberger are indigenous**. **They are not**, so the page says "Regional", not "Local".
(I also used the correct spelling, Württemberg, double t, since "Würtemberg" looked like a typo.)
| | Origin | Reached Württemberg | In Württemberg today |
|---|---|---|---|
| **Trollinger** | very probably South Tyrol / Trentino; German name is a corruption of "Tirolinger" ("of Tyrol"); Italian names Schiava, Vernatsch | centuries ago; the region became the main German growing area in the 17th century | 1,855 of 1,888 ha = **98%** (German Wine Institute, 2023) |
| **Lemberger** (Blaufränkisch) | Lower Styria, now northeastern Slovenia (DNA and historical sources agree); name from Lemberg in Styria | **19th century**; an 1877 export is recorded | 1,757 of 1,917 ha = **~92%** (2023) |
The German Wine Institute's own Lemberger page says it "originated in what is now northeastern Slovenia and made its way to
Württemberg in the 19th century". Its Trollinger page calls the grape "mainly native to Württemberg", which is loose wording for
"almost all grown there". What is true, and more interesting than "native", is the concentration: both are **imports that became
regional specialties**. The body says so: "Trollinger and Lemberger lead; both are imports."
- **A caveat on "Mostly":** Trollinger and Lemberger are about 32% of Württemberg's vineyard area, roughly **half** of its red
  plantings (66%). "Mostly" is a stretch; "Leans Heavily On" would be exact. Your wording is kept.
- **Layout:** a two-line heading plus a two-line body pushed "Cheers!" to 56 px from the page edge, so the body is one line
  (about 49 characters fit) and "Cheers!" is 156 px up.

## Cover zoom-out (round 7): the bunches
Steve asked to zoom the cover out to see more of the grape bunches. **The whole photograph is now visible**, village at the top and bunches at the
base, nothing cropped (zoom 0.60). A photo smaller than the page width leaves bands at the sides, so the page stays full-bleed with the photo's own
edges mirrored outward and blurred. I measured the effect on the dark, non-green mass below the village (bunches and dark vine bases): **15% visible
before, 40% at zoom 0.76, 57% at 0.68, 85% at 0.60.** A first measurement used a color mask and was wrong (it counted dark roofs as grapes); position
fixed it. **Two things to know:** the first backdrop (a blurred, dimmed copy) looked like a gray pillarbox and was replaced; and even the mirrored version
makes the sharp photo only 60% of the page width, so the sides read as an out-of-focus continuation. `zoom=0.68` or `0.76` are one parameter away if
you want a wider photo with fewer bunches.

## Social Pass (round 7)
Run: see `SOCIAL_PASS_FFFA_german_reds.md`. Five gates pass, two fail for structural reasons (4: the final slide has no question; 6: the cover names
a topic) and need your decision, and gate 2 was strengthened: **page 5's chart now has five rows from D3** (Nahe under 25%, Germany 32%, Baden about 39%,
Württemberg 66%, Ahr about 80%) instead of three. A caption is drafted: `CAPTION_FFFA_german_reds.md`.

## Cover reframe (round 6, superseded by round 7): the village
Steve asked to see the village below the vineyard, which the round 5 framing had cropped out. **The cover is now top-aligned**, so the
roofs, garden walls, street and trees are in view above the vines. **The trade-off:** at full width the photo is 2,880 px tall but only
about 1,780 px sit above the type zone, and the grape clusters are at 68-98% of the original's height while the village is at 0-27%,
so both cannot show. I compared three framings with the type on (top-aligned, shifted 150 px, shifted 330 px); top-aligned shows the
village best and the others only swap it for foliage without bringing the grapes back. Only the small clusters along the right edge of
the row survive. The fade into black was made steeper (1560 to 1780) to keep as many as the type zone allows. If the grapes matter
more than the village, the round 5 framing is one parameter away (`shift_up=1180`).

## Page 6 photo (round 6): the toast
Steve supplied a toast photograph ("use this picture on one of the pages"). **I put it on page 6**, where a toast with red wine pays off the
"Cheers!" sign-off. **The trade-off:** it replaced the Stuttgart terraces, so the Württemberg fact no longer carries a Württemberg image
(the page claims no location for the toast: Pexels gives none). Move it to another page if you prefer, and the terraces can return.
- The photo is 5538 x 3692, a 3:2 frame that fits the fact-page photo band almost uncropped, and it is bright (mean luminance 0.34 against
  0.19-0.30 on the other pages), so the dark-photo fix from round 1 no longer applies.
- **Credit:** "RDNE Stock project / Pexels", taken from the file name (`pexels-rdne-...`; "rdne" is the Pexels contributor "RDNE Stock project").
  Tell me if the name is wrong.
- **A credit-legibility catch:** the format printed the credit in dark ink (correct for the bright corner), and an average-contrast check passed
  (10.9:1). But at full size a dark tree trunk in the photo crossed one or two letters. The fix is a soft paper-toned chip behind the credit,
  an **opt-in** format option (`credit_chip=True`); no earlier FFFA deck changes.
- The photo shows identifiable people. Pexels' license covers that use, but a model release is not visible to me.

## Cover change (round 5, framing superseded by round 6): the vineyard photo
Steve supplied a photograph of a vine row with clusters of dark grapes and asked for it as the cover. It is 3024 x 4032 (crisp),
credited "Sayed Masoumi / Pexels" (the name is from the file name; Pexels carries no location, so none is asserted). The clusters
sit in the lower third, where the type goes, so the photo is scaled to the page width, shifted up so the clusters land just above
the type zone, and faded into near-black below them. The houses at the top of the original are cropped out. The fade ends at the
photo's own bottom edge; a first pass that ran past it would have left a faint step. It replaced the two-glasses photo, so the
license and resolution worries about that one no longer apply.

## Cover change (round 2, superseded by round 5)
Steve supplied a photograph of two glasses of red wine and asked for it as the cover, cropped
closely on the glasses. It replaced the red-wine splash.
- **The source is 612 x 408 px.** A close crop around both glasses is 334 px wide, so filling the 2160 px cover is a
  **6.5x enlargement**, which no treatment can make sharp. I tested three on the real output: plain Lanczos showed blocky
  JPEG stair-steps along the rims; denoising first, then two 2x steps and a light unsharp, was clean; adding fine
  film grain made the remaining softness read as photographic texture. The grain version is in. It is still soft up close; at
  the size it is seen on a phone it reads as a warm, candlelit close-up.
- The stems and table **fade into near-black** under the wine so the type has a dark ground: measured behind the type
  zone, mean luminance 0.0006, so the white kicker has 19:1 even against the brightest pixel there.
- **No credit is printed**: the file has no photographer, agency or license data, and none was supplied. **612 x 408 is
  typical of a stock site's preview image. If it is a comp, it needs a license before this posts**; the full-size
  version would also fix the softness.
- (The scarlet headline color sampled from the old splash cover was **superseded by the flag colors**: see the next section.)

## Text colors: the German flag (round 3)
Steve asked for the font color scheme to match the German flag (black, red 221/0/0, gold 255/206/0).
- **Gold** is the cover subject, every fact headline and "Cheers": **10.60:1** on the ink block (the scarlet it
  replaced was 3.86:1). **Red** is the cover kicker, the 01-05 numerals and the closing "!": **3.07:1** on ink
  (floor 3.0), and the cobalt numerals it replaced were **1.98:1**, so they are more legible too.
- **Black stays the ground**, not a font color: black on the ink block is 1.33:1, invisible. The cover is already pure
  black, so the cover reads black / red / gold from the ground up.
- The cover's red kicker is 3.46:1 against the photo behind it at the 98th percentile; the very faintest stem
  remnants (about 2% of that zone) dip to 2.1:1. It reads clearly.
- **Not changed, and your call:** the cobalt grid mark (top right of every photo), the short cobalt rules, and the chart
  bars. They are not fonts, and cobalt is what makes FFFA read as FFFA. Say if you want them in flag colors too.
- Format: `fff_cover(kicker_color=)` and `fff_fact(accent_text_color=)` are new optional overrides (numerals and the "!");
  with them unset, every existing deck renders exactly as before (verified pixel-identical).

## Open
- **Caption**: not written. **Social Pass**: not run. **Not locked.**
- (The earlier cover photo's license and resolution concerns are moot: that photo is no longer used.)
- "about 80%" on the chart: say if you'd rather show D3's 81% (or the official 79%).
- The Ahr photo has people under a red tent in the lower right; it reads as a harvest or tasting stand, not a distraction, but it is a choice.

**Photography** (location-verified): cover, Steve's supplied photo (no credit data; the earlier splash cover was Saman Taheri); fact 1 Jugenheim (Rheinhessen), Sven
Wilhelm; fact 2 Waltershofen (Baden), Sven Finger; fact 3 Rheinland-Pfalz, Luca J; fact 4
Mayschoss (Ahr), Superbass (Wikimedia Commons, CC BY-SA 3.0; Mayschoss is the village D3 names for the
world's oldest cooperative); fact 5 Stuttgart, Heliao. Grape varieties are not asserted for any photograph.
