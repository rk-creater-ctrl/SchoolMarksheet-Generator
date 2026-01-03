# pdf_generator.py - FINAL FIXED VERSION (SELLING READY)

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
from datetime import datetime


def get_grade(marks, max_marks=100):
    percent = (marks / max_marks) * 100
    if percent >= 90:
        return "A1"
    elif percent >= 80:
        return "A2"
    elif percent >= 70:
        return "B1"
    elif percent >= 60:
        return "B2"
    elif percent >= 50:
        return "C1"
    elif percent >= 40:
        return "C2"
    elif percent >= 33:
        return "D"
    else:
        return "F"


def generate_pdf(save_path, roll, s):
    """
    save_path : full path selected by user
    roll      : roll number
    s         : student data dictionary
    """

    c = canvas.Canvas(save_path, pagesize=A4)
    w, h = A4

    # ---------------- BACKGROUND ----------------
    bg = "assets/marksheet_bg.jpg"
    if os.path.exists(bg):
        c.drawImage(bg, 0, 0, w, h)

    # ---------------- HEADER ----------------
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(w / 2, h - 3 * cm, s["school"]["name"].upper())

    c.setFont("Helvetica", 12)
    c.drawCentredString(w / 2, h - 4 * cm, "AFFILIATED TO MP BOARD")
    c.drawCentredString(
        w / 2,
        h - 4.8 * cm,
        f"ANNUAL EXAMINATION {datetime.now().year}",
    )

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(
        w / 2,
        h - 6 * cm,
        f"{s['student']['class']} MARKSHEET",
    )

    # ---------------- STUDENT DETAILS ----------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, h - 8 * cm, "STUDENT DETAILS")

    c.setFont("Helvetica", 11)
    st = s["student"]

    c.drawString(2 * cm, h - 8.8 * cm, f"Name        : {st['name']}")
    c.drawString(2 * cm, h - 9.4 * cm, f"Father Name : {st['father']}")
    c.drawString(2 * cm, h - 10 * cm, f"Mother Name : {st['mother']}")
    c.drawString(2 * cm, h - 10.6 * cm, f"Roll No     : {roll}")
    c.drawString(2 * cm, h - 11.2 * cm, f"Class       : {st['class']}")
    c.drawString(
        2 * cm,
        h - 11.8 * cm,
        f"Session     : {datetime.now().year-1}-{str(datetime.now().year)[-2:]}",
    )

    # ---------------- TABLE HEADER ----------------
    table_y = h - 8 * cm
    c.setFont("Helvetica-Bold", 11)

    c.drawString(12 * cm, table_y, "S.No")
    c.drawString(14 * cm, table_y, "SUBJECT")
    c.drawString(19 * cm, table_y, "MAX")
    c.drawString(21 * cm, table_y, "OBT")
    c.drawString(23 * cm, table_y, "GR")

    # ---------------- SUBJECTS ----------------
    c.setFont("Helvetica", 10)
    y = table_y - 0.8 * cm

    total = 0
    max_total = 0

    for i, sub in enumerate(s["subjects"], 1):
        theory = sub["theory"]
        practical = sub.get("practical", 0)
        obtained = theory + practical
        max_marks = sub["max"]

        total += obtained
        max_total += max_marks

        c.drawRightString(13 * cm, y, str(i))
        c.drawString(14 * cm, y, sub["name"][:20])
        c.drawRightString(20 * cm, y, str(max_marks))
        c.drawRightString(22 * cm, y, str(obtained))
        c.drawRightString(
            24 * cm,
            y,
            get_grade(obtained, max_marks),
        )

        y -= 0.6 * cm

    # ---------------- RESULT ----------------
    percent = (total / max_total) * 100 if max_total else 0
    result = "PASS" if percent >= 33 else "FAIL"

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, y - 1 * cm, f"TOTAL : {total} / {max_total}")
    c.drawCentredString(w / 2, y - 1.8 * cm, f"PERCENTAGE : {percent:.2f}%")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w / 2, y - 3 * cm, result)

    division = (
        "FIRST DIVISION"
        if percent >= 60
        else "SECOND DIVISION"
        if percent >= 45
        else "THIRD DIVISION"
    )

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w / 2, y - 4.2 * cm, division)

    # ---------------- SIGNATURE ----------------
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(7 * cm, 3 * cm, "Class Teacher")
    c.drawCentredString(14 * cm, 3 * cm, "Principal")
    c.drawCentredString(21 * cm, 3 * cm, "Head Examiner")

    # ---------------- FOOTER ----------------
    c.setFont("Helvetica", 9)
    c.drawCentredString(
        w / 2,
        1.5 * cm,
        f"Date : {datetime.now().strftime('%d/%m/%Y')}",
    )
    c.drawCentredString(
        w / 2,
        1 * cm,
        "This is a computer generated marksheet",
    )

    c.save()
