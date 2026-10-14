"""Bottle cut-outs for The Field Guide: Mendocino, slide 10, from Steve's photos (white-background JPEGs).

Removes ONLY the white background connected to the image border (a flood fill from every edge pixel), so near-white
labels inside the bottle survive; then softens the edge by one pixel and crops to the bottle. Output: RGBA PNGs under
the file names the deck reads.
Usage: python3 prepare_bottle_cutouts.py <roederer.jpg> <domaine_anderson.jpg> <navarro.jpg>
"""
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageFilter

OUT = {0: "bottle_mendo_roederer_lermitage_2019", 1: "bottle_mendo_domaine_anderson_pn_2023",
       2: "bottle_mendo_navarro_gewurz_deep_end"}


def cutout(path, thresh=242):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    white = (a.min(axis=2) >= thresh) & ((a.max(axis=2) - a.min(axis=2)) <= 14)
    h, w = white.shape
    bg = np.zeros_like(white)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if white[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if white[y, x] and not bg[y, x]:
                bg[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and white[ny, nx] and not bg[ny, nx]:
                bg[ny, nx] = True; q.append((ny, nx))
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.copy(); rgba.putalpha(alpha)
    return rgba.crop(rgba.getbbox()), bg.mean()


if __name__ == "__main__":
    for i, p in enumerate(sys.argv[1:4]):
        out, frac = cutout(p)
        out.save(f"../photos/{OUT[i]}.png")
        print(f"{OUT[i]}: {out.size}, background removed {frac:.0%}")
