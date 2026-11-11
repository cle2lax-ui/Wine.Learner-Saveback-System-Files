# ARC 5: WINES OF SOUTH AFRICA (plan for Steve's approval, Nov 2026; revised: less Pinotage, more Bordeaux blends and Cap Classique)

Arc 4 (Climate) is closed at Steve's word. The next arc is a country arc, and the first since Arc 3 (Mendocino) to follow one place from its ground up. Anchor: WSET Diploma D3, chapter 30 (South Africa, pp. 503-523), with D4 chapter 20 (Cap Classique, pp. 115-119) for sparkling and the CSW study guide (ch. 19) as a cross-check.

**Revision (Steve):** less on Pinotage, more on Bordeaux blends and Cap Classique. Pinotage is now one clause (the red Cape blend, 30-70%) and no longer has a slide, a Fact or the Split Decision. Cap Classique, which D4 documents in depth, gets two Field Guide slides, a Guess page and the Split Decision. The Bordeaux blends carry the red wine story (Stellenbosch, Simonsberg, Franschhoek, Paarl). **A limit to know:** D3 gives no South African tasting profile for Cabernet and Bordeaux blends (it sends the reader to its Bordeaux chapter for the varieties), so the blends' glass profile comes from the Bordeaux chapter's variety descriptions plus D3's regional comparisons, and says so.

**Thesis:** Two currents and a wind shape the Cape, where Cabernet-led blends and a rule-bound sparkling wine now carry its reputation, in a wine country that only became free in 1994.

**STATUS (Nov 2026): entry 1, The Field Guide, is BUILT as a draft, round 2** (`arc5/render_fg_sa.py`, caption `arc5/CAPTION_FG_SA.md`, review `arc5/REVIEW_FG_SA.md`): 16 slides, forest green, "Two Currents, One Wind", every claim re-read against D3/D4. Differences from the table below: slide 9 became a Stellenbosch-Paarl-Franschhoek side rail (not a duel), slide 3 a photo-led facts page, and the Swartland, cool-south and soils slides are text and color because no open-licensed photos were found. The trailer Reel is also built. Entries 2-6 are next.

## 0. Arc 4 close-out (for the record)
Built and locked: The Field Guide, "Climate's Impact on Wine" (`fg-climate-final`); the Tondonia What Am I Drinking? (`wad-tondonia-final`); Five Fascinating Facts About Climate Change (`fffa-climate-final`); the Willamette Valley Guess the Wine Region (`gtr-willamette-final`). Not built, now dropped: the Split Decision ("Move Uphill or Change the Grape?") and the summary Reel. Still open from Arc 4 before it posts: the Field Guide's end card says "NEXT UP: GUESS THE REGION" (the series is now "Guess the Wine Region"), and its posting order (Field Guide, then GTR, then FFFA, then the Tondonia).

