# Verifiable Secret Sharing: Feldman

## Problem

Sam Shamir Secret Sharing zakłada uczciwego dealera. Jeśli dealer wyśle błędny udział, uczestnik nie ma lokalnie sposobu, aby to wykryć.

Feldman VSS dodaje publiczne zobowiązania do współczynników wielomianu:

```text
C_j = a_j * G
```

dla każdego współczynnika `a_j`.

## Weryfikacja udziału

Dla udziału `(i, s_i)` uczestnik sprawdza:

```text
s_i * G == C_0 + i*C_1 + i^2*C_2 + ... + i^(t-1)*C_(t-1)
```

Jeśli równość zachodzi, udział pasuje do publicznych zobowiązań dealera.

## Implementacja

Moduły:

- `dkglab.vss.feldman`
- `dkglab.vss.verification`

Funkcje:

- `build_feldman_commitments(coefficients)`
- `create_vss_package(share, coefficients)`
- `verify_share(share, commitments)`
- `verify_vss_package(package)`

## Ograniczenia

Feldman VSS zapewnia weryfikowalność, ale nie ukrywa publicznie zobowiązań przed analizą brute-force dla bardzo małych sekretów. W projekcie sekrety są skalarami grupy, więc dokumentujemy to jako ograniczenie akademickie, nie jako produkcyjny protokół poufności.
