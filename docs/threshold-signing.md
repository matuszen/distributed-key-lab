# Threshold Schnorr Signing

## Goal

After DKG, each participant holds only its private share `sk_i`. The project implements a signing path where selected participants jointly create a Schnorr signature without reconstructing the full private key `SK`.

## Flow for Selected Participants

### The coordinator selects at least `t` participants

### Each selected participant generates a nonce `k_i` and publishes `R_i = k_i*G`

### The session aggregates nonce commitments

```text
R = R_1 + R_2 + ... + R_t
```

### Everyone computes the challenge

```text
e = H(R, PK, m)
```

### Each participant computes its Lagrange coefficient `lambda_i` for the signing set

### The partial signature is

```text
z_i = k_i + e * lambda_i * sk_i mod n
```

### The aggregator verifies each partial signature

```text
z_i*G == R_i + e*lambda_i*Y_i
```

where `Y_i = F(i)G` comes from the public DKG commitments.

### The final signature is

```text
s = sum(z_i) mod n
signature = (R, s)
```

The standard Schnorr verifier is used for the final check:

```text
verify_signature(PK, message, signature)
```

## Implementation

Module:

- `dkglab.protocols.threshold_signature`

Elements:

- `ThresholdSigningSession`
- `NonceShare`
- `NonceCommitment`
- `PartialSignature`
- `create_partial_signature`
- `verify_partial_signature`
- `aggregate_signatures`

## Security Limits

This is an educational threshold protocol, not full FROST. The project does not implement production binding factors, nonce-reuse protection, or network-level malicious participant handling. These limits are explicit so the implementation is not presented as a production wallet protocol.
