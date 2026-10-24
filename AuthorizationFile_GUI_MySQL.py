import bcrypt
import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="IFS3_DB"
)

cursor = db.cursor()

def register_user(current_user, new_username, new_password, new_permissions):
    cursor.execute(
        "SELECT role FROM users WHERE username=%s",
        (current_user,)
    )
    user = cursor.fetchone()

    if not user or user[0] != "admin":
        messagebox.showerror("Denied", "Only Admin can register new users.")
        return

    hashed_pw = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    )
    permissions_str = ",".join(new_permissions)
    cursor.execute(
        """
        INSERT INTO users
        (username,password,permissions,role)
        VALUES (%s,%s,%s,%s)
        """,
        (
            new_username,
            hashed_pw,
            permissions_str,
            "user"
        )
    )
    db.commit()
    messagebox.showinfo(
        "Success",
        f"User {new_username} registered successfully."
    )

def authenticate(username, password):
    cursor.execute(
        "SELECT password FROM users WHERE username=%s",
        (username,)
    )
    user = cursor.fetchone()
    if user and bcrypt.checkpw(
        password.encode(),
        user[0]
    ):
        return True
    return False

def authorize(username, action):
    cursor.execute(
        "SELECT permissions FROM users WHERE username=%s",
        (username,)
    )
    user = cursor.fetchone()
    if user:
        permissions = user[0].split(",")

        if action in permissions:
            return True
    return False

def file_operation(username,
                   action,
                   filename="DemoIFS3.txt"):

    if not authorize(username, action):
        messagebox.showerror(
            "Access Denied",
            f"{username} cannot {action} this file."
        )
        return

    if action == "read":
        try:
            with open(filename, "r") as f:
                content = f.read()

            messagebox.showinfo(
                "File Content",
                content
            )
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "File not found."
            )

    elif action == "write":
        data = simpledialog.askstring(
            "Write",
            "Enter text to write:"
        )
        if data:
            with open(filename, "a") as f:
                f.write(data + "\n")

            messagebox.showinfo(
                "Success",
                "Written successfully."
            )

    elif action == "execute":
        messagebox.showinfo(
            "Execute",
            "Executing file operation (simulated)."
        )

    else:
        messagebox.showerror(
            "Error",
            "Invalid action."
        )

def show_login():
    clear_frame()
    tk.Label(
        root,
        text="Username:"
    ).pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    tk.Label(
        root,
        text="Password:"
    ).pack(pady=5)
    password_entry = tk.Entry(
        root,
        show="*"
    )
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if authenticate(username, password):
            show_actions(username)
        else:
            messagebox.showerror(
                "Denied",
                "Authentication Failed."
            )

    tk.Button(
        root,
        text="Login",
        command=login
    ).pack(pady=10)

def show_actions(username):
    clear_frame()
    messagebox.showinfo(
        "Granted",
        "Authentication Successful."
    )
    tk.Label(
        root,
        text=f"Welcome {username}",
        font=("Arial", 14)
    ).pack(pady=10)

    tk.Button(
        root,
        text="Read",
        width=15,
        command=lambda:
        file_operation(username, "read")
    ).pack(pady=5)

    tk.Button(
        root,
        text="Write",
        width=15,
        command=lambda:
        file_operation(username, "write")
    ).pack(pady=5)

    tk.Button(
        root,
        text="Execute",
        width=15,
        command=lambda:
        file_operation(username, "execute")
    ).pack(pady=5)

    cursor.execute(
        "SELECT role FROM users WHERE username=%s",
        (username,)
    )

    user = cursor.fetchone()
    if user and user[0] == "admin":
        tk.Button(
            root,
            text="Register New User",
            width=15,
            command=lambda:
            show_register(username)
        ).pack(pady=5)

    tk.Button(
        root,
        text="Back",
        width=15,
        command=show_login
    ).pack(pady=15)


def show_register(current_user):
    clear_frame()
    tk.Label(
        root,
        text="New Username:"
    ).pack(pady=5)

    new_username_entry = tk.Entry(root)
    new_username_entry.pack(pady=5)

    tk.Label(
        root,
        text="New Password:"
    ).pack(pady=5)

    new_password_entry = tk.Entry(
        root,
        show="*"
    )

    new_password_entry.pack(pady=5)

    tk.Label(
        root,
        text="Permissions (comma separated):"
    ).pack(pady=5)

    permissions_entry = tk.Entry(root)
    permissions_entry.pack(pady=5)

    def register():
        username = new_username_entry.get()
        password = new_password_entry.get()

        permissions = [
            p.strip()
            for p in permissions_entry.get().split(",")
        ]

        register_user(
            current_user,
            username,
            password,
            permissions
        )

    tk.Button(
        root,
        text="Register",
        command=register
    ).pack(pady=10)

    tk.Button(
        root,
        text="Back",
        command=lambda:
        show_actions(current_user)
    ).pack(pady=10)


def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Secure File Access")
root.geometry("300x300")

show_login()

root.mainloop()