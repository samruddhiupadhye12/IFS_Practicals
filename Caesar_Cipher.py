def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        
        if char.isupper():
            result = result + chr((ord(char) - 65 + shift) % 26 + 65)  #-65 to normalize to 0-25, %26 to wrap around, +65 to convert back to ASCII
    
        elif char.islower():
            result = result + chr((ord(char) - 97 + shift) % 26 + 97)
        # Keep non-alphabet characters unchanged
        else:
            result = result + char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

message = input("Enter message : ")  #SECURITY - 83, 69, 67, 85, 82, 73, 84, 89 , shift - 3
shift_value = int(input("Enter shift value : "))

encrypted = caesar_encrypt(message, shift_value)
decrypted = caesar_decrypt(encrypted, shift_value)

print("Original:", message)
print("Shifted by : ",shift_value)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)