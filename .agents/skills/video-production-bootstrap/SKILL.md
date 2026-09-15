---
name: video-production-bootstrap
description: "Set up and operate this repository's reusable video workflow: check dependencies, install pinned GitHub Skills, create isolated project folders, route source media and outputs, and enforce editing and render approval gates. Use after cloning, when starting a new video, when locating project media, or when diagnosing setup. Do not read personal projects, edit, render, or upload merely because setup was requested."
---

# Video Production Bootstrap

For a complete edit, use the repository's unified `skills/video-editing-workflow/SKILL.md` entry point. This bootstrap Skill remains responsible for setup, project isolation, dependency checks, and approval boundaries; the unified Skill routes the actual `video-use -> video-shotcraft -> Remotion` production chain.

Use the public workflow without exposing the author's projects or mixing multiple videos.

## First read

Read these files from the repository root:

1. `skills/video-editing-workflow/SKILL.md`
2. `workflow.json`
3. `docs/00-先读我.md` and `dependencies.json` for setup
4. `effects.json` and `特效与切屏规范.md` only after material readiness and when packaging begins

Run the read-only dependency check before installing anything:

```bash
python3 .agents/skills/video-production-bootstrap/scripts/check_dependencies.py
```

Do not install, create credentials, read project media, edit, render, or upload unless the user's request authorizes that exact action.

## Install external Skills

After explicit installation approval, run:

```bash
python3 .agents/skills/video-production-bootstrap/scripts/install_dependencies.py --install
```

The installer clones only the pinned external Skill commits in `dependencies.json`. It does not install Homebrew packages, Codex plugins, API keys, or project npm dependencies. It never overwrites an existing non-Skill directory or prints secret values.

To install the repository's unified Skill and the pinned external Skills in one explicit step:

```bash
python3 .agents/skills/video-production-bootstrap/scripts/install_workflow.py --all
```

The command creates a symlink for `skills/video-editing-workflow` under `~/.codex/skills/` (or `$CODEX_HOME/skills/`) and then delegates external installation to `install_dependencies.py`. It refuses to overwrite an unrelated existing path.

## Create or select a project

Create one project for every independent video. Continue an existing project for corrections, supplemental footage, subtitle changes, or new versions of the same video.

If a new project is needed, run:

```bash
python3 .agents/skills/video-production-bootstrap/scripts/create_video_project.py --name "<项目名称>"
```

Use `--dry-run` when the user only wants to inspect the planned structure. Abort if the target already exists; never merge projects automatically.

For an existing project, require a unique directory containing `project.json`. Prefer the path explicitly supplied by the user. If the project cannot be uniquely identified, ask before reading media.

## Runtime scope

After selecting the project:

1. Read its `project.json`.
2. Follow `workflow.json` `runtime.read_order`.
3. Treat everything under `01-原始素材/` as immutable.
4. Write generated files only to the corresponding `02-转录与剪辑决策` through `07-成片` directory.
5. Do not scan another project, the author's ignored personal directories, or an unrelated filesystem path.

The repository root is the local collection folder. Keep old projects, the shared motion library, and finished media in their existing local locations; do not move them outside the collection folder. Runtime work still selects exactly one current project containing `project.json` and does not enumerate other projects or the whole motion library.

## Efficiency helpers

The scripts under `scripts/` are scoped to one explicit current project:

- `create_short_proxy.py` reads one source range and writes a proxy plus a relink manifest. It defaults to dry-run; `--execute` is required to write.
- `batch_extract_frames.py` reads an existing preview and extracts multiple time points in one FFmpeg process. It does not render Remotion and defaults to dry-run.
- `check_render_processes.py` only lists suspected Remotion, FFmpeg, Chromium, and render-Node processes associated with the exact current project path. It is read-only and has no termination mode.

These helpers do not authorize editing, preview rendering, final rendering, process termination, or upload.

## Exclusions

`.gitignore` only controls Git collection. VS Code `files.watcherExclude`/`search.exclude` and the generated project's Remotion `Config.overrideWebpackConfig()` `watchOptions.ignored` are the supported watcher exclusions in this repository. Node.js has no universal watcher exclusion; run tools from the selected project's `05-Remotion工程/` and only import explicitly selected motion assets.

An explicit user-supplied external file path may be read for the current project, but do not move, rename, delete, or overwrite that source.

## Motion and screen changes

Follow `skills/video-editing-workflow/SKILL.md`. For the material gap checklist, read the `.docx` Word transcript beside `project.json` and do not open, play, probe, extract, transcribe, or frame-extract the talking-head video. If the Word file is unavailable or ambiguous, request the correct file rather than falling back to video. Only after material review passes should packaging load `effects.json` and write the effect map or storyboard.

- Keep talking-head footage fullscreen for direct narration.
- Move the same talking-head clip into a safe-corner PIP for product names, titles, recordings, screenshots, images, documents, or canvas scenes.
- Put titles, product names, and captions on the main composition, never inside the PIP.
- Make recordings and supporting materials fullscreen and readable.
- Use a semantic transition for every visual-state change; clean jump cuts are allowed only for speech cleanup inside the same state.

`video-shotcraft` comes from `https://github.com/Vincentwei1021/video-shotcraft` at the pinned commit in `dependencies.json`. Treat it as a Skill and shot-recipe library. Validate every selected Gallery card and style, then read the complete recipe and its exact demo TSX. Reuse the motion structure and implementation patterns, but adapt all copy, typography, colors, screenshots, recordings, and people to the current project. Never use Gallery previews as project footage.

## Credentials

- `ELEVENLABS_API_KEY`: optional for video-use word-level transcription.
- `OPENAI_API_KEY`: optional for the bundled OpenAI transcribe Skill.

Ask the user to set keys locally. Never ask them to paste a full key into chat. Prefer existing transcripts before any paid transcription call.

## Approval gates

Treat environment installation, source inventory, paid transcription, fine-cut execution, preview creation, final rendering, and upload as separate permissions. Respect `workflow.json` gates and any narrower project-specific instruction.

“先看小样”, “禁止直接做视频”, and “不允许 render” always block full-video rendering. A successful setup or preview does not authorize final rendering.

## Local-only boundary

This project is local-only by default. Unless the user explicitly requests it, never stage, push, or upload any files. Never publish `视频项目/`, `旧版项目/`, `本地项目/`, `动效库/`, `memory/reference/参考分析缓存/`, media, transcripts, credentials, plugin caches, third-party checkouts, or renders.

Inspect exact staged paths. Never use `git add -A`, `git add .`, or an equivalent broad stage in this repository.
