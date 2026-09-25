---
name: scroll-video-parallax
description: Build, recreate, debug, optimize, and verify scroll-linked parallax storytelling websites driven by video or extracted frames. Use when a request mentions scroll-controlled video, frame-by-frame scrubbing, room or chapter transitions, door-open page changes, scroll anchors, parallax media, keyframe extraction, black-screen media failures, or scroll performance.
---

# Scroll Video Parallax

Build the smallest reliable scroll-linked experience that preserves the supplied design and media.

## Start by inspecting

1. Inspect the existing project, media paths, framework, route structure, and current scroll implementation before changing files.
2. Reuse the project's component and styling patterns. Do not rebuild a working site or replace its visual direction without a request.
3. Inspect the source video with `ffprobe` when available. Record duration, dimensions, frame rate, codec, pixel format, and keyframe spacing.
4. Identify the narrative events and their exact media times, such as door opening, room arrival, object transformation, or chapter end.

## Choose one renderer

- Prefer one fixed `<video>` element whose `currentTime` follows scroll progress for short H.264 MP4/WebM media that supports byte-range requests.
- Use an extracted image sequence only when exact per-frame control is required or browser seeking remains visibly unstable after media optimization.
- Keep Vimeo or YouTube embeds out of the scrubbing layer. Their iframes are not reliable frame-accurate scroll sources. Use a direct media URL or local asset instead.
- Do not add a second decoder, animation library, or state system when the project already has a working one.

## Map scroll to time

Use one normalized scroll source and one piecewise mapping for the entire story:

```js
const clamp = (n, min, max) => Math.min(max, Math.max(min, n));

function mapStoryTime(position, cues) {
  const max = cues.length - 1;
  const safe = clamp(Number.isFinite(position) ? position : 0, 0, max);
  const chapter = Math.min(max - 1, Math.floor(safe));
  const local = safe - chapter;
  return cues[chapter] + (cues[chapter + 1] - cues[chapter]) * local;
}
```

- Let `position` span `0..chapterCount`; each integer is a room or chapter boundary.
- Store verified event times in one ordered `cues` array. Door openings and page changes must use these same boundaries.
- Derive active page, text state, gradients, and navigation from the same position. Avoid independent scroll listeners with separate thresholds.
- Make the mapping symmetrical so reverse scrolling restores the earlier frame and UI state.
- Leave one assertion covering the important boundary times.

## Seek without stutter

Use one video decoder and keep only the latest requested time:

1. Update normalized scroll position in a passive scroll listener wrapped by `requestAnimationFrame`.
2. Save the newest target time.
3. If the video is already seeking, wait for `seeked`; then seek directly to the newest target.
4. Ignore differences smaller than roughly one source frame.
5. On scroll stop, perform one final exact seek.

Set `muted`, `playsInline`, and a useful `preload` value. Keep the visual layer fixed and move only transform/opacity properties. Do not drive React state for every decorative pixel when CSS custom properties or direct element updates suffice.

## Coordinate page content

- The first room's text is visible on initial load.
- Before a room boundary, its text exits upward while fading.
- The next room's text appears immediately after the boundary, with short staggered per-letter or per-line fades when requested.
- Bind every dark gradient or overlay to its owning page's visibility. Its opacity must return to zero when that page exits in either direction.
- Keep information panels narrow or translucent enough that the background media remains readable.
- Honor `prefers-reduced-motion` with a readable, non-scrubbed fallback.

## Prepare media for the web

- Prefer H.264, `yuv420p`, constant frame rate, `faststart`, and frequent keyframes for MP4 scrubbing.
- Confirm the host returns a correct MIME type, CORS headers when cross-origin, byte ranges, and successful partial-content responses.
- Provide a poster or first-frame fallback so a loading or decoding failure does not become a black screen.
- Keep media outside the code package when the delivery platform has a small upload limit; use stable relative paths or a documented direct URL.

Read [implementation.md](references/implementation.md) when implementing the scrub loop, optimizing media, or diagnosing black screens and mismatched transitions.

## Verify before delivery

1. Run the project's existing lint, test, and production build commands.
2. Serve the production build locally rather than checking only the development server.
3. Scroll slowly and quickly from start to end, then end to start.
4. Confirm every narrative event aligns with its page boundary, including both directions.
5. Confirm initial text is present, outgoing text and gradients disappear, incoming text appears, and the final page contains its intended media.
6. Check desktop and narrow mobile viewports, reduced-motion mode, refresh at a middle scroll position, and direct navigation.
7. Check the browser console and network panel for decode, CORS, range, and missing-asset errors.
8. If motion stutters, measure whether the bottleneck is media seeking, oversized assets, layout/paint work, or too many scroll updates before changing architecture.

Do not claim smoothness from a successful build alone. Verify the rendered interaction.
