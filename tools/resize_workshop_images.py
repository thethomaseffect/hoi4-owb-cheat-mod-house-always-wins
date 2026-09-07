"""Resize the HOI4 thumbnail and Steam Workshop screenshots to the required sizes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

THUMBNAIL_SIZE = (512, 512)
SCREENSHOT_SIZE = (1920, 1080)
MAX_BYTES = 1_000_000
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def cover_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    src_w, src_h = image.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(round(src_h * target_ratio))
        left = (src_w - new_w) // 2
        image = image.crop((left, 0, left + new_w, src_h))
    elif src_ratio < target_ratio:
        new_h = int(round(src_w / target_ratio))
        top = (src_h - new_h) // 2
        image = image.crop((0, top, src_w, top + new_h))
    if image.size != size:
        image = image.resize(size, Image.Resampling.LANCZOS)
    return image


def as_rgb(image: Image.Image) -> Image.Image:
    if image.mode in {"RGB", "L"}:
        return image
    if image.mode == "RGBA":
        background = Image.new("RGB", image.size, (0, 0, 0))
        background.paste(image, mask=image.split()[3])
        return background
    return image.convert("RGB")


def save_under_limit(image: Image.Image, path: Path, png: bool) -> None:
    if png:
        image.save(path, format="PNG", optimize=True, compress_level=9)
        if path.stat().st_size <= MAX_BYTES:
            return
        quantized = image.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
        quantized.save(path, format="PNG", optimize=True, compress_level=9)
        return

    rgb = as_rgb(image)
    for quality in (90, 80, 70, 60, 50):
        rgb.save(path, format="JPEG", quality=quality, optimize=True)
        if path.stat().st_size <= MAX_BYTES:
            return


def process_image(path: Path, size: tuple[int, int], force_png: bool) -> str:
    with Image.open(path) as opened:
        image = opened.convert("RGBA") if force_png or path.suffix.lower() == ".png" else opened.convert("RGB")
        image.load()
        already_ok = image.size == size and path.stat().st_size <= MAX_BYTES
        resized = cover_resize(image, size)

    png = force_png or path.suffix.lower() == ".png"
    if already_ok and resized.size == size:
        return f"OK {path.name} {size[0]}x{size[1]}"

    save_under_limit(resized, path, png=png)
    size_kb = path.stat().st_size / 1024
    note = "" if path.stat().st_size <= MAX_BYTES else " (still over 1 MB)"
    return f"Resized {path.name} -> {size[0]}x{size[1]} ({size_kb:.0f} KB){note}"


def iter_screenshots(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )


def resize_all(repo: Path) -> list[str]:
    messages: list[str] = []
    thumbnail = repo / "thumbnail.png"
    if thumbnail.is_file():
        messages.append(process_image(thumbnail, THUMBNAIL_SIZE, force_png=True))
    else:
        messages.append("No thumbnail.png yet")

    screenshots = iter_screenshots(repo / "screenshots")
    if not screenshots:
        messages.append("No images in screenshots/")
    for path in screenshots:
        messages.append(process_image(path, SCREENSHOT_SIZE, force_png=False))
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    for line in resize_all(repo):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
