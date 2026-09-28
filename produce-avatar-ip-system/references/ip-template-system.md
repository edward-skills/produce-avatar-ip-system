# IP Character Template System

An IP template is not a fixed character image. It is a composable parameter contract that tells any agent how to build, review, and reproduce a character direction without inheriting an accidental face, body, outfit, or pose from an example render.

Use `assets/templates/ip-template-catalog.json` as the canonical machine-readable catalog and copy `assets/templates/ip-template-selection.example.json` once per persona. The scaffold names these `ip-template-selection-p01.json`, `ip-template-selection-p02.json`, and so on. Resolve each selection with `scripts/assemble_avatar_prompt.py` before generating.

## Template stack

Choose each dimension independently. Do not use a style image as a shortcut for all of them.

| Dimension | Controls | Must not silently control |
| --- | --- | --- |
| `style` | rendering language, material, facial simplification, lighting | identity, gender, outfit, body shape |
| `proportion` | head share, eye scale, shoulder/head ratio, torso compactness | hairstyle, clothing, presentation |
| `gender_presentation` | optional facial styling and attitude cues | chest, hair length, job, color, clothing |
| `body_construction` | chest plane, shoulders, torso taper, neck and garment drape | identity or gender label |
| `face_shape` | contour family and cheek/jaw construction | ethnicity, skin tone, age |
| `hair` | silhouette, parting, crown, strand grouping | gender or personality by implication |
| `outfit` | garment category, silhouette, layering, material/hardware | identity, anatomy, pose |
| `wearable` | detachable face/head accessory and optical behavior | hairstyle or face geometry |
| `prop` | object topology, readable surface, hand contact | pose beyond the required interaction |
| `palette` | dominant/secondary/accent/emissive color roles | material or whole-image color grade |
| `composition` | camera, crop, headroom, roll, eye and shoulder anchors | identity, style, anatomy |

Identity remains project-specific. A template may describe a soft-round face or sculpted bob, but it must not ship a fixed person's likeness as the reusable default.

## Required selection order

1. Select one `style` and one `proportion`.
2. Select `gender_presentation`, `body_construction`, and `face_shape` separately. For a masculine character with a flat chest, choose both a masculine presentation preset and `flat-straight`; do not expect the gender label to repair anatomy.
3. Select hair and palette.
4. For the neutral base, force `plain-base-tee`, `none` wearable, `none` prop, and `neutral-front-upper-body` composition regardless of later modules.
5. After neutral approval, validate the signature look. If the user supplied one, use `signature-source-reconstruction`; otherwise use one chosen outfit category.
6. Only after the signature look passes may the agent expand outfit, wearable, prop, palette, scene, and motion variants.

## Gender and body safeguards

The catalog uses presentation, anatomy, and styling as separate dimensions. These presets are art-direction conveniences, not claims about biology or identity.

- Never infer hair length, breast shape, shoulder width, clothing, color, occupation, or personality from a gender label.
- Never describe a body as “male” or “female” when the intended correction is geometric. Specify `flat chest plane`, `soft curved chest plane`, `straight torso`, `broad shoulders`, or another visible construction.
- Preserve the same approved head scale, crown headroom, camera, and shoulder/head ratio across the cast unless a persona contract explicitly versions them.
- Use `custom` presentation when the user supplies their own description. Do not force a binary preset.

## Stage resolution

The prompt assembler deliberately includes different dimensions at different gates:

| Stage | Included template dimensions | Forced behavior |
| --- | --- | --- |
| `concept` | style, proportion, presentation, body, face, hair, outfit, wearable, palette, composition | no prop unless explicitly requested in custom blocks |
| `neutral-base` | style, proportion, presentation, body, face, hair, palette | front view, zero head roll, plain crew-neck T-shirt, no wearable, prop, signature styling, or action |
| `signature-look` | neutral identity stack + outfit, wearable, palette, composition | supplied signature source wins over catalog fashion invention |
| `complete-character` | full selected stack | prop remains optional and must obey topology/grip rules |
| `scene` | full stack | action, background, and effects come from project-specific scene fields |

This prevents the common failure where a “base character” already contains a fashion look, prop, pose, and camera angle that have not been approved.

## Prompt resolution

Run:

```bash
python scripts/assemble_avatar_prompt.py \
  brief/ip-template-selection-p01.json \
  --stage neutral-base \
  --output review/prompts/p01-neutral-base.txt \
  --resolved-output review/prompts/p01-neutral-base.resolved.json
```

The resolved JSON is the reproducibility record. It contains selected IDs, stage overrides, and final prompt blocks. Keep it beside generated candidates and record its path in the generation log.

For image editing, place reference roles before the resolved template blocks:

```text
Image 1 is the exact identity source. Preserve only its identity-bearing features.
Image 2 is style/material only. Do not transfer its face, body, outfit, or pose.
[resolved template prompt]
```

## User-facing shorthand

Users do not need to know IDs. Translate ordinary language into a proposed selection and show the readable summary before generation.

```text
“可爱但更酷、潮流、不要太拟人”
→ style: cute-collectible-3d
→ proportion: cute-large-head-upper-body
→ hair: sculpted-bob-undercut
→ outfit: neo-street-tech
→ palette: cobalt-ultraviolet
→ composition: neutral-front-upper-body for the base gate
```

Ask only about high-impact ambiguity. Otherwise propose 2–3 materially different stacks and label every changed dimension.

## Compatibility rules

- `q-chibi-3d` should normally pair with `q-chibi-upper-body`; do not graft it onto realistic anatomy.
- `realistic-digital-human` should normally pair with `realistic-upper-body`; avoid toy materials and oversized collectible eyes.
- `neutral-base` always overrides outfit, wearable, prop, pose, and scene styling.
- `signature-source-reconstruction` requires an `outfit_source` or `signature_look_source`; if missing, stop and choose a catalog outfit instead.
- Optical wearables require visible eye QA; props require object-topology and grip QA.
- A palette changes material colors by role. It must not tint skin, hair, eyes, or the entire image.

## Adding templates

Add a stable ID, human label, visible controls, one positive `prompt_block`, and focused `avoid` items. Keep each option orthogonal. If a new option changes two independent axes, split it into two dimensions rather than hiding the coupling in prose.
