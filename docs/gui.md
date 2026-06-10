# Desktop GUI

## Goal

The project includes a Python desktop application for the main DKG + threshold-signature workflow:

- DKG for the `3-of-5` scenario,
- threshold Schnorr signing by exactly three selected participants,
- a `t-1` attack simulation showing that two participants cannot produce a valid signature.

The interface follows the same flow as the protocol: first the participants generate a joint public key, then selected participants produce a threshold signature, and finally the threshold condition is checked with a negative scenario.

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

## Screen Layout

- signer list, defaulting to `1,3,5`,
- message input, defaulting to `Hello world!`,
- one full scenario button,
- three step buttons: DKG, threshold signature, and `t-1` attack,
- a text panel with the protocol output.

The fastest way to run the full flow is to click `Uruchom pelny scenariusz`. Individual steps can also be rerun separately.
