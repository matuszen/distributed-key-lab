"""Participant abstraction for local DKG simulations."""

from __future__ import annotations

import logging
from typing import Dict, List, Sequence

from ecdsa.ellipticcurve import INFINITY, Point

from dkglab.crypto.curves import GROUP_ORDER
from dkglab.secret_sharing.splitting import (
    create_shares_from_coefficients,
    generate_coefficients,
)
from dkglab.utils.types import Share, VSSPackage
from dkglab.vss.feldman import build_feldman_commitments
from dkglab.vss.verification import verify_share

logger = logging.getLogger(__name__)


class Participant:
    """Represents a DKG participant with local, in-memory state."""

    def __init__(
        self, participant_id: int, num_participants: int, threshold: int
    ) -> None:
        if participant_id <= 0:
            raise ValueError("Participant id must be positive.")
        if num_participants <= 0:
            raise ValueError("Number of participants must be positive.")
        if threshold <= 0:
            raise ValueError("Threshold must be greater than zero.")
        if threshold > num_participants:
            raise ValueError("Threshold cannot exceed number of participants.")

        self.id = participant_id
        self.n = num_participants
        self.t = threshold

        self.coefficients: List[int] | None = None
        self.commitments: List[Point] | None = None
        self.own_share: Share | None = None

        self.outgoing: Dict[int, VSSPackage] = {}
        self.received_shares: Dict[int, Share] = {}
        self.final_share: Share | None = None

    def generate_and_broadcast_shares(self, secret: int) -> Dict[int, VSSPackage]:
        """Generate a polynomial, commitments, and per-recipient VSS packages."""
        coefficients = generate_coefficients(
            secret=secret, threshold=self.t, modulus=GROUP_ORDER
        )
        commitments = build_feldman_commitments(coefficients)
        shares = create_shares_from_coefficients(
            coefficients, self.n, modulus=GROUP_ORDER
        )

        packages: Dict[int, VSSPackage] = {}
        for share in shares:
            packages[share.x] = VSSPackage(share=share, commitments=commitments)
            if share.x == self.id:
                self.own_share = share

        self.coefficients = coefficients
        self.commitments = commitments
        self.outgoing = packages

        logger.info("Participant %s generated shares", self.id)
        return packages

    def receive_share(self, package: VSSPackage, from_id: int) -> bool:
        """Verify and store a share sent by another participant."""
        if package.share.x != self.id:
            logger.warning(
                "Participant %s received misrouted share for %s from %s",
                self.id,
                package.share.x,
                from_id,
            )
            return False

        try:
            is_valid = verify_share(
                share=package.share, commitments=package.commitments
            )
        except ValueError:
            is_valid = False

        if is_valid:
            self.received_shares[from_id] = package.share
            logger.info("Participant %s accepted share from %s", self.id, from_id)
            return True

        logger.warning("Participant %s rejected share from %s", self.id, from_id)
        return False

    def aggregate_final_share(self) -> Share:
        """Aggregate all verified shares into the final private share."""
        if self.own_share is None:
            raise ValueError("Own share is missing; generate shares first.")
        if len(self.received_shares) < self.n - 1:
            raise ValueError("Not all shares have been received.")

        total = self.own_share.y
        for share in self.received_shares.values():
            total = (total + share.y) % GROUP_ORDER

        self.final_share = Share(x=self.id, y=total)
        logger.info("Participant %s aggregated final share", self.id)
        return self.final_share

    def compute_partial_public_key(self) -> Point:
        """Return the public contribution corresponding to the secret term."""
        if not self.commitments:
            raise ValueError("Commitments not available.")
        return self.commitments[0]

    @staticmethod
    def aggregate_public_key(commitments_list: Sequence[Sequence[Point]]) -> Point:
        """Aggregate commitment-0 points into a joint public key."""
        if not commitments_list:
            raise ValueError("Commitments list cannot be empty.")

        acc: Point = INFINITY
        for commitments in commitments_list:
            if not commitments:
                raise ValueError("Commitments list cannot be empty.")
            acc = acc + commitments[0]
        return acc
