---
name: produce-avatar-ip-system
description: Design and produce a reusable avatar or digital-employee IP system across cute, chibi, stylized 3D, semi-real, or realistic directions, including identity masters, modular outfits and props, editable backgrounds, scene variants, loop videos, Figma components, manifests, and production QA. Use for character-system creation or refinement; do not use for application-code integration, pull requests, or product UI implementation.
metadata:
  version: "1.0.0"
  license: MIT
  repository: https://github.com/Edward-J-create/produce-avatar-ip-system
---

# Produce Avatar IP System

Turn a visual brief into a coherent character system rather than a pile of unrelated generations. Preserve approved identities and art direction while varying only the intended axis: palette, outfit, prop, background, scene, pose, expression, or motion.

## Scope boundary

This skill ends at reviewed source assets, Figma organization, prompt documentation, manifests, QA reports, and delivery packages. Do not edit application code, create branches, commit, push, open a pull request, or implement product UI under this skill. Treat later product integration as a separate task with separate authorization.

## Required routing

1. Read [references/io-contract.md](references/io-contract.md) for intake, inputs, stage outputs, and delivery structure.
2. Read [references/portability-and-readiness.md](references/portability-and-readiness.md) before starting. It defines the approval stops, capability fallbacks, handoff state, and cross-agent acceptance tests.
3. Read [references/style-presets.md](references/style-presets.md) whenever choosing or changing cute, chibi, stylized, semi-real, or realistic direction. A style change versions the identity contract; it is not a suffix appended to every prompt.
4. Read [references/workflow.md](references/workflow.md) and [references/asset-contract.md](references/asset-contract.md) before multiplying variants.
5. Read [references/prompt-templates.md](references/prompt-templates.md) for static or motion generation.
6. Read [references/tool-provenance.md](references/tool-provenance.md) whenever the user asks which tools/models were used, requests the source Aident workflow, or wants exact model/action IDs.
7. Read [references/capability-selection.md](references/capability-selection.md) and [references/tool-routing.md](references/tool-routing.md) before external generation, Figma mutation, or paid batch work.
8. Read [references/figma-system.md](references/figma-system.md) when using Figma or adapting the source Vertical Agents file.
9. Apply [references/qa-and-recovery.md](references/qa-and-recovery.md) before approval, batching, replacement, or packaging.

## Operating invariants

- Separate `identity`, `style`, `presentation`, `scene`, `background`, and `motion`. Lock each upstream layer before multiplying downstream variants.
- Treat the user's latest approved high-resolution source as the identity source of truth. Never continue editing a degraded derivative.
- Keep an acceptance ledger: approved direction, style preset and version, persona IDs, exact references, matrix axes, anchors, target Figma nodes, formats, budget, active corrections, superseded feedback, and explicit non-goals.
- Change one axis at a time. A phone correction must not change the face, hairstyle, skin tone, outfit, crop, lighting, or background.
- Generate real 3D/raster character material with an image model. Use Figma to organize, compose, document, expose variants, and keep backgrounds editable—not to fake the 3D character with flat vectors.
- Deliver the subject and background separately whenever replacement is required: transparent subject master, editable background plate/token, and a composed preview/card.
- Do not assume a checkerboard is transparency. Verify alpha, corners, edge matte, and hidden RGB.
- Define held objects physically: front/back planes, hinges, labels, screens, grip, and which hand touches which surface.
- Verify a Figma node after every upload or replacement by fill/hash and a fresh screenshot. Upload success alone does not prove application.
- Do not add logos, symbols, text, halos, or brand marks unless requested.

## Production sequence

1. Fill or adapt `assets/templates/avatar-project-brief.yaml`; infer only low-risk omissions and show the user the proposed matrix before a paid or large batch.
2. Explore 2–3 materially different style directions or accept the user's existing approved reference. Select one style preset and version its style/material lock.
3. Define persona IDs, visual anchors, palette roles, asset families, editable-background strategy, Figma targets, formats, and naming.
4. Approve identity masters first, then upper bodies, native wearables, standalone outfits/props, complete characters, scene renders, background plates/cards, and motion—in that order.
5. Generate contact sheets at every matrix stage and review at both detail size and real product size.
6. For motion, validate one failure-prone representative scene before batching. Use a true first-frame field; when supported, use the same approved frame as the end frame.
7. Organize approved assets in the supplied Figma target. Preserve confirmed nodes and update in place unless the user asks for a new page/library.
8. Package only approved assets with `assets/templates/asset-manifest.csv`, prompt/model revisions, contact sheets, and a QA report.

## Required approval stops

This is an approval-gated pipeline, not a one-shot generation prompt:

1. Start from the user's own idea, even when it is only a short sentence. Propose safe defaults and 2–3 visibly different base-IP directions; stop for direction and identity approval.
2. From the approved base IP only, produce the palette, outfit, prop, wearable, and requested combination sample/matrix; stop for modular-system approval.
3. From the approved combination sources only, produce transparent scene subjects, editable backgrounds, and composed previews; stop for scene approval.
4. From an approved composed scene frame, produce and inspect one representative animation; stop for motion approval before the remaining video batch.
5. Deliver only after the promised matrix, provenance log, Figma/package state, and QA report all agree.

Approval of one stage does not silently approve later stages, a larger paid batch, or a different style version. Another agent must be able to resume from the brief, prompt contract, acceptance ledger, manifest, and approved files without depending on chat memory.

## Real tools and model truth

The source workflow did not use one model for everything. Its raw task log contains 66 Codex `image_gen` calls for concept, identity, modular, scene, and correction work. Those results identify the OpenAI host media service but do not expose a concrete GPT Image model ID. It also used Fal through Aident for model comparison and video, Figma for component organization, local Pillow/FFmpeg for deterministic media work, and Fal MiniMax H3 Max for the final 20-loop batch. The exact historical actions, endpoint IDs, and counts are in [references/tool-provenance.md](references/tool-provenance.md).

Never rewrite an unexposed host model as a guessed name such as “Image 2.5.” Record `OpenAI host ImageGen` unless the result reports a concrete ID. Conversely, when an external endpoint is explicit, record the complete ID such as `minimax/h3-max/image-to-video`.

Provider catalogs, schemas, and prices change. Use the installed Aident router for external capabilities, list current models, inspect the live schema, preflight exact input/cost, and then execute one representative sample. A timeout is an unknown result; check audit/history before resubmitting.

## Bundled resources

- `assets/templates/avatar-project-brief.yaml`: reusable intake and matrix template.
- `assets/templates/prompt-contract.yaml`: versioned style, identity, composition, background, and motion locks.
- `assets/templates/asset-manifest.csv`: delivery/provenance manifest columns.
- `assets/templates/h3-max-loop-input.example.json`: proven first/end-frame request shape; replace all IDs and verify the live schema.
- `references/portability-and-readiness.md`: agent-neutral capability detection, approval gates, resume state, and release acceptance tests.
- `scripts/normalize_avatar_png.py`: key a uniform background or reuse alpha, then normalize the subject canvas.
- `scripts/build_review_sheet.py`: create labeled contact sheets from static images or representative video frames.
- `scripts/inspect_avatar_delivery.py`: inspect alpha/dimensions and video dimensions, duration, audio, frame rate, and optional first/last SSIM.

Run helpers with `--help`. Write candidates, reports, and previews to a task-specific output directory; never overwrite the last approved source before the replacement passes.
