# Capability Selection and Aident Boundaries

This reference separates the creative model from the execution surface. Seedream, Nano Banana, Kling, and MiniMax may be hosted by Fal or another provider; Aident Loadout is the managed discovery, schema, credential, file, execution, pricing, and audit layer used to reach those external capabilities in the source workflow.

Provider catalogs and model IDs are time-sensitive. Search the live catalog and inspect the current schema before every new production run. The identifiers below document capabilities observed in the source workflow, not permanent API contracts.

Read [tool-provenance.md](tool-provenance.md) for the exact historical record and a dated live-catalog snapshot. Keep these truths separate:

- the source concept comparison included Nano Banana 2 and Seedream 5 Pro;
- most approved static production used host OpenAI ImageGen with no exposed model ID;
- “Gemini 2.5 Flash Image / original Nano Banana,” “Nano Banana Pro,” and “Nano Banana 2” are distinct selectable endpoints;
- never rename a historical output to a newer model family because the names sound related.

## Decision table

| Need | Preferred capability | Aident needed? | Why / observed behavior | Switch when |
| --- | --- | ---: | --- | --- |
| Art-direction exploration | Codex built-in `image_gen` / OpenAI host ImageGen; use a GPT Image product/model name only when the result explicitly exposes it | No | Strong concept boards and visual editing with multiple supplied references; fastest path when already available in the host | Use an external model comparison when the direction is not converging or the user explicitly asks for one |
| Identity-preserving static edits | Codex built-in OpenAI ImageGen | No | The final static production in the source workflow used exact reference images plus narrow edits for heads, upper bodies, optical variants, outfits, complete characters, and scenes | Try a current external edit model if built-in edits cannot preserve the required material or anatomy |
| Discover current external image/video models | Aident Loadout capability search and model-list actions | Yes | Finds current Fal-hosted or other managed actions, required fields, pricing, and connection state without hard-coding a remembered model | Use a direct provider surface only when Aident lacks the action, is unavailable, or the user explicitly requests direct access |
| Neutral/light-anime concept generation | Seedream 5 Pro text-to-image through Fal | Yes in this workflow | Produced a strong culturally neutral, light-anime, bright-tech concept and followed the visual brief well | Do not assume it can create production layers or real alpha |
| Automatic layer extraction | Seedream 5 Pro Layerize through Fal | Yes in this workflow | Worth a one-asset experiment, but both complex-board and simplified-avatar tests failed in the source workflow | Fall back to separate reference-guided asset generation plus deterministic keying; do not retry the whole batch |
| Checklist-heavy reference editing | Nano Banana family through Fal; source comparison was labeled Nano Banana 2 | Yes in this workflow | Followed modular clothing/prop lists well and was useful for comparison | Select an explicit live endpoint; its requested transparent layer was a painted checkerboard in the source test, so verify alpha before reuse |
| First-frame-preserving expressive loop | Fal MiniMax H3 Max image-to-video | Yes in this workflow | Gave strong small-UI character/prop interaction and 1:1 loops after the true first-frame field was used | Switch if current schema lacks a true first/end frame, identity drifts, or target codec/alpha is unsupported |
| Alternative high-quality character motion | Fal Kling Video v3 Pro image-to-video | Yes in this workflow | Strong hands, phone interaction, synchronized glow, and very high first/last similarity in the representative sample | Higher cost and slower generation may favor H3 Max; transparent input became black and needed a composited background |
| Figma inspection and mutation | Authorized Figma connector/MCP | No | Reads nodes, creates component variants and prompt cards, replaces image fills, and verifies screenshots/hashes | Manual import may be required when the connector runtime cannot create video fills |
| External-provider input hosting | Aident managed file storage | Yes when the selected action requires a URL/asset ID | Creates upload URLs and managed asset IDs for local/Figma sources before Fal execution | Skip when the generation tool accepts local referenced paths directly |
| Alpha cleanup, normalization, contact sheets | Pillow/local scripts | No | Deterministic and cheap; catches fake checkerboards and standardizes a matrix | Regenerate if the source itself is blurred, structurally wrong, or contaminated; post-processing cannot repair identity |
| Video inspection/transcode/package | `ffprobe`, `ffmpeg`, archive tools | No | Confirms streams, resolution, duration, audio, first/last SSIM and creates WebM/MP4 delivery | Regenerate rather than transcode when hands, props, identity, or motion are wrong |

