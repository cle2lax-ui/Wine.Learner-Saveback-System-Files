# Design Process & System Rules — v8

Everything in this document was earned the hard way during the Oregon Field
Guide build (2026-08) and is now a standing rule for every deck, not just
that one. Where a rule references "the Oregon session," that's the concrete
bug or failure that motivated it — read those notes before deciding a rule
doesn't apply to your situation; it probably applies more than it looks
like it does.

---

## 1. Font hierarchy — locked

**The rule:** headline > lead-in words > body text, strictly, every time.
Nothing below the headline in a text stack may render at a size equal to
or larger than the headline itself.

This sounds obvious and was violated repeatedly before it was caught,
because the failure is easy to miss in isolation: a lead-in phrase at
150px looked like tasteful emphasis when reviewed on its own slide, and
only became an obvious problem once it sat directly under a headline that
had auto-shrunk to ~110px to fit its own line. Two elements of near-equal
size and weight stacked on top of each other destroy hierarchy — the eye
can't tell which one is the actual headline.

**Enforcement:**
- `core.headline()` computes its own actual rendered size (it auto-shrinks
  to fit); don't hardcode a headline size assumption elsewhere in a deck.
  If you need to know it, call `headline()` first and inspect what size it
  landed on, or check `TYPE["display_md"]` / `TYPE["display_lg"]` as an
  upper bound (150 is close to the top of that range and is exactly the
  size that caused the original violation — treat it as a sign, not a
  safe default).
- When using `standfirst_lead_words` / `run_in()`-based lead-ins, set
  `lead_size` explicitly and keep it comfortably under the headline's
  rendered size — 90px against a ~110-115px headline is the value that
  worked in practice across several modules in the Oregon deck.
- Body text under a lead-in should step down again — 60px against a 90px
  lead-in was the working ratio.

**Color, not just size, carries hierarchy.** The Oregon deck's `LEAD`
palette key (see §3) exists specifically so a lead-in phrase can be
visually distinct from the headline in *color* as well as size — this
turned out to matter as much as size did. A green headline followed by a
green lead-in of a smaller size still read as competing; making the
lead-in gold (a different color, tied to `pal["LEAD"]`) resolved it
completely, and made the size-hierarchy easier to police at a glance
during review.

