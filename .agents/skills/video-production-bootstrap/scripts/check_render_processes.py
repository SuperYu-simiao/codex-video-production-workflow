#!/usr/bin/env python3
"""List suspected render processes associated with one explicit video project."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def require_project(value: Path) -> Path:
    project = value.expanduser().resolve(strict=True)
    if not project.is_dir() or not (project / "project.json").is_file():
        raise ValueError(f"project must be a directory containing project.json: {project}")
    return project


def process_kind(command: str) -> str | None:
    lowered = command.lower()
    executable = Path(command.split(maxsplit=1)[0]).name.lower() if command.split() else ""
    if executable.startswith("ffmpeg") or "/ffmpeg " in lowered:
        return "ffmpeg"
    if "remotion" in lowered:
        return "remotion"
    if "chromium" in lowered or "chrome headless shell" in lowered:
        return "chromium"
    node_markers = (" render ", "render.js", "render.ts", "renderer", "bundle")
    if (executable in {"node", "nodejs", "npm", "npx"} or "/node " in lowered) and any(
        marker in lowered for marker in node_markers
    ):
        return "render-node"
    return None


def process_cwd(pid: int, lsof: str | None) -> Path | None:
    if not lsof:
        return None
    completed = subprocess.run(
        [lsof, "-a", "-p", str(pid), "-d", "cwd", "-Fn"],
        capture_output=True,
        text=True,
        check=False,
        timeout=5,
    )
    if completed.returncode != 0:
        return None
    for line in completed.stdout.splitlines():
        if line.startswith("n/"):
            try:
                return Path(line[1:]).resolve()
            except OSError:
                return None
    return None


def is_inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def command_mentions_project(command: str, project: Path) -> bool:
    escaped = re.escape(str(project))
    return re.search(rf"(?:^|[\s='\"]){escaped}(?:$|[/\s'\"])", command) is not None


def collect(project: Path) -> list[dict[str, Any]]:
    ps = shutil.which("ps")
    if not ps:
        raise FileNotFoundError("required executable not found: ps")
    completed = subprocess.run(
        [ps, "-axo", "pid=,etime=,command="], capture_output=True, text=True, check=True
    )
    lsof = shutil.which("lsof")
    project_text = str(project)
    matches: list[dict[str, Any]] = []
    for line in completed.stdout.splitlines():
        fields = line.strip().split(maxsplit=2)
        if len(fields) != 3:
            continue
        pid_text, elapsed, command = fields
        try:
            pid = int(pid_text)
        except ValueError:
            continue
        if pid == os.getpid():
            continue
        kind = process_kind(command)
        if not kind:
            continue
        association = "command"
        cwd: Path | None = None
        if not command_mentions_project(command, project):
            cwd = process_cwd(pid, lsof)
            if not cwd or not is_inside(cwd, project):
                continue
            association = "working_directory"
        matches.append(
            {
                "pid": pid,
                "elapsed": elapsed,
                "kind": kind,
                "command": command,
                "associated_project_path": project_text,
                "association_evidence": association,
                **({"working_directory": str(cwd)} if cwd else {}),
            }
        )
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=(
            "This tool is intentionally read-only. It has no kill/terminate option; "
            "review exact PIDs and commands before using a separate explicit process command."
        ),
    )
    parser.add_argument("--project", required=True, type=Path, help="Current project directory containing project.json")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    project = require_project(args.project)
    matches = collect(project)
    if args.json:
        print(
            json.dumps(
                {
                    "project": str(project),
                    "read_only": True,
                    "terminate_supported": False,
                    "matches": matches,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"CURRENT PROJECT: {project}")
        print("READ ONLY: no process will be signaled or terminated.")
        if not matches:
            print("No suspected Remotion, FFmpeg, Chromium, or render Node process matched this project.")
        else:
            print(f"MATCHED {len(matches)} process(es):")
            for item in matches:
                print(
                    f"PID={item['pid']} ELAPSED={item['elapsed']} KIND={item['kind']} "
                    f"PROJECT={item['associated_project_path']}"
                )
                print(f"  COMMAND={item['command']}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
