"""Schnorr signature primitives for single-signer use."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass

from ecdsa.ellipticcurve import INFINITY, Point

from dkglab.crypto.curves import GENERATOR, GROUP_ORDER

SCALAR_LENGTH = (GROUP_ORDER.bit_length() + 7) // 8


@dataclass(frozen=True)
class SchnorrSignature:
    R: Point
    s: int


@dataclass(frozen=True)
class SchnorrKeyPair:
    private_key: int
    public_key: Point


def generate_keypair() -> SchnorrKeyPair:
    private_key = secrets.randbelow(GROUP_ORDER - 1) + 1
    public_key = private_key * GENERATOR
    return SchnorrKeyPair(private_key=private_key, public_key=public_key)


def sign_message(
    private_key: int, message: bytes, nonce: int | None = None
) -> SchnorrSignature:
    if not (0 < private_key < GROUP_ORDER):
        raise ValueError("Private key must be in the range [1, n-1].")
    if not isinstance(message, (bytes, bytearray)):
        raise TypeError("Message must be bytes.")

    k = nonce if nonce is not None else secrets.randbelow(GROUP_ORDER - 1) + 1
    if not (0 < k < GROUP_ORDER):
        raise ValueError("Nonce must be in the range [1, n-1].")

    R = k * GENERATOR
    public_key = private_key * GENERATOR
    challenge = compute_challenge(R, public_key, bytes(message))
    s = (k + challenge * private_key) % GROUP_ORDER

    return SchnorrSignature(R=R, s=s)


def verify_signature(
    public_key: Point, message: bytes, signature: SchnorrSignature
) -> bool:
    if not isinstance(message, (bytes, bytearray)):
        raise TypeError("Message must be bytes.")
    if signature.R == INFINITY:
        return False
    if public_key == INFINITY:
        return False
    if not (0 <= signature.s < GROUP_ORDER):
        return False

    challenge = compute_challenge(signature.R, public_key, bytes(message))
    lhs = signature.s * GENERATOR
    rhs = signature.R + challenge * public_key

    return lhs == rhs


def compute_challenge(R: Point, public_key: Point, message: bytes) -> int:
    """Compute the Schnorr challenge e = H(R, message, PK) modulo the group order."""
    if not isinstance(message, (bytes, bytearray)):
        raise TypeError("Message must be bytes.")
    if R == INFINITY:
        raise ValueError("R cannot be infinity.")
    if public_key == INFINITY:
        raise ValueError("Public key cannot be infinity.")

    data = (
        b"DKG-LAB-SCHNORR"
        + _int_to_bytes(R.x(), SCALAR_LENGTH)
        + _int_to_bytes(R.y(), SCALAR_LENGTH)
    )
    data += _int_to_bytes(public_key.x(), SCALAR_LENGTH) + _int_to_bytes(
        public_key.y(), SCALAR_LENGTH
    )
    data += bytes(message)

    digest = hashlib.sha256(data).digest()
    return int.from_bytes(digest, "big") % GROUP_ORDER


def point_to_hex(point: Point) -> str:
    """Serialize an elliptic-curve point as stable uncompressed hexadecimal text."""
    if point == INFINITY:
        raise ValueError("Cannot serialize point at infinity.")
    return "04" + _int_to_bytes(point.x(), SCALAR_LENGTH).hex() + _int_to_bytes(
        point.y(), SCALAR_LENGTH
    ).hex()


def scalar_to_hex(value: int) -> str:
    """Serialize a scalar modulo the group order as fixed-width hexadecimal text."""
    if not (0 <= value < GROUP_ORDER):
        raise ValueError("Scalar must be in the range [0, n-1].")
    return _int_to_bytes(value, SCALAR_LENGTH).hex()


def _int_to_bytes(value: int, length: int) -> bytes:
    if value < 0:
        raise ValueError("Value must be non-negative.")
    return value.to_bytes(length, "big")
