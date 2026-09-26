# Tool and Model Provenance

This reference has two purposes:

1. preserve what the source Vertical Agents project actually used;
2. show how to resolve current endpoints without rewriting history.

Historical observations are evidence from the referenced Codex task, Figma file, local artifacts, and Aident audit. Current catalog observations are a snapshot from 2026-09-26 and must still be refreshed before a new paid run.

## Source workflow: what actually happened

| Phase | Tool surface | Actual action/model | Result and use |
| --- | --- | --- | --- |
| Initial concept directions | Codex host ImageGen | Model ID not exposed | Three distinct 3D directions; later brightened, halo removed, full skull/base-head rule added |
| External concept comparison | Aident Loadout → Fal | `direct:fal:fal_text_to_image`, then-default result labeled Nano Banana 2; request omitted an explicit model | Strong modular inventory/checklist compliance; do not repeat the omission in a new run |
| External concept comparison | Aident Loadout → Fal | `bytedance/seedream/v5/pro/text-to-image` through `direct:fal:fal_text_to_image` | Best early neutral, light-anime, bright-tech direction |
| Automatic layer experiment | Aident Loadout → Fal | `bytedance/seedream/v5/pro/layerize` through `direct:fal:fal_edit_image` | Complex-board and simplified-avatar layerization did not yield a reliable production split |
| Approved static production | Codex `image_gen` / host OpenAI ImageGen | 66 tool calls; exact underlying model was not surfaced | Identity heads, upper bodies, native visors, outfits, complete characters, scene renders, backgrounds, and narrow corrections |
| Alpha/canvas/review | Local Python/Pillow and FFmpeg | `normalize_avatar_png.py`-style keying, normalization, contact sheets | Produced real transparent 720×720 masters and exposed fake checkerboards |
| Design system | Figma connector/MCP | `search_design_system`, `get_design_context`, `get_metadata`, `get_screenshot`, `download_assets`, `upload_assets`, `use_figma` | Organized assets/components, exported/imported media, replaced fills, stored prompt notes, and verified visuals |
| External input hosting | Aident managed file storage | `direct:file_storage_tools:file_create_upload_url` | Hosted local/Figma frames for Fal URL inputs |
| Representative motion sample | Aident Loadout → Fal | `fal-ai/kling-video/v3/pro/image-to-video` via `direct:fal:fal_image_to_video` | Strong phone interaction and identity preservation; transparent input required a composed bright background |
| Final motion sample and 20-loop batch | Aident Loadout → Fal | `minimax/h3-max/image-to-video` via `direct:fal:fal_image_to_video` | Final 4 personas × 5 scenes batch |
| Video QA/delivery | `ffprobe`, `ffmpeg` | H.264 MP4, VP9 WebM, frame extraction, SSIM | 768×768, 5.184 s, 24 fps, silent loop deliverables |

Do not claim Nano Banana, Seedream, or Figma drew the final approved static matrix. They contributed comparison, experiments, organization, and delivery at different phases; most final static art came from host OpenAI ImageGen.

### Codex ImageGen evidence and naming limit

The source rollout contains **66** invocations of `image_gen__imagegen`. Returned events were typed `image_gen.generation`, and generated PNG metadata identified the generator as `OpenAI Media Service API`. Neither the tool request nor its result exposed a selectable or returned model ID. This proves use of Codex/OpenAI's hosted image-generation capability; it does **not** prove GPT Image 2, GPT Image 2.5, or any other concrete model/version.

Use this historical provenance string verbatim unless stronger product telemetry is supplied:

```text
Codex image_gen / OpenAI host ImageGen (underlying model ID not exposed)
```

Do not convert `OpenAI Media Service API` into a model name. A user-provided admin/billing/model trace may refine the record, but visual appearance, date, and service branding may not.

### Exact Aident execution inventory

The raw source task recorded these generation/storage executions:

| Aident action | Count | Exact historical endpoint/result |
| --- | ---: | --- |
| `direct:fal:fal_text_to_image` | 3 | 1 omitted-model run returned `fal-ai/nano-banana-2`; 2 runs used `bytedance/seedream/v5/pro/text-to-image` |
| `direct:fal:fal_edit_image` | 3 | 1 omitted-model run returned `fal-ai/nano-banana-2/edit`; 2 runs used `bytedance/seedream/v5/pro/layerize` |
| `direct:fal:fal_image_to_video` | 28 | 3 used `fal-ai/kling-video/v3/pro/image-to-video`; 25 used `minimax/h3-max/image-to-video` |
| `direct:file_storage_tools:file_create_upload_url` | 28 in-scope production calls | Managed source-frame hosting for provider URL inputs; two later post-production/product-integration uploads in the broader audit window are excluded from this skill |

The omitted-model Nano Banana calls document historical defaults only. New runs must select an explicit live model ID.

In addition to those executions, Aident Loadout supplied capability search, action/schema inspection, live model listing, connection checks, preflight/cost validation, and audit recovery. Search terms included Nano Banana, Seedream, Midjourney, reference-image editing, layerization, Fal image generation, and image-to-video. These orchestration operations are capabilities, not creative models.

### Exact Figma connector inventory

The source rollout recorded the following Figma MCP calls: `download_assets` 190, `use_figma` 119, `get_screenshot` 60, `upload_assets` 21, `get_metadata` 17, `get_design_context` 10, and `search_design_system` 1. Counts describe tool invocations, not the number of final approved assets. Figma was the inspection, organization, editable-composition, and delivery surface; it was not the model that rendered the approved 3D character art.

