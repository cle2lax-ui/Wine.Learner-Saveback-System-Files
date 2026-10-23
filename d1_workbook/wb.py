# -*- coding: utf-8 -*-
"""D1 Companion Workbook -- layout engine.

US Letter, full-width pages with mirrored punch-side margins (like the Mastery Guide's
exam pages). Same fonts, palette and line weights as the Mastery Guide, so the two
documents read as one family.

Each exercise mechanic is a small function or Flowable. Content files describe an
exercise once; the same call registers its answers with the chapter's answer key, so the
exercise and its key can never drift apart.
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "d1_mastery"))
sys.path.insert(0, HERE)

from mastery import (INK, BURGUNDY, GOLD, SLATE, MUTE, HAIRLINE, FEINT, RULE, BOXFILL, BANDFILL,
                     BOXEDGE, LINE_HAIR, LINE_RULE, LINE_BOLD, BIND, OUTER, TOP_Y, BOT_Y, FULL_W,
                     tracked, tracked_width, _p)
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, Flowable, PageBreak)

W = FULL_W                      # 518 pt of usable width on every page
ANS = BURGUNDY                  # answers are always printed in the accent colour

# ------------------------------------------------------------------ styles
WS = {
    "instr": _p("w_instr", fontName="Sans-I", fontSize=9.4, leading=12.6, textColor=SLATE,
                spaceBefore=3, spaceAfter=7, keepWithNext=1),
    "body":  _p("w_body", fontSize=10.0, leading=13.4, spaceAfter=4),
    "cell":  _p("w_cell", fontSize=9.6, leading=12.4),
    "cellb": _p("w_cellb", fontName="Sans-B", fontSize=9.6, leading=12.4, textColor=BURGUNDY),
    "cellc": _p("w_cellc", fontSize=9.4, leading=12.0, alignment=TA_CENTER),
    "hdr":   _p("w_hdr", fontName="Sans-B", fontSize=7.4, leading=9.6, textColor=SLATE),
    "small": _p("w_small", fontSize=8.6, leading=11.2, textColor=SLATE),
    "q":     _p("w_q", fontSize=10.0, leading=13.0),
    "opt":   _p("w_opt", fontSize=9.6, leading=12.2),
    "cloze": _p("w_cloze", fontSize=10.2, leading=23, spaceAfter=2),
    "key":   _p("w_key", fontSize=8.6, leading=11.0, spaceAfter=1.6),
    "keyc":  _p("w_keyc", fontSize=8.4, leading=10.2),
    "keyh":  _p("w_keyh", fontName="Sans-B", fontSize=8.8, leading=11.0, textColor=BURGUNDY,
                spaceBefore=4.5, spaceAfter=1.5, keepWithNext=1),
    "title": _p("w_title", fontName="Serif-B", fontSize=21, leading=24, textColor=BURGUNDY),
    "sub":   _p("w_sub", fontSize=10.4, leading=13.6, textColor=SLATE, spaceAfter=6),
}


def hexc(col):
    return "#%02X%02X%02X" % (int(col.red * 255), int(col.green * 255), int(col.blue * 255))


def instr(text):
    return Paragraph(text, WS["instr"])


# =================================================================== page frame
def _page(canv, doc):
    canv.saveState()
    pno = doc.page
    odd = pno % 2 == 1
    cx = BIND if odd else OUTER
    canv.setFont("Serif", 8.4); canv.setFillColor(SLATE)
    canv.drawString(cx, TOP_Y + 7, doc._wb_title)
    canv.setFont("Sans-B", 6.8); canv.setFillColor(GOLD)
    tracked(canv, cx + W, TOP_Y + 7.4, "COMPANION WORKBOOK", 1.3, align="r")
    canv.setStrokeColor(HAIRLINE); canv.setLineWidth(0.6)
    canv.line(cx, TOP_Y + 2, cx + W, TOP_Y + 2)
    canv.setLineWidth(0.4)
    canv.line(cx, BOT_Y - 10, cx + W, BOT_Y - 10)
    canv.setFont("Sans", 7.5); canv.setFillColor(SLATE)
    canv.drawString(cx, BOT_Y - 21,
                    "WSET Level 4 Diploma in Wines \u2014 D1: Wine Production \u00b7 Companion Workbook")
    canv.setFont("Sans-B", 7.8); canv.setFillColor(BURGUNDY)
    canv.drawRightString(cx + W, BOT_Y - 21, "%s\u2009\u00b7\u2009%d" % (doc._wb_chap, pno))
    canv.restoreState()


class KeyMarker(Flowable):
    """Zero-size flowable: everything after it (from the next page) is laid out as the two-column key."""
    def __init__(self, chap, title, items):
        Flowable.__init__(self); self.chap, self.title, self.items = chap, title, items

    def wrap(self, aw, ah):
        return (0, 0)

    def draw(self):
        pass


KEY_BOTTOM = 118          # height reserved at the foot of the key page for the scorecard
KEY_TOP = 58              # height reserved at the head for the title block
COLW = (W - 18) / 2.0


class _Doc(BaseDocTemplate):
    _key_mode = False

    def handle_pageBegin(self):
        BaseDocTemplate.handle_pageBegin(self)
        nxt = self.page + 1
        self.handle_nextPageTemplate(("k" if self._key_mode else "") + ("odd" if nxt % 2 == 1 else "even"))

    def afterFlowable(self, f):
        if isinstance(f, KeyMarker):
            self._key_mode = True
            self._key_info = (f.chap, f.title, f.items)
            self._key_first = self.page + 1
            nxt = self.page + 1
            self.handle_nextPageTemplate("k" + ("odd" if nxt % 2 == 1 else "even"))


def _page_key(canv, doc):
    _page(canv, doc)
    if doc.page != getattr(doc, "_key_first", -1):
        return
    chap, title, items = doc._key_info
    odd = doc.page % 2 == 1
    cx = BIND if odd else OUTER
    canv.saveState()
    canv.setFont("Sans-B", 7.2); canv.setFillColor(GOLD); tracked(canv, cx, TOP_Y - 11, "ANSWER KEY", 1.6)
    canv.setFont("Serif-B", 16); canv.setFillColor(BURGUNDY)
    canv.drawString(cx, TOP_Y - 30, "Chapter %s \u2014 %s" % (chap, title))
    canv.setFont("Sans", 8.6); canv.setFillColor(SLATE)
    canv.drawString(cx, TOP_Y - 44, "Mark in a different color. For every miss, note why before moving on \u2014 "
                                   "a wrong answer you understand beats a right one you guessed.")
    canv.setStrokeColor(INK); canv.setLineWidth(LINE_BOLD); canv.line(cx, TOP_Y - 50, cx + W, TOP_Y - 50)
    sc = Scorecard(items)
    sc.wrap(W, 200)
    sc.drawOn(canv, cx, BOT_Y + 2)
    canv.restoreState()


def build_pdf(path, chap, title, story):
    doc = _Doc(path, pagesize=letter, leftMargin=OUTER, rightMargin=OUTER,
               topMargin=letter[1] - TOP_Y, bottomMargin=BOT_Y,
               title="D1 Workbook \u2014 Chapter %s" % chap, author="D1 Companion Workbook")
    doc._wb_title, doc._wb_chap = "D1 \u00b7 Chapter %s \u2014 %s \u00b7 Workbook" % (chap, title), chap
    tm = []
    for tid, x in (("odd", BIND), ("even", OUTER)):
        fr = Frame(x, BOT_Y, W, TOP_Y - BOT_Y, id=tid, leftPadding=0, rightPadding=0,
                   topPadding=0, bottomPadding=0)
        tm.append(PageTemplate(id=tid, frames=[fr], onPage=_page))
    kh = TOP_Y - KEY_TOP - (BOT_Y + KEY_BOTTOM)
    for tid, x in (("kodd", BIND), ("keven", OUTER)):
        frs = [Frame(x + k * (COLW + 18), BOT_Y + KEY_BOTTOM, COLW, kh, id="%s%d" % (tid, k), leftPadding=0,
                     rightPadding=0, topPadding=0, bottomPadding=0) for k in (0, 1)]
        tm.append(PageTemplate(id=tid, frames=frs, onPage=_page_key))
    doc.addPageTemplates(tm)
    doc.build(story)
    from pypdf import PdfReader
    return len(PdfReader(path).pages)


# =================================================================== small parts
def _bubble(c, x, y, label, r=6.3, fill=None, txt=INK):
    c.setLineWidth(0.7); c.setStrokeColor(INK)
    if fill is not None:
        c.setFillColor(fill); c.circle(x, y, r, stroke=1, fill=1)
    else:
        c.circle(x, y, r, stroke=1, fill=0)
    c.setFont("Sans-B", 6.9); c.setFillColor(txt)
    c.drawCentredString(x, y - 2.4, label)


class Bubble(Flowable):
    def __init__(self, label, r=6.3):
        Flowable.__init__(self); self.label, self.r = label, r

    def wrap(self, aw, ah):
        return (self.r * 2 + 2, self.r * 2 + 2)

    def draw(self):
        _bubble(self.canv, self.r + 1, self.r + 1, self.label, self.r)


class AnsBox(Flowable):
    """A small empty box to write a letter or number into."""
    def __init__(self, w=26, h=17, text=None):
        Flowable.__init__(self); self.w, self.h, self.text = w, h, text

    def wrap(self, aw, ah):
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        c.setStrokeColor(INK); c.setLineWidth(0.7); c.roundRect(0, 0, self.w, self.h, 2.5, stroke=1, fill=0)
        if self.text:
            c.setFont("Sans-B", 10); c.setFillColor(ANS); c.drawCentredString(self.w / 2, 4.6, self.text)


class FillCell(Flowable):
    """A tinted write-in area (compare grids, chains)."""
    def __init__(self, w, h=26, text=None, lines=1):
        Flowable.__init__(self); self.w, self.h, self.text, self.lines = w, h, text, lines

    def wrap(self, aw, ah):
        self.w = min(self.w, aw) if self.w else aw
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        if self.text is None:
            c.setStrokeColor(colors.HexColor("#B9BCC0")); c.setLineWidth(0.5)
            for i in range(self.lines):
                y = 5 + i * 13.0
                c.line(0, y, self.w, y)
        else:
            p = Paragraph('<font color="%s"><b>%s</b></font>' % (hexc(ANS), self.text), WS["cell"])
            pw, ph = p.wrap(self.w, 200)
            p.drawOn(c, 0, max(self.h - ph, 0))


class LineFill(Flowable):
    """'Label: ________' on one line."""
    def __init__(self, label, w=W, text=None, h=17, size=8.4):
        Flowable.__init__(self); self.label, self.w, self.text, self.h, self.size = label, w, text, h, size

    def wrap(self, aw, ah):
        self.w = min(self.w, aw)
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        c.setFont("Sans", self.size); c.setFillColor(SLATE)
        lw = c.stringWidth(self.label, "Sans", self.size)
        c.drawString(0, 5.4, self.label)
        c.setStrokeColor(INK); c.setLineWidth(0.5)
        c.line(lw + 4, 3.5, self.w, 3.5)
        if self.text:
            c.setFont("Sans-B", self.size + 0.6); c.setFillColor(ANS)
            c.drawString(lw + 8, 5.4, self.text)


class WriteBox(Flowable):
    """Ruled writing space."""
    def __init__(self, h, label=None, w=W, gap=19.5, border=False):
        Flowable.__init__(self); self.h, self.w, self.label, self.gap, self.border = h, w, label, gap, border
        self.spaceBefore = 0

    def wrap(self, aw, ah):
        self.w = min(self.w, aw)
        return (self.w, self.h)

    def draw(self):
        c = self.canv
        if self.border:
            c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_RULE)
            c.roundRect(0, 0, self.w, self.h, 3, stroke=1, fill=0)
        c.setStrokeColor(RULE); c.setLineWidth(0.5)
        y = self.h - self.gap
        while y > 3:
            c.line(6 if self.border else 0, y, self.w - (6 if self.border else 0), y)
            y -= self.gap
        if self.label:
            c.setFont("Sans-B", 6.3); c.setFillColor(MUTE)
            tracked(c, 8 if self.border else 0, self.h - 9, self.label, 1.0)


# =================================================================== headers
class ExHeader(Flowable):
    """Exercise banner: mechanic chip, exercise number, title, score box."""
    def __init__(self, num, kind, title, pts, mins=None, ref=None):
        Flowable.__init__(self)
        self.num, self.kind, self.title, self.pts, self.mins, self.ref = num, kind, title, pts, mins, ref
        self.keepWithNext = 1
        self.spaceBefore = 15; self.spaceAfter = 0

    def wrap(self, aw, ah):
        self.w = aw
        return (aw, 40)

    def draw(self):
        c, w = self.canv, self.w
        c.setStrokeColor(INK); c.setLineWidth(LINE_BOLD); c.line(0, 39, w, 39)
        c.setFont("Sans-B", 6.6)
        tw = tracked_width(c, self.kind, 1.0)
        c.setFillColor(BURGUNDY); c.roundRect(0, 22.0, tw + 12, 12.8, 2.2, stroke=0, fill=1)
        c.setFillColor(colors.white); tracked(c, 6, 25.9, self.kind, 1.0)
        c.setFont("Sans-B", 7.0); c.setFillColor(GOLD)
        tracked(c, tw + 20, 25.9, "EXERCISE %s" % self.num, 1.2)
        c.setFont("Serif-B", 13.2); c.setFillColor(BURGUNDY); c.drawString(0, 5.5, self.title)
        bw, bh = 96, 26
        x0 = w - bw
        c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_RULE); c.roundRect(x0, 3.5, bw, bh, 3, stroke=1, fill=0)
        c.setFont("Sans-B", 5.8); c.setFillColor(MUTE); tracked(c, x0 + 7, 22.0, "SCORE", 1.0)
        c.setFont("Sans-B", 10.2); c.setFillColor(SLATE); c.drawRightString(x0 + bw - 8, 8.6, "/ %s" % self.pts)
        c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(x0 + 9, 9.4, x0 + bw - 34, 9.4)
        meta = "  \u00b7  ".join(x for x in ((("%s MIN" % self.mins) if self.mins else None), self.ref) if x)
        if meta:
            c.setFont("Sans-B", 6.4); c.setFillColor(MUTE)
            tracked(c, x0 - 10, 25.9, meta.upper(), 0.9, align="r")


# =================================================================== word bank
class WordBank(Flowable):
    def __init__(self, words, ncols=5, label="WORD BANK"):
        Flowable.__init__(self)
        self.words, self.ncols, self.label = words, ncols, label
        self.rows = int(math.ceil(len(words) / float(ncols)))
        self.spaceAfter = 8

    def wrap(self, aw, ah):
        self.w = aw
        self.h = 22 + self.rows * 16
        return (aw, self.h)

    def draw(self):
        c = self.canv
        c.setFillColor(BOXFILL); c.setStrokeColor(BOXEDGE); c.setLineWidth(0.6)
        c.roundRect(0, 0, self.w, self.h, 3, stroke=1, fill=1)
        c.setFont("Sans-B", 6.4); c.setFillColor(GOLD); tracked(c, 10, self.h - 12, self.label, 1.3)
        cw = (self.w - 20) / float(self.ncols)
        for i, wd in enumerate(self.words):
            r, k = divmod(i, self.ncols)
            x, y = 10 + k * cw, self.h - 30 - r * 16
            c.setStrokeColor(MUTE); c.setLineWidth(0.6); c.circle(x + 3.6, y + 3.3, 3.3, stroke=1, fill=0)
            c.setFont("Sans", 9.4); c.setFillColor(INK); c.drawString(x + 11, y, wd)


# =================================================================== cloze
_NB = " "   # no-break space


def blank(n, w=78, key=None):
    """A numbered, underlined blank. Used inside Paragraph markup."""
    from reportlab.pdfbase import pdfmetrics
    num = '<font name="Sans-B" size="6.8" color="%s">(%s)</font>' % (hexc(GOLD), n)
    if key is not None:
        return num + "&nbsp;<font name=\"Sans-B\" color=\"%s\"><u>%s</u></font>" % (hexc(ANS), key)
    sp = pdfmetrics.stringWidth(" ", "Sans", 10.2)
    return num + "&nbsp;<u>" + "&nbsp;" * int(w / sp) + "</u>"


def cloze(paragraphs, start=1, width=78):
    """paragraphs: strings with {{answer}} markers. Returns (flowables, answers)."""
    n = start
    flows, answers = [], []
    for txt in paragraphs:
        out = ""
        while "{{" in txt:
            a, rest = txt.split("{{", 1)
            ans, txt = rest.split("}}", 1)
            w = max(width, 6.2 * len(ans) + 14)
            out += a + blank(n, w=w)
            answers.append(ans)
            n += 1
        out += txt
        flows.append(Paragraph(out, WS["cloze"]))
    return flows, answers


# =================================================================== matching
def match(left, right, answer):
    """left: list of terms; right: list of definitions in DISPLAY order;
    answer: list of letters (A..) -- the correct letter for each left item."""
    L = "ABCDEFGHIJKLMNOP"
    rows = []
    for i in range(max(len(left), len(right))):
        lt = Paragraph("<b>%d.</b>&nbsp;&nbsp;%s" % (i + 1, left[i]), WS["cellb"]) if i < len(left) else ""
        rt = Paragraph("<b>%s.</b>&nbsp;&nbsp;%s" % (L[i], right[i]), WS["cell"]) if i < len(right) else ""
        rows.append([lt, AnsBox(), "", rt])
    t = Table(rows, colWidths=[150, 36, 14, W - 200], hAlign="LEFT")
    st = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 4.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
          ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
          ("LINEBELOW", (0, 0), (-1, -2), 0.3, FEINT)]
    t.setStyle(TableStyle(st))
    return t


# =================================================================== true / false
class TFItem(Flowable):
    """Statement + T/F bubbles + a line to correct a false statement."""
    def __init__(self, num, text, width=W, fix=True):
        Flowable.__init__(self); self.num, self.text, self.fix = num, text, fix

    def wrap(self, aw, ah):
        self.w = aw
        self.p = Paragraph(self.text, WS["q"])
        pw, self.ph = self.p.wrap(aw - 112, 200)
        self.h = max(self.ph, 15) + (31 if self.fix else 10)
        return (aw, self.h)

    def draw(self):
        c = self.canv
        top = self.h
        c.setFont("Sans-B", 10); c.setFillColor(BURGUNDY); c.drawString(0, top - 11, "%d." % self.num)
        self.p.drawOn(c, 22, top - self.ph)
        _bubble(c, self.w - 52, top - 8, "T"); _bubble(c, self.w - 26, top - 8, "F")
        if self.fix:
            c.setFont("Sans", 8.2); c.setFillColor(SLATE)
            lab = "If false, correct it:"
            c.drawString(22, 12.2, lab)
            lw = c.stringWidth(lab, "Sans", 8.2)
            c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(22 + lw + 5, 10.4, self.w, 10.4)
            c.setStrokeColor(FEINT); c.setLineWidth(0.3); c.line(0, 0.5, self.w, 0.5)


# =================================================================== multiple choice
class MCQ(Flowable):
    def __init__(self, num, q, opts):
        Flowable.__init__(self); self.num, self.q, self.opts = num, q, opts

    def wrap(self, aw, ah):
        self.w = aw
        self.qp = Paragraph("<b><font color=\"%s\">%d.</font></b>&nbsp;&nbsp;%s" % (hexc(BURGUNDY), self.num, self.q), WS["q"])
        qw, self.qh = self.qp.wrap(aw, 200)
        colw = (aw - 24) / 2.0
        self.ops = [Paragraph(o, WS["opt"]) for o in self.opts]
        hs = [p.wrap(colw - 22, 200)[1] for p in self.ops]
        self.rowh = [max(hs[i:i + 2] + [14]) + 3 for i in range(0, len(hs), 2)]
        self.colw = colw
        self.h = self.qh + 5 + sum(self.rowh) + 7
        return (aw, self.h)

    def draw(self):
        c = self.canv
        top = self.h
        self.qp.drawOn(c, 0, top - self.qh)
        y = top - self.qh - 5
        for r, rh in enumerate(self.rowh):
            for k in range(2):
                i = r * 2 + k
                if i >= len(self.ops):
                    continue
                x = 14 + k * (self.colw + 12)
                _bubble(c, x + 6.3, y - 8.5, "ABCD"[i])
                self.ops[i].drawOn(c, x + 18, y - self.ops[i].height - 1.5)
            y -= rh


# =================================================================== ordering
def order(items, answer_nums):
    """items in DISPLAY order, answer_nums[i] = correct position (1-based) of items[i]."""
    rows = [[AnsBox(26, 17), Paragraph(t, WS["cell"])] for t in items]
    t = Table(rows, colWidths=[40, W - 40], hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("LINEBELOW", (0, 0), (-1, -2), 0.3, FEINT)]))
    return t


# =================================================================== sorting
def sort_bank(items, ncols=3):
    """A bank of numbered chips to be sorted into columns."""
    cells = []
    for i, it in enumerate(items):
        cells.append(Paragraph('<b><font color="%s">%d</font></b>&nbsp;&nbsp;%s' % (hexc(BURGUNDY), i + 1, it), WS["cell"]))
    rows = [cells[i:i + ncols] for i in range(0, len(cells), ncols)]
    for r in rows:
        r += [""] * (ncols - len(r))
    t = Table(rows, colWidths=[W / float(ncols)] * ncols, hAlign="LEFT")
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BOXFILL), ("BOX", (0, 0), (-1, -1), 0.6, BOXEDGE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def sort_columns(headers, h=64, subs=None):
    ncols = len(headers)
    cw = (W - 10 * (ncols - 1)) / float(ncols)
    head = [Paragraph(x.upper(), WS["hdr"]) for x in headers]
    body = [WriteBox(h, w=cw, gap=19.5) for _ in headers]
    cols, widths = [], []
    for i in range(ncols):
        cols.append(i)
    data = [head, body]
    # interleave a 10pt gutter between columns
    data2 = [[], []]
    widths = []
    for i in range(ncols):
        data2[0].append(data[0][i]); data2[1].append(data[1][i]); widths.append(cw)
        if i < ncols - 1:
            data2[0].append(""); data2[1].append(""); widths.append(10)
    t = Table(data2, colWidths=widths, hAlign="LEFT")
    st = [("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
          ("VALIGN", (0, 0), (-1, -1), "TOP")]
    for i in range(ncols):
        x = i * 2
        st += [("LINEBELOW", (x, 0), (x, 0), LINE_RULE, INK), ("LINEABOVE", (x, 0), (x, 0), LINE_BOLD, INK)]
    t.setStyle(TableStyle(st))
    return t


# =================================================================== compare grid
class Blank:
    """Marks a cell the student must fill. `a` is the answer shown in the key."""
    def __init__(self, a, lines=1):
        self.a, self.lines = a, lines


def compare(header, rows, widths, key=False, rowh=30, compact=False):
    data = [[Paragraph(h.upper(), WS["hdr"]) for h in header]]
    cs = WS["keyc"] if compact else WS["cell"]
    for r in rows:
        line = [Paragraph(r[0], _p("kc_l", fontName="Sans-B", fontSize=8.4, leading=10.2, textColor=BURGUNDY)
                          if compact else WS["cellb"])]
        for j, cell in enumerate(r[1:], 1):
            cw = widths[j] - 12
            if isinstance(cell, Blank):
                if compact:
                    line.append(Paragraph('<font color="%s"><b>%s</b></font>' % (hexc(ANS), cell.a), cs))
                else:
                    line.append(FillCell(cw, h=(rowh if cell.lines == 1 else 13 * cell.lines + 8),
                                         text=(cell.a if key else None), lines=cell.lines))
            else:
                line.append(Paragraph(cell, cs))
        data.append(line)
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.2 if compact else 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 if compact else 5),
                           ("LINEABOVE", (0, 0), (-1, 0), LINE_BOLD, INK),
                           ("LINEBELOW", (0, 0), (-1, 0), LINE_RULE, INK),
                           ("LINEBELOW", (0, 1), (-1, -2), 0.3, FEINT),
                           ("LINEBELOW", (0, -1), (-1, -1), LINE_BOLD, INK)]))
    return t


# =================================================================== cause -> effect chain
class Chain(Flowable):
    """Boxes joined by arrows. Strings are given; Blank()s are for the student to fill."""
    def __init__(self, items, key=False, label=None, box_h=40):
        Flowable.__init__(self)
        self.items, self.key, self.label, self.box_h = items, key, label, box_h
        self.spaceBefore = 3; self.spaceAfter = 6

    def wrap(self, aw, ah):
        self.w = aw
        return (aw, self.box_h + (13 if self.label else 0))

    def draw(self):
        c = self.canv
        n, gap = len(self.items), 15.0
        bw = (self.w - gap * (n - 1)) / n
        y0 = 0
        for i, it in enumerate(self.items):
            x = i * (bw + gap)
            blank_ = isinstance(it, Blank)
            if blank_ and not self.key:
                c.setFillColor(colors.white); c.setStrokeColor(BURGUNDY); c.setLineWidth(0.9); c.setDash(2.6, 2.2)
            elif blank_:
                c.setFillColor(colors.HexColor("#F6E9EC")); c.setStrokeColor(BURGUNDY); c.setLineWidth(0.9); c.setDash(1, 0)
            else:
                c.setFillColor(BOXFILL); c.setStrokeColor(BOXEDGE); c.setLineWidth(0.6); c.setDash(1, 0)
            c.roundRect(x, y0, bw, self.box_h, 3, stroke=1, fill=1)
            c.setDash(1, 0)
            if not (blank_ and not self.key):
                txt = it.a if blank_ else it
                st = _p("chain_t", fontName="Sans-B" if blank_ else "Sans", fontSize=8.6, leading=10.8,
                        textColor=ANS if blank_ else INK, alignment=TA_CENTER)
                p = Paragraph(txt, st); pw, ph = p.wrap(bw - 10, self.box_h)
                p.drawOn(c, x + 5, y0 + (self.box_h - ph) / 2.0)
            if i < n - 1:
                ax = x + bw + 2
                c.setStrokeColor(GOLD); c.setFillColor(GOLD); c.setLineWidth(1.1)
                c.line(ax, y0 + self.box_h / 2.0, ax + gap - 6, y0 + self.box_h / 2.0)
                pth = c.beginPath(); pth.moveTo(ax + gap - 2, y0 + self.box_h / 2.0)
                pth.lineTo(ax + gap - 7.5, y0 + self.box_h / 2.0 + 3); pth.lineTo(ax + gap - 7.5, y0 + self.box_h / 2.0 - 3)
                pth.close(); c.drawPath(pth, stroke=0, fill=1)
        if self.label:
            c.setFont("Sans-B", 6.4); c.setFillColor(MUTE); tracked(c, 0, self.box_h + 4, self.label.upper(), 1.0)
        # arrows above all use the same geometry


# =================================================================== calendar (Gantt) shading
MONTHS = "JFMAMJJASOND"


class Gantt(Flowable):
    """Shade the months each stage occupies. rows: (label, start, end, south_text)."""
    def __init__(self, rows, key=False, row_h=21.0):
        Flowable.__init__(self); self.rows, self.key, self.row_h = rows, key, row_h
        self.spaceBefore = 2; self.spaceAfter = 4

    def wrap(self, aw, ah):
        self.w = aw
        return (aw, 20 + len(self.rows) * self.row_h)

    def draw(self):
        c, w = self.canv, self.w
        lab_w, cw = 128.0, 21.0
        gx = lab_w
        H = 20 + len(self.rows) * self.row_h
        # header
        c.setFont("Sans-B", 6.8); c.setFillColor(SLATE)
        for m in range(12):
            c.drawCentredString(gx + m * cw + cw / 2.0, H - 12, MONTHS[m])
        tracked(c, gx + 12 * cw + 14, H - 12, "SOUTHERN HEMISPHERE", 0.9)
        c.setFillColor(GOLD); tracked(c, 0, H - 12, "NORTHERN HEMISPHERE", 0.9)
        c.setStrokeColor(INK); c.setLineWidth(LINE_BOLD); c.line(0, H - 17, w, H - 17)
        for r, (label, s, e, south) in enumerate(self.rows):
            y = H - 20 - (r + 1) * self.row_h
            c.setFont("Sans-B", 8.8); c.setFillColor(BURGUNDY); c.drawString(0, y + 7, label)
            for m in range(12):
                inside = (s <= m <= e) if s <= e else (m >= s or m <= e)
                x = gx + m * cw
                if self.key and inside:
                    c.setFillColor(colors.HexColor("#C98E99")); c.setStrokeColor(colors.HexColor("#A25A68"))
                    c.setLineWidth(0.5); c.rect(x + 1, y + 2, cw - 2, self.row_h - 4, stroke=1, fill=1)
                else:
                    c.setFillColor(colors.white); c.setStrokeColor(colors.HexColor("#B9BCC0"))
                    c.setLineWidth(0.5); c.rect(x + 1, y + 2, cw - 2, self.row_h - 4, stroke=1, fill=1)
            sx = gx + 12 * cw + 14
            if self.key:
                c.setFont("Sans-B", 8.8); c.setFillColor(ANS); c.drawString(sx, y + 7, south)
            else:
                c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(sx, y + 5, w, y + 5)
            c.setStrokeColor(FEINT); c.setLineWidth(0.3); c.line(0, y, w, y)
        c.setStrokeColor(INK); c.setLineWidth(LINE_BOLD); c.line(0, 0, w, 0)


# =================================================================== label the diagram
def ordered_targets(art):
    """[(num, name, (x, y), side)] -- left-hand labels first, each side top to bottom."""
    tg = [(t[0], t[1], t[2] if len(t) > 2 else "R") for t in art.targets]
    left = sorted([t for t in tg if t[2] == "L"], key=lambda t: -t[1][1])
    right = sorted([t for t in tg if t[2] == "R"], key=lambda t: -t[1][1])
    return [(i + 1,) + t for i, t in enumerate(left + right)]


def label_key(art):
    return " \u00b7 ".join('<b>%d</b> %s' % (n, name) for n, name, _, _ in ordered_targets(art))


class LabelFigure(Flowable):
    """An unlabelled drawing with numbered blanks joined to it by leader lines."""
    def __init__(self, art, align="center", sub=None, subs=None, key=False):
        Flowable.__init__(self)
        self.art, self.align, self.sub, self.subs, self.key = art, align, sub, subs or {}, key
        self.spaceBefore = 2; self.spaceAfter = 4

    def wrap(self, aw, ah):
        self.w = aw
        return (aw, self.art.H + 10)

    def _tg(self):
        return ordered_targets(self.art)

    def draw(self):
        c, art = self.canv, self.art
        Wd, Ht = art.W, art.H
        v0, v1 = art.vis
        vw = (v1 - v0) * Wd
        art_x = ((self.w - vw) / 2.0 - v0 * Wd) if self.align == "center" else (10 - v0 * Wd)
        y0 = 5
        c.saveState(); c.translate(art_x, y0)
        clip = c.beginPath(); clip.rect(v0 * Wd - 10, -4, (v1 - v0) * Wd + 20, Ht + 8)
        c.clipPath(clip, stroke=0, fill=0)
        art.draw(c); c.restoreState()
        tg = self._tg()
        left = [t for t in tg if t[3] == "L"]
        right = [t for t in tg if t[3] == "R"]
        two = bool(self.sub)
        for side, group in (("L", left), ("R", right)):
            if not group:
                continue
            if side == "R":
                colx0, colx1 = art_x + v1 * Wd + 30, self.w
            else:
                colx0, colx1 = 0, art_x + v0 * Wd - 30
            top, bot = Ht - 8, (30 if two else 14)
            n = len(group)
            for k, (num, name, (tx, ty), _) in enumerate(group):
                sy = y0 + (top - k * (top - bot) / float(max(n - 1, 1)) if n > 1 else (top + bot) / 2.0)
                px, py = art_x + tx, y0 + ty
                # leader
                if side == "R":
                    cnx = colx0 + 6
                    ex = cnx - 6
                    ln0, ln1 = cnx + 10, colx1
                else:
                    cnx = colx1 - 6
                    ex = cnx + 6
                    ln0, ln1 = colx0, cnx - 10
                c.setStrokeColor(MUTE); c.setLineWidth(0.5); c.line(px, py, ex, sy)
                c.setFillColor(BURGUNDY); c.setStrokeColor(colors.white); c.setLineWidth(0.8)
                c.circle(px, py, 2.4, stroke=1, fill=1)
                _bubble(c, cnx, sy, str(num), r=6.6, fill=BURGUNDY, txt=colors.white)
                c.setStrokeColor(INK); c.setLineWidth(0.6); c.line(ln0, sy - 4, ln1, sy - 4)
                if self.key:
                    c.setFont("Sans-B", 9.4); c.setFillColor(ANS); c.drawString(ln0 + 2, sy - 1.6, name)
                if two:
                    c.setFont("Sans", 7.4); c.setFillColor(SLATE)
                    lab = self.sub
                    lw = c.stringWidth(lab, "Sans", 7.4)
                    c.drawString(ln0, sy - 17.5, lab)
                    c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(ln0 + lw + 4, sy - 19.2, ln1, sy - 19.2)
                    if self.key and name in self.subs:
                        c.setFont("Sans-B", 8.2); c.setFillColor(ANS); c.drawString(ln0 + lw + 7, sy - 17.0, self.subs[name])


# =================================================================== stage chooser (circle 1-4)
def choose(statements, labels, answers=None, key=False):
    """Each statement gets a row of numbered/lettered bubbles to circle."""
    rows = []
    for i, st in enumerate(statements):
        bub = []
        for j, lb in enumerate(labels):
            bub.append(_ChoiceBubble(lb, filled=(key and answers is not None and answers[i] == j)))
        rows.append([Paragraph("<b><font color=\"%s\">%d.</font></b>&nbsp;&nbsp;%s" % (hexc(BURGUNDY), i + 1, st), WS["cell"])] + bub)
    cw = 24
    t = Table(rows, colWidths=[W - cw * len(labels) - 4] + [cw] * len(labels), hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.4),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("LINEBELOW", (0, 0), (-1, -2), 0.3, FEINT)]))
    return t


class _ChoiceBubble(Flowable):
    def __init__(self, label, filled=False):
        Flowable.__init__(self); self.label, self.filled = label, filled

    def wrap(self, aw, ah):
        return (22, 17)

    def draw(self):
        c = self.canv
        if self.filled:
            _bubble(c, 11, 8.5, self.label, r=7.2, fill=ANS, txt=colors.white)
        else:
            _bubble(c, 11, 8.5, self.label, r=7.2)


# =================================================================== explain-it + self-marking
def explain(question, points, lines=6, key=False):
    """A short written answer, marked against a checklist of mark points."""
    q = Table([[Paragraph(question, WS["body"])]], colWidths=[W])
    q.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BOXFILL), ("LINEBEFORE", (0, 0), (0, -1), 1.6, GOLD),
                           ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    out = [q, Spacer(1, 4), WriteBox(lines * 19.5 + 4)]
    return out


class Checklist(Flowable):
    """Mark points with a tick-box each, for self-marking."""
    def __init__(self, points, title="SELF-MARK \u2014 TICK EACH POINT YOU MADE"):
        Flowable.__init__(self); self.points, self.title = points, title
        self.spaceBefore = 5

    def wrap(self, aw, ah):
        self.w = aw
        self.ps = [Paragraph(p, WS["cell"]) for p in self.points]
        self.hs = [p.wrap(aw - 30, 100)[1] for p in self.ps]
        self.h = 16 + sum(h + 4 for h in self.hs) + 4
        return (aw, self.h)

    def draw(self):
        c = self.canv
        c.setFont("Sans-B", 6.4); c.setFillColor(GOLD); tracked(c, 0, self.h - 8, self.title, 1.1)
        c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR); c.line(0, self.h - 12, self.w, self.h - 12)
        y = self.h - 16
        for p, h in zip(self.ps, self.hs):
            c.setStrokeColor(INK); c.setLineWidth(0.7); c.rect(2, y - h + 1.5, 9, 9, stroke=1, fill=0)
            p.drawOn(c, 22, y - h)
            y -= h + 4


# =================================================================== chapter opener + tracker
class Opener(Flowable):
    """Page-one block: how to use this workbook and what you will be able to do."""
    def __init__(self, chap, title, objectives, guide_ref):
        Flowable.__init__(self)
        self.chap, self.title, self.obj, self.guide = chap, title, objectives, guide_ref

    def wrap(self, aw, ah):
        self.w = aw
        self.h = 150
        return (aw, self.h)

    def draw(self):
        c, w, H = self.canv, self.w, self.h
        c.setFont("Sans-B", 7.2); c.setFillColor(GOLD)
        tracked(c, 0, H - 9, "CHAPTER %s WORKBOOK" % self.chap, 1.6)
        c.setFont("Serif-B", 22); c.setFillColor(BURGUNDY); c.drawString(0, H - 33, self.title)
        c.setFont("Sans", 9.4); c.setFillColor(SLATE)
        c.drawString(0, H - 48, "Companion to D1 Chapter %s and %s. Work in pencil; check, then correct in ink." % (self.chap, self.guide))
        c.setStrokeColor(INK); c.setLineWidth(LINE_BOLD); c.line(0, H - 56, w, H - 56)
        steps = [("1", "ATTEMPT", "Close the book. Answer from memory."),
                 ("2", "CHECK", "Mark yourself against the key at the back; fix errors in ink."),
                 ("3", "REVISIT", "Redo what you missed on days 3, 7 and 21 (tick them on the scorecard).")]
        y = H - 76
        for num, head, body in steps:
            _bubble(c, 9, y + 3, num, r=7.4, fill=BURGUNDY, txt=colors.white)
            c.setFont("Sans-B", 7.2); c.setFillColor(BURGUNDY); tracked(c, 24, y + 5, head, 1.1)
            p = Paragraph(body, _p("st", fontSize=8.4, leading=10.2))
            pw, ph = p.wrap(210, 40)
            p.drawOn(c, 24, y - 4 - ph + 8.5)
            y -= 31
        ox = 262
        c.setFont("Sans-B", 6.6); c.setFillColor(GOLD); tracked(c, ox, H - 70, "BY THE END YOU CAN", 1.2)
        yy = H - 84
        for ob in self.obj:
            p = Paragraph(ob, _p("ob", fontSize=8.8, leading=10.8, leftIndent=9, bulletIndent=0, bulletColor=GOLD),
                          bulletText="\u2022")
            pw, ph = p.wrap(w - ox, 100)
            p.drawOn(c, ox, yy - ph + 8)
            yy -= ph + 2.4


class Scorecard(Flowable):
    """Score boxes for every exercise, a total, and a spaced-review tick row."""
    def __init__(self, items):
        Flowable.__init__(self); self.items = items

    def wrap(self, aw, ah):
        self.w = aw
        self.h = 108
        return (aw, self.h)

    def draw(self):
        c, w, H = self.canv, self.w, self.h
        c.setStrokeColor(INK); c.setLineWidth(LINE_BOLD); c.line(0, H - 2, w, H - 2)
        c.setFont("Sans-B", 6.8); c.setFillColor(GOLD); tracked(c, 0, H - 14, "YOUR SCORECARD", 1.4)
        n = len(self.items)
        per = int(math.ceil(n / 2.0))
        cw = (w - 100) / float(per)
        for i, (num, pts) in enumerate(self.items):
            r, k = divmod(i, per)
            x, y = k * cw, H - 40 - r * 28
            c.setFont("Sans-B", 7.2); c.setFillColor(BURGUNDY); c.drawString(x, y + 11, num)
            c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(x, y + 2, x + cw - 24, y + 2)
            c.setFont("Sans", 7.2); c.setFillColor(SLATE); c.drawString(x + cw - 22, y + 3.4, "/%s" % pts)
        tx = w - 90
        c.setStrokeColor(BURGUNDY); c.setLineWidth(0.9); c.roundRect(tx, H - 78, 90, 56, 3, stroke=1, fill=0)
        c.setFont("Sans-B", 6.4); c.setFillColor(BURGUNDY); tracked(c, tx + 8, H - 32, "TOTAL", 1.2)
        tot = sum(p for _, p in self.items)
        c.setFont("Sans-B", 11); c.setFillColor(SLATE); c.drawRightString(tx + 82, H - 70, "/ %d" % tot)
        c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(tx + 10, H - 58, tx + 52, H - 58)
        ry = 4
        c.setFont("Sans-B", 6.6); c.setFillColor(GOLD); tracked(c, 0, ry + 12, "SPACED REVIEW", 1.2)
        xx = 100
        for lab in ("DAY 1", "DAY 3", "DAY 7", "DAY 21"):
            c.setStrokeColor(INK); c.setLineWidth(0.7); c.rect(xx, ry + 9, 9, 9, stroke=1, fill=0)
            c.setFont("Sans-B", 6.8); c.setFillColor(SLATE); tracked(c, xx + 14, ry + 11.2, lab, 0.9)
            c.setStrokeColor(INK); c.setLineWidth(0.5); c.line(xx + 44, ry + 9.4, xx + 96, ry + 9.4)
            xx += 108


# =================================================================== crossword
def make_crossword(words, size=15, seed=7, tries=600):
    """words: [(WORD, clue)]. Greedy placement, best of many random orders."""
    rnd = random.Random(seed)
    best = None
    for _ in range(tries):
        order_ = list(words)
        rnd.shuffle(order_)
        order_.sort(key=lambda x: -len(x[0]) + rnd.random() * 2.2)
        grid = {}
        placed = []

        def can(word, r, c_, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            cross = 0
            br, bc = r - dr, c_ - dc
            if (br, bc) in grid:
                return None
            er, ec = r + dr * len(word), c_ + dc * len(word)
            if (er, ec) in grid:
                return None
            for i, ch in enumerate(word):
                rr, cc = r + dr * i, c_ + dc * i
                if not (0 <= rr < size and 0 <= cc < size):
                    return None
                if (rr, cc) in grid:
                    if grid[(rr, cc)] != ch:
                        return None
                    cross += 1
                else:
                    pr, pc = rr + dc, cc + dr
                    nr, nc = rr - dc, cc - dr
                    if (pr, pc) in grid or (nr, nc) in grid:
                        return None
            return cross

        def put(word, clue, r, c_, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            for i, ch in enumerate(word):
                grid[(r + dr * i, c_ + dc * i)] = ch
            placed.append((word, clue, r, c_, d))

        w0, cl0 = order_[0]
        put(w0, cl0, size // 2, (size - len(w0)) // 2, "A")
        for word, clue in order_[1:]:
            opts = []
            for (r0, c0, d0) in [(p[2], p[3], p[4]) for p in placed]:
                pass
            for r in range(size):
                for c_ in range(size):
                    for d in ("A", "D"):
                        k = can(word, r, c_, d)
                        if k:
                            opts.append((k, r, c_, d))
            if not opts:
                continue
            mx = max(o[0] for o in opts)
            top = [o for o in opts if o[0] == mx]
            k, r, c_, d = rnd.choice(top)
            put(word, clue, r, c_, d)
        rs = [r for (r, _) in grid]; cs = [c_ for (_, c_) in grid]
        area = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        score = (len(placed), -area)
        if best is None or score > best[0]:
            best = (score, dict(grid), list(placed))
    _, grid, placed = best
    r0 = min(r for (r, _) in grid); c0 = min(c_ for (_, c_) in grid)
    grid = {(r - r0, c_ - c0): ch for (r, c_), ch in grid.items()}
    placed = [(w, cl, r - r0, c_ - c0, d) for (w, cl, r, c_, d) in placed]
    rows = max(r for (r, _) in grid) + 1; cols = max(c_ for (_, c_) in grid) + 1
    starts = {}
    n = 0
    for r in range(rows):
        for c_ in range(cols):
            if (r, c_) not in grid:
                continue
            a = ((r, c_ - 1) not in grid) and ((r, c_ + 1) in grid)
            d = ((r - 1, c_) not in grid) and ((r + 1, c_) in grid)
            if a or d:
                n += 1
                starts[(r, c_)] = n
    clues = {"A": [], "D": []}
    for (w, cl, r, c_, d) in placed:
        clues[d].append((starts[(r, c_)], cl, w))
    for d in clues:
        clues[d].sort()
    return dict(grid=grid, starts=starts, rows=rows, cols=cols, clues=clues)


class CrosswordGrid(Flowable):
    def __init__(self, cw, cell=17.5, key=False):
        Flowable.__init__(self); self.cw, self.cell, self.key = cw, cell, key

    def wrap(self, aw, ah):
        return (self.cw["cols"] * self.cell + 2, self.cw["rows"] * self.cell + 2)

    def draw(self):
        c, cs, rows = self.canv, self.cell, self.cw["rows"]
        for (r, k), ch in self.cw["grid"].items():
            x, y = 1 + k * cs, 1 + (rows - 1 - r) * cs
            c.setFillColor(colors.white if not self.key else colors.HexColor("#FBF3F4"))
            c.setStrokeColor(INK); c.setLineWidth(0.7); c.rect(x, y, cs, cs, stroke=1, fill=1)
            if (r, k) in self.cw["starts"]:
                c.setFont("Sans-B", 5.4); c.setFillColor(GOLD)
                c.drawString(x + 1.6, y + cs - 6.2, str(self.cw["starts"][(r, k)]))
            if self.key:
                c.setFont("Sans-B", 9.6); c.setFillColor(ANS); c.drawCentredString(x + cs / 2.0, y + 4.4, ch)


def crossword_block(cw, key=False, cell=17.5):
    def clue_pars(d, label):
        out = [Paragraph(label, _p("cwh", fontName="Sans-B", fontSize=7.0, leading=9, textColor=GOLD, spaceBefore=2, spaceAfter=2))]
        for n, cl, w in cw["clues"][d]:
            out.append(Paragraph("<b><font color=\"%s\">%d</font></b>&nbsp;&nbsp;%s" % (hexc(BURGUNDY), n, cl),
                                 _p("cwc", fontSize=8.7, leading=10.6, spaceAfter=2.2, leftIndent=12, firstLineIndent=-12)))
        return out
    gw = cw["cols"] * cell + 2
    right = clue_pars("A", "ACROSS") + [Spacer(1, 5)] + clue_pars("D", "DOWN")
    t = Table([[CrosswordGrid(cw, cell, key), right]], colWidths=[gw + 14, W - gw - 14], hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t


# =================================================================== answer key
class Key:
    def __init__(self):
        self.entries = []

    def add(self, exid, title, flows):
        if not isinstance(flows, (list, tuple)):
            flows = [flows]
        flat = []
        for f in flows:
            flat.extend(f if isinstance(f, (list, tuple)) else [f])
        self.entries.append((exid, title, flat))

    def flowables(self, chap, title, items=None):
        out = [KeyMarker(chap, title, items or []), PageBreak()]
        for exid, ttl, flows in self.entries:
            blk = [Paragraph("%s&nbsp;&nbsp;<font color=\"%s\">%s</font>" % (exid, hexc(SLATE), ttl), WS["keyh"])] + flows
            out.append(KeepTogether(blk))
        return out


class _Rule(Flowable):
    def wrap(self, aw, ah):
        self.w = aw
        return (aw, 8)

    def draw(self):
        self.canv.setStrokeColor(INK); self.canv.setLineWidth(LINE_BOLD); self.canv.line(0, 4, self.w, 4)


def kp(text):
    return Paragraph(text, WS["key"])


def pairs(items, ncols=10, width=W):
    """items: [(label, answer)] -> compact grid for the key."""
    cells = ['<b>%s</b>&nbsp;<font color="%s"><b>%s</b></font>' % (a, hexc(ANS), b) for a, b in items]
    rows = [cells[i:i + ncols] for i in range(0, len(cells), ncols)]
    for r in rows:
        r += [""] * (ncols - len(r))
    t = Table([[Paragraph(x, WS["key"]) for x in r] for r in rows], colWidths=[width / ncols] * ncols, hAlign="LEFT")
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return t


def numbered(items):
    """items: [(n, text)] -> a numbered answer list, one per line, sized for a key column."""
    out = []
    for n, t in items:
        out.append(Paragraph('<b>%s</b>&nbsp;&nbsp;%s' % (n, t),
                             _p("kn", fontSize=8.6, leading=10.6, spaceAfter=1.4, leftIndent=14, firstLineIndent=-14)))
    return out


def crossword_answers(cw):
    """The solved crossword as two short lines of text for the key."""
    def line(d, label):
        return "<b>%s</b>&nbsp; " % label + " \u00b7 ".join(
            '%d <font color="%s"><b>%s</b></font>' % (n, hexc(ANS), w) for n, cl, w in cw["clues"][d])
    return [kp(line("A", "Across")), kp(line("D", "Down"))]
