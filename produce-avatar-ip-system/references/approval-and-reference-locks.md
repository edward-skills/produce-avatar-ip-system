# Approval and Reference Locks

Use this reference whenever a source image contains more than one kind of truth, whenever an approval could be ambiguous, or before expanding one representative character into a cast or matrix.

## Why this gate exists

A technically clean front view can still be the wrong person. A neutral T-shirt base can look like a style regression even when it is only a construction master. A newly invented outfit can satisfy a verbal label such as “tech bomber” while losing the approved fashion language. Prevent those failures by approving axes separately and showing the user evidence for each axis.

## Classify every supplied image before generation

Create `brief/reference-role-map.yaml` from the bundled template. An image may serve several roles, but record each role independently:

- `identity_source`: exact person—face contour, feature spacing, eyes, brows, nose, mouth, cheeks, jaw, skin, hair silhouette/color, visual age, and stylization;
- `style_source`: rendering language—proportion, material, geometry, lighting, and detail density;
- `composition_source`: camera, head roll, eye line, crop, scale, shoulder line, arm placement, and headroom only;
- `signature_look_source`: the approved personality-bearing combination of hairstyle details, accessories, outfit construction, palette hierarchy, and attitude;
- `outfit_source`, `wearable_source`, `prop_source`, `background_source`, and `motion_source`: the named downstream asset only.

Reference precedence is role-specific. A composition template never overrides the identity source. A style reference never silently becomes the exact face unless it is also marked `identity_source`. When a source contains an approved person in an approved look, mark both `identity_source` and `signature_look_source`; do not reduce it to “style reference.”

## Representative-first rule

Choose one `anchor_persona` before creating the cast. Do not expand to more personas until the anchor passes both views below:

1. `neutral construction master`: exact identity, standardized camera/crop/body anchors, simple base garment, no final accessories or props;
2. `signature-look validation`: the same identity and standardized presentation while restoring the supplied signature outfit/accessories/palette hierarchy exactly.

The neutral view proves reuse and proportion. The signature view proves that standardization did not erase the original person, attitude, or fashion language. Only the neutral view becomes the construction source; the signature view becomes the first outfit/look source.

If the user supplied no signature look, create only the neutral master and label the signature view `not applicable`. Do not invent extra styling merely to fill the pair.

## Identity lineage lock

Every identity master, recovery render, complete character, and scene must include the highest-resolution approved `identity_source` directly. A generated derivative may be used as a composition or outfit reference, but it must not become the only identity reference.

If the face has drifted, restart from the identity source. Do not repair identity through a chain of increasingly edited derivatives. Local post-processing may normalize canvas and alpha; it must not redefine facial identity.

## Base-IP review board

The review board must show, with explicit labels:

- `SOURCE OF TRUTH`: original approved identity/signature source;
- `NEUTRAL BASE CANDIDATE`: construction-only, not the final outfit;
- `SIGNATURE LOOK CANDIDATE`: exact signature reconstruction when applicable;
- `SUPERSEDED` or `REJECTED`: only when teaching or documenting a failure, never mixed with candidates without a visible status label.

Show a detail-size board and the real target size. Do not present only a candidate image. The user should be able to answer these independently:

1. Is this still the same person?
2. Are the camera, head roll, head/body ratio, torso, and crop correct?
3. Does the signature look preserve the original style, outfit construction, accessories, and dominant/accent color balance?

An unqualified “OK” approves only the visibly labeled asset and axes in the current review board. It does not approve hidden files, other personas, a larger matrix, or downstream stages.

## Approval receipt

After each user decision, write `review/approval-receipt-<stage>.yaml` from the template. Record:

- exact reviewed asset IDs and source-of-truth IDs;
- approved axes;
- rejected or pending axes;
- corrections requested;
- files promoted to `approved/`;
- next allowed action.

Do not promote files before this receipt exists. If the approval wording is ambiguous across multiple axes, continue safe non-destructive analysis but ask one short axis-specific question before promotion or batch expansion.

## Signature outfit lock

Before inventing outfit families, reconstruct one supplied signature outfit exactly. Record:

- silhouette and length;
- collar/neckline, sleeve, hem, and layering;
- complete inner garment behind openings;
- material and hardware language;
- accessory set;
- palette hierarchy by approximate area: dominant, secondary, accent, emissive;
- prohibited reinterpretations such as `not varsity`, `not armor`, or `not full-accent-color body`.

Only after the reconstruction is approved may new outfits derive from that fashion grammar. A phrase such as “cropped tech bomber” is not a sufficient outfit lock by itself.

## Cast expansion lock

For each new persona, create `brief/persona-<id>.yaml` from the persona contract. Keep face identity separate from body construction. Record:

- gender presentation only when requested or relevant;
- chest plane, shoulder width, torso taper, neck length, arm thickness, and garment drape;
- apparent head-to-shoulder ratio and face width at the common crop;
- zero-roll/front-view requirements or intentional angle;
- immutable hairstyle, facial landmarks, skin tone, and personality cues.

Review the full cast at large size and the real product size. A male or broad-shouldered body must not make the head appear smaller than the rest of a cute cast; normalize apparent scale using eye/chin/face-width anchors, not outer hair bounds alone.

## Recovery classifier

| User feedback | Treat as | Required response |
| --- | --- | --- |
| “This is not the same person” | Identity failure | Reopen `base_ip_review`; restore the original identity source directly; invalidate dependent assets. |
| “The style changed” | Style/material failure | Compare against the exact style source; version the style only if the requested direction truly changed. |
| “Why is the base wearing a T-shirt?” | Presentation ambiguity | Explain and label the neutral base as construction-only; show the paired signature look. |
| “The outfit is not the original style” | Signature-look failure | Reconstruct the exact supplied outfit before generating derived fashions. |
| “Eyes/head/body are off” | Composition/anatomy failure | Change only the named anchor; keep the original identity source present. |
| “OK” after a mixed board | Ambiguous approval | Write what is definitely approved; ask only about unresolved axes before promotion. |

## Minimize user effort

- Infer low-risk production defaults, but never infer identity approval.
- Present one labeled decision board instead of sending isolated images across many turns.
- Ask at most three short, axis-specific questions at a gate; usually the three base questions above are sufficient.
- Do not expose internal filenames without user-facing labels.
- After approval, summarize the exact locks once and proceed until the next promised gate.