## 1. Shape and cadence
| # | Format | Title (working) | Source |
|---|---|---|---|
| 1 | The Field Guide, 15 slides | Two Currents, One Wind (alt. "The Cape, From the Ground Up") | D3 ch. 30; D4 ch. 20 |
| 2 | Guess the Wine Region, 2 pages | A Narrow Valley, A River of Cool Air (Robertson and Bonnievale; alternates below) | D4 p. 117; D3 pp. 518-519 |
| 3 | Five Fascinating Facts About South African Wine, 6 pages | (series title) | D3 ch. 30; D4 ch. 20 |
| 4 | Split Decision, 2 pages | Cap Classique: 12 Months or 36? | D4 pp. 116-117 |
| 5 | What Am I Drinking?, 2 pages | A Stellenbosch Cabernet blend or a Cap Classique (needs Steve's bottle) | D3 pp. 514-515; D4 pp. 115-119 |
| 6 | Summary Reel (optional) | The Cape in 60 seconds | all of the above |

**Look:** arc signature **forest green** (Arc 3 green, Arc 4 burgundy; Steve's rule is burgundy or forest green for general topics). All type through `core.legible`; `engine/text_audit.py` on every deck before locking; American English; five hashtags; "The Field Guide" with "The".

## 2. Entry 1: The Field Guide (15 slides, all from D3 unless marked)
| # | Slide | Content | Layout idea |
|---|---|---|---|
| 1 | Cover | Hook: 32 to 35 degrees South, two oceans, one wind; a 370-year-old wine country that is only 30 years free | cover_bleed |
| 2 | Where it grows | Almost all in the Western Cape, 32-35 S (like central Chile, much of Mendoza), most within about 50 km of the coast; warm Mediterranean (p. 505) | map: schematic Western Cape with districts |
| 3 | Two currents, one wind | cold Benguela up the west coast, warm Agulhas down the east, meeting at Cape Agulhas; morning fog; the Cape Doctor, a strong south-easterly: cools, curbs disease, can cut flowering and yields; frost rare (p. 505) | graphic: two arrows and a wind |
| 4 | The rain gradient | Constantia about 1,000 mm; Paarl 800-900; Stellenbosch over 700; Durbanville about 500; Swartland 400-500 (see note); Olifants River 150-250. Irrigation or old vines in the dry north; the 2015-18 drought (pp. 505-506, 513-519) | chart_stack |
| 5 | Three soils | Table Mountain sandstone (sandy, poor, high slopes: Stellenbosch, Constantia); granite (holds water, dry-farming: Paarl); shale (fertile, holds water: Swartland); many soils acidic, limed at planting (p. 506) | blades |
| 6 | From 1652 to 1994 | first Europeans 1652; enslaved labor until the 1860s; the "dop" system, abolished 1961 but lasting to 1994; KWV controlled volumes and prices and backed apartheid; Chenin, Colombard and Cinsaut required for brandy, under a third of grapes made wine; 1994 democracy; KWV ceased as a co-op in 1997; about 85% of grapes made wine by 2017 (p. 504) | timeline; plain wording |
| 7 | Chenin Blanc | 16,000 ha, double the Loire; high-volume vs small-batch premium (old vines, hand-sorted, 100% Chenin) (pp. 507-508) | duel |
| 8 | Cabernet country | Stellenbosch: warm climate favors Cabernet and Merlot; very good to outstanding, premium-priced Cabernet and related blends; mountain slopes of granite and shale, 100-500 m, cooled by False Bay winds; Simonsberg-Stellenbosch (more diurnal range; Kanonkop, Rustenberg); the country's only oenology degree (pp. 514-515) | photo and stat |
| 9 | The Bordeaux blend, Cape-style | red Bordeaux blend as one of three main blends (with the white Cape blend and the red Cape blend, whose Pinotage share is 30-70%, one clause); Franschhoek's Bordeaux varieties; Paarl's fuller, riper style, and super-premium Vilafonte; Cabernet and Merlot character from the Bordeaux chapter (p. 9) (pp. 510-511, 515) | duel: Stellenbosch vs Paarl |
| 10 | Swartland | old vines (over 35 years) mostly unirrigated; since 2000 Spice Route's Charles Back, then Eben Sadie and the Mullineuxs: low yields, dry farming, old oak, ambient yeast (p. 516) | blades |
| 11 | The cool south | Constantia (since 1685, False Bay 10 km, no Pinot Noir: too windy); Elgin, the coolest area (250-500 m plateau, cloud cover); Hemel-en-Aarde, Pinot Noir and Chardonnay, up to 55% clay (pp. 512-513, 519-521) | graphic: a cooling ladder |
| 12 | Wine of Origin | four tiers: geographical unit, region, district, ward; 100% from the place named, 85% for a stated vintage or variety, tasting by the certification authority (p. 511) | diagram: nested rings |
| 13 | Cap Classique: the rules | traditional method since Simonsig in 1971; whole-bunch pressing mandatory; at least 12 months on the lees; the 2022 Extended Lees Aging tier (36 months, Chardonnay, Pinot Noir and Pinot Meunier only); association founded 1992 (D4 pp. 115-117) | blades |
| 14 | Cap Classique: the grapes | picked about 90 days after flowering at 9.5-11% potential alcohol, extra leaf cover to slow ripening; Robertson and Bonnievale: limestone, narrow shaded valleys, cool river breezes, the biggest day-night swing; the style: medium (+) acidity, ripe apple and citrus (D4 pp. 116-118) | graphic: a river of cool air |
| 15 | The glass, and the market | Cap Classique about 40% of sparkling wine sold (2021-23 average 3.9 million bottles a year), nearly 70% exported; a hand-off to the rest of the arc (D4 p. 119) | statement |

## 3. Entries 2-6
**2. Guess the Wine Region.** Page 1 names nothing: a hot, dry valley; limestone; a river that carries cool afternoon breezes up from the sea; the biggest day-night swing in the Cape; grapes that end up as bubbles (D4 p. 117; D3 p. 517). Page 2: Robertson (with Bonnievale), Breede River Valley, a source of Cap Classique and home to Graham Beck and De Wetshof (D3 p. 519). Alternates: **Simonsberg-Stellenbosch** (Cabernet-based blends), **Constantia** (since 1685, the lost and revived Vin de Constance), **Elgin** (the coolest area). Robertson's district text (D3 pp. 518-519) is to be read in full at build.

**3. Five Fascinating Facts About South African Wine** (cover plus five): (1) Cap Classique must be whole-bunch pressed and spend at least 12 months on the lees, and 36 in the new tier; (2) its grapes are picked about 90 days after flowering at 9.5-11% potential alcohol, so the finished wine is near 12%; (3) it is about 40% of the sparkling wine sold, and nearly 70% is exported; (4) in Stellenbosch the reputation rests on Cabernet and its blends (the Simonsberg peak is 1,390 m); (5) Chenin Blanc covers double the Loire's area. Reserves: the Cape Doctor, Vin de Constance's return, Swartland's old vines.

**4. Split Decision, "Cap Classique: 12 Months or 36?"** Side A: the standard rule (12 months on the lees; medium (+) acidity, ripe apple and citrus). Side B: Extended Lees Aging (36 months, Chardonnay, Pinot Noir and Pinot Meunier only, from 2022). The two sides need D4 text on what longer lees aging does to the wine, which is to be read before the post is built. Alternate: "Bordeaux Blend or Single-Variety Cabernet?"

**5. What Am I Drinking?** Default: a Stellenbosch Cabernet-based blend (D3 names Kanonkop, Rustenberg, Rust en Vrede and Raats), or a Cap Classique (D4 names Graham Beck and J. C. Le Roux). An old-vine Chenin is now the alternate. **Needs Steve's bottle photo and producer sheet** (send a 1,500 px or larger shot). The page-1 clue must not name the grape or the place.

**6. Summary Reel** (optional): The Cape in a handful of beats, ending on Cap Classique.

**Trailer Reel (built, draft):** "Watch our Page for These Posts", 30 s, posted with the Field Guide to tease entries 2-5 (`reels/sa_trailer_reel.py`, caption `reels/CAPTION_SA_TRAILER.md`). It rests only on facts the textbooks fix, so it stays true if the posts change; its strings are listed in the caption notes. It replaces the Arc 4 trailer.

## 4. Rules for this arc
- **Facts: D3 first.** D4 for Cap Classique only. The CSW guide is a cross-check, and where it differs (older planting figures, the 1918 KWV date), D3 wins and the difference is logged.
- **Known D3 inconsistency:** Swartland rainfall is 400 mm in the climate section (p. 506) and "around 500 mm" in the district entry (p. 516). The deck prints "400 to 500 mm" or leaves it out.
- **Pinotage is one clause, nowhere more.** It appears only as the 30-70% share in the red Cape blend; no slide, Fact or Split Decision.
- **Bordeaux blends: the thin spot.** D3 gives geography and quality for South African Cabernet and its blends but no tasting profile; use the Bordeaux chapter's variety descriptions (p. 9) and D3's own comparisons (Paarl fuller than Stellenbosch; mountain slopes cooler), and label which is which.
- **Cap Classique is sourced from D4 ch. 20** (pp. 115-119), not D3, and cited as D4.
- **History is stated plainly.** Slavery, the "dop" system and apartheid appear as D3 states them, in plain words, once, in the Field Guide's timeline slide. They are not decoration, a pun or a hook, and they are not in the Facts or Guess posts.
- **Producers:** only those D3 names (Klein Constantia, Hamilton-Russell, Sadie, Mullineux, Alheit, Kanonkop and so on), spelled as D3 spells them. No unsourced claims about a producer.
- **Photos:** location-verified Wikimedia Commons (probe category names first). Needs: Constantia, Stellenbosch with the mountains, Swartland bush vines, Elgin, Hemel-en-Aarde, a Franschhoek or Paarl view, old Chenin vines. Credits on each page.
- **Map:** Natural Earth coastline with the districts placed by latitude and longitude, labeled "schematic".

## 5. Decisions for Steve (defaults in bold)
1. Arc signature: **forest green**, or burgundy.
2. Order and cadence as in the table: **yes**.
3. Field Guide title: **"Two Currents, One Wind"** (alt. "The Cape, From the Ground Up").
4. Entry 2's answer: **Robertson and Bonnievale** (alt. Simonsberg-Stellenbosch, Constantia, Elgin).
5. Entry 4: **Cap Classique, 12 months or 36** (alt. Bordeaux blend or single-variety Cabernet).
6. Entry 5: a **Stellenbosch Cabernet blend** or a Cap Classique bottle; send the photo and producer sheet when ready (not needed before entry 1).
7. Entry 6: **include a summary Reel**, or skip it as in Arc 4.

## 6. Build order and what carries over
Order: 1, 2, 3, 4, 5, 6. Entry 1 is the heavy build (a schematic map, three diagrams, a timeline and about eight photos). Entries 2-4 reuse existing formats. From earlier arcs: `core.legible`, `text_audit.py`, the 42/42 and 26/26 guards, the brevity counter (`arc4/brevity_count.py`; posts under 70 words per slide), the four-designer pass and then the Social Pass, and the lock routine (tag, pixel-hash check, ZIP).
