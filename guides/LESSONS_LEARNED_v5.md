# RETROSPECTIVE — Why v4.x Got Arduous, and What v5.0 Fixes

Written at the close of the Super Zone (Southeast Australia) build. This document
is the reason for every architectural decision in v5.0. Read it before touching
modules.py.

---

## 1 · The core failure pattern: fixed pixel budgets vs. variable content

Almost every collision bug this cycle traced back to the same root cause:
modules allocate a **hardcoded pixel budget** for a text stack (e.g.
`text_budget = 480`), then draw content that may run longer than that budget,
with no feedback loop between "how much space did I reserve" and "how much
space did I actually use."

Concrete instances:
- `showcase_shelf`: text_budget was sized for a 3-line stack (name/style/origin).
  Adding a producer line broke every row silently — QA caught the *symptom*
  (collision) but nothing caught the *cause* until traced by hand.
- `duel` table mode: row pitch assumed 1-line labels. A label wider than
  `label_w` didn't wrap at all — it just overflowed into the next column,
  and QA's box for that row didn't separate label from value, so the
  collision was invisible to the checker.
- `mosaic`: captions were never wrapped in the first place (single `d.text()`
  call) — not a budget mismatch, just a missing feature that looked like one.

**v5.0 fix:** every module that stacks variable-length text now measures the
actual rendered height *before* committing to a row pitch, and asserts
`actual_height <= budget` internally, raising a clear build-time error
("row 3 needs 340px, budget is 280px — shorten copy or raise the budget")
instead of a silent collision two layers downstream. Budgets are still
explicit constants (predictability matters more than cleverness), but they're
now checked, not assumed.

## 2 · `wrap()` had a latent bug for exactly two years of use

When a single word is wider than the column, the old `wrap()` emitted a
leading empty-string line before it. This went undetected because most copy
doesn't have single unbreakable words wider than a column — until "Subregion"
and "Benchmark" in a narrow table column did. **Fixed at the root** (not
patched at every call site) — this class of bug could have been silently
present in any narrow-column module all along.

## 3 · QA's blind spots — collision-checking is necessary, not sufficient

The `QA` class catches: type-floor violations, headline/body hierarchy,
box-pair collisions, content-zone overflow, word budget. It does **not**
catch:
- Canvas edge overflow (labels running off the left/right of the page —
  found on the facsimile map, twice, because nothing checked `box[0] < 0`
  or `box[2] > W`).
- Text-over-photo contrast (found the duel slide's white label text at
  luminance 175 on a near-white product photo — QA has no concept of
  "what's under this text").
- Underfilled slides ("open space where there should be editorial copy" —
  QA has no lower bound, only an upper one).
- Whether a background-removal mask actually removed the background
  (three failed bottle-cutout attempts this cycle, and the *verification*
  method itself had a seeding bug that reported false holes).

**v5.0 fix:** `QA` gains three new checks that run automatically, not as
manual post-hoc scripts: `qa.check_bounds()` (every box within [0,W]×[0,H]),
`qa.check_contrast(region, text_color)` (luminance-delta sampling under any
text drawn on a photo), and a documented, tested `remove_background()`
utility with a **correct** hole-check (padded before flood-fill, so the seed
pixel is guaranteed exterior — the old check's bug produced false positives
that led to a wrong diagnosis being reported as fact).

## 4 · Scrim() is one function serving two different jobs badly

`scrim()` is a top/bottom gradient — right for blending a photo into a
caption zone, wrong for a solid UI chip (like a kicker label) that needs
guaranteed uniform contrast regardless of what's under it. Using the gradient
for both gave the mosaic kicker a scrim that faded to *zero* strength exactly
where the text sat.

**v5.0 fix:** two distinct primitives — `scrim()` stays a gradient for photo
blending; new `chip()` draws a flat, full-opacity rectangle for any text
that must be legible regardless of the photo underneath. Modules pick the
right one by what they're doing, not by copy-pasting whichever was closest.

