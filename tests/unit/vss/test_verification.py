from dkglab.crypto.curves import GROUP_ORDER
from dkglab.utils.types import Share
from dkglab.vss.feldman import build_feldman_commitments
from dkglab.vss.verification import verify_share


def poly_eval(coeffs: list[int], x: int, modulus: int) -> int:
    acc = 0
    power = 1
    for coefficient in coeffs:
        acc = (acc + coefficient * power) % modulus
        power = (power * x) % modulus
    return acc


def test_verify_share_true_for_valid_share() -> None:
    coeffs = [12345, 222, 333]
    commitments = build_feldman_commitments(coeffs)
    idx = 3
    share = Share(x=idx, y=poly_eval(coeffs, idx, GROUP_ORDER))

    assert verify_share(share=share, commitments=commitments)


def test_verify_share_false_for_tampered_share() -> None:
    coeffs = [54321, 111, 999]
    commitments = build_feldman_commitments(coeffs)
    idx = 2
    valid_y = poly_eval(coeffs, idx, GROUP_ORDER)
    tampered = Share(x=idx, y=(valid_y + 1) % GROUP_ORDER)

    assert not verify_share(share=tampered, commitments=commitments)


def test_verify_share_false_for_tampered_commitment() -> None:
    coeffs = [76543, 55, 77]
    commitments = build_feldman_commitments(coeffs)
    idx = 4
    share = Share(x=idx, y=poly_eval(coeffs, idx, GROUP_ORDER))

    commitments[0] = commitments[0] + commitments[1]
    assert not verify_share(share=share, commitments=commitments)
