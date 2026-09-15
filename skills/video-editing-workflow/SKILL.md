---
name: video-editing-workflow
description: "Turn a rough talking-head video into a transcript-aligned, motion-packaged Remotion edit with video-use, video-shotcraft, and reproducible QA. Use for complete video editing, captions, screen recordings, packaging plans, previews, and final delivery."
metadata:
  short-description: "Complete talking-head editing workflow"
---

# Complete Video Editing Workflow

Use this as the single entry point for a full talking-head or AI/product explainer edit. It coordinates the repository workflow with the external `video-use` and `video-shotcraft` Skills and the Remotion runtime. It does not replace those tools or invent editorial timing.

## Start here

Read the repository files in this order:

1. Resolve this Skill's real repository root, then read `workflow.json` from that same root. Do not mix rules from another worktree named in an old project file.
2. For the supplementary-material stage, read `project.json`, then the `.docx` transcript beside it and the existing inventory. Do not open or analyze the talking-head video at this stage.
3. Read `00-先读我.md` and `dependencies.json` only for setup.
4. Read `effects.json`, `特效与切屏规范.md`, the packaging Skill and visual references only after material readiness permits packaging.

Select exactly one project containing `project.json`. Keep `01-原始素材/` immutable and write generated work only to the project's `02` through `07` stage directories.

## Responsibility chain

Keep the handoff explicit:

- **`video-use` directs the edit.** It inventories media, transcribes, removes unusable speech, corrects terminology, creates captions, marks semantic cues, and owns source time, source-to-master mapping, speaker layout, and insertions.
- **`video-shotcraft` supplies calibrated motion.** Validate every chosen card and `style-key` in the Gallery, read the complete card, then read the exact referenced demo TSX. Adapt copy and assets without replacing the calibrated motion with a name-only approximation.
- **Remotion composes approved tracks.** Keep source video, continuous speech audio, speaker/matte, background, material, effect, caption, music, and SFX tracks separate. Remotion follows the director timeline; it does not decide the cut or create unapproved audience copy.

## Production stages

### 1. Inventory and transcript

For the initial supplementary-material pass, use the Word transcript placed beside `project.json`. Ignore `~$*.docx`. If several valid Word files exist, use a `project.json` registration, then a unique title match; if still ambiguous, ask the user. If the Word file is missing or unreadable, stop this stage and request it instead of opening the video.

During this pass, do not open, play, probe, extract audio from, frame-extract, transcribe, or use a proxy of the talking-head video. Inventory other assets by filenames and existing ledgers. Label the checklist `定位依据：Word逐字稿` and `时间码状态：未对音频核验`. Source dimensions, frame rate, duration, audio streams, word timing, and audiovisual checks belong to the later authorized production stage.

Run the repository subtitle check before using an SRT:

```bash
python3 .agents/skills/video-production-bootstrap/scripts/validate_subtitles.py \
  --srt '/absolute/path/to/captions.srt'
```

The check must pass for positive durations, monotonic cues, no overlaps, valid UTF-8, and no out-of-order blocks. It is a structural check, not a substitute for listening to the speech.

### 2. Material gap and collection pass

Use the Word transcript semantics and inventory to write the supplementary-recording checklist and collection ledger first. Do not design shots, select effects, assign speaker layouts, or estimate final-screen timing. For an explicitly started collection task, follow the user's current standing authorization to save public stills, logos, official website and GitHub screenshots with provenance. Give the user links and exact recording instructions for dynamic pages and real operations. A narrower current request overrides the standing authorization.

### 3. Material review

Re-inventory all relevant media after collection. Proceed only when required evidence is ready or the user explicitly accepts a missing item and an honest alternative. Record unresolved items and accepted exceptions in `material_readiness`; waiting for a reply never counts as acceptance.

### 4. Packaging and director plan

Now load the packaging and visual references and produce one consistent version of the package plan, updated gap list, public asset table and effect map. Mark `已锁定` only after user confirmation. Align real speech before implementation, then create the director timeline from that audio rather than estimated proportional timing.

Write these artifacts in `04-动效与包装/`: `包装方案-<slug>.md`, `需要补录的操作素材-<slug>.md`, `工具官网-GitHub截图素材表-<slug>.md`, and `特效映射-<slug>.json`. Write `02-转录与剪辑决策/导演时间线-<slug>.json` once real audio timing is available. Each segment records the spoken cue, source/master frames, visual and speaker states, crop, material, verified card/style/demo paths, caption region, audio behavior, stable reading time, and editor-only notes. Notes never become viewer copy.

Use the selected local style library when it exists. Otherwise use `skills/video-packaging-structure/references/style-library-2-public-baseline.md` as the portable baseline.

### 5. Editorial and caption pass

