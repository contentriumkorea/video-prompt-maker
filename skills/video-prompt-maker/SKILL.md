---
name: video-prompt-maker
description: Use for creating, rewriting, translating, optimizing, reviewing, or troubleshooting any video-generation prompt, including T2V, I2V, reference-to-video, multi-shot, storyboard-to-video, or an I2V request that explicitly asks for a prompt deliverable to make an image move. Trigger when Seedance, Higgsfield, Veo, Kling, Sora, Runway, or any other video model is named; always deliver Seedance 2.0-style natural-language prompts even for other named models. Do not use for standalone still-image prompts, video editing without a prompt deliverable, actual video generation, or informational model-spec questions.
---

# Video Prompt Maker

## Non-negotiable output contract

- Always use the Seedance 2.0 house style, including when another model is named.
- Default to English; preserve exact supplied Korean dialogue/screen text in quotation marks.
- Deliver each prompt in its own fenced code block.
- Keep each body at or below 3,800 by Unicode characters and UTF-16 code units.
- Include exact `[Sound] no music` once.
- Remove all generated-music cues and resolve music-centered conflicts before drafting.
- Do not promise model behavior; the contract governs the prompt text.

## Workflow

1. Classify T2V/I2V/reference, single/multi-shot, dialogue, and repair/compression mode.
2. Isolate the current request and map each reference to one responsibility.
3. Establish first-frame occupancy, geography, facing, gaze, contact, and continuity state only when relevant.
4. Write observable action/performance, one dominant camera movement per shot, motivated light, and relevant physical cause/effect.
5. Compile in the single semantic order: subject/motion; environment/spatial state/light; performance/physics; camera/composition; one consolidated visual style clause; dialogue/non-musical sound; constraints/continuity.
6. Use numbered `Shot N` blocks for multi-shot by default; exact timestamps only when required.
7. Perform the semantic music review in `references/quality-check.md`, then compress and validate each prompt body with `scripts/validate_prompt.py`; revise until exit status 0.

## Reference routing

- Read `references/prompt-architecture.md` for all builds.
- Read `references/acting-performance.md` for visible characters or dialogue.
- Read `references/visual-continuity.md` for uploaded assets, I2V, or recurring characters/locations/props.
- Read `references/spatial-physics.md` for multi-character blocking, continuity, interaction, impact, liquids, cloth, or debris.
- Read `references/quality-check.md` before final delivery and for repair/compression.

## Conflict handling

- The no-music and 3,800-character contracts override conflicting prompt-preservation requests.
- If exact user text alone exceeds the limit, request shortening or a split; never truncate it silently.
- If music-making is the indispensable visual premise, ask for a non-musical replacement; otherwise convert it to a silent non-performing state.
- Do not claim that the Seedance house style is an official format for another named model.

## Delivery

- Default to the finished prompt only.
- Put requested analysis outside the prompt code block.
- Validate multiple variants independently.
