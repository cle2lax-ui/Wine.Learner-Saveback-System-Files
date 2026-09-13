# Reel — Three Ways Into Syrah
**Arc 1 week two, Tuesday 15 September — first Reel built under REELS_SPEC_v2.md**

Replaces the originally-planned 1-page Three Ways static post. Same
subject, same sourced numbers (D3 Ch. 7), new format.

---

## Why this subject fits the format

Three discrete things (Crozes-Hermitage / Saint-Joseph / Hermitage)
map close to 1:1 onto hook / thing / thing / thing / close — no filler
beat needed, unlike a two-pole Split Decision, which needs an explicit
"turn" beat to avoid feeling like two disconnected halves. Noted in
REELS_SPEC_v2.md's Source Formats section as the reason Three Ways is
now a confirmed third good source format alongside FFFA and Split
Decision.

---

## Photography — resolved this session

| Region | Asset | Status |
|---|---|---|
| Hermitage | `nr_hermitage_hill.jpg` or `nr_chapoutier_vy.jpg` | Already in repo (week one) |
| Crozes-Hermitage | none yet | **Thin** — Commons category has only 7 files total. Needs a dedicated pass before build; not blocking the storyboard. |
| Saint-Joseph | `nr_saintjoseph_sarras_vigne.jpg` | **Sourced this session** |

**Saint-Joseph sourcing note, worth repeating for any future session:**
the AOC name is useless as a Commons search term — it returns almost
nothing but the Catholic saint and EU regulatory filings.
`Category:Saint-Joseph (AOC)` has zero members. The fix is searching by
commune instead: Sarras, Mauves, Tournon-sur-Rhône, Saint-Jean-de-Muzols,
Chavanay, Charnas, Saint-Désirat. Sarras alone yielded a real, unambiguous
find — "Sarras vigne et village," François Bassaget, CC BY-SA 4.0,
1250×940 — Syrah vines in autumn colour on the hillside above the
village, with the Rhône below. Sarras is a genuine Saint-Joseph commune,
and the photographer's own caption confirms these are vines, not an
orchard misread from a distance (a real risk with several of the other
candidates pulled from the same search, which were wide village-from-
above shots where cultivated rows could not be confidently identified
as vineyard vs. orchard from the image alone — those were not used).
Resolution is modest for a 1080-wide vertical canvas; expect to lean on
the v2 colour-grade/vignette treatment to keep it visually consistent
with the sharper Hermitage source, not just crop it in isolation.

**Still needed before build:** a Crozes-Hermitage photo. Seven files
total in the whole Commons category is not much to work with — this
needs its own commune-level pass (Larnage, Mercurol, Gervans, Pont-de-
l'Isère, Beaumont-Monteux are the appellation's communes) rather than
searching "Crozes-Hermitage" directly, on the same logic that just
worked for Saint-Joseph.

---

## Storyboard — five beats, 20 seconds (v2 default: 4s/beat)

### Beat 1 — Hook (0:00–0:04)
**Visual:** Wide shot, Tain-l'Hermitage / the Rhône (`nr_tain_rhone.jpg`),
slow scale per the still-photo default.
**Super:** "Three Ways Into Syrah" (slides up + fades in at 0:00.2,
holds, fades out 0:03.6)
**v2 motion:** Progress strip draws in at bottom third — three small
nodes on a thin horizontal line, all unlit/empty. This is the frame
the closing beat has to visually complete against for the loop to read
as continuous, not reset — flagged in REELS_SPEC_v2.md as the thing
most likely to need a second pass once this is actually built.

### Beat 2 — Crozes-Hermitage (0:04–0:08)
**Visual:** Crozes-Hermitage vineyard (sourcing pending — see above)
**Super:** "Crozes-Hermitage" (region name, larger) / "~1,700 ha · 45 hL/ha"
(stat line, smaller, directly below)
**v2 motion:** Node 1 lights up and scales in (~0.3s) at beat start.
Stat bar fills left-to-right over the first ~1.2s to a length
representing the region's yield ceiling (45 hL/ha) — same fill-bar
visual language as the static decks' dashboards. Super slides/fades
per the standard v2 treatment.

### Beat 3 — Saint-Joseph (0:08–0:12)
**Visual:** `nr_saintjoseph_sarras_vigne.jpg` — vine rows in foreground,
Sarras and the Rhône below.
**Super:** "Saint-Joseph" / "50 km of appellation · 40 hL/ha"
**v2 motion:** Node 2 lights up. Bar fills to 40 hL/ha's relative
position (visibly shorter than Crozes' bar, since the ceiling is
lower — the two bars sitting in memory across a hard cut is doing real
comparative work here, not just decoration).

### Beat 4 — Hermitage (0:12–0:16)
**Visual:** `nr_hermitage_hill.jpg` (steep granite slope) or
`nr_chapoutier_vy.jpg` — whichever reads more clearly as a *slope*
at reel crop, decide at build time by looking at both cropped to
1080×1920, not by assuming from the 4:5 version.
**Super:** "Hermitage" / "137 ha · 40 hL/ha · mostly super-premium"
**v2 motion:** Node 3 lights up. Bar fills — same length as
Saint-Joseph's (both 40 hL/ha), which visually makes the point that
yield ceiling alone doesn't explain Hermitage's price tier; hectares
and soil do.

### Beat 5 — Close (0:16–0:20)
**Visual:** Return to beat 1's photo and framing (`nr_tain_rhone.jpg`)
— required for the loop-close, not a new establishing shot.
**Super:** "Same grape. The difference is the soil, and how steeply it
sits." — trimmed from the original static post's payload line
("Crozes-Hermitage surrounds the hill of Hermitage on three sides...
the difference is not the grape and barely the climate — it is the
depth of the soil and how steeply it sits").
**v2 motion:** All three nodes lit, progress strip completes (a final
connecting line draws across all three, or the strip fills solid —
decide at build time by testing both against the actual frame, per
the open loop-close question flagged in the spec).

---

## What this deliberately does NOT do

- No crossfades or wipes between beats. Hard cuts only — v2 keeps this
  from v1 without change.
- No motion during a beat beyond what's listed above. The photo scale,
  where used, stays slow and steady per the original spec; v2 adds
  categories, it doesn't invite unlimited motion.
- Audio track left empty at export, per spec, for attachment at upload.

## Open decisions for build time, not resolved by this storyboard

1. Crozes-Hermitage photography — needs its own sourcing pass.
2. Hermitage: `nr_hermitage_hill` vs `nr_chapoutier_vy` — pick by
   testing both at actual reel crop, not by assumption.
3. The progress-strip "complete" state on beat 5 — solid fill vs. a
   drawn connecting line vs. something else. Build two candidates if
   the first doesn't read clearly against beat 1's empty state.
4. Exact stat-bar proportions (do bars scale to the region's own
   yield ceiling only, or to some other shared metric across all
   three beats) — needs deciding before the animation code is written,
   not during it.
