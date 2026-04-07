from itertools import combinations

import pytest

from dkglab.crypto.curves import GROUP_ORDER
from dkglab.utils.types import Share
from dkglab.secret_sharing.recovery import recover_secret


def poly_eval(coeffs: list[int], x: int, modulus: int) -> int:
    acc = 0
    power = 1
    for coefficient in coeffs:
        acc = (acc + coefficient * power) % modulus
        power = (power * x) % modulus
    return acc


def build_shares(secret: int, coeffs_rest: list[int], n: int) -> list[Share]:
    coeffs = [secret] + coeffs_rest
    return [Share(x=i, y=poly_eval(coeffs, i, GROUP_ORDER)) for i in range(1, n + 1)]


def test_recover_secret_from_any_three_of_five() -> None:
    secret = 123456789
    shares = build_shares(secret=secret, coeffs_rest=[7, 11], n=5)

    for chosen in combinations(shares, 3):
        assert recover_secret(list(chosen), threshold=3) == secret


def test_recover_secret_fails_with_t_minus_one() -> None:
    secret = 987654321
    shares = build_shares(secret=secret, coeffs_rest=[17, 33], n=5)

    with pytest.raises(ValueError, match="Not enough shares"):
        recover_secret(shares[:2], threshold=3)


def test_recover_secret_rejects_duplicate_indexes() -> None:
    shares = [Share(1, 10), Share(1, 20), Share(2, 30)]
    with pytest.raises(ValueError, match="unique"):
        recover_secret(shares, threshold=3)
