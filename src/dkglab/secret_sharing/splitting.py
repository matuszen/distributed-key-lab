"""Share generation helpers for Shamir secret sharing."""

from __future__ import annotations

import secrets
from typing import Iterable, List, Sequence

from dkglab.crypto.curves import GROUP_ORDER
from dkglab.utils.types import Share


def generate_coefficients(
    secret: int, threshold: int, modulus: int = GROUP_ORDER
) -> List[int]:
    if threshold <= 0:
        raise ValueError("Threshold must be greater than zero.")
    if not (0 < secret < modulus):
        raise ValueError("Secret must be in the range [1, modulus-1].")

    if threshold == 1:
        return [secret]

    middle_coefficients = [
        secrets.randbelow(modulus) for _ in range(threshold - 2)
    ]
    highest_coefficient = secrets.randbelow(modulus - 1) + 1
    return [secret] + middle_coefficients + [highest_coefficient]


def evaluate_polynomial(coefficients: Iterable[int], x: int, modulus: int) -> int:
    coeffs = list(coefficients)
    acc = 0
    for coefficient in reversed(coeffs):
        acc = (acc * x + coefficient) % modulus
    return acc


def create_shares_from_coefficients(
    coefficients: Sequence[int], num_participants: int, modulus: int = GROUP_ORDER
) -> List[Share]:
    if num_participants <= 0:
        raise ValueError("Number of participants must be positive.")
    if not coefficients:
        raise ValueError("Coefficient list cannot be empty.")

    return [
        Share(x=idx, y=evaluate_polynomial(coefficients, idx, modulus))
        for idx in range(1, num_participants + 1)
    ]


def create_shares(
    secret: int, threshold: int, num_participants: int, modulus: int = GROUP_ORDER
) -> List[Share]:
    if threshold > num_participants:
        raise ValueError("Threshold cannot be greater than number of participants.")
    coefficients = generate_coefficients(
        secret=secret, threshold=threshold, modulus=modulus
    )
    return create_shares_from_coefficients(coefficients, num_participants, modulus)
