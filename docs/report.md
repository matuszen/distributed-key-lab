# Final Report

## Topic

Distributed Key Generation and threshold Schnorr signatures in a `t-of-n` model.

## Abstract

The project implements a complete educational path from elliptic-curve parameters, through Shamir Secret Sharing and Feldman VSS, to a local DKG simulation and threshold Schnorr signing. The main demonstration scenario is a `3-of-5` wallet: any three participants can sign a message, while two participants are blocked before signing.

## Environment

- Python 3.10+
- `ecdsa`
- `pytest`
- `ruff`
- `isort`
- `SECP256k1`

## Method

1. Cryptographic parameters are validated by `setup_check.py`.
2. The secret is split with a Shamir polynomial over the group order.
3. Share correctness is protected with Feldman commitments.
4. DKG is implemented as local VSS package exchange between `Participant` objects.
5. The joint public key is derived from public contributions.
6. Threshold signing is built from Lagrange-weighted partial signatures.

## Results

- Unit tests cover SSS, VSS, DKG, Schnorr, TSS, GUI services, and examples.
- `threshold_wallet_3of5.py` produces a signature accepted by `verify_signature`.
- `attack_t_minus_one.py` blocks a signing attempt below the threshold.
- The DKG benchmark shows a simple timing trend as the number of participants grows.
- The Tkinter GUI exposes the main demonstrations through forms.

## Limits

The implementation is academic. It is not full FROST and does not include networking, persistent storage, side-channel protection, or production-grade malicious participant handling. Deterministic secrets and nonces appear in tests and demos for reproducibility; default protocol helpers use `secrets`.

## Conclusion

The project meets its educational goal: it shows the mathematical foundation, share verifiability, distributed generation of a joint public key, and a valid threshold signature without reconstructing the full private key during the signing path.
