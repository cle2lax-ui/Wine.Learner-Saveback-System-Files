# SPLIT DECISION — BRAND MARK
Locked. Supersedes nothing; this format previously had no mark.

---

## 1. The mark

Two **Quick Sips glasses** tilted toward each other at the moment of the
clink. It is the QS glyph used twice, not a redrawn wine glass — the two
series share a piece of house furniture rather than each owning a
similar-but-different glass. That shared origin is what makes them read
as one house at thumbnail size instead of as two people who each drew a
wine glass.

The left glass takes **SIGNATURE**, the right takes **ACCENT**.

## 2. Colour is not fixed

Split Decision inherits its arc's Field Guide palette. `sd_mark` takes
the palette dict and reads SIGNATURE and ACCENT from it, so the mark
restyles itself per arc with no per-deck code and the SD post reads as a
sibling of that arc's Field Guide in the grid.

The two glasses must always differ from each other. The style guide
requires the poles to be distinguished by colour and never by size or
weight — neither side may look like the favoured one before it has been
read. A single-colour version exists for mono printing only.

## 3. The code is canonical

`sd_brand.py` is the mark. The exported PNGs are one arc's *instance* of
it, for places that cannot run the code — a profile image, a slide
template, a printer. Regenerate them per arc; do not treat them as the
logo.

```
sd_mark(img, x, y, size, pal)              -> (w, h)
sd_mark_bbox(size, gap=0.30, tilt=18)      -> (w, h)
sd_lockup(img, x, y, size, pal)            -> (w, h)   mark + wordmark
```

`size` is the height of one glass. The mark's drawn width is about 1.7x
that; use `sd_mark_bbox` rather than assuming, because the rotation
pushes the ink outside the nominal box.

## 4. Geometry — do not re-derive these

- **tilt = 18°**, and the LEFT glass takes the negative value. PIL
  rotates counter-clockwise for positive angles, so signing it the
  obvious way leans both glasses outward and the mark reads as two
  glasses being set down rather than a toast.
- **gap = 0.30**, the fraction of a glass's width by which the two
  overlap. The QS glyph carries padding either side of its bowl, so at
  a small gap the rims sit visibly apart and the mark reads as two
  separate glasses instead of contact.
- **The liquid surface stays level.** The QS glyph draws the wine as a
  bar across the bowl; rotated with the glass, that bar tilts, which is
  what wine does not do. So `_glass_parts` lifts the bar out of the
  glyph and `_liquid_mask` redraws it pre-rotated by `tilt + slosh`, so
  that after the glass is rotated the surface comes out level. **slosh
  = 3°** tips it just off true, so it reads as wine that has been
  knocked rather than a spirit level.
- The replacement surface is clipped to the bowl interior, which is
  found by **flood fill** from a seed inside the bowl. Reading wall
  edges row by row does not work: the bar's own rows return a single
  run and have to be interpolated across, and one stray anti-aliased
  run throws that interpolation far enough off to bleed the mask
  outside the glass on one side and cut a diagonal out of it on the
  other. A flood fill cannot escape a closed outline.

## 5. Wordmark

Playfair Black — the Field Guide and Quick Sips display face, not
FFFA's grotesque. Since SD inherits its arc's palette, it inherits the
house serif too. Centred under the mark, with a short ACCENT rule at
half the wordmark's width beneath it. The rule is the same device FFFA
uses, so the marks share a family resemblance without repeating a glyph.

## 6. Minimum size

72 px for the mark. Tested against the Quick Sips mark at the same size:
the two are distinguishable by count and colour, which survives
thumbnail scale. Below 72 the two bowls start to merge.

## 7. Known dependency

Unlike the FFFA checklist and the GTR folded map, this mark depends on a
file — `QS_glass_icon_ink.png` in the styleguide photo directory. That
is a deliberate trade, since sharing the glyph is the point.

The risk is real: that icon has already shipped once as an opaque white
square and once missing entirely. So `_glass_glyph`:

- **raises** a `FileNotFoundError` naming the expected path rather than
  silently drawing nothing, and
- **repairs** a fully-opaque source by deriving alpha from luminance,
  the same way the icon rebuild did, rather than painting a white box
  onto every page.

If the icon goes missing again, the failure is loud.

## 8. Exported files

`out_sd_logo/`, all transparent-background PNG:

| File | Use |
|---|---|
| `mark_arc1_{1024,512,256,128}` | Arc 1 (Northern Rhône) palette |
| `mark_reversed_*` | on a SIGNATURE ground |
| `mark_mono-ink_*` / `mark_mono-paper_*` | single-colour, mono printing only |
| `lockup_arc1_1024`, `lockup_reversed_1024` | mark + wordmark |
| `avatar_arc1_1080` | square, centred, for a profile image |
