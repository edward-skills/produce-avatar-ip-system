# Reusable Asset Contract

Define this contract before multiplying variants. Values below are a proven square-avatar starting point, not mandatory brand choices.

## Identity and matrix model

Assign stable persona IDs such as `m1`, `f1`, `m2`, and `f2`, or neutral IDs such as `p01` through `p04`. A persona ID represents a persistent face, head shape, hair silhouette/color, stylization level, and baseline skin tone. Clothing, optical color, scene, and motion must not redefine identity.

Use explicit matrices:

| Matrix | Typical purpose |
| --- | --- |
| `style-version` | one coherent style contract; only multiply when the product intentionally offers styles |
| `persona` | approved identity masters |
| `persona × upper-body` | neutral reusable busts |
| `persona × optical-color` | native-rendered visor/glasses variants when overlay is unreliable |
| `fit × outfit` | standalone garment components |
| `persona × outfit` | front-facing complete characters |
| `persona × scene` | expressive complete scene renders |
| `scene × background` | reusable background plates/cards without changing identity |
| `persona × scene × motion-mode` | loops, usually silent plus optional sound |

Do not generate `style × persona × color × outfit × scene` unless the product truly exposes that full combination space. Most systems have one approved style version and a much smaller set of real product combinations.

## Visual anchors

Choose one reference canvas and store anchors as percentages so source resolution can change. A practical 1:1 bust template is:

- hair crown near 5% of canvas height;
- eye line near 29% to 30%;
- chin near 41% to 42%;
- shoulder line near 49% to 50%;
- lower torso crop near 96%;
- head including hair about 37% of canvas height;
- shoulders about 64% of canvas width.

These numbers are a starting scaffold. Set them once from the approved cast, then keep them stable. Measure apparent face width and eye/chin placement, not just the outer PNG bounds; large hair silhouettes can make equal bounding boxes look unequal.

Useful production sizes:

- `720 × 720` transparent masters for static components;
- `560 × 560` or another common inner frame for head variants;
- `768 × 768` or a provider-supported square resolution for motion.

Prefer the user's requested sizes. Never resample repeatedly between working generations; derive all delivery sizes from the highest-resolution approved source.

## Material and lighting lock

Write a short immutable material statement, for example:

```text
Premium bright stylized 3D anime collectible; simplified facial planes; soft polymer and tactile fabric; clean rounded geometry; soft frontal studio key; restrained colored rim; crisp optical glass; friendly and competent rather than photoreal or chibi.
```

Also record:

- camera angle and projection feel;
- lens/refraction behavior;
- skin tone and color temperature policy;
- fabric and hardware language;
- allowed saturated accents;
- prohibited motifs and marks.

When the user changes art direction, version the material lock. Do not blend two approved but incompatible styles inside one asset family.

## Alpha and backgrounds

There are three legitimate output types:

1. Transparent production master: real alpha, subject edges reviewed.
2. Chroma-key intermediate: a uniform color absent from the subject, used only for deterministic keying.
3. Final scene/card: an intentional colored background and decorative elements.

When backgrounds must remain editable, deliver all three layers of the contract:

- transparent scene subject;
- independent editable background plate/token;
- composed card used for approval and motion input.

A painted checkerboard is not alpha. A fully opaque PNG with white corners is not a transparent master. Preserve lossless PNG masters even if WebP derivatives are later generated.

For video generation, transparency may become black or be ignored. Use a composited final background as the input frame unless the selected model and delivery codec have verified alpha support.

## Figma component axes

Keep source assets visible and component axes semantic. A useful property set is:

- `Persona`: stable identity ID;
- `Style`: only when multiple style versions intentionally coexist;
- `Scene`: business or emotional scene;
- `Color`: semantic optical/background color;
- `Outfit`: garment ID;
- `Fit`: only when standalone clothing genuinely has separate fits;
- `State`: default, working, success, warning, celebrate;
- `Background`: transparent, semantic token, or named plate;
- `Motion`: static, silent-loop, sound;
- `Size`: compact, card, hero only when composition genuinely differs.

Do not use obsolete design-direction names as product-facing variant properties. Do not convert draft experiments into the production component set merely because they already exist.

Suggested Figma layout:

```text
Prompt Contract
  Material lock
  Identity lock
  Static templates
  Motion templates
  Negative constraints
  Tool/model notes

Assets
  Identity Heads
  Upper Bodies
  Optical Renders
  Outfits
  Complete Characters
  Scene Renders
  Background Plates
  Scene Cards
  Motion Posters / Videos
```

Update the user's designated asset board in place. Keep drafts as ordinary frames or clearly marked experiments if the user wants them preserved.

## Naming and manifest

Use filenames that identify the matrix cell without embedding transient model names:

```text
identity-p01.png
upper-p01.png
visor-p01-cyan.png
outfit-o03-fit-a.png
complete-p01-o03.png
scene-p01-store-ops.png
background-store-ops-blue.png
scene-p01-store-ops-card.png
motion-p01-store-ops-silent.mp4
motion-p01-store-ops-silent.webm
```

Keep model and prompt revisions in the manifest:

| Field | Meaning |
| --- | --- |
| `asset_id` | stable logical ID |
| `persona` | identity source |
| `axis_values` | color, outfit, scene, state, motion mode |
| `style_version` | selected preset/custom style contract revision |
| `source_reference` | approved local file or Figma node |
| `prompt_revision` | prompt contract version |
| `provider_model` | explicit generation model used |
| `dimensions` | width and height |
| `alpha` | none, binary, or translucent |
| `background_contract` | transparent subject, editable plate, composed card, or baked opaque motion frame |
| `duration_fps_audio` | for motion |
| `qa` | pass/fail and reviewer notes |
| `figma_target` | page/node/component ID when applicable |

Source filenames and Figma node names should remain stable when content is corrected. Verify replacement rather than creating duplicates unless version history is explicitly requested.

## Use-case derivatives

Derive these from approved masters instead of regenerating identity:

| Use case | Recommended source |
| --- | --- |
| Avatar selector/profile | identity or upper-body master with compact crop |
| Notification/status | upper body or scene subject with simplified gesture and strong silhouette |
| Empty/success/error state | scene subject + editable semantic background |
| Onboarding/assistant card | complete character + background plate |
| Marketing key art | highest-resolution complete/scene source with expanded composition |
| Sticker/reaction | identity-preserving expression/gesture derivative |
| Looping UI motion | approved scene card as first/end frame, silent by default |
| Spoken digital human | separate lip-sync/talking-head workflow; do not repurpose silent prop loops |
