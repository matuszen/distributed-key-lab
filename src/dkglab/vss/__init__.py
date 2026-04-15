"""Verifiable secret sharing (Feldman) utilities."""

from dkglab.vss.feldman import build_feldman_commitments
from dkglab.vss.verification import verify_share

__all__ = ["build_feldman_commitments", "verify_share"]
