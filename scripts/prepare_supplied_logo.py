"""Trim empty JPG margins and create an optimized, undistorted PNG logo asset."""

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageOps


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    image = ImageOps.exif_transpose(Image.open(args.source)).convert("RGB")
    white = Image.new("RGB", image.size, "white")
    difference = ImageChops.difference(image, white).convert("L").filter(ImageFilter.GaussianBlur(1))
    mask = difference.point(lambda value: 255 if value > 18 else 0)
    bounds = mask.getbbox()
    if bounds:
        padding = 24
        left = max(0, bounds[0] - padding)
        top = max(0, bounds[1] - padding)
        right = min(image.width, bounds[2] + padding)
        bottom = min(image.height, bounds[3] + padding)
        image = image.crop((left, top, right, bottom))

    image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.destination, "PNG", optimize=True)


if __name__ == "__main__":
    main()
