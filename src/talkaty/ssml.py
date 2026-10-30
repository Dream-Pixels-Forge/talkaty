"""SSML-lite markup parsing for talkaty scripts.

Supported tags:
- <break time='Nms'/> or <break time='Ns'/> — pause in milliseconds
- <emphasis>text</emphasis> — emphasized spoken text
- <pitch>N</pitch> — set pitch (semitones) for all following text until
  another <pitch> tag; the number is consumed and not spoken
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SSMLSegment:
    """A single speakable segment with optional SSML controls."""

    text: str
    break_ms: int = 0
    emphasis: bool = False
    pitch: float | None = None


def parse_ssml(text: str) -> list[SSMLSegment]:
    """Parse SSML-lite markup into a list of SSMLSegment."""
    segments: list[SSMLSegment] = []
    emphasis = False
    pitch: float | None = None
    pending_text: list[str] = []

    def flush_text() -> None:
        nonlocal pending_text
        if not pending_text:
            return
        chunk = "".join(pending_text).strip()
        pending_text = []
        if not chunk:
            return
        for sentence in _split_sentences(chunk):
            sentence = sentence.strip()
            if sentence:
                segments.append(
                    SSMLSegment(
                        text=sentence,
                        break_ms=0,
                        emphasis=emphasis,
                        pitch=pitch,
                    )
                )

    token_pattern = re.compile(r"(<[^>]+>)|([^<]+)")
    tokens = list(token_pattern.finditer(text))
    i = 0
    while i < len(tokens):
        m = tokens[i]
        tag = m.group(1)
        plain = m.group(2)

        if tag:
            flush_text()
            tag_lower = tag.strip().lower()

            # <break time='Nms'/> or <break time='Ns'/>
            br = re.match(r"<break\s+time=['\"](\d+(?:\.\d+)?)(\w*)['\"]\s*/?>", tag_lower)
            if br:
                value = float(br.group(1))
                unit = br.group(2).lower()
                ms = value * 1000 if unit in ("s", "sec", "secs") else value
                segments.append(SSMLSegment(text="", break_ms=int(ms), emphasis=False, pitch=None))
                i += 1
                continue

            # <emphasis> / </emphasis>
            if tag_lower == "<emphasis>":
                emphasis = True
                i += 1
                continue
            if tag_lower == "</emphasis>":
                emphasis = False
                i += 1
                continue

            # <pitch> — opening tag; next plain token is the pitch value
            if tag_lower == "<pitch>":
                i += 1
                if i < len(tokens):
                    next_plain = (tokens[i].group(2) or "").strip()
                    try:
                        pitch = float(next_plain)
                    except ValueError:
                        pitch = None
                i += 1
                continue

            # </pitch> — no-op: pitch persists until another <pitch> tag
            if tag_lower == "</pitch>":
                i += 1
                continue

        if plain:
            pending_text.append(plain)
        i += 1

    flush_text()
    return segments


def _split_sentences(text: str) -> list[str]:
    """Split text on sentence boundaries (. ! ? followed by whitespace)."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p for p in parts if p.strip()]
