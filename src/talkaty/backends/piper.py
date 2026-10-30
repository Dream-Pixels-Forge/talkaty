"""Piper TTS backend — local, offline TTS using .onnx voice models.

Each Piper model is a single voice. Provide the model path via --model.
"""

from __future__ import annotations

import io
import wave

from talkaty.backends.base import TTSBackend, VoiceInfo


class PiperTTS(TTSBackend):
    name = "piper"

    def __init__(self, model_path: str, config_path: str | None = None) -> None:
        try:
            from piper_tts import PiperVoice  # type: ignore
        except ImportError as exc:  # pragma: no cover - optional dep
            raise ImportError("piper-tts is not installed. `pip install talkaty[piper]`") from exc

        self.model_path = model_path
        self.config_path = config_path
        self._voice = PiperVoice.load(model_path, config_path)

    async def synthesize(
        self,
        text: str,
        voice: str,
        pitch: float | str = 0.0,
        speed: float = 1.0,
    ) -> bytes:
        """Synthesize `text` using the loaded Piper model.

        Piper does not support per-call pitch/speed adjustment; those
        controls are silently ignored for this backend.
        """

        buf = io.BytesIO()
        sample_rate = int(self._voice.config.sample_rate)
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            for audio_bytes in self._voice.synthesize_stream_raw(text):
                wf.writeframes(audio_bytes)
        buf.seek(0)
        return buf.getvalue()

    def list_voices(self) -> list[VoiceInfo]:
        return [
            VoiceInfo(
                id=self.model_path,
                name=self.model_path,
                accent="",
                gender="unknown",
                backend="piper",
            )
        ]
