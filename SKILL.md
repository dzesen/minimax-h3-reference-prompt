---
name: minimax-h3-reference-prompt
description: Convert, expand, or review reference-based video briefs in any language as production-ready MiniMax H3 Ref2VA prompts. Use when images, videos, or audio define subjects, keyframes, motion, style, editing sources, continuation, voice, or soundtrack relationships and the output should use the six-section subject_definitions format. Do not use for text-only T2VA briefs with no reference asset.
---

# MiniMax H3 Reference Prompt

Compile multilingual briefs into the canonical MiniMax H3 full-reference structure without changing the user's creative intent.

## Workflow

1. Read [references/format-spec.md](references/format-spec.md) completely before drafting, revising, or reviewing a prompt.
2. Extract the target duration, aspect ratio, reference assets and roles, preserved subject traits, shot beats, camera paths, spoken or visible text, physical sounds, and audience-only music.
3. Resolve only execution-level ambiguity. Preserve every explicit creative choice. If duration is missing, use 10 seconds; if aspect ratio is missing, infer it from the intended platform or reference composition and disclose that assumption in one short line outside the prompt.
4. Build a continuous audiovisual timeline, then compile the six sections in the exact order from the format specification.
5. Run the preflight in the format specification. Repair every failed check before returning the prompt.

## Language Contract

- Accept source briefs in any language, including mixed-language input.
- Write all six section labels, descriptions, shot directions, and fixed relationship markers in English.
- Preserve user-supplied dialogue, lyrics, product copy, signage, and other visible text exactly in its original language. Do not translate, paraphrase, or silently correct it.
- Use the same language contract when reviewing or revising an existing prompt.

## Intent and Feasibility

- Treat duration, aspect ratio, reference identity, wardrobe or product design, required actions, exact words, prohibited content, and requested shot moments as hard constraints.
- Add concrete staging, lighting, motion continuity, and sound details only when they clarify the user's intent.
- Give each major action observable anticipation, execution, and follow-through. When a timeline is overloaded, simplify secondary camera motion or environmental effects before changing a required action.
- Give each shot one readable dominant camera trajectory. Describe motion type, range, and speed in natural English, and state how the subject remains framed.
- Replace unsupported impact sounds with a visible sound source or a clearly non-diegetic music accent. Do not imply an unseen opponent, prop, or event.
- Express exclusions as positive scene states when possible, such as an empty stage with abstract graphics and no legible lettering.

## Response Modes

For a new or revised prompt, return one copy-ready plain-text block containing the six sections. Keep assumptions or material conflict notes outside that block and to one short paragraph.

For review-only requests, lead with the highest-impact issues in concise prose. Do not rewrite the prompt unless the user asks for a revision or optimization.

If the request contains no real or named reference image, video, or audio, explain that this Ref2VA skill must not fabricate reference labels. Recommend an H3 base-mode prompt instead, or ask for the intended reference asset when the user specifically requires the six-section format.
