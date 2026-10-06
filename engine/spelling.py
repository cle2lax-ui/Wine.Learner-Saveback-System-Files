"""House style: AMERICAN ENGLISH (Steve: "Always use American English").

Everything this system writes is American English: slide copy, captions, guides, notes.
This module catches the British forms that actually turn up in wine writing, including the
wine-specific ones (botrytised, sulphite, greywacke, hectolitre) that a general spell-checker
treats as correct. D3 and most wine books are British-English sources, so their wording
creeps in when copy is adapted from them: "per cent", "trebled", "colour".

FUTURE WORK ONLY. Steve's direction is that new work is American English; decks and captions
made before it are NOT rewritten and NOT scanned ("Don't scan earlier decks"). So the build-time
check is OPT-IN: a new deck turns it on, and an earlier deck that is rebuilt never sees it.

TWO USES
  1. Build time, opt-in. A deck script sets AMERICAN_ENGLISH=1 (os.environ.setdefault, before it
     builds). core.QA.add_words() then passes each piece of slide text through scan(); any hit is
     reported as a WARNING in the QA line. AMERICAN_ENGLISH_STRICT=1 makes it a failure instead.
  2. A tool for new copy. `python3 engine/spelling.py PATH [PATH ...]` prints each hit with its
     line number and the American form; `--summary` prints counts per file. Point it at what you
     are writing now, not at earlier decks.

SCOPE AND LIMITS. A curated list, not a dictionary: it will not catch a British spelling that is
not on it, and it can flag a proper noun or a direct quotation of a British source. Quotations
and names stay as written; the warning is a prompt to look, not a verdict. Add a rule to RULES
when a new British form turns up.
"""
import os
import re
import sys

# (regex, American template). \\1 etc. is the matched suffix group where there is one.
RULES = [
    (r"per cent", "percent"),
    (r"colour(s|ed|ing|ful|less|ation)?", r"color\1"),
    (r"flavour(s|ed|ing|ful|less|some)?", r"flavor\1"),
    (r"favour(s|ed|ing|ite|ites|able|ably)?", r"favor\1"),
    (r"honour(s|ed|ing|able)?", r"honor\1"),
    (r"labour(s|ed|ing)?", r"labor\1"),
    (r"neighbour(s|ing|hood|hoods)?", r"neighbor\1"),
    (r"vapour(s)?", r"vapor\1"),
    (r"ageing", "aging"),
    (r"grey(s|ish)?", r"gray\1"),
    (r"greywacke", "graywacke"),
    (r"centre(s|d)?", r"center\1"),
    (r"(hecto|kilo|milli|centi|deci)?litre(s)?", r"\1liter\2"),
    (r"(kilo|milli|centi)?metre(s)?", r"\1meter\2"),
    (r"organis(e|es|ed|ing|ation|ations)", r"organiz\1"),
    (r"recognis(e|es|ed|ing)", r"recogniz\1"),
    (r"realis(e|es|ed|ing)", r"realiz\1"),
    (r"specialis(e|es|ed|ing)", r"specializ\1"),
    (r"summaris(e|es|ed|ing)", r"summariz\1"),
    (r"criticis(e|es|ed|ing|m|ms)", r"criticiz\1"),
    (r"utilis(e|es|ed|ing|ation)", r"utiliz\1"),
    (r"maximis(e|es|ed|ing)", r"maximiz\1"),
    (r"minimis(e|es|ed|ing)", r"minimiz\1"),
    (r"emphasis(e|es|ed|ing)", r"emphasiz\1"),
    (r"stabilis(e|es|ed|ing|ation)", r"stabiliz\1"),
    (r"oxidis(e|es|ed|ing|ation)", r"oxidiz\1"),
    (r"sterilis(e|es|ed|ing|ation)", r"steriliz\1"),
    (r"pasteuris(e|es|ed|ing|ation)", r"pasteuriz\1"),
    (r"homogenis(e|es|ed|ing)", r"homogeniz\1"),
    (r"crystallis(e|es|ed|ing|ation)", r"crystalliz\1"),
    (r"characteris(e|es|ed|ing|ation)", r"characteriz\1"),
    (r"harmonis(e|es|ed|ing|ation)", r"harmoniz\1"),
    (r"standardis(e|es|ed|ing|ation)", r"standardiz\1"),
    (r"optimis(e|es|ed|ing|ation)", r"optimiz\1"),
    (r"prioritis(e|es|ed|ing)", r"prioritiz\1"),
    (r"botrytis(ed|ing)", r"botrytiz\1"),
    (r"analys(e|es|ed|ing)", r"analyz\1"),
    (r"programme(s)?", r"program\1"),
    (r"whilst", "while"),
    (r"co-operative(s)?", r"cooperative\1"),
    (r"treble(d|s)?", r"triple\1"),
    (r"trebling", "tripling"),
    (r"sulphur", "sulfur"),
    (r"sulphite(s)?", r"sulfite\1"),
    (r"sulphide(s)?", r"sulfide\1"),
    (r"sulphate(s)?", r"sulfate\1"),
    (r"mould(s|y|ing)?", r"mold\1"),
    (r"licence(s)?", r"license\1"),
    (r"defence", "defense"),
    (r"practise(d|s)?", r"practice\1"),
    (r"learnt", "learned"),
    (r"catalogue(s)?", r"catalog\1"),
    (r"fulfil", "fulfill"),
    (r"plough(s|ed|ing)?", r"plow\1"),
    (r"tyre(s)?", r"tire\1"),
    (r"maths", "math"),
    # doubled final consonant before -ed/-ing/-er (labelled, travelled, shrivelled...): American drops it
    (r"(label|model|travel|cancel|level|shrivel|fuel|signal|channel|total|marvel|counsel|tunnel|dial|enrol)l(ed|ing|er|ers)", r"\1\2"),
    (r"marvellous", "marvelous"),
    # -our words that turn up in tasting notes and vineyard writing
    (r"(odo|savo|vigo|rigo|humo|rumo|splendo|endeavo|behavio|armo|cando|clamo|fervo|harbo|arbo|parlo|valo|tumo|glamo|savio)ur(s|ed|ing|y|ies|ous|ful|less)?", r"\1r\2"),
    (r"judgement(s)?", r"judgment\1"),
    (r"acknowledgement(s)?", r"acknowledgment\1"),
    (r"enquir(y|ies|ing|ed)", r"inquir\1"),
    (r"scepti(c|cal|cs|cism)", r"skepti\1"),
    (r"aluminium", "aluminum"),
    (r"skilful(ly)?", r"skillful\1"),
    (r"(instal|enrol|fulfil)ment(s)?", r"\1lment\2"),
]
_COMPILED = [(re.compile(r"\b" + p + r"\b", re.IGNORECASE), t) for p, t in RULES]


