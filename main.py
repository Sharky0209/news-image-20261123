"""Copy entry.png next to this file to /output/entry.png.

Standard library only (os, shutil). No network, no clock, no randomness,
no environment input. Fails if the entry is over the 1 MiB limit.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1048576


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    size = os.path.getsize(DST)
    if size > MAX_BYTES:
        raise SystemExit("entry.png too large: %d > %d bytes" % (size, MAX_BYTES))
    print("copied %s -> %s (%d bytes)" % (SRC, DST, size))


if __name__ == "__main__":
    main()
