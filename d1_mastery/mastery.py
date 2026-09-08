"""
Chapter Mastery Guide — layout engine
US Letter portrait. Content column left, light-ruled note-taking column right.
Headings: Title Case serif (Playfair Display). Body: Sentence case sans (Archivo).
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether, Flowable,
                                ListFlowable, ListItem, PageBreak, CondPageBreak)

FONTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
for name, fn in [("Serif", "Serif-Semi.ttf"), ("Serif-B", "Serif-Bold.ttf"),
                 ("Sans", "Sans-Reg.ttf"), ("Sans-B", "Sans-Bold.ttf"),
                 ("Sans-I", "Sans-Ital.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONTDIR, fn)))

# ---------------------------------------------------------------- tokens
INK       = colors.HexColor("#16161A")
BURGUNDY  = colors.HexColor("#6E2B36")     # the single accent
GOLD      = colors.HexColor("#8A6A2C")     # the single secondary
SLATE     = colors.HexColor("#5A5D63")
MUTE      = colors.HexColor("#8B8E93")
HAIRLINE  = colors.HexColor("#C6C8CB")
FEINT     = colors.HexColor("#E6E4E0")     # row rules inside exhibits
RULE      = colors.HexColor("#E1E3E5")     # note-taking rules
BOXFILL   = colors.HexColor("#F7F5F1")
BANDFILL  = colors.HexColor("#F0ECE4")
BOXEDGE   = colors.HexColor("#DED8CD")
LINE_HAIR = 0.3
LINE_RULE = 0.6
LINE_BOLD = 1.1
GAP = 30.0   # 40px exactly (40/96*72) — the one gap used before every
             # section, exhibit and graphic THAT ISN'T a heading's own
             # immediate content. See _degap_heading_adjacent() below: content
             # that directly follows a heading has this zeroed out, so a
             # heading and its own material sit at normal line spacing.

PW, PH = letter                 # 612 x 792
BIND    = 54                    # margin on the three-hole-punched edge
OUTER   = 40                    # margin on the free edge
GUTTER  = 24
L_W     = 336                   # content column width (constant on every page)
N_W     = 158                   # notes column width (constant on every page)
TOP_Y   = 726
BOT_Y   = 56
RULE_GAP = 19.5

# Odd (recto) pages are punched on the left: content left, notes right.
# Even (verso) pages mirror it: notes left, content right.
ODD  = dict(content_x=BIND,  notes_x=BIND + L_W + GUTTER)
EVEN = dict(content_x=OUTER + N_W + GUTTER, notes_x=OUTER)
L_X, N_X = ODD["content_x"], ODD["notes_x"]
FULL_W = PW - BIND - OUTER      # content width when the notes column is dropped
FULL_ODD  = dict(content_x=BIND,  notes_x=None)
FULL_EVEN = dict(content_x=OUTER, notes_x=None)

COL_W = L_W                     # width the box flowables should span


def set_col_width(w):
    global COL_W
    COL_W = w


def zones(page_no):
    return ODD if page_no % 2 == 1 else EVEN

# ---------------------------------------------------------------- styles
def _p(name, **kw):
    base = dict(fontName="Sans", fontSize=9.7, leading=13.1, textColor=INK,
                alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    base.update(kw)
    # ReportLab defaults bullets to 10pt Helvetica; inherit the paragraph's own face instead.
    base.setdefault("bulletFontName", base["fontName"])
    base.setdefault("bulletFontSize", base["fontSize"])
    base.setdefault("bulletColor", base["textColor"])
    return ParagraphStyle(name, **base)

S = {
 # --- headings: Title Case serif, held slightly back so the body can grow ---
 "h1":      _p("h1", fontName="Serif-B", fontSize=18.0, leading=20.6, textColor=BURGUNDY,
               spaceBefore=0, spaceAfter=2),
 "h1sub":   _p("h1sub", fontName="Sans", fontSize=10.0, leading=13.0, textColor=SLATE,
               spaceAfter=9),
 "h2":      _p("h2", fontName="Serif-B", fontSize=13.5, leading=15.8, textColor=BURGUNDY,
               spaceBefore=GAP, spaceAfter=6, keepWithNext=1),
 "h3":      _p("h3", fontName="Serif", fontSize=11.5, leading=13.6, textColor=INK,
               spaceBefore=GAP, spaceAfter=5, keepWithNext=1),
 "h4":      _p("h4", fontName="Sans-B", fontSize=10.0, leading=12.4, textColor=GOLD,
               spaceBefore=GAP, spaceAfter=4, keepWithNext=1),
 # --- body copy: sentence case sans, floor 10pt ---
 "body":    _p("body", fontSize=10.0, leading=13.5, spaceAfter=5),
 "bullet":  _p("bullet", fontSize=10.0, leading=13.2, leftIndent=12.5, bulletIndent=1.7,
               spaceAfter=3.2, bulletColor=GOLD),
 "sub":     _p("sub", fontSize=10.0, leading=13.0, leftIndent=24.5, bulletIndent=14,
               spaceAfter=2.6, textColor=SLATE, bulletColor=GOLD),
 "note":    _p("note", fontSize=10.0, leading=13.2, textColor=SLATE, spaceAfter=4.5),
 "box":     _p("box", fontSize=10.0, leading=13.4, spaceAfter=4),
 "boxb":    _p("boxb", fontName="Sans-B", fontSize=10.0, leading=13.4, spaceAfter=2.5),
 # --- exhibits and flow charts: floor 9pt ---
 "cap":     _p("cap", fontName="Sans-B", fontSize=9.0, leading=11.0, textColor=GOLD,
               spaceAfter=3, keepWithNext=1),
 "capin":   _p("capin", fontName="Sans-B", fontSize=7.0, leading=9.0, textColor=GOLD,
               spaceAfter=0),
 "tbl":     _p("tbl", fontSize=9.0, leading=12.2, textColor=INK),
 "tblh":    _p("tblh", fontName="Sans-B", fontSize=7.3, leading=9.8, textColor=SLATE),
 "tbll":    _p("tbll", fontName="Sans-B", fontSize=9.0, leading=12.2, textColor=BURGUNDY),
 "flow":    _p("flow", fontSize=8.6, leading=11.0, alignment=TA_LEFT, textColor=SLATE),
 "flowb":   _p("flowb", fontName="Sans-B", fontSize=8.4, leading=10.8, alignment=TA_LEFT, textColor=BURGUNDY),
 # --- exam sections ---
 "q":       _p("q", fontName="Sans-B", fontSize=10.2, leading=13.2, spaceBefore=7, spaceAfter=3),
 "opt":     _p("opt", fontSize=10.0, leading=13.0, leftIndent=17.5, bulletIndent=3.4,
               spaceAfter=2.0, bulletFontName="Sans-B", bulletColor=BURGUNDY),
 "ans":     _p("ans", fontSize=10.0, leading=13.2, textColor=SLATE, spaceAfter=4.5),
}

def tracked(c, x, y, text, track=1.2, align="l", width=None):
    """Draw letterspaced text. ReportLab's canvas has no setCharSpace, so the
    spacing is applied glyph by glyph."""
    total = c.stringWidth(text, c._fontname, c._fontsize) + track * max(len(text) - 1, 0)
    if align == "c":
        x -= total / 2.0
    elif align == "r":
        x -= total
    for ch in text:
        c.drawString(x, y, ch)
        x += c.stringWidth(ch, c._fontname, c._fontsize) + track
    return total


def tracked_width(c, text, track=1.2):
    return c.stringWidth(text, c._fontname, c._fontsize) + track * max(len(text) - 1, 0)


# ---------------------------------------------------------------- helpers
def H1(t, sub=None):
    out = [Paragraph(t, S["h1"])]
    if sub:
        out.append(Paragraph(sub, S["h1sub"]))
    return out

def H2(t):  return Paragraph(t, S["h2"])
def H3(t):  return Paragraph(t, S["h3"])
def H4(t):  return Paragraph(t, S["h4"])
def P(t, st="body"): return Paragraph(t, S[st])
def SP(h=5): return Spacer(1, h)

def BUL(items, st="bullet", mark="\u2022"):
    """Bulleted list. An item may be a string, or (string, [subitems])."""
    out = []
    for it in items:
        if isinstance(it, tuple):
            main, subs = it
            out.append(Paragraph(main, S[st], bulletText=mark))
            for s in subs:
                out.append(Paragraph(s, S["sub"], bulletText="\u2013"))
        else:
            out.append(Paragraph(it, S[st], bulletText=mark))
    return out

def NUM(items, st="bullet"):
    return [Paragraph(t, S[st], bulletText=f"{i+1}.") for i, t in enumerate(items)]


class Rule(Flowable):
    """Thin horizontal rule."""
    def __init__(self, w=L_W, thick=0.6, col=HAIRLINE, pad=4):
        Flowable.__init__(self); self.w, self.t, self.c, self.pad = w, thick, col, pad
    def wrap(self, aw, ah):
        self.w = min(self.w, aw); return (self.w, self.t + self.pad * 2)
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0, self.pad, self.w, self.pad)


class CapRule(Flowable):
    """Letterspaced small-caps label sitting on a hairline rule.

    Used as the caption for every exhibit and figure so the two systems share
    one typographic signature.
    """
    def __init__(self, label, width=None, colour=None, size=7.0, track=1.25,
                 rule=True, pad=4.5, space_before=None):
        Flowable.__init__(self)
        self.label, self.colour, self.size = label.upper(), colour or GOLD, size
        self.track, self.rule, self.pad = track, rule, pad
        self.width = width or L_W
        self.keepWithNext = 1
        # ReportLab collapses adjacent spacing to the larger of the two, so a
        # caption directly under its own heading still sits close, while one
        # following body copy gets a clear break.
        self.spaceBefore = GAP if space_before is None else space_before

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return (self.width, self.size + self.pad + (2.5 if self.rule else 0))

    def draw(self):
        c = self.canv
        y = self.pad + (2.5 if self.rule else 0)
        c.setFont("Sans-B", self.size); c.setFillColor(self.colour)
        tracked(c, 0, y, self.label, self.track)
        if self.rule:
            c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
            c.line(0, y - 3.5, self.width, y - 3.5)


def EXHIBIT(label, rows, widths, header=True, fs=7.5, keep=None):
    """Rule-ruled data table \u2014 no vertical lines, no fills.

    Structure follows classical Swiss table setting: a bold rule above the
    column heads, a fine rule below them, feint rules between rows, and a bold
    rule closing the table. Caption and heads are letterspaced caps so the
    exhibit reads as part of the same system as the figures.
    """
    ncols = len(widths)
    if keep is None:
        keep = True
    data = []
    cap_row = 0
    if not keep:
        # A splittable exhibit carries its caption as a repeating row, so the
        # label reappears on the continuation and no KeepTogether is needed.
        data.append([Paragraph(label.upper(), S["capin"])] + [""] * (ncols - 1))
        cap_row = 1
    for r_i, row in enumerate(rows):
        if header and r_i == 0:
            data.append([Paragraph(str(c).upper(), S["tblh"]) for c in row])
        else:
            data.append([Paragraph(str(c), S["tbll"] if i == 0 else S["tbl"])
                         for i, c in enumerate(row)])
    rep = (1 if header else 0) + cap_row
    tb = Table(data, colWidths=widths, repeatRows=rep,
               splitByRow=0 if keep else 1)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
          ("LEFTPADDING", (0, 0), (0, -1), 0),
          ("RIGHTPADDING", (-1, 0), (-1, -1), 0),
          ("TOPPADDING", (0, 0), (-1, -1), 5.0),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 5.0),
          ("LINEBELOW", (0, cap_row), (-1, -2), LINE_HAIR, FEINT),
          ("LINEABOVE", (0, cap_row), (-1, cap_row), LINE_BOLD, INK),
          ("LINEBELOW", (0, -1), (-1, -1), LINE_BOLD, INK)]
    if cap_row:
        st += [("SPAN", (0, 0), (-1, 0)),
               ("TOPPADDING", (0, 0), (-1, 0), 0),
               ("BOTTOMPADDING", (0, 0), (-1, 0), 3.0)]
    if header:
        st += [("TOPPADDING", (0, cap_row), (-1, cap_row), 4.0),
               ("BOTTOMPADDING", (0, cap_row), (-1, cap_row), 4.0),
               ("LINEBELOW", (0, cap_row), (-1, cap_row), LINE_RULE, INK)]
    tb.setStyle(TableStyle(st))
    if keep:
        return [CapRule(label), SP(1.5), tb]
    tb.spaceBefore = GAP
    return [tb]


def CALLOUT(title, flows, accent=GOLD, fill=BOXFILL, split=True, width=None):
    """Tinted panel with a fine accent rule at the left edge.

    No outer border: the tint alone separates it from the page, which keeps the
    page quiet. The title repeats if the panel splits, so a heading can never be
    left without its content.
    """
    head = CapRule(title, width=(width or COL_W) - 16, colour=accent, size=6.9,
                   rule=False, pad=1.5, space_before=0)
    cw = width or COL_W
    common = [("BACKGROUND", (0, 0), (-1, -1), fill),
              ("LINEBEFORE", (0, 0), (0, -1), 1.6, accent),
              ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 11),
              ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if split:
        data = [[head]] + [[f] for f in flows]
        tb = Table(data, colWidths=[cw], repeatRows=1)
        tb.hAlign = "LEFT"
        tb.setStyle(TableStyle(common + [
            ("TOPPADDING", (0, 0), (-1, -1), 1.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
            ("TOPPADDING", (0, 0), (0, 0), 9),
            ("BOTTOMPADDING", (0, 0), (0, 0), 5),
            ("BOTTOMPADDING", (0, -1), (0, -1), 9)]))
        tb.spaceBefore = GAP
        return [tb]
    tb = Table([[[head, SP(4)] + list(flows)]], colWidths=[cw], splitByRow=0)
    tb.hAlign = "LEFT"
    tb.setStyle(TableStyle(common + [
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    tb.spaceBefore = GAP
    return [tb]


class FlowChart(Flowable):
    """Vertical flow chart: boxes joined by arrows. Optional side annotations.

    steps: list of (title, detail, side) — detail/side may be None.
    """
    def __init__(self, steps, width=L_W, box_w=None, gap=13, pad=5.5):
        Flowable.__init__(self)
        self.spaceBefore = GAP
        self.spaceAfter = 0
        self.steps, self.width, self.gap, self.pad = steps, width, gap, pad
        self.box_w = box_w or (width * 0.68)
        self._h = None

    def _measure(self):
        self.rows = []
        self.has_side = any(st[2] for st in self.steps)
        # With side annotations the boxes sit left so the notes have room inside the frame.
        self.x0 = 0.0 if self.has_side else (self.width - self.box_w) / 2.0
        self.side_x = self.x0 + self.box_w + 12
        self.side_w = max(self.width - self.side_x, 40)
        inner = self.box_w - 2 * self.pad
        for title, detail, side in self.steps:
            pt = Paragraph(title, S["flowb"]); _, ht = pt.wrap(inner, 1000)
            pd, hd = None, 0
            if detail:
                pd = Paragraph(detail, S["flow"]); _, hd = pd.wrap(inner, 1000)
            bh = ht + hd + (2.5 if detail else 0) + 2 * self.pad
            ps, hs = None, 0
            if side:
                ps = Paragraph(side, ParagraphStyle("fs", parent=S["flow"],
                               fontSize=6.9, leading=8.5, textColor=SLATE,
                               alignment=TA_LEFT))
                _, hs = ps.wrap(self.side_w, 1000)
            self.rows.append((pt, pd, ps, max(bh, hs + 2 * self.pad), hs))
        self._h = sum(r[3] for r in self.rows) + self.gap * (len(self.rows) - 1)

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        if any(st[2] for st in self.steps):
            self.box_w = min(self.box_w, self.width * 0.60)
        else:
            self.box_w = min(self.box_w, self.width * 0.80)
        self._measure()
        return (self.width, self._h + 6)

    def draw(self):
        c = self.canv
        x0 = self.x0
        y = self._h + 3
        for i, (pt, pd, ps, bh, hs) in enumerate(self.rows):
            top = y; bot = y - bh
            # flat tinted panel with a fine accent rule at the left edge
            c.setFillColor(BOXFILL)
            c.rect(x0, bot, self.box_w, bh, stroke=0, fill=1)
            c.setFillColor(BURGUNDY)
            c.rect(x0, bot, 1.6, bh, stroke=0, fill=1)
            iy = top - self.pad
            th = pt.height; pt.drawOn(c, x0 + self.pad + 4, iy - th); iy -= th
            if pd:
                iy -= 2.5; pd.drawOn(c, x0 + self.pad + 4, iy - pd.height)
            if ps:
                ps.drawOn(c, self.side_x, top - bh / 2 - hs / 2)
                c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
                c.line(x0 + self.box_w + 3, top - bh / 2, self.side_x - 4, top - bh / 2)
            if i < len(self.rows) - 1:
                mx = x0 + self.box_w / 2.0
                c.setStrokeColor(GOLD); c.setLineWidth(LINE_RULE)
                c.line(mx, bot, mx, bot - self.gap + 3.5)
                c.setFillColor(GOLD)
                pth = c.beginPath(); pth.moveTo(mx - 2.6, bot - self.gap + 4.0)
                pth.lineTo(mx + 2.6, bot - self.gap + 4.0)
                pth.lineTo(mx, bot - self.gap - 0.6)
                pth.close(); c.drawPath(pth, stroke=0, fill=1)
            y = bot - self.gap

    # Flow charts are deliberately NOT splittable: a chart broken across a page
    # loses the visual logic it exists to carry.

class Continuum(Flowable):
    """Horizontal axis with poles and mid-labels — for 'cool <-> warm' style exhibits."""
    def __init__(self, left_lbl, right_lbl, items, width=L_W):
        Flowable.__init__(self)
        self.l, self.r, self.items, self.width = left_lbl, right_lbl, items, width
    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self._paras = []
        cw = self.width / len(self.items)
        h = 0
        for a, b in self.items:
            pa = Paragraph(a, ParagraphStyle("ca", parent=S["flow"], fontSize=6.8,
                           leading=8.2, fontName="Sans-B"))
            pb = Paragraph(b, ParagraphStyle("cb", parent=S["flow"], fontSize=6.6,
                           leading=8.0, textColor=SLATE))
            _, ha = pa.wrap(cw - 8, 500); _, hb = pb.wrap(cw - 8, 500)
            self._paras.append((pa, pb, ha, hb)); h = max(h, ha + hb + 2)
        self._blockh = h
        return (self.width, h + 30)
    def draw(self):
        c = self.canv; w = self.width
        ay = self._blockh + 12
        c.setStrokeColor(GOLD); c.setLineWidth(1.1); c.line(6, ay, w - 6, ay)
        for xx, d in ((6, -1), (w - 6, 1)):
            c.setFillColor(GOLD); pth = c.beginPath()
            pth.moveTo(xx + d * 5, ay); pth.lineTo(xx, ay + 3); pth.lineTo(xx, ay - 3)
            pth.close(); c.drawPath(pth, stroke=0, fill=1)
        c.setFont("Sans-B", 7.7); c.setFillColor(BURGUNDY)
        c.drawString(0, ay + 6, self.l.upper())
        c.drawRightString(w, ay + 6, self.r.upper())
        cw = w / len(self.items)
        for i, (pa, pb, ha, hb) in enumerate(self._paras):
            cx = i * cw
            c.setStrokeColor(HAIRLINE); c.setLineWidth(0.5)
            c.line(cx + cw / 2, ay, cx + cw / 2, ay - 5)
            pa.drawOn(c, cx + 4, ay - 8 - ha)
            pb.drawOn(c, cx + 4, ay - 10 - ha - hb)


# ---------------------------------------------------------------- page furniture
def _page(canv, doc):
    canv.saveState()
    pno = doc._mg_offset + canv.getPageNumber()
    odd = pno % 2 == 1
    if doc._mg_notes:
        z = ODD if odd else EVEN
        cx, nx, cw = z["content_x"], z["notes_x"], L_W
        canv.setFont("Sans-B", 7.5); canv.setFillColor(GOLD)
        canv.drawString(nx, TOP_Y + 7, "N O T E S")
        canv.setStrokeColor(HAIRLINE); canv.setLineWidth(0.6)
        canv.line(nx, TOP_Y + 2, nx + N_W, TOP_Y + 2)
        canv.setStrokeColor(RULE); canv.setLineWidth(0.35)
        y = TOP_Y - RULE_GAP
        while y > BOT_Y:
            canv.line(nx, y, nx + N_W, y); y -= RULE_GAP
        fx0, fx1 = min(cx, nx), max(cx + cw, nx + N_W)
    else:
        cx = BIND if odd else OUTER
        cw = FULL_W
        fx0, fx1 = cx, cx + cw
    canv.setFont("Serif", 8.4); canv.setFillColor(SLATE)
    canv.drawString(cx, TOP_Y + 7, doc._mg_title)
    canv.setStrokeColor(HAIRLINE); canv.setLineWidth(0.6)
    canv.line(cx, TOP_Y + 2, cx + cw, TOP_Y + 2)
    canv.setStrokeColor(HAIRLINE); canv.setLineWidth(0.4)
    canv.line(fx0, BOT_Y - 10, fx1, BOT_Y - 10)
    canv.setFont("Sans", 7.5); canv.setFillColor(SLATE)
    canv.drawString(fx0, BOT_Y - 21,
        "WSET Level 4 Diploma in Wines \u2014 D1: Wine Production \u00b7 Chapter Mastery Guide")
    canv.setFont("Sans-B", 7.8); canv.setFillColor(BURGUNDY)
    canv.drawRightString(fx1, BOT_Y - 21, str(pno))
    canv.restoreState()


class _MirrorDoc(BaseDocTemplate):
    """Alternates the content column so the notes always fall on the outer edge
    when sheets are printed two-sided and three-hole punched."""
    def handle_pageBegin(self):
        BaseDocTemplate.handle_pageBegin(self)
        nxt = self._mg_offset + self.page + 1
        self.handle_nextPageTemplate("odd" if nxt % 2 == 1 else "even")


def _flat(seq, out=None):
    out = [] if out is None else out
    for it in seq:
        if isinstance(it, (list, tuple)):
            _flat(it, out)
        else:
            out.append(it)
    return out


MIN_LINES_AFTER_HEADING = 4


def _est_lines(f, colw):
    """Rough line count for a flowable, used only to size heading groups.

    Spacers, rules and CapRule captions are furniture, not content: counting
    them would let a heading satisfy the four-line rule while its actual
    material \u2014 a table or a diagram \u2014 fell to the next page.
    """
    if isinstance(f, (Spacer, Rule, CapRule)):
        return 0.0
    if isinstance(f, Paragraph):
        try:
            _, h = f.wrap(colw, 100000)
            lead = getattr(f.style, "leading", 12) or 12
            return max(h / lead, 1.0)
        except Exception:
            return 1.0
    return 99.0        # tables, flow charts and callouts satisfy the rule outright


def _measure(f, colw):
    try:
        _, h = f.wrap(colw, 100000)
        return float(h)
    except Exception:
        return 0.0


def _spacing(f):
    """Space a flowable claims above and below itself. CondPageBreak reserves
    raw height only, so this has to be added or the reservation falls short by
    exactly the heading's space-before."""
    s = 0.0
    for m in ("getSpaceBefore", "getSpaceAfter"):
        try:
            s += float(getattr(f, m)())
        except Exception:
            pass
    return s


