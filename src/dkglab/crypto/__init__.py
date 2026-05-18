"""Elliptic-curve domain parameters and crypto primitives."""

from dkglab.crypto.curves import CURVE, GENERATOR, GROUP_ORDER
from dkglab.crypto.schnorr import (
    SchnorrKeyPair,
    SchnorrSignature,
    generate_keypair,
    sign_message,
    verify_signature,
)

__all__ = [
    "CURVE",
    "GENERATOR",
    "GROUP_ORDER",
    "SchnorrKeyPair",
    "SchnorrSignature",
    "generate_keypair",
    "sign_message",
    "verify_signature",
]
