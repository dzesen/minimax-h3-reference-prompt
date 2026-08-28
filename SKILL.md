---
name: minimax-h3-reference-prompt
description: Compile, review, revise, or reverse-reconstruct reference-based video briefs and media in any language as production-ready MiniMax H3 Ref2VA prompts. Use when attached or named images, videos, or audio define subjects, concrete frame anchors, motion, style, editing sources, continuation, voice, or soundtrack relationships, including requests to recreate an observed result as the canonical six-section subject_definitions format. Do not use for text-only T2VA briefs with no reference asset.
---

# MiniMax H3 Reference Prompt

Compile multilingual briefs or observed media into the canonical MiniMax H3 full-reference structure without changing the user's creative intent, inventing references, or claiming to recover unavailable generation data.

## Workflow

1. Classify the request as forward compilation, review, revision, or reverse reconstruction. Confirm that at least one real or named reference image, video, or audio will remain attached to the H3 run.
2. Read [references/format-spec.md](references/format-spec.md) completely before drafting, revising, or reviewing. For a revision, also read [references/revision-compiler.md](references/revision-compiler.md). For reverse reconstruction, also read [references/reverse-reconstruction.md](references/reverse-reconstruction.md) before inspecting media.
3. Check the platform envelope before writing. Do not compile an impossible request and hope prose will repair it.
4. Build an internal director blueprint with the constraint ledger, Reference Responsibility Matrix, beat/state ledger, and audio routing table described below. Do not expose these working tables unless the user asks.
5. Compile the blueprint into the six sections in the exact order from the format specification. Preserve the user's literals and hard creative choices; add only low-risk execution detail.
6. Run the deterministic validator when local execution is available, then perform the semantic preflight. Repair errors; review warnings rather than mechanically suppressing them.

## Platform Envelope

- Target duration is an integer from 4 through 15 seconds. If omitted, use 10 seconds as this skill's convenience assumption and disclose that assumption outside the prompt; it is not an official H3 default.
- The prompt is at most 7,000 Unicode characters. Compress by priority and recompile if needed; never truncate by characters or lines.
- A Ref2VA request supports at most 9 images, 3 videos, 3 audio files, and 12 mixed reference files. Each reference video or audio file is 2-15 seconds; total reference-video duration and total reference-audio duration are each at most 15 seconds. The API request body is at most 64 MB.
- If aspect ratio is omitted, keep the Ref2VA run `adaptive`. Lock a fixed ratio only when the user or delivery platform explicitly requires it. Do not infer a fixed ratio merely from one reference's composition.
- API transport roles and prompt semantic labels are different layers. `first_frame` or `last_frame` API roles cannot coexist with any `reference_*` role in one request. A `<Picture N>` used as a Ref2VA keyframe or composition anchor is still uploaded as a reference image; do not relabel it as an API first/last-frame role.
- Treat an audio-only reference set as a feasibility warning: MiniMax's open-source announcement requires a reference image or video alongside reference audio. Do not fabricate a visual reference to silence the warning.
- If the requested target exceeds 15 seconds, never emit one invalid prompt. Shorten only with permission. When the user clearly requests a long-form or multi-clip deliverable, split it into legal clips and carry an explicit continuity handoff; otherwise ask whether to shorten or segment.

## Director Blueprint

### Constraint Ledger

Lock the user's duration, fixed ratio if any, identities, wardrobe or product design, required actions, exact words, required frame moments, prohibited content, and requested output mode. Mark each item as `literal`, `hard`, or `flexible`. User-provided literals and hard constraints outrank embellishment.

### Reference Responsibility Matrix

Create one internal row for every attached asset:

`asset/order -> API transport role -> semantic labels -> primary contribution -> optional secondary contribution -> preserve/change boundary -> conflict priority -> active shots/time -> audio-track handling -> confidence`

- Give each asset a narrow primary responsibility. One asset may supply multiple subjects, and one subject may combine appearance, motion, or sound from several assets.
- State conflict priority instead of asking the model to reconcile incompatible identity, costume, composition, motion, or camera evidence.
- Do not introduce a label for an unattached asset. Do not leave an attached asset's intended role implicit.
- A multi-panel character sheet is an identity or layout source unless the user explicitly wants the grid reproduced. Warn when its layout may be copied unintentionally.

### Beat and State Ledger

