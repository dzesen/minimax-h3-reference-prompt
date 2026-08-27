# MiniMax H3 Ref2VA Format Specification

Use this specification for every new, revised, or reviewed full-reference prompt.

## Canonical Output

Keep these exact lowercase field names and this exact order:

```text
subject_definitions:
<Subject 1> is ...

summary:
[reference generation] ...

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - ...

detailed_description:
The target video ...
[Shot 1] ...
[Shot 2] At 00:03.000, the shot cuts to ...

overall_soundscape:
...

non_diegetic_music:
...
```

Use one blank line between sections. Do not add Markdown headings, bullets, commentary, or negative-prompt fields inside the prompt block.

## Reference Labels

Define every label exactly once in `subject_definitions`, keep its meaning stable, and use it wherever its role takes effect.

- `<Subject N>` identifies reusable visible content abstracted from reference media: a person, animal, object, environment, wardrobe, interface, effect, style, action, expression, or pose. Describe its provenance and the traits the target must follow.
- `<Picture N>` is a standalone entry only when the image is a concrete first frame, last frame, keyframe, edited frame, storyboard, or composition anchor. When an image only defines a subject or style, cite it inside the corresponding `<Subject N>` definition instead.
- `<Video N>` identifies a whole-video relationship such as direct editing, continuation, or borrowed camera, cut, rhythm, or temporal structure. Visible content taken from a video still receives its own `<Subject N>` label.
- `<Audio N>` identifies an audio signal that is copied or referenced for voice, dialogue, lyrics, music, beat, ambience, effects, or continuity. A video with sound does not automatically require an audio label.

Number each label type independently from 1. Do not introduce a new label after `subject_definitions`.

## Summary

Write one short paragraph beginning with the applicable fixed task types joined by ` + `:

- `keyframe completion` when a picture is a concrete target-video frame anchor.
- `reference generation` when media guides identity, scene, style, motion, camera, storyboard, or other generation without being edited or continued directly.
- `video editing` when the target directly modifies an existing video.
- `video continuation` when the target continues from an existing video.
- `audio reuse` when the same audio signal is copied in full or in part.
- `audio reference` when only timbre, words, rhythm, music style, effect texture, or continuity is followed.

Do not infer a task type from asset presence alone.

## Retention Analysis

Write one line for every defined label and name the shots or structural role in which it appears.

Visible labels use exactly one of these markers:

- `fully_preserved`: the defined identity, design, frame role, or structure remains intact.
- `partially_preserved`: the content remains identifiable but some defined traits change or only part is retained.
- `attribute_transfer`: defined traits move to a different identifiable target.
- `weak_reference`: only broad style, category, composition, or atmosphere remains.

Audio labels use exactly one of these markers:

- `fully_copy`: the complete source signal is the complete final audio track.
- `partially_copy`: only part or selected layers are copied, or copied audio is otherwise changed.
- `reference`: only timbre, words, rhythm, music style, delivery, or sound texture guides new audio.
- `weak_reference`: only broad category or atmosphere remains.

New actions, settings, or plot events are not fidelity losses unless they contradict a trait defined for the reference label.

## Detailed Description

Write a playback-order audiovisual description, normally 350–500 English words for a generation task. Prioritize a complete, executable timeline over mechanically reaching the range.

Start with one or two sentences establishing duration, aspect ratio, rendering style, visual grammar, lighting, grade, and global scene constraints. Then write every shot in order.

- `[Shot 1]` has no cut timestamp.
- Every later shot begins `[Shot N] At MM:SS.mmm, ...` with a strictly increasing cut time inside the requested duration.
- Use precise internal ranges such as `From 00:03.000-00:04.000` when actions or camera phases need synchronization.
- Cover the full duration without unexplained gaps or overlapping incompatible events.
- At a subject's first clear appearance, state its visible reference traits, position, pose, and action. Later shots may use the label without redefining it.
- For every shot, make composition, environment, lighting, action and state changes, dominant camera trajectory, framing continuity, and synchronized sound readable.
- Describe secondary cloth, hair, straps, smoke, particles, or reflections as consequences of the main motion rather than independent competing actions.
- A cut must reveal a new viewpoint, scale, state, time, or information. Use continuous camera motion for a small framing change.
- Distinguish a physical `push in` or `pull back` from an optical `zoom in` or `zoom out`.
- If a strict overhead view would hide a required facial expression or silhouette, schedule those requirements in separate readable phases or shots.

For dialogue or singing, assign stable `(S1)`, `(S2)`, and later IDs in order of first audible vocal event. Put exact words only inside `<d>[Language] ...</d>`. Preserve original text exactly. Visible text appears in English double quotation marks and remains in its original language. Do not assign speaker IDs to silent subjects.

## Audio Sections

`overall_soundscape` is one continuous English paragraph of 1–4 sentences summarizing ambience, physical action sounds, cloth and object sounds, and non-verbal human sounds. Keep precisely synchronized sound events in `detailed_description`. Use `N/A` only when the user explicitly requests complete silence.

`non_diegetic_music` is 1–3 English sentences describing audience-only score through instrumentation, tempo or pulse, rhythm, and dynamic changes. Diegetic radio, phone, instrument, or performance music stays in `detailed_description`. Use `N/A` when no audience-only music exists.

## Preflight

Before returning a prompt, verify all of the following:

1. Duration is 4–15 seconds and every timestamp fits it.
2. The six field names and their order are exact.
3. Every used label is defined once; every defined label that matters later is used consistently.
4. Every defined label has one retention line with a valid fixed marker.
5. Picture labels are standalone only for concrete frame or planning anchors.
6. Shot numbers and cut times strictly increase, and internal time ranges have no unexplained gaps or contradictions.
7. Each shot has a readable main action, dominant camera path, and stable subject framing.
8. Required identity traits, wardrobe or product details, style, key actions, and exact words survive the rewrite.
9. Physical impacts have visible causes; music accents are identified as non-diegetic.
10. Dialogue, lyrics, and visible text remain exact and untranslated.
11. `overall_soundscape` and `non_diegetic_music` contain only their proper audio layers.
12. The prompt introduces no unrequested character, prop, readable text, or reference relationship.
