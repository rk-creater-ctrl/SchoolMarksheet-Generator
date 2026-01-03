import tkinter as tk
from tkinter import ttk

# Import your internal modules (EXE safe)
import admin_login
import user_view

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("School Marksheet System")
root.state("zoomed")
root.configure(bg="#f2f4f8")

# Auto scaling (desktop + mobile safe)
scale = min(root.winfo_screenwidth() / 1366,
            root.winfo_screenheight() / 768)
root.tk.call("tk", "scaling", scale)

# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TButton",
    font=("Segoe UI", 16),
    padding=15
)

# ---------------- CENTER CARD ----------------
card = tk.Frame(root, bg="white")
card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=480)

tk.Label(
    card,
    text="📘 School Marksheet System",
    font=("Segoe UI", 22, "bold"),
    bg="white"
).pack(pady=40)

# ---------------- FUNCTIONS ----------------
def open_admin():
    import admin_panel
    admin_panel.start()

def open_user():
    import user_view
    user_view.start()

# ---------------- BUTTONS ----------------
ttk.Button(
    card,
    text="👨‍🏫 ADMIN PANEL",
    command=open_admin
).pack(pady=20)

ttk.Button(
    card,
    text="🎓 VIEW RESULT",
    command=open_user
).pack(pady=20)

# ---------------- FOOTER ----------------
tk.Label(
    card,
    text="© School Result Management System",
    bg="white",
    font=("Segoe UI", 10)
).pack(side="bottom", pady=20)

root.mainloop()
