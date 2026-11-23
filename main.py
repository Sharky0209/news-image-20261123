"""Standard-library-only entry point for news-image-20261123 (v4).

The artwork is drawn by build_entry.py (Pillow). This file does no
drawing, no network access and no image decoding: it only copies the
pre-built entry.png sitting next to this script into /output/entry.png
and verifies the copy byte-for-byte by size.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        raise FileNotFoundError("entry.png not found next to main.py: %s" % source)
    os.makedirs("/output", exist_ok=True)
    dest = os.path.join("/output", "entry.png")
    if os.path.abspath(source) == os.path.abspath(dest):
        raise RuntimeError("source and destination are the same file: %s" % source)
    shutil.copyfile(source, dest)
    src_size = os.path.getsize(source)
    dst_size = os.path.getsize(dest)
    if src_size != dst_size:
        raise RuntimeError(
            "copy size mismatch: source %d bytes, dest %d bytes" % (src_size, dst_size)
        )
    print("%s (%d bytes)" % (dest, dst_size))


if __name__ == "__main__":
    main()
