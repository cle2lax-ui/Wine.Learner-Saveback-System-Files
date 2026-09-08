# Changelog — v9 (Series System)

2026-09. This save-back adds a publishing layer above the existing
deck-build system. No changes to `core.py` or `modules.py` in this
package.

## New

- **`SERIES_SYSTEM_v9.md`** — master publishing doc. Audience strata,
  format-to-signal mapping, five-per-week cadence, the two-week arc
  structure, source hierarchy and the flagging rule, review-session
  protocol, caption architecture, photo-sourcing order of preference.
- **`SPLIT_DECISION_STYLE_GUIDE.md`** — sixth series, two slides,
  built to generate argument. Includes the three-part question test a
  candidate subject must fail to ship.
- **`REELS_SPEC_v1.md`** — vertical distribution treatment. 1080×1920
  re-composition, never a crop of the 4:5 render.
- **`wc_commons.py`** — Wikimedia Commons sourcing module. Category
  browsing, file metadata resolution, attribution, throttling with
  429-as-JSONDecodeError handling, and a manifest workflow that lets
  research proceed while bash network access is unavailable.
- **`FG_NORTHERN_RHONE_SPEC.md`** — Arc 1 pillar deck spec, fully
  sourced to D3 Ch. 7, with a flagged-for-verification block.

## Findings recorded this session

- **`thumb.wikimedia.org` is not Commons access.** It is a bare
  redirect host as of 2026-09: file paths 301 to commons, thumbnail
  paths return 400. It serves no bytes. Both `commons.wikimedia.org`
  and `upload.wikimedia.org` are required.
- **web_search / web_fetch are not bound by the bash allowlist.**
  Commons category and file pages remain reachable through them when
  bash is blocked. This makes photo research separable from photo
  download, which is now the documented fallback workflow.
- **Unsplash search is strict.** Multi-word specific queries
  ("Cote Rotie vineyard terraces") return zero results while the API
  reports 200 and healthy rate-limit headers. Two-word generic queries
  work. Zero results are not automatically a rate-limit signal, but
  check `x-ratelimit-remaining` before concluding either way.
- **Unsplash key is demo tier** — 50 requests/hour. Batch accordingly;
  a full deck's sourcing run will exhaust it.
- **Three unsourced claims caught before render** on Arc 1: a Viognier
  1960s hectarage figure, Syrah's parentage, and Hermitage's historic
  price parity with first-growth Bordeaux. None appear in D3 Ch. 7.
  All three were in the originally proposed content and would have
  shipped unflagged without the primary-source check.

## Open / not done

- No AOC boundary dataset in hand for the northern Rhône crus. The
  atlas standard calls for real traced geometry; the fallback is
  labelled cru points against a real traced departmental outline and
  real river course. Decision pending.
- `wc_commons.py` is untested against live network — written blind
  against a blocked host. Test before relying on it.
- Arc 1 photography not sourced. Blocked on the allowlist change.
