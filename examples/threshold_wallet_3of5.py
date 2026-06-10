"""Demo use case: a 3-of-5 threshold wallet signs one message."""

from dkglab.crypto.schnorr import point_to_hex, scalar_to_hex, verify_signature
from dkglab.protocols.dkg import run_dkg
from dkglab.protocols.threshold_signature import (
    NonceCommitment,
    ThresholdSigningSession,
    aggregate_signatures,
    create_partial_signature,
    generate_nonce_commitment,
)


def main() -> None:
    message = b"wallet: transfer 10 lab-coins to student-team"
    selected_ids = [1, 3, 5]
    dkg_result = run_dkg(
        num_participants=5,
        threshold=3,
        secrets=[11, 22, 33, 44, 55],
    )

    session = ThresholdSigningSession(
        selected_ids=set(selected_ids),
        threshold=dkg_result.threshold,
        message=message,
        public_key=dkg_result.public_key,
        aggregated_commitments=dkg_result.aggregated_commitments,
    )

    nonce_shares = {}
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
    is_valid = verify_signature(dkg_result.public_key, message, signature)

    print("Use case: threshold wallet 3-of-5")
    print("Message:", message.decode("utf-8"))
    print("Selected participants:", selected_ids)
    print("Joint public key PK:", point_to_hex(dkg_result.public_key))
    print("Aggregated nonce R:", point_to_hex(signature.R))
    print("Signature scalar s:", scalar_to_hex(signature.s))
    print("Signature valid:", is_valid)


if __name__ == "__main__":
    main()
