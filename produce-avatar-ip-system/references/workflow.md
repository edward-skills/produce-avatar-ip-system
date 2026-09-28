# End-to-End Production Workflow

Use this workflow for a reusable avatar/IP family whose identities must stay recognizable across color, clothing, props, scenes, and motion.

## 0. Intake and acceptance ledger

Read [ip-template-system.md](ip-template-system.md). Translate the idea into one `ip-template-selection-pXX.json` per persona. The reusable template is the selected parameter stack; example character images are references or candidates, never the template itself.

Capture the minimum decisions that prevent expensive rework:

| Field | Questions to resolve |
| --- | --- |
| Product role | Where will the avatar appear: selector, profile image, notification, empty state, result state, onboarding, marketing, or video? |
| Audience and tone | Friendly, expert, playful, premium, cute, neutral, localized, B2C, B2B? |
| Style preset | Cute collectible, Q/chibi, soft-anime tech, premium toy, semi-real, realistic, or a supplied custom reference? |
| Construction templates | Which head/body ratio, gender presentation, body construction, face shape, hair, outfit, wearable, prop, palette, and composition IDs apply? |
| Identity count | How many persistent personas? Which distinctions must remain visible at small size? |
| Variant axes | Color, hair, optical wearable, outfit, prop, scene, state, audio, or motion? |
| Required matrices | Which combinations are real deliverables? Avoid the full Cartesian product unless the product needs it. |
| Output contract | Canvas, crop, alpha, static formats, video formats, duration, audio, naming, and manifest? |
| Brand constraints | Palette, material, prohibited marks, cultural boundaries, and references? |
| Source of truth | Which image or Figma node is approved for each identity and each downstream asset? |
| Background contract | Transparent subject, editable background plate/token, composed card, baked video frame, or which combination? |
| Cost and tools | Available generation surfaces, expected paid steps, sample/batch authorization, and concurrency limits? |
| Non-goals | Common examples: no application integration, no UI implementation, no PR, no full-body art, no speech. |

Write corrections as an active ledger. Mark old feedback as superseded instead of carrying contradictory instructions into new prompts.

Create a reference-role map before generation. When a hero image contains the exact person, visual style, signature outfit, accessories, and a nonstandard pose, record all of those roles separately. Never use the pose defect as identity truth or treat the outfit as generic “style.”

## 1. Concept direction gate

Read [style-presets.md](style-presets.md). Create two or three parameter stacks that differ in labeled dimensions such as silhouette, facial language, proportion, material, fashion, palette, and emotional tone. Keep the same intended modular framing so the options are comparable. Resolve each stack with `scripts/assemble_avatar_prompt.py`; do not carry vague adjectives such as “cuter” or “more real” without showing the values they change.

Each concept board should show enough to evaluate the system:

- an equal hero pair or representative persona set;
- color behavior on the same character, not isolated swatches only;
- a few outfit/prop roles;
- notification-scale crops;
- a visible layer or variant model;
- bright and dark context only when the product genuinely needs both.

Do not ask a single concept generation to finalize identities, transparent production layers, dozens of variants, props, and documentation at once. That often causes identity collapse or repeated silhouettes. Select the direction first.

Gate: the user has approved one direction or supplied an existing approved reference that serves as the direction.

Changing head/body ratio, eye scale, feature detail, material, or lighting after this gate creates a new style version. Return to identity masters rather than patching the full downstream matrix.

## 2. System contract gate

Before more image generation, define:

- persona IDs and one-line immutable identity descriptions;
- style preset/version and its explicit proportions, material, lighting, expression, and motion-amplitude tokens;
- exact reference image for each persona;
- material, lighting, camera, expression baseline, and stylization level;
- canvas and percentage anchors;
- palette roles rather than merely hex colors;
- asset families and actual variant matrices;
- alpha strategy and fallback key color;
- transparent-subject, editable-background, and composed-preview rules;
- naming and Figma placement;
- prohibited changes and marks.

Record the contract in Figma beside the assets or in a versioned prompt/manifest file. Do not leave the only copy in chat.

## 3. Anchor-persona paired validation

Choose one representative `anchor_persona` before generating the rest of the cast. Read [approval-and-reference-locks.md](approval-and-reference-locks.md).

Create one labeled review board containing:

