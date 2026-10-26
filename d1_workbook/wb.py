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
    def __init__(self, chap, title, objectives, guide_ref, fit=False):
        Flowable.__init__(self)
        self.chap, self.title, self.obj, self.guide, self.fit = chap, title, objectives, guide_ref, fit

    OBX = 262

    def _obj_paras(self, w):
        out = []
        for ob in self.obj:
            p = Paragraph(ob, _p("ob", fontSize=8.8, leading=10.8, leftIndent=9, bulletIndent=0, bulletColor=GOLD),
                          bulletText="\u2022")
            pw, ph = p.wrap(w - self.OBX, 100)
            out.append((p, ph))
        return out

    def wrap(self, aw, ah):
        self.w = aw
        ps = self._obj_paras(aw)
        need = 78 + sum(ph for _, ph in ps) + 2.4 * (len(ps) - 1) + 2
        self.h = max(150, need) if self.fit else 150
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
        ox = self.OBX
        c.setFont("Sans-B", 6.6); c.setFillColor(GOLD); tracked(c, ox, H - 70, "BY THE END YOU CAN", 1.2)
        yy = H - 84
        for p, ph in self._obj_paras(w):
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


def make_crossword2(words, size=13, seed=1, tries=400, second_pass=True, min_words=12):
    """A denser crossword: candidate placements come from matching letters, every extra word takes the most crossings
    available, unplaced words get a second chance, and the best grid by (words placed, crossings, compactness) wins."""
    rnd = random.Random(seed)
    best = None
    words = [w for w in words if len(w[0]) <= size]
    for _ in range(tries):
        order_ = list(words)
        rnd.shuffle(order_)
        order_.sort(key=lambda x: -len(x[0]) + rnd.random() * 3.0)
        grid, placed, crossings = {}, [], [0]

        def can(word, r, c_, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            cross = 0
            if (r - dr, c_ - dc) in grid or (r + dr * len(word), c_ + dc * len(word)) in grid:
                return None
            for i, chx in enumerate(word):
                rr, cc = r + dr * i, c_ + dc * i
                if not (0 <= rr < size and 0 <= cc < size):
                    return None
                if (rr, cc) in grid:
                    if grid[(rr, cc)] != chx:
                        return None
                    cross += 1
                elif (rr + dc, cc + dr) in grid or (rr - dc, cc - dr) in grid:
                    return None
            return cross

        def put(word, clue, r, c_, d, k):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            for i, chx in enumerate(word):
                grid[(r + dr * i, c_ + dc * i)] = chx
            placed.append((word, clue, r, c_, d))
            crossings[0] += k

        def try_place(word, clue):
            opts = []
            seen = set()
            for (gr, gc), g in list(grid.items()):
                for i, chx in enumerate(word):
                    if chx != g:
                        continue
                    for d in ("A", "D"):
                        r, c_ = (gr, gc - i) if d == "A" else (gr - i, gc)
                        if (r, c_, d) in seen:
                            continue
                        seen.add((r, c_, d))
                        k = can(word, r, c_, d)
                        if k:
                            opts.append((k, r, c_, d))
            if not opts:
                return False
            mx = max(o[0] for o in opts)
            k, r, c_, d = rnd.choice([o for o in opts if o[0] == mx])
            put(word, clue, r, c_, d, k)
            return True

        w0, cl0 = order_[0]
        put(w0, cl0, size // 2, (size - len(w0)) // 2, "A", 0)
        left = []
        for word, clue in order_[1:]:
            if not try_place(word, clue):
                left.append((word, clue))
        if second_pass:
            for word, clue in left:
                try_place(word, clue)
        rs = [r for (r, _) in grid]; cs = [c_ for (_, c_) in grid]
        area = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        score = (len(placed) >= min_words, crossings[0], len(placed), -area)
        if best is None or score > best[0]:
            best = (score, dict(grid), list(placed), crossings[0])
    _, grid, placed, nx = best
    r0 = min(r for (r, _) in grid); c0 = min(c_ for (_, c_) in grid)
    grid = {(r - r0, c_ - c0): chx for (r, c_), chx in grid.items()}
    placed = [(w, cl, r - r0, c_ - c0, d) for (w, cl, r, c_, d) in placed]
    rows = max(r for (r, _) in grid) + 1; cols = max(c_ for (_, c_) in grid) + 1
    starts, n = {}, 0
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
    return dict(grid=grid, starts=starts, rows=rows, cols=cols, clues=clues, crossings=nx)


def make_crossword3(words, size=12, seed=1, tries=60, min_words=12, max_words=18):
    """Best-first crossword: at every step place whichever remaining word and position gives the MOST crossings, so the
    grid interlocks tightly. The best grid over many random starts wins on (crossings, words, compactness)."""
    rnd = random.Random(seed)
    words = [w for w in words if len(w[0]) <= size]
    best = None
    for t in range(tries):
        grid, placed, crossings = {}, [], 0
        letters = {}

        def can(word, r, c_, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            cross = 0
            if (r - dr, c_ - dc) in grid or (r + dr * len(word), c_ + dc * len(word)) in grid:
                return None
            for i, chx in enumerate(word):
                rr, cc = r + dr * i, c_ + dc * i
                if not (0 <= rr < size and 0 <= cc < size):
                    return None
                if (rr, cc) in grid:
                    if grid[(rr, cc)] != chx:
                        return None
                    cross += 1
                elif (rr + dc, cc + dr) in grid or (rr - dc, cc - dr) in grid:
                    return None
            return cross

        def put(word, clue, r, c_, d):
            dr, dc = (0, 1) if d == "A" else (1, 0)
            for i, chx in enumerate(word):
                p = (r + dr * i, c_ + dc * i)
                if p not in grid:
                    grid[p] = chx
                    letters.setdefault(chx, []).append(p)
            placed.append((word, clue, r, c_, d))

        pool = list(words)
        longs = [w for w in pool if len(w[0]) >= 8] or pool
        first = rnd.choice(longs)
        pool.remove(first)
        put(first[0], first[1], size // 2, (size - len(first[0])) // 2, "A")
        while pool and len(placed) < max_words:
            cands = []
            top = 0
            for (word, clue) in pool:
                seen = set()
                for i, chx in enumerate(word):
                    for (gr, gc) in letters.get(chx, ()):
                        for d in ("A", "D"):
                            r, c_ = (gr, gc - i) if d == "A" else (gr - i, gc)
                            if (r, c_, d) in seen:
                                continue
                            seen.add((r, c_, d))
                            k = can(word, r, c_, d)
                            if k and k >= top:
                                if k > top:
                                    cands, top = [], k
                                cands.append((word, clue, r, c_, d))
            if not cands:
                break
            word, clue, r, c_, d = rnd.choice(cands)
            crossings += top
            put(word, clue, r, c_, d)
            pool = [w for w in pool if w[0] != word]
        rs = [r for (r, _) in grid]; cs = [c_ for (_, c_) in grid]
        area = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        score = (len(placed) >= min_words, crossings, len(placed), -area)
        if best is None or score > best[0]:
            best = (score, dict(grid), list(placed), crossings)
    _, grid, placed, nx = best
    r0 = min(r for (r, _) in grid); c0 = min(c_ for (_, c_) in grid)
    grid = {(r - r0, c_ - c0): chx for (r, c_), chx in grid.items()}
    placed = [(w, cl, r - r0, c_ - c0, d) for (w, cl, r, c_, d) in placed]
    rows = max(r for (r, _) in grid) + 1; cols = max(c_ for (_, c_) in grid) + 1
    starts, n = {}, 0
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
    return dict(grid=grid, starts=starts, rows=rows, cols=cols, clues=clues, crossings=nx)


def make_crossword4(words, size=13, seed=1, tries=300, iters=1500, min_words=14, max_words=22):
    """Densest crossword: best-first starts, then local search (drop a word, refill with the most-crossing placements,
    keep if the (words, crossings, compactness) score does not fall)."""
    rnd = random.Random(seed)
    words = [w for w in words if len(w[0]) <= size]
    clue_of = {w: cl for w, cl in words}

    def cells_of(item):
        word, clue, r, c_, d = item
        dr, dc = (0, 1) if d == "A" else (1, 0)
        return [(r + dr * i, c_ + dc * i) for i in range(len(word))]

    def grid_of(pl):
        g = {}
        for it in pl:
            for p, chx in zip(cells_of(it), it[0]):
                g[p] = chx
        return g

    def cross_of(pl):
        cnt = {}
        for it in pl:
            for p in cells_of(it):
                cnt[p] = cnt.get(p, 0) + 1
        return sum(1 for v in cnt.values() if v > 1)

    def connected(pl):
        if not pl:
            return False
        cs = [set(cells_of(it)) for it in pl]
        seen, stack = {0}, [0]
        while stack:
            i = stack.pop()
            for j in range(len(pl)):
                if j not in seen and cs[i] & cs[j]:
                    seen.add(j); stack.append(j)
        return len(seen) == len(pl)

    def can(grid, word, r, c_, d):
        dr, dc = (0, 1) if d == "A" else (1, 0)
        cross = 0
        if (r - dr, c_ - dc) in grid or (r + dr * len(word), c_ + dc * len(word)) in grid:
            return None
        for i, chx in enumerate(word):
            rr, cc = r + dr * i, c_ + dc * i
            if not (0 <= rr < size and 0 <= cc < size):
                return None
            if (rr, cc) in grid:
                if grid[(rr, cc)] != chx:
                    return None
                cross += 1
            elif (rr + dc, cc + dr) in grid or (rr - dc, cc - dr) in grid:
                return None
        return cross

    def fill(pl, pool):
        pl = list(pl)
        pool = [w for w in pool if w[0] not in {p[0] for p in pl}]
        while pool and len(pl) < max_words:
            grid = grid_of(pl)
            letters = {}
            for p, chx in grid.items():
                letters.setdefault(chx, []).append(p)
            cands, top = [], 0
            for (word, clue) in pool:
                seen = set()
                for i, chx in enumerate(word):
                    for (gr, gc) in letters.get(chx, ()):
                        for d in ("A", "D"):
                            r, c_ = (gr, gc - i) if d == "A" else (gr - i, gc)
                            if (r, c_, d) in seen:
                                continue
                            seen.add((r, c_, d))
                            k = can(grid, word, r, c_, d)
                            if k and k >= top:
                                if k > top:
                                    cands, top = [], k
                                cands.append((word, clue, r, c_, d))
            if not cands:
                break
            pick = rnd.choice(cands)
            pl.append(pick)
            pool = [w for w in pool if w[0] != pick[0]]
        return pl

    def score(pl):
        g = grid_of(pl)
        rs = [r for (r, _) in g]; cs = [c_ for (_, c_) in g]
        area = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        return (len(pl) >= min_words, cross_of(pl), len(pl), -area)

    best = None
    for _ in range(tries):
        longs = [w for w in words if len(w[0]) >= 8] or words
        f = rnd.choice(longs)
        pl = [(f[0], f[1], size // 2, (size - len(f[0])) // 2, "A")]
        pl = fill(pl, words)
        sc = score(pl)
        if best is None or sc > best[0]:
            best = (sc, pl)
    cur_sc, cur = best
    for _ in range(iters):
        if len(cur) < 3:
            break
        drop = rnd.sample(range(len(cur)), rnd.choice((1, 1, 2)))
        rest = [it for i, it in enumerate(cur) if i not in drop]
        if not connected(rest):
            continue
        cand = fill(rest, words)
        sc = score(cand)
        if sc >= cur_sc:
            cur_sc, cur = sc, cand
    placed = cur
    grid = grid_of(placed)
    r0 = min(r for (r, _) in grid); c0 = min(c_ for (_, c_) in grid)
    grid = {(r - r0, c_ - c0): chx for (r, c_), chx in grid.items()}
    placed = [(w, cl, r - r0, c_ - c0, d) for (w, cl, r, c_, d) in placed]
    rows = max(r for (r, _) in grid) + 1; cols = max(c_ for (_, c_) in grid) + 1
    starts, n = {}, 0
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
    return dict(grid=grid, starts=starts, rows=rows, cols=cols, clues=clues, crossings=cross_of(placed))


def crossword_from_placed(placed):
    """Normalize a list of (word, clue, r, c, dir) into the dict the renderer expects."""
    grid = {}
    for (w, cl, r, c_, d) in placed:
        dr, dc = (0, 1) if d == "A" else (1, 0)
        for i, chx in enumerate(w):
            grid[(r + dr * i, c_ + dc * i)] = chx
    r0 = min(r for (r, _) in grid); c0 = min(c_ for (_, c_) in grid)
    grid = {(r - r0, c_ - c0): chx for (r, c_), chx in grid.items()}
    placed = [(w, cl, r - r0, c_ - c0, d) for (w, cl, r, c_, d) in placed]
    rows = max(r for (r, _) in grid) + 1; cols = max(c_ for (_, c_) in grid) + 1
    starts, n = {}, 0
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
    cnt = {}
    for (w, cl, r, c_, d) in placed:
        dr, dc = (0, 1) if d == "A" else (1, 0)
        for i in range(len(w)):
            p = (r + dr * i, c_ + dc * i)
            cnt[p] = cnt.get(p, 0) + 1
    crossings = sum(1 for v in cnt.values() if v > 1)
    return dict(grid=grid, starts=starts, rows=rows, cols=cols, clues=clues, crossings=crossings, placed=placed)


def crossword_stats(cw):
    pl = cw["placed"]
    cnt = {}
    for (w, cl, r, c_, d) in pl:
        dr, dc = (0, 1) if d == "A" else (1, 0)
        for i in range(len(w)):
            p = (r + dr * i, c_ + dc * i)
            cnt[p] = cnt.get(p, 0) + 1
    per = []
    for (w, cl, r, c_, d) in pl:
        dr, dc = (0, 1) if d == "A" else (1, 0)
        per.append(sum(1 for i in range(len(w)) if cnt[(r + dr * i, c_ + dc * i)] > 1))
    nA = sum(1 for p in pl if p[4] == "A"); nD = len(pl) - nA
    fill = len(cw["grid"]) / float(cw["rows"] * cw["cols"])
    return dict(words=len(pl), across=nA, down=nD, crossings=cw["crossings"], min_cross=min(per), avg_cross=sum(per) / float(len(per)),
                grid="%dx%d" % (cw["rows"], cw["cols"]), fill="%.0f%%" % (100 * fill))


def make_crossword5(words, size=13, seed=1, tries=80, iters=3000, min_words=15, max_words=20):
    """Newspaper-style themed crossword: balanced Across/Down, every word crossing at least two others, as many crossings as the
    vocabulary allows, compact grid. Score = (enough words, balance, no single-crossing words, crossings, words, compactness)."""
    rnd = random.Random(seed)
    words = [w for w in words if len(w[0]) <= size]

    def cells_of(item):
        word, clue, r, c_, d = item
        dr, dc = (0, 1) if d == "A" else (1, 0)
        return [(r + dr * i, c_ + dc * i) for i in range(len(word))]

    def grid_of(pl):
        g = {}
        for it in pl:
            for p, chx in zip(cells_of(it), it[0]):
                g[p] = chx
        return g

    def per_word(pl):
        cnt = {}
        for it in pl:
            for p in cells_of(it):
                cnt[p] = cnt.get(p, 0) + 1
        return [sum(1 for p in cells_of(it) if cnt[p] > 1) for it in pl], sum(1 for v in cnt.values() if v > 1)

    def connected(pl):
        if not pl:
            return False
        cs = [set(cells_of(it)) for it in pl]
        seen, stack = {0}, [0]
        while stack:
            i = stack.pop()
            for j in range(len(pl)):
                if j not in seen and cs[i] & cs[j]:
                    seen.add(j); stack.append(j)
        return len(seen) == len(pl)

    def can(grid, word, r, c_, d, used):
        dr, dc = (0, 1) if d == "A" else (1, 0)
        cross = 0
        if (r - dr, c_ - dc) in grid or (r + dr * len(word), c_ + dc * len(word)) in grid:
            return None
        for i, chx in enumerate(word):
            rr, cc = r + dr * i, c_ + dc * i
            if not (0 <= rr < size and 0 <= cc < size):
                return None
            if (rr, cc) in grid:
                if grid[(rr, cc)] != chx or ((rr, cc), d) in used:
                    return None
                cross += 1
            elif (rr + dc, cc + dr) in grid or (rr - dc, cc - dr) in grid:
                return None
        return cross

    def fill(pl, pool):
        pl = list(pl)
        pool = [w for w in pool if w[0] not in {p[0] for p in pl}]
        while pool and len(pl) < max_words:
            grid = grid_of(pl)
            used = {(p, it[4]) for it in pl for p in cells_of(it)}
            letters = {}
            for p, chx in grid.items():
                letters.setdefault(chx, []).append(p)
            nA = sum(1 for p in pl if p[4] == "A"); nD = len(pl) - nA
            want = "D" if nA > nD else "A" if nD > nA else None
            cands, top = [], 0
            for (word, clue) in pool:
                seen = set()
                for i, chx in enumerate(word):
                    for (gr, gc) in letters.get(chx, ()):
                        for d in ("A", "D"):
                            r, c_ = (gr, gc - i) if d == "A" else (gr - i, gc)
                            if (r, c_, d) in seen:
                                continue
                            seen.add((r, c_, d))
                            k = can(grid, word, r, c_, d, used)
                            if k and k >= top:
                                if k > top:
                                    cands, top = [], k
                                cands.append((word, clue, r, c_, d))
            if not cands:
                break
            pref = [x for x in cands if want and x[4] == want]
            pick = rnd.choice(pref if (pref and rnd.random() < 0.85) else cands)
            pl.append(pick)
            pool = [w for w in pool if w[0] != pick[0]]
        return pl

    def score(pl):
        g = grid_of(pl)
        rs = [r for (r, _) in g]; cs = [c_ for (_, c_) in g]
        area = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        per, cross = per_word(pl)
        nA = sum(1 for p in pl if p[4] == "A"); nD = len(pl) - nA
        return (-sum(1 for k in per if k < 2), len(pl) >= min_words, -max(0, abs(nA - nD) - 1), cross, len(pl), -area)

    best = None
    for _ in range(tries):
        longs = [w for w in words if len(w[0]) >= 8] or words
        f = rnd.choice(longs)
        pl = fill([(f[0], f[1], size // 2, (size - len(f[0])) // 2, "A")], words)
        sc = score(pl)
        if best is None or sc > best[0]:
            best = (sc, pl)
    cur_sc, cur = best
    for _ in range(iters):
        if len(cur) < 4:
            break
        drop = rnd.sample(range(len(cur)), rnd.choice((1, 1, 2, 3)))
        rest = [it for i, it in enumerate(cur) if i not in drop]
        if not connected(rest):
            continue
        cand = fill(rest, words)
        sc = score(cand)
        if sc >= cur_sc:
            cur_sc, cur = sc, cand
    return crossword_from_placed(cur)


def cached_crossword(ch):
    """Load a chapter's cached crossword layout (see gen_crosswords.py); clues are always read fresh from the vocabulary bank."""
    import json as _json
    import cw_vocab as _CV
    here = os.path.dirname(os.path.abspath(__file__))
    d = _json.load(open(os.path.join(here, "crosswords", "ch%d.json" % ch), encoding="utf-8"))
    window = {1: [1], 4: [2, 3, 4], 7: [5, 6, 7], 10: [8, 9, 10], 13: [11, 12, 13], 16: [14, 15, 16], 19: [17, 18, 19]}[ch]
    pool, _ = _CV.pool(window)
    clue = dict(pool)
    placed = []
    for (word, _old, r, c_, dr) in d["placed"]:
        placed.append((word, clue[word], r, c_, dr))
    return crossword_from_placed(placed)


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
    """Grid at the left; the Across and Down clue lists side by side at the right (keeps a 20-word puzzle compact)."""
    gw = cw["cols"] * cell + 2
    avail = W - gw - 14
    colw = (avail - 12) / 2.0

    def clue_pars(d, label):
        out = [Paragraph(label, _p("cwh", fontName="Sans-B", fontSize=7.0, leading=9, textColor=GOLD, spaceBefore=0, spaceAfter=2))]
        for n, cl, w in cw["clues"][d]:
            out.append(Paragraph("<b><font color=\"%s\">%d</font></b>&nbsp;&nbsp;%s" % (hexc(BURGUNDY), n, cl),
                                 _p("cwc", fontSize=8.0, leading=9.4, spaceAfter=2.0, leftIndent=11, firstLineIndent=-11)))
        return out
    clues = Table([[clue_pars("A", "ACROSS"), clue_pars("D", "DOWN")]], colWidths=[colw + 6, colw + 6])
    clues.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("RIGHTPADDING", (0, 0), (0, 0), 6), ("RIGHTPADDING", (1, 0), (1, 0), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    t = Table([[CrosswordGrid(cw, cell, key), clues]], colWidths=[gw + 14, avail], hAlign="LEFT")
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


# =================================================================== tick grid
def tickgrid(rows, cols, label_w=None):
    """Statements down the side, category columns across: tick every box that applies.
    rows: [str]; cols: [str]. Returns a Table of empty bubbles."""
    n = len(cols)
    cw = 62 if n <= 4 else 50
    lw = label_w or (W - cw * n)
    head = [Paragraph("", WS["hdr"])] + [Paragraph(c.upper(), _p("tg_h", fontName="Sans-B", fontSize=6.0, leading=7.6,
                                                              textColor=SLATE, alignment=TA_CENTER)) for c in cols]
    data = [head]
    for i, r in enumerate(rows):
        data.append([Paragraph("<b><font color=\"%s\">%d.</font></b>&nbsp;&nbsp;%s" % (hexc(BURGUNDY), i + 1, r), WS["cell"])]
                    + [_ChoiceBubble("") for _ in cols])
    t = Table(data, colWidths=[lw] + [cw] * n, hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 3.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
                           ("LINEABOVE", (0, 0), (-1, 0), LINE_BOLD, INK), ("LINEBELOW", (0, 0), (-1, 0), LINE_RULE, INK),
                           ("LINEBELOW", (0, 1), (-1, -2), 0.3, FEINT), ("LINEBELOW", (0, -1), (-1, -1), LINE_BOLD, INK)]))
    return t


# =================================================================== vertical process flow with blanks
class VFlow(Flowable):
    """A process drawn top to bottom. Strings are given steps; Blank()s are for the student to complete.
    `cols` lays the boxes out in that many parallel columns (a step list that reads down each column)."""
    def __init__(self, items, key=False, box_h=25, gap=13, width=None, side=None):
        Flowable.__init__(self)
        self.items, self.key, self.box_h, self.gap, self.width = items, key, box_h, gap, width
        self.side = side or {}          # {index: "note text"} annotations to the right
        self.spaceBefore = 2; self.spaceAfter = 5

    def wrap(self, aw, ah):
        self.w = min(self.width or aw, aw)
        n = len(self.items)
        return (self.w, n * self.box_h + (n - 1) * self.gap)

    def draw(self):
        c = self.canv
        n = len(self.items)
        bw = self.w * (0.62 if self.side else 1.0)
        H = n * self.box_h + (n - 1) * self.gap
        for i, it in enumerate(self.items):
            y = H - (i + 1) * self.box_h - i * self.gap
            blank_ = isinstance(it, Blank)
            if blank_ and not self.key:
                c.setFillColor(colors.white); c.setStrokeColor(BURGUNDY); c.setLineWidth(0.9); c.setDash(2.6, 2.2)
            elif blank_:
                c.setFillColor(colors.HexColor("#F6E9EC")); c.setStrokeColor(BURGUNDY); c.setLineWidth(0.9); c.setDash(1, 0)
            else:
                c.setFillColor(BOXFILL); c.setStrokeColor(BOXEDGE); c.setLineWidth(0.6); c.setDash(1, 0)
            c.roundRect(0, y, bw, self.box_h, 3, stroke=1, fill=1)
            c.setDash(1, 0)
            if not (blank_ and not self.key):
                txt = it.a if blank_ else it
                st = _p("vf_t", fontName="Sans-B" if blank_ else "Sans", fontSize=8.8, leading=10.6,
                        textColor=ANS if blank_ else INK, alignment=TA_CENTER)
                p = Paragraph(txt, st); pw, ph = p.wrap(bw - 12, self.box_h)
                p.drawOn(c, 6, y + (self.box_h - ph) / 2.0)
            if i < n - 1:
                ax, ay = bw / 2.0, y - 1
                c.setStrokeColor(GOLD); c.setFillColor(GOLD); c.setLineWidth(1.1)
                c.line(ax, ay, ax, ay - self.gap + 5)
                pth = c.beginPath(); pth.moveTo(ax, ay - self.gap + 1.5); pth.lineTo(ax - 3, ay - self.gap + 7); pth.lineTo(ax + 3, ay - self.gap + 7)
                pth.close(); c.drawPath(pth, stroke=0, fill=1)
            if i in self.side:
                p = Paragraph(self.side[i], _p("vf_s", fontSize=8.4, leading=10.2, textColor=SLATE))
                pw, ph = p.wrap(self.w - bw - 14, self.box_h + self.gap)
                p.drawOn(c, bw + 12, y + (self.box_h - ph) / 2.0)
                c.setStrokeColor(HAIRLINE); c.setLineWidth(0.5); c.line(bw + 2, y + self.box_h / 2.0, bw + 9, y + self.box_h / 2.0)


# =================================================================== a row of small drawings to be named
class PanelFigure(Flowable):
    """Several small drawings side by side, each with a number and a line to write its name on."""
    def __init__(self, arts, gap=12, names=None, key=False):
        Flowable.__init__(self)
        self.arts, self.gap, self.names, self.key = arts, gap, names or [], key
        self.spaceBefore = 2; self.spaceAfter = 4

    def wrap(self, aw, ah):
        self.w = aw
        return (aw, self.arts[0].H + 40)

    def draw(self):
        c = self.canv
        tot = sum(a.W for a in self.arts) + self.gap * (len(self.arts) - 1)
        x = (self.w - tot) / 2.0
        for i, art in enumerate(self.arts):
            c.setFillColor(colors.HexColor("#FBFAF6")); c.setStrokeColor(BOXEDGE); c.setLineWidth(0.6)
            c.roundRect(x - 2, 26, art.W + 4, art.H + 12, 4, stroke=1, fill=1)
            c.saveState(); c.translate(x, 30); art.draw(c); c.restoreState()
            _bubble(c, x + 8, 26 + art.H + 4, str(i + 1), r=6.6, fill=BURGUNDY, txt=colors.white)
            c.setStrokeColor(INK); c.setLineWidth(0.6); c.line(x, 11, x + art.W, 11)
            if self.key and i < len(self.names):
                c.setFont("Sans-B", 8.6); c.setFillColor(ANS); c.drawCentredString(x + art.W / 2.0, 13.4, self.names[i])
            x += art.W + self.gap


# =================================================================== nested rings (each ring contains the next)
class NestRings(Flowable):
    """Concentric rounded boxes. rings = [(given_text, answer)], outermost first. The student names each ring."""
    def __init__(self, rings, key=False, height=170, inset=30):
        Flowable.__init__(self)
        self.rings, self.key, self.hh, self.inset = rings, key, height, inset
        self.spaceBefore = 2; self.spaceAfter = 5

    def wrap(self, aw, ah):
        self.w = aw
        return (aw, self.hh)

    def draw(self):
        c, w, H, d = self.canv, self.w, self.hh, self.inset
        n = len(self.rings)
        tints = ["#FBFAF6", "#F3EEE2", "#EADFC9", "#E0D0B0"]
        for i, (given, ans) in enumerate(self.rings):
            x0, x1, y0, y1 = i * 38, w - i * 38, i * 9, H - i * 36
            c.setFillColor(colors.HexColor(tints[min(i, 3)])); c.setStrokeColor(BOXEDGE if i else INK); c.setLineWidth(0.9 if i else 1.1)
            c.roundRect(x0, y0, x1 - x0, y1 - y0, 10, stroke=1, fill=1)
        for i, (given, ans) in enumerate(self.rings):
            x0, y1 = i * 38, H - i * 36
            ty = y1 - 19
            _bubble(c, x0 + 15, ty + 3, str(i + 1), r=6.6, fill=BURGUNDY, txt=colors.white)
            c.setFont("Sans", 8.8); c.setFillColor(INK)
            c.drawString(x0 + 28, ty, given)
            bx = (self.w - i * 38) - 14 - 150
            if self.key:
                c.setFont("Sans-B", 9.2); c.setFillColor(ANS); c.drawString(bx + 4, ty, ans)
            else:
                c.setStrokeColor(BURGUNDY); c.setLineWidth(0.9); c.setDash(2.6, 2.2)
                c.setFillColor(colors.white); c.roundRect(bx, ty - 5, 150, 17, 3, stroke=1, fill=1); c.setDash(1, 0)


# =================================================================== a coloured scale with callout boxes to complete
class BandScale(Flowable):
    """A horizontal scale (e.g. temperature) split into bands. Each band has a given header and a box to complete.
    bands = [(lo, hi, colour_hex, header, answer)]; ticks = [values]"""
    def __init__(self, lo, hi, bands, ticks, unit="\u00b0C", key=False, box_h=50):
        Flowable.__init__(self)
        self.lo, self.hi, self.bands, self.ticks, self.unit, self.key, self.box_h = lo, hi, bands, ticks, unit, key, box_h
        self.spaceBefore = 2; self.spaceAfter = 5

    def wrap(self, aw, ah):
        self.w = aw
        return (aw, self.box_h + 74)

    def draw(self):
        c, w = self.canv, self.w
        X = lambda v: 10 + (v - self.lo) / float(self.hi - self.lo) * (w - 20)
        by, bh = 18, 20
        c.setFillColor(colors.HexColor("#ECE8DE")); c.setStrokeColor(INK); c.setLineWidth(0.9)
        c.rect(X(self.lo), by, X(self.hi) - X(self.lo), bh, stroke=1, fill=1)
        for (a, b, col, head, ans) in self.bands:
            c.setFillColor(colors.HexColor(col)); c.setStrokeColor(INK); c.setLineWidth(0.7)
            c.rect(X(a), by, X(b) - X(a), bh, stroke=1, fill=1)
        c.setFont("Sans", 7.2); c.setFillColor(SLATE)
        for t in self.ticks:
            c.setStrokeColor(INK); c.setLineWidth(0.6); c.line(X(t), by, X(t), by - 3)
            c.drawCentredString(X(t), by - 11, "%g%s" % (t, self.unit))
        n = len(self.bands)
        gap = 10
        bw = (w - gap * (n - 1)) / float(n)
        top = self.box_h + 74
        for i, (a, b, col, head, ans) in enumerate(self.bands):
            bx = i * (bw + gap)
            by0 = top - self.box_h
            cx = (X(a) + X(b)) / 2.0
            c.setStrokeColor(HAIRLINE); c.setLineWidth(0.7)
            c.line(cx, by + bh, bx + bw / 2.0, by0)
            c.setFillColor(colors.HexColor(col)); c.circle(cx, by + bh, 2.2, stroke=0, fill=1)
            c.setFillColor(colors.HexColor("#FBFAF6")); c.setStrokeColor(BOXEDGE); c.setLineWidth(0.6)
            c.roundRect(bx, by0, bw, self.box_h, 4, stroke=1, fill=1)
            c.setFont("Sans-B", 7.6); c.setFillColor(BURGUNDY)
            c.drawString(bx + 6, top - 12, head)
            if self.key:
                p = Paragraph(ans, _p("bs_k", fontName="Sans-B", fontSize=7.8, leading=9.2, textColor=ANS))
                pw, ph = p.wrap(bw - 12, self.box_h - 16)
                p.drawOn(c, bx + 6, by0 + (self.box_h - 16 - ph) / 2.0 + 2)
            else:
                c.setStrokeColor(BURGUNDY); c.setLineWidth(0.8); c.setDash(2.4, 2.0)
                c.setFillColor(colors.white); c.roundRect(bx + 5, by0 + 5, bw - 10, self.box_h - 22, 3, stroke=1, fill=1); c.setDash(1, 0)


# =================================================================== bars whose value labels are left blank
class FillBars(Flowable):
    """A simple bar chart: the student writes each bar's value in the dotted box above it.
    bars = [(label, fraction_of_full_height, answer_text)]"""
    def __init__(self, bars, width=330, height=118, key=False, unit_note=None):
        Flowable.__init__(self)
        self.bars, self.fw, self.fh, self.key, self.note = bars, width, height, key, unit_note
        self.spaceBefore = 2; self.spaceAfter = 4

    def wrap(self, aw, ah):
        return (aw, self.fh)

    def draw(self):
        c = self.canv
        n = len(self.bars)
        base, top = 20, self.fh - 30
        bw = 62
        gap = (self.fw - n * bw) / float(n + 1)
        c.setStrokeColor(INK); c.setLineWidth(0.9); c.line(0, base, self.fw, base)
        for i, (lab, frac, ans) in enumerate(self.bars):
            x = gap + i * (bw + gap)
            h = max(4, (top - base) * frac)
            c.setFillColor(colors.HexColor("#A98255")); c.setStrokeColor(colors.HexColor("#3A2A18")); c.setLineWidth(1.0)
            c.roundRect(x, base, bw, h, 3, stroke=1, fill=1)
            c.setFillColor(colors.HexColor("#C9A271")); c.rect(x + 7, base + 3, 7, max(h - 8, 2), stroke=0, fill=1)
            c.setFont("Sans-B", 7.6); c.setFillColor(SLATE); c.drawCentredString(x + bw / 2.0, base - 11, lab)
            by = base + h + 5
            if self.key:
                c.setFont("Sans-B", 9.2); c.setFillColor(ANS); c.drawCentredString(x + bw / 2.0, by + 3, ans)
            else:
                c.setStrokeColor(BURGUNDY); c.setLineWidth(0.9); c.setDash(2.6, 2.2)
                c.setFillColor(colors.white); c.roundRect(x + 2, by, bw - 4, 17, 3, stroke=1, fill=1); c.setDash(1, 0)
