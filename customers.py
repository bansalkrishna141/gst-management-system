import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from theme import BG, CARD, TEXT, MUTED
from ui_helpers import make_title, make_subtitle, make_card, make_label, make_entry, make_button

def open_customers(root):
    window = tk.Toplevel(root)
    window.title("Customer Management")
    window.geometry("820x620")
    window.configure(bg=BG)

    make_title(window, "Customer Management", 22).pack(anchor="w", padx=28, pady=(24, 2))
    make_subtitle(window, "Add and review customer records.").pack(anchor="w", padx=28)

    form_card = make_card(window)
    form_card.pack(fill="x", padx=28, pady=20)

    make_label(form_card, "Name").grid(row=0, column=0, sticky="w", padx=20, pady=(18, 5))
    make_label(form_card, "Phone").grid(row=0, column=1, sticky="w", padx=20, pady=(18, 5))
    make_label(form_card, "Email").grid(row=0, column=2, sticky="w", padx=20, pady=(18, 5))

    name_entry = make_entry(form_card, 22)
    phone_entry = make_entry(form_card, 18)
    email_entry = make_entry(form_card, 28)

    name_entry.grid(row=1, column=0, padx=20, pady=(0, 16), ipady=6)
    phone_entry.grid(row=1, column=1, padx=20, pady=(0, 16), ipady=6)
    email_entry.grid(row=1, column=2, padx=20, pady=(0, 16), ipady=6)

    table_card = make_card(window)
    table_card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

    columns = ("ID", "Name", "Phone", "Email")
    tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)

    widths = {"ID": 70, "Name": 220, "Phone": 170, "Email": 260}
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=widths[column], anchor="w")

    tree.pack(fill="both", expand=True, padx=14, pady=14)

    def load_customers():
        for item in tree.get_children():
            tree.delete(item)

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, name, phone, email FROM customers ORDER BY id DESC"
            )
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        for row in rows:
            tree.insert("", tk.END, values=row)

    def add_customer():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()

        if not name:
            messagebox.showwarning("Missing Information", "Customer name is required.")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)",
                (name, phone, email)
            )
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        load_customers()
        messagebox.showinfo("Success", "Customer added successfully.")

    add_btn = make_button(form_card, "Add Customer", add_customer, primary=True, width=18)
    add_btn.grid(row=1, column=3, padx=(6, 20), pady=(0, 16))

    load_customers()
