def vernam_encrypt(message, key):
    if len(message) != len(key):
        raise ValueError("Key must be the same length as message")
    result = []
    for m_char, k_char in zip(message, key):
        xor_val = ord(m_char) ^ ord(k_char)
        # Convert to 2-digit hex string 
        result.append(format(xor_val, '02x'))
    return ''.join(result)

def vernam_decrypt(ciphertext_hex, key):
    if len(ciphertext_hex) // 2 != len(key):
        raise ValueError("Ciphertext length must be twice the key length (hex encoding)")
    result = []
    for i, k_char in enumerate(key):
        xor_val = int(ciphertext_hex[2*i:2*i+2], 16)
        result.append(chr(xor_val ^ ord(k_char)))
    return ''.join(result)

message = input("Enter the plain text: ")
key     = input("Enter the key (same length as msg): ")
ciphertext = vernam_encrypt(message, key)
print("Ciphertext (hex):", ciphertext)
decrypted = vernam_decrypt(ciphertext, key)
print("Decrypted:", decrypted)