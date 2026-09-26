#!/usr/bin/env python3
"""Normalize avatar PNGs onto a shared transparent canvas.

The script either preserves meaningful source alpha or removes an explicitly
provided uniform chroma color. It never overwrites files unless --overwrite is
passed. Use a key color that does not occur in the subject.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - dependency diagnostic
    raise SystemExit("Pillow is required: install the 'Pillow' package.") from exc


def parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = (int(part) for part in value.lower().split("x", 1))
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("size must look like 720x720") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("size dimensions must be positive")
    return width, height


def parse_color(value: str) -> tuple[int, int, int]:
    raw = value.strip().removeprefix("#")
    if len(raw) != 6:
        raise argparse.ArgumentTypeError("color must be a six-digit hex value")
    try:
        return tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("color must be a six-digit hex value") from exc


def key_color(
    image: Image.Image,
    key: tuple[int, int, int],
    tolerance: float,
    softness: float,
) -> Image.Image:
    if softness <= 0:
        raise ValueError("softness must be positive")

    output: list[tuple[int, int, int, int]] = []
    for red, green, blue, source_alpha in image.convert("RGBA").getdata():
        distance = math.sqrt(
            (red - key[0]) ** 2 + (green - key[1]) ** 2 + (blue - key[2]) ** 2
        )
        if distance <= tolerance:
            factor = 0.0
        elif distance >= tolerance + softness:
            factor = 1.0
        else:
            factor = (distance - tolerance) / softness

        alpha = round(source_alpha * factor)
        if alpha <= 0:
            output.append((0, 0, 0, 0))
            continue

        if factor < 1.0:
            channels = []
            for channel, key_channel in zip((red, green, blue), key):
                unmixed = (channel - key_channel * (1.0 - factor)) / factor
                channels.append(max(0, min(255, round(unmixed))))
            output.append((*channels, alpha))
        else:
            output.append((red, green, blue, source_alpha))

    keyed = Image.new("RGBA", image.size)
    keyed.putdata(output)
    return keyed


def key_magenta(image: Image.Image) -> Image.Image:
    """Key a magenta screen using chroma dominance rather than RGB distance."""
    rgba = image.convert("RGBA")
    rgb = rgba.convert("RGB")
    output: list[tuple[int, int, int, int]] = []
    for y in range(rgb.height):
        left = rgb.getpixel((min(2, rgb.width - 1), y))
        right = rgb.getpixel((max(0, rgb.width - 3), y))
        row_key = tuple(round((a + b) / 2) for a, b in zip(left, right))
        for x in range(rgb.width):
            red, green, blue = rgb.getpixel((x, y))
            source_alpha = rgba.getpixel((x, y))[3]
            magenta_strength = min(red - green, blue - green)
            factor = max(0.0, min(1.0, (122.0 - magenta_strength) / 72.0))
            alpha = round(source_alpha * factor)
            if alpha <= 0:
                output.append((0, 0, 0, 0))
                continue
            if factor < 1.0:
                channels = []
                for channel, key_channel in zip((red, green, blue), row_key):
                    unmixed = (channel - key_channel * (1.0 - factor)) / factor
                    channels.append(max(0, min(255, round(unmixed))))
                output.append((*channels, alpha))
            else:
                output.append((red, green, blue, source_alpha))

    keyed = Image.new("RGBA", image.size)
    keyed.putdata(output)
    return keyed


def has_meaningful_alpha(image: Image.Image) -> bool:
    alpha = image.convert("RGBA").getchannel("A")
    low, high = alpha.getextrema()
    return low < 255 and high > 0


def normalize(
    image: Image.Image,
    canvas: tuple[int, int],
    target_height: int,
    bottom: int,
    padding: int,
    alpha_threshold: int,
) -> tuple[Image.Image, tuple[int, int, int, int]]:
    rgba = image.convert("RGBA")
    mask = rgba.getchannel("A").point(
        lambda value: 255 if value >= alpha_threshold else 0
    )
    bbox = mask.getbbox()
    if bbox is None:
        raise ValueError("no visible subject remains after alpha/key processing")

    subject = rgba.crop(bbox)
    available_width = canvas[0] - 2 * padding
    available_height = min(target_height, bottom)
    if available_width <= 0 or available_height <= 0:
        raise ValueError("padding, target height, and bottom leave no usable canvas")

    scale = min(target_height / subject.height, available_width / subject.width)
    scaled = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    subject = subject.resize(scaled, Image.Resampling.LANCZOS)

    x = (canvas[0] - scaled[0]) // 2
    y = bottom - scaled[1]
    if y < 0 or y + scaled[1] > canvas[1]:
        raise ValueError("normalized subject falls outside the requested canvas")

    result = Image.new("RGBA", canvas, (0, 0, 0, 0))
    result.alpha_composite(subject, (x, y))
    return result, (x, y, x + scaled[0], y + scaled[1])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="source PNG file(s)")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--canvas", type=parse_size, default=(720, 720))
    parser.add_argument("--subject-height", type=int, default=690)
    parser.add_argument(
        "--bottom",
        type=int,
        help="subject bottom coordinate; defaults to canvas height",
    )
    parser.add_argument("--padding", type=int, default=8)
    parser.add_argument("--alpha-threshold", type=int, default=24)
    parser.add_argument(
        "--key-color",
        type=parse_color,
        help="uniform chroma background, for example #FF00FF",
    )
    parser.add_argument(
        "--key-mode",
        choices=("auto", "distance", "magenta"),
        default="auto",
        help="auto uses a tuned spill-resistant method for #FF00FF and RGB distance otherwise",
    )
    parser.add_argument("--key-tolerance", type=float, default=28.0)
    parser.add_argument("--key-softness", type=float, default=90.0)
    parser.add_argument("--overwrite", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not 1 <= args.alpha_threshold <= 255:
        raise SystemExit("--alpha-threshold must be between 1 and 255")
    if args.subject_height <= 0 or args.padding < 0:
        raise SystemExit("--subject-height must be positive and --padding non-negative")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    bottom = args.bottom if args.bottom is not None else args.canvas[1]
    failures = 0

    for source in args.inputs:
        try:
            if not source.is_file():
                raise ValueError("input does not exist or is not a file")
            image = Image.open(source).convert("RGBA")
            if args.key_color is not None:
                use_magenta = args.key_mode == "magenta" or (
                    args.key_mode == "auto"
                    and args.key_color[0] >= 240
                    and args.key_color[1] <= 20
                    and args.key_color[2] >= 240
                )
                image = (
                    key_magenta(image)
                    if use_magenta
                    else key_color(
                        image,
                        args.key_color,
                        args.key_tolerance,
                        args.key_softness,
                    )
                )
            elif not has_meaningful_alpha(image):
                raise ValueError(
                    "source has no meaningful alpha; pass --key-color for a uniform chroma background"
                )

            result, bbox = normalize(
                image,
                args.canvas,
                args.subject_height,
                bottom,
                args.padding,
                args.alpha_threshold,
            )
            target = args.output_dir / f"{source.stem}.png"
            if target.exists() and not args.overwrite:
                raise ValueError(f"target exists: {target}; pass --overwrite to replace it")
            result.save(target)
            print(
                f"OK\t{source}\t{target}\tcanvas={args.canvas[0]}x{args.canvas[1]}\tbbox={bbox}"
            )
        except Exception as exc:  # per-file reporting for batch use
            failures += 1
            print(f"ERROR\t{source}\t{exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
