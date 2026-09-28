# Portability and Readiness Contract

This file defines when the skill is ready for another user and another capable agent. It is agent-neutral: a tool name is historical evidence or a routing hint, never an assumption that every host exposes the same surface.

## Cross-agent discovery contract

- The portable entrypoint is the package-root `SKILL.md`. Codex, Claude Code, Cursor, OpenCode, and other filesystem-Skill hosts must load the same entrypoint and relative resources.
- `agents/openai.yaml` is optional OpenAI UI metadata, not a runtime dependency. A host that ignores it must still be able to execute the complete workflow from `SKILL.md`.
- Keep every package link relative. Never require the original repository checkout, a machine-specific absolute path, chat history, or a Codex-only tool name to read the workflow.
- Route by capability: image generation/editing, external model discovery, Figma mutation, raster processing, and video inspection. If a host lacks one capability, preserve upstream outputs and record an honest partial handoff.
- A cross-agent release must pass package discovery and copy-install with the public `skills` CLI for at least Codex, Claude Code, Cursor, and OpenCode, plus the readiness scenarios below. Installation success does not replace behavioral or media QA.

## Start from a freeform idea

Accept a short input such as “做一个可靠但可爱的财务数字员工，绿色系，后面要做提醒和成功动画.” Do not require the user to fill every field before work starts.

1. Run `../scripts/init_avatar_project.py` or copy the project brief, template catalog, and one template-selection file per persona into a task-specific output directory.
2. Extract the concept, audience, use case, desired personality, explicit style words, colors, prohibited motifs, persona count, and requested deliverables.
3. Propose low-risk defaults for missing presentation details. Mark them as proposals, not user facts.
4. If style is underspecified, offer 2–3 materially different parameter stacks from `ip-template-system.md`; label every differing template ID. Avoid changing only adjectives while keeping the same visual direction.
5. Produce the smallest reviewable sample at each stage before multiplying a matrix or spending on a batch. For base IP, this means one anchor persona shown as source + neutral construction master + signature-look validation when applicable.

## Non-negotiable stage machine

| State | Produce | Required evidence | Transition |
| --- | --- | --- | --- |
| `idea_received` | Filled brief and proposed matrix | User idea plus stated assumptions | Generate 2–3 base directions |
| `base_ip_review` | Concept sheet; anchor source/neutral/signature review; then cast candidates | Axis-scoped approval receipt, style/material lock, identity/body anchors | User approves the anchor pair and then each persistent identity |
| `modular_review` | Palette tokens, outfits, wearables, props, and representative combinations | Only approved identity sources were used | User approves the modular system/matrix |
| `scene_review` | Transparent scene subjects, separate editable backgrounds, composed previews | Alpha/background checks and scene contact sheet | User approves scenes and source frames |
| `motion_review` | One representative loop plus first/mid/last frames and technical report | Exact model/action and true first-frame fields | User approves the representative motion and batch budget |
| `batch_review` | Remaining approved static/video matrix | Counts, provenance, visual and technical QA | User approves final package |
| `delivered` | Figma/package output, manifest, prompt contract, generation log, QA report | All promised files agree with approvals | End |

Never infer a transition from tool success. Only explicit user approval, or an already supplied approved source, advances a review state.

## Capability detection and honest fallbacks

At the start of a run, inventory the available capabilities without generating paid/batch output:

| Capability needed | Preferred route | Portable fallback |
| --- | --- | --- |
| Static generation/editing | Host image-generation tool such as Codex `image_gen` | Use an explicit external image action discovered through the available router/provider; otherwise return prompts and the production plan, marked unrendered |
| Named external model | Aident Loadout search → schema/model list → preflight → execute | Use a direct provider only when authorized and available; never silently substitute a different model |
| Editable system board | Authorized Figma connector/MCP | Deliver organized files, semantic naming, manifest, and a Figma placement/component plan; mark Figma mutation pending |
| Alpha/canvas/contact sheets | Bundled scripts with Python/Pillow | Preserve source files and report the missing dependency; do not claim verified transparency |
| Video inspection/transcode | `ffprobe` and `ffmpeg` | Deliver provider output plus an unverified technical-status note; do not claim codec/loop compliance |
| Motion generation | Explicit live image-to-video endpoint with true first-frame support | Deliver approved scene frames and motion prompts/JSON as a production-ready kit, marked unrendered |

