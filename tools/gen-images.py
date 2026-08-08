#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""Regenerate the site's icon artwork from the app's SVG.

    python3 tools/gen-images.py

Since 2026-08-07 the single source of truth is
`app/resources/icons/ingetrazo.svg` in the product repo — before that the master
was an 816 px PNG and there was no vector at all. This brings the site along:

  * images/logo.png        256  — header, footer, apple-touch-icon and JSON-LD
  * images/logo-512.png    512
  * images/favicon-16.png   16
  * images/favicon-32.png   32
  * images/og-banner.jpg  1200x630 — re-rendered from .cover-build/og.html,
                                     which embeds logo.png, so it must come last

TWO SNAP TRAPS, both of which cost time the first time round:

  * Chromium here is the snap. Its `home` interface gives it NO access to hidden
    directories, so it can neither READ `.cover-build/og.html` nor WRITE a
    screenshot into `.cover-build/`. The build therefore stages a copy of that
    folder in a VISIBLE directory under $HOME, renders there, and copies back.
  * It also cannot write to /tmp at all. Same workaround.

Needs Inkscape, Pillow and Chromium.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parents[1]
IMAGES = HERE / "images"
COVER = HERE / ".cover-build"

LOGOS = {256: "logo.png", 512: "logo-512.png", 16: "favicon-16.png",
         32: "favicon-32.png"}
BANNER = "og-banner.jpg"


def _chromium() -> str | None:
    for name in ("chromium-browser", "chromium", "google-chrome"):
        if shutil.which(name):
            return name
    return None


def render_svg(svg: Path, size: int, out: Path) -> None:
    subprocess.run(["inkscape", "-w", str(size), "-h", str(size), str(svg),
                    "-o", str(out)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def rebuild_banner() -> bool:
    """Re-render og.html at 1200x630 and save it as the OG banner."""
    browser = _chromium()
    if browser is None:
        print("!! no chromium on PATH; leaving og-banner.jpg alone", file=sys.stderr)
        return False
    if not (COVER / "og.html").is_file():
        print(f"!! missing {COVER / 'og.html'}", file=sys.stderr)
        return False

    # Visible staging dir: see the snap notes in the module docstring.
    stage = Path(tempfile.mkdtemp(prefix="ingetrazo-og-", dir=Path.home() / "Imágenes"))
    try:
        shutil.copytree(COVER, stage / "cover")
        shutil.copytree(IMAGES, stage / "images")     # og.html reads ../images/
        shot = stage / "og.png"
        subprocess.run([browser, "--headless", "--no-sandbox", "--disable-gpu",
                        "--hide-scrollbars", "--window-size=1200,630",
                        f"--screenshot={shot}", "--virtual-time-budget=6000",
                        (stage / "cover" / "og.html").as_uri()],
                       check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        if not shot.is_file():
            print("!! chromium wrote no screenshot", file=sys.stderr)
            return False
        im = Image.open(shot).convert("RGB")
        if im.size != (1200, 630):
            im = im.crop((0, 0, 1200, 630))
        im.save(IMAGES / BANNER, "JPEG", quality=90, optimize=True, progressive=True)
        print(f"  images/{BANNER}  {im.size[0]}x{im.size[1]}")
        return True
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def main() -> int:
    if not shutil.which("inkscape"):
        print("!! inkscape is not on PATH", file=sys.stderr)
        return 1
    svg = HERE.parent / "app" / "resources" / "icons" / "ingetrazo.svg"
    if not svg.is_file():
        print(f"!! missing {svg}", file=sys.stderr)
        return 1

    for size, name in LOGOS.items():
        render_svg(svg, size, IMAGES / name)
        print(f"  images/{name}  ({size}px)")
    rebuild_banner()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
