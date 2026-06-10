# Requirements Specification

## Project Goal

The project demonstrates an academic implementation of Distributed Key Generation (DKG) and threshold Schnorr signatures for a `t-of-n` setting. The system should show that:

- a secret can be split with Shamir Secret Sharing,
- share correctness can be verified with Feldman VSS,
- participants can derive a joint public key without reconstructing the full private key,
- any valid group of at least `t` participants can produce a signature,
- fewer than `t` participants cannot start a valid signing path.

## Functional Scope

- Python 3.10+ and the `ecdsa` library.
- `SECP256k1` curve parameters.
- Shamir Secret Sharing over the curve group order.
- Feldman VSS commitments on elliptic-curve points.
- Local in-memory DKG simulation.
- Local Schnorr signing and verification.
- Educational threshold Schnorr signing without reconstructing the full private key.
- Console examples, a Tkinter desktop app, automated tests, and Markdown documentation.

## Out of Scope

- Full FROST implementation.
- Networking, transport security, and participant authentication.
- Side-channel protection.
- Persistent private-share storage.
- Production-grade failure handling or slashing for malicious participants.

## Acceptance Criteria

- `python setup_check.py` prints curve parameters and confirms `n*G == INFINITY`.
- `pytest` passes.
- `examples/threshold_wallet_3of5.py` ends with `Signature valid: True`.
- `examples/attack_t_minus_one.py` ends with `Attack blocked`.
- The Markdown documentation explains the security assumptions and implementation limits.
