#!/usr/bin/env python3
"""Validate an SRT file's structure without changing it or interpreting its speech."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TIME_RE = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")


def parse_time(value: str) -> int:
    match = TIME_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"invalid SRT timestamp: {value!r}")
    hours, minutes, seconds, millis = (int(part) for part in match.groups())
    if minutes > 59 or seconds > 59:
        raise ValueError(f"timestamp component out of range: {value!r}")
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def parse_srt(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n"))
    cues: list[dict[str, object]] = []
    for block_number, block in enumerate(blocks, start=1):
        lines = [line.rstrip() for line in block.split("\n")]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        if not lines:
            continue
        if len(lines) < 3:
            raise ValueError(f"block {block_number} must contain an index, timing line, and text")
        try:
            index = int(lines[0].strip())
        except ValueError as exc:
            raise ValueError(f"block {block_number} has a non-numeric index") from exc
        if index <= 0:
            raise ValueError(f"block {block_number} index must be positive")
        timing = lines[1].split("-->")
        if len(timing) != 2:
            raise ValueError(f"block {block_number} has an invalid timing line")
        start = parse_time(timing[0])
        end = parse_time(timing[1])
        if end <= start:
            raise ValueError(f"block {block_number} has non-positive duration")
        text_lines = [line.strip() for line in lines[2:] if line.strip()]
        if not text_lines:
            raise ValueError(f"block {block_number} has empty text")
        cues.append({"index": index, "start_ms": start, "end_ms": end, "text": "\n".join(text_lines)})
    if not cues:
        raise ValueError("SRT contains no cues")
    return cues


def validate(cues: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    previous_index = 0
    previous_end = -1
    seen_indices: set[int] = set()
    for position, cue in enumerate(cues, start=1):
        index = int(cue["index"])
        start = int(cue["start_ms"])
        end = int(cue["end_ms"])
        if index in seen_indices:
            errors.append(f"cue {position}: duplicate index {index}")
        seen_indices.add(index)
        if index <= previous_index:
            errors.append(f"cue {position}: index {index} is not strictly increasing")
        if start < previous_end:
            errors.append(f"cue {position}: overlaps previous cue by {previous_end - start}ms")
        previous_index = index
        previous_end = end
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--srt", type=Path, required=True, help="SRT file to validate")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable report")
    args = parser.parse_args()
    try:
        cues = parse_srt(args.srt.resolve())
        errors = validate(cues)
    except (OSError, UnicodeError, ValueError) as exc:
        errors = [str(exc)]
        cues = []
    report = {
        "path": str(args.srt.resolve()),
        "ok": not errors,
        "cue_count": len(cues),
        "duration_ms": cues[-1]["end_ms"] if cues else None,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"SRT: {report['path']}")
        print(f"Cues: {report['cue_count']}")
        if errors:
            print("INVALID")
            for error in errors:
                print(f"- {error}")
        else:
            print("VALID: timestamps, ordering, durations, and overlaps passed")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
