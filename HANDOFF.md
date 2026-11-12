# Handoff — talkaty (v1.2.1 release-ready)

> **Project:** `talkaty` — terminal-native TTS voiceover CLI  
> **Location:** `Dev/cli/talkaty/` (category `cli`)  
> **Version:** 1.2.1  
> **Git branch:** `main`  
> **Last commit:** `4f5ca72` — fix: add LICENSE + SPDX license; bump to v1.2.1  
> **Handoff date:** 2026-11-12  
> **Last update:** docs updated; `__about__.py` synced to 1.2.1; LICENSE added  

---

## Project in one line

Turn a `script.md` (+ optional `brief.txt`) into accurate voiceover audio in any accent, using open-source TTS backends (edge-tts default, kittenTTS offline, Piper `.onnx`), exposed via both a CLI and an MCP stdio server for coding agents.

---

## Where things stand

**v1.2.1 is code-complete — acceptance gates:**

| Gate | Status |
|------|--------|
| 13 personas across 8 accents (US, UK, AU, NG, FR, ZH, HI, ES, DE) | ✅ Code complete |
| SSML-lite markup (`<break>`, `<emphasis>`, `<pitch>`) | ✅ Code complete |
| Docker containerization (Dockerfile + docker-compose + .dockerignore) | ✅ Code complete (build not network-tested) |
| Piper TTS backend (local offline `.onnx` models) | ✅ Code complete (needs `.onnx` model for full synthesis) |
| kittenTTS backend (local offline fallback) | ✅ Code complete (needs `kittentts` package for full synthesis) |
| Parallel batch processing (`--jobs`, default 4) | ✅ Code complete |
| MCP stdio server (`tts_generate`, `list_voices`, `list_personas`, `preview`) | ✅ Code complete |
| PyPI publishing infrastructure (CI publish job on tags, `.pypirc.example`) | ✅ Configured |
| Agent skill (`skills/talkaty/`) | ✅ Present |
| 35 tests passing; mypy/ruff/ruff-format clean | ✅ Verified |
| `twine check` on dist artifacts | ✅ Passed |
| `__about__.py` synced to pyproject version (1.2.1) | ✅ Fixed |
| LICENSE file present | ✅ Added |

**End-to-end verification pending (code implemented, not yet tested against real inputs):**

- [ ] `talkaty generate --backend kittentts` produces playable audio
- [ ] `talkaty generate --subtitles` produces valid `.srt`
- [ ] `talkaty batch scripts/ out/` produces N outputs for N inputs
- [ ] Brief accent auto-selection (NG, UK, US, FR, ZH)
- [ ] `talkaty preview` without a script file
- [ ] Docker build (`docker build -t talkaty:latest .`)

**Git status:** clean working tree, on `main`, tag `v1.2.1` pushed to origin.

**Publishing blocker — PyPI account access:**
2FA and recovery codes are forgotten. Recover before publishing:
1. https://pypi.org/account/recover/ (if you still have the account email)
2. Or email `pypi-admin@python.org` to verify identity and reset 2FA
3. Then add `PYPI_API_TOKEN` to GitHub Secrets for production publish

CI `.github/workflows/ci.yml` already builds + publishes to TestPyPI on version tags.

---

## How to build / test / run

```bash
cd /home/dimona/Dream-Pixels-Forge/Dev/cli/talkaty

# Install (edge-tts default backend) — already installed
pip install -e .

# Optional backends — already installed
pip install -e .[kittentts]   # kittenTTS offline fallback
pip install -e .[piper]        # Piper .onnx voice models

# Verify backends import
python3 -c "from talkaty.backends import edge_tts, kittentts, piper; print('OK')"

# CLI
talkaty --help
talkaty voices
talkaty generate script.md --voice narrator --pitch -2 --speed 0.85 --subtitles
talkaty batch scripts/ out/ --jobs 4

# Tests
pytest -q

# Lint / type / format
mypy src/
ruff check src/ tests/
ruff format --check src/ tests/

# Build dist (for publishing)
python3 -m build
python3 -m twine check dist/*

# Docker (build is network-bound; works when pip can reach PyPI)
docker build -t talkaty:latest .
docker run --rm -v $(pwd)/scripts:/data/scripts:ro -v $(pwd)/out:/data/out talkaty generate /data/scripts/foo.md
```

**MCP server** (`talkaty`): registered in both MCP configs — command `python3 -m talkaty.mcp_server` (stdio). Exposes `tts_generate`, `list_voices`, `list_personas`, `preview`.

---

## Personas (13)

| Persona | Accent | Style |
|---------|--------|-------|
| alpha male | US | bold, authoritative |
| smooth female | US | warm, friendly |
| warm narrator | UK | storytelling |
| energetic | US | ads, hype |
| calm | AU | meditation, ASMR |
| nigerian narrator | NG | Nigerian English |
| french narrator | FR | French storytelling |
| deep french narrator | FR | deep mystery French |
| chinese narrator | ZH | Mandarin |
| narrator | US | deep mystery documentary |
| hindi narrator | HI | Hindi storytelling |
| spanish narrator | ES | Spanish storytelling |
| german narrator | DE | German storytelling |

---

## How to resume

```bash
cd /home/dimona/Dream-Pixels-Forge/Dev/cli/talkaty
git status            # should be clean
git log --oneline -5  # see last commit
pytest -q             # 35 passing
talkaty --help        # CLI works
python3 -c "from talkaty.backends import edge_tts, kittentts, piper; print('backends OK')"
python3 -m build && python3 -m twine check dist/*
```

**MCP:** `talkaty` server is registered in `.mcp.json` and `.pi/agent/mcp.json` — connect any MCP client to use `tts_generate`, `list_voices`, `list_personas`, `preview`.

No in-progress branches, no uncommitted changes. The project is in a clean, shippable state — pending PyPI 2FA recovery and optional end-to-end verification of the pending items above.
