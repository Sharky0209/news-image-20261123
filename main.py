"""Standard-library-only entry point for news-image-20261123.

The artwork is drawn by build_entry.py (Pillow). This file does no
drawing, no network access and no image decoding: it only copies the
pre-built entry.png that sits next to this script into /output/entry.png
and verifies the copy by size.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError("entry.png not found next to main.py: %s" % src)
    with open(src, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png next to main.py is not a PNG file: %s" % src)
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    if src_size != dst_size:
        raise RuntimeError(
            "copy size mismatch: source %d bytes, output %d bytes"
            % (src_size, dst_size)
        )
    print("Copied %s (%d bytes) -> %s" % (src, src_size, dst))


if __name__ == "__main__":
    main()
