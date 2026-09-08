# New Deck Starter — v8.2 addendum

Additive on top of `NEW_DECK_STARTER_v8_ADDENDUM.md`, the same way that
was additive on v7. This addendum adds the third carousel series,
**"Five Fascinating Facts About..." (FFFA)**, built and iterated to a
locked deck (Champagne) this session.

## New series: FFFA — fixed 6-page format, not a module sequence

Unlike Field Guide (variable-length module sequence) or Quick Sips
(2-page), FFFA is **always exactly 6 pages**: one cover
(`fff_cover()`) + five facts (`fff_fact()`, the fifth call passing
`closing=True`). There is no intake step for "how many slides" or
"which modules" the way Field Guide has — the shape is fixed, so the
only real creative decisions per deck are the topic and the five facts
themselves.

**Canned prompt for kicking off a new FFFA deck:**

```
Use the v8.2 system: FFFA_STYLE_GUIDE.md, DESIGN_PROCESS_v8.md,
core.py, tokens.py, fff_facts.py, fetch_pexels.py, fetch_unsplash.py,
specimen.py.
```

### Before writing any code

1. Pull 5 facts from the CSW Study Guide (primary) plus the approved
   secondary sources (Wine with Seth's WineWiki, Wine Folly, Wine Wit
   & Wisdom) — own words, no direct quotes beyond what copyright
   compliance allows.
2. For each fact, ask: **is this claim fundamentally comparative or
   scalar?** If yes, plan a diagram (see FFFA_STYLE_GUIDE.md's
   "Diagrams" section) instead of relying on a stock photo to carry it
   — no stock library has ever had a photo that shows five bottle
   formats at true relative scale, and it isn't going to start now.
3. Source photos from Unsplash first, then Pexels, per the standing
   instruction — but confirm at full resolution before committing,
   not just the search-result thumbnail. Two photo swaps this session
   were caught only after a full-res check: a glassware etching that
   read as a logo, and a "bubbles" search result that turned out to be
   condensation on the outside of a glass, not bubbles rising through
   the liquid.

### Locked design decisions (don't re-litigate per deck)

- Cover is photo-only, no color block (v2+; the deck started with a
  flat-red block cover and moved off it after the first review round).
- Signature color is cobalt (`FFFA_ACCENT`), not red or gold — reserved
  so FFFA never gets visually confused with Field Guide or Quick Sips.
- Cover subject and every fact headline render in Playfair Black,
  golden yellow (`FFFA_YELLOW`); everything else (kicker, numerals,
  body, diagram labels) stays sans/cobalt/paper.
- Checklist icon (drawn from primitives, never an asset) appears full-
  size on the cover and at reduced scale next to every fact numeral —
  this is now the series' one repeating brand device, alongside the
  small cobalt grid-mark square top-right of every photo.
- 35px minimum font size on any chart/diagram label — see
  DESIGN_PROCESS_v8.md section 9.

### What's still deck-specific and open to direction

- The five facts and their exact framing.
- Photo choice and mood (this session's Champagne deck went through
  five photo swaps chasing "warmer, moodier, bubbles actually rising
  through the glass, no logos" — expect iteration here, it's genuinely
  subjective).
- Whether a given fact gets a diagram or stays photo-only — not every
  fact needs one; forcing a diagram onto a non-comparative fact would
  be clutter, not clarity.

## Before final delivery

Same four-designer review (Wintour → Chanel → Ive → Vignelli) as every
other series, over every slide — FFFA is not exempt just because it's
a fixed format. Same PDF-first review / ZIP-only-on-lock delivery rule
as the rest of the system.
