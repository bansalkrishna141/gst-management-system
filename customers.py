import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

def open_customers():
    window = tk.Toplevel()
    window.title("Customer Management")
    window.geometry("700x500")

    tk.Label(
        window,
        text="Customer Management",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    form = tk.Frame(window)
    form.pack(pady=10)

    tk.Label(form, text="Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(form, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form, text="Phone").grid(row=1, column=0, padx=10, pady=5)
    phone_entry = tk.Entry(form, width=30)
    phone_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form, text="Email").grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(form, width=30)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    columns = ("ID", "Name", "Phone", "Email")
    tree = ttk.Treeview(window, columns=columns, show="headings", height=12)

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=150)

    tree.pack(pady=20)

    def load_customers():
        for item in tree.get_children():
            tree.delete(item)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id, name, phone, email FROM customers ORDER BY id DESC"
        )

        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        cursor.close()
        connection.close()

    def add_customer():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Missing Information",
                "Customer name is required."
            )
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)",
            (name, phone, email)
        )

        connection.commit()
        cursor.close()
        connection.close()

        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

        load_customers()
        messagebox.showinfo("Success", "Customer added successfully.")

    tk.Button(
        form,
        text="Add Customer",
        width=20,
        command=add_customer
    ).grid(row=3, column=0, columnspan=2, pady=15)

    load_customers()
