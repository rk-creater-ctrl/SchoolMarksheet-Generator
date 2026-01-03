def start() :
    # user_view.py - FIXED VERSION
    import tkinter as tk
    from tkinter import ttk, messagebox
    from PIL import Image, ImageTk
    import json, os
    from pdf_generator import generate_pdf

    def start(parent):
        win = tk.Toplevel()
        win.title("View Result")
        win.protocol("WM_DELETE_WINDOW", lambda: (win.destroy(), parent.deiconify()))


    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_FILE = os.path.join(BASE_DIR, "students.json")
    BG_PATH = os.path.join(BASE_DIR, "assets", "marksheet_bg.jpg")

    def load_db():
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    db = load_db()

    root = tk.Tk()
    root.title("🎓 Student Result Portal")
    root.state("zoomed")
    root.configure(bg="#f1f5f9")

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    scale = min(screen_w / 1366, screen_h / 768)
    root.tk.call("tk", "scaling", scale)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Segoe UI", 14), padding=12)
    style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), background="#f1f5f9")

    # Header
    ttk.Label(root, text="🎓 Student Result Portal", style="Header.TLabel").pack(pady=30)

    # Search Card
    card = ttk.LabelFrame(root, text="🔍 Search Result", padding=30)
    card.pack(padx=50, pady=20, fill="x")

    session_var = tk.StringVar()
    roll_var = tk.StringVar()

    ttk.Label(card, text="Session (2024-25)", font=("Segoe UI", 13)).grid(row=0, column=0, sticky="w", pady=10)
    ttk.Entry(card, textvariable=session_var, font=("Segoe UI", 13), width=20).grid(row=1, column=0, padx=20, pady=5, sticky="ew")

    ttk.Label(card, text="Roll Number", font=("Segoe UI", 13)).grid(row=0, column=1, sticky="w", pady=10)
    ttk.Entry(card, textvariable=roll_var, font=("Segoe UI", 13), width=20).grid(row=1, column=1, pady=5, sticky="ew")

    card.columnconfigure(1, weight=1)

    # PDF Preview Canvas (A4 size)
    preview_frame = ttk.LabelFrame(root, text="📄 Marksheet Preview", padding=10)
    preview_frame.pack(padx=50, pady=20, fill="both", expand=True)

    canvas = tk.Canvas(preview_frame, width=600, height=850, bg="white", relief="solid", bd=2)
    canvas.pack(pady=10)

    # Background
    if os.path.exists(BG_PATH):
        try:
            bg_img = Image.open(BG_PATH).resize((600, 850), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_img)
            canvas.create_image(0, 0, image=bg_photo, anchor="nw")
            canvas.bg_photo = bg_photo
        except:
            pass

    def view_result():
        canvas.delete("result_data")

        try:
            session = session_var.get()
            roll = roll_var.get()
            data = db[session][roll]
            student = data["student"]
            school = data.get("school", {})
        except KeyError:
            messagebox.showerror("❌ Not Found", "Result not found for this Roll No/Session!")
            return

        # School Header
        canvas.create_text(300, 80, text=school.get("name", "ABC PUBLIC SCHOOL"), 
                          font=("Arial", 16, "bold"), fill="navy", tags="result_data")
        canvas.create_text(300, 110, text=school.get("address", ""), 
                          font=("Arial", 12), tags="result_data")

        # Student Details
        canvas.create_text(100, 180, text="Name:", font=("Arial", 11, "bold"), tags="result_data")
        canvas.create_text(250, 180, text=student["name"], font=("Arial", 11), tags="result_data")

        canvas.create_text(100, 210, text="Father:", font=("Arial", 11, "bold"), tags="result_data")
        canvas.create_text(250, 210, text=student["father"], font=("Arial", 11), tags="result_data")

        canvas.create_text(450, 180, text="Roll:", font=("Arial", 11, "bold"), tags="result_data")
        canvas.create_text(500, 180, text=roll, font=("Arial", 11), tags="result_data")

        canvas.create_text(450, 210, text="Class:", font=("Arial", 11, "bold"), tags="result_data")
        canvas.create_text(500, 210, text=student["class"], font=("Arial", 11), tags="result_data")

        # Subjects Table
        y = 260
        canvas.create_text(80, y, text="S.No", font=("Arial", 11, "bold"), tags="result_data")
        canvas.create_text(120, y, text="Subject", font=("Arial", 11, "bold"), tags="result_data")
        canvas.create_text(350, y, text="Max", font=("Arial", 11, "bold"), tags="result_data")
        canvas.create_text(420, y, text="Obt", font=("Arial", 11, "bold"), tags="result_data")
        canvas.create_text(500, y, text="Grade", font=("Arial", 11, "bold"), tags="result_data")
        y += 30

        total_obt, total_max = 0, 0
        for i, sub in enumerate(data["subjects"], 1):
            marks = sub["theory"] + sub["practical"]
            total_obt += marks
            total_max += sub["max"]

            canvas.create_text(70, y, text=str(i), font=("Arial", 10), tags="result_data")
            canvas.create_text(120, y, text=sub["name"][:20], font=("Arial", 10), anchor="w", tags="result_data")
            canvas.create_text(370, y, text=str(sub["max"]), font=("Arial", 10), tags="result_data")
            canvas.create_text(440, y, text=str(marks), font=("Arial", 10), tags="result_data")
            canvas.create_text(520, y, text=get_grade(marks, sub["max"]), font=("Arial", 10), tags="result_data")
            y += 28

        # Result Summary
        percent = (total_obt / total_max) * 100 if total_max else 0
        result = "PASS" if percent >= 33 else "FAIL"

        canvas.create_text(300, y+20, text=f"TOTAL: {total_obt}/{total_max}", 
                          font=("Arial", 14, "bold"), tags="result_data")
        canvas.create_text(300, y+50, text=f"PERCENTAGE: {percent:.1f}%", 
                          font=("Arial", 14, "bold"), tags="result_data")
        canvas.create_text(300, y+80, text=result, 
                          font=("Arial", 18, "bold"), fill="green" if result == "PASS" else "red", tags="result_data")

    def get_grade(marks, max_marks):
        percent = (marks / max_marks) * 100
        if percent >= 90: return "A1"
        elif percent >= 80: return "A2"
        elif percent >= 70: return "B1"
        elif percent >= 60: return "B2"
        elif percent >= 50: return "C1"
        elif percent >= 40: return "C2"
        elif percent >= 33: return "D"
        else: return "F"

    def export_pdf():
        try:
            session = session_var.get()
            roll = roll_var.get()
            data = db[session][roll]
            generate_pdf(roll, data, data["school"]["name"])
            messagebox.showinfo("✅ Success", f"Marksheet_{roll}.pdf generated successfully!")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to generate PDF: {str(e)}")

    # Buttons
    btn_frame = tk.Frame(card)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

    ttk.Button(btn_frame, text="🔍 VIEW RESULT", command=view_result).pack(side="left", padx=10)
    ttk.Button(btn_frame, text="⬇️ DOWNLOAD PDF", command=export_pdf).pack(side="left", padx=10)

    root.mainloop()
