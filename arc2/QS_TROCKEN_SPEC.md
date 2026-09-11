# Quick Sips — "Dry Is a Number, Not a Taste"
**Arc 2, opening post — Monday 21 September 2026**
2 pages · verified against D3 Ch. 11 (Aug 2026 edition) unless flagged

---

## The idea

`trocken` is a laboratory threshold, not a sensory promise. The
derogation built into it — up to 9 g/L residual sugar where the sugar
does not exceed total acidity by more than 2 g/L — is satisfied almost
by definition by high-acid Riesling. So the driest-tasting wines in
Germany are frequently the ones carrying the most sugar, and Ch. 11
says so outright.

This is the arc's doorway. Everything Tuesday's pillar does with the
must-weight ladder depends on the reader already accepting that the
words on a German label are measurements.

---

## Page 1 — cover (`quick_sip_cover`)

**Photo:** Middle Mosel slope, morning, river visible. Commons —
shortlist from `Bernkastel-Kues` (227 files) or `Brauneberg` (74).
Contrast-check the title colour against the real photo before locking;
legibility chip on if the slope is busy.

**Title (left-anchored, flush to photo bottom edge):**
Dry Is a Number

**Tagline:** What "trocken" actually measures

**Run-in paragraph 1** — bold lead-in `THE THRESHOLD.`
A German wine labelled trocken carries no more than 4 g/L of residual
sugar. Except that it can carry up to 9 g/L, as long as the sugar does
not exceed the wine's total acidity by more than 2 g/L. Riesling, which
holds high acidity even when fully ripe, clears that condition
routinely.

**Run-in paragraph 2** — bold lead-in `THE CONSEQUENCE.`
Which means the number on the certificate and the sensation in the
mouth are two different things. Ch. 11 puts it plainly: a high-acid
Riesling will likely taste drier than a medium-acidity Müller-Thurgau
holding exactly the same sugar. Acid is doing the work the label gets
credit for.

> Word budget: `qa.word_limit = 130` for this series — note the fix in
> `QUICK_SIPS_STYLE_GUIDE.md`; decks before that fix were silently
> enforced at 70.

---

## Page 2 — detail (`quick_sip_detail`)

**Heading:** Halbtrocken, and the Word That Replaced It
*(benchmark-bottle heading does not auto-wrap — break on a literal `\n`)*

**Body:**
The next band up, **halbtrocken**, runs 4 to 12 g/L — or up to 18 g/L
on the same kind of acid derogation. It has fallen out of favour: the
word reads as a hedge, so producers who still make the wine either say
nothing about sweetness at all or use **feinherb**, which is not
defined in law, covers the legal halbtrocken range, and stretches a
little past it.

**The regional tell.** In 2021 trocken was just under **50 per cent**
of German production, **64 per cent** in Baden — and **26 per cent** in
the Mosel. Warmer regions get ripeness to balance acid without sugar.
The Mosel, at the northern edge, mostly doesn't, and mostly doesn't
try.

### Bottle slots — Steve's photography required

Two Mosel Rieslings that sit either side of the line:

- **Slot A** — a Mosel Riesling labelled **trocken**. Ideally one whose
  back label or tech sheet gives an actual residual sugar figure, so the
  9 g/L derogation can be shown rather than asserted.
- **Slot B** — a Mosel Riesling at **Kabinett** with visible residual
  sugar, from the same village if possible, ideally the same producer.
  Same site, same hand, opposite side of the threshold.

Dashboards render as **placeholder blocks** until the bottles land. No
tasting descriptors, alcohol figures or sugar numbers are pre-written
into this spec — Arc 1's Clape/Paris alcohol inversion was only worth
printing because it was read off the actual bottles rather than
inferred. Descriptors when they come are **WSET Level 3 vocabulary
only**, per the series guide.

Dashboard shape: **5-row white.** Sweetness → Acidity → Alcohol → Body
→ Aroma Intensity. No tannin row.

**Footer:** suppress the SWIPE cue on page 2 via
`modules._finish(footer_label=...)`.

---

## Notes

**Why this and not Eiswein.** Eiswein was the obvious opener and it is
better used as the pillar's decode layer on slide 11, where a reader
who has swiped eleven slides gets rewarded. An arc that opens on its
most colourful fact has nowhere to go.

**Callback target.** Tuesday's slide 7 restates the trocken thresholds
in full. That is deliberate repetition across two days, not an
oversight — the Monday post is where a reader learns it and the
Tuesday slide is where they recognise it.
