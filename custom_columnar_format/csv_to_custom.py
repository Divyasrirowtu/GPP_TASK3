import sys
import csv

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)

with open(output_file, 'w') as f:
    for row in rows:
        f.write(','.join(row) + '\n')

print(f"{output_file} created successfully!")
