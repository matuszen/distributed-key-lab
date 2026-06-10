# Scenariusze testów bezpieczeństwa

## Testy pozytywne

- SSS odzyskuje sekret z dowolnych `t` udziałów.
- VSS akceptuje poprawny udział.
- DKG generuje jeden wspólny `PK` dla wszystkich uczestników.
- TSS 3 z 5 tworzy podpis przechodzący standardową weryfikację Schnorra.
- TSS działa dla niekolejnych uczestników, np. `{2, 4, 5}`.

## Testy negatywne

- SSS odrzuca rekonstrukcję z `t-1` udziałów.
- VSS odrzuca zmodyfikowany udział.
- VSS odrzuca zmodyfikowany commitment.
- DKG odrzuca błędnie zaadresowany albo zdublowany udział.
- Sesja TSS odrzuca mniej niż `t` uczestników.
- Sesja TSS odrzuca podmieniony partial signature.
- Finalna weryfikacja Schnorra odrzuca:
  - inną wiadomość,
  - inny klucz publiczny,
  - podmieniony punkt `R`.

## Uruchomienie

```bash
pytest -q
```

Smoke testy przykładów są częścią testów jednostkowych i sprawdzają najważniejsze komendy demonstracyjne.
