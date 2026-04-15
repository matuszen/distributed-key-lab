"""Verification of shares against Feldman commitments."""

from __future__ import annotations

from typing import Sequence

from ecdsa.ellipticcurve import INFINITY, Point

from dkglab.crypto.curves import GENERATOR, GROUP_ORDER
from dkglab.utils.types import Share


def verify_share(
    share: Share,
    commitments: Sequence[Point],
    participant_index: int | None = None,
    modulus: int = GROUP_ORDER,
) -> bool:
    if not commitments:
        raise ValueError("Commitments list cannot be empty.")

    index = participant_index if participant_index is not None else share.x
    if index <= 0:
        raise ValueError("Participant index must be positive.")

    lhs = (share.y % modulus) * GENERATOR

    rhs = INFINITY
    for power, commitment in enumerate(commitments):
        scalar = pow(index, power, modulus)
        rhs = rhs + scalar * commitment

    return lhs == rhs