1. the original `SOURCE OF TRUTH`;
2. a `NEUTRAL BASE CANDIDATE` with simple base garment and standardized camera/body anchors;
3. a `SIGNATURE LOOK CANDIDATE` that restores the supplied outfit, accessories, material, palette hierarchy, and attitude exactly, when such a look exists.

The neutral candidate must use the `neutral-base` resolver stage. It forces `plain-base-tee`, `none` wearable, `none` prop, and `neutral-front-upper-body`, including zero head roll and complete crown. It is invalid if final fashion, props, gestures, or a three-quarter pose appear.

The neutral candidate proves construction. The signature candidate proves that normalization did not replace the person or dilute the approved fashion language. Use the original high-resolution identity source directly in both generations; a front-view derivative may be composition-only.

Review at detail size and the real target size. Ask separately whether the person is the same, whether the standardized body/camera is correct, and whether the signature look is faithful. Write an approval receipt before promotion.

Gate: the anchor identity, neutral construction, and signature look (or explicit `not applicable`) are approved. Do not expand the cast before this gate.

## 4. Identity masters and cast expansion

Build the remaining persistent identities from the approved anchor style and body system before modular clothes or props.

1. Generate head-and-neck masters only. Keep the same front-facing camera, eye line, crown, chin, neck base, background, and lighting.
2. Use hair silhouette, hair color, eye/eyebrow shape, face contour, and expression to create readable differences. Keep the same stylization level across personas.
3. Compare the full set in one contact sheet at actual product sizes as well as large review size.
4. Normalize the approved images mechanically onto the target canvas when apparent scale differs. Prompt text alone rarely guarantees identical visual size.
5. Define each persona's body construction separately: chest plane, shoulders relative to head, torso taper, neck, arms, garment drape, and apparent head-to-shoulder ratio.
6. Freeze the approved master for each persona. Every downstream prompt must include that exact high-resolution identity reference directly.

Gate: every persona is distinct, belongs to the same cast, has the intended skin tone and stylization, and matches the shared anchors.

## 5. Upper-body bases

Create a neutral upper-body reference for every persona from its approved identity master.

- Use one continuous 3D render for head, neck, shoulders, and torso. Do not paste a corrected head onto a body when the final result should look like a single sculpt; seams and scale drift become visible.
- Use a simple neutral base garment unless the product requires a body-only layer.
- Lock head-to-shoulder ratio, shoulder width, eye line, bottom crop, camera distance, and arm treatment.
- If one persona is out of scale, use another approved upper body as the composition template and the persona master as the identity reference.

Gate: the contact sheet reads as one cast with a common camera and body system.

Label these bases `construction-only / not final outfit` in user-facing review. Pair the board with the approved signature-look anchor so a plain T-shirt is not mistaken for the final fashion direction.

## 6. Signature outfit, wearables, derived outfits, and props

If the user supplied a signature look, reconstruct it first. Lock silhouette, layering, neckline, sleeves, hem, material, hardware, accessories, and dominant/secondary/accent color area. Do not translate a precise supplied garment into a loosely named category such as “tech bomber” and then invent a different varsity, athletic, armor, or gaming interpretation.

Approve the signature reconstruction before generating derived outfit families.

Choose between a true swappable layer and a native-rendered variant based on visual behavior:

- A flat or rigid accessory can remain a canonical component if it aligns reliably across every persona.
- Transparent or emissive optical wear often looks better when natively rendered onto each identity. Test one canonical master first. If perspective, face contact, refraction, or glow cannot survive overlay, generate persona-specific native renders while using the same approved optical reference.
- Color variants of glass, glow, or reflective material should be independently rendered with the chosen color driving fill, internal refraction, rim light, and outer bloom. Do not recolor the whole image or change only the fill.
- Generate clothing as the same 3D material family as the characters. Keep neckline, shoulder, sleeve, and hem anchors constant. For open jackets, explicitly require a complete inner garment so transparent holes are not mistaken for design.
- Generate `prop + hand` together when the prop requires contact. This is safer than compositing an unrelated hand later.

Gate: all assets share the approved material and anchors; transparent edges are real; no asset obscures the face unintentionally.

## 7. Complete front-facing characters

Generate only the combinations the product needs, such as `persona × outfit` or `persona × visor-color`. Supply separate references with explicit roles:

1. identity/upper-body reference;
2. approved wearable reference;
3. approved outfit reference.

