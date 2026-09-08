"""Flag any page whose last line is a heading with no content beneath it."""
import re, sys
from pypdf import PdfReader

# A numbered heading carries no further sentence-ending period; that excludes
# numbered prose items inside callout boxes, which are not headings.
HEAD = re.compile(r'^(\d+\.\s+[A-Z][^.]*|[A-Z][A-Z \u2014\u2013\'/,\-]{6,}|Model Answer.*|Sample Examination.*|Short Written Answer.*|Question \d+)$')

def check(path):
    bad = []
    for i, pg in enumerate(PdfReader(path).pages):
        lines = [l.strip() for l in (pg.extract_text() or "").split("\n") if l.strip()]
        # drop the footer line and page number
        lines = [l for l in lines if not l.startswith("WSET Level 4 Diploma")
                 and not re.fullmatch(r'\d{1,2}', l)]
        if not lines:
            continue
        last = lines[-1]
        # a real heading is short; long numbered lines are answer-key entries
        if len(last) <= 70 and HEAD.match(last):
            bad.append((i + 1, last))
    return bad

for f in sys.argv[1:]:
    b = check(f)
    print(f"{f.split('/')[-1]}: " + ("no orphaned headings" if not b else "ORPHANS"))
    for pg, h in b:
        print(f"    p{pg}: {h!r}")

# --- widow check: a heading must carry >= MIN lines of its own content --------
