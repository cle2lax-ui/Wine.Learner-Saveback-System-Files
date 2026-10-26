# -*- coding: utf-8 -*-
"""Chapter builder: auto-numbers exercises, collects scores and keys, builds the PDF and checks the page budget."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wb import *
import wb_art as A
import wb_art2 as A2

MAX_PAGES = 7


def ans_inline(answers):
    return " \u00b7 ".join('<b>(%d)</b> <font color="%s"><b>%s</b></font>' % (i + 1, hexc(ANS), a)
                           for i, a in enumerate(answers))


class Chapter:
    def __init__(self, chap, title, objectives, guide=None, outfile=None):
        self.chap, self.title = str(chap), title
        self.K, self.story, self.items, self.n = Key(), [], [], 0
        self.add = self.story.append
        self.add(Opener(self.chap, title, objectives, guide or ("Mastery Guide Chapter %s" % chap), fit=True))
        self.outfile = outfile

    def page(self):
        self.add(PageBreak())

    def ex(self, kind, title, pts, instruction, flows, key, mins=None, ref=None):
        """Add one exercise. `flows` is a flowable or list; `key` a flowable/paragraph or list."""
        self.n += 1
        num = "%s.%d" % (self.chap, self.n)
        self.add(ExHeader(num, kind, title, pts, mins=mins, ref=("Guide \u00a7%s" % ref) if ref else None))
        if instruction:
            self.add(instr(instruction))
        for f in (flows if isinstance(flows, (list, tuple)) else [flows]):
            self.add(f)
        self.K.add(num, title, key if isinstance(key, (list, tuple)) else [key])
        self.items.append((num, pts))
        return num

    def build(self, path=None):
        path = path or self.outfile or "/tmp/wb_ch%s.pdf" % self.chap
        expected = sum(1 for f in self.story if isinstance(f, PageBreak)) + 2      # exercise pages + the key
        for f in self.K.flowables(self.chap, self.title, self.items):
            self.add(f)
        n = build_pdf(path, self.chap, self.title, self.story)
        flag = "" if n <= MAX_PAGES else "   *** OVER %d PAGES ***" % MAX_PAGES
        if n != expected:
            flag += "   *** SPILL: designed %d pages, got %d ***" % (expected, n)
        print("Chapter %s workbook: %d pages -> %s%s" % (self.chap, n, path, flag))
        return n
