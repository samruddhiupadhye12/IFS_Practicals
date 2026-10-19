def rail_fence_encrypt(text, rails):
    fence = []  #fence = [[], [], []] for 3 rails
    for i in range(rails):
        rail_each = []
        fence.append(rail_each)  
        rail = 0
        direction = 1   #1=down, -1=up

    for char in text:
        fence[rail].append(char)
        rail = rail + direction
        if rail == 0 or rail == rails - 1:
            direction = direction * -1            
    return ''.join([''.join(row) for row in fence])

def rail_fence_decrypt(cipher, rails):    
    pattern = []
    for i in range(rails):
        rail_each = []
        pattern.append(rail_each)
        rail = 0
        direction = 1

    for i in range(len(cipher)):
        pattern[rail].append(i)
        rail = rail + direction
        if rail == 0 or rail == rails - 1:
            direction = direction * -1
    order = [pos for row in pattern for pos in row] 
    
    result = [''] * len(cipher)
    idx = 0
    for pos in order:
        result[pos] = cipher[idx]
        idx = idx + 1
    return ''.join(result)

msg = input("Enter the message : ")
rails = int(input("Enter the number of rails : "))

encrypted = rail_fence_encrypt(msg, rails)
decrypted = rail_fence_decrypt(encrypted, rails)

print("Original : ", msg)
print("Encrypted : ", encrypted)
print("Decrypted: ", decrypted)