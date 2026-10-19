import hashlib   

def hash_file(filename):
    sha256 = hashlib.sha256()

    with open(filename, "rb") as f:
        while True:
            data = f.read(4096)  
            if not data:
                break
            sha256.update(data)  
             
    return sha256.hexdigest()

filename = "DemoIFS3.txt"
print("SHA256 Hash of file:", hash_file(filename))