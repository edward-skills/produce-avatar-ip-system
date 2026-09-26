#!/usr/bin/env python3
"""Inspect avatar image/video delivery invariants and emit a JSON report."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - dependency diagnostic
    raise SystemExit("Pillow is required: install the 'Pillow' package.") from exc


IMAGE_EXTENSIONS = {".png"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".m4v"}
SSIM_PATTERN = re.compile(r"All:([0-9.]+)")


def parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = (int(part) for part in value.lower().split("x", 1))
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("size must look like 720x720") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("size dimensions must be positive")
    return width, height


def collect(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(
                candidate
                for candidate in path.rglob("*")
                if candidate.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
            )
        elif path.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS:
            files.append(path)
    return sorted(set(files), key=lambda item: str(item).lower())


def inspect_image(
    path: Path, expected_size: tuple[int, int] | None, require_alpha: bool
) -> dict[str, object]:
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    low, high = alpha.getextrema()
    histogram = alpha.histogram()
    pixel_count = image.width * image.height
    transparent_ratio = sum(histogram[:255]) / pixel_count
    bbox = alpha.point(lambda value: 255 if value >= 24 else 0).getbbox()
    issues: list[str] = []

    if expected_size and image.size != expected_size:
        issues.append(
            f"image size {image.width}x{image.height}, expected {expected_size[0]}x{expected_size[1]}"
        )
    if require_alpha and not (low < 255 and high > 0):
        issues.append("image lacks meaningful transparency")
    if bbox is None:
        issues.append("image has no visible subject at alpha threshold 24")

    return {
        "path": str(path),
        "kind": "image",
        "size": [image.width, image.height],
        "alpha_extrema": [low, high],
        "transparent_pixel_ratio": round(transparent_ratio, 6),
        "visible_bbox": list(bbox) if bbox else None,
        "issues": issues,
        "pass": not issues,
    }


def ffprobe(path: Path) -> dict[str, object]:
    if shutil.which("ffprobe") is None:
        raise RuntimeError("ffprobe is required for video inspection")
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def calculate_ssim(path: Path, last_offset: float) -> float:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required for --loop-ssim")
    with tempfile.TemporaryDirectory(prefix="avatar-loop-qa-") as tmp:
        first = Path(tmp) / "first.png"
        last = Path(tmp) / "last.png"
        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(path),
                "-frames:v",
                "1",
                str(first),
            ],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-y",
                "-sseof",
                f"-{last_offset}",
                "-i",
                str(path),
                "-vf",
                "reverse",
                "-frames:v",
                "1",
                str(last),
            ],
            check=True,
            capture_output=True,
        )
        result = subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(first),
                "-i",
                str(last),
                "-lavfi",
                "ssim",
                "-f",
                "null",
                "-",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        match = SSIM_PATTERN.search(result.stderr)
        if match is None:
            raise RuntimeError("ffmpeg did not report an All: SSIM value")
        return float(match.group(1))


def inspect_video(path: Path, args: argparse.Namespace) -> dict[str, object]:
    metadata = ffprobe(path)
    streams = metadata.get("streams", [])
    video_streams = [stream for stream in streams if stream.get("codec_type") == "video"]
    audio_streams = [stream for stream in streams if stream.get("codec_type") == "audio"]
    issues: list[str] = []
    if not video_streams:
        return {
            "path": str(path),
            "kind": "video",
            "issues": ["no video stream"],
            "pass": False,
        }

    stream = video_streams[0]
    width = int(stream.get("width", 0))
    height = int(stream.get("height", 0))
    duration_raw = metadata.get("format", {}).get("duration") or stream.get("duration")
    duration = float(duration_raw) if duration_raw is not None else None
    frame_rate_raw = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1"
    try:
        frame_rate = float(Fraction(frame_rate_raw))
    except (ValueError, ZeroDivisionError):
        frame_rate = None

    if args.expected_video_size and (width, height) != args.expected_video_size:
        issues.append(
            f"video size {width}x{height}, expected {args.expected_video_size[0]}x{args.expected_video_size[1]}"
        )
    if args.target_duration is not None:
        if duration is None or abs(duration - args.target_duration) > args.duration_tolerance:
            issues.append(
                f"duration {duration}, expected {args.target_duration} ± {args.duration_tolerance}"
            )
    if args.expect_audio == "silent" and audio_streams:
        issues.append("audio stream present but silent delivery was requested")
    if args.expect_audio == "present" and not audio_streams:
        issues.append("audio stream missing")

    ssim = None
    if args.loop_ssim:
        ssim = calculate_ssim(path, args.last_offset)
        if ssim < args.min_loop_ssim:
            issues.append(f"first/last SSIM {ssim:.6f} below {args.min_loop_ssim}")

    return {
        "path": str(path),
        "kind": "video",
        "size": [width, height],
        "codec": stream.get("codec_name"),
        "pixel_format": stream.get("pix_fmt"),
        "duration": duration,
        "frame_rate": round(frame_rate, 6) if frame_rate is not None else None,
        "audio_streams": len(audio_streams),
        "first_last_ssim": round(ssim, 6) if ssim is not None else None,
        "issues": issues,
        "pass": not issues,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--expected-image-size", type=parse_size)
    parser.add_argument("--expected-video-size", type=parse_size)
    parser.add_argument("--require-alpha", action="store_true")
    parser.add_argument(
        "--expect-audio", choices=("any", "silent", "present"), default="any"
    )
    parser.add_argument("--target-duration", type=float)
    parser.add_argument("--duration-tolerance", type=float, default=0.15)
    parser.add_argument("--loop-ssim", action="store_true")
    parser.add_argument("--min-loop-ssim", type=float, default=0.95)
    parser.add_argument(
        "--last-offset",
        type=float,
        default=0.25,
        help="tail window decoded in reverse to select the exact final frame",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.duration_tolerance < 0 or args.last_offset <= 0:
        raise SystemExit("duration tolerance must be non-negative and last offset positive")
    if not 0.0 <= args.min_loop_ssim <= 1.0:
        raise SystemExit("--min-loop-ssim must be between 0 and 1")

    files = collect(args.inputs)
    if not files:
        raise SystemExit("no PNG or supported video files found")

    results: list[dict[str, object]] = []
    fatal_errors: list[str] = []
    for path in files:
        try:
            if path.suffix.lower() in IMAGE_EXTENSIONS:
                results.append(
                    inspect_image(path, args.expected_image_size, args.require_alpha)
                )
            else:
                results.append(inspect_video(path, args))
        except Exception as exc:
            fatal_errors.append(f"{path}: {exc}")
            results.append(
                {
                    "path": str(path),
                    "kind": "unknown",
                    "issues": [str(exc)],
                    "pass": False,
                }
            )

    failed = [item for item in results if not item.get("pass")]
    report = {
        "summary": {
            "files": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "images": sum(item.get("kind") == "image" for item in results),
            "videos": sum(item.get("kind") == "video" for item in results),
        },
        "results": results,
        "fatal_errors": fatal_errors,
    }
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
