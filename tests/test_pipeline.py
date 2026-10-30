"""Tests for the generation pipeline."""

import os
import tempfile

from talkaty.pipeline import GenerateOptions, run


async def _run_brief(brief_text: str, accent: str | None = None):
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
            )
        )


def test_pipeline_auto_accent_from_brief_nigerian():
    """Brief mentioning 'Nigerian' auto-selects the NG voice without --accent."""
    import asyncio

    result = asyncio.run(_run_brief("Use a Nigerian accent for the narrator.", accent=None))
    assert result.voice_used == "nigerian narrator", (
        f"expected nigerian narrator, got {result.voice_used}"
    )


def test_pipeline_auto_accent_from_brief_french():
    """Brief mentioning 'French' auto-selects the French voice."""
    import asyncio

    result = asyncio.run(_run_brief("Use a French accent.", accent=None))
    assert result.voice_used == "french narrator", (
        f"expected french narrator, got {result.voice_used}"
    )


def test_pipeline_auto_accent_from_brief_chinese():
    """Brief mentioning 'Chinese' auto-selects the Chinese voice."""
    import asyncio

    result = asyncio.run(_run_brief("Read in Chinese.", accent=None))
    assert result.voice_used == "chinese narrator", (
        f"expected chinese narrator, got {result.voice_used}"
    )


def test_pipeline_explicit_accent_wins_over_brief():
    """Explicit --accent overrides brief hint."""
    import asyncio

    result = asyncio.run(_run_brief("Use a Nigerian accent.", accent="UK"))
    assert result.voice_used == "warm narrator", (
        f"expected warm narrator (UK), got {result.voice_used}"
    )


def test_pipeline_default_accent_us():
    """No brief and no --accent defaults to US (smooth female)."""
    import asyncio

    result = asyncio.run(_run_brief(None, accent=None))
    assert result.voice_used == "smooth female"
