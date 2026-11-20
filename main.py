"""Entry program for the make.fun bounty "Sum up 20 November's world news
in one image" (news-image-20261120).

The poster itself is painted ahead of time by tools/build_image.py (which
drives render.py) and sealed into assets/entry.png.b64. This program is
deliberately standard-library only: it decodes that sealed image, checks
the PNG the way the gate will -- signature, chunk checksums, dimensions,
size -- and only then writes it as entry.png in the output directory.
No third-party package is imported, so the program runs the same in any
bare Python the grader provides.

    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import base64
import os
import struct
import sys
import zlib

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "assets", "entry.png.b64")


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


def load_poster():
    """Decode the sealed poster asset back into the exact PNG bytes."""
    with open(ASSET, "r", encoding="ascii") as fh:
        encoded = "".join(fh.read().split())
    return base64.b64decode(encoded, validate=True)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    blob = load_poster()
    width, height = check_png(blob)
    if (width, height) != (1024, 1024):
        raise ValueError(f"sealed poster is {width}x{height}, expected 1024x1024")
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as fh:
        fh.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
