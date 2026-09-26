# Agent operating contract

This repository contains a portable Agent Skill. Load the package directory `produce-avatar-ip-system/`, not this file alone.

## Read first

1. `produce-avatar-ip-system/SKILL.md`
2. `references/portability-and-readiness.md`
3. `references/io-contract.md`
4. The mode-specific references routed from `SKILL.md`

## Rules that do not change per host

- Preserve the four separate approval boundaries: base IP, modular combinations, editable scenes, and representative motion before batching.
- Never guess an unexposed image model ID. “Image 2.5” is not a generic name.
- Use an exact external endpoint only after live capability/schema discovery and preflight.
- Keep identity, style, presentation, scene, background, and motion as separate contracts.
- Do not claim fake alpha, editable Figma state, playable video, or completed batches without verification.
- Do not publish source Figma links, user artwork, credentials, signed URLs, or request payload secrets.
- Application-code integration and pull requests are outside this Skill.

## Validate

From the repository root:

```bash
python3 scripts/validate_package.py
```
