"""
wc_commons.py — Wikimedia Commons sourcing for deck photography.

Commons is the only photo source with reliable geographic verification
for European vineyard sites. Unsplash and Pexels do not verify location
and their alt text is not evidence.

NETWORK REQUIREMENT
-------------------
Needs BOTH of these on the bash allowlist:

    commons.wikimedia.org
    upload.wikimedia.org

`thumb.wikimedia.org` alone is useless. As of 2026-09 it is a bare
redirect host: file paths return 301 to commons.wikimedia.org and
thumbnail paths return 400. It serves no image bytes. Do not treat its
presence on an allowlist as Commons access.

WORKAROUND WHEN THE ALLOWLIST IS NOT YET SET
--------------------------------------------
Research can proceed without bash network access. The web_search and
web_fetch tools are not bound by the bash allowlist and can reach
Commons category and file pages. Use them to build a manifest with
`manifest_stub()` below, then run `download_manifest()` in a later
session once the allowlist permits. The research is the slow part.

RATE LIMITING
-------------
3-second inter-request floor, exponential backoff on failure. A 429
from Commons returns HTML, so the JSON parse fails opaquely rather than
raising a clean rate-limit error — treat any JSONDecodeError as a
probable 429 and back off rather than retrying immediately.
"""

import json
import os
import subprocess
import time
import urllib.parse

API = "https://commons.wikimedia.org/w/api.php"
UA = "WineDeckBuilder/1.0 (educational carousel production)"

_MIN_INTERVAL = 3.0
_last_call = [0.0]


def _throttle():
    delta = time.time() - _last_call[0]
    if delta < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - delta)
    _last_call[0] = time.time()


def _get_json(params, attempt=0):
    """GET the Commons API with throttling and backoff.

    Returns None after 4 failed attempts rather than raising, so a
    single bad category does not abort a whole sourcing run.
    """
    _throttle()
    qs = urllib.parse.urlencode(params)
    url = f"{API}?{qs}"
    try:
        out = subprocess.run(
            ["curl", "-s", "-m", "30", "-H", f"User-Agent: {UA}", url],
            capture_output=True, text=True, timeout=45,
        ).stdout
        return json.loads(out)
    except json.JSONDecodeError:
        # Almost always a 429 served as an HTML error page.
        if attempt < 3:
            time.sleep(2 ** (attempt + 2))
            return _get_json(params, attempt + 1)
        return None
    except Exception:
        if attempt < 3:
            time.sleep(2 ** (attempt + 2))
            return _get_json(params, attempt + 1)
        return None


def category_files(category, limit=50):
    """List File: titles in a category.

    Category browsing is materially more reliable than keyword search
    for location-verified imagery — a file in Category:Cote-Rotie has
    been categorised by a human who knew where it was taken, whereas a
    keyword hit has only matched a filename.
    """
    data = _get_json({
        "action": "query", "format": "json", "list": "categorymembers",
        "cmtitle": f"Category:{category.replace(' ', '_')}",
        "cmtype": "file", "cmlimit": str(limit),
    })
    if not data:
        return []
    return [m["title"] for m in data.get("query", {}).get("categorymembers", [])]


def file_info(title):
    """Resolve a File: title to URL, dimensions, author and licence.

    Returns None if the file cannot be resolved. Always check `author`
    and `license` are populated before using an image in a deliverable
    — a missing author is a blocker, not a formatting detail.
    """
    data = _get_json({
        "action": "query", "format": "json", "prop": "imageinfo",
        "titles": title.replace(" ", "_"),
        "iiprop": "url|size|extmetadata",
    })
    if not data:
        return None
    pages = data.get("query", {}).get("pages", {})
    for _, page in pages.items():
        info = (page.get("imageinfo") or [{}])[0]
        if not info:
            continue
        meta = info.get("extmetadata", {})
        return {
            "title": title,
            "url": info.get("url"),
            "width": info.get("width"),
            "height": info.get("height"),
            "author": _strip_html(meta.get("Artist", {}).get("value", "")),
            "license": meta.get("LicenseShortName", {}).get("value", ""),
            "description": _strip_html(
                meta.get("ImageDescription", {}).get("value", "")),
        }
    return None


def _strip_html(s):
    out, depth = [], 0
    for ch in s:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return " ".join("".join(out).split())


def credit_line(info):
    """Attribution string matching the house convention."""
    author = info.get("author") or "Unknown"
    lic = info.get("license") or ""
    return f"{author} / Wikimedia Commons" + (f" ({lic})" if lic else "")


def manifest_stub(title, slot, note=""):
    """A manifest entry built by hand from web_fetch research.

    Use when bash cannot reach Commons. `slot` is the deck-local photo
    name the render script will call `core.load_photo()` with.
    """
    return {"title": title, "slot": slot, "note": note,
            "url": None, "author": None, "license": None}


def download_manifest(manifest, dest_dir, resolve_missing=True):
    """Download every entry in a manifest to dest_dir/<slot>.jpg.

    Entries created by `manifest_stub` have no URL; with
    resolve_missing=True they are resolved via file_info() first.
    Returns (downloaded, failed) — inspect `failed` rather than
    assuming a clean run.
    """
    os.makedirs(dest_dir, exist_ok=True)
    done, failed = [], []
    for entry in manifest:
        if not entry.get("url") and resolve_missing:
            info = file_info(entry["title"])
            if not info:
                failed.append((entry["title"], "could not resolve"))
                continue
            entry.update(info)
        path = os.path.join(dest_dir, f"{entry['slot']}.jpg")
        _throttle()
        r = subprocess.run(
            ["curl", "-s", "-m", "60", "-H", f"User-Agent: {UA}",
             "-o", path, entry["url"]],
            capture_output=True, timeout=90,
        )
        if r.returncode == 0 and os.path.getsize(path) > 5000:
            entry["local_path"] = path
            done.append(entry)
        else:
            failed.append((entry["title"], "download failed"))
    return done, failed
