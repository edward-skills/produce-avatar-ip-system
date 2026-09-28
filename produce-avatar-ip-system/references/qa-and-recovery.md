# Quality Gates and Recovery

Run visual review before technical checks. A file can satisfy dimensions and still be unusable.

## Review gates

### Concept gate

- Direction is visibly distinct from rejected alternatives.
- Character family is equal and coherent; no accidental single-person dominance.
- Silhouette and eyes read at the smallest target size.
- Proposed modular axes make product sense.
- Prohibited motifs and marks are absent.

### Style gate

- One named preset/custom style version is active.
- Head/body ratio, eye scale, feature detail, material, lighting, expression, and motion amplitude agree.
- Every persona belongs to the same realism/stylization level.
- Outfit, prop, wearable, and background detail match the character style.
- A style change was validated on one identity before downstream regeneration.

### Identity gate

- The board includes the original labeled source of truth, not only generated candidates.
- Persona is recognizable against its source of truth.
- The highest-resolution identity source was supplied directly; composition references did not redefine the face.
- All personas share camera, material, lighting, stylization, visual age range, and crop.
- Hair crown, eye line, chin, neck base, apparent face width, and head scale align.
- Skin tone is intentional and not contaminated by hair or glow color.
- Full head is structurally complete; no missing crown or hollow under hair.
- For the anchor persona, both the neutral construction master and the signature-look validation read as the same person.

### Approval gate

- The review board labels `SOURCE OF TRUTH`, candidate type, and any `SUPERSEDED/REJECTED` image visibly.
- Identity, style/material, composition/body, and signature-look axes are reviewed independently.
- A detail-size and real-product-size view exist.
- An approval receipt records exact assets, approved axes, pending/rejected axes, and next allowed action.
- No candidate is promoted and no cast/matrix expansion starts from an ambiguous “OK.”

### Static asset gate

- Image dimensions and canvas are consistent within the asset family.
- Alpha exists when required; corners and negative space are actually transparent.
- No checkerboard is painted into RGB.
- Fine edges are neither jagged nor surrounded by a white/color fringe.
- Outfit openings contain the intended inner garment; no accidental transparent hole.
- Optical wear has correct geometry, contact, transparency, and matching fill/refraction/rim/bloom.
- Complete characters have no head/body seam and no unintended lower body.
- Every matrix row and column changes only its declared axis.

### Scene gate

- Pose, gaze, expression, and prop action communicate the scene at target UI size.
- Four personas in one scene do not all use the same pose.
- Hands are complete and connected.
- Prop front/back and grip logic are physically possible.
- Device screens, labels, charts, and effect origins stay on the correct surfaces.
- Scale anchors remain consistent across the full matrix.

### Editable-background gate

- Transparent scene subject contains no baked gradient, atmosphere, floor, stars, card, or rectangular shadow.
- Background plate contains no character/prop pixels.
- Subject composites cleanly on light, dark, and intended brand plates.
- Composed card is traceable to the exact subject and plate.
- Figma background fills/decorations can be replaced without changing the character.
- Opaque motion input is labeled as a composed frame rather than transparent video.

### Motion gate

- Exact model and keyframe fields are confirmed from the live schema.
- Source frame is the latest approved artwork, including background.
- Identity, skin, hair, outfit, wearable, prop, and background stay stable.
- Action is readable at target size and includes real prop interaction.
- Effect timing is causally tied to the interaction.
- Camera and crop remain locked.
- First/end continuity looks acceptable; hands and prop return to the resting pose.
- Output size, duration, frame rate, codec, and audio state match delivery.

### Figma gate

- Correct page and source node were used.
- Existing approved nodes were updated rather than duplicated unless versioning was requested.
- Image fill/hash changed to the intended asset.
- Fresh screenshot shows the new asset at the correct size and position.
- Component set has the expected count, semantic properties, and no unnamed leftovers.
- Prompt contract and manifest point to the final sources, not rejected candidates.
- Video preview is genuinely playable when claimed; a poster frame is labeled as a poster.

### Package gate

- File counts equal manifest counts.
- Lossless transparent masters are present.
- Optimized derivatives are traceable to masters.
- WebM/MP4 pairs exist where promised.
- Contact sheets and QA report are included.
- Archive integrity test passes.

### Cross-agent release gate

- A new agent can start from a freeform idea plus this skill and locate the intake, style presets, prompt templates, asset contract, and approval sequence without the source chat.
- The brief, acceptance ledger, prompt contract, generation log, manifest, and approved files contain enough state for a different agent to resume at the next unapproved stage.
- No instruction depends on an absolute user path, a remembered thread, an implicit provider default, or a guessed model name.
- Every tool is selected by capability first; exact action/model IDs are recorded only after live discovery or explicit host disclosure.
- Missing Figma, Aident, ImageGen, Pillow, or FFmpeg capability produces an honest fallback/blocked deliverable state rather than a false completion claim.
- The four user-facing approvals remain separate: base IP; palette/outfit/prop combinations; editable scenes; representative animation before batch.

## Technical checks

Use `scripts/inspect_avatar_delivery.py` for repeatable checks. For a 720 px static set and 768 px silent loops, a typical invocation is:

