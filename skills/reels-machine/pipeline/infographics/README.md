# Code-drawn animated infographics (HTML/SVG/CSS -> transparent PNG frames)

Beautiful, on-brand infographics animated in code and rendered to transparent
frame sequences, then overlaid on the reel. This is the preferred way to add
infographics (per DIVERSITY_LAWS: "больше инфографики нарисованной кодом,
анимационной"). Zero static: every insert moves.

## How it works

Each template exposes a global `window.render(t)` where `t` goes 0..1 across the
clip. `capture.js` drives it deterministically — no wall-clock, no `requestAnimationFrame` —
so the output is frame-exact and reproducible.

```bash
# render N frames (= round(segment_seconds * 30)) to transparent PNGs
node capture.js "$PWD/html/price.html" 230 frames/price
# encode to a small lossless-alpha MOV (RLE compresses the transparent areas)
ffmpeg -y -framerate 30 -i frames/price/f%03d.png -c:v qtrle -pix_fmt argb price.mov
# overlay on the base video at the beat's start time (itsoffset), hold base after it ends
ffmpeg -y -i base.mp4 -itsoffset 20.66 -i price.mov \
  -filter_complex "[0:v][1:v]overlay=0:0:eof_action=pass:format=auto[v]" \
  -map "[v]" -c:v libx264 -crf 20 out.mp4
```

Chain several overlays in one `-filter_complex` (one encode) to avoid re-encode
generation loss.

## Environment notes (this cloud)

- Playwright's bundled browser version can mismatch `/opt/pw-browsers`. `capture.js`
  pins `executablePath` to the installed Chromium (`/opt/pw-browsers/chromium-<v>/chrome-linux/chrome`).
  Update the version if the path changes.
- Fonts are loaded from `../../../fonts/` (the skill's `fonts/` dir). `capture.js`
  waits on `document.fonts.ready` before the first frame.
- Screenshot with `omitBackground:true` for straight alpha.
- ProRes 4444 is huge (~100MB/6s); use `qtrle`/`argb` for intermediates — transparent
  regions RLE-compress well. The final reel is H.264 regardless.

## Templates (all 1080x1920, content in a face-safe zone)

- `spec.html`   — engine gauge: number counts up, SVG arc sweeps, spec chips stagger in.
- `susp.html`   — suspension physics: wheels roll over a scrolling bumpy terrain while the
                  chassis bar stays perfectly level (visualises "гасит тряску").
- `price.html`  — price count-up in a glowing pill + a process tracker (node lights up per step);
                  includes a soft radial scrim (darkens the video for contrast, not a rectangle card).
- `check.html`  — "уже в цене" checklist: rows with brand icons tick in one by one.

Each is a *starting point*: per DIVERSITY_LAWS, rewrite the numbers/metaphor/copy for
every reel — never just swap digits on the previous graphic. Vary the FORM (panel /
center pill / left card) so consecutive inserts don't repeat.

## Layout contract (avoids collisions)

- Infographic cards live in the upper-middle band (y ~ 560..1280).
- Karaoke subtitles sit at the bottom (ASS `MarginV ~256`, `Alignment 2`).
- Keep faces unobstructed; darken video under text via scrim/eq, never a flat plate.
