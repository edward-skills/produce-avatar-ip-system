#!/usr/bin/env python3
"""Initialize a resumable avatar-IP project from the bundled contracts."""

from __future__ import annotations

import argparse
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "assets" / "templates"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="task-specific output directory")
    parser.add_argument("--project-name", default="avatar-ip-project")
    parser.add_argument("--personas", type=int, default=1)
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite scaffold files but never generated/approved media",
    )
    return parser


def write_from_template(source: Path, target: Path, replacements: dict[str, str], force: bool) -> None:
    if target.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing scaffold: {target}")
    body = source.read_text(encoding="utf-8")
    for old, new in replacements.items():
        body = body.replace(old, new)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    if args.personas <= 0 or args.personas > 32:
        raise SystemExit("--personas must be between 1 and 32")

    output = args.output.resolve()
    for relative in (
        "brief",
        "sources/identity",
        "sources/style",
        "sources/outfit",
        "sources/prop",
        "sources/background",
        "approved/identity",
        "approved/upper-body",
        "approved/signature-look",
        "approved/wearable",
        "approved/outfit",
        "approved/complete-character",
        "approved/scene-subject",
        "approved/background",
        "approved/scene-card",
        "approved/motion",
        "candidates",
        "review/contact-sheets",
        "review/frames",
        "review/qa",
        "manifests",
        "delivery",
    ):
        (output / relative).mkdir(parents=True, exist_ok=True)

    replacements = {
        "name: avatar-ip-project": f"name: {args.project_name}",
        "project: avatar-ip-project": f"project: {args.project_name}",
        '"project": "avatar-ip-project"': f'"project": "{args.project_name}"',
    }
    template_map = {
        "avatar-project-brief.yaml": output / "brief/avatar-project-brief.yaml",
        "ip-template-catalog.json": output / "brief/ip-template-catalog.snapshot.json",
        "prompt-contract.yaml": output / "brief/prompt-contract.yaml",
        "reference-role-map.yaml": output / "brief/reference-role-map.yaml",
        "modular-system-contract.yaml": output / "brief/modular-system-contract.yaml",
        "approval-receipt.yaml": output / "review/approval-receipt-base_ip_review.yaml",
        "acceptance-ledger.md": output / "review/acceptance-ledger.md",
        "asset-manifest.csv": output / "manifests/asset-manifest.csv",
    }
    for template, target in template_map.items():
        write_from_template(TEMPLATES / template, target, replacements, args.force)

    brief_path = output / "brief/avatar-project-brief.yaml"
    brief = brief_path.read_text(encoding="utf-8")
    before, marker, remainder = brief.partition("personas:\n")
    _old_personas, framing_marker, after = remainder.partition("\nframing:\n")
    if not marker or not framing_marker:
        raise RuntimeError("avatar-project-brief template is missing personas/framing sections")
    persona_lines: list[str] = []
    for index in range(1, args.personas + 1):
        persona_id = f"p{index:02d}"
        persona_lines.extend(
            [
                f"  - id: {persona_id}",
                '    immutable_identity: ""',
                '    approved_source: ""',
                f"    contract: brief/persona-{persona_id}.yaml",
                f"    template_selection: brief/ip-template-selection-{persona_id}.json",
                f"    anchor: {'true' if index == 1 else 'false'}",
            ]
        )
    brief_path.write_text(
        before
        + "personas:\n"
        + "\n".join(persona_lines)
        + "\n\nframing:\n"
        + after,
        encoding="utf-8",
    )

    persona_template = TEMPLATES / "persona-contract.yaml"
    selection_template = TEMPLATES / "ip-template-selection.example.json"
    for index in range(1, args.personas + 1):
        persona_id = f"p{index:02d}"
        write_from_template(
            persona_template,
            output / f"brief/persona-{persona_id}.yaml",
            {
                "persona_id: p01": f"persona_id: {persona_id}",
                "anchor_persona: true": f"anchor_persona: {'true' if index == 1 else 'false'}",
                "source: brief/ip-template-selection-p01.json": f"source: brief/ip-template-selection-{persona_id}.json",
            },
            args.force,
        )
        write_from_template(
            selection_template,
            output / f"brief/ip-template-selection-{persona_id}.json",
            {
                '"project": "avatar-ip-project"': f'"project": "{args.project_name}"',
                '"persona_id": "p01"': f'"persona_id": "{persona_id}"',
            },
            args.force,
        )

    generation_log = output / "manifests/generation-log.jsonl"
    if not generation_log.exists():
        generation_log.touch()
    elif args.force:
        # Keep provenance history even when refreshing scaffold files.
        pass

    print(f"OK\t{output}\tpersonas={args.personas}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
