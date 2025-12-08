from reader import CCFReader
import csv, sys

if len(sys.argv) != 3:
    print("Usage: python custom_to_csv.py input.ccf output.csv")
    sys.exit(1)

r = CCFReader(sys.argv[1])
rows = r.read_all()

with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=r.column_names())
    writer.writeheader()
    writer.writerows(rows)

print("[OK] Wrote", sys.argv[2])
