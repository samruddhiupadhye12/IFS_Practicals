# MongoDB

# import bcrypt
# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["IFS3_DB"]
# users_collection = db["users"]

# # Create Admin user
# username = "Admin"
# password = "Admin@1020"
# permissions = ["read", "write", "execute"]

# hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# users_collection.insert_one({
#     "username": username,
#     "password": hashed_pw,
#     "permissions": permissions,
#     "role": "admin"
# })

# print("✅ Admin user added successfully")


# MySQL

import bcrypt
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",
    database="IFS3_DB"
)

cursor = db.cursor()

# Admin details
username = "admin"
password = "admin123"
permissions = "read,write,execute"
role = "admin"

# Generate bcrypt hash
hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Convert bytes to string because MySQL stores text
hashed_pw_str = hashed_pw.decode()

# Insert Admin
query = """
INSERT INTO users(username, password, permissions, role)
VALUES(%s, %s, %s, %s)
"""

values = (username, hashed_pw_str, permissions, role)

cursor.execute(query, values)
db.commit()

print("✅ Admin inserted successfully")

cursor.close()
db.close()