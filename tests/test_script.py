"""Tests for script parsing."""

from talkaty.script import parse_script, parse_brief


def test_parse_script_splits_paragraphs():
    import tempfile, os

    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
        fh.write("# Title\n\nFirst paragraph.\n\nSecond paragraph.\n")
        path = fh.name
    try:
        segs = parse_script(path)
        assert len(segs) >= 2
        assert all(s.text for s in segs)
    finally:
        os.unlink(path)


def test_parse_brief():
    import tempfile, os

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
        fh.write("accent: Nigerian\ntone: energetic\n")
        path = fh.name
    try:
        hints = parse_brief(path)
        assert hints["accent"] == "Nigerian"
        assert hints["tone"] == "energetic"
    finally:
        os.unlink(path)