**Underlines are not a hierarchy mechanism.** `core.headline()`'s optional
accent underline (`show_underline`, default `True` for backward
compatibility with existing decks) was a leftover from before color-coded
hierarchy existed. Once headline/lead-in/body have distinct colors, the
underline adds nothing but visual noise — it was removed deck-wide in the
Oregon build (`show_headline_underline=False` on every slide) and every
slide read calmer and more confident without it. **New decks should set
`show_headline_underline=False` by default** and only re-enable it if a
specific slide has a real reason to need it (e.g. a single-color palette
where color alone can't differentiate levels).

---

## 2. Font color luminance — locked

**The rule:** any color used for text sitting directly on the paper/cream
background must be checked for contrast, not just pulled from the deck's
accent palette as-is. A palette's ACCENT gold, tuned to read well on a
photo or a dark chip, is frequently too light for body-weight text on
cream paper.

**The fix pattern (`GOLD_NAME` in the Oregon deck):** when a palette
color needs to double as small/body-weight text color on paper, darken it
before using it as text — the Oregon deck used `(140, 106, 30)`, a
darkened version of its `(232, 165, 22)` accent gold, specifically for
this purpose, and kept the lighter original gold for large display type
and dark-background chips where the lighter value has enough contrast on
its own.

**Two dedicated palette keys exist for this and should be set explicitly
per deck, not left to fall back silently:**
- `pal["MARK"]` — dot/glyph color (kicker dots, map pins, table markers),
  falls back to `pal["SIGNATURE"]` if unset. Lets a deck give its small
  accent marks a different color from its main headline color (e.g. red
  pips on a forest-green-and-gold deck) without touching SIGNATURE
  everywhere else.
- `pal["LEAD"]` — lead-in word color, falls back to `pal["SIGNATURE"]` if
  unset. Set this explicitly per §1 above; do not let it default to
  SIGNATURE if SIGNATURE is also the headline color.

---

## 3. Grid design, module by module — general principles

These are cross-module principles, distilled from specific fixes made
during the Oregon build. Apply per-module as relevant; not every module
has every failure mode.

**Parallel content blocks must terminate together.** Multi-column layouts
(feature_trio's three descriptions, spotlight's two callouts, duel's
table cells) read as one coherent grid only if their content blocks end
within a line of each other. A column that runs 9 lines against its
neighbors' 6-7 is a real defect, not a minor imbalance — it was caught and
fixed twice in the Oregon build (feature_trio, then spotlight) by
trimming the long outlier's copy to match, not by forcing the layout to
accommodate the imbalance.

**Whitespace should be structural, not leftover.** If a layout change
(smaller fonts, a tighter list, fewer rows) opens up empty space at the
bottom of a slide, that space needs a deliberate purpose — a repositioned
element, a supporting visual, or an explicit decision that the space is
fine as breathing room — not just be left as an accidental byproduct of
an unrelated fix. The Oregon session flagged this explicitly on several
slides after a font-hierarchy fix freed up space nobody had re-filled on
purpose; when in doubt, surface it rather than silently ignore it.

**Data claims should be visible in form, not just stated in text.** If a
headline claims a magnitude ("a state built on ONE grape"), the
supporting visual should make that magnitude legible at a glance, not
just list the numbers. The grapes-data slide's proportional photo-stack
(each grape's photo height scaled to its real acreage share, with a
legibility floor so the smallest entry still reads as a photo) is the
reference pattern for this — it turned a list of percentages that
required reading into a shape that communicates the claim instantly.

**Reused photos across a stack/grid should differ enough not to blur
together.** When multiple images sit side by side or stacked (a grape
data column, a bottle grid), don't reuse near-duplicate source photos for
adjacent entries even if both are individually "correct" for their
label — pick genuinely distinct shots.

**Blade layout for a closing/anchoring photo.** `modules.spectrum()`
supports `photo_position="bottom"`, which renders the photo as a
full-width band anchored to `CONTENT_BOTTOM` rather than a small image
floating mid-content. Use this whenever a photo's role on a page is to
anchor/close the slide rather than illustrate a specific point next to
text — it reads as a deliberate design choice instead of an image that
happens to be small.

---

## 4. Map labeling system — see `map_atlas.py`

The full algorithm, and the specific bugs each rule in it fixes, are
documented in `map_atlas.py`'s module docstring — read that file directly
rather than duplicating it here, since the code and the rationale need to
stay in sync. In brief, the eight working rules are:

1. Each label anchors to its own natural target position, never cascaded
   from another label.
2. Collision resolution is forward-pass only, then whole-chain-clamped.
3. Left-side label x-position is adaptive per label, never one fixed
   margin for the whole panel.
4. Obstacle avoidance tries all four directions and takes the smallest
   move.
5. Run a cross-side box-overlap check in addition to same-side checks.
6. Zoom/callout lines anchor to a polygon's actual extreme points, not
   its bounding-box corners.
7. Glyph layers for rotated/curved text size from font ascent+descent,
   never character width.
8. (Not yet done — flagged as the next refinement) side assignment should
   choose whichever side puts a label closest to its own region's visual
   center, rather than a simple panel-half rule.

**Also carry forward from earlier map work** (pre-dating the Oregon
session but still load-bearing): simplify a source polygon before
smoothing it, never raise Chaikin iteration count alone to force a rough
polygon smoother (point count roughly doubles per iteration and this can
blow up well before it looks smooth); use real interior points
(`polylabel`) for label anchor targets, not centroids, which can land
outside a concave polygon; sans-serif for region/AVA labels, serif for
city names, to keep the two label classes visually distinct at a glance.

**When building a new map for a new deck:** use `map_atlas.regional_atlas()`
as the slide function rather than writing deck-local map code from
scratch. If the deck's map needs something the generic version doesn't
support, extend `regional_atlas()` / `draw_map_panel()` in `map_atlas.py`
itself so the improvement is available to every future deck, rather than
forking a copy into deck-local code the way the Oregon build originally
did (and which this save-back specifically undoes).

---

## 5. Four-designer review — mandatory final step

**This runs on every deck, after the deck is otherwise content-complete,
before final delivery. Not optional, not skippable because the deck
"already looks good."**

Four full passes, one designer lens per pass, over **every slide** in the
deck — not one representative slide standing in for the rest. Order:

1. **Anna Wintour** — editorial authority. Does each slide make a clear,
   confident claim? Cut anything that hedges, pads, or dilutes the point.
   Check for genuine errors masquerading as "style" (e.g. a wine's
   varietal name repeated as literally identical text in two adjacent
   fields) as well as bigger structural calls.
2. **Coco Chanel** — "elegance is refusal." For each slide: is there one
   more element that could come off without losing anything real? Only
   remove what's genuinely decorative — a map's region color-coding, a
   lettered pin system, a data-carrying repeated label are load-bearing
   for clarity or navigation and are not fair game just because they
   "look" prunable. Removing a decorative element that has no functional
   role (e.g. a redundant underline once color hierarchy exists) is the
   right kind of cut.
3. **Jony Ive** — true simplicity. Does each slide's visual FORM actually
   reveal its content's real claim, or does the design stay neutral while
   the claim is only asserted in text? Also: obsess over details a casual
   pass wouldn't catch — a craft-level defect (cramped footer clearance,
   map linework running through label text, a photo crop that doesn't
   read) is exactly what this pass exists to find, and finding it may
   require pixel-level measurement, not just a glance.
