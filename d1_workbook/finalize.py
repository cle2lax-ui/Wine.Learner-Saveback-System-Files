"""Lock the finished master into the FINAL release PDF.

Reads  D1_Wine_Production_Companion_Workbook_MASTER.pdf  (built by build_master.py)
writes D1_Wine_Production_Companion_Workbook_FINAL.pdf   with metadata, viewer settings and permissions.

Permissions: open freely, print (high quality), copy text, add annotations; no editing, page assembly or form changes.
The owner password comes from the environment variable D1_OWNER_PW (never stored in the repository).
"""
import os
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions as P
from pypdf.generic import NameObject, BooleanObject, DictionaryObject

OUT = "/mnt/user-data/outputs"
SRC = os.path.join(OUT, "D1_Wine_Production_Companion_Workbook_MASTER.pdf")
DST = os.path.join(OUT, "D1_Wine_Production_Companion_Workbook_FINAL.pdf")


def main():
    owner = os.environ.get("D1_OWNER_PW")
    if not owner:
        sys.exit("set D1_OWNER_PW")
    w = PdfWriter(clone_from=PdfReader(SRC))
    w.add_metadata({
        "/Title": "D1: Wine Production \u2014 Companion Workbook (Final)",
        "/Author": "Independent study companion to the WSET Level 4 Diploma in Wines, D1 (August 2026 edition)",
        "/Subject": "Exercises, answer keys, glossary and spaced-review tracker for D1 Chapters 1\u201321",
        "/Keywords": "WSET, Diploma, D1, wine production, viticulture, winemaking, workbook, study guide",
        "/Creator": "D1 Companion Workbook build system",
        "/Producer": "ReportLab + pypdf",
    })
    w.page_mode = "/UseOutlines"                     # open with the bookmarks panel
    w.page_layout = "/TwoPageRight"                  # book spreads, cover alone on the right
    w._root_object[NameObject("/ViewerPreferences")] = DictionaryObject({NameObject("/DisplayDocTitle"): BooleanObject(True)})
    perms = (P.PRINT | P.PRINT_TO_REPRESENTATION | P.EXTRACT | P.EXTRACT_TEXT_AND_GRAPHICS | P.ADD_OR_MODIFY)
    w.encrypt(user_password="", owner_password=owner, permissions_flag=perms, algorithm="AES-256")
    with open(DST, "wb") as f:
        w.write(f)
    print("wrote", DST)


if __name__ == "__main__":
    main()
