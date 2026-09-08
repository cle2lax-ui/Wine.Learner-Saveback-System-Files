"""Rebuild /home/claude/styleguide/fonts from upstream sources.

Playfair Display and Archivo ship as variable fonts; the pipeline wants
static instances at named weights. Sourced from google/fonts via
codeload.github.com — the GitHub REST API rate-limits this sandbox's egress
IP almost immediately, codeload does not.
"""
import os, subprocess, sys, tarfile, tempfile

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

DEST = "/home/claude/styleguide/fonts"
REPOS = {
    "playfair": ("google/fonts", "ofl/playfairdisplay"),
    "archivo": ("google/fonts", "ofl/archivo"),
    "cormorant": ("google/fonts", "ofl/cormorant"),
}

# target file -> (source VF, axis settings)
WANT = {
    "Playfair-Black.ttf":        ("PlayfairDisplay[wght].ttf", {"wght": 900}),
    "Playfair-XBold.ttf":        ("PlayfairDisplay[wght].ttf", {"wght": 800}),
    "Playfair-Bold.ttf":         ("PlayfairDisplay[wght].ttf", {"wght": 700}),
    "Playfair-Regular.ttf":      ("PlayfairDisplay[wght].ttf", {"wght": 400}),
    "Playfair-BoldItalic.ttf":   ("PlayfairDisplay-Italic[wght].ttf", {"wght": 700}),
    "Playfair-MediumItalic.ttf": ("PlayfairDisplay-Italic[wght].ttf", {"wght": 500}),
    "Archivo-Medium.ttf":        ("Archivo[wdth,wght].ttf", {"wght": 500, "wdth": 100}),
    "Archivo-Light.ttf":         ("Archivo[wdth,wght].ttf", {"wght": 300, "wdth": 100}),
    "Archivo-Bold.ttf":          ("Archivo[wdth,wght].ttf", {"wght": 700, "wdth": 100}),
    "Archivo-Black.ttf":         ("Archivo[wdth,wght].ttf", {"wght": 900, "wdth": 100}),
    "ArchivoCond-SemiBold.ttf":  ("Archivo[wdth,wght].ttf", {"wght": 600, "wdth": 75}),
    "ArchivoCond-Bold.ttf":      ("Archivo[wdth,wght].ttf", {"wght": 700, "wdth": 75}),
    "ArchivoCond-Black.ttf":     ("Archivo[wdth,wght].ttf", {"wght": 900, "wdth": 75}),
}
COPY = {
    "Archivo-VF.ttf": "Archivo[wdth,wght].ttf",
    "Cormorant-Italic.ttf": "Cormorant-Italic[wght].ttf",
}


def main():
    os.makedirs(DEST, exist_ok=True)
    tmp = tempfile.mkdtemp()
    tar = os.path.join(tmp, "fonts.tar.gz")
    subprocess.run(
        ["curl", "-sL", "-o", tar,
         "https://codeload.github.com/google/fonts/tar.gz/refs/heads/main"],
        check=True, timeout=900)

    srcs = {}
    with tarfile.open(tar) as t:
        for m in t.getmembers():
            base = os.path.basename(m.name)
            if not base.endswith(".ttf"):
                continue
            if any(k in m.name for k in
                   ("ofl/playfairdisplay/", "ofl/archivo/", "ofl/cormorant/")):
                f = t.extractfile(m)
                if f:
                    srcs[base] = f.read()
    print(f"pulled {len(srcs)} candidate faces")

    for out, src in COPY.items():
        if src in srcs:
            open(os.path.join(DEST, out), "wb").write(srcs[src])
            print(f"  copy     {out}")
        else:
            print(f"  MISSING  {out}  (no {src})")

    cache = {}
    for out, (src, axes) in WANT.items():
        if src not in srcs:
            print(f"  MISSING  {out}  (no {src})")
            continue
        if src not in cache:
            p = os.path.join(tmp, src)
            open(p, "wb").write(srcs[src])
            cache[src] = p
        vf = TTFont(cache[src])
        instantiateVariableFont(vf, axes, inplace=True, updateFontNames=False)
        vf.save(os.path.join(DEST, out))
        print(f"  instance {out}  {axes}")


if __name__ == "__main__":
    main()
