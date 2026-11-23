"""news-image-20261123 entrypoint: copy the prebuilt entry.png to /output.

Stdlib only: the server runs this program as Python 3.13 with no
third-party packages installed, so it must not import Pillow or anything
else outside the standard library. The image itself is built by
build_entry.py (Pillow + DejaVu, deterministic) and shipped in the
repository as entry.png; this entrypoint only copies that file to the
output directory. Running it twice writes byte-identical output.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, "/output/entry.png")
    print("wrote /output/entry.png")


if __name__ == "__main__":
    main()
