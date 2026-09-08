# -*- coding: utf-8 -*-
"""Graphical devices for the Chapter Mastery Guides.

Everything here is a ReportLab Flowable that draws on the canvas, so the guides
can carry real diagrams rather than tables of text.
"""
import math
import random
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import Flowable, Paragraph, KeepTogether
from mastery import (S, L_W, INK, BURGUNDY, GOLD, SLATE, MUTE, HAIRLINE, FEINT,
                     BOXFILL, BANDFILL, BOXEDGE, SP, CapRule, tracked,
                     LINE_HAIR, LINE_RULE, LINE_BOLD, GAP)

# --------------------------------------------------------------- palette
# A single cool-to-hot sequential ramp, tuned to sit beside burgundy and gold
# without competing with them. Nothing else is coloured.
COOL = colors.HexColor("#4E6E8C")
MILD = colors.HexColor("#6F8A6B")
LEAF = colors.HexColor("#7E9463")
WARM = colors.HexColor("#BE8B45")
HOT  = colors.HexColor("#A6462F")
SOIL = colors.HexColor("#8A7355")
SKY  = colors.HexColor("#E7EDF2")
PAPER = colors.HexColor("#FBFAF8")
GROUND = colors.HexColor("#F7F5F1")


# One type scale for every diagram: label / value / annotation.
G_LABEL, G_VALUE, G_NOTE = 7.6, 7.0, 6.4


def _t(txt, size=7.6, bold=False, colr=INK, align=TA_LEFT, lead=None):
    return Paragraph(txt, ParagraphStyle(
        "g", fontName="Sans-B" if bold else "Sans", fontSize=size,
        leading=lead or size * 1.28, textColor=colr, alignment=align))


def tracked_w(c, text, track=1.2):
    return c.stringWidth(text, c._fontname, c._fontsize) + track * max(len(text) - 1, 0)


def CAPTION(label):
    return CapRule(label)


def FIGURE(label, flow, note=None):
    """Caption + diagram + optional footnote.

    The caption carries the exact 80px gap above the whole block (via CapRule's
    default spaceBefore). The diagram itself is zeroed here so that gap is not
    doubled \u2014 every graphic class defaults spaceBefore=GAP for when it is used
    standalone, without a caption, and this override only applies when composed
    inside FIGURE().

    Returned as a plain list, NOT a KeepTogether: the caption already carries
    keepWithNext and the diagram flowables cannot split, so the heading grouper
    binds them cleanly. Wrapping them here would nest KeepTogethers and
    re-orphan the heading above.
    """
    flow.spaceBefore = 0
    out = [CAPTION(label), SP(4), flow]
    if note:
        out.append(SP(3))
        out.append(Paragraph(note, S["note"]))
    return out


# =============================================================== thermometer
class ThresholdScale(Flowable):
    """A temperature number line: shaded bands beneath, labelled markers above.

    bands: [(lo, hi, label, colour)]   marks: [(value, label)]
    """
    def __init__(self, lo, hi, bands=(), marks=(), width=L_W, unit="\u00b0C",
                 bar_h=15, tick_every=None):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.lo, self.hi, self.bands, self.marks = lo, hi, list(bands), list(marks)
        self.width, self.unit, self.bar_h = width, unit, bar_h
        self.tick_every = tick_every

    def _x(self, v):
        return 6 + (v - self.lo) / float(self.hi - self.lo) * (self.width - 12)

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        # stagger marker labels over two rows to avoid collisions
        self._rows = []
        order = sorted(range(len(self.marks)), key=lambda i: self.marks[i][0])
        lvl, last = {}, {}
        for i in order:
            v, lab = self.marks[i][0], self.marks[i][1]
            w = pdfmetrics.stringWidth(lab, "Sans-B", 6.7) + 0.5 * max(len(lab) - 1, 0)
            x = self._x(v)
            k = 0
            # a row is free only if this label clears the previous one on it
            while k in last and (x - w / 2.0) < last[k] + 7:
                k += 1
            lvl[i] = k
            last[k] = x + w / 2.0
        self._lvl = lvl
        self._nlev = (max(lvl.values()) + 1) if lvl else 1
        self._h = self.bar_h + 26 + self._nlev * 20
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        base = 22
        # bands \u2014 flat, butted, no strokes; the ramp does the work
        for lo, hi, lab, col in self.bands:
            x0, x1 = self._x(max(lo, self.lo)), self._x(min(hi, self.hi))
            c.setFillColor(col)
            c.rect(x0, base, x1 - x0, self.bar_h, stroke=0, fill=1)
            if lab:
                c.setFont("Sans-B", 6.2); c.setFillColor(colors.white)
                if tracked_w(c, lab, 0.9) < (x1 - x0) - 10:
                    tracked(c, (x0 + x1) / 2.0, base + self.bar_h / 2 - 2.1, lab, 0.9, "c")
        # baseline and end values
        c.setStrokeColor(INK); c.setLineWidth(LINE_RULE)
        c.line(6, base, self.width - 6, base)
        c.setFont("Sans", 6.2); c.setFillColor(MUTE)
        c.drawString(6, base - 10, f"{self.lo}{self.unit}")
        c.drawRightString(self.width - 6, base - 10, f"{self.hi}{self.unit}")
        # markers: a fine stem to a tracked label, no dots, no plates
        for i, (v, lab) in enumerate(self.marks):
            x = self._x(v); k = self._lvl[i]
            y = base + self.bar_h + 9 + k * 19
            c.setStrokeColor(BURGUNDY); c.setLineWidth(LINE_HAIR)
            c.line(x, base + self.bar_h + 1, x, y - 3)
            c.setStrokeColor(BURGUNDY); c.setLineWidth(LINE_BOLD)
            c.line(x, base, x, base + self.bar_h)
            c.setFont("Sans-B", 6.7); c.setFillColor(BURGUNDY)
            w = tracked_w(c, lab, 0.5)
            tx = min(max(x - w / 2.0, 0), self.width - w)
            tracked(c, tx, y, lab, 0.5)


class RangeCompare(Flowable):
    """Overlapping optimum windows drawn as stacked bars on one shared axis.

    ranges: [(lo, hi, label, colour)] \u2014 each gets its own row, so windows that
    overlap stay readable instead of painting over one another.
    """
    def __init__(self, lo, hi, ranges, width=L_W, unit="\u00b0C", row_h=13, gap=5,
                 ticks=()):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.lo, self.hi, self.ranges = lo, hi, list(ranges)
        self.width, self.unit, self.row_h, self.gap = width, unit, row_h, gap
        self.ticks = list(ticks)

    def _x(self, v):
        return self.lab_w + (v - self.lo) / float(self.hi - self.lo) * (self.width - self.lab_w - 8)

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self.lab_w = 96
        self._h = len(self.ranges) * (self.row_h + self.gap) + 22
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        top = self._h - 6
        axis_y = 16
        for v in self.ticks:
            x = self._x(v)
            c.setStrokeColor(FEINT); c.setLineWidth(LINE_HAIR)
            c.line(x, axis_y + 2, x, top)
            c.setFont("Sans", 6.2); c.setFillColor(MUTE)
            c.drawCentredString(x, axis_y - 9, f"{v}")
        c.setStrokeColor(INK); c.setLineWidth(LINE_RULE)
        c.line(self.lab_w, axis_y, self.width - 8, axis_y)
        y = top - self.row_h
        for lo, hi, lab, col in self.ranges:
            x0, x1 = self._x(lo), self._x(hi)
            c.setFillColor(col)
            c.rect(x0, y, max(x1 - x0, 3), self.row_h, stroke=0, fill=1)
            span = f"{lo}\u2013{hi}{self.unit}"
            c.setFont("Sans-B", 6.4)
            if tracked_w(c, span, 0.6) < (x1 - x0) - 10:
                c.setFillColor(colors.white)
                tracked(c, (x0 + x1) / 2.0, y + self.row_h / 2 - 2.1, span, 0.6, "c")
            else:
                c.setFillColor(col)
                tracked(c, x1 + 5, y + self.row_h / 2 - 2.1, span, 0.6)
            c.setFont("Sans", G_VALUE); c.setFillColor(INK)
            c.drawRightString(self.lab_w - 9, y + self.row_h / 2 - 2.4, lab)
            y -= self.row_h + self.gap


