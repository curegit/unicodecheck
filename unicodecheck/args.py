# 入力パスを受ける変換関数（標準入力は None として返す）
def src(str: str) -> str | None:
    if str == "-":
        return None
    elif str:
        return str
    else:
        raise ValueError()


# 大小文字を区別しないラベルマッチのための変換関数（大文字にする）
def upper(label: str) -> str:
    return str.upper(label)
