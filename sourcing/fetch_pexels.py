"""
Pexels photo search + download helper, established pattern for this
project: curl subprocess (not urllib), no per-photo tracking ping
required (unlike Unsplash).
"""
import subprocess
import json
import os

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")


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


def search_pexels(query, per_page=10, orientation=None):
    """Returns list of dicts: id, width, height, alt, photographer,
    photographer_url, url (large2x for downloading)."""
    params = f"query={query.replace(' ', '+')}&per_page={per_page}"
    if orientation:
        params += f"&orientation={orientation}"
    url = f"https://api.pexels.com/v1/search?{params}"
    headers = [f"Authorization: {PEXELS_API_KEY}"]
    data = _curl_json(url, headers)
    results = []
    for p in data.get("photos", []):
        results.append({
            "id": p["id"],
            "width": p["width"],
            "height": p["height"],
            "alt": p.get("alt", ""),
            "photographer": p["photographer"],
            "photographer_url": p["photographer_url"],
            "url": p["src"]["large2x"],
            "url_original": p["src"]["original"],
        })
    return results


def download_pexels_photo(photo, dest_path, use_original=False):
    url = photo["url_original"] if use_original else photo["url"]
    cmd = ["curl", "-sL", "-o", dest_path, url]
    subprocess.run(cmd, capture_output=True)
    return os.path.exists(dest_path) and os.path.getsize(dest_path) > 0


def credit_line(photo):
    return f"{photo['photographer']} / Pexels"
