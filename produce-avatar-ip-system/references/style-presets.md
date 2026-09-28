# Style Presets and Switching

Style is an upstream contract. Select or define it before identity approval. Switching style after identity approval creates a new `style_version` and requires new identity masters; do not mix a realistic head with a chibi body or keep editing an old derivative until it vaguely resembles the new direction.

The canonical machine-readable style and proportion options live in `assets/templates/ip-template-catalog.json`. Read [ip-template-system.md](ip-template-system.md) and choose style and proportion separately. A style preset is not a fixed face, hairstyle, outfit, gender, or character image.

## Style token schema

Record these fields in `prompt-contract.yaml`:

| Token | Controls |
| --- | --- |
| `preset` | Stable preset ID |
| `realism` | Stylized → realistic continuum |
| `head_body_ratio` | Apparent head share within the visible upper body |
| `eye_scale` | Relative to normal human/anime proportions |
| `feature_detail` | Nose, lips, skin, brows, lashes |
| `material` | Vinyl, clay, soft polymer, PBR skin/fabric, etc. |
| `geometry` | Rounded/simplified versus anatomical/angular |
| `lighting` | Studio softness, contrast, rim intensity |
| `expression` | Neutrality and emotional range |
| `motion_amplitude` | Small-UI readability versus natural subtlety |
| `negative_style` | Drift patterns to exclude |

Identity tokens—face contour, hair silhouette, skin tone, eye/brow shape—remain separate. A style preset must not define a specific ethnicity, gender, or brand identity.

## Translate subjective words into separate controls

Do not let one adjective change every axis. Record these user-facing controls independently:

| User intent | Change by default | Do not change unless requested |
| --- | --- | --- |
| `cool / trendy` | hair silhouette, outfit silhouette, accessories, hardware, palette contrast, attitude | realism, facial anatomy, visual age, head/body ratio |
| `cuter` | head/body ratio, eye scale, cheek/jaw softness, compact torso | gender presentation, identity, signature outfit |
| `more Q / chibi` | use/version the Q preset and regenerate the anchor identity | merely enlarge the head on a realistic torso |
| `more real` | feature detail, anatomy, skin/hair/fabric material, lighting | celebrity likeness or unapproved identity changes |
| `more premium` | material separation, hardware restraint, lighting, seam/detail discipline | automatic dark grade, hard armor, excessive gloss |

When the user asks for “cool but cute,” keep the selected cute/realism contract stable and express coolness through fashion and attitude. Show the resulting values on the direction board so later corrections do not silently change the wrong axis.

## Preset: `soft-anime-tech-3d`

Best for approachable digital employees, product avatars, B2C/B2B assistants, notifications, and compact UI.

~~~text
Friendly premium stylized 3D anime digital employee; slightly enlarged expressive eyes; simplified nose and mouth; soft rounded jaw; compact upper-body proportions; clean continuous sculpt; tactile soft-polymer skin, soft-vinyl accessories, and fabric with restrained stitching; bright warm studio key, gentle colored rim, crisp translucent optics; competent and friendly, not childish; readable at small UI size.
~~~

- `realism`: 0.35
- `head_body_ratio`: 0.42–0.48 of visible upper-body composition
- `eye_scale`: 1.12–1.22× natural
- `motion_amplitude`: medium-high
- avoid: photoreal pores, hard cyberpunk armor, dark dystopian grade, baby proportions.

This is closest to the source Aident system, but it is not a universal default.

## Preset: `cute-collectible-3d`

Best for consumer emotion, onboarding rewards, stickers, celebration states, and collectible variants.

~~~text
Cute premium 3D collectible character; rounded silhouette; larger head and eyes; short compact torso; soft cheeks and simplified features; plush-vinyl material mix with clean seams; gentle pastel studio light; clear joyful expressions; polished product-toy finish rather than infant or mascot caricature.
~~~

- `realism`: 0.22
- `head_body_ratio`: 0.50–0.56
- `eye_scale`: 1.22–1.35×
- `motion_amplitude`: high with overshoot and settle
- props: simplified 10–20% larger for readability
- avoid: baby cues, drool, toddler anatomy, overly glossy plastic, franchise imitation.

## Preset: `q-chibi-3d`

Best for very small avatars, sticker packs, gamified states, and highly expressive motion.

