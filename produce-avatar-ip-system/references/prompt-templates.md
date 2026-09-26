# Prompt Contracts and Templates

These templates encode reference roles and invariants. Replace bracketed placeholders. Keep only relevant clauses; excessive constraints can compete with the actual edit.

## Prompt grammar

Before writing a production prompt, read [style-presets.md](style-presets.md) and insert exactly one approved style block. Keep the style block separate from identity. “Cute,” “Q/chibi,” “semi-real,” and “realistic” change proportion, feature detail, material, lighting, and motion amplitude; they are not interchangeable adjectives.

For every production prompt, use this order:

1. `Use case` and `asset type`.
2. The exact role of each input image.
3. The one intended change.
4. Identity, style-version, and material invariants.
5. Composition anchors.
6. Object or optical physics.
7. Background/alpha method.
8. Exclusions and failure modes.

Say which image is the identity source, which is the composition template, and which is the accessory/outfit reference. Avoid phrases such as “use these references” without roles.

Use this assembly order:

~~~text
[use case and asset type]
[reference roles]
[identity lock]
[one style preset block]
[material and lighting lock]
[one intended change]
[composition anchors]
[prop/wearable physics]
[background contract]
[negative constraints]
~~~

When switching styles, regenerate one identity master from the highest-resolution source and approve it before reusing the downstream templates. Do not append “make it more chibi” to a complete-character or scene prompt and batch the whole matrix.

## Concept board

```text
Use case: stylized concept exploration
Asset type: modular [brand/product] digital-employee character-system board

References:
- Image 1 is a collection-system reference only. Use its repeatable framing and visible variant logic; do not copy its characters or motifs.
- Image 2 is a brand material/color reference only.
- Image 3 is a product-context reference only.

Create one coherent [width × height] editorial concept board for a reusable [3D style] avatar family. Show [persona count] equal-status base characters with the same camera, bust crop, proportions, neutral pose, and attachment zones. Include a small color strip, [role count] role/outfit/prop examples, notification-scale crops, and one compact exploded variant diagram.

Style: [style preset block].
Material and lighting: [material lock].
Tone: [emotional qualities].
Product constraints: readable at [small size], upper body only, props never hide faces, no unrelated text or UI chrome.
Avoid: copied franchise design, photoreal people, generic robot plating, crypto/NFT motifs, weapons, watermarks, [brand-specific prohibited motifs].
```

Use separate prompts for genuinely different directions. Do not generate the production layer library from the concept board itself.

## Identity head master

```text
Use case: character identity master
Asset type: reusable head-and-neck 3D avatar source

Create one [persona description] who belongs to the approved [cast/style] family. Keep [front-facing or specified] camera, full hair crown, complete head, neck base, neutral expression, and exact square framing. Match the approved cast's eye-to-face ratio, simplified features, skin material, visual age, lighting, and stylization level.

Identity distinction: [hair silhouette/color], [eye/eyebrow shape], [face contour], [expression].
Shared material: [material lock].
Background: uniform [chroma color] with no gradient or shadow, or genuine transparent alpha only if the generator reliably returns it.
No clothing, visor, earrings, props, logo, halo, text, border, floor, checkerboard, missing crown, open skull, or extra elements.
```

## Upper-body base

```text
Use case: identity-preserving generation
Asset type: neutral upper-body avatar base

Image 1 is the exact persona identity. Image 2, when present, is only the approved composition/proportion template.

Create one continuous 3D render of head, neck, shoulders, arms, and torso. Preserve Image 1's face, hair, skin tone, eye design, expression, and stylization exactly. Match Image 2's camera distance, head-to-shoulder ratio, eye line, shoulder line, torso width, arm placement, and bottom crop.

Wear only [neutral base garment]. Render a natural seamless neck and shoulders with no pasted layer, collar gap, floating edge, or compositing seam. Use [percentage anchors].
Background: [transparent or uniform chroma].
No final outfit, visor, jewelry, props, logo, text, legs, pants, floor, or background scene.
```

If a head/body seam or scale mismatch appears, regenerate the full continuous character using the composition template. Do not keep patching the neck.

## Native optical wearable

```text
Use case: identity-preserving edit
Asset type: persona with standardized [visor/glasses]

Image 1 is the exact persona. Image 2 is the approved optical design and material master.

Edit Image 1 only. Preserve the exact identity, hair, skin tone, face proportions, expression, head size, camera, crop, and 3D material. Transfer Image 2's exact silhouette, lens height, bridge/temple geometry, face contact, and optical material.

Color/material: [color] drives the lens tint, internal refraction, upper-rim energy line, edge glow, and outer bloom. Keep lens transparency near [target] so eyes, pupils, eyebrows, and eyelids remain crisp. Glow must not recolor skin or hair.

No opaque eye panel, fogged lens, eye obstruction, geometry drift, whole-image color grade, logo, symbols, text, halo, headset, or extra accessories.
```