def _match_case(found, american):
    if found.isupper() and len(found) > 1:
        return american.upper()
    if found[:1].isupper():
        return american[:1].upper() + american[1:]
    return american


def scan(text):
    """Returns [(british_form_as_found, american_suggestion)] for the text."""
    hits = []
    for rx, tmpl in _COMPILED:
        for m in rx.finditer(text or ""):
            hits.append((m.group(0), _match_case(m.group(0), m.expand(tmpl))))
    return hits


def enabled():
    """Opt-in: off unless a new deck (or the person running it) turns it on."""
    return os.environ.get("AMERICAN_ENGLISH") == "1" or strict()


def strict():
    return os.environ.get("AMERICAN_ENGLISH_STRICT") == "1"


def scan_file(path):
    out = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for n, line in enumerate(f, 1):
                for found, am in scan(line):
                    out.append((n, found, am, line.strip()[:90]))
    except OSError:
        pass
    return out


def _main(argv):
    summary = "--summary" in argv
    paths = [a for a in argv if not a.startswith("--")]
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, fs in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
                files += [os.path.join(root, f) for f in fs
                          if f.endswith((".py", ".md", ".txt")) and f != "spelling.py"]  # its rules ARE the British forms
        else:
            files.append(p)
    total = 0
    rows = []
    for f in sorted(files):
        hits = scan_file(f)
        if hits:
            total += len(hits)
            rows.append((f, hits))
    for f, hits in rows:
        if summary:
            print(f"{len(hits):4d}  {f}")
        else:
            for n, found, am, line in hits:
                print(f"{f}:{n}: '{found}' -> '{am}'   | {line}")
    print(f"\n{total} British form(s) in {len(rows)} of {len(files)} file(s) scanned")
    return 1 if (total and strict()) else 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
