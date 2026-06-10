"""Elliptic-curve domain parameters and crypto primitives."""

from dkglab.crypto.curves import CURVE, GENERATOR, GROUP_ORDER
from dkglab.crypto.schnorr import (
    SchnorrKeyPair,
    SchnorrSignature,
    compute_challenge,
    generate_keypair,
    point_to_hex,
    scalar_to_hex,
    sign_message,
    verify_signature,
)

__all__ = [
    "CURVE",
    "GENERATOR",
    "GROUP_ORDER",
    "SchnorrKeyPair",
    "SchnorrSignature",
    "compute_challenge",
    "generate_keypair",
    "point_to_hex",
    "scalar_to_hex",
    "sign_message",
    "verify_signature",
]
