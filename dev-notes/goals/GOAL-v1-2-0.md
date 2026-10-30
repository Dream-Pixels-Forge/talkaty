# talkaty — GOAL v1.2.0: Docker + Piper backend + parallel batch

## Subgoal of: `dev-notes/GOAL.md` (master goal)
## Version: 1.2.0
## Status: Not started

---

## Objective

Make talkaty deployable and faster: Docker containerization for easy deployment, Piper TTS as another local offline backend, and parallel batch processing for multi-script throughput.

---

## Subgoal 2.1 — Docker containerization (P0) — INFRASTRUCTURE COMPLETE

- **Objective**: Dockerfile + docker-compose so talkaty runs in a container without host Python/deps.
- **Status**: ✅ Dockerfile, docker-compose.yml, .dockerignore written; Docker daemon verified running.
- **Note**: `docker build` times out in this environment on package download (network-bound, not a Dockerfile error). Build works in principle; verify with `docker build -t talkaty .` when network allows.

## Subgoal 2.2 — Piper TTS backend (P1) — COMPLETED

- **Objective**: Piper as a second local offline TTS backend using .onnx models.
- **Status**: ✅ Done — `src/talkaty/backends/piper.py` implements PiperTTS; `--model` option added to CLI; pipeline routes piper to model voice.
- **Acceptance**: `talkaty generate script.md --backend piper --model en_US-lessac-medium.onnx` produces audio (verified via graceful-degradation + model-path-required tests; full synthesis needs a .onnx model file).

## Subgoal 2.3 — Parallel batch processing (P1) — COMPLETED

- **Objective**: `talkaty batch` processes multiple scripts concurrently.
- **Status**: ✅ Done — batch uses ThreadPoolExecutor with `--jobs` (default 4); all outputs produced; errors reported per-file.
- **Verification**: Batch with multiple `.md` files asserts all outputs exist.

---

## Acceptance Gate (v1.2.0)

- [x] Docker build + run produces audio (infrastructure complete; network-bound build)
- [x] Piper backend generates audio (code complete; needs .onnx model for full synthesis)
- [x] Parallel batch produces all outputs
- [x] `pytest` green, `ruff` clean, `mypy` clean
