# MONTAGE_CAPABILITIES — извлечено из OpenMontage (calesthio/OpenMontage)

Полный разбор возможностей открытой системы OpenMontage (39k⭐, **AGPL-3.0**) и что из
этого забираем в наш скилл. **Важно про лицензию:** AGPL-3.0 — копилефт. Мы забираем
ИДЕИ, ТЕХНИКИ и АРХИТЕКТУРНЫЕ ПРИЁМЫ (они не защищены копирайтом) и реализуем их СВОИМ
кодом. Их .py-исходники в наши репозитории НЕ вносим, иначе репозиторий станет обязан
открыться под AGPL. Этот файл — карта возможностей и план внедрения, а не их код.

## 0. Архитектура (что перенять концептуально)
Три слоя знания:
- **Layer 1 — инструменты** (`tools/tool_registry.py`): «что существует» + стоимость/провайдер/раннтайм.
- **Layer 2 — скиллы-режиссёры** (`skills/`): «как это применять» по стадиям пайплайна.
- **Layer 3 — вендорские скиллы** (`.agents/skills/*.md`, 60+): глубина по каждому провайдеру/движку.
Пайплайн-стейт-машина: `idea → script → scene_plan → assets → edit → compose → publish`,
на каждой стадии свой director-скилл, чекпоинт и (опц.) человеческое подтверждение.
Наш вывод: у нас уже есть эквивалент (reels-machine SKILL.md), но стоит перенять
**реестр возможностей + чекпоинты + decision_log** для автономного цикла.

## 1. Инструменты (tools/) — карта и наши эквиваленты
| Возможность | Их провайдеры | Free/Paid | У НАС |
|---|---|---|---|
| TTS | ElevenLabs, GoogleTTS, OpenAI, **Piper (free/local)** | смешанно | edge-tts Dmitry (free) ✓ — лучше для RU |
| Image gen | FLUX, Imagen, GPTImage, Recraft | paid/free | Pollinations FLUX (free), Higgsfield (paid) ✓ |
| Video gen | Kling, Seedance 2.0, Gemini Omni, LTX2 | paid | Higgsfield (paid), сток Pexels ✓ |
| Music | MusicGen | paid | Freesound (free) ✓ |
| Transcribe | **Whisper (offline)**, Azure STT | free/paid | faster-whisper ✓ — но не для таймингов слов (GAP, см. §7) |
| Compose | VideoCompose → FFmpeg / Remotion / HyperFrames | free | ffmpeg + Playwright(HTML/CSS) ✓ |
| Audio mix | AudioMixer (crossfade) | free | ffmpeg amix+sidechain ✓ |
| Subtitles | **SubtitleGen** (.srt из транскрипта+таймингов) | free | наш kinetic HTML ✓ |
| Avatar/lip-sync | HeyGen, FaceSwap, VideoTranslate | paid | — (GAP, редко нужно) |
| Character anim | SVG-риги, pose-библиотеки (Ink Puppet) | free | — (GAP, см. §8) |

## 2. Пайплайны (pipeline_defs/*.yaml) — 12 шаблонов
talking-head, animated-explainer, screen-demo, **clip-factory** (короткий формат пачкой),
podcast-repurpose, cinematic, animation, character-animation, hybrid, avatar-spokesperson,
localization-dub, framework-smoke. Нам ближе всего **clip-factory** (наш контент-завод) и
**cinematic**. Идея: описывать каждый тип ролика как YAML-манифест со стадиями — упорядочит
масштабирование до 500 роликов.

## 3. Скиллы-техники (skills/) — что перенять
- `skills/meta/taste-direction.md` — «читать дизайн-референс и задавать визуальный подход».
- `skills/meta/reviewer.md` — самопроверка ролика (≤2 раунда) перед выдачей.
- `skills/meta/video-reference-analyst.md` — анализ референс-видео (у нас = разбор конкурентов от 1M).
- `skills/meta/animation-runtime-selector.md` — выбор Remotion/GSAP/Lottie/Manim/D3 под задачу.
- `skills/meta/bespoke-composition.md` — ручная «ателье»-композиция под сложные сцены.
- `skills/pipelines/<p>/edit-director.md` — монтажные решения: бит-мэппинг, тайминг склеек.

## 4. Ремоушн-компоненты (remotion-composer/src/components/) — идеи для наших HTML-оверлеев
TextCard, **StatCard**, **ProgressBar**, **CalloutBox**, **ComparisonCard**, charts/.
У нас уже есть аналоги в `pipeline/infographics/`. Добавить в нашу библиотеку:
ComparisonCard (до/после) и ProgressBar как отдельные шаблоны.

