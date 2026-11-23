"""Stdlib-only entry point for news-image-20261123.

The artwork itself is drawn by build_entry.py (Pillow). This file only
copies the pre-built entry.png that sits next to this script into
/output/entry.png, using nothing but the Python standard library.
"""

import hashlib
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise FileNotFoundError("entry.png not found next to main.py: %s" % src)
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the copy byte-for-byte, not just by size: a same-size but
    # different file must still fail loudly.
    with open(src, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        dst_hash = hashlib.sha256(f.read()).hexdigest()
    if src_hash != dst_hash:
        raise ValueError(
            "copy hash mismatch: source %s, destination %s" % (src_hash, dst_hash)
        )
    print(
        "entry.png copied to %s (%d bytes, sha256 %s)"
        % (dst, os.path.getsize(dst), dst_hash)
    )


if __name__ == "__main__":
    main()