# =============================================================== cycle wheel
class CycleWheel(Flowable):
    """Annual growth cycle as a labelled ring. segments: [(name, inner, outer)]"""
    def __init__(self, segments, width=L_W, r_out=None, title=None):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.seg, self.width, self.title = list(segments), width, title
        self.r_out = r_out

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self.r_out = self.r_out or min(self.width * 0.29, 84)
        self._h = self.r_out * 2 + 96
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        cx, cy = self.width / 2.0, self._h / 2.0 + 4
        ro, ri = self.r_out, self.r_out * 0.62
        n = len(self.seg)
        step = 360.0 / n
        cols = [COOL, MILD, LEAF, WARM, colors.HexColor("#C4763A"), HOT]
        for i, (name, a_, b_) in enumerate(self.seg):
            start = 90 - (i + 1) * step
            col = cols[i % len(cols)]
            c.setFillColor(col); c.setStrokeColor(colors.white); c.setLineWidth(1.6)
            p = c.beginPath()
            p.moveTo(cx + ri * math.cos(math.radians(start)),
                     cy + ri * math.sin(math.radians(start)))
            p.arcTo(cx - ro, cy - ro, cx + ro, cy + ro, start, step)
            p.arcTo(cx - ri, cy - ri, cx + ri, cy + ri, start + step, -step)
            p.close(); c.drawPath(p, stroke=1, fill=1)
            mid = math.radians(start + step / 2)
            # hairline leader from the ring out to the label
            lx0 = cx + (ro + 3) * math.cos(mid)
            ly0 = cy + (ro + 3) * math.sin(mid)
            lx = cx + (ro + 12) * math.cos(mid)
            ly = cy + (ro + 12) * math.sin(mid)
            c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
            c.line(lx0, ly0, lx, ly)
            right = math.cos(mid) > 0
            c.setFont("Sans-B", 6.9); c.setFillColor(INK)
            if right:
                tracked(c, lx + 3, ly + 1, name.upper(), 0.6)
                c.setFont("Sans", 6.2); c.setFillColor(MUTE)
                c.drawString(lx + 3, ly - 7.5, a_)
                c.drawString(lx + 3, ly - 14.5, b_)
            else:
                tracked(c, lx - 3, ly + 1, name.upper(), 0.6, "r")
                c.setFont("Sans", 6.2); c.setFillColor(MUTE)
                c.drawRightString(lx - 3, ly - 7.5, a_)
                c.drawRightString(lx - 3, ly - 14.5, b_)
        # direction chevrons riding the mid-line of the ring, one per boundary
        rm = (ro + ri) / 2.0
        for i in range(n):
            adeg = 90 - (i + 0.5) * step        # centre of each segment
            a = math.radians(adeg)
            px, py = cx + rm * math.cos(a), cy + rm * math.sin(a)
            c.saveState(); c.translate(px, py)
            # The clockwise tangent at angle a is (sin a, -cos a); the chevron is
            # drawn pointing along local -y, so rotating by a aligns the two.
            c.rotate(adeg)
            c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.92))
            c.setLineWidth(1.5); c.setLineCap(1); c.setLineJoin(1)
            for dy in (2.6, -1.8):
                p2 = c.beginPath()
                p2.moveTo(-3.6, dy + 3.4); p2.lineTo(0, dy); p2.lineTo(3.6, dy + 3.4)
                c.drawPath(p2, stroke=1, fill=0)
            c.restoreState()

        c.setFillColor(colors.white); c.setStrokeColor(FEINT); c.setLineWidth(LINE_HAIR)
        c.circle(cx, cy, ri - 1.5, stroke=1, fill=1)
        c.setFont("Serif-B", 9.6); c.setFillColor(BURGUNDY)
        c.drawCentredString(cx, cy + 3, "The Vine")
        c.drawCentredString(cx, cy - 8, "Year")
        c.setFont("Sans", 6.0); c.setFillColor(MUTE)
        tracked(c, self.width / 2.0, 2, "UPPER LINE  NORTHERN HEMISPHERE    \u00b7    "
                                        "LOWER LINE  SOUTHERN HEMISPHERE", 0.7, "c")
        c.setFont("Sans", 6.0); c.setFillColor(MUTE)
        tracked(c, self.width / 2.0, 11, "CHEVRONS SHOW THE DIRECTION OF THE CYCLE", 0.7, "c")


# =============================================================== venn
class Venn(Flowable):
    """Free-placed labelled circles with wrapped notes beneath.

    items: dicts with x, y (0\u20131 of the plot box), r (fraction of WIDTH),
    label, sub (\u2018|\u2019 separates lines), colour, ly (label height, 0\u20131).
    """
    def __init__(self, items, width=L_W, height=180, notes=None):
        Flowable.__init__(self)
        self.items, self.width, self.plot_h = list(items), width, height
        self.notes = list(notes or [])

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self._np = []
        h = 0
        for n in self.notes:
            p = _t("\u25aa\u2003" + n, 6.4, colr=SLATE, lead=8.4)
            p.wrapOn(self.canv, self.width - 4, 200)
            self._np.append(p); h += p.height + 3.5
        self._notes_h = h
        return (self.width, self.plot_h + self._notes_h + (6 if h else 0))

    def draw(self):
        c = self.canv
        H = self.plot_h
        y0 = self._notes_h + (6 if self._notes_h else 0)
        for it in self.items:
            cx, cy = it["x"] * self.width, y0 + it["y"] * H
            r = it["r"] * self.width
            col = it.get("colour", BURGUNDY)
            c.setFillColor(colors.Color(col.red, col.green, col.blue, alpha=0.15))
            c.setStrokeColor(col); c.setLineWidth(1.2)
            c.circle(cx, cy, r, stroke=1, fill=1)
        for it in self.items:
            cx = it["x"] * self.width
            ly = y0 + it.get("ly", it["y"]) * H
            col = it.get("colour", BURGUNDY)
            c.setFont("Sans-B", 7.6); c.setFillColor(col)
            c.drawCentredString(cx, ly, it["label"])
            if it.get("sub"):
                c.setFont("Sans", 6.3); c.setFillColor(SLATE)
                for j, ln in enumerate(it["sub"].split("|")):
                    c.drawCentredString(cx, ly - 9 - j * 7.6, ln)
        yy = self._notes_h
        for p in self._np:
            yy -= p.height
            p.drawOn(c, 2, yy)
            yy -= 3.5


# =============================================================== nested rings
class InclusionRings(Flowable):
    """Concentric rings for strictly nested categories (A includes B includes C).

    Far more honest than a Venn diagram when the relationship truly is nesting
    rather than partial overlap \u2014 e.g. Demeter requires organic certification
    as a baseline, so biodynamic sits wholly inside organic. Rings are drawn
    thinnest-inside-out with leader-line annotations to the right, reusing the
    same visual grammar as the vine and berry figures so the whole set of
    illustrations reads as one system.

    rings: outermost first \u2014 [(label, sub, colour), ...]
    tags: small satellite labels for cross-cutting tools, drawn below with a
        short connecting note rather than forced into the nest.
    """
    def __init__(self, rings, width=L_W, size=None, tags=None):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.rings, self.width, self.tags = list(rings), width, list(tags or [])
        self.size = size

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self.size = self.size or min(self.width * 0.40, 118)
        tag_h = 15 * len(self.tags) + (16 if self.tags else 0)
        self._h = self.size + 26 + tag_h
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        n = len(self.rings)
        cx, cy = self.size / 2.0 + 4, self._h - self.size / 2.0 - 4
        r_out = self.size / 2.0
        step = r_out / n
        lx = self.size + 26
        radii = [r_out * (1.0 - i * (0.62 / max(n - 1, 1))) for i in range(n)]
        for i, (label, sub, col) in enumerate(self.rings):
            r = radii[i]
            tint = colors.Color(col.red, col.green, col.blue, alpha=0.85 if i == n - 1 else 0.20)
            c.setFillColor(tint)
            c.circle(cx, cy, r, stroke=0, fill=1)
        for i, (label, sub, col) in enumerate(self.rings):
            r = radii[i]
            c.setStrokeColor(col); c.setLineWidth(LINE_RULE)
            c.circle(cx, cy, r, stroke=1, fill=0)
        # leader lines from each ring's rim (staggered angles so they don't cross)
        angles = [70, 25, -25, -60][:n]
        tag_h = 15 * len(self.tags) + (16 if self.tags else 0)
        ys = []
        top_y = self._h - 10
        bottom_y = tag_h + 22          # keep clear of the tag divider below
        for i in range(n):
            ys.append(top_y - i * ((top_y - bottom_y) / max(n - 1, 1)))
        for i, (label, sub, col) in enumerate(self.rings):
            r = radii[i]
            a = math.radians(angles[i % len(angles)])
            px, py = cx + r * math.cos(a), cy + r * math.sin(a)
            ty = ys[i]
            c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
            c.line(px, py, lx - 10, ty)
            c.setStrokeColor(col); c.setLineWidth(LINE_BOLD)
            c.line(lx - 10, ty - 3.2, lx - 10, ty + 3.2)
            c.setFont("Sans-B", 7.0); c.setFillColor(col)
            tracked(c, lx, ty - 2.2, label, 0.6)
            p = _t(sub, 6.1, colr=SLATE, lead=7.8)
            p.wrapOn(c, self.width - lx, 40)
            p.drawOn(c, lx, ty - 6.5 - p.height)
        if self.tags:
            ty = tag_h - 8
            c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
            c.line(0, ty + 12, self.width, ty + 12)
            for j, (tag, note) in enumerate(self.tags):
                yy = ty - j * 15
                c.setFont("Sans-B", 6.6); c.setFillColor(GOLD)
                tracked(c, 0, yy, tag, 0.9)
                w = tracked_w(c, tag, 0.9)
                c.setFont("Sans", 6.4); c.setFillColor(SLATE)
                c.drawString(w + 8, yy, note)


