import sys
import rich
from glob import iglob
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from .args import nonempty, upper
from .utils import eprint
from .core import is_binary, detect_unicode_enc, is_norm, normalize, diff

def main():
    exit_code = 0
    parser = ArgumentParser(allow_abbrev=False, formatter_class=ArgumentDefaultsHelpFormatter, description="")
    parser.add_argument("paths", metavar="PATH", type=nonempty, nargs="+", help="describe input files")
    parser.add_argument("--", dest="stdin", action="store_true", help="")
    parser.add_argument("-m", "--mode", type=upper, choices=["NFC", "NFD", "NFKC", "NFKD"], default="auto", help="")
    parser.add_argument("-d", "--diff", action="store_true", help="")
    parser.add_argument("-r", "--recursive", action="store_true", help="")
    parser.add_argument("-i", "--include-hidden", action="store_true", help="include hidden directories")
    parser.add_argument("-v", "--verbose", action="store_true", help="include hidden directories")
    args = parser.parse_args()
    treeiter = iglob()
    
    try:
        pass
        #paths = [ for ]
    except:
        pass

    fsiter = 
    for p in paths:
        if p.isdir():
            if 
    
    for f in fsiter:
        file = None
        try:
            if f is None:
                fname = "<stdin>"
                stream = sys.stdin.buffer.read()
            else:
                file = stream = open(f, "rb")


            #buf = f.read()
            if is_binary(stream):
                if args.verbose:
                    print("skip binary")
                continue
            stream.seek(0)
            enc = detect_unicode_encoding(stream)
            if enc is None:
                if args.verbose:
                    print("Not unicode")

            try:
                stream.seek(0)
                s = stream.read().decode(enc)
            except:
                print("invalid unicode (or misunderstanding encoding)")

            if is_norm(s):
                continue
            else:
                original = s
                normalized = norm(original)
                dfs = diff(original, normalized)


        finally:
            if file is not None:
                file.close()



        
            
                

    return exit_code



if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        eprint("KeyboardInterrupt")
        exit(130)
