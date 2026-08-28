# Reverse Reconstruction

Use this reference only when the user asks to infer, reconstruct, recreate, reverse-engineer, or derive an H3 prompt from existing image, video, or audio media.

The result is a functional reconstruction prompt, not recovery of the original prompt. Source wording, seed, sampler, hidden model settings, omitted references, and creator intent remain unavailable unless the user supplies them.

## Choose the Reconstruction Target

Establish how the observed media will relate to the next H3 generation before assigning labels.

- **Media remains attached:** When the image, video, or audio will be supplied to H3, produce the six-section Ref2VA prompt. Assign labels according to the role the asset will play in the new generation.
- **Finished video as a reference:** Use `<Video N>` for camera, cut, action, pacing, or temporal structure. Define visible people, objects, environments, styles, or performances derived from it as separate `<Subject N>` entries. Define `<Audio N>` only when its signal or audible properties will actually be copied or referenced.
- **Text-only recreation:** When the observed media will not be supplied to H3, do not emit unresolved reference labels or pretend the media remains available. Return an evidence-based reconstruction brief and recommend compilation with an H3 base-mode prompt.

If the user's intended target is ambiguous, prefer a Ref2VA reconstruction only when the supplied media is clearly meant to remain attached for generation. Otherwise state the two possible outputs and ask which one they need.

## Build an Evidence Ledger

Inspect the available media with suitable host tools before writing. Sample the beginning, end, every cut boundary, action extrema, identity-revealing close-ups, composition changes, and meaningful audio transitions. Inspect additional frames when fast movement, occlusion, or a suspected cut remains ambiguous.

Record three evidence classes:

- **Observed:** Directly visible, audible, or available from reliable media metadata. Examples include duration, aspect ratio, cut time, clothing color, subject position, spoken words that are clearly intelligible, and the presence of a music layer.
- **Inferred:** A plausible production instruction derived from evidence but not directly recoverable. Examples include a push-in inferred from parallax, approximate tempo, a likely wide lens, intended secondary cloth motion, or lighting direction.
- **Unavailable:** Original wording, random seed, sampler, hidden generation parameters, references not provided, and any obscured or inaudible content.

Keep the ledger outside the final H3 prompt. The prompt itself should be decisive and production-ready, while the reconstruction note discloses uncertainty concisely in the user's language.

## Reconstruct the Timeline

1. Read technical metadata when available: duration, dimensions, aspect ratio, frame rate, and whether an audio stream exists.
2. Mark shot boundaries and transition types. Distinguish a true cut from motion blur, occlusion, flashes, or a fast whip.
3. For every shot, record opening composition, subject placement and appearance, environment, lighting, action phases, camera trajectory, framing result, synchronized sounds, and end state.
4. Distinguish subject motion from camera motion. Use parallax, changing perspective, scale change, and background displacement to separate tracking, arc, pan, push, pull, zoom, rise, and roll.
5. Track recurring subjects across shots. Preserve only traits supported by clear views or supplied reference assets; leave concealed details unspecified.
6. Segment audio into dialogue or singing, physical effects, ambience, diegetic music, and audience-only score. Preserve exact words only when reliably audible. Use `[unclear]` for unintelligible spans instead of guessing.
7. Convert the evidence ledger into reference roles, then apply the canonical format specification.

## Reconstruction Discipline

- Prefer functional camera language over unsupported technical precision. When focal length, aperture, BPM, lighting hardware, or stabilization method is uncertain, describe the observable visual or audible result.
- Treat compression noise, frame interpolation artifacts, accidental flicker, watermarks, and isolated anatomy failures as source artifacts unless the user explicitly wants them reproduced.
- Treat repeated, coherent rendering traits as style evidence. A single blurred or occluded frame is weak evidence.
- Preserve chronology and spatial continuity even when the source contains rapid action. Allocate explicit time for anticipation, execution, follow-through, and camera settling.
- A single image supports appearance, composition, environment, and style reconstruction, but not observed temporal motion or audio. Any proposed action, camera path, or sound from a still image is inference and belongs in the reconstruction note.
- An audio-free or muted source supports no claim about dialogue, ambience, effects, or music. Use the user's requested audio design or `N/A` where the canonical format permits it.
- Visible text, dialogue, and lyrics remain exact when legible or intelligible. Do not complete cropped, obscured, or unclear content from context.

## Reconstruction Note

Before the prompt block, write one compact note in the user's language using this semantic structure:

```text
Reconstruction note: Observed — ... Inferred — ... Unavailable — ...
```

Include only uncertainties that materially affect reuse. Do not repeat the whole prompt or place confidence annotations inside the six H3 sections.

## Reverse Preflight

Before returning the reconstruction, verify all of the following in addition to the main format preflight:

1. The output is described as a reconstruction rather than the recovered original.
2. Every reference label maps to media that will actually be available to H3.
3. Observed, inferred, and unavailable information remain distinguishable in the reconstruction note.
4. Shot boundaries, duration, and aspect ratio match the inspected source when metadata is available.
5. Camera descriptions follow visual evidence and do not confuse subject motion with camera motion.
6. Exact dialogue, lyrics, and visible text are included only when reliably readable or audible.
7. The prompt excludes source artifacts unless the user requests them.
8. No seed, sampler, hidden setting, absent reference, or creator intent is fabricated.