# =============================================================== lineage chart
class LineageChart(Flowable):
    """Cross versus hybrid, shown as parentage against a species boundary.

    Two coloured lanes (same-species / different-species) with parent chips
    placed in the correct lane and merged with a connector into an offspring
    chip. A cross keeps both parents in one lane; a hybrid's offspring straddles
    the boundary. The rule is shown, not stated.
    """
    def __init__(self, lanes, rows, width=L_W, row_h=54):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.lanes, self.rows, self.width, self.row_h = lanes, list(rows), width, row_h

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self._h = self.row_h * len(self.rows) + 26
        return (self.width, self._h)

    def _chip(self, c, cx, cy, label, col, w=None):
        p = _t(label, 7.0, bold=True, colr=colors.white, align=TA_CENTER)
        w = w or (tracked_w(c, label, 0.3) + 16)
        h = 15
        c.setFillColor(col)
        c.roundRect(cx - w / 2, cy - h / 2, w, h, h / 2, stroke=0, fill=1)
        c.setFont("Sans-B", 7.0); c.setFillColor(colors.white)
        tracked(c, cx, cy - 2.4, label, 0.3, "c")
        return w

    def draw(self):
        c = self.canv
        W = self.width
        laneA_x = (0, W * 0.42)
        laneB_x = (W * 0.58, W)
        (labA, colA), (labB, colB) = self.lanes
        top = self._h - 6
        c.setFillColor(colors.Color(colA.red, colA.green, colA.blue, alpha=0.08))
        c.rect(laneA_x[0], 0, laneA_x[1] - laneA_x[0], top - 8, stroke=0, fill=1)
        c.setFillColor(colors.Color(colB.red, colB.green, colB.blue, alpha=0.08))
        c.rect(laneB_x[0], 0, laneB_x[1] - laneB_x[0], top - 8, stroke=0, fill=1)
        c.setFont("Sans-B", 6.6); c.setFillColor(colA)
        tracked(c, (laneA_x[0] + laneA_x[1]) / 2, top, labA, 0.9, "c")
        c.setFillColor(colB)
        tracked(c, (laneB_x[0] + laneB_x[1]) / 2, top, labB, 0.9, "c")
        c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR); c.setDash(1.5, 2)
        c.line(W / 2.0, 0, W / 2.0, top - 4); c.setDash()

        y = top - 24
        for parent1, lane1, parent2, lane2, child, tag, tagcol in self.rows:
            lx = {"A": sum(laneA_x) / 2 - W * 0.10, "B": sum(laneB_x) / 2 - W * 0.10}[lane1]
            rx = {"A": sum(laneA_x) / 2 + W * 0.10, "B": sum(laneB_x) / 2 + W * 0.10}[lane2]
            p1x = {"A": laneA_x[0] + (laneA_x[1] - laneA_x[0]) * 0.30,
                   "B": laneB_x[0] + (laneB_x[1] - laneB_x[0]) * 0.30}[lane1]
            p2x = {"A": laneA_x[0] + (laneA_x[1] - laneA_x[0]) * 0.70,
                   "B": laneB_x[0] + (laneB_x[1] - laneB_x[0]) * 0.70}[lane2]
            cx = (p1x + p2x) / 2.0
            cy = y - 22
            self._chip(c, p1x, y, parent1, SLATE)
            self._chip(c, p2x, y, parent2, SLATE)
            c.setStrokeColor(MUTE); c.setLineWidth(LINE_HAIR)
            c.line(p1x, y - 8, cx, cy + 8)
            c.line(p2x, y - 8, cx, cy + 8)
            self._chip(c, cx, cy, child, tagcol)
            c.setFont("Sans-B", 6.6); c.setFillColor(tagcol)
            tracked(c, cx + 46, cy - 2.2, tag, 0.9)
            y -= self.row_h


# =============================================================== bar chart
class BarChart(Flowable):
    """Horizontal bars. rows: [(label, value, display)] \u2014 display defaults to value%."""
    def __init__(self, rows, maxv=None, width=L_W, lab_w=124, bar_h=12, gap=6,
                 colour=BURGUNDY, highlight=None):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.rows, self.width, self.lab_w = list(rows), width, lab_w
        self.bar_h, self.gap, self.colour = bar_h, gap, colour
        self.maxv = maxv or max(r[1] for r in rows)
        self.highlight = highlight or []

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self._h = len(self.rows) * (self.bar_h + self.gap) + 4
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        avail = self.width - self.lab_w - 46
        y = self._h - self.bar_h - 2
        for lab, val, *rest in self.rows:
            disp = rest[0] if rest else f"{val}%"
            col = GOLD if lab in self.highlight else self.colour
            c.setFont("Sans", 7.2); c.setFillColor(INK)
            c.drawRightString(self.lab_w - 6, y + 3, lab)
            c.setFillColor(colors.HexColor("#EDEAE4"))
            c.rect(self.lab_w, y, avail, self.bar_h, stroke=0, fill=1)
            w = max(avail * val / float(self.maxv), 1.2)
            c.setFillColor(col); c.rect(self.lab_w, y, w, self.bar_h, stroke=0, fill=1)
            c.setFont("Sans-B", 7.2); c.setFillColor(col)
            c.drawString(self.lab_w + w + 5, y + 3, disp)
            y -= self.bar_h + self.gap


# =============================================================== slope profile
class SlopeDiagram(Flowable):
    """Hillside cross-section: sun angle, aspect and the flat-land contrast."""
    def __init__(self, width=L_W, height=162):
        Flowable.__init__(self); self.width, self.height = width, height
        self.spaceBefore = GAP; self.spaceAfter = 0

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        base = 54                      # ground line; legend sits below it
        top = H - 4
        c.setFillColor(SKY); c.setStrokeColor(HAIRLINE); c.setLineWidth(0.5)
        c.rect(0, base, W, top - base, stroke=1, fill=1)
        # hill
        c.setFillColor(colors.HexColor("#C9B48E")); c.setStrokeColor(SOIL); c.setLineWidth(0.9)
        p = c.beginPath(); p.moveTo(0, base)
        p.lineTo(W * 0.28, base)
        p.curveTo(W * 0.42, base + 6, W * 0.44, base + (top - base) * 0.62,
                  W * 0.55, base + (top - base) * 0.66)
        p.curveTo(W * 0.66, base + (top - base) * 0.70, W * 0.74, base + 34, W * 0.88, base)
        p.lineTo(W, base); p.close(); c.drawPath(p, stroke=1, fill=1)
        # sun, upper left, with rays angling down onto the sun-facing flank
        sx, sy = W * 0.16, top - 20
        c.setFillColor(GOLD); c.circle(sx, sy, 7.5, stroke=0, fill=1)
        c.setFont("Sans-B", 6.3); c.setFillColor(GOLD)
        c.drawCentredString(sx, sy + 11, "SUN")
        c.setStrokeColor(GOLD); c.setLineWidth(0.8)
        for i in range(4):
            x0 = sx + 9 + i * 3
            y0 = sy - 3 - i * 4
            c.line(x0, y0, x0 + W * 0.22, y0 - (top - base) * 0.30)
            # arrow head
            c.setFillColor(GOLD)
            hx, hy = x0 + W * 0.22, y0 - (top - base) * 0.30
            pa = c.beginPath(); pa.moveTo(hx, hy); pa.lineTo(hx - 5, hy + 1.5)
            pa.lineTo(hx - 3, hy + 4.5); pa.close(); c.drawPath(pa, stroke=0, fill=1)
        # on-hill label, white on brown
        c.setFont("Sans-B", 7.0); c.setFillColor(colors.white)
        c.drawCentredString(W * 0.47, base + (top - base) * 0.26, "SUN-FACING SLOPE")
        c.setFont("Sans", 6.1)
        c.drawCentredString(W * 0.47, base + (top - base) * 0.26 - 8,
                            "radiation nearer perpendicular")
        c.drawCentredString(W * 0.47, base + (top - base) * 0.26 - 15,
                            "\u2192 more intense heat and light")
        # ground line + legend row beneath
        c.setStrokeColor(SLATE); c.setLineWidth(0.8); c.line(0, base, W, base)
        keys = [("FLAT LAND", "radiation spread over a wider area"),
                ("SUN-FACING", "extends the viable season at both ends"),
                ("SHADED / AWAY", "limits heat \u2014 wanted in warm climates")]
        cw = W / 3.0
        for i, (k, v) in enumerate(keys):
            x = i * cw
            c.setFillColor(GOLD if i == 1 else SLATE)
            c.rect(x, base - 16, 5, 5, stroke=0, fill=1)
            c.setFont("Sans-B", 6.4); c.setFillColor(BURGUNDY)
            c.drawString(x + 8, base - 16, k)
            c.setFont("Sans", 6.0); c.setFillColor(SLATE)
            c.drawString(x + 8, base - 24, v)
        c.setFont("Sans", 6.1); c.setFillColor(SLATE)
        c.drawString(0, base - 38, "Sun-facing = SOUTH in the northern hemisphere, NORTH in the "
                                   "southern. Importance rises with latitude,")
        c.drawString(0, base - 46, "and is greatest in spring and autumn when the sun sits lowest.")


