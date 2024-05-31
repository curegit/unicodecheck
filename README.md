# Unicodecheck

Simple tool to check if Unicode text files are Unicode-normalized

## Install

```sh
pip3 install unicodecheck
```

## Usage

### Quickstart

```sh
unicodecheck -iv SPAM.txt
```

To check files in a directory recursively:

```sh
unicodecheck -ivr Ham/Eggs/
```

### Synopsis

The main program can be invoked either through the `unicodecheck` command or through the Python main module option `python3 -m unicodecheck`.

```txt
usage: unicodecheck [-h] [-V] [-m {NFC,NFD,NFKC,NFKD}] [-d] [-u [NUMBER]] [-r] [-i] [-v]
                    PATH [PATH ...]
```

### Options

```txt
positional arguments:
  PATH                  describe input file or directory (pass '-' to specify stdin)

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -m {NFC,NFD,NFKC,NFKD}, --mode {NFC,NFD,NFKC,NFKD}
                        target Unicode normalization (default: NFC)
  -d, --diff            show diffs between the original and normalized (default: False)
  -u [NUMBER], -U [NUMBER], --unified [NUMBER]
                        show unified diffs with NUMBER lines of context [NUMBER=3] (default: False)
  -r, --recursive       follow the directory tree rooted in each PATH argument (default: False)
  -i, --include-hidden  include hidden files and directories (default: False)
  -b PATTERN [PATTERN ...], --blacklist PATTERN [PATTERN ...]
                        notify if having PATTERN (case-sensitive) (default: None)
  -e, --error           return non-zero exit code on detection (default: False)
  -v, --verbose         report non-essential logs (default: False)
```

## Tips

### Check whether filenames are normalized

The `convmv` command is a good alternative to using this application.

#### NFC

```sh
convmv -f utf8 -t utf8 --nfc -r ./
```

#### NFD

```sh
convmv -f utf8 -t utf8 --nfd -r ./
```

## Notes

- This tool doesn't provide auto in-place (write) file normalization because Unicode normalization doesn't guarantee content equivalence.
- The procedure for determining the binary file refers to Git's algorithm.

## License

MIT
