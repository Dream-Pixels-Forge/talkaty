"""Tests for script parsing."""

from talkaty.script import parse_brief, parse_script


def test_parse_script_splits_paragraphs():
    import os
    import tempfile

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
    import os
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
        fh.write("accent: Nigerian\ntone: energetic\n")
        path = fh.name
    try:
        hints = parse_brief(path)
        assert hints["accent"] == "NG"
        assert hints["tone"] == "energetic"
    finally:
        os.unlink(path)


def test_parse_brief_accent():
    """Brief mentioning accent keywords should extract an accent hint."""
    import os
    import tempfile

    cases = [
        ("Use a Nigerian accent for the narrator.", "NG"),
        ("The speaker has a British accent.", "UK"),
        ("Deliver in US English.", "US"),
        ("Australian accent preferred.", "AU"),
        ("Use a French accent.", "FR"),
        ("Read in Chinese.", "ZH"),
        ("Mandarin Chinese voice please.", "ZH"),
        ("Speak in Hindi.", "HI"),
        ("Spanish voice please.", "ES"),
        ("German accent preferred.", "DE"),
        ("Deep mystery documentary narrator voice.", None),
        ("No accent mentioned here.", None),
    ]
    for text, expected in cases:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
            fh.write(text)
            path = fh.name
        try:
            hints = parse_brief(path)
            if expected:
                assert hints.get("accent") == expected, (
                    f"expected {expected} for '{text}', got {hints.get('accent')}"
                )
            else:
                assert "accent" not in hints, (
                    f"expected no accent for '{text}', got {hints.get('accent')}"
                )
        finally:
            os.unlink(path)
