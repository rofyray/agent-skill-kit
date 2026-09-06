#!/usr/bin/env python3
"""Generate opaque alphanumeric seeds for divergent design exploration."""

from __future__ import annotations

import argparse
import secrets
import string


ALPHABETS = {
    "alphanumeric": string.ascii_letters + string.digits,
    "hex": string.hexdigits.lower()[:16],
}


def positive_bounded(value: str, *, minimum: int, maximum: int, label: str) -> int:
    parsed = int(value)
    if not minimum <= parsed <= maximum:
        raise argparse.ArgumentTypeError(
            f"{label} must be between {minimum} and {maximum}"
        )
    return parsed


def generate_seed(length: int, alphabet: str) -> str:
    characters = ALPHABETS[alphabet]
    return "".join(secrets.choice(characters) for _ in range(length))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--length",
        type=lambda value: positive_bounded(
            value, minimum=16, maximum=256, label="length"
        ),
        default=64,
        help="seed length from 16 to 256 characters (default: 64)",
    )
    parser.add_argument(
        "--count",
        type=lambda value: positive_bounded(
            value, minimum=1, maximum=32, label="count"
        ),
        default=1,
        help="number of seeds from 1 to 32 (default: 1)",
    )
    parser.add_argument(
        "--alphabet",
        choices=sorted(ALPHABETS),
        default="alphanumeric",
        help="character set to use (default: alphanumeric)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    for _ in range(args.count):
        print(generate_seed(args.length, args.alphabet))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
