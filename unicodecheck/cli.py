import sys
import glob
import os.path
from pathlib import Path
from io import BufferedIOBase
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from rich.console import Console
from rich.text import Text
from .args import uint, src, upper
from .core import is_binary, detect_unicode_enc, is_norm, normalize, diff


def main() -> int:
    console = Console()
    error_console = Console(stderr=True)

    def write(text: str | None = None) -> None:
        if text is not None:
            console.print(text, end="")

    def print(text: str | None = None) -> None:
        if text is not None:
            console.print(text)
        else:
            console.print()

    def print_issue(text: str) -> None:
        t = Text.assemble(("Info:", "bold yellow"), " ", text)
        error_console.print(t)

    def print_verbose(text: str) -> None:
        t = Text.assemble(("Info:", "green"), " ", text)
        error_console.print(t)

    def print_cancel(text: str) -> None:
        error_console.print(text)

    def print_error(text: str) -> None:
        t = Text.assemble(("Error:", "bold red"), " ", text)
        error_console.print(t)

    try:
        from . import __version__ as version

        exit_code = 0
        parser = ArgumentParser(
            prog="unicodecheck",
            allow_abbrev=False,
            formatter_class=ArgumentDefaultsHelpFormatter,
            description="Check if Unicode text files are Unicode-normalized",
            prefix_chars="-",
        )
        parser.add_argument("paths", metavar="PATH", type=src, nargs="+", help="describe input file or directory (pass '-' to specify stdin)")
        parser.add_argument("-V", "--version", action="version", version=version)
        parser.add_argument("-m", "--mode", type=upper, choices=["NFC", "NFD", "NFKC", "NFKD"], default="NFC", help="target Unicode normalization")
        parser.add_argument("-d", "--diff", action="store_true", help="show diffs between the original and normalized")
        parser.add_argument("-u", "-U", "--unified", metavar="NUMBER", default=False, type=uint, nargs="?", const=3, help="use unified diff with NUMBER lines of context [NUMBER=3]")
        parser.add_argument("-r", "--recursive", action="store_true", help="follow the directory tree rooted in each PATH argument")
        parser.add_argument("-i", "--include-hidden", action="store_true", help="include hidden files and directories")
        parser.add_argument("-v", "--verbose", action="store_true", help="report non-essential logs")
        args = parser.parse_args()

        mode: str = args.mode
        show_diff: bool = args.diff
        unified_diff: bool = args.unified is not False
        context_lines: int = 0 if args.unified is None else args.unified
        recursive: bool = args.recursive
        include_hidden: bool = args.include_hidden
        verbose: bool = args.verbose
        paths = list(args.paths)

        # stdin の出現を 1 回にする
        if None in paths:
            paths = [p for p in paths if p is not None]
            paths.append(None)
        # 各入力パスについて処理
        for p in paths:
            files: list[Path | None] = []
            # stdin の場合
            if p is None:
                files.append(None)
            # それ以外
            else:
                try:
                    path = Path(p).resolve(strict=False)
                    # 存在するファイルならそれを追加
                    if path.is_file():
                        files.append(path)
                    # 存在するディレクトリなら中身を追加
                    elif path.is_dir():
                        if recursive:
                            pattern = os.path.join(glob.escape(str(path)), "**", "*")
                        else:
                            pattern = os.path.join(glob.escape(str(path)), "*")
                        globs = (Path(e) for e in glob.iglob(pattern, recursive=recursive, include_hidden=include_hidden))
                        files += [f for f in globs if f.is_file()]
                    # 存在しないパスの場合
                    else:
                        print_error(f"{path}: No such file or directory")
                        exit_code = 1
                        break
                except Exception:
                    print_error(f"{p}: Unprocessable path")
                    exit_code = 1
                    break
            # ファイルごとに処理
            for f in files:
                file = None
                try:
                    stream: bytes | BufferedIOBase
                    if f is None:
                        fpath = "<stdin>"
                        fname = fpath
                        stream = sys.stdin.buffer.read()
                    else:
                        fpath = str(f)
                        fname = f.name
                        file = stream = open(f, "rb")
                    # バイナリファイルをフィルタ
                    isbin = is_binary(stream)
                    if isbin is None:
                        if verbose:
                            print_verbose(f"{fpath}: Skip empty file")
                        continue
                    if isbin:
                        if verbose:
                            print_verbose(f"{fpath}: Skip binary file")
                        continue
                    # ユニコードの符号方式を調べる
                    encoding = detect_unicode_enc(stream)
                    if encoding is None:
                        if args.verbose:
                            print_verbose(f"{fpath}: Skip non-Unicode file")
                        continue
                    # デコードをテスト
                    try:
                        if isinstance(stream, bytes):
                            text = stream.decode(encoding)
                        else:
                            text = stream.read().decode(encoding)
                    except Exception:
                        print_issue(f"{fpath}: Invalid Unicode (or misunderstanding encoding)")
                        continue
                    # 正規形かテスト
                    if is_norm(text, mode):
                        if verbose:
                            print_verbose(f"{fpath}: OK ({mode})")
                        continue
                    # 正規形でない場合
                    print_issue(f"{fpath}: Not normalized in {mode}")
                    if show_diff:
                        normalized = normalize(text, mode)
                        for line in diff(text, normalized, filename=fname, unified=unified_diff, n=context_lines):
                            write(line)
                        print()
                # 想定しないエラーを強調表示して続行（パーミッションエラーなど）
                except Exception as e:
                    print_error(f"{fpath}: {e}")
                # ファイルの後処理
                finally:
                    if file is not None:
                        file.close()
        return exit_code

    # SIGINT での終了を短く表示
    except KeyboardInterrupt:
        print_cancel("KeyboardInterrupt")
        return 130
