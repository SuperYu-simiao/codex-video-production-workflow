---
name: chatcut
description: Prepare editable fine-cut handoff plans for ChatCut or a manual video editor after an automated video draft exists. Use when the user asks for ChatCut, 可编辑精修, 精剪, 细修, 手动精修, editable cut, reviewable edit plan, or when a tech video needs human-adjustable timing for TechIntro, KineticTitle, DataStream, UiPanel, SceneTransition, captions, or talking-head cuts.
---

# ChatCut

## Overview

Convert a rough video edit or generated Remotion/video-use plan into a precise, editable refinement brief. Focus on timecoded changes that a human editor or ChatCut-style tool can adjust without rebuilding the whole video.

## Workflow

1. Start only after there is a draft, rough cut, EDL, transcript, SRT, or rendered preview.
2. Inspect the edit for timing, readability, caption placement, transition smoothness, audio balance, and places where graphics distract from speech.
3. Produce timecoded refinement instructions. Keep each note actionable: trim, extend, replace, move, fade, reduce, brighten, recolor, retime, or swap.
4. Preserve edit intent. Do not rewrite the creative concept unless the user asks for a new direction.
5. Flag decisions requiring user taste: music style, aggressive glitch level, brand colors, face-retouching, claim wording, and legal/factual text.

## Refinement Categories

- Cut timing: pauses, breath trims, jump cuts, section openings, ending snap.
- Text motion: KineticTitle duration, emphasis words, pop timing, safe margins, contrast.
- Tech layers: DataStream opacity, particle density, UI panel legibility, scanline strength.
- Transitions: glitch length, scan speed, flash intensity, push/pull direction, audio hit sync.
- Captions: line breaks, timing offsets, technical term spelling, overlap with UI/speaker.
- Finish: color consistency, loudness, SFX/music ducking, export notes.

## Output Format

Use a table:

| Timecode | Layer/Track | Issue | Edit Instruction | Priority |
| --- | --- | --- | --- | --- |

Then include:

- Global fixes: color/audio/caption rules that apply throughout.
- Keep as-is: strong moments that should not be disturbed.
- Needs user call: unresolved creative or factual decisions.

## Coordination

If no rough cut exists, use AI Visual Director and video-use first. If the user asks for actual rendered motion graphics, use Remotion before or alongside this handoff.
