"""Voice persona presets and accent → voice-id mapping."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    id: str
    description: str
    voice_id: str
    accent: str
    gender: str
    backend: str = "edge-tts"


PERSONAS: dict[str, Persona] = {
    "alpha male": Persona(
        id="alpha male",
        description="Bold, authoritative male voice",
        voice_id="en-US-GuyNeural",
        accent="US",
        gender="male",
    ),
    "smooth female": Persona(
        id="smooth female",
        description="Warm, friendly female voice",
        voice_id="en-US-JennyNeural",
        accent="US",
        gender="female",
    ),
    "warm narrator": Persona(
        id="warm narrator",
        description="Storytelling female voice",
        voice_id="en-GB-SoniaNeural",
        accent="UK",
        gender="female",
    ),
    "energetic": Persona(
        id="energetic",
        description="High-energy voice for ads/hype",
        voice_id="en-US-AriaNeural",
        accent="US",
        gender="female",
    ),
    "calm": Persona(
        id="calm",
        description="Calm male voice for meditation/ASMR",
        voice_id="en-AU-WilliamNeural",
        accent="AU",
        gender="male",
    ),
}

# Accent → list of persona ids that match
ACCENT_MAP: dict[str, list[str]] = {
    "US": ["alpha male", "smooth female", "energetic"],
    "UK": ["warm narrator"],
    "AU": ["calm"],
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
    return [p for p in PERSONAS.values() if p.backend == backend]
