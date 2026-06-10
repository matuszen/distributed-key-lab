# Security Test Scenarios

## Positive Tests

- SSS reconstructs a secret from any valid set of `t` shares.
- VSS accepts a valid share.
- DKG produces one joint `PK` for all participants.
- TSS 3-of-5 creates a signature that passes standard Schnorr verification.
- TSS works for non-consecutive participants, for example `{2, 4, 5}`.

## Negative Tests

- SSS rejects reconstruction with `t-1` shares.
- VSS rejects a modified share.
- VSS rejects a modified commitment.
- DKG rejects a misrouted or duplicated share.
- TSS rejects fewer than `t` selected participants.
- TSS rejects a tampered partial signature.
- Final Schnorr verification rejects:
  - a different message,
  - a different public key,
  - a modified point `R`.

## Running Tests

```bash
pytest -q
```

Smoke tests for the console examples are included in the unit test suite and cover the main demonstration commands.
