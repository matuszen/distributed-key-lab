# Przykłady użycia

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Parametry krzywej

```bash
python setup_check.py
```

Oczekiwane elementy wyniku:

- `Curve: SECP256k1`
- współrzędne `G.x` i `G.y`,
- rząd grupy `n`,
- `Sanity check n*G == INFINITY: True`.

## Demo DKG

```bash
python examples/dkg_demo.py
```

Pokazuje:

- liczbę uczestników,
- próg,
- wspólny klucz publiczny `PK`,
- publiczną weryfikację finalnych udziałów.

## Portfel 3 z 5

```bash
python examples/threshold_wallet_3of5.py
```

Oczekiwany wynik zawiera:

```text
Use case: threshold wallet 3-of-5
Signature valid: True
```

## Atak t-1

```bash
python examples/attack_t_minus_one.py
```

Oczekiwany wynik:

```text
Attack blocked: Not enough selected participants for threshold.
```

## Benchmark DKG

```bash
python examples/benchmark_dkg.py
```

Wynik ma format CSV:

```text
n,t,time_ms
```

## Aplikacja okienkowa

```bash
python examples/gui_app.py
```

Po ponownym `pip install -e .[dev]` można też użyć entry pointu:

```bash
dkglab-gui
```

Aplikacja pozwala wykonać te same scenariusze z formularzy: SSS, DKG, podpis progowy, atak `t-1` i benchmark.
