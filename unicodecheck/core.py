import os
import difflib
import unicodedata
from io import BytesIO, BufferedReader
from chardet import UniversalDetector


def is_binary(stream: bytes | BufferedReader):
    # BOM を調べる
    #= stream.read(4)

    #= stream.seek(-3, os.SEEK_CUR)

    #
    #stream
    if isinstance(stream, bytes):
        buffer = stream
    else:
        buffer = stream.read(8000)
        stream.seek(-len(buffer), os.SEEK_CUR)
    return b"\0" in buffer


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
    enc = detector.result["encoding"]
    if enc and (encoding := enc.lower()) in ["utf-8", "utf-16", "utf-32"]:
        return encoding
    else:
        return None


def diff(str1, str2):
    d = difflib.Differ()
    dif = d.compare(str1.splitlines(), str2.splitlines())
    for line in dif:
        #
        # if line.startswith("+ ")
        # if line.startswith("- ")
        print(line)


def is_norm(text: str, mode: str) -> bool:
    return unicodedata.is_normalized(mode, text)


def normalize(text: str, mode: str) -> str:
    return unicodedata.normalize(text, mode)
