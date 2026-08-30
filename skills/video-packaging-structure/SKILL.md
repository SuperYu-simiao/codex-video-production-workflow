---
name: video-packaging-structure
description: "Apply the user's default talking-head and product-video packaging structure before editing: chapter transitions, tool cards, step chains, opening lockups, readable code or prompt displays, and real product-page reveals."
metadata:
  short-description: Default packaging structure before video editing
---

# Default Video Packaging Structure

Use this skill whenever the user asks to design, package, edit, or produce a video in this workflow. It defines the user's preferred structure; it does not authorize editing, material collection, preview rendering, final rendering, upload, or publication.

## Stage Gate

Before editing the source, collecting public screenshots, or writing animation code, read:

- `00-先读我.md`
- `workflow.json`
- `dependencies.json`
- `effects.json`
- `特效与切屏规范.md`
- this skill's [default structure reference](references/default-structure.md)
- this skill's [talking-head layout and transition prompts](references/talking-head-layout-motion.md)
- the current project's `project.json` and `01-原始素材/`

Produce reviewable planning documents in the current project's `04-动效与包装/`:

1. `包装方案-<slug>.md`
2. `需要补录的操作素材-<slug>.md`
3. `工具官网-GitHub截图素材表-<slug>.md`
4. `特效映射-<slug>.json`

The documents must state the current approval stage and explicitly say whether editing, public-asset capture, preview, and rendering are authorized. Keep source media immutable. If the user has not approved the next stage, stop after the documents.

The packaging plan must include a `人物构图与转场轨` for every segment: talking-head state, crop ratio, screen position, width, whether gestures remain visible, supporting-material state, entry/exit transition, stable reading time, and caption-safe area. Do not leave the person in one fixed composition for the whole video when the script has clear semantic state changes.

## Visual Style Routing

Before choosing colors, stage geometry, type, materials, or motion density, read `视觉规范与参考/风格库索引.md` and the complete entry for the style selected by the user when those local files are available. In a clean clone, use `references/style-library-2-public-baseline.md` as the portable fallback. A style library is the visual system; Shotcraft cards supply motion grammar. Do not replace the selected style with a generic dark-tech skin merely because the requested cards came from Shotcraft.

When the user selects `风格库2` and the private/local style files exist, read both:

- `视觉规范与参考/风格库2.MD`
- `视觉规范与参考/风格库2-video-shotcraft特效映射.md`

Use its low-contrast black perspective-grid stage, one conceptual metaphor per segment, real webpage/document evidence, restrained glitch, and fast-versus-review motion contrast as the visual base. When the user asks to continue the approved Episode 5 opening language or says “按第五期那个开头”, also read [the Episode 5 opening baseline](references/episode5-opening-baseline.md) before planning or implementation.

When those local files are not present, use [the portable Style Library 2 baseline](references/style-library-2-public-baseline.md) and keep the same visual principles without requiring private references.

## Production Responsibility Chain

Keep these responsibilities separate and make the handoff explicit in the project artifacts:

1. **`video-use` directs the edit.** It owns the confirmed transcript, phrase/word timing, source-video timebase, caption cues, media states, speaker layout, insertions, and the mapping from source time to master time.
2. **`video-shotcraft` supplies calibrated motion.** For every selected card, validate the Gallery card and `style-key`, read the complete card and exact demo TSX, then adapt that implementation. A card name is not an implementation specification.
3. **Remotion composes the approved tracks.** Build separate source-video, speaker/matte, background, effect, material, caption, music, and SFX tracks. Remotion does not decide the editorial timing or invent substitute on-screen copy.

Before writing animation code, create or update `02-转录与剪辑决策/导演时间线-<slug>.json` using [the director timeline schema](references/director-timeline-schema.json). It records `fps`, timing basis/confidence, transcript cue, source in/out, master in/out, visual state, speaker state, material, card/style/demo, caption region, audio behavior, and every inserted duration. Proportional transcript estimates may support planning, but they cannot drive an implementation preview; align the approved preview range to the actual speech or audio first.

For an inserted pause or bridge, split the source-video track around the insertion. Resume from the same source frame after the inserted segment and apply one shared `source -> master` mapping to all later captions, materials, effects, and recordings. Muting or covering a continuously advancing source video is not a pause.

