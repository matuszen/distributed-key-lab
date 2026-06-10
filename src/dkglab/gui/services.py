"""Testable service functions used by the desktop GUI."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from time import perf_counter
from typing import Callable

from ecdsa.ellipticcurve import INFINITY

from dkglab.crypto.curves import CURVE, GENERATOR, GROUP_ORDER
from dkglab.crypto.schnorr import (
    SchnorrSignature,
    point_to_hex,
    scalar_to_hex,
    verify_signature,
)
from dkglab.protocols.dkg import DKGResult, public_share_for_index, run_dkg
from dkglab.protocols.threshold_signature import (
    NonceCommitment,
    NonceShare,
    PartialSignature,
    ThresholdSigningSession,
    aggregate_signatures,
    create_partial_signature,
    generate_nonce_commitment,
)
from dkglab.secret_sharing.recovery import recover_secret
from dkglab.secret_sharing.splitting import create_shares
from dkglab.vss.verification import verify_share

DEFAULT_DKG_SECRETS = [11, 22, 33, 44, 55]
DEFAULT_MESSAGE = "Hello world!"


@dataclass(frozen=True)
class TextResult:
    title: str
    body: str


def curve_summary() -> TextResult:
    """Return the same curve sanity information shown by setup_check.py."""
    body = "\n".join(
        [
            f"Curve: {CURVE.name}",
            f"Generator G.x: {hex(GENERATOR.x())}",
            f"Generator G.y: {hex(GENERATOR.y())}",
            f"Group order n: {hex(GROUP_ORDER)}",
            f"Sanity check n*G == INFINITY: {GROUP_ORDER * GENERATOR == INFINITY}",
        ]
    )
    return TextResult(title="Curve setup", body=body)


def shamir_demo(secret: int, threshold: int, num_participants: int) -> TextResult:
    """Split a secret and show recovery from every threshold-sized subset."""
    shares = create_shares(secret, threshold, num_participants)
    recovered_values = []
    for selected in combinations(shares, threshold):
        recovered_values.append(recover_secret(list(selected), threshold))

    unique_recovered = sorted(set(recovered_values))
    t_minus_one_message = _expect_error(
        lambda: recover_secret(shares[: threshold - 1], threshold),
    )

    share_lines = [f"P{share.x}: {share.y}" for share in shares]
    body = "\n".join(
        [
            f"Secret: {secret}",
            f"Threshold: {threshold}",
            f"Participants: {num_participants}",
            "",
            "Shares:",
            *share_lines,
            "",
            f"Recovered values from all {threshold}-share subsets: {unique_recovered}",
            f"Recovery with t-1 shares: blocked ({t_minus_one_message})",
        ]
    )
    return TextResult(title="Shamir Secret Sharing", body=body)


def dkg_demo(num_participants: int, threshold: int) -> TextResult:
    """Run a DKG round and show public verification of each final share."""
    result = _run_demo_dkg(num_participants, threshold)
    lines = [
        f"Participants: {result.num_participants}",
        f"Threshold: {result.threshold}",
        f"Joint public key PK: {point_to_hex(result.public_key)}",
        f"Commitment transcript entries: {len(result.commitment_transcript)}",
        "",
        "Final share checks:",
    ]

    for participant in result.participants:
        if participant.final_share is None:
            raise RuntimeError("DKG participant has no final share.")
        public_share = public_share_for_index(
            result.aggregated_commitments,
            participant.id,
        )
        lines.append(
            f"P{participant.id}: VSS={verify_share(participant.final_share, result.aggregated_commitments)}; "
            f"public_share={point_to_hex(public_share)}"
        )

    return TextResult(title="Distributed Key Generation", body="\n".join(lines))


def threshold_wallet_demo(
    selected_ids: list[int],
    message: str = DEFAULT_MESSAGE,
    num_participants: int = 5,
    threshold: int = 3,
) -> TextResult:
    """Run DKG and threshold-sign one message with the selected participants."""
    dkg_result = _run_demo_dkg(num_participants, threshold)
    partials, signature, session = _sign_with_selected_participants(
        dkg_result=dkg_result,
        selected_ids=selected_ids,
        message=message.encode("utf-8"),
    )

    partial_lines = [
        f"P{partial.participant_id}: z_i={scalar_to_hex(partial.value)}"
        for partial in partials
    ]
    is_valid = verify_signature(dkg_result.public_key, session.message, signature)
    body = "\n".join(
        [
            "Use case: threshold wallet 3-of-5",
            f"Message: {message}",
            f"Selected participants: {selected_ids}",
            f"Joint public key PK: {point_to_hex(dkg_result.public_key)}",
            f"Aggregated nonce R: {point_to_hex(signature.R)}",
            f"Signature scalar s: {scalar_to_hex(signature.s)}",
            f"Signature valid: {is_valid}",
            "",
            "Partial signatures:",
            *partial_lines,
        ]
    )
    return TextResult(title="Threshold wallet", body=body)


def attack_t_minus_one_demo(
    num_participants: int = 5,
    threshold: int = 3,
) -> TextResult:
    """Show that fewer than threshold participants cannot start a signing session."""
    dkg_result = _run_demo_dkg(num_participants, threshold)
    selected_ids = set(range(1, threshold))
    blocked_message = _expect_error(
        lambda: ThresholdSigningSession(
            selected_ids=selected_ids,
            threshold=dkg_result.threshold,
            message=b"attacker tries to sign with too few shares",
            public_key=dkg_result.public_key,
            aggregated_commitments=dkg_result.aggregated_commitments,
        )
    )
    body = "\n".join(
        [
            f"Attempted signer set: {sorted(selected_ids)}",
            f"Required threshold: {threshold}",
            f"Attack blocked: {blocked_message}",
        ]
    )
    return TextResult(title="t-1 attack simulation", body=body)


def benchmark_dkg(configs: list[tuple[int, int]] | None = None) -> TextResult:
    """Run a small DKG timing demo."""
    configs = configs or [(3, 2), (5, 3), (7, 4), (10, 6)]
    lines = ["n,t,time_ms"]
    for num_participants, threshold in configs:
        start = perf_counter()
        run_dkg(num_participants=num_participants, threshold=threshold)
        elapsed_ms = (perf_counter() - start) * 1000
        lines.append(f"{num_participants},{threshold},{elapsed_ms:.3f}")
    return TextResult(title="DKG benchmark", body="\n".join(lines))


def parse_participant_ids(value: str) -> list[int]:
    """Parse comma-separated participant ids, preserving the user's order."""
    if not value.strip():
        raise ValueError("Participant list cannot be empty.")
    parsed = [int(part.strip()) for part in value.split(",") if part.strip()]
    if len(set(parsed)) != len(parsed):
        raise ValueError("Participant ids must be unique.")
    if any(participant_id <= 0 for participant_id in parsed):
        raise ValueError("Participant ids must be positive.")
    return parsed


