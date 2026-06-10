# Distributed Key Lab

Academic Python lab for distributed key generation and threshold Schnorr signatures.

The project demonstrates a complete educational `t-of-n` flow:

- Shamir Secret Sharing,
- Feldman Verifiable Secret Sharing,
- in-memory distributed key generation,
- local Schnorr signatures,
- threshold Schnorr signing without reconstructing the full private key.

It is suitable for learning and tests. It is not a production FROST implementation.

## Project Status

Implemented:

- curve setup check for `SECP256k1`,
- Shamir Secret Sharing split and recovery,
- Feldman verifiable commitments and share verification,
- distributed key generation participant simulation,
- joint public key generation,
- local Schnorr sign and verify,
- threshold Schnorr partial signatures and aggregation,
- positive and negative security scenarios,
- Tkinter desktop application for the distributed key generation and threshold-signature workflow,
- example scripts and Markdown documentation.

## Project Structure

- `src/dkglab/crypto`: elliptic-curve parameters and Schnorr primitives
- `src/dkglab/secret_sharing`: Shamir splitting and Lagrange recovery
- `src/dkglab/vss`: Feldman commitments and verification
- `src/dkglab/protocols`: distributed key generation and threshold signing orchestration
- `examples`: runnable demo and attack scenarios
- `src/dkglab/gui`: desktop application and GUI service layer
- `tests/unit`: unit and smoke tests
- `docs`: documentation, use cases and report

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e .[dev]
```

Validate the curve setup:

```bash
python setup_check.py
```

Run tests and checks:

```bash
pytest -q
ruff check .
isort . --check-only --diff
```

## Demos

Distributed key generation round:

```bash
python examples/dkg_demo.py
```

Threshold wallet `3-of-5`:

```bash
python examples/threshold_wallet_3of5.py
```

Expected final line:

```text
Signature valid: True
```

Attack with too few participants:

```bash
python examples/attack_t_minus_one.py
```

Expected output:

```text
Attack blocked: Not enough selected participants for threshold.
```

Simple distributed key generation benchmark:

```bash
python examples/benchmark_dkg.py
```

Desktop GUI:

```bash
python examples/gui_app.py
```

or, after reinstalling the editable package so the script entry point is refreshed:

```bash
dkglab-gui
```

The GUI uses standard `tkinter` and exposes the main distributed key generation and threshold-signature workflow. On some Linux installations you may need the system package `python3-tk`.

## Documentation

- [Requirements](docs/requirements.md)
- [Setup](docs/setup.md)
- [Shamir Secret Sharing](docs/sss.md)
- [Feldman Verifiable Secret Sharing](docs/vss-feldman.md)
- [Distributed Key Generation](docs/dkg.md)
- [Schnorr](docs/schnorr.md)
- [Threshold Signing](docs/threshold-signing.md)
- [Use Cases](docs/use-cases.md)
- [Desktop GUI](docs/gui.md)
- [Security Tests](docs/security-tests.md)
- [Final Report](docs/report.md)

## Security Notes

This project is a local educational simulation. It does not implement networking, persistent key storage, side-channel protections, or the full FROST protocol. Deterministic secrets and nonces appear in tests and demos for reproducibility; default protocol helpers use `secrets` where random values are needed.
