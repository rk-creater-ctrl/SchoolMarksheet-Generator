import tkinter as tk
from tkinter import ttk
import subprocess, sys

root = tk.Tk()
root.title("School Marksheet System")
root.state("zoomed")
root.configure(bg="#f2f4f8")

# Auto scaling (mobile safe, invisible)
scale = min(root.winfo_screenwidth()/1366, root.winfo_screenheight()/768)
root.tk.call("tk", "scaling", scale)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 16), padding=15)

card = tk.Frame(root, bg="white")
card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=480)

tk.Label(card, text="📘 School Marksheet",
         font=("Segoe UI", 24, "bold"), bg="white").pack(pady=40)

def open_admin():
    subprocess.Popen([sys.executable, "admin_login.py"])

def open_user():
    subprocess.Popen([sys.executable, "user_view.py"])

ttk.Button(card, text="👨‍🏫 ADMIN PANEL",
           command=open_admin).pack(pady=20)
ttk.Button(card, text="🎓 VIEW RESULT",
           command=open_user).pack(pady=20)

tk.Label(card, text="© School Result System",
         bg="white", font=("Segoe UI", 10)).pack(side="bottom", pady=20)

root.mainloop()
