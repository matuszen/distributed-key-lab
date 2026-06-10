import pytest

from dkglab.gui.services import (
    attack_t_minus_one_demo,
    benchmark_dkg,
    curve_summary,
    parse_participant_ids,
    shamir_demo,
    threshold_wallet_demo,
)


def test_curve_summary_contains_sanity_check() -> None:
    result = curve_summary()

    assert result.title == "Curve setup"
    assert "SECP256k1" in result.body
    assert "Sanity check n*G == INFINITY: True" in result.body


def test_shamir_demo_blocks_t_minus_one() -> None:
    result = shamir_demo(secret=12345, threshold=3, num_participants=5)

    assert "Recovered values from all 3-share subsets: [12345]" in result.body
    assert "Recovery with t-1 shares: blocked" in result.body


def test_threshold_wallet_demo_signs_message() -> None:
    result = threshold_wallet_demo(selected_ids=[1, 3, 5], message="hello")

    assert "Selected participants: [1, 3, 5]" in result.body
    assert "Signature valid: True" in result.body
    assert "Partial signatures:" in result.body


def test_threshold_wallet_demo_rejects_unknown_participant() -> None:
    with pytest.raises(ValueError, match="must exist"):
        threshold_wallet_demo(selected_ids=[1, 3, 9], message="hello")


def test_attack_t_minus_one_demo_is_blocked() -> None:
    result = attack_t_minus_one_demo()

    assert "Attack blocked: Not enough selected participants for threshold." in result.body


def test_benchmark_dkg_returns_csv_like_output() -> None:
    result = benchmark_dkg(configs=[(3, 2)])

    assert result.body.splitlines()[0] == "n,t,time_ms"
    assert result.body.splitlines()[1].startswith("3,2,")


def test_parse_participant_ids() -> None:
    assert parse_participant_ids("1, 3,5") == [1, 3, 5]

    with pytest.raises(ValueError, match="unique"):
        parse_participant_ids("1,1,2")
