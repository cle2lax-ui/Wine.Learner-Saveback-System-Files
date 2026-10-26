# -*- coding: utf-8 -*-
"""Compile the 21 workbook chapters into one master PDF:
cover (after the D1 textbook's front cover), about page, contents, chapters, glossary, spaced-review tracker.
usage: python3 build_master.py [outputs_dir]"""
import io, os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wb import *                                   # fonts, palette, engine
from wb import _p
import wb_ink as K
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Flowable
from reportlab.lib.enums import TA_JUSTIFY
from pypdf import PdfReader, PdfWriter
import glossary_data

OUT = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs"
PW, PH = 612.0, 792.0
CREAM = colors.HexColor("#F6F0E2")
DEEP = colors.HexColor("#3A0C18")
WINE = colors.HexColor("#6B1A2D")

CHAPTERS = [
    (1, "The Vine", "Ch1_The_Vine"), (2, "The Vine Growth Cycle", "Ch2_Vine_Growth_Cycle"),
    (3, "The Growing Environment", "Ch3_The_Growing_Environment"), (4, "Approaches to Grape Growing", "Ch4_Approaches_to_Grape_Growing"),
    (5, "Vineyard Establishment", "Ch5_Vineyard_Establishment"), (6, "Managing Nutrients and Water", "Ch6_Managing_Nutrients_and_Water"),
    (7, "Canopy Management", "Ch7_Canopy_Management"), (8, "Hazards, Pests and Diseases", "Ch8_Hazards_Pests_and_Diseases"),
    (9, "Harvest", "Ch9_Harvest"), (10, "Viticulture Scenarios", "Ch10_Viticulture_Scenarios"),
    (11, "Wine Components", "Ch11_Wine_Components"), (12, "Approaches to Winemaking", "Ch12_Approaches_to_Winemaking"),
    (13, "General Winemaking Options", "Ch13_General_Winemaking_Options"), (14, "Maturation", "Ch14_Maturation"),
    (15, "Finishing and Packaging", "Ch15_Finishing_and_Packaging"),
    (16, "Specific Options for White Winemaking", "Ch16_White_Winemaking"),
    (17, "Specific Options for Producing Wines with Residual Sugar", "Ch17_Residual_Sugar"),
    (18, "Specific Options for Red Winemaking", "Ch18_Red_Winemaking"),
    (19, "Specific Options for Ros\u00e9 Winemaking", "Ch19_Rose_Winemaking"),
    (20, "Specific Options for No- and Low-Alcohol Winemaking", "Ch20_No_Low_Alcohol"),
    (21, "Examples of Winemaking Choices for Different Styles of Wine", "Ch21_Winemaking_Choices_by_Style"),
]


# ====================================================================================== shared page chrome
def chrome(c, pageno, title, right):
    odd = pageno % 2 == 1
    cx = BIND if odd else OUTER
    c.saveState()
    c.setFont("Serif", 8.4); c.setFillColor(SLATE); c.drawString(cx, TOP_Y + 7, title)
    c.setFont("Sans-B", 6.8); c.setFillColor(GOLD); tracked(c, cx + W, TOP_Y + 7.4, "COMPANION WORKBOOK", 1.3, align="r")
    c.setStrokeColor(HAIRLINE); c.setLineWidth(0.6); c.line(cx, TOP_Y + 2, cx + W, TOP_Y + 2)
    c.setLineWidth(0.4); c.line(cx, BOT_Y - 10, cx + W, BOT_Y - 10)
    c.setFont("Sans", 7.5); c.setFillColor(SLATE)
    c.drawString(cx, BOT_Y - 21, "WSET Level 4 Diploma in Wines \u2014 D1: Wine Production \u00b7 Companion Workbook")
    c.setFont("Sans-B", 7.8); c.setFillColor(BURGUNDY); c.drawRightString(cx + W, BOT_Y - 21, right)
    c.restoreState()
    return cx


def one_page(draw, pageno):
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(PW, PH))
    draw(c, pageno)
    c.showPage(); c.save()
    return PdfReader(io.BytesIO(buf.getvalue())).pages[0]


