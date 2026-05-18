"""DKG protocol orchestration helpers."""

from __future__ import annotations

import logging
import secrets as secrets_module
from dataclasses import dataclass
from typing import List, Sequence

from ecdsa.ellipticcurve import INFINITY, Point

from dkglab.crypto.curves import GROUP_ORDER
from dkglab.protocols.participant import Participant

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DKGResult:
    participants: List[Participant]
    aggregated_commitments: List[Point]
    public_key: Point


def aggregate_commitments(commitments_list: Sequence[Sequence[Point]]) -> List[Point]:
    if not commitments_list:
        raise ValueError("Commitments list cannot be empty.")
    length = len(commitments_list[0])
    if length == 0:
        raise ValueError("Commitments list cannot be empty.")

    for commitments in commitments_list:
        if len(commitments) != length:
            raise ValueError("Commitments must have equal length.")

    aggregated: List[Point] = []
    for idx in range(length):
        acc: Point = INFINITY
        for commitments in commitments_list:
            acc = acc + commitments[idx]
        aggregated.append(acc)
    return aggregated


def run_dkg(
    num_participants: int, threshold: int, secrets: Sequence[int] | None = None
) -> DKGResult:
    """Run a single, in-memory DKG round for testing and demos."""
    if num_participants <= 0:
        raise ValueError("Number of participants must be positive.")
    if threshold <= 0:
        raise ValueError("Threshold must be greater than zero.")
    if threshold > num_participants:
        raise ValueError("Threshold cannot exceed number of participants.")
    if secrets is not None and len(secrets) != num_participants:
        raise ValueError("Secrets list must match number of participants.")

    participants = [
        Participant(i + 1, num_participants, threshold) for i in range(num_participants)
    ]

    for idx, participant in enumerate(participants):
        secret = (
            secrets[idx]
            if secrets is not None
            else secrets_module.randbelow(GROUP_ORDER)
        )
        participant.generate_and_broadcast_shares(secret)

    for sender in participants:
        for recipient_id, package in sender.outgoing.items():
            if recipient_id == sender.id:
                continue
            recipient = participants[recipient_id - 1]
            accepted = recipient.receive_share(package, from_id=sender.id)
            if not accepted:
                raise ValueError(
                    f"Share from {sender.id} to {recipient_id} failed verification."
                )

    for participant in participants:
        participant.aggregate_final_share()

    commitments_list: List[List[Point]] = []
    for participant in participants:
        if participant.commitments is None:
            raise ValueError("Commitments missing for a participant.")
        commitments_list.append(participant.commitments)

    aggregated_commitments = aggregate_commitments(commitments_list)
    public_key = Participant.aggregate_public_key(commitments_list)

    logger.info("DKG completed for %s participants", num_participants)
    return DKGResult(
        participants=participants,
        aggregated_commitments=aggregated_commitments,
        public_key=public_key,
    )
