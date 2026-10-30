"""Parse script.md (+ optional brief.txt) into speakable segments."""

from dataclasses import dataclass


@dataclass
class Segment:
    index: int
    text: str
    start_ms: int = 0
    end_ms: int = 0


def parse_script(path: str) -> list[Segment]:
    """Read a markdown script and split into speakable segments.

    Splits on blank lines (paragraphs) and sentence boundaries so each
    segment is a natural breath group for TTS.
    """
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()

    # Strip markdown headings markers but keep the text
    lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            stripped = stripped.lstrip("#").strip()
        if stripped:
            lines.append(stripped)

    text = "\n".join(lines)

    # Split into paragraphs on blank lines
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    segments: list[Segment] = []
    idx = 0
    for para in paragraphs:
        # Further split long paragraphs on sentence boundaries
        sentences = _split_sentences(para)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                segments.append(Segment(index=idx, text=sentence))
                idx += 1

    return segments


def _split_sentences(text: str) -> list[str]:
    import re

    # crude sentence split on . ! ? followed by space/newline
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p for p in parts if p.strip()]


def parse_brief(path: str | None) -> dict[str, str]:
    """Read an optional brief file and return hints (accent, tone, ...)."""
    if not path:
        return {}
    hints: dict[str, str] = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, val = line.split(":", 1)
                hints[key.strip().lower()] = val.strip()
            else:
                hints["note"] = hints.get("note", "") + " " + line
    return hints
