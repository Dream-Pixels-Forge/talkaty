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


def _normalize_accent(value: str) -> str | None:
    """Normalize an accent string to a code (NG, UK, AU, US, FR, ZH, HI, ES, DE) or None."""
    import re

    lowered = value.lower()
    if re.search(r"nigerian|nigeria", lowered):
        return "NG"
    if re.search(r"french|france", lowered):
        return "FR"
    if re.search(r"chinese|china|mandarin", lowered):
        return "ZH"
    if re.search(r"hindi|india", lowered):
        return "HI"
    if re.search(r"spanish|spain|espa.ol", lowered):
        return "ES"
    if re.search(r"german|deutschland|deutsch", lowered):
        return "DE"
    if re.search(r"british|\buk\b", lowered) and "nigerian" not in lowered:
        return "UK"
    if re.search(r"australian|\bau\b", lowered):
        return "AU"
    if re.search(r"\bus\b|american", lowered):
        return "US"
    return None


def _detect_accent(text: str) -> str | None:
    """Detect accent from free text. Returns accent code or None."""
    import re

    lowered = text.lower()
    patterns = {
        "NG": [r"nigerian"],
        "FR": [r"french", r"france"],
        "ZH": [r"chinese", r"china", r"mandarin"],
        "HI": [r"hindi", r"india"],
        "ES": [r"spanish", r"spain", r"espa.ol"],
        "DE": [r"german", r"deutschland", r"deutsch"],
        "UK": [r"british", r"\buk\b"],
        "AU": [r"australian", r"\bau\b"],
        "US": [r"\bus\b", r"american"],
    }
    for accent, pats in patterns.items():
        for pat in pats:
            if re.search(pat, lowered):
                return accent
    return None


def parse_brief(path: str | None) -> dict[str, str]:
    """Read an optional brief file and return hints (accent, tone, ...).

    Scans both ``key: value`` pairs and free text for accent hints
    (e.g. "Nigerian accent", "British", "US English").
    """
    if not path:
        return {}
    hints: dict[str, str] = {}
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            hints[key.strip().lower()] = val.strip()
        else:
            hints["note"] = hints.get("note", "") + " " + line
    # Normalize the accent hint to a code (NG, UK, AU, US).
    raw_accent = hints.get("accent")
    if raw_accent:
        normalized = _normalize_accent(raw_accent)
        if normalized:
            hints["accent"] = normalized
        else:
            hints.pop("accent", None)
    # Scan free text for accent keywords when no usable accent key.
    if "accent" not in hints:
        detected = _detect_accent(raw)
        if detected:
            hints["accent"] = detected
    return hints
