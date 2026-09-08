# Save-back — v9 (Series System)

Copy every file in this package into `/mnt/project/`. Nothing here
overwrites an existing file; all six are new.

```
SERIES_SYSTEM_v9.md              <- read this one first
SPLIT_DECISION_STYLE_GUIDE.md
REELS_SPEC_v1.md
wc_commons.py
FG_NORTHERN_RHONE_SPEC.md
CHANGELOG_v9.md
```

## What this changes about how sessions run

`SERIES_SYSTEM_v9.md` is now the document that answers "what are we
building today." The existing per-series style guides still answer
"how do we build it." Start a session by reading the arc table in §4
of the system doc, not by picking a subject fresh.

## Before the next session

1. **Allowlist:** add `commons.wikimedia.org` and
   `upload.wikimedia.org` under Settings → Capabilities → Code
   execution → Domain allowlist. A fresh session may be required for
   it to take effect. `thumb.wikimedia.org` can be removed; it does
   nothing.
2. **Test `wc_commons.py`** — it has never run against a reachable
   host. `category_files("Cote-Rotie")` is the smoke test.
3. **Unsplash tier** — if deck photography is going to lean on it,
   50 requests/hour will be the binding constraint, not the search
   quality.

## Standing reminder

`core.py` still has no canonical copy under version control in the
project, and this package does not fix that. Diff working copies
against `/mnt/project/` at the start of any session that touches
`core.py` or `modules.py`.
