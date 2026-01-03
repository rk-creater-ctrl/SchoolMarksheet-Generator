def start() :
    import tkinter as tk
    from tkinter import ttk, messagebox
    import subprocess, sys
    
    def start(parent):
        win = tk.Toplevel()
        win.title("Admin Login")
        win.protocol("WM_DELETE_WINDOW", lambda: (win.destroy(), parent.deiconify()))
    
    
    ADMIN_PASSWORD = "admin123"
    
    root = tk.Tk()
    root.title("Admin Login")
    root.geometry("400x300")
    root.configure(bg="#f2f4f8")
    
    card = tk.Frame(root, bg="white")
    card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=220)
    
    tk.Label(card, text="🔐 Admin Login",
             font=("Segoe UI", 18, "bold"), bg="white").pack(pady=20)
    
    pwd = tk.StringVar()
    ttk.Entry(card, textvariable=pwd, show="*",
              font=("Segoe UI", 14)).pack(pady=10)
    
    def login():
        if pwd.get() == ADMIN_PASSWORD:
            root.destroy()
            subprocess.Popen([sys.executable, "admin_panel.py"])
        else:
            messagebox.showerror("Error", "Wrong Password")
    
    ttk.Button(card, text="LOGIN", command=login).pack(pady=20)
    
    root.mainloop()
    