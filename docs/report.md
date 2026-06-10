# Raport końcowy

## Temat

Rozproszona generacja klucza i podpis progowy Schnorra w modelu `t-of-n`.

## Streszczenie

Projekt implementuje kompletną ścieżkę edukacyjną od parametrów krzywej eliptycznej, przez Shamir Secret Sharing i Feldman VSS, po lokalną symulację DKG oraz podpis progowy Schnorra. Główny scenariusz demonstracyjny to portfel `3 z 5`, w którym dowolnych trzech uczestników może podpisać wiadomość, ale dwóch uczestników jest blokowanych przed podpisywaniem.

## Środowisko

- Python 3.10+
- `ecdsa`
- `pytest`
- `ruff`
- `isort`
- krzywa `SECP256k1`

## Metody

1. Parametry kryptograficzne sprawdzono przez `setup_check.py`.
2. Sekret podzielono przez wielomian Shamira nad rzędem grupy.
3. Poprawność udziałów zabezpieczono commitmentami Feldmana.
4. DKG zrealizowano jako lokalną wymianę pakietów VSS między obiektami `Participant`.
5. Wspólny klucz publiczny wyliczono jako sumę publicznych contribution.
6. Podpis progowy zbudowano na partial signatures ważonych współczynnikami Lagrange'a.

## Wyniki

- Testy jednostkowe pokrywają SSS, VSS, DKG, Schnorra, TSS oraz przykłady.
- Demo `threshold_wallet_3of5.py` generuje podpis przechodzący `verify_signature`.
- Demo `attack_t_minus_one.py` blokuje próbę podpisu przez mniej niż próg.
- Benchmark DKG pokazuje prosty trend kosztu wraz ze wzrostem liczby uczestników.

## Ograniczenia

Implementacja jest akademicka. Nie jest pełnym FROST i nie obejmuje sieci, trwałego storage, ochrony przed side-channel ani produkcyjnej obsługi złośliwych uczestników. Nonce w przykładach bywają deterministyczne dla powtarzalności testów; kod domyślny używa `secrets`.

## Wniosek

Projekt spełnia cel zaliczeniowy: pokazuje matematyczne podstawy, weryfikowalność udziałów, rozproszoną generację wspólnego klucza publicznego i poprawny podpis progowy bez odtwarzania pełnego klucza prywatnego w ścieżce podpisywania.
