#!/usr/bin/env python3

import os
import unicodedata

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    dirname = "data"
    modes = ["NFC", "NFD", "NFKC", "NFKD"]
    encodings = ["utf_8", "utf_16", "utf_32"]

    safe_text1 = """Egg and bacon
Egg, sausage, and bacon
Egg and Spam
Egg, bacon, and Spam
Egg, bacon, sausage, and Spam
Spam, bacon, sausage, and Spam
"""

    safe_text2 = """Spam, egg, Spam, Spam, bacon, and Spam
Spam, Spam, Spam, egg, and Spam
Spam, Spam, Spam, Spam, Spam, Spam, baked beans, Spam, Spam, Spam, and Spam
"""

    for mode in modes:
        for enc in encodings:
            for i, text in enumerate(["プリキュア", "Lobster Thermidor aux crevettes with a Mornay sauce, garnished with truffle pâté, brandy, and a fried egg on top, and Spam"]):
                with open(f"{dirname}/{mode}-{i}-{enc}.txt", "wb") as f:
                    s = unicodedata.normalize(mode, text + "\n")
                    f.write(safe_text1.encode(enc))
                    f.write(s.encode(enc))
                    f.write(safe_text2.encode(enc))
    for enc in encodings:
        for i, text in enumerate(["羽羽羽"]):
            with open(f"{dirname}/neither-{i}-{enc}.txt", "wb") as f:
                f.write(safe_text1.encode(enc))
                f.write((text + "\n").encode(enc))
                f.write(safe_text2.encode(enc))
