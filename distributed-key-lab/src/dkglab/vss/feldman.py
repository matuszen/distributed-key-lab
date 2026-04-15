from __future__ import annotations

from typing import Iterable, List

from ecdsa.ellipticcurve import Point

from dkglab.crypto.curves import GENERATOR, GROUP_ORDER
from dkglab.utils.types import Share, VSSPackage


def build_feldman_commitments(
    coefficients: Iterable[int], modulus: int = GROUP_ORDER
) -> List[Point]:
    commitments: List[Point] = []
    for coefficient in coefficients:
        commitments.append((coefficient % modulus) * GENERATOR)
    return commitments


def create_vss_package(share: Share, coefficients: List[int]) -> VSSPackage:
    """
    Creates a Verifiable Secret Sharing package.
    
    Args:
        share: The private share for a participant.
        coefficients: The secret polynomial coefficients.
        
    Returns:
        A VSSPackage containing the share and public commitments.
    """
    commitments = build_feldman_commitments(coefficients)
    
    return VSSPackage(share=share, commitments=commitments)