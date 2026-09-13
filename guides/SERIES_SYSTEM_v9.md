# Series System — v9

The publishing layer that sits above the individual style guides. Every
existing series doc (`STYLE_GUIDE_v5.md`, `QUICK_SIPS_STYLE_GUIDE.md`,
`FFFA_STYLE_GUIDE.md`, `GTR_STYLE_GUIDE.md`, `THREE_WAYS_STYLE_GUIDE.md`)
governs how a deck is *built*. This document governs what gets built,
when, and why — the editorial calendar, the arc structure, and the
division of labour across review sessions.

Established 2026-09.

---

## 1. Audience strata

Ranked core-outward. Every post should serve stratum 1 without
excluding stratum 4; no post should be built for stratum 4 alone.

1. WSET / CMS / CSW students
2. Serious wine enthusiasts
3. Interested but not deeply knowledgeable
4. Hospitality, food and wine-enjoyment audience

The technical register does not get lowered for reach. Reach comes from
format selection, not from dilution — a Split Decision about whole-bunch
fermentation is legible to stratum 4 as an argument even when the
mechanism is only fully legible to stratum 1.

---

## 2. Format roles

Each series exists to produce a different engagement signal. Do not
build two formats that chase the same one.

| Series | Length | Signal | Strata |
|---|---|---|---|
| Field Guide | 10–12 slides | saves, dwell time | 1–2 |
| FFFA | 6 slides | sends | 2–3 |
| Quick Sips | 2 slides | sends | 3–4 |
| GTR | 2 slides | comments (short) | 1–3 |
| **Split Decision** | 2 slides | comments (long) | all |
| Three Ways | 1 slide | saves, purchase intent | 2–4 |
| Letter Wine List | print | — | off-platform |

**Split Decision is new in v9.** See `SPLIT_DECISION_STYLE_GUIDE.md`.
It exists because every other format resolves; nothing published before
v9 was built to be argued with, and comment depth is the signal the
back catalogue was weakest on.

---

## 3. Cadence — five posts per week

| Day | Format |
|---|---|
| Mon | Quick Sips |
| Tue | Field Guide (wk 1) / Three Ways (wk 2) |
| Wed | GTR |
| Thu | FFFA |
| Sat | Split Decision |

Field Guide sits on Tuesday, not Friday — long carousels need weekday
dwell time. Split Decision sits on Saturday because arguments run
overnight and the audience is actually drinking.

Friday and Sunday are deliberately empty. They are the buffer that
absorbs a slipped build without breaking the streak.

---

## 4. The two-week arc

Ten consecutive posts share one subject spine, normally a single D3
chapter.

**Week 1** — Quick Sips · **Field Guide (pillar)** · GTR · FFFA · Split Decision
**Week 2** — Quick Sips · **Three Ways** · GTR · FFFA · Split Decision

Why arcs rather than daily variety:
- The grid reads as a coherent body of work rather than a stream.
- Saves compound onto one subject; a follower arriving on day 8 has
  nine related posts to work backwards through.
- Sourcing stays inside one authoritative chapter per cycle, which is
  the single biggest accuracy control in the system.

Roughly 26 arcs a year against 33 D3 regional chapters. Break regional
runs with D1 mechanism arcs (canopy management, MLF, oxygen handling)
and D5 fortified arcs so the calendar does not read as a march through
a textbook's table of contents.

**Arc 1 (Sep 7–19, 2026):** Northern Rhône, D3 Ch. 7
**Arc 2 (Sep 21–Oct 3):** Germany, Mosel-weighted, D3 Ch. 11
**Arc 3 (Oct 5–17):** Piedmont, D3 Ch. 17

---

## 5. Sources

**Primary:** the WSET Level 4 Diploma texts in `/mnt/project/` — D1
(production), D2 (business), D3 (regions), D5 (fortified). Any number,
hectarage, yield ceiling, or regulatory claim that appears on a slide
must be traceable to a specific passage in these.

**Secondary:** `winewithseth.com/winewiki` — reachable via web fetch.
Useful for producer detail, vintage context, and Head-to-Head framing
that D3 does not cover. Secondary means secondary: where the two
disagree, D3 wins, and where D3 is silent the claim is flagged rather
than asserted.

**The flagging rule (locked).** If a fact does not appear in the primary
source, it goes into a "flagged for verification" block in the deck
spec and does not render until sourced. It is never silently softened
into a vaguer version of itself. Three claims were caught this way on
the very first arc — a Viognier hectarage figure, a Syrah parentage
claim, and a Hermitage price-parity claim — none of which are in D3
Ch. 7.

---

## 6. Review sessions

Two per week. Each locks 3–4 days forward, so publication always runs
5–9 days behind the current build.

**Session A** — arc open. Field Guide fully rendered, that half-week's
satellites, all captions drafted, bottle slots as placeholder blocks.
**Session B** — arc close. Remaining posts, revisions from Session A,
and the proposed spine for the *next* arc so subject is approved before
build begins.

**What arrives at review already done:** the four-designer pass
(Wintour, Chanel, Ive, Vignelli) plus the social pass. Steve edits a
fifth draft, never a first.

**What Steve supplies:** high-resolution bottle photography, per-slide
direction, and the subject veto.

**Delivery:** single merged PDF for review. ZIP of source PNGs only
after explicit lock. Unchanged from v8.

---

## 7. Caption architecture

Three parts, every post, every format.

1. **Hook** — must survive truncation at ~125 characters. The first
   line does the work; nothing load-bearing after the fold.
2. **Body** — three to five lines that add something the slides do not
   already say. A caption that restates the carousel is wasted space.
3. **Close** — a question calibrated to the format's target signal.
   Split Decision and GTR ask something genuinely open. Field Guide and
   FFFA can close on an assertion instead; a save does not need a prompt.

**Hashtags:** roughly 5 broad / 8 niche / 2 owned, rotated per arc.
Never ship the same block twice in a row — a fixed block is a
fingerprint.

---

## 8. Reels layer

Vertical cuts are a distribution treatment, not a series. See
`REELS_SPEC_v2.md`. Two per week, assembled from arc content already
built. No separate editorial.

The critical constraint: slides are 2160×2700 (4:5). Cropping to 9:16
discards 40% of the frame and guillotines type. Vertical content is
**re-composed on a 1080×1920 canvas**, never cropped from an existing
render.

---

## 9. Photo sourcing under this system

Order of preference for any location-specific claim:

1. **Wikimedia Commons** — the only source with reliable geographic
   verification for European vineyard sites. Requires
   `commons.wikimedia.org` and `upload.wikimedia.org` on the network
   allowlist. `thumb.wikimedia.org` alone is useless — it is a bare
   redirect host and serves no image bytes.
2. **Unsplash** — good for texture, produce, cellar interiors. Search
   is strict: multi-word specific queries return zero. Use two-word
   generic queries. Demo-tier key is 50 requests/hour, so batch.
3. **Pexels** — same role as Unsplash, unreliable geodata, always
   cross-check.

**When Commons is unreachable**, research can still proceed via web
search and fetch, which are not bound by the bash allowlist. Build the
shortlist and attribution manifest with those tools, then download in
one pass once the allowlist permits. See `wc_commons.py`.

**Never** attach a location claim to a stock photo whose location is
not independently verified. Generic imagery with a caption that makes
no location claim is always preferable to a confident guess.