- Separate a Shot, which begins at a cut, from timed beats inside the same continuous shot.
- Divide each shot into causal phases only as needed: establish, prepare, execute, settle/hold, and end-state lock. A beat may contain secondary reactions, but it has one main observable state change.
- Track subject pose, hands and props, gaze, screen position, environment landmarks, camera side/height/distance/direction/speed, light, particles, audible phase, and unfinished momentum. The next beat's initial state must match the previous locked end state unless an explicit cut reveals a justified change.
- Give each shot one dominant camera trajectory. Describe movement type, range, speed, motivation, and framing result when material. Do not add camera motion merely to make the prompt sound cinematic.
- Resolve spatial camera language against named anchors. State whether "behind," "around," or "to the side" is relative to the subject, a vehicle, a prop, or the set; ask only when two plausible readings would materially change the result.
- Allocate real time for anticipation, execution, follow-through, dialogue, reaction, and camera settling. Simplify flexible secondary motion before altering a required beat.

### Audio Routing Table

- Route dialogue and lyrics to the timed shot description; ambience, Foley, physical sounds, and non-verbal human sounds to `overall_soundscape`; diegetic music to the timed shot; audience-only score to `non_diegetic_music`.
- Bind each impact to a visible cause or identify it as an audience-only score accent. Do not imply an unseen opponent, prop, or event.
- Prevent one BGM from being requested simultaneously as copied source audio, newly generated diegetic music, and independent non-diegetic score unless the user explicitly wants layered versions.
- If an analysis tool did not actually hear or transcribe audio, do not invent timbre, words, rhythm, or music structure. Ask for a transcript or role description only when the missing information materially changes the result.

## Language Contract

- Accept source briefs in any language, including mixed-language input.
- Write all six section labels, descriptions, shot directions, and fixed relationship markers in English.
- Preserve user-supplied dialogue, lyrics, product copy, signage, proper names, and other visible text exactly, including punctuation, in its original language. Do not translate, paraphrase, or silently correct it.
- For words transcribed from reference audio, preserve the source words and language, normalize only basic sentence punctuation as required by the official Ref2VA guide, and use `[unclear]` instead of guessing.
- Use the same language contract when reviewing or revising an existing prompt.

## Intent and Feasibility

- Treat duration, aspect ratio, reference identity, wardrobe or product design, required actions, exact words, prohibited content, and requested shot moments as hard constraints.
- Add concrete staging, lighting, motion continuity, and sound details only when they clarify the user's intent.
- Do not invent characters, brands, dialogue, readable text, props, audio categories, plot turns, or reference relationships. If creative latitude is necessary, prefer reversible environment or lighting details and keep them sparse.
- Give each major action observable anticipation, execution, and follow-through when the action needs those phases to read. When a timeline is overloaded, simplify secondary camera motion or environmental effects before changing a required action.
- Replace unsupported impact sounds with a visible sound source or a clearly non-diegetic music accent. Do not imply an unseen opponent, prop, or event.
- Express exclusions as positive scene states when possible, such as an empty stage with abstract graphics and no legible lettering.
- Use a short, scoped negative constraint only when a strong model prior would otherwise contradict a hard requirement. Never append a generic negative-prompt dump.

## Validation

When the script is available, run:

```text
python scripts/validate_ref2va_prompt.py PROMPT.txt --duration SECONDS --picture-count N --video-count N --audio-count N
```

Pass only facts known from the actual request. A PASS covers supplied metadata only: omitted reference-file durations and request size remain unchecked. The validator proves syntax, limits, numbering, label/retention closure, and timestamp consistency; it cannot prove identity fidelity, physical plausibility, exact literal preservation, absence of invented content, or generation quality. Treat its warnings as review prompts, not reasons to distort the user's brief.

## Response Modes

For a new or revised prompt, return one copy-ready plain-text block containing the six sections. Keep assumptions or material conflict notes outside that block and to one short paragraph.

For review-only requests, lead with the highest-impact issues in concise prose. Do not rewrite the prompt unless the user asks for a revision or optimization.

For reverse-reconstruction requests, return a concise reconstruction note followed by one copy-ready prompt block. The note distinguishes observed evidence, inference, and unavailable information; it is not part of the H3 prompt. Describe the result as a reconstruction, never as the recovered original prompt.

If the generation run will contain no real or named reference image, video, or audio, explain that this Ref2VA skill must not fabricate reference labels. Recommend an H3 base-mode prompt instead, including when the user wants a text-only recreation of finished media that will not remain attached as a reference.
