"""Verifiable secret sharing (Feldman) utilities."""

from dkglab.vss.feldman import build_feldman_commitments, create_vss_package
from dkglab.vss.verification import verify_share, verify_vss_package

__all__ = [
    "build_feldman_commitments",
    "create_vss_package",
    "verify_share",
    "verify_vss_package",
]