## Host ImageGen and model naming

Use the host's built-in image-generation/editing tool directly when the user asks for Codex/OpenAI image generation and that tool is available. If the user names a concrete GPT Image model or version, verify that the active tool exposes and can select that exact model; otherwise state that the host model is unresolved rather than claiming compliance. Record `Codex image_gen / OpenAI host ImageGen (model ID not exposed)` unless the result explicitly reports a model. “Image 2.5” is not a generic label for image generation, and it must never be inferred from output quality or from an OpenAI service marker. Do not route host ImageGen through Aident merely to make the pipeline uniform.

Built-in ImageGen is a good default for:

- initial concept boards;
- exact-reference identity creation;
- one-region corrections;
- native optical material variants;
- outfits and complete static scene assets.

Use Aident only if the user requests an external model comparison, the built-in capability is insufficient, or the desired model exists behind a managed external integration.

## Aident-required path

Use the installed Aident skill/router before calling external catalog actions. In the source workflow, Aident was used for:

1. Searching model capabilities and alternatives such as Nano Banana, Seedream, Midjourney, Fal image generation, layerization, and image-to-video.
2. Listing current Fal text-to-image, image-edit, and video models plus their live fields and pricing.
3. Uploading local/Figma media to managed temporary storage when the provider required a remote asset ID.
4. Preflighting input validity and exact/estimated cost.
5. Executing Seedream, Nano Banana, Kling, and MiniMax H3 Max actions.
6. Checking audit/history after a timeout so a paid request was not submitted twice.

Observed action names included:

```text
direct:fal:fal_list_text_to_image_models
direct:fal:fal_text_to_image
direct:fal:fal_list_image_edit_models
direct:fal:fal_edit_image
direct:fal:fal_list_image_to_video_models
direct:fal:fal_image_to_video
direct:file_storage_tools:file_create_upload_url
```

Treat those as search hints. Run live capability search and inspect the selected schema rather than assuming they still exist unchanged.

Typical Aident sequence:

```text
read installed aident-skill
→ capabilities search for the task/provider
→ inspect/list current models and fields
→ check managed connection state if required
→ upload approved source if a remote asset is required
→ preflight exact input and cost
→ execute one representative sample
→ record request/model/cost/output IDs
→ download and inspect locally
→ batch only after acceptance
```

## Source-workflow findings

These observations explain the production choices; they are not universal model rankings.

- Seedream 5 Pro was the best early external concept direction for a bright, neutral, light-anime digital employee.
- The Nano Banana 2 comparison followed modular inventory instructions well, but its “transparent PNG layer” baked a checkerboard into opaque pixels. This is evidence about that run, not every current Nano Banana endpoint.
- Seedream Layerize did not reliably split either a complex concept board or a simplified single avatar. Separate generation of heads, garments, prop+hand, and complete scenes was more reliable.
- Final static production moved to built-in OpenAI ImageGen because reference-guided editing and narrow corrections preserved approved identities more consistently.
- Kling v3 Pro produced a strong phone-interaction loop, but the transparent input became a black background and the sample had a nontrivial paid cost.
- MiniMax H3 Max initially redrew the character and changed aspect ratio when a weak reference field was used. After switching to the live schema's true first-frame field and using the same source for the end frame, it preserved identity and produced the final 20-loop batch.
- Midjourney was not found in the live Aident catalog during the source workflow. “Not found then” is not a permanent exclusion; search again if requested.

## Selection flow

```text
Need a static concept or controlled edit?
  → Use built-in OpenAI ImageGen first.

Need a named external model, comparison, or managed provider action?
  → Use Aident search → live schema → preflight → execute.

Need true character/prop motion?
  → Use Aident-managed image-to-video; test one first-frame-anchored sample.

Need reusable transparency?
  → Ask the generator for real alpha only as a test.
  → If false, use a uniform key background and local deterministic processing.

Need asset/component organization?
  → Use Figma directly; Aident is not the Figma layer.

Need technical QA or delivery encodes?
  → Use local Pillow/ffmpeg; no Aident call.
```
