# Visual Gallery

English | [Chinese](preview-gallery.zh.md)

This gallery shows what the Skill can produce and how its review gates prevent identity, proportion, outfit, and scene drift. The images come from two separate production systems. They are evidence of range and workflow depth, not characters or styles that every run must copy.

## System A — soft anime-tech digital employees

This source production system keeps four distinct identities recognizable while changing role styling and downstream usage. The first matrix demonstrates modular wardrobe expansion: each row remains the same person while outfit construction, color emphasis, and accessories vary by role.

![Four persistent personas across five outfit families](images/08-soft-anime-tech-outfit-matrix.jpg)

The scene matrix demonstrates the next production stage. Approved identities and complete-character combinations are placed into five business contexts: campaign launch, store operations, growth analytics, fulfillment, and an AI workbench. Scene framing changes without silently redesigning the person.

![Four persistent personas across five business scenes](images/09-soft-anime-tech-scene-matrix.jpg)

The motion-source board contains twenty scene frames prepared as the visual basis for short loops. In an actual run, one representative image-to-video result must pass identity, loop, and motion review before the remaining batch is rendered.

![Twenty loop-ready motion source frames](images/10-soft-anime-tech-motion-source-frames.jpg)

## System B — cool/cute neo-street collectible

This later quality-validation case explores a more graphic, less human-like, fashion-led collectible direction. The approved style source combines a large cute head/body ratio, simplified facial structure, dark navy hair with electric-blue accents, and a compact neo-street silhouette.

![Cool cute neo-street digital character](images/00-digital-human-ip-neo-street-tech.png)

The concept board shows why the Skill starts with materially different style directions rather than generating a complete wardrobe immediately. A user approves one direction first; identity construction, gender presentation, outfits, props, scenes, and video are expanded only after the relevant gate passes.

![Three materially different visual directions](images/01-style-directions.png)

## Review evidence, not only polished output

The comparison below records a common failure: a clean render can still be the wrong character. Review boards must compare face geometry, eye spacing, head scale, hair silhouette, head roll, and body construction—not merely image quality.

![Identity drift and recovery comparison](images/02-identity-drift-and-recovery.png)

The outfit recovery board makes the same rule explicit for fashion. A neutral construction master is not a finished signature look, and a generic replacement outfit cannot inherit approval from the identity gate.

![Signature-look drift and recovery comparison](images/03-signature-look-recovery.png)

## Approval-gated production framework

![Approval-gated workflow from idea to reusable IP system](images/en/04-workflow-gates.svg)

![Reusable project contracts and review records](images/en/05-contract-templates.svg)

![Independent dimensions in the composable IP template stack](images/en/06-ip-template-stack.svg)

![Proportion and body-construction templates](images/en/07-proportion-and-body-templates.svg)

The template stack is intentionally independent. A user can change rendering style, proportion, gender presentation, body construction, face, hair, outfit, wearable, prop, palette, or composition without turning an example image into a fixed character template. Stable IDs live in [`ip-template-catalog.json`](../produce-avatar-ip-system/assets/templates/ip-template-catalog.json); workflow rules live in [`ip-template-system.md`](../produce-avatar-ip-system/references/ip-template-system.md).

## Reproduce the structured review loop

Initialize a resumable production workspace:

```bash
python produce-avatar-ip-system/scripts/init_avatar_project.py ./my-avatar-project \
  --project-name my-avatar-project \
  --personas 4
```

Resolve a selected parameter stack into a stage-specific prompt and a machine-readable receipt:

```bash
python produce-avatar-ip-system/scripts/assemble_avatar_prompt.py \
  ./my-avatar-project/brief/ip-template-selection-p01.json \
  --catalog ./my-avatar-project/brief/ip-template-catalog.snapshot.json \
  --stage neutral-base \
  --output ./my-avatar-project/prompts/p01-neutral-base.txt \
  --resolved-output ./my-avatar-project/prompts/p01-neutral-base.resolved.json
```

Build a labeled review board from candidate images or representative video frames:

```bash
python produce-avatar-ip-system/scripts/build_review_sheet.py \
  ./my-avatar-project/candidates/identity/*.png \
  --output ./my-avatar-project/review/contact-sheets/identity-review.png \
  --columns 4 \
  --title "Identity construction review"
```

Only approved assets advance. The source images above are a curated public preview; credentials, signed URLs, private Figma source links, and third-party client source artwork are not included.
