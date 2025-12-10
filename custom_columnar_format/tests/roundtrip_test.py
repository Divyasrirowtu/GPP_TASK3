# roundtrip_test.py
import csv
import os
from csv_to_custom import csv_to_custom
from custom_to_csv import custom_to_csv

def read_csv_as_list(path):
    """Reads a CSV file into a list of rows (each row = list of strings)."""
    with open(path, newline="", encoding="utf-8") as f:
        return [row for row in csv.reader(f)]

def compare_csv_files(file1, file2):
    """Compares two CSV files row-by-row and column-by-column."""
    csv1 = read_csv_as_list(file1)
    csv2 = read_csv_as_list(file2)

    if csv1 == csv2:
        return True
    else:
        print("\n❌ Difference detected!")
        print("Expected:")
        print(csv1)
        print("Got:")
        print(csv2)
        return False

def run_roundtrip_test(input_csv, ccf_file, output_csv):
    print("▶ Converting CSV → CCF...")
    csv_to_custom(input_csv, ccf_file)

    print("▶ Converting CCF → CSV...")
    custom_to_csv(ccf_file, output_csv)

    print("▶ Comparing results...")
    if compare_csv_files(input_csv, output_csv):
        print("\n✅ ROUNDTRIP SUCCESS: Output CSV matches original CSV.\n")
    else:
        print("\n❌ ROUNDTRIP FAILED: Output CSV does NOT match original.\n")

if __name__ == "__main__":
    INPUT_CSV = "sample.csv"
    CCF_FILE = "test_output.ccf"
    OUTPUT_CSV = "reconstructed.csv"

    # Check file existence
    if not os.path.exists(INPUT_CSV):
        print(f"❌ Input CSV '{INPUT_CSV}' not found! Create sample.csv first.")
        exit(1)

    run_roundtrip_test(INPUT_CSV, CCF_FILE, OUTPUT_CSV)
    