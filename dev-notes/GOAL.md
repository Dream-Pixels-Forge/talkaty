# talkaty — GOAL.md

## Meta Information
- **Version**: 0.1.0
- **Mode**: New project (blank slate)
- **Target Repository**: `Dev/cli/talkaty/` (category `cli`)
- **Zero-Tolerance Invariant**: `tts_generate` must produce a playable MP3/WAV from any valid `script.md` using only open-source TTS backends; zero secrets in repo; 100% CI pass rate.

---

## Pre-Flight Checkpoint: Characterization Baseline
- [ ] **0.1 Python 3.12.3 available**
  - *Verification Command*: `python3 --version` → `Python 3.12.3`
- [ ] **0.2 edge-tts and/or kittenTTS installable**
  - *Verification Command*: `pip install edge-tts` succeeds
- [ ] **0.3 `talkaty` console entry point registered**
  - *Verification Command*: `talkaty --help` prints usage

---

## Phase 1 — MVP (P0): script.md → voiceover MP3

### 1.1 Scaffold repo
- *Objective*: `pyproject.toml`, `src/talkaty/`, `tests/`, `.gitignore`, `README.md`, `.github/workflows/ci.yml`
- *Acceptance*: `pnpm`? No — Python. `pip install -e .` succeeds; `talkaty --help` works.

### 1.2 CLI `talkaty generate script.md`
- *Objective*: Read a `script.md`, synthesize speech via edge-tts default voice, write `script.mp3` next to input.
- *Acceptance*: `talkaty generate samples/demo.md` produces `demo.mp3` that is playable (non-zero bytes, valid MP3 header).

### 1.3 MCP stdio server with `tts_generate` tool
- *Objective*: Expose `talkaty.tts_generate(script_path, brief_path?, voice, accent, output_path)` over MCP stdio.
- *Acceptance*: `memorius`? No — use an MCP inspector/client to call `tts_generate` and confirm it returns a valid audio file path.

### 1.4 Persona presets
- *Objective*: Predefined voice configs: alpha male, smooth female, warm narrator, energetic, calm.
- *Acceptance*: `talkaty voices` lists personas; `--voice "smooth female"` changes output voice.

### 1.5 Controls: --pitch, --speed, --accent
- *Objective*: CLI flags to adjust pitch (st), speed (rate multiplier), accent (US/UK/AU/etc.).
- *Acceptance*: `talkaty generate script.md --pitch 2 --speed 1.2 --accent UK` runs without error.

---

## Phase 2 — Subtitles + batch (P1)

### 2.1 SRT subtitle generation
- *Objective*: Emit `script.srt` with word-level timestamps alongside audio.
- *Acceptance*: `.srt` file is valid (parseable by pysrt or simple regex).

### 2.2 kittenTTS backend (local fallback)
- *Objective*: Second TTS backend that works offline when edge-tts is unreachable.
- *Acceptance*: `--backend kittentts` produces audio.

### 2.3 `talkaty batch` directory mode
- *Objective*: Generate voiceovers for all `*.md` in a directory.
- *Acceptance*: `talkaty batch scripts/ out/` creates one audio per `.md`.

---

## Phase 3 — Polish (P2)

### 3.1 Brief-driven accent auto-selection
- *Objective*: Parse `brief.txt` for accent hints ("Nigerian accent", "British") and auto-select.
- *Acceptance*: Brief mentioning "Nigerian" selects a NG voice automatically.

### 3.2 Preview mode
- *Objective*: `talkaty preview "Hello world" --voice "alpha male"` — short sample, no full script needed.

### 3.3 Docs + CI/CD pipeline
- *Acceptance*: README with examples; GitHub CI runs pytest + ruff + mypy and is green.

---

## Acceptance Gate (v0.1.0)
- [ ] `talkaty generate script.md --voice "smooth female" --accent US` produces `script.mp3`
- [ ] MCP `tts_generate` returns valid audio file path
- [ ] `pytest` green, `ruff` clean, `mypy` clean
- [ ] `pip install -e .` + `talkaty --help` works
- [ ] Zero hardcoded secrets/API keys in repo
