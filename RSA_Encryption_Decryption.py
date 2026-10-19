import rsa
public_key, private_key = rsa.newkeys(1024)
message = input("Enter a message to encrypt: ").encode('utf-8')
encrypted = rsa.encrypt(message, public_key)
decrypted = rsa.decrypt(encrypted, private_key).decode('utf-8')
print("Encrypted (Bytes) :", encrypted)
print("Encrypted (Hex)   :", encrypted.hex())
print("Decrypted:", decrypted)