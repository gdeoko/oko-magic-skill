# pipeline/factory — рабочие генераторы (референс с эталонного ролика DIESEL)

Проверенные боем скрипты сборки ролика (голос → кадры → инфографика кодом →
субтитры → музыка/SFX → композит → обложка → анимированная финалка).

Порядок: `plan.py` (тайминги+караоке-данные) → `assemble.py` (база: обложка+клипы,
crop-pan+грейд) → инфографика/оверлеи (`build_accents.py`, `build_subs.py`,
`build_titles.py`, `html/*` через `capture.js`/`cap_opaque.js` → qtrle .mov) →
`audio.py` (VO+музыка fade+даккинг+разные SFX) → `compose.py` (оверлеи+субтитры+финалка).
Обложка — `make_cover.py`. Анимированная финалка — `html/endcard_tpl.html`.

ВАЖНО (адаптация под сессию/клиента):
- В скриптах и `html/*` путь к шрифтам задан как `FB=file:///.../fonts` или
  `../../../fonts/`. **Поправить на реальный путь к `skills/reels-machine/fonts/`**
  (Soyuz Grotesk Bold + Montserrat + Manrope лежат там).
- Playwright: `capture.js` пинит chromium `/opt/pw-browsers/chromium-<v>/chrome-linux/chrome` —
  обновить версию под окружение.
- Тексты/данные ролика (сценарий, ACCENTS, TITLES, цвета) — переписываются ЗАНОВО под
  каждый ролик по законам разнообразия. Это не шаблон-с-подменой-цифр, а каркас.
- Клиентские ассеты (лого, шрифт, бренд-профиль) — в `../../oko-content-factory/clients/<slug>/`.
