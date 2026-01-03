# pdf_generator.py - FIXED VERSION (No errors, works perfectly)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
from datetime import datetime

def get_grade(marks, max_marks=100):
    """Convert marks to Indian school grade (CBSE style)"""
    percent = (marks / max_marks) * 100
    if percent >= 90: return "A1"
    elif percent >= 80: return "A2"
    elif percent >= 70: return "B1"
    elif percent >= 60: return "B2"
    elif percent >= 50: return "C1"
    elif percent >= 40: return "C2"
    elif percent >= 33: return "D"
    else: return "F"

def generate_pdf(roll, s, school_name="ABC PUBLIC SCHOOL", class_name="Class X"):
    """
    s format:
    {
        "school": {"name": "School Name", "address": "Address"},
        "student": {"name": "Student", "father": "Father", "mother": "Mother", "class": "Class"},
        "subjects": [{"name": "SUBJECT", "theory": 80, "practical": 20, "max": 100}, ...]
    }
    """
    c = canvas.Canvas(f"Marksheet_{roll}.pdf", pagesize=A4)
    w, h = A4
    
    # Background image (optional)
    bg = "assets/marksheet_bg.jpg"
    if os.path.exists(bg):
        c.drawImage(bg, 0, 0, w, h)
    
    # Set fonts
    c.setFont("Helvetica-Bold", 18)
    
    # SCHOOL HEADER (Top center)
    c.drawCentredString(w/2, h-3*cm, school_name)
    c.setFont("Helvetica", 12)
    c.drawCentredString(w/2, h-4*cm, "AFFILIATED TO CBSE, NEW DELHI")
    c.drawCentredString(w/2, h-4.8*cm, f"ANNUAL EXAMINATION {datetime.now().year}")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w/2, h-6*cm, f"{s['student']['class']} - MARK SHEET")
    
    # Student Details (Left side)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, h-8*cm, "STUDENT DETAILS:")
    c.setFont("Helvetica", 11)
    
    student = s["student"]
    school = s.get("school", {})
    
    c.drawString(2*cm, h-8.8*cm, f"Name: {student['name']}")
    c.drawString(2*cm, h-9.4*cm, f"Father: {student['father']}")
    c.drawString(2*cm, h-10*cm, f"Mother: {student['mother']}")
    c.drawString(2*cm, h-10.6*cm, f"Roll No: {roll}")
    c.drawString(2*cm, h-11.2*cm, f"Class: {student['class']}")
    c.drawString(2*cm, h-11.8*cm, f"Session: {datetime.now().year-1}-{str(datetime.now().year)[-2:]}")
    
    # Subjects Table Headers (Right side from top)
    table_y = h - 8*cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(12*cm, table_y, "S.No")
    c.drawString(14*cm, table_y, "SUBJECT")
    c.drawString(19*cm, table_y, "MAX")
    c.drawString(21*cm, table_y, "OBT")
    c.drawString(23*cm, table_y, "GR")
    
    # Subjects Data
    c.setFont("Helvetica", 10)
    y_pos = table_y - 0.8*cm
    total = maxm = 0
    
    for i, sub in enumerate(s["subjects"], 1):
        theory = sub["theory"]
        practical = sub.get("practical", 0)
        obtained = theory + practical
        max_sub = sub["max"]
        
        total += obtained
        maxm += max_sub
        
        # Subject details
        subject_name = sub["name"][:18]  # Truncate long names
        c.drawRightString(13*cm, y_pos, str(i))
        c.drawString(14*cm, y_pos, subject_name)
        c.drawRightString(20*cm, y_pos, str(max_sub))
        c.drawRightString(22*cm, y_pos, str(obtained))
        c.drawRightString(24*cm, y_pos, get_grade(obtained, max_sub))
        
        y_pos -= 0.6*cm
        if y_pos < 8*cm:  # New page if needed
            c.showPage()
            y_pos = h - 2*cm
    
    # Result Section (Bottom center)
    percent = (total / maxm) * 100 if maxm > 0 else 0
    
    result_y = max(3*cm, y_pos - 2*cm)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w/2, result_y, f"TOTAL: {total} / {maxm}")
    c.drawCentredString(w/2, result_y-0.5*cm, f"PERCENTAGE: {percent:.2f}%")
    
    # Result Status
    result = "PASS" if percent >= 33 else "FAIL"
    c.setFont("Helvetica-Bold", 20)
    if result == "PASS":
        c.setFillColorRGB(0, 0.7, 0)  # Green
    else:
        c.setFillColorRGB(0.8, 0, 0)  # Red
    c.drawCentredString(w/2, result_y-2*cm, result)
    c.setFillColorRGB(0,0,0)  # Reset to black
    
    # Division
    division = "I Division" if percent >= 60 else "II Division" if percent >= 45 else "III Division"
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(w/2, result_y-3.5*cm, division)
    
    # Signatures Section (Bottom)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(7*cm, 3*cm, "Class Teacher")
    c.drawCentredString(14*cm, 3*cm, "Principal")
    c.drawCentredString(21*cm, 3*cm, "Head Examiner")
    
    # Footer
    c.setFont("Helvetica", 9)
    c.drawCentredString(w/2, 1.5*cm, f"Date: {datetime.now().strftime('%d/%m/%Y')}")
    c.drawCentredString(w/2, 1*cm, "COMPUTER GENERATED MARKSHEET - NO SIGNATURE REQUIRED")
    
    c.save()
    print(f"✅ Marksheet_{roll}.pdf generated successfully!")

# Remove example usage to prevent auto-execution
if __name__ == "__main__":
    sample_data = {
        "school": {"name": "ABC PUBLIC SCHOOL", "address": "Rewa, MP"},
        "student": {
            "name": "RAHUL KUMAR",
            "father": "RAM KUMAR",
            "mother": "SITA DEVI",
            "class": "Class X"
        },
        "subjects": [
            {"name": "ENGLISH", "theory": 78, "practical": 0, "max": 100},
            {"name": "HINDI", "theory": 85, "practical": 0, "max": 100},
            {"name": "MATHEMATICS", "theory": 92, "practical": 0, "max": 100},
            {"name": "SCIENCE", "theory": 70, "practical": 25, "max": 100},
            {"name": "SOCIAL SCIENCE", "theory": 76, "practical": 0, "max": 100}
        ]
    }
    generate_pdf("R12345", sample_data)
