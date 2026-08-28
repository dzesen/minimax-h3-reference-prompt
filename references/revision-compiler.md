# Revision Compiler

Use this reference whenever the user asks to add, replace, remove, move, retime, tighten, or otherwise revise an existing Ref2VA prompt. A revision is a recompile from the current active requirements, not a prose patch pasted onto the old output.

## Preserve the Active State

Extract the current prompt into an internal state before applying the request:

- Constraint ledger: literals, hard requirements, flexible execution details, and explicit exclusions.
- Reference Responsibility Matrix: each attached asset, label, role, preserve/change boundary, priority, active shots/time, and audio handling.
- Timeline ledger: shots, cut times, internal beats, actions, camera paths, speakers, exact text, sound cues, and locked end states.
- Six-section dependencies: definitions, task prefixes, retention lines, first appearances, later label uses, and audio summaries.

The user's new instruction modifies this active state. Unmentioned literals and hard constraints remain locked. Flexible details remain only when they do not conflict with the new instruction.

## Classify the Operation

Classify every requested change as one or more operations:

- `ADD`: introduce a real reference, required element, beat, sound, line, or constraint.
- `REPLACE`: substitute identity, design, action, camera, wording, sound, or relationship while removing the superseded value.
- `REMOVE`: delete an element and every instruction that depends on it.
- `MOVE`: change the shot, beat, spatial position, or audio phase in which an active element occurs.
- `RETIME`: change duration, cut point, internal range, line timing, or music cue while preserving the intended event.

A request such as "remove Shot 2 and make the close-up start at 00:04" is `REMOVE + MOVE + RETIME`; do not treat it as a sentence edit.

## Invalidate Dependencies

After changing the active state, invalidate and recompute every affected dependency:

1. Reference labels and numbering.
2. Subject provenance and asset conflict priority.
3. Summary task types and relationships.
4. Retention entries, marker family, and shot coverage.
5. Shot numbering, cut times, internal ranges, and full-duration coverage.
6. First appearances, identity restatement, pose, hand/prop state, gaze, screen position, and environment landmarks.
7. Camera side, height, distance, direction, speed, framing result, and 180-degree continuity.
8. Speaker numbering, `<d>` blocks, `<scenetrans>`, `<cutoff>`, visible text, and lip-state requirements.
9. Synchronized effects, ambience, diegetic music, non-diegetic score, and every `<Audio N>` relationship.
10. Character count, media counts, target duration, and other platform-envelope checks.

Deleting a subject must remove its actions, sounds, speaker events, retention entry, later mentions, and unsupported reactions from other subjects. Deleting a shot must retime later cuts and repair the previous-to-next state handoff. Replacing an audio relationship may change the task prefix, marker family, dialogue source, and both audio summaries.

## Recompile, Do Not Accumulate

Serialize a fresh six-section prompt from the revised state.

- Do not append "instead," "ignore the previous instruction," "no longer," or other stale correction language inside the final prompt.
- Do not retain both old and new values for the same identity trait, action, camera path, line, timestamp, or audio role.
- Do not preserve an unused definition merely to avoid renumbering. Renumber each label family contiguously and update all uses.
- Do not solve a 7,000-character overflow by truncation. Compress in this order: redundant restatement, flexible atmosphere, secondary reactions, decorative camera language, then nonessential sound detail. Never cut a field, definition, hard action, exact literal, or timeline boundary in half.

## Revision Preflight

In addition to the main format preflight, verify:

1. Every requested operation is reflected in the active state and final output.
2. Every superseded or removed instruction is absent from all six sections.
3. Unmentioned literals and hard constraints remain unchanged.
4. Reference labels, numbering, task types, and retention entries were regenerated rather than locally patched.
5. Timeline coverage, state handoffs, camera continuity, speakers, exact text, and audio routes remain coherent after the change.
6. The rebuilt prompt passes deterministic validation and contains no repair commentary.
