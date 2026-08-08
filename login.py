import tkinter as tk
from tkinter import messagebox
from database import get_connection
from theme import BG, CARD, TEXT, MUTED, PRIMARY, BORDER
from ui_helpers import make_entry, make_button

def show_login(root, on_success):
    login_window = tk.Toplevel(root)
    login_window.title("GST Management System - Login")
    login_window.geometry("460x420")
    login_window.configure(bg=BG)
    login_window.resizable(False, False)

    card = tk.Frame(
        login_window,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=310)

    tk.Label(
        card,
        text="GST Management System",
        bg=CARD,
        fg=TEXT,
        font=("Helvetica", 20, "bold")
    ).pack(pady=(28, 4))

    tk.Label(
        card,
        text="Sign in to continue",
        bg=CARD,
        fg=MUTED,
        font=("Helvetica", 11)
    ).pack(pady=(0, 20))

    tk.Label(card, text="Username", bg=CARD, fg=TEXT).pack(anchor="w", padx=40)
    username_entry = make_entry(card, width=30)
    username_entry.pack(padx=40, pady=(5, 14), ipady=6)

    tk.Label(card, text="Password", bg=CARD, fg=TEXT).pack(anchor="w", padx=40)
    password_entry = make_entry(card, width=30, show="*")
    password_entry.pack(padx=40, pady=(5, 18), ipady=6)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both username and password."
            )
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            cursor.close()
            connection.close()
        except Exception as exc:
            messagebox.showerror(
                "Database Error",
                f"Could not connect to MySQL.\n\n{exc}"
            )
            return

        if user:
            login_window.destroy()
            on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_button = make_button(card, "Login", login, primary=True, width=24)
    login_button.pack(pady=6)

    username_entry.focus_set()
    login_window.bind("<Return>", lambda event: login())
    login_window.protocol("WM_DELETE_WINDOW", root.destroy)
    login_window.transient(root)
    login_window.grab_set()
