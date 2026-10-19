import hashlib   

message = input("Enter a message : ")

message_bytes = message.encode('utf-8')

md5_hash = hashlib.md5(message_bytes).hexdigest()

sha256_hash = hashlib.sha256(message_bytes).hexdigest()

print("Original Message:", message)
print("MD5 Hash:", md5_hash)
print("SHA256 Hash:", sha256_hash)