# talkaty — Deep Brainstorm (TTS Voiceover)

> **Project:** `talkaty` — "talkative"  
> **Purpose:** Generate accurate voiceover audio of any accent from a script.md + brief/description  
> **Interface:** MCP server for coding agents + standalone CLI  
> **TTS backends:** open-source (edge-tts, kittenTTS, etc.)  
> **Controls:** pitch, speed, pacing presets; voice personas (alpha male, smooth female, etc.)  
> **Location:** `Dev/cli/talkaty/` (category `cli`)  
> **Status:** Blank slate — zero code  
> **Author:** Agentic brainstorm (ponytail level: full)

---

## 1. One-line pitch

Talkaty turns a `script.md` (plus brief/description) into a polished voiceover audio file in any accent, using open-source TTS engines, with persona-based presets (pitch/speed/pacing) — exposed both as an MCP tool for coding agents and as a CLI.

---

## 2. Problem it solves

DPF teams produce scripts (`script.md`) but have no terminal-native way to turn them into voiceover audio. Existing TTS tools are either:
- Web UI only (no CLI/MCP, not agent-scriptable)
- Proprietary / API-key gated
- One voice, no accent control, no presets

Talkaty fills the gap: script → voiceover, fully local/open-source, agent-callable via MCP.

---

## 3. User personas

| Persona | Goal | How talkaty helps |
|---------|------|-------------------|
| Coding agent (via MCP) | Generate voiceover for a video/demo from a script | Calls `talkaty.tts_generate(script, brief, voice, accent)` → audio file |
| Content creator | Narrate a script.md with the right accent/tone | `talkaty generate script.md --voice "smooth female" --accent US` |
| DPF video producer | Quick voiceover drafts for promo/ads | Batch generate from multiple scripts, preset voices |
| Accessibility | Audio version of written docs | `talkaty generate README.md` |

---

## 4. Core capabilities

### Input
- `script.md` (primary) — the voiceover script
- `brief.txt` / `description.txt` — tone, audience, accent hints
- Optional: SSML-like markup for emphasis/pauses

### TTS backends (open source, pluggable)
| Backend | Strength | Notes |
|---------|----------|-------|
| **edge-tts** | 400+ voices, many accents, free, no API key | Microsoft Edge TTS, Python `edge-tts` package |
| **kittenTTS** | Small, local, fast | Good for offline/low-resource |
| **Coqui TTS / Piper** | Voice cloning, high quality | Optional later |

### Voice controls
- **Persona presets:** alpha male, smooth female, warm narrator, energetic, calm, etc.
- **Pitch:** ±st / multiplier
- **Speed / rate:** words per minute multiplier
- **Pacing:** pause insertion between sentences/paragraphs
- **Accent:** US, UK, AU, IN, NG, ZA, etc. (backend dependent)

### Output
- Audio: MP3 / WAV
- Optional: SRT / VTT subtitles with word-level timestamps
- Sidecar JSON: metadata (voice, backend, duration, settings)

---

## 5. MCP interface (agent-facing)

Talkaty runs as an MCP stdio server exposing tools:

```
talkaty.tts_generate(script_path, brief_path?, voice, accent, output_path)
talkaty.list_voices(backend?, accent?)
talkaty.list_personas()
talkaty.preview(text, voice)   # short sample
talkaty.batch_generate(scripts_dir, output_dir)
```

A coding agent can invoke these from its own tool loop to produce voiceover for demos, videos, docs.

---

## 6. CLI interface (human-facing)

```
talkaty generate script.md [--brief brief.txt] [--voice "smooth female"] \
    [--accent US] [--pitch 0] [--speed 1.0] [--output out.mp3]
talkaty voices [--accent US]
talkaty personas
talkaty preview "Hello world" --voice "alpha male"
```

---

## 7. Architecture

```
talkaty/
├── pyproject.toml
├── src/talkaty/
│   ├── __init__.py
│   ├── __about__.py
│   ├── cli.py          (typer app)
│   ├── mcp_server.py   (stdio MCP server + tool definitions)
│   ├── config.py       (pydantic settings)
│   ├── backends/       (TTS backend adapters)
│   │   ├── base.py     (TTSBackend ABC)
│   │   ├── edge_tts.py
│   │   └── kittentts.py
│   ├── voices.py       (personas, presets, accent map)
│   ├── script.py       (parse script.md + brief)
│   ├── pipeline.py     (orchestrate parse → tts → audio → subtitles)
│   └── audio.py        (output formats, duration, concat)
├── tests/
├── dev-notes/
│   ├── GOAL.md
│   ├── BRAINSTORM.md   (this file)
│   └── SPEC.md
└── scripts/
```

---

## 8. Data flow

1. Agent/user calls `tts_generate(script.md, brief, voice="smooth female", accent="US")`
2. `script.py` parses `script.md` → segments (paragraphs/sentences)
3. `voices.py` resolves persona → backend voice ID + pitch/speed/pacing
4. `pipeline.py` iterates segments → calls backend TTS → concatenates audio
5. `audio.py` writes MP3/WAV + optional SRT subtitles + metadata JSON
6. Returns output path to agent/user

---

## 9. Non-goals (out of scope)

- Voice cloning / training custom voices (v1)
- Real-time streaming TTS (v1 is file-based)
- Multi-speaker dialogue in one file (single speaker per generation)
- Proprietary API TTS (ElevenLabs, etc.) as default — open source only

---

## 10. Milestones

| Milestone | Criteria |
|-----------|----------|
| v0.1.0 | CLI `generate` via edge-tts, 3 personas, MP3 output, MCP server stub |
| v0.2.0 | kittenTTS backend, subtitles (SRT), brief-driven accent selection |
| v0.3.0 | batch mode, pitch/speed/pacing CLI flags, backend pluggability |
| v1.0.0 | Stable MCP server, all backends, docs, CI |

---

## 11. Immediate next steps

1. **Correct memorius** — supersede the wrong chat-client context with this TTS definition.
2. **Write GOAL.md** — measurable success criteria (DPF goal-writer).
3. **Write SPEC.md** — MCP tool schemas, CLI flags, backend adapter contract.
4. **Scaffold repo** — `git init`, `pyproject.toml`, `src/talkaty/`, `tests/`, CI workflow.
5. **Implement MVP** — edge-tts backend + CLI `generate` + MCP `tts_generate`.

---

## 12. Risks

- **Backend voice quality varies by accent** — test each accent; document which backends support which accents.
- **MCP stdio + audio output** — MCP returns text paths, not binary audio; agent reads file from disk. Ensure output dir is accessible.
- **edge-tts reliability** — depends on Microsoft's endpoint; kittenTTS as local fallback.
