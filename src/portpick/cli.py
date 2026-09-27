from __future__ import annotations

import argparse
import json

from .core import PortRangeError, find_available_ports


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="portpick",
        description="Find available TCP ports in a predictable range.",
    )
    parser.add_argument("--from", dest="start", type=int, default=3000, help="first port (default: 3000)")
    parser.add_argument("--to", dest="end", type=int, default=3999, help="last port (default: 3999)")
    parser.add_argument("--host", default="127.0.0.1", help="bind host used for the check")
    parser.add_argument("--count", type=int, default=1, help="number of ports to find")
    parser.add_argument(
        "--exclude",
        action="append",
        type=int,
        default=[],
        metavar="PORT",
        help="skip a port; may be repeated",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit JSON")
    parser.add_argument(
        "--separator",
        default="\n",
        help=r"separator for plain output; supports \n, \t, and commas",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        ports = find_available_ports(
            args.start,
            args.end,
            host=args.host,
            count=args.count,
            exclude=set(args.exclude),
        )
    except (PortRangeError, OSError) as error:
        payload = {"ok": False, "error": str(error)}
        print(json.dumps(payload) if args.as_json else f"portpick: {error}")
        return 1

    if args.as_json:
        print(json.dumps({"ok": True, "host": args.host, "ports": ports}))
    else:
        separator = args.separator.encode().decode("unicode_escape")
        print(separator.join(str(port) for port in ports))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
