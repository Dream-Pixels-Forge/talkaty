# talkaty

Terminal-native TTS voiceover tool. Turn a `script.md` (plus optional brief) into polished voiceover audio in any accent, using open-source TTS backends. Exposes both a CLI and an MCP stdio server for coding agents.

## Install

```bash
pip install -e .
```

## CLI

```bash
# Generate voiceover from a script
talkaty generate script.md --voice "smooth female" --accent US

# With pitch/speed controls and subtitles
talkaty generate script.md --pitch 2 --speed 1.2 --subtitles

# List available personas
talkaty personas

# Preview a short sample
talkaty preview "Hello world" --voice "alpha male"

# Batch a directory of scripts
talkaty batch scripts/ out/
```

## MCP

talkaty runs as an MCP stdio server exposing `tts_generate`, `list_voices`, `list_personas`, and `preview`. Connect it to any MCP-compatible coding agent to generate voiceover from within your agent loop.

## Backends

- `edge-tts` (default): 400+ voices, many accents, free, no API key
- `kitten-tts`: local, offline fallback (`pip install talkaty[kittentts]`)

## Personas

alpha male, smooth female, warm narrator, energetic, calm
