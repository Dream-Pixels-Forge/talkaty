"""edge-tts backend — Microsoft Edge TTS, free, 400+ voices, many accents."""

from __future__ import annotations

from talkaty.backends.base import TTSBackend, VoiceInfo


class EdgeTTS(TTSBackend):
    name = "edge-tts"

    async def synthesize(
        self,
        text: str,
        voice: str,
        pitch: float = 0.0,
        speed: float = 1.0,
    ) -> bytes:
        import edge_tts

        communicate = edge_tts.Communicate(
            text,
            voice,
            pitch=f"{pitch:+.0f}Hz",
            rate=f"{(speed - 1) * 100:+.0f}%",
        )
        chunks: list[bytes] = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        return b"".join(chunks)

    def list_voices(self) -> list[VoiceInfo]:
        import edge_tts

        voices = []
        # edge-tts.list_voices() is async
        import asyncio

        async def _fetch():
            return await edge_tts.list_voices()

        raw = asyncio.run(_fetch())
        for v in raw:
            voices.append(
                VoiceInfo(
                    id=v["ShortName"],
                    name=v.get("FriendlyName", v["ShortName"]),
                    accent=v.get("Locale", "")[:2].upper(),
                    gender=v.get("Gender", "unknown"),
                    backend="edge-tts",
                )
            )
        return voices
