def encrypt_columnar(text, key):
    text = text.replace(" ", "")
    num_cols = len(key)
    num_rows = -(-len(text) // num_cols)  
    padded_text = text.ljust(num_rows * num_cols, 'x')

    matrix = []     
    for i in range(0, len(padded_text), num_cols):
        row = padded_text[i:i+num_cols]   
        matrix.append(row)     

    col_order = sorted(range(len(key)), key=lambda k: key[k])

    ciphertext = ''.join(''.join(row[i] for row in matrix) for i in col_order)    
    return ciphertext

def decrypt_columnar(ciphertext, key):
    num_cols = len(key)
    num_rows = -(-len(ciphertext) // num_cols)
    col_order = sorted(range(len(key)), key=lambda k: key[k]) #lambda used to pair index with char
    col_length = num_rows
    
    # Split ciphertext into columns
    columns = {}
    start = 0
    for i in col_order:
        columns[i] = ciphertext[start:start+col_length]
        start = start + col_length
    
    # Reconstruct the matrix row by row
    matrix = []
    for r in range(num_rows):
        row = ""   
        for c in range(num_cols):
            row = row + columns[c][r]
        matrix.append(row)
    
    plaintext = ''.join(matrix).rstrip('x')
    return plaintext

key = input("Enter the key: ")
text = input("Enter the plaintext: ")

print("Plaintext : ", text)
cipher = encrypt_columnar(text, key)
print("Ciphertext : ", cipher)

plain = decrypt_columnar(cipher, key)
print("Plaintext : ", plain)