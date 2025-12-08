#!/usr/bin/env python3
import sys, csv
from reader import CCFReader

def main():
    if len(sys.argv) != 3:
        print("Usage: python custom_to_csv.py input.ccf output.csv")
        raise SystemExit(1)
    r = CCFReader(sys.argv[1])
    rows = r.read_all()
    cols = r.column_names()
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in rows:
            # convert None to empty string for CSV
            out = {k: ("" if v is None else v) for k, v in row.items()}
            writer.writerow(out)
    print("[OK] Wrote", sys.argv[2])

if __name__ == "__main__":
    main()
