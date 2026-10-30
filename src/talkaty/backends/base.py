"""Abstract base class for TTS backends."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class VoiceInfo:
    id: str
    name: str
    accent: str
    gender: str
    backend: str


class TTSBackend(ABC):
    """A TTS backend turns text + voice controls into audio bytes."""

    name: str

    @abstractmethod
    async def synthesize(
        self,
        text: str,
        voice: str,
        pitch: float | str = 0.0,
        speed: float = 1.0,
    ) -> bytes:
        """Synthesize `text` with `voice`, returning audio bytes (MP3)."""

    @abstractmethod
    def list_voices(self) -> list[VoiceInfo]:
        """List available voices for this backend."""
