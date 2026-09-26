#!/usr/bin/env python3
"""Validate the public produce-avatar-ip-system repository package."""

from __future__ import annotations

import ast
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "produce-avatar-ip-system"
EXPECTED_NAME = "produce-avatar-ip-system"
EXPECTED_VERSION = "1.0.0"

REQUIRED_FILES = [
    "SKILL.md",
    "LICENSE.md",
    "NOTICE.md",
    "README.md",
    "README.zh.md",
    "agents/openai.yaml",
    "assets/templates/asset-manifest.csv",
    "assets/templates/avatar-project-brief.yaml",
    "assets/templates/h3-max-loop-input.example.json",
    "assets/templates/prompt-contract.yaml",
    "references/asset-contract.md",
    "references/capability-selection.md",
    "references/figma-system.md",
    "references/io-contract.md",
    "references/portability-and-readiness.md",
    "references/prompt-templates.md",
    "references/qa-and-recovery.md",
    "references/style-presets.md",
    "references/tool-provenance.md",
    "references/tool-routing.md",
    "references/workflow.md",
    "scripts/build_review_sheet.py",
    "scripts/inspect_avatar_delivery.py",
    "scripts/normalize_avatar_png.py",
]

REQUIRED_MANIFEST_COLUMNS = {
    "asset_id",
    "stage",
    "persona",
    "style_version",
    "source_reference",
    "prompt_revision",
    "tool_surface",
    "action",
    "provider_model",
    "request_id",
    "figma_node_id",
    "qa_status",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def markdown_links(path: Path) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    if ROOT.name != EXPECTED_NAME:
        errors.append(f"package folder must be {EXPECTED_NAME!r}")

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = ROOT / "SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(skill)
        if frontmatter.get("name") != EXPECTED_NAME:
            errors.append("SKILL.md frontmatter name does not match package")
        if frontmatter.get("version") != EXPECTED_VERSION:
            errors.append(
                f"SKILL.md metadata version must be {EXPECTED_VERSION}, "
                f"got {frontmatter.get('version')!r}"
            )
        for required in (
            "Required approval stops",
            "portability-and-readiness.md",
            "tool-provenance.md",
            "Codex `image_gen`",
            "do not expose a concrete GPT Image model ID",
        ):
            if required not in skill:
                errors.append(f"SKILL.md missing required contract text: {required}")

    for md in ROOT.rglob("*.md"):
        for target in markdown_links(md):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            if not (md.parent / target_path).resolve().exists():
                errors.append(
                    f"broken relative link in {md.relative_to(ROOT)}: {target}"
                )

    text_extensions = {".md", ".yaml", ".yml", ".json", ".csv", ".py"}
    secret_patterns = {
        "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        "GitHub token": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
        "Google key": re.compile(r"\bAIza[A-Za-z0-9_-]{20,}\b"),
        "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in text_extensions:
            continue
        body = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"/Users/[^/]+/|[A-Za-z]:\\Users\\", body):
            errors.append(f"machine-specific user path in {path.relative_to(ROOT)}")
        if "figma.com/design/" in body:
            errors.append(f"source Figma design URL leaked in {path.relative_to(ROOT)}")
        for label, pattern in secret_patterns.items():
            if pattern.search(body):
                errors.append(f"{label} found in {path.relative_to(ROOT)}")

    provenance = ROOT / "references/tool-provenance.md"
    if provenance.is_file():
        body = provenance.read_text(encoding="utf-8")
        for required in (
            "66",
            "OpenAI Media Service API",
            "model ID not exposed",
            "fal-ai/nano-banana-2",
            "bytedance/seedream/v5/pro/text-to-image",
            "fal-ai/kling-video/v3/pro/image-to-video",
            "minimax/h3-max/image-to-video",
        ):
            if required not in body:
                errors.append(f"tool provenance missing {required!r}")

    json_path = ROOT / "assets/templates/h3-max-loop-input.example.json"
    if json_path.is_file():
        try:
            request = json.loads(json_path.read_text(encoding="utf-8"))
            if request.get("model") != "minimax/h3-max/image-to-video":
                errors.append("H3 Max example does not pin the expected endpoint")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid H3 Max example JSON: {exc}")

    manifest_path = ROOT / "assets/templates/asset-manifest.csv"
    if manifest_path.is_file():
        with manifest_path.open(encoding="utf-8", newline="") as handle:
            header = set(next(csv.reader(handle), []))
        missing = sorted(REQUIRED_MANIFEST_COLUMNS - header)
        if missing:
            errors.append(f"asset manifest missing columns: {', '.join(missing)}")

    for script in (ROOT / "scripts").glob("*.py"):
        try:
            ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
        except SyntaxError as exc:
            errors.append(f"Python syntax error in {script.name}: {exc}")

    for script in (
        "normalize_avatar_png.py",
        "build_review_sheet.py",
        "inspect_avatar_delivery.py",
    ):
        path = ROOT / "scripts" / script
        if not path.is_file():
            continue
        result = subprocess.run(
            [sys.executable, str(path), "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            errors.append(
                f"{script} --help failed: {(result.stderr or result.stdout).strip()}"
            )

    print(f"validate_package: root={ROOT}")
    print(f"required_files={len(REQUIRED_FILES)}")
    if errors:
        print(f"FAIL ({len(errors)} error(s))")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
