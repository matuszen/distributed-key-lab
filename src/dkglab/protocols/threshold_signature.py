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
    compute_challenge,
    generate_keypair,
    sign_message,
    verify_signature,
)
from dkglab.protocols.dkg import public_share_for_index
from dkglab.secret_sharing.lagrange import lagrange_coefficient_at_zero
from dkglab.utils.types import Share


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


@dataclass(frozen=True)
class PartialSignature:
    participant_id: int
    value: int
    nonce_commitment: Point


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
    message: bytes = b""
    threshold: int | None = None
    public_key: Point | None = None
    aggregated_commitments: Sequence[Point] | None = None
    commitments: Dict[int, Point] = field(default_factory=dict)
    partial_signatures: Dict[int, PartialSignature] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Normalize and validate session parameters after dataclass initialization."""
        self.selected_ids = set(self.selected_ids)
        if not self.selected_ids:
            raise ValueError("At least one participant must be selected.")
        if any(participant_id <= 0 for participant_id in self.selected_ids):
            raise ValueError("Participant ids must be positive.")
        if not isinstance(self.message, (bytes, bytearray)):
            raise TypeError("Message must be bytes.")
        self.message = bytes(self.message)

        if self.threshold is not None:
            if self.threshold <= 0:
                raise ValueError("Threshold must be greater than zero.")
            if len(self.selected_ids) < self.threshold:
                raise ValueError("Not enough selected participants for threshold.")

        if self.public_key == INFINITY:
            raise ValueError("Public key cannot be infinity.")
        if self.aggregated_commitments is not None:
            if not self.aggregated_commitments:
                raise ValueError("Aggregated commitments cannot be empty.")
            self.aggregated_commitments = list(self.aggregated_commitments)

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

    def challenge(self) -> int:
        self._require_signing_context()
        pkey = self.public_key if self.public_key is not None else INFINITY
        return compute_challenge(self.aggregate_commitment(), pkey, self.message)

    def lagrange_coefficient(self, participant_id: int) -> int:
        if participant_id not in self.selected_ids:
            raise ValueError("Participant is not selected for signing.")
        return lagrange_coefficient_at_zero(
            participant_id, sorted(self.selected_ids), GROUP_ORDER
        )

    def add_partial_signature(self, partial_signature: PartialSignature) -> None:
        if partial_signature.participant_id in self.partial_signatures:
            raise ValueError("Partial signature already received from participant.")
        if not verify_partial_signature(partial_signature, self):
            raise ValueError("Partial signature failed verification.")

        self.partial_signatures[partial_signature.participant_id] = partial_signature

    def aggregate_signature(
        self, partial_signatures: Sequence[PartialSignature] | None = None
    ) -> SchnorrSignature:
        if partial_signatures is not None:
            for partial_signature in partial_signatures:
                self.add_partial_signature(partial_signature)

        if len(self.partial_signatures) != len(self.selected_ids):
            raise ValueError("Not all partial signatures have been collected.")

        s = sum(partial.value for partial in self.partial_signatures.values())
        signature = SchnorrSignature(R=self.aggregate_commitment(), s=s % GROUP_ORDER)
        self._require_signing_context()
        pkey = self.public_key if self.public_key is not None else INFINITY
        if not verify_signature(pkey, self.message, signature):
            raise ValueError("Aggregated signature failed verification.")
        return signature

    def _require_signing_context(self) -> None:
        if self.public_key is None:
            raise ValueError("Public key is required for threshold signing.")
        if self.aggregated_commitments is None:
            raise ValueError("Aggregated commitments are required for threshold signing.")


def create_partial_signature(
    participant_id: int,
    private_share: Share | int,
    nonce_share: NonceShare,
    session: ThresholdSigningSession,
) -> PartialSignature:
    """Create z_i = k_i + e * lambda_i * sk_i for a selected participant."""
    if participant_id not in session.selected_ids:
        raise ValueError("Participant is not selected for signing.")
    if nonce_share.participant_id != participant_id:
        raise ValueError("Nonce share belongs to a different participant.")
    if session.commitments.get(participant_id) != nonce_share.commitment:
        raise ValueError("Nonce commitment must be registered before signing.")

    share_value = _private_share_value(private_share, participant_id)
    challenge = session.challenge()
    lambda_i = session.lagrange_coefficient(participant_id)
    value = (nonce_share.nonce + challenge * lambda_i * share_value) % GROUP_ORDER
    return PartialSignature(
        participant_id=participant_id,
        value=value,
        nonce_commitment=nonce_share.commitment,
    )


def verify_partial_signature(
    partial_signature: PartialSignature, session: ThresholdSigningSession
) -> bool:
    """Verify z_i * G == R_i + e * lambda_i * Y_i for a partial signature."""
    try:
        session._require_signing_context()
        if not session.is_complete():
            raise ValueError("Not all nonce commitments have been collected.")
        if partial_signature.participant_id not in session.selected_ids:
            return False
        if not (0 <= partial_signature.value < GROUP_ORDER):
            return False
        if partial_signature.nonce_commitment == INFINITY:
            return False
        if (
            session.commitments.get(partial_signature.participant_id)
            != partial_signature.nonce_commitment
        ):
            return False

        challenge = session.challenge()
        lambda_i = session.lagrange_coefficient(partial_signature.participant_id)
        public_share = public_share_for_index(
            session.aggregated_commitments if session.aggregated_commitments is not None else [],
            partial_signature.participant_id,
        )

        lhs = partial_signature.value * GENERATOR
        rhs = partial_signature.nonce_commitment + (
            (challenge * lambda_i) % GROUP_ORDER
        ) * public_share
        return lhs == rhs
    except ValueError:
        return False


def aggregate_signatures(
    session: ThresholdSigningSession,
    partial_signatures: Sequence[PartialSignature],
) -> SchnorrSignature:
    """Aggregate verified partial signatures into a standard Schnorr signature."""
    return session.aggregate_signature(partial_signatures)


def _private_share_value(private_share: Share | int, participant_id: int) -> int:
    if isinstance(private_share, Share):
        if private_share.x != participant_id:
            raise ValueError("Private share belongs to a different participant.")
        share_value = private_share.y
    else:
        share_value = private_share

    if not (0 <= share_value < GROUP_ORDER):
        raise ValueError("Private share must be in the range [0, n-1].")
    return share_value
