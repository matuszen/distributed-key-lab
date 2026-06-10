# Specyfikacja wymagań

## Cel projektu

Projekt demonstruje akademicką implementację rozproszonej generacji klucza (DKG) i podpisu progowego Schnorra dla schematu `t-of-n`. System ma pokazać, że:

- sekret może zostać podzielony metodą Shamira,
- poprawność udziałów można sprawdzić przez Feldman VSS,
- grupa uczestników może wygenerować wspólny klucz publiczny bez składania pełnego klucza prywatnego,
- dowolne co najmniej `t` poprawnych udziałów może wygenerować podpis,
- mniej niż `t` uczestników nie przechodzi ścieżki podpisywania.

## Zakres funkcjonalny

- Python 3.10+ i biblioteka `ecdsa`.
- Krzywa `SECP256k1`.
- Shamir Secret Sharing nad rzędem grupy krzywej.
- Feldman VSS na punktach krzywej.
- Lokalna symulacja DKG w pamięci procesu.
- Lokalny podpis Schnorra i weryfikacja podpisu.
- Edukacyjny podpis progowy Schnorra bez odtwarzania pełnego `SK`.
- Przykłady konsolowe i testy automatyczne.

## Poza zakresem

- Pełny protokół FROST.
- Sieć, transport wiadomości i autoryzacja uczestników.
- Ochrona side-channel.
- Trwałe przechowywanie udziałów.
- Produkcyjna obsługa awarii i karanie uczestników.

## Kryteria akceptacji

- `python setup_check.py` drukuje parametry krzywej i potwierdza `n*G == INFINITY`.
- `pytest` przechodzi wszystkie testy.
- `examples/threshold_wallet_3of5.py` kończy się `Signature valid: True`.
- `examples/attack_t_minus_one.py` kończy się komunikatem `Attack blocked`.
- Dokumentacja opisuje założenia bezpieczeństwa i ograniczenia implementacji.
