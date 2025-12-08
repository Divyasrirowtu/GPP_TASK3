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
- INT32:
    null_bitmap (ceil(N/8) bytes), followed by N int32 values (little-endian).
- FLOAT64:
    null_bitmap, followed by N float64 values.
- STRING:
    null_bitmap, offsets array (N+1 uint64 little-endian), followed by concatenated UTF-8 bytes.

Null bitmap: bit i == 1 => NULL for row i. Bits packed LSB-first in each byte.

Compression: Each column block (the uncompressed bytes above) is compressed using zlib (DEFLATE). The header stores both compressed and uncompressed sizes and the absolute offset to the compressed bytes.

Notes:
- All integer sizes explicitly typed (uint16, uint64, int32).
- All offsets are absolute file offsets.
