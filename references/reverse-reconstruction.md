# Reverse Reconstruction

Use this reference only when the user asks to infer, reconstruct, recreate, reverse-engineer, or derive an H3 prompt from existing image, video, or audio media.

This is a non-official extension workflow for producing a functional reconstruction prompt, not recovery of the original prompt. Source wording, negative instructions, seed, sampler, hidden model settings, omitted references, original role mapping, and creator intent remain unavailable unless the user supplies them.

## Choose the Reconstruction Target

Establish how the observed media will relate to the next H3 generation before assigning labels.

- **Media remains attached:** When the image, video, or audio will be supplied to H3, produce the six-section Ref2VA prompt. Assign labels according to the role the asset will play in the new generation.
- **Finished video as a reference:** Use `<Video N>` for camera, cut, action, pacing, or temporal structure. Define visible people, objects, environments, styles, or performances derived from it as separate `<Subject N>` entries. Define `<Audio N>` only when its signal or audible properties will actually be copied or referenced.
- **Text-only recreation:** When the observed media will not be supplied to H3, do not emit unresolved reference labels or pretend the media remains available. Return an evidence-based reconstruction brief and recommend compilation with an H3 base-mode prompt.

If the user's intended target is ambiguous, prefer a Ref2VA reconstruction only when the supplied media is clearly meant to remain attached for generation. Otherwise state that a text-only observation brief cannot honestly use unresolved reference labels and ask which output they need.

## Build an Evidence Ledger

Inspect the available media with suitable host tools before writing. Read metadata first, measure rather than estimate cut times where possible, and sample the beginning, end, every cut boundary, action extrema, identity-revealing close-ups, composition changes, and meaningful audio transitions. Inspect additional frames when fast movement, occlusion, flash, or a suspected cut remains ambiguous. For small identity, prop, text, or hand details, inspect native-resolution crops rather than relying on a reduced contact sheet.

Record three evidence classes:

- **Observed:** Directly visible, audible, or available from reliable media metadata. Examples include duration, aspect ratio, cut time, clothing color, subject position, spoken words that are clearly intelligible, and the presence of a music layer.
- **Inferred:** A plausible production instruction derived from evidence but not directly recoverable. Examples include a push-in inferred from parallax, approximate tempo, a likely wide lens, intended secondary cloth motion, or lighting direction.
- **Unavailable:** Original wording, random seed, sampler, hidden generation parameters, references not provided, and any obscured or inaudible content.

Keep the ledger outside the final H3 prompt. The prompt itself should be decisive and production-ready, while the reconstruction note discloses uncertainty concisely in the user's language.

## Reconstruct the Timeline

1. Read technical metadata when available: duration, dimensions, aspect ratio, frame rate, and whether an audio stream exists.
2. Mark shot boundaries and transition types. Use measured frame times, then manually verify candidate boundaries on both sides. Distinguish a true cut from motion blur, occlusion, flashes, or a fast whip.
3. For every shot, record opening composition, subject placement and appearance, environment, lighting, action phases, camera trajectory, framing result, synchronized sounds, and end state. Distinguish a cut-defined Shot from several timed action beats inside one continuous camera take.
4. Distinguish subject motion from camera motion. Use parallax, changing perspective, scale change, and background displacement to separate tracking, arc, pan, push, pull, zoom, rise, and roll.
5. Track recurring subjects across shots. Preserve only traits supported by clear views or supplied reference assets; leave concealed details unspecified.
6. If audio can actually be monitored or transcribed, segment it into dialogue or singing, physical effects, ambience, diegetic music, and audience-only score. Preserve exact words only when reliably audible. Use `[unclear]` for unintelligible spans instead of guessing. Do not classify music, dialogue, or ambience from mean/max volume statistics.
7. Create a continuity state vector at every cut and at the final frame: pose, hand and prop state, gaze, screen position, camera side/height/distance/direction/speed, lighting, particles, audio phase, and unfinished momentum.
8. Convert the evidence ledger into the Reference Responsibility Matrix and target-video roles, then apply the canonical format specification.

## Reconstruction Discipline

- Prefer functional camera language over unsupported technical precision. When focal length, aperture, BPM, lighting hardware, or stabilization method is uncertain, describe the observable visual or audible result.
- Treat compression noise, frame interpolation artifacts, accidental flicker, watermarks, and isolated anatomy failures as source artifacts unless the user explicitly wants them reproduced.
- Treat repeated, coherent rendering traits as style evidence. A single blurred or occluded frame is weak evidence.
- Preserve chronology and spatial continuity even when the source contains rapid action. Allocate explicit time for anticipation, execution, follow-through, and camera settling.
- A single image supports appearance, composition, environment, and style reconstruction, but not observed temporal motion or audio. Any proposed action, camera path, or sound from a still image is inference and belongs in the reconstruction note.
- An audio-free or muted source supports no claim about dialogue, ambience, effects, or music. A tool that sampled frames but did not hear the audio also supports no such claim. Use the user's requested audio design, request a transcript when material, or use `N/A` where the canonical format permits it.
- A contact sheet supports ordering and broad visual change, not continuous velocity, exact camera dynamics, or audio. Phrase those as inference unless verified from playback or denser measurement.
- Visible text, dialogue, and lyrics remain exact when legible or intelligible. Do not complete cropped, obscured, or unclear content from context.
- When the observed source is longer than 15 seconds, do not compress it into one illegal H3 prompt. Select a user-authorized segment or produce multiple legal clip prompts with explicit seam states. Each clip must independently satisfy the format and platform envelope.
- For continuation or multi-clip reconstruction, the next clip begins from the measured preceding end state and normally introduces only one primary new change before other motion layers enter.

## Reconstruction Note

Before the prompt block, write one compact note in the user's language using this semantic structure:

```text
Reconstruction note: Observed - ... Inferred - ... Unavailable - ...
```

Include only uncertainties that materially affect reuse. Do not repeat the whole prompt or place confidence annotations inside the six H3 sections.

## Reverse Preflight

Before returning the reconstruction, verify all of the following in addition to the main format preflight:

1. The output is described as a reconstruction rather than the recovered original.
2. Every reference label maps to media that will actually be available to H3.
3. Observed, inferred, and unavailable information remain distinguishable in the reconstruction note.
4. Shot boundaries, duration, and aspect ratio match the inspected source when metadata is available.
5. Camera descriptions follow visual evidence and do not confuse subject motion with camera motion.
6. Every cut has a continuity state vector and the target timeline preserves or intentionally changes that state.
7. Exact dialogue, lyrics, and visible text are included only when reliably readable or audible.
8. The prompt excludes source artifacts unless the user requests them.
9. No seed, sampler, hidden setting, negative prompt, absent reference, original role mapping, or creator intent is fabricated.
10. Any unavailable audio analysis, sparse frame sampling, uncertain cut, or low-resolution identity detail is disclosed rather than silently promoted to Observed.
