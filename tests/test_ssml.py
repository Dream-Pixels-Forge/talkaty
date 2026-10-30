"""Tests for SSML-lite markup parsing in scripts."""

from talkaty.ssml import parse_ssml


def test_parse_ssml_plain_text():
    """Plain text with no tags returns one segment."""
    segs = parse_ssml("Hello world.")
    assert len(segs) == 1
    assert segs[0].text == "Hello world."
    assert segs[0].break_ms == 0
    assert segs[0].emphasis is False
    assert segs[0].pitch is None


def test_parse_ssml_break_tag():
    """<break time='1s'/> inserts a pause segment."""
    segs = parse_ssml("Hello.<break time='1000ms'/>World.")
    assert len(segs) == 3
    assert segs[0].text == "Hello."
    assert segs[1].break_ms == 1000
    assert segs[1].text == ""
    assert segs[2].text == "World."


def test_parse_ssml_break_seconds():
    """<break time='1s'/> parses seconds too."""
    segs = parse_ssml("A.<break time='1s'/>B.")
    pause = [s for s in segs if s.break_ms > 0]
    assert len(pause) == 1
    assert pause[0].break_ms == 1000


def test_parse_ssml_emphasis():
    """<emphasis> wraps text with emphasis flag."""
    segs = parse_ssml("Normal <emphasis>important</emphasis> text.")
    emph = [s for s in segs if s.emphasis]
    assert len(emph) == 1
    assert emph[0].text == "important"


def test_parse_ssml_pitch():
    """<pitch>N</pitch> sets pitch for following text."""
    segs = parse_ssml("Start <pitch>+2</pitch> higher end.")
    pitch_segs = [s for s in segs if s.pitch is not None]
    assert len(pitch_segs) == 1
    assert pitch_segs[0].pitch == 2.0


def test_parse_ssml_negative_pitch():
    """<pitch>-2</pitch> parses negative values."""
    segs = parse_ssml("<pitch>-2</pitch> deeper voice.")
    pitch_segs = [s for s in segs if s.pitch is not None]
    assert len(pitch_segs) == 1
    assert pitch_segs[0].pitch == -2.0


def test_parse_ssml_combined():
    """Multiple tags combined in one script."""
    segs = parse_ssml(
        "<pitch>+1</pitch>Hello.<break time='500ms'/> <emphasis>Listen</emphasis> now."
    )
    texts = [s.text for s in segs if s.text.strip()]
    assert "Hello." in texts
    assert "Listen" in texts
    assert "now." in texts
    breaks = [s for s in segs if s.break_ms > 0]
    assert len(breaks) == 1
    assert breaks[0].break_ms == 500
