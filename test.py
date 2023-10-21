import unicodedata

def is_binary(file_path):
    with open(file_path, 'rb') as file:
        return b'\0' in file.read(8000)

def is_ok(f):
    return unicodedata.is_normalized("NFC", open(f, "rb").read().decode()) 

p = open("a.txt", "wb")
strr = unicodedata.normalize("NFD", "プリキュア")
p.write(strr.encode("utf-8"))
p.close()
is_ok("a.txt")
