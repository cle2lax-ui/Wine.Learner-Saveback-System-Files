"""Font-aware widow check.

Text extracted as plain strings cannot tell a section heading from a label
drawn inside a diagram. This walks the PDF with pdfminer, keeps the font name
and size of every line, and only treats a line as a heading if it is set in one
of the guide's actual heading faces. It then counts the body lines that follow
it on the same page.
"""
import sys, glob
from collections import defaultdict
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LAParams

MIN_LINES = 4
BODY_MIN_SIZE = 8.0          # anything smaller is a diagram label or a footer


def line_info(line):
    if isinstance(line, LTChar):
        return None
    try:
        chars = [c for c in line if isinstance(c, LTChar)]
    except TypeError:
        return None
    if not chars:
        return None
    sizes = defaultdict(float)
    fonts = defaultdict(float)
    for c in chars:
        if c.get_text().strip():
            sizes[round(c.size, 1)] += 1
            fonts[c.fontname.split("+")[-1]] += 1
    if not sizes:
        return None
    size = max(sizes, key=sizes.get)
    font = max(fonts, key=fonts.get)
    return dict(text=line.get_text().strip(), size=size, font=font,
                x=line.x0, y=line.y0)


# The instanced Playfair/Archivo faces keep one internal name per family, so
# weight cannot be read from the font name. Headings are identified instead by
# family + size + case, and by sitting flush on the content column's left edge.
COLUMN_LEFTS = (40.0, 54.0, 222.0)


def on_column(li, tol=3.0):
    return any(abs(li["x"] - L) < tol for L in COLUMN_LEFTS)


def is_heading(li):
    f, s, t = li["font"], li["size"], li["text"]
    if not t or not on_column(li):
        return None
    letters = [ch for ch in t if ch.isalpha()]
    upper = bool(letters) and all(ch.isupper() for ch in letters)
    if "Playfair" in f and s >= 11.0:
        return "section heading"
    if 9.6 <= s <= 10.6 and upper and not t.startswith("\u2022"):
        return "sub-heading"
    if 6.7 <= s <= 7.6 and upper and len(t) > 8:
        return "caption"
    return None


def check(path):
    problems = []
    la = LAParams(line_margin=0.35)
    for pno, page in enumerate(extract_pages(path, laparams=la), 1):
        lines = []
        for el in page:
            if isinstance(el, LTTextContainer):
                for ln in el:
                    li = line_info(ln)
                    if li and li["text"]:
                        lines.append(li)
        lines.sort(key=lambda d: -d["y"])
        # body lines are the ones a reader would count as content
        for i, li in enumerate(lines):
            kind = is_heading(li)
            if not kind:
                continue
            if li["text"].startswith("WSET Level 4"):
                continue
            below = [q for q in lines[i + 1:]
                     if q["size"] >= BODY_MIN_SIZE
                     and not q["text"].startswith("WSET Level 4")]
            # A diagram directly beneath a heading IS its content, but its
            # labels are set below body size and so are not counted above.
            has_graphic = any(q["size"] < BODY_MIN_SIZE for q in lines[i + 1:i + 6])
            if len(below) < MIN_LINES and not has_graphic:
                problems.append((pno, kind, li["text"][:58], len(below)))
    return problems


total = 0
for f in sorted(sys.argv[1:]):
    p = check(f)
    total += len(p)
    name = f.split("/")[-1]
    print(f"{name:<52} {'clean' if not p else str(len(p)) + ' issue(s)'}")
    for pno, kind, txt, n in p:
        print(f"    p{pno:<3} {kind:<24} {n} line(s) below  \u2014 {txt!r}")
print("total:", total)
