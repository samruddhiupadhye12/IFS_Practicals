def vernam_encrypt_decrypt(text, key):
    if len(text) != len(key):
        print("Key length should be same as the plaintext length.")
        return
    result =""
    for m_bit, n_bit in zip(text, key):
        if m_bit == n_bit:
            result = result + '0'
        else:
            result= result + '1'
    return result

msg = input("Enter plaintext (Binary) : ")
key = input("Enter key (Binary, same length as PT) : ")
encrypted = vernam_encrypt_decrypt(msg, key)
decrypted = vernam_encrypt_decrypt(encrypted, key)
print("Plaintext : ",msg)
print("key : ",key)
print("Encrypted (binary) : ",encrypted)
print("Decrypted (binary) : ",decrypted)
