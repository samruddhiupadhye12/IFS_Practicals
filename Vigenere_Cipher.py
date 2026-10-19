def vigenere_encrypt(text, key):
    result = ""
    key = key.upper() #convert in uppercase
    key_length = len(key)
    key_index = 0

    for char in text:
        if char.isalpha():
            # Get shift from key letter
            shift = ord(key[key_index % key_length]) - 65  #repeats through PT using key

            if char.isupper():
                result = result + chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                result = result + chr((ord(char) - 97 + shift) % 26 + 97)

            # Move to next key letter
            key_index = key_index + 1

        else:
            result = result + char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    key_length = len(key)
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % key_length]) - 65

            if char.isupper():
                result = result + chr((ord(char) - 65 - shift) % 26 + 65)
            else:
                result = result + chr((ord(char) - 97 - shift) % 26 + 97)

            key_index = key_index + 1
        else:
            result = result + char
    return result

message = input("Enter message : ") 
keyword = input("Enter keyword value : ")

# HELLO - 72, 69, 76, 76, 79
#KEY - 75, 69, 89

encrypted = vigenere_encrypt(message, keyword)
decrypted = vigenere_decrypt(encrypted, keyword)

print("Original:", message)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)