def para(c, text, style, x, y_top, width):
    p = Paragraph(text, style)
    w, h = p.wrap(width, 2000)
    p.drawOn(c, x, y_top - h)
    return h


# ====================================================================================== cover
def draw_cover(c, pageno):
    """Full-bleed photograph, title stack at the lower left, publisher-style block at the foot: the textbook's cover order."""
    from reportlab.lib.utils import ImageReader
    c.drawImage(ImageReader(os.path.join(HERE, "cover", "cover_photo.jpg")), 0, 0, width=PW, height=PH)
    # a small tag at the upper left, standing in for the publisher's mark
    c.setFillColor(BURGUNDY); c.rect(40, PH - 74, 188, 26, stroke=0, fill=1)
    c.setFont("Sans-B", 8.6); c.setFillColor(colors.white); tracked(c, 52, PH - 65, "COMPANION WORKBOOK", 2.0)
    # title block, in the textbook's order: title, edition, accompaniment line
    c.setFillColor(colors.white); c.setFont("Sans-B", 58)
    c.drawString(40, 238, "D1: Wine"); c.drawString(40, 176, "Production")
    c.setFont("Sans-B", 10.5); c.setFillColor(colors.white); tracked(c, 42, 148, "AUGUST 2026 EDITION", 2.2)
    c.setFont("Sans", 13.5); c.drawString(42, 122, "An accompaniment to the")
    c.setFont("Sans-B", 13.5); c.drawString(42, 104, "WSET\u00ae Level 4 Diploma in Wines")
    # publisher-style block at the foot
    c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.55)); c.setLineWidth(0.6); c.line(40, 84, PW - 40, 84)
    c.setFont("Sans-B", 8.4); c.setFillColor(colors.white)
    c.drawString(40, 69, "Companion to D1: Wine Production, August 2026 edition (Issue 1.7)")
    c.setFont("Sans", 7.2); c.setFillColor(colors.Color(1, 1, 1, alpha=0.88))
    lines = ["Chapters 1\u201321: exercises, answer keys, glossary and a spaced-review tracker.",
             "An independent study companion. Not produced, reviewed or endorsed by the Wine & Spirit Education Trust. WSET\u00ae is a registered trademark of the Trust."]
    y = 56
    for ln in lines:
        c.drawString(40, y, ln); y -= 10.6


