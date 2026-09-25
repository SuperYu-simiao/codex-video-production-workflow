# Implementation reference

Use only the parts needed by the current project.

## One-decoder scrub loop

```js
const video = document.querySelector('video');
let targetTime = 0;
let raf = 0;
let settleTimer = 0;

function seekLatest() {
  if (!video || video.readyState < 1 || video.seeking) return;
  const frame = 1 / 60;
  const wanted = Math.max(0.001, Math.min(video.duration - 0.04, targetTime));
  if (Math.abs(video.currentTime - wanted) > frame) video.currentTime = wanted;
}

function update() {
  const travel = document.documentElement.scrollHeight - innerHeight;
  const progress = travel > 0 ? scrollY / travel : 0;
  targetTime = progress * video.duration;
  seekLatest();
  clearTimeout(settleTimer);
  settleTimer = setTimeout(seekLatest, 120);
}

addEventListener('scroll', () => {
  cancelAnimationFrame(raf);
  raf = requestAnimationFrame(update);
}, { passive: true });

video.addEventListener('seeked', seekLatest);
video.addEventListener('loadedmetadata', update);
```

For chapter-specific cues, replace `progress * video.duration` with the piecewise mapping from `SKILL.md`.

## Useful media inspection

```sh
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,duration \
  -of default=noprint_wrappers=1 input.mp4
```

## Scrub-friendly MP4

```sh
ffmpeg -i input.mp4 -an -c:v libx264 -pix_fmt yuv420p -preset slow -crf 20 \
  -r 60 -g 6 -keyint_min 6 -sc_threshold 0 -movflags +faststart output.mp4
```

Use the source frame rate instead of 60 when the source is lower. Frequent keyframes increase file size; start here for short hero videos and relax the interval only after measuring.

## Hosting checks

```sh
curl -I https://example.com/video.mp4
curl -I -H 'Range: bytes=0-1023' https://example.com/video.mp4
```

Expect an appropriate `Content-Type`, byte-range support, and `206 Partial Content` for the range request. A cross-origin browser load also needs a suitable `Access-Control-Allow-Origin` header.

## Black-screen checklist

1. Open the media URL directly.
2. Check for `404`, HTML returned as video, wrong MIME type, or blocked CORS.
3. Confirm the browser supports the codec and pixel format.
4. Wait for `loadedmetadata` before calculating time.
5. Clamp seeks below the exact duration.
6. Show a poster/fallback while loading and on error.

## Transition checklist

- Use one ordered cue list.
- Test exact cue boundaries plus a small value before and after each one.
- Test reverse scrolling.
- Derive text, gradient, navigation, and media time from the same story position.
- Avoid persistent classes that are only added on forward scroll and never removed.
