# Portable Style Library 2 Baseline

This is the public, reusable version of the Style Library 2 decisions used by the talking-head packaging workflow. It describes visual mechanisms, not any private project, source media, account, or personal reference file.

## Visual system

- Stage: a low-contrast black and gray perspective grid. Keep it quiet enough for captions and real product evidence.
- Concept: one conceptual metaphor per segment. The metaphor should explain the spoken idea rather than decorate every sentence.
- Evidence: real public landing pages, GitHub repository homes, product recordings, documents, and result images take priority over invented UI.
- Motion contrast: use fast, high-energy movement for hooks and state changes, then stop the camera for reading and explanation.
- Glitch: restrained and short. Never cover a face, caption, table, code, or product identity with continuous distortion.

## Talking-head language

- Start with a clean fullscreen speaker state for the hook and personal opinion.
- Reframe the same continuous clip into a 4:5 or 9:16 side column for steps and explanation, preserving eyes and meaningful gestures.
- Use a 1:1 safe-corner PIP for real recordings and screenshots. Center the crop on the person's face and torso, not on the source canvas.
- Hide the speaker only when a dense document or concept visual needs the full canvas; bring the speaker back for the next complete sentence.
- Keep captions on the main composition and reserve an independent bottom-safe band.

## Motion grammar

Use the Shotcraft card that matches the cue, then read its exact card and demo implementation:

| Cue | Card | Role |
|---|---|---|
| Chapter or small title | `aurora-bloom-bg-flip` | Reframe into a readable title hold |
| Tool or Skill identity | `assemble-then-type-flyin` | Assemble the card and reveal the verified name |
| Named process steps | `autolayout-gap-dial` | Connect and settle each step |
| Opening pause/bridge | `card-flock-tumble` | Hold the speaker and bridge with an approved music/SFX layer |
| Real public page evidence | `runway-ground-skim` or `skeleton-reveal` | Introduce a real page, then stop for reading |

Optional opening layers such as `gradient-word-sweep` and `neon-triple-marquee` must provide real alpha or an explicit mask. Lowering opacity on an opaque demo does not make it transparent.

## Review standard

Every state change should be explainable by the spoken sentence. After a primary motion, leave a stable reading hold. Review representative frames at the final composition resolution and verify that the person, captions, evidence, and public identity sources remain readable and correctly layered.
