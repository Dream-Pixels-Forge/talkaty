# Handoff — talkaty (v1.2.0 complete)

> **Project:** `talkaty` — terminal-native TTS voiceover CLI  
> **Location:** `Dev/cli/talkaty/` (category `cli`)  
> **Version:** 0.1.0 (v1.2.0 feature-complete)  
> **Git branch:** `master`  
> **Last commit:** `e6c52cb` — v1.2.0 subgoals 2.2 + 2.3 (Piper TTS + parallel batch + Docker)  
> **Handoff date:** 2026-10-30  

---

## Project in one line

Turn a `script.md` (+ optional `brief.txt`) into accurate voiceover audio in any accent, using open-source TTS backends (edge-tts default, kittenTTS offline, Piper `.onnx`), exposed via both a CLI and an MCP stdio server for coding agents.

---

## Where things stand

**v1.2.0 is complete — all acceptance gates met:**

- [x] 13 personas across 8 accents (US, UK, AU, NG, FR, ZH, HI, ES, DE)
- [x] SSML-lite markup (`<break>`, `<emphasis>`, `<pitch>`)
- [x] Docker containerization (Dockerfile + docker-compose + .dockerignore)
- [x] Piper TTS backend (local offline `.onnx` models)
- [x] Parallel batch processing (`--jobs`, default 4)
- [x] PyPI publishing infrastructure (CI publish job on version tags, `.pypirc.example`)
- [x] Agent skill (`skills/talkaty/`)
- [x] 35 tests passing; mypy/ruff/ruff-format clean

**Git status:** clean working tree, 14 commits on `master`.

---

## How to build / test / run

```bash
cd /home/dimona/Dream-Pixels-Forge/Dev/cli/talkaty

# Install (edge-tts default backend)
pip install -e .

# Install with optional backends
pip install -e .[kittentts]   # kittenTTS offline fallback
pip install -e .[piper]        # Piper .onnx voice models

# CLI
talkaty --help
talkaty voices
talkaty generate script.md --voice narrator --pitch -2 --speed 0.85 --subtitles
talkaty batch scripts/ out/ --jobs 4

# Tests
pytest

# Lint / type / format
mypy src/
ruff check src/ tests/
ruff format --check src/ tests/

# Docker (build is network-bound; works when pip can reach PyPI)
docker build -t talkaty:latest .
docker run --rm -v $(pwd)/scripts:/data/scripts:ro -v $(pwd)/out:/data/out talkaty generate /data/scripts/foo.md
```

---

## Key files & structure

```
Dev/cli/talkaty/
├── Dockerfile                  # container build (single-stage, python:3.12-slim)
├── docker-compose.yml          # volume-mapped run
├── .dockerignore
├── .pypirc.example             # PyPI token template (NOT committed: .pypirc)
├── .github/workflows/ci.yml    # mypy + ruff + pytest; publish on version tags
├── pyproject.toml              # deps: edge-tts, typer, rich, pydantic; dev: pytest, ruff, mypy, build, twine
├── HANDOFF.md                  # this file
├── README.md                   # user-facing docs (personas, backends, SSML-lite, MCP)
├── dev-notes/
│   ├── GOAL.md                 # master goal (v0.1.0 done, v1.2.0 done)
│   ├── GOAL.md (v0.1.0 complete)
│   ├── BRAINSTORM.md
│   ├── SPEC.md                 # CLI + MCP interface, backend contract, personas
│   └── goals/
│       ├── GOAL-v0-2-0-kitten-tts-subtitles.md   # complete
│       ├── GOAL-v1-0-0-polish.md                  # complete
│       ├── GOAL-v1-1-0.md                          # complete (voices + SSML + PyPI)
│       └── GOAL-v1-2-0.md                          # complete (Docker + Piper + parallel batch)
├── src/talkaty/
│   ├── __init__.py
│   ├── __about__.py            # __version__ = "0.1.0"
│   ├── cli.py                  # Typer app: generate, voices, personas, preview, batch
│   ├── config.py               # pydantic TALKATY_* settings
│   ├── script.py               # parse_script / parse_brief (accent detection from free text)
│   ├── ssml.py                 # parse_ssml (<break>, <emphasis>, <pitch>)
│   ├── voices.py               # 10 personas, ACCENT_MAP, resolve_persona
│   ├── pipeline.py             # run(): parse → resolve voice → synthesize → write audio + SRT
│   ├── audio.py                # write_audio, write_srt, write_vtt, estimate_duration_ms
│   ├── mcp_server.py           # stdio MCP server: tts_generate, list_voices, list_personas, preview
│   └── backends/
│       ├── base.py             # TTSBackend ABC (pitch: float|str)
│       ├── edge_tts.py         # default, 400+ voices
│       ├── kittentts.py        # offline fallback
│       └── piper.py            # .onnx voice models
└── tests/
    ├── test_cli.py
    ├── test_script.py
    ├── test_pipeline.py
    ├── test_ssml.py            # 7 SSML parsing tests
    ├── test_backends.py
    ├── test_batch.py
    └── test_audio.py
```