4. **Massimo Vignelli** — grid discipline. Do parallel content blocks
   actually terminate together (§3 above)? Is whitespace doing structural
   work? Note: legitimate, purposeful asymmetry (e.g. a comparison
   layout where opposing columns intentionally fan outward toward their
   respective poles) is not a grid violation — Vignelli's own stated
   position values "careful use of asymmetry... to invest designs with
   tension and dynamism." Don't flatten a deliberate asymmetric choice
   into false uniformity.

**Rules for running this well, learned from doing it badly the first
time and well the second:**

- Actually render and view every slide for every round. A round that
  claims to review the whole deck but only shows edits on one or two
  slides has not actually been run — go back and do it properly rather
  than presenting a partial pass as complete.
- It is normal, and a sign the process is working rather than failing,
  for later rounds on an already-polished deck to find fewer issues than
  earlier ones. Do not manufacture a change just to show a round
  "happened" — an honest "reviewed, no violations found, here's what I
  specifically checked" is a valid and expected outcome for some slides
  in later rounds.
- When a fix for one issue introduces a new one (this happened multiple
  times during map-label work), say so plainly and keep iterating rather
  than presenting a partially-broken result as finished. Verify
  numerically (distance measurements, overlap checks) as well as
  visually before calling a fix done — a screenshot alone missed real
  regressions more than once in the Oregon session.
- After all four rounds, do one final full-deck rebuild and re-present
  the whole deck, not just the individually-edited slides, so the
  reviewer sees the actual current state of everything together.

---

## 6. Photo sourcing — Unsplash, alongside Pexels

A second photo source is now available alongside the existing Pexels
integration: `fetch_unsplash.py` (in this save-back), mirroring
`fetch_pexels.py`'s pattern (`search_unsplash`, `download_unsplash_photo`,
`credit_line`).

**Setup for a new environment:**
1. Set the `UNSPLASH_ACCESS_KEY` environment variable. The key is in
   `SETUP_KEYS.md` in this save-back, alongside the existing Pexels key.
