"""Tests for the generation pipeline."""

import asyncio
import os
import tempfile

from talkaty.pipeline import GenerateOptions, run
from talkaty.voices import PERSONAS


async def _run_brief(
    brief_text: str | None = None,
    accent: str | None = None,
    voice: str | None = None,
):
    with tempfile.TemporaryDirectory() as d:
        script = os.path.join(d, "script.md")
        with open(script, "w", encoding="utf-8") as fh:
            fh.write("# Test\n\nHello world.\n")
        brief = None
        if brief_text is not None:
            brief = os.path.join(d, "brief.txt")
            with open(brief, "w", encoding="utf-8") as fh:
                fh.write(brief_text)
        return await run(
            GenerateOptions(
                script_path=script,
                brief_path=brief,
                accent=accent,
                voice=voice,
            )
        )


def test_pipeline_auto_accent_from_brief_nigerian():
    """Brief mentioning 'Nigerian' auto-selects the NG voice without --accent."""
    result = asyncio.run(_run_brief("Use a Nigerian accent for the narrator."))
    assert result.voice_used == "nigerian narrator", (
        f"expected nigerian narrator, got {result.voice_used}"
    )


def test_pipeline_auto_accent_from_brief_french():
    """Brief mentioning 'French' auto-selects the French voice."""
    result = asyncio.run(_run_brief("Use a French accent."))
    assert result.voice_used == "french narrator", (
        f"expected french narrator, got {result.voice_used}"
    )


def test_pipeline_auto_accent_from_brief_chinese():
    """Brief mentioning 'Chinese' auto-selects the Chinese voice."""
    result = asyncio.run(_run_brief("Read in Chinese."))
    assert result.voice_used == "chinese narrator", (
        f"expected chinese narrator, got {result.voice_used}"
    )


def test_pipeline_explicit_narrator_voice():
    """Explicit --voice 'narrator' selects the deep mystery narrator."""
    result = asyncio.run(_run_brief(None, voice="narrator"))
    assert result.voice_used == "narrator", f"expected narrator, got {result.voice_used}"


def test_pipeline_explicit_deep_french_narrator_voice():
    """Explicit --voice 'deep french narrator' selects the deep French narrator."""
    result = asyncio.run(_run_brief(None, voice="deep french narrator"))
    assert result.voice_used == "deep french narrator", (
        f"expected deep french narrator, got {result.voice_used}"
    )


def test_pipeline_explicit_accent_wins_over_brief():
    """Explicit --accent overrides brief hint."""
    result = asyncio.run(_run_brief("Use a Nigerian accent.", accent="UK"))
    assert result.voice_used == "warm narrator", (
        f"expected warm narrator (UK), got {result.voice_used}"
    )


def test_pipeline_default_accent_us():
    """No brief and no --accent defaults to US (smooth female)."""
    result = asyncio.run(_run_brief(None))
    assert result.voice_used == "smooth female"


def test_all_personas_resolvable():
    """Every persona id resolves to itself via resolve_persona."""
    from talkaty.voices import resolve_persona

    for pid in PERSONAS:
        p = resolve_persona(pid, None, "edge-tts")
        assert p.id == pid
