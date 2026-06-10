import pytest

from dkglab.secret_sharing.splitting import create_shares, generate_coefficients


def test_create_shares_basic() -> None:
    """Verify that the correct number of shares is generated with expected attributes."""
    secret = 12345
    threshold, num_participants = 3, 5
    shares = create_shares(secret, threshold, num_participants)

    assert len(shares) == num_participants
    assert all(hasattr(share, "x") and hasattr(share, "y") for share in shares)


def test_create_shares_unique_indices() -> None:
    """Ensure that each participant receives a unique x-coordinate (index)."""
    shares = create_shares(500, 2, 4)
    xs = [share.x for share in shares]
    assert len(set(xs)) == len(
        xs
    ), "Share indices must be unique across all participants"


def test_create_shares_invalid_params() -> None:
    """Ensure the system raises an error if the threshold exceeds the number of participants."""
    with pytest.raises(
        ValueError, match="Threshold cannot be greater than number of participants."
    ):
        create_shares(100, 5, 3)


def test_generate_coefficients_keeps_expected_polynomial_degree() -> None:
    coefficients = generate_coefficients(secret=123, threshold=3)

    assert len(coefficients) == 3
    assert coefficients[-1] != 0


def test_generate_coefficients_rejects_zero_secret() -> None:
    with pytest.raises(ValueError, match="Secret must be"):
        generate_coefficients(secret=0, threshold=3)
