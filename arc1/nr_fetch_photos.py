"""Download the Arc 1 Commons manifest as thumbnails, not originals.

Requesting `imageinfo`'s `url` (the original file) now gets a hard 429 from
upload.wikimedia.org, with an error body that says in as many words: use a
thumbnail in one of the listed standard sizes instead. Full-resolution
originals are the disruptive access pattern, and 5472x3648 is well past
anything a 2160px canvas can use.

So: ask the API for a rendered thumbnail via `iiurlwidth`, rewrite
thumb.wikimedia.org -> upload.wikimedia.org (identical bytes, and only the
latter is on the egress allowlist), and pull at 2560px — the widest standard
size, comfortably above the 2160px canvas width so a full-bleed crop still
has headroom.
"""
import json, os, subprocess, time

import wc_commons as wc

WIDTH = 2560
DEST = "/home/claude/work/photos"
MANIFEST = "/home/claude/work/NR_PHOTO_MANIFEST.json"


def thumb_url(u):
    """thumb.wikimedia.org is not on the allowlist; upload is. Same bytes."""
    return (u or "").split("?")[0].replace(
        "https://thumb.wikimedia.org/", "https://upload.wikimedia.org/")


def main():
    man = json.load(open(MANIFEST))
    os.makedirs(DEST, exist_ok=True)
    ok, bad = [], []

    for e in man:
        data = wc._get_json({
            "action": "query", "format": "json", "prop": "imageinfo",
            "titles": e["title"].replace(" ", "_"),
            "iiprop": "url|size", "iiurlwidth": str(WIDTH),
        })
        if not data:
            bad.append((e["slot"], "imageinfo failed"))
            continue
        page = list(data["query"]["pages"].values())[0]
        info = (page.get("imageinfo") or [{}])[0]
        url = thumb_url(info.get("thumburl") or info.get("url"))

        path = os.path.join(DEST, f"{e['slot']}.jpg")
        time.sleep(2.0)
        subprocess.run(["curl", "-s", "-m", "90", "-H", f"User-Agent: {wc.UA}",
                        "-o", path, url], capture_output=True, timeout=120)

        size = os.path.getsize(path) if os.path.exists(path) else 0
        head = open(path, "rb").read(4) if size else b""
        if size > 20000 and head[:2] == b"\xff\xd8":
            e["thumb_url"] = url
            e["local_path"] = path
            e["thumb_w"] = info.get("thumbwidth")
            e["thumb_h"] = info.get("thumbheight")
            ok.append(e)
            print(f"  ok   {e['slot']:<24} {info.get('thumbwidth')}x"
                  f"{info.get('thumbheight')}  {size/1024:,.0f} KB")
        else:
            bad.append((e["slot"], f"{size} bytes, not JPEG"))
            print(f"  FAIL {e['slot']:<24} {size} bytes")

    json.dump(man, open(MANIFEST, "w"), ensure_ascii=False, indent=1)
    print(f"\n{len(ok)} downloaded, {len(bad)} failed")
    for b in bad:
        print("  ", b)


if __name__ == "__main__":
    main()
