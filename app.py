import tkinter as tk
from tkinter import messagebox

from database import test_connection
from login import show_login
from customers import open_customers
from products import open_products
from invoices import open_invoices, open_invoice_history
from theme import BG, CARD, TEXT, MUTED, PRIMARY, BORDER
from ui_helpers import configure_ttk, make_title, make_subtitle, make_card, make_button

root = tk.Tk()
root.title("GST Management System")
root.geometry("860x560")
root.configure(bg=BG)
root.minsize(820, 520)
# root.withdraw()

configure_ttk()

def show_dashboard():
    root.deiconify()

    for widget in root.winfo_children():
        widget.destroy()

    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=34, pady=(30, 10))

    make_title(header, "GST Management System", 26).pack(anchor="w")
    make_subtitle(
        header,
        "Business billing, customer records, products, and GST invoices."
    ).pack(anchor="w", pady=(4, 0))

    db_ok, db_message = test_connection()

    status_text = "MySQL connected" if db_ok else "MySQL connection issue"
    status_color = "#15803D" if db_ok else "#B91C1C"

    tk.Label(
        header,
        text=f"● {status_text}",
        bg=BG,
        fg=status_color,
        font=("Helvetica", 10, "bold")
    ).pack(anchor="w", pady=(12, 0))

    content = tk.Frame(root, bg=BG)
    content.pack(fill="both", expand=True, padx=34, pady=14)

    cards = [
        (
            "Customers",
            "Add and review customer records.",
            lambda: open_customers(root)
        ),
        (
            "Products",
            "Manage products, prices, and GST rates.",
            lambda: open_products(root)
        ),
        (
            "Create Invoice",
            "Build invoices with automatic GST calculation.",
            lambda: open_invoices(root)
        ),
        (
            "Invoice History",
            "Search and review previously saved invoices.",
            lambda: open_invoice_history(root)
        )
    ]

    for index, (title, description, command) in enumerate(cards):
        row = index // 2
        col = index % 2

        card = make_card(content)
        card.grid(
            row=row,
            column=col,
            sticky="nsew",
            padx=10,
            pady=10,
            ipadx=18,
            ipady=18
        )

        tk.Label(
            card,
            text=title,
            bg=CARD,
            fg=TEXT,
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 6))

        tk.Label(
            card,
            text=description,
            bg=CARD,
            fg=MUTED,
            justify="left",
            wraplength=290,
            font=("Helvetica", 11)
        ).pack(anchor="w", padx=20, pady=(0, 18))

        make_button(
            card,
            f"Open {title}",
            command,
            primary=True,
            width=18
        ).pack(anchor="w", padx=20, pady=(0, 18))

    content.grid_columnconfigure(0, weight=1)
    content.grid_columnconfigure(1, weight=1)
    content.grid_rowconfigure(0, weight=1)
    content.grid_rowconfigure(1, weight=1)

    footer = tk.Frame(root, bg=BG)
    footer.pack(fill="x", padx=34, pady=(0, 22))

    make_button(
        footer,
        "Exit",
        root.destroy,
        width=12
    ).pack(side="right")

    if not db_ok:
        messagebox.showwarning(
            "Database Connection",
            "The app opened, but MySQL could not be reached.\n\n"
            f"{db_message}\n\n"
            "Make sure MySQL is running and your environment settings are correct."
        )

show_login(root, show_dashboard)

root.mainloop()
