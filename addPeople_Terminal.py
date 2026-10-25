import bcrypt, mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="DemoDB"
)

cursor = db.cursor()

username = "Sampada"
password = "Sampada@15"
permissions = "read,execute"

hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

cursor.execute("INSERT INTO user(username, password, permissions) VALUES(%s,%s,%s)", (username, hashed_pw, permissions))
db.commit()
print("Inserted successfully!")

cursor.close()
db.close()