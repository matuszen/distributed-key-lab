# Feldman VSS and verify_share

## Idea
The dealer publishes commitments to polynomial coefficients:
C_j = a_j * G.

## Share Verification
For participant i with share s_i, verify:
s_i * G == sum(C_j * i^j).

If equality holds, the share is consistent with the public commitments.

## Security Benefit
Participants can reject incorrect shares without revealing the secret,
which mitigates dealer cheating.
