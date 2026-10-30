"""Tests for batch mode."""

import os
import tempfile

from typer.testing import CliRunner

from talkaty.cli import app


def test_batch_creates_one_output_per_input():
    runner = CliRunner()
    with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as out_dir:
        # create 3 script.md files
        for name in ["a.md", "b.md", "c.md"]:
            with open(os.path.join(src_dir, name), "w", encoding="utf-8") as fh:
                fh.write(f"# {name}\n\nTest content for {name}.\n")
        result = runner.invoke(
            app,
            ["batch", src_dir, out_dir, "--voice", "smooth female"],
        )
        # batch calls edge-tts over network; may fail in CI without network.
        # Assert it attempts each file (exit code reflects attempts, not network).
        assert result.exit_code == 0
        # At minimum the command ran without crashing.
        outputs = [f for f in os.listdir(out_dir) if f.endswith(".mp3")]
        assert len(outputs) == 3, f"expected 3 outputs, got {len(outputs)}: {outputs}"
