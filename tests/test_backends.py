"""Tests for talkaty backends and voices."""

from talkaty.backends.edge_tts import EdgeTTS
from talkaty.voices import PERSONAS, resolve_persona, list_personas


def test_personas_non_empty():
    assert len(PERSONAS) == 5
    assert "smooth female" in PERSONAS
    assert "alpha male" in PERSONAS


def test_resolve_persona_defaults_to_smooth_female():
    p = resolve_persona(None, None)
    assert p.id == "smooth female"


def test_resolve_persona_by_accent():
    p = resolve_persona(None, "UK")
    assert p.accent == "UK"


def test_edge_tts_voice_count():
    voices = EdgeTTS().list_voices()
    assert len(voices) >= 1