def _run_demo_dkg(num_participants: int, threshold: int) -> DKGResult:
    if num_participants == 5 and threshold == 3:
        return run_dkg(
            num_participants=num_participants,
            threshold=threshold,
            secrets=DEFAULT_DKG_SECRETS,
        )
    return run_dkg(num_participants=num_participants, threshold=threshold)


def _sign_with_selected_participants(
    dkg_result: DKGResult,
    selected_ids: list[int],
    message: bytes,
) -> tuple[list[PartialSignature], SchnorrSignature, ThresholdSigningSession]:
    if any(
        participant_id > dkg_result.num_participants for participant_id in selected_ids
    ):
        raise ValueError("Selected participants must exist in the DKG result.")

    session = ThresholdSigningSession(
        selected_ids=set(selected_ids),
        threshold=dkg_result.threshold,
        message=message,
        public_key=dkg_result.public_key,
        aggregated_commitments=dkg_result.aggregated_commitments,
    )

    nonce_shares: dict[int, NonceShare] = {}
    for participant_id in selected_ids:
        nonce_share = generate_nonce_commitment(
            participant_id=participant_id,
            nonce=100 + participant_id,
        )
        nonce_shares[participant_id] = nonce_share
        session.add_commitment(
            NonceCommitment(
                participant_id=participant_id,
                commitment=nonce_share.commitment,
            )
        )

    partials = []
    for participant_id in selected_ids:
        participant = dkg_result.participants[participant_id - 1]
        if participant.final_share is None:
            raise RuntimeError("DKG participant has no final share.")
        partials.append(
            create_partial_signature(
                participant_id=participant_id,
                private_share=participant.final_share,
                nonce_share=nonce_shares[participant_id],
                session=session,
            )
        )

    signature = aggregate_signatures(session, partials)
    return partials, signature, session


def _expect_error(action: Callable[[], object]) -> str:
    try:
        action()
    except ValueError as exc:
        return str(exc)
    raise RuntimeError("Expected action to fail.")