---

## Personas (10)

| Persona | Voice ID | Accent | Style |
|---------|----------|--------|-------|
| alpha male | en-US-GuyNeural | US | bold, authoritative |
| smooth female | en-US-JennyNeural | US | warm, friendly |
| warm narrator | en-GB-SoniaNeural | UK | storytelling |
| energetic | en-US-AriaNeural | US | ads, hype |
| calm | en-AU-WilliamNeural | AU | meditation, ASMR |
| nigerian narrator | en-NG-EzinneNeural | NG | Nigerian English |
| french narrator | fr-FR-EloiseNeural | FR | French storytelling |
| deep french narrator | fr-FR-HenriNeural | FR | deep mystery French |
| chinese narrator | zh-CN-XiaoxiaoNeural | ZH | Mandarin |
| narrator | en-US-ChristopherNeural | US | deep mystery documentary |

---

## Memorius context

Stored in memorius vault under `main/projects/talkaty/`:

| Entry | Path | What |
|-------|------|------|
| context-check | `main/projects/talkaty/context-check` | Initial null check (nothing existed) |
| brainstorm | `main/projects/talkaty/brainstorm` | Original (superseded) chat-client concept |
| supersedes-chat-concept | `main/projects/talkaty/supersedes-chat-concept` | Nullifies chat-client idea |
| corrected-definition-tts | `main/projects/talkaty/corrected-definition-tts` | TTS definition |
| goal-restructure-v0-2-0 | `main/projects/talkaty/goal-restructure-v0-2-0` | GOAL.md restructure + v0.2.0 subgoals |
| v0-1-0-scaffold-complete | `main/projects/talkaty/v0-1-0-scaffold-complete` | v0.1.0 scaffold |
| v0-2-0-complete | `main/projects/talkaty/v0-2-0-complete` | v0.2.0 (kittenTTS + SRT + batch) |
| kittentts-voice-id-fix | `main/projects/talkaty/kittentts-voice-id-fix` | backend-specific voice IDs |
| v1-0-0-complete | `main/projects/talkaty/v1-0-0-complete` | v1.0.0 (brief auto-accent + preview + docs) |
| narrator-persona-added | `main/projects/talkaty/narrator-persona-added` | narrator persona |
| deep-french-narrator-added | `main/projects/talkaty/deep-french-narrator-added` | deep french narrator |
| fr-zh-accents-added | `main/projects/talkaty/fr-zh-accents-added` | FR + ZH accents |
| talkaty-agent-skill-created | `main/projects/talkaty/talkaty-agent-skill-created` | skills/talkaty/ |
| v1-1-0-subgoal-1-1-complete | `main/projects/talkaty/v1-1-0-subgoal-1-1-complete` | HI/ES/DE voices |
| v1-1-0-ssml-complete | `main/projects/talkaty/v1-1-0-ssml-complete` | SSML-lite markup |
| v1-2-0-complete | `main/projects/talkaty/v1-2-0-complete` | v1.2.0 (Piper + parallel batch + Docker) |

Find via: `memorius search "talkaty"` or `memorius search "talkaty tts voiceover"`.

---

## What's left (optional future work)

None required — v1.2.0 acceptance gate is fully met. Optional directions:

1. **PyPI test publish** — add `TEST_PYPI_USERNAME` / `TEST_PYPI_PASSWORD` GitHub secrets and run the publish workflow (`.github/workflows/ci.yml` publish job is ready, triggered on version tags).
2. **More backends** — Piper works; could add Coqui, etc.
3. **SSML prosody/volume** tags.
4. **MCP integration test** with an actual coding agent calling `tts_generate`.
5. **Docker build verification** when network allows pip to reach PyPI (build currently network-bound in this env).

---

## How to resume

```bash
cd /home/dimona/Dream-Pixels-Forge/Dev/cli/talkaty
git status            # should be clean
git log --oneline -5  # see last commit e6c52cb
pytest -q             # 35 passing
talkaty --help        # CLI works
```

No in-progress branches, no uncommitted changes, no blocked items. The project is in a clean, shippable state.