2. Confirm network settings allow `api.unsplash.com` and
   `images.unsplash.com` (Domain allowlist → "Package managers and
   specific domains" → add both under Additional allowed domains). A
   fresh session may be needed after adding them to take effect.

**Unsplash-specific requirement Pexels does not have:** every photo
actually used in a deliverable (not just previewed) requires a GET ping
to its `download_location` URL, per Unsplash's API terms. This is already
handled inside `download_unsplash_photo()` — don't bypass it by
downloading Unsplash images via a different path.

Attribution format: `f"{photographer} / Unsplash"`, via `credit_line()`,
matching the existing `"{photographer} / Pexels"` convention used
throughout every deck.

---

## 7. Photo legibility scrims — check contrast before defaulting on

`quick_sips.py`'s cover page (and any future module with the same
pattern) defaults text-over-photo legibility protection to ON
(`caption_chip=True`, applied to both the corner-mark scrim and the
title/tagline scrim) — deliberately, because most photos genuinely need
some protection for white text and the safe default avoids illegible
text shipping by accident. **That default is correct and should not be
flipped system-wide** — a prior session already reasoned through this
and left an explicit code comment saying so; don't re-litigate it on the
strength of one photo.

What was missing was the judgment call itself: nobody was actually
*checking* whether a given photo needed the scrim before accepting the
default. The Alsace Edelzwicker deck's cover photo had genuinely dark
natural areas (half-timbered roof tiles, tree canopy) sitting directly
under both text zones — mean pixel brightness in the low 80s out of 255
in both the corner-mark region and the title/tagline region — and got a
heavy 62-72% black scrim it never needed, flattening real photo detail
for no legibility gain.

**The rule going forward:** before accepting the default `caption_chip`
value on any cover-style photo layout, actually check the pixel
brightness of the region the text will sit over (rough eyeball is fine
for an obviously dark or obviously bright area; measure it directly —
crop the region, check mean brightness — when it's borderline). If the
photo already reads dark enough there for white text to sit cleanly on
it, set `caption_chip=False` explicitly and verify visually. If it's
genuinely bright/busy in that zone, leave the default on. This is a
per-photo decision made once per deck, not a settings change — don't
generalize a specific photo's good contrast into a system-wide default
flip, and don't skip the check and let every deck's photo get an
unnecessary scrim by default either.

## 8. Locked module-level fixes (bugs, not style choices)

These were genuine bugs in shared code, not one-deck style calls — they
are already fixed in this save-back's `core.py` / `modules.py` and this
section just documents what they were, so no one reintroduces them.

- **`core.headline()` had no wrap fallback.** It would shrink font size
  down to a floor and then, if the text still didn't fit at floor size,
  silently overflow the slide with no further recourse. This produced
  visibly clipped headlines on three separate slides in one deck before
  being caught — it is not a rare edge case for a sufficiently long
  title. Fixed: wraps to multiple lines if it still doesn't fit at floor
  size.
- **`spectrum()`'s photo credit used the wrong slot key.** It read
  `slot.get("credit")`, but every slide in every deck sets
  `photo_credit`. This meant photo credits silently never rendered for
  any `spectrum` slide using the (pre-existing) top-photo layout, in any
  deck, until it was traced down while wiring up the new bottom-photo
  layout. Fixed in both the top-photo and new bottom-photo paths.
- **`statement()` never passed `footer_label` through to `_finish()`.**
  A slide setting `footer_label=""` to suppress "SWIPE ←" on a genuinely
  final slide had no effect. Fixed.
- **`_curved_text()`'s per-character rotation layer was sized from
  character width, not font ascent+descent.** See map_atlas.py rule #7.
  This silently clipped most rotated/curved text to illegible fragments,
  invisible to any pixel-count-based QA check — only caught by actually
  zooming into the rendered output. If any other module ever adds
  rotated text, size the rotation layer from `font.getmetrics()`
  ascent+descent, not from measured character width.
- **`Image.rotate(angle, expand=True, center=(x,y))` destroys alpha.**
  Passing an explicit `center` together with `expand=True` is a genuine
  PIL footgun — it silently zeroed the alpha channel on every rotated
  glyph with no error raised. `expand=True` alone (letting PIL compute
  its own center) works correctly. Never combine the two.

---

## 9. FFFA series — Vignelli-grid treatment (locked)

Third carousel series, "Five Fascinating Facts About...". Full detail
in `FFFA_STYLE_GUIDE.md`; this section is the subset of rules that are
system-locked rather than deck-specific, the same distinction section
1-8 draw for the other series.

- **Fixed 6-page format** — cover + 5 facts, not a variable module
  sequence. `fff_facts.py` is a peer module file to `modules.py`, same
  relationship `guess_the_region.py` and `map_atlas.py` already have.
- **Own palette, deliberately not shared with Field Guide or Quick
  Sips**: flat cobalt (`FFFA_ACCENT`) for numerals/rules/grid-mark,
  golden yellow (`FFFA_YELLOW`) for the cover subject and every fact
  headline only, ink/paper for everything else. No gold accent from
  either sibling series.
- **Cover is photo-only** — no flat color block. Whether the text zone
  needs a scrim is decided per-photo by measuring actual rendered
  luminance (`region_luminance()`) under the text, same discipline as
  section 7, never assumed either way.
- **Checklist icon is drawn from primitives** (`_checklist_icon()` in
  `fff_facts.py`), never sourced as an asset — appears full-size on the
  cover and at reduced scale beside every fact numeral, aligned to the
  numeral's actual glyph top (measured via `textbbox`, not the font's
  nominal ascent box).