# =============================================================== texture triangle
class TextureTriangle(Flowable):
    """Ternary diagram of sand / silt / clay with the properties of each corner."""
    def __init__(self, width=L_W, size=None):
        Flowable.__init__(self); self.width = width; self.size = size
        self.spaceBefore = GAP; self.spaceAfter = 0

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self.size = self.size or min(self.width * 0.58, 152)
        self._h = self.size * 0.866 + 70
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        s = self.size
        ox = (self.width - s) / 2.0
        oy = 52
        ax, ay = ox, oy                       # sand (bottom-left)
        bx, by = ox + s, oy                    # clay (bottom-right)
        tx, ty = ox + s / 2.0, oy + s * 0.866  # silt (top)
        c.setFillColor(colors.HexColor("#F1EDE6")); c.setStrokeColor(SOIL); c.setLineWidth(1.0)
        p = c.beginPath(); p.moveTo(ax, ay); p.lineTo(bx, by); p.lineTo(tx, ty); p.close()
        c.drawPath(p, stroke=1, fill=1)
        # loam in the middle
        gx, gy = (ax + bx + tx) / 3.0, (ay + by + ty) / 3.0
        c.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.30))
        c.setStrokeColor(GOLD); c.setLineWidth(0.8)
        c.circle(gx, gy, s * 0.155, stroke=1, fill=1)
        c.setFont("Sans-B", 7.4); c.setFillColor(BURGUNDY)
        c.drawCentredString(gx, gy + 2, "LOAM")
        c.setFont("Sans", 6.0); c.setFillColor(SLATE)
        c.drawCentredString(gx, gy - 7, "moderate proportions")
        c.drawCentredString(gx, gy - 14, "of all three")
        # corners
        def corner(x, y, name, lines, dx, dy, anchor):
            c.setFillColor(BURGUNDY); c.circle(x, y, 2.4, stroke=0, fill=1)
            c.setFont("Sans-B", 7.2); c.setFillColor(BURGUNDY)
            f = c.drawCentredString if anchor == "c" else (
                c.drawString if anchor == "l" else c.drawRightString)
            f(x + dx, y + dy, name)
            c.setFont("Sans", 6.1); c.setFillColor(SLATE)
            for i, ln in enumerate(lines):
                f(x + dx, y + dy - 7.4 * (i + 1), ln)
        corner(ax, ay, "SAND", ["large particles \u00b7 drains easily",
                                "poor at nutrients", "loose \u2014 easy for roots"], -4, -11, "l")
        corner(bx, by, "CLAY", ["very small particles",
                                "holds water and nutrients", "sticky; hard for roots"], 4, -11, "r")
        corner(tx, ty, "SILT", ["intermediate size", "properties between the two"], 0, 13, "c")
        c.setFont("Sans", 6.1); c.setFillColor(SLATE)
        c.drawCentredString(self.width / 2.0, 3,
                            "Gravel and pebbles improve drainage but lower water- and "
                            "nutrient-holding capacity")


# =============================================================== botanical parts
def _blend(c1, c2, k):
    return colors.Color(c1.red + (c2.red - c1.red) * k,
                        c1.green + (c2.green - c1.green) * k,
                        c1.blue + (c2.blue - c1.blue) * k)


LEAF_MID   = colors.HexColor("#5F7A46")
LEAF_LIGHT = colors.HexColor("#7E9A5E")
LEAF_DARK  = colors.HexColor("#3F5730")
BERRY_DARK = colors.HexColor("#4A1B2C")
BERRY_MID  = colors.HexColor("#6E2740")
BERRY_LIT  = colors.HexColor("#8E4059")
WOOD_DARK  = colors.HexColor("#4E3A26")
WOOD_MID   = colors.HexColor("#6E5236")
WOOD_LIT   = colors.HexColor("#8B6C48")


def _vine_leaf(c, cx, cy, R, rot=0.0, fill=LEAF_MID, veins=True, flip=False, stalk=True):
    """A Cabernet Sauvignon-type leaf: a closed, orbicular five-lobe rosette.

    Real Vitis leaves stay cohesive even when deeply cut \u2014 the apex, two
    laterals and two basal lobes all read as one rounded body, not five
    separate blobs. This is built as a single closed loop of five lobes (no
    special-cased petiole gap): the apex is longest, the laterals shorter, the
    two basal lobes shortest, and the sinus between the two basal lobes \u2014
    which is where the petiole attaches \u2014 is simply the fifth sinus in the
    loop, matching the closed, near-overlapping petiolar sinus that gives the
    variety its \u2018mask\u2019 nickname among ampelographers. The stalk is drawn
    afterward as a short line from that low point, external to the fill.
    """
    centers = (18.0, 90.0, 162.0, 234.0, 306.0)   # lat-R, apex, lat-L, basal-L, basal-R
    tops = (0.90, 1.00, 0.90, 0.72, 0.72)
    floors = (0.60, 0.60, 0.66, 0.58, 0.66)        # superior, superior, inferior, petiolar, inferior
    p_exp = 0.80
    N = 220
    pts = []
    for i in range(N + 1):
        u = i / float(N)
        seg = min(int(u * 5), 4)
        s = u * 5 - seg
        topA, topB = tops[seg], tops[(seg + 1) % 5]
        floor = floors[seg]
        top_env = topA + (topB - topA) * s
        shape = (math.cos(2 * math.pi * s) + 1) / 2.0
        tooth = 0.009 * math.sin(u * math.pi * 13)
        r = R * max(floor + (top_env - floor) * (shape ** p_exp) + tooth, 0.25)
        adeg = centers[seg] + s * 72.0 + rot
        a = math.radians(adeg)
        x = cx + r * math.cos(a) * (1.0 if not flip else -1.0)
        y = cy + r * math.sin(a)
        pts.append((x, y))
    c.setFillColor(fill); c.setStrokeColor(LEAF_DARK); c.setLineWidth(0.3)
    path = c.beginPath(); path.moveTo(*pts[0])
    for x, y in pts[1:]:
        path.lineTo(x, y)
    path.close(); c.drawPath(path, stroke=1, fill=1)

    if veins:
        c.setStrokeColor(_blend(fill, LEAF_DARK, 0.5))
        base_a = math.radians(270.0 + rot)         # the petiolar sinus point
        bx = cx + R * floors[3] * math.cos(base_a) * (1.0 if not flip else -1.0)
        by = cy + R * floors[3] * math.sin(base_a)
        for k, ctr in enumerate(centers):
            a = math.radians(ctr + rot)
            r = R * tops[k] * 0.88
            c.setLineWidth(0.5 if k == 1 else 0.32)
            c.line(bx, by, cx + r * math.cos(a) * (1.0 if not flip else -1.0),
                   cy + r * math.sin(a))

    if stalk:
        base_a = math.radians(270.0 + rot)
        bx = cx + R * floors[3] * math.cos(base_a) * (1.0 if not flip else -1.0)
        by = cy + R * floors[3] * math.sin(base_a)
        c.setStrokeColor(_blend(fill, WOOD_DARK, 0.35)); c.setLineWidth(1.3)
        c.line(bx, by, bx - (2.2 if not flip else -2.2), by - R * 0.30)


def _bunch(c, cx, cy, w, h, rows=None):
    """A conical bunch: overlapping berries, widest at the shoulder, tapering
    to a single berry at the tip, each with a small specular highlight."""
    rows = rows or [4, 4, 3, 3, 2, 1]
    n = len(rows)
    rad = w / (max(rows) * 1.55)
    for ri, count in enumerate(rows):
        fy = ri / float(n - 1)
        y = cy - fy * h
        spread = w * (1.0 - 0.72 * fy) / 2.0
        for k in range(count):
            fx = 0.5 if count == 1 else k / float(count - 1)
            x = cx - spread + fx * spread * 2
            jitter = ((ri * 7 + k * 13) % 5 - 2) * 0.30
            rr = rad * (1.0 - 0.14 * fy)
            c.setFillColor(_blend(BERRY_MID, BERRY_DARK, fy * 0.5))
            c.setStrokeColor(BERRY_DARK); c.setLineWidth(0.25)
            c.circle(x + jitter, y, rr, stroke=1, fill=1)
            c.setFillColor(_blend(BERRY_LIT, colors.white, 0.35))
            c.circle(x + jitter - rr * 0.30, y + rr * 0.32, rr * 0.20, stroke=0, fill=1)


def _taper(c, x0, y0, x1, y1, w0, w1, fill):
    """A stroke that tapers from w0 to w1 \u2014 drawn as a quadrilateral so wood
    and roots thin out naturally rather than reading as pipes."""
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / ln, dx / ln
    c.setFillColor(fill)
    p = c.beginPath()
    p.moveTo(x0 + nx * w0 / 2, y0 + ny * w0 / 2)
    p.lineTo(x1 + nx * w1 / 2, y1 + ny * w1 / 2)
    p.lineTo(x1 - nx * w1 / 2, y1 - ny * w1 / 2)
    p.lineTo(x0 - nx * w0 / 2, y0 - ny * w0 / 2)
    p.close(); c.drawPath(p, stroke=0, fill=1)


def _arm(c, x0, y0, x1, y1, w0, w1, rise=4.0, fill=WOOD_MID, steps=26):
    """A curved, tapering woody arm \u2014 used for cordons, which are neither
    straight nor of constant thickness."""
    top, bot = [], []
    for i in range(steps + 1):
        u = i / float(steps)
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u + rise * math.sin(math.pi * u)
        w = w0 + (w1 - w0) * u
        top.append((x, y + w / 2)); bot.append((x, y - w / 2))
    c.setFillColor(fill)
    p = c.beginPath(); p.moveTo(*top[0])
    for pt in top[1:]:
        p.lineTo(*pt)
    for pt in reversed(bot):
        p.lineTo(*pt)
    p.close(); c.drawPath(p, stroke=0, fill=1)


