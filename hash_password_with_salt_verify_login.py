import mysql.connector
import os, getpass, hashlib

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="pass_salt"
)
cursor = db.cursor()

def register():
    username = input("Enter username : ")
    password = getpass.getpass("Enter password : ")
    salt = os.urandom(16)
    salt_hex = salt.hex()
    pass_hash = hashlib.sha256(salt+password.encode('utf-8')).hexdigest()
    
    cursor.execute("INSERT INTO users(username, password, salt) VALUES(%s,%s,%s)", (username,pass_hash,salt_hex))
    db.commit()

    print("User stored successfully!")
    return

def login():
    username = input("Enter username : ")
    password = getpass.getpass("Enter password : ")

    cursor.execute("SELECT password,salt FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    login_hash = hashlib.sha256( bytes.fromhex(user[1])+password.encode() ).hexdigest()

    if login_hash == user[0]:
        print("Logged in successfully!")
        return
    else:
        print("Login failed!")
        return
    
print("\n1.Register")
print("2.Login")
choice = input("Enter choice : ")
if choice == '1':
    register()
elif choice == '2':
    login()
else:
    print("Invalid choice")