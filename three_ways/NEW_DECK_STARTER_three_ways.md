# NEW DECK STARTER — Three Ways (v1)

Kickoff checklist for a new "Three Ways" one-pager. Read
THREE_WAYS_STYLE_GUIDE.md first if this is your first one — this doc
is the fast path once you already know the system.

## 1. Pick the three bottles

Same discipline as any other series: real, specific, currently
available bottlings, budget-appropriate, with a defensible reason
each one is the pick (not just "cheapest that fits"). If a request
gives an impossible constraint (e.g. a producer/price combination that
doesn't exist in the current market), say so and offer real
alternatives — don't force a wrong bottle silently.

## 2. Research + draft copy

For each bottle: producer, wine name, style/appellation line, origin,
and a one-sentence tasting note pulled from real critic reviews (name
the source in your own working notes even if it doesn't appear on the
slide). Keep notes tight — two sentences is already pushing it at this
type size across three columns.

## 3. Source three region photos

One per bottle's home region, confirmed via geodata (Unsplash location
field or equivalent) — not just a plausible-looking stock photo. This
deck's build caught a mismatch (Napa vs. the intended AVA) before it
shipped by checking; do the same. If the exact micro-region has no
inventory, the next-broadest confirmed match is fine — just don't
caption it more specifically than what's actually confirmed.

## 4. Ask for the bottle photos

Bottle photos are supplied by the deck owner, not sourced from stock —
a labeled product photo of a *different* real wine standing in for
the one being discussed would misrepresent an actual product. Ask for:
white/near-white background studio shots, upright, full bottle in
frame, one per wine. Build the rest of the layout with placeholder
bottle silhouettes in the meantime so there's something to review
before the real photos arrive (see
`render_three_ways_EXAMPLE_zinfandel.py` for how the placeholder
bottles were generated).

## 5. Process each bottle photo

```python
from core import remove_background
img, hole_frac = remove_background(path)   # try white_threshold=730-750
                                             # if hole_frac isn't 0
```

Then **green-screen check** every cutout before trusting it — paste
onto a loud, unrealistic color (not white, not the deck's actual
background) and look at the corners, not just the silhouette:

```python
from PIL import Image
im = Image.open(cutout_path)
bg = Image.new("RGB", im.size, (30, 120, 30))
bg.paste(im, (0, 0), im)
bg.save("check.png")   # view this before moving on
```

A tilted bottle photo can leave an isolated pocket of background in a
corner that survives `remove_background()`'s flood fill — invisible
on a paper-colored page, glaring on a dark one. If you find one,
reseed a flood fill from a point inside the pocket rather than
re-cropping blind (see modules.py's Three Ways changelog entry, or
just: BFS from a known-bad pixel, clear same-color-neighbors' alpha).

## 6. Build the render script

Copy `render_three_ways_EXAMPLE_zinfandel.py` as your starting point.
It's a complete, working reference for: the palette recipe, the
region-photo-aligned column grid, `bottle_lift` + `panel_gap` tuned
together, the off-white scrim, and bold shrink-to-fit captions. Swap
in your kicker/mark/products/region_photos and adjust to taste.

**Compute `col_x_positions` and `col_w_override` before you render**
— don't eyeball three column starts and hope they land on the photo
segments below. See the style guide's "Column alignment" section for
the formula; it's two lines of arithmetic, not a design judgment call.

## 7. Render, check QA, then check it visually anyway

QA passing means no box collisions and every font is at or above
floor — it does not mean the captions don't collide with each other
inside their own segment, or that a caption's contrast holds up
against a specific patch of a specific photo. Zoom into: the
kicker/bottle-lift overlap zone, the shelf-scrim seam, each region
caption against its actual photo background.

## 8. This is a one-pager

Set `footer_label=""` and `show_page_num=False` — there's nothing to
swipe to and no page 2 of 2. Don't ship the default GTR/Quick Sips
footer furniture on a standalone slide.
