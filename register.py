import tkinter as tk
from tkinter import messagebox, Entry, Label, Button, Frame, ttk
import mysql.connector
import bcrypt
conn=None;
# MySQL config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'users',
    'port':3360
}

def register_user():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    user_type = type_var.get()

    if not username or not password or not user_type:
        messagebox.showerror("Error", "All fields are required")
        return

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, type) VALUES (%s, %s, %s)", 
                       (username, hashed_password.decode(), user_type))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully")
        register_window.destroy()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Tkinter UI for registration
register_window = tk.Tk()
register_window.title("Register")
register_window.geometry("300x300")

frame = Frame(register_window)
frame.pack(pady=30)

Label(frame, text="Register", font=("Arial", 16, "bold")).pack(pady=10)

Label(frame, text="Username").pack()
username_entry = Entry(frame)
username_entry.pack()

Label(frame, text="Password").pack()
password_entry = Entry(frame, show="*")
password_entry.pack()

Label(frame, text="User Type").pack()
type_var = tk.StringVar()
type_combo = ttk.Combobox(frame, textvariable=type_var, values=["admin", "staff"], state="readonly")
type_combo.pack()

Button(frame, text="Register", command=register_user, bg="#0085FF", fg="white").pack(pady=15)

register_window.mainloop()
