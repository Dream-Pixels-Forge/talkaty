# talkaty — GOAL.md (master)

## Meta Information
- **Version**: 1.2.1 (release-ready)
- **Mode**: Existing project — v0.1.0 complete, subgoals tracked in `dev-notes/goals/`
- **Target Repository**: `Dev/cli/talkaty/` (category `cli`)
- **Zero-Tolerance Invariant**: `tts_generate` must produce a playable MP3/WAV from any valid `script.md` using only open-source TTS backends; zero secrets in repo; 100% CI pass rate.

---

## Subgoal Index (lives in `dev-notes/goals/`)

| Subgoal | File | Version | Status |
|---------|------|---------|--------|
| kittenTTS backend + SRT subtitles + batch | `dev-notes/goals/GOAL-v0-2-0-kitten-tts-subtitles.md` | 0.2.0 | Completed (in code, notes stale) |
| Brief auto-accent + preview + docs + CI | `dev-notes/goals/GOAL-v1-0-0-polish.md` | 1.0.0 | Completed (in code, notes stale) |
| More voices + SSML-lite + PyPI infra | `dev-notes/goals/GOAL-v1-1-0.md` | 1.1.0 | Completed |
| Docker + Piper backend + parallel batch | `dev-notes/goals/GOAL-v1-2-0.md` | 1.2.0 | Completed |

> Convention: one master `GOAL.md` here; each version's detailed acceptance criteria lives in its own file under `dev-notes/goals/`.

---

## v0.1.0 — COMPLETED (committed: `61b5299`)

All acceptance criteria met:

- [x] `talkaty generate script.md --voice "smooth female" --accent US` produces `script.mp3` (verified: 16.2s demo.mp3)
- [x] MCP `tts_generate` returns valid audio file path (server implemented in `src/talkaty/mcp_server.py`)
- [x] `pytest` green — 9 tests passing
- [x] `pip install -e .` + `talkaty --help` works
- [x] Zero hardcoded secrets/API keys in repo
- [x] CLI: `generate`, `voices`, `personas`, `preview`, `batch`
- [x] Personas: alpha male, smooth female, warm narrator, energetic, calm
- [x] Controls: `--pitch`, `--speed`, `--accent`; optional `--subtitles`
- [x] Backends: edge-tts (default), kittenTTS (optional)
- [x] CI: `.github/workflows/ci.yml` (mypy, ruff, pytest)

### Completed sub-tasks
- Scaffold repo: `pyproject.toml`, `src/talkaty/`, `tests/`, `.gitignore`, `README.md`, `.env.example`
- Git initialized + initial commit
- dev-notes: `BRAINSTORM.md`, `GOAL.md`, `SPEC.md`

---

## Pre-Flight Checkpoint (baseline, already verified)

- [x] **0.1 Python 3.12.3 available** → `Python 3.12.3`
- [x] **0.2 edge-tts installable** → edge-tts 7.3.1 installed
- [x] **0.3 `talkaty` console entry point registered** → `talkaty --help` works

---

## Next immediate work

None — all subgoals complete. The only blocker to publishing is PyPI account access (2FA + recovery codes forgotten).

1. Recover PyPI 2FA at https://pypi.org/account/recover/ or contact pypi-admin@python.org
2. Add PyPI token to GitHub secrets (`PYPI_API_TOKEN`)
3. Tag a release: `git tag v1.2.0 && git push origin v1.2.0`
4. CI builds + publishes to TestPyPI; add production PyPI publish step for the main release
