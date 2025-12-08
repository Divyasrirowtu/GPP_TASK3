#!/usr/bin/env python3
# writer.py - write CCF files

import struct, zlib, csv
from typing import List, Dict, Any, Optional
import math

MAGIC = b"CCF1"
VERSION = 1

TYPE_INT32 = 1
TYPE_FLOAT64 = 2
TYPE_UTF8 = 3

def pack_null_bitmap(nulls: List[bool]) -> bytes:
    n = len(nulls)
    b = bytearray((n + 7) // 8)
    for i, is_null in enumerate(nulls):
        if is_null:
            idx = i // 8
            bit = i % 8
            b[idx] |= (1 << bit)
    return bytes(b)

def infer_type(values: List[Optional[str]]) -> int:
    # try int -> float -> string
    has_nonnull = False
    for v in values:
        if v is None or v == "":
            continue
        has_nonnull = True
        try:
            int(v)
        except:
            break
    else:
        if has_nonnull:
            return TYPE_INT32

    has_nonnull = False
    for v in values:
        if v is None or v == "":
            continue
        has_nonnull = True
        try:
            float(v)
        except:
            break
    else:
        if has_nonnull:
            return TYPE_FLOAT64

    return TYPE_UTF8

def build_column_block(values: List[Optional[str]], type_id: int) -> bytes:
    n = len(values)
    nulls = [(v is None) or (v == "") for v in values]
    bitmap = pack_null_bitmap(nulls)
    if type_id == TYPE_INT32:
        body = bytearray()
        for v, is_null in zip(values, nulls):
            if is_null:
                body += struct.pack("<i", 0)
            else:
                body += struct.pack("<i", int(v))
        return bitmap + bytes(body)
    elif type_id == TYPE_FLOAT64:
        body = bytearray()
        for v, is_null in zip(values, nulls):
            if is_null:
                body += struct.pack("<d", 0.0)
            else:
                body += struct.pack("<d", float(v))
        return bitmap + bytes(body)
    elif type_id == TYPE_UTF8:
        offsets = [0]
        data = bytearray()
        for v, is_null in zip(values, nulls):
            if is_null:
                offsets.append(offsets[-1])
            else:
                b = v.encode("utf-8")
                data += b
                offsets.append(offsets[-1] + len(b))
        off_bytes = bytearray()
        for o in offsets:
            off_bytes += struct.pack("<Q", o)
        return bitmap + bytes(off_bytes) + bytes(data)
    else:
        raise ValueError("unknown type")

def write_ccf(path: str, rows: List[Dict[str,str]]):
    if not rows:
        raise ValueError("no rows")
    columns = list(rows[0].keys())
    nrows = len(rows)
    cols_values = {c: [row.get(c, "") for row in rows] for c in columns}
    types = {c: infer_type(cols_values[c]) for c in columns}

    # Build raw uncompressed blocks
    raw_blocks = {}
    for c in columns:
        raw_blocks[c] = build_column_block(cols_values[c], types[c])

    # Compress and gather meta
    meta = {}
    for c in columns:
        raw = raw_blocks[c]
        comp = zlib.compress(raw)
        meta[c] = {
            "type": types[c],
            "uncompressed_size": len(raw),
            "compressed_size": len(comp),
            "comp_bytes": comp,
        }

    # Build header in-memory
    header = bytearray()
    header += struct.pack("<B", VERSION)
    header += struct.pack("<Q", nrows)
    header += struct.pack("<H", len(columns))
    for c in columns:
        name_b = c.encode("utf-8")
        header += struct.pack("<H", len(name_b))
        header += name_b
        header += struct.pack("<B", meta[c]["type"])
        header += struct.pack("<Q", meta[c]["uncompressed_size"])
        header += struct.pack("<Q", meta[c]["compressed_size"])
        header += struct.pack("<Q", 0)  # placeholder for offset

    # compute offsets (absolute)
    magic_len = len(MAGIC)
    header_len = len(header)
    first_block_offset = magic_len + header_len
    offset = first_block_offset
    for c in columns:
        meta[c]["offset"] = offset
        offset += meta[c]["compressed_size"]

    # rebuild header with correct offsets
    header = bytearray()
    header += struct.pack("<B", VERSION)
    header += struct.pack("<Q", nrows)
    header += struct.pack("<H", len(columns))
    for c in columns:
        name_b = c.encode("utf-8")
        header += struct.pack("<H", len(name_b))
        header += name_b
        header += struct.pack("<B", meta[c]["type"])
        header += struct.pack("<Q", meta[c]["uncompressed_size"])
        header += struct.pack("<Q", meta[c]["compressed_size"])
        header += struct.pack("<Q", meta[c]["offset"])

    # write file
    with open(path, "wb") as f:
        f.write(MAGIC)
        f.write(header)
        for c in columns:
            f.write(meta[c]["comp_bytes"])

def read_csv_to_rows(path: str):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python writer.py input.csv out.ccf")
        raise SystemExit(1)
    rows = read_csv_to_rows(sys.argv[1])
    write_ccf(sys.argv[2], rows)
    print("Wrote", sys.argv[2])
