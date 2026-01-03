# admin_panel.py - COMPLETE FIXED VERSION
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os
from PIL import Image, ImageTk
from pdf_generator import generate_pdf

DB_FILE = "students.json"
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

db = load_db()
subjects = []
school_logo = ""
student_photo = ""

root = tk.Tk()
root.title("Admin Panel - School Marksheet System")
root.state("zoomed")
root.configure(bg="#edf1f7")

scale = min(root.winfo_screenwidth()/1366, root.winfo_screenheight()/768)
root.tk.call("tk", "scaling", scale)

main = tk.Frame(root, bg="#edf1f7", width=1200, height=750)
main.place(relx=0.5, rely=0.5, anchor="center")
main.pack_propagate(False)

# ========== SUBJECTS PANEL ==========
subjects_frame = tk.LabelFrame(main, text="📚 Subjects Configuration", bg="white", padx=15, pady=10)
subjects_frame.pack(fill="x", padx=20, pady=10)

def add_subject():
    win = tk.Toplevel(root)
    win.title("Add Subject")
    win.geometry("400x300")
    win.configure(bg="white")
    win.transient(root)
    win.grab_set()
    
    tk.Label(win, text="Subject Name", font=("Segoe UI", 12), bg="white").pack(pady=10)
    sub_name = tk.StringVar()
    tk.Entry(win, textvariable=sub_name, font=("Segoe UI", 12), width=30).pack(pady=5)
    
    tk.Label(win, text="Max Marks", font=("Segoe UI", 12), bg="white").pack(pady=10)
    max_marks = tk.StringVar(value="100")
    tk.Entry(win, textvariable=max_marks, font=("Segoe UI", 12), width=30).pack(pady=5)
    
    tk.Label(win, text="Theory Marks", font=("Segoe UI", 12), bg="white").pack(pady=10)
    theory = tk.StringVar(value="80")
    tk.Entry(win, textvariable=theory, font=("Segoe UI", 12), width=30).pack(pady=5)
    
    tk.Label(win, text="Practical Marks", font=("Segoe UI", 12), bg="white").pack(pady=10)
    practical = tk.StringVar(value="20")
    tk.Entry(win, textvariable=practical, font=("Segoe UI", 12), width=30).pack(pady=5)
    
    def save_sub():
        subjects.append({
            "name": sub_name.get().upper(),
            "theory": int(theory.get()),
            "practical": int(practical.get()),
            "max": int(max_marks.get())
        })
        update_subjects_list()
        win.destroy()
    
    ttk.Button(win, text="Add Subject", command=save_sub).pack(pady=20)

def update_subjects_list():
    for widget in subjects_list.winfo_children():
        widget.destroy()
    for i, sub in enumerate(subjects):
        ttk.Label(subjects_list, text=f"{i+1}. {sub['name']} ({sub['theory']}+{sub['practical']}={sub['max']})",
                 font=("Segoe UI", 10)).pack(anchor="w")

subjects_list = tk.Listbox(subjects_frame, height=6, font=("Segoe UI", 10))
subjects_list.pack(fill="x", pady=5)

ttk.Button(subjects_frame, text="➕ Add Subject", command=add_subject).pack(pady=5)
ttk.Button(subjects_frame, text="🗑 Clear All", 
          command=lambda: [globals().__setitem__('subjects', []), update_subjects_list()]).pack(pady=5)

# ========== STUDENT DETAILS ==========
card = tk.LabelFrame(main, text="👤 Student Details", bg="white", padx=20, pady=15)
card.pack(fill="x", padx=20, pady=10)
card.columnconfigure((0,1,2), weight=1)

def field(p, t, r, c):
    tk.Label(p, text=t, bg="white", font=("Segoe UI", 11, "bold")).grid(row=r, column=c, sticky="w", pady=5)
    v = tk.StringVar()
    ttk.Entry(p, textvariable=v, font=("Segoe UI", 11)).grid(row=r+1, column=c, sticky="ew", pady=5)
    return v

session = field(card, "📅 Session (2024-25)", 0, 0)
roll    = field(card, "🎫 Roll No", 0, 1)
clas    = field(card, "🏫 Class", 0, 2)
name    = field(card, "👨‍👩‍👦 Name", 2, 0)
father  = field(card, "👨 Father", 2, 1)
mother  = field(card, "👩 Mother", 2, 2)
dob     = field(card, "📅 DOB (DD/MM/YYYY)", 4, 0)

# ========== SCHOOL INFO ==========
school_frame = tk.LabelFrame(main, text="🏫 School Information", bg="white", padx=20, pady=15)
school_frame.pack(fill="x", padx=20, pady=10)
school_frame.columnconfigure(0, weight=1)

school_name = tk.StringVar(value="ABC PUBLIC SCHOOL")
school_addr = tk.StringVar(value="Rewa, Madhya Pradesh")
tk.Label(school_frame, text="School Name", bg="white", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
ttk.Entry(school_frame, textvariable=school_name, font=("Segoe UI", 11)).grid(row=1, column=0, sticky="ew", pady=5)

tk.Label(school_frame, text="Address", bg="white", font=("Segoe UI", 11, "bold")).grid(row=2, column=0, sticky="w")
ttk.Entry(school_frame, textvariable=school_addr, font=("Segoe UI", 11)).grid(row=3, column=0, sticky="ew", pady=5)

def save():
    if not subjects:
        messagebox.showerror("Error", "Add at least one subject first!")
        return
    
    if not all([name.get(), roll.get(), session.get()]):
        messagebox.showerror("Error", "Fill mandatory fields!")
        return
    
    db.setdefault(session.get(), {})[roll.get()] = {
        "school": {
            "name": school_name.get(),
            "address": school_addr.get()
        },
        "student": {
            "name": name.get(),
            "father": father.get(),
            "mother": mother.get(),
            "class": clas.get(),
            "dob": dob.get()
        },
        "subjects": subjects.copy()
    }
    save_db(db)
    messagebox.showinfo("✅ Saved", f"Record saved for {name.get()}")

def preview_pdf():
    if not subjects or not roll.get():
        messagebox.showerror("Error", "Add subjects and roll number first!")
        return
    try:
        generate_pdf(roll.get(), {
            "school": {"name": school_name.get(), "address": school_addr.get()},
            "student": {"name": name.get(), "father": father.get(), "mother": mother.get(), "class": clas.get()},
            "subjects": subjects
        }, school_name.get())
        messagebox.showinfo("✅ Preview", "PDF Generated! Check Marksheet_R12345.pdf")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ========== BUTTONS ==========
btn_frame = tk.Frame(main, bg="#edf1f7")
btn_frame.pack(pady=20)

ttk.Button(btn_frame, text="💾 SAVE STUDENT", command=save, style="Accent.TButton").pack(side="left", padx=10)
ttk.Button(btn_frame, text="👁️ PREVIEW PDF", command=preview_pdf).pack(side="left", padx=10)
ttk.Button(btn_frame, text="🔄 NEW STUDENT", command=lambda: [globals().__setitem__('subjects', []), update_subjects_list(), 
                                                             [v.set("") for v in [name, father, mother, roll, session, clas, dob]]]).pack(side="left", padx=10)

# Style accent button
style = ttk.Style()
style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"), padding=15)

root.mainloop()
