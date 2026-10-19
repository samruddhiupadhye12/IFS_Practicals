import hashlib
import os   

password = input("Enter your password : ")

salt = os.urandom(16)

password_bytes = password.encode('utf-8') + salt

hashed_password = hashlib.sha256(password_bytes).hexdigest()

print("Salt (hex) : ", salt.hex())
print("Your SHA256 hashed password is : ", hashed_password)