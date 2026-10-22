"""Brevity count: EVERY visible word per slide (the layout QA counts only what a module registers, which understates tables and tiles).
Records every text call while the deck builds, merges letter-spaced text (drawn one character at a time), drops duplicate blocks, and
leaves out only the footer furniture (READ MORE, page number) and the photo-credit line. Usage: python3 brevity_count.py [module] [--copy]
The Field Guide budget is 70 words per slide (Mosel benchmark: 725 total; Mendocino: 561)."""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
os.environ.setdefault("AMERICAN_ENGLISH", "1")
from PIL import ImageDraw
import importlib, modules
R = importlib.import_module(next((a for a in sys.argv[1:] if not a.startswith("--")), "render_fg_climate"))
texts = collections.defaultdict(list); cur = {"i": 0}
orig = ImageDraw.ImageDraw.text
def rec(self, xy, text, *a, **k):
    texts[cur["i"]].append(str(text)); return orig(self, xy, text, *a, **k)
ImageDraw.ImageDraw.text = rec
names = {}
for i, (name, slot) in enumerate(R.SLIDES, 1):
    cur["i"] = i; names[i] = name; slot = dict(slot); fac = slot.pop("_factor", None)
    img = modules.MODULES[name](slot, i, len(R.SLIDES), R.PAL); cur["i"] = 0
    if fac and hasattr(R, "_badge"): R._badge(img, *fac)
def merge(calls):
    out, run = [], []
    for t in calls:
        if len(t) == 1: run.append(t)
        else:
            if run: out.append("".join(run)); run = []
            out.append(t)
    if run: out.append("".join(run))
    return out
def dedupe(L):
    ch = True
    while ch:
        ch = False
        for n in range(6, 0, -1):
            for i in range(len(L) - 2 * n + 1):
                if L[i:i + n] == L[i + n:i + 2 * n]: L = L[:i + n] + L[i + 2 * n:]; ch = True; break
            if ch: break
    return L
furniture = lambda t: t.strip().startswith("READ MORE") or re.fullmatch(r"\d{2}/\d{2}", t.strip()) or "Wikimedia" in t or "/ Pexels" in t
total, over = 0, 0
print(f"{'#':>2} {'layout':15s} {'words':>5}")
for i in sorted(k for k in texts if k):
    L = [t for t in dedupe(merge(texts[i])) if t.strip() and not furniture(t)]
    w = sum(len(t.split()) for t in L); total += w; over += w > 70
    print(f"{i:>2} {names[i]:15s} {w:>5} {'OVER' if w > 70 else ''}")
    if "--copy" in sys.argv: print("     " + "  |  ".join(L))
print(f"TOTAL {total}; slides over 70: {over}")
