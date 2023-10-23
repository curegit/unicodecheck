import sys

# 標準エラー出力にプリントする
def eprint(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)
