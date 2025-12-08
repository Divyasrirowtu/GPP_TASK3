Custom Columnar Format (CCF) — SPEC v1

Magic: 4 bytes ASCII "CCF1"
Endianness: little-endian for all integer/float encodings.

Header layout (bytes after magic):
- uint8 version
- uint64 total_rows
- uint16 num_columns
Then, for each column (repeated num_columns times):
- uint16 name_len
- name_len bytes UTF-8: column name
- uint8 type_id    (1 = INT32, 2 = FLOAT64, 3 = UTF8 STRING)
- uint64 block_uncompressed_size
- uint64 block_compressed_size
- uint64 block_offset   (absolute file offset to start of compressed block)

Column block (UNCOMPRESSED) formats:
- INT32: null bitmap + N int32 values
- FLOAT64: null bitmap + N float64 values
- STRING: null bitmap + offsets array (N+1 uint64) + concatenated UTF-8 bytes

Compression: Each column block compressed using zlib (DEFLATE)
