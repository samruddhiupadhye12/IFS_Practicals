import bcrypt
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["IFS3_DB"]
users_collection = db["users"]

# Create Admin user
username = "Admin"
password = "Admin@1020"
permissions = ["read", "write", "execute"]

hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

users_collection.insert_one({
    "username": username,
    "password": hashed_pw,
    "permissions": permissions,
    "role": "admin"
})

print("✅ Admin user added successfully")

