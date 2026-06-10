# Desktop GUI

## Goal

The project includes a Python desktop application for the main distributed key generation and threshold-signature workflow:

- distributed key generation for the `3-of-5` scenario,
- threshold Schnorr signing by exactly three selected participants,
- a negative scenario showing that two participants cannot produce a valid signature.

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
- three step buttons: distributed key generation, threshold signature, and the too-few-participants check,
- a scrollable text panel with the protocol output.

Run the steps in order: first distributed key generation, then threshold signing, then the too-few-participants check. The joint public key, the shared signing nonce point, and the signature scalar are printed in full.
