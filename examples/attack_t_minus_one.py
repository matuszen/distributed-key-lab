"""Negative demo: two participants cannot sign in a 3-of-5 setup."""

from dkglab.protocols.dkg import run_dkg
from dkglab.protocols.threshold_signature import ThresholdSigningSession


def main() -> None:
    dkg_result = run_dkg(
        num_participants=5,
        threshold=3,
        secrets=[11, 22, 33, 44, 55],
    )

    try:
        ThresholdSigningSession(
            selected_ids={1, 2},
            threshold=dkg_result.threshold,
            message=b"attacker tries to sign with only two shares",
            public_key=dkg_result.public_key,
            aggregated_commitments=dkg_result.aggregated_commitments,
        )
    except ValueError as exc:
        print("Attack blocked:", exc)
        return

    raise RuntimeError("Attack was not blocked.")


if __name__ == "__main__":
    main()