def _roots(c, x, y, ang, length, w, depth=0, seed=0, floor=3.0):
    """Recursive tapering root system, clipped to the soil band."""
    if depth > 3 or length < 3.5:
        return
    a = math.radians(ang)
    x1 = x + length * math.cos(a)
    y1 = y + length * math.sin(a)
    if y1 < floor:                        # never draw below the soil band
        if y - floor < 2:
            return
        k = (y - floor) / max(y - y1, 0.001)
        x1, y1 = x + (x1 - x) * k, floor
    _taper(c, x, y, x1, y1, w, w * 0.55,
           _blend(WOOD_MID, colors.HexColor("#B9A183"), min(depth * 0.28, 0.85)))
    spread = 26 - depth * 4
    for s in (-1, 1):
        _roots(c, x1, y1, ang + s * (spread + ((seed + depth * 5) % 7)),
               length * 0.62, w * 0.55, depth + 1, seed + 1, floor)


def _seed(c, x, y, R, rot=0):
    """Pyriform grape seed: rounded body, tapered beak, visible chalaza."""
    c.saveState(); c.translate(x, y); c.rotate(rot)
    c.setFillColor(colors.HexColor("#7A5A32")); c.setStrokeColor(colors.HexColor("#4E3A20"))
    c.setLineWidth(0.3)
    p = c.beginPath()
    p.moveTo(0, R)                                   # beak tip
    p.curveTo(R * 0.62, R * 0.42, R * 0.72, -R * 0.42, 0, -R)
    p.curveTo(-R * 0.72, -R * 0.42, -R * 0.62, R * 0.42, 0, R)
    p.close(); c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#9C7A4A"))
    c.ellipse(-R * 0.26, -R * 0.46, R * 0.26, R * 0.04, stroke=0, fill=1)
    c.restoreState()


# =============================================================== trellis profiles
class TrellisProfile(Flowable):
    """Four schematic vine cross-sections, side by side, showing the physical
    canopy shape each training/trellising system produces \u2014 an actual
    illustration rather than a text comparison, using the same leaf-drawing
    primitive as the other botanical figures so the whole set reads as one
    system."""
    def __init__(self, width=L_W, height=112):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.width, self.height = width, height

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return (self.width, self.height)

    def _leaf_cluster(self, c, cx, cy_start, n, spread_x, dy, seed, upward=True):
        rnd = random.Random(seed)
        for i in range(n):
            ly = cy_start + (i * dy if upward else -i * dy)
            lx = cx + rnd.uniform(-spread_x, spread_x)
            r = rnd.uniform(4.2, 6.0)
            fill = _blend(LEAF_MID, LEAF_LIGHT, rnd.random())
            _vine_leaf(c, lx, ly, r, rot=rnd.uniform(0, 360), fill=fill, stalk=False)

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        base = 32
        n = 4
        colw = W / n
        panels = [
            ("BUSH VINE", "No wires \u2014 shoots droop and self-shade", self._bush),
            ("VSP", "Single narrow vertical canopy", self._vsp),
            ("GDC / LYRE", "Canopy split sideways into two curtains", self._gdc),
            ("SCOTT-HENRY", "Canopy split up and down from one point", self._scott_henry),
        ]
        for i, (label, note, fn) in enumerate(panels):
            cx = colw * i + colw / 2.0
            c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
            c.line(colw * i + 6, base, colw * i + colw - 6, base)
            fn(c, cx, base)
            c.setFont("Sans-B", 6.4); c.setFillColor(BURGUNDY)
            c.drawCentredString(cx, base - 12, label)
            c.setFont("Sans", 5.7); c.setFillColor(MUTE)
            words = note.split()
            line1, line2 = " ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])
            c.drawCentredString(cx, base - 20, line1)
            c.drawCentredString(cx, base - 27, line2)

    def _bush(self, c, cx, base):
        top = base + 26
        _taper(c, cx, base, cx, top, 5, 3, WOOD_MID)
        self._leaf_cluster(c, cx, top - 6, 11, 15, 0, seed=1, upward=True)

    def _vsp(self, c, cx, base):
        top = base + 62
        _taper(c, cx, base, cx, top, 4, 2.5, WOOD_MID)
        c.setStrokeColor(HAIRLINE); c.setLineWidth(0.6)
        for wy in (base + 24, base + 40, base + 56):
            c.line(cx - 15, wy, cx + 15, wy)
        self._leaf_cluster(c, cx, base + 20, 11, 6.5, 3.6, seed=2, upward=True)

    def _gdc(self, c, cx, base):
        mid = base + 42
        _taper(c, cx, base, cx, mid, 4, 3, WOOD_MID)
        _arm(c, cx, mid, cx - 20, mid + 3, 3, 2, rise=5, fill=WOOD_MID)
        _arm(c, cx, mid, cx + 20, mid + 3, 3, 2, rise=5, fill=WOOD_MID)
        for side in (-1, 1):
            self._leaf_cluster(c, cx + side * 20, mid - 2, 7, 4.5, 3.2,
                                seed=3 + side, upward=False)

    def _scott_henry(self, c, cx, base):
        split = base + 38
        _taper(c, cx, base, cx, split, 4, 2.5, WOOD_MID)
        c.setStrokeColor(HAIRLINE); c.setLineWidth(0.6)
        c.line(cx - 14, split, cx + 14, split)
        self._leaf_cluster(c, cx, split + 6, 6, 6, 3.4, seed=5, upward=True)
        self._leaf_cluster(c, cx, split - 6, 6, 6, 3.4, seed=6, upward=False)


# =============================================================== irrigation profiles
WATER = colors.HexColor("#4E6E8C")
WATER_LIT = colors.HexColor("#7FA0BE")


class IrrigationProfile(Flowable):
    """Four schematic cross-sections showing how each irrigation method
    physically delivers water \u2014 an illustration of mechanism, not just a
    labelled list of names."""
    def __init__(self, width=L_W, height=130):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.width, self.height = width, height

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return (self.width, self.height)

    def _vine(self, c, cx, base, h=22):
        _taper(c, cx, base, cx, base + h, 3.5, 2.2, WOOD_MID)
        rnd = random.Random(int(cx))
        for i in range(5):
            ly = base + h - 4 + rnd.uniform(-2, 4)
            lx = cx + rnd.uniform(-9, 9)
            _vine_leaf(c, lx, ly, rnd.uniform(3.6, 4.8), rot=rnd.uniform(0, 360),
                       fill=_blend(LEAF_MID, LEAF_LIGHT, rnd.random()), stalk=False)

    def _soil(self, c, x0, x1, base):
        c.setFillColor(colors.HexColor("#DED2B8"))
        c.rect(x0, base - 8, x1 - x0, 8, stroke=0, fill=1)

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        base = 40
        n = 4
        colw = W / n
        panels = [("DRIP", self._drip), ("FLOOD", self._flood),
                  ("CHANNEL", self._channel), ("OVERHEAD", self._overhead)]
        for i, (label, fn) in enumerate(panels):
            x0, x1 = colw * i + 6, colw * i + colw - 6
            cx = (x0 + x1) / 2.0
            self._soil(c, x0, x1, base)
            fn(c, cx, x0, x1, base)
            self._vine(c, cx, base)
            c.setFont("Sans-B", 6.4); c.setFillColor(BURGUNDY)
            c.drawCentredString(cx, base - 20, label)

    def _drip(self, c, cx, x0, x1, base):
        c.setStrokeColor(WATER); c.setLineWidth(1.4)
        c.line(x0 + 6, base + 26, x1 - 6, base + 26)
        rnd = random.Random(11)
        for dx in (-14, 0, 14):
            c.setFillColor(WATER_LIT)
            c.circle(cx + dx, base + 26, 1.3, stroke=0, fill=1)
            c.setFillColor(WATER)
            c.circle(cx + dx, base - 3, 1.6, stroke=0, fill=1)
            c.setStrokeColor(WATER); c.setLineWidth(0.5)
            c.line(cx + dx, base + 24, cx + dx, base - 1)

    def _flood(self, c, cx, x0, x1, base):
        c.setFillColor(colors.Color(WATER.red, WATER.green, WATER.blue, alpha=0.55))
        c.rect(x0, base - 8, x1 - x0, 7, stroke=0, fill=1)
        c.setStrokeColor(WATER_LIT); c.setLineWidth(0.6)
        for wx in range(int(x0) + 4, int(x1) - 3, 7):
            c.line(wx, base - 2, wx + 4, base - 2)

    def _channel(self, c, cx, x0, x1, base):
        c.setStrokeColor(colors.HexColor("#DED2B8")); c.setLineWidth(6)
        c.setFillColor(WATER)
        p = c.beginPath()
        p.moveTo(cx - 10, base - 1); p.lineTo(cx, base - 7); p.lineTo(cx + 10, base - 1)
        p.lineTo(cx + 10, base - 8); p.lineTo(cx, base - 12); p.lineTo(cx - 10, base - 8)
        p.close(); c.drawPath(p, stroke=0, fill=1)
        c.setFillColor(WATER); c.setFont("Sans-B", 7)
        c.drawCentredString(cx + 16, base - 6, "\u2192")

    def _overhead(self, c, cx, x0, x1, base):
        sx, sy = cx, base + 40
        c.setStrokeColor(SLATE); c.setLineWidth(1.0)
        c.line(sx - 5, sy, sx + 5, sy)
        c.setStrokeColor(WATER); c.setLineWidth(0.6)
        for ang in (-55, -20, 20, 55):
            a = math.radians(ang - 90)
            ex = sx + 20 * math.sin(math.radians(ang))
            ey = sy + 20 * math.cos(math.radians(ang))
            c.line(sx, sy, ex, ey)
            c.setFillColor(WATER_LIT); c.circle(ex, ey, 1.1, stroke=0, fill=1)


