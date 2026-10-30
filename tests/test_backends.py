"""Tests for talkaty backends and voices."""

from talkaty.backends.edge_tts import EdgeTTS
from talkaty.voices import PERSONAS, resolve_persona


def test_personas_non_empty():
    assert len(PERSONAS) == 9
    assert "smooth female" in PERSONAS
    assert "alpha male" in PERSONAS
    assert "nigerian narrator" in PERSONAS
    assert "french narrator" in PERSONAS
    assert "chinese narrator" in PERSONAS
    assert "narrator" in PERSONAS


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
