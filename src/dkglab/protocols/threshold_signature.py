"""Schnorr signing interface used before threshold signing rounds."""

from __future__ import annotations

from dataclasses import dataclass

from ecdsa.ellipticcurve import Point

from dkglab.crypto.schnorr import (
    SchnorrKeyPair,
    SchnorrSignature,
    generate_keypair,
    sign_message,
    verify_signature,
)


@dataclass(frozen=True)
class SchnorrSigner:
    """Single-signer interface to be reused by threshold orchestration."""

    private_key: int
    public_key: Point

    @classmethod
    def generate(cls) -> "SchnorrSigner":
        keypair: SchnorrKeyPair = generate_keypair()
        return cls(private_key=keypair.private_key, public_key=keypair.public_key)

    def sign(self, message: bytes) -> SchnorrSignature:
        return sign_message(self.private_key, message)

    @staticmethod
    def verify(public_key: Point, message: bytes, signature: SchnorrSignature) -> bool:
        return verify_signature(public_key, message, signature)
