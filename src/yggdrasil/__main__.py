from __future__ import annotations

import argparse
import json
import sys

from yggdrasil import __version__, classify


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="yggdrasil")
    parser.add_argument("--version", action="store_true")
    sub = parser.add_subparsers(dest="cmd")
    c = sub.add_parser("classify")
    c.add_argument("atom", help="route atom JSON")
    args = parser.parse_args(argv)
    if args.version:
        print(__version__)
        return 0
    if args.cmd == "classify":
        atom = json.loads(args.atom)
        json.dump(classify(atom), sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
