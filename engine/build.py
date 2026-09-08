"""
FIELD GUIDE STYLE SYSTEM v4 — BUILDER
A deck is a manifest: palette overrides + an ordered list of (module, slots).
This runs every module, enforces QA (any failure aborts the build), and
assembles the PNG set plus a review PDF.

Delivery is two explicit phases (see core.py's assemble_pdf/lock_deck_zip
docstrings for the full rationale): build_deck() always produces PNGs + a
merged PDF for review -- present the PDF, not the PNGs. Only call
lock_deck() afterward, once the person has explicitly signed off, to
package the ZIP of source PNGs.

Usage:
    from build import build_deck, lock_deck
    pdf, paths = build_deck(MANIFEST, out_dir="out", name="My_Deck")
    # ... present pdf for review, iterate ...
    zp = lock_deck(paths, out_dir="out", name="My_Deck")   # only once locked
"""
import os
from PIL import Image
from tokens import DEFAULT_PALETTE, EXPORT
from modules import MODULES
from core import assemble_pdf, lock_deck_zip


def build_deck(manifest, out_dir="out", name="deck", export_half=True):
    pal = dict(DEFAULT_PALETTE)
    pal.update(manifest.get("palette", {}))
    slides = manifest["slides"]
    total = len(slides)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, (module_name, slots) in enumerate(slides, start=1):
        fn = MODULES[module_name]
        img = fn(slots, i, total, pal)
        if export_half:
            img = img.resize(EXPORT, Image.LANCZOS)
        p = f"{out_dir}/{name}_s{i:02d}.png"
        img.save(p)
        paths.append(p)
    pdf = assemble_pdf(paths, f"{out_dir}/{name}.pdf")
    print(f"BUILD OK: {total} slides -> {pdf} (review PDF; PNGs held for lock_deck())")
    return pdf, paths


def lock_deck(paths, out_dir="out", name="deck"):
    """Call only after explicit sign-off that the deck is final."""
    zp = lock_deck_zip(paths, f"{out_dir}/{name}_PNGs.zip")
    print(f"LOCKED: {zp}")
    return zp
