import pytest
from ecdsa.ellipticcurve import INFINITY

from dkglab.crypto.curves import GENERATOR, GROUP_ORDER
from dkglab.crypto.schnorr import SchnorrSignature, generate_keypair, verify_signature
from dkglab.protocols.dkg import DKGResult, run_dkg
from dkglab.protocols.threshold_signature import (
    NonceCommitment,
    NonceShare,
    PartialSignature,
    ThresholdSigningSession,
    aggregate_signatures,
    create_partial_signature,
    generate_nonce_commitment,
    select_participants,
    verify_partial_signature,
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


def test_threshold_signature_3_of_5_roundtrip() -> None:
    result, session, nonce_shares = build_threshold_session(selected_ids=[1, 2, 3])

    partials = []
    for participant_id in [1, 2, 3]:
        participant = result.participants[participant_id - 1]
        assert participant.final_share is not None
        partial = create_partial_signature(
            participant_id=participant_id,
            private_share=participant.final_share,
            nonce_share=nonce_shares[participant_id],
            session=session,
        )
        assert verify_partial_signature(partial, session)
        partials.append(partial)

    signature = aggregate_signatures(session, partials)

    assert verify_signature(result.public_key, session.message, signature)


def test_threshold_signature_accepts_non_consecutive_signers() -> None:
    result, session, nonce_shares = build_threshold_session(selected_ids=[2, 4, 5])

    partials = []
    for participant_id in [2, 4, 5]:
        participant = result.participants[participant_id - 1]
        assert participant.final_share is not None
        partials.append(
            create_partial_signature(
                participant_id=participant_id,
                private_share=participant.final_share,
                nonce_share=nonce_shares[participant_id],
                session=session,
            )
        )

    signature = aggregate_signatures(session, partials)

    assert verify_signature(result.public_key, session.message, signature)


def test_threshold_signature_rejects_t_minus_one_before_signing() -> None:
    result = run_dkg(num_participants=5, threshold=3, secrets=[11, 22, 33, 44, 55])

    with pytest.raises(ValueError, match="Not enough selected"):
        ThresholdSigningSession(
            selected_ids={1, 2},
            threshold=result.threshold,
            message=b"too few",
            public_key=result.public_key,
            aggregated_commitments=result.aggregated_commitments,
        )


def test_threshold_signature_rejects_tampered_partial_signature() -> None:
    result, session, nonce_shares = build_threshold_session(selected_ids=[1, 2, 3])
    participant = result.participants[0]
    assert participant.final_share is not None

    partial = create_partial_signature(
        participant_id=1,
        private_share=participant.final_share,
        nonce_share=nonce_shares[1],
        session=session,
    )
    tampered = PartialSignature(
        participant_id=partial.participant_id,
        value=(partial.value + 1) % GROUP_ORDER,
        nonce_commitment=partial.nonce_commitment,
    )

    assert not verify_partial_signature(tampered, session)
    with pytest.raises(ValueError, match="failed verification"):
        session.add_partial_signature(tampered)


def test_threshold_signature_final_signature_is_bound_to_message_r_and_pk() -> None:
    result, session, nonce_shares = build_threshold_session(selected_ids=[1, 2, 3])
    partials = []
    for participant_id in [1, 2, 3]:
        participant = result.participants[participant_id - 1]
        assert participant.final_share is not None
        partials.append(
            create_partial_signature(
                participant_id=participant_id,
                private_share=participant.final_share,
                nonce_share=nonce_shares[participant_id],
                session=session,
            )
        )

    signature = aggregate_signatures(session, partials)
    wrong_public_key = generate_keypair().public_key
    wrong_R = SchnorrSignature(R=signature.R + GENERATOR, s=signature.s)

    assert not verify_signature(result.public_key, b"other message", signature)
    assert not verify_signature(wrong_public_key, session.message, signature)
    assert not verify_signature(result.public_key, session.message, wrong_R)


def build_threshold_session(
    selected_ids: list[int],
) -> tuple[DKGResult, ThresholdSigningSession, dict[int, NonceShare]]:
    result = run_dkg(num_participants=5, threshold=3, secrets=[11, 22, 33, 44, 55])
    session = ThresholdSigningSession(
        selected_ids=set(selected_ids),
        threshold=result.threshold,
        message=b"threshold schnorr message",
        public_key=result.public_key,
        aggregated_commitments=result.aggregated_commitments,
    )

    nonce_shares = {}
    for participant_id in selected_ids:
        nonce_share = generate_nonce_commitment(
            participant_id=participant_id,
            nonce=participant_id + 100,
        )
        nonce_shares[participant_id] = nonce_share
        session.add_commitment(
            NonceCommitment(
                participant_id=participant_id,
                commitment=nonce_share.commitment,
            )
        )

    return result, session, nonce_shares
