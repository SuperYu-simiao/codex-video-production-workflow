#!/usr/bin/env python3
"""Install this repository's unified video-editing Skill and optional external Skills."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "workflow.json").is_file() and (parent / "skills" / "video-editing-workflow" / "SKILL.md").is_file():
            return parent
    raise FileNotFoundError("Could not locate workflow.json and skills/video-editing-workflow/SKILL.md")


def codex_skills_root() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return (Path(configured).expanduser() if configured else Path.home() / ".codex") / "skills"


def install_link(source: Path, destination: Path, execute: bool) -> None:
    source = source.resolve()
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() and destination.resolve() == source:
            print(f"SKIP {destination}: already linked")
            return
        raise FileExistsError(f"Refusing to overwrite existing path: {destination}")
    print(f"WOULD LINK {source} -> {destination}" if not execute else f"LINK {source} -> {destination}")
    if execute:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(source, target_is_directory=True)


def run_external_installer(repo_root: Path) -> int:
    script = repo_root / ".agents" / "skills" / "video-production-bootstrap" / "scripts" / "install_dependencies.py"
    completed = subprocess.run([sys.executable, str(script), "--install"], check=False)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="Create the local Skill link")
    parser.add_argument("--with-external", action="store_true", help="Also install pinned video-use and video-shotcraft Skills")
    parser.add_argument("--all", action="store_true", help="Install the local Skill and pinned external Skills")
    args = parser.parse_args()
    if args.with_external or args.all:
        args.install = True

    repo_root = find_repo_root(Path(__file__).resolve())
    source = repo_root / "skills" / "video-editing-workflow"
    destination = codex_skills_root() / "video-editing-workflow"
    if not args.install:
        print("Dry run only. No files were changed.")
        install_link(source, destination, execute=False)
        if args.with_external or args.all:
            print("WOULD RUN pinned external Skill installer")
        print("Pass --install for the local Skill, or --all for the full setup.")
        return 0

    install_link(source, destination, execute=True)
    if args.with_external or args.all:
        if not shutil.which("git"):
            raise RuntimeError("git is required before external Skills can be installed")
        return run_external_installer(repo_root)
    print("Installed the unified Skill. Run check_dependencies.py to inspect optional external tools.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FileNotFoundError, FileExistsError, OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
