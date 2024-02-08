import os
import difflib
import unicodedata
from io import BytesIO, BufferedReader
from chardet import UniversalDetector


# ファイルがバイナリかテキストか判定する
def is_binary(stream: bytes | BufferedReader) -> bool:
    if isinstance(stream, bytes):
        buf = stream
    else:
        buf = stream.read(8000)
        stream.seek(-len(buf), os.SEEK_CUR)
        if not isinstance(buf, bytes):
            raise RuntimeError()
    # BOM ベースの識別
    length = len(buf)
    if length >= 4:
        head = buf[:2]
        if head == bytes.fromhex("FEFF") and length % 2 == 0:
            return False
        if head == bytes.fromhex("FFFE") and length % 2 == 0:
            return False
    if length >= 8:
        head = buf[:4]
        if head == bytes.fromhex("0000FEFF") and length % 4 == 0:
            return False
        if head == bytes.fromhex("FFFE0000") and length % 4 == 0:
            return False
    # Git の方式を参考に
    return b"\0" in buf


# Unicode エンコードを検出して返す
# utf-8, utf-16, utf-32 のどれでもない場合は None を返す
def detect_unicode_enc(stream: bytes | BufferedReader) -> str | None:
    match stream:
        case bytes() as b:
            buf = BytesIO(b)
        case BufferedReader() as b:
            buf = b
        case _:
            return None
    pos = buf.tell()
    detector = UniversalDetector()
    for line in buf:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    buf.seek(pos)
    enc = detector.result["encoding"]
    if enc and (encoding := enc.lower()) in ["utf-8", "utf-16", "utf-32"]:
        return encoding
    else:
        return None


def diff(str1, str2):
    d = difflib.Differ()
    diffs = d.compare(str1.splitlines(), str2.splitlines())
    for line in diffs:
        # TODO
        # if line.startswith("+ ")
        # if line.startswith("- ")
        yield line


def is_norm(text: str, mode: str) -> bool:
    return unicodedata.is_normalized(mode, text)


def normalize(text: str, mode: str) -> str:
    return unicodedata.normalize(mode, text)