# ====================================================================================== about page
def draw_about(c, pageno):
    cx = chrome(c, pageno, "D1 \u00b7 About this workbook", "About")
    y = TOP_Y - 14
    c.setFont("Sans-B", 7.2); c.setFillColor(GOLD); tracked(c, cx, y, "READ THIS FIRST", 1.6)
    c.setFont("Serif-B", 24); c.setFillColor(BURGUNDY); c.drawString(cx, y - 30, "About this workbook")
    body = _p("ab_b", fontSize=10.0, leading=14.0, spaceAfter=5)
    h = _p("ab_h", fontName="Sans-B", fontSize=9.4, leading=12, textColor=BURGUNDY, spaceBefore=8, spaceAfter=2)
    items = [
        ("What it is", "A companion to <b>D1: Wine Production</b> in 21 chapters, one for each textbook chapter (Chapter 22 is a reading list and has no workbook). "
                       "Each chapter is a short set of exercises, followed by a one-page answer key and a scorecard. Match, tick, sort, order, label a drawing, "
                       "complete a diagram, fill a calculation, true-or-false with correction, multiple choice and a written \u2018explain it\u2019 with a self-marking checklist."),
        ("How to use a chapter", "<b>1 Attempt</b> in pencil, from memory, with the textbook closed. <b>2 Check</b> against the key at the back of the chapter and correct every miss in ink. "
                                  "<b>3 Revisit</b> what you missed on days 3, 7 and 21 and tick the boxes on the chapter scorecard. The last page of the book collects all 21 chapters in one tracker."),
        ("Marks and the real exam", "Each chapter totals its own points. The live D1 paper is written, not multiple choice: the multiple-choice and tick-box exercises are for finding gaps, "
                                    "and the \u2018explain it\u2019 questions rehearse the answer style the examiners reward: cause and effect, the named reason, and the named example."),
        ("Every third chapter", "Chapters 1, 4, 7, 10, 13, 16 and 19 each include a crossword that reviews the vocabulary of the last three chapters. Every word in each grid crosses at least two others."),
        ("The drawings", "Illustrations are pen-and-ink studies made for this workbook. Where a drawing is used, you are asked to label, name or interpret it, and the answer key tells you what each part shows."),
        ("Glossary", "The glossary at the back covers the whole textbook, Chapters 1\u201321, with the chapter or chapters where each term is taught. The textbook itself has no glossary, "
                     "so these entries are compiled from it: use them for a quick check, and go back to the textbook for the exact wording."),
        ("How the book is laid out", "Every chapter starts on a right-hand page so the punch-side margin stays correct if you print double-sided. Where a chapter ends on a right-hand page, a ruled "
                                     "<b>Notes</b> page follows. Each page carries its chapter and page number (for example 7\u20093) at the foot, and a running page number for the whole book (p. 29, for example) beside it. "
                                     "In a PDF reader, use the bookmarks panel to jump to any chapter, its answer key, or a letter of the glossary."),
    ]
    yy = y - 50
    for ttl, txt in items:
        hh = para(c, ttl, h, cx, yy, W); yy -= hh
        hh = para(c, txt, body, cx, yy, W); yy -= hh
    # source line
    c.setFont("Sans", 8.0); c.setFillColor(SLATE)
    c.drawString(cx, BOT_Y + 6, "Built from the D1: Wine Production textbook, August 2026 edition (Issue 1.7). Independent study aid: not affiliated with or endorsed by WSET.")


# ====================================================================================== contents
def toc_row(c, cx, y, num, title, sub, page):
    c.setFont("Serif-B", 17); c.setFillColor(BURGUNDY); c.drawString(cx, y - 15, str(num))
    tx = cx + 34
    st = _p("toc_t", fontName="Sans-B", fontSize=10.2, leading=12.4)
    avail = W - 34 - 40
    p = Paragraph(title, st); w_, h_ = p.wrap(avail, 60)
    p.drawOn(c, tx, y - 3 - h_)
    last = p.getActualLineWidths0()[-1]
    ly = y - 3 - h_ + 3.4                                          # baseline of the title's last line
    c.setFont("Sans", 7.8); c.setFillColor(SLATE); c.drawString(tx, y - 5 - h_ - 8.4, sub)
    c.setFont("Sans-B", 10.5); c.setFillColor(BURGUNDY); c.drawRightString(cx + W, ly, str(page))
    c.setStrokeColor(HAIRLINE); c.setLineWidth(0.6); c.setDash(0.8, 2.8)
    c.line(tx + last + 8, ly + 0.5, cx + W - 24, ly + 0.5)
    c.setDash(1, 0)
    return h_ + 24


