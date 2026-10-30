# talkaty — Examples

Copy-pasteable CLI and MCP examples for accurate voiceover generation.

---

## CLI examples

### Basic generation
```bash
talkaty generate script.md --voice "smooth female" --accent US
```

### With brief (accent auto-selection)
```bash
talkaty generate script.md --brief brief.txt
# If brief.txt contains "French accent" → selects french narrator
```

### Mystery documentary (deep, slow)
```bash
talkaty generate script.md --voice narrator --pitch -2 --speed 0.85 --subtitles
```

### Deep French documentary
```bash
talkaty generate script.md --voice "deep french narrator" --pitch -1 --speed 0.9 --subtitles
```

### Energetic ad
```bash
talkaty generate script.md --voice energetic --pitch 0 --speed 1.2 --accent US
```

### Warm, friendly narration
```bash
talkaty generate script.md --voice "smooth female" --speed 1.0
```

### Authoritative
```bash
talkaty generate script.md --voice "alpha male" --pitch -1 --speed 0.95 --accent US
```

### Calm / meditation
```bash
talkaty generate script.md --voice calm --pitch 1 --speed 0.8 --accent AU
```

### Offline (kittenTTS)
```bash
talkaty generate script.md --backend kittentts --voice "smooth female"
```

### Preview (no script file needed)
```bash
talkaty preview "Hello world" --voice "deep french narrator"
```

### List voices
```bash
talkaty voices
talkaty voices --backend kittentts
```

### Batch directory
```bash
talkaty batch scripts/ out/ --voice narrator --subtitles
```

### Custom output path
```bash
talkaty generate script.md --output my_audio.mp3
```

---

## MCP examples

### tts_generate (agent calls this)
```json
{
  "name": "tts_generate",
  "arguments": {
    "script_path": "script.md",
    "brief_path": "brief.txt",
    "voice": "narrator",
    "accent": "US",
    "backend": "edge-tts",
    "pitch": -2,
    "speed": 0.85,
    "output_path": "mystery.mp3",
    "subtitles": true
  }
}
```

Returns:
```json
{
  "audio_path": "/abs/path/to/mystery.mp3",
  "duration_seconds": 12.4,
  "voice_used": "narrator",
  "backend_used": "edge-tts"
}
```

### list_voices
```json
{
  "name": "list_voices",
  "arguments": { "backend": "edge-tts" }
}
```

### list_personas
```json
{
  "name": "list_personas",
  "arguments": {}
}
```

### preview
```json
{
  "name": "preview",
  "arguments": { "text": "Hello world", "voice": "deep french narrator" }
}
```

---

## Connecting an MCP agent

Launch talkaty as an MCP stdio server:

```bash
python -m talkaty.mcp_server
```

Then configure your agent's MCP client to connect to this stdio command. The agent calls `tts_generate` and reads the returned `audio_path` from disk.
