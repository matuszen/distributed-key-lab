# Presentation Outline

## Slide 1: Project Goal

- DKG and `t-of-n` threshold signing.
- Example: shared `3-of-5` wallet.
- The full private key is never held by one participant.

## Slide 2: Cryptographic Parameters

- Python and `ecdsa`.
- `SECP256k1` curve.
- Base point `G` and group order `n`.
- `setup_check.py`.

## Slide 3: Shamir Secret Sharing

- Secret as `f(0)`.
- Shares as polynomial points.
- Reconstruction with Lagrange interpolation.

## Slide 4: Feldman VSS

- Commitments `C_j = a_j*G`.
- Verification through `s_i*G`.
- Protection against a dishonest dealer.

## Slide 5: DKG

- Each participant is a dealer for its own secret.
- Shares are verified and summed.
- Joint `PK` is derived from public commitments.

## Slide 6: Schnorr

- `R = kG`.
- `e = H(R, PK, m)`.
- `s = k + eSK`.
- Standard verification equation.

## Slide 7: Threshold Signing

- Each signer holds only `sk_i`.
- Each signer creates a partial signature `z_i`.
- Partial signatures aggregate into one `(R, s)` signature.

## Slide 8: Test Scenarios

- Valid `3-of-5`.
- Invalid `2-of-5`.
- Modified VSS share.
- Modified partial signature.

## Slide 9: Demo

- `python examples/dkg_demo.py`
- `python examples/threshold_wallet_3of5.py`
- `python examples/attack_t_minus_one.py`
- `python examples/gui_app.py`

## Slide 10: Limits and Conclusion

- Academic implementation, not production FROST.
- No networking or persistent storage.
- The mathematical and demonstration goals are met.
