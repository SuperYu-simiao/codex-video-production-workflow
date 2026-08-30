#!/usr/bin/env python3
"""Create a short, reconnectable FFmpeg proxy for one explicit source range."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SAFE_STEM = re.compile(r"[^0-9A-Za-z._\u4e00-\u9fff-]+")


def parse_time(value: str) -> float:
    text = value.strip()
    if not text:
        raise argparse.ArgumentTypeError("time cannot be empty")
    try:
        if ":" not in text:
            seconds = float(text)
        else:
            parts = text.split(":")
            if len(parts) not in {2, 3}:
                raise ValueError
            numbers = [float(part) for part in parts]
            if any(part < 0 for part in numbers):
                raise ValueError
            seconds = numbers[-1] + numbers[-2] * 60
            if len(numbers) == 3:
                seconds += numbers[0] * 3600
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid time {value!r}; use seconds or HH:MM:SS.mmm"
        ) from exc
    if seconds < 0:
        raise argparse.ArgumentTypeError("time cannot be negative")
    return seconds


def require_executable(name: str) -> str:
    executable = shutil.which(name)
    if not executable:
        raise FileNotFoundError(f"required executable not found: {name}")
    return executable


def require_project(value: Path) -> Path:
    project = value.expanduser().resolve(strict=True)
    if not project.is_dir() or not (project / "project.json").is_file():
        raise ValueError(f"project must be a directory containing project.json: {project}")
    return project


def probe(path: Path, ffprobe: str) -> dict[str, Any]:
    command = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,avg_frame_rate,r_frame_rate:format=duration",
        "-of",
        "json",
        str(path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "unknown ffprobe error"
        raise RuntimeError(f"ffprobe failed for {path}: {detail}")
    data = json.loads(completed.stdout)
    streams = data.get("streams", [])
    if not streams:
        raise ValueError(f"video stream not found: {path}")
    stream = streams[0]
    duration_text = data.get("format", {}).get("duration")
    if duration_text is None:
        raise ValueError(f"video duration not available: {path}")
    return {
        "duration_seconds": float(duration_text),
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "frame_rate": stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "unknown",
    }


def time_slug(seconds: float) -> str:
    return f"{round(seconds * 1000):012d}"


def safe_stem(path: Path) -> str:
    cleaned = SAFE_STEM.sub("-", path.stem).strip("-._")
    return (cleaned or "source")[:80]


def ensure_inside(path: Path, parent: Path, label: str) -> None:
    try:
        path.relative_to(parent)
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside {parent}: {path}") from exc


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        publish_no_overwrite(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def publish_no_overwrite(source: Path, destination: Path) -> None:
    """Atomically publish a same-filesystem file without replacing a target."""
    try:
        os.link(source, destination)
    except FileExistsError as exc:
        raise FileExistsError(f"refusing to overwrite existing target: {destination}") from exc
    try:
        source.unlink()
    except OSError:
        destination.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path, help="Current project directory containing project.json")
    parser.add_argument("--input", required=True, type=Path, help="Explicit source video path; it is always read-only")
    parser.add_argument("--start", required=True, type=parse_time, help="Range start in seconds or HH:MM:SS.mmm")
    parser.add_argument("--end", required=True, type=parse_time, help="Range end in seconds or HH:MM:SS.mmm")
    parser.add_argument("--height", type=int, default=720, help="Maximum proxy height (default: 720)")
    parser.add_argument("--fps", type=float, default=30.0, help="Proxy frame rate (default: 30)")
    parser.add_argument("--output-name", help="Optional .mp4 filename inside 03-精剪输出/代理片段")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Validate and print the plan without writing (default)")
    mode.add_argument("--execute", action="store_true", help="Create the proxy and its sidecar JSON manifest")
    args = parser.parse_args()

    if args.end <= args.start:
        raise ValueError("--end must be greater than --start")
    if args.height < 144 or args.height > 4320:
        raise ValueError("--height must be between 144 and 4320")
    if args.fps <= 0 or args.fps > 120:
        raise ValueError("--fps must be greater than 0 and at most 120")

    project = require_project(args.project)
    source = args.input.expanduser().resolve(strict=True)
    if not source.is_file():
        raise ValueError(f"input is not a file: {source}")
    ffmpeg = require_executable("ffmpeg")
    ffprobe = require_executable("ffprobe")
    source_info = probe(source, ffprobe)
    if args.start >= source_info["duration_seconds"]:
        raise ValueError("--start is outside the source duration")
    if args.end > source_info["duration_seconds"] + 0.001:
        raise ValueError(
            f"--end ({args.end:.3f}) exceeds source duration ({source_info['duration_seconds']:.3f})"
        )

    output_dir = (project / "03-精剪输出" / "代理片段").resolve()
    ensure_inside(output_dir, project, "proxy output directory")
    default_name = (
        f"{safe_stem(source)}__{time_slug(args.start)}-{time_slug(args.end)}-proxy.mp4"
    )
    output_name = args.output_name or default_name
    if Path(output_name).name != output_name or not output_name.lower().endswith(".mp4"):
        raise ValueError("--output-name must be a plain filename ending in .mp4")
    output = (output_dir / output_name).resolve()
    ensure_inside(output, output_dir, "proxy output")
    manifest = output.with_suffix(".proxy.json")
    if output == source:
        raise ValueError("proxy output cannot be the source file")
    for target in (output, manifest):
        if target.exists():
            raise FileExistsError(f"refusing to overwrite existing target: {target}")

    duration = args.end - args.start
    command = [
        ffmpeg,
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-n",
        "-ss",
        f"{args.start:.6f}",
        "-i",
        str(source),
        "-t",
        f"{duration:.6f}",
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-vf",
        f"scale=-2:'trunc(min({args.height},ih)/2)*2'",
        "-r",
        f"{args.fps:g}",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
    ]

    plan = {
        "mode": "execute" if args.execute else "dry-run",
        "project": str(project),
        "source_read_only": str(source),
        "source_duration_seconds": source_info["duration_seconds"],
        "range": {"start_seconds": args.start, "end_seconds": args.end, "duration_seconds": duration},
        "proxy": str(output),
        "manifest": str(manifest),
        "command": [*command, str(output)],
    }
    if not args.execute:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        print("DRY RUN: no directory or media file was created.")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=".proxy-", dir=output_dir))
    temporary_output = temporary_dir / output.name
    try:
        completed = subprocess.run([*command, str(temporary_output)], check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"ffmpeg exited with status {completed.returncode}")
        proxy_info = probe(temporary_output, ffprobe)
        if output.exists() or manifest.exists():
            raise FileExistsError("a target appeared while FFmpeg was running; refusing to overwrite it")
        publish_no_overwrite(temporary_output, output)
        payload = {
            "schema_version": 1,
            "kind": "short_proxy",
            "created_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "project_path": str(project),
            "source": {
                "absolute_path": str(source),
                "read_only": True,
                "duration_seconds": source_info["duration_seconds"],
            },
            "range": {
                "start_seconds": args.start,
                "end_seconds": args.end,
                "duration_seconds": duration,
            },
            "proxy": {
                "absolute_path": str(output),
                "project_relative_path": str(output.relative_to(project)),
                "width": proxy_info["width"],
                "height": proxy_info["height"],
                "frame_rate": proxy_info["frame_rate"],
                "duration_seconds": proxy_info["duration_seconds"],
            },
            "relink": {
                "source_absolute_path": str(source),
                "source_in_seconds": args.start,
                "source_out_seconds": args.end,
            },
        }
        try:
            atomic_write_json(manifest, payload)
        except Exception:
            output.unlink(missing_ok=True)
            raise
    finally:
        shutil.rmtree(temporary_dir, ignore_errors=True)

    print(f"CREATED PROXY {output}")
    print(f"CREATED MANIFEST {manifest}")
    print("SOURCE UNCHANGED: original media was only read by FFmpeg.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileExistsError, FileNotFoundError, json.JSONDecodeError, OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
