"""Copy the pre-rendered front page to the grader's output directory.

The image (entry.png) is committed in this repository. This program only
copies it: destination is the first command-line argument, else the
MAKEFUN_OUTPUT_DIR environment variable, else /output. It writes
/output/entry.png (or <dir>/entry.png) and exits 0 on success, 1 on any
failure. Standard library only: os, shutil, sys.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = ""
    if len(sys.argv) > 1 and sys.argv[1]:
        target_dir = sys.argv[1]
    if not target_dir:
        target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not target_dir:
        target_dir = "/output"
    try:
        if not os.path.isfile(source):
            return 1
        with open(source, "rb") as handle:
            if handle.read(8) != b"\x89PNG\r\n\x1a\n":
                return 1
        os.makedirs(target_dir, exist_ok=True)
        shutil.copyfile(source, os.path.join(target_dir, "entry.png"))
    except OSError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