def _group_headings(story, colw, min_lines=MIN_LINES_AFTER_HEADING,
                    max_group_h=250.0):
    """A heading must carry at least `min_lines` of its own content onto the page.

    Short groups are bound with KeepTogether. Tall ones are not: wrapping a
    splittable table inside a KeepTogether makes it unsplittable, so it jumps to
    the next page whole and strands half a page of white. Those instead get a
    CondPageBreak sized to the heading plus the required lines, which moves the
    heading down only if that much space is unavailable and otherwise lets the
    table split and fill the page.
    """
    out, i, n = [], 0, len(story)
    line_h = 13.5
    while i < n:
        f = story[i]
        if (not isinstance(f, KeepTogether) and getattr(f, "getKeepWithNext", None)
                and f.getKeepWithNext()):
            grp, lines, j = [f], 0.0, i + 1
            while j < n and lines < min_lines:
                g = story[j]
                if isinstance(g, (KeepTogether, PageBreak)):
                    break
                grp.append(g)
                lines += _est_lines(g, colw)
                j += 1
            if len(grp) > 1:
                gh = sum(_measure(x, colw) for x in grp)
                pad0 = sum(_spacing(x) for x in grp)
                if gh + pad0 <= max_group_h:
                    out.append(KeepTogether(grp))
                else:
                    # Only a table that is allowed to split can honour a partial
                    # reservation; anything else (a diagram, a flow chart, a
                    # locked table) has to be reserved in full or the heading
                    # ends up with two or three lines under it.
                    tail = [x for x in grp[1:] if not isinstance(x, Spacer)]
                    splittable = bool(tail) and isinstance(tail[-1], Table) \
                        and getattr(tail[-1], "splitByRow", 0)
                    pad = sum(_spacing(x) for x in grp) + 8
                    if splittable:
                        tbl = tail[-1]
                        tbl.wrap(colw, 100000)
                        rh = getattr(tbl, "_rowHeights", None)
                        rep = getattr(tbl, "repeatRows", 0) or 0
                        if rh:
                            # Reserve real header/caption rows plus one actual data
                            # row, not a generic line-count guess. A guess can
                            # under-reserve badly when the first data row wraps
                            # tall (long cell text) \u2014 Table.split() then finds
                            # even the reserved space insufficient to place a
                            # single real row, returns nothing fits, and the
                            # *whole* table (plus its heading) jumps to the next
                            # page regardless of how much room was actually left.
                            first_rows_h = sum(rh[:rep + 1])
                        else:
                            first_rows_h = min_lines * line_h
                        need = sum(_measure(x, colw) for x in grp
                                   if _est_lines(x, colw) < 90) \
                            + first_rows_h + pad
                        # ReportLab's own DocTemplate.handle_keepWithNext runs at
                        # draw time, independently of everything above: it sees
                        # the heading's style still carries keepWithNext=1 and
                        # atomically wraps heading+table in its OWN KeepTogether
                        # before the frame ever asks the table whether it can
                        # split \u2014 silently undoing this whole reservation and
                        # sending the entire table to the next page regardless of
                        # how much room the CondPageBreak already confirmed was
                        # there. Clearing it on the instance (not the shared
                        # style) stops that second, independent grouping.
                        grp[0].__dict__["keepWithNext"] = 0
                    else:
                        need = gh + pad
                    out.append(CondPageBreak(min(need, TOP_Y - BOT_Y - 4)))
                    out.extend(grp)
                i = j
                continue
        out.append(f)
        i += 1
    return out



