# Produce Avatar IP System Skill

This directory is the portable Agent Skill package. It turns an informal avatar or digital-employee idea into an approval-gated, reusable IP system with identity masters, palettes, outfits, wearables, props, combination renders, editable scenes, and optional loop videos.

Start with [`SKILL.md`](SKILL.md). The required execution and approval contract is in [`portability-and-readiness.md`](references/portability-and-readiness.md); exact historical tool/model evidence is in [`tool-provenance.md`](references/tool-provenance.md).

The package is designed for capability-based routing across Codex, Claude Code, Cursor, OpenCode, and other hosts that support filesystem Agent Skills. Host-specific tools are optional: missing ImageGen, Figma, Aident, Pillow, or FFmpeg must produce an explicit partial/blocked state rather than a false completion claim.

Version 1.2 adds a real IP-template system rather than a fixed example character: machine-readable, independently selectable IDs for rendering style, head/body ratio, gender presentation, body construction, face shape, hair, outfit, wearable, prop, palette, and composition. A stage resolver produces reproducible prompts and forces the neutral-base gate back to a front-facing plain T-shirt with no prop or final styling. The representative-first identity and approval gates from 1.1 remain required.

Start a resumable project with:

```bash
python scripts/init_avatar_project.py ./my-avatar-project \
  --project-name my-avatar-project \
  --personas 4
```

Then resolve a stage prompt from the generated per-persona selection file:

```bash
python scripts/assemble_avatar_prompt.py \
  ./my-avatar-project/brief/ip-template-selection-p01.json \
  --catalog ./my-avatar-project/brief/ip-template-catalog.snapshot.json \
  --stage neutral-base
```

Install with:

```bash
npx skills add Edward-J-create/produce-avatar-ip-system \
  --skill produce-avatar-ip-system
```

The package has been smoke-tested through the public `skills` CLI for Codex, Claude Code, Cursor, and OpenCode. All hosts load the same `SKILL.md`, relative references, templates, and scripts. The optional `agents/openai.yaml` improves OpenAI-hosted discovery but is not required by other agents.

License: MIT. No source character artwork or private Figma file is bundled.