~~~text
Q-version chibi 3D character with an oversized complete head, very compact upper body, large readable eyes, tiny simplified nose and mouth, rounded hands and props, bold clean silhouette, soft toy-like material, simple high-contrast lighting, and expressive but controlled gesture language.
~~~

- `realism`: 0.12
- `head_body_ratio`: 0.58–0.66
- `eye_scale`: 1.35–1.55×
- `motion_amplitude`: very high; keep camera locked
- hands: simplified but complete, five fingers only when the chosen rendering level makes them legible
- avoid: grafting a large head onto an unchanged realistic torso, infant anatomy, excessive detail at small scale.

## Preset: `premium-toy-3d`

Best for brand mascots, marketing key art, landing pages, and merchandise-like collectibles.

~~~text
Premium designer-toy 3D character; iconic silhouette; simplified sculptural facial planes; satin vinyl, anodized hardware, tactile fabric, and controlled translucent accents; editorial product lighting; restrained expression; high material separation and collectible-grade finish.
~~~

- `realism`: 0.30
- `head_body_ratio`: 0.44–0.52
- `eye_scale`: 1.05–1.18×
- `motion_amplitude`: medium
- avoid: cheap plastic shine, busy seams, NFT/crypto motifs unless requested.

## Preset: `semi-real-digital-human-3d`

Best for expert assistants, enterprise roles, presentations, and high-trust product surfaces.

~~~text
Semi-realistic 3D digital employee; anatomically plausible head and upper body; natural eye size with slightly softened proportions; refined but simplified skin, hair, and fabric; premium PBR material without uncanny pore-level detail; soft cinematic studio lighting; subtle professional expression and natural gesture.
~~~

- `realism`: 0.62
- `head_body_ratio`: 0.34–0.40
- `eye_scale`: 1.00–1.06×
- `motion_amplitude`: medium-low, amplified only enough for target size
- avoid: photoreal celebrity resemblance, waxy skin, doll eyes, anime mouth, toy torso.

## Preset: `realistic-digital-human`

Best when the user explicitly wants a human-like spokesperson or photoreal employee rather than an IP mascot.

~~~text
Realistic but non-celebrity digital human; anatomically accurate face and upper body; natural eye and head proportions; realistic skin with restrained texture, believable hair strands, physically based fabric and hardware, neutral studio color science, and authentic professional micro-expression.
~~~

- `realism`: 0.85
- `head_body_ratio`: 0.31–0.36
- `eye_scale`: 1.0×
- `motion_amplitude`: low-natural
- require: explicit consent/rights for any real-person reference
- avoid: identity cloning without authorization, celebrity likeness, beauty-filter distortion, stylized eye/face ratios.

## Prompt assembly

Build prompts from independent blocks:

~~~text
[USE CASE]
[REFERENCE ROLES]
[IDENTITY LOCK]
[STYLE PRESET BLOCK]
[MATERIAL/LIGHTING LOCK]
[ASSET-SPECIFIC CHANGE]
[COMPOSITION ANCHORS]
[PROP/WEARABLE PHYSICS]
[BACKGROUND CONTRACT]
[NEGATIVE CONSTRAINTS]
~~~

Use one preset block. Do not concatenate `cute`, `realistic`, `chibi`, and `premium` adjectives. If the user wants a blend, define a named custom preset with explicit numeric/visual tokens and version it.

## Switching styles

When the user asks “make it cuter/more realistic/more Q”:

1. Identify whether this is a local adjustment or a new preset.
2. If head/body ratio, eye scale, feature detail, material, or lighting changes materially, create a new style version.
3. Return to the highest-resolution identity source.
4. Generate one representative identity sample in the new style.
5. Approve it beside the old version at the real target size.
6. Regenerate downstream assets from the new identity master; do not transform the entire old matrix blindly.
7. Keep filenames stable only when the new style intentionally replaces the old system. Otherwise add a style-version field to the manifest and Figma component axes.

## Style consistency checks

- Face, hair silhouette, skin tone, and persona distinctions survive the preset.
- All personas use the same realism level and material family.
- Outfit and prop detail matches the character detail level.
- Background complexity does not exceed the subject style.
- Motion amplitude matches the preset and target display size.
- No matrix cell drifts toward another preset.
- Subjective words were translated into explicit controls; fashion adjectives did not silently change realism or identity.
