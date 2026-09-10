# D1 Chapter Mastery Guide — Style Guide

**Status:** Chapters 1–5 locked and shipped as of this save-back. This document exists so a
future chat building Chapter 6 onward doesn't have to re-derive any of this through
iteration. Read this fully before writing new content or touching the engine.

**What this series is:** WSET Level 4 Diploma D1 (Viticulture), two-sided three-hole-punched
binder pages, one guide per textbook chapter. Each guide condenses its chapter to the
critical points, then closes with an exam-practice section (10 MCQ + answer key, 2 short
written answer questions with Distinction-standard model answers).

---

## 1. File architecture

```
mastery.py       — the layout engine: fonts, colours, page geometry, paragraph styles,
                    EXHIBIT/CALLOUT/FlowChart/H1-H4 builders, the widow-prevention system,
                    PDF assembly (build())
graphics.py      — the bespoke diagram library (14 Flowable classes) plus botanical drawing
                    primitives; imports from mastery.py
examkit.py       — mcq_section(), swa_section(), exam_traps(), answer_head(), examiner_note()
mindmap.py       — the Content Mind Map Summary engine: one landscape page per chapter,
                    hub -> branch -> sub -> twig as a real branching tree, closing the chapter
                    immediately before its practice test. Imports mastery.py's actual fonts
                    and colour/line-weight tokens directly (not a separate copy), so it can
                    never visually drift from the rest of the guide. Standard starting Chapter
                    Eleven — see §10 and mastery.build()'s mindmap= parameter
mindmaps/        — one content_chN.py per chapter: the Node-tree data (hub label, branches,
                    subs, twigs, cross-links, optional inset) that mindmap.py renders. Kept
                    separate from chN.py itself so the mind map's content can be reviewed and
                    cross-checked against the locked chapter body independently
qa_orphans.py    — text-based orphaned-heading scan (fast, coarse — use qa_widows.py for the
                    real check)
qa_widows.py     — font-aware widow/four-line-rule scan; this is the one that actually
                    matters, see §8
ch1.py … ch10.py — one file per chapter, each a flat sequence of s.append(...) calls building
                    the body, followed by MCQ/q1/q2 lists and calls into examkit
```

All files are flat at project root — no subfolders, aside from `fonts/` (regenerated font
files, see §2) and `mindmaps/` (mind-map content, above). A new chapter is a new `ch11.py`
living alongside these. **Copy `ch10.py` as your starting template** — it's the most recently
built and carries every convention below already applied. Don't start a chapter from a blank
file; you will silently drop conventions that live only in the reference chapters (this
happened before in the sibling wine-deck project and is why this rule exists).

---

## 2. Fonts — regenerate every session, never persisted

Static font files (`fonts/Serif-Semi.ttf`, `Serif-Bold.ttf`, `Sans-Reg.ttf`, `Sans-Bold.ttf`,
`Sans-Ital.ttf`) are instanced from three variable-font source files fetched from Google
Fonts. **Nothing font-related is stored in this save-back** — same convention as every other
project in this account. Run this at the start of any session that renders a guide:

```python
import os, subprocess
os.makedirs("fonts", exist_ok=True)
raw = {
  "fonts/raw_PlayfairDisplay%5Bwght%5D.ttf":
    "https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
  "fonts/raw_Archivo%5Bwdth,wght%5D.ttf":
    "https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/Archivo%5Bwdth,wght%5D.ttf",
  "fonts/raw_ArchivoItalic.ttf":
    "https://raw.githubusercontent.com/google/fonts/main/ofl/archivo/Archivo-Italic%5Bwdth,wght%5D.ttf",
}
for path, url in raw.items():
    subprocess.run(["curl", "-s", "-o", path, url], check=True)

from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib import TTFont

jobs = [
    ("fonts/raw_PlayfairDisplay%5Bwght%5D.ttf", {"wght": 600}, "fonts/Serif-Semi.ttf"),
    ("fonts/raw_PlayfairDisplay%5Bwght%5D.ttf", {"wght": 700}, "fonts/Serif-Bold.ttf"),
    ("fonts/raw_Archivo%5Bwdth,wght%5D.ttf", {"wght": 400, "wdth": 100}, "fonts/Sans-Reg.ttf"),
    ("fonts/raw_Archivo%5Bwdth,wght%5D.ttf", {"wght": 700, "wdth": 100}, "fonts/Sans-Bold.ttf"),
    ("fonts/raw_ArchivoItalic.ttf", {"wght": 400, "wdth": 100}, "fonts/Sans-Ital.ttf"),
]
for src, axes, out in jobs:
    f = TTFont(src)
    instantiateVariableFont(f, axes, inplace=True)
    f.save(out)
```

