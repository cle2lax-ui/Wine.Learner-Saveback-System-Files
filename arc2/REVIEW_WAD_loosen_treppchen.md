# Four-designer review + brevity pass: What Am I Drinking? (Dr. Loosen Erdener Treppchen Auslese 2020)

Run per `guides/DESIGN_PROCESS_v8.md` §5, in order: **Wintour** (claims) → **Chanel**
(editing) → **Ive** (craft, with pixel measurement) → **Vignelli** (grid), plus a
**brevity pass** (the series rule: cut copy, never shrink type). "Brevity pass" isn't
defined in any guide; here it means the word count of every block, a target, and the
exact cut.

Both pages were rendered and viewed. **Nothing below has been applied to the deck.**
A preview of every suggestion together is in `WAD_Loosen_PROPOSED_changes_preview.pdf`
(built separately; the deck and its PDF are unchanged).

Severity: **Fix** (an accuracy or defect problem) · **Recommend** · **Optional** ·
**Decision** (needs Steve) · **OK** (checked, no violation: a valid outcome).

---

## 1 · Wintour: claims

| # | Sev. | Finding | Proposed |
|---|---|---|---|
| W1 | **Fix** | **The bottle label contradicts the copy on the same page.** Page 2 says "just 8% alcohol" (Wine.com lists the 2020 at 8%); the bottle's label in the photo reads **9.0% vol**. The photo is very probably another vintage's bottle. | Replace the photo with a shot of the **2020** label (also fixes I5). Failing that, drop the number rather than leave a visible contradiction. |
| W2 | **Fix** | **"this vineyard"** (page 1) points at the hero photo, which is the Mosel bend at **Bremm** (Lower Mosel), not the Treppchen (Middle Mosel, Erden). The photo is uncaptioned, but "this" makes it a claim. | "…built into **the** vineyard centuries ago…" |
| W3 | **Fix** | "under one winemaker since 1988 **it has been built on** old, ungrafted vines" overstates the source: the importer says the 1988 owner saw **ungrafted vines averaging 60 years old in some of the top vineyards** as his raw material, not that the estate is built on them. | "One family has owned the estate for over 200 years; **some of its best vineyards carry** old, ungrafted vines." |
| W4 | **Fix (small)** | "citrus **zest**": the producer's wording is white peach and citrus; "zest" is an embellishment. | "…white peach, citrus." |
| W5 | Recommend | Page 2 lead **"Sweet, never heavy."** is an absolute that sits against Wine Enthusiast's "unctuous", and page 1's own Body row (Medium (+)). | "Sweet, held in balance." |

**OK, traced to a source:** hero-paragraph steps and iron-rich red slate with peppery
minerality (producer); family ownership over 200 years (importer); Aromas / Palate /
Finish (Wine Enthusiast, 93, 2020 + producer); 8% alcohol → **Low** (Wine.com, WSET low
< 11%); Acidity **High**; Aroma **Pronounced**; "VDP ranks the site Grosse Lage"
(producer product pages); "Wine Enthusiast gave this 2020 a 93"; "very ripe, partly
botrytised bunches" (importer). No names appear on page 1 (the build guard checks the
text; the photo has no signs).

**Standing disclosures (already in the deck script, not new):** Sweetness **Sweet** is
*inferred*: no 2020 residual sugar was published; Body **Medium (+)** weighs two sources
against one retailer's "medium-bodied".

## 2 · Chanel: editing

| # | Sev. | Cut |
|---|---|---|
| C1 | Recommend | **Page 2:** cut "Auslese is selected harvest:" (the name says Auslese; the audience knows it) and "the producer sees great potential for ageing" (soft, and the 93 already carries the quality claim). **−15 words.** |
| C2 | Recommend | **Page 1:** the closing sentence (W3) is also the longest; the rewrite is **−5 words.** |
| C3 | Optional | **Page 2:** remove the short gold rule between the name and the body. It is decorative (size and colour already separate them). |
| C4 | Optional (your wording) | The italic line is 11 words. "(Guess first, then turn the page)" is 6. Left alone unless you want it. |

**OK (load-bearing, not fair game):** all five dashboard rows; the notes source line
(attribution); the hero credit.

## 3 · Ive: craft (measured)

| # | Sev. | Finding | Proposed |
|---|---|---|---|
| I1 | Recommend | **The centred lockup sits on the photo's subject.** At `photo_anchor 0.5` it covers the vineyard peninsula. At **1.0** the terraces sit clear above it and the lockup lands on the dark river. Measured (90th-percentile background): title / gold line **3.6 / 3.9:1 at scrim 0.25**, **3.8 / 4.1:1 at 0.28** (both ≥ 3:1), versus 0.40 now. The photo is **18% brighter** (luminance 0.182 vs 0.154). | `photo_anchor=1.0`, `scrim_strength=0.28`. **Cost:** the dark disc is less distinct against the dark river; if it bothers you, disc opacity 1.0 or a hairline ring. |
| I2 | **Fix** | **Widow:** "focused." alone on a line in the notes. Tested by rendering. | "Long, unctuous, **focused**." fits one line and keeps *unctuous*; the notes column ends **83 px** higher. |
| I3 | Recommend | **The repeated lockup isn't identical:** page 1 disc 320 / title 160; page 2 disc 300 / 150. A repeated mark should be the same size. | Page 2 → 320 / 160. |
| I4 | Optional | **The bottle panel seam:** pure white (255) beside the page's cream (251, 249, 244), only 4–6 levels apart. Nearly invisible, so it reads as neither a deliberate panel nor a seamless page. | Multiply the bottle shot into the paper tone (seamless), or leave it. |
| I5 | **Decision** | **The bottle shot is 344 × 1200**, enlarged 2.2×. The label is legible but soft. | A shot ≥ 1,500 px tall, of the 2020 label (also W1). |

