---
name: video-packaging-structure
description: "Design and lock a material-aware talking-head packaging plan after recordings and public assets are ready."
metadata:
  short-description: Packaging design after material readiness
---

# Material-aware Video Packaging

This Skill starts only after `skills/video-editing-workflow/SKILL.md` material review passes. During inventory and collection, produce only the supplementary-recording checklist and collection ledger. Do not design shots early.

Resolve the real repository root and read from that same root: `skills/video-editing-workflow/SKILL.md`, `workflow.json`, `effects.json`, `特效与切屏规范.md`, `references/default-structure.md` and `references/talking-head-layout-motion.md`. Read the selected project's `project.json`, current ledger and collected inputs. Do not mix rules from an old worktree path.

When selected, read the complete local style entry. For 风格库2, read both local entries; use the portable baseline only when they are absent. Read `memory/reference/AI剪辑参考会话沉淀.md` when reusing the approved reference language. Its counts and frames are historical evidence, not a quota. Read `episode5-opening-baseline.md` only when that opening structure applies.

## Output and lock

After required material is ready, or the user explicitly accepts unresolved items and an honest alternative, re-inventory all relevant input. Check usable ranges, meaning, quality, source/rights and redaction. Produce one consistent version of:

1. `包装方案-<slug>.md`
2. `需要补录的操作素材-<slug>.md`, with every item `完成`, `缺失` or `不可用`
3. `工具官网-GitHub截图素材表-<slug>.md`
4. `特效映射-<slug>.json`

All four identify the same inventory basis and version. Mark `已锁定` only after user confirmation; otherwise use `待锁定`. A lock does not authorize editing, animation, preview, rendering or upload.

For every segment record the spoken cue; timing basis; material ID/path and usable range; visual and speaker states; face/torso crop, position and gestures; entry, primary action, reading hold and exit; caption region; audio behavior; card/style/demo. Keep scene IDs stable. If speech is not aligned, leave source/master fields empty and set `implementation_ready=false`.

## Motion and evidence

Bind movement to spoken meaning and available evidence. Use one primary motion per shot and leave a stable hold. Real recordings, documents and screenshots take the main canvas; move the same continuous presenter to a face-centered safe PIP or hide it when needed. Captions remain on the main composition.

Semantic candidates include `aurora-bloom-bg-flip` for chapters, `assemble-then-type-flyin` for first tool identity, `autolayout-gap-dial` for named steps, `document-typewriter-reveal` for supplied copyable text and a true `card-flock-tumble` pause bridge. Do not force them or repeat full identity builds.

For every selected Shotcraft card, validate the Gallery, read the full card and exact demo TSX, then adapt copy, typography, color and assets. Prefer an approved component. Record original reference, local adaptation or verified runtime import/call; a name or read receipt is not execution proof.

## Production handoff

After packaging is locked and the relevant action is authorized, `video-use` owns actual speech timing, edits, captions, source/master mapping and director timeline; Shotcraft supplies calibrated motion; Remotion composes independent tracks.

An inserted bridge splits and holds source video/audio, resumes from the same source frame and applies one mapping to every later track. Director notes never become viewer copy. Full-resolution visual previews use original-quality sources. Preview, final render and upload remain separate gates.
