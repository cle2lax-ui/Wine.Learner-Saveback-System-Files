# Reels Spec — v2

A distribution treatment, not a series. Two per week, assembled from
arc content already built and already reviewed.

**v2 supersedes v1 as of Arc 1 week two's Three Ways reel.** v1's
governing idea was restraint: a slow scale on a still, hard cuts only,
motion capped deliberately low because the format was new and
unproven. Two builds in (whole-bunch Split Decision, then a duration
extension on the same file) showed the format holds up under more
than that — Steve's ask for "more polished and glossy editing, with
animation of graphic elements" on Three Ways is the point v1's ceiling
started actively working against the content rather than protecting
it. v2 raises that ceiling. It does not lower the bar on anything else
below.

---

## What v1 got right and v2 keeps

- **1080 × 1920, 9:16.** Vertical content is re-composed on this canvas
  from source content. Still never cropped from the 2160×2700 (4:5)
  slide render — that crop discards roughly 40% of the frame and cuts
  through type. Any module used for Reels still needs a vertical
  layout mode of its own.
- **Frame 1 carries the complete hook** — legible in the first 0.5s, no
  build-up, no title card.
- **Final frame closes the loop** back to frame 1 so the replay reads
  as continuous. This got harder to satisfy as beats gained animated
  elements (a progress strip has to visibly *complete*, not just
  match frame 1's static content) — see the Motion section below.
  Still non-negotiable.
- **Silent-legible throughout.** Assume sound off, always. Animated
  supers make this easier to hit, not harder, if built right — see
  below.
- **Hard cuts between beats.** This is the one piece of v1's "no
  transitions" rule that survives unchanged. What happens *inside* a
  beat can now move; what happens *between* beats still can't cross-
  fade, wipe, or otherwise blend. A hard cut is still what makes five
  beats read as five distinct claims rather than one continuous shot.
- **Audio left empty at export.** Trending audio is selected and
  attached at upload — it cannot be chosen days in advance and stay
  current. Unchanged.

---

## What v2 changes

### Duration: 20 seconds, five beats at ~4 seconds

v1 specified 15–18s at ~3s/beat. Both Reels built so far ran 4s/beat
(20s total) on Steve's explicit call, on the grounds that 3 seconds is
tight for the amount of type a beat now carries — and that was before
v2's animated supers and stat bars added more per-beat content, not
less. 20s / 4s-per-beat is the new default. Treat anything shorter as
a deliberate exception to justify in that file's own docstring, not
the other way around.

### Motion: animated graphic elements, not just a scale on a still

v1: "Motion, if any, is a slow scale on a still — not animation."
v2 replaces this with three sanctioned categories of in-beat motion,
in addition to the still scale (which remains fine, and remains the
default for any beat that doesn't need more):

1. **A persistent progress element.** Where a Reel covers N discrete
   things (regions, poles of an argument, steps in a sequence), a
   small fixed UI element — a node strip, a fill bar, a counter —
   tracks position through the sequence across the whole Reel, not
   just within one beat. It updates once per beat (a node lights up,
   a bar extends) rather than animating continuously, so it reads
   clearly even to someone who glances in mid-beat. This is the
   element principally responsible for the loop-close requirement now
   needing more than a matched photo: the progress element has to
   visibly *complete* on the closing beat, in step with frame 1's
   *empty* state, for the loop to read as continuous rather than reset.

2. **Animated stat callouts.** A bar filling, a number counting up,
   drawn over roughly the first 1–1.5s of the beat it belongs to, then
   holding static for the remainder. Values and the visual language
   (a left-to-right fill bar) should match the same numbers' treatment
   in that week's static decks where the two overlap — a viewer who's
   seen both should recognize the system, not learn two.

3. **Supers that move, not sit.** Text overlays slide and fade in
   (~0.4s) at the start of their window and fade out (~0.3s) before
   the hard cut, rather than appearing at full opacity for the full
   beat and disappearing on the cut. This is the single change most
   responsible for the "polished" read Steve asked for — static supers
   over a moving photo is what every v1 Reel looked like; supers with
   their own motion is what a v2 Reel looks like.

None of these three are required on every beat of every Reel. A Reel
built from a two-pole argument (a Split Decision) may only need
category 3. A Reel built from a numbered sequence (Three Ways, a
ranked list) is the natural home for categories 1 and 2 together.
Match the device to what the content actually has structure in —
don't add a progress strip to a Reel with nothing sequential to track.

### Visual treatment: a consistent grade across sourced photos

v1 didn't address this because it didn't need to — one Reel, one
source photo set, shot consistently enough not to need reconciling.
Three Ways pulls from three different photographers across two
Commons categories of very different quality and colour temperature.
v2 calls for a light, consistent treatment across every photo in a
single Reel — a unifying colour grade and a shared vignette
treatment — applied uniformly, not photo-by-photo to taste, so a cut
between a crisp modern DSLR frame and a flatter older upload doesn't
read as a quality drop mid-Reel. This is a real, applied, and
inspectable step, not a suggestion to "make it look nice" — verify it
by comparing before/after frames from each source photo side by side,
the same way every other visual claim in this project gets verified
before being called done.

---

## Source formats

FFFA and Split Decision still cut best on structure — both are already
beat-structured. Three Ways is now a confirmed third: N discrete
things (2–4) map close to 1:1 onto hook / thing / thing / thing / close,
often more cleanly than Split Decision's two-pole shape, which needs an
explicit "turn" beat to avoid feeling like two disconnected halves.
Field Guide still cuts poorly — 12 slides of dense argument does not
compress to 20 seconds without becoming a slideshow of headlines, v2's
extra motion budget doesn't change that math.

---

## Still open

- No Reel yet under v2 has shipped. This file is written ahead of that
  build, not after it — treat the categories above as the direction to
  build toward, and update this file again if the first v2 build
  surfaces something that doesn't hold up in practice, the same way
  the 20-second duration got promoted from "exception noted in a
  docstring" to "the default" only after two builds confirmed it.
- The progress-strip / loop-close interaction (see category 1 above)
  is a real design problem, not a solved one — first v2 build should
  treat it as the thing most likely to need a second pass.
