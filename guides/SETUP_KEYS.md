# API Keys — environment setup

Both keys are read from environment variables by their respective fetch
scripts (`fetch_pexels.py`, `fetch_unsplash.py`) — never hardcoded into
deck build scripts directly.

## Pexels (existing, unchanged)

```
PEXELS_API_KEY=B9u7GUmGEiDEr4mVkbDdQHggsWLJx5Pxk0rpb3I7sCGRN6thbdYuEMHA
```

No network allowlist action needed beyond what's already configured
(`api.pexels.com`, `images.pexels.com`, `image.pexels.com`). No per-photo
tracking ping required.

## Unsplash (new in v8)

```
UNSPLASH_ACCESS_KEY=pBh4zg0SJFUtoREb5MEmT3t6KjEdDLbgYaHkrtGhNO4
```

**Network allowlist action required in the new environment:** under
Settings → Capabilities → Code execution and file creation → Domain
allowlist, set to "Package managers and specific domains" and add both
of the following under Additional allowed domains:

```
api.unsplash.com
images.unsplash.com
```

If the fetch script still can't reach Unsplash immediately after adding
these, start a fresh conversation — there's a known propagation delay
where newly-added domains don't take effect mid-session.

**Behavioral difference from Pexels, already handled in
`fetch_unsplash.py` — don't bypass it:** Unsplash's API terms require a
GET ping to the photo's `download_location` URL at the moment a photo is
actually used in a deliverable (not during search/preview). Always use
`download_unsplash_photo()` to pull a chosen photo rather than fetching
its URL directly, since that function performs the required ping as part
of the download.

Attribution format for both sources, for consistency in `photo_credit`
fields: `"{photographer} / Pexels"` or `"{photographer} / Unsplash"`.
`fetch_unsplash.py`'s `credit_line()` helper produces the latter
automatically.