Tool absence may narrow delivery, but it must not corrupt provenance. Do not call an external model “Codex ImageGen,” do not call Codex ImageGen “Image 2.5,” and do not claim a poster is an editable Figma/video asset.

## Cross-agent handoff state

Keep these files current so work can move between agents without replaying chat history:

- `brief/avatar-project-brief.yaml`: requested scope, assumptions, matrix, budget, and targets;
- `brief/ip-template-catalog.snapshot.json`: exact reusable option definitions used by this project;
- `brief/ip-template-selection-<id>.json`: independent style, proportion, presentation, body, face, hair, outfit, wearable, prop, palette, and composition selection for each persona;
- `brief/prompt-contract.yaml`: style, identity, composition, background, prop, and motion locks;
- `brief/reference-role-map.yaml`: source roles, precedence, known defects, and forbidden transfers;
- `brief/persona-<id>.yaml`: immutable face/hair identity, body construction, composition, and signature look;
- `manifests/generation-log.jsonl`: exact surface, action, model disclosure, request, prompt revision, inputs, cost, output, and QA state;
- `manifests/asset-manifest.csv`: logical asset IDs, files, variants, approval, provenance, and delivery status;
- an acceptance ledger: current state, approved source IDs, approved/rejected notes, active correction, and next allowed action;
- stage approval receipts: exact board, assets, axes, user wording, promotion, and next allowed action;
- `review/`: contact sheets, representative frames, technical reports, and QA result;
- `approved/` versus `candidates/`: never mix them.

Use paths relative to the task output directory in the package. External Figma node IDs or durable asset references may be recorded, but signed URLs, tokens, cookies, credentials, and machine-specific temporary paths may not.

## Model naming rules

1. Record the exact provider endpoint when the execution result exposes it.
2. If a host tool does not expose a model ID, record the surface plus `(model ID not exposed)`.
3. Treat `gemini-2.5-flash-image`, Nano Banana, Nano Banana Pro, Nano Banana 2, GPT Image, and any numbered Image model as distinct names. Never use one as a category label for another.
4. A C2PA/service generator string proves a service or issuer only; it does not prove an underlying model version.
5. Historical defaults are not current defaults. For every new external request, select an explicit live ID after schema inspection.

## Ready acceptance scenarios

The skill is ready only if another agent can satisfy all of these without the source thread:

1. **Sparse idea:** turn one sentence into a filled brief, reference-role map, 2–3 labeled parameter stacks, resolved prompt receipts, and a base-IP review checkpoint.
2. **Style switch:** change cute/chibi/stylized/semi-real/realistic by versioning the style contract and regenerating the identity master before derivatives.
3. **Anchor identity:** preserve one supplied person through a resolver-forced front-facing neutral construction master and signature-look validation without conflating identity, camera, clothing, presentation, or body geometry.
4. **Modular expansion:** from the approved anchor/cast, reconstruct the signature outfit before making palette, derived outfit, wearable, prop, and combination assets without identity drift.
5. **Editable scene:** deliver a clean transparent subject, a separately replaceable background, and an exact composed preview.
6. **Motion:** animate only an approved composed frame, validate one loop, and wait for approval before a paid/full batch.
7. **Provenance:** distinguish host ImageGen with an undisclosed model from explicit Aident/Fal endpoints.
8. **Resume:** continue from the acceptance ledger and approval receipts at the next unapproved stage without asking the user to repeat already recorded decisions.
9. **Graceful degradation:** when a capability is missing, deliver the valid upstream artifacts and clearly mark what remains pending instead of claiming completion.

Passing these scenarios means the workflow is reusable. It does not mean every agent has every connector or provider authorization; runtime capability and user approval must still be checked on each job.