For five optical colors, generate five native optical materials from the same source. Do not post-process only the fill or apply a global hue shift.

## Standalone outfit

```text
Use case: modular asset generation
Asset type: standalone 3D avatar clothing component

Image 1 is the approved garment/style reference.

Generate a production-ready [fit] version of [garment description] in the exact character-system material: [material lock]. Garment only, front-facing, symmetrical, centered, with collar at [anchor], shoulders level, sleeves fully visible, and hem at [anchor]. Preserve the shared camera, scale, light, stitching, rounded geometry, and hardware language.

Fit behavior: [specific shoulder/waist/length/sleeve differences].
Construction: include a complete [inner shirt/panel] behind every open zipper or placket. No hollow center, missing fabric, or transparent hole.
Background: [genuine alpha or uniform chroma].
No person, head, neck, skin, hands, mannequin, hanger, legs, text, logo, badge, halo, or prop.
```

## Complete front-facing character

```text
Use case: identity-preserving composition
Asset type: complete reusable upper-body avatar

Image 1 is the exact identity and body-proportion reference. Image 2 is the exact native-rendered wearable reference. Image 3 is the exact outfit reference.

Create [persona] wearing the exact outfit from Image 3 and the exact [wearable/color] from Image 2. Preserve Image 1's face, head size, eye shape, hair, hair color, skin tone, stylization, and body scale. Preserve the approved 3D material and soft studio lighting.

Composition: [front-facing], head and upper body only, [percentage anchors].
Wearable lock: preserve geometry, transparency, refraction, rim light, and bloom; eyes remain visible; no skin tint.
Outfit lock: preserve silhouette, panels, colors, pockets, seams, hardware, and complete inner garment.
Background: genuine transparent alpha or the approved chroma intermediate.
No text, logo, halo, prop, visible lower body, extra accessories, or camera-angle change.
```

## Expressive scene render

```text
Use case: identity-preserving scene generation
Asset type: standalone upper-body [scene name] avatar

Image 1 is the exact complete persona identity and material reference. Image 2, when present, is the exact prop construction and holding-logic reference.

Create [persona] performing [job/action]. Preserve the exact face, hair, skin, stylization, wearable, outfit, material, and lighting from Image 1. Keep the shared scale template [percentage anchors], but make the pose expressive: torso rotated [angle], head [turn/tilt], eyes [direction], expression [emotion], and free hand [gesture].

Prop physics: [literal front/back/hinge/grip/display/label description]. The prop remains below the face and never hides identity-critical features. Both hands are connected and anatomically complete.
Effect: [semantic colored effect] starts from the interaction point and may connect prop, wearable, and existing background accents.
Background: [transparent production master or specified scene].
No identity drift, extra props, mutated UI/text, logo, halo, watermark, legs, full body, extra/missing fingers, or impossible device surfaces.
```

Example physical clauses:

- Phone: `The visible UI is the front glass screen; the holding palm stays behind the back shell, the thumb rests on the near bezel, and other fingers wrap only around the far edge/back. The free index touches the front glass.`
- Laptop: `One vertical screen faces the viewer, one horizontal keyboard deck projects below it, and a hinge connects them. One palm supports the underside of the deck; the pointing hand touches only the screen. No display exists on the outer lid or keyboard deck.`
- Tablet: `The front plane remains viewer-facing and nearly parallel to the image plane; hands grip only the side and lower bezels.`
- Package: `The box remains rigid; the shipping label stays on one visible face and never wraps or migrates.`
- Megaphone: `The cone opening and rim remain intact and point away from the character; the grip hand stays on the handle.`

## Transparent scene subject

Use this when the background must remain replaceable:

~~~text
Use case: editable scene system
Asset type: transparent upper-body scene subject

Image 1 is the exact approved persona/complete-character source. Image 2 is the prop construction reference. Image 3, when present, is composition-only and must not be baked into the subject.

Create only the character, clothing, wearable, hands, prop, and subject-attached interaction effect for [scene/action]. Preserve the exact identity, approved [style version], material, camera, crop, and anchors. Keep all subject pixels within the canvas with clean translucent edges.

Background contract: genuine transparent alpha. No background gradient, atmosphere, floor, vignette, stars, floating decoration, light card, checkerboard, white matte, shadow rectangle, or baked scene.

