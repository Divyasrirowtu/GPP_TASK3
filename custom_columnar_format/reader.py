#!/usr/bin/env python3
# reader.py - read CCF files with selective column reads

import struct, zlib, math
from typing import List, Dict, Optional

MAGIC = b"CCF1"
TYPE_INT32 = 1
TYPE_FLOAT64 = 2
TYPE_UTF8 = 3

class ColumnMeta:
    def __init__(self, name, type_id, uncompressed_size, compressed_size, offset):
        self.name = name
        self.type_id = type_id
        self.uncompressed_size = uncompressed_size
        self.compressed_size = compressed_size
        self.offset = offset

class CCFReader:
    def __init__(self, path: str):
        self.path = path
        self._parse_header()

    def _parse_header(self):
        with open(self.path, "rb") as f:
            magic = f.read(4)
            if magic != MAGIC:
                raise ValueError("bad magic")
            version = struct.unpack("<B", f.read(1))[0]
            total_rows = struct.unpack("<Q", f.read(8))[0]
            num_columns = struct.unpack("<H", f.read(2))[0]
            self.version = version
            self.total_rows = total_rows
            self.num_columns = num_columns
            self.columns = []
            for _ in range(num_columns):
                name_len = struct.unpack("<H", f.read(2))[0]
                name = f.read(name_len).decode("utf-8")
                type_id = struct.unpack("<B", f.read(1))[0]
                uncompressed_size = struct.unpack("<Q", f.read(8))[0]
                compressed_size = struct.unpack("<Q", f.read(8))[0]
                offset = struct.unpack("<Q", f.read(8))[0]
                self.columns.append(ColumnMeta(name, type_id, uncompressed_size, compressed_size, offset))

    def column_names(self) -> List[str]:
        return [c.name for c in self.columns]

    def _parse_null_bitmap(self, data: bytes, nrows: int):
        nb_len = (nrows + 7) // 8
        bitmap = data[:nb_len]
        nulls = []
        for i in range(nrows):
            byte_idx = i // 8
            bit_idx = i % 8
            nulls.append(bool((bitmap[byte_idx] >> bit_idx) & 1))
        return nulls, nb_len

    def _read_column_block(self, col: ColumnMeta):
        with open(self.path, "rb") as f:
            f.seek(col.offset)
            comp = f.read(col.compressed_size)
        raw = zlib.decompress(comp)
        n = self.total_rows
        nulls, nb_len = self._parse_null_bitmap(raw, n)
        pos = nb_len
        if col.type_id == TYPE_INT32:
            vals = []
            for i in range(n):
                v = struct.unpack_from("<i", raw, pos + i*4)[0]
                if nulls[i]:
                    vals.append(None)
                else:
                    vals.append(v)
            return vals
        elif col.type_id == TYPE_FLOAT64:
            vals = []
            for i in range(n):
                v = struct.unpack_from("<d", raw, pos + i*8)[0]
                if nulls[i]:
                    vals.append(None)
                else:
                    vals.append(v)
            return vals
        elif col.type_id == TYPE_UTF8:
            # offsets: (n+1) uint64
            offs = []
            for i in range(n+1):
                o = struct.unpack_from("<Q", raw, pos + i*8)[0]
                offs.append(o)
            pos_offsets = pos + (n+1)*8
            data_bytes = raw[pos_offsets:]
            vals = []
            for i in range(n):
                if nulls[i]:
                    vals.append(None)
                else:
                    start = offs[i]
                    end = offs[i+1]
                    vals.append(data_bytes[start:end].decode("utf-8"))
            return vals
        else:
            raise ValueError("unknown type")

    def read_columns(self, names: List[str]):
        # return dict name -> list of values
        name_to_meta = {c.name: c for c in self.columns}
        out = {}
        for name in names:
            if name not in name_to_meta:
                raise KeyError(name)
            out[name] = self._read_column_block(name_to_meta[name])
        return out

    def read_all(self) -> List[Dict[str,Optional[str]]]:
        cols = self.column_names()
        data = self.read_columns(cols)
        rows = []
        n = self.total_rows
        for i in range(n):
            row = {}
            for c in cols:
                row[c] = data[c][i]
            rows.append(row)
        return rows
