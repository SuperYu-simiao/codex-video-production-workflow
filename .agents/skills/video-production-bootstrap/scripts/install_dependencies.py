#!/usr/bin/env python3
"""Install pinned external video Skills after explicit authorization."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "dependencies.json").is_file() and (parent / "workflow.json").is_file():
            return parent
    raise FileNotFoundError("Could not locate dependencies.json and workflow.json")


def expand_path(value: str, repo_root: Path) -> Path:
    return Path(os.path.expanduser(value.replace("${REPO_ROOT}", str(repo_root)))).resolve()


def run(argv: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(argv))
    subprocess.run(argv, cwd=cwd, check=True)


def install_skill(item: dict[str, Any], repo_root: Path, install_deps: bool) -> None:
    destination = expand_path(item["install_path"], repo_root)
    if (destination / "SKILL.md").is_file():
        print(f"SKIP {item['name']}: already installed at {destination}")
        return
    if destination.exists():
        raise RuntimeError(f"Refusing to overwrite non-Skill path: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)

    temp_path = Path(tempfile.mkdtemp(prefix=f".{item['name']}-", dir=destination.parent))
    try:
        run(["git", "clone", "--filter=blob:none", "--no-checkout", item["repository"], str(temp_path)])
        run(["git", "-C", str(temp_path), "checkout", "--detach", item["ref"]])
        head = subprocess.check_output(["git", "-C", str(temp_path), "rev-parse", "HEAD"], text=True).strip()
        if head != item["ref"]:
            raise RuntimeError(f"Commit verification failed for {item['name']}: {head}")
        if not (temp_path / "SKILL.md").is_file():
            raise RuntimeError(f"Downloaded repository has no root SKILL.md: {item['repository']}")
        os.replace(temp_path, destination)
    except Exception:
        shutil.rmtree(temp_path, ignore_errors=True)
        raise

    print(f"INSTALLED {item['name']} at {destination}")
    post_install = item.get("post_install")
    if install_deps and post_install and post_install.get("kind") == "uv_sync":
        if not shutil.which("uv"):
            raise RuntimeError(f"uv is required to finish installing {item['name']}")
        run(["uv", "sync"], cwd=destination)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="Perform external Skill installation")
    parser.add_argument("--skip-skill-deps", action="store_true", help="Clone Skills without running uv sync")
    parser.add_argument("--manifest", type=Path, help="Override dependencies.json path")
    args = parser.parse_args()

    repo_root = find_repo_root(Path(__file__).resolve())
    manifest_path = args.manifest.resolve() if args.manifest else repo_root / "dependencies.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if not args.install:
        print("Dry run only. No files were changed.")
        for item in manifest["external_skills"]:
            if item["required"]:
                print(f"WOULD INSTALL {item['name']} {item['ref']} -> {item['install_path']}")
        print("Pass --install only after the user explicitly authorizes installation.")
        return 0

    if not shutil.which("git"):
        raise RuntimeError("git is required before external Skills can be installed")
    for item in manifest["external_skills"]:
        if item["required"]:
            install_skill(item, repo_root, install_deps=not args.skip_skill_deps)

    checker = Path(__file__).with_name("check_dependencies.py")
    completed = subprocess.run([sys.executable, str(checker)], check=False)
    return completed.returncode


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
