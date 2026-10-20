import bcrypt
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="IFS3_DB"
)

cursor = db.cursor()

password = bcrypt.hashpw(
    "admin123".encode(),
    bcrypt.gensalt()
)

cursor.execute(
    """
    INSERT INTO users
    (username,password,permissions,role)
    VALUES (%s,%s,%s,%s)
    """,
    (
        "admin",
        password,
        "read,write,execute",
        "admin"
    )
)

db.commit()
print("Admin created")