## Default Cue Rules

These are defaults when the matching semantic cue exists. Do not force a card into a shot that has no matching cue.

1. **Small chapter-title transitions:** use `aurora-bloom-bg-flip`. Put the new title after the light-to-dark flip, leave a readable hold, and do not stack another primary transition on the same beat.
2. **Tool or Skill names:** use `assemble-then-type-flyin`. Put the real public landing-page screenshot, GitHub repository home, or official logo in the right frame. First occurrence may fully assemble; repeated mentions should reuse or briefly recall the established card unless the spoken cue introduces new evidence. Never use a logged-in or private page as an identity card.
3. **Step names:** use `autolayout-gap-dial` to connect the named steps. Derive the labels and any numeric relationship from the actual script; keep each step readable and let the chain settle before the next operation.
4. **Opening proposition lockup:** for the opening's concluding sentence or key promise, use `logo-shrink-wordmark-lockup` full-screen with the real product trademark or approved wordmark. Then hold or pause the talking-head bridge and use `card-flock-tumble` as the energetic handoff, with a rights-cleared music bridge and the real product mark. The lockup card is being adapted from its outro role; preserve its core motion and do not invent a trademark.

## Optional Opening Layers

Use only when the first seconds have enough semantic and timing room; these layers are not a checklist:

- `graze-face-tour`: first product-name mention, with a real public product-page screenshot as the UI surface.
- `gradient-word-sweep`: transparent/masked overlay over the person so the face remains visible; use only after the preview proves the demo background is not an opaque rectangle.
- `neon-triple-marquee`: transparent or masked layer behind the person and in front of the room background. Default words: `人物、字幕、信息、画面和这些动效`.
- `flying-words`: transparent or masked keyword layer behind the person. Keep it subordinate to the face and subtitles.

The three background-layer cards are written for specific dark-background demos. Lowering opacity does not make an opaque demo transparent. If the exact implementation cannot provide alpha, isolate the motion in code or with a mask and verify it in a preview before using it.

## Copyable Text and Product Pages

- When the script supplies an exact prompt, code block, command, configuration, or other text the viewer may copy, use `document-typewriter-reveal`. Preserve the supplied text verbatim, paginate semantically, keep the type readable, and keep captions outside the document.
- When showing a real product website or UI, use `runway-ground-skim` for a card-group drop-and-settle reveal or `skeleton-reveal` for a sketch-to-skeleton-to-real-content reveal. Choose one primary motion per shot, use real screenshots or recordings, and stop camera motion while the UI is being read.

## Shotcraft Verification

For every selected card, validate the exact card name and `style-key` in the installed Shotcraft Gallery, read the complete card, and read the exact demo TSX named by its reference implementation. Adapt copy, colors, typography, screenshot, recording, and logo to the current project. Do not treat a Gallery poster or preview as project footage.

If a previously approved project component already implements the requested visual language, use it as the baseline and preserve its calibrated motion before making content-specific adaptations. Do not collapse an approved multi-component opening into one newly invented TSX file. Record the baseline component paths and which parameters/content were changed.

## Safety and Readability

- Official identity screenshots must be public, non-login pages; record URL, date, and source scope.
- Do not expose keys, tokens, accounts, private paths, customer data, real invoices, or unapproved project names.
- Product screenshots, recordings, documents, and tables take the main canvas. Move the talking head to a stable safe-corner PIP or hide it when dense content requires it.
- Vary the talking-head crop and position only at semantic state changes. Reuse the same source clip and continuous audio while animating crop, mask, scale, position, and layer order; do not manufacture continuity by restarting the speaker clip.
- Captions stay on the main composition and avoid the face, PIP, controls, tables, and copyable text.
- After a primary motion, leave a stable reading hold. Do not add continuous decorative motion during evidence or reading beats.
- On-screen titles and captions must come from the transcript or approved content. Director notes such as “这里展示步骤” or “给工具名证据” belong in planning files and must never appear as audience-facing copy.
- A user-facing visual-quality preview must read the full-resolution source and render at the review resolution. A low-resolution proxy is allowed for timing/debug checks only and must be labelled as such; do not ask the user to judge face clarity, type, masks, or final styling from a double-encoded proxy.
