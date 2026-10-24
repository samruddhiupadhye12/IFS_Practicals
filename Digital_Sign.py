import rsa
public_key, private_key = rsa.newkeys(2048)
msg = input("Enter the message for signing : ").encode()
tampered_msg = b'This is a tampered message'

sign = rsa.sign(msg, private_key, 'SHA-256')
print("Original Message : ", msg)
print("Digital Signature : ", sign.hex())
try:
    verify = rsa.verify(msg, sign, public_key)  #tampered_msg can also be used
    print("Digital signature is valid.")
except Exception:
    print("Digital signature is invalid.")