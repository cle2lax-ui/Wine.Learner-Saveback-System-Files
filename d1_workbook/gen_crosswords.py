# -*- coding: utf-8 -*-
"""Generate the workbook's crosswords once and cache them as JSON (crosswords/ch<N>.json).
Each puzzle is a themed, newspaper-style grid: balanced Across/Down, every word crossing at least two others.
usage: python3 gen_crosswords.py 4 7 10 13 [--seeds 8]"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cw_vocab as CV
from wb import make_crossword5, crossword_stats

WINDOWS = {1: [1], 4: [2, 3, 4], 7: [5, 6, 7], 10: [8, 9, 10], 13: [11, 12, 13], 16: [14, 15, 16], 19: [17, 18, 19]}
HERE = os.path.dirname(os.path.abspath(__file__))


def _run(args):
    pool, size, seed, tries, iters, min_words, max_words = args
    cw = make_crossword5(pool, size=size, seed=seed, tries=tries, iters=iters, min_words=min_words, max_words=max_words)
    st = crossword_stats(cw)
    key = (st["min_cross"] >= 2, st["words"] >= min_words, abs(st["across"] - st["down"]) <= 1, st["crossings"], st["words"])
    return key, seed, cw


def _key(st, min_words=16):
    return (st['min_cross'] >= 2, st['words'] >= min_words, abs(st['across'] - st['down']) <= 1, st['crossings'], st['words'])


def generate(ch, seeds=8, size=13, tries=40, iters=3500, min_words=16, max_words=20, seed0=0):
    pool, cur = CV.pool(WINDOWS[ch])
    jobs = [(pool, size, s, tries, iters, min_words, max_words) for s in range(seed0 + 1, seed0 + seeds + 1)]
    res = [_run(j) for j in jobs]
    res.sort(key=lambda x: x[0], reverse=True)
    key, seed, cw = res[0]
    out = dict(chapter=ch, seed=seed, size=size, placed=[list(x) for x in cw["placed"]], stats=crossword_stats(cw))
    os.makedirs(os.path.join(HERE, "crosswords"), exist_ok=True)
    fn = os.path.join(HERE, "crosswords", "ch%d.json" % ch)
    if os.path.exists(fn):
        old = json.load(open(fn, encoding="utf-8"))["stats"]
        if _key(old, min_words) >= _key(out["stats"], min_words):
            return dict(kept_existing=True, **old)
    json.dump(out, open(fn, "w"), ensure_ascii=False, indent=1)
    return out["stats"]


if __name__ == "__main__":
    seeds = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 8
    skip = ({sys.argv.index("--seeds") + 1} if "--seeds" in sys.argv else set()) | ({sys.argv.index("--seed0") + 1} if "--seed0" in sys.argv else set())
    args = [a for i, a in enumerate(sys.argv) if i > 0 and not a.startswith("--") and i not in skip]
    seed0 = int(sys.argv[sys.argv.index("--seed0") + 1]) if "--seed0" in sys.argv else 0
    args = [a for a in args if a != str(seed0) or "--seed0" not in sys.argv]
    for a in args:
        if a.isdigit():
            t = time.time()
            print("Ch", a, generate(int(a), seeds=seeds, seed0=seed0), "%.0fs" % (time.time() - t), flush=True)
