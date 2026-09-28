#!/usr/bin/env python3
"""Build a labeled contact sheet from images or representative video frames."""

from __future__ import annotations

import argparse
import io
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover - dependency diagnostic
    raise SystemExit("Pillow is required: install the 'Pillow' package.") from exc


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".m4v"}


def parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = (int(part) for part in value.lower().split("x", 1))
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("size must look like 320x320") from exc
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


def collect(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path.is_dir():
            candidates = sorted(
                (
                candidate
                for candidate in path.rglob("*")
                if candidate.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
                ),
                key=lambda item: str(item).lower(),
            )
        elif path.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
            candidates = [path]
        else:
            candidates = []
        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved not in seen:
                files.append(candidate)
                seen.add(resolved)
    return files


def video_duration(path: Path) -> float:
    if shutil.which("ffprobe") is None:
        raise RuntimeError("ffprobe is required for video contact sheets")
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def video_frame(path: Path, position: float) -> Image.Image:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required for video contact sheets")
    duration = video_duration(path)
    timestamp = max(0.0, min(duration - 0.04, duration * position))
    result = subprocess.run(
        [
            "ffmpeg",
            "-loglevel",
            "error",
            "-ss",
            f"{timestamp:.4f}",
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-f",
            "image2pipe",
            "-vcodec",
            "png",
            "-",
        ],
        check=True,
        capture_output=True,
    )
    return Image.open(io.BytesIO(result.stdout)).convert("RGBA")


def checkerboard(
    size: tuple[int, int], background: tuple[int, int, int], checker: int
) -> Image.Image:
    alternate = tuple(max(0, channel - 13) for channel in background)
    result = Image.new("RGBA", size, (*background, 255))
    draw = ImageDraw.Draw(result)
    for y in range(0, size[1], checker):
        for x in range(0, size[0], checker):
            if (x // checker + y // checker) % 2:
                draw.rectangle(
                    (x, y, min(x + checker, size[0]), min(y + checker, size[1])),
                    fill=(*alternate, 255),
                )
    return result


def fit_image(image: Image.Image, cell: tuple[int, int]) -> Image.Image:
    contained = image.copy()
    contained.thumbnail(cell, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", cell, (0, 0, 0, 0))
    offset = ((cell[0] - contained.width) // 2, (cell[1] - contained.height) // 2)
    canvas.alpha_composite(contained, offset)
    return canvas


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--cell", type=parse_size, default=(320, 320))
    parser.add_argument("--label-height", type=int, default=34)
    parser.add_argument(
        "--labels",
        nargs="+",
        help="ordered labels for explicit inputs; count must match collected items",
    )
    parser.add_argument("--title", default="", help="optional review-board title")
    parser.add_argument("--title-height", type=int, default=54)
    parser.add_argument("--background", type=parse_color, default=(241, 244, 248))
    parser.add_argument("--checker-size", type=int, default=16)
    parser.add_argument(
        "--video-position",
        type=float,
        default=0.5,
        help="fraction of video duration used for each representative frame",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if (
        args.columns <= 0
        or args.label_height < 0
        or args.title_height < 0
        or args.checker_size <= 0
    ):
        raise SystemExit("columns/checker size must be positive and label height non-negative")
    if not 0.0 <= args.video_position <= 1.0:
        raise SystemExit("--video-position must be between 0 and 1")

    files = collect(args.inputs)
    if not files:
        raise SystemExit("no supported image or video files found")
    if args.labels is not None and len(args.labels) != len(files):
        raise SystemExit(
            f"--labels count ({len(args.labels)}) must match collected items ({len(files)})"
        )

    rows = math.ceil(len(files) / args.columns)
    cell_width, cell_height = args.cell
    title_height = args.title_height if args.title else 0
    sheet = Image.new(
        "RGBA",
        (
            args.columns * cell_width,
            title_height + rows * (cell_height + args.label_height),
        ),
        (*args.background, 255),
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    if args.title:
        draw.rectangle(
            (0, 0, sheet.width, title_height),
            fill=(24, 32, 45, 255),
        )
        draw.text((14, 18), args.title, fill=(255, 255, 255), font=font)

    for index, path in enumerate(files):
        try:
            if path.suffix.lower() in VIDEO_EXTENSIONS:
                image = video_frame(path, args.video_position)
            else:
                image = Image.open(path).convert("RGBA")
        except Exception as exc:
            print(f"ERROR\t{path}\t{exc}", file=sys.stderr)
            return 1

        column = index % args.columns
        row = index // args.columns
        x = column * cell_width
        y = title_height + row * (cell_height + args.label_height)
        backdrop = checkerboard(args.cell, args.background, args.checker_size)
        backdrop.alpha_composite(fit_image(image, args.cell))
        sheet.alpha_composite(backdrop, (x, y))
        label = args.labels[index] if args.labels is not None else path.name
        if len(label) > 44:
            label = f"{label[:20]}…{label[-21:]}"
        draw.text((x + 7, y + cell_height + 9), label, fill=(24, 32, 45), font=font)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.suffix.lower() in {".jpg", ".jpeg"}:
        sheet.convert("RGB").save(args.output, quality=92)
    else:
        sheet.save(args.output)
    print(f"OK\t{args.output}\titems={len(files)}\tgrid={args.columns}x{rows}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
