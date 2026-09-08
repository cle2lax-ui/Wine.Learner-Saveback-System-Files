"""
Unsplash photo search + download helper, mirroring fetch_pexels.py's
established pattern for this project (curl subprocess, not urllib).

Unsplash's API terms require: (1) attribution to the photographer and
Unsplash, and (2) a GET ping to the photo's `download_location` URL at
the moment it's actually used/downloaded for a real deliverable (not
just previewed) -- this is different from Pexels, which has no such
tracking-ping requirement. Both are handled here.
"""
import subprocess
import json
import os

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")


def _curl_json(url, headers=None):
    cmd = ["curl", "-s"]
    for h in (headers or []):
        cmd += ["-H", h]
    cmd.append(url)
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    try:
        return json.loads(out)
    except Exception:
        return {}


def search_unsplash(query, per_page=10, orientation=None):
    """Returns a list of dicts: id, width, height, description/alt,
    photographer, photographer_url, download_location, url (regular-size
    for downloading)."""
    params = f"query={query.replace(' ', '+')}&per_page={per_page}"
    if orientation:
        params += f"&orientation={orientation}"
    url = f"https://api.unsplash.com/search/photos?{params}"
    headers = [f"Authorization: Client-ID {UNSPLASH_ACCESS_KEY}"]
    data = _curl_json(url, headers)
    results = []
    for p in data.get("results", []):
        results.append({
            "id": p["id"],
            "width": p["width"],
            "height": p["height"],
            "alt": p.get("alt_description") or p.get("description") or "",
            "photographer": p["user"]["name"],
            "photographer_url": p["user"]["links"]["html"],
            "download_location": p["links"]["download_location"],
            "url": p["urls"]["regular"],
            "url_full": p["urls"]["full"],
        })
    return results


def download_unsplash_photo(photo, dest_path, use_full=False):
    """Downloads the photo AND pings download_location per Unsplash's
    API guidelines -- required whenever a photo is used in a real
    deliverable, not optional. Call this at the point a photo is
    actually chosen for a deck, not during browsing/search."""
    url = photo["url_full"] if use_full else photo["url"]
    subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", dest_path, url])
    headers = [f"Authorization: Client-ID {UNSPLASH_ACCESS_KEY}"]
    _curl_json(photo["download_location"], headers)  # required tracking ping
    return dest_path


def credit_line(photo):
    """Standard Unsplash attribution string for photo_credit fields."""
    return f"{photo['photographer']} / Unsplash"
