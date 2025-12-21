# GPP_TASK3: Custom Columnar File Format (CCF)

## Project Overview
This project implements a **Custom Columnar File Format (CCF)** in Python.  
The goal is to efficiently store and read tabular data in a **column-oriented binary format** with support for:

- Column-wise storage
- Selective column reads
- CSV to CCF conversion and back
- Round-trip testing

The format is designed according to the specifications in `SPEC.md`.

---

## Repository Structure

custom_columnar_format/
├── csv_to_custom.py # Script to convert CSV to CCF
├── custom_to_csv.py # Script to convert CCF back to CSV
├── reader.py # CustomReader implementation
├── writer.py # CustomWriter implementation
├── SPEC.md # Format specification
├── README.md # Project documentation
├── tests/ # Unit and round-trip tests
└── pycache/ # Temporary Python cache files (ignored in Git)


---

## Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/Divyasrirowtu/GPP_TASK3.git
cd GPP_TASK3/custom_columnar_format

2.Create a virtual environment (optional but recommended)

python -m venv venv
.\venv\Scripts\activate    # Windows
source venv/bin/activate   # Linux/macOS


3.Install dependencies

pip install -r requirements.txt


(If requirements.txt does not exist, the project uses only standard Python libraries: csv, sys.)

Usage
Convert CSV → CCF
python csv_to_custom.py input.csv output.ccf

Convert CCF → CSV
python custom_to_csv.py output.ccf restored.csv

Run Tests
python -m unittest discover tests

Features Implemented

Reads and writes CSV/CCF data.

Columnar storage with dictionary representation in memory.

Round-trip conversion to ensure correctness.

Input validation for command-line arguments.

Notes

This implementation is text-based (row-wise dictionary) for demonstration; binary columnar format is described in SPEC.md.

To implement full binary, header, type handling, and compression, follow the SPEC.md guidelines.

.gitignore ignores temporary CSV/CCF files and Python cache files.