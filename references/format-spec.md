# MiniMax H3 Ref2VA Format Specification

Use this specification for every new, revised, or reviewed full-reference prompt.

## Platform Feasibility

Check request feasibility before drafting. These are transport or model constraints, not prose suggestions:

- The target duration is an integer from 4 through 15 seconds.
- The final prompt is at most 7,000 Unicode characters.
- A request contains at most 9 reference images, 3 reference videos, 3 reference audio files, and 12 mixed reference files.
- Each reference video and audio file is 2-15 seconds. Total reference-video duration and total reference-audio duration are each at most 15 seconds.
- The complete API request body is at most 64 MB.
- Ref2VA aspect ratio defaults to `adaptive` when the run setting is omitted. Do not invent a fixed ratio from a reference image alone.
- API roles `first_frame` and `last_frame` are mutually exclusive with every `reference_*` role in the same request. Prompt labels such as `<Picture 1>` are semantic references, not API upload roles; a Ref2VA picture anchor remains a reference image at transport time.
- Reference audio without any reference image or video is a documented feasibility risk. Warn rather than inventing a visual asset.

If a requirement exceeds a hard limit, do not hide the conflict inside a valid-looking prompt. For an explicitly requested multi-clip project, split the plan into legal prompts and carry a continuity seam. Otherwise ask whether to shorten or segment.

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

Before serialization, use an internal Reference Responsibility Matrix and timeline ledger. These are planning artifacts and do not appear in the six-section output.

## Internal Reference Responsibility Matrix

For each actual attached asset, record:

```text
asset/order | API transport role | semantic label(s) | primary contribution | optional secondary contribution | preserve/change boundary | conflict priority | active shots/time | audio-track handling | confidence
```

Use the matrix to prevent reference leakage. Assign narrow responsibilities, resolve conflicts explicitly, and never create a label for an unattached asset. One subject may combine appearance from a picture, motion from a video, and voice from audio; conversely, one asset may define several subjects. The matrix does not require a standalone definition for every file: a picture used only as a Subject's provenance remains cited inside that Subject definition.

## Reference Labels

Line-define every tracked content label exactly once in `subject_definitions`, keep its meaning stable, and use it wherever its role takes effect. A source-only picture or video label may appear solely as provenance inside a Subject definition and then receives no separate definition or retention line.

- `<Subject N>` identifies reusable visible content abstracted from reference media: a person, animal, object, environment, wardrobe, interface, effect, style, action, expression, or pose. Describe its provenance and the traits the target must follow.
- `<Picture N>` is a standalone entry only when the image is a concrete first frame, last frame, keyframe, edited frame, storyboard, or composition anchor. When an image only defines a subject or style, cite it inside the corresponding `<Subject N>` definition instead.
- `<Video N>` identifies a whole-video relationship such as direct editing, continuation, or borrowed camera, cut, rhythm, or temporal structure. Visible content taken from a video still receives its own `<Subject N>` label.
- `<Audio N>` identifies an audio signal that is copied or referenced for voice, dialogue, lyrics, music, beat, ambience, effects, or continuity. A video with sound does not automatically require an audio label.

Number each label type independently from 1. Do not introduce a new tracked label after `subject_definitions`, and do not use a provenance-only media label in later sections unless it is promoted to its own definition.

Do not confuse asset order with label meaning. Numbering records order within one label family and does not imply that `<Video 1>` and `<Audio 1>` came from the same file.

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

For a narrowly defined `<Video N>` role, such as one exact continuous camera path and pacing pattern, use `fully_preserved` when that entire defined role is executed. Use `weak_reference` when the target borrows only a broad handheld feel, rhythm, genre, or atmosphere. Judge preservation against the label's defined responsibility, not against every visible detail in the source file.

## Detailed Description

Write a playback-order audiovisual description, normally 350-500 English words for a generation task. Prioritize a complete, executable timeline over mechanically reaching the range.

Start with one or two sentences establishing the known duration, any explicitly fixed aspect ratio, rendering style, visual grammar, lighting, grade, and global scene constraints. Omit a fixed ratio when the Ref2VA run remains adaptive. Then write every shot in order.

- `[Shot 1]` has no cut timestamp.
- Every later shot begins `[Shot N] At MM:SS.mmm, ...` with a strictly increasing cut time inside the requested duration.
- Use precise internal ranges such as `From 00:03.000-00:04.000` when actions or camera phases need synchronization.
- Cover the full duration without unexplained gaps or overlapping incompatible events.
- Treat a Shot as a cut-defined camera segment and a timed range inside it as a beat. Do not create a new Shot merely because the action changes while the camera remains continuous.
- Give each beat one main observable state change. Establish, prepare, execute, settle/hold, and lock an end state only to the level needed by the action; do not mechanically add all five labels to simple motion.
- The next beat's initial state must match the previous beat's locked end state unless a cut explicitly reveals a justified state change. Track pose, hands and props, gaze, screen position, environment landmarks, camera side/height/distance/direction/speed, lighting, particles, audible phase, and unfinished momentum when relevant.
- At a subject's first clear appearance, state its visible reference traits, position, pose, and action. Later shots may use the label without redefining it.
- For every shot, make composition, environment, lighting, action and state changes, dominant camera trajectory when any, framing continuity, and synchronized sound readable.
- Describe secondary cloth, hair, straps, smoke, particles, or reflections as consequences of the main motion rather than independent competing actions.
- A cut must reveal a new viewpoint, scale, state, time, or information. Use continuous camera motion for a small framing change.
- Distinguish a physical `push in` or `pull back` from an optical `zoom in` or `zoom out`.
- Describe camera type, range, speed, motivation, and framing result when they materially affect the shot. A locked camera is valid; do not add motion for decoration.
- Resolve spatial terms against explicit anchors: for example, "the camera moves from behind the car around its rear bumper to the driver's-door side," not merely "moves from behind to the side." Name the anchor whenever subject-relative and object-relative readings differ.
- If a strict overhead view would hide a required facial expression or silhouette, schedule those requirements in separate readable phases or shots.
- Preserve time for dialogue and reaction. If the shot is overloaded, remove flexible particles, cloth beats, decorative camera flourishes, or redundant description before changing a hard action or exact line.