These exact weight/width values were verified against the working font set for this
save-back (byte-identical on 4 of 5 outputs; the fifth, Sans-Bold, is functionally identical
at wght=700 — a few bytes differ only from fontTools-version table ordering). Don't guess
different values.

`mastery.py` registers these five as ReportLab font names: `Serif`, `Serif-B`, `Sans`,
`Sans-B`, `Sans-I`. Headings use `Serif`/`Serif-B` (Playfair Display). Everything else uses
`Sans`/`Sans-B`/`Sans-I` (Archivo).

---

## 3. Colour palette — one accent, one secondary, disciplined neutrals

```python
INK       = "#16161A"   # body text
BURGUNDY  = "#6E2B36"   # the single accent — section numerals, sub-heading labels, table
                         #   row-label column, callout accent rules (default)
GOLD      = "#8A6A2C"   # the single secondary — exhibit/figure captions, callout accent
                         #   (when distinguishing from BURGUNDY), gold markers in diagrams
SLATE     = "#5A5D63"   # secondary text — H1 subtitle, note-style paragraphs
MUTE      = "#8B8E93"   # tertiary — axis labels, muted annotations inside diagrams
HAIRLINE  = "#C6C8CB"   # dividers, leader lines
FEINT     = "#E6E4E0"   # row rules inside exhibit tables
BOXFILL   = "#F7F5F1"   # callout panel tint (gold-accented callouts)
BANDFILL  = "#F0ECE4"   # flow chart box tint
BOXEDGE   = "#DED8CD"   # (legacy — rarely used now that tables are rule-only)
```

**Do not introduce new named colours for new chapters.** If a diagram needs a sequential
ramp (temperature, climate bands, anything ordered low→high), use the existing ramp in
`graphics.py`:

```python
COOL = "#4E6E8C"   MILD = "#6F8A6B"   LEAF = "#7E9463"   WARM = "#BE8B45"   HOT = "#A6462F"
```

This ramp is reserved for genuinely ordered/sequential data (temperature scales, climate
bands). Don't use it decoratively.

**Line weights** — three only, named constants in `mastery.py`:
```python
LINE_HAIR = 0.3   # leader lines, fine dividers inside diagrams
LINE_RULE = 0.6   # standard rules (under exhibit headers, hairlines)
LINE_BOLD = 1.1   # table top/bottom rules, accent marks
```

---

## 4. Page geometry

- US Letter, portrait, mirrored two-column layout for two-sided binding: odd pages have the
  ruled notes column on the **right**, even pages on the **left**. `BIND` margin (punched
  edge) = 54pt, `OUTER` margin (free edge) = 40pt.
- Body pages: content column `L_W` = 336pt + notes column `N_W` = 158pt.
- Exam pages: full width `FULL_W` = 518pt, no notes column (a separate flow, merged in via
  `build()`'s `exam` parameter — see any `ch#.py`'s tail for the pattern).
- **Page budget: 18 pages hard default (`maxpages=18` in `build()`), extendable to 19 if a
  chapter genuinely needs it** (Chapter 3 — the longest — ships at 18; this was fought for
  hard through several rounds of trimming rather than raised casually). Do not raise the cap
  as a first resort. If a new chapter is running long: cut lower-yield examples first, then
  fold a short sub-section under an adjacent one, then — only if still over — ask before
  raising the cap.
- Typical split is roughly 60–65% body pages to 35–40% exam pages.

---

## 5. Typography scale