def draw_toc(part):
    def f(c, pageno):
        cx = chrome(c, pageno, "D1 \u00b7 Contents", "Contents")
        y = TOP_Y - 14
        c.setFont("Sans-B", 7.2); c.setFillColor(GOLD); tracked(c, cx, y, "COMPANION WORKBOOK TO D1: WINE PRODUCTION", 1.6)
        c.setFont("Serif-B", 26); c.setFillColor(BURGUNDY); c.drawString(cx, y - 32, "Contents" + ("" if part == 1 else " (continued)"))
        yy = y - 56
        if part == 1:
            yy = band(c, cx, yy, "FRONT MATTER")
            for (t, p) in (("About this workbook", 2), ):
                c.setFont("Sans", 10.2); c.setFillColor(INK); c.drawString(cx + 34, yy - 12, t)
                c.setFont("Sans-B", 10.5); c.setFillColor(BURGUNDY); c.drawRightString(cx + W, yy - 12, str(p)); yy -= 24
            yy = band(c, cx, yy - 4, "PART ONE  \u00b7  VITICULTURE   (Chapters 1\u201310)")
            for n, title, sub, pg in PLAN_ROWS[:10]:
                yy -= toc_row(c, cx, yy, n, title, sub, pg)
        else:
            yy = band(c, cx, yy, "PART TWO  \u00b7  WINEMAKING   (Chapters 11\u201321)")
            for n, title, sub, pg in PLAN_ROWS[10:]:
                yy -= toc_row(c, cx, yy, n, title, sub, pg)
            yy = band(c, cx, yy - 6, "BACK MATTER")
            for (t, p) in (("Glossary of terms", PLAN["glossary"]), ("Spaced-review tracker", PLAN["tracker"])):
                c.setFont("Sans", 10.2); c.setFillColor(INK); c.drawString(cx + 34, yy - 12, t)
                c.setFont("Sans-B", 10.5); c.setFillColor(BURGUNDY); c.drawRightString(cx + W, yy - 12, str(p)); yy -= 24
            c.setFont("Sans", 8.0); c.setFillColor(SLATE)
            c.drawString(cx, BOT_Y + 6, "Page numbers are the running numbers (p. 29) at the foot of each page, left of the chapter label. Chapter 22 of the textbook is a reading list and has no workbook chapter.")
    return f


def band(c, cx, y, text):
    c.setFillColor(colors.HexColor("#F1E9D6")); c.rect(cx, y - 17, W, 17, stroke=0, fill=1)
    c.setFont("Sans-B", 7.4); c.setFillColor(BURGUNDY); tracked(c, cx + 8, y - 12, text, 1.5)
    return y - 24


# ====================================================================================== notes page
def draw_notes(chap_prev):
    def f(c, pageno):
        cx = chrome(c, pageno, "D1 \u00b7 Notes", "Notes")
        c.setFont("Sans-B", 7.2); c.setFillColor(GOLD); tracked(c, cx, TOP_Y - 14, "AFTER CHAPTER %d" % chap_prev, 1.6)
        c.setFont("Serif-B", 22); c.setFillColor(BURGUNDY); c.drawString(cx, TOP_Y - 42, "Notes")
        y = TOP_Y - 70
        for head, nlines in (("The three facts I keep forgetting", 4), ("Questions to ask the textbook", 5), ("My own summary, in my own words", 14)):
            c.setFont("Sans-B", 8.4); c.setFillColor(BURGUNDY); c.drawString(cx, y, head); y -= 7
            c.setStrokeColor(FEINT); c.setLineWidth(0.5)
            for i in range(nlines):
                y -= 22
                c.line(cx, y, cx + W, y)
            y -= 20
    return f