# =============================================================== decision tree
class DecisionTree(Flowable):
    """A branching diagnostic tree \u2014 one root question, two first-level
    branches, each either a terminal outcome or a second question splitting
    into two more outcomes. The structural complement to FlowChart: FlowChart
    is for a fixed sequence with no choice point, this is for 'it depends'.

    root_q: the root question text.
    branches: exactly two (edge_label, content) pairs, where content is
    either a leaf string (terminal outcome) or a further
    (question_text, [(edge_label, leaf_string), ...2 items]) tuple.
    """
    def __init__(self, root_q, branches, width=L_W, height=None):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.root_q, self.branches, self.width = root_q, branches, width
        self._height_override = height

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        any_split = any(isinstance(c, tuple) for _, c in self.branches)
        self._h = self._height_override or (150 if any_split else 90)
        return (self.width, self._h)

    def _box(self, c, x, y, w, h, text, accent, bold=False, size=6.6):
        c.setFillColor(colors.HexColor("#F7F5F1"))
        c.setStrokeColor(BOXEDGE); c.setLineWidth(0.5)
        c.rect(x, y, w, h, stroke=1, fill=1)
        c.setFillColor(accent)
        c.rect(x, y, 2.2, h, stroke=0, fill=1)
        p = _t(text, size, colr=INK, bold=bold)
        p.wrapOn(c, w - 10, h - 6)
        p.drawOn(c, x + 6, y + h - p.height - 5)

    def _edge(self, c, x0, y0, x1, y1, label):
        c.setStrokeColor(SLATE); c.setLineWidth(0.8)
        c.line(x0, y0, x1, y1)
        mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        c.setFont("Sans-B", 6.0)
        lw = pdfmetrics.stringWidth(label, "Sans-B", 6.0) + 6
        c.setFillColor(colors.white); c.rect(mx - lw / 2, my - 5, lw, 10, stroke=0, fill=1)
        c.setFillColor(GOLD); c.drawCentredString(mx, my - 2.1, label)

    def draw(self):
        c = self.canv
        W, top = self.width, self._h - 6
        rw, rh = min(W * 0.62, 240), 30
        rx, ry = (W - rw) / 2.0, top - rh
        self._box(c, rx, ry, rw, rh, self.root_q, BURGUNDY, bold=True, size=6.8)
        n = len(self.branches)
        colw = W / n
        for i, (label, content) in enumerate(self.branches):
            bx = colw * i + colw / 2.0
            branch_top = ry - 30
            self._edge(c, rx + rw / 2.0, ry, bx, branch_top + 12, label)
            if isinstance(content, tuple):
                q2, leaves2 = content
                qw, qh = min(colw * 0.88, 150), 24
                qx, qy = bx - qw / 2.0, branch_top - qh
                self._box(c, qx, qy, qw, qh, q2, SLATE, size=6.2)
                n2 = len(leaves2)
                subw = colw / n2
                for j, (lab2, leaf) in enumerate(leaves2):
                    lx = colw * i + subw * j + subw / 2.0
                    ly = qy - 36
                    lw2, lh2 = min(subw * 0.92, 118), 24
                    self._box(c, lx - lw2 / 2.0, ly, lw2, lh2, leaf, MILD, size=6.0)
                    self._edge(c, qx + qw / 2.0, qy, lx, ly + lh2, lab2)
            else:
                lw2, lh2 = min(colw * 0.9, 150), 24
                self._box(c, bx - lw2 / 2.0, branch_top - lh2, lw2, lh2, content, MILD)


# =============================================================== timeline
class Timeline(Flowable):
    """A time-proportional axis \u2014 distinct from FlowChart, whose boxes are
    evenly spaced regardless of how much real time separates the steps.
    Here horizontal position is proportional to an actual date/value, so a
    reader can see which events are close together and which are far apart.

    lo, hi: axis bounds (numeric \u2014 a year, or a day-of-season count).
    events: [(value, label, note)] \u2014 note may be "" for a bare marker.
    """
    def __init__(self, lo, hi, events, width=L_W, axis_label="", unit=""):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.lo, self.hi, self.events = lo, hi, list(events)
        self.width, self.axis_label, self.unit = width, axis_label, unit

    def _x(self, v):
        return 10 + (v - self.lo) / float(self.hi - self.lo) * (self.width - 20)

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        order = sorted(range(len(self.events)), key=lambda i: self.events[i][0])
        lvl, last = {}, {}
        for i in order:
            v = self.events[i][0]
            x = self._x(v)
            k = 0
            while k in last and (x - 42) < last[k]:
                k += 1
            lvl[i] = k
            last[k] = x + 42
        self._lvl = lvl
        self._nlev = (max(lvl.values()) + 1) if lvl else 1
        self._h = 30 + self._nlev * 40
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        axis_y = self._h - self._nlev * 40 - 4
        c.setStrokeColor(INK); c.setLineWidth(LINE_RULE)
        c.line(10, axis_y, self.width - 10, axis_y)
        c.setFont("Sans", 6.0); c.setFillColor(MUTE)
        c.drawString(10, axis_y - 10, f"{self.lo}{self.unit}")
        c.drawRightString(self.width - 10, axis_y - 10, f"{self.hi}{self.unit}")
        for i, (v, label, note) in enumerate(self.events):
            x = self._x(v)
            k = self._lvl[i]
            c.setFillColor(BURGUNDY); c.circle(x, axis_y, 2.3, stroke=0, fill=1)
            c.setStrokeColor(BURGUNDY); c.setLineWidth(LINE_HAIR)
            y0 = axis_y + 5
            y1 = axis_y + 16 + k * 40
            c.line(x, y0, x, y1)
            c.setFont("Sans-B", 6.6); c.setFillColor(BURGUNDY)
            c.drawCentredString(x, y1 + 3, label)
            if note:
                p = _t(note, 5.9, colr=SLATE)
                aw = min(self.width / max(len(self.events), 1) + 20, 110)
                p.wrapOn(c, aw, 30)
                p.drawOn(c, x - aw / 2.0, y1 + 12)


# =============================================================== pie chart
class PieChart(Flowable):
    """Parts-of-a-whole. slices: [(label, value, colour)] \u2014 values need not
    be pre-converted to percentages, the chart normalises them."""
    def __init__(self, slices, width=L_W, diameter=92, title=""):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.slices, self.width, self.diameter, self.title = list(slices), width, diameter, title

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        self._h = self.diameter + 10
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        total = sum(v for _, v, _ in self.slices) or 1.0
        r = self.diameter / 2.0
        cx, cy = r + 6, self._h / 2.0
        start = 90.0
        legend_x = self.diameter + 24
        ly = self._h - 12
        for label, val, col in self.slices:
            sweep = -360.0 * val / total
            c.setFillColor(col); c.setStrokeColor(colors.white); c.setLineWidth(1.2)
            p = c.beginPath()
            p.moveTo(cx, cy)
            p.arcTo(cx - r, cy - r, cx + r, cy + r, start + sweep, -sweep)
            p.close(); c.drawPath(p, stroke=1, fill=1)
            start += sweep
            pct = round(100.0 * val / total)
            c.setFillColor(colors.HexColor("#EDEAE4"))
            c.rect(legend_x, ly - 8, 8, 8, stroke=0, fill=1)
            c.setFillColor(col); c.rect(legend_x, ly - 8, 8, 8, stroke=0, fill=1)
            c.setFont("Sans-B", 6.8); c.setFillColor(INK)
            c.drawString(legend_x + 12, ly - 6.5, f"{label} \u2014 {pct}%")
            ly -= 14