| Style | Font | Size / leading | Use |
|---|---|---|---|
| `h1` | Serif-B | 18 / 20.6 | Chapter title (once per guide) |
| `h1sub` | Sans, Slate | 10 / 13 | Chapter subtitle line under the title |
| `h2` | Serif-B | ~13.5 | Numbered sections ("1. Species") |
| `h3` | Serif-B | smaller | Sub-sections within a numbered section |
| `h4` | Sans-B, tracked caps | ~9.6–10.6 | Minor headings inside a section |
| `body` | Sans | 10 / 13.5 | Standard paragraph text |
| `note` | Sans, Slate | 10 / 13.5 | Explanatory asides — same size as body, distinguished by
colour only |
| `bullet` | Sans | 10 / 13.2 | List items |
| `tbl` / `tblh` / `tbll` | Sans / Sans-B / Sans-B | 9 / ~12.2 | Exhibit table body / header
caps / row-label column (Burgundy) |
| caption (`CapRule`) | Sans-B, tracked, Gold | 7.0 | "EXHIBIT X.X — ..." / "FIGURE X.X — ..."
labels |

**Type floor is enforced.** Never shrink body text below 10pt or table text below 9pt to fit
content — cut copy instead. This is a hard rule carried from the sibling deck project and
applies here too.

---

## 6. The spacing system — GAP, and the heading exemption

**`GAP = 30.0` (exactly 40px: 40÷96×72).** This is the *only* spacing value used anywhere in
the system, applied as `spaceBefore` on:
- every section heading (H2/H3/H4 — all the same value, not tiered)
- every exhibit table (via its `CapRule` caption, or directly on the table when the caption
  is embedded as a repeating row — see §7)
- every callout panel
- every graphic device (`FlowChart`, `ThresholdScale`, `Matrix2x2`, etc.) when used standalone

**The exemption — content that directly follows a heading gets normal line spacing, not
GAP.** A heading followed immediately by its own exhibit/figure/callout should sit tight
against it, not have a 40px gap wedged in. This is handled automatically by
`_degap_heading_adjacent()` in `mastery.py`, which runs right after content is flattened and
right before widow-prevention grouping: it walks the page in order and zeroes the
`spaceBefore` of anything that immediately follows a heading. **You don't need to do anything
manually for this** — just write `s.append(H2(...))` followed directly by
`s.append(EXHIBIT(...))` or `s.append(FIGURE(...))` and the engine handles the tight spacing.
The GAP only survives where something *other than a heading* precedes the next block.

**Do not add manual `SP(n)` spacer calls between sections, exhibits, or graphics.** The whole
point of this system is that GAP is the single source of truth. A leftover manual spacer
will stack on top of GAP (spacers are additive, not collapsible, unlike `spaceBefore` which
collapses to the larger of adjacent values) and break the "exactly 40px" guarantee. Small
`SP(n)` calls (1.5–4pt) are still fine *inside* a figure/exhibit for tight internal spacing
(e.g. between a caption and its diagram) — those are not section-level gaps.

If a future revision needs a different GAP value, change the one constant in `mastery.py`
and rebuild — do not hand-tune individual `spaceBefore` values.

---

## 7. Never orphan a heading — the four-line rule

**Standing rule: any heading, exhibit caption, or figure caption must have at least four
lines of real content following it on the same page, or it moves to the next page as a
unit.** This is enforced by `_group_headings()` in `mastery.py`, which runs after
`_degap_heading_adjacent()`. Mechanics, if you need to touch this code:

- Anything with `keepWithNext=1` (H1–H4 headings and `CapRule` captions) triggers grouping.
  It gathers forward until 4 lines of content are captured or a hard break is hit.
- **Short groups** (under ~250pt total) get wrapped in a plain `KeepTogether` — simple,
  reliable, moves the whole small group together if it doesn't fit.
- **Tall groups** get a `CondPageBreak` sized to just the heading + minimum content, *not*
  the whole group — this lets a splittable table start on the current page and flow onto the
  next rather than jumping the entire table as one block and stranding a large gap. Whether a
  table can honour this partial reservation depends on `EXHIBIT(..., keep=False)` — see §8.

