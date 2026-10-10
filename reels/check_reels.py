"""Regression guard for locked Reels: re-renders reference frames and compares hashes with REEL_HASHES.json.
Run after any change to reel_lib.py, reel_audio.py, tfg_bumper.py or a Reel's own module (the GTR Reel reuses
all three, so this protects the locked Field Guide Reel from side effects)."""
import hashlib
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reel_lib import finish  # noqa: E402

ref = json.load(open(f"{HERE}/REEL_HASHES.json"))
bad = 0
for mod, frames in ref.items():
    m = importlib.import_module(mod)
    for t, h in frames.items():
        got = hashlib.sha256(finish(m.frame_at(float(t)), int(round(float(t) * 30))).tobytes()).hexdigest()[:24]
        if got != h:
            bad += 1
            print(f"CHANGED  {mod} @ {t}s")
total = sum(len(v) for v in ref.values())
print(f"{total - bad} of {total} locked Reel frames match the reference")
sys.exit(1 if bad else 0)
