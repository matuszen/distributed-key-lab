# Podpis Schnorra

## Lokalny algorytm

Dla klucza prywatnego `x`, klucza publicznego `PK = x*G` i wiadomości `m`:

```text
R = k * G
e = H(R, PK, m)
s = k + e*x mod n
signature = (R, s)
```

Weryfikacja:

```text
s * G == R + e * PK
```

## Implementacja

Moduł:

- `dkglab.crypto.schnorr`

Funkcje:

- `generate_keypair()`
- `sign_message(private_key, message)`
- `verify_signature(public_key, message, signature)`
- `compute_challenge(R, public_key, message)`
- `point_to_hex(point)`
- `scalar_to_hex(value)`

## Uwagi

`compute_challenge` jest publiczne, bo podpis progowy używa dokładnie tej samej wartości `e` dla częściowych podpisów i finalnej weryfikacji.
