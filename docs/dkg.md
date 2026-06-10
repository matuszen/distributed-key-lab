# Distributed Key Generation

## Goal

DKG allows multiple participants to derive one joint public key `PK` while the full private key `SK` never exists in one place during the protocol path.

## Simulation Flow

1. Each participant samples its own secret `x_j`.
2. Each participant builds a Shamir polynomial of degree `t-1`.
3. Each participant publishes Feldman commitments to the polynomial coefficients.
4. Each participant sends the appropriate share to every other participant.
5. Receivers verify shares with Feldman VSS.
6. Each participant sums accepted shares plus its own local share.
7. The result is the participant's final private share `sk_i`.
8. The joint public key is the sum of constant commitments:

```text
PK = C_0,1 + C_0,2 + ... + C_0,n
```

## Public Shares

The project also computes the public counterpart of each final private share:

```text
Y_i = F(i) * G
```

where `F` is the sum of all dealer polynomials. `Y_i` is used to verify threshold partial signatures.

## Implementation

Modules:

- `dkglab.protocols.participant`
- `dkglab.protocols.dkg`

Key elements:

- `Participant`
- `run_dkg(num_participants, threshold)`
- `DKGResult`
- `public_share_for_index(aggregated_commitments, participant_id)`

## Simulation Character

This is a local academic simulation. It does not model networking, latency, message authentication, or persistent share storage.
