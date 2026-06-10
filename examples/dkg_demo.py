"""Demo of one in-memory DKG round for five participants."""

from dkglab.crypto.schnorr import point_to_hex
from dkglab.protocols.dkg import public_share_for_index, run_dkg
from dkglab.vss.verification import verify_share


def main() -> None:
    dkg_result = run_dkg(
        num_participants=5,
        threshold=3,
        secrets=[11, 22, 33, 44, 55],
    )

    print("DKG demo: 3-of-5")
    print("Participants:", dkg_result.num_participants)
    print("Threshold:", dkg_result.threshold)
    print("Joint public key PK:", point_to_hex(dkg_result.public_key))
    print("Commitment transcript entries:", len(dkg_result.commitment_transcript))

    for participant in dkg_result.participants:
        if participant.final_share is None:
            raise RuntimeError("DKG participant has no final share.")
        public_share = public_share_for_index(
            dkg_result.aggregated_commitments,
            participant.id,
        )
        print(
            f"P{participant.id}: final share verified = "
            f"{verify_share(participant.final_share, dkg_result.aggregated_commitments)}, "
            f"public share = {point_to_hex(public_share)}"
        )


if __name__ == "__main__":
    main()
