# 非空列を受ける変換関数
def nonempty(string: str) -> str:
    if string:
        return string
    else:
        raise ValueError()


# 非負整数を受ける変換関数
def uint(string: str | int) -> int:
    value = int(string)
    if value >= 0:
        return value
    raise ValueError()


# 入力パスを受ける変換関数（標準入力は None として返す）
def src(string: str) -> str | None:
    if string == "-":
        return None
    elif string:
        return string
    else:
        raise ValueError()


# 大小文字を区別しないラベルマッチのための変換関数（大文字にする）
def upper(label: str) -> str:
    return str.upper(label)
