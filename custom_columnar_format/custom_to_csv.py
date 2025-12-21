from reader import CustomReader
import csv, sys

if len(sys.argv) != 3:
    print("Usage: python custom_to_csv.py input.ccf output.csv")
    sys.exit(1)

infile, outfile = sys.argv[1], sys.argv[2]

reader = CustomReader()
rows = reader.read_all(infile)

if not rows:
    print("No rows found")
    sys.exit(0)

fieldnames = list(rows[0].keys())
with open(outfile, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Wrote:", outfile)
