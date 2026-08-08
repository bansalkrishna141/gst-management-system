import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from theme import BG, CARD, TEXT, MUTED, BORDER
from ui_helpers import make_title, make_subtitle, make_card, make_label, make_entry, make_button

def open_invoices(root):
    window = tk.Toplevel(root)
    window.title("Create Invoice")
    window.geometry("1000x720")
    window.configure(bg=BG)

    make_title(window, "Create GST Invoice", 22).pack(anchor="w", padx=28, pady=(24, 2))
    make_subtitle(window, "Build a multi-item invoice with automatic GST calculation.").pack(anchor="w", padx=28)

    form_card = make_card(window)
    form_card.pack(fill="x", padx=28, pady=18)

    customer_var = tk.StringVar()
    product_var = tk.StringVar()
    quantity_var = tk.StringVar(value="1")

    customer_map = {}
    product_map = {}
    items = []

    make_label(form_card, "Customer").grid(row=0, column=0, sticky="w", padx=20, pady=(18, 5))
    make_label(form_card, "Product").grid(row=0, column=1, sticky="w", padx=20, pady=(18, 5))
    make_label(form_card, "Quantity").grid(row=0, column=2, sticky="w", padx=20, pady=(18, 5))

    customer_combo = ttk.Combobox(form_card, textvariable=customer_var, width=28, state="readonly")
    product_combo = ttk.Combobox(form_card, textvariable=product_var, width=28, state="readonly")
    quantity_entry = make_entry(form_card, 12)

    customer_combo.grid(row=1, column=0, padx=20, pady=(0, 16), ipady=4)
    product_combo.grid(row=1, column=1, padx=20, pady=(0, 16), ipady=4)
    quantity_entry.grid(row=1, column=2, padx=20, pady=(0, 16), ipady=6)

    table_card = make_card(window)
    table_card.pack(fill="both", expand=True, padx=28, pady=(0, 12))

    columns = ("Product", "Qty", "Unit Price", "GST %", "GST Amount", "Line Total")
    tree = ttk.Treeview(table_card, columns=columns, show="headings", height=12)

    widths = {
        "Product": 260,
        "Qty": 70,
        "Unit Price": 140,
        "GST %": 110,
        "GST Amount": 140,
        "Line Total": 150
    }

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=widths[column], anchor="w")

    tree.pack(fill="both", expand=True, padx=14, pady=14)

    summary = tk.Frame(window, bg=BG)
    summary.pack(fill="x", padx=28, pady=(0, 20))

    subtotal_label = tk.Label(summary, text="Subtotal: ₹0.00", bg=BG, fg=TEXT, font=("Helvetica", 12))
    gst_label = tk.Label(summary, text="GST: ₹0.00", bg=BG, fg=TEXT, font=("Helvetica", 12))
    total_label = tk.Label(summary, text="Total: ₹0.00", bg=BG, fg=TEXT, font=("Helvetica", 15, "bold"))

    subtotal_label.pack(side="left", padx=(0, 24))
    gst_label.pack(side="left", padx=(0, 24))
    total_label.pack(side="left")

    def load_data():
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT id, name FROM customers ORDER BY name")
            customers = cursor.fetchall()

            customer_map.clear()
            customer_names = []
            for customer_id, name in customers:
                customer_map[name] = customer_id
                customer_names.append(name)
            customer_combo["values"] = customer_names

            cursor.execute("SELECT id, name, price, gst_rate FROM products ORDER BY name")
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
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))

    def update_totals():
        subtotal = sum(item["subtotal"] for item in items)
        gst_total = sum(item["gst_amount"] for item in items)
        total = subtotal + gst_total

        subtotal_label.config(text=f"Subtotal: ₹{subtotal:.2f}")
        gst_label.config(text=f"GST: ₹{gst_total:.2f}")
        total_label.config(text=f"Total: ₹{total:.2f}")

    def add_item():
        product_name = product_var.get().strip()

        if not product_name:
            messagebox.showwarning("Select Product", "Please select a product.")
            return

        try:
            quantity = int(quantity_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Quantity must be a positive integer.")
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
                f"{gst_rate:.2f}%",
                f"₹{gst_amount:.2f}",
                f"₹{total:.2f}"
            )
        )

        update_totals()

    def save_invoice():
        customer_name = customer_var.get().strip()

        if not customer_name:
            messagebox.showwarning("Select Customer", "Please select a customer.")
            return

        if not items:
            messagebox.showwarning("No Items", "Add at least one item to the invoice.")
            return

        customer_id = customer_map[customer_name]
        subtotal = sum(item["subtotal"] for item in items)
        gst_total = sum(item["gst_amount"] for item in items)
        grand_total = subtotal + gst_total

        try:
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

        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        messagebox.showinfo("Invoice Saved", f"Invoice #{invoice_id} saved successfully.")
        window.destroy()

    add_btn = make_button(form_card, "Add Item", add_item, primary=True, width=16)
    add_btn.grid(row=1, column=3, padx=(6, 20), pady=(0, 16))

    save_btn = make_button(summary, "Save Invoice", save_invoice, primary=True, width=18)
    save_btn.pack(side="right")

    load_data()

