# GST Management System V3

A desktop GST billing and invoice management application built with Python, Tkinter, and MySQL.

This repository is a reconstructed and improved version of an earlier GST management prototype. Version 2 focuses on clearer code structure, a Mac dark-mode-safe interface, improved database error handling, and invoice history.

## Features

- Login authentication
- Customer management
- Product management
- Configurable GST rates
- Automatic GST calculation
- Multi-item invoice creation
- MySQL invoice storage
- Invoice history and customer search
- Dark-mode-safe custom Tkinter colors
- Database connection status on dashboard

## Tech Stack

- Python
- Tkinter
- MySQL
- mysql-connector-python

## Project Structure

```text
gst-management-system-v3/
├── app.py
├── customers.py
├── database.py
├── invoices.py
├── login.py
├── products.py
├── pdf_invoice.py
├── theme.py
├── ui_helpers.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup on macOS

### 1. Install dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Start MySQL

If installed with Homebrew:

```bash
brew services start mysql
```

### 3. Create the database

From inside this project folder:

```bash
mysql -u root < schema.sql
```

If your MySQL root user requires a password:

```bash
mysql -u root -p < schema.sql
```

### 4. Configure database credentials

The app reads these optional environment variables:

```text
GST_DB_HOST
GST_DB_USER
GST_DB_PASSWORD
GST_DB_NAME
```

For a Homebrew MySQL setup with a root user and no password, no changes are required.

If you have a password, run this before starting the app:

```bash
export GST_DB_PASSWORD="your-password"
```

Do not commit your actual password to GitHub.

### 5. Run the app

```bash
python3 app.py
```

## Default Demo Login

```text
Username: admin
Password: admin123
```

These credentials are only for local demonstration.

## Future Improvements

- Password hashing
- PDF invoice generation ✅
- Invoice detail view
- Delete/edit customers and products
- Inventory management
- CSV/Excel export
- Dashboard analytics
- Automated tests

## Background

This project is a modern reimplementation of an earlier academic/personal GST management prototype. The current codebase was rebuilt with a cleaner architecture and a more polished desktop interface.

## Author

Krishna Bansal


## PDF Invoices

After an invoice is saved, the application automatically creates a PDF in:

```text
generated_invoices/
```

Generated PDFs are excluded from Git commits through `.gitignore`.
