# Produce Avatar IP System Skill

This directory is the portable Agent Skill package. It turns an informal avatar or digital-employee idea into an approval-gated, reusable IP system with identity masters, palettes, outfits, wearables, props, combination renders, editable scenes, and optional loop videos.

Start with [`SKILL.md`](SKILL.md). The required execution and approval contract is in [`portability-and-readiness.md`](references/portability-and-readiness.md); exact historical tool/model evidence is in [`tool-provenance.md`](references/tool-provenance.md).

The package is designed for capability-based routing across Codex, Claude Code, Cursor, OpenCode, and other hosts that support filesystem Agent Skills. Host-specific tools are optional: missing ImageGen, Figma, Aident, Pillow, or FFmpeg must produce an explicit partial/blocked state rather than a false completion claim.

Install with:

```bash
npx skills add Edward-J-create/produce-avatar-ip-system \
  --skill produce-avatar-ip-system
```

License: MIT. No source character artwork or private Figma file is bundled.
