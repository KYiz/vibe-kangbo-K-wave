"""Deterministic 256px transparent film-grain texture; stdlib only."""
from pathlib import Path
import random
import struct
import zlib

size = 256
rng = random.Random(419)
rows = []
for _ in range(size):
    row = bytearray([0])
    for _ in range(size):
        shade = rng.choice((34, 70, 116, 150, 190, 225))
        row.extend((shade, shade, shade, rng.randrange(18, 55)))
    rows.append(row)


def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))


png = bytearray(b"\x89PNG\r\n\x1a\n")
png.extend(chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)))
png.extend(chunk(b"IDAT", zlib.compress(b"".join(rows), 9)))
png.extend(chunk(b"IEND", b""))
(Path(__file__).parent / "grain.png").write_bytes(png)