# =============================================================== location map
class LocationMap(Flowable):
    """A minimal latitude/longitude grid with labelled points \u2014 honest about
    being schematic (no coastlines are drawn, since approximating them badly
    would be worse than not drawing them), but genuinely spatial: relative
    latitude and longitude are real and to scale."""
    def __init__(self, lon_lo, lon_hi, lat_lo, lat_hi, points, width=L_W, height=140):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.lon_lo, self.lon_hi, self.lat_lo, self.lat_hi = lon_lo, lon_hi, lat_lo, lat_hi
        self.points, self.width, self.height = list(points), width, height

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return (self.width, self.height)

    def _xy(self, lon, lat):
        x = 8 + (lon - self.lon_lo) / float(self.lon_hi - self.lon_lo) * (self.width - 16)
        y = 22 + (lat - self.lat_lo) / float(self.lat_hi - self.lat_lo) * (self.height - 40)
        return x, y

    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#F7F5F1")); c.setStrokeColor(BOXEDGE)
        c.setLineWidth(0.6)
        c.rect(4, 18, self.width - 8, self.height - 30, stroke=1, fill=1)
        for lat in range(int(self.lat_lo) // 5 * 5, int(self.lat_hi) + 1, 5):
            if not (self.lat_lo <= lat <= self.lat_hi):
                continue
            _, y = self._xy(self.lon_lo, lat)
            c.setStrokeColor(colors.HexColor("#E4E0D6")); c.setLineWidth(0.4)
            c.line(6, y, self.width - 6, y)
            c.setFont("Sans", 5.4); c.setFillColor(MUTE)
            c.drawString(8, y - 8, f"{lat}\u00b0N")
        for lon, lat, label, note in self.points:
            x, y = self._xy(lon, lat)
            # clamp label alignment near the frame edges so text never spills out
            if x < self.width * 0.22:
                align = "l"
            elif x > self.width * 0.78:
                align = "r"
            else:
                align = "c"
            c.setFillColor(BURGUNDY); c.circle(x, y, 2.6, stroke=0, fill=1)
            c.setFont("Sans-B", 6.4); c.setFillColor(BURGUNDY)
            ly = y + 18
            lx = x if align == "c" else (x - 9 if align == "r" else x + 9)
            if align == "l":
                c.drawString(lx, ly, label)
            elif align == "r":
                c.drawRightString(lx, ly, label)
            else:
                c.drawCentredString(lx, ly, label)
            if note:
                c.setFont("Sans", 5.6); c.setFillColor(SLATE)
                if align == "l":
                    c.drawString(lx, ly - 9, note)
                elif align == "r":
                    c.drawRightString(lx, ly - 9, note)
                else:
                    c.drawCentredString(lx, ly - 9, note)


# =============================================================== pictogram
class Pictogram(Flowable):
    """A count shown as repeated icons rather than a number \u2014 for small,
    concrete quantities where 'see it' lands harder than 'read it'.
    icon_fn(canv, cx, cy, r, filled) draws one unit; filled distinguishes the
    counted portion from the uncounted remainder."""
    def __init__(self, total, counted, icon_fn, width=L_W, label="", r=7, per_row=10):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.total, self.counted, self.icon_fn = total, counted, icon_fn
        self.width, self.label, self.r, self.per_row = width, label, r, per_row

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        rows = math.ceil(self.total / float(self.per_row))
        self._h = rows * (self.r * 2.4) + 22
        return (self.width, self._h)

    def draw(self):
        c = self.canv
        gap = min((self.width - 16) / self.per_row, self.r * 2.6)
        x0 = 8
        top = self._h - self.r - 4
        for i in range(self.total):
            row, col = divmod(i, self.per_row)
            cx = x0 + col * gap + self.r
            cy = top - row * (self.r * 2.4)
            self.icon_fn(c, cx, cy, self.r, i < self.counted)
        if self.label:
            c.setFont("Sans", 6.4); c.setFillColor(SLATE)
            c.drawString(x0, 8, self.label)


def grape_icon(c, cx, cy, r, filled):
    col = BURGUNDY if filled else colors.HexColor("#DCD7CB")
    c.setFillColor(col); c.setStrokeColor(colors.white); c.setLineWidth(0.6)
    for dx, dy in ((-r * 0.4, r * 0.15), (r * 0.4, r * 0.15), (0, -r * 0.35)):
        c.circle(cx + dx, cy + dy, r * 0.42, stroke=1, fill=1)


# =============================================================== berry section
class BerrySection(Flowable):
    """Cross-section of a grape berry, annotated."""
    def __init__(self, width=L_W, height=186):
        Flowable.__init__(self); self.width, self.height = width, height
        self.spaceBefore = GAP; self.spaceAfter = 0

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        cx, cy = W * 0.235, H * 0.50
        R = min(W * 0.185, H * 0.34)
        ry = R * 1.08                      # berries are slightly prolate

        # bloom \u2014 a soft haze built from stacked translucent rings
        for i in range(7):
            k = i / 6.0
            c.setFillColor(colors.Color(0.90, 0.90, 0.94, alpha=0.10))
            c.ellipse(cx - R * (1.02 + k * 0.13), cy - ry * (1.02 + k * 0.13),
                      cx + R * (1.02 + k * 0.13), cy + ry * (1.02 + k * 0.13),
                      stroke=0, fill=1)

        # pedicel and brush
        c.setStrokeColor(colors.HexColor("#5E7141")); c.setLineWidth(2.4)
        c.line(cx, cy + ry * 0.96, cx - 2, cy + ry + 15)
        c.setStrokeColor(colors.HexColor("#C7B48F")); c.setLineWidth(0.4)
        for i in range(5):
            c.line(cx, cy + ry * 0.90, cx - 5 + i * 2.5, cy + ry * 0.55)

        # skin \u2014 concentric bands to fake a gradient from dark rim to inner face
        for i in range(9):
            k = i / 8.0
            c.setFillColor(_blend(BERRY_DARK, BERRY_LIT, k))
            f = 1.0 - k * 0.095
            c.ellipse(cx - R * f, cy - ry * f, cx + R * f, cy + ry * f, stroke=0, fill=1)

        # pulp
        pr = 0.845
        c.setFillColor(colors.HexColor("#EDE5D0"))
        c.ellipse(cx - R * pr, cy - ry * pr, cx + R * pr, cy + ry * pr, stroke=0, fill=1)
        # faint radial cell walls
        c.setStrokeColor(colors.HexColor("#DCD0B4")); c.setLineWidth(0.3)
        for i in range(22):
            a_ = math.radians(i * 360.0 / 22)
            c.line(cx + R * 0.18 * math.cos(a_), cy + ry * 0.18 * math.sin(a_),
                   cx + R * (pr - 0.03) * math.cos(a_), cy + ry * (pr - 0.03) * math.sin(a_))
        # locule division
        c.setStrokeColor(colors.HexColor("#D3C5A6")); c.setLineWidth(0.45)
        c.line(cx, cy - ry * pr * 0.9, cx, cy + ry * pr * 0.9)

        # seeds \u2014 two per locule, beaks toward the stem end
        for dx, dy, rot in ((-0.34, 0.16, -18), (0.34, 0.16, 18),
                            (-0.30, -0.30, -30), (0.30, -0.30, 30)):
            _seed(c, cx + dx * R, cy + dy * ry, R * 0.215, rot)

        # specular highlight on the skin
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.20))
        c.saveState(); c.translate(cx - R * 0.46, cy + ry * 0.52); c.rotate(-36)
        c.ellipse(-R * 0.24, -R * 0.075, R * 0.24, R * 0.075, stroke=0, fill=1)
        c.restoreState()

        ann = [
            (0.885, "SKIN", "aroma compounds and precursors \u00b7 <b>tannins</b> \u00b7 <b>colour</b><br/>"
                            "far higher tannin and colour in black grapes"),
            (0.665, "PULP", "water \u00b7 sugars \u00b7 acids \u00b7 some aroma compounds<br/>"
                            "most of the weight and volume \u00b7 <b>colourless</b> except teinturier"),
            (0.455, "SEEDS", "oils \u00b7 tannins \u00b7 the embryo<br/>mature from yellow to dark brown"),
            (0.265, "BLOOM", "powdery waxy coating on the berry surface"),
            (0.095, "STEM", "<b>tannins</b> \u00b7 attaches the grape to the vine"),
        ]
        lx = W * 0.50
        for frac, name, sub in ann:
            y = H * frac
            c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
            c.line(cx + R * 1.30, y, lx - 6, y)
            c.setStrokeColor(BURGUNDY); c.setLineWidth(LINE_BOLD)
            c.line(lx - 6, y - 3.2, lx - 6, y + 3.2)
            c.setFont("Sans-B", 7.0); c.setFillColor(BURGUNDY)
            tracked(c, lx, y - 2.4, name, 0.7)
            p = _t(sub, 6.2, colr=SLATE, lead=8.0)
            p.wrapOn(c, W - lx - 42, 60)
            p.drawOn(c, lx + 42, y - p.height + 5.5)


