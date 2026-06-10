# Shamir Secret Sharing

## Idea

Sekret `a_0` jest stałym wyrazem wielomianu:

```text
f(x) = a_0 + a_1*x + ... + a_(t-1)*x^(t-1) mod n
```

gdzie `n` to rząd grupy krzywej `SECP256k1`. Udział uczestnika `i` to punkt:

```text
share_i = (i, f(i))
```

Dowolne `t` udziałów pozwala odtworzyć `f(0)`, czyli sekret. Mniej niż `t` udziałów nie wystarcza do jednoznacznego odtworzenia wielomianu.

## Implementacja

Moduły:

- `dkglab.secret_sharing.splitting`
- `dkglab.secret_sharing.lagrange`
- `dkglab.secret_sharing.recovery`

Ważne decyzje:

- indeksy udziałów są dodatnie i unikalne,
- sekret jest skalarem z zakresu `[1, n-1]`,
- dla `threshold > 1` najwyższy współczynnik wielomianu jest niezerowy,
- rekonstrukcja używa interpolacji Lagrange'a w punkcie `x=0`.

## Testy

Testy sprawdzają:

- podział sekretu na `5` udziałów,
- rekonstrukcję z dowolnych `3`,
- błąd przy `2` udziałach dla progu `3`,
- odrzucenie duplikatów indeksów,
- poprawność współczynników Lagrange'a dla niekolejnych indeksów, np. `{2, 4, 5}`.
