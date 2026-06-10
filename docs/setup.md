# Setup and Curve Parameters

## Goal

Validate the Python environment and `SECP256k1` parameters used by the project.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python setup_check.py
```

If you want to run the desktop GUI, make sure Python has `tkinter` installed. On Ubuntu/Debian this is usually provided by:

```bash
sudo apt install python3-tk
```

## Expected Output

The script prints:

- curve name,
- base point coordinates G,
- group order n,
- a basic group relation sanity check.

The final line should be:

```text
Sanity check n*G == INFINITY: True
```

## Next Steps

- Run the unit tests: `pytest -q`
- Run the DKG demo: `python examples/dkg_demo.py`
- Run the threshold wallet demo: `python examples/threshold_wallet_3of5.py`
- Run the desktop GUI: `python examples/gui_app.py`
