"""Validate stable release versions and their notes."""

import argparse
import re
import sys
from pathlib import Path

VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\Z")


def parse_version(value: str) -> tuple[int, int, int]:
    match = VERSION.fullmatch(value.strip())
    if match is None:
        raise ValueError("Invalid stable semantic version")
    return tuple(map(int, match.groups()))


def validate_version(current: tuple[int, int, int], previous: str | None) -> None:
    if previous is None:
        if current != (1, 0, 0):
            raise ValueError("Initial version must be 1.0.0")
    elif current <= parse_version(previous):
        raise ValueError("Version must increase")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("version", type=Path)
    parser.add_argument("notes", type=Path)
    parser.add_argument("--previous")
    args = parser.parse_args()
    try:
        current = parse_version(args.version.read_text(encoding="utf-8"))
        if not args.notes.read_text(encoding="utf-8").strip():
            raise ValueError("Release notes are empty")
        validate_version(current, args.previous)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(".".join(map(str, current)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
