import os
import difflib
import unicodedata
from typing import Literal, TypeAlias
from collections.abc import Iterable
from io import BytesIO, IOBase
from chardet import UniversalDetector


ModeStr: TypeAlias = Literal["NFC", "NFD", "NFKC", "NFKD"]

modes: tuple[Literal["NFC"], Literal["NFD"], Literal["NFKC"], Literal["NFKD"]] = "NFC", "NFD", "NFKC", "NFKD"


# ファイルがバイナリかテキストか判定する (空列なら None)
def is_binary(stream: bytes | IOBase) -> bool | None:
    if isinstance(stream, bytes):
        buf = stream
    else:
        buf = stream.read(8000)
        stream.seek(-len(buf), os.SEEK_CUR)
        if not isinstance(buf, bytes):
            raise RuntimeError()
    length = len(buf)
    if length == 0:
        return None
    # BOM ベースの識別
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
def detect_unicode_enc(stream: bytes | IOBase) -> str | None:
    match stream:
        case IOBase() as b:
            buf = b
        case bytes() as b:
            buf = BytesIO(b)
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


def diff(original: str, normalized: str, *, filename: str, unified=False, n=3) -> Iterable[str]:
    a = original.splitlines(keepends=True)
    b = normalized.splitlines(keepends=True)
    if unified:
        fromfile = filename + " <ORIGINAL>"
        tofile = filename + " <NORMALIZED>"
        return difflib.unified_diff(a, b, fromfile=fromfile, tofile=tofile, n=n)
    else:
        return difflib.ndiff(a, b)


def is_norm(text: str, mode: ModeStr) -> bool:
    return unicodedata.is_normalized(mode, text)


def normalize(text: str, mode: ModeStr) -> str:
    return unicodedata.normalize(mode, text)
