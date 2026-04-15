import pytest
from dkglab.secret_sharing.splitting import create_shares
from dkglab.crypto.curves import GROUP_ORDER

def test_create_shares_basic():
    """Verify that the correct number of shares is generated with expected attributes."""
    secret = 12345
    threshold, num_participants = 3, 5
    shares = create_shares(secret, threshold, num_participants)
    
    assert len(shares) == num_participants
    # Ensure each share object has the required coordinates
    assert all(hasattr(s, 'x') and hasattr(s, 'y') for s in shares)

def test_create_shares_unique_indices():
    """Ensure that each participant receives a unique x-coordinate (index)."""
    shares = create_shares(500, 2, 4)
    xs = [s.x for s in shares]
    assert len(set(xs)) == len(xs), "Share indices must be unique across all participants"

def test_create_shares_invalid_params():
    """Ensure the system raises an error if the threshold exceeds the number of participants."""
    with pytest.raises(ValueError, match="Threshold cannot be greater than number of participants."):
        # t=5, n=3 is an invalid configuration for Shamir's Secret Sharing
        create_shares(100, 5, 3)