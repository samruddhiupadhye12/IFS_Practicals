import bcrypt
import tkinter as tk
from tkinter import messagebox, simpledialog
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["IFS3_DB"]
users_collection = db["users"]

def register_user(current_user, new_username, new_password, new_permissions):
    user = users_collection.find_one({"username": current_user})
    if not user or user.get("role") != "admin":
        messagebox.showerror("Denied", "Only Admin can register new users.")
        return
    hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    users_collection.insert_one({
        "username": new_username,
        "password": hashed_pw,
        "permissions": new_permissions, 
        "role": "user"  
    })
    messagebox.showinfo("Success", f"User {new_username} registered successfully.")

def authenticate(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return True
    return False

def authorize(username, action):
    user = users_collection.find_one({"username": username})
    if user and action in user["permissions"]:
        return True
    return False

def file_operation(username, action, filename="DemoIFS3.txt"):
    if not authorize(username, action):
        messagebox.showerror("Access Denied", f"{username} cannot {action} this file.")
        return
    if action == "read":
        try:
            with open(filename, "r") as f:
                content = f.read()
            messagebox.showinfo("File Content", content)
        except FileNotFoundError:
            messagebox.showerror("File not found.", "Error")
    elif action == "write":
        data = simpledialog.askstring("Write", "Enter text to write:")
        if data:
            with open(filename, "a") as f:
                f.write(data + "\n")
            messagebox.showinfo("Success", "Written successfully.")
    elif action == "execute":
        messagebox.showinfo("Execute", "Executing file operation (simulated).")
    else:
        messagebox.showerror("Invalid action.", "Error")

def show_login():
    clear_frame()
    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if authenticate(username, password):
            show_actions(username)
        else:
            messagebox.showerror("Denied", "Authentication Failed.")

    tk.Button(root, text="Login", command=login).pack(pady=10)

def show_actions(username):
    clear_frame()
    messagebox.showinfo("Granted", "Authentication Successful.")
    tk.Label(root, text=f"!!Welcome {username}!!", font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="Read", width=15, command=lambda: file_operation(username, "read")).pack(pady=5)
    tk.Button(root, text="Write", width=15, command=lambda: file_operation(username, "write")).pack(pady=5)
    tk.Button(root, text="Execute", width=15, command=lambda: file_operation(username, "execute")).pack(pady=5)

    user = users_collection.find_one({"username": username})
    if user and user.get("role") == "admin":
        tk.Button(root, text="Register New User", width=15, command=lambda: show_register(username)).pack(pady=5)

    tk.Button(root, text="⬅ Back", width=15, command=show_login).pack(pady=15)

def show_register(current_user):
    clear_frame()
    tk.Label(root, text="New Username:").pack(pady=5)
    new_username_entry = tk.Entry(root)
    new_username_entry.pack(pady=5)

    tk.Label(root, text="New Password:").pack(pady=5)
    new_password_entry = tk.Entry(root, show="*")
    new_password_entry.pack(pady=5)

    tk.Label(root, text="Permissions (comma separated):").pack(pady=5)
    permissions_entry = tk.Entry(root)
    permissions_entry.pack(pady=5)

    def register():
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()
        permissions = [p.strip() for p in permissions_entry.get().split(",")]
        register_user(current_user, new_username, new_password, permissions)

    tk.Button(root, text="Register", command=register).pack(pady=10)
    tk.Button(root, text="⬅ Back", command=lambda: show_actions(current_user)).pack(pady=10)

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Secure File Access")
root.geometry("300x300")

show_login()
root.mainloop()