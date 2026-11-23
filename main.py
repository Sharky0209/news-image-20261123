"""Standard-library-only entry point for news-image-20261123.

The drawing itself lives in build_entry.py (Pillow). This file only
locates the rendered entry.png next to this script and copies it to
/output/entry.png, verifying the copy by size.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        raise FileNotFoundError("entry.png not found next to main.py: %s" % SOURCE)
    os.makedirs(DEST_DIR, exist_ok=True)
    # Copy to a temp file first, then atomically replace the destination,
    # so an interrupted copy never leaves a partial /output/entry.png.
    tmp_dest = DEST + ".tmp"
    shutil.copyfile(SOURCE, tmp_dest)
    src_size = os.path.getsize(SOURCE)
    tmp_size = os.path.getsize(tmp_dest)
    if src_size != tmp_size:
        os.remove(tmp_dest)
        raise RuntimeError(
            "copy size mismatch: source %d bytes, temp %d bytes"
            % (src_size, tmp_size)
        )
    os.replace(tmp_dest, DEST)
    dst_size = os.path.getsize(DEST)
    if src_size != dst_size:
        raise RuntimeError(
            "copy size mismatch: source %d bytes, dest %d bytes" % (src_size, dst_size)
        )
    print("copied %s -> %s (%d bytes)" % (SOURCE, DEST, dst_size))


if __name__ == "__main__":
    main()
