import bcrypt, getpass
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DemoDB"
)
cur = db.cursor()

username = input("Username: ")
password = getpass.getpass("Password: ")

cur.execute(
    "SELECT password,permissions FROM user WHERE username=%s",
    (username,)
)
user = cur.fetchone()

if user and bcrypt.checkpw(password.encode(), user[0]):
    print("Login Successful")
    action = input("Action(read/write/execute): ")

    permissions = user[1].split(",")

    if action in permissions:
        if action == "read":
            with open("Demo.txt", "r") as f:
                print("\nFile Content:")
                print(f.read())
        elif action == "write":
            text = input("Enter text: ")
            with open("Demo.txt", "a") as f:
                f.write(text + "\n")
            print("Written Successfully")
        elif action == "execute":
            print("Executing File Operation...")
    else:
        print("Permission Denied")

else:
    print("Authentication Failed")