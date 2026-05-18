from dkglab.crypto.curves import GROUP_ORDER
from dkglab.protocols.dkg import run_dkg
from dkglab.protocols.participant import Participant
from dkglab.secret_sharing.recovery import recover_secret
from dkglab.utils.types import Share, VSSPackage
from dkglab.vss.verification import verify_share


def test_dkg_round_aggregates_consistently() -> None:
    secrets = [11, 22, 33, 44, 55]
    result = run_dkg(num_participants=5, threshold=3, secrets=secrets)

    aggregated_secret = sum(secrets) % GROUP_ORDER

    commitments_list = []
    for participant in result.participants:
        assert participant.commitments is not None
        commitments_list.append(participant.commitments)

    for participant in result.participants:
        assert participant.final_share is not None
        assert verify_share(participant.final_share, result.aggregated_commitments)
        assert (
            participant.compute_joint_public_key(commitments_list) == result.public_key
        )

    final_shares = [
        participant.final_share
        for participant in result.participants
        if participant.final_share
    ]
    recovered = recover_secret(final_shares[:3], threshold=3)

    assert recovered == aggregated_secret
    assert result.public_key == result.aggregated_commitments[0]


def test_receive_share_rejects_invalid_package() -> None:
    participants = [Participant(1, 2, 2), Participant(2, 2, 2)]
    packages = participants[0].generate_and_broadcast_shares(secret=123)

    valid_package = packages[2]
    tampered_share = Share(
        x=valid_package.share.x, y=(valid_package.share.y + 1) % GROUP_ORDER
    )
    tampered_package = VSSPackage(
        share=tampered_share, commitments=valid_package.commitments
    )

    assert participants[1].receive_share(tampered_package, from_id=1) is False
    assert 1 not in participants[1].received_shares
