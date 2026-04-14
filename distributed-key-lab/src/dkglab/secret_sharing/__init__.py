"""Secret sharing primitives and recovery logic."""

from dkglab.secret_sharing.recovery import recover_secret
from dkglab.secret_sharing.splitting import create_shares


__all__ = ["recover_secret", "create_shares"]