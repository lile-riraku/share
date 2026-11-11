#!/usr/bin/env python3
"""Calculate compound growth with tax on positive interest each period."""

import argparse
from decimal import Decimal, InvalidOperation, localcontext
from math import prod


def parse_rate(value: str) -> Decimal:
    try:
        rate = Decimal(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError("rate must be a number") from None
    if not rate.is_finite() or rate < -1:
        raise argparse.ArgumentTypeError("rate must be finite and at least -1")
    return rate


def parse_tax_rate(value: str) -> Decimal:
    rate = parse_rate(value)
    if not 0 <= rate <= 1:
        raise argparse.ArgumentTypeError("tax rate must be between 0 and 1")
    return rate


def parse_times(value: str) -> int:
    try:
        count = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("times must be integers") from None
    if count < 0:
        raise argparse.ArgumentTypeError("times must be non-negative")
    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate compound growth, taxing positive interest each period.",
    )
    parser.add_argument(
        "--interest-rate", type=parse_rate, required=True,
        help="Rate per period as a decimal; e.g. 0.005 means 0.5%%.",
    )
    parser.add_argument(
        "--times", type=parse_times, nargs="+", required=True,
        help="One or more non-negative integers to multiply, e.g. 15 12 5.",
    )
    parser.add_argument(
        "--tax-rate", type=parse_tax_rate, default=Decimal(0),
        help="Tax on positive profits each period, from 0 to 1; default: 0. E.g. 0.2 means 20%%.",
    )
    args = parser.parse_args()
    periods = prod(args.times)
    with localcontext() as context:
        context.prec = 50
        after_tax_rate = args.interest_rate - max(args.interest_rate, Decimal(0)) * args.tax_rate
        # Zero periods means no change, including when the interest rate is -1.
        multiplier = (1 + args.interest_rate) ** periods if periods else Decimal(1)
        after_tax_multiplier = (1 + after_tax_rate) ** periods if periods else Decimal(1)
        print(f"Periods: {' * '.join(map(str, args.times))} = {periods}")
        print(f"Final multiplier: {multiplier:.6f}")
        print(f"Total return: {(multiplier - 1) * 100:.6f}%")
        print(f"Tax rate: {args.tax_rate * 100:.6f}%")
        print(f"After-tax multiplier: {after_tax_multiplier:.6f}")
        print(f"After-tax return: {(after_tax_multiplier - 1) * 100:.6f}%")


if __name__ == "__main__":
    main()