Keep the result front-facing and standardized if it will power selection cards or composable avatar UI. Preserve skin tone separately from emissive colors.

Gate: matrix count is correct, every cell uses the intended source assets, and row/column changes affect only their declared axis.

## 8. Expressive scene renders

Scene renders are complete authored character illustrations, not mechanical layer composites. When the background must remain replaceable, author the subject and background as separate deliverables even if a composed card is also required.

1. Define scene semantics before posing: what job is happening, what prop proves it, what direction must the prop face, and what emotion should read?
2. Start from the approved complete character or upper body as identity and material reference.
3. Keep the shared scale anchors while allowing controlled torso rotation, head turn, eye direction, expression, and gesture.
4. Give each persona a different supporting gesture within a shared scene grammar. Four identical front-facing poses with different faces feel lifeless.
5. Describe object physics literally. Example: a laptop has one vertical screen facing the viewer, one horizontal keyboard deck below it, a hinge between them, a palm under the deck, and a pointing hand that does not cross the display.
6. Deliver a transparent subject master for each required scene, a separate editable background plate/token, and a composed preview/card when background replacement is in scope.
7. Review the entire `persona × scene` matrix before updating Figma.

Gate: identities and scale are stable, scene behavior is distinct, hands are intact, and every prop is physically legible at the target UI size.

## 9. Editable backgrounds and scene cards

Use three explicit asset types:

1. `scene subject`: transparent character/prop/effects that belong to the subject;
2. `background plate`: reusable fill, gradient, atmosphere, floor, and decoration;
3. `scene card`: approved composition of subject plus background.

Keep background atmosphere and decorative stars out of the transparent subject when the user expects later replacement. In Figma, prefer variables, gradients, ellipses, and independent decoration layers for editable backgrounds. If an image-to-video model cannot preserve alpha, compose the approved subject and approved background into a temporary generation frame; retain the transparent static source and record that the video is opaque.

Gate: the subject composites cleanly over light and dark checks, the plate can be replaced without regenerating the character, and the composed card matches the approved preview.

## 10. Motion loops

Use motion only after the source scene art is approved.

1. Choose the most failure-prone representative scene for the first sample, usually one with a face, both hands, a device screen, and emissive effects.
2. Verify the live image-to-video schema. Distinguish a weak reference-image field from a true first-frame field.
3. If the model cannot interpret transparent pixels predictably, composite the approved transparent character onto the final colored background before video generation.
4. When supported, use the exact approved frame as both first and end keyframe. Keep the camera locked.
5. Animate a clear sequence: resting pose, readable face/body action, prop interaction, synchronized effect, and smooth return to the exact resting pose.
6. Design for the real display size. A subtle blink may vanish in a 48 px avatar; use clear head turns, shoulder bounce, prop movement, and high-contrast effect timing without breaking identity.
7. Inspect sample duration, dimensions, audio, identity, hands, prop direction, and first/last continuity. Expand only after it passes.
8. Batch by scene in conservative groups. Review a midpoint/contact sheet after each scene group, then run final technical QA and encode delivery formats.

Gate: the representative sample is approved; every batch item passes visual and technical checks; failed cells are regenerated individually rather than restarting the whole batch.

## 11. Figma organization and delivery

Prefer the exact user-supplied page and node. Do not create duplicate pages or move confirmed artwork without consent.

Suggested asset families:

- `Identity / Head`
- `Identity / Upper Body`
- `Wearable / Visor` or `Identity / Visor Render`
- `Outfit`
- `Complete Character`
- `Scene Render / Transparent`
- `Background Plate / Editable`
- `Scene Card / With Background`
- `Motion / Silent`
- `Motion / Sound` only when requested
- `Prompt Contract`

For Figma video preview, use an import path supported by the current Figma environment. If an API cannot write video fills, do not represent a poster frame as if it were a working video. Keep H.264 MP4 for Figma/manual preview when supported; use WebM plus MP4 fallback for product delivery unless the user's platform requires something else.

Final package should include:

- approved transparent PNGs or equivalent lossless sources;
- optional optimized WebP derivatives, never as the only master;
- scene artwork and background variants;
- separate editable background plates/tokens plus composed scene cards;
- silent WebM and H.264 MP4 loops when motion is requested;
- contact sheets;
- a manifest with source, prompt/model revision, dimensions, duration/audio, and QA status;
- the reusable prompt contract in Figma or a maintained text file.
