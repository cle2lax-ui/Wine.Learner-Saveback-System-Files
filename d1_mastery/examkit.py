"""Shared builders for the assessment sections of each Mastery Guide."""
from mastery import (H2, H3, H4, P, SP, BUL, CALLOUT, Rule, S, L_W, FULL_W, GOLD,
                     BURGUNDY, SLATE, BOXFILL, BANDFILL, BOXEDGE)
from graphics import PlanningRules
from reportlab.platypus import Paragraph, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

LETTERS = "ABCD"


def mcq_section(questions, intro=None):
    """questions: list of dict(q=..., opts=[4], ans=index, why=...)"""
    head = [H2("Sample Examination \u2014 Multiple Choice"),
            P(intro or
        "Ten questions to audit recall before you attempt written work. Note that the live D1 "
        "paper contains no multiple choice \u2014 it is short written answer throughout \u2014 so treat "
        "this purely as a diagnostic. Any item you cannot answer instantly marks a gap to close "
        "before you write.", "note"),
            Rule(FULL_W)]
    blocks = []
    for i, q in enumerate(questions):
        blk = [Paragraph(f"{i+1}.&nbsp;&nbsp;{q['q']}", S["q"])]
        for j, o in enumerate(q["opts"]):
            blk.append(Paragraph(o, S["opt"], bulletText=f"{LETTERS[j]}."))
        blocks.append(blk)
    # the heading and its intro travel with the first question, never alone
    out = [KeepTogether(head + blocks[0])]
    for blk in blocks[1:]:
        out.append(KeepTogether(blk))
    # answer key
    rows = []
    for i, q in enumerate(questions):
        rows.append(Paragraph(
            f"<b>{i+1}. {LETTERS[q['ans']]}</b> &nbsp;\u2014&nbsp; {q['why']}", S["ans"]))
    out.append(CALLOUT("ANSWER KEY AND RATIONALE", rows, accent=BURGUNDY,
                       fill=BOXFILL, split=True, width=FULL_W))
    return out


def swa_section(items, guidance=None):
    """items: list of dict(stem=..., parts=[(text, pct)], answer=[flowables])"""
    head = [H2("Short Written Answer \u2014 Examination Practice"),
            P(guidance or
        "D1 is assessed by a single 90-minute closed-book paper of short written answer "
        "questions. Each question carries a stated percentage of the total mark; that "
        "percentage is your time budget, not a fact count. Marks are awarded for explained "
        "cause and effect, so a bare list will pass at best. The two questions below mirror "
        "that structure. Attempt them under timed conditions before reading the model answers.",
        "note"),
            Rule(FULL_W)]
    blocks = []
    for n, it in enumerate(items):
        blk = [Paragraph(f"Question {n+1}", ParagraphStyle(
            "sq", parent=S["h3"], textColor=BURGUNDY, fontName="Serif-B", spaceBefore=9))]
        if it.get("stem"):
            blk.append(P(it["stem"]))
        total = 0
        for pi, (txt, pct) in enumerate(it["parts"]):
            blk.append(Paragraph(
                f"<b>Part {chr(97+pi)})</b>&nbsp; {txt} &nbsp;<font color='#8A6A2C'><b>({pct})</b></font>",
                ParagraphStyle("pp", parent=S["body"], leftIndent=10, spaceAfter=4)))
            try:
                total += int(str(pct).strip().rstrip("%"))
            except ValueError:
                pass
        if total:
            blk.append(Paragraph(
                f"Total for this question: <b>{total}%</b> of the paper \u2014 which is also your "
                f"share of the 90 minutes.",
                ParagraphStyle("ptot", parent=S["note"], leftIndent=10, spaceBefore=2,
                               spaceAfter=6)))
        blocks.append(blk)
    # heading + intro stay with Question 1 rather than stranding at a page foot
    out = [KeepTogether(head + blocks[0])]
    for blk in blocks[1:]:
        out.append(KeepTogether(blk))
    out.append(PlanningRules())

    for n, it in enumerate(items):
        # Only the first model answer starts a fresh page, so the questions can be
        # attempted before any answer is visible; later answers flow on.
        if n == 0:
            out.append(PageBreak())
        out.append(H2(f"Model Answer \u2014 Question {n+1}"))
        out.append(P("Written as a Distinction-standard candidate would produce it under exam "
                     "conditions: signposted, cause-and-effect throughout, examples deployed as "
                     "evidence rather than decoration.", "note"))
        out.append(Rule(FULL_W))
        out.extend(it["answer"])
    return out


def answer_head(t):
    return Paragraph(t, ParagraphStyle("ah", parent=S["h4"], textColor=BURGUNDY,
                                       fontName="Sans-B", fontSize=8.2, spaceBefore=8,
                                       spaceAfter=3))


def examiner_note(flows):
    return CALLOUT("EXAMINER'S EYE \u2014 WHY THIS SCORES AT DISTINCTION", flows,
                   accent=GOLD, fill=BANDFILL, split=True, width=FULL_W)


def exam_traps(traps):
    """The five confusions that most reliably cost marks in this chapter.

    traps: list of (trap, correction) tuples. Only the first five are used.
    """
    traps = traps[:5]
    rows = []
    for tr, fix in traps:
        rows.append(Paragraph(
            f"<b>{tr}</b><br/><font color='#55585C'>{fix}</font>", S["box"]))
    return CALLOUT("EXAM TRAPS \u2014 WHERE MARKS ARE LOST", rows,
                   accent=colors.HexColor("#8C2F2F"),
                   fill=colors.HexColor("#F7F0EE"), split=True)
