# GST Management System

A desktop-based GST billing and invoice management application developed using Python, Tkinter, and MySQL.

This project is a modern reimplementation of an earlier GST management prototype originally developed as an academic/personal project. The application was rebuilt to improve code organization, database design, and usability.

## Features

- User authentication
- Customer management
- Product management
- GST percentage configuration
- Automatic GST calculation
- Multi-product invoice creation
- Invoice storage using MySQL
- Invoice item tracking
- Desktop graphical interface using Tkinter

## Tech Stack

- Python
- Tkinter
- MySQL
- mysql-connector-python

## Project Structure

```text
gst-management-system/
├── app.py
├── database.py
├── login.py
├── customers.py
├── products.py
├── invoices.py
├── schema.sql
├── requirements.txt
├── .gitignore
└── README.md
```

## Database Design

The application uses the following tables:

- users
- customers
- products
- invoices
- invoice_items

Each invoice is linked to a customer and can contain multiple products.

## GST Calculation

GST Amount = Price × Quantity × GST Rate / 100

Final Amount = Subtotal + GST Amount

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run `schema.sql` in MySQL.

3. Update your MySQL credentials in `database.py`.

4. Start the application:

```bash
python app.py
```

## Default Login

```text
Username: admin
Password: admin123
```

The default credentials are intended only for demonstration purposes.

## Future Improvements

- Password hashing
- PDF invoice generation
- Invoice search and filtering
- Dashboard analytics
- Inventory management
- Excel export
- Improved UI design

## Author

Krishna Bansal
