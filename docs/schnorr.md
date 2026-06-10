# Schnorr Signature

## Local Algorithm

For private key `x`, public key `PK = x*G`, and message `m`:

```text
R = k * G
e = H(R, PK, m)
s = k + e*x mod n
signature = (R, s)
```

Verification:

```text
s * G == R + e * PK
```

## Implementation

Module:

- `dkglab.crypto.schnorr`

Functions:

- `generate_keypair()`
- `sign_message(private_key, message)`
- `verify_signature(public_key, message, signature)`
- `compute_challenge(R, public_key, message)`
- `point_to_hex(point)`
- `scalar_to_hex(value)`

## Notes

`compute_challenge` is public because threshold signing must use exactly the same challenge `e` as the final Schnorr verifier.
