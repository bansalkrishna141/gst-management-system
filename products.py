import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from theme import BG
from ui_helpers import make_title, make_subtitle, make_card, make_label, make_entry, make_button

def open_products(root):
    window = tk.Toplevel(root)
    window.title("Product Management")
    window.geometry("820x620")
    window.configure(bg=BG)

    make_title(window, "Product Management", 22).pack(anchor="w", padx=28, pady=(24, 2))
    make_subtitle(window, "Create products and configure GST rates.").pack(anchor="w", padx=28)

    form_card = make_card(window)
    form_card.pack(fill="x", padx=28, pady=20)

    make_label(form_card, "Product Name").grid(row=0, column=0, sticky="w", padx=20, pady=(18, 5))
    make_label(form_card, "Price").grid(row=0, column=1, sticky="w", padx=20, pady=(18, 5))
    make_label(form_card, "GST Rate (%)").grid(row=0, column=2, sticky="w", padx=20, pady=(18, 5))

    name_entry = make_entry(form_card, 24)
    price_entry = make_entry(form_card, 16)
    gst_entry = make_entry(form_card, 16)

    name_entry.grid(row=1, column=0, padx=20, pady=(0, 16), ipady=6)
    price_entry.grid(row=1, column=1, padx=20, pady=(0, 16), ipady=6)
    gst_entry.grid(row=1, column=2, padx=20, pady=(0, 16), ipady=6)

    table_card = make_card(window)
    table_card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

    columns = ("ID", "Product", "Price", "GST %")
    tree = ttk.Treeview(table_card, columns=columns, show="headings", height=14)

    widths = {"ID": 80, "Product": 300, "Price": 180, "GST %": 160}
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=widths[column], anchor="w")

    tree.pack(fill="both", expand=True, padx=14, pady=14)

    def load_products():
        for item in tree.get_children():
            tree.delete(item)

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, name, price, gst_rate FROM products ORDER BY id DESC"
            )
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        for product_id, name, price, gst_rate in rows:
            tree.insert(
                "",
                tk.END,
                values=(product_id, name, f"₹{float(price):.2f}", f"{float(gst_rate):.2f}%")
            )

    def add_product():
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        gst = gst_entry.get().strip()

        if not name or not price or not gst:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return

        try:
            price_value = float(price)
            gst_value = float(gst)
            if price_value < 0 or gst_value < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Price and GST must be valid non-negative numbers.")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO products (name, price, gst_rate) VALUES (%s, %s, %s)",
                (name, price_value, gst_value)
            )
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        gst_entry.delete(0, tk.END)
        load_products()
        messagebox.showinfo("Success", "Product added successfully.")

    add_btn = make_button(form_card, "Add Product", add_product, primary=True, width=18)
    add_btn.grid(row=1, column=3, padx=(6, 20), pady=(0, 16))

    load_products()