## 5 · Locked conventions that were only locked in prose, not in code

Memory said "producer name above wine name (shared function)." The code had
no producer field at all. A convention that lives only in a memory note or a
docstring comment is not locked — it's a suggestion nobody's enforcing.

**v5.0 fix:** every "shared function" convention referenced in memory now has
a corresponding code path that will *fail to build* without it (e.g.
`showcase_shelf` requires a `producer` field in every product tuple — no
silent fallback). If it's locked, the schema enforces it.

## 6 · Bespoke one-off scripts vs. real modules

The Australia map went through several iterations as a standalone script
(`render_facsimile.py`) before finally being generalized into `M18
map_facsimile`. That generalization was the right call — it made ghosting,
nudges, and the whole SOP reusable — but it happened *after* a lot of
one-off debugging that a proper module (with its own QA integration from
day one) would have caught earlier.

**v5.0 fix:** no more "build it as a script, promote it to a module later."
Anything that's going to recur — and cartography clearly recurs — starts as
a module with QA wired in from the first render.

## 7 · Process discipline that has to be non-negotiable

- **PDF + zip, every time, no exceptions.** This was skipped once this cycle
  and caught immediately by the user. It's now the literal last step of
  `build.py`, not a manual afterthought.
- **Bottle/product photo processing is a real pipeline, not ad hoc code
  written fresh each time.** Flood-fill background removal, tight trim,
  hole-check verification — this happened *six separate times* this cycle
  with six slightly different implementations, several of them buggy.
- **When visual inspection isn't available, say so plainly and verify
  numerically instead** — but audit the numeric method itself before trusting
  it. "Verified numerically" was stated confidently on a check that had its
  own bug; that's worse than admitting uncertainty.
- **Diff working copy against project files at the start of any session
  touching the system** — still true, still the standing rule, restated here
  because it's easy to forget mid-flow.

## 8 · What made Castilla y León the high-water mark

Working backward from the complaint ("we've taken a step back"): that deck's
strength wasn't a fundamentally different design language — it's that the
system was young enough that every module was still being used within the
bounds it was actually tested for. As the system accreted patches (map
facsimile, producer fields, chip vs. scrim, wrap fixes), each fix was correct
in isolation but the *whole system's* test coverage — the specimen deck —
wasn't kept in lockstep. A module could drift from its own documented
contract and nothing would notice until a real deck hit the gap.

**v5.0 fix:** the specimen deck is not a nice-to-have reference — it's the
regression suite. Every module change gets re-rendered in the specimen deck
before it ships. If the specimen deck doesn't render clean, nothing ships.

---

## Carried forward unchanged (these were right, keep them)

- The Source-Faithful Map SOP (v4.3, section 7b) — extraction → leader-line
  matching → single uniform fit → nudge-only collision resolution →
  ghost-don't-delete for off-scope areas. This process is sound; nothing
  this cycle contradicted it.
- The general QA philosophy (hard floors, collision detection, word budgets,
  `"!"` exemption convention for approved exceptions) — the mechanism is
  right, it just needed the three additions in §3.
- The locked palette, type ramp, and margin system — no complaints surfaced
  against these; they're not being touched.

---

## Addendum · The specimen deck caught two more bugs immediately

Within minutes of actually building `specimen.py` — running realistic,
non-trivial placeholder copy through every module — it failed two modules
that had shipped as "working" all cycle:

- **`showcase_shelf`** still collided at its own documented default
  `zone_h` once realistic producer names and a full tasting note were
  used across all six products, not the artificially short copy that
  happened to fit in the decks built this cycle. The default budget was
  tuned to what today's placeholder copy needed, not to what the schema
  actually promises — the exact anti-pattern in §1, and it survived until
  something finally stress-tested it. Fixed by raising `text_budget` and
  lowering the default `zone_h` so the out-of-the-box default is safe
  without per-deck tuning.
