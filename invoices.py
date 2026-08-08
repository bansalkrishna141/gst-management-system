import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

def open_invoices():
    window = tk.Toplevel()
    window.title("Create Invoice")
    window.geometry("900x650")

    tk.Label(
        window,
        text="Create GST Invoice",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    customer_var = tk.StringVar()
    product_var = tk.StringVar()
    quantity_var = tk.StringVar(value="1")

    customer_map = {}
    product_map = {}

    form = tk.Frame(window)
    form.pack(pady=10)

    tk.Label(form, text="Customer").grid(row=0, column=0, padx=10, pady=5)
    customer_combo = ttk.Combobox(
        form, textvariable=customer_var, width=30, state="readonly"
    )
    customer_combo.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form, text="Product").grid(row=1, column=0, padx=10, pady=5)
    product_combo = ttk.Combobox(
        form, textvariable=product_var, width=30, state="readonly"
    )
    product_combo.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form, text="Quantity").grid(row=2, column=0, padx=10, pady=5)
    quantity_entry = tk.Entry(form, textvariable=quantity_var, width=32)
    quantity_entry.grid(row=2, column=1, padx=10, pady=5)

    columns = ("Product", "Quantity", "Price", "GST %", "GST Amount", "Total")
    tree = ttk.Treeview(window, columns=columns, show="headings", height=12)

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=130)

    tree.pack(pady=20)

    items = []

    subtotal_label = tk.Label(window, text="Subtotal: ₹0.00", font=("Arial", 12))
    subtotal_label.pack()

    gst_label = tk.Label(window, text="GST: ₹0.00", font=("Arial", 12))
    gst_label.pack()

    total_label = tk.Label(
        window, text="Total: ₹0.00", font=("Arial", 14, "bold")
    )
    total_label.pack(pady=5)

    def load_data():
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name FROM customers")
        customers = cursor.fetchall()

        customer_map.clear()
        customer_names = []

        for customer_id, name in customers:
            customer_map[name] = customer_id
            customer_names.append(name)

        customer_combo["values"] = customer_names

        cursor.execute("SELECT id, name, price, gst_rate FROM products")
        products = cursor.fetchall()

        product_map.clear()
        product_names = []

        for product_id, name, price, gst_rate in products:
            product_map[name] = {
                "id": product_id,
                "price": float(price),
                "gst": float(gst_rate)
            }
            product_names.append(name)

        product_combo["values"] = product_names

        cursor.close()
        connection.close()

    def update_totals():
        subtotal = sum(item["subtotal"] for item in items)
        gst_total = sum(item["gst_amount"] for item in items)
        grand_total = subtotal + gst_total

        subtotal_label.config(text=f"Subtotal: ₹{subtotal:.2f}")
        gst_label.config(text=f"GST: ₹{gst_total:.2f}")
        total_label.config(text=f"Total: ₹{grand_total:.2f}")

    def add_item():
        product_name = product_var.get()

        if not product_name:
            messagebox.showwarning("Select Product", "Please select a product.")
            return

        try:
            quantity = int(quantity_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a positive integer."
            )
            return

        product = product_map[product_name]
        price = product["price"]
        gst_rate = product["gst"]

        subtotal = price * quantity
        gst_amount = subtotal * gst_rate / 100
        total = subtotal + gst_amount

        item = {
            "product_id": product["id"],
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "gst_rate": gst_rate,
            "subtotal": subtotal,
            "gst_amount": gst_amount,
            "total": total
        }

        items.append(item)

        tree.insert(
            "",
            tk.END,
            values=(
                product_name,
                quantity,
                f"₹{price:.2f}",
                f"{gst_rate:.2f}",
                f"₹{gst_amount:.2f}",
                f"₹{total:.2f}"
            )
        )

        update_totals()

    def save_invoice():
        customer_name = customer_var.get()

        if not customer_name:
            messagebox.showwarning(
                "Select Customer",
                "Please select a customer."
            )
            return

        if not items:
            messagebox.showwarning(
                "No Items",
                "Please add at least one product."
            )
            return

        customer_id = customer_map[customer_name]

        subtotal = sum(item["subtotal"] for item in items)
        gst_total = sum(item["gst_amount"] for item in items)
        grand_total = subtotal + gst_total

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO invoices
            (customer_id, subtotal, gst_amount, total_amount)
            VALUES (%s, %s, %s, %s)
            """,
            (customer_id, subtotal, gst_total, grand_total)
        )

        invoice_id = cursor.lastrowid

        for item in items:
            cursor.execute(
                """
                INSERT INTO invoice_items
                (invoice_id, product_id, quantity, unit_price, gst_rate, line_total)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    invoice_id,
                    item["product_id"],
                    item["quantity"],
                    item["price"],
                    item["gst_rate"],
                    item["total"]
                )
            )

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Invoice Saved",
            f"Invoice #{invoice_id} saved successfully."
        )

        window.destroy()

    tk.Button(
        form,
        text="Add Item",
        width=20,
        command=add_item
    ).grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(
        window,
        text="Save Invoice",
        width=25,
        height=2,
        command=save_invoice
    ).pack(pady=20)

    load_data()