# =============================================================== vine schematic
class VineSchematic(Flowable):
    """A trained vine drawn botanically, with the four structural zones called out."""
    def __init__(self, width=L_W, height=188):
        Flowable.__init__(self); self.width, self.height = width, height
        self.spaceBefore = GAP; self.spaceAfter = 0

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        W, H = self.width, self.height
        gx = W * 0.30                       # vine axis
        soil_y = H * 0.29
        half = W * 0.148                    # cordon reach

        # ---- soil -----------------------------------------------------------
        c.setFillColor(colors.HexColor("#E8DFCE"))
        c.rect(0, 0, W, soil_y, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#DCD0B8"))
        for i in range(120):                # a light aggregate texture
            x = (i * 61.8) % W
            y = ((i * 37.3) % (soil_y - 6)) + 3
            c.circle(x, y, 0.55 + ((i % 3) * 0.35), stroke=0, fill=1)
        c.setStrokeColor(SOIL); c.setLineWidth(LINE_RULE)
        c.line(0, soil_y, W, soil_y)

        # ---- roots ----------------------------------------------------------
        for ang, ln, w in ((-62, soil_y * 0.30, 3.2), (-90, soil_y * 0.36, 3.8),
                           (-118, soil_y * 0.30, 3.2), (-36, soil_y * 0.22, 2.2),
                           (-144, soil_y * 0.22, 2.2)):
            _roots(c, gx, soil_y - 1, ang, ln, w, 0, int(abs(ang)), floor=4.0)

        # ---- trunk: tapered, slightly sinuous, with bark shading ------------
        trunk_top = soil_y + H * 0.235
        for k, (off, wid, col) in enumerate(((0, 11.0, WOOD_MID), (-1.6, 5.0, WOOD_DARK),
                                             (2.6, 3.0, WOOD_LIT))):
            c.setFillColor(col)
            p = c.beginPath()
            p.moveTo(gx - wid / 2 + off, soil_y - 2)
            p.curveTo(gx - wid / 2 - 2 + off, soil_y + H * 0.10,
                      gx - wid / 2 + 2.5 + off, soil_y + H * 0.17,
                      gx - wid * 0.34 + off, trunk_top)
            p.lineTo(gx + wid * 0.34 + off, trunk_top)
            p.curveTo(gx + wid / 2 + 2.5 + off, soil_y + H * 0.17,
                      gx + wid / 2 - 2 + off, soil_y + H * 0.10,
                      gx + wid / 2 + off, soil_y - 2)
            p.close(); c.drawPath(p, stroke=0, fill=1)

        # ---- cordons: curved, tapering arms with spur nubs ------------------
        for s in (-1, 1):
            _arm(c, gx, trunk_top, gx + s * half, trunk_top - 1.5, 8.4, 3.6,
                 rise=3.2, fill=WOOD_MID)
            _arm(c, gx, trunk_top + 1.2, gx + s * half * 0.97, trunk_top - 0.4,
                 3.0, 1.2, rise=3.2, fill=WOOD_LIT)
            _arm(c, gx, trunk_top - 2.6, gx + s * half, trunk_top - 3.4,
                 2.2, 0.9, rise=3.2, fill=WOOD_DARK)

        # ---- shoots, leaves, tendrils, bunches ------------------------------
        shoot_h = H * 0.285
        n = 6
        for i in range(n):
            fx = i / float(n - 1)
            x = gx - half * 0.92 + fx * half * 1.84
            lean = (fx - 0.5) * 12
            top_y = trunk_top + shoot_h * (0.82 + 0.18 * math.sin(i * 1.7))
            # spur nub where the shoot leaves the cordon
            c.setFillColor(WOOD_DARK)
            c.circle(x, trunk_top + 2.4, 2.1, stroke=0, fill=1)
            c.setStrokeColor(LEAF_DARK); c.setLineWidth(1.15)
            p = c.beginPath(); p.moveTo(x, trunk_top + 3)
            p.curveTo(x + lean * 0.3, trunk_top + shoot_h * 0.4,
                      x + lean * 0.8, trunk_top + shoot_h * 0.7, x + lean, top_y)
            c.drawPath(p, stroke=1, fill=0)
            # tendril at the tip
            c.setStrokeColor(LEAF_MID); c.setLineWidth(0.55)
            p = c.beginPath(); p.moveTo(x + lean, top_y)
            p.curveTo(x + lean + 7, top_y + 4, x + lean + 2, top_y + 9,
                      x + lean + 8, top_y + 11)
            c.drawPath(p, stroke=1, fill=0)
            # leaves alternating along the shoot
            for j in range(3):
                fy = 0.26 + j * 0.28
                lx = x + lean * fy
                ly = trunk_top + 3 + shoot_h * fy * 0.95
                side = 1 if (i + j) % 2 == 0 else -1
                shade = _blend(LEAF_MID, LEAF_LIGHT, (j % 2) * 0.55)
                _vine_leaf(c, lx + side * 6.8, ly + 2, 7.4 + (j % 2) * 1.0,
                           rot=side * 16 + j * 11, fill=shade, flip=side < 0,
                           stalk=False)
            # bunches hang below the shoulder on alternate shoots
            if i in (1, 3, 5):
                _bunch(c, x + lean * 0.18, trunk_top - 3, 10.0, 13.0)

        # ---- annotation ------------------------------------------------------
        zones = [
            (trunk_top + shoot_h * 0.72, 0.955, "SHOOTS",
             "current season's green growth \u2014 buds, leaves, laterals, tendrils, bunches. "
             "<b>Shoots + their structures = the canopy</b>"),
            (trunk_top + 1, 0.680, "ONE-YEAR-OLD WOOD",
             "last season's shoots kept at winter pruning; carries the compound buds. "
             "Left as a <b>cane</b> or a <b>spur</b>"),
            (soil_y + H * 0.115, 0.440, "PERMANENT WOOD",
             "trunk and cordons \u2014 support, transport, carbohydrate and nutrient storage"),
            (soil_y * 0.44, 0.185, "ROOTS",
             "anchorage, uptake, storage, <b>hormone production</b>. Most in the "
             "<b>top 50 cm</b>; some beyond <b>6 m</b>"),
        ]
        lx = W * 0.585
        for fy, sy_frac, name, sub in zones:
            ly = H * sy_frac
            c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
            c.line(gx + half + 6, fy, lx - 16, fy)
            c.line(lx - 16, fy, lx - 7, ly - 2)
            c.setStrokeColor(BURGUNDY); c.setLineWidth(LINE_BOLD)
            c.line(lx - 7, ly - 5.4, lx - 7, ly + 1.2)
            c.setFont("Sans-B", 7.0); c.setFillColor(BURGUNDY)
            tracked(c, lx, ly - 4, name, 0.7)
            p = _t(sub, 6.2, colr=SLATE, lead=8.0)
            p.wrapOn(c, W - lx - 2, 60)
            p.drawOn(c, lx, ly - 9 - p.height)


# =============================================================== 2x2 matrix
class Matrix2x2(Flowable):
    """Quadrant chart. quads: dict of 'tl','tr','bl','br' \u2192 (title, body)."""
    def __init__(self, x_lo, x_hi, y_lo, y_hi, quads, width=L_W, height=176,
                 x_axis="", y_axis=""):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.x_lo, self.x_hi, self.y_lo, self.y_hi = x_lo, x_hi, y_lo, y_hi
        self.quads, self.width, self.height = quads, width, height
        self.x_axis, self.y_axis = x_axis, y_axis

    def wrap(self, aw, ah):
        self.width = min(self.width, aw)
        return (self.width, self.height + 14)

    def draw(self):
        c = self.canv
        W = self.width; H = self.height
        L, B = 26, 26
        w2 = (W - L) / 2.0; h2 = (H - B) / 2.0
        fills = {"tl": colors.HexColor("#F3EFE8"), "tr": colors.HexColor("#EDE7DA"),
                 "bl": colors.HexColor("#F7F5F1"), "br": colors.HexColor("#F1EDE4")}
        pos = {"tl": (L, B + h2), "tr": (L + w2, B + h2), "bl": (L, B), "br": (L + w2, B)}
        for k, (x, y) in pos.items():
            if k not in self.quads:
                continue
            title, bodytxt = self.quads[k]
            c.setFillColor(fills[k]); c.setStrokeColor(BOXEDGE); c.setLineWidth(0.5)
            c.rect(x, y, w2, h2, stroke=1, fill=1)
            pt = _t(title, 7.0, bold=True, colr=BURGUNDY)
            pt.wrapOn(c, w2 - 12, 40); pt.drawOn(c, x + 6, y + h2 - pt.height - 6)
            pb = _t(bodytxt, 6.2, colr=INK)
            pb.wrapOn(c, w2 - 12, h2 - 24)
            pb.drawOn(c, x + 6, y + h2 - pt.height - 10 - pb.height)
        # axes
        c.setStrokeColor(SLATE); c.setLineWidth(0.9)
        c.line(L, B, W, B); c.line(L, B, L, B + 2 * h2)
        c.setFillColor(SLATE)
        for xx, yy, dx, dy in ((W, B, -5, 0), (L, B + 2 * h2, 0, -5)):
            p = c.beginPath()
            if dx: p.moveTo(xx, yy); p.lineTo(xx + dx, yy + 3); p.lineTo(xx + dx, yy - 3)
            else:  p.moveTo(xx, yy); p.lineTo(xx + 3, yy + dy); p.lineTo(xx - 3, yy + dy)
            p.close(); c.drawPath(p, stroke=0, fill=1)
        c.setFont("Sans-B", 6.4); c.setFillColor(BURGUNDY)
        c.drawString(L, B - 10, self.x_lo)
        c.drawRightString(W, B - 10, self.x_hi)
        c.saveState(); c.translate(L - 8, B); c.rotate(90)
        c.drawString(0, 0, self.y_lo); c.drawRightString(2 * h2, 0, self.y_hi)
        c.restoreState()
        if self.x_axis:
            c.setFont("Sans", 6.2); c.setFillColor(SLATE)
            c.drawCentredString(L + w2, B - 19, self.x_axis)


# =============================================================== planning space
class PlanningRules(Flowable):
    """Ruled planning space that expands to fill whatever is left of the page.

    Because wrap() reports the frame's remaining height, this never forces a new
    page \u2014 it simply converts leftover space on the short-written-answer page
    into somewhere to plan an answer before turning over.
    """
    def __init__(self, label="PLAN YOUR ANSWER", gap=19.5, min_h=70):
        Flowable.__init__(self)
        self.spaceBefore = GAP; self.spaceAfter = 0
        self.label, self.gap, self.min_h = label, gap, min_h

    def wrap(self, aw, ah):
        self.width = aw
        self._h = max(ah - 4, 0)
        if self._h < self.min_h:
            self._h = 0
        return (self.width, self._h)

    def draw(self):
        if not self._h:
            return
        c = self.canv
        top = self._h - 12
        c.setFont("Sans-B", 6.8); c.setFillColor(MUTE)
        tracked(c, 0, top, self.label, 1.25)
        c.setStrokeColor(HAIRLINE); c.setLineWidth(LINE_HAIR)
        c.line(0, top - 5, self.width, top - 5)
        y = top - 5 - self.gap
        c.setStrokeColor(colors.HexColor("#E9E7E3")); c.setLineWidth(0.3)
        while y > 2:
            c.line(0, y, self.width, y)
            y -= self.gap
