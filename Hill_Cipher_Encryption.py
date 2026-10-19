import numpy as np   
def text_to_numbers(text):
    numbers = []
    for char in text:
        value = ord(char.upper()) - ord('A')
        numbers.append(value)
    return numbers

def numbers_to_text(numbers):
    text = ""
    for num in numbers:
        text = text + chr(num % 26 + ord('A'))
    return text

def hill_encrypt(plaintext, key_matrix):
    numbers = text_to_numbers(plaintext)  

    block_size = key_matrix.shape[0]
    if len(numbers) % block_size != 0:
        numbers = numbers + [ord('X') - ord('A')]

    chunks = []                                
    for i in range(0, len(numbers), block_size):  #start, end, increment
        chunk = numbers[i:i+block_size]    #numbers[0:2] => [7, 4] for "HE"   
        chunks.append(chunk)  

    # Encrypt each chunk 
    encrypted_chunks = []
    for chunk in chunks:
        vector = np.array(chunk)
        encrypted_vector = np.dot(key_matrix, vector) % 26
        encrypted_chunks.extend(encrypted_vector) 

    # Convert back to text
    return numbers_to_text(encrypted_chunks)

n = int(input("Enter size of key matrix (e.g., 2 for 2x2): "))
print(f"Enter the {n*n} elements of the key matrix row by row:")
elements = []
for i in range(n):
    row = list(map(int, input(f"Row {i+1}: ").split()))
    elements.append(row)
    
key_matrix = np.array(elements)

plaintext = input("Enter the message : ")
print("Key Matrix : \n", key_matrix)
ciphertext = hill_encrypt(plaintext, key_matrix)
print("Plaintext : ", plaintext.upper())
print("Ciphertext : ", ciphertext)