# ====================================================================================== tracker
def draw_tracker(c, pageno):
    cx = chrome(c, pageno, "D1 \u00b7 Spaced-review tracker", "Tracker")
    c.setFont("Sans-B", 7.2); c.setFillColor(GOLD); tracked(c, cx, TOP_Y - 14, "ALL 21 CHAPTERS ON ONE PAGE", 1.6)
    c.setFont("Serif-B", 22); c.setFillColor(BURGUNDY); c.drawString(cx, TOP_Y - 42, "Spaced-review tracker")
    c.setFont("Sans", 8.6); c.setFillColor(SLATE)
    c.drawString(cx, TOP_Y - 58, "Write each first-attempt score, then tick Day 1 (check against the key), Day 3, Day 7 and Day 21 as you revisit the chapter.")
    y = TOP_Y - 78
    cols = [("CH", 24), ("TITLE", 190), ("SCORE", 66), ("DAY 1", 38), ("DAY 3", 38), ("DAY 7", 38), ("DAY 21", 42), ("WEAK SPOTS", 0)]
    x = cx
    xs = []
    c.setFont("Sans-B", 6.8); c.setFillColor(SLATE)
    for name, wd in cols:
        xs.append(x); c.drawString(x + 2, y, name); x += wd if wd else 0
    wk = xs[-1]
    c.setStrokeColor(INK); c.setLineWidth(1.0); c.line(cx, y + 9, cx + W, y + 9); c.setLineWidth(0.6); c.line(cx, y - 4, cx + W, y - 4)
    rh = 24.5
    for i, (n, title, fn) in enumerate(CHAPTERS):
        yy = y - 4 - (i + 1) * rh
        c.setStrokeColor(FEINT); c.setLineWidth(0.4); c.line(cx, yy, cx + W, yy)
        c.setFont("Serif-B", 12); c.setFillColor(BURGUNDY); c.drawString(xs[0] + 2, yy + 9, str(n))
        short = {16: "White Winemaking", 17: "Wines with Residual Sugar", 18: "Red Winemaking", 19: "Ros\u00e9 Winemaking",
                 20: "No- and Low-Alcohol Winemaking", 21: "Winemaking Choices by Style"}.get(n, title)
        c.setFont("Sans", 8.4); c.setFillColor(INK); c.drawString(xs[1] + 2, yy + 9.5, short)
        c.setFont("Sans", 8.0); c.setFillColor(SLATE); c.drawString(xs[2] + 22, yy + 9.5, "/ %s" % PTS.get(n, ""))
        c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(xs[2] + 2, yy + 8, xs[2] + 20, yy + 8)
        for k in (3, 4, 5, 6):
            c.setStrokeColor(INK); c.setLineWidth(0.7); c.rect(xs[k] + 8, yy + 5, 11, 11, stroke=1, fill=0)
    yy = y - 4 - 22 * rh - 4
    c.setFont("Sans-B", 8.4); c.setFillColor(BURGUNDY); c.drawString(xs[1] + 2, yy - 6, "TOTAL")
    c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(xs[2] + 2, yy - 8, xs[2] + 20, yy - 8)
    c.setFont("Sans", 8.0); c.setFillColor(SLATE); c.drawString(xs[2] + 22, yy - 8, "/ %d" % sum(PTS.values()))


# ====================================================================================== glossary
class _GDoc(BaseDocTemplate):
    def handle_pageBegin(self):
        BaseDocTemplate.handle_pageBegin(self)
        self.handle_nextPageTemplate("godd" if (self.page + 1) % 2 == 1 else "geven")


class LetterHead(Flowable):
    def __init__(self, letter):
        Flowable.__init__(self); self.letter = letter
    def wrap(self, aw, ah):
        return (aw, 27)
    def draw(self):
        c = self.canv
        doc = self.canv._doc if hasattr(self.canv, "_doc") else None
        c.setFont("Serif-B", 19); c.setFillColor(BURGUNDY); c.drawString(0, 8, self.letter)
        c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(22, 12, self.width_ if hasattr(self, "width_") else 240, 12)


