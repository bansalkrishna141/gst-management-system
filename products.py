import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

def open_products():
    window = tk.Toplevel()
    window.title("Product Management")
    window.geometry("700x500")

    tk.Label(
        window,
        text="Product Management",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    form = tk.Frame(window)
    form.pack(pady=10)

    tk.Label(form, text="Product Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(form, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form, text="Price").grid(row=1, column=0, padx=10, pady=5)
    price_entry = tk.Entry(form, width=30)
    price_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form, text="GST Rate (%)").grid(row=2, column=0, padx=10, pady=5)
    gst_entry = tk.Entry(form, width=30)
    gst_entry.grid(row=2, column=1, padx=10, pady=5)

    columns = ("ID", "Product", "Price", "GST")
    tree = ttk.Treeview(window, columns=columns, show="headings", height=12)

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=150)

    tree.pack(pady=20)

    def load_products():
        for item in tree.get_children():
            tree.delete(item)

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, price, gst_rate FROM products ORDER BY id DESC"
        )

        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        cursor.close()
        connection.close()

    def add_product():
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        gst = gst_entry.get().strip()

        if not name or not price or not gst:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        try:
            price_value = float(price)
            gst_value = float(gst)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Price and GST must be numeric."
            )
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO products (name, price, gst_rate) VALUES (%s, %s, %s)",
            (name, price_value, gst_value)
        )

        connection.commit()
        cursor.close()
        connection.close()

        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        gst_entry.delete(0, tk.END)

        load_products()
        messagebox.showinfo("Success", "Product added successfully.")

    tk.Button(
        form,
        text="Add Product",
        width=20,
        command=add_product
    ).grid(row=3, column=0, columnspan=2, pady=15)

    load_products()
