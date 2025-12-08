#!/usr/bin/env python3
import sys
from writer import read_csv_to_rows, write_ccf

def main():
    if len(sys.argv) != 3:
        print("Usage: python csv_to_custom.py input.csv output.ccf")
        raise SystemExit(1)
    rows = read_csv_to_rows(sys.argv[1])
    write_ccf(sys.argv[2], rows)
    print("[OK] Wrote", sys.argv[2])

if __name__ == "__main__":
    main()
