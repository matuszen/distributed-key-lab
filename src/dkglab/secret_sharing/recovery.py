"""Secret reconstruction API based on Lagrange interpolation."""

from __future__ import annotations

from typing import Sequence

from dkglab.crypto.curves import GROUP_ORDER
from dkglab.secret_sharing.lagrange import interpolate_at_zero
from dkglab.utils.types import Share


def recover_secret(
    shares: Sequence[Share], threshold: int, modulus: int = GROUP_ORDER
) -> int:
    if threshold <= 0:
        raise ValueError("Threshold must be greater than zero.")
    if len(shares) < threshold:
        raise ValueError("Not enough shares to recover secret.")

    selected_shares = list(shares)[:threshold]
    return interpolate_at_zero(selected_shares, modulus)
