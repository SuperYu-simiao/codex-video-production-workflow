#!/usr/bin/env python3
"""Read-only dependency checker for the shared video-production workflow."""

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


def find_repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "dependencies.json").is_file() and (parent / "workflow.json").is_file():
            return parent
    raise FileNotFoundError("Could not locate dependencies.json and workflow.json")


def version_tuple(value: str) -> tuple[int, ...]:
    match = re.search(r"(\d+(?:\.\d+)+)", value)
    return tuple(int(part) for part in match.group(1).split(".")) if match else ()


def meets_minimum(actual: str, minimum: str | None) -> bool:
    if not minimum:
        return True
    actual_parts = version_tuple(actual)
    minimum_parts = version_tuple(minimum)
    width = max(len(actual_parts), len(minimum_parts))
    return actual_parts + (0,) * (width - len(actual_parts)) >= minimum_parts + (0,) * (width - len(minimum_parts))


def expand_path(value: str, repo_root: Path) -> Path:
    replaced = value.replace("${REPO_ROOT}", str(repo_root))
    return Path(os.path.expanduser(replaced)).resolve()


def command_result(item: dict[str, Any]) -> dict[str, Any]:
    argv = item["command"]
    executable = shutil.which(argv[0])
    result = {
        "category": "system_tool",
        "name": item["id"],
        "required": item["required"],
        "status": "missing",
        "details": item.get("install_hint_macos", ""),
    }
    if not executable:
        return result
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=15, check=False)
    output = (completed.stdout or completed.stderr).splitlines()
    actual = output[0].strip() if output else "installed"
    result["details"] = actual
    if completed.returncode != 0:
        result["status"] = "error"
    elif meets_minimum(actual, item.get("minimum_version")):
        result["status"] = "ok"
    else:
        result["status"] = "outdated"
        result["details"] = f"{actual}; requires >= {item['minimum_version']}"
    return result


def check(manifest: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    results = [command_result(item) for item in manifest["system_tools"]]

    for item in manifest["repo_skills"]:
        path = repo_root / item["path"]
        results.append({
            "category": "repo_skill",
            "name": item["name"],
            "required": item["required"],
            "status": "ok" if path.is_file() else "missing",
            "details": str(path),
        })

    for item in manifest["external_skills"]:
        candidates = [expand_path(path, repo_root) for path in item["accepted_paths"]]
        installed = next((path for path in candidates if (path / "SKILL.md").is_file()), None)
        results.append({
            "category": "external_skill",
            "name": item["name"],
            "required": item["required"],
            "status": "ok" if installed else "missing",
            "details": str(installed or expand_path(item["install_path"], repo_root)),
        })

    plugin_cache = Path.home() / ".codex" / "plugins" / "cache"
    for item in manifest["codex_plugins"]:
        matches = list(plugin_cache.glob(item["cache_glob"])) if plugin_cache.exists() else []
        results.append({
            "category": "codex_plugin",
            "name": item["id"],
            "required": item["required"],
            "status": "ok" if matches else "missing",
            "details": str(matches[-1]) if matches else item["install_method"],
        })

    for item in manifest["accounts_and_credentials"]:
        variables = item.get("environment_variables", [])
        if not variables:
            continue
        present = any(os.environ.get(variable) for variable in variables)
        results.append({
            "category": "credential",
            "name": item["id"],
            "required": item["required"],
            "status": "ok" if present else "missing",
            "details": "environment variable is set" if present else f"set one of: {', '.join(variables)}",
        })

    workflow = manifest["workflow"]
    for relative_path in workflow["required_files"]:
        path = repo_root / relative_path
        results.append({
            "category": "workflow",
            "name": relative_path,
            "required": True,
            "status": "ok" if path.is_file() else "missing",
            "details": str(path),
        })

    workflow_path = repo_root / workflow["definition"]
    if workflow_path.is_file():
        definition = json.loads(workflow_path.read_text(encoding="utf-8"))
        layout_count = len(definition.get("project_directories", []))
        results.append({
            "category": "workflow",
            "name": "project-directory-layout",
            "required": True,
            "status": "ok" if layout_count else "missing",
            "details": f"{layout_count} project directories defined in {workflow_path}",
        })

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, help="Override dependencies.json path")
    parser.add_argument("--json", action="store_true", help="Print machine-readable results")
    args = parser.parse_args()

    script_path = Path(__file__).resolve()
    repo_root = find_repo_root(script_path)
    manifest_path = args.manifest.resolve() if args.manifest else repo_root / "dependencies.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    results = check(manifest, repo_root)
    failures = [item for item in results if item["required"] and item["status"] != "ok"]

    if args.json:
        print(json.dumps({"manifest": str(manifest_path), "ok": not failures, "results": results}, ensure_ascii=False, indent=2))
    else:
        print(f"Manifest: {manifest_path}")
        for item in results:
            requirement = "required" if item["required"] else "optional"
            print(f"[{item['status']:<8}] {item['category']:<16} {item['name']} ({requirement})")
            print(f"           {item['details']}")
        print()
        if failures:
            print(f"Required items needing attention: {len(failures)}")
            print("External Skills can be installed only after approval with:")
            print("  python3 .agents/skills/video-production-bootstrap/scripts/install_dependencies.py --install")
        else:
            print("All required checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