## Historical motion request shapes

MiniMax H3 Max final batch:

~~~json
{
  "model": "minimax/h3-max/image-to-video",
  "model_input": {
    "prompt": "<locked-camera identity-preserving loop prompt>",
    "duration": 5,
    "resolution": "768P",
    "prompt_expansion_mode": "balanced"
  },
  "asset_inputs": {
    "image_url": "<approved-frame-asset-id>",
    "end_image_url": "<same-approved-frame-asset-id>"
  }
}
~~~

Kling v3 Pro representative sample:

~~~json
{
  "model": "fal-ai/kling-video/v3/pro/image-to-video",
  "model_input": {
    "duration": "5",
    "generate_audio": false,
    "cfg_scale": 0.5,
    "shot_type": "customize",
    "prompt": "<motion prompt>",
    "negative_prompt": "<failure constraints>"
  },
  "asset_inputs": {
    "start_image_url": "<approved-composited-frame-asset-id>",
    "end_image_url": "<same-approved-frame-asset-id>"
  }
}
~~~

Always inspect the live list-model output. The source task first used H3 Max's weak `reference_image_urls` route and got a redrawn 16:9 character; switching to true first-frame `image_url` plus the same `end_image_url` preserved the square artwork and identity.

## Source audit evidence

The Aident audit for 2026-08-29 through 2026-09-04 recorded:

- 63 `direct:fal` calls;
- 45 successes and 18 errors;
- 28 `fal_image_to_video` calls;
- 14 model-list video calls;
- 9 model-list image-edit calls;
- 6 model-list text-to-image calls;
- 3 image-edit and 3 text-to-image calls;
- historical settled total: US$2.30.

The same broad date-window audit contained 30 `file_create_upload_url` calls. The reusable avatar-production workflow accounts for 28; two later calls belong to the excluded post-production/product-integration portion of the source task. Keep this distinction when reporting “thread total” versus “skill-scope total.”

The three paid Kling video generations were US$0.70 each. The archived H3 Max runs recorded US$0.00 under the pricing/promotion state at that time. Never infer that H3 Max is free now; preflight every new request.

## “Nano Banana Pro” versus “Image 2.5”

These are not interchangeable names.

The source concept comparison explicitly used a run labeled Nano Banana 2 and a separate Seedream 5 Pro run. The approved static matrix later used host OpenAI ImageGen, whose underlying model ID was not exposed. Therefore:

- do not relabel source output as Nano Banana Pro;
- do not relabel host OpenAI ImageGen as “Image 2.5”;
- record the endpoint returned by the live tool when an explicit external model is used.

The live Aident/Fal catalog snapshot on 2026-09-26 exposed these distinct edit endpoints:

| Display meaning | Exact endpoint |
| --- | --- |
| Nano Banana 2 default edit | `fal-ai/nano-banana-2/edit` |
| Gemini 2.5 Flash Image, original Nano Banana | `fal-ai/gemini-25-flash-image/edit` |
| Gemini 3 Pro Image Preview, Nano Banana Pro | `fal-ai/gemini-3-pro-image-preview/edit` |
| Nano Banana Pro alias | `fal-ai/nano-banana-pro/edit` |
| Seedream 5.0 Pro edit | `bytedance/seedream/v5/pro/edit` |
| Seedream 5.0 Pro layerize | `bytedance/seedream/v5/pro/layerize` |

The connected Gemini action also exposed `gemini-2.5-flash-image` and `gemini-3-pro-image-preview`. Choose one surface, use its exact schema, and record it; do not mix Fal endpoint IDs with Gemini action IDs in one request.

## Current live motion IDs observed on 2026-09-26

| Need | Exact endpoint |
| --- | --- |
| H3 Max image-to-video | `minimax/h3-max/image-to-video` |
| H3 Max Turbo | `minimax/h3-max-turbo/image-to-video` |
| H3 Max subject/style reference video | `minimax/h3-max/reference-to-video` |
| Kling v3 Pro image-to-video | `fal-ai/kling-video/v3/pro/image-to-video` |
| Kling v3 Turbo Pro | `fal-ai/kling-video/v3/turbo/pro/image-to-video` |

Current catalog values are not permanent. Query and preflight again when executing.

## Reproducible Aident route

Use the installed `aident-skill` before external generation. A representative command sequence is:

~~~bash
aident capabilities search --query "reference image editing" --types action --json
aident capabilities get --name direct:fal:fal_list_image_edit_models --json
aident capabilities execute --name direct:fal:fal_list_image_edit_models --input '{"query":"nano banana","limit":10}' --json
aident capabilities get --name direct:fal:fal_edit_image --json
aident capabilities preflight --name direct:fal:fal_edit_image --input '<exact-json>' --json
aident capabilities execute --name direct:fal:fal_edit_image --input '<same-exact-json>' --json
~~~

For motion, replace the list/execute action with `direct:fal:fal_list_image_to_video_models` and `direct:fal:fal_image_to_video`.

Record:

- exact action and endpoint ID;
- live required/default fields;
- input asset roles and IDs, without signed URLs or secrets;
- prompt revision;
- request ID;
- quoted and settled cost;
- output file;
- visual and technical QA state.

If execution times out, use `aident audit recent` and recover the persisted result before considering a retry.
