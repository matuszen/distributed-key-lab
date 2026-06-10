# Verifiable Secret Sharing: Feldman

## Problem

Plain Shamir Secret Sharing assumes an honest dealer. If the dealer sends an invalid share, the receiver has no local way to detect it.

Feldman VSS adds public commitments to the polynomial coefficients:

```text
C_j = a_j * G
```

for every coefficient `a_j`.

## Share Verification

For a share `(i, s_i)`, the participant checks:

```text
s_i * G == C_0 + i*C_1 + i^2*C_2 + ... + i^(t-1)*C_(t-1)
```

If the equality holds, the share matches the dealer's public commitments.

## Implementation

Modules:

- `dkglab.vss.feldman`
- `dkglab.vss.verification`

Functions:

- `build_feldman_commitments(coefficients)`
- `create_vss_package(share, coefficients)`
- `verify_share(share, commitments)`
- `verify_vss_package(package)`

## Limits

Feldman VSS provides verifiability, but it is not a hiding commitment scheme. For this project, secrets are large group scalars, and this limitation is documented as part of the academic threat model.
