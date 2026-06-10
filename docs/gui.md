# Desktop GUI

## Goal

The project includes a simple Python desktop application that runs the main project functionality without requiring terminal commands:

- curve parameter preview,
- Shamir Secret Sharing,
- DKG for the `3-of-5` scenario,
- threshold Schnorr signing,
- `t-1` attack simulation,
- DKG benchmark.

## Technology

The app uses standard `tkinter`. It does not require an additional `pip` dependency, but the system Python must provide the Tk module.

On Ubuntu/Debian this is usually installed with:

```bash
sudo apt install python3-tk
```

Then install the project:

```bash
pip install -e .[dev]
```

## Running the App

After installing the entry point:

```bash
dkglab-gui
```

Alternatively:

```bash
python examples/gui_app.py
```

or:

```bash
python -m dkglab.gui.app
```

## Tabs

- `Start`: quick demo actions.
- `SSS`: form for secret, threshold, and participant count.
- `DKG / TSS`: message signing by selected participants, `t-1` attack, and benchmark.

Each action writes its result to the text panel on the right side of the window.
