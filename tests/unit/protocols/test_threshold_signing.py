import pytest
from ecdsa.ellipticcurve import INFINITY

from dkglab.protocols.threshold_signature import (
    NonceCommitment,
    ThresholdSigningSession,
    generate_nonce_commitment,
    select_participants,
)


def test_select_participants_defaults_to_sorted_subset() -> None:
    available = [3, 1, 2, 5]
    selected = select_participants(available, threshold=2)

    assert selected == [1, 2]


def test_select_participants_accepts_explicit_selection() -> None:
    available = [1, 2, 3, 4]
    selected = select_participants(available, threshold=2, selection=[4, 2])

    assert selected == [4, 2]


def test_nonce_commitments_aggregate() -> None:
    selected_ids = {1, 2, 3}
    session = ThresholdSigningSession(selected_ids=selected_ids)

    commitments = []
    for participant_id in sorted(selected_ids):
        nonce_share = generate_nonce_commitment(
            participant_id, nonce=participant_id + 10
        )
        commitments.append(nonce_share.commitment)
        session.add_commitment(
            NonceCommitment(
                participant_id=participant_id, commitment=nonce_share.commitment
            )
        )

    assert session.is_complete()

    expected = INFINITY
    for commitment in commitments:
        expected = expected + commitment

    assert session.aggregate_commitment() == expected


def test_nonce_commitment_rejects_unselected_participant() -> None:
    session = ThresholdSigningSession(selected_ids={1, 2})
    nonce_share = generate_nonce_commitment(participant_id=3, nonce=15)

    with pytest.raises(ValueError, match="not selected"):
        session.add_commitment(
            NonceCommitment(
                participant_id=nonce_share.participant_id,
                commitment=nonce_share.commitment,
            )
        )


def test_nonce_commitment_rejects_duplicate() -> None:
    session = ThresholdSigningSession(selected_ids={1})
    nonce_share = generate_nonce_commitment(participant_id=1, nonce=9)

    session.add_commitment(
        NonceCommitment(participant_id=1, commitment=nonce_share.commitment)
    )

    with pytest.raises(ValueError, match="already received"):
        session.add_commitment(
            NonceCommitment(participant_id=1, commitment=nonce_share.commitment)
        )


def test_nonce_commitment_rejects_infinity() -> None:
    session = ThresholdSigningSession(selected_ids={1})

    with pytest.raises(ValueError, match="infinity"):
        session.add_commitment(NonceCommitment(participant_id=1, commitment=INFINITY))
