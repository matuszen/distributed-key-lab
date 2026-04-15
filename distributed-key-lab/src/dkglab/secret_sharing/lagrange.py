from __future__ import annotations

from typing import Sequence

from dkglab.utils.types import Share


def mod_inverse(value: int, modulus: int) -> int:
    if value % modulus == 0:
        raise ValueError("No modular inverse for zero.")
    return pow(value, -1, modulus)


def validate_shares(shares: Sequence[Share]) -> None:
    if len(shares) == 0:
        raise ValueError("At least one share is required.")

    xs = [share.x for share in shares]
    if any(x <= 0 for x in xs):
        raise ValueError("Share indices must be positive integers.")
    if len(set(xs)) != len(xs):
        raise ValueError("Share indices must be unique.")


def lagrange_coefficient_at_zero(x_i: int, xs: Sequence[int], modulus: int) -> int:
    numerator = 1
    denominator = 1
    for x_j in xs:
        if x_j == x_i:
            continue
        numerator = (numerator * (-x_j % modulus)) % modulus
        denominator = (denominator * ((x_i - x_j) % modulus)) % modulus
    return (numerator * mod_inverse(denominator, modulus)) % modulus


def interpolate_at_zero(shares: Sequence[Share], modulus: int) -> int:
    validate_shares(shares)
    xs = [share.x for share in shares]

    secret = 0
    for share in shares:
        lambda_i = lagrange_coefficient_at_zero(share.x, xs, modulus)
        secret = (secret + (share.y % modulus) * lambda_i) % modulus
    return secret
