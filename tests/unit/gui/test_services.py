import pytest

from dkglab.gui.services import (
    attack_t_minus_one_demo,
    benchmark_dkg,
    curve_summary,
    parse_participant_ids,
    shamir_demo,
    threshold_wallet_demo,
    workflow_attack_summary,
    workflow_dkg_summary,
    workflow_signature_summary,
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


def test_workflow_dkg_summary_is_project_focused() -> None:
    result = workflow_dkg_summary()
    pk_line = next(line for line in result.body.splitlines() if line.startswith("Wspolny klucz publiczny: "))

    assert result.title == "Rozproszona generacja klucza - wspolny klucz publiczny"
    assert "ETAP 1 - Rozproszona generacja klucza" in result.body
    assert "Model: 3 z 5" in result.body
    assert "Wspolny klucz publiczny:" in result.body
    assert "Wspolny klucz publiczny PK:" not in result.body
    assert "SK" not in result.body
    assert len(pk_line.removeprefix("Wspolny klucz publiczny: ")) == 130
    assert "..." not in result.body


def test_workflow_signature_summary_signs_with_three_participants() -> None:
    result = workflow_signature_summary(selected_ids=[1, 3, 5], message="hello")
    pk_line = next(line for line in result.body.splitlines() if line.startswith("Wspolny klucz publiczny: "))
    nonce_line = next(line for line in result.body.splitlines() if line.startswith("Wspolny punkt losowy podpisu: "))
    scalar_line = next(line for line in result.body.splitlines() if line.startswith("Skalar podpisu: "))

    assert result.title == "Podpis progowy - podpis 3 z 5"
    assert "Podpisujacy: [1, 3, 5]" in result.body
    assert "Finalny podpis przechodzi standardowa weryfikacje Schnorra: True" in result.body
    assert "Wspolny klucz publiczny: 04" in result.body
    assert "Wspolny punkt losowy podpisu: 04" in result.body
    assert "PK:" not in result.body
    assert "R:" not in result.body
    assert "s:" not in result.body
    assert "SK" not in result.body
    assert "TSS" not in result.title
    assert len(pk_line.removeprefix("Wspolny klucz publiczny: ")) == 130
    assert len(nonce_line.removeprefix("Wspolny punkt losowy podpisu: ")) == 130
    assert len(scalar_line.removeprefix("Skalar podpisu: ")) == 64
    assert "..." not in result.body


def test_workflow_signature_summary_requires_exactly_three_signers() -> None:
    with pytest.raises(ValueError, match="exactly 3"):
        workflow_signature_summary(selected_ids=[1, 2], message="hello")


def test_workflow_attack_summary_explains_t_minus_one_block() -> None:
    result = workflow_attack_summary()

    assert result.title == "Test progu - zablokowany"
    assert "Proba podpisu przez: [1, 2]" in result.body
    assert "Wynik: atak zablokowany" in result.body
    assert "t-1" not in result.title


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
