# Distributed Key Lab

## Target Functionality

The project targets a complete pipeline for:

- distributed key generation (DKG), where no single party holds the full private key,
- threshold signatures, where any t-of-n participants can jointly produce a valid signature.

Core cryptographic components include:

- Shamir Secret Sharing for secret splitting and recovery,
- Verifiable Secret Sharing (Feldman) for share correctness checks,
- Schnorr-style signing flow for local and threshold signature verification.

## Project Structure

The repository uses a domain-oriented layout:

- src/dkglab/crypto: elliptic-curve parameters and crypto primitives
- src/dkglab/secret_sharing: Shamir interpolation and secret recovery
- src/dkglab/vss: Feldman commitments and share verification
- src/dkglab/protocols: orchestration layer for DKG and threshold signing
- tests/unit: unit tests grouped by domain
- docs: setup and domain documentation

## Run

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e .[dev]
```

3. Validate the curve setup (secp256k1):

```bash
python3 setup_check.py
```

4. Run tests:

```bash
pytest
```
