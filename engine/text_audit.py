"""Text-contrast audit: measures EVERY piece of text a deck draws against the pixels actually behind it.

Hooks PIL's ImageDraw.text, so it sees text from every module, format and deck script, whatever color it uses. For each
call it samples the region under the text BEFORE drawing, takes the median background, and records the WCAG contrast
ratio. It exists because a palette check misses the real cases (gold on paper, gold on a green block, gold on a photo
scrim): the number that matters is text against what is really behind it.

    python3 engine/text_audit.py <script.py> <out.json> [cwd]     # run one deck script under the hook
    python3 engine/text_audit.py --report <out.json> [<out.json> ...] [--gold]

Thresholds (WCAG AA): 4.5:1 for text under LARGE_PX tall, 3:1 for larger. Text drawn into transparent layers (shadows,
rotated labels) and translucent fills are skipped: only text over opaque pixels is measured.
"""
import json
import os
import runpy
import sys

import numpy as np
from PIL import ImageDraw

LARGE_PX = 100
SMALL_MIN, LARGE_MIN = 4.5, 3.0
RECORDS = {}
_orig = ImageDraw.ImageDraw.text


def _lin(a):
    a = a / 255.0
    return np.where(a <= 0.03928, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def _lum(rgb):
    v = _lin(np.asarray(rgb, float))
    return 0.2126 * v[..., 0] + 0.7152 * v[..., 1] + 0.0722 * v[..., 2]


def _ratio(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _hook(self, xy, text, fill=None, font=None, *a, **k):
    try:
        img = getattr(self, "_image", None)
        if (img is not None and isinstance(fill, (tuple, list)) and len(fill) in (3, 4) and str(text).strip()
                and (len(fill) == 3 or fill[3] == 255) and font is not None):
            x0, y0, x1, y1 = [int(v) for v in self.textbbox(xy, text, font=font, **{kk: vv for kk, vv in k.items() if kk in ("anchor", "spacing", "align")})]
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(img.width, x1), min(img.height, y1)
            if x1 - x0 > 2 and y1 - y0 > 2:
                reg = np.asarray(img.crop((x0, y0, x1, y1)))
                if reg.shape[-1] == 3 or reg[..., 3].mean() > 250:
                    rgb = reg[..., :3].reshape(-1, 3)
                    lums = _lum(rgb)
                    med = np.median(rgb, axis=0)
                    fl = float(_lum(np.array(fill[:3])))
                    bg_l = float(_lum(med))
                    # worst case: the background pixels closest in luminance to the text
                    worst = float(np.percentile(lums, 95 if fl > bg_l else 5))
                    key = (CONTEXT["label"], tuple(int(c) for c in fill[:3]), tuple(int(c // 24) for c in med), int(getattr(font, "size", 0)))   # one group per SIZE: small text must not hide behind large text in the same color
                    size = getattr(font, "size", 0)
                    r = RECORDS.setdefault(key, dict(ctx=CONTEXT["label"], fill=list(map(int, fill[:3])),
                                                     bg=[int(c) for c in med], text="", n=0, size=size,
                                                     ratio=_ratio(fl, bg_l), worst=_ratio(fl, worst)))
                    r["n"] += 1
                    if len(r["text"]) < 34:
                        r["text"] += str(text).replace("\n", " ")
                    r["ratio"] = min(r["ratio"], _ratio(fl, bg_l))
                    r["worst"] = min(r["worst"], _ratio(fl, worst))
    except Exception:
        pass
    return _orig(self, xy, text, fill, font, *a, **k)


CONTEXT = {"label": ""}


def install():
    ImageDraw.ImageDraw.text = _hook


def context(label):
    CONTEXT["label"] = label


def _need(size):
    return LARGE_MIN if size >= LARGE_PX else SMALL_MIN


def failures(records):
    return [r for r in records if r["ratio"] < _need(r["size"])]


def is_gold(fill):
    r, g, b = fill
    return r > g > b and r - b > 60 and g > 90 and r > 120      # warm, yellow-orange family


def main():
    if sys.argv[1] == "--report":
        args = [a for a in sys.argv[2:] if not a.startswith("--")]
        gold_only = "--gold" in sys.argv
        recs = [r for p in args for r in json.load(open(p))]
        bad = failures(recs)
        if gold_only:
            bad = [r for r in bad if is_gold(r["fill"])]
        for r in sorted(bad, key=lambda r: (r["ctx"], r["ratio"])):
            print(f"{r['ratio']:5.2f}:1 (needs {_need(r['size']):.1f}, {r['size']:>3}px)  fill {tuple(r['fill'])} on {tuple(r['bg'])}  "
                  f"{r['ctx']}: '{r['text'][:34]}'")
        gold_all = [r for r in recs if is_gold(r["fill"])]
        print(f"\n{len(recs)} text groups measured; {len(failures(recs))} below threshold "
              f"({len([r for r in failures(recs) if is_gold(r['fill'])])} of them gold; {len(gold_all)} gold groups in all)")
        return
    script, out = os.path.abspath(sys.argv[1]), sys.argv[2]
    cwd = os.path.abspath(sys.argv[3]) if len(sys.argv) > 3 else os.path.dirname(script)
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    for p in (f"{root}/engine", f"{root}/formats", cwd):
        sys.path.insert(0, p)
    import modules
    install()
    # label by module + slide number for decks that go through modules.MODULES
    for name, fn in list(modules.MODULES.items()):
        def wrap(fn=fn, name=name):
            def inner(slot, slide_no, total, pal, *a, **k):
                context(f"{os.path.basename(script)[:-3]} #{slide_no} {name}")
                return fn(slot, slide_no, total, pal, *a, **k)
            return inner
        modules.MODULES[name] = wrap()
    os.chdir(cwd)
    runpy.run_path(script, run_name="__main__")
    json.dump(list(RECORDS.values()), open(out, "w"))
    print(f"{script}: {len(RECORDS)} text groups -> {out}")


if __name__ == "__main__":
    main()
