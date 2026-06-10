# Distributed Key Generation

## Cel

DKG pozwala wielu uczestnikom wygenerować wspólny klucz publiczny `PK`, przy czym pełny klucz prywatny `SK` nigdy nie istnieje w jednym miejscu w ścieżce protokołu.

## Przebieg symulacji

1. Każdy uczestnik losuje własny sekret `x_j`.
2. Każdy uczestnik buduje wielomian Shamira stopnia `t-1`.
3. Każdy uczestnik publikuje commitmenty Feldmana do współczynników.
4. Każdy uczestnik wysyła odpowiedni udział do każdego innego uczestnika.
5. Odbiorcy weryfikują udziały przez Feldman VSS.
6. Każdy uczestnik sumuje zaakceptowane udziały i swój udział własny.
7. Powstaje finalny udział prywatny `sk_i`.
8. Wspólny klucz publiczny to suma commitmentów stałych:

```text
PK = C_0,1 + C_0,2 + ... + C_0,n
```

## Publiczne udziały

Projekt wylicza też publiczny odpowiednik finalnego udziału:

```text
Y_i = F(i) * G
```

gdzie `F` jest sumą wszystkich wielomianów. `Y_i` jest potrzebny do weryfikacji częściowych podpisów.

## Implementacja

Moduły:

- `dkglab.protocols.participant`
- `dkglab.protocols.dkg`

Najważniejsze elementy:

- `Participant`
- `run_dkg(num_participants, threshold)`
- `DKGResult`
- `public_share_for_index(aggregated_commitments, participant_id)`

## Charakter symulacji

To lokalna symulacja akademicka. Nie modeluje sieci, opóźnień, uwierzytelnienia wiadomości ani trwałego przechowywania udziałów.
