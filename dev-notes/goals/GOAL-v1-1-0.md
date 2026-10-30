# talkaty — GOAL v1.1.0: more voices + SSML-lite + PyPI publish

## Subgoal of: `dev-notes/GOAL.md` (master goal)
## Version: 1.1.0
## Status: Not started

---

## Objective

Expand talkaty's voice/accent coverage, add SSML-lite markup for finer control over emphasis and pauses, and prepare for PyPI publishing.

---

## Subgoal 1.1 — More voices/accents (COMPLETED)

- **Objective**: Add Indian Hindi (HI), Spanish (ES), German (DE) personas.
- **Status**: ✅ Done — 13 personas total, edge-tts voice IDs verified, end-to-end generate works for each.

## Subgoal 1.2 — SSML-lite markup in scripts

- **Objective**: Support `<break time="1s"/>`, `<emphasis>text</emphasis>`, `<pitch>N</pitch>` in script.md for fine control.
- **Acceptance**: Scripts with SSML-lite tags synthesize with correct pauses/emphasis.
- **Verification**: `tests/test_ssml.py` parses and applies tags.

## Subgoal 1.3 — PyPI publishing setup

- **Objective**: Add `build`, `twine`, provenance config; `.pypirc` example; CI publish job.
- **Acceptance**: `pip install talkaty` works from TestPyPI; publish pipeline ready.
- **Verification**: `dpf-publisher` skill used for release process.

---

## Acceptance Gate (v1.1.0)

- [x] 13 personas including HI, ES, DE
- [ ] SSML-lite tags parsed and applied
- [ ] PyPI publish pipeline configured
- [ ] `pytest` green, `ruff` clean, `mypy` clean
