# Szkic prezentacji

## Slajd 1: Cel projektu

- DKG i podpis progowy `t-of-n`.
- Przykład: wspólny portfel `3 z 5`.
- Pełny klucz prywatny nie istnieje w jednym miejscu.

## Slajd 2: Parametry kryptograficzne

- Python i `ecdsa`.
- Krzywa `SECP256k1`.
- Punkt bazowy `G` i rząd grupy `n`.
- `setup_check.py`.

## Slajd 3: Shamir Secret Sharing

- Sekret jako `f(0)`.
- Udziały jako punkty wielomianu.
- Rekonstrukcja przez Lagrange'a.

## Slajd 4: Feldman VSS

- Commitmenty `C_j = a_j*G`.
- Weryfikacja `s_i*G`.
- Ochrona przed nieuczciwym dealerem.

## Slajd 5: DKG

- Każdy uczestnik jest dealerem dla własnego sekretu.
- Udziały są weryfikowane i sumowane.
- Wspólny `PK` powstaje z publicznych commitmentów.

## Slajd 6: Schnorr

- `R = kG`.
- `e = H(R, PK, m)`.
- `s = k + eSK`.
- Standardowa weryfikacja.

## Slajd 7: Podpis progowy

- Każdy podpisujący ma tylko `sk_i`.
- Partial signature `z_i`.
- Agregacja do jednego podpisu `(R, s)`.

## Slajd 8: Scenariusze testowe

- Poprawny `3-of-5`.
- Niepoprawny `2-of-5`.
- Podmieniony udział VSS.
- Podmieniony partial signature.

## Slajd 9: Demo

- `python examples/dkg_demo.py`
- `python examples/threshold_wallet_3of5.py`
- `python examples/attack_t_minus_one.py`

## Slajd 10: Ograniczenia i wnioski

- Implementacja akademicka, nie produkcyjny FROST.
- Brak sieci i storage.
- Cel matematyczny i demonstracyjny został osiągnięty.
