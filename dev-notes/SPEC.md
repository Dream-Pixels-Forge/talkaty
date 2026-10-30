# talkaty — SPEC.md

## Overview
talkaty converts a `script.md` (plus optional `brief.txt`) into voiceover audio using open-source TTS backends. It exposes a CLI for humans and an MCP stdio server for coding agents.

---

## 1. CLI Interface

```
talkaty generate SCRIPT.md [OPTIONS]
talkaty voices [--backend edge-tts|kittentts]
talkaty personas
talkaty preview TEXT [--voice VOICE] [--backend BACKEND]
talkaty batch SCRIPTS_DIR OUTPUT_DIR [OPTIONS]
```

### `generate` options

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--brief` | path | None | Optional brief/description file for tone & accent hints |
| `--voice` | str | "smooth female" | Persona name or backend voice ID |
| `--accent` | str | "US" | Accent hint (US, UK, AU, IN, NG, ZA, ...) |
| `--backend` | str | "edge-tts" | TTS backend: edge-tts or kittentts |
| `--pitch` | float | 0.0 | Pitch shift in semitones |
| `--speed` | float | 1.0 | Speed multiplier (0.5–2.0) |
| `--output` | path | None | Output audio path (default: script.mp3 next to input) |
| `--subtitles` | flag | false | Also emit `.srt` subtitle file |

### `preview` options
Same as generate minus `--brief`/`--subtitles`/`--output`. Synthesizes a short sample (~5s).

---

## 2. MCP Interface (stdio server)

Server name: `talkaty`

### Tools

**`tts_generate`**
```
input:
  script_path: string   (required)  path to script.md
  brief_path: string    (optional)  path to brief.txt
  voice: string         (optional)  default "smooth female"
  accent: string        (optional)  default "US"
  backend: string       (optional)  default "edge-tts"
  pitch: number         (optional)  default 0
  speed: number         (optional)  default 1.0
  output_path: string   (optional)  default: <script>.mp3
output:
  audio_path: string    absolute path to generated MP3/WAV
  duration_seconds: number
  voice_used: string
  backend_used: string
```

**`list_voices`**
```
input:
  backend: string (optional)
output:
  voices: [{id, name, accent, gender, backend}]
```

**`list_personas`**
```
input: {}
output:
  personas: [{id, description, voice_id, backend}]
```

**`preview`**
```
input:
  text: string (required)
  voice: string (optional)
  backend: string (optional)
output:
  audio_path: string
```

---

## 3. Persona Presets

| Persona | Voice ID (edge-tts) | Gender | Accent | Use case |
|---------|---------------------|--------|--------|----------|
| alpha male | en-US-GuyNeural | male | US | bold, authoritative |
| smooth female | en-US-JennyNeural | female | US | warm, friendly |
| warm narrator | en-GB-SoniaNeural | female | UK | storytelling |
| energetic | en-US-AriaNeural | female | US | hype, ads |
| calm | en-AU-WilliamNeural | male | AU | meditation, ASMR |

---

## 4. Backend Adapter Contract

`src/talkaty/backends/base.py` defines `TTSBackend` ABC:

```python
class TTSBackend(ABC):
    @abstractmethod
    async def synthesize(self, text: str, voice: str, pitch: float, speed: float) -> bytes: ...
    @abstractmethod
    def list_voices(self) -> list[VoiceInfo]: ...
```

Each backend (`edge_tts.py`, `kittentts.py`) implements this. The pipeline picks the backend and passes segments through.

---

## 5. Data Flow

1. `script.py.parse_script(path)` → list of `Segment` (text, start_ms, end_ms)
2. `voices.py.resolve(persona, accent, backend)` → `(voice_id, pitch, speed)`
3. `pipeline.py.run(segments, backend, ...)` → per segment: `backend.synthesize()` → concat bytes
4. `audio.py.write(path, bytes, format)` → MP3/WAV
5. Optional: `audio.py.write_subtitles(path, segments)` → `.srt`
6. Return metadata: path, duration, voice, backend

---

## 6. Output Formats
- Audio: MP3 (default), WAV
- Subtitles: SRT, VTT
- Metadata: sidecar `.json` with voice, backend, duration, settings

---

## 7. Non-Goals
- Voice cloning / custom voice training
- Real-time streaming TTS
- Multi-speaker dialogue in one file
- Proprietary TTS (ElevenLabs, etc.)
