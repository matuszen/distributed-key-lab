"""Schnorr signing interface used before threshold signing rounds."""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Set

from ecdsa.ellipticcurve import INFINITY, Point

from dkglab.crypto.curves import GENERATOR, GROUP_ORDER
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


@dataclass(frozen=True)
class NonceCommitment:
    participant_id: int
    commitment: Point


@dataclass(frozen=True)
class NonceShare:
    participant_id: int
    nonce: int
    commitment: Point


def generate_nonce_commitment(
    participant_id: int, nonce: int | None = None
) -> NonceShare:
    if participant_id <= 0:
        raise ValueError("Participant id must be positive.")

    k = nonce if nonce is not None else secrets.randbelow(GROUP_ORDER - 1) + 1
    if not (0 < k < GROUP_ORDER):
        raise ValueError("Nonce must be in the range [1, n-1].")

    commitment = k * GENERATOR
    if commitment == INFINITY:
        raise ValueError("Nonce commitment cannot be infinity.")

    return NonceShare(participant_id=participant_id, nonce=k, commitment=commitment)


def select_participants(
    available_ids: Sequence[int], threshold: int, selection: Sequence[int] | None = None
) -> List[int]:
    if threshold <= 0:
        raise ValueError("Threshold must be greater than zero.")
    if not available_ids:
        raise ValueError("At least one participant must be available.")

    unique_available = list(dict.fromkeys(available_ids))
    if any(pid <= 0 for pid in unique_available):
        raise ValueError("Participant ids must be positive.")

    if selection is not None:
        if len(selection) != threshold:
            raise ValueError("Selection size must match threshold.")
        if any(pid not in unique_available for pid in selection):
            raise ValueError("Selection must be a subset of available ids.")
        if len(set(selection)) != len(selection):
            raise ValueError("Selection must contain unique ids.")
        return list(selection)

    if threshold > len(unique_available):
        raise ValueError("Threshold cannot exceed number of available participants.")

    return sorted(unique_available)[:threshold]


@dataclass
class ThresholdSigningSession:
    selected_ids: Set[int]
    commitments: Dict[int, Point] = field(default_factory=dict)

    def add_commitment(self, commitment: NonceCommitment) -> None:
        if commitment.participant_id not in self.selected_ids:
            raise ValueError("Participant is not selected for signing.")
        if commitment.participant_id in self.commitments:
            raise ValueError("Commitment already received from participant.")
        if commitment.commitment == INFINITY:
            raise ValueError("Commitment cannot be infinity.")

        self.commitments[commitment.participant_id] = commitment.commitment

    def missing_participants(self) -> List[int]:
        return sorted(self.selected_ids - set(self.commitments))

    def is_complete(self) -> bool:
        return len(self.commitments) == len(self.selected_ids)

    def aggregate_commitment(self) -> Point:
        if not self.is_complete():
            raise ValueError("Not all nonce commitments have been collected.")

        acc: Point = INFINITY
        for commitment in self.commitments.values():
            acc = acc + commitment
        return acc
