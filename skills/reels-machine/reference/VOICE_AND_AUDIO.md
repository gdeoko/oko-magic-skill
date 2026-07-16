# Voice & Audio — production rules (tested)

## VOICE — free, natural, error-free Russian

**Default: `edge-tts` `ru-RU-DmitryNeural` on PLAIN text.** Free (Microsoft neural),
natural male, and — critically — it places Russian stress correctly BY ITSELF.

- **NEVER feed manual stress marks** (`+`, RUAccent output, or U+0301). They BREAK
  pronunciation ("становится китайский язык"). The earlier RUAccent -> edge/Silero
  pipeline was the source of every stress error. Plain text is correct text.
- Numbers: write them as **words** ("девятисот девяноста пяти тысяч рублей"), not digits.
- Generate **per segment** (s1..sN as separate files) — you need per-segment durations
  to drive karaoke timing and cut points.
- Speed: `rate="+6%"` reads a touch brisker for reels without sounding rushed. Tune per voice.

```python
import asyncio, edge_tts
async def one(text, out):
    await edge_tts.Communicate(text, "ru-RU-DmitryNeural", rate="+6%").save(out)
```

### Rejected engines (do not reintroduce without a new brief)
- **Silero** (eugene/aidar): stress errors, "не живой". Rejected.
- **RUAccent -> any TTS**: the accent marks themselves cause the errors. Rejected.
- **XTTS-v2**: dependency hell (torch/coqpit/transformers), output not better. Not worth it.
- **Seed Audio (ByteDance) `seed_audio` / `Vlad`**: Chinese-origin engine, Russian is
  secondary — audible stress errors. Rejected.

### Paid cloud TTS — only if the client explicitly pays for it
ElevenLabs / MiniMax (via Higgsfield `text2speech_v2`) are higher quality but **cost
credits** — treat as paid. Default policy is FREE engines only; do not spend credits on
voice unless the owner approves for that client.

### Self-QC
Run `faster-whisper` (small) over the final mp3 to sanity-check words. Note: small-model
ASR is unreliable for judging *stress* (it transcribes phonemes, garbles at 24kHz) — use
it to catch dropped/wrong WORDS, not to verify stress. Dmitry-on-plain-text is the
guarantee for stress.

## MUSIC (individual per reel)
- Pick a track **individually per reel** (niche/tone/tempo of the script). Do not reuse
  the same bed across reels. Freesound search by the script's mood keywords.
- **Fade in at the start, fade out at the end — no abrupt cut:**
  `afade=t=in:st=0:d=1.3, afade=t=out:st=<end-1.6>:d=1.6`
- **Duck under the VO** with sidechain compression (music is the main, VO the sidechain):
  `[music][vo]sidechaincompress=threshold=0.04:ratio=7:attack=12:release=320:makeup=1`
  (split the VO with `asplit` — it feeds both the sidechain and the final mix).
- Base music volume ~0.15–0.18.

## SFX (varied, logical, full — not one repeated whoosh)
The old failure: the same whoosh on every overlay, clipped into fragments — annoying and
illogical. Rules:
- **Varied**: keep a small library (2 whooshes, riser, impact, tick, pop, check/confirm,
  shimmer, engine, splash, ...) and pick the sound that FITS the action:
  number appears -> tick/pop; price slam -> impact (often preceded by a riser); swipe/cut ->
  whoosh (alternate a/b); checkmark -> confirm; logo reveal -> shimmer; on-screen engine ->
  low engine rumble; water/mud shot -> splash.
- **Logical & full**: play each SFX in full (natural decay); never chop it into a fragment.
  Alternate transition sounds so no two consecutive cuts use the same one.
- Keep an in-repo `USED_SFX` habit: don't lean on one effect every reel.
- Levels: transitions ~0.5, accents 0.4–0.7, ambient beds (engine) ~0.28, all under the VO.

## RHYTHM (cuts & overlays every 3–5s, by meaning)
- Footage cut and overlay changes every **3–5 seconds**, driven by the **meaning of the
  script/text** — one script beat -> one clip + one overlay that fits that beat. Not a
  mechanical metronome.

## Karaoke subtitles (layout that never overflows)
- Group **<=2 words / <=15 chars** per line (long Russian words overflow at 3 words).
- Font ~66px, active word amber (brand) at ~109% scale, bottom `MarginV ~256`, `MarginL/R ~110`.
- Sits below the upper-middle infographic band — no collision.