```bash
python scripts/inspect_avatar_delivery.py ./delivery \
  --expected-image-size 720x720 \
  --expected-video-size 768x768 \
  --expect-audio silent \
  --target-duration 5.184 \
  --duration-tolerance 0.15 \
  --loop-ssim \
  --min-loop-ssim 0.95
```

SSIM is a heuristic, not proof of a good loop. `0.95` worked as a strict batch threshold for a same-keyframe square avatar workflow, but set the threshold from a known-good sample for the current material and encoder. Always inspect the first, middle, and near-last frames visually.

Use `scripts/build_review_sheet.py` to compare a matrix. Review large enough to see fingers and device surfaces, then again at the actual UI size.

## Failure patterns and responses

| Symptom | Likely cause | Response |
| --- | --- | --- |
| Repeated male/female silhouette or lost persona | Too many variables were requested in one generation | Return to identity-only generation; approve each persona before variants. |
| Neutral base is technically standardized but the user says it is a different person | Identity and composition references were conflated, or a derivative became the only source | Reopen the base gate; use the original high-resolution identity directly and mark the front-view image composition-only. Invalidate dependent assets. |
| User asks why the plain T-shirt lost the original cool/style language | The construction base was shown without its role or paired signature look | Label it `construction-only / not final outfit` and show the source plus standardized signature-look validation on the same board. |
| First modular outfit looks sporty, armored, or unrelated to the supplied fashion | A loose category name replaced the exact signature outfit | Reconstruct the supplied signature outfit first; lock silhouette, layers, hardware, accessories, and dominant/secondary/accent area before derived outfits. |
| “OK” was interpreted as approval of identity, body, clothing, and the whole cast | Approval axes and reviewed assets were not recorded | Revert unproven promotions, create an approval receipt, and ask only about unresolved axes. |
| Head roll or three-quarter construction propagates through the cast | A tilted identity/style source was reused as composition truth | Use a separate front-view composition reference; lock zero roll, level eyes, and centered nose-mouth-chin-neck while keeping the original identity source direct. |
| Male torso reads feminine or its head looks smaller than the cast | Body construction and apparent scale were not contracted separately | Define chest plane, shoulder/head ratio, torso taper, neck, arms, and garment drape; compare apparent face/head scale at product size. |
| Head sizes still look unequal despite equal bounds | Hair volume or face width differs | Align eye/chin/face-width anchors and normalize apparent subject scale mechanically. |
| Head/body seam or floating neck | Layer replacement used for a final render | Regenerate the entire upper body as one continuous 3D model. |
| Character becomes more photoreal while making it “cool” | The model interprets age/sharpness as realism | Supply an approved cast member as the stylization reference; keep simplified nose, eye ratio, and soft material explicit. |
| Blue/purple hair makes skin yellow, blue, or purple | Generation light or global color correction contaminated skin | Lock skin to the identity master; edit only skin regions or regenerate without whole-image grading. |
| Optical color changes but glow stays cyan | Fill-only recolor | Natively render each optical color with matching refraction, rim, and bloom. |
| Transparent result contains a checkerboard | Model painted the transparency preview | Regenerate on a uniform key background or replace only the background, then key deterministically. |
| “Cute” variant keeps realistic torso or “real” variant keeps chibi eyes | Style was treated as a prompt adjective instead of an upstream contract | Select/version one style preset, regenerate an identity master, then rebuild downstream assets from that master. |
| Replacing the background leaves stars/gradient around the subject | Scene effects were baked into the transparent source | Regenerate or isolate a clean scene subject; move atmosphere and decoration to a background plate/Figma layers. |
| Edge quality degrades over revisions | Editing an already edited image | Restart from the highest-resolution approved source and make one scoped edit. |
| Phone screen appears on the back | Grip and visible plane are ambiguous | State front glass, back shell, bezel, palm, finger, and viewer orientation literally; use a correct construction reference. |
| Laptop outer lid becomes a display | Device topology is ambiguous | Specify one inner vertical screen, one horizontal keyboard deck, one hinge, and no display on outer lid/deck. |
| Tablet rotates edge-on in video | Prop motion competes with character motion | Lock the tablet front plane; put motion into head, torso, finger, and effects. |
| Figma appears unchanged after upload | Asset uploaded but node fill not replaced | Read the node's fill/hash, explicitly replace it, then verify with a fresh screenshot. |
| Video reference becomes a different character or aspect ratio | A reference-image field was mistaken for first-frame input | Inspect live schema; use the real first-frame field and explicit aspect/resolution. |
| Transparent video input becomes black | Provider ignores input alpha | Composite the approved character onto the final background before generation. |
| Timeout after paid execution | Client lost the response while provider may still be running | Check request/audit history and persisted result; retry only when absence and no charge are confirmed. |
| Rate limit during batch | Concurrency too high | Keep successes, reduce to small scene batches, and resume missing cells only. |
| Contact sheet passes but one motion feels weak in product | Review was too large | Review at target avatar size; amplify silhouette motion and effect contrast. |

## Regeneration policy

- Regenerate one failed matrix cell when the source identity and contract remain valid.
- Regenerate an entire row only when the shared scene/outfit prompt is wrong.
- Regenerate the whole matrix only when the upstream identity, material, anchors, or accepted art direction changed.
- Never overwrite the last approved source before the replacement passes. Keep candidate and approved states distinct.
- When identity drift is found after downstream work started, mark every dependent asset rejected or superseded; do not salvage its outfit, scene, or motion as a new source.
