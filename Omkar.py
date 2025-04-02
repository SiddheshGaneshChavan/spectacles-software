
import tkinter as tk
from tkinter import Entry, Label, Button, Frame, messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
import bcrypt
from tkcalendar import DateEntry
import datetime
import os,sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Get the current date in YYYY-MM-DD format
current_date = datetime.datetime.today().strftime('%Y-%m-%d')


DB_NAME = "users.db"
# Function to get correct file paths (for PyInstaller compatibility)

def fetch_data():
    """Fetch data from Stocks table and display in Treeview."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Stocks")
    rows = cursor.fetchall()
    conn.close()

    global tree  # Ensure tree is accessible
    if 'tree'in globals():
        for item in tree.get_children():
            tree.delete(item)

        for row in rows:
            tree.insert("", "end", values=row)

    if 'tree2' in globals():
        for item in tree2.get_children():
            tree2.delete(item)

        for row in rows:
            tree2.insert("", "end", values=row)


def add_stock():
    global entry_frame_add, entry_type_add, entry_count_add, entry_date_add
    
    frame = entry_frame_add.get()
    type_ = entry_type_add.get()
    count = entry_count_add.get()
    date = entry_date_add.get()

    if not (frame and type_ and count.isdigit() and date):
        messagebox.showerror("Input Error", "Please enter valid values.")
        return
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Stocks (Frame, Type, Count, Date) VALUES (?, ?, ?, ?)",
                       (frame, type_, int(count), date))
        conn.commit()
        conn.close()
        fetch_data()
        messagebox.showinfo("Success", "Stock added successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Frame & Type combination already exists!")

def update_stock():
    """Update the selected stock record in the database."""
    selected_item = tree2.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a record to update.")
        return

    frame = entry_frame_update.get()
    type_ = entry_type_update.get()
    count = entry_count_update.get()
    date = entry_date_update.get()

    if not (frame and type_ and count.isdigit() and date):
        messagebox.showerror("Input Error", "Please enter valid values.")
        return

    item_values = tree.item(selected_item)["values"]
    stock_id = item_values[0]  # Get the "No" column (Primary Key)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE Stocks SET Frame=?, Type=?, Count=?, Date=? WHERE No=?",
                   (frame, type_, int(count), date, stock_id))
    conn.commit()
    conn.close()
    fetch_data()
    messagebox.showinfo("Success", "Stock updated successfully.")

def on_row_selected(event):
    """Populate input fields when a row is selected."""
    selected_item = tree2.selection()
    if not selected_item:
        return

    item_values = tree2.item(selected_item)["values"]
    entry_frame_update.delete(0, tk.END)
    entry_frame_update.insert(0, item_values[1])

    entry_type_update.delete(0, tk.END)
    entry_type_update.insert(0, item_values[2])

    entry_count_update.delete(0, tk.END)
    entry_count_update.insert(0, item_values[3])


def open_admin():
    global entry_frame_add, entry_type_add, entry_count_add, entry_date_add
    global entry_frame_update, entry_type_update, entry_count_update, entry_date_update, tree ,tree2
    
    root = tk.Tk()
    root.title("Stock Management")
    root.geometry("750x450")
    root.configure(bg='#f0f0f0')
    
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TEntry", font=("Arial", 12))
    
    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, fill='both', expand=True)

    frame_add = ttk.Frame(notebook, padding=10)
    notebook.add(frame_add, text="Add Stock")

    ttk.Label(frame_add, text="Frame:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_frame_add = ttk.Entry(frame_add, width=30)
    entry_frame_add.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_add, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_type_add = ttk.Entry(frame_add, width=30)
    entry_type_add.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_add, text="Count:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    entry_count_add = ttk.Entry(frame_add, width=30)
    entry_count_add.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_add, text="Date:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
    entry_date_add = ttk.Entry(frame_add, width=30)
    entry_date_add.insert(0,current_date)
    entry_date_add.config(state="readonly")
    entry_date_add.grid(row=3, column=1, padx=5, pady=5)

    btn_add = ttk.Button(frame_add, text="Add Stock", command=add_stock)
    btn_add.grid(row=4, column=0, columnspan=2, pady=10)

    columns = ("No","Frame", "Type", "Count", "Date")
    tree = ttk.Treeview(frame_add, columns=columns, show="headings", height=5)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    scrollbar = ttk.Scrollbar(frame_add, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)

    tree.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
    scrollbar.grid(row=5, column=2, sticky="ns")
    frame_add.grid_columnconfigure(1, weight=1)
    frame_add.grid_rowconfigure(5, weight=1)

    frame_update = ttk.Frame(notebook, padding=10)
    notebook.add(frame_update, text="Update Stock")

    ttk.Label(frame_update, text="Frame:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_frame_update = ttk.Entry(frame_update, width=30)
    entry_frame_update.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_update, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_type_update = ttk.Entry(frame_update, width=30)
    entry_type_update.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_update, text="Count:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    entry_count_update = ttk.Entry(frame_update, width=30)
    entry_count_update.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_update, text="Date:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
    entry_date_update = ttk.Entry(frame_update, width=30)
    entry_date_update.insert(0,current_date)
    entry_date_update.config(state="readonly")
    entry_date_update.grid(row=3, column=1, padx=5, pady=5)

    btn_update = ttk.Button(frame_update, text="Update Stock", command=update_stock)
    btn_update.grid(row=4, column=0, columnspan=2, pady=10)

    tree2 = ttk.Treeview(frame_update, columns=columns, show="headings", height=5)

    for col in columns:
        tree2.heading(col, text=col)
        tree2.column(col, width=100)

    scrollbar = ttk.Scrollbar(frame_update, orient="vertical", command=tree.yview)
    tree2.configure(yscroll=scrollbar.set)
    tree2.bind("<<TreeviewSelect>>", on_row_selected)
    tree2.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
    scrollbar.grid(row=5, column=2, sticky="ns")
    frame_update.grid_columnconfigure(1, weight=1)
    frame_update.grid_rowconfigure(5, weight=1)

    fetch_data()
    root.mainloop()

def login_user():
    """Handles user login by validating credentials."""
    username = usrname_entry.get().strip()
    password = passwd_entry.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty")
        return

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, type FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        messagebox.showinfo("Success", "Login successful")
        main.destroy()  # Close login window
        
        if user[1] == "admin":
            open_admin()  # Redirect admin users
        else:
            open_dashboard()  # Redirect normal users
    else:
        messagebox.showerror("Error", "Invalid username or password")

def open_dashboard():
    """Opens the main dashboard after successful login."""
    dashboard = tk.Tk()
    dashboard.title("Dashboard")
    dashboard.geometry("900x450")
    dashboard.configure(bg="white")

    # Tabs for Customer Details
    notebook = ttk.Notebook(dashboard)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    tab1 = tk.Frame(notebook)
    tab2 = tk.Frame(notebook)
    tab3 = tk.Frame(notebook)
    notebook.add(tab1, text="Customer Details")
    notebook.add(tab2, text="Update Bill Details")
    notebook.add(tab3, text="Details of Spectacles")

    def get_options(column, frame=None):
        """Fetch distinct values from Stocks table. Optionally filter Type by Frame."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        if frame:
            cursor.execute("SELECT DISTINCT Type FROM Stocks WHERE Frame = ? AND Count > 0", (frame,))
        else:
            cursor.execute(f"SELECT DISTINCT {column} FROM Stocks WHERE Count > 0")
        options = [row[0] for row in cursor.fetchall()]
        conn.close()
        return options

    def update_type_options(event):
        """Update Type dropdown based on selected Frame."""
        selected_frame = frame_combobox.get()
        type_options = get_options("Type", selected_frame)
        type_combobox["values"] = type_options if type_options else ["No Types Available"]
        type_combobox.current(0)  # Set default selection

    frame_options = get_options("Frame")

    # Customer Details Section
    tk.Label(tab1, text="Bill no", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    transaction = tk.Entry(tab1, font=("Arial", 12), width=30)
    transaction.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(tab1, text="Date of Order:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    date_entry = tk.Entry(tab1, font=("Arial", 12), width=30)
    date_entry.insert(0, current_date)
    date_entry.config(state="readonly")
    date_entry.grid(row=1, column=1, padx=10, pady=5)

    
    def validate_phone(P):
        """Validate phone number input (only digits, max length 10)."""
        if P.isdigit() and len(P) <= 10:
            return True
        elif P == "":  # Allow backspace
            return True
        else:
            return False
        
    vcmd = dashboard.register(validate_phone)

    tk.Label(tab1, text="Phone No:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    phone_entry = tk.Entry(tab1, font=("Arial", 12), width=30, validate="key", validatecommand=(vcmd, "%P"))
    phone_entry.grid(row=2, column=1, padx=10, pady=5)      
    
    tk.Label(tab1, text="Name:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(tab1, font=("Arial", 12), width=30)
    name_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(tab1, text="DOB:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    dob_entry = DateEntry(tab1, font=("Arial", 12), width=28, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
    dob_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(tab1, text="Frame:", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
    frame_combobox = ttk.Combobox(tab1, values=frame_options, font=("Arial", 12), width=28)
    frame_combobox.grid(row=5, column=1, padx=10, pady=5)
    frame_combobox.set("Select Frame")
    frame_combobox.bind("<<ComboboxSelected>>", update_type_options)

    def refresh_data():
        """Refresh frame and type options from the database."""
        frame_options = get_options("Frame")  # Fetch latest Frame options
        frame_combobox["values"] = frame_options if frame_options else ["No Frames Available"]
    
        selected_frame = frame_combobox.get()
        type_options = get_options("Type", selected_frame)  # Fetch latest Type options
        type_combobox["values"] = type_options if type_options else ["No Types Available"]

        frame_combobox.set("Select Frame")  # Reset selection
        type_combobox.set("Select Type")

    refresh_button = tk.Button(tab1, text="Refresh Data", font=("Arial", 12), bg="white", command=refresh_data)
    refresh_button.grid(row=5, column=2, columnspan=2, padx=10, pady=5)

    tk.Label(tab1, text="Type:", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=5, sticky="w")
    type_combobox = ttk.Combobox(tab1, values=["Select a Frame First"], font=("Arial", 12), width=28)
    type_combobox.grid(row=6, column=1, padx=10, pady=5)
    type_combobox.set("Select Type")

    tk.Label(tab1, text="Lens", font=("Arial", 12)).grid(row=7, column=0, padx=10, pady=5, sticky="w")
    Lens_entry = tk.Entry(tab1, font=("Arial", 12), width=30)
    Lens_entry.grid(row=7, column=1, padx=10, pady=5)

    table_frame = tk.Frame(tab1, bg="white")
    table_frame.grid(row=8, column=1, columnspan=3, padx=10, pady=10)

    headers = ["", "R.E", "", "", "L.E", "", ""]
    sub_headers = ["", "SPH", "CYL", "AXIS", "SPH", "CYL", "AXIS"]

    # Creating Header Labels
    for col, text in enumerate(headers):
        label = tk.Label(table_frame, text=text, font=("Arial", 12, "bold"), bg="white", padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=0, column=col, sticky="nsew")

    # Creating Sub-Headers
    for col, text in enumerate(sub_headers):
        label = tk.Label(table_frame, text=text, font=("Arial", 10, "bold"), bg="white", padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=1, column=col, sticky="nsew")

    # Labels for Distance and Reading
    row_labels = ["Distance", "Reading"]
    for row, text in enumerate(row_labels, start=2):
        label = tk.Label(table_frame, text=text, font=("Arial", 12), bg="white", padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=row, column=0, sticky="nsew")

    # Creating Entry Fields
    entries = []
    for row in range(2, 4):  # Distance & Reading rows
        row_entries = []
        for col in range(1, 7):  # Six columns for SPH, CYL, AXIS of both eyes
            entry = tk.Entry(table_frame, font=("Arial", 12), width=10)
            entry.grid(row=row, column=col, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

    # Amount Section
    def calculate_balance(*args):
        try:
            total = float(total_amt.get()) if total_amt.get() else 0
            advance = float(advance_amt.get()) if advance_amt.get() else 0
            balance = total - advance
            balance_amt.config(state="normal")
            balance_amt.delete(0, tk.END)
            balance_amt.insert(0, f"{balance:.2f}")
            balance_amt.config(state="readonly")
        except ValueError:
            balance_amt.config(state="normal")
            balance_amt.delete(0, tk.END)
            balance_amt.insert(0, "Invalid Input")
            balance_amt.config(state="readonly")

    tk.Label(tab1, text="Total Amount:", font=("Arial", 12)).grid(row=9, column=0, padx=10, pady=5, sticky="w")
    total_amt = tk.Entry(tab1, font=("Arial", 12), width=30)
    total_amt.grid(row=9, column=1, padx=10, pady=5)
    total_amt.bind("<KeyRelease>", calculate_balance)

    tk.Label(tab1, text="Advanced Amount:", font=("Arial", 12)).grid(row=10, column=0, padx=10, pady=5, sticky="w")
    advance_amt = tk.Entry(tab1, font=("Arial", 12), width=30)
    advance_amt.grid(row=10, column=1, padx=10, pady=5)
    advance_amt.bind("<KeyRelease>", calculate_balance)

    tk.Label(tab1, text="Balance Amount:", font=("Arial", 12)).grid(row=11, column=0, padx=10, pady=5, sticky="w")
    balance_amt = tk.Entry(tab1, font=("Arial", 12), width=30, state="readonly")
    balance_amt.grid(row=11, column=1, padx=10, pady=5)

    def insert_data():
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

        # Fetch data from entry fields
            name = name_entry.get()
            phone_no = phone_entry.get()
            bill_no = transaction.get()
            order_date = date_entry.get()
            dob = dob_entry.get()
            frame = frame_combobox.get()
            frame_type = type_combobox.get()
            lens = Lens_entry.get()
            total_amount = total_amt.get()
            advance_amount = advance_amt.get()
            balance_amount = balance_amt.get()
            re_sph_dist = entries[0][0].get()
            re_cyl_dist = entries[0][1].get()
            re_axis_dist = entries[0][2].get()
            le_sph_dist = entries[0][3].get()
            le_cyl_dist = entries[0][4].get()
            le_axis_dist = entries[0][5].get()

            re_sph_read = entries[1][0].get()
            re_cyl_read = entries[1][1].get()
            re_axis_read = entries[1][2].get()
            le_sph_read = entries[1][3].get()
            le_cyl_read = entries[1][4].get()
            le_axis_read = entries[1][5].get()
        # Validate required fields
            if not (name and phone_no and bill_no and frame and frame_type and total_amount):
                messagebox.showerror("Error", "All fields must be filled!")
                return

            cursor.execute("BEGIN TRANSACTION;")

        # Insert into Customers table
            cursor.execute("""INSERT INTO customers (name, phone_no, bill_no, order_date, dob, Frame, Type, total_amount, advance_amount, balance_amount, Lens) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (name, phone_no, bill_no, order_date, dob, frame, frame_type, float(total_amount), float(advance_amount), float(balance_amount), lens))
        # Get last inserted customer ID
            customer_id = cursor.lastrowid

        # Insert Distance and Reading prescriptions
            cursor.executemany("""
            INSERT INTO eye_prescriptions (
                customer_id, eye_type, re_sph, re_cyl, re_axis, le_sph, le_cyl, le_axis
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, [
            (customer_id, "Distance", re_sph_dist, re_cyl_dist, re_axis_dist, le_sph_dist, le_cyl_dist, le_axis_dist),
            (customer_id, "Reading", re_sph_read, re_cyl_read, re_axis_read, le_sph_read, le_cyl_read, le_axis_read)
        ])

        # Commit the transaction
            conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")

        except sqlite3.Error as e:
            conn.rollback()  # Rollback transaction in case of error
            messagebox.showerror("Database Error", f"Error: {e}")

        finally:
            conn.close()

    insert_button = tk.Button(tab1, text="Insert Data", font=("Arial", 12), bg="green", fg="white", command=insert_data)
    insert_button.grid(row=12, column=0, columnspan=2, padx=10, pady=5)
    # Adding ComboBox to tab2
    def fetch_bill_numbers():
        conn = sqlite3.connect(DB_NAME)  # Replace with actual database path
        cursor = conn.cursor()
        cursor.execute("SELECT bill_no FROM customers WHERE payment=?", ('Not Paid',))
        bills = [row[0] for row in cursor.fetchall()]
        conn.close()
        return bills if bills else []
    
    # Fetch balance amount based on selected bill number
    def fetch_balance_amount(event):
        selected_bill = customer_combo.get()
        if not selected_bill:
            return  # Prevent errors if nothing is selected
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT balance_amount FROM customers WHERE bill_no = ?", (selected_bill,))
        balance = cursor.fetchone()
        conn.close()
        if balance:
            balance_amt_up.config(state="normal")
            balance_amt_up.delete(0, tk.END)
            balance_amt_up.insert(0, str(balance[0]))
            balance_amt_up.config(state="readonly")
        else:
            balance_amt_up.config(state="normal")
            balance_amt_up.delete(0, tk.END)
            balance_amt_up.config(state="readonly")
    
    # Adding ComboBox to tab2
    ttk.Label(tab2, text="Select Billno:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    customer_combo = ttk.Combobox(tab2, values=fetch_bill_numbers(), font=("Arial", 12), width=28)
    customer_combo.grid(row=0, column=1, padx=10, pady=5)
    customer_combo.bind("<<ComboboxSelected>>", fetch_balance_amount)
    
    # Adding Balance Amount Entry
    ttk.Label(tab2, text="Balance Amount:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    balance_amt_up = tk.Entry(tab2, font=("Arial", 12), width=30, state="readonly")
    balance_amt_up.grid(row=1, column=1, padx=10, pady=5)
    
    def refresh_combobox2():
        customer_combo["values"] = fetch_bill_numbers()
        customer_combo.set("")
        balance_amt_up.config(state="normal")
        balance_amt_up.delete(0, tk.END)
        balance_amt_up.config(state="readonly")
    
    def update_balance():
        selected_bill = customer_combo.get()
        if not selected_bill:
            return
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT balance_amount, advance_amount FROM customers WHERE bill_no = ?", (selected_bill,))
        result = cursor.fetchone()
        
        if result:
            new_advance_amount = result[0] + result[1]  # balance_amt + advance_amt
            cursor.execute("UPDATE customers SET advance_amount = ?, balance_amount = 0 WHERE bill_no = ?", (new_advance_amount, selected_bill))
            messagebox.showinfo("Payment Update", f"Bill No {selected_bill} has been marked as Paid.")
            conn.commit()
        
        conn.close()
        customer_combo.set("") 
        balance_amt_up.config(state="normal")
        balance_amt_up.delete(0, tk.END)
        balance_amt_up.config(state="readonly")
        load_customers()  # Refresh the data
    
    refresh_button2 = ttk.Button(tab2, text="Refresh", command=refresh_combobox2)
    refresh_button2.grid(row=0, column=2, padx=10, pady=5)
    # Adding Button to tab2
    update_button = ttk.Button(tab2, text="Update Details", command=update_balance)
    update_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    
    # Adding Treeview to tab2
    tree = ttk.Treeview(tab2, columns=("Billno", "Name", "Phone_no", "Balance Amount"), show="headings")
    tree.heading("Billno", text="Billno")
    tree.heading("Name", text="Name")
    tree.heading("Phone_no", text="Phone No")
    tree.heading("Balance Amount", text="Balance Amount")
    tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    
    # Configure grid to expand properly
    tab2.grid_columnconfigure(0, weight=1)
    tab2.grid_columnconfigure(1, weight=1)
    tab2.grid_columnconfigure(2, weight=1)
    tab2.grid_rowconfigure(2, weight=1)
    
    # Function to fetch and display customers with balance > 0
    def load_customers():
        conn = sqlite3.connect(DB_NAME)  # Replace with actual database path
        cursor = conn.cursor()
        cursor.execute("SELECT bill_no, name, phone_no, balance_amount FROM customers WHERE payment=?", ('Not Paid',))
        rows = cursor.fetchall()
        
        tree.delete(*tree.get_children())  # Clear existing data
        for row in rows:
            tree.insert("", "end", values=row)
        
        conn.close()
        dashboard.after(5000, load_customers)  # Refresh data every 5 seconds
    
    load_customers()

    #tab3
    # Labels and Entries in tab3
    def search_customer():
        phone = phone_select.get().strip()
        bill = transaction_select.get().strip()

    # Clear previous search results
        for item in tree2.get_children():
            tree2.delete(item)

    # Connect to SQLite database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

    # Search query: Match either phone number or bill number
        query = """
        SELECT customers.id, customers.name, customers.phone_no, customers.bill_no, 
               eye_prescriptions.eye_type, eye_prescriptions.re_sph, eye_prescriptions.re_cyl, 
               eye_prescriptions.re_axis, eye_prescriptions.le_sph, eye_prescriptions.le_cyl, 
               eye_prescriptions.le_axis
        FROM customers
        LEFT JOIN eye_prescriptions ON customers.id = eye_prescriptions.customer_id
        WHERE customers.phone_no = ? OR customers.bill_no = ?
    """

        cursor.execute(query, (phone, bill))
        records = cursor.fetchall()

    # Populate the Treeview
        for row in records:
            tree2.insert("", tk.END, values=row)

        conn.close()
    global transaction_select, phone_select, tree2
    tk.Label(tab3, text="Bill no", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w") 
    transaction_select = tk.Entry(tab3, font=("Arial", 12), width=30)
    transaction_select.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(tab3, text="Phone No:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    phone_select = tk.Entry(tab3, font=("Arial", 12), width=30)
    phone_select.grid(row=1, column=1, padx=10, pady=5)
    
    # Search Button
    search_button = tk.Button(tab3, text="Search", font=("Arial", 12),command=search_customer)
    search_button.grid(row=2, column=0, columnspan=2, pady=10)

    table_frame2 = tk.Frame(tab3)
    table_frame2.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    columns = ("ID", "Name", "Phone", "Bill No", "Eye Type", "RE SPH", "RE CYL", "RE Axis", "LE SPH", "LE CYL", "LE Axis")
    tree2 = ttk.Treeview(table_frame2, columns=columns, show='headings')
    
    for col in columns:
        tree2.heading(col, text=col)
        tree2.column(col, width=80)  # Adjust column width
    
    tree2.pack(expand=True, fill="both")

    # Configure grid weights for proper resizing
    tab3.grid_columnconfigure(0, weight=1)
    tab3.grid_columnconfigure(1, weight=1)
    tab3.grid_rowconfigure(3, weight=1)  # Ensuring treeview expands properly

    dashboard.mainloop()

# GUI Setup
main = tk.Tk()
main.title("Omkar Optics Login Page")
main.configure(bg="white")
main.resizable(False, False)


# Get the absolute path to the directory where the script is located
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Load and resize the image
image_path = os.path.join(BASE_DIR, "Bg1.png")
image = Image.open(image_path)
image = image.resize((500, 500), Image.Resampling.LANCZOS)

# Convert to Tkinter-compatible format
bg_img = ImageTk.PhotoImage(image)

# Keep a reference to prevent garbage collection
label = Label(main, image=bg_img)
label.grid(row=0, column=0)
label.image = bg_img  # Store reference

# Login Frame
frame1 = Frame(main, bg="#D9D9D9", height=350, width=300)
frame1.grid(row=0, column=1, padx=40)

Label(frame1, text="Welcome Back! \nLogin to Account", fg="black", bg="#D9D9D9", font=("", 18, "bold")).grid(row=0, column=0, sticky="nw", pady=30, padx=10)

# Username
Label(frame1, text="Username", fg="black", bg="#D9D9D9", font=("", 12, "bold")).grid(row=1, column=0, sticky="w", padx=30)
usrname_entry = Entry(frame1, fg="black", bg="white", font=("", 16, "bold"), width=20)
usrname_entry.grid(row=2, column=0, sticky="nwe", padx=30)

# Password
Label(frame1, text="Password", fg="black", bg="#D9D9D9", font=("", 12, "bold")).grid(row=3, column=0, sticky="w", padx=30, pady=(10, 0))
passwd_entry = Entry(frame1, fg="black", bg="white", font=("", 16, "bold"), width=20, show="*")
passwd_entry.grid(row=4, column=0, sticky="nwe", padx=30, pady=5)

# Login Button
Button(frame1, text="Login", font=("", 15, "bold"), height=1, width=10, bg="#0085FF", fg="white", cursor="hand2", 
       command=login_user).grid(row=5, column=0, sticky="ne", pady=20, padx=35)


main.mainloop()
