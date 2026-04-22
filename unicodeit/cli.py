import sys

from .replace import replace


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    result = [replace(value) for value in args]
    print(' '.join(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
