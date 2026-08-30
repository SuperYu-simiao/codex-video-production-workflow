#!/usr/bin/env python3
"""Create one isolated local video project from the public workflow template."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


INVALID_NAME = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "workflow.json").is_file() and (parent / "项目模板").is_dir():
            return parent
    raise FileNotFoundError("Could not locate workflow.json and 项目模板")


def validate_name(value: str) -> str:
    name = value.strip()
    if not name or name in {".", ".."}:
        raise ValueError("Project name cannot be empty, '.' or '..'")
    if name.startswith(".") or INVALID_NAME.search(name):
        raise ValueError("Project name contains a hidden-path prefix or unsupported filename character")
    if len(name) > 80:
        raise ValueError("Project name must be 80 characters or fewer")
    return name


def render_template(path: Path, project_name: str, created_at: str) -> str:
    return (
        path.read_text(encoding="utf-8")
        .replace("__PROJECT_NAME__", project_name)
        .replace("__CREATED_AT__", created_at)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="Project folder name, for example 产品功能演示")
    parser.add_argument("--projects-root", type=Path, help="Override the default 本地项目 directory")
    parser.add_argument("--dry-run", action="store_true", help="Print the planned project structure without creating it")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve())
    workflow_path = repo_root / "workflow.json"
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    project_name = validate_name(args.name)
    projects_root = (args.projects_root or (repo_root / workflow["projects_root"])).expanduser().resolve()
    target = (projects_root / project_name).resolve()
    if target.parent != projects_root:
        raise ValueError("Project path escaped the configured projects root")
    if target.exists():
        raise FileExistsError(f"Project already exists: {target}")

    directories = [item["path"] for item in workflow["project_directories"]]
    if args.dry_run:
        print(f"WOULD CREATE {target}")
        print("  project.json")
        print("  项目说明.md")
        for relative_path in directories:
            print(f"  {relative_path}/")
        for item in workflow.get("project_template_files", []):
            print(f"  {item['destination']}")
        return 0

    template_root = repo_root / workflow["project_template"]
    created_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    projects_root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{project_name}-", dir=projects_root))
    try:
        for relative_path in directories:
            (staging / relative_path).mkdir(parents=True, exist_ok=True)
        (staging / "project.json").write_text(
            render_template(template_root / "project.json", project_name, created_at),
            encoding="utf-8",
        )
        (staging / "项目说明.md").write_text(
            render_template(template_root / "项目说明.md", project_name, created_at),
            encoding="utf-8",
        )
        for item in workflow.get("project_template_files", []):
            source = template_root / item["source"]
            destination = staging / item["destination"]
            if not source.is_file():
                raise FileNotFoundError(f"Project template file does not exist: {source}")
            if destination.exists():
                raise FileExistsError(f"Project template destination already exists: {destination}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                render_template(source, project_name, created_at), encoding="utf-8"
            )
        os.replace(staging, target)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    print(f"CREATED {target}")
    print(f"NEXT: Put source files in {target / '01-原始素材'}")
    print(f"START: Tell Codex to continue project '{project_name}'")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileExistsError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
