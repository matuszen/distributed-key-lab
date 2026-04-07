from __future__ import annotations

from typing import Iterable, List

from ecdsa.ellipticcurve import Point

from dkglab.crypto.curves import GENERATOR, GROUP_ORDER


def build_feldman_commitments(
    coefficients: Iterable[int], modulus: int = GROUP_ORDER
) -> List[Point]:
    commitments: List[Point] = []
    for coefficient in coefficients:
        commitments.append((coefficient % modulus) * GENERATOR)
    return commitments
