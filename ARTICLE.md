# How one Claude Code session built an Awwwards-style 3D scroll site (and what it taught me)

*Companion article for the [OKO magic skill](https://github.com/gdeoko/oko-magic-skill). Feel free to republish.*

I asked Claude Code to build a promo site "like those cinematic 3D scroll sites from design showcases" for a pet wholesale brand. One session later it shipped a scroll-driven night flight through a 3D world: spline camera, bloom, silhouette "moon theatre" stations, a glowing portal you fly through, an interactive animated fox, game-style HUD, synthesized ambient audio. Live: https://spicy-panther-317.higgsfield.app

Here is everything non-obvious it had to figure out — now baked into a reusable skill.

## 1. Free AI asset generation without any API keys
Hugging Face Spaces expose Gradio APIs. `pip install gradio_client`, then:
```python
from gradio_client import Client
c = Client("mcp-tools/FLUX.1-Krea-dev")
res = c.predict(prompt=..., api_name="/infer")  # returns a local file path
```
Claude generated brand-styled animal art, cut the silhouettes out with numpy flood-fill, and placed them on brand-colored discs — consistent art direction from an inconsistent generator. Spaces die weekly, so the skill says: always probe `view_api()` first, and keep a verified-alive list.

## 2. The CatmullRom gotcha that ruins scroll journeys
Everyone's recipe: put camera positions on a `CatmullRomCurve3`, sample with scroll progress. Nobody tells you: **control points are NOT at uniform parameters**. Chapter 2 at `t=0.4` will NOT be at your second waypoint - text overlays drift off their 3D scenes. Fix: sample the curve densely once, find each control point's actual parameter (argmin distance), then piecewise-remap scroll progress through those anchors. Ten lines, saves hours.

## 3. Bloom eats yellow for breakfast
`UnrealBloomPass` with default-ish strength turns any emissive yellow into a white blob. What worked: strength 0.45-0.55, threshold ~0.8, emissiveIntensity around 1.0, and never use additive-blended billboard sprites as glowing backdrops near the camera — use a vertical `CircleGeometry` with `MeshBasicMaterial` instead. It foreshortens naturally instead of blowing up.

## 4. Scroll-scrubbed video that doesn't stutter
The trick isn't the JS (`gsap.to(video, {currentTime: duration, scrollTrigger:{scrub}})`). It's the encode: `ffmpeg -c:v libx264 -crf 26 -g 4 -movflags +faststart -an` — a keyframe every 4 frames makes `currentTime` seeking buttery. Default GOP sizes make it slideshow-y.

## 5. Rive behind a proxy: only one build works
`@rive-app/canvas` fetches its WASM from a CDN at runtime — it silently fails offline or behind strict proxies. `@rive-app/canvas-single` inlines the WASM (~1.7MB) and just works. Vendor it.

## 6. Claude reviewing its own work is the real unlock
The skill makes self-QA mandatory: Playwright + system Chromium (WebGL works headless via swiftshader), screenshots at multiple scroll positions, real `mouse.wheel` events (smooth-scroll libs ignore programmatic scrollTo), then Claude *looks* at the screenshots and fixes what's wrong. The site above took 4 self-review iterations - blown-out exposure, drifted chapters, unreadable text - all caught and fixed before a human ever saw it.

## 7. Memory that survives ephemeral sessions
Cloud sessions are wiped. The skill keeps an Obsidian-compatible `brain/` vault in git: project memory, session logs, and an "infrastructure gotchas" file that grows with every fight. Next session reads it first and starts smart.

Grab the skill (MIT): **github.com/gdeoko/oko-magic-skill** — one file into `.claude/skills/oko-magic/`.
