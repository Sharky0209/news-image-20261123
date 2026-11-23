"""news-image-20261123 entrypoint.

Stdlib-only: it copies the pre-built entry.png next to this file to
/output/entry.png. All drawing lives in build_entry.py, which needs
Pillow; the server runs this entrypoint with no third-party packages
installed, so it must not import anything beyond the standard library.
"""

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = "/output/entry.png"


def main():
    if not os.path.exists(SRC):
        raise SystemExit("missing entry image: " + SRC)
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copyfile(SRC, DST)
    if os.path.getsize(SRC) != os.path.getsize(DST):
        raise SystemExit("copy incomplete: " + DST)
    print("wrote " + DST)


if __name__ == "__main__":
    main()
