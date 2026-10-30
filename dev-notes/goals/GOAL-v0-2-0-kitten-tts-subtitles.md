# talkaty — GOAL v0.2.0: kittenTTS backend + subtitles + batch

## Subgoal of: `dev-notes/GOAL.md` (master goal)
## Version: 0.2.0
## Status: Not started

---

## Objective

Add the kittenTTS local offline backend, validated SRT subtitle output, and `talkaty batch` directory mode. This makes talkaty usable without network access (edge-tts fallback) and usable for multi-script production runs.

---

## Subgoal 2.1 — kittenTTS backend (local fallback)

- **Objective**: Second TTS backend that works offline when edge-tts is unreachable.
- **Acceptance**: `talkaty generate script.md --backend kittentts` produces playable audio; `list_voices --backend kittentts` returns voices.
- **Verification**: `pytest tests/test_backends.py` includes kittenTTS path; end-to-end `--backend kittentts` generates audio.
- **Notes**: kittenTTS is an optional dependency (`pip install talkaty[kittentts]`). Must degrade gracefully if not installed.

## Subgoal 2.2 — SRT subtitle generation (validated)

- **Objective**: Emit `script.srt` with word-level timestamps alongside audio via `--subtitles`.
- **Acceptance**: `.srt` file is valid and parseable by `pysrt` or a simple regex; timestamps align to segments.
- **Verification**: `tests/test_audio.py::test_write_srt_valid` passes; end-to-end `--subtitles` produces `.srt` next to `.mp3`.

## Subgoal 2.3 — `talkaty batch` directory mode

- **Objective**: Generate voiceovers for all `*.md` in a directory.
- **Acceptance**: `talkaty batch scripts/ out/` creates one `.mp3` (and optional `.srt`) per `.md` input.
- **Verification**: `tests/test_cli.py::test_batch` runs against a temp dir with 3 `.md` files and asserts 3 outputs.

---

## Acceptance Gate (v0.2.0)

- [ ] `talkaty generate script.md --backend kittentts` produces playable audio (or graceful skip if kittenTTS not installed)
- [ ] `talkaty generate script.md --subtitles` produces valid `.srt`
- [ ] `talkaty batch scripts/ out/` produces N outputs for N inputs
- [ ] `pytest` green, `ruff` clean, `mypy` clean
- [ ] CI passes
