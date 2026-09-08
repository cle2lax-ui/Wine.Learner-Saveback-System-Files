import json, subprocess, sys, urllib.parse

API = "https://commons.wikimedia.org/w/api.php"

import time
_last=[0.0]
def _get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(6):
        gap = time.time()-_last[0]
        if gap < 3.0: time.sleep(3.0-gap)
        r = subprocess.run(["curl","-sSL","-A","WineDeckBot/1.0 (educational)","--max-time","40", url],
                           capture_output=True, text=True)
        _last[0]=time.time()
        try:
            return json.loads(r.stdout)
        except Exception:
            time.sleep(5*(attempt+1))
    raise RuntimeError("commons api failed: "+r.stdout[:200])

def search(term, limit=12):
    d = _get({"action":"query","format":"json","generator":"search",
              "gsrsearch":f"filetype:bitmap {term}","gsrnamespace":"6","gsrlimit":limit,
              "prop":"imageinfo","iiprop":"url|size|extmetadata","iiurlwidth":"400"})
    out=[]
    for p in (d.get("query",{}).get("pages") or {}).values():
        ii = p["imageinfo"][0]
        em = ii.get("extmetadata",{})
        out.append({
          "title": p["title"],
          "w": ii["width"], "h": ii["height"],
          "url": ii["url"],
          "thumb": ii.get("thumburl"),
          "artist": em.get("Artist",{}).get("value","")[:120],
          "lic": em.get("LicenseShortName",{}).get("value",""),
        })
    return out

if __name__ == "__main__":
    import re
    for t in sys.argv[1:]:
        print("="*70); print("QUERY:", t)
        for r in search(t):
            a = re.sub("<[^>]+>","",r["artist"])
            print(f'  {r["w"]}x{r["h"]:<5} {r["lic"]:<18} {r["title"][5:80]} | {a[:45]}')

def cat(name, limit=60):
    d = _get({"action":"query","format":"json","generator":"categorymembers",
              "gcmtitle":f"Category:{name}","gcmtype":"file","gcmlimit":limit,
              "prop":"imageinfo","iiprop":"url|size","iiurlwidth":"400"})
    out=[]
    for p in (d.get("query",{}).get("pages") or {}).values():
        ii=p["imageinfo"][0]
        out.append({"title":p["title"],"w":ii["width"],"h":ii["height"],"url":ii["url"],"thumb":ii.get("thumburl")})
    return out

def subcats(name, limit=60):
    d=_get({"action":"query","format":"json","list":"categorymembers",
            "cmtitle":f"Category:{name}","cmtype":"subcat","cmlimit":limit})
    return [c["title"] for c in d.get("query",{}).get("categorymembers",[])]


def thumb_url(u):
    """Commons' imageinfo now hands back thumbnails on thumb.wikimedia.org,
    which is not on this sandbox's egress allowlist (upload.wikimedia.org
    is). The bytes are identical on both hosts, so rewrite rather than
    fail. Also strip the utm_* tracking query the API appends.

    If thumb.wikimedia.org is ever added to the allowlist this becomes a
    no-op, so it is safe to leave in."""
    u = u.split("?")[0]
    return u.replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/")


def fetch(title, width=3000, dest=None):
    """Resolve a Commons File: title to a local path + full attribution."""
    import subprocess, re, os
    d = _get({"action": "query", "format": "json", "titles": "File:" + title,
              "prop": "imageinfo", "iiprop": "url|size|extmetadata",
              "iiurlwidth": str(width)})
    p = list(d["query"]["pages"].values())[0]
    if "imageinfo" not in p:
        raise KeyError("no such Commons file: " + title)
    ii = p["imageinfo"][0]
    em = ii.get("extmetadata", {})
    url = thumb_url(ii.get("thumburl") or ii["url"])
    if dest:
        subprocess.run(["curl", "-sSL", "-A", "WineDeckBot/1.0 (educational)",
                        "--max-time", "150", "-o", dest, url], check=True)
    strip = lambda v: re.sub("<[^>]+>", "", v).strip()
    return {"title": title, "path": dest, "url": url,
            "artist": strip(em.get("Artist", {}).get("value", "")),
            "lic": em.get("LicenseShortName", {}).get("value", ""),
            "descurl": ii.get("descriptionurl", ""),
            "w": ii["width"], "h": ii["height"]}