def build_glossary(first_page_parity_odd=True):
    ents = glossary_data.entries()
    buf = io.BytesIO()
    TOPG = TOP_Y - 8
    gap = 18.0
    cw = (W - gap) / 2.0
    state = {"letters": {}}

    def frames(cx, top):
        return [Frame(cx, BOT_Y + 8, cw, top - (BOT_Y + 8), leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="c1"),
                Frame(cx + cw + gap, BOT_Y + 8, cw, top - (BOT_Y + 8), leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="c2")]

    def page_cb(canv, doc):
        chrome(canv, doc.page, "D1 \u00b7 Glossary of terms", "Glossary\u2009\u00b7\u2009%d" % doc.page)

    def first_cb(canv, doc):
        page_cb(canv, doc)
        cx = BIND
        canv.setFont("Sans-B", 7.2); canv.setFillColor(GOLD); tracked(canv, cx, TOP_Y - 14, "THE WHOLE TEXTBOOK, CHAPTERS 1\u201321", 1.6)
        canv.setFont("Serif-B", 26); canv.setFillColor(BURGUNDY); canv.drawString(cx, TOP_Y - 44, "Glossary of terms")
        canv.setFont("Sans", 8.4); canv.setFillColor(SLATE)
        canv.drawString(cx, TOP_Y - 60, "Compiled from the textbook. The number after each entry is the chapter or chapters where the term is taught.")

    doc = _GDoc(buf, pagesize=(PW, PH), leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0)
    odd_f, even_f = frames(BIND, TOPG), frames(OUTER, TOPG)
    first_f = frames(BIND, TOP_Y - 72)
    doc.addPageTemplates([PageTemplate(id="gfirst", frames=first_f, onPage=first_cb),
                          PageTemplate(id="godd", frames=odd_f, onPage=page_cb),
                          PageTemplate(id="geven", frames=even_f, onPage=page_cb)])
    ent_st = _p("g_e", fontSize=8.5, leading=10.8, spaceAfter=3.0, alignment=0)
    story = []

    class Mark(Flowable):
        def __init__(self, letter):
            Flowable.__init__(self); self.letter = letter
        def wrap(self, aw, ah):
            return (aw, 24)
        def draw(self):
            c = self.canv
            state["letters"].setdefault(self.letter, self._doc_page)
            c.setFont("Serif-B", 17); c.setFillColor(BURGUNDY); c.drawString(0, 6, self.letter)
            c.setStrokeColor(GOLD); c.setLineWidth(0.8); c.line(20, 10, cw, 10)
        _doc_page = 0
    cur = None
    marks = []
    for (t, d, ch) in ents:
        letter = t[0].upper()
        import unicodedata
        letter = unicodedata.normalize("NFKD", letter).encode("ascii", "ignore").decode().upper() or letter
        if letter != cur:
            cur = letter
            m = Mark(letter); marks.append(m)
            story.append(KeepTogetherLetter(m))
        story.append(Paragraph("<b><font color=\"%s\">%s</font></b> \u2014 %s <font name=\"Sans-B\" size=\"6.6\" color=\"%s\">\u00a0CH\u00a0%s</font>"
                               % (hexc(BURGUNDY), t, d, hexc(GOLD), ch), ent_st))
    doc._marks = marks

    class _Rec(BaseDocTemplate):
        pass
    # record the page each letter lands on
    def after_flowable(f):
        if isinstance(f, KeepTogetherLetter):
            state["letters"].setdefault(f.mark.letter, doc.page)
    doc.afterFlowable = after_flowable
    doc.build(story)
    return buf.getvalue(), state["letters"]


class KeepTogetherLetter(Flowable):
    """A letter heading that never sits alone at the foot of a column (keeps with the next entry)."""
    def __init__(self, mark):
        Flowable.__init__(self); self.mark = mark; self.keepWithNext = True
    def wrap(self, aw, ah):
        self.mark._doc_page = 0
        return self.mark.wrap(aw, ah)
    def draw(self):
        self.mark.canv = self.canv
        self.mark.draw()


# ====================================================================================== assemble
def chapter_points(reader):
    t = reader.pages[-1].extract_text() or ""
    m = re.findall(r"/\s*(\d+)", t[t.find("SCORECARD"):]) if "SCORECARD" in t.upper() else re.findall(r"/\s*(\d+)", t)
    return int(m[-1]) if m else 0