def open_invoice_history(root):
    window = tk.Toplevel(root)
    window.title("Invoice History")
    window.geometry("980x620")
    window.configure(bg=BG)

    make_title(window, "Invoice History", 22).pack(anchor="w", padx=28, pady=(24, 2))
    make_subtitle(window, "Review saved invoices and totals.").pack(anchor="w", padx=28)

    search_card = make_card(window)
    search_card.pack(fill="x", padx=28, pady=18)

    make_label(search_card, "Search by customer name").pack(side="left", padx=(20, 10), pady=16)

    search_entry = make_entry(search_card, 28)
    search_entry.pack(side="left", padx=(0, 12), pady=16, ipady=6)

    table_card = make_card(window)
    table_card.pack(fill="both", expand=True, padx=28, pady=(0, 24))

    columns = ("Invoice ID", "Customer", "Subtotal", "GST", "Total", "Created")
    tree = ttk.Treeview(table_card, columns=columns, show="headings", height=15)

    widths = {
        "Invoice ID": 100,
        "Customer": 220,
        "Subtotal": 130,
        "GST": 120,
        "Total": 130,
        "Created": 180
    }

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=widths[column], anchor="w")

    tree.pack(fill="both", expand=True, padx=14, pady=14)

    def load_history():
        keyword = search_entry.get().strip()

        sql = """
            SELECT i.id, c.name, i.subtotal, i.gst_amount, i.total_amount, i.created_at
            FROM invoices i
            JOIN customers c ON c.id = i.customer_id
        """
        params = ()

        if keyword:
            sql += " WHERE c.name LIKE %s"
            params = (f"%{keyword}%",)

        sql += " ORDER BY i.id DESC"

        for item in tree.get_children():
            tree.delete(item)

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as exc:
            messagebox.showerror("Database Error", str(exc))
            return

        for invoice_id, customer, subtotal, gst, total, created in rows:
            tree.insert(
                "",
                tk.END,
                values=(
                    invoice_id,
                    customer,
                    f"₹{float(subtotal):.2f}",
                    f"₹{float(gst):.2f}",
                    f"₹{float(total):.2f}",
                    created.strftime("%Y-%m-%d %H:%M")
                )
            )

    search_btn = make_button(search_card, "Search", load_history, primary=True, width=12)
    search_btn.pack(side="left", padx=(0, 8), pady=16)

    clear_btn = make_button(
        search_card,
        "Clear",
        lambda: (search_entry.delete(0, tk.END), load_history()),
        width=10
    )
    clear_btn.pack(side="left", pady=16)

    load_history()
