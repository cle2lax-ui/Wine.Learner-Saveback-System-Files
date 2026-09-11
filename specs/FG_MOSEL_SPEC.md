# Field Guide — The Mosel
## "Ripeness Was the Law"
**Arc 2, pillar post — Tuesday 22 September 2026**
12 slides · every factual claim below verified against D3 Ch. 11 (Aug 2026 edition) unless flagged

---

### 1 — Cover (`grid_cover`)
**Title:** Ripeness Was the Law
**Subtitle:** The Mosel — Ninety-One Per Cent White, Sixty-Two Per Cent Riesling

Grid: blue-grey slate fragment, a 70 per cent slope with the river
below, budburst on Riesling, a Fuder cask head, a winch rail, morning
mist on the water, a gold capsule, an A.P. number on a back label, an
abandoned terrace.

*Cover hook (gate 6):* the title is a past tense. It is doing work —
the 2021 revision is the law trying to stop being about ripeness.

> **Note on the subtitle.** Arc 1's cover led on hectarage. Ch. 11
> gives no hectare figure for the Mosel, so this one leads on the two
> proportions it does give. See the flagged list in
> `arc2/ARC2_GERMANY_PLAN.md`.

---

### 2 — Two Germanys (`editorial_lead`)
**Kicker:** THE REPUTATION PROBLEM
**Headline:** The Same Country Sold Both of These
**Standfirst:** Germany is the world's largest producer of Riesling and the country most people still associate with sugared brand wine. Both things are true, and the second one paid for the first one's collapse.

- **Riesling** — nearly a quarter of German plantings, and close to 40 per cent of the world's Riesling vineyard area.
- **Liebfraumilch** — by the 1980s this style was around 60 per cent of all German wine exports, under brands like Black Tower and Blue Nun.
- **The fall** — export volume has almost halved this century: roughly 2 million hL a year in the 2000s, around 1 million by the mid-2010s.

*Payload fact:* over the same period, average **price per hectolitre
rose by about half again** — fewer litres, worth more each, as bulk
shipping gave way to bottled exports.

> **Currency flagged.** Ch. 11 gives the absolute figures but the
> currency mark does not survive extraction. Stated as a proportion.

---

### 3 — The Map (`map_atlas.regional_atlas`)
The Mosel from the Upper through the Middle to the Lower stretch, with
the Saar and Ruwer tributaries.

Villages, upstream to down: **Piesport · Brauneberg · Bernkastel ·
Graach · Wehlen · Ürzig · Erden.** Saar: **Scharzhofberg.**

Middle Mosel is the largest of the three sections and holds the
majority of the best vineyards. Locator inset: Germany, the 13
Anbaugebiete, Mosel filled, marker verified point-in-polygon.

> **Open build question.** No public Einzellage polygon set is in
> hand; Ch. 11 gives 2,658 registered Einzellagen and no geometry.
> Option (a) traced river courses and boundaries with verified
> labelled village points — honest and achievable. Option (b) true
> polygons if a dataset surfaces. Not drawing shapes either way.
> Detail in `arc2/ARC2_GERMANY_PLAN.md`.

---

### 4 — Why Anyone Farms a Cliff (`spectrum`, photo bottom)
**Kicker:** THE SLOPE
**Headline:** Everything Here Is a Workaround for Latitude

Germany's regions sit around **49–50°N**, among the most northerly in
the world. Baden excepted, nothing about the climate is generous, so
the Mosel is a stack of corrections:

- **The river** radiates heat, moderates temperature and extends the season.
- **The aspect** — the best sites are steep and south-facing. Gradients reach **70 per cent**.
- **The slate** is dark. It takes heat in during the day and gives it back at night.
- **The altitude** is low, mostly under 200 m — at this latitude, height is not an asset.
- **The autumn** is long and dry, which is what lets sugar accumulate, and the morning mists off the water are what bring botrytis.

---

### 5 — The Cost of the Correction (`fact_file`)
**Headline:** The Bill for Farming at Thirty-Five Degrees

Steep sites need **substantially more labour** than flat ones. Erosion
is constant: owners winch soil and rock back up the slope as routine
maintenance. In the Mosel, spraying is often only practicable **by
helicopter** — which is also why organic certification is difficult
here, since drift onto a neighbour's fruit is a live risk. Nationally
about **nine per cent** of German vineyard area is certified organic.

Where consolidation under **Flurbereinigung** was not practicable —
much of the Mosel — **abandoned vineyards can still be seen.**

The blunt version: **on these slopes, often only Riesling can command
a price that makes the farming sustainable.**

---

### 6 — The Ladder (`card_grid`)
**Headline:** Six Rungs, and Not One of Them Means "Sweet"

Prädikatswein levels, in increasing order of **must weight** — sugar
in the grape at harvest, not sugar in the bottle.

