#!/usr/bin/env python3
import os, time, csv
from writer import read_csv_to_rows, write_ccf
from reader import CCFReader

def create_sample(path):
    with open(path, "w", encoding="utf-8", newline='') as f:
        f.write("id,score,name,notes\n")
        f.write("1,88.5,Alice,likes apples\n")
        f.write("2,92.0,Bob,\n")
        f.write("3,77.3,Charlie,enjoys chess\n")
        f.write("4,,Diana,null\n")
        f.write("5,81.2,,unicode\n")

def compare_csv(a, b):
    with open(a, encoding='utf-8') as f1, open(b, encoding='utf-8') as f2:
        return f1.read().strip() == f2.read().strip()

def benchmark_selective(ccf_path, colname):
    r = CCFReader(ccf_path)
    t0 = time.time()
    vals = r.read_columns([colname])[colname]
    t1 = time.time()
    return t1 - t0, vals[:5]

def benchmark_csv_parse(csv_path, colname):
    t0 = time.time()
    out = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            out.append(row.get(colname, ""))
    t1 = time.time()
    return t1 - t0, out[:5]

def run():
    sample = "tests_sample.csv"
    ccf = "tests_sample.ccf"
    out_csv = "tests_sample_out.csv"
    create_sample(sample)
    rows = read_csv_to_rows(sample)
    write_ccf(ccf, rows)
    # convert back
    r = CCFReader(ccf)
    rows_back = r.read_all()
    cols = r.column_names()
    with open(out_csv, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        for row in rows_back:
            out = {k: ("" if v is None else v) for k,v in row.items()}
            writer.writerow(out)
    ok = compare_csv(sample, out_csv)
    print("Round-trip identical:", ok)
    t_csv, _ = benchmark_csv_parse(sample, "name")
    t_sel, _ = benchmark_selective(ccf, "name")
    print(f"CSV parse time (name): {t_csv:.6f}s, selective CCF read (name): {t_sel:.6f}s")

if __name__ == "__main__":
    run()
