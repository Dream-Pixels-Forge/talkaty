"""Tests for audio output (SRT/VTT)."""

import os
import tempfile

from talkaty.audio import write_srt, write_vtt
from talkaty.script import Segment


def _make_segments():
    return [
        Segment(index=0, text="Hello world.", start_ms=0, end_ms=2000),
        Segment(index=1, text="This is a test.", start_ms=2000, end_ms=4500),
    ]


def test_write_srt_valid():
    segs = _make_segments()
    with tempfile.NamedTemporaryFile("w", suffix=".srt", delete=False) as fh:
        path = fh.name
    try:
        write_srt(path, segs)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert "1\n" in content
        assert "00:00:00,000 --> 00:00:02,000" in content
        assert "Hello world." in content
        assert "This is a test." in content
        # two entries
        assert content.count("\n\n") >= 1
    finally:
        if os.path.exists(path):
            os.unlink(path)


def test_write_vtt_valid():
    segs = _make_segments()
    with tempfile.NamedTemporaryFile("w", suffix=".vtt", delete=False) as fh:
        path = fh.name
    try:
        write_vtt(path, segs)
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
        assert content.startswith("WEBVTT")
        assert "00:00:00.000 --> 00:00:02.000" in content
    finally:
        if os.path.exists(path):
            os.unlink(path)
