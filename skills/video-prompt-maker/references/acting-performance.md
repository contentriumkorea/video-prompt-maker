# Acting and Performance

## Scope and intent

Use this reference when visible character performance or dialogue matters. Do not add an acting arc to an unpeopled landscape, product shot, or purely mechanical action. A neutral performance can remain neutral.

Translate the character's immediate objective into behavior the camera can record: obtaining an answer, maintaining composure, hiding a reaction, or refusing an approach. Use the current request and reference evidence; do not invent history, relationships, trauma, or new plot to explain motivation. A label such as `she feels suspicious` is not enough by itself. Select a paused reach, guarded weight shift, tightened grip, or directed glance only when it serves that objective and is visible.

## Keep planning layers separate

Keep shared identity, wardrobe, geography, and accumulated state at the scene level; framing and the dominant camera instruction at the shot level; and performance changes inside that shot. Compile these into the existing prompt order, not a mandatory eight-field table or a second output format.

One dominant visual event can contain several small, causally connected acting beats. A character can hold composure, briefly lose it, and recover during one confrontation without requiring three shots or three camera moves. Do not add a fixed number of beats, timestamps, or unnecessary cuts.

## Cue, change, and carry-forward state

For a meaningful change, connect only the necessary parts of this sequence:

- Entry state and immediate objective: what the character is visibly doing or trying to maintain.
- Trigger: a supplied word, another visible character's response, a named event, or a meaningful absence of an expected response.
- Observable change: the smallest readable shift in gaze, breath, posture, hands, distance, facial movement, or speech delivery.
- Exit state: what remains after the line or action and carries into the next beat or shot.

Do not merely stack opposing emotion labels. When the request calls for restraint or mixed emotion, show what the character is trying to suppress and what visibly gives way first. For example, a character may keep questioning while only the last word trembles; this is different from immediate sobbing. Do not default every emotion to tears, shouting, or a smile.

## Timing and intensity

- For a brief shot, choose one readable action and at most one supporting reaction.
- For a medium shot, connect the trigger, visible change, and consequence.
- For a longer shot, allow the current state to persist before it changes; carry attention, breath, posture, and interpersonal distance forward rather than resetting the performance.

Where timing matters, describe onset (when the response begins), apex (its strongest point), and offset (how it settles). Do not start every reaction at full intensity or force a complete recovery. A pause can contain held attention, a swallowed word, a delayed breath, or another requested visible action; it need not be empty.

Prefer relative cues such as `after the unanswered question` or `on the final word`. Use exact seconds only when the user supplies them or synchronization requires them; fit the response to the requested duration rather than inventing precise physiological timing.

## Dialogue as a timing reference

Keep supplied dialogue exact, including Korean wording and punctuation. Put delivery instructions outside the quoted line; do not insert ellipses, stutters, extra words, or rewritten punctuation into locked text. Use `says in Korean: "..."` when language identification is needed.

Anchor a change to the speaker's supplied word or the other character's supplied response when useful. Specify what is visible before speech, which part changes delivery, what happens during a meaningful pause, and what remains after speech. Select only what the scene needs; do not mark every word or invent an interlocutor's answer.

If exact text cannot fit the duration intelligibly, ask for an approved shortening, more time, or a split. Do not solve the conflict by rushing speech or changing the words.

## Prevent premature reactions

When a premature response would spoil the requested progression, bound the inhibition to a cue or interval: `no tears before the second question ends`, rather than an unqualified `never cry` when later tears are required. Show the effort to hold the response back when visible and relevant.

Check that each prohibition ends when the permitted response begins. A shared final Constraints line must not contradict a later beat. If the user forbids a response for the entire scene, preserve that full exclusion instead of inventing a later release.

## Facial detail and optional FACS/AU

Describe visible facial motion in plain language first: its region, direction, intensity, and timing. Prefer one or two useful changes to a simultaneous list of brow, lid, nose, lip, and chin commands. A facial close-up can support details that a distant or rear view cannot.

FACS action units (AU) are optional anatomical shorthand, not emotion labels or model-native tokens. Use an AU only when its meaning is known, the model can usefully receive it, and the request or a difficult visible distinction benefits from technical precision. Keep the plain-language movement with it. Otherwise omit the code; never guess a number, require AU in every prompt, or map one AU to one emotion. Do not assume all models understand AU codes or A-E intensity scales, and do not promise exact compliance.

## Character scope and continuity

Direct only characters present in the shot and features visible in the framing. Name the gaze target when it matters. Use hands or posture only when visible; do not add off-screen reactions or hidden facial details.

Preserve state inertia: a soaked coat stays heavy, a guarded stance does not vanish between shots, and an impact affects balance until visible recovery. Carry the exit state of a performance beat into the next one. A cut alone does not reset composure, wetness, attention, or unresolved tension.

## Review and compression

Review whether the trigger precedes the reaction, the response fits the framing and duration, its inhibition has the correct scope, and the next beat inherits its exit state. These are semantic checks: the bundled validator checks text contracts, not acting quality or model performance.

Under the selected length limit, preserve the objective's visible evidence, the decisive cue and response, exact dialogue, and necessary carry-forward state. Remove optional AU notation and redundant facial detail before breaking that causal chain. Never relax the selected limit or the sound contract.

## Exclusions

- Do not use demographic, cultural, gendered, disability, or occupational stereotypes as acting shorthand.
- Do not require eye contact, blinking, tears, smiles, breath changes, or an emotional reversal in every performance.
- Do not guarantee emotional realism, lip sync, facial consistency, precise response timing, or performance reproduction.

## Source note

This reference incorporates an original, scoped adaptation of the acting-direction ideas illustrated in [Foyege's tutorial](https://www.youtube.com/watch?v=XMfnuc2Nf_w), particularly dialogue cues, response timing, scoped inhibition, and natural-language-first facial direction. It does not reproduce the tutorial's full prompts or adopt its quality claims as guarantees.
