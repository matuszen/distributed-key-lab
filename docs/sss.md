# Shamir Secret Sharing

## Idea

The secret `a_0` is the constant term of a polynomial:

```text
f(x) = a_0 + a_1*x + ... + a_(t-1)*x^(t-1) mod n
```

where `n` is the group order of `SECP256k1`. Participant `i` receives:

```text
share_i = (i, f(i))
```

Any `t` shares can reconstruct `f(0)`, which is the secret. Fewer than `t` shares do not determine the polynomial uniquely.

## Implementation

Modules:

- `dkglab.secret_sharing.splitting`
- `dkglab.secret_sharing.lagrange`
- `dkglab.secret_sharing.recovery`

Important decisions:

- share indexes must be positive and unique,
- the secret is a scalar in `[1, n-1]`,
- for `threshold > 1`, the highest polynomial coefficient is non-zero,
- reconstruction uses Lagrange interpolation at `x=0`.

## Tests

The tests cover:

- splitting one secret into `5` shares,
- reconstruction from any valid set of `3`,
- failure with `2` shares when the threshold is `3`,
- rejection of duplicate indexes,
- Lagrange coefficients for non-consecutive indexes such as `{2, 4, 5}`.