- **`lexicon_cloud`** claimed `terms[...x10-14]` in its own docstring and
  failed to fit 10 terms with realistic (not one-word) glosses — needing
  2674px against 1810px available. The module itself wasn't broken (it
  fails loudly with an exact px-needed-vs-available count, which is
  correct v5.0 behavior) — its documented capacity claim was just wrong.
  Fixed the docstring to say what's actually true: capacity depends on
  gloss length, not term count alone.

Neither of these was hypothetical — both shipped, passed every review
this cycle, and broke the moment realistic content actually exercised
them. This is the whole argument for keeping the specimen deck as a real
regression suite: it has to run real content, not minimal placeholders,
or it doesn't catch anything.

---

## 9 · The Cava/Corpinnat/Clàssic Penedès build: a second wave of the same pattern

A full 11-slide deck built end-to-end surfaced another round of real bugs —
almost all the same root cause as §1 (unmeasured text vs. assumed space), plus
a few genuinely new categories (image orientation, transparency, cartographic
accuracy). Logged here so they don't recur.

**Unbounded single-line text (the headline/title family of bugs).** Three
separate functions drew a title/headline as one `d.text()` call with zero
width-checking: `core.headline()` (used by nearly every module),
`quick_sip_cover`'s title, and `quick_sip_detail`'s headline (Quick Sips has
its own renderers, doesn't go through `core.headline()`). All three now
shrink the font in small steps until the text fits the available width,
with a floor tied to the hierarchy rule (`core.headline()`) or to `FLOOR`
(Quick Sips). **Fix pattern to reuse:** any place that draws a single line
of caller-supplied text at a fixed size needs this same shrink-loop, not
just the "big" headline calls — `statement()`'s lower_left cover subtitle
and `ladder()`'s tier labels needed the identical treatment (see below).

**`ladder()`'s tier labels — a pyramid-specific variant of the same bug,
plus a second vertical bug once the first was fixed.** The label was drawn
unbounded, and because a pyramid narrows toward the top, the longest label
often lands on the *narrowest* tier — worse than a uniform-width column
would be. Fixed with the same shrink-then-wrap approach. But fixing the
label alone wasn't sufficient: once the label could wrap to two lines, the
label+note combined height could exceed the tier's own fixed height,
overflowing the shape vertically. The real fix measures the tier's actual
remaining vertical space after the label renders and fits the note within
*that*, shrinking or dropping to one line rather than assuming two
fixed-height lines always fit. Verify both axes when a shape has both — a
width fix that ignores height (or vice versa) just moves the overflow.

**`duel()` table mode — the "which box did the collision check use" trap
from §1, still shipping.** `lv`/`rv` values were single unbounded lines
identical to the headline bug, AND the QA box registered for
`row_val{i}` spanned the *entire* row width (`xc` to `W-M`) rather than
each column separately — so even if one value's text visually ran into
the other column, the collision checker had no way to see it, because
both columns' text lived inside the same oversized box. Both problems
have the same underlying lesson as §1's `showcase_shelf` case: **a
generic-looking QA box is not the same as a box that actually bounds the
content it's meant to catch.** Fixed by wrapping both values to their own
column width and giving each its own box.

**`process_map()` never counted words at all — caught and fixed
mid-session.** No `qa.add_words()` call existed anywhere in the original
function, so its body text was invisible to the 70-word budget check
regardless of actual length. Fixed as part of the same pass that
reworked the module's step rendering (font sizing, wrapping, sequential
numbering) — `qa.add_words(text)` now runs per step. Verified by
re-running the module and confirming `qa.report()` shows a real,
non-zero word count that matches the actual copy, not just that the
function executes without error. Column titles are still not counted
(they're short labels, not body prose, the same convention as kicker/
headline text elsewhere) — a deliberate omission, not a gap.

