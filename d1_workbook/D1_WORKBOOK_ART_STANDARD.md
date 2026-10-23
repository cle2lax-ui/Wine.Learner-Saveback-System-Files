# D1 Workbook — Art Standard

Every drawing in the workbook is built with `wb_ink.py` so the whole book shares one hand.
This file is the rulebook. Read it before drawing anything new.

## Reference

Botanical figures from Lodi Grape Growers (grape flower: closed bud, cap lifting, open flower with
stamens, cutaway ovary with pollen tube, embryo sac and eggs). The goal is that a student could not
tell where one workbook drawing ends and another begins — and that each one looks like a finished
textbook illustration, not a diagram.

## The look, in six rules

1. **Inked outline on every form.** Dark, slightly heavy (1.2–1.9 pt), round joins and caps.
   Olive-black on greens (`INK_G`), warm brown on yellows (`INK_Y`), dark brown on wood (`INK_W`),
   near-black plum on fruit (`INK_P`). Never a mid-grey or coloured stroke.
2. **Soft gradient fills, never flat.** A pale yellow-green light spot upper-left falling to a deep
   green shadow at the opposite edge (radial), or pale-to-deep across a stem (linear).
3. **Highlight stripes on tubes.** Stems, filaments, petioles, roots and canes carry a thin pale
   stripe down the lit side and a faint shadow stripe down the other (`tube()`).
4. **Warm gold for reproductive parts.** Anthers, stigma lobes, pollen, eggs: `Y_LIGHT → Y_MID →
   Y_DARK` with a brown rim; anthers get a darker crease line and a pore dot.
5. **Simplified, friendly shapes.** Barrel ovary, bean anther, lobed nectary cushion. No
   photographic detail, no hairline schematics.
6. **Feet dissolve, they are not cut.** A stem that leaves the picture fades to the page
   (`fill_linear_faded()`), as in the reference.

## Palette (from `wb_ink.py`)

| Role | Tokens |
|---|---|
| Greens | `G_LIGHT #A9D68A` · `G_MID #58A049` · `G_DARK #2F7034` · `G_DEEP #1F5428` · `G_PALE #CFE5B3` · `G_FIL #BBD6A6` |
| Golds | `Y_LIGHT #FBE59A` · `Y_MID #F0C75A` · `Y_DARK #DFA73B` · `CREAM #F3E6BF` |
| Wood | `WOOD_L #A98255` · `WOOD_M #7B5733` · `WOOD_D #4F3721` |
| Fruit | `BERRY_L #8A4A66` · `BERRY_M #5B2342` · `BERRY_D #341326` |
| Ground | `SOIL_L #E9DDC3` · `SOIL_D #CDB88F` |

One accent only per figure: the page's burgundy is reserved for label numbers and leader dots, never
used inside a drawing.

## Building blocks

| Helper | Use |
|---|---|
| `blob()` | any soft-shaded ellipse with an inked rim — anthers, eggs, pollen, berries, buds, nodes |
| `tube()` | tapered stems, filaments, petioles, roots, cane, trunk (with highlight and shadow) |
| `leaf()` | the five-lobe vine leaf (same silhouette as the Mastery Guide), gradient and pale veins |
| `berry()` / `bunch()` | inked berries with a specular highlight; conical bunch |
| `fill_radial()` / `fill_linear()` | gradient fill clipped to any path |
| `fill_linear_faded()` | gradient whose foot dissolves into the page, seam-free |
| `path()`, `bezier()`, `ellipse_path()` | geometry |

## Construction rules

- Draw back to front: pedicel → receptacle → filaments → ovary → chamber → inner structures →
  nectary/front lobes → stigma → anthers → floating pollen.
- Each drawing is an `Art` subclass with `draw(c)`, `targets` and `vis`. Targets are
  `(name, (x, y), "L" | "R")`; choose the side so leader lines do **not** cross the artwork.
- `vis` is the horizontal extent actually painted (fractions of `W`). `LabelFigure` centres and
  clips to it.
- Keep **one structure per node / location**, well separated, so every label has an unambiguous
  target. If two targets sit within ~15 pt of each other, move one (we moved *Ovule* below the eggs).
- Sizes: a figure must leave room on its page for the other exercise. Typical heights 200–300 pt.

## Hard-won pitfalls

- **Translucency leaks.** `setFillColor(colour_with_alpha)` stays in force until the graphics state
  is restored. Always wrap alpha fills in `saveState()` / `restoreState()` — or everything drawn
  afterwards turns pale.
- **Alpha-stripe fades show hairlines** in some viewers. Fade with opaque overlapping slices.
- **Seams where two tubes meet** (cordons at the trunk): cover with a shoulder blob.
- Do not point a label at a shape's outline; point to its interior.

## Checklist for a new drawing

1. Put the reference and your drawing **side by side** at the same height and compare: proportions,
   outline weight, shading direction, colour temperature.
2. Render at 150 dpi and zoom into every joint.
3. Check each label target lands inside the structure it names, and that numbers read top to bottom.
4. Confirm the key (`label_key()`) matches the numbering on the page.
5. Rebuild the chapter and confirm the page count did not change.
