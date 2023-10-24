# 非空列を受ける変換関数
def nonempty(str: str) -> str | None:
    if str == "--":
        return None
    elif str:
        return str
    else:
        raise ValueError()


# 大小文字を区別しないラベルマッチのための変換関数（大文字にする）
def upper(label: str) -> str:
    return str.upper(label)