For dialogue or singing, assign stable `(S1)`, `(S2)`, and later IDs in order of first audible vocal event. Put exact words only inside `<d>[Language] ...</d>`. Do not assign speaker IDs to silent subjects or write speaker IDs in `retention_analysis`.

- Preserve user-supplied dialogue, lyrics, names, product copy, and visible text exactly, including punctuation.
- For reference-audio transcription, preserve the source words and language, normalize only basic sentence punctuation, and insert `[unclear]` for unintelligible spans instead of guessing.
- When a defined referenced subject physically speaks, write `<Subject N> (Sx)` at the vocal event. If `<Audio N>` is bound to that speaker, its definition may reuse the same global `(Sx)` after `<Subject N>`; the audio definition does not create or renumber the speaker ID independently.
- For voiceover, use the phrase `says in an off-screen voiceover` and state after the `<d>` block that the corresponding on-screen character's lips remain closed. A vocal cue that exists only inside directly reused music or a complete soundtrack uses `<Audio N>` without inventing a separate speaker.
- If one line crosses a cut, place `<scenetrans>` at the connecting point in both parts and explicitly state that audio continues across the cut. Use `<cutoff>` only when speech is truncated by the video ending.
- Visible text appears in English double quotation marks, remains untranslated, and includes its timing, location, layout, and disappearance when those details matter. Do not treat subtitles as ordinary environmental signage.

## Audio Sections

`overall_soundscape` is one continuous English paragraph of 1-4 sentences summarizing ambience, physical action sounds, cloth and object sounds, and non-verbal human sounds. Keep precisely synchronized sound events in `detailed_description`. Use `N/A` only when the user explicitly requests complete silence.

`non_diegetic_music` is 1-3 English sentences describing audience-only score through instrumentation, tempo or pulse, rhythm, and dynamic changes. Diegetic radio, phone, instrument, or performance music stays in `detailed_description`. Use `N/A` when no audience-only music exists.

Do not repeat complete dialogue or lyrics in either audio summary. Avoid asking for the same BGM as copied reference audio, newly generated diegetic music, and a separate non-diegetic score unless the user explicitly wants distinct layers. If `<Audio N>` is `fully_copy`, do not casually add new sounds that would contradict its status as the complete final track; downgrade the marker or remove the additions.

## Preflight

Before returning a prompt, verify all of the following. Items marked **hard** can be checked deterministically; the remaining items require semantic review.

1. **Hard:** Duration is an integer from 4 through 15 seconds; every timestamp fits it; the prompt is at most 7,000 Unicode characters.
2. **Hard:** Asset counts, media durations, mixed total, body size, and API transport-role combination fit the platform envelope when those facts are known.
3. **Hard:** The six field names appear once in exact order and each field is nonempty.
4. **Hard:** Every label used outside `subject_definitions` is line-defined once, numbering is contiguous within each family, and no tracked label is introduced after `subject_definitions`. Source-only media labels remain provenance citations inside Subject definitions.
5. **Hard:** Every defined label has exactly one retention line using the correct visual or audio marker family.
6. **Hard:** Shot numbers and cut times strictly increase; later shots use `MM:SS.mmm`; internal ranges have positive duration and fit the target.
7. **Hard:** Dialogue tags are balanced, speaker IDs are stable and contiguous, and `<scenetrans>`/`<cutoff>` are used only for their defined continuity cases.
8. Picture labels are standalone only for concrete frame or planning anchors, and every actual asset has a clear responsibility in the internal matrix.
9. Each beat has one readable main state change, achievable timing, a non-conflicting dominant camera path, and a locked handoff state.
10. Required identity traits, wardrobe or product details, style, actions, reference priorities, and exact literals survive the rewrite.
11. Physical impacts have visible causes; dialogue, ambience, diegetic music, and audience-only score are routed to the correct layers without accidental duplication.
12. The prompt introduces no unrequested character, prop, brand, dialogue, readable text, audio category, plot turn, or reference relationship.

The 350-500-word range is normally appropriate for reference-generation descriptions, but deviations are warnings rather than structural failure when dialogue density, editing scope, or source complexity justifies them. A validator cannot prove reference fidelity, physical plausibility, creative quality, or full semantic intent preservation.