**The one real gotcha here, if you extend this code:** `CapRule` (the caption flowable used
by both exhibits and figures) also carries `keepWithNext=1`, so *every* exhibit/figure
caption independently triggers this grouping logic, not just chapter headings. This is
intentional (a caption should never be orphaned from its own table/diagram either) but it
means the grouping pass runs far more often than you'd expect from reading only the H1–H4
code. If you see an unexplained page-end gap, check whether a nearby `CapRule`-headed group
is being forced into a full `KeepTogether` instead of the partial-reservation path — this was
a real bug found and fixed during this build (the fix: allowing exhibit tables to declare
`keep=False` so they're recognized as splittable and get the smarter reservation).

**Run `qa_widows.py` before shipping any chapter — every time, no exceptions.** It is
font-aware (reads actual typeface/size/position via pdfminer, not just text order), so it
correctly distinguishes a real section heading from a diagram's internal label. `qa_orphans.py`
is an older, cruder text-based version kept for a fast first pass; it is not a substitute for
`qa_widows.py`. A chapter is not done until both report clean.

---

## 8. Exhibits, callouts, and when to use which

### EXHIBIT — a Swiss rule-only data table
```python
s.append(EXHIBIT("EXHIBIT 3.1 — TEMPERATURE THROUGH THE GROWTH CYCLE", [
    ["Stage", "Effect"],
    ["Winter", "Below <b>10°C / 50°F</b> ensures dormancy..."],
    ...
], [76, W - 76], keep=False))
```
- No vertical rules, no cell fills. Bold rule above headers, fine rule below, feint rules
  between data rows, bold rule closing the table — this is the whole visual language, don't
  add borders or shading.
- `keep=True` (default): small tables (2–4 rows) that should stay visually whole. Caption is
  a separate `CapRule` flowable above the table.
- `keep=False`: tables with enough rows that forcing them whole risks a large page-end gap.
  The caption is embedded as a repeating first row instead of a separate flowable, so it
  reappears if the table splits across a page boundary. **Use `keep=False` on any exhibit
  with 5+ rows or noticeably long cells** — this is the single biggest lever for avoiding
  wasted page space, learned the hard way this session.
- First column width is typically a fixed pixel value (label column); remaining columns
  split the rest of `W` (`L_W` inside body pages).

### CALLOUT — a tinted panel with an accent rule
```python
s.append(CALLOUT("DISTINCTION DIFFERENTIATORS — CHAPTER THREE", [
    P("<b>1. ...</b> ...", "box"),
    ...
]))
```
- Used for: Distinction Differentiators (5 items, every chapter, standard closing callout),
  Exam Traps (5 items, via `examkit.exam_traps()`), and one-off analytical asides ("THE
  ANALYTICAL POINT THIS SECTION EXISTS TO MAKE", "THE CLAIM THE TEXTBOOK EXPLICITLY DECLINES
  TO MAKE" — name these to state the *point*, not just the topic).
- No outer border — the tint alone separates it from the page. Default accent is Gold;
  Exam Traps uses Burgundy (see `examkit.py`).

### FlowChart — a vertical sequence of tinted boxes with connectors
Use for genuine linear processes (cross fertilisation → seeds → assessment → registration →
propagation; sufficient water → lack of water → consequence). Not a general-purpose list
substitute — if the items aren't sequential/causal, use `BUL()` instead.

### FIGURE(label, diagram, note=None) — caption + bespoke graphic
Wraps any `graphics.py` device with a `CapRule` caption and optional footnote paragraph. See
§9 for the full device catalogue.

---

## 9. The graphics library — what each device is for

All in `graphics.py`. Import what you need into a new chapter file; don't duplicate drawing
code. Some of these are so specific to viticulture (the vine, the berry) that a new chapter
is unlikely to reuse them directly — but treat the *botanical drawing primitives*
(`_vine_leaf`, `_bunch`, `_roots`, `_arm`, `_taper`, `_seed`) as a reusable toolkit if a
future chapter needs another plant-anatomy illustration.

| Device | Use for | Do not use for |
|---|---|---|
| `ThresholdScale` | A single numeric axis with coloured bands and labelled threshold markers (temperature ranges, climate bands) | Two independent variables — use `Matrix2x2` |
| `RangeCompare` | Several optimum *windows* stacked on one shared axis, to show they don't coincide | A single range — use `ThresholdScale` |
| `CycleWheel` | An annual/cyclical process, with directional chevrons | A one-way linear process — use `FlowChart` |
| `Matrix2x2` | Two genuinely independent axes crossing to produce four distinct outcomes (site selection: price × climate; rootstock: vigour × site) | A simple pro/con list — that's a two-column `EXHIBIT` |
| `InclusionRings` | Strictly nested categories (A contains B contains C) — concentric rings, leader-line labels | Partial overlap between categories — that's a genuine Venn relationship, which this library does not currently implement (the old `Venn` class exists but is unused/deprecated; nested rings and `LineageChart` proved better for every real case encountered) |
| `LineageChart` | Two-lane parentage/boundary relationships (cross vs hybrid: same lane or crosses lanes) | General comparison — use `Matrix2x2` or an `EXHIBIT` |
| `BarChart` | Simple ranked numeric comparison across several items | Two-axis comparison — use `Matrix2x2` |
| `SlopeDiagram`, `TextureTriangle` | One-off bespoke illustrations for this specific content (aspect/sun angle; soil texture ternary) | — |
| `BerrySection`, `VineSchematic` | Botanical cross-sections, built from the reusable drawing primitives | — |
| `PlanningRules` | Ruled space that expands to fill whatever's left on an SWA question page | Anywhere else — it's a single-purpose device for `examkit.py`'s `swa_section()` |

**Before adding a new diagram class, check this table for a device that already fits.** Most
comparison needs map onto `Matrix2x2` or a plain `EXHIBIT`; most single-axis numeric needs map
onto `ThresholdScale`. New bespoke classes should follow the existing pattern: default
`spaceBefore = GAP` in `__init__` (for standalone use), reuse the shared type scale
(`G_LABEL`/`G_VALUE`/`G_NOTE` constants), reuse `tracked()`/`tracked_w()` for any letterspaced
text, and reuse the established line-weight constants (§3) rather than picking new ones.

---

## 10. Content structure — the pattern every chapter follows

1. **`H1(title, subtitle)`** — chapter title, subtitle names the WSET unit sections covered
   (e.g. "3.1 Dormancy → 3.6 Other Changes in the Vine").
2. **Two summary paragraphs** — no more, no fewer. First: what this chapter is and why it
   matters relative to the rest of D1 (its "load-bearing" role, how it's typically examined).
   Second: what's *reliably* examined — name the specific constructions the exam favours.
   These are the only place besides model answers where extended prose is expected; **cut
   copy in these paragraphs harder than anywhere else in the chapter, since they set the
   reader's expectation for the whole guide's register.**
3. **Numbered `H2` sections** following the WSET unit's own structure. Each section is
   built from `EXHIBIT`, `FIGURE`, `BUL()` lists, and short `P(..., "note")` asides — prose
   paragraphs are the exception inside a section, not the default. If you're writing more
   than 2–3 sentences of flowing prose inside a numbered section, stop and ask whether it
   should be a list, exhibit, or diagram instead.
4. **Closing callouts, every chapter, same order:**
   - `CALLOUT("DISTINCTION DIFFERENTIATORS — CHAPTER N", [...])` — exactly 5 items, each a
     numbered, named principle with a concrete example. These are meta-level exam strategy
     ("derive the mechanism before naming the example," "name the transport tissue"), not
     more content recap.
   - `exam_traps([...])` — exactly 5 items, each `("Wrong claim.", "The correction, with the
     right figure or distinction.")`.
5. **Content Mind Map Summary — standard starting Chapter Eleven.** One landscape page,
   built via `mindmap.py` from that chapter's `mindmaps/content_chN.py`, inserted via
   `mastery.build(..., mindmap="path/to/rendered_page.pdf")` between the closing callouts
   and the practice test — hence its position here, between steps 4 and 6. Not a second
   pass at writing the chapter: the mind map's content should be checked against what's
   already locked in that same `chN.py`, not re-derived independently from the source
   textbook, so the summary and the body can never quietly disagree. Chapters One through
   Ten predate this convention and are not required to add one retroactively.
6. **`mcq_section(MCQ)`** — 10 questions. Diagnostic only (the real D1 paper has no MCQ,
   state this once per guide in the exam intro — see `examkit.py`). Each has 4 options, a
   0-indexed `ans`, and a `why=` rationale that names *why the distractors are wrong*, not
   just why the answer is right.
7. **`swa_section([q1, q2])`** — 2 short written answer questions, each with 2 parts and
   stated percentage weights that sum and get framed as "your share of the 90 minutes" (see
   `examkit.py`'s total-percentage logic). Each question gets a full Distinction-standard
   model answer via `answer_head()` + `P()` paragraphs, closing with `examiner_note([...])`
   — 2 short paragraphs naming *what specifically* makes the answer Distinction-level, not a
   generic "well done."

**Never reference chapter numbers, unit numbers, or "the textbook" in the copy itself.**
Write as though explaining the material directly. This applies throughout — body content,
exhibits, callouts, model answers.

---

## 11. Editorial voice — brevity without losing meaning

**The standing rule, carried through every locked chapter: never use ten words if five will
do.** In practice this means, in descending order of how hard to enforce:

- **Model answers** get real scrutiny but a lighter touch than everything else — they exist
  to demonstrate full Distinction-level essay technique (signposting, cause-and-effect,
  named evidence), so don't compress them into fragments. Cut connective filler ("it is
  important to note that," "the reason for this is") and redundant restatement, but preserve
  full sentences and the complete analytical arc.
- **Body content, exhibit cells, MCQ rationales, callouts** — no mercy. Every one of these
  went through a dedicated line-by-line trim pass on this save-back. Redundant lead-ins
  ("The wine species. Over 1,000 varieties..." → "Over 1,000 varieties..."), padded
  connectives ("so the technique can increase disease spread" → "increasing disease spread"),
  doubled words, and stacked hedges are the recurring patterns to watch for.
- Exhibit cells specifically: aim for phrase fragments, not full sentences, wherever the
  table structure already supplies the grammar (row label + column header = implied subject
  and verb).

**Source discipline:** the D1 textbook is the sole permitted source for content. Don't
supplement from outside material, even to fill a thin section — thinness is better than
drift from the syllabus.

---

## 12. Known minor issues (not fixed — guides are locked)

- `ch2.py` has a duplicate exhibit label — two tables are both numbered "EXHIBIT 2.7"
  (should be 2.7 and 2.8). Cosmetic only, left as-is per the lock. Fix in a future revision
  if you're touching that file anyway, but it doesn't warrant reopening a locked guide on
  its own.
- The old `Venn` class in `graphics.py` is unused (superseded by `InclusionRings` and
  `LineageChart` for every case that came up). Left in place in case a genuine partial-overlap
  relationship arises in a future chapter, but don't reach for it by default — it's visually
  weaker than the two devices that replaced it.

---

## 13. Building a new chapter — checklist

1. Copy `ch10.py` to `ch11.py` as your starting structure.
2. Regenerate fonts (§2) if starting a fresh session.
3. Extract the relevant textbook chapter to plain text; work section by section against the
   WSET unit's own structure.
4. Write the two-paragraph opening summary last, once you know what the chapter actually
   emphasizes.
5. Build each section as exhibit/list/diagram first, prose only where genuinely necessary
   (§10.3).
6. Pick graphics from §9's table before inventing a new device.
7. Write Distinction Differentiators (5) and Exam Traps (5) per §10.4.
8. Build the Content Mind Map Summary (`mindmaps/content_ch11.py` + `mindmap.py`) per §10.5
   — check it against the chapter body you just locked, not the source textbook independently.
   Render it to its own single-page PDF first and spot-check it alone before wiring it into
   the full chapter build.
9. Build MCQ (10) and SWA (2, with model answers + examiner notes) per §10.6–10.7.
10. `python3 ch11.py`, passing the rendered mind-map page to `build(..., mindmap=...)` — check
    the page count against your target (§4); a chapter carrying a mind map should budget one
    extra page over what it would otherwise need.
11. Run **both** `qa_orphans.py` and `qa_widows.py` against the output PDF. Fix until both
    report clean. Neither one checks the mind-map page — it doesn't flow text the way the
    rest of the guide does, so its own QA is a visual label-overlap check instead: verify
    every sub/twig line is fully enclosed in its panel and no cross-link label sits on top of
    another element, since it's a fixed-position layout rather than reflowing text.
12. Visual spot-check: render a few pages to image and eyeball spacing, table splits, and
    diagram legibility — the QA scripts catch structural problems, not aesthetic ones.
13. Save back into the project (this file, plus the updated chapter `.py` files — see the
    accompanying README for what to replace vs. add).
