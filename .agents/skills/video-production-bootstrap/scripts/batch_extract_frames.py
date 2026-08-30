#!/usr/bin/env python3
"""Extract several preview frames in one FFmpeg process for one explicit project."""

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


def parse_time(value: str) -> float:
    text = value.strip()
    try:
        if ":" not in text:
            result = float(text)
        else:
            parts = [float(part) for part in text.split(":")]
            if len(parts) not in {2, 3} or any(part < 0 for part in parts):
                raise ValueError
            result = parts[-1] + parts[-2] * 60
            if len(parts) == 3:
                result += parts[0] * 3600
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid time {value!r}; use seconds or HH:MM:SS.mmm"
        ) from exc
    if result < 0:
        raise argparse.ArgumentTypeError("time cannot be negative")
    return result


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
        raise RuntimeError(completed.stderr.strip() or "ffprobe failed")
    data = json.loads(completed.stdout)
    streams = data.get("streams", [])
    if not streams:
        raise ValueError(f"video stream not found: {path}")
    stream = streams[0]
    return {
        "duration_seconds": float(data["format"]["duration"]),
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "frame_rate": stream.get("avg_frame_rate") or stream.get("r_frame_rate"),
    }


def ensure_unique(values: list[float]) -> list[float]:
    result = sorted(values)
    if len(set(result)) != len(result):
        raise ValueError("time points must be unique")
    return result


def safe_stem(path: Path) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z._\u4e00-\u9fff-]+", "-", path.stem).strip("-._")
    return (cleaned or "preview")[:60]


def ensure_inside(path: Path, parent: Path, label: str) -> None:
    try:
        path.relative_to(parent)
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside {parent}: {path}") from exc


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
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
    parser.add_argument("--input", required=True, type=Path, help="Existing video preview; it is never rendered automatically")
    parser.add_argument("--time", required=True, type=parse_time, action="append", dest="times", help="Frame time; repeat for multiple points")
    parser.add_argument("--width", type=int, default=1280, help="Maximum output width (default: 1280)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Validate and print the plan without writing (default)")
    mode.add_argument("--execute", action="store_true", help="Extract frames and write the JSON index")
    args = parser.parse_args()

    if args.width < 160 or args.width > 7680:
        raise ValueError("--width must be between 160 and 7680")
    times = ensure_unique(args.times)
    project = require_project(args.project)
    preview_candidate = args.input.expanduser()
    if not preview_candidate.exists():
        raise FileNotFoundError(
            f"preview does not exist: {preview_candidate}; Remotion will not be rendered automatically"
        )
    preview = preview_candidate.resolve(strict=True)
    if not preview.is_file():
        raise ValueError(f"preview is not a file: {preview}")
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise FileNotFoundError("ffmpeg and ffprobe are required")
    info = probe(preview, ffprobe)
    if any(time >= info["duration_seconds"] for time in times):
        raise ValueError(f"all time points must be before preview duration ({info['duration_seconds']:.3f}s)")

    output_dir = (project / "06-预览与审核" / "关键帧").resolve()
    ensure_inside(output_dir, project, "keyframe output directory")
    prefix = safe_stem(preview)
    filenames = [f"{prefix}__{index:03d}__{time:012.3f}s.png" for index, time in enumerate(times, start=1)]
    targets = [output_dir / name for name in filenames]
    index_path = output_dir / f"{prefix}__关键帧索引.json"
    for target in [*targets, index_path]:
        if target.exists():
            raise FileExistsError(f"refusing to overwrite existing target: {target}")

    split_outputs = "".join(f"[v{index}]" for index in range(len(times)))
    filter_parts = [f"[0:v]split={len(times)}{split_outputs}"]
    for index, time in enumerate(times):
        filter_parts.append(
            f"[v{index}]trim=start={time:.6f},setpts=PTS-STARTPTS,"
            f"scale='trunc(min({args.width},iw)/2)*2':-2[f{index}]"
        )
    filter_complex = ";".join(filter_parts)
    command = [
        ffmpeg,
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-n",
        "-i",
        str(preview),
        "-filter_complex",
        filter_complex,
    ]
    for index, target in enumerate(targets):
        command.extend(
            ["-map", f"[f{index}]", "-frames:v", "1", "-fps_mode", "vfr", str(target)]
        )
    plan = {
        "mode": "execute" if args.execute else "dry-run",
        "project": str(project),
        "preview": str(preview),
        "time_points_seconds": times,
        "source_frame_rate": info["frame_rate"],
        "outputs": [str(target) for target in targets],
        "index": str(index_path),
        "single_ffmpeg_process": True,
        "remotion_render": False,
        "command": command,
    }
    if not args.execute:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        print("DRY RUN: no frames, index, Remotion process, or render was started.")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=".frames-", dir=output_dir))
    temporary_targets = [temporary_dir / target.name for target in targets]
    execution_command = [
        ffmpeg,
        "-nostdin",
        "-hide_banner",
        "-loglevel",
        "error",
        "-n",
        "-i",
        str(preview),
        "-filter_complex",
        filter_complex,
    ]
    for index, target in enumerate(temporary_targets):
        execution_command.extend(
            ["-map", f"[f{index}]", "-frames:v", "1", "-fps_mode", "vfr", str(target)]
        )
    published: list[Path] = []
    try:
        completed = subprocess.run(execution_command, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"ffmpeg exited with status {completed.returncode}")
        generated = [target for target in temporary_targets if target.is_file()]
        if len(generated) != len(times):
            raise RuntimeError(f"ffmpeg produced {len(generated)} frames; expected {len(times)}")
        if any(target.exists() for target in [*targets, index_path]):
            raise FileExistsError("a target appeared while FFmpeg was running; refusing to overwrite it")
        for source_path, target in zip(generated, targets):
            publish_no_overwrite(source_path, target)
            published.append(target)
        payload = {
            "schema_version": 1,
            "kind": "preview_keyframes",
            "created_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            "project_path": str(project),
            "preview_absolute_path": str(preview),
            "preview_read_only": True,
            "source": {
                "width": info["width"],
                "height": info["height"],
                "frame_rate": info["frame_rate"],
                "duration_seconds": info["duration_seconds"],
            },
            "frames": [
                {
                    "time_seconds": time,
                    "selection": "first decoded frame at or after the requested time",
                    "image_absolute_path": str(target),
                    "project_relative_path": str(target.relative_to(project)),
                }
                for time, target in zip(times, targets)
            ],
        }
        atomic_write(index_path, payload)
        published.clear()
    except Exception:
        for target in published:
            target.unlink(missing_ok=True)
        raise
    finally:
        shutil.rmtree(temporary_dir, ignore_errors=True)

    print(f"EXTRACTED {len(targets)} FRAMES with one FFmpeg process")
    print(f"CREATED INDEX {index_path}")
    print("REMOTION NOT RENDERED: the supplied preview was read only.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileExistsError, FileNotFoundError, json.JSONDecodeError, OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