| Level | The distinction | Note |
|---|---|---|
| Kabinett | Lowest must weight of the six | Lightest, highest acid. Dry to medium-sweet |
| Spätlese | "Late picked" — usually ~2 weeks after Kabinett | Riper, fuller, typically stone fruit in Riesling |
| Auslese | "Selected harvest" — extra-ripe bunches | **The last level that can be dry.** Botrytis often present |
| Beerenauslese | Individually selected berries | Hand-harvest compulsory. Always sweet |
| Eiswein | Same minimum must weight as BA | But frozen on the vine — see slide 11 |
| Trockenbeerenauslese | Shrivelled, botrytis-affected berries | Germany's most expensive wines. Rarely more than ~100 bottles a time |

Alcohol runs the other way from what the ladder suggests: a dry
Kabinett can reach **12% abv**, a sweet one can sit at the legal
minimum of **7%**, and BA, Eiswein and TBA bottom out at **5.5%**.

---

### 7 — Prädikat Is Not Sweetness (`duel`, columns)
**Kicker:** THE WORD ON THE LABEL
**Headline:** Dry Is a Measurement

Below Beerenauslese, a wine at any Prädikat level can be made at any
sweetness. The sweetness terms are separate, and they are numbers:

- **trocken** — no more than 4 g/L residual sugar, **or up to 9 g/L** where the sugar does not exceed total acidity by more than 2 g/L.
- **halbtrocken** — 4 to 12 g/L, **or up to 18 g/L** on the same kind of acid derogation (10 g/L).
- **lieblich** — 12 to 45 g/L.
- **süss** — over 45 g/L.

These do not track taste. Ch. 11 says it plainly: a high-acid Riesling
will likely **taste** drier than a medium-acidity Müller-Thurgau
carrying the same sugar.

**And the region votes differently.** In 2021, trocken was just under
**50 per cent** nationally, **64 per cent** in Baden — and **26 per
cent** in the Mosel.

*Two terms worth knowing:* **feinherb**, undefined in law, used by
producers who make halbtrocken wine and do not want the word on the
label; and **Goldkapsel**, also unofficial, marking Auslese-level
wines characterised by botrytis.

---

### 8 — The Mosel (`side_rail`)
**Kicker:** THE MAIN VALLEY
**Headline:** Pale, Light, Low in Alcohol, and Built to Outlive You

**91 per cent white. Riesling 62 per cent on its own.** Three sections
— Upper, Middle, Lower — with the Middle the largest and the home of
most of the best sites.

The village-and-vineyard pairs to know: **Brauneberg** (Juffer,
Juffer-Sonnenuhr) · **Erden** (Treppchen, Prälat) · **Graach**
(Himmelreich, Domprobst) · **Ürzig** (Würzgarten) · **Wehlen**
(Sonnenuhr) · **Bernkastel** (Doctor) · **Piesport**
(Goldtröpfchen). On a label, village first: *Bernkasteler Doctor.*

**In the glass:** paler, lighter-bodied, lower in alcohol and higher
in acidity than German Riesling from anywhere else, with pronounced
floral and green fruit. The balance of acid against flavour intensity
is what gives them the ageing.

The slate is not one colour — grey, blue, brown and red — and
producers are increasingly working on what those differences do.

*Scale, for context:* about **20 per cent** of the region's wine comes
from the **Moselland** co-operative at Bernkastel, which makes it the
**world's largest producer of Riesling.**

---

### 9 — The Saar and the Ruwer (`side_rail`)
**Kicker:** THE TRIBUTARIES
**Headline:** Colder Water, Higher Acid

Both are tributaries of the Mosel and both sit inside the same
Anbaugebiet. The best vineyards are not on the main channel but in the
**sheltered side valleys**, facing south, south-east and south-west.

Slightly **higher altitude** than the Middle Mosel, so slightly
**lower temperatures** — and acidity in the wines that can run higher
still. Small areas, several highly reputed vineyards, the most famous
being **Scharzhofberg** in the Saar.

---

### 10 — Two Wines Called Piesporter (`duel`, columns)
**Kicker:** THE LABEL TRAP
**Headline:** Same Village. Not the Same Wine.

Under the 1971 law every German vineyard was surveyed and registered
as either an **Einzellage** (individual site) or a **Grosslage**
(collective site).

| | Einzellage | Grosslage |
|---|---|---|
| Registered | 2,658 | 167 |
| Size | under 1 ha to over 200 ha | 600 to 1,800 ha |
| Piesport's | **Goldtröpfchen** — some of the finest Mosel Riesling | **Michelsberg** — largely inexpensive, lower-quality wine |

Both are legal. Both are preceded by the village name. Nothing on the
label tells a consumer which is which. The *-er* on **Piesporter**
only says the site belongs to the village.

