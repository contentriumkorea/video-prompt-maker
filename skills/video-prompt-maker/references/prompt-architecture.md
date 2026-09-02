# Prompt Architecture

## Authority boundary

Use official documentation for the named model only to understand supported inputs, asset roles, and product limitations. Do not present undocumented behavior as supported or guaranteed. Treat the Seedance 2.0 natural-language structure as this skill's cross-model house style, not as an official format for every model. Treat the model-specific character ceilings and exact `[Sound] no music` directive as user-defined house rules, not official model syntax.

## Semantic order

Build every prompt once in this order:

1. Subject and observable motion.
2. Environment, spatial state, and motivated lighting.
3. Performance and relevant physical cause/effect.
4. Camera movement and composition.
5. One consolidated visual style clause.
6. Exact dialogue or screen text, then non-musical sound.
7. Constraints and continuity.

Use natural prose for the scene groups. After camera/composition, write exactly one consolidated `Style:` clause. Place `[Sound] no music` after that style clause and place all constraints/continuity locks after the Sound line. Do not scatter visual-style instructions before or after the single style clause. Keep subject motion separate from camera movement. Give each shot one dominant visual event and one dominant camera movement; a locked-off camera counts as the shot's single camera instruction.

## Input branches

### T2V

Describe the subject, visible action, environment, lighting, performance or physics, camera, and style from the request. State only details that can appear on screen or be heard as non-musical sound. Do not invent unsupported reference assets.

### First-frame I2V

Identify the supplied image by its actual ordinal, such as `Image 1`, and state that it supplies the first frame. Focus on motion and change after that frame instead of redescribing or contradicting the visible subject. Preserve the composition, colors, and lighting unless the user explicitly requests a visible transition.

### First-and-last-frame I2V

Assign one image as the first frame and one as the final frame using their actual ordinals. Describe a coherent visible transition between those states, preserving identity, geography, and causal continuity. Do not invent intermediate reference tags or claim a perfect match.

### Reference-to-video

Assign each supplied asset one separable responsibility, then describe the target scene. Use an image for a visible identity, object, location, style, first frame, or final frame; use a video for motion, camera rhythm, or a visible action pattern; use audio only for exact dialogue or non-musical ambience that can be separated from any music.

## Reference naming

Refer to assets only as `Image N`, `Video N`, or `Audio N`, matching the user's upload order. State the responsibility explicitly: `Use Image 1 for the character's stable identity` or `Use Video 1 for the walking cadence`. Do not add invented handles, bracket tags, file names, weights, or model-specific tokens that the user did not provide.

## Shot patterns

For a single shot, write one continuous paragraph in the semantic order. Choose one dominant event and one camera instruction.

For multiple shots, use numbered blocks by default and one global style clause after the final shot:

```text
Shot 1: subject/motion; environment/spatial state/light; performance/physics; camera/composition.
Shot 2: subject/motion; environment/spatial state/light; performance/physics; camera/composition.
Style: one global visual treatment.
[Sound] no music, non-musical ambience and effects.
Constraints: continuity locks shared by the sequence.
```

Use exact timestamps only when duration or synchronization is explicitly required. A timed multi-shot block keeps both identifiers in the form `[0s] Shot 1:`. Keep one shot type, one dominant visual event, and one camera movement in each timed beat. Reuse the same character and object names across all shots.

## Exact text and duration

Keep supplied Korean dialogue and screen text verbatim inside quotation marks. Format dialogue as `says in Korean: "..."` when the spoken language matters. Change delivery, timing, gesture, or shot allocation without rewriting the words. If subtitles are requested, keep the same exact wording. Fit dialogue to the available duration; when the exact text is too long, request a longer duration, shorter approved wording, or a split instead of silently truncating or accelerating it beyond intelligibility.