Prop physics: [literal front/back/hinge/grip/display/label description].
No identity drift, style drift, skin-tone shift, extra/missing fingers, text mutation, watermark, or unrelated object.
~~~

## Editable background plate

~~~text
Use case: replaceable avatar background
Asset type: background plate only

Create a [square/target ratio] background for [scene/state] using [semantic palette]. Match the approved style's lighting softness and visual complexity while keeping the central avatar-safe region clear. Include only [gradient/atmosphere/floor/decorative accents] as separate-looking elements suitable for reconstruction in Figma.

No character, face, body, clothing, hands, wearable, prop, text, logo, watermark, foreground occluder, or baked character shadow. Keep the plate reusable across every persona in the scene.
~~~

For maximum editability, build simple fills, gradients, atmosphere ellipses, and stars directly as separate Figma layers; use generated plates only when the visual language cannot be reproduced reliably with design primitives.

## Composed scene card

~~~text
Compose the approved transparent subject over the approved background plate without regenerating either. Preserve subject scale and anchors. Match only contact shadow, ambient light, and edge integration; do not change face, hair, skin, outfit, wearable, hands, prop, or background layout. Export the composed card while retaining both sources separately.
~~~

## Targeted correction

Use a narrow edit prompt when exactly one local defect can be fixed without degrading the source:

```text
Edit Image 1 only. Image 2 is solely the correct [geometry/proportion/material] reference.
Change only [specific defect]. Preserve the exact identity, face, hair, skin tone, pose, crop, outfit, wearable, lighting, background, and all unaffected geometry. Do not regenerate or restyle any other region.
```

If the asset has already undergone multiple edits, restart from the highest-resolution approved source and regenerate. Narrow prompts cannot restore detail lost in earlier generations.

## Image-to-video loop base

```text
Locked square camera. Preserve the exact approved background colors, gradients, and decorative elements from the supplied frame. Preserve the exact 3D identity, face proportions, skin tone, hairstyle, transparent wearable, outfit, prop geometry, hand anatomy, crop, and material. Start from and return to the identical supplied frame for a seamless [duration]-second loop.

Make motion bold and readable at [target UI size]: [face action], [head/shoulder action], [prop interaction], then [reaction]. [Colored effect] travels from [interaction point] to [wearable/background accent]. Add controlled breathing and hair/fabric secondary motion. Return every hand, prop, expression, and body part smoothly to the exact starting pose.

No camera movement, zoom, crop change, background recolor, face/skin/hair/outfit/material change, prop flip or deformation, UI/label/text mutation, extra or missing fingers, warped hands, cuts, or speech.
```

When the provider supports true first and end frames, use the same approved frame for both. The prompt does not replace the keyframe fields.

If the static subject has alpha but the video endpoint does not preserve it, first compose the approved subject over the approved final background plate and use that exact composed frame for both first and end input. Do not feed transparent pixels and accept an accidental black background.

## Scene motion grammar

Vary persona performance while sharing the scene's semantic action:

| Scene | Prop action | Face/body action | Effect origin | Critical lock |
| --- | --- | --- | --- | --- |
| Store operations | tap/swipe one product card | wink or eyebrow raise, lean, nod | selected card | phone front remains viewer-facing |
| AI workbench | trace chart, present screen | head turn, shoulder bounce | chart/dashboard | screen and keyboard deck remain physically correct |
| Growth analytics | point to rising data | idea gesture, confident nod | data line/bar | tablet remains front-facing |
| Fulfillment | scan/tap label, lift box | inspect, present, thumbs-up | shipping label | rigid box and readable label |
| Campaign launch | raise megaphone, invitation gesture | clear smile/wink, torso lean | megaphone rim | cone and grip do not deform |

Decorative elements that must appear from nothing need explicit state language: `start at zero opacity and zero scale, overshoot, settle, then shrink and fade fully to zero before the end frame`.

## Negative constraint library

Select only relevant items:

```text
identity drift, face change, hairstyle change, skin-tone shift, whole-image color cast,
different stylization level, photorealism, oversized head, undersized head, crop shift,
opaque lens, hidden eyes, mismatched glow color, halo, logo, text, watermark,
fake checkerboard transparency, white matte, jagged alpha edge,
missing fingers, fused fingers, extra fingers, detached hands, extra limbs,
phone flip, screen on phone back, screen on laptop outer lid, screen on keyboard deck,
tablet edge-on, package deformation, moving label, megaphone deformation,
camera motion, zoom, cut, flicker, background recolor, UI or text mutation
```
