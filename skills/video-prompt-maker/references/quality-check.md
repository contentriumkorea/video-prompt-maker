# Quality Check

## Review in this exact order

1. **Intent:** Confirm the prompt produces the requested scene and deliverable rather than commentary or an actual video.
2. **Stale context:** Remove superseded details, prior variants, and assumptions that belong to earlier requests.
3. **References:** Verify every supplied `Image N`, `Video N`, and `Audio N` has one clear responsibility and no asset or tag was invented.
4. **Blocking:** Confirm relevant first-frame occupancy, position, facing, gaze, landmarks, contact, screen direction, and accumulated state.
5. **Action:** Keep one dominant observable visual event per shot with a readable cause or transition.
6. **Camera:** Keep one dominant camera movement or one locked-off instruction per shot; remove competing moves and technical rituals.
7. **Lighting:** Name a motivated light source or a clear lighting condition and keep its direction consistent unless it visibly changes.
8. **Acting:** Use duration-appropriate, visible reaction, gaze, breath, posture, hands, distance, and state inertia without stereotypes.
9. **Physics:** Retain only relevant mass, contact, inertia, friction, weight transfer, cloth, liquid, debris, or impact cues; respect stylized rules.
10. **Style:** Consolidate visual treatment into exactly one `Style:` clause after camera/composition.
11. **Dialogue/text:** Preserve supplied Korean dialogue and screen text exactly in quotation marks, and ensure it can fit the duration.
12. **Music:** Apply the contextual policy below and keep exact `[Sound] no music` once after the Style clause.
13. **Constraints:** Keep continuity locks after the Sound line.
14. **Length:** Resolve the target model and validate the body at or below its limit by both Unicode characters and UTF-16 code units. Use Seedance 2.0 when no model is named or the named model is unlisted.

## Music-term policy

Remove generated-music language after preserving the one exact Sound directive. Reject high-confidence musical requests or structures, including `BGM`, `OST`, `soundtrack`, `background music`, instrumental/orchestral/musical scores or tracks, described song/singing/humming, melodic whistling, a band/orchestra/choir performing, a named musician playing, and audience motion synchronized to a beat or tempo. Treat Korean cues such as `배경음악`, music starting or playing, singing, instrument/band performance, and motion `박자에 맞춰` as the same conflict.

Judge terms in context, not as isolated words. `Song dynasty`, `color harmony`, `choir stalls`, `sports score`, `tracking shot`, `heartbeat`, `narrative beat`, and `pitch-black` are non-musical uses and remain valid. Replace a requested soundtrack with scene-motivated ambience or effects only when that preserves the visual premise. If performing music is indispensable to the visible action, ask for a non-musical replacement before drafting.

Treat requested singing, instrument or band performance, audience movement synchronized to a musical beat, and soundtrack or OST dependence as indispensable music-making when they define the scene. Stop and ask for a non-musical replacement before drafting; do not restage them as silent or indirectly worded performance.

## Compression priority

Preserve, in order, the core action, exact supplied dialogue or screen text, explicit reference responsibilities, spatial and state continuity, and exact Sound directive. Then preserve the single camera instruction, motivated light, and necessary performance or physical consequence. Compress or remove repeated adjectives, duplicate style clauses, secondary environment detail, redundant negative constraints, and decorative modifiers first. Never silently truncate exact text or split a required reference mapping.

## Validator

Save only the prompt body, without the surrounding code fence, as a UTF-8 text file. Run with the canonical target model:

```powershell
python scripts/validate_prompt.py --model "Kling 3.0" prompt.txt
```

Use `Seedance 2.0` (3,800), `Seedance 2.5` (14,000), `MiniMax H3` (6,500), or `Kling 3.0` (8,000). Omit `--model` only when no target model is named; an omitted or unlisted model uses Seedance 2.0. Repeat `--model` for one shared prompt targeting multiple models; the validator applies the smallest applicable limit. Validate separate variants with their own model argument.

Exit status `0` and output `ok=true ... violations=none model=<resolved-model> max_chars=<limit>` mean the deterministic contract passes. Exit status `1` identifies one or more prompt violations: `empty`, `unicode-length`, `utf16-length`, `sound-directive-count`, `music-language`, or `code-fence`. Exit status `2` means the input could not be read or decoded. Revise the prompt body and rerun until status `0`.

The validator uses only high-confidence contextual patterns. It cannot recognize every euphemism, visual performance, Korean phrasing, or indirect musical concept. Semantic music review is mandatory even after exit status `0`; never describe the validator as a guarantee that a stochastic model will emit no music.

## Boundary and guarantees

The model-specific limits and exact `[Sound] no music` string are user-approved house rules, not official model syntax. Official model documentation may describe supported inputs or limits, but it does not turn this cross-model house style into a native format. A prompt-only prohibition removes requests for generated music; it cannot guarantee that a stochastic video system will never output music, nor can any prompt guarantee exact acting, motion, identity, physics, or continuity.
