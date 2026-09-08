# D1 Chapter Mastery Guide — Changelog

## v1 — first locked release, Chapters 1–5

Full build-out across one extended session, then five further passes of iteration per
explicit direction. Documented here in the order it happened, since the reasoning behind
several decisions matters for anyone extending this later.

### Build 1 — layout engine and Chapters 1–5, first draft
- `mastery.py` built from scratch: US Letter, mirrored two-column notes layout for two-sided
  binding, custom Flowable-based heading/exhibit/callout system.
- Six chapters drafted (Chapter 3 initially split into two volumes — Temperature/Sunlight/
  Water and Nutrients/Soil/Climate — because at the original type size 24 combined pages
  didn't fit).
- QA scripts (`qa_orphans.py`) written to catch orphaned headings.

### Pass 2 — condense for brevity
- Every chapter rewritten from flowing prose into lists, exhibits and flow charts, with
  prose retained only for two opening summary paragraphs per chapter and the SWA model
  answers.
- Condensing was aggressive enough that Chapter 3's two volumes collapsed back into one
  18-page file — the two-volume split was no longer needed.

### Pass 3 — graphics pass: creative devices beyond tables
- Nine new diagram device types added to a new `graphics.py`: `ThresholdScale`, `RangeCompare`,
  `CycleWheel`, `Venn` (later superseded), `BarChart`, `SlopeDiagram`, `TextureTriangle`,
  `Matrix2x2`, and the first botanical illustrations (`VineSchematic`, `BerrySection`).

### Pass 4 — Vignelli/Ive design pass
- Typography and colour system overhauled: single accent (Burgundy) + single secondary
  (Gold), three disciplined line weights, exhibit tables rebuilt as rule-only Swiss-style
  tables (no fills, no vertical rules), letterspaced `CapRule` caption system shared by every
  exhibit and figure.
- Botanical illustrations substantially reworked — the vine and grape-leaf geometry went
  through several complete rebuilds (see "Leaf geometry" below).

### Pass 5 — vertical rhythm: three blank rows between sections
- First version of a standardized section-gap rule, applied as `spaceBefore` tiered by
  heading level.
- **Bug found and fixed:** a `CondPageBreak`/`KeepTogether` grouping bug where exhibit
  captions (which independently carry `keepWithNext=1`) were forcing entire tall groups into
  monolithic `KeepTogether` blocks instead of the smarter partial-reservation path, causing
  large unexplained gaps at page ends. Fixed by lowering the group-size threshold that
  decides which path a group takes, and by teaching `EXHIBIT(..., keep=False)` tables to
  declare themselves splittable so the reservation logic recognizes them correctly.
- **Font-aware widow checker built** (`qa_widows.py`) — the original `qa_orphans.py` worked
  on raw extracted text and couldn't distinguish a real section heading from a diagram's
  internal label. The new script reads actual font, size and position via pdfminer, correctly
  identifying headings by typeface/size/case rather than content, and was verified against a
  negative control (rule disabled) to confirm it actually fires on real violations.

### Pass 6 — leaf geometry, grounded in real Cabernet Sauvignon morphology
- Web research established the defining trait: a closed, overlapping petiolar sinus and
  narrow overlapping lateral sinuses (the "mask" look ampelographers name the variety for).
- Several complete geometry rewrites followed, each diagnosed by rendering in isolation
  before moving on:
  1. First attempt used a flat `smoothstep` plateau per lobe — produced a "clover" shape
     (lobes read as rounded squares, not tapering points).
  2. A cosine-union petal formula fixed the taper but the base gap (petiole attachment)
     read as a deep, spiky notch rather than a closed sinus.
  3. **Final structure:** the leaf is a true five-segment *closed loop* (not four lobes plus
     a separate petiole gap) — the petiolar sinus is simply the fifth gap in the rosette,
     which is what makes it read as closed/overlapping rather than an open wedge. This is
     the version shipped.
- The vine diagram itself was shrunk twice more per explicit direction (final: 188pt tall,
  six shoots, proportionally smaller cordons and bunches).

### Pass 7 — spacing standardized to an exact pixel value, twice revised
- 80px (60pt) requested, then reduced to 40px (30pt) — both converted precisely (px÷96×72),
  not approximated.
- **Structural change, not just a number change:** the gap was made conditional on what
  precedes each element. A new pass, `_degap_heading_adjacent()`, runs after content
  flattening and before widow-prevention grouping, zeroing the `spaceBefore` of anything
  that directly follows a heading — so a heading and its own first exhibit/figure sit at
  normal line spacing, while genuine section-to-section transitions get the full gap. This
  required removing every leftover manual `Spacer` call that would otherwise stack
  (additively, since Spacers don't participate in ReportLab's spaceBefore/spaceAfter
  collapsing) on top of the new single-source gap.

### Pass 8 — Venn diagrams replaced
- The original `Venn` device read as large and visually flat. Replaced with two new,
  purpose-built devices:
  - `InclusionRings` — concentric rings for genuinely nested categories (Sustainable ⊃
    Organic ⊃ Biodynamic), reusing the leader-line annotation style already established by
    the botanical diagrams so the whole set reads as one system.
  - `LineageChart` — two-lane parentage diagrams (cross vs hybrid), far more compact than
    the circles it replaced.
- Two new `Matrix2x2` uses added where a genuine two-axis relationship existed (water stress
  by timing × severity in Chapter 3; vine quality by age × site condition in Chapter 5).

### Pass 9 — full editorial brevity pass, three rounds
1. Model answers and body content tightened chapter by chapter — heaviest cuts in the two
   model answers per chapter, since they carry the most prose volume; lighter touch than
   body content to preserve full Distinction-level essay structure.
2. MCQ rationales and exhibit-cell text reviewed specifically (the gap flagged after round 1).
3. **Every exhibit cell in all five chapters reviewed line by line** for further word-count
   trims — redundant lead-ins, padded connectives, doubled words. Page counts held exactly
   (exhibits were already dense enough that word-level trims moved bytes, not layout).

### Final state
Ch1 15 pages · Ch2 16 · Ch3 18 · Ch4 15 · Ch5 14. Both QA scripts clean on all five. Chapters
locked; this save-back follows.

## Known issues carried forward (see style guide §12)
- `ch2.py` duplicate "EXHIBIT 2.7" label (cosmetic).
- `Venn` class unused but retained in `graphics.py`.