**Image orientation and transparency — not text-layout bugs, but the same
"nothing checked this before" flavor.** `load_photo()` never applied EXIF
rotation metadata (phone photos with a rotation tag displayed sideways)
and forced `.convert("RGB")` on load (which drops alpha and keeps whatever
raw RGB sat under a transparent pixel — invisible on a plain white photo,
a solid black or garbage-colored box on anything with real transparency
pasted onto a colored background). Both fixed at the source in
`load_photo()`; a new `load_photo_rgba()` was added for the specific case
of product cutouts that need their transparency preserved through the
paste (`showcase_shelf`), rather than composited onto white. See
STYLE_GUIDE_v5 §8 for the full writeup — this replaces what used to be a
manual-inspection workaround note with an actual fix.

**A background-removal script written ad hoc for one photo reintroduced
a bug the project's own locked `core.remove_background()` had already
solved.** Mid-session, a quick flood-fill script (written outside the
existing pipeline, to strip a plain white background from one product
photo) leaked into the bottle's own silhouette and cut a hole straight
through it — confirmed by checking the alpha channel row-by-row, not by
eyeballing the render. `core.remove_background()` already has a
documented hole-check specifically because this exact failure mode
shipped once before (per its own docstring / LESSONS_LEARNED history).
**Lesson: use the project's existing, hardened image-processing
functions instead of re-deriving ad hoc versions under time pressure,
even for what looks like a simple one-off case** — the hardening exists
because the simple version already failed before.

**A source photo can be corrupted in ways that look like a design
choice.** One showcase-shelf bottle photo had a hard-edged, ~94%-solid
black rectangle baked into the file, disconnected from the bottle's own
silhouette. First instinct was to read it as legitimate dark
packaging/capsule — wrong; confirmed by checking fill-ratio and edge
hardness (a real photographic element has soft/organic edges and varies
in density; this was a flat, sharp-edged block). It was inflating the
crop's bounding box, which was *also* the cause of a separate-looking
complaint ("this bottle renders too small") — both symptoms had the same
one root cause. Patch obviously-artificial defects out (white fill over
the exact connected-component bounds) before running background removal,
rather than adjusting unrelated scale parameters to compensate for a
corrupted crop.

**Cartographic work: "accurate" and "schematic" are different promises,
and the module needs to support both explicitly.** A user-supplied
reference map (raster, not vector) needed the same locked-SOP treatment
(`map_facsimile`'s "trace, don't eyeball" principle) despite not fitting
its PDF-vector extraction pipeline — solved with an equivalent
color-segmentation + contour-extraction approach reaching the same
standard by a different technical route. Separately, `atlas()`'s
decorative locator inset was upgraded from a freehand schematic
silhouette to a real traced country outline (public boundary data,
dissolved with shapely) with a real traced sub-region highlight, gold
marker verified by point-in-polygon rather than eyeballed — now the
locked default for any deck's locator inset (see STYLE_GUIDE_v5 §7,
`atlas` row). The lesson isn't "always use real data" (a decorative inset
can legitimately be schematic) — it's that the module needs to make
which promise is being kept *explicit* (schematic vs. traced) rather than
leaving it ambiguous, because the person asking often means the stronger
one even for a "small" inset.

**Kickers and several other labels were forced ALL CAPS system-wide, with
no per-deck opt-out.** Not a bug exactly, but a locked convention that
turned out not to be what this deck's owner wanted, and it was baked into
`core.kicker_block()` plus five other call sites individually
(`atlas()`'s state labels and inset label, `mosaic()`'s kicker,
`euler_nesting()`'s exceptions label, `editorial_lead()`/`side_rail()`'s
table/list group titles) rather than one shared switch — meaning "remove
the forced uppercase" was six separate edits, not one. Now removed at all
six (plus the Quick Sips equivalents: stat-strip labels, cover eyebrow).
**If a future convention change needs to apply "everywhere," check for
every duplicated implementation of the same visual rule, not just the
most obvious/shared one** — `kicker_block()` looked like the single
source of truth and wasn't.

