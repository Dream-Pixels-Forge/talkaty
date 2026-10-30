"""kittenTTS backend — small, local, offline TTS fallback."""

from __future__ import annotations

from talkaty.backends.base import TTSBackend, VoiceInfo


class KittenTTS(TTSBackend):
    name = "kittentts"

    def __init__(self) -> None:
        try:
            import kitten_tts  # type: ignore

            self._model = kitten_tts.KittenTTS()
        except ImportError as exc:  # pragma: no cover - optional dep
            raise ImportError(
                "kitten-tts is not installed. `pip install talkaty[kittentts]`"
            ) from exc

    async def synthesize(
        self,
        text: str,
        voice: str,
        pitch: float = 0.0,
        speed: float = 1.0,
    ) -> bytes:
        import io

        import soundfile as sf  # type: ignore

        audio = self._model.generate(text, voice=voice, speed=speed)
        buf = io.BytesIO()
        sf.write(buf, audio, 24000, format="WAV")
        return buf.getvalue()

    def list_voices(self) -> list[VoiceInfo]:
        # kittenTTS exposes a small fixed voice set
        return [
            VoiceInfo(
                id="expr-voice-2-f",
                name="Expressive Female",
                accent="US",
                gender="female",
                backend="kittentts",
            ),
            VoiceInfo(
                id="expr-voice-2-m",
                name="Expressive Male",
                accent="US",
                gender="male",
                backend="kittentts",
            ),
        ]
