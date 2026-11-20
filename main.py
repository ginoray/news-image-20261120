"""Entry program for the make.fun bounty "Sum up 20 November's world news
in one image" (news-image-20261120).

Paints the poster described in render.py, checks the encoded PNG the way
the gate will -- signature, chunk checksums, dimensions, size -- and only
then writes it as entry.png in the output directory. Painting is pure
arithmetic on fixed content, so two runs write the same bytes.

    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import io
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import draw_poster

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_png(blob):
    """Walk the chunk list, verifying each CRC and the IHDR geometry."""
    if not blob.startswith(PNG_MAGIC):
        raise ValueError("missing PNG signature")
    pos = len(PNG_MAGIC)
    width = height = None
    saw_end = False
    while pos < len(blob):
        (length,) = struct.unpack(">I", blob[pos:pos + 4])
        kind = blob[pos + 4:pos + 8]
        payload = blob[pos + 8:pos + 8 + length]
        (crc,) = struct.unpack(">I", blob[pos + 8 + length:pos + 12 + length])
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != crc:
            raise ValueError(f"CRC mismatch in chunk {kind!r}")
        if kind == b"IHDR":
            width, height = struct.unpack(">II", payload[:8])
        if kind == b"IEND":
            saw_end = True
            break
        pos += 12 + length
    if not saw_end:
        raise ValueError("no IEND chunk")
    if width is None or width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"bad dimensions {width}x{height}")
    if len(blob) > MAX_BYTES:
        raise ValueError(f"image too large: {len(blob)} bytes")
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    buf = io.BytesIO()
    draw_poster().save(buf, format="PNG", optimize=True)
    blob = buf.getvalue()
    check_png(blob)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as fh:
        fh.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
