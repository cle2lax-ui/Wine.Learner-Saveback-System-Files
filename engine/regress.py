"""Pixel-hash regression guard for the shared engine.

Re-renders (1) the specimen suite -- one slide per module, M01-M26 --
(2) the locked Mosel Field Guide (plus the Cornas GTR and the What Am I Drinking? deck), and (3) the Cornas GTR (the format's
regression subject), hashes every PNG's decoded pixels, and
compares against reference/PIXEL_HASHES.json. The Mosel deck is the
system's visual benchmark (guides/VISUAL_BENCHMARK_v10.md), so a change to
core.py / modules.py that alters even one of its pixels is caught here
before it ships.

    python3 engine/regress.py            # compare; exit 1 on any change
    python3 engine/regress.py --freeze   # accept the current renders as the
                                         # new reference (after an APPROVED change)

Hashes are exact, so a change in PIL / font rendering across environments
will also trip it -- that is "environment drift" in STYLE_GUIDE_v5 §9's
sense: find out which it is before building a real deck. Photos the specimen
suite lacks are replaced with a stand-in, so specimen hashes depend on
photos/de_bernkastel_aerial.jpg staying as it is.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REF = os.path.join(ROOT, "reference", "PIXEL_HASHES.json")
SPEC_OUT = "/home/claude/specimen_renders"
MOSEL_OUT = "/home/claude/out_fg_mosel"
CORNAS_OUT = "/home/claude/out_gtr_cornas"
WAD_OUT = "/home/claude/out_wad_loosen"
ENV = dict(os.environ, PYTHONPATH=f"{ROOT}/engine:{ROOT}/formats")


def _hash(path):
    a = np.asarray(Image.open(path).convert("RGB"))
    return hashlib.sha256(a.tobytes() + str(a.shape).encode()).hexdigest()[:20]


def _render():
    os.makedirs(SPEC_OUT, exist_ok=True)
    for f in glob.glob(f"{SPEC_OUT}/*.png"):
        os.remove(f)
    for cmd, cwd in ((["python3", "specimen.py"], f"{ROOT}/engine"),
                     (["python3", "render_fg_mosel.py"], f"{ROOT}/arc2"),
                     (["python3", "render_gtr_cornas.py"], f"{ROOT}/arc1"),
                     (["python3", "render_wad_loosen_treppchen.py"], f"{ROOT}/arc2")):
        r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=900)
        if r.returncode != 0:
            print(r.stdout[-1500:], r.stderr[-1500:])
            sys.exit(f"render failed: {' '.join(cmd)}")
    return {
        "specimen": {os.path.basename(p): _hash(p) for p in sorted(glob.glob(f"{SPEC_OUT}/spec*.png"))},
        "fg_mosel": {os.path.basename(p): _hash(p) for p in sorted(glob.glob(f"{MOSEL_OUT}/[0-9]*.png"))},
        # The GTR format's regression subject: its guide names a reference
        # deck + GTR_REFERENCE_HASHES.txt, but that file never made it into
        # the repo. Cornas is the GTR deck whose photos are present.
        "gtr_cornas": {os.path.basename(p): _hash(p) for p in sorted(glob.glob(f"{CORNAS_OUT}/0*.png"))},
        # What Am I Drinking? (the redesigned Quick Sips two-pager): locked reference deck,
        # Dr. Loosen Erdener Treppchen Auslese 2020, tag wad-loosen-treppchen-final.
        "wad_loosen": {os.path.basename(p): _hash(p) for p in sorted(glob.glob(f"{WAD_OUT}/0*.png"))},
    }


def main():
    now = _render()
    if "--freeze" in sys.argv:
        os.makedirs(os.path.dirname(REF), exist_ok=True)
        json.dump(now, open(REF, "w"), indent=1, sort_keys=True)
        print(f"froze {len(now['specimen'])} specimen + {len(now['fg_mosel'])} Mosel + {len(now['gtr_cornas'])} Cornas + {len(now['wad_loosen'])} What-Am-I-Drinking hashes -> {REF}")
        return
    ref = json.load(open(REF))
    changed = 0
    for group in ("specimen", "fg_mosel", "gtr_cornas", "wad_loosen"):
        for name in sorted(set(ref[group]) | set(now[group])):
            a, b = ref.get(group, {}).get(name), now[group].get(name)
            if a != b:
                changed += 1
                print(f"CHANGED  {group}/{name}" + ("  (missing now)" if b is None else "  (new)" if a is None else ""))
    total = sum(len(v) for v in ref.values())
    print(f"{total - changed} of {total} renders match the reference" + ("" if not changed else f"; {changed} DIFFER"))
    sys.exit(1 if changed else 0)


if __name__ == "__main__":
    main()
