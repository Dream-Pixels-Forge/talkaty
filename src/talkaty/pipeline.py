"""Generation pipeline: parse → resolve voice → synthesize → write audio + subtitles."""

from __future__ import annotations

import os
from dataclasses import dataclass

from .audio import AudioResult, estimate_duration_ms, write_audio, write_srt
from .backends.base import TTSBackend
from .backends.edge_tts import EdgeTTS
from .script import parse_brief, parse_script
from .voices import resolve_persona


def _semitones_to_hz(semitones: float) -> str:
    """Convert semitone offset to edge-tts pitch string (e.g. '+50Hz')."""
    offset_hz = 440.0 * (2.0 ** (semitones / 12.0) - 1.0)
    sign = "+" if offset_hz >= 0 else "-"
    return f"{sign}{abs(offset_hz):.0f}Hz"


@dataclass
class GenerateOptions:
    script_path: str
    brief_path: str | None = None
    voice: str | None = None
    accent: str | None = None
    backend: str = "edge-tts"
    pitch: float = 0.0
    speed: float = 1.0
    output_path: str | None = None
    subtitles: bool = False
    model_path: str | None = None


async def run(opts: GenerateOptions) -> AudioResult:
    """Run the full generation pipeline."""
    segments = parse_script(opts.script_path)
    brief = parse_brief(opts.brief_path)

    # Brief-driven accent override; explicit --accent wins.
    # Default (None) keeps persona fallback (smooth female) instead of forcing US.
    accent = opts.accent or brief.get("accent")

    persona = resolve_persona(opts.voice, accent, opts.backend)

    piper_model_path: str | None = None
    backend: TTSBackend
    if opts.backend == "edge-tts":
        backend = EdgeTTS()
    elif opts.backend == "piper":
        piper_model_path = opts.model_path
        if not piper_model_path:
            raise ValueError("Piper backend requires --model PATH to a .onnx voice model")
        try:
            from .backends.piper import PiperTTS

            backend = PiperTTS(model_path=piper_model_path)
        except ImportError as exc:
            raise RuntimeError(
                f"Backend '{opts.backend}' unavailable. Install it with "
                "`pip install talkaty[piper]`."
            ) from exc
    else:
        try:
            from .backends.kittentts import KittenTTS

            backend = KittenTTS()
        except ImportError as exc:
            raise RuntimeError(
                f"Backend '{opts.backend}' unavailable. Install it or use edge-tts."
            ) from exc

    # Synthesize each segment and concatenate
    audio_parts: list[bytes] = []
    cursor_ms = 0
    for seg in segments:
        # Break segment: no audio, just advance the clock (tracked in SRT)
        if not seg.text.strip():
            cursor_ms += seg.break_ms
            continue

        # Piper uses its model voice; voice_id/pitch/speed are ignored
        if opts.backend == "piper":
            assert piper_model_path is not None  # narrowed by ValueError above
            tts_voice: str = piper_model_path
        else:
            tts_voice = persona.voice_id(opts.backend)
        # Per-segment pitch: global opts.pitch + seg.pitch (SSML <pitch>)
        seg_pitch = (opts.pitch or 0.0) + (seg.pitch or 0.0)
        # Emphasis: slight pitch boost
        if seg.emphasis:
            seg_pitch += 2.0

        part = await backend.synthesize(
            seg.text,
            tts_voice,
            pitch=_semitones_to_hz(seg_pitch),
            speed=opts.speed,
        )
        audio_parts.append(part)
        seg.start_ms = cursor_ms
        # estimate segment duration for subtitles
        seg.end_ms = cursor_ms + estimate_duration_ms([seg])
        cursor_ms = seg.end_ms

    audio_data = b"".join(audio_parts)
    duration_seconds = cursor_ms / 1000.0

    # Output path
    if opts.output_path:
        out_path = opts.output_path
    else:
        base = os.path.splitext(opts.script_path)[0]
        out_path = base + ".mp3"

    write_audio(out_path, audio_data, fmt="mp3")

    if opts.subtitles:
        srt_path = os.path.splitext(out_path)[0] + ".srt"
        write_srt(srt_path, segments)

    return AudioResult(
        path=os.path.abspath(out_path),
        duration_seconds=duration_seconds,
        voice_used=persona.id,
        backend_used=opts.backend,
    )
