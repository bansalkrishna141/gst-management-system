import tkinter as tk
from tkinter import ttk
from theme import BG, CARD, TEXT, MUTED, PRIMARY, BORDER, INPUT_BG

def configure_ttk():
    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "TCombobox",
        fieldbackground=INPUT_BG,
        background=INPUT_BG,
        foreground=TEXT,
        bordercolor=BORDER,
        arrowsize=14
    )

    style.map(
        "TCombobox",
        fieldbackground=[("readonly", INPUT_BG)],
        foreground=[("readonly", TEXT)]
    )

    style.configure(
        "Treeview",
        background=CARD,
        fieldbackground=CARD,
        foreground=TEXT,
        rowheight=28,
        bordercolor=BORDER,
        borderwidth=1
    )

    style.configure(
        "Treeview.Heading",
        background="#E5E7EB",
        foreground=TEXT,
        relief="flat",
        font=("Helvetica", 11, "bold")
    )

    style.map(
        "Treeview",
        background=[("selected", "#DBEAFE")],
        foreground=[("selected", TEXT)]
    )

def make_title(parent, text, size=24):
    return tk.Label(
        parent,
        text=text,
        bg=BG,
        fg=TEXT,
        font=("Helvetica", size, "bold")
    )

def make_subtitle(parent, text):
    return tk.Label(
        parent,
        text=text,
        bg=BG,
        fg=MUTED,
        font=("Helvetica", 11)
    )

def make_card(parent, **kwargs):
    return tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1,
        bd=0,
        **kwargs
    )

def make_label(parent, text):
    return tk.Label(
        parent,
        text=text,
        bg=CARD,
        fg=TEXT,
        font=("Helvetica", 11)
    )

def make_entry(parent, width=32, show=None):
    return tk.Entry(
        parent,
        width=width,
        show=show,
        bg=INPUT_BG,
        fg=TEXT,
        insertbackground=TEXT,
        relief="solid",
        bd=1,
        highlightthickness=0,
        font=("Helvetica", 11)
    )

def make_button(parent, text, command, primary=False, width=18):
    bg = PRIMARY if primary else "#E5E7EB"
    fg = "white" if primary else TEXT

    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        relief="flat",
        bd=0,
        padx=10,
        pady=10,
        cursor="hand2",
        font=("Helvetica", 11, "bold")
    )
