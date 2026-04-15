from dkglab.crypto.curves import GROUP_ORDER
from dkglab.utils.types import Share
from dkglab.vss.feldman import build_feldman_commitments, create_vss_package
from dkglab.vss.verification import verify_share, verify_vss_package


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

def test_verify_vss_package_true_for_valid_data() -> None:
    """Tests the full flow using VSSPackage with valid data."""
    coeffs = [100, 200, 300]
    idx = 5
    
    # 1. Create a valid share
    y_val = poly_eval(coeffs, idx, GROUP_ORDER)
    share = Share(x=idx, y=y_val)
    
    # 2. Create the VSSPackage using your new function
    package = create_vss_package(share, coeffs)
    
    # 3. Verify using your new wrapper
    assert verify_vss_package(package) is True


def test_verify_vss_package_false_for_wrong_share() -> None:
    """Tests if verify_vss_package correctly rejects a tampered share."""
    coeffs = [10, 20, 30]
    idx = 1
    
    # 1. Create a valid share and package
    y_val = poly_eval(coeffs, idx, GROUP_ORDER)
    share = Share(x=idx, y=y_val)
    package = create_vss_package(share, coeffs)
    
    # 2. Tamper with the share inside the package
    # We create a new package with a corrupted share value
    corrupted_share = Share(x=idx, y=y_val + 1)
    bad_package = create_vss_package(corrupted_share, coeffs)
    
    # 3. Verification should fail
    assert verify_vss_package(bad_package) is False


