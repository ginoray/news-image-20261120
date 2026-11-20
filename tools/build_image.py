"""Build-time tool: paint the poster and seal it into assets/entry.png.b64.

This is the only step that needs Pillow. It imports render.py's
draw_poster(), encodes the PNG exactly as the entry will ship it, and
stores the bytes base64-wrapped in assets/entry.png.b64, which the
standard-library-only main.py later decodes. Run it whenever render.py
changes:

    python3 tools/build_image.py
"""

import base64
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from render import draw_poster  # noqa: E402

ASSET = os.path.join(ROOT, "assets", "entry.png.b64")


def main():
    buf = io.BytesIO()
    draw_poster().save(buf, format="PNG", optimize=True)
    blob = buf.getvalue()
    os.makedirs(os.path.dirname(ASSET), exist_ok=True)
    wrapped = base64.encodebytes(blob).decode("ascii")
    with open(ASSET, "w", encoding="ascii") as fh:
        fh.write(wrapped)
    print(f"sealed {len(blob)} PNG bytes into {ASSET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
