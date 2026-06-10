# Use Cases

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Curve Parameters

```bash
python setup_check.py
```

Expected output includes:

- `Curve: SECP256k1`,
- `G.x` and `G.y`,
- group order `n`,
- `Sanity check n*G == INFINITY: True`.

## DKG Demo

```bash
python examples/dkg_demo.py
```

Shows:

- participant count,
- threshold,
- joint public key `PK`,
- public verification of final shares.

## 3-of-5 Wallet

```bash
python examples/threshold_wallet_3of5.py
```

Expected output includes:

```text
Use case: threshold wallet 3-of-5
Signature valid: True
```

## t-1 Attack

```bash
python examples/attack_t_minus_one.py
```

Expected output:

```text
Attack blocked: Not enough selected participants for threshold.
```

## DKG Benchmark

```bash
python examples/benchmark_dkg.py
```

The output is CSV-like:

```text
n,t,time_ms
```

## Desktop GUI

```bash
python examples/gui_app.py
```

After reinstalling the editable package, the script entry point is also available:

```bash
dkglab-gui
```

The app runs the main DKG + threshold-signature workflow: DKG, threshold signing, and the `t-1` attack check.