Note also: **Grosslage** and **Grosse Lage** are unrelated. One is a
1971 collective site. The other is the top tier of the VDP
classification. They are one letter apart.

*This is Saturday's argument. Slide 10 sets it up and does not settle it.*

---

### 11 — Decode layer: Eiswein (`fact_file`)
**Kicker:** THE RUNG THAT ISN'T ABOUT SUGAR
**Headline:** A Prädikat Defined by Temperature

Eiswein got its own category in **1982**. Its minimum must weight is
the same as Beerenauslese — so on the ladder it is not a step up. What
makes it its own rung is a rule about the weather:

- Grapes must be picked **frozen, below –7°C (19°F)**.
- They must be **pressed while still frozen.** Artificial freezing is not permitted.
- Harvest can run from December — occasionally November — through to **February of the following year**, and **the vintage on the label is the year the harvest started.**
- The fruit must be **very healthy**: pressing concentrates flavour, and it would concentrate rot along with everything else.

Growers waiting for the freeze **regularly lose part of the crop, and
sometimes all of it**, to disease or to birds and animals. Some now
sheet the fruit in plastic to improve the odds.

Mosel winters are **almost always cold enough.** That is not true of
most of the wine world.

---

### 12 — Closing (`statement`, closing variant)
**Headline:** The Law Is Trying to Change Its Mind
**Subtitle:** Every fix Germany has proposed since 1971 has been an attempt to put place back into a system built on sugar.

The **VDP** — around 200 members, about 5 per cent of German vineyard
area, 3 per cent of volume, **7.5 per cent of value** — runs a
four-tier site hierarchy on a Burgundian model: Gutswein, Ortswein,
**Erste Lage** (60 hL/ha, hand-harvested, Spätlese-ripe minimum) and
**Grosse Lage** (50 hL/ha), with dry Grosse Lage wine sold as **GG**.
VDP members label their dry wines **Qualitätswein trocken** and reserve
Prädikat terms for wines with sugar — a quiet rejection of the ladder
by the people best placed to climb it.

The **2021 revision** does the same thing in statute: a geographic
hierarchy for Qualitätswein on the principle that **the smaller the
unit of origin, the higher the quality** — Anbaugebiet, Region,
Ortswein, Einzellage, then **Erstes Gewächs** (60 hL/ha, 70 on steep
slopes, 11% minimum natural alcohol) and **Grosses Gewächs** (50
hL/ha, hand-picked, 12%). Both must be dry. Grosslage is gone,
replaced by "Region."

**The open question, for Saturday:** if the best producers already
ignore the ladder and the state has now built a place-based system
alongside it, what is must weight still doing at the centre of German
wine law?

---

## Four-designer pass — notes

**Wintour (claims).** Five things this deck wanted to say and cannot:
Mosel hectarage, the export price in currency, the Sonnenuhr sundials,
Scharzhofberg as a village-prefix exception, and "Mosel-Saar-Ruwer" as
a former Anbaugebiet name. All five are out. Full reasoning in
`arc2/ARC2_GERMANY_PLAN.md`.

**Chanel (editing).** Slides 4 and 5 were one slide in the first cut —
climate and cost together — and it ran to about 180 words against a
70-word budget. Split rather than shrunk; per house rule, cut copy,
never shrink type. Slide 6's table carries the ladder so the body copy
underneath it only has to carry the alcohol inversion.

**Ive (craft).** Slide 6 and slide 10 are both tabular and sit four
apart, which is close enough to read as a pattern if they share a
treatment. Slide 6 is `card_grid` (six items, equal weight); slide 10
is `duel` in columns (two items, opposed). Different modules, on
purpose.

**Vignelli (grid).** Slides 8 and 9 are both `side_rail` and
consecutive. Arc 1 did the same with Côte-Rôtie and Hermitage and it
held, on the condition that the photo alternates sides. Slide 8 photo
right, slide 9 photo left. Check `footer_adaptive` on both — the
Arc 1 fix.

## Social pass — gates

1. **Decode layer** — slide 11, Eiswein. Placed late, as Arc 1 moved Château-Grillet to slide 11.
2. **Save asset** — slide 6, the ladder table. This is the slide that gets screenshotted before an exam.
3. **Send line** — slide 10. "Same village, not the same wine" is the line people send to the friend who bought Piesporter Michelsberg.
4. **Open question** — slide 12, handed to Saturday.
5. **Callback** — slide 7 closes the loop on Monday's Quick Sips, which is entirely about the trocken definition.
6. **Cover hook** — the past tense in "Ripeness *Was* the Law."
7. **Search surface** — Kabinett, Spätlese, Auslese, trocken, Einzellage, Grosslage, VDP, GG, Eiswein all appear as literal words on slides.
8. **Second beat** — Wednesday's GTR is solvable from slide 9. Story poll Tuesday evening on slide 12's question.
