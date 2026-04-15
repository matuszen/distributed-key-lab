"""Core package for distributed-key-lab."""

from dkglab.secret_sharing.recovery import recover_secret
from dkglab.vss.verification import verify_share

__all__ = ["recover_secret", "verify_share"]
