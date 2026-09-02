---
name: video-prompt-maker
description: Use when a user asks to create, rewrite, translate, optimize, review, or troubleshoot a video-generation prompt for T2V, I2V, reference-to-video, multi-shot, storyboard-to-video, Seedance, Higgsfield, Veo, Kling, Sora, Runway, or another video model; also use for I2V requests with a prompt deliverable that makes an image move. Do not use for a standalone still-image prompt, video editing without a prompt deliverable, actual video generation, or an informational model-spec question.
---

# Video Prompt Maker

## Non-negotiable output contract

- Always use the Seedance 2.0 house style, including when another model is named.
- Default to English; preserve exact supplied Korean dialogue/screen text in quotation marks.
- Deliver each prompt in its own fenced code block.
- Keep each body at or below the selected model limit by both Unicode characters and UTF-16 code units.
- Include exact `[Sound] no music` once.
- Remove all generated-music cues and resolve music-centered conflicts before drafting.
- Do not promise model behavior; the contract governs the prompt text.

## Model length policy

| Target model | Maximum characters |
| --- | ---: |
| Seedance 2.0 | 3,800 |
| Seedance 2.5 | 14,000 |
| MiniMax H3 | 6,500 |
| Kling 3.0 | 8,000 |

- When no target model is named, use the Seedance 2.0 limit.
- Treat an unlisted target model as Seedance 2.0 for length validation.
- For separate model variants, apply each variant's own limit independently.
- For one shared prompt targeting multiple models, use the smallest applicable limit; an unlisted model contributes the Seedance 2.0 default.

## Workflow

1. Classify T2V/I2V/reference, single/multi-shot, dialogue, and repair/compression mode.
2. Isolate the current request and map each reference to one responsibility.
3. Establish first-frame occupancy, geography, facing, gaze, contact, and continuity state only when relevant.
4. Write observable action/performance, one dominant camera movement per shot, motivated light, and relevant physical cause/effect.
5. Compile in the single semantic order: subject/motion; environment/spatial state/light; performance/physics; camera/composition; one consolidated visual style clause; dialogue/non-musical sound; constraints/continuity.
6. Use numbered `Shot N` blocks for multi-shot by default; exact timestamps only when required.
7. Resolve the target model, perform the semantic music review in `references/quality-check.md`, then compress and validate each prompt body with `scripts/validate_prompt.py --model "<target model>"`; omit `--model` only when the request names no model. Revise until exit status 0.

## Reference routing

- Read `references/prompt-architecture.md` for all builds.
- Read `references/acting-performance.md` for visible characters or dialogue.
- Read `references/visual-continuity.md` for uploaded assets, I2V, or recurring characters/locations/props.
- Read `references/spatial-physics.md` for multi-character blocking, continuity, interaction, impact, liquids, cloth, or debris.
- Read `references/quality-check.md` before final delivery and for repair/compression.

## Conflict handling

- The no-music and selected model-length contracts override conflicting prompt-preservation requests.
- If exact user text alone exceeds the limit, request shortening or a split; never truncate it silently.
- If music-making is the indispensable visual premise, ask for a non-musical replacement; otherwise convert it to a silent non-performing state.
- Do not claim that the Seedance house style is an official format for another named model.

## Delivery

- Default to the finished prompt only.
- Put requested analysis outside the prompt code block.
- Validate multiple variants independently.
