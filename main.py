# main.py -- news-image-20261123 v7 entrypoint
# Rebuilds entry.png from build_entry.py (pure standard library) and
# writes it to $MAKEFUN_OUTPUT_DIR (default /output). Deterministic:
# two runs write byte-identical files.
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_entry import build_png


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = build_png()
    if len(data) > 1048576:
        raise SystemExit("entry.png too large: %d bytes" % len(data))
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, sha256 %s)"
          % (path, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
