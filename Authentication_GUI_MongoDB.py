import tkinter as tk
from tkinter import messagebox
import re, bcrypt, random, string
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["user_database"]
users_collection = db["users"]

login_attempts = {}
captcha_value = ""  # store current captcha

# Password validation
def validate_password(password):
    return (len(password) >= 8 and
            re.search(r"[a-z]", password) and
            re.search(r"[A-Z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[\$\%\&\@\#\!\^\*]", password))

# Switch frames
def show_frame(frame):
    frame.tkraise()
    if frame == login_frame:
        generate_captcha()  # refresh captcha each time login page opens

# Generate captcha (random letters/numbers)
def generate_captcha():
    global captcha_value
    captcha_value = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))
    captcha_label.config(text=f"Captcha: {captcha_value}")
    entry_captcha.delete(0, tk.END)

# Register logic
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()

    if not validate_password(password):
        messagebox.showerror("Error", "Password must meet complexity rules.")
        return

    if users_collection.find_one({"username": username}):
        messagebox.showerror("Error", "Username already exists.")
        return

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed_pw, "email": email})
    messagebox.showinfo("Success", "Registration successful!")
    show_frame(success_frame)

# Login logic with captcha
def login_user():
    username = entry_login_username.get()
    password = entry_login_password.get()
    entered_captcha = entry_captcha.get()

    # Check captcha first
    if entered_captcha != captcha_value:
        messagebox.showerror("Error", "Invalid captcha. Try again.")
        generate_captcha()
        return

    if username not in login_attempts:
        login_attempts[username] = 0

    if login_attempts[username] >= 3:
        messagebox.showerror("Locked", "Too many failed attempts. Application will close.")
        root.destroy()
        return

    user = users_collection.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        messagebox.showinfo("Success", "Login successful!")
        login_attempts[username] = 0
        show_frame(success_frame)
    else:
        login_attempts[username] += 1
        entry_login_username.delete(0, tk.END)
        entry_login_password.delete(0, tk.END)
        entry_captcha.delete(0, tk.END)
        generate_captcha()

        if login_attempts[username] == 1:
            messagebox.showerror("Error", "Incorrect. 2 attempts left.")
        elif login_attempts[username] == 2:
            messagebox.showerror("Error", "Incorrect. 1 attempt left.")
        elif login_attempts[username] >= 3:
            messagebox.showerror("Locked", "Too many failed attempts. Application will close.")
            root.destroy()

# Main window
root = tk.Tk()
root.title("Application")
root.geometry("290x300")

# Frames
welcome_frame = tk.Frame(root)
register_frame = tk.Frame(root)
login_frame = tk.Frame(root)
success_frame = tk.Frame(root)

for frame in (welcome_frame, register_frame, login_frame, success_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Welcome screen
tk.Label(welcome_frame, text="Welcome to the Application", font=("Arial", 16)).pack(pady=20)  
tk.Button(welcome_frame, text="Register", command=lambda: show_frame(register_frame)).pack(pady=10)
tk.Button(welcome_frame, text="Login", command=lambda: show_frame(login_frame)).pack(pady=10)

# Register page
tk.Label(register_frame, text="Register", font=("Arial", 14)).pack(pady=10)

tk.Label(register_frame, text="Username").pack()
entry_username = tk.Entry(register_frame)   #Entry() is used to a single line text box for user input
entry_username.pack()   #pack() is used to available the widget on the screen.

tk.Label(register_frame, text="Password").pack()
entry_password = tk.Entry(register_frame, show="*")
entry_password.pack()

tk.Label(register_frame, text="Email").pack()
entry_email = tk.Entry(register_frame)
entry_email.pack()

tk.Button(register_frame, text="Register", command=register_user).pack(pady=10)
tk.Button(register_frame, text="Back", command=lambda: show_frame(welcome_frame)).pack()

# Login page
tk.Label(login_frame, text="Login", font=("Arial", 14)).pack(pady=10)

tk.Label(login_frame, text="Username").pack()
entry_login_username = tk.Entry(login_frame)
entry_login_username.pack()

tk.Label(login_frame, text="Password").pack()
entry_login_password = tk.Entry(login_frame, show="*")
entry_login_password.pack()

# Captcha
captcha_label = tk.Label(login_frame, text="Captcha: ")
captcha_label.pack(pady=5)
entry_captcha = tk.Entry(login_frame)
entry_captcha.pack()
tk.Button(login_frame, text="Refresh Captcha", command=generate_captcha).pack(pady=5)

login_button = tk.Button(login_frame, text="Login", command=login_user)
login_button.pack(pady=10)
tk.Button(login_frame, text="Back", command=lambda: show_frame(welcome_frame)).pack()

# Success page
tk.Label(success_frame, text="You are ready to use the application", font=("Arial", 14)).pack(pady=20)
tk.Button(success_frame, text="Back", command=lambda: show_frame(welcome_frame)).pack()

# Start with welcome
show_frame(welcome_frame)
root.mainloop()