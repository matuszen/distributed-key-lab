# Aplikacja okienkowa

## Cel

Projekt zawiera prostą aplikację okienkową w Pythonie, która pozwala uruchomić główne funkcjonalności bez pisania komend w terminalu:

- podgląd parametrów krzywej,
- Shamir Secret Sharing,
- DKG dla scenariusza `3 z 5`,
- podpis progowy Schnorra,
- symulację ataku `t-1`,
- benchmark DKG.

## Technologia

Aplikacja używa standardowego `tkinter`. Nie wymaga dodatkowej biblioteki z `pip`, ale systemowy Python musi mieć dostępny moduł Tk.

Na Ubuntu/Debian zwykle wystarczy:

```bash
sudo apt install python3-tk
```

Następnie zainstaluj projekt:

```bash
pip install -e .[dev]
```

## Uruchomienie

Po instalacji entry pointu:

```bash
dkglab-gui
```

Alternatywnie:

```bash
python examples/gui_app.py
```

albo:

```bash
python -m dkglab.gui.app
```

## Zakładki

- `Start`: szybkie akcje demonstracyjne.
- `SSS`: formularz sekretu, progu i liczby uczestników.
- `DKG / TSS`: podpis wiadomości przez wybranych uczestników, atak `t-1` i benchmark.

Wynik każdej akcji jest pokazywany w panelu tekstowym po prawej stronie.
