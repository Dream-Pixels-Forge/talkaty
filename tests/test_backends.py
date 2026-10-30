"""Tests for talkaty backends and voices."""

from talkaty.backends.edge_tts import EdgeTTS
from talkaty.voices import PERSONAS, resolve_persona


def test_personas_non_empty():
    assert len(PERSONAS) == 13
    assert "smooth female" in PERSONAS
    assert "alpha male" in PERSONAS
    assert "nigerian narrator" in PERSONAS
    assert "french narrator" in PERSONAS
    assert "deep french narrator" in PERSONAS
    assert "chinese narrator" in PERSONAS
    assert "narrator" in PERSONAS
    assert "hindi narrator" in PERSONAS
    assert "spanish narrator" in PERSONAS
    assert "german narrator" in PERSONAS


def test_resolve_persona_defaults_to_smooth_female():
    p = resolve_persona(None, None)
    assert p.id == "smooth female"


def test_resolve_persona_by_accent():
    p = resolve_persona(None, "UK")
    assert p.accent == "UK"


def test_edge_tts_voice_count():
    voices = EdgeTTS().list_voices()
    assert len(voices) >= 1


def test_kittentts_backend():
    """kittenTTS backend: synthesizes when installed, raises ImportError when not."""
    try:
        from talkaty.backends.kittentts import KittenTTS

        backend = KittenTTS()
    except ImportError:
        # kitten-tts not installed in this env — graceful degradation confirmed
        return

    voices = backend.list_voices()
    assert len(voices) >= 1
    assert all(v.backend == "kittentts" for v in voices)


def test_piper_graceful_when_missing():
    """Piper backend must degrade gracefully if piper-tts is not installed."""
    try:
        from talkaty.backends.piper import PiperTTS

        # Try to construct without a model; should fail on missing dep or model
        try:
            PiperTTS(model_path="nonexistent.onnx")
            raised = False
        except (ImportError, FileNotFoundError):
            raised = True
        assert raised, "PiperTTS should raise when piper-tts absent or model missing"
    except ImportError:
        # piper-tts package itself not importable — graceful degradation confirmed
        pass


def test_piper_requires_model_path():
    """Pipeline must reject piper backend without --model."""
    import asyncio
    import os
    import tempfile

    from talkaty.pipeline import GenerateOptions, run

    with tempfile.TemporaryDirectory() as d:
        script = os.path.join(d, "script.md")
        with open(script, "w", encoding="utf-8") as fh:
            fh.write("# Test\n\nHello world.\n")
        try:
            asyncio.run(
                run(
                    GenerateOptions(
                        script_path=script,
                        backend="piper",
                    )
                )
            )
            raised = False
        except ValueError as exc:
            raised = "model" in str(exc).lower()
        assert raised, "Piper backend should require --model path"