- **35px minimum font size for any chart/diagram label** — sits below
  the body-text floor deliberately (charts pack tighter than prose)
  but is still a hard floor. Applies to any current or future FFFA
  diagram, not just the two shipped with the Champagne deck.
- **Diagrams over stock photos for comparative/scalar/relational
  claims.** Same "data claims should be visible in form" principle as
  section 3, made explicit as a locked FFFA rule because the failure
  mode is predictable: a claim like "these five things differ by size"
  or "this thing is the parent of that thing" will never be well
  served by a single stock photo, no matter how long the photo search
  runs. Three diagram types exist as of v3 (bottle-scale, ranked-bar,
  parentage) — but a diagram is available per-fact, not mandatory per-
  fact; a fact that reads fine as photo + copy should stay that way.
- **Per-deck headline color override, sampled from the photo, not
  guessed.** `fff_cover()` / `fff_fact()` take an optional
  `headline_color=` kwarg (default `FFFA_YELLOW`). When a deck's
  subject calls for a different accent (a red wine deck wanting a red
  headline, confirmed working in v3 on Cabernet Franc), derive the
  exact color from the actual cover photo via HSV hue/saturation
  filtering + brightness ranking (see FFFA_STYLE_GUIDE.md for the
  snippet) rather than picking a value by eye, and always verify the
  result against `core.contrast()` before shipping — the first
  unverified guess this session came in under the 3.0 floor.

## Delivery: PDF-first, ZIP-on-lock (locked, per Steve, 2026-08)

**The rule:** when presenting a deck in review, share a single merged PDF
— never the individual slide PNGs. Only hand over a ZIP of the source
PNGs once the person has explicitly confirmed the deck is locked/final.

**Why:** loose PNGs in a review round scatter the deck into separate
file cards, make slide order harder to follow, and risk the person
reviewing a stale individual PNG after a re-render. A PDF reads as one
document. The ZIP is a production asset for after sign-off, not a
review artifact.

**Enforcement:**
- `core.py` provides `assemble_pdf(png_paths, pdf_path)` and
  `lock_deck_zip(png_paths, zip_path)` as two deliberately separate
  functions — not one call with a mode flag. `assemble_pdf` is safe to
  call on every iteration. `lock_deck_zip` is a one-directional "this is
  final" action and should only be invoked after explicit sign-off, so
  it is never wired to run automatically alongside the PDF build.
- `build.py`'s `build_deck()` always produces PNGs + the review PDF and
  returns both; it does NOT zip. A separate `lock_deck()` call (new
  function, same file) takes the returned PNG paths and produces the
  ZIP — call it only once told the deck is locked.
- Any standalone render script (a deck outside the `build_deck()`
  manifest flow, e.g. Guess the Region's per-deck scripts) should still
  call `core.assemble_pdf()` directly on its output PNGs and present
  that PDF, for the same reason.
- When presenting to the person: default to sharing the PDF. Only
  share/mention the ZIP after they've said the deck is locked.
