#!/usr/bin/env python3
"""Resolve a composable avatar-IP selection into a stage-specific prompt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = SKILL_ROOT / "assets" / "templates" / "ip-template-catalog.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selection", type=Path, help="project ip-template-selection JSON")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument(
        "--stage",
        choices=("concept", "neutral-base", "signature-look", "complete-character", "scene"),
        help="override selection.stage",
    )
    parser.add_argument("--output", type=Path, help="write prompt text; stdout when omitted")
    parser.add_argument("--resolved-output", type=Path, help="write resolved JSON receipt")
    return parser


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"expected a JSON object: {path}")
    return value


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{label} must be a non-empty string")
    return value.strip()


def main() -> int:
    args = build_parser().parse_args()
    catalog = load_json(args.catalog)
    selection = load_json(args.selection)
    stage = args.stage or require_text(selection.get("stage"), "selection.stage")

    stage_overrides = catalog.get("stage_overrides", {})
    if stage not in stage_overrides:
        raise SystemExit(f"unknown stage: {stage}")
    stage_rule = stage_overrides[stage]
    selected = selection.get("selected")
    if not isinstance(selected, dict):
        raise SystemExit("selection.selected must be an object")

    resolved_ids = dict(selected)
    forced = stage_rule.get("forced", {})
    if not isinstance(forced, dict):
        raise SystemExit(f"catalog stage {stage} forced field must be an object")
    resolved_ids.update(forced)

    dimensions = catalog.get("dimensions", {})
    blocks: list[dict[str, str]] = []
    avoid: list[str] = []
    for dimension in stage_rule.get("include", []):
        option_id = resolved_ids.get(dimension)
        if not isinstance(option_id, str) or not option_id:
            raise SystemExit(f"missing selected template ID: {dimension}")
        options = dimensions.get(dimension, {}).get("options", {})
        if option_id not in options:
            valid = ", ".join(sorted(options))
            raise SystemExit(f"unknown {dimension} ID {option_id!r}; valid: {valid}")
        option = options[option_id]
        block = require_text(option.get("prompt_block"), f"{dimension}.{option_id}.prompt_block")
        blocks.append({"dimension": dimension, "id": option_id, "text": block})
        for item in option.get("avoid", []):
            if isinstance(item, str) and item not in avoid:
                avoid.append(item)

    identity = selection.get("identity", {})
    if not isinstance(identity, dict):
        raise SystemExit("selection.identity must be an object")
    identity_parts: list[str] = []
    for key in ("visual_age", "skin_tone", "eye_details"):
        value = identity.get(key)
        if isinstance(value, str) and value.strip():
            identity_parts.append(f"{key.replace('_', ' ')}: {value.strip()}")
    for key in ("distinctive_features", "personality_cues"):
        value = identity.get(key, [])
        if isinstance(value, list) and value:
            identity_parts.append(f"{key.replace('_', ' ')}: {', '.join(str(item) for item in value)}")

    use_case = require_text(selection.get("use_case"), "selection.use_case")
    stage_details = selection.get("stage_details", {})
    if not isinstance(stage_details, dict):
        raise SystemExit("selection.stage_details must be an object")
    custom_blocks = selection.get("custom_prompt_blocks", [])
    custom_exclusions = selection.get("custom_exclusions", [])
    if not isinstance(custom_blocks, list) or not isinstance(custom_exclusions, list):
        raise SystemExit("custom prompt blocks and exclusions must be arrays")

    lines = [
        f"Use case: {use_case}",
        f"Asset stage: {stage}",
        f"Persona: {selection.get('persona_id', 'p01')}",
        "",
        "Identity contract:",
        "; ".join(identity_parts) if identity_parts else "Preserve the approved project identity source exactly.",
        "",
        "Resolved template blocks:",
    ]
    for block in blocks:
        lines.append(f"- [{block['dimension']}={block['id']}] {block['text']}")
    lines.extend(["", "Stage rule:", require_text(stage_rule.get("prompt_block"), f"stage {stage} prompt_block")])

    if stage == "signature-look" and stage_details.get("signature_source_description"):
        lines.extend(["", "Signature source construction:", str(stage_details["signature_source_description"])])
    if stage == "scene":
        action = str(stage_details.get("scene_action", "")).strip()
        background = str(stage_details.get("background_contract", "")).strip()
        if action:
            lines.extend(["", "Scene action:", action])
        if background:
            lines.extend(["", "Background contract:", background])
    if custom_blocks:
        lines.extend(["", "Project-specific blocks:"])
        lines.extend(f"- {str(item)}" for item in custom_blocks if str(item).strip())

    for item in catalog.get("global_avoid", []):
        if isinstance(item, str) and item not in avoid:
            avoid.append(item)
    for item in custom_exclusions:
        text = str(item).strip()
        if text and text not in avoid:
            avoid.append(text)
    lines.extend(["", "Avoid:", ", ".join(avoid) + "."])
    prompt = "\n".join(lines).rstrip() + "\n"

    resolved = {
        "schema_version": "1.0",
        "project": selection.get("project", "avatar-ip-project"),
        "persona_id": selection.get("persona_id", "p01"),
        "stage": stage,
        "selected_original": selected,
        "forced_by_stage": forced,
        "selected_resolved": {key: resolved_ids[key] for key in stage_rule.get("include", [])},
        "prompt_blocks": blocks,
        "avoid": avoid,
        "prompt": prompt,
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(prompt, encoding="utf-8")
    else:
        print(prompt, end="")
    if args.resolved_output:
        args.resolved_output.parent.mkdir(parents=True, exist_ok=True)
        args.resolved_output.write_text(
            json.dumps(resolved, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
