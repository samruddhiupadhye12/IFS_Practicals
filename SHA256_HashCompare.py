import hashlib 

m1 = input("Enter the first message: ")
m2 = input("Enter the second message: ")

bytes1 = m1.encode('utf-8')
bytes2 = m2.encode('utf-8')

hash1 = hashlib.sha256(bytes1).hexdigest()
hash2 = hashlib.sha256(bytes2).hexdigest()

if hash1 == hash2:
    print("Both messages have the SAME hash.")
else:
    print("Hashes are DIFFERENT.")

print("Message 1:", m1)
print("SHA256 Hash 1:", hash1)
print("Message 2:", m2)
print("SHA256 Hash 2:", hash2)