# Podpis progowy Schnorra

## Cel

Po DKG każdy uczestnik ma tylko swój udział `sk_i`. Projekt implementuje podpis, w którym wybrani uczestnicy wspólnie tworzą podpis Schnorra bez odtwarzania pełnego `SK`.

## Przebieg dla wybranych uczestników

1. Koordynator wybiera co najmniej `t` uczestników.
2. Każdy wybrany uczestnik generuje nonce `k_i` i publikuje `R_i = k_i*G`.
3. Sesja sumuje commitmenty nonce:

```text
R = R_1 + R_2 + ... + R_t
```

4. Wszyscy liczą challenge:

```text
e = H(R, PK, m)
```

5. Każdy uczestnik liczy współczynnik Lagrange'a `lambda_i` dla zbioru podpisującego.
6. Częściowy podpis:

```text
z_i = k_i + e * lambda_i * sk_i mod n
```

7. Agregator sprawdza część:

```text
z_i*G == R_i + e*lambda_i*Y_i
```

gdzie `Y_i = F(i)G` pochodzi z publicznych commitmentów DKG.

8. Finalny podpis:

```text
s = sum(z_i) mod n
signature = (R, s)
```

Finalna weryfikacja używa zwykłej funkcji Schnorra:

```text
verify_signature(PK, message, signature)
```

## Implementacja

Moduł:

- `dkglab.protocols.threshold_signature`

Elementy:

- `ThresholdSigningSession`
- `NonceShare`
- `NonceCommitment`
- `PartialSignature`
- `create_partial_signature`
- `verify_partial_signature`
- `aggregate_signatures`

## Ograniczenia bezpieczeństwa

To edukacyjny protokół progowy, nie pełny FROST. Projekt nie implementuje produkcyjnego mechanizmu binding factors, ochrony przed ponownym użyciem nonce ani sieciowej obsługi oszustów. Te ograniczenia są świadome i opisane, aby nie przedstawiać implementacji jako gotowej do użycia w portfelu produkcyjnym.