**OK:** footer clearance is **180 px** from the lowest content; the lockup group is
centred to **1 px** (276 above, 277 below the 1000 px band); series gold on paper
**3.4:1** (60 px+ bold italic is large type, ≥ 3:1); lead-word brown **5.2:1**; page 1
title 4.6:1 and gold line 3.6:1 at the 90th percentile today; both pages pass QA.

## 4 · Vignelli: grid

**OK, measured:** left margin **120 px** on both pages; page 2 text sits **100 px** from
the panel; the panel starts at **70.0%** (x = 1512) as briefed; the lockup disc's left
edge equals the text's left edge on both pages; the **dashboard and notes columns end
within a line** (50 px apart today; 33 px after I2); and page 2's **text top and the
bottle top are the same line (y = 101)**, a strong alignment worth keeping.

| # | Sev. | Finding | Options |
|---|---|---|---|
| V1 | **Decision** | **Page 2 whitespace must be structural.** The text ends 276 px above the bottle's base today; with the shorter copy (C1) it ends **564 px** above it. | (a) Accept: the text hangs from the shared top line. (b) **Bottom-anchor** the body's last line to the bottle's base, so text and bottle share a top and a bottom axis (needs a small format option; **my recommendation if C1 is adopted**). (c) Enlarge the body type. |
| V2 | Recommend | The lockup size mismatch (I3). | As I3. |

## 5 · Brevity pass: words (series budget 130 per page)

| Block | Now | Proposed |
|---|---|---|
| Page 1 paragraph | 51 | 46 |
| Page 1 notes (dashboard unchanged at 11) | 25 | 23 (W4 drops "zest"; I2 drops "yet") |
| Page 1 total (QA count) | 88 | **81** |
| Page 2 body | 58 | **43** |
| Page 2 total (QA count) | 66 | **50** |

Both pages are well inside the budget today; the cuts are for quality, not compliance.

## 6 · Decisions for Steve

1. **Apply** W2–W5, I2, I3, C1, C2 (low risk, all measured)? Recommended: yes.
2. **Hero crop** (I1): `photo_anchor 1.0` + scrim 0.28? Recommended: yes; the one trade-off is the disc's edge.
3. **Page 2 whitespace** (V1): option (a), (b) or (c)?
4. **Optional:** the gold rule (C3), the 6-word italic line (C4), the seam (I4).
5. **Bottle photo** (W1, I5): can you supply a larger shot of the **2020** label? This is the one finding I can't fix myself.

**Not run:** the **Social Pass** (the fifth pass), which wasn't asked for, and no caption
exists yet.

---

## 7 · Resolution log (the suggestions applied)

Steve supplied a new bottle shot and asked for every fix and recommendation to be
applied. **All Fix and Recommend items are in; so are the Optional ones I own.**

| Item | Status |
|---|---|
| W1 bottle label vs copy | **Resolved differently than proposed.** The new label reads 7.5%; Wine.com lists the 2020 at 8%; Wine-Searcher gives 7.5-8%; the label's vintage is not visible. Copy now says **"7.5-8%"**, true under any reading. |
| W2 "this vineyard" | Done: "the vineyard". |
| W3 "built on" ungrafted vines | Done: "some of its best vineyards carry old, ungrafted vines". |
| W4 "citrus zest" | Done: "citrus". |
| W5 "never heavy" | Done: "Sweet, held in balance." |
| C1, C2 cuts | Done. Page 1 88 -> 76 words (also the italic line changed), page 2 66 -> 50. |
| C3 gold rule | Removed. |
| C4 6-word italic line | **Not applied**: it was your wording. Superseded anyway: you later asked for "(find out on the next page!)". |
| I1 hero crop | **Re-decided.** `photo_anchor 1.0` was right for a centred lockup; for the corner lockup you then asked for, it pushed the peninsula under the lockup. **0.0** won; scrim swept to 0.52. |
| I2 widow | Done: "Long, unctuous, focused." |
| I3 lockup sizes | Done: page 2 now defaults to page 1's 320 / 160, and the lockup's ink top is aligned to the bottle top. |
| I4 seam | Done, and verified at **0 levels**. The first attempt left a 1-level step (the processed background had drifted from the original's 255); fixed by measuring after processing. |
| I5 bottle softness | **Not fixable in code.** The new shot (235x706) is *smaller* than the old (344x1200): 3.5x vs 2.2x enlargement. Large label type legible, fine print not. A shot >=1,500px tall would fix it. |
| V1 page 2 whitespace | Done as recommended, option (b): the body's last line is bottom-anchored to the bottle's base. **My own regression, caught and fixed:** anchored on the content limit, it ended 57px above the page number; the base now sits 120px higher (177px clearance). |

**Later request, not from the review:** the lockup moved to the upper-left corner,
title on one line at a smaller size (120 pt, with a build-failing no-wrap check).
