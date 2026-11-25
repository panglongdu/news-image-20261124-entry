"""make.fun news-image-20261124 entry — v2.

The deliverable is entry.png beside this file: a 1024x1024 magazine
front page summarising the world news of 24 November 2026, drawn by
build_image.py. This program simply delivers that image to the output
directory: MAKEFUN_OUTPUT_DIR when the environment sets it, /output
otherwise, creating the directory first if it does not exist.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"


def deliver():
    if not IMAGE.is_file():
        raise SystemExit(f"entry image missing: {IMAGE}")
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(IMAGE, target)
    return target


if __name__ == "__main__":
    print("wrote", deliver())