HEADING_STYLES = {'h1', 'h1sub', 'h2', 'h3', 'h4'}


def _degap_heading_adjacent(story):
    """Content that DIRECTLY follows a heading is that heading's own material,
    not a new block \u2014 it keeps normal line spacing, never the standard GAP.

    Walks the flat story once: whenever the current flowable is set in one of
    the heading styles and the next one is not, the next flowable's own
    spaceBefore (an exhibit caption, a callout panel, a graphic \u2014 anything
    that defaults to GAP) is zeroed, so the only separation left is the
    heading's own small spaceAfter.
    """
    for i in range(len(story) - 1):
        cur = story[i]
        cur_style = getattr(getattr(cur, "style", None), "name", None)
        if cur_style not in HEADING_STYLES:
            continue
        nxt = story[i + 1]
        nxt_style = getattr(getattr(nxt, "style", None), "name", None)
        if nxt_style in HEADING_STYLES:
            continue
        if hasattr(nxt, "spaceBefore"):
            nxt.spaceBefore = 0
    return story


def _render(path, title, story, notes, offset):
    if notes:
        zo, ze, cw = ODD, EVEN, L_W
    else:
        zo, ze, cw = FULL_ODD, FULL_EVEN, FULL_W
    set_col_width(cw)
    doc = _MirrorDoc(path, pagesize=letter,
                     leftMargin=OUTER, rightMargin=OUTER,
                     topMargin=PH - TOP_Y, bottomMargin=BOT_Y,
                     title=title, author="Chapter Mastery Guide")
    doc._mg_title, doc._mg_notes, doc._mg_offset = title, notes, offset
    tmpl = []
    for tid, z in (("odd", zo), ("even", ze)):
        fr = Frame(z["content_x"], BOT_Y, cw, TOP_Y - BOT_Y, id="content",
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        tmpl.append(PageTemplate(id=tid, frames=[fr], onPage=_page))
    doc.addPageTemplates(tmpl)
    # the first page of this part must use the template matching its true parity
    if (offset + 1) % 2 == 0:
        doc.pageTemplates = [tmpl[1], tmpl[0]]
    doc.build(_group_headings(_degap_heading_adjacent(_flat(story)), cw))
    from pypdf import PdfReader
    return len(PdfReader(path).pages)


def build(path, title, body, exam=None, maxpages=16):
    """Body pages carry the ruled notes column; exam pages run full width."""
    import tempfile
    from pypdf import PdfReader, PdfWriter
    d = tempfile.mkdtemp()
    a = os.path.join(d, "a.pdf"); b = os.path.join(d, "b.pdf")
    na = _render(a, title, body, notes=True, offset=0)
    parts = [a]
    nb = 0
    if exam:
        nb = _render(b, title, exam, notes=False, offset=na)
        parts.append(b)
    w = PdfWriter()
    for f in parts:
        for pg in PdfReader(f).pages:
            w.add_page(pg)
    with open(path, "wb") as fh:
        w.write(fh)
    n = na + nb
    flag = "" if n <= maxpages else f"   *** OVER LIMIT ({maxpages}) ***"
    print(f"{os.path.basename(path):<48} {na:>2} + {nb:>2} = {n:>2} pages{flag}")
    return n
