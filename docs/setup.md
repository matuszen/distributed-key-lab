# Setup and Curve Parameters

## Goal
Validate the Python environment and secp256k1 parameters used by the project.

## Run
1. Install dependencies: `pip install -e .[dev]`
2. Run: `python3 setup_check.py`

## Expected Output
The script prints:
- curve name,
- base point coordinates G,
- group order n,
- a basic group relation sanity check.
