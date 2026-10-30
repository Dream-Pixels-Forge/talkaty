---
name: talkaty
description: Teach a coding agent how to use talkaty — the terminal-native TTS voiceover tool (script.md + brief → audio in any accent, CLI or MCP). Covers script/brief reformatting, persona selection, pitch/speed/pacing controls, and accurate voiceover generation. Use when the user wants to generate voiceover audio, format scripts/briefs for TTS, or wire talkaty into an agent via MCP.
---

# talkaty — Voiceover Generation Skill

Teaches a coding agent how to use **talkaty**: convert a `script.md` (plus optional `brief.txt`) into accurate voiceover audio in any accent, using open-source TTS backends (edge-tts default, kittenTTS offline fallback). Exposes both a CLI and an MCP stdio server for coding agents.

## Quick start

```bash
# Install
pip install -e .                # edge-tts backend (default)
pip install -e .[kittentts]     # add kittenTTS offline fallback

# Generate voiceover from a script.md
talkaty generate script.md --voice "smooth female" --accent US

# With personality/emotion controls (pitch, speed, pacing via --speed)
talkaty generate script.md --voice "narrator" --pitch -2 --speed 0.9 --subtitles

# Brief-driven accent auto-selection (brief mentions "French" → French voice)
talkaty generate script.md --brief brief.txt

# List available personas
talkaty voices

# Preview a short sample
talkaty preview "Hello world" --voice "deep french narrator"

# Batch a directory of scripts
talkaty batch scripts/ out/
```

## Workflows

### 1. Generate voiceover from script.md (+ brief)

1. Write `script.md` — the text to speak (see [REFERENCE.md](REFERENCE.md) for formatting rules).
2. Optionally write `brief.txt` — tone, accent, emotion hints (e.g. "French accent", "mysterious", "energetic").
3. Choose a persona (see `talkaty voices`).
4. Run `talkaty generate script.md [--brief brief.txt] [--voice PERSONA] [--accent CODE] [--pitch N] [--speed N] [--subtitles]`.
5. Verify output MP3 (+ optional SRT subtitles).

### 2. Reformat script & brief for accurate TTS

- See [REFERENCE.md](REFERENCE.md) for script formatting (paragraphs, sentence breaks, SSML-like markup) and brief formatting (key:value hints + free-text accent/emotion keywords).
- Use `parse_script`/`parse_brief` logic: blank lines split paragraphs, sentence boundaries split breath groups.
- Brief auto-selects accent from keywords: Nigerian/NG, UK/British, US, AU/Australian, FR/French/France, ZH/Chinese/China/Mandarin.

### 3. Wire talkaty into a coding agent via MCP

talkaty runs as an MCP stdio server exposing four tools:

- `tts_generate(script_path, brief_path?, voice?, accent?, backend?, pitch?, speed?, output_path?, subtitles?)` → `{audio_path, duration_seconds, voice_used, backend_used}`
- `list_voices(backend?)` → available voices
- `list_personas()` → persona presets
- `preview(text, voice?, backend?)` → short sample audio

Connect the agent's MCP client to `talkaty mcp_server.py` (stdio). The agent calls `tts_generate` and reads the returned `audio_path` from disk.

## Personas (personality/emotion presets)

| Persona | Voice | Accent | Best for |
|---------|-------|--------|----------|
| alpha male | en-US-GuyNeural | US | bold, authoritative |
| smooth female | en-US-JennyNeural | US | warm, friendly |
| warm narrator | en-GB-SoniaNeural | UK | storytelling |
| energetic | en-US-AriaNeural | US | ads, hype |
| calm | en-AU-WilliamNeural | AU | meditation, ASMR |
| nigerian narrator | en-NG-EzinneNeural | NG | Nigerian English storytelling |
| french narrator | fr-FR-EloiseNeural | FR | French storytelling |
| deep french narrator | fr-FR-HenriNeural | FR | deep, mysterious French documentary |
| chinese narrator | zh-CN-XiaoxiaoNeural | ZH | Mandarin Chinese storytelling |
| narrator | en-US-ChristopherNeural | US | deep mystery documentary |

## Controls

- `--pitch N` — pitch shift in semitones (negative = deeper, positive = higher)
- `--speed N` — speed multiplier (0.5 = slow/dramatic, 1.0 = normal, 1.5 = fast/energetic)
- `--subtitles` — emit `.srt` subtitle file with timestamps

## Advanced features

See [REFERENCE.md](REFERENCE.md) for detailed script/brief formatting, backend selection, and edge cases. See [EXAMPLES.md](EXAMPLES.md) for copy-pasteable CLI and MCP examples.

## Review checklist

- [ ] Description includes triggers ("Use when...") — covered
- [ ] SKILL.md under 100 lines — covered
- [ ] Concrete examples included — covered
- [ ] References one level deep (REFERENCE.md, EXAMPLES.md) — covered
