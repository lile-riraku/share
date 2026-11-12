#!/usr/bin/env python3
"""Show a base value increased by 1% through 10%."""

import argparse
from decimal import Decimal, InvalidOperation, localcontext


def parse_base(value: str) -> Decimal:
    try:
        base = Decimal(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError("base must be a number") from None
    if not base.is_finite():
        raise argparse.ArgumentTypeError("base must be finite")
    return base


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate base * (1 + percentage) for 1%% through 10%%.",
    )
    parser.add_argument("--base", type=parse_base, required=True, help="Base value to increase.")
    args = parser.parse_args()
    with localcontext() as context:
        context.prec = max(28, len(args.base.as_tuple().digits) + 4)
        print(f"Base: {args.base}")
        for percent in range(1, 11):
            result = args.base * (Decimal(100 + percent) / 100)
            print(f"+{percent:2d}%: {result:f}")


if __name__ == "__main__":
    main()
