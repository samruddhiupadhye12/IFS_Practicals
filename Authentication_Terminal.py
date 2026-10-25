import mysql.connector
import bcrypt, random, string, getpass, re

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="Authentication_Users"
)
cursor = db.cursor()

def validate_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[@#$%^&*!]", password)
    )

def generate_captcha():
    return ''.join(random.choices( string.ascii_letters + string.digits,k=5 ))

# Register
def register():
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    if not validate_password(password):
        print("Password must contain:")
        print("1 Uppercase, 1 Lowercase, 1 Number, 1 Special Character, Minimum 8 Characters")
        return
    
    hashed_pw = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

    cursor.execute("INSERT INTO users(username,password) VALUES(%s,%s)",(username, hashed_pw))
    db.commit()

    print("Registration Successful")
    print("You are ready to use application!")

# Login
def login():
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    
    captcha = generate_captcha()
    print("Captcha:", captcha)
    user_captcha = input("Enter Captcha: ")
    if user_captcha != captcha:
        print("Invalid Captcha")
        return

    cursor.execute("SELECT password FROM users WHERE username=%s",(username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode(),user[0]):
        print("Login Successful")
        print("You are ready to use application!")
    else:
        print("Invalid Username or Password")

# Main Menu
while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter Choice: ")
    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        break
    else:
        print("Invalid Choice")