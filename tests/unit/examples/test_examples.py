import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def run_example(script_name: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    return subprocess.run(  # noqa: S603
        [sys.executable, str(REPO_ROOT / "examples" / script_name)],
        capture_output=True,
        check=True,
        env=env,
        text=True,
    )


def test_threshold_wallet_example_smoke() -> None:
    result = run_example("threshold_wallet_3of5.py")

    assert "Use case: threshold wallet 3-of-5" in result.stdout
    assert "Signature valid: True" in result.stdout


def test_attack_t_minus_one_example_smoke() -> None:
    result = run_example("attack_t_minus_one.py")

    assert "Attack blocked: Not enough selected participants for threshold." in result.stdout
