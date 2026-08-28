#!/usr/bin/env python3
"""Deterministic structural validator for MiniMax H3 Ref2VA prompts.

This validator checks only facts that can be established from prompt text and
optional request metadata. It does not score creative quality or predict model
compliance.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FIELDS = [
    "subject_definitions",
    "summary",
    "retention_analysis",
    "detailed_description",
    "overall_soundscape",
    "non_diegetic_music",
]

TASK_TYPES = {
    "keyframe completion",
    "reference generation",
    "video editing",
    "video continuation",
    "audio reuse",
    "audio reference",
}

VISUAL_MARKERS = {
    "fully_preserved",
    "partially_preserved",
    "attribute_transfer",
    "weak_reference",
}

AUDIO_MARKERS = {
    "fully_copy",
    "partially_copy",
    "reference",
    "weak_reference",
}

LABEL_RE = re.compile(r"<(Subject|Picture|Video|Audio)\s+(\d+)>")
LEADING_LABEL_RE = re.compile(
    r"(?m)^\s*(<(Subject|Picture|Video|Audio)\s+(\d+)>)\s+"
)
RETENTION_RE = re.compile(
    r"(?m)^\s*(<(Subject|Picture|Video|Audio)\s+(\d+)>)"
    r"\s*(?:\([^\n]*?\))?\s*:\s*([a-z_]+)\s*-\s*\S"
)
TIMECODE_RE = r"\d{2}:\d{2}\.\d{3}"


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str


def add(issues: list[Issue], severity: str, code: str, message: str) -> None:
    issues.append(Issue(severity, code, message))


def parse_timecode(value: str) -> float:
    minutes, remainder = value.split(":", 1)
    seconds, milliseconds = remainder.split(".", 1)
    return int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000


def parse_sections(text: str, issues: list[Issue]) -> dict[str, str]:
    matches: dict[str, re.Match[str]] = {}
    for field in FIELDS:
        found = list(re.finditer(rf"(?m)^{re.escape(field)}:[ \t]*$", text))
        if len(found) != 1:
            add(
                issues,
                "ERROR",
                "FIELD_COUNT",
                f"{field}: expected exactly once, found {len(found)}.",
            )
        elif found:
            matches[field] = found[0]

    if len(matches) != len(FIELDS):
        return {}

    positions = [matches[field].start() for field in FIELDS]
    if positions != sorted(positions):
        add(issues, "ERROR", "FIELD_ORDER", "The six fields are not in canonical order.")
        return {}

    sections: dict[str, str] = {}
    for index, field in enumerate(FIELDS):
        start = matches[field].end()
        end = matches[FIELDS[index + 1]].start() if index + 1 < len(FIELDS) else len(text)
        body = text[start:end].strip()
        sections[field] = body
        if not body:
            add(issues, "ERROR", "EMPTY_FIELD", f"{field}: section is empty.")
    return sections


def label_key(kind: str, number: str | int) -> str:
    return f"<{kind} {int(number)}>"


def validate_labels(sections: dict[str, str], issues: list[Issue]) -> None:
    subject_text = sections["subject_definitions"]
    tracked_matches = list(LEADING_LABEL_RE.finditer(subject_text))
    tracked = [label_key(match.group(2), match.group(3)) for match in tracked_matches]

    for label in sorted(set(tracked)):
        if tracked.count(label) > 1:
            add(issues, "ERROR", "DUPLICATE_DEFINITION", f"{label} is defined more than once.")

    outside_definitions = "\n".join(sections[field] for field in FIELDS[1:])
    used_outside = {
        label_key(match.group(1), match.group(2))
        for match in LABEL_RE.finditer(outside_definitions)
    }
    tracked_set = set(tracked)
    for label in sorted(used_outside - tracked_set):
        add(
            issues,
            "ERROR",
            "UNDEFINED_LABEL",
            f"{label} is used outside subject_definitions but has no line-leading definition there.",
        )

    all_labels = {
        label_key(match.group(1), match.group(2))
        for match in LABEL_RE.finditer(subject_text)
    }
    for kind in ("Subject", "Picture", "Video", "Audio"):
        numbers = sorted(
            int(match.group(1))
            for label in all_labels
            if (match := re.fullmatch(rf"<{kind} (\d+)>", label))
        )
        if numbers and numbers != list(range(1, max(numbers) + 1)):
            add(
                issues,
                "ERROR",
                "LABEL_SEQUENCE",
                f"{kind} numbering is not contiguous from 1: {numbers}.",
            )

    retention_text = sections["retention_analysis"]
    retention_matches = list(RETENTION_RE.finditer(retention_text))
    retention: dict[str, list[str]] = {}
    for match in retention_matches:
        label = label_key(match.group(2), match.group(3))
        retention.setdefault(label, []).append(match.group(4))

    for label in tracked:
        markers = retention.get(label, [])
        if len(markers) != 1:
            add(
                issues,
                "ERROR",
                "RETENTION_COUNT",
                f"{label} requires exactly one retention line; found {len(markers)}.",
            )
            continue
        kind = label[1:].split(" ", 1)[0]
        allowed = AUDIO_MARKERS if kind == "Audio" else VISUAL_MARKERS
        if markers[0] not in allowed:
            add(
                issues,
                "ERROR",
                "RETENTION_MARKER",
                f"{label} uses {markers[0]!r}; allowed markers are {sorted(allowed)}.",
            )

    for label in sorted(set(retention) - set(tracked)):
        add(
            issues,
            "ERROR",
            "ORPHAN_RETENTION",
            f"{label} has a retention line but is not a line-leading definition.",
        )

    if re.search(r"\(S\d+\)", retention_text):
        add(
            issues,
            "ERROR",
            "SPEAKER_IN_RETENTION",
            "Speaker IDs must not appear in retention_analysis.",
        )


def validate_summary(sections: dict[str, str], issues: list[Issue]) -> set[str]:
    summary = sections["summary"]
    prefix = re.match(r"^\[([^\]]+)\]\s+", summary)
    if not prefix:
        add(issues, "ERROR", "TASK_PREFIX", "summary must begin with a bracketed task type.")
        return set()

    raw_types = prefix.group(1).split(" + ")
    if len(raw_types) != len(set(raw_types)):
        add(issues, "ERROR", "TASK_PREFIX_DUPLICATE", "summary repeats a task type.")
    for task_type in raw_types:
        if task_type not in TASK_TYPES:
            add(
                issues,
                "ERROR",
                "TASK_PREFIX_VALUE",
                f"Unknown task type {task_type!r}.",
            )

    if "\n" in summary:
        add(issues, "WARNING", "SUMMARY_PARAGRAPH", "summary should be one short paragraph.")
    return set(raw_types)


def infer_duration(detail: str) -> int | None:
    patterns = [
        r"(?i)\btarget video is (?:a|an)\s+(\d{1,2})-second\b",
        r"(?i)\btarget video (?:runs|lasts)\s+(\d{1,2})\s+seconds?\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, detail)
        if match:
            return int(match.group(1))
    return None


def validate_timeline(
    detail: str, requested_duration: int | None, issues: list[Issue]
) -> int | None:
    inferred = infer_duration(detail)
    duration = requested_duration if requested_duration is not None else inferred

    if requested_duration is not None and inferred is not None and inferred != requested_duration:
        add(
            issues,
            "ERROR",
            "DURATION_CONFLICT",
            f"CLI duration is {requested_duration}s but detailed_description says {inferred}s.",
        )
    if duration is None:
        add(
            issues,
            "WARNING",
            "DURATION_UNKNOWN",
            "Duration could not be established; pass --duration to check time bounds.",
        )
    elif not 4 <= duration <= 15:
        add(issues, "ERROR", "DURATION_LIMIT", f"Target duration {duration}s is outside 4-15s.")

    shot_matches = list(re.finditer(r"\[Shot\s+(\d+)\]", detail))
    if not shot_matches:
        add(issues, "ERROR", "SHOT_MISSING", "detailed_description contains no [Shot N] marker.")
        return duration

    shot_numbers = [int(match.group(1)) for match in shot_matches]
    if shot_numbers != list(range(1, len(shot_numbers) + 1)):
        add(
            issues,
            "ERROR",
            "SHOT_SEQUENCE",
            f"Shot numbers must be contiguous from 1; found {shot_numbers}.",
        )

    cut_times: list[float] = []
    for index, match in enumerate(shot_matches):
        following = detail[match.end() : match.end() + 40]
        timestamp = re.match(rf"\s+At\s+({TIMECODE_RE}),", following)
        shot_number = int(match.group(1))
        if index == 0:
            if timestamp:
                add(issues, "ERROR", "SHOT1_TIMESTAMP", "[Shot 1] must not have a cut timestamp.")
            continue
        if not timestamp:
            add(
                issues,
                "ERROR",
                "SHOT_TIMESTAMP",
                f"[Shot {shot_number}] must begin with 'At MM:SS.mmm,'.",
            )
            continue
        value = parse_timecode(timestamp.group(1))
        cut_times.append(value)
        if duration is not None and value >= duration:
            add(
                issues,
                "ERROR",
                "TIMESTAMP_BOUNDS",
                f"[Shot {shot_number}] cut {timestamp.group(1)} is not inside {duration}s.",
            )

    if any(later <= earlier for earlier, later in zip(cut_times, cut_times[1:])):
        add(issues, "ERROR", "CUT_ORDER", "Later-shot cut timestamps are not strictly increasing.")

    range_pattern = re.compile(rf"(?i)\b(?:From\s+)?({TIMECODE_RE})-({TIMECODE_RE})")
    for match in range_pattern.finditer(detail):
        start = parse_timecode(match.group(1))
        end = parse_timecode(match.group(2))
        if end <= start:
            add(
                issues,
                "ERROR",
                "RANGE_ORDER",
                f"Time range {match.group(1)}-{match.group(2)} is not positive.",
            )
        if duration is not None and end > duration:
            add(
                issues,
                "ERROR",
                "RANGE_BOUNDS",
                f"Time range {match.group(1)}-{match.group(2)} exceeds {duration}s.",
            )
    return duration


def validate_dialogue(sections: dict[str, str], issues: list[Issue]) -> None:
    detail = sections["detailed_description"]
    open_count = len(re.findall(r"<d>", detail))
    close_count = len(re.findall(r"</d>", detail))
    blocks = list(re.finditer(r"<d>\[([^\]\n]+)\]\s*.*?</d>", detail, flags=re.DOTALL))
    if open_count != close_count or len(blocks) != open_count:
        add(
            issues,
            "ERROR",
            "DIALOGUE_TAGS",
            "Every <d> must be balanced and begin with [Language].",
        )

    for field in ("subject_definitions", "summary", "retention_analysis", "overall_soundscape", "non_diegetic_music"):
        if "<d>" in sections[field] or "</d>" in sections[field]:
            add(
                issues,
                "ERROR",
                "DIALOGUE_LAYER",
                f"Complete dialogue/lyrics must stay in detailed_description, not {field}.",
            )

    speaker_ids = [int(value) for value in re.findall(r"\(S(\d+)\)", detail)]
    first_seen = list(dict.fromkeys(speaker_ids))
    if first_seen and first_seen != list(range(1, max(first_seen) + 1)):
        add(
            issues,
            "ERROR",
            "SPEAKER_SEQUENCE",
            f"Speaker IDs must first appear contiguously from S1; found {first_seen}.",
        )

    for block in blocks:
        prefix = detail[max(0, block.start() - 220) : block.start()]
        if not re.search(r"(?:\(S\d+(?:,S\d+)*\)|<Audio\s+\d+>)", prefix):
            add(
                issues,
                "WARNING",
                "DIALOGUE_SOURCE",
                "A <d> block has no nearby speaker ID or Audio label; verify its audible source.",
            )

    scenetrans_count = detail.count("<scenetrans>")
    if scenetrans_count % 2:
        add(
            issues,
            "ERROR",
            "SCENETRANS_PAIR",
            "<scenetrans> should appear at both connecting parts of dialogue crossing a cut.",
        )
    if "<cutoff>" in detail and not re.search(r"(?i)(end|ending|final frame|video cuts off)", detail):
        add(
            issues,
            "WARNING",
            "CUTOFF_CONTEXT",
            "<cutoff> appears without an explicit end-of-video truncation description.",
        )

    for match in re.finditer(r"(?i)off-screen voiceover", detail):
        nearby = detail[match.start() : match.start() + 500]
        if not re.search(r"(?i)lips?\s+(?:remain|stays?|are)\s+(?:completely\s+)?closed", nearby):
            add(
                issues,
                "WARNING",
                "VOICEOVER_LIPS",
                "Off-screen voiceover should state that the on-screen character's lips remain closed.",
            )


def asset_count_from_text(text: str, kind: str) -> int:
    numbers = {int(value) for value in re.findall(rf"<{kind}\s+(\d+)>", text)}
    return max(numbers) if numbers else 0


def validate_asset_envelope(args: argparse.Namespace, text: str, issues: list[Issue]) -> None:
    inferred = {
        "Picture": asset_count_from_text(text, "Picture"),
        "Video": asset_count_from_text(text, "Video"),
        "Audio": asset_count_from_text(text, "Audio"),
    }
    counts = {
        "Picture": args.picture_count if args.picture_count is not None else inferred["Picture"],
        "Video": args.video_count if args.video_count is not None else inferred["Video"],
        "Audio": args.audio_count if args.audio_count is not None else inferred["Audio"],
    }
    supplied_counts = {
        "Picture": args.picture_count,
        "Video": args.video_count,
        "Audio": args.audio_count,
    }
    limits = {"Picture": 9, "Video": 3, "Audio": 3}
    for kind, count in counts.items():
        if count < 0:
            add(issues, "ERROR", "ASSET_COUNT", f"{kind} count cannot be negative.")
        elif count > limits[kind]:
            add(
                issues,
                "ERROR",
                "ASSET_LIMIT",
                f"{kind} count {count} exceeds the limit of {limits[kind]}.",
            )
        supplied = supplied_counts[kind]
        if supplied is not None and inferred[kind] > supplied:
            add(
                issues,
                "ERROR",
                "MISSING_ATTACHMENT",
                f"Prompt uses {kind} {inferred[kind]} but only {supplied} {kind} attachment(s) were declared.",
            )
        elif supplied is not None and supplied > inferred[kind]:
            add(
                issues,
                "WARNING",
                "UNMAPPED_ATTACHMENT",
                f"{supplied} {kind} attachment(s) were declared, but prompt labels map only through {kind} {inferred[kind]}.",
            )
    total = sum(counts.values())
    if total == 0:
        add(
            issues,
            "ERROR",
            "NO_REFERENCE_ASSET",
            "A Ref2VA prompt requires at least one real reference image, video, or audio asset.",
        )
    if total > 12:
        add(issues, "ERROR", "MIXED_ASSET_LIMIT", f"Mixed reference count {total} exceeds 12.")

    if counts["Audio"] and not counts["Picture"] and not counts["Video"]:
        add(
            issues,
            "WARNING",
            "AUDIO_ONLY_REFERENCE",
            "Reference audio without a reference image/video is a documented feasibility risk.",
        )

    uses_reference = total > 0 or args.uses_reference_role
    if uses_reference and (args.uses_first_frame or args.uses_last_frame):
        add(
            issues,
            "ERROR",
            "API_ROLE_CONFLICT",
            "first_frame/last_frame API roles cannot coexist with reference_* roles.",
        )

    for kind, durations, count in (
        ("video", args.video_duration, counts["Video"]),
        ("audio", args.audio_duration, counts["Audio"]),
    ):
        if durations and len(durations) != count:
            add(
                issues,
                "WARNING",
                "MEDIA_DURATION_COUNT",
                f"Received {len(durations)} {kind} durations for {count} {kind} assets.",
            )
        for value in durations:
            if not 2 <= value <= 15:
                add(
                    issues,
                    "ERROR",
                    "MEDIA_DURATION_LIMIT",
                    f"Reference {kind} duration {value:g}s is outside 2-15s.",
                )
        if sum(durations) > 15:
            add(
                issues,
                "ERROR",
                "MEDIA_TOTAL_DURATION",
                f"Total reference {kind} duration {sum(durations):g}s exceeds 15s.",
            )

    if args.request_bytes is not None and args.request_bytes > 64 * 1024 * 1024:
        add(
            issues,
            "ERROR",
            "REQUEST_SIZE",
            f"Request body {args.request_bytes} bytes exceeds 64 MiB.",
        )


def validate_quality_signals(
    sections: dict[str, str], tasks: set[str], issues: list[Issue]
) -> None:
    detail = sections["detailed_description"]
    english_words = re.findall(r"\b[A-Za-z]+(?:[-'][A-Za-z]+)*\b", detail)
    if "reference generation" in tasks and not ({"video editing", "video continuation"} & tasks):
        if not 350 <= len(english_words) <= 500:
            add(
                issues,
                "WARNING",
                "DESCRIPTION_LENGTH",
                f"Generation detailed_description has about {len(english_words)} English words; 350-500 is usual, not mandatory.",
            )

    if re.search(r"(?i)negative prompt\s*:", "\n".join(sections.values())):
        add(
            issues,
            "ERROR",
            "NEGATIVE_FIELD",
            "Do not add a separate negative-prompt field inside the six-section prompt.",
        )

    fully_copy = re.search(r"(?m)^\s*<Audio\s+\d+>.*:\s*fully_copy\s*-", sections["retention_analysis"])
    if fully_copy:
        audio_summaries = sections["overall_soundscape"] + "\n" + sections["non_diegetic_music"]
        if not re.search(r"<Audio\s+\d+>", audio_summaries):
            add(
                issues,
                "WARNING",
                "FULLY_COPY_LAYERING",
                "An Audio label is fully_copy; verify that new sound/music layers do not contradict a complete final-track copy.",
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", type=Path, help="UTF-8 text file containing one six-section prompt")
    parser.add_argument("--duration", type=int, help="Target duration in integer seconds")
    parser.add_argument("--picture-count", type=int, help="Actual attached reference-image count")
    parser.add_argument("--video-count", type=int, help="Actual attached reference-video count")
    parser.add_argument("--audio-count", type=int, help="Actual attached reference-audio count")
    parser.add_argument(
        "--video-duration", type=float, action="append", default=[], help="Duration of one reference video; repeat per file"
    )
    parser.add_argument(
        "--audio-duration", type=float, action="append", default=[], help="Duration of one reference audio file; repeat per file"
    )
    parser.add_argument("--request-bytes", type=int, help="Complete API request-body size in bytes")
    parser.add_argument("--uses-first-frame", action="store_true", help="Request uses the first_frame API role")
    parser.add_argument("--uses-last-frame", action="store_true", help="Request uses the last_frame API role")
    parser.add_argument("--uses-reference-role", action="store_true", help="Request uses any reference_* API role")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        text = args.prompt.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    except OSError as exc:
        print(f"ERROR IO: {exc}")
        return 2

    issues: list[Issue] = []
    if len(text) > 7000:
        add(issues, "ERROR", "CHAR_LIMIT", f"Prompt has {len(text)} characters; maximum is 7000.")
    if "```" in text:
        add(issues, "ERROR", "MARKDOWN_FENCE", "Remove Markdown code fences from the prompt text.")
    if re.search(r"(?m)^\s*#{1,6}\s+", text):
        add(issues, "ERROR", "MARKDOWN_HEADING", "Remove Markdown headings from the prompt text.")
    if re.search(r"(?m)^\s*[-*+]\s+", text):
        add(issues, "ERROR", "MARKDOWN_LIST", "Remove Markdown list bullets from the prompt text.")

    sections = parse_sections(text, issues)
    tasks: set[str] = set()
    if sections:
        validate_labels(sections, issues)
        tasks = validate_summary(sections, issues)
        validate_timeline(sections["detailed_description"], args.duration, issues)
        validate_dialogue(sections, issues)
        validate_quality_signals(sections, tasks, issues)
    validate_asset_envelope(args, text, issues)

    severity_order = {"ERROR": 0, "WARNING": 1}
    for issue in sorted(issues, key=lambda item: (severity_order[item.severity], item.code, item.message)):
        print(f"{issue.severity} {issue.code}: {issue.message}")

    error_count = sum(issue.severity == "ERROR" for issue in issues)
    warning_count = sum(issue.severity == "WARNING" for issue in issues)
    if error_count:
        print(f"FAIL: {error_count} error(s), {warning_count} warning(s).")
        return 1
    print(f"PASS: 0 errors, {warning_count} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
