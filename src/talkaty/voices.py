"""Voice persona presets and accent → voice-id mapping."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    id: str
    description: str
    voice_ids: dict[str, str]  # backend -> voice id
    accent: str
    gender: str
    backend: str = "edge-tts"

    def voice_id(self, backend: str | None = None) -> str:
        """Return the voice id for `backend`, falling back to default backend."""
        b = backend or self.backend
        return self.voice_ids.get(b, self.voice_ids[self.backend])


PERSONAS: dict[str, Persona] = {
    "alpha male": Persona(
        id="alpha male",
        description="Bold, authoritative male voice",
        voice_ids={"edge-tts": "en-US-GuyNeural", "kittentts": "expr-voice-2-m"},
        accent="US",
        gender="male",
    ),
    "smooth female": Persona(
        id="smooth female",
        description="Warm, friendly female voice",
        voice_ids={"edge-tts": "en-US-JennyNeural", "kittentts": "expr-voice-2-f"},
        accent="US",
        gender="female",
    ),
    "warm narrator": Persona(
        id="warm narrator",
        description="Storytelling female voice",
        voice_ids={"edge-tts": "en-GB-SoniaNeural", "kittentts": "expr-voice-2-f"},
        accent="UK",
        gender="female",
    ),
    "energetic": Persona(
        id="energetic",
        description="High-energy voice for ads/hype",
        voice_ids={"edge-tts": "en-US-AriaNeural", "kittentts": "expr-voice-2-f"},
        accent="US",
        gender="female",
    ),
    "calm": Persona(
        id="calm",
        description="Calm male voice for meditation/ASMR",
        voice_ids={"edge-tts": "en-AU-WilliamNeural", "kittentts": "expr-voice-2-m"},
        accent="AU",
        gender="male",
    ),
    "nigerian narrator": Persona(
        id="nigerian narrator",
        description="Nigerian English storytelling voice",
        voice_ids={"edge-tts": "en-NG-EzinneNeural", "kittentts": "expr-voice-2-f"},
        accent="NG",
        gender="female",
    ),
    "french narrator": Persona(
        id="french narrator",
        description="French storytelling voice",
        voice_ids={"edge-tts": "fr-FR-EloiseNeural", "kittentts": "expr-voice-2-f"},
        accent="FR",
        gender="female",
    ),
    "chinese narrator": Persona(
        id="chinese narrator",
        description="Mandarin Chinese storytelling voice",
        voice_ids={"edge-tts": "zh-CN-XiaoxiaoNeural", "kittentts": "expr-voice-2-f"},
        accent="ZH",
        gender="female",
    ),
}

# Accent → list of persona ids that match
ACCENT_MAP: dict[str, list[str]] = {
    "US": ["alpha male", "smooth female", "energetic"],
    "UK": ["warm narrator"],
    "AU": ["calm"],
    "NG": ["nigerian narrator"],
    "FR": ["french narrator"],
    "ZH": ["chinese narrator"],
}


def resolve_persona(persona: str | None, accent: str | None, backend: str = "edge-tts") -> Persona:
    """Resolve a (persona, accent) pair to a Persona, falling back sensibly."""
    if persona and persona in PERSONAS:
        return PERSONAS[persona]
    if accent and accent in ACCENT_MAP:
        return PERSONAS[ACCENT_MAP[accent][0]]
    return PERSONAS["smooth female"]


def list_personas() -> list[Persona]:
    return list(PERSONAS.values())


def list_voices(backend: str = "edge-tts") -> list[Persona]:
    return [p for p in PERSONAS.values() if backend in p.voice_ids]
