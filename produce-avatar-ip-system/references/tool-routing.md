# Tool, Provider, and Cost Routing

Capabilities and schemas change. Treat tool names and model IDs from prior projects as examples, then confirm the current environment before acting.

## Image generation

Use the host's image generation/editing capability for:

- concept directions;
- identity masters;
- narrow identity-preserving edits;
- native-rendered wearables;
- outfits, complete characters, and scene renders.

Supply the fewest references that establish identity, composition, and the one changed asset. Inspect every provided image before editing it. When the user names a provider or integration, prefer that surface if it is available; otherwise use the host's supported image tool and state the fallback.

External catalogs may help compare models, but do not turn a one-off comparison into a permanent provider rule. Model selection should consider:

- identity preservation;
- reference-image role clarity;
- square output and resolution;
- real alpha versus chroma workflow;
- anatomy and prop compliance;
- native optical/glow rendering;
- price and batch limits.

When using Aident-managed media, read the installed `aident-skill` first. Search by operation, then list the relevant Fal model category. Use an explicit model ID in generation calls even when the action has a default. This prevents a provider-default change from silently altering the style or cost.

Do not conflate:

- `fal-ai/gemini-25-flash-image/edit`: Gemini 2.5 Flash Image / original Nano Banana;
- `fal-ai/gemini-3-pro-image-preview/edit` or `fal-ai/nano-banana-pro/edit`: Nano Banana Pro;
- `fal-ai/nano-banana-2/edit`: Nano Banana 2.

Refresh these IDs from the live catalog before use; they are included here to prevent ambiguous model naming, not to bypass discovery.

## Figma

Before mutation:

1. Parse the exact file and node IDs supplied by the user.
2. Inspect page, parent, dimensions, existing components, variants, names, and source fills.
3. Read the applicable Figma skill/instructions required by the available connector.
4. Decide whether the task is source organization, component creation, image replacement, documentation, or video preview.
5. Define whether backgrounds must remain editable and identify the separate subject, plate, and composed-card nodes.

After mutation:

1. Verify created/mutated node IDs.
2. Re-read target fills or image hashes.
3. Capture a fresh screenshot of the relevant board/component set.
4. Confirm count, layout, names, and actual visual replacement.
5. Confirm transparent subjects remain independent from background fills and decoration.

If the connector cannot write video fills, tell the user the exact limitation and provide the real video files for manual import. Do not silently substitute GIF or a poster frame when the requested behavior is video.

## External image/video actions

When an integration layer such as a managed capability catalog is available:

1. Search current capabilities by task and provider.
2. Read the selected action's live schema.
3. Check connection state when required.
4. Use an explicit model ID; never rely on a contradictory description/default.
5. Upload only approved input assets using managed storage.
6. Preflight input validity and price when available.
7. Execute one representative sample.
8. Record request ID, model, prompt revision, output asset ID/URL, and cost.
9. Download and validate the artifact before declaring success.

Do not ask for raw secrets when managed credentials are available.

For the Aident/Fal surface used in the source workflow:

~~~text
direct:fal:fal_list_text_to_image_models → direct:fal:fal_text_to_image
direct:fal:fal_list_image_edit_models → direct:fal:fal_edit_image
direct:fal:fal_list_image_to_video_models → direct:fal:fal_image_to_video
direct:file_storage_tools:file_create_upload_url → upload local/Figma media when a provider URL is required
~~~

## Video model fields

Identify which fields truly control:

- first frame;
- end frame;
- weak reference images;
- duration;
- resolution/aspect ratio;
- prompt expansion;
- audio generation;
- safety checks.

The difference is material. In one production workflow, a weak `reference_image_urls` field allowed a complete character redraw and 16:9 output, while the actual `image_url` first-frame field preserved the 1:1 source. Use the live schema rather than memorizing that field name for every provider.

## Sample and batch authorization

- If generation is paid, surface the exact or estimated sample cost before execution when the user has not already authorized it.
- Treat acceptance of one sample as approval for that sample, not automatically for a materially larger batch.
- Before batching, report matrix size, per-item estimate, expected retry allowance, formats, and stopping condition.
- Stop on insufficient credits or a provider billing error. Do not retry an unchanged paid request blindly.

## Concurrency and recovery

Start with conservative parallelism for expensive media actions. A practical initial batch size is three or four, then adjust from observed rate limits.

On HTTP 429:

- retain completed outputs;
- wait according to the provider response when available;
- lower concurrency;
- retry only missing or explicitly failed items.

On timeout or network interruption:

- assume the request may have been submitted;
- inspect audit/history or provider request status;
- reuse the same request/idempotency identifier when the surface supports it;
- retry once only after confirming no persistent result and no charge.

## Local media tools

Use deterministic local tooling after generation:

- Pillow for alpha inspection, chroma removal, canvas normalization, and contact sheets;
- `ffprobe` for codecs, streams, dimensions, duration, and frame rate;
- `ffmpeg` for representative frames, SSIM, muted transcodes, H.264 MP4, and VP9 WebM;
- archive integrity checks after packaging.

Do not use repeated image resampling or global color correction as a substitute for a valid source generation. Local processing should standardize delivery, not redesign the character.
