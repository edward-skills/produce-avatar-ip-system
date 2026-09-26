# Figma Asset and Component System

Use this reference when adapting an existing Figma asset board or when building the reusable source/component structure for a new avatar system.

## Historical source case

The workflow was derived from a real Vertical Agents Figma production board. The private file key, URLs, and node IDs are intentionally not distributed with this open skill. The matrix and component rules below preserve the reusable system without exposing the source design file.

For a new project, require the user to provide or confirm its own Figma file, page, and target node. Record those project-specific anchors in the task brief and manifest; never copy historical node IDs into another user's file.

## Verified source matrix

Personas:

- `M1 / Black Tousled`
- `F1 / Black Bob`
- `M2 / Cobalt Buzz Cut`
- `F2 / Cobalt Ponytail`

Palette:

- Cyan `#1EEAEA`
- Blue `#1381FF`
- Indigo `#6863FF`
- Orange `#FF7D03`
- Green `#34A853`

Scene grammar:

- Store Operations / phone;
- AI Workbench / laptop;
- Growth Analytics / tablet/chart;
- Cross-border Fulfillment / shipping box;
- Campaign Launch / megaphone.

The Assets board contains:

- 4 identity masters;
- 4 × 5 native visor/color renders;
- 10 standalone outfit assets across fit/presentation;
- 5 prop + hand assets;
- 20 complete persona/outfit variants;
- 20 transparent scene renders;
- background-composed big-avatar cards;
- static and motion prompt documentation.

## Recommended source structure

~~~text
Prompt Contract
  Style and material lock
  Identity lock
  Composition anchors
  Static templates
  Motion templates
  Negative constraints
  Tool/model provenance

Source Assets
  Identity / Head
  Identity / Upper Body
  Wearable / Native Render
  Outfit / Standalone
  Prop / Standalone or Prop + Hand
  Complete Character
  Scene Subject / Transparent
  Background Plate
  Scene Card / Composed

Components
  Avatar / Compact
  Avatar / Scene Static
  Avatar / Motion Poster or Video
~~~

Keep raster source assets visible beside component sets so replacements can be audited.

## Semantic component axes

Use only axes that the product actually exposes:

- `Persona`: stable identity;
- `Style`: only when multiple style systems intentionally coexist;
- `Scene`: semantic business/emotional situation;
- `Accent` or `Color`: brand color role;
- `Outfit`: garment;
- `State`: default, working, success, warning, celebrate;
- `Background`: none/transparent, token or plate;
- `Motion`: static, silent-loop, sound;
- `Shape`: circle/square when the crop container truly differs;
- `Size`: compact/card/hero when composition genuinely differs.

Do not encode transient model names or rejected design-direction names as product-facing variant properties.

## Editable-background contract

For every background-replaceable scene, maintain three things:

1. transparent subject source;
2. editable background built from Figma shapes, variables, gradients, or a separate background plate;
3. composed preview/card.

The subject must not contain baked atmosphere, stars, gradient, floor, or light spill that prevents reuse unless those effects are intentionally part of the subject. Keep decorative accents as separate Figma layers when practical.

Use background variables or semantic names such as:

- `Background/Avatar/Cyan`
- `Background/Avatar/Blue`
- `Background/Avatar/Indigo`
- `Background/Avatar/Orange`
- `Background/Avatar/Green`

When AI video requires a baked background, create a composed generation frame from the same approved subject and background. Retain the transparent static subject separately; do not pretend the video has alpha unless the codec and decoded output verify it.

## Figma execution rules

Before any write:

1. Load the applicable `figma-use` skill and required references.
2. Inspect the exact file, page, target node, current components, names, fills, and bounds.
3. Preserve confirmed nodes and IDs where possible.
4. Work incrementally and return every mutated/created node ID.

For image replacement:

1. identify the exact target nodes;
2. upload the real PNG/WebP source;
3. verify the target fill/hash changed;
4. get a fresh screenshot;
5. confirm size, crop, alpha, and neighboring component instances.

For component creation:

1. keep source art as ordinary nodes;
2. create semantic components/variants from approved sources;
3. validate property count and variant count;
4. verify no nested instance was unintentionally detached;
5. capture the whole component set and representative variants.

## Video in Figma

Use H.264 MP4 for manual/native Figma video fills when the current Figma environment supports them. Use WebM plus MP4 fallback for product delivery.

Connector runtimes may not support creating video fills even when the Figma product supports video. If the active tool cannot write a video fill:

- keep a clearly labeled poster/component;
- provide the real MP4 and its target node/name for manual import;
- do not substitute a GIF or still poster while claiming it is a working video.

## Final Figma gate

- correct file/page/node;
- expected source and component counts;
- semantic property names;
- no duplicate approved assets;
- transparent sources remain transparent;
- background layers remain replaceable;
- prompt and provenance notes point to final—not rejected—sources;
- claimed video previews actually play;
- fresh screenshots show correct layout and no clipped prompt text.
