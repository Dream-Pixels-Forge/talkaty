"""Audio output: write MP3/WAV, compute duration, write SRT/VTT subtitles."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AudioResult:
    path: str
    duration_seconds: float
    voice_used: str
    backend_used: str


def write_audio(path: str, data: bytes, fmt: str = "mp3") -> str:
    """Write raw audio bytes to `path`. Returns the path written."""
    with open(path, "wb") as fh:
        fh.write(data)
    return path


def estimate_duration_ms(segments: list, words_per_minute: int = 150) -> int:
    """Rough duration estimate from segment text (fallback when backend doesn't report)."""
    total_chars = sum(len(seg.text) for seg in segments)
    # ~5 chars per word average
    words = total_chars / 5.0
    minutes = words / words_per_minute
    return int(minutes * 60 * 1000)


def write_srt(path: str, segments: list, start_ms: int = 0) -> str:
    """Write an SRT subtitle file from segments with start/end ms."""
    offset = start_ms
    with open(path, "w", encoding="utf-8") as fh:
        for i, seg in enumerate(segments, 1):
            start = offset + (seg.start_ms or 0)
            end = offset + (seg.end_ms or start + 2000)
            fh.write(f"{i}\n")
            fh.write(f"{_fmt_ts(start)} --> {_fmt_ts(end)}\n")
            fh.write(f"{seg.text}\n\n")
    return path


def write_vtt(path: str, segments: list, start_ms: int = 0) -> str:
    """Write a VTT subtitle file."""
    offset = start_ms
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("WEBVTT\n\n")
        for i, seg in enumerate(segments, 1):
            start = offset + (seg.start_ms or 0)
            end = offset + (seg.end_ms or start + 2000)
            fh.write(f"{i}\n")
            fh.write(f"{_fmt_vtt_ts(start)} --> {_fmt_vtt_ts(end)}\n")
            fh.write(f"{seg.text}\n\n")
    return path


def _fmt_ts(ms: int) -> str:
    total = ms // 1000
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{ms % 1000:03d}"


def _fmt_vtt_ts(ms: int) -> str:
    total = ms // 1000
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms % 1000:03d}"
