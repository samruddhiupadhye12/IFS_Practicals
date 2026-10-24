import bcrypt
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DemoDB"
)

cursor = db.cursor()

username = "Samruddhi"
password = "Samruddhi@12"
permissions = "read,write"

hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

hashed_pw_str = hashed_pw.decode()

query = "INSERT INTO user(username, password, permissions) VALUES(%s, %s, %s)"

values = (username, hashed_pw_str, permissions)

cursor.execute(query, values)
db.commit()

print("Inserted successfully")

cursor.close()
db.close()