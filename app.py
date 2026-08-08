import tkinter as tk

from login import show_login
from customers import open_customers
from products import open_products
from invoices import open_invoices

root = tk.Tk()
root.title("GST Management System")
root.geometry("700x500")
root.withdraw()

def show_dashboard():
    root.deiconify()

    title = tk.Label(
        root,
        text="GST Management System",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=40)

    subtitle = tk.Label(
        root,
        text="Business Billing & GST Management",
        font=("Arial", 12)
    )
    subtitle.pack(pady=5)

    frame = tk.Frame(root)
    frame.pack(pady=40)

    tk.Button(
        frame,
        text="Manage Customers",
        width=22,
        height=2,
        command=open_customers
    ).grid(row=0, column=0, padx=15, pady=15)

    tk.Button(
        frame,
        text="Manage Products",
        width=22,
        height=2,
        command=open_products
    ).grid(row=0, column=1, padx=15, pady=15)

    tk.Button(
        frame,
        text="Create Invoice",
        width=22,
        height=2,
        command=open_invoices
    ).grid(row=1, column=0, padx=15, pady=15)

    tk.Button(
        frame,
        text="Exit",
        width=22,
        height=2,
        command=root.destroy
    ).grid(row=1, column=1, padx=15, pady=15)

show_login(root, show_dashboard)
root.mainloop()
