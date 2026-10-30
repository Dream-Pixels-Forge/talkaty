# talkaty — Reference: script & brief formatting for accurate TTS

Detailed rules for formatting `script.md` and `brief.txt` so talkaty produces accurate, expressive voiceover with the right personality, emotion, pitch, and pacing.

---

## 1. script.md formatting

talkaty reads `script.md` and splits it into speakable segments. Follow these rules for the most accurate results:

### Paragraphs → breath groups
Separate distinct ideas with **blank lines**. Each blank-line-separated block becomes one breath group (segment), synthesized with a natural pause between groups.

```markdown
# Introduction

Welcome to the show.

This is the first segment — a complete thought.

# Body

This is the second segment. It flows after a pause.

And here is a third, shorter segment.
```

### Sentence boundaries
Within a paragraph, sentences ending in `.`, `!`, or `?` followed by whitespace are split into sub-segments. This lets talkaty apply natural pacing between sentences.

### Markdown headings
Heading markers (`#`, `##`, etc.) are stripped but the text is kept. Use headings for organization, not for speech content.

### Avoid
- Tables, code fences, and lists — these are not stripped and may be spoken literally.
- Emojis and special symbols — may not render well in TTS.
- Inline markdown links `[text](url)` — the raw markdown will be spoken.

### Pacing hints
To force a longer pause between two thoughts, put them in separate paragraphs (blank line between). To speed up delivery, keep thoughts in one paragraph with short sentences.

---

## 2. brief.txt formatting

The brief tells talkaty the tone, accent, and emotion. Two formats are supported:

### Key:value lines
```text
accent: French
tone: mysterious
emotion: suspenseful
pacing: slow
```

### Free-text keywords (auto-detected)
talkaty scans free text for accent keywords and auto-selects the matching voice when `--accent` is not given:

| Keyword | Accent code | Voice selected |
|---------|-------------|----------------|
| Nigerian / Nigeria | NG | nigerian narrator |
| British / UK | UK | warm narrator |
| US / American | US | smooth female |
| Australian / AU | AU | calm |
| French / France | FR | french narrator |
| Chinese / China / Mandarin | ZH | chinese narrator |

### Emotion / personality hints (informational)
Emotion words (`mysterious`, `energetic`, `calm`, `authoritative`, `warm`, `suspenseful`) are stored in the brief but do not auto-select a persona. Choose the matching persona manually via `--voice`:
- mysterious / suspenseful → `narrator` or `deep french narrator`
- energetic / hype → `energetic`
- warm / friendly → `smooth female`
- authoritative → `alpha male`
- calm / meditation → `calm`

---

## 3. Personality, emotion, pitch, pacing controls

Use CLI flags to fine-tune the delivery for accuracy:

| Control | Flag | Range | Effect |
|---------|------|-------|--------|
| Pitch | `--pitch N` | semitones | Negative = deeper voice; Positive = higher voice |
| Speed / pacing | `--speed N` | 0.5–2.0 | Below 1.0 = slower, more dramatic; Above 1.0 = faster, more energetic |
| Voice / persona | `--voice NAME` | persona id | Selects the voice timbre and accent |
| Accent | `--accent CODE` | US/UK/AU/NG/FR/ZH | Overrides brief auto-selection |
| Backend | `--backend NAME` | edge-tts/kittentts | edge-tts (default, online) or kittentts (offline) |
| Subtitles | `--subtitles` | flag | Emits `.srt` with word timestamps |

### Recommended combinations

| Goal | --voice | --pitch | --speed | --accent |
|------|---------|---------|---------|----------|
| Mystery documentary | narrator | -2 | 0.85 | US |
| Deep French documentary | deep french narrator | -1 | 0.9 | FR |
| Energetic ad | energetic | 0 | 1.2 | US |
| Warm narration | smooth female | 0 | 1.0 | US |
| Authoritative | alpha male | -1 | 0.95 | US |
| Calm ASMR | calm | 1 | 0.8 | AU |

---

## 4. Backend selection

- `edge-tts` (default): 400+ voices, many accents, free, no API key. Requires network access to Microsoft's endpoint.
- `kittentts`: local, offline fallback. Install with `pip install talkaty[kittentts]`. Smaller voice set (`expr-voice-2-m`, `expr-voice-2-f`).

Use `--backend kittentts` when edge-tts is unreachable or you need fully offline generation.

---

## 5. Output

- Audio: MP3 (default), next to the input script (or `--output` path).
- Subtitles: `.srt` with `--subtitles` (timestamps aligned to segments).
- Metadata: sidecar `.json` with voice, backend, duration, settings.

---

## 6. Example: accurate mystery documentary voiceover

`script.md`:
```markdown
# The Vanishing

Midnight. The rain fell in sheets across the empty streets.

Detective Vale stepped into the alley. Something was wrong.

He could feel it in his bones.
```

`brief.txt`:
```text
tone: mysterious
emotion: suspenseful
pacing: slow
```

Command:
```bash
talkaty generate script.md --brief brief.txt --voice narrator --pitch -2 --speed 0.85 --subtitles
```

Result: `script.mp3` + `script.srt` with a deep, slow, mysterious delivery.