---

## 10 · The "Clash of the Titans" deck: system-wide preference changes,
## a bespoke cover build, and a second wave of the §9 headline bug

This was a full Field Guide build (Cabernet Sauvignon, four regions)
that ran long enough to surface both new standing preferences and a
second round of the exact bug class documented in §9. Also the first
deck to require a genuinely bespoke, hand-built cover (a four-bottle
lineup with custom labels) rather than composing from existing modules.

**Two system-wide preference changes, not per-slide fixes.** Mid-deck,
the person set two new standing defaults across every layout: bottom
content margin `CONTENT_BOTTOM` moved from `H-400` to `H-200` (more
usable space per slide), and `MAX_BODY_WORDS` moved from 70 to 105
(+50%). Both are `tokens.py` constants, so both took effect everywhere
at once — but this meant several already-built slides that had been
tuned to fit the *old*, tighter budget suddenly had unused room, and
had to be revisited and re-expanded on request rather than left
artificially short. **When a token-level constant changes mid-session,
audit content built before the change — "fits" was measured against a
boundary that no longer applies.**

**§9's headline bug recurred independently in two more places.**
`side_rail()`'s headline draw was a bare `for ln in
slot["headline"].split("\n")` with no width-checking at all — same
failure as the original `core.headline()` bug, just in a different
function that draws its own text instead of calling the shared one.
Confirmed by direct measurement, not guesswork: the actual headline
text measured 1956px against 1110px of available column width, drawn
as one line with the overflow just running off-canvas. `mosaic()`'s
`overlay_title` needed the same treatment. **The lesson from §9 stands
and keeps proving true: there is no single shared code path that
protects every headline-shaped string in this codebase.** Any module
that draws its own title/headline outside `core.headline()` needs its
own explicit width-check-and-shrink; audit for this specifically
before assuming a "headline" is safe.

**A leader-line bug that looked fixed on the first pass wasn't —
verify the actual pixel math, not just that the code runs.**
`atlas()`'s marker leader lines connected at the *raw, unadjusted*
label y-coordinate — which for any wrapped multi-line label fell
*inside* the last line's own vertical span (measured: the line spanned
y-30 to y+57, and the leader was drawn at y+0, squarely inside that
range), so it was visibly cutting through the letters. The first
attempted fix (anchoring to the block's vertical center) was still
wrong in a different way — better, but not what was asked for. The
working fix anchored to the *top-middle of the label's first word*,
computed from that specific word's actual rendered width and position
— and a further request narrowed it to a *specific letter* inside that
word (`anchor_letter='t'` targeting the literal rendered position of
the "t" in "Left"), which required locating a substring's pixel offset
directly rather than reasoning about the word as a whole. **When a
person says a fix "isn't good," don't just try a different guess —
compute the actual geometry (row spans, pixel offsets) the way the
person is looking at it, the same way §1 and earlier sections in this
document establish for text collision generally.**

**Marker dots, `wrap_w`, `anchor_letter`, and `no_leader` were all
needed because a cartographic slide got iterated on repeatedly, not
because they were anticipated up front.** This is a normal pattern
worth naming: `atlas()`'s `markers` list started as a fixed-position,
single-line, always-has-a-leader-line feature and picked up four
separate optional behaviors over the course of one slide's revision
history (bigger dots, label wrapping for labels moved into open ocean,
a specific-letter anchor override, and a way to turn the leader off
entirely for markers close enough to their target not to need one).
None of these were designed in advance; each came from a specific,
concrete complaint about how the current render looked. Building
these as slot-level options (defaulting to the old behavior) rather
than one-off script edits is what made each of them reusable for the
*next* map-heavy deck instead of one-time patches.

**A `lat_bands` feature (faded latitude bands, e.g. the 30°–50° "wine
belt") had to be composited with real alpha blending, not drawn
underneath the landmass fill.** The landmass polygons are drawn
opaque; a band drawn *before* them would be completely invisible
wherever land covers it, showing only over ocean. The fix draws the
band as a separate `RGBA` overlay and alpha-composites it *on top of*
the already-rendered land + sea, so the tint reads consistently across
both — the same "order of operations matters for transparency" lesson
that also applied to `showcase_shelf`'s bottle-pasting fix in §1.

**`atlas()` had no way to render a flowing paragraph — only a 3-column
key-value legend strip.** Adding a `paragraph`/`paragraph_lead` slot
(reusing the deck's standard bold-serif-lead-in `run_in()` pattern,
including the `justify` and `leading` parameters added this session)
was a real capability gap, not a bug — the module had genuinely never
needed to say anything in prose before.

**`showcase_shelf` hardcoded `cols = 3`.** A four-bottle showcase (one
bottle per region, matching the cover's four-bottle lineup) wrapped
the 4th product to a second row, and because the deck's `zone_h` was
sized for large single-row bottles, that second row's height alone
exceeded the canvas — confirmed by tracing the actual row-position
formula, not by guessing: `cy = panel_top + (i//cols) * (row_h+24)`
put row 2 starting past y=2700 on a 2700px-tall canvas. Fixed by
making `cols` a slot parameter; a four-region deck now uses `cols=4`
for a single row instead of forcing a 3+1 wrap. **Any hardcoded "N per
row" constant is a latent bug for the next deck that doesn't have
exactly N of that thing** — this is the same shape of bug as the
Cava/Corpinnat session's word-budget and column-count assumptions,
just in a new module.

**A four-bottle cover lineup required bespoke, hand-rolled image work
outside the module system entirely** — this deck's cover isn't built
from `statement()` or any single module, because no existing cover
variant supports laying out four separate bottle images with generated
labels. Worth recording the real techniques that came out of it, since
they're reusable for the next "product lineup" cover:
- **Flag-filled country/region outlines** for the bottle labels: trace
  the real country boundary (same `shapely`/geo-data approach as
  `atlas()`'s locator inset), build an alpha mask from the traced
  polygon, and composite the national flag through that mask — not a
  flat color fill or a generic icon. A California-shaped label used
  the *USA* flag, not a California state flag, because the deck's
  convention was "one country flag per bottle" and Napa is a US
  region, not its own nation — a judgment call worth stating explicitly
  when the geographic subject doesn't map 1:1 to "country."
- **Curved-label "wrapped around the bottle" effect was tried and
  explicitly rejected** — a parabolic top/bottom edge looked like a
  bug (a stray white seam) rather than a subtle 3D cue, and the person
  asked to revert to flat rectangles. Recorded so it isn't
  re-attempted as a "would be nice" polish item without being asked.
- **Label edge-cleaning needs padding, not just erosion.** Background
  removal on a product photo can leave a bright anti-aliased fringe
  right at the image's own canvas edge — eroding the alpha mask alone
  can't fix this if the bright pixel sits on the very last row/column,
  because there's no room to erode *into*. The fix pads the canvas
  with transparent pixels on all sides *before* eroding, so the fade
  has somewhere to go. Confirmed by checking the specific pixel's alpha
  value before and after (255 → 26), not just re-rendering and eyeballing.
- **A corrupted source photo can look like a legitimate design
  choice.** One bottle photo had a hard-edged, ~94%-solid black
  rectangle baked into the file — first instinct was to read it as
  plausible dark packaging, which was wrong. Confirmed via
  connected-component fill-ratio and edge-hardness (a real photographic
  element has soft, organic edges and varies in density; this was a
  flat, sharp-edged, near-100%-fill block, touching the image border in
  a way no part of the actual bottle did). This is the same category of
  mistake as the Cava/Corpinnat session's black-band defect, still
  worth checking for on any product photo that looks visually "off"
  in a way that doesn't match the rest of the image.
- **Matte-paper shading should be a blurred/softened version of the
  bottle's own glass highlight, not a copy of it.** Sampling the raw
  brightness gradient from the glass and applying it directly to the
  label at the same intensity read as glossy — because glass has a
  sharp specular highlight and paper doesn't. Passing the sampled
  profile through a 1D Gaussian blur before using it as a shading
  overlay approximates the softer, more diffuse light falloff an
  actual matte surface would show.

**"Barossa Valley" was the wrong regional choice, and reworking it
touched far more than a find-and-replace.** The person caught, mid-deck,
that Barossa is known for Shiraz, not Cabernet — Coonawarra is the
actual Australian Cabernet benchmark region (terra rossa over
limestone, cooler maritime climate). Swapping the label text was the
easy part. The harder part: **every piece of *content* that had been
written to be true of Barossa specifically had to be re-verified, not
just relabeled** — the atlas marker needed real Coonawarra coordinates
(not Barossa's), the "how it's made" oak/extraction copy had grouped
Napa and Barossa together as the hot, heavy-extraction pair, but
Coonawarra's cooler climate actually puts it *with* Bordeaux's
restraint — the opposite grouping. Treating a regional swap as a
content problem, not just a label problem, is the actual lesson;
checking "does this claim still hold for the new subject" against
every paragraph that mentioned the old one is what real accuracy
requires here, not a global search-and-replace.

**A file-labeling mix-up recurred, caught the same way as before: by
actually opening and viewing the file, not trusting the order it was
uploaded in.** Two bottle photos arrived captioned "the last two
bottles for the shelf slide" and were saved under filenames guessed
from upload order; the images were actually a different pair than
assumed. Caught before it propagated by opening each saved file and
reading its own label text — the same discipline as the Cava/Corpinnat
session's Bordeaux-château mislabeling, and worth repeating as a
standing practice: **when a person uploads multiple files without
explicitly naming which is which, verify by viewing the content, not
by inferring from message order or prior context.**

---

## 11 · The Ridge Zinfandel Quick Sips session: a broken source asset,
## and losing an established template between sessions

This Quick Sips deck ("Ridge Zinfandel from Hot Sonoma") surfaced a
different category of problem than most of this document: not a
rendering bug in `core.py`/`modules.py`, but (a) a genuinely broken
binary asset that had been silently broken since before this session,
and (b) a demonstration that starting a new deck as one-off script
calls, instead of a real deck-definition file, actively loses
established conventions rather than just being less tidy.

**"Copy the file again" is not a fix if the file itself is broken.**
The Quick Sips wine-glass icon rendered as a solid white block. The
first response — re-copying `QS_glass_icon.png` from the project's
canonical location into the new deck's photo folder — did not fix it,
because *every copy of that file across the entire system* was the
same broken asset: plain RGB, zero alpha channel. The rendering code
does `Image.open(path).convert("RGBA")` and pastes using the image's
own alpha as the mask; converting a flat RGB image to RGBA just adds a
fully-opaque (255) alpha channel, so the *entire bounding box* pastes
as a solid rectangle showing whatever color sits there — exactly a
"white block." The actual fix required going to the asset's own cited
source (`_qs_glass()`'s docstring names it as "Lucide 'wine' icon,
ISC licensed"), fetching the real SVG from lucide.dev's own repo, and
rendering fresh PNGs with genuine transparency (verified: alpha range
0–255, not flat). **When a "missing" or "broken" asset turns out to
exist everywhere in the exact same broken state, the problem is the
asset, not its location — re-copying a broken file produces the same
broken file.**

**Building a new deck as one-off script invocations, instead of a real
deck-definition file matching the established template
(`quick_sips_volcanic_whites.py`), loses conventions that aren't
written down anywhere else.** The first pass at this deck's cover page
dropped the tasting-and-structure dashboard entirely, used an
`eyebrow` slot the reference deck doesn't use, and left every sizing
parameter (`body_size`, `lead_size`, `dashboard_gap`, `bottle_h`,
`cap_w`) at bare code defaults instead of the reference deck's tuned
values. None of these were things a person had said not to do — they
were just never written into a `SLIDES = [...]` file that mirrors the
one working example, so nothing forced a comparison against it.
Rebuilding as `quick_sips_ridge_zinfandel.py`, structured exactly like
the reference file (`PALETTE` override pattern, `SLIDES` list of
`(function, dict)` tuples), immediately surfaced the dashboard gap by
direct comparison. **The deck-definition-file convention isn't just
organizational tidiness — it's the actual mechanism that carries
forward conventions from one deck to the next; skipping it for "just a
couple of pages" script calls throws away everything the last deck
learned.**

**The Quick Sips tasting dashboard's row set is red/white-dependent,
and the difference is easy to lose track of by memory alone.** The
locked SOP is Sweetness → Acidity → Tannins (**red wines only** —
omit for whites/rosés) → Alcohol → Body → Aroma Intensity. The
volcanic whites reference deck correctly has no Tannin row (it's
white wine); a first pass at this red-wine deck's cover initially
had no dashboard at all, and once added, needed the *full* six-row
set including Tannin to match the SOP — easy to under-include by
pattern-matching against the one visible reference example (which
happens to be a white and thus has one fewer row) rather than the
actual written rule.

**Two new `quick_sips.py` capabilities, both gaps rather than bugs:**
`photo_caption` didn't exist on either `quick_sip_cover` or
`quick_sip_detail` — added to both, positioned bottom-right on the
cover specifically to avoid colliding with the left-aligned
title/tagline stack that already occupies the photo's bottom-left.
`content_pad` (the gap between a detail page's photo and its headline)
was hardcoded to 60px with no override — added as a slot parameter
after a request to "move the headline down a little."

**A factual correction changed the shape of a paragraph, not just a
word.** The person asked to credit Ridge's Monte Bello Cabernet with
"winning" the 1976 Judgment of Paris; that's not accurate — Stag's
Leap won the 1976 tasting outright, and Monte Bello placed *fifth*
that day. Monte Bello's real, well-documented "winner" moment is the
30th-anniversary rematch in 2006, where it topped both the London and
Napa panels by 18 points over second place. Surfaced this via a direct
search rather than either silently complying with the imprecise
framing or silently rewriting it without flagging the correction —
stated the correction plainly, then wrote the paragraph around the
*accurate* version of the claim.

**Burgundy lead-in highlighting is controlled by a word *count*
(`lead_words`), not by marking specific words — trimming it requires
knowing exactly which words are first, not just shortening the
sentence.** Two separate requests ("remove the highlighting from 'is
just as'" and "remove it from 'was'") were really requests to reduce
`para2_lead_words`/`body_lead_words` from a number that happened to
extend past the intended lead phrase down to the exact count that
stops at the right word — e.g. "Their Sonoma Zinfandel is just as"
(6 words highlighted) needed to become just "Their Sonoma Zinfandel"
(3 words) to stop the color at the right place. Fixing this required
counting the actual words in the lead phrase, not guessing at a
smaller number.

**The same paragraph-vs-bottle-lockup overlap bug from earlier
sessions recurred repeatedly within this one deck, and cutting a
*word* often isn't enough to clear it — cutting a full wrapped
*line* is what actually changes the rendered height.** Across several
rounds of copy edits on this deck's cover, trimming one or two words
from a paragraph sometimes left the reported overflow amount exactly
unchanged, because the wrap width absorbed the removed word without
dropping a line. The reliable fix each time was to directly measure
the actual wrapped line count via `core.wrap()` at the real rendering
size (not estimate it), identify how many lines needed to disappear,
and cut enough text to remove a *whole* line — the same discipline
already established in §1 and §9, still the correct approach and still
easy to skip under iteration pressure.
