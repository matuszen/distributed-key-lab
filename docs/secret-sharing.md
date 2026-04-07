# Secret Sharing and recover_secret

## Idea
The secret is the constant term of a degree-(t-1) polynomial over a finite field.
Each share is a point (x_i, y_i) on that polynomial.

## Recovery
The recover_secret function reconstructs the constant term using Lagrange interpolation at x=0.
For threshold t, at least t valid shares are required.

## Implementation Notes
- x indices must be positive and unique,
- fewer than t shares raises an error,
- arithmetic is performed modulo the selected field order.
