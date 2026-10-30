# talkaty — GOAL v1.0.0: polish (brief auto-accent, preview, docs)

## Subgoal of: `dev-notes/GOAL.md` (master goal)
## Version: 1.0.0
## Status: Not started (deferred from v0.1.0)

---

## Objective

Polish talkaty into a stable release: brief-driven accent auto-selection, preview mode, full docs, and CI/CD pipeline. These were deferred from v0.1.0 to keep the initial release focused.

---

## Subgoal 1.1 — Brief-driven accent auto-selection

- **Objective**: Parse `brief.txt` for accent hints ("Nigerian accent", "British", "US") and auto-select the matching voice/backend when `--accent` is not explicitly given.
- **Acceptance**: Brief mentioning "Nigerian" selects a NG voice automatically; brief mentioning "British" selects UK.
- **Verification**: `tests/test_script.py::test_parse_brief_accent` extracts accent hints; `tests/test_pipeline.py` asserts auto-selection from brief.

## Subgoal 1.2 — Preview mode

- **Objective**: `talkaty preview "Hello world" --voice "alpha male"` — short sample, no full script file needed.
- **Acceptance**: `preview` synthesizes text directly (temp file internally) and returns an audio path.
- **Verification**: `tests/test_cli.py::test_preview` runs preview and asserts output path exists.

## Subgoal 1.3 — Docs + CI/CD pipeline

- **Objective**: README with examples (generate, voices, batch, MCP usage); GitHub CI runs mypy + ruff + pytest and is green.
- **Acceptance**: `README.md` has copy-pasteable examples; `.github/workflows/ci.yml` passes on push/PR.
- **Verification**: CI badge/green status; README examples run without error in a fresh venv.

---

## Acceptance Gate (v1.0.0)

- [ ] Brief accent auto-selection works for at least NG, UK, US hints
- [ ] `talkaty preview` works without a script file
- [ ] README complete with examples
- [ ] CI green on push/PR
- [ ] `pytest` green, `ruff` clean, `mypy` clean
