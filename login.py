import tkinter as tk
from tkinter import messagebox
from database import get_connection

def show_login(root, on_success):
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("350x250")
    login_window.resizable(False, False)

    tk.Label(
        login_window,
        text="GST Management System",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            login_window.destroy()
            on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(
        login_window,
        text="Login",
        width=15,
        command=login
    ).pack(pady=20)

    login_window.grab_set()