Use `video-use` to preserve meaning while removing harmful silence, repeated starts, filler-heavy dead air, and mistakes. Keep intentional emphasis. Produce:

- a fine-cut media file that does not overwrite the source;
- an SRT or VTT plus a machine-readable cue file;
- an edit decision list with source in/out frames;
- a terminology correction record when ASR needs repair.

Captions belong to the main composition, use at most two lines, and avoid faces, hands, PIP windows, buttons, tables, and copyable code. After any cut or insertion, regenerate or remap caption cues from the approved timeline.

### 6. Motion and layout

Bind movement to sentence meaning, not fixed intervals. The default semantic mapping is:

- small chapter title: `aurora-bloom-bg-flip`;
- first tool or Skill name: `assemble-then-type-flyin`, with a public landing page, GitHub home, or official logo in the side frame;
- named procedural steps: `autolayout-gap-dial`;
- copyable prompt, command, configuration, or exact long text: `document-typewriter-reveal`;
- opening proposition followed by a real pause/bridge: `card-flock-tumble` with approved music;
- optional opening layers: `graze-face-tour`, transparent/masked `gradient-word-sweep`, and transparent/masked `neon-triple-marquee` behind the person.

When a screen recording, webpage, document, or screenshot is the main visual, move the same continuous talking-head clip into a stable safe-corner PIP. For a square PIP, crop by face and torso center rather than geometric center; keep eyes, mouth, chin, and necessary gestures inside the frame. Animate fullscreen-to-PIP over roughly 12–20 frames at 30fps, then hold the composition while the evidence is read.

Every visual-state change gets one semantic transition. Do not stack primary transitions or keep high-energy motion running over a dense reading section. Aim for a meaningful change about every two or three spoken sentences, while allowing a stable hold when the viewer needs to read.

### 7. Pause and timebase invariant

An inserted bridge is a real timeline insertion. Split the source-video track at `source_at_frame`, pause source audio, place the independent bridge visual/music, then resume from the same source frame. Apply one shared `source -> master` mapping to every later caption, material, recording, and effect. Muting a continuously advancing source clip and covering it with a freeze frame is not a pause.

### 8. Preview and approval

Make a full-resolution representative preview before a full render. Cover the opening, first tool card, first recording, square speaker PIP, densest reading scene, a pause bridge, and the ending. Extract representative frames from the existing preview with `batch_extract_frames.py`. Check:

- caption alignment and corrected terminology;
- centered speaker crop and safe areas;
- readable recordings, documents, and public identity evidence;
- transition entry/hold/exit and pause resume point;
- layer order: background, behind-person effects, person, materials, captions;
- no private paths, accounts, keys, tokens, or notifications.

Preview approval allows expansion to the full review version; it does not authorize final rendering or upload.

### 9. Final delivery QA

After explicit final-render approval, render into `07-成片/` and keep a QA report beside the output. Verify with typecheck, full decode, `ffprobe`, black-frame detection, subtitle structure, duration/frame count, audio sample rate/channels/loudness, and BT.709 limited-range delivery (`yuv420p`, `tv`, `bt709` where the target requires it). If BGM is configurable, render both the BGM version and the no-BGM version with identical video-track hashes. Never publish or upload without a separate destination approval.

## Reusable prompts

Start a complete run with:

```text
请使用 $video-editing-workflow，读取当前项目的 project.json 和 01-原始素材/。
按 video-use → video-shotcraft → Remotion 的职责链工作。
先读取项目根目录与 project.json 同级的 Word 逐字稿，再盘点现有素材并输出补录清单和素材收集台账；这一步禁止读取或分析口播视频，不设计包装或选特效。
按已授权范围保存公开静态素材；动态页面给我链接和录法，由我录制。
素材整理好后再统一设计包装；小样和渲染仍按阶段授权。
```

For a later approved preview:

```text
包装方案和开头视觉基线已确认。只制作指定范围的全分辨率审核小样，
保持已确认的组件和字幕规则，检查代表帧与 source-to-master 补偿，
不要写入 07-成片/，不要上传。
```

## Safety and scope

Installation, media inventory, transcription, editing, preview rendering, final rendering, process termination, and upload have separate scopes. Public screenshot collection follows the current user's established authorization and any narrower instruction in the active task. Never read or commit credentials, raw talking-head footage, private recordings, private transcripts, renders, review frames, plugin caches, or unrelated projects. Do not use `git add -A` or `git add .` in this repository.

The portable installation entry point is:

```bash
python3 .agents/skills/video-production-bootstrap/scripts/install_workflow.py --all
```

It installs this repository's unified Skill and then the pinned external Skills after explicit authorization. It refuses to overwrite an existing unrelated destination.
