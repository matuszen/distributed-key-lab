"""Core package for distributed-key-lab."""

from dkglab.secret_sharing.recovery import recover_secret
from dkglab.secret_sharing.splitting import create_shares
from dkglab.vss.verification import verify_share, verify_vss_package

__all__ = ["recover_secret", "verify_share", "verify_vss_package", "create_shares"]
