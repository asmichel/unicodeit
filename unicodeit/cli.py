import argparse
import sys

from .replace import replace


def main(argv=None):
    """Read UnicodeIt source from sys.stdin and reject argv positional input."""
    parser = argparse.ArgumentParser(
        prog='unicodeit',
        description='Convert LaTeX snippets from stdin to Unicode.',
    )
    args = sys.argv[1:] if argv is None else argv

    if '-h' in args or '--help' in args:
        parser.print_help()
        return 0

    if args:
        parser.print_help()
        return 1

    print(replace(sys.stdin.read()), end='')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