def main():
    global PLAN, PLAN_ROWS, PTS
    readers = {}
    PTS = {}
    for n, title, fn in CHAPTERS:
        r = PdfReader(os.path.join(OUT, "D1_Workbook_%s.pdf" % fn))
        readers[n] = r
        PTS[n] = chapter_points(r)
    # ---- the plan: where everything lands
    start = 5                                          # cover 1, about 2, contents 3-4
    starts, notes_after = {}, []
    page = start
    for n, title, fn in CHAPTERS:
        assert page % 2 == 1
        starts[n] = page
        page += len(readers[n].pages)
        if n < 21 and page % 2 == 0:                   # next chapter must start on a right-hand page
            notes_after.append((n, page)); page += 1
    if page % 2 == 0:                                  # glossary starts on a right-hand page
        notes_after.append((21, page)); page += 1
    gloss_start = page
    gl_bytes, letters = build_glossary()
    gl_reader = PdfReader(io.BytesIO(gl_bytes))
    tracker_page = gloss_start + len(gl_reader.pages)
    total = tracker_page
    PLAN = {"glossary": gloss_start, "tracker": tracker_page}
    PLAN_ROWS = []
    for n, title, fn in CHAPTERS:
        npg = len(readers[n].pages)
        s = starts[n]
        PLAN_ROWS.append((n, title.replace("&", "&amp;"),
                          "Exercises pp. %d\u2013%d  \u00b7  Answer key p. %d  \u00b7  %d points" % (s, s + npg - 2, s + npg - 1, PTS[n]), s))
    # ---- write the master
    w = PdfWriter()
    w.add_page(one_page(draw_cover, 1))
    w.add_page(one_page(draw_about, 2))
    w.add_page(one_page(draw_toc(1), 3))
    w.add_page(one_page(draw_toc(2), 4))
    notes_map = dict(notes_after)
    pno = 5
    for n, title, fn in CHAPTERS:
        for p in readers[n].pages:
            w.add_page(p); pno += 1
        if n in notes_map and notes_map[n] == pno:
            w.add_page(one_page(draw_notes(n), pno)); pno += 1
    assert pno == gloss_start, (pno, gloss_start)
    for p in gl_reader.pages:
        w.add_page(p); pno += 1
    w.add_page(one_page(draw_tracker, pno)); pno += 1
    assert pno - 1 == total
    # ---- the running folio, centered at the foot of every page but the cover
    obuf = io.BytesIO()
    oc = rl_canvas.Canvas(obuf, pagesize=(PW, PH))
    for i in range(1, total + 1):
        if i > 1:
            cxp = BIND if i % 2 == 1 else OUTER
            oc.setFont("Sans", 7.6); oc.setFillColor(SLATE); oc.drawRightString(cxp + W - 64, BOT_Y - 21, "p.\u2009%d" % i)
        oc.showPage()
    oc.save()
    ov = PdfReader(io.BytesIO(obuf.getvalue()))
    for i, page in enumerate(w.pages):
        page.merge_page(ov.pages[i])
    # ---- bookmarks
    w.add_outline_item("Cover", 0)
    w.add_outline_item("About this workbook", 1)
    w.add_outline_item("Contents", 2)
    p1 = w.add_outline_item("Part One \u00b7 Viticulture (Chapters 1\u201310)", starts[1] - 1)
    p2 = w.add_outline_item("Part Two \u00b7 Winemaking (Chapters 11\u201321)", starts[11] - 1)
    for n, title, fn in CHAPTERS:
        par = p1 if n <= 10 else p2
        ci = w.add_outline_item("%d  %s" % (n, title), starts[n] - 1, parent=par)
        w.add_outline_item("Exercises", starts[n] - 1, parent=ci)
        w.add_outline_item("Answer key", starts[n] + len(readers[n].pages) - 2, parent=ci)
    g = w.add_outline_item("Glossary of terms", gloss_start - 1)
    for L in sorted(letters):
        w.add_outline_item(L, gloss_start - 1 + letters[L] - 1, parent=g)
    w.add_outline_item("Spaced-review tracker", tracker_page - 1)
    w.add_metadata({"/Title": "D1: Wine Production \u2014 Companion Workbook (Chapters 1\u201321)",
                    "/Subject": "WSET Level 4 Diploma in Wines, Unit D1: exercises, answer keys and glossary",
                    "/Author": "Independent study companion", "/Keywords": "WSET, D1, wine production, workbook, glossary"})
    w.page_mode = "/UseOutlines"
    out = os.path.join(OUT, "D1_Wine_Production_Companion_Workbook_MASTER.pdf")
    with open(out, "wb") as fh:
        w.write(fh)
    print("master: %d pages -> %s" % (total, out))
    print("chapter starts:", starts)
    print("notes pages after chapters:", notes_after, "| glossary p.%d (%d pp) | tracker p.%d" % (gloss_start, len(gl_reader.pages), tracker_page))
    print("points:", PTS, "total", sum(PTS.values()))


if __name__ == "__main__":
    main()