## 5. Субтитры/заголовки — их правила стайлинга (совпадают с нашим выводом)
Их контракт прямо запрещает «дешёвый» вид:
- **НЕ использовать обводку (outline) на тексте** — только dropshadow или полупрозрачная подложка.
- НЕ системные шрифты — явно задавать font-weight/letter-spacing/line-height.
- НЕ статичные субтитры — анимация: fade-in в начале сцены, уход перед следующей.
- Word-by-word — через spring-физику (framer-motion) или GSAP SplitText (stagger reveal).
- Позиция — нижние 20% кадра, поля 10% по бокам.
- Иерархия: hero-заголовки 48–72px bold; секции 32–48px; субтитры 18–24px.
**Наш итог (внедрено):** kinetic HTML-субтитры БЕЗ обводки (мягкая тень), Soyuz Grotesk +
Montserrat, активное слово амбер-текст/амбер-плашка, read-ahead dimming; либо чистые
анимационные ЗАГОЛОВКИ на сценах (mask-reveal), один шрифт, без рамок.

## 6. Пейсинг (правила ритма — берём в наш чеклист)
- Соц-клипы (TikTok/Reels): жёсткая склейка каждые **1–3 сек**, музыка ведёт пейсинг.
- Explainer: 1 сцена / 4–8 сек; образовательное: 6–10 сек; трейлер: 0.5–2 сек.
- Склейки привязывать к битам музыки/голосу; субтитры менять на склейке или на бите,
  не посреди фразы. (У нас правило 3–5 сек — уточнить: для динамичных беров можно 1–3 сек.)

## 7. Governance — что стоит внедрить нам (реально полезно для автономности)
- **cost_tracker** (estimate → reserve → reconcile) + порог на действие + жёсткий cap трат.
  Нам критично, чтобы автономный цикл не жёг кредиты Higgsfield/Gemini.
- **decision_log**: логировать выбор провайдера/голоса/приёма с причиной; при смене —
  до-логировать. Прозрачность для Даниэля.
- **reviewer/self-review** перед выдачей: чеклист (ноль статики, лицо не перекрыто,
  тайминг субтитров, громкости, длительность).
- **schemas/artifacts**: brief/script/scene_plan/asset_manifest/edit_decisions/render_report —
  形ализовать наши промежуточные артефакты (упростит масштаб и дебаг).

## 8. GAPs — чего у нас нет и стоит добавить
1. **Точный пословный тайминг субтитров** — их `SubtitleGen` берёт тайминги из транскрипта
   (WhisperX word-level). У нас — пропорциональная оценка. **ADOPT:** прогонять итоговую
   озвучку через faster-whisper с `word_timestamps=True` и брать реальные тайминги слов.
2. **Больше бесплатных источников кадров** — у них Archive.org / NASA / Wikimedia Commons.
   **ADOPT:** добавить их в fetch как доп. источники (шире пул, лучше дедуп/разнообразие).
3. **Character animation (SVG-риги, pose-библиотеки, Ink Puppet)** — рисованный персонаж-маскот.
   Потенциально ценно для бренд-разнообразия. Реализуем своим кодом при необходимости.
4. **Runtime-selector анимаций** — формальный выбор Remotion/GSAP/Lottie/Manim/D3 под задачу.
5. **Slideshow-risk gate** — числовая проверка «не превратилось ли в слайдшоу» (наш «ноль статики»).
6. **ComparisonCard / ProgressBar** как готовые code-инфографики.

## 9. Установка «во все чаты» — как это работает у них и у нас
У OpenMontage НЕТ авто-инсталла: скиллы — это markdown, которые агент просто ЧИТАЕТ
(`skills/`, `.agents/skills/`), а инструменты — Python-классы, импортируемые в рантайме.
«Загрузка скилла» = агент прочитал файл. Платформенные файлы (CLAUDE.md, CURSOR.md,
COPILOT.md, CODEX.md, .windsurfrules) — статические справки под каждого ассистента.
**Для нас:** держать наши скиллы в `gdeoko/oko-magic-skill` (грузятся в наших сессиях).
Вносить AGPL-код OpenMontage в наши репозитории НЕ следует; берём техники (этот файл) и
реализуем сами. Если нужен именно их код — держать OpenMontage отдельным клоном-референсом.

## 10. ADOPT NOW (приоритет)
1. WhisperX/faster-whisper **word-level тайминги** → точные субтитры/заголовки.
2. **Archive.org + Wikimedia Commons** в источники кадров.
3. **Budget-cap + decision_log** в автономный цикл (не жечь кредиты).
4. **Self-review чеклист** перед выдачей ролика.
5. **ComparisonCard / ProgressBar** code-инфографики + пейсинг 1–3 сек для динамичных беров.
