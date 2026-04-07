"""Elliptic-curve constants used across the project."""

from ecdsa.curves import SECP256k1

CURVE = SECP256k1
GENERATOR = CURVE.generator
GROUP_ORDER = CURVE.order
