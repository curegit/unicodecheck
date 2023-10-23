import difflib
import unicodedata
from io import BytesIO, BufferedReader
from chardet import UniversalDetector

def is_binary(stream: bytes | BufferedReader):
    buffer = stream if isinstance(stream, bytes) else stream.read(8000)
    return b'\0' in buffer


def detect_unicode_enc(stream: bytes | BufferedReader) -> str | None:
    match stream:
         case bytes() as b:
              buf = BytesIO(b)
         case BufferedReader() as buf:
              buf = buf
         case _:
              return None
    detector = UniversalDetector()
    for line in buf:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    enc = detector.result["encoding"].lower()
    if enc in ["utf-8", "utf-16", "utf-32"]:
        return enc
    else:
        return None

def diff(str1, str2):
    d = difflib.Differ()
    dif = d.compare(str1.splitlines(), str2.splitlines())
    for line in dif:
        #
        #if line.startswith("+ ")
        #if line.startswith("- ")
        print(line)

def is_norm(str, mode):
    return unicodedata.is_normalized(mode, str)

def normalize():
    pass


