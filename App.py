import tkinter as tk
from tkinter import messagebox
import base64
import os

DATA_FILE = "data.txt"
MASTER_FILE = "master.txt"

# ---------- Security ----------
def encode(text):
    return base64.b64encode(text.encode()).decode()

def decode(text):
    return base64.b64decode(text.encode()).decode()

# ---------- Master Password ----------
def setup_master():
    if not os.path.exists(MASTER_FILE):
        with open(MASTER_FILE, "w") as file:
            file.write(encode("admin"))  # default password

setup_master()

def check_login():
    entered = password_login.get()

    with open(MASTER_FILE, "r") as file:
        saved = decode(file.read())

    if entered == saved:
        login_window.destroy()
        open_manager()
    else:
        messagebox.showerror("Error", "Wrong password")

# ---------- Password Manager ----------
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return file.readlines()
    except:
        return []

def refresh():
    listbox.delete(0, tk.END)

    for line in load_data():
        account, password = line.strip().split(":")
        listbox.insert(tk.END, f"{account} → {decode(password)}")

def save_password():
    account = account_entry.get()
    password = password_entry.get()

    if account and password:
        with open(DATA_FILE, "a") as file:
            file.write(f"{account}:{encode(password)}\n")

        account_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        refresh()

def delete_password():
    selected = listbox.curselection()

    if selected:
        index = selected[0]

        data = load_data()
        data.pop(index)

        with open(DATA_FILE, "w") as file:
            file.writelines(data)

        refresh()

# ---------- Main Manager Window ----------
def open_manager():
    global account_entry, password_entry, listbox

    root = tk.Tk()
    root.title("Password Manager")

    tk.Label(root, text="Account").pack()
    account_entry = tk.Entry(root, width=40)
    account_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, width=40, show="*")
    password_entry.pack()

    tk.Button(root, text="Save", command=save_password).pack(pady=5)

    listbox = tk.Listbox(root, width=50)
    listbox.pack(pady=10)

    tk.Button(root, text="Delete Selected", command=delete_password).pack()

    refresh()

    root.mainloop()

# ---------- Login Window ----------
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Enter Master Password").pack(pady=10)

password_login = tk.Entry(login_window, show="*", width=30)
password_login.pack()

tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

login_window.mainloop()
