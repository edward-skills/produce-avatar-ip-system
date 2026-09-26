# Input and Output Contract

Use this reference to turn an informal request into a reproducible production job. Copy `assets/templates/avatar-project-brief.yaml` into the task output directory and fill it progressively; do not block on fields that can safely be inferred from supplied references.

## Input priority

Use the highest-priority available input for each decision:

1. Explicit user instruction from the current turn.
2. Latest user-approved image, Figma node, or delivered asset.
3. Versioned prompt/style contract from the same project.
4. Earlier approved source from the project.
5. A clearly stated proposal by the agent.

Do not let an older chat correction override the latest approved source. Mark conflicting older notes as superseded.

## Minimum viable intake

The work can start when these are known or can be proposed:

| Input | Required meaning | Safe default only when absent |
| --- | --- | --- |
| Use cases | Avatar picker, profile, notification, empty/success/error state, onboarding, marketing, video, sticker, or other | Ask/derive the primary product surface; do not assume every use case |
| Persona count | Number of persistent identities | One representative persona for a sample; never silently multiply |
| Style | Preset or supplied visual reference | `soft-anime-tech-3d` only for a brief matching the Aident source case |
| Framing | Head, bust, upper body, three-quarter, or full body | Upper body for product avatar systems |
| Variant axes | Palette, outfit, prop, scene, state, background, motion | Generate only requested axes |
| Source of truth | Image/file/Figma node for each identity | The latest clearly approved source |
| Formats | Static/video sizes, alpha, audio, codecs | PNG master; WebP derivative; silent WebM + H.264 MP4 when motion is requested |
| Figma target | File/page/node and whether updates are allowed | No Figma mutation without a supplied/confirmed target |
| Cost authority | Sample and batch budget | Preflight and request approval before paid sample/batch |

## Optional but high-value inputs

- brand palette and prohibited colors;
- cultural or demographic boundaries;
- material references;
- wearable construction;
- outfit roles;
- prop topology references;
- background behavior;
- desired motion amplitude and duration;
- localization or text restrictions;
- accessibility constraints such as reduced motion;
- exact smallest display size.

## Reference-role map

Never pass a bundle of images without assigning roles. Record each reference as one of:

- `identity_source`: exact face, hair, skin, and stylization;
- `style_source`: material, lighting, rendering language only;
- `composition_source`: crop, camera, anchors, and scale;
- `outfit_source`: silhouette, construction, seams, palette;
- `prop_source`: topology, visible faces, label/screen placement, grip;
- `background_source`: gradient, atmosphere, and decoration;
- `motion_source`: timing and action only, never identity unless explicitly intended.

One image may hold several roles, but state them independently.

## Stage outputs

Each numbered stage is an explicit review boundary. Write the approval decision and approved source IDs to the acceptance ledger, then stop. Do not begin the next stage until the user approves the current stage; a request to “make the whole system” authorizes the workflow, not silent approval of unseen outputs.

### 1. Direction package

- 2–3 concept directions or one adopted existing direction;
- selected style preset and version;
- material/lighting lock;
- rejection notes and prohibited motifs;
- concept contact sheet.

### 2. Identity package

- one lossless master per persona;
- normalized transparent/chroma working source;
- persona identity card;
- identity contact sheet at review and product sizes.

### 3. Modular asset package

- upper-body bases;
- native wearable variants;
- standalone outfits;
- standalone props or `prop + hand` interaction assets;
- complete front-facing characters;
- palette/token sheet;
- transparent masters plus optimized derivatives.

### 4. Scene/background package

- transparent scene subjects;
- editable background plates/tokens;
- composed scene cards;
- action/state variants;
- scene contact sheets.

### 5. Motion package

- approved source frame;
- exact request JSON and prompt revision;
- silent master/intermediate;
- H.264 MP4 and VP9 WebM delivery files;
- first/mid/last frames;
- technical inspection report and loop-quality result.

### 6. Figma/package output

- semantic component sets and source nodes;
- prompt contract and tool/model notes;
- asset manifest;
- QA report;
- delivery archive.

## Recommended delivery tree

~~~text
avatar-ip-project/
  brief/
    avatar-project-brief.yaml
    prompt-contract.yaml
  sources/
    identity/
    style/
    outfit/
    prop/
    background/
  approved/
    identity/
    upper-body/
    wearable/
    outfit/
    complete-character/
    scene-subject/
    background/
    scene-card/
    motion/
  candidates/
  review/
    contact-sheets/
    frames/
    qa/
  manifests/
    asset-manifest.csv
    generation-log.jsonl
  delivery/
~~~

Keep `sources`, `approved`, and `candidates` distinct. A generated file is not approved merely because the tool returned successfully.

## Generation log

For every external generation, append one record containing:

~~~json
{
  "timestamp": "ISO-8601",
  "logical_asset_id": "scene-p01-store-ops",
  "stage": "scene",
  "tool_surface": "Aident Loadout",
  "action": "direct:fal:fal_edit_image",
  "provider_model": "exact endpoint id or OpenAI host ImageGen",
  "request_id": "when returned",
  "prompt_revision": "scene-v3",
  "source_references": ["path-or-figma-node"],
  "input_fields": {"only": "non-secret reproducibility fields"},
  "quoted_cost_usd": 0.0,
  "settled_cost_usd": 0.0,
  "output": "local path or durable asset reference",
  "qa": "candidate|pass|fail",
  "notes": "failure or correction"
}
~~~

Never log tokens, signed upload URLs, cookies, or provider credentials.

## Completion criteria

The job is complete only when:

- the user approved the base direction/identity, modular system, scenes, and representative motion at their separate gates;
- every promised matrix cell exists once;
- approved identity/style/anchors remain stable;
- transparent and background-composed outputs are correctly distinguished;
- editable backgrounds are separately available when requested;
- static/video formats match the brief;
- Figma counts and properties match the manifest;
- prompts and exact model/action provenance are recorded;
- failed/rejected candidates are excluded from delivery;
- the package passes [qa-and-recovery.md](qa-and-recovery.md).
