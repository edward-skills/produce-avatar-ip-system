# Produce Avatar IP System

An open, cross-agent Skill for turning a user's idea into a reusable avatar or digital-employee IP system: approved identity masters, palettes, outfits, wearables, props, combination renders, editable scenes, and loop-video production packages.

The workflow is approval-gated. It does not jump from a one-line idea directly into an uncontrolled batch:

1. Base-IP directions and identity approval.
2. Palette, outfit, prop, wearable, and combination approval.
3. Transparent scene subjects, editable backgrounds, and scene approval.
4. One representative animation, then approval before video batching.

## What is packaged

| Layer | Included |
| --- | --- |
| Agent entrypoint | `produce-avatar-ip-system/SKILL.md` |
| Style controls | Cute, chibi/Q, stylized 3D, semi-real, realistic, and custom versioned presets |
| Prompt system | Identity, wearable, outfit, prop, scene, correction, background, and motion templates |
| Production contracts | Intake brief, prompt contract, asset manifest, approval state machine, and QA gates |
| Tool routing | Codex/OpenAI host ImageGen, Aident/Fal discovery and execution, Figma organization, Pillow, FFmpeg/ffprobe |
| Helpers | PNG alpha/canvas normalization, contact-sheet generation, static/video delivery inspection |

No private source artwork, source Figma file, credentials, signed URLs, or generated client assets are included.

## Cross-agent installation

The portable package is [`produce-avatar-ip-system/`](produce-avatar-ip-system/).

```bash
npx skills add Edward-J-create/produce-avatar-ip-system \
  --skill produce-avatar-ip-system
```

Install globally for the agents already configured on a machine:

```bash
npx skills add Edward-J-create/produce-avatar-ip-system \
  --skill produce-avatar-ip-system \
  --global \
  --agent codex claude-code cursor opencode \
  --yes
```

Manual install: copy the complete `produce-avatar-ip-system/` directory to a supported skill directory such as `~/.agents/skills/`, `~/.codex/skills/`, `~/.claude/skills/`, or `.cursor/skills/`. Hosts may ignore the optional Codex discovery metadata in `agents/openai.yaml`.

## Requirements

- An image-generation or image-editing capability for rendered assets.
- Python 3 and Pillow for the bundled static helpers.
- FFmpeg/ffprobe for video contact sheets, inspection, transcode, and loop SSIM.
- Optional: an authorized Figma connector for editable component organization.
- Optional: Aident Loadout with an authorized provider connection for explicit external models such as Fal-hosted Seedream, Nano Banana, Kling, or MiniMax.

Missing optional capabilities produce a documented partial handoff; the Skill must not claim that an unrendered prompt, poster frame, or unmutated Figma file is a finished deliverable.

## Model provenance

The source case used 66 Codex `image_gen` calls for most approved static production. The host exposed `OpenAI Media Service API`, but not a concrete model ID. The repository therefore records those calls as:

```text
Codex image_gen / OpenAI host ImageGen (underlying model ID not exposed)
```

It does not rename them to GPT Image 2 or “Image 2.5.” Explicit external endpoints are recorded by their full provider IDs. See [`tool-provenance.md`](produce-avatar-ip-system/references/tool-provenance.md).

## Validate

```bash
python3 -m pip install Pillow
python3 scripts/validate_package.py
```

The validator checks the portable package structure, frontmatter, relative links, templates, model-provenance safeguards, Python syntax, helper CLIs, and accidental private-path/Figma-source leakage.

## License

MIT. Provider, product, and model names remain trademarks of their respective owners. Generated-asset rights and provider terms must be evaluated for each production